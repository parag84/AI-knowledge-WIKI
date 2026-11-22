"""Reconciliation (supersede / reinforce via Claude) and deterministic freshness (stale / archive)."""
from __future__ import annotations

import json
import logging
from datetime import date

from .analyze import profile_text
from .config import Config
from .llm import JSONModel, render_prompt
from .store import Store, parse_date

log = logging.getLogger(__name__)

LIVE = ("active", "stale")

RECONCILE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["decisions", "synthesis", "open_questions"],
    "properties": {
        "decisions": {
            "type": "array",
            "items": {
                "type": "object", "additionalProperties": False,
                "required": ["action", "old_id", "new_id", "reason"],
                "properties": {
                    "action": {"type": "string", "enum": ["supersede", "reinforce"]},
                    "old_id": {"type": "string"},
                    "new_id": {"type": "string"},
                    "reason": {"type": "string"},
                },
            },
        },
        "synthesis": {"type": "string"},
        "open_questions": {"type": "array", "items": {"type": "string"}},
    },
}


def _brief(i: dict) -> dict:
    return {"id": i["id"], "date": i["date"], "status": i["status"], "text": i["text"], "facts": i.get("facts", [])}


def reconcile_topic(cfg: Config, llm: JSONModel, store: Store, slug: str, new_ids: set[str], today: date) -> dict:
    """Run one reconciliation call for a topic and apply its decisions. Returns counts."""
    topic = next((t for t in cfg.topics if t["slug"] == slug), {"slug": slug, "name": slug})
    live = store.insights_for_topic(slug, LIVE)
    new = [i for i in live if i["id"] in new_ids]
    existing = [i for i in live if i["id"] not in new_ids]
    counts = {"superseded": 0, "reinforced": 0}
    if not live:
        store.topics_state[slug] = {
            "synthesis": "", "open_questions": [], "updated": today.isoformat(),
        }
        return counts

    system = render_prompt(cfg.paths.prompts / "topic_reconciliation.md", profile=profile_text(cfg))
    user = (
        f"Topic: {topic['name']} (`{slug}`): {topic.get('description', '')}\n"
        f"Today: {today.isoformat()}\n\n"
        f"Existing insights:\n{json.dumps([_brief(i) for i in existing], ensure_ascii=False, indent=1)}\n\n"
        f"New insights this week:\n{json.dumps([_brief(i) for i in new], ensure_ascii=False, indent=1)}"
    )
    result = llm.call_json(system=system, user=user, schema=RECONCILE_SCHEMA)

    day = today.isoformat()
    known_new = {i["id"] for i in new}
    known_old = {i["id"] for i in existing}
    for d in result.get("decisions", []):
        old, newer = store.insights.get(d["old_id"]), store.insights.get(d["new_id"])
        # Only accept decisions about IDs we sent, old -> new, and never on already-final insights.
        # Two new videos in the same run may also supersede each other (older publish date loses).
        if (not old or not newer or d["old_id"] == d["new_id"] or d["new_id"] not in known_new
                or d["old_id"] not in (known_old | known_new) or old["date"] > newer["date"]):
            log.info("ignoring invalid decision: %s", d)
            continue
        if old["status"] not in LIVE:
            continue
        reason = d["reason"].strip().replace("\n", " ")
        if d["action"] == "supersede":
            old.update(status="superseded", superseded_by=newer["id"], status_changed=day, status_reason=reason)
            store.log(day=day, action="superseded", insight_id=old["id"], replaced_by=newer["id"],
                      reason=reason, topic=slug)
            counts["superseded"] += 1
        else:
            was_stale = old["status"] == "stale"
            old["last_reinforced"] = max(old.get("last_reinforced", old["date"]), newer["date"])
            old.setdefault("reinforced_by", [])
            if newer["id"] not in old["reinforced_by"]:
                old["reinforced_by"].append(newer["id"])
            if was_stale:
                old.update(status="active", status_changed=day, status_reason=f"reinforced: {reason}")
                store.log(day=day, action="refreshed", insight_id=old["id"], reason=reason, topic=slug)
            counts["reinforced"] += 1

    store.topics_state[slug] = {
        "synthesis": result.get("synthesis", "").strip(),
        "open_questions": [q.strip() for q in result.get("open_questions", []) if q.strip()][:5],
        "updated": day,
    }
    return counts


def apply_freshness(cfg: Config, store: Store, today: date) -> dict:
    """Flag unreinforced insights as stale after N days and archive them after M days.

    Returns {'stale': [...ids], 'archived': [...ids]}.
    """
    stale_days = int(cfg.setting("freshness.stale_after_days", 90))
    archive_days = int(cfg.setting("freshness.archive_after_days", 180))
    day = today.isoformat()
    changed = {"stale": [], "archived": []}
    for ins in sorted(store.insights.values(), key=lambda i: i["id"]):
        if ins["status"] not in LIVE:
            continue
        age = (today - parse_date(ins.get("last_reinforced") or ins["date"])).days
        topic = (ins.get("topics") or [""])[0]
        if age >= archive_days:
            ins.update(status="archived", status_changed=day,
                       status_reason=f"not reinforced for {age} days")
            store.log(day=day, action="archived", insight_id=ins["id"], topic=topic,
                      reason=f"Not reinforced by any newer video for {age} days")
            changed["archived"].append(ins["id"])
        elif age >= stale_days and ins["status"] == "active":
            ins.update(status="stale", status_changed=day, status_reason=f"not reinforced for {age} days")
            store.log(day=day, action="stale", insight_id=ins["id"], topic=topic,
                      reason=f"Not reinforced by any newer video for {age} days; review")
            changed["stale"].append(ins["id"])
    return changed


def video_status(store: Store, video_id: str) -> str:
    """Derive a video's knowledge status from its insights."""
    statuses = {i["status"] for i in store.insights_for_video(video_id)}
    if not statuses or statuses & set(LIVE):
        return "active"
    if "archived" in statuses:
        return "archived"
    return "superseded"
