import json
from datetime import date, datetime, timezone

import yaml

from hub.config import load_config
from hub.pipeline import run
from hub.site_build import build_site
from hub.store import Store

NOW = datetime(2026, 11, 22, 6, 0, tzinfo=timezone.utc)


def snapshot(root):
    files = {}
    for d in ("knowledge", "digests", "data"):
        for f in sorted((root / d).rglob("*")):
            if f.is_file() and f.name != "state.json":
                files[str(f.relative_to(root))] = f.read_text()
    return files


def test_first_run_end_to_end(repo, yt_get, fake_llm):
    cfg = load_config(repo)
    llm = fake_llm()
    s = run(cfg, get=yt_get, llm=llm, now=NOW)

    assert s["new_videos_found"] == 1 and s["skipped_short"] == 1
    assert s["analyzed"] == 1 and s["new_insights"] == 3
    assert s["commit_message"] == "weekly update 2026-W47: 1 new, 0 superseded"

    store = Store(repo / "data")
    assert store.videos["short000001"]["status"] == "skipped_short"
    assert "old00000001" not in store.videos  # outside the 30-day backfill
    v = store.videos["vid00000001"]
    assert v["status"] == "analyzed" and v["relevance"] == 5
    assert [m["seconds"] for m in v["analysis"]["best_moments"]] == [41]  # out-of-range moment dropped
    assert store.insights["vid00000001-2"]["topics"] == ["mcp-tools"]  # unknown slug dropped

    page = (repo / "knowledge/videos/2026-11-18-designing-agent-uis-with-mcp-approval-flows-that-users-trust.md")
    text = page.read_text()
    fm = yaml.safe_load(text.split("---")[1])
    assert fm["status"] == "active" and fm["relevance"] == 5 and fm["topics"] == ["ux-for-ai", "mcp-tools"]
    assert "## How this applies to AX / design systems" in text
    assert "&t=41s" in text

    topic = (repo / "knowledge/topics/ux-for-ai.md").read_text()
    assert "Agents need inline approvals." in topic and "Inline diff cards" in topic

    digest = (repo / "digests/2026-W47.md").read_text()
    assert "Inline approval cards beat modals." in digest and "Prototype an approval card" in digest

    # Proposed topic goes to the review list, not the approved taxonomy.
    topics = yaml.safe_load((repo / "config/topics.yaml").read_text())
    assert [p["slug"] for p in topics["proposed_topics"]] == ["agent-approvals"]
    assert "agent-approvals" not in [t["slug"] for t in topics["topics"]]
    # One analysis call, one reconcile per touched topic (2), one digest call.
    assert [c["kind"] for c in llm.calls].count("summary") == 1


def test_rerun_is_idempotent(repo, yt_get, fake_llm):
    cfg = load_config(repo)
    run(cfg, get=yt_get, llm=fake_llm(), now=NOW)
    before = snapshot(repo)
    llm = fake_llm()
    s = run(load_config(repo), get=yt_get, llm=llm, now=NOW, backfill_days=30)
    assert s["analyzed"] == 0 and s["new_videos_found"] == 0
    assert not [c for c in llm.calls if c["kind"] == "summary"]
    assert snapshot(repo) == before


def test_supersede_flow(repo, yt_get, fake_llm):
    run(load_config(repo), get=yt_get, llm=fake_llm(), now=NOW)

    # A week later a new video replaces the MCP claim.
    store = Store(repo / "data")
    store.videos["vid00000002"] = {
        "id": "vid00000002", "title": "MCP 2026-11 changes tool annotations", "channel": "Anthropic",
        "channel_id": "x", "published_at": "2026-11-25T10:00:00Z", "duration_s": 900,
        "url": "https://www.youtube.com/watch?v=vid00000002", "description": "", "thumbnail_url": "",
        "status": "pending", "transcript_attempts": 0,
    }
    store.save()
    cache = repo / ".cache/transcripts"
    (cache / "vid00000002.json").write_text(json.dumps([{"start": 0, "text": "new annotations"}]))

    new_video = {
        "summary": "s", "topics": ["mcp-tools"], "proposed_topics": [], "relevance": 4, "relevance_reason": "r",
        "insights": [{"text": "MCP 2026-11 replaces readOnlyHint with a permissions block.",
                      "facts": ["MCP spec 2026-11"], "topics": ["mcp-tools"]}],
        "tools_mentioned": [], "applies_to_work": "a", "best_moments": [], "has_visual_content": False,
    }

    def reconcile(user):
        if "vid00000002-1" in user and "vid00000001-2" in user:
            return {"decisions": [{"action": "supersede", "old_id": "vid00000001-2", "new_id": "vid00000002-1",
                                   "reason": "MCP 2026-11 replaces readOnlyHint"},
                                  {"action": "supersede", "old_id": "vid00000002-1", "new_id": "bogus",
                                   "reason": "invalid id is ignored"}],
                    "synthesis": "Use the permissions block.", "open_questions": []}
        return None

    s = run(load_config(repo), get=None, llm=fake_llm(video=new_video, reconcile=reconcile), fetch=False,
            now=datetime(2026, 11, 29, 6, tzinfo=timezone.utc))
    assert s["superseded"] == 1
    assert s["commit_message"] == "weekly update 2026-W48: 1 new, 1 superseded"
    store = Store(repo / "data")
    old = store.insights["vid00000001-2"]
    assert old["status"] == "superseded" and old["superseded_by"] == "vid00000002-1"
    assert store.insights["vid00000002-1"]["status"] == "active"
    changelog = (repo / "knowledge/changelog.md").read_text()
    assert "MCP 2026-11 replaces readOnlyHint" in changelog
    page = next((repo / "knowledge/videos").glob("2026-11-18-*.md")).read_text()
    assert "~~MCP 2026-06" in page and "replaced by" in page
    # Topic synthesis is rewritten; superseded insight no longer listed as active.
    topic = (repo / "knowledge/topics/mcp-tools.md").read_text()
    assert "Use the permissions block." in topic
    assert "readOnlyHint annotation" not in topic.split("## Latest active insights")[1].split("##")[0]


