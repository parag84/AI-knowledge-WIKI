"""Per-video analysis: transcript -> structured insights (one Claude call per video)."""
from __future__ import annotations

import re

import yaml

from .config import Config
from .llm import JSONModel, render_prompt
from .transcripts import fmt_ts, to_prompt_text


def profile_text(cfg: Config) -> str:
    return yaml.safe_dump(cfg.profile, sort_keys=False, allow_unicode=True).strip()


def taxonomy_text(cfg: Config) -> str:
    return "\n".join(f"- `{t['slug']}`: {t['name']}. {t.get('description', '')}" for t in cfg.topics)


def video_schema(topic_slugs: list[str]) -> dict:
    topic_list = {"type": "array", "items": {"type": "string", "enum": topic_slugs}}
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["summary", "topics", "proposed_topics", "relevance", "relevance_reason", "insights",
                     "tools_mentioned", "applies_to_work", "best_moments", "has_visual_content"],
        "properties": {
            "summary": {"type": "string"},
            "topics": topic_list,
            "proposed_topics": {
                "type": "array",
                "items": {
                    "type": "object", "additionalProperties": False,
                    "required": ["slug", "name", "why"],
                    "properties": {"slug": {"type": "string"}, "name": {"type": "string"},
                                   "why": {"type": "string"}},
                },
            },
            "relevance": {"type": "integer", "enum": [1, 2, 3, 4, 5]},
            "relevance_reason": {"type": "string"},
            "insights": {
                "type": "array",
                "items": {
                    "type": "object", "additionalProperties": False,
                    "required": ["text", "facts", "topics"],
                    "properties": {
                        "text": {"type": "string"},
                        "facts": {"type": "array", "items": {"type": "string"}},
                        "topics": topic_list,
                    },
                },
            },
            "tools_mentioned": {
                "type": "array",
                "items": {
                    "type": "object", "additionalProperties": False,
                    "required": ["name", "version", "kind"],
                    "properties": {
                        "name": {"type": "string"}, "version": {"type": "string"},
                        "kind": {"type": "string",
                                 "enum": ["model", "api", "sdk", "framework", "product", "protocol", "other"]},
                    },
                },
            },
            "applies_to_work": {"type": "string"},
            "best_moments": {
                "type": "array",
                "items": {
                    "type": "object", "additionalProperties": False,
                    "required": ["seconds", "note"],
                    "properties": {"seconds": {"type": "integer"}, "note": {"type": "string"}},
                },
            },
            "has_visual_content": {"type": "boolean"},
        },
    }


def slugify(text: str, max_len: int = 60) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:max_len].rstrip("-") or "video"


def analyze_video(cfg: Config, llm: JSONModel, video: dict, segments: list[dict]) -> dict:
    system = render_prompt(cfg.paths.prompts / "video_insight.md",
                           profile=profile_text(cfg), taxonomy=taxonomy_text(cfg))
    user = (
        f"Title: {video['title']}\n"
        f"Channel: {video['channel']}\n"
        f"Published: {video['published_at'][:10]}\n"
        f"Duration: {fmt_ts(video['duration_s'])}\n"
        f"URL: {video['url']}\n"
        f"Description:\n{video.get('description', '')}\n\n"
        f"Transcript (timestamped):\n{to_prompt_text(segments)}"
    )
    result = llm.call_json(system=system, user=user, schema=video_schema(cfg.topic_slugs))
    return normalise_analysis(result, cfg.topic_slugs, video["duration_s"])


def normalise_analysis(result: dict, slugs: list[str], duration_s: int) -> dict:
    """Enforce the limits the schema can't express (counts, ranges)."""
    allowed = set(slugs)
    result["insights"] = [i for i in result.get("insights", []) if i.get("text", "").strip()][:7]
    for ins in result["insights"]:
        ins["topics"] = [t for t in dict.fromkeys(ins.get("topics", [])) if t in allowed][:3]
    topics = [t for t in dict.fromkeys(result.get("topics", [])) if t in allowed]
    # Make sure every insight topic shows up on the video too.
    for ins in result["insights"]:
        topics += [t for t in ins["topics"] if t not in topics]
    result["topics"] = topics
    result["relevance"] = min(5, max(1, int(result.get("relevance", 1))))
    result["best_moments"] = sorted(
        (m for m in result.get("best_moments", []) if 0 <= int(m.get("seconds", -1)) <= max(duration_s, 1)),
        key=lambda m: m["seconds"],
    )[:5]
    return result
