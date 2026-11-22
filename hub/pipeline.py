"""Weekly pipeline: fetch -> transcripts -> analyse -> reconcile -> freshness -> render -> digest."""
from __future__ import annotations

import logging

import requests
from datetime import date, datetime, timedelta

from . import visuals
from .analyze import analyze_video, slugify
from .config import Config, add_proposed_topics
from .digest import build_digest
from .llm import JSONModel, LLMError
from .reconcile import apply_freshness, reconcile_topic
from .render import render_all
from .store import Store, iso_week, parse_dt, utcnow
from .transcripts import get_transcript
from .youtube import Getter, YouTubeError, list_uploads_since, resolve_channel, video_details

log = logging.getLogger(__name__)


def fetch_new_videos(cfg: Config, store: Store, get: Getter, since: datetime) -> dict:
    """Add newly published videos to the store. Returns counts and per-channel errors."""
    min_dur = int(cfg.setting("fetch.min_duration_seconds", 180))
    resolved = store.state.setdefault("channels", {})
    added, short, errors = 0, 0, []
    for ch in cfg.channels:
        key = ch.get("channel_id") or ch.get("handle")
        try:
            info = resolved.get(ch["name"])
            if not info or info.get("key") != key:
                info = {**resolve_channel(get, ch), "key": key}
                resolved[ch["name"]] = info
                log.info("resolved %s -> %s (%s)", ch["name"], info["channel_id"], info["title"])
            ids = [i for i in list_uploads_since(get, info["uploads"], since) if i not in store.videos]
            for d in video_details(get, ids):
                if d["live"] in ("live", "upcoming"):
                    continue  # pick up once the stream has finished
                status = "skipped_short" if d["duration_s"] < min_dur else "pending"
                short += status == "skipped_short"
                added += status == "pending"
                store.videos[d["id"]] = {
                    "id": d["id"], "title": d["title"], "channel": ch["name"], "channel_id": d["channel_id"],
                    "published_at": d["published_at"], "duration_s": d["duration_s"], "url": d["url"],
                    "description": d["description"], "thumbnail_url": d["thumbnail_url"], "status": status,
                    "discovered_at": utcnow().date().isoformat(), "transcript_attempts": 0,
                }
        except (YouTubeError, KeyError, requests.RequestException) as e:
            log.error("channel %s failed: %s", ch.get("name"), e)
            errors.append(f"{ch.get('name')}: {e}")
    return {"added": added, "skipped_short": short, "errors": errors}


def process_videos(cfg: Config, store: Store, llm: JSONModel, today: date, max_videos: int) -> dict:
    """Transcripts + analysis for pending videos, newest first, up to the cap."""
    max_attempts = int(cfg.setting("analysis.max_transcript_attempts", 4))
    vis = cfg.settings.get("visuals", {}) or {}
    kf = vis.get("keyframes", {}) or {}
    queue = sorted((v for v in store.videos.values() if v["status"] in ("pending", "transcript_missing", "failed")),
                   key=lambda v: v["published_at"], reverse=True)
    analyzed, missing, failed, proposed = [], 0, 0, []
    new_insight_ids: set[str] = set()
    for v in queue:
        if len(analyzed) >= max_videos:
            break
        segs, source = get_transcript(v["id"], cfg.paths.transcripts)
        if not segs:
            v["transcript_attempts"] = v.get("transcript_attempts", 0) + 1
            v["status"] = "transcript_unavailable" if v["transcript_attempts"] >= max_attempts else "transcript_missing"
            missing += 1
            continue
        try:
            a = analyze_video(cfg, llm, v, segs)
        except LLMError as e:
            v["status"], v["error"] = "failed", str(e)
            v["transcript_attempts"] = v.get("transcript_attempts", 0) + 1
            if v["transcript_attempts"] >= max_attempts:
                v["status"] = "analysis_unavailable"
            failed += 1
            log.error("analysis failed for %s: %s", v["id"], e)
            continue

        day = today.isoformat()
        v.pop("error", None)
        v.update(
            status="analyzed", analyzed_at=day, transcript_source=source, topics=a["topics"],
            relevance=a["relevance"], file=f"{v['published_at'][:10]}-{slugify(v['title'])}",
            analysis={k: a[k] for k in ("summary", "relevance_reason", "tools_mentioned", "applies_to_work",
                                        "best_moments", "has_visual_content")},
        )
        for n, ins in enumerate(a["insights"], 1):
            iid = f"{v['id']}-{n}"
            store.insights[iid] = {
                "id": iid, "video_id": v["id"], "text": ins["text"].strip(), "facts": ins.get("facts", []),
                "topics": ins["topics"] or a["topics"][:1], "date": v["published_at"][:10], "first_seen": day,
                "last_reinforced": v["published_at"][:10], "status": "active",
            }
            new_insight_ids.add(iid)
        for p in a.get("proposed_topics", []):
            proposed.append({**p, "first_seen_in": v["id"]})

        thumb = f"{v['id']}.webp"
        if visuals.download_thumbnail(v.get("thumbnail_url", ""), cfg.paths.assets / "thumbs" / thumb,
                                      int(vis.get("thumbnail_width", 480)), int(vis.get("max_kb", 150))):
            v["thumbnail"] = thumb
        if kf.get("enabled") and (a["has_visual_content"] or
                                  visuals.slides_likely(v["title"], v.get("description", ""), kf.get("keywords", []))):
            secs = [m["seconds"] for m in a["best_moments"]][: int(kf.get("max_frames", 4))]
            frames = visuals.extract_keyframes(v["id"], secs, cfg.paths.assets / "frames",
                                               max_kb=int(vis.get("max_kb", 150)))
            if frames:
                v["keyframes"] = frames
        analyzed.append(v["id"])
        log.info("analyzed %s: %s (%d insights)", v["id"], v["title"], len(a["insights"]))

    added_topics = add_proposed_topics(cfg, proposed)
    pending_left = sum(v["status"] in ("pending", "transcript_missing", "failed") for v in store.videos.values())
    return {"analyzed": analyzed, "transcript_missing": missing, "failed": failed,
            "new_insight_ids": new_insight_ids, "proposed_topics": [p["slug"] for p in added_topics],
            "pending_left": pending_left}


