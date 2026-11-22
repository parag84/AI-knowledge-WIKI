---
title: Build a "software factory" that doesn’t produce AI Slop
channel: Google Cloud Tech
url: https://www.youtube.com/watch?v=EFejzwBLAVo
video_id: EFejzwBLAVo
published: '2026-11-19'
duration: '9:32'
topics:
- coding-agents
- agents
- ux-for-ai
- mcp-tools
- infra-cost
- model-releases
relevance: 3
status: active
superseded_by: []
---

# Build a "software factory" that doesn’t produce AI Slop

[![Build a "software factory" that doesn’t produce AI Slop](../assets/thumbs/EFejzwBLAVo.webp)](https://www.youtube.com/watch?v=EFejzwBLAVo)

**Google Cloud Tech** · 2026-11-19 · 9:32 · relevance 3/5 · [Watch on YouTube](https://www.youtube.com/watch?v=EFejzwBLAVo)

## Summary

A Google Cloud Tech demo in which Rody Davis of the Antigravity DevRel team builds a "software factory" in Google Antigravity using Gemini 4 Argon and custom subagents defined in Markdown. The factory runs an "Evergreen platform" audit across Node, Jetpack Compose and SwiftUI codebases. Parallel per-platform subagents check the code against a platform version policy, remove obsolete polyfills and legacy APIs, and produce a Git-history freshness report. The takeaway is to point agents at the trailing edge (pruning and auditing code) rather than only generating new code, while keeping the human in a supervisory "floor manager" role with observability and steering.

## Key insights

- Define each platform's audit as a separate custom subagent written in Markdown (a "factory line"). The main agent can then dispatch an ambiguous task and decide on its own which subagents to invoke.
  - _Relies on:_ Google Antigravity custom subagents are defined in Markdown; Demo subagents cover Web (Node.js), Android (Jetpack Compose) and iOS (SwiftUI) _(as of 2026-11-19)_
- A shared platform config file sets how many browser or mobile OS versions back the team must support. Subagents use it to find polyfills and legacy APIs that are now safe to remove. The right policy differs between indie developers on the bleeding edge and stable enterprises that need two to three versions back.
  - _Relies on:_ Platform version policy config defines the number of versions supported per platform _(as of 2026-11-19)_
- Each custom subagent runs in its own context window and in parallel. This reduces how often the main chat session has to compact its context.
  - _Relies on:_ Antigravity custom subagents have isolated context windows and run in parallel _(as of 2026-11-19)_
- Tools can be included or excluded per subagent. In the demo, the reviewer workers are set to read-only so they can review code but cannot write any.
  - _Relies on:_ Per-subagent tool allow/exclude configuration in Antigravity _(as of 2026-11-19)_
- Antigravity's supervision features include clicking into any worker to see its full conversation and messaging subagents directly to steer or stop them. A /learn command lets the agent repair and refine the workers' procedures over time.
  - _Relies on:_ /learn built-in command; Direct messaging to subagents (recently added feature) _(as of 2026-11-19)_
- The Automation panel can schedule the freshness audit, for example at the start of each month or around WWDC and Google I/O. The audit can pull in external sources such as MDN browser-compatibility data through web search.
  - _Relies on:_ Antigravity Automation panel for scheduled tasks; Example triggers: monthly, WWDC, Google I/O; source: MDN _(as of 2026-11-19)_
- For more hands-off work, Gemini 4 Argon offers two modes. Teamwork Preview uses many teams of subagents, while the /boost command works linearly and spins up subagents ad hoc. The speaker says Gemini 4 Argon is strong at long-horizon tasks.
  - _Relies on:_ Gemini 4 Argon, medium effort level used in demo; Teamwork Preview; /boost command _(as of 2026-11-19)_

## Tools, models & APIs mentioned

- **Google Antigravity** (product)
- **Gemini 4 Argon** (model)
- **Jetpack Compose** (framework)
- **SwiftUI** (framework)
- **Node.js** (framework)
- **MDN** (other)
- **GitHub** (product)

## How this applies to AX / design systems

Several Antigravity UI patterns map directly onto the AI component library and AX guidelines: the "floor manager" view of parallel workers, click-through into each subagent's conversation, a direct-message control to steer or stop a worker, and a final status/report artifact. A concrete experiment would be to run an "evergreen" subagent over the Lit/Web Components design system, using a browser-support policy config to flag polyfills and deprecated APIs that can be removed. The resulting freshness report could feed component governance dashboards. Read-only reviewer agents are also a useful pattern to document on developer portals.

_Relevance 3/5: This is primarily a coding-agent workflow demo, but its supervision patterns are useful AX reference material for Parag: a floor-manager view of workers, direct messaging to subagents, read-only tool scoping and a final report._

## Best moments

- [1:01](https://www.youtube.com/watch?v=EFejzwBLAVo&t=61s): Introduces the platform config and the custom subagents as factory lines
- [3:04](https://www.youtube.com/watch?v=EFejzwBLAVo&t=184s): Floor-manager framing and /learn for repairing workers
- [5:10](https://www.youtube.com/watch?v=EFejzwBLAVo&t=310s): Read-only tool scoping, worker observability and direct messaging to subagents
- [6:43](https://www.youtube.com/watch?v=EFejzwBLAVo&t=403s): Final report and Git-history freshness report
- [7:15](https://www.youtube.com/watch?v=EFejzwBLAVo&t=435s): Automation panel scheduling plus the Teamwork Preview and /boost modes
