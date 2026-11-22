import json
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from hub.llm import ClaudeJSON, LLMError
from hub.transcripts import parse_json3, parse_vtt, to_prompt_text
from hub.youtube import list_uploads_since, parse_duration, resolve_channel, YouTubeError

FIX = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize("iso,secs", [("PT24M30S", 1470), ("PT58S", 58), ("PT1H2M3S", 3723), ("P1DT1S", 86401),
                                      ("PT0S", 0), ("garbage", 0)])
def test_parse_duration(iso, secs):
    assert parse_duration(iso) == secs


def test_parse_vtt_dedupes_and_strips_tags():
    segs = parse_vtt((FIX / "sample.vtt").read_text())
    assert [s["text"] for s in segs] == ["hello world", "second line"]
    assert segs[1]["start"] == 62.5


def test_parse_json3():
    data = {"events": [{"tStartMs": 1500, "segs": [{"utf8": "hi "}, {"utf8": "there"}]}, {"tStartMs": 3000}]}
    assert parse_json3(data) == [{"start": 1.5, "text": "hi there"}]


def test_prompt_text_groups_by_window():
    segs = json.loads((FIX / "sample_transcript.json").read_text())
    text = to_prompt_text(segs)
    assert text.splitlines()[0].startswith("[0:00] Welcome")
    assert "[15:00] Questions?" in text


def test_resolve_channel_not_found():
    with pytest.raises(YouTubeError):
        resolve_channel(lambda e, p: {"items": []}, {"name": "X", "handle": "@x"})


def test_list_uploads_stops_at_older_page():
    pages = [
        {"items": [{"contentDetails": {"videoId": "a", "videoPublishedAt": "2026-11-20T00:00:00Z"}},
                   {"contentDetails": {"videoId": "b", "videoPublishedAt": "2026-10-01T00:00:00Z"}}],
         "nextPageToken": "p2"},
        {"items": [{"contentDetails": {"videoId": "c", "videoPublishedAt": "2026-09-01T00:00:00Z"}}]},
    ]
    calls = []

    def get(endpoint, params):
        calls.append(params)
        return pages[len(calls) - 1]

    ids = list_uploads_since(get, "UU", datetime(2026, 11, 1, tzinfo=timezone.utc))
    assert ids == ["a"] and len(calls) == 1


class FakeMessages:
    def __init__(self, resp):
        self.resp, self.kwargs = resp, None

    def create(self, **kwargs):
        self.kwargs = kwargs
        return self.resp


def fake_client(text, stop="end_turn"):
    resp = SimpleNamespace(stop_reason=stop, content=[SimpleNamespace(type="thinking"),
                                                      SimpleNamespace(type="text", text=text)],
                           usage=SimpleNamespace(input_tokens=10, output_tokens=5, cache_read_input_tokens=0))
    msgs = FakeMessages(resp)
    return SimpleNamespace(messages=msgs, beta=SimpleNamespace(messages=msgs)), msgs


def test_claude_json_request_shape():
    client, msgs = fake_client('{"ok": true}')
    llm = ClaudeJSON("claude-opus-5-5", effort="medium", client=client)
    assert llm.call_json(system="sys", user="u", schema={"type": "object"}) == {"ok": True}
    k = msgs.kwargs
    assert k["model"] == "claude-opus-5-5"
    assert k["output_config"]["format"]["type"] == "json_schema" and k["output_config"]["effort"] == "medium"
    assert k["system"][0]["cache_control"] == {"type": "ephemeral"}
    assert k["fallbacks"] == "default" and k["betas"] == ["server-side-fallback-2026-07-01"]
    assert llm.usage["calls"] == 1


def test_claude_json_without_fallbacks_uses_plain_endpoint():
    client, msgs = fake_client('{"ok": 1}')
    ClaudeJSON("m", client=client, fallbacks=None).call_json(system="s", user="u", schema={})
    assert "fallbacks" not in msgs.kwargs and "betas" not in msgs.kwargs


@pytest.mark.parametrize("stop", ["refusal", "max_tokens"])
def test_claude_json_bad_stop_reasons(stop):
    client, _ = fake_client("{}", stop=stop)
    with pytest.raises(LLMError):
        ClaudeJSON("m", client=client).call_json(system="s", user="u", schema={})


def test_api_errors_become_llm_errors():
    import anthropic

    class FakeAPIError(anthropic.APIError):
        def __init__(self):
            Exception.__init__(self, "connection dropped")

    class Boom:
        def create(self, **kw):
            raise FakeAPIError()

    client = SimpleNamespace(messages=Boom(), beta=SimpleNamespace(messages=Boom()))
    with pytest.raises(LLMError):
        ClaudeJSON("m", client=client).call_json(system="s", user="u", schema={})
