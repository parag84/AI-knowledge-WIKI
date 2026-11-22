"""YouTube Data API v3: resolve channels, list recent uploads, fetch video details."""
from __future__ import annotations

import logging
import re
from datetime import datetime
from typing import Callable

import requests

from .store import parse_dt

log = logging.getLogger(__name__)

API = "https://www.googleapis.com/youtube/v3"

Getter = Callable[[str, dict], dict]


class YouTubeError(RuntimeError):
    pass


def http_getter(api_key: str, timeout: int = 30) -> Getter:
    session = requests.Session()

    def get(endpoint: str, params: dict) -> dict:
        resp = session.get(f"{API}/{endpoint}", params={**params, "key": api_key}, timeout=timeout)
        if resp.status_code != 200:
            # Never echo the key back in errors.
            raise YouTubeError(f"YouTube API {endpoint} returned {resp.status_code}: {resp.text[:300]}")
        return resp.json()

    return get


_DURATION = re.compile(r"P(?:(?P<d>\d+)D)?(?:T(?:(?P<h>\d+)H)?(?:(?P<m>\d+)M)?(?:(?P<s>\d+)S)?)?$")


def parse_duration(iso: str) -> int:
    """ISO-8601 duration (e.g. PT1H2M3S) to seconds. Unknown formats return 0."""
    m = _DURATION.match(iso or "")
    if not m:
        return 0
    d, h, mi, s = (int(m.group(k) or 0) for k in ("d", "h", "m", "s"))
    return ((d * 24 + h) * 60 + mi) * 60 + s


def resolve_channel(get: Getter, channel: dict) -> dict:
    """Return {'channel_id', 'uploads', 'title'} for a config entry with `channel_id` or `handle`."""
    params = {"part": "contentDetails,snippet"}
    if channel.get("channel_id"):
        params["id"] = channel["channel_id"]
    elif channel.get("handle"):
        params["forHandle"] = channel["handle"]
    else:
        raise YouTubeError(f"Channel {channel.get('name')!r} needs a handle or channel_id")
    items = get("channels", params).get("items") or []
    if not items:
        raise YouTubeError(
            f"Channel {channel.get('name')!r} not found ({channel.get('channel_id') or channel.get('handle')}). "
            "Set `channel_id` in config/channels.yaml."
        )
    item = items[0]
    return {
        "channel_id": item["id"],
        "uploads": item["contentDetails"]["relatedPlaylists"]["uploads"],
        "title": item["snippet"]["title"],
    }


def list_uploads_since(get: Getter, uploads_playlist: str, since: datetime, max_pages: int = 10) -> list[str]:
    """Video IDs from the uploads playlist published at or after `since` (newest first)."""
    ids: list[str] = []
    token = None
    for _ in range(max_pages):
        params = {"part": "contentDetails", "playlistId": uploads_playlist, "maxResults": 50}
        if token:
            params["pageToken"] = token
        data = get("playlistItems", params)
        reached_older = False
        for item in data.get("items", []):
            published = item["contentDetails"].get("videoPublishedAt")
            if not published:
                continue  # private/deleted
            if parse_dt(published) >= since:
                ids.append(item["contentDetails"]["videoId"])
            else:
                reached_older = True
        token = data.get("nextPageToken")
        # Uploads playlists are newest-first; once a page reaches older videos, later pages are older still.
        if not token or reached_older:
            break
    return ids


def video_details(get: Getter, video_ids: list[str]) -> list[dict]:
    out = []
    for start in range(0, len(video_ids), 50):
        batch = video_ids[start:start + 50]
        data = get("videos", {"part": "snippet,contentDetails", "id": ",".join(batch), "maxResults": 50})
        for item in data.get("items", []):
            sn = item["snippet"]
            thumbs = sn.get("thumbnails", {})
            thumb = next((thumbs[k]["url"] for k in ("maxres", "standard", "high", "medium", "default")
                          if k in thumbs), "")
            out.append({
                "id": item["id"],
                "title": sn.get("title", ""),
                "channel_title": sn.get("channelTitle", ""),
                "channel_id": sn.get("channelId", ""),
                "published_at": sn.get("publishedAt", ""),
                "description": (sn.get("description") or "")[:1500],
                "duration_s": parse_duration(item["contentDetails"].get("duration", "")),
                "live": sn.get("liveBroadcastContent", "none"),
                "thumbnail_url": thumb,
                "url": f"https://www.youtube.com/watch?v={item['id']}",
            })
    return out
