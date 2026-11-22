"""JSON / JSONL persistence. JSON in data/ is the source of truth; Markdown is generated from it."""
from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def iso_week(d: date) -> str:
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def parse_date(value: str) -> date:
    return date.fromisoformat(value[:10])


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: Iterable[dict], key: str | None = None) -> None:
    rows = list(rows)
    if key:
        rows.sort(key=lambda r: str(r.get(key, "")))
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    tmp.replace(path)


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text_if_changed(path: Path, text: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8", newline="\n")  # LF even on Windows runners
    return True


class Store:
    """Loads and saves everything under data/."""

    def __init__(self, data_dir: Path):
        self.dir = data_dir
        self.videos: dict[str, dict] = {v["id"]: v for v in read_jsonl(data_dir / "videos.jsonl")}
        self.insights: dict[str, dict] = {i["id"]: i for i in read_jsonl(data_dir / "insights.jsonl")}
        self.changelog: list[dict] = read_jsonl(data_dir / "changelog.jsonl")
        self.topics_state: dict[str, dict] = read_json(data_dir / "topics_state.json", {}) or {}
        self.state: dict = read_json(data_dir / "state.json", {}) or {}

    def save(self) -> None:
        write_jsonl(self.dir / "videos.jsonl", self.videos.values(), key="id")
        write_jsonl(self.dir / "insights.jsonl", self.insights.values(), key="id")
        write_jsonl(self.dir / "changelog.jsonl", self.changelog)
        write_json(self.dir / "topics_state.json", self.topics_state)
        write_json(self.dir / "state.json", self.state)

    # --- helpers -----------------------------------------------------------
    def insights_for_video(self, video_id: str) -> list[dict]:
        return sorted(
            (i for i in self.insights.values() if i["video_id"] == video_id), key=lambda i: i["id"]
        )

    def insights_for_topic(self, slug: str, statuses: Iterable[str] | None = None) -> list[dict]:
        statuses = set(statuses) if statuses else None
        out = [
            i
            for i in self.insights.values()
            if slug in i.get("topics", []) and (statuses is None or i["status"] in statuses)
        ]
        return sorted(out, key=lambda i: (i["date"], i["id"]), reverse=True)

    def log(self, *, day: str, action: str, insight_id: str, reason: str, topic: str = "",
            replaced_by: str | None = None) -> None:
        entry = {"date": day, "action": action, "insight_id": insight_id, "reason": reason, "topic": topic}
        if replaced_by:
            entry["replaced_by"] = replaced_by
        # Idempotent: identical decision on the same day is recorded once.
        if entry not in self.changelog:
            self.changelog.append(entry)
