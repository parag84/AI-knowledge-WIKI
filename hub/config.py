"""Paths and YAML config loading."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class Paths:
    root: Path

    @property
    def config(self) -> Path:
        return self.root / "config"

    @property
    def prompts(self) -> Path:
        return self.root / "prompts"

    @property
    def data(self) -> Path:
        return self.root / "data"

    @property
    def knowledge(self) -> Path:
        return self.root / "knowledge"

    @property
    def videos_md(self) -> Path:
        return self.knowledge / "videos"

    @property
    def topics_md(self) -> Path:
        return self.knowledge / "topics"

    @property
    def archive_md(self) -> Path:
        return self.knowledge / "archive"

    @property
    def assets(self) -> Path:
        return self.knowledge / "assets"

    @property
    def digests(self) -> Path:
        return self.root / "digests"

    @property
    def site_src(self) -> Path:
        return self.root / "site"

    @property
    def cache(self) -> Path:
        return self.root / ".cache"

    @property
    def transcripts(self) -> Path:
        return self.cache / "transcripts"


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


@dataclass
class Config:
    paths: Paths
    channels: list[dict]
    topics: list[dict]
    proposed_topics: list[dict]
    profile: dict
    settings: dict

    @property
    def topic_slugs(self) -> list[str]:
        return [t["slug"] for t in self.topics]

    def setting(self, dotted: str, default: Any = None) -> Any:
        node: Any = self.settings
        for part in dotted.split("."):
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
        return node


def load_config(root: Path | str) -> Config:
    paths = Paths(Path(root).resolve())
    channels = load_yaml(paths.config / "channels.yaml").get("channels", [])
    topics_doc = load_yaml(paths.config / "topics.yaml")
    return Config(
        paths=paths,
        channels=channels,
        topics=topics_doc.get("topics", []) or [],
        proposed_topics=topics_doc.get("proposed_topics", []) or [],
        profile=load_yaml(paths.config / "profile.yaml"),
        settings=load_yaml(paths.config / "settings.yaml"),
    )


def add_proposed_topics(cfg: Config, proposals: list[dict]) -> list[dict]:
    """Append new topic proposals to config/topics.yaml without touching approved topics.

    Returns the proposals that were actually added (deduplicated by slug).
    """
    known = set(cfg.topic_slugs) | {p.get("slug") for p in cfg.proposed_topics}
    added = []
    for p in proposals:
        slug = (p.get("slug") or "").strip().lower()
        if not slug or slug in known:
            continue
        entry = {
            "slug": slug,
            "name": p.get("name", slug),
            "why": p.get("why", ""),
            "first_seen_in": p.get("first_seen_in", ""),
        }
        cfg.proposed_topics.append(entry)
        known.add(slug)
        added.append(entry)
    if added:
        path = cfg.paths.config / "topics.yaml"
        text = path.read_text(encoding="utf-8")
        head = text.split("\nproposed_topics:")[0].rstrip("\n")
        tail = yaml.safe_dump(
            {"proposed_topics": cfg.proposed_topics}, sort_keys=False, allow_unicode=True, width=120
        )
        path.write_text(head + "\n" + tail, encoding="utf-8", newline="\n")
    return added
