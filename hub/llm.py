"""Thin wrapper around the Anthropic Python SDK returning schema-validated JSON."""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Protocol

log = logging.getLogger(__name__)


class LLMError(RuntimeError):
    pass


class JSONModel(Protocol):
    def call_json(self, *, system: str, user: str, schema: dict, max_tokens: int | None = None) -> dict: ...


def render_prompt(path: Path, **values: str) -> str:
    """Fill {{placeholders}} in a prompt template."""
    text = path.read_text(encoding="utf-8")
    for k, v in values.items():
        text = text.replace("{{" + k + "}}", v)
    return text


class ClaudeJSON:
    """One request per call; structured output via output_config.format (JSON schema)."""

    def __init__(self, model: str, effort: str = "medium", max_tokens: int = 16000,
                 fallbacks: Any = "default", client: Any = None):
        import anthropic

        self.anthropic = anthropic
        self.client = client or anthropic.Anthropic(max_retries=4)
        self.model = model
        self.effort = effort
        self.max_tokens = max_tokens
        self.fallbacks = fallbacks
        self.usage = {"input_tokens": 0, "output_tokens": 0, "cache_read_input_tokens": 0, "calls": 0}

    def call_json(self, *, system: str, user: str, schema: dict, max_tokens: int | None = None) -> dict:
        kwargs: dict[str, Any] = dict(
            model=self.model,
            max_tokens=max_tokens or self.max_tokens,
            # The system prompt (instructions + profile + taxonomy) is identical across videos: cache it.
            system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": user}],
            output_config={"effort": self.effort, "format": {"type": "json_schema", "schema": schema}},
        )
        try:
            if self.fallbacks:
                resp = self.client.beta.messages.create(
                    betas=["server-side-fallback-2026-07-01"], fallbacks=self.fallbacks, **kwargs
                )
            else:
                resp = self.client.messages.create(**kwargs)
        except self.anthropic.APIError as e:
            # The SDK already retried 429/5xx/connection errors; surface the rest as a per-item failure.
            raise LLMError(f"{type(e).__name__}: {e}") from e

        u = resp.usage
        self.usage["calls"] += 1
        self.usage["input_tokens"] += getattr(u, "input_tokens", 0) or 0
        self.usage["output_tokens"] += getattr(u, "output_tokens", 0) or 0
        self.usage["cache_read_input_tokens"] += getattr(u, "cache_read_input_tokens", 0) or 0

        if resp.stop_reason == "refusal":
            raise LLMError("model declined the request (refusal)")
        if resp.stop_reason == "max_tokens":
            raise LLMError("response hit max_tokens before finishing")
        text = next((b.text for b in resp.content if getattr(b, "type", "") == "text"), None)
        if text is None:
            raise LLMError("no text block in response")
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise LLMError(f"invalid JSON from model: {e}") from e


def from_config(cfg) -> ClaudeJSON:
    return ClaudeJSON(
        model=cfg.setting("llm.model", "claude-opus-5-5"),
        effort=cfg.setting("llm.effort", "medium"),
        max_tokens=int(cfg.setting("llm.max_tokens", 16000)),
        fallbacks=cfg.setting("llm.fallbacks", "default"),
    )
