"""Build the static dashboard into an output folder (data.json + static files + images).

Only summaries, insights, short notes and links are published. Transcripts are never read here.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from .config import Config
from .reconcile import video_status
from .store import Store, iso_week, parse_date, read_json, utcnow, write_json


def build_site(cfg: Config, out: Path) -> Path:
    store = Store(cfg.paths.data)
    out.mkdir(parents=True, exist_ok=True)
    for f in cfg.paths.site_src.iterdir():
        if f.is_file():
            shutil.copy2(f, out / f.name)
    for sub in ("thumbs", "frames"):
        src = cfg.paths.assets / sub
        if src.exists():
            shutil.copytree(src, out / "assets" / sub, dirs_exist_ok=True)

    videos = []
    for v in store.videos.values():
        if v.get("status") != "analyzed":
            continue
        a = v.get("analysis", {})
        videos.append({
            "id": v["id"], "title": v["title"], "channel": v["channel"], "url": v["url"],
            "published": v["published_at"][:10], "week": iso_week(parse_date(v["published_at"])),
            "duration_s": v["duration_s"], "topics": v.get("topics", []), "relevance": v.get("relevance"),
            "status": video_status(store, v["id"]), "summary": a.get("summary", ""),
            "applies": a.get("applies_to_work", ""), "relevance_reason": a.get("relevance_reason", ""),
            "tools": a.get("tools_mentioned", []), "moments": a.get("best_moments", []),
            "thumb": f"assets/thumbs/{v['thumbnail']}" if v.get("thumbnail") else "",
            "frames": [f"assets/frames/{f}" for f in v.get("keyframes", [])],
            "analyzed_at": v.get("analyzed_at", ""),
        })
    insights = [{k: i.get(k) for k in ("id", "video_id", "text", "facts", "topics", "date", "first_seen", "status",
                                       "superseded_by", "status_reason", "status_changed", "last_reinforced")}
                for i in store.insights.values()]
    topics = [{**t, **store.topics_state.get(t["slug"], {})} for t in cfg.topics]
    digests = []
    if cfg.paths.digests.exists():
        for f in sorted(cfg.paths.digests.glob("*.md"), reverse=True):
            digests.append({"week": f.stem, "markdown": f.read_text(encoding="utf-8")})

    write_json(out / "data.json", {
        "title": cfg.setting("site.title", "AI Video Knowledge Hub"),
        "generated": utcnow().isoformat(timespec="minutes"),
        "last_run": (read_json(cfg.paths.data / "state.json", {}) or {}).get("last_run", {}),
        "topics": topics, "proposed_topics": cfg.proposed_topics,
        "videos": sorted(videos, key=lambda v: v["published"], reverse=True),
        "insights": sorted(insights, key=lambda i: i["id"]),
        "changelog": list(reversed(store.changelog)),
        "digests": digests,
    })
    (out / ".nojekyll").write_text("")
    return out
