"""Weekly digest: digests/<yyyy-Www>.md, also opened as a GitHub issue by the workflow."""
from __future__ import annotations

import json
from datetime import date, timedelta

from .analyze import profile_text
from .config import Config
from .llm import JSONModel, render_prompt
from .render import video_relpath
from .reconcile import video_status
from .store import Store, iso_week, parse_date, write_text_if_changed

DIGEST_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["headline", "top_insights", "changes_summary", "experiments"],
    "properties": {
        "headline": {"type": "string"},
        "top_insights": {
            "type": "array",
            "items": {"type": "object", "additionalProperties": False, "required": ["insight_id", "why"],
                      "properties": {"insight_id": {"type": "string"}, "why": {"type": "string"}}},
        },
        "changes_summary": {"type": "string"},
        "experiments": {
            "type": "array",
            "items": {"type": "object", "additionalProperties": False,
                      "required": ["title", "description", "effort"],
                      "properties": {"title": {"type": "string"}, "description": {"type": "string"},
                                     "effort": {"type": "string", "enum": ["small", "medium", "large"]}}},
        },
    },
}


def week_bounds(d: date) -> tuple[date, date]:
    start = d - timedelta(days=d.isoweekday() - 1)
    return start, start + timedelta(days=6)


def build_digest(cfg: Config, llm: JSONModel | None, store: Store, today: date, repo_url: str = "",
                 notice: str = "") -> tuple[str, str]:
    """Write the digest for today's ISO week. Returns (path relative to repo root, title)."""
    week = iso_week(today)
    start, end = week_bounds(today)
    in_week = lambda s: s and start <= parse_date(s) <= end  # noqa: E731

    new = [i for i in store.insights.values() if in_week(i.get("first_seen")) and i["status"] in ("active", "stale")]
    new.sort(key=lambda i: (-(store.videos[i["video_id"]].get("relevance") or 0), i["id"]))
    changes = [e for e in store.changelog if in_week(e["date"])]
    new_videos = sorted({i["video_id"] for i in new})

    def vlink(i: dict) -> str:
        v = store.videos[i["video_id"]]
        path = f"knowledge/{video_relpath(v, video_status(store, v['id']))}"
        href = f"{repo_url}/blob/main/{path}" if repo_url else f"../{path}"
        return f"[{v['title']}]({href})"

    title = f"Weekly AI digest {week}"
    lines = [f"# {title}", "", f"_{start.isoformat()} to {end.isoformat()} · {len(new_videos)} new videos · "
             f"{len(new)} new insights · {len(changes)} knowledge changes_", ""]
    if notice:
        lines += [f"> ⚠️ {notice}", ""]

    result = None
    if llm and (new or changes):
        system = render_prompt(cfg.paths.prompts / "weekly_digest.md", profile=profile_text(cfg))
        payload_new = [{"id": i["id"], "text": i["text"], "topics": i["topics"],
                        "relevance": store.videos[i["video_id"]].get("relevance"),
                        "video": store.videos[i["video_id"]]["title"]} for i in new[:60]]
        payload_changes = [{**e, "text": store.insights.get(e["insight_id"], {}).get("text", "")} for e in changes]
        user = (f"Week: {week}\n\nNew insights:\n{json.dumps(payload_new, ensure_ascii=False, indent=1)}\n\n"
                f"Knowledge changes:\n{json.dumps(payload_changes, ensure_ascii=False, indent=1)}")
        result = llm.call_json(system=system, user=user, schema=DIGEST_SCHEMA)

    if result:
        lines += [f"**{result['headline'].strip()}**", "", "## Top insights", ""]
        n = 0
        for t in result["top_insights"]:
            i = store.insights.get(t["insight_id"])
            if not i or n >= 5:
                continue
            n += 1
            lines += [f"{n}. {i['text']}", f"   - _Why it matters:_ {t['why']}", f"   - Source: {vlink(i)}"]
        lines.append("")
    else:
        lines += ["## Top insights", ""]
        lines += [f"{n}. {i['text']} ({vlink(i)})" for n, i in enumerate(new[:5], 1)] or ["_No new insights this week._"]
        lines.append("")

    lines += ["## What changed or got superseded", ""]
    if result:
        lines += [result["changes_summary"].strip(), ""]
    for e in changes:
        old = store.insights.get(e["insight_id"], {})
        extra = f" → replaced by `{e['replaced_by']}`" if e.get("replaced_by") else ""
        lines.append(f"- **{e['action']}**: {old.get('text', e['insight_id'])}{extra}. _{e['reason']}_")
    if not changes and not result:
        lines.append("_Nothing superseded, flagged stale or archived this week._")
    lines.append("")

    if result and result.get("experiments"):
        lines += ["## Suggested experiments", ""]
        for x in result["experiments"][:3]:
            lines += [f"- **{x['title']}** ({x['effort']}): {x['description']}"]
        lines.append("")

    proposed = cfg.proposed_topics
    if proposed:
        lines += ["## Proposed topics awaiting your review", "",
                  "Approve by moving them into `topics` in `config/topics.yaml`.", ""]
        lines += [f"- `{p['slug']}`: {p.get('why', '')}" for p in proposed]
        lines.append("")

    rel = f"digests/{week}.md"
    write_text_if_changed(cfg.paths.root / rel, "\n".join(lines).rstrip() + "\n")
    return rel, title
