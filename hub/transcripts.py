"""Transcript fetching: youtube-transcript-api first, yt-dlp auto-captions as fallback.

Transcripts are cached in .cache/transcripts/ (gitignored) and are never committed or published.
Failures never raise: they return None, and the caller marks the video `transcript_missing`.
"""
from __future__ import annotations

import json
import logging
import os
import re
import tempfile
from pathlib import Path

log = logging.getLogger(__name__)

# Optional: route transcript requests through a proxy when GitHub runner IPs are blocked.
PROXY_ENV = "TRANSCRIPT_PROXY_URL"


def _proxy() -> str | None:
    return os.environ.get(PROXY_ENV) or None


def fetch_via_transcript_api(video_id: str) -> list[dict] | None:
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api.proxies import GenericProxyConfig

        proxy = _proxy()
        api = YouTubeTranscriptApi(
            proxy_config=GenericProxyConfig(http_url=proxy, https_url=proxy) if proxy else None
        )
        fetched = api.fetch(video_id, languages=("en", "en-US", "en-GB"))
        segs = [{"start": float(s.start), "text": s.text} for s in fetched]
        return segs or None
    except Exception as e:  # noqa: BLE001 - library raises many types; all mean "not available"
        log.warning("transcript-api failed for %s: %s", video_id, type(e).__name__)
        return None


def parse_json3(data: dict) -> list[dict]:
    segs = []
    for ev in data.get("events", []):
        text = "".join(s.get("utf8", "") for s in ev.get("segs", []) or []).strip()
        if text:
            segs.append({"start": ev.get("tStartMs", 0) / 1000.0, "text": text})
    return segs


_VTT_TS = re.compile(r"(\d+):(\d{2}):(\d{2})[.,](\d{3})\s+-->")


def parse_vtt(text: str) -> list[dict]:
    segs, start, buf = [], None, []
    for line in text.splitlines():
        m = _VTT_TS.match(line)
        if m:
            if start is not None and buf:
                segs.append({"start": start, "text": " ".join(buf)})
            h, mi, s, ms = map(int, m.groups())
            start, buf = h * 3600 + mi * 60 + s + ms / 1000, []
        elif line.strip() and start is not None and not line.startswith(("WEBVTT", "Kind:", "Language:")):
            buf.append(re.sub(r"<[^>]+>", "", line).strip())
    if start is not None and buf:
        segs.append({"start": start, "text": " ".join(buf)})
    # Auto-captions repeat rolling lines; drop consecutive duplicates.
    out = []
    for s in segs:
        if not out or s["text"] != out[-1]["text"]:
            out.append(s)
    return out


def fetch_via_ytdlp(video_id: str) -> list[dict] | None:
    try:
        import yt_dlp

        with tempfile.TemporaryDirectory() as tmp:
            opts = {
                "skip_download": True,
                "writesubtitles": True,
                "writeautomaticsub": True,
                "subtitleslangs": ["en", "en-US", "en-orig", "en.*"],
                "subtitlesformat": "json3/vtt/best",
                "outtmpl": str(Path(tmp) / "%(id)s.%(ext)s"),
                "quiet": True,
                "no_warnings": True,
            }
            if _proxy():
                opts["proxy"] = _proxy()
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
            files = sorted(Path(tmp).glob(f"{video_id}*"))
            for f in files:
                if f.suffix == ".json3":
                    segs = parse_json3(json.loads(f.read_text(encoding="utf-8")))
                elif f.suffix == ".vtt":
                    segs = parse_vtt(f.read_text(encoding="utf-8"))
                else:
                    continue
                if segs:
                    return segs
        return None
    except Exception as e:  # noqa: BLE001
        log.warning("yt-dlp captions failed for %s: %s", video_id, type(e).__name__)
        return None


def get_transcript(video_id: str, cache_dir: Path) -> tuple[list[dict] | None, str]:
    """Return (segments, source). Source is 'cache', 'transcript-api', 'yt-dlp' or 'missing'."""
    cache_file = cache_dir / f"{video_id}.json"
    if cache_file.exists():
        return json.loads(cache_file.read_text(encoding="utf-8")), "cache"
    for source, fn in (("transcript-api", fetch_via_transcript_api), ("yt-dlp", fetch_via_ytdlp)):
        segs = fn(video_id)
        if segs:
            cache_dir.mkdir(parents=True, exist_ok=True)
            cache_file.write_text(json.dumps(segs, ensure_ascii=False), encoding="utf-8")
            return segs, source
    return None, "missing"


def fmt_ts(seconds: float) -> str:
    s = int(seconds)
    h, rem = divmod(s, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def to_prompt_text(segs: list[dict], window: float = 30.0) -> str:
    """Compact transcript: one line per ~30s window, prefixed with [m:ss] so Claude can cite timestamps."""
    lines, cur_start, buf = [], None, []
    for s in segs:
        if cur_start is None:
            cur_start = s["start"]
        if s["start"] - cur_start >= window and buf:
            lines.append(f"[{fmt_ts(cur_start)}] {' '.join(buf)}")
            cur_start, buf = s["start"], []
        buf.append(s["text"].replace("\n", " ").strip())
    if buf:
        lines.append(f"[{fmt_ts(cur_start or 0)}] {' '.join(buf)}")
    return "\n".join(lines)
