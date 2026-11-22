"""Thumbnails and optional keyframes, saved as small webp images (under max_kb)."""
from __future__ import annotations

import io
import logging
import shutil
import subprocess
import tempfile
from pathlib import Path

import requests
from PIL import Image

log = logging.getLogger(__name__)


def save_webp(img: Image.Image, dest: Path, width: int, max_kb: int) -> bool:
    img = img.convert("RGB")
    if img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    for quality in (80, 70, 60, 50, 40, 30):
        buf = io.BytesIO()
        img.save(buf, "WEBP", quality=quality, method=6)
        if buf.tell() <= max_kb * 1024:
            dest.write_bytes(buf.getvalue())
            return True
    log.warning("Could not get %s under %d KB", dest.name, max_kb)
    return False


def download_thumbnail(url: str, dest: Path, width: int = 480, max_kb: int = 150) -> bool:
    if dest.exists():
        return True
    if not url:
        return False
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return save_webp(Image.open(io.BytesIO(resp.content)), dest, width, max_kb)
    except Exception as e:  # noqa: BLE001
        log.warning("thumbnail failed for %s: %s", dest.stem, e)
        return False


def slides_likely(title: str, description: str, keywords: list[str]) -> bool:
    text = f"{title} {description}".lower()
    return any(k.lower() in text for k in keywords)


def extract_keyframes(video_id: str, seconds: list[int], dest_dir: Path, width: int = 640,
                      max_kb: int = 150) -> list[str]:
    """Download a low-res copy with yt-dlp and grab frames at the given timestamps with ffmpeg.

    Returns the relative filenames written. Any failure returns what was written so far.
    """
    if not seconds or not shutil.which("ffmpeg"):
        return []
    written: list[str] = []
    try:
        import yt_dlp

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "v.mp4"
            opts = {"format": "worst[ext=mp4][height>=360]/worst[ext=mp4]/worst", "outtmpl": str(out),
                    "quiet": True, "no_warnings": True}
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
            src = next(Path(tmp).glob("v.*"), None)
            if not src:
                return []
            for n, t in enumerate(seconds, 1):
                png = Path(tmp) / f"f{n}.png"
                subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(t), "-i", str(src), "-frames:v", "1",
                                str(png)], check=True, timeout=120)
                name = f"{video_id}-{n}.webp"
                if save_webp(Image.open(png), dest_dir / name, width, max_kb):
                    written.append(name)
    except Exception as e:  # noqa: BLE001
        log.warning("keyframes failed for %s: %s", video_id, e)
    return written
