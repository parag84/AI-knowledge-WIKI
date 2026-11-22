"""Command line: python -m hub <command>."""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path

from .config import load_config


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="hub", description=__doc__)
    p.add_argument("--root", default=".", help="repository root (default: current directory)")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="full weekly run: fetch, analyse, reconcile, render, digest")
    r.add_argument("--backfill-days", type=int, help="look back N days instead of since the last run")
    r.add_argument("--max-videos", type=int, help="cap on videos analysed this run (default from settings)")
    r.add_argument("--no-fetch", action="store_true", help="only process videos already in data/videos.jsonl")
    r.add_argument("--summary-out", help="also write the run summary JSON to this path")

    sub.add_parser("render", help="regenerate knowledge/ Markdown from data/ (no API calls)")
    s = sub.add_parser("build-site", help="build the static dashboard")
    s.add_argument("--out", default="_site")

    args = p.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    cfg = load_config(args.root)

    if args.cmd == "render":
        from .render import render_all
        from .store import Store

        changed = render_all(cfg, Store(cfg.paths.data))
        print(f"{len(changed)} files changed")
        return 0

    if args.cmd == "build-site":
        from .site_build import build_site

        print(build_site(cfg, Path(args.out)))
        return 0

    # run
    from .llm import from_config
    from .pipeline import run
    from .youtube import http_getter

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY is not set", file=sys.stderr)
        return 2
    get = None
    if not args.no_fetch:
        key = os.environ.get("YOUTUBE_API_KEY")
        if not key:
            print("YOUTUBE_API_KEY is not set (or pass --no-fetch)", file=sys.stderr)
            return 2
        get = http_getter(key)
    repo = os.environ.get("GITHUB_REPOSITORY")
    summary = run(cfg, get=get, llm=from_config(cfg), backfill_days=args.backfill_days,
                  max_videos=args.max_videos, fetch=not args.no_fetch,
                  repo_url=f"https://github.com/{repo}" if repo else "")
    text = json.dumps(summary, indent=2)
    print(text)
    if args.summary_out:
        Path(args.summary_out).write_text(text, encoding="utf-8")
    return 0
