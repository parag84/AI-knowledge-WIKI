"""Steps of the weekly job on the self-hosted Windows runner (standard library only).

The workflow calls this through `cmd` instead of PowerShell or bash: PowerShell script files can be
blocked by the machine's execution policy, and a bare `bash` can resolve to the WSL launcher.

    python scripts/runner_step.py setup    # create .venv and install requirements
    python scripts/runner_step.py run      # run the pipeline (reads BACKFILL_DAYS / MAX_VIDEOS)
    python scripts/runner_step.py commit   # commit and push the results, if anything changed
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENV = ROOT / ".venv"
SUMMARY = Path(os.environ.get("RUNNER_TEMP", ROOT)) / "summary.json"


def venv_python() -> Path:
    win = VENV / "Scripts" / "python.exe"
    return win if win.exists() else VENV / "bin" / "python"


def sh(*cmd: str | Path, check: bool = True) -> int:
    print("+", " ".join(str(c) for c in cmd), flush=True)
    code = subprocess.call([str(c) for c in cmd], cwd=ROOT)
    if check and code:
        sys.exit(code)
    return code


def setup() -> None:
    print(f"Python {sys.version.split()[0]} at {sys.executable}", flush=True)
    venv.EnvBuilder(with_pip=True, clear=True).create(VENV)
    py = venv_python()
    sh(py, "-m", "pip", "install", "-q", "--upgrade", "pip")
    sh(py, "-m", "pip", "install", "-q", "-r", ROOT / "requirements.txt")


def run() -> None:
    args = ["--summary-out", str(SUMMARY)]
    if os.environ.get("BACKFILL_DAYS"):
        args += ["--backfill-days", os.environ["BACKFILL_DAYS"]]
    if os.environ.get("MAX_VIDEOS"):
        args += ["--max-videos", os.environ["MAX_VIDEOS"]]
    sh(venv_python(), "-m", "hub", "run", *args)


def commit() -> None:
    sh("git", "config", "user.name", "knowledge-hub-bot")
    sh("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    sh("git", "add", "-A", "data", "knowledge", "digests", "config/topics.yaml")
    if sh("git", "diff", "--cached", "--quiet", check=False) == 0:
        print("No changes to commit")
        return
    message = json.loads(SUMMARY.read_text(encoding="utf-8"))["commit_message"]
    sh("git", "commit", "-m", message)
    # main may have moved while the run was going (e.g. a merged PR): replay the results on top of it.
    for attempt in range(3):
        if sh("git", "pull", "--rebase", "origin", "main", check=False) != 0:
            sh("git", "rebase", "--abort", check=False)
            sys.exit("Results conflict with newer commits on main; re-run the workflow to regenerate them.")
        if sh("git", "push", "origin", "HEAD:main", check=False) == 0:
            return
    sys.exit("Push to main failed three times.")


if __name__ == "__main__":
    steps = {"setup": setup, "run": run, "commit": commit}
    if len(sys.argv) != 2 or sys.argv[1] not in steps:
        sys.exit(f"usage: runner_step.py {{{'|'.join(steps)}}}")
    steps[sys.argv[1]]()
