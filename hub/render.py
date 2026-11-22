"""Generate the Markdown knowledge base from data/ (idempotent full regeneration)."""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import yaml

from .config import Config
from .reconcile import video_status
from .store import Store, write_text_if_changed
from .transcripts import fmt_ts

STATUS_BADGE = {"active": "", "stale": " ⚠️ _stale: needs review_", "superseded": " ~~superseded~~",
                "archived": " 🗄️ _archived_"}


def video_relpath(video: dict, status: str) -> str:
    """Path of a video page relative to knowledge/."""
    base = "archive/videos" if status == "archived" else "videos"
    return f"{base}/{video['file']}.md"


def _rel(from_dir: str, target: str) -> str:
    depth = len([p for p in from_dir.split("/") if p])
    return "../" * depth + target


def _yt_at(url: str, seconds: int) -> str:
    return f"{url}&t={int(seconds)}s"


def render_video(cfg: Config, store: Store, v: dict) -> tuple[str, str]:
    status = video_status(store, v["id"])
    rel = video_relpath(v, status)
    here = str(Path(rel).parent)
    insights = store.insights_for_video(v["id"])
    a = v.get("analysis", {})

    superseders = []
    for i in insights:
        if i.get("superseded_by") and i["superseded_by"] in store.insights:
            other = store.videos.get(store.insights[i["superseded_by"]]["video_id"])
            if other and other["id"] != v["id"] and other["file"] not in superseders:
                superseders.append(other["file"])

    fm = {
        "title": v["title"],
        "channel": v["channel"],
        "url": v["url"],
        "video_id": v["id"],
        "published": v["published_at"][:10],
        "duration": fmt_ts(v["duration_s"]),
        "topics": v.get("topics", []),
        "relevance": v.get("relevance"),
        "status": status,
        "superseded_by": superseders,
    }
    lines = ["---", yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip(), "---", "",
             f"# {v['title']}", ""]
    if v.get("thumbnail"):
        lines += [f"[![{v['title']}]({_rel(here, 'assets/thumbs/' + v['thumbnail'])})]({v['url']})", ""]
    lines += [f"**{v['channel']}** · {v['published_at'][:10]} · {fmt_ts(v['duration_s'])} · "
              f"relevance {v.get('relevance', '?')}/5 · [Watch on YouTube]({v['url']})", ""]
    lines += ["## Summary", "", a.get("summary", "").strip(), ""]

    lines += ["## Key insights", ""]
    for i in insights:
        text = f"~~{i['text']}~~" if i["status"] in ("superseded", "archived") else i["text"]
        line = f"- {text}{STATUS_BADGE.get(i['status'], '')}"
        if i["status"] == "superseded" and i.get("superseded_by") in store.insights:
            sup = store.insights[i["superseded_by"]]
            sv = store.videos.get(sup["video_id"])
            if sv:
                line += (f" → replaced by [{sv['title']}]"
                         f"({_rel(here, video_relpath(sv, video_status(store, sv['id'])))})"
                         f": {i.get('status_reason', '')}")
        lines.append(line)
        if i.get("facts"):
            lines.append(f"  - _Relies on:_ {'; '.join(i['facts'])} _(as of {i['date']})_")
    lines.append("")

    tools = a.get("tools_mentioned", [])
    if tools:
        lines += ["## Tools, models & APIs mentioned", ""]
        for t in tools:
            ver = f" {t['version']}" if t.get("version") else ""
            lines.append(f"- **{t['name']}**{ver} ({t.get('kind', 'other')})")
        lines.append("")

    lines += ["## How this applies to AX / design systems", "", a.get("applies_to_work", "").strip(), ""]
    if a.get("relevance_reason"):
        lines += [f"_Relevance {v.get('relevance')}/5: {a['relevance_reason']}_", ""]

    moments = a.get("best_moments", [])
    if moments:
        lines += ["## Best moments", ""]
        lines += [f"- [{fmt_ts(m['seconds'])}]({_yt_at(v['url'], m['seconds'])}): {m['note']}" for m in moments]
        lines.append("")

    frames = v.get("keyframes", [])
    if frames:
        lines += ["## Keyframes", ""]
        lines += [f"![keyframe {n}]({_rel(here, 'assets/frames/' + f)})" for n, f in enumerate(frames, 1)]
        lines.append("")
    return rel, "\n".join(lines).rstrip() + "\n"


def _insight_line(store: Store, i: dict, here: str) -> str:
    v = store.videos.get(i["video_id"], {})
    link = _rel(here, video_relpath(v, video_status(store, v["id"]))) if v else ""
    rel = f", relevance {v.get('relevance')}/5" if v.get("relevance") else ""
    return f"- {i['text']} ([{v.get('title', i['video_id'])}]({link}), {i['date']}{rel})"


