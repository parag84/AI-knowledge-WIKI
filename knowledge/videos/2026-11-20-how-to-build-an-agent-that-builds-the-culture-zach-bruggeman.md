---
title: How to build an agent that builds the culture — Zach Bruggeman, Ramp
channel: AI Engineer
url: https://www.youtube.com/watch?v=MDI81OaZAD4
video_id: MDI81OaZAD4
published: '2026-11-20'
duration: '14:28'
topics:
- coding-agents
- ux-for-ai
- agents
- startups-product
- infra-cost
relevance: 4
status: active
superseded_by: []
---

# How to build an agent that builds the culture — Zach Bruggeman, Ramp

[![How to build an agent that builds the culture — Zach Bruggeman, Ramp](../assets/thumbs/MDI81OaZAD4.webp)](https://www.youtube.com/watch?v=MDI81OaZAD4)

**AI Engineer** · 2026-11-20 · 14:28 · relevance 4/5 · [Watch on YouTube](https://www.youtube.com/watch?v=MDI81OaZAD4)

## Summary

Zach Bruggeman of Ramp presents the engineering culture built around Inspect, Ramp's remote, multiplayer coding agent that he says now writes and ships around 75% of Ramp's code. He argues that a single shared agent, sessions that are public by default, and visible verification artifacts break information silos and build trust, illustrated by a public debugging thread on a telemetry bug and the grassroots Review Buddy code review agent. The takeaway is that the hard part is now culture rather than the technology, and tools should be designed to make collaboration and shared learning the default rather than celebrating the lone-wolf operator.

## Key insights

- Running one shared, company-wide coding agent as a solid baseline spreads improvements to everyone invisibly and removes per-person setup cost, so Ramp never needed to mandate its use.
  - _Relies on:_ Inspect is Ramp's collaborative coding agent, started about a year before the talk; Around 75% of Ramp's code is written and shipped by Inspect; Example setup cost cited: about 15 minutes per person, multiplied across a multi-hundred or multi-thousand person org _(as of 2026-11-20)_
- Making every agent session public by default replaces formal AI training: people learn by watching teammates' sessions, and can even ask the agent to summarize how a colleague structures prompts or breaks down problems.
  - _Relies on:_ Inspect sessions are public within Ramp by default; Inspect integrates with Slack, Linear and other tools _(as of 2026-11-20)_
- Trust in agent output comes from attaching provenance to the PR: the full conversation, the tools used, before and after screenshots, and a video of a verification agent clicking through the app in a browser.
  - _Relies on:_ Inspect includes a verification agent that records browser walkthroughs; Built-in design primitives, review agents and verification flows _(as of 2026-11-20)_
- In a public thread, a skeptical user's bug report turned into a collaborative fix: the agent traced the errors to the OTel exporter calling fetch without reading or cancelling the response body on Cloudflare Workers, and patched it to explicitly cancel the body.
  - _Relies on:_ Bug reported in February; Inspect had DataDog access; Root cause: OTel library for Cloudflare Workers never read or cancelled the fetch response body, hitting a Cloudflare platform limitation _(as of 2026-11-20)_
- Event-driven automation triggers, such as firing when a pull request is opened, let engineers build new agents on the platform without asking permission; Review Buddy replaced several off-the-shelf code review products this way.
  - _Relies on:_ Review Buddy is Ramp's internal code review agent built by engineers Daniel and Pranjal; Inspect sandboxes spin up in under 5 seconds _(as of 2026-11-20)_

## Tools, models & APIs mentioned

- **Inspect** (product)
- **Review Buddy** (product)
- **Claude Code** (product)
- **DataDog** (product)
- **Cloudflare Workers** (product)
- **OpenTelemetry** (framework)
- **Slack** (product)
- **Linear** (product)

## How this applies to AX / design systems

Design a 'session as artifact' pattern for AX: a shareable agent-session view that bundles the conversation, a tool-call log, before and after screenshots and a verification video, which could be a reusable Lit component in the AI component library. In developer portals, a public gallery of example agent sessions could teach usage by observation instead of static tutorials. A concrete experiment is a PR-review panel component that shows agent provenance next to the diff and testing whether reviewers trust and approve faster.

_Relevance 4/5: Public-by-default sessions, verification artifacts attached to PRs and multiplayer agent threads are concrete trust and supervision patterns for agentic UX that Parag could prototype, though the talk is about culture rather than design systems._

## Best moments

- [0:44](https://www.youtube.com/watch?v=MDI81OaZAD4&t=44s): Overview of Inspect's primitives, integrations and the 75% code share claim
- [4:20](https://www.youtube.com/watch?v=MDI81OaZAD4&t=260s): Public-by-default sessions replace AI training sessions
- [6:24](https://www.youtube.com/watch?v=MDI81OaZAD4&t=384s): Verification artifacts on PRs: conversation, tools, screenshots and a browser video
- [6:56](https://www.youtube.com/watch?v=MDI81OaZAD4&t=416s): Telemetry bug story showing trust built through a public thread
- [11:39](https://www.youtube.com/watch?v=MDI81OaZAD4&t=699s): Review Buddy built bottom-up on automation triggers