def run(cfg: Config, *, get: Getter | None, llm: JSONModel, today: date | None = None,
        backfill_days: int | None = None, max_videos: int | None = None, repo_url: str = "",
        fetch: bool = True, now: datetime | None = None) -> dict:
    now = now or utcnow()
    today = today or now.date()
    store = Store(cfg.paths.data)

    last = store.state.get("last_success_run")
    if backfill_days is not None or not last:
        since = now - timedelta(days=backfill_days or int(cfg.setting("fetch.backfill_days", 30)))
    else:
        since = parse_dt(last) - timedelta(hours=int(cfg.setting("fetch.overlap_hours", 24)))

    fetched = {"added": 0, "skipped_short": 0, "errors": []}
    if fetch and get is not None:
        fetched = fetch_new_videos(cfg, store, get, since)
        store.save()  # keep discovered IDs even if a later step fails

    cap = max_videos if max_videos is not None else int(cfg.setting("analysis.max_videos_per_run", 40))
    proc = process_videos(cfg, store, llm, today, cap)
    store.save()

    # Freshness first so stale/archived status is current, then reconcile every touched topic.
    fresh = apply_freshness(cfg, store, today)
    touched = set()
    for iid in proc["new_insight_ids"] | set(fresh["stale"]) | set(fresh["archived"]):
        touched.update(store.insights[iid].get("topics", []))
    totals = {"superseded": 0, "reinforced": 0}
    for slug in sorted(t for t in touched if t in cfg.topic_slugs):
        try:
            c = reconcile_topic(cfg, llm, store, slug, proc["new_insight_ids"], today)
            totals = {k: totals[k] + c[k] for k in totals}
        except LLMError as e:
            log.error("reconcile %s failed: %s", slug, e)
    store.save()

    render_all(cfg, store)
    try:
        digest_path, digest_title = build_digest(cfg, llm, store, today, repo_url=repo_url)
    except LLMError as e:
        log.error("digest call failed, writing a digest without the summary: %s", e)
        digest_path, digest_title = build_digest(cfg, None, store, today, repo_url=repo_url)

    summary = {
        "week": iso_week(today),
        "date": today.isoformat(),
        "since": since.isoformat(),
        "new_videos_found": fetched["added"],
        "skipped_short": fetched["skipped_short"],
        "analyzed": len(proc["analyzed"]),
        "new_insights": len(proc["new_insight_ids"]),
        "transcript_missing": proc["transcript_missing"],
        "failed": proc["failed"],
        "pending_left": proc["pending_left"],
        "superseded": totals["superseded"],
        "reinforced": totals["reinforced"],
        "stale": len(fresh["stale"]),
        "archived": len(fresh["archived"]),
        "proposed_topics": proc["proposed_topics"],
        "channel_errors": fetched["errors"],
        "digest": digest_path,
        "digest_title": digest_title,
        "llm_usage": getattr(llm, "usage", {}),
    }
    summary["commit_message"] = (f"weekly update {summary['week']}: {summary['analyzed']} new, "
                                 f"{summary['superseded']} superseded")
    if summary["stale"] or summary["archived"]:
        summary["commit_message"] += f", {summary['stale']} stale, {summary['archived']} archived"
    # A run with a total fetch failure (every channel errored) doesn't advance the window.
    if not fetch or len(fetched["errors"]) < len(cfg.channels):
        store.state["last_success_run"] = now.isoformat()
    store.state["last_run"] = summary
    store.save()
    return summary
