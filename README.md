# AI Video Knowledge Hub

A self-maintaining knowledge base. Every Sunday it collects new educational videos from selected AI YouTube
channels, reads their transcripts, writes concise insights for agentic UX, design systems and developer-portal
work, groups them by topic, prunes outdated knowledge, opens a weekly digest issue and publishes a dashboard to
GitHub Pages.

- **Dashboard:** `https://<your-user>.github.io/<this-repo>/`, with views for what's new, by topic, by week, by relevance, what's outdated, digests and full-text search
- **Knowledge in the repo:** [`knowledge/topics/`](knowledge/topics/README.md) · [`knowledge/videos/`](knowledge/videos/) · [`knowledge/changelog.md`](knowledge/changelog.md) · [`knowledge/archive/`](knowledge/archive/README.md) · [`digests/`](digests/)

## Setup (one time)

1. **Add two repository secrets** in *Settings → Secrets and variables → Actions → New repository secret*:
   - `YOUTUBE_API_KEY`: a YouTube Data API v3 key. In Google Cloud Console, create a project, enable
     *YouTube Data API v3*, then go to *Credentials → Create credentials → API key*. Restrict the key to that API.
     A weekly run uses about 50 quota units out of the free 10,000 per day.
   - `ANTHROPIC_API_KEY`: from <https://console.anthropic.com/settings/keys>.
   - `TRANSCRIPT_PROXY_URL`: needed in practice, because YouTube blocks transcript downloads from GitHub's
     servers. Use a **rotating residential** proxy. With Webshare, buy a "Residential" plan (not "Proxy Server"
     or "Static Residential"), take the Proxy Username and Password from
     <https://dashboard.webshare.io/proxy/settings>, and set the secret to
     `http://<username>-rotate:<password>@p.webshare.io:80/`.
2. **Enable Pages:** go to *Settings → Pages → Build and deployment → Source* and choose **GitHub Actions**.
3. **Allow the workflow to push:** go to *Settings → Actions → General → Workflow permissions* and choose
   **Read and write permissions**.
4. **Run the first backfill:** (after the self-hosted runner below is set up) go to *Actions → Weekly knowledge update → Run workflow* and set
   `backfill_days` to `30`. Later runs pick up from the last successful run automatically.
