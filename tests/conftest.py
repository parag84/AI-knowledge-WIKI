import json
import shutil
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
FIX = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A throwaway copy of the repo's config, prompts and site, with one cached transcript."""
    for d in ("config", "prompts", "site"):
        shutil.copytree(ROOT / d, tmp_path / d)
    (tmp_path / "data").mkdir()
    cache = tmp_path / ".cache" / "transcripts"
    cache.mkdir(parents=True)
    shutil.copy(FIX / "sample_transcript.json", cache / "vid00000001.json")
    # Keep tests offline: no thumbnail downloads.
    from hub import visuals
    monkeypatch.setattr(visuals, "download_thumbnail", lambda *a, **k: False)
    # Only one channel in tests.
    (tmp_path / "config" / "channels.yaml").write_text(
        "channels:\n  - name: AI Engineer\n    handle: \"@aiDotEngineer\"\n")
    return tmp_path


@pytest.fixture
def yt_get():
    api = json.loads((FIX / "youtube_api.json").read_text())
    calls = []

    def get(endpoint, params):
        calls.append((endpoint, params))
        if endpoint == "videos":
            wanted = params["id"].split(",")
            return {"items": [v for v in api["videos"]["items"] if v["id"] in wanted]}
        return api[endpoint]

    get.calls = calls
    return get


class FakeLLM:
    """Returns canned JSON by recognising which schema it was given."""

    def __init__(self, video=None, reconcile=None, digest=None):
        self.calls = []
        self.video = video
        self.reconcile = reconcile
        self.digest = digest
        self.usage = {"calls": 0}

    def call_json(self, *, system, user, schema, max_tokens=None):
        props = schema["properties"]
        self.calls.append({"system": system, "user": user, "kind": next(iter(props))})
        self.usage["calls"] += 1
        if "insights" in props:
            return json.loads(json.dumps(self.video or default_video()))
        if "decisions" in props:
            r = self.reconcile(user) if callable(self.reconcile) else self.reconcile
            return r or {"decisions": [], "synthesis": "Agents need inline approvals.",
                         "open_questions": ["How should approvals batch?"]}
        if "experiments" in props:
            return self.digest or {
                "headline": "Inline approval cards beat modals.",
                "top_insights": [{"insight_id": "vid00000001-1", "why": "Directly shapes the tool-call component."}],
                "changes_summary": "Nothing superseded.",
                "experiments": [{"title": "Prototype an approval card", "description": "Build a Lit card.",
                                 "effort": "small"}],
            }
        raise AssertionError("unknown schema")


def default_video():
    return {
        "summary": "A talk on approval flows. It shows inline diff cards. Approvals rose.",
        "topics": ["ux-for-ai", "mcp-tools"],
        "proposed_topics": [{"slug": "agent-approvals", "name": "Agent approvals", "why": "Recurring theme."}],
        "relevance": 5,
        "relevance_reason": "Directly about agentic UX components.",
        "insights": [
            {"text": "Inline diff cards for tool-call approval beat modal confirms.", "facts": [],
             "topics": ["ux-for-ai"]},
            {"text": "MCP 2026-06 tool annotations mark read-only tools, so those can skip approval.",
             "facts": ["MCP spec 2026-06", "readOnlyHint annotation"], "topics": ["mcp-tools", "not-a-topic"]},
            {"text": "Model each tool-call state as its own web component.", "facts": [],
             "topics": ["ux-for-ai"]},
        ],
        "tools_mentioned": [{"name": "Model Context Protocol", "version": "2026-06", "kind": "protocol"}],
        "applies_to_work": "Build an approval-card Lit component.",
        "best_moments": [{"seconds": 41, "note": "Modal vs inline"}, {"seconds": 99999, "note": "bogus"}],
        "has_visual_content": True,
    }


@pytest.fixture
def fake_llm():
    return FakeLLM