def render_topic(cfg: Config, store: Store, topic: dict) -> str:
    slug = topic["slug"]
    here = "topics"
    st = store.topics_state.get(slug, {})
    active = store.insights_for_topic(slug, ["active"])
    stale = store.insights_for_topic(slug, ["stale"])
    lines = [f"# {topic['name']}", "", f"> {topic.get('description', '')}", ""]
    lines += [f"_{len(active)} active · {len(stale)} stale · synthesis updated {st.get('updated', 'never')}_", ""]
    lines += ["## Current best understanding", "", st.get("synthesis") or "_No synthesis yet._", ""]
    lines += ["## Latest active insights", ""]
    lines += [_insight_line(store, i, here) for i in active[:25]] or ["_None yet._"]
    lines.append("")
    if stale:
        lines += ["## Stale: needs review", "",
                  "_Not reinforced by a newer video for 90+ days. Archived automatically at 180 days._", ""]
        lines += [_insight_line(store, i, here) for i in stale]
        lines.append("")
    lines += ["## Open questions", ""]
    lines += [f"- {q}" for q in st.get("open_questions", [])] or ["_None recorded._"]
    lines.append("")
    entries = [e for e in store.changelog if e.get("topic") == slug][-20:]
    lines += ["## Changelog", ""]
    lines += [f"- {e['date']}: **{e['action']}** `{e['insight_id']}`: {e['reason']}" for e in reversed(entries)] \
        or ["_No changes yet._"]
    return "\n".join(lines).rstrip() + "\n"


def render_all(cfg: Config, store: Store) -> list[str]:
    """Write every generated Markdown file; remove stale generated video pages. Returns changed paths."""
    k = cfg.paths.knowledge
    changed: list[str] = []
    expected: set[Path] = set()

    for v in sorted(store.videos.values(), key=lambda v: v["id"]):
        if v.get("status") != "analyzed":
            continue
        rel, text = render_video(cfg, store, v)
        expected.add(k / rel)
        if write_text_if_changed(k / rel, text):
            changed.append(rel)
    # A video page moves to archive/videos when all its insights are archived.
    for d in (k / "videos", k / "archive" / "videos"):
        for f in d.glob("*.md") if d.exists() else []:
            if f not in expected:
                f.unlink()
                changed.append(str(f.relative_to(k)))

    for t in cfg.topics:
        if write_text_if_changed(k / "topics" / f"{t['slug']}.md", render_topic(cfg, store, t)):
            changed.append(f"topics/{t['slug']}.md")

    # Topic index
    rows = ["# Topics", "", "| Topic | Active | Stale | Updated |", "|---|---|---|---|"]
    for t in cfg.topics:
        st = store.topics_state.get(t["slug"], {})
        rows.append(f"| [{t['name']}]({t['slug']}.md) | {len(store.insights_for_topic(t['slug'], ['active']))} | "
                    f"{len(store.insights_for_topic(t['slug'], ['stale']))} | {st.get('updated', 'never')} |")
    if cfg.proposed_topics:
        rows += ["", "## Proposed topics (awaiting approval in `config/topics.yaml`)", ""]
        rows += [f"- `{p['slug']}` {p.get('name', '')}: {p.get('why', '')}" for p in cfg.proposed_topics]
    write_text_if_changed(k / "topics" / "README.md", "\n".join(rows) + "\n")

    # Archive index
    by_topic: dict[str, list[dict]] = defaultdict(list)
    for i in store.insights.values():
        if i["status"] == "archived":
            by_topic[(i.get("topics") or ["untagged"])[0]].append(i)
    arch = ["# Archive", "",
            "Insights that no newer video reinforced for 180+ days. Nothing is deleted: the source video pages "
            "are in `archive/videos/` and full history is in git.", ""]
    for slug in sorted(by_topic):
        arch += [f"## {slug}", ""]
        arch += [_insight_line(store, i, "archive") + f" (archived {i.get('status_changed', '')})"
                 for i in sorted(by_topic[slug], key=lambda i: i["date"], reverse=True)]
        arch.append("")
    if not by_topic:
        arch.append("_Nothing archived yet._")
    write_text_if_changed(k / "archive" / "README.md", "\n".join(arch).rstrip() + "\n")

    # Global changelog
    by_day: dict[str, list[dict]] = defaultdict(list)
    for e in store.changelog:
        by_day[e["date"]].append(e)
    cl = ["# Knowledge changelog", "",
          "Every supersede, stale and archive decision, with a one-line reason. Newest first.", ""]
    for day in sorted(by_day, reverse=True):
        cl += [f"## {day}", ""]
        for e in by_day[day]:
            extra = f" → `{e['replaced_by']}`" if e.get("replaced_by") else ""
            cl.append(f"- **{e['action']}** `{e['insight_id']}`{extra} [{e.get('topic', '')}]: {e['reason']}")
        cl.append("")
    if not by_day:
        cl.append("_No changes yet._")
    write_text_if_changed(k / "changelog.md", "\n".join(cl).rstrip() + "\n")
    return changed