def test_freshness_stale_then_archive(repo, yt_get, fake_llm):
    run(load_config(repo), get=yt_get, llm=fake_llm(), now=NOW)
    # 95 days later: stale.
    s = run(load_config(repo), get=None, llm=fake_llm(), fetch=False,
            now=datetime(2027, 2, 21, 6, tzinfo=timezone.utc))
    assert s["stale"] == 3 and s["archived"] == 0
    store = Store(repo / "data")
    assert {i["status"] for i in store.insights.values()} == {"stale"}
    assert "Stale: needs review" in (repo / "knowledge/topics/ux-for-ai.md").read_text()

    # 185 days after publish: archived, and the video page moves to knowledge/archive/videos/.
    s = run(load_config(repo), get=None, llm=fake_llm(), fetch=False,
            now=datetime(2027, 5, 22, 6, tzinfo=timezone.utc))
    assert s["archived"] == 3
    assert not list((repo / "knowledge/videos").glob("*.md"))
    archived = list((repo / "knowledge/archive/videos").glob("*.md"))
    assert len(archived) == 1 and "status: archived" in archived[0].read_text()
    assert "Inline diff cards" in (repo / "knowledge/archive/README.md").read_text()
    log = (repo / "knowledge/changelog.md").read_text()
    assert "**stale**" in log and "**archived**" in log


def test_reinforce_refreshes_stale(repo, yt_get, fake_llm):
    run(load_config(repo), get=yt_get, llm=fake_llm(), now=NOW)
    store = Store(repo / "data")
    for i in store.insights.values():
        i["status"] = "stale"
    store.videos["vid00000003"] = {
        "id": "vid00000003", "title": "Approvals again", "channel": "Claude", "channel_id": "x",
        "published_at": "2027-02-20T10:00:00Z", "duration_s": 900, "url": "https://www.youtube.com/watch?v=vid00000003",
        "description": "", "thumbnail_url": "", "status": "pending", "transcript_attempts": 0,
    }
    store.save()
    (repo / ".cache/transcripts/vid00000003.json").write_text(json.dumps([{"start": 0, "text": "x"}]))
    vid = {"summary": "s", "topics": ["ux-for-ai"], "proposed_topics": [], "relevance": 5, "relevance_reason": "r",
           "insights": [{"text": "Inline approvals still win.", "facts": [], "topics": ["ux-for-ai"]}],
           "tools_mentioned": [], "applies_to_work": "a", "best_moments": [], "has_visual_content": False}
    rec = {"decisions": [{"action": "reinforce", "old_id": "vid00000001-1", "new_id": "vid00000003-1",
                          "reason": "confirmed again"}], "synthesis": "x", "open_questions": []}
    run(load_config(repo), get=None, llm=fake_llm(video=vid, reconcile=rec), fetch=False,
        now=datetime(2027, 2, 21, 6, tzinfo=timezone.utc))
    ins = Store(repo / "data").insights["vid00000001-1"]
    assert ins["status"] == "active" and ins["last_reinforced"] == "2027-02-20"


def test_transcript_missing_never_crashes(repo, yt_get, fake_llm, monkeypatch):
    (repo / ".cache/transcripts/vid00000001.json").unlink()
    from hub import transcripts
    monkeypatch.setattr(transcripts, "fetch_via_transcript_api", lambda vid: None)
    monkeypatch.setattr(transcripts, "fetch_via_ytdlp", lambda vid: None)
    s = run(load_config(repo), get=yt_get, llm=fake_llm(), now=NOW)
    assert s["transcript_missing"] == 1 and s["analyzed"] == 0
    v = Store(repo / "data").videos["vid00000001"]
    assert v["status"] == "transcript_missing" and v["transcript_attempts"] == 1
    # Retried next week; gives up after max attempts.
    for _ in range(3):
        run(load_config(repo), get=None, llm=fake_llm(), fetch=False, now=NOW)
    assert Store(repo / "data").videos["vid00000001"]["status"] == "transcript_unavailable"


def test_max_videos_cap(repo, yt_get, fake_llm):
    s = run(load_config(repo), get=yt_get, llm=fake_llm(), now=NOW, max_videos=0)
    assert s["analyzed"] == 0 and s["pending_left"] == 1


def test_site_never_publishes_transcripts(repo, yt_get, fake_llm, tmp_path):
    run(load_config(repo), get=yt_get, llm=fake_llm(), now=NOW)
    out = build_site(load_config(repo), tmp_path / "site_out")
    data = (out / "data.json").read_text()
    assert "Welcome everyone, today we're talking" not in data
    parsed = json.loads(data)
    assert len(parsed["videos"]) == 1 and parsed["digests"][0]["week"] == "2026-W47"
    assert (out / "index.html").exists() and (out / "app.js").exists()


def test_llm_failure_marks_video_failed_and_run_completes(repo, yt_get, fake_llm):
    from hub.llm import LLMError

    class Failing(fake_llm):
        def call_json(self, **kw):
            raise LLMError("boom")

    s = run(load_config(repo), get=yt_get, llm=Failing(), now=NOW)
    assert s["failed"] == 1 and s["analyzed"] == 0
    assert Store(repo / "data").videos["vid00000001"]["status"] == "failed"
    assert (repo / "digests/2026-W47.md").exists()
    # Next run retries and succeeds.
    s = run(load_config(repo), get=None, llm=fake_llm(), fetch=False, now=NOW)
    assert s["analyzed"] == 1