5. **Review** the first digest issue and the taxonomy (`config/topics.yaml`, including `proposed_topics`). See
   [Reviewing the taxonomy](#reviewing-the-taxonomy).

## Self-hosted runner (Windows PC)

YouTube blocks transcript downloads from GitHub's own servers, so the weekly **update** job runs on your PC
(`runs-on: [self-hosted, knowledge-hub]`). Publishing the dashboard still runs on GitHub. The job starts on
Sundays at 19:00 UTC. If the PC is off, it waits in the queue for up to 24 hours and starts as soon as the PC is on.

One-time setup on the PC:

1. Install **Python 3.12** from <https://www.python.org/downloads/windows/>. In the installer tick
   **Add python.exe to PATH**, choose **Customize installation → Install Python for all users**.
2. Install **Git for Windows** from <https://git-scm.com/download/win> with the default options. The workflow
   steps run in Windows PowerShell and start Python through the `py` launcher, so nothing else is needed.
3. In GitHub: **Settings → Actions → Runners → New self-hosted runner → Windows (x64)**. Open **PowerShell
   as Administrator** and run the *Download* commands shown there, then the *Configure* command. When it asks:
   - runner group, name, work folder: press Enter for the defaults
   - **labels: type `knowledge-hub`**
   - **run as a service: `Y`**, then press Enter to accept the default service account
4. Restart the PC once so the service picks up the new PATH. The runner shows as **Idle** on the Runners page.
5. Security, because this repo is public: **Settings → Actions → General → Approval for running fork pull
   request workflows from contributors → Require approval for all external contributors.** This stops a
   stranger's pull request from running code on your PC.

## How a run works

```
fetch (YouTube Data API) → transcripts (youtube-transcript-api → yt-dlp) → analyse each video (Claude)
  → freshness pass (stale / archive) → reconcile each touched topic (Claude) → render Markdown
  → weekly digest (Claude) → commit → digest issue → deploy dashboard
```

| Step | What happens |
|---|---|
| Fetch | Reads each channel's uploads playlist for videos published since the last successful run (with 24 h of overlap). Videos already in `data/videos.jsonl` are skipped. Videos under 3 minutes are recorded as `skipped_short`. |
| Transcripts | Tries `youtube-transcript-api` first, then `yt-dlp` auto-captions. If both fail, the video is marked `transcript_missing` and retried on the next run, for up to 4 weeks. The run never crashes on this. |
| Analysis | One Claude call per video, with at most 40 videos per run. Output is schema-validated JSON: a 3-sentence summary, 3–7 insights (each with the facts it relies on), tools/models/APIs with versions, a relevance score from 1 to 5 for your work, a "how this applies to AX / design systems" note and the best timestamps. |
| Freshness | Insights not reinforced by a newer video for **90 days** become `stale`. After **180 days** they're `archived` and the video page moves to `knowledge/archive/videos/`. |
| Reconciliation | One Claude call per touched topic. It compares new insights with existing ones and marks older claims `superseded` (newer model, deprecated API, changed practice) or `reinforced`, then rewrites the topic synthesis from active insights only. Every decision is logged with a one-line reason in `knowledge/changelog.md`. |
| Digest | Writes `digests/<yyyy>-W<ww>.md` with the top 5 insights, what changed and 2–3 suggested experiments, then opens it as a GitHub issue labelled `digest`. A re-run updates that week's issue instead of opening a new one. |

Re-running a week is idempotent: no duplicate videos, insights, changelog entries or issues.

## Repo layout

```
config/
  channels.yaml   channels to follow (add one by editing YAML only)
  topics.yaml     controlled taxonomy + proposed_topics awaiting approval
  profile.yaml    your focus areas, used for relevance scoring and "applies to my work" notes
  settings.yaml   caps, model, freshness windows, visuals
prompts/          video_insight.md · topic_reconciliation.md · weekly_digest.md
hub/              the Python pipeline (python -m hub …)
data/             source of truth: videos.jsonl, insights.jsonl, changelog.jsonl, topics_state.json, state.json
knowledge/        generated Markdown: videos/, topics/, archive/, changelog.md, assets/ (webp thumbnails)
digests/          weekly digests
site/             static dashboard (plain HTML + JS); data.json is generated at deploy time
tests/            offline tests using one sample video
.github/workflows weekly.yml (Sun 06:00 UTC + manual) · pages.yml · ci.yml
```

Markdown under `knowledge/` is regenerated from `data/` on every run. Edit `data/` or `config/`, not the
generated pages.

## Reviewing the taxonomy

Claude can only tag insights with slugs listed under `topics:` in `config/topics.yaml`. When it sees a recurring
theme that doesn't fit, it adds an entry to `proposed_topics:`, and the digest lists it. To approve one, move it
into `topics:` and give it a `description`. To reject one, delete it. To rename a topic, change the `name` and
keep the `slug`.

## Common changes

- **Add a channel:** append `- name: …` with `handle: "@…"` (or `channel_id: UC…`) to `config/channels.yaml`.
  If a handle doesn't resolve, the run logs it and carries on. Pin the channel ID shown on the channel's
  *About → Share channel → Copy channel ID*.
- **Spend:** `analysis.max_videos_per_run` caps the number of Claude calls per run. The default model is
  `claude-opus-5-5` at medium effort, roughly $0.05–0.15 per video depending on length. Set `llm.model` to
  `claude-sonnet-5-5` or `claude-haiku-5-5` to cut cost. The run summary in the workflow log shows token usage.
- **Keyframes:** set `visuals.keyframes.enabled: true` to capture up to 4 frames at the best moments of
  slide-heavy talks. This downloads a low-res copy of the video with yt-dlp + ffmpeg, which GitHub runners are
  often blocked from doing. It fails quietly when that happens.
- **Freshness windows:** `freshness.stale_after_days` and `freshness.archive_after_days`.

## Privacy and copyright

Full transcripts are cached only in `.cache/` (gitignored, persisted between runs with `actions/cache`). They
are never committed or published. The repo and the dashboard hold summaries, short notes and links back to
YouTube.

## Local development

```bash
pip install -r requirements.txt
python -m pytest -q                       # offline tests
export YOUTUBE_API_KEY=… ANTHROPIC_API_KEY=…
python -m hub run --backfill-days 7 --max-videos 3
python -m hub render                      # regenerate Markdown from data/
python -m hub build-site --out _site && python -m http.server -d _site
```
