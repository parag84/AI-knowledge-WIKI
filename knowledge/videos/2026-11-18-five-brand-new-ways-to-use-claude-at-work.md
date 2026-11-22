---
title: Five brand new ways to use Claude at work
channel: Claude
url: https://www.youtube.com/watch?v=t2Zo3YAJdj4
video_id: t2Zo3YAJdj4
published: '2026-11-18'
duration: '4:03'
topics:
- ux-for-ai
- agents
- mcp-tools
- model-releases
- rag
relevance: 4
status: active
superseded_by: []
---

# Five brand new ways to use Claude at work

[![Five brand new ways to use Claude at work](../assets/thumbs/t2Zo3YAJdj4.webp)](https://www.youtube.com/watch?v=t2Zo3YAJdj4)

**Claude** · 2026-11-18 · 4:03 · relevance 4/5 · [Watch on YouTube](https://www.youtube.com/watch?v=t2Zo3YAJdj4)

## Summary

A four-minute Anthropic product video announcing new Claude workplace tools: Claude Meetings, Claude Whiteboards, Claude Sheets, Claude Data (renamed from Claude Dashboards) and interactive connectors. It demos a team year-in-review where Claude joins a call as a visible participant, builds a shared whiteboard and timeline live, generates a formula-driven scorecard spreadsheet with highlighted edits, and produces certified-data charts and narrated data stories. The main takeaway is that Claude is positioned as a co-present, multiplayer collaborator inside artifacts and third-party apps, with visible edits, approval of actions and per-user permissions as the trust mechanisms.

## Key insights

- Claude Meetings joins a call from the calendar as a participant everyone can see. It takes notes, answers questions in writing, and builds docs or whiteboards on a shared meeting page during the call, so artifacts are ready when the call ends.
  - _Relies on:_ Claude Meetings: rolling out in beta on Team and Enterprise plans; Added from calendar; visible participant; Pulls from connected tools with each person's permission _(as of 2026-11-18)_
- In Claude Sheets, every edit Claude makes is outlined as it lands while humans edit the same cells. This is a concrete visible-diff pattern for supervising agent changes in multiplayer artifacts.
  - _Relies on:_ Claude Sheets: beta, all paid plans; Generates formulas; export supported _(as of 2026-11-18)_
- In Whiteboards, a user can drag a box around a messy region and ask Claude about only that selection. This spatial-selection-as-scope pattern lets the user set the agent's context through direct manipulation instead of prompting.
  - _Relies on:_ Claude Whiteboards: beta, all paid plans; multiple users can edit simultaneously _(as of 2026-11-18)_
- Claude Data lets data teams certify queries, and any chart built on a certified query shows a certified badge. The badge acts as a provenance and trust signal on AI-generated visualizations, and live sharing shows up-to-date dashboards to viewers who lack data-source access.
  - _Relies on:_ Claude Data is the new name for Claude Dashboards, now out of beta; Certified queries and live sharing are in beta; Can produce data stories or short narrated videos _(as of 2026-11-18)_
- Interactive connectors open third-party apps in full beside the chat. The user can edit directly or ask Claude to edit, and approves everything Claude does, with Claude operating within each person's existing permissions.
  - _Relies on:_ Interactive connectors rolling out on all plans; Business-app plugins ship with built-in skills, some in beta _(as of 2026-11-18)_

## Tools, models & APIs mentioned

- **Claude Meetings** beta (product)
- **Claude Whiteboards** beta (product)
- **Claude Sheets** beta (product)
- **Claude Data** (product)
- **Claude interactive connectors** (product)
- **Claude Docs** (product)
- **Claude Slides** (product)
- **Claude Design** (product)

## How this applies to AX / design systems

These patterns map directly onto AI component library primitives: an 'agent participant' presence indicator, an outlined live-edit/diff highlight token for agent changes, a selection-scoped prompt affordance, and a certified/provenance badge component. The app-beside-chat split view with per-action approval is a strong reference for tool-call approval UI and permission-inheritance messaging in developer portals. A worthwhile experiment is defining design tokens for agent-authored edits versus human edits, plus a trust-badge variant, in the Lit component set.

_Relevance 4/5: The video is a product announcement, but it shows several concrete agentic UX patterns Parag designs for: agent as visible meeting participant, outlined live edits, certified-data badges, side-by-side app panels with approval, and permission inheritance._

## Best moments

- [0:00](https://www.youtube.com/watch?v=t2Zo3YAJdj4&t=0s): Drag-select region on whiteboard and ask Claude about it
- [0:31](https://www.youtube.com/watch?v=t2Zo3YAJdj4&t=31s): Claude added from calendar as a visible meeting participant
- [1:02](https://www.youtube.com/watch?v=t2Zo3YAJdj4&t=62s): Permissions per person and live collaborative meeting page
- [2:04](https://www.youtube.com/watch?v=t2Zo3YAJdj4&t=124s): Agent edits outlined as they land in Sheets
- [2:35](https://www.youtube.com/watch?v=t2Zo3YAJdj4&t=155s): Certified query badges and live sharing in Claude Data
