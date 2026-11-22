---
title: Build the Workshop Before the Software Factory — Armin Ronacher, Earendil
channel: AI Engineer
url: https://www.youtube.com/watch?v=JNexz3Tbiu8
video_id: JNexz3Tbiu8
published: '2026-11-22'
duration: '19:56'
topics:
- coding-agents
- agents
- ux-for-ai
- mcp-tools
- infra-cost
- evals
- startups-product
relevance: 4
status: active
superseded_by: []
---

# Build the Workshop Before the Software Factory — Armin Ronacher, Earendil

[![Build the Workshop Before the Software Factory — Armin Ronacher, Earendil](../assets/thumbs/JNexz3Tbiu8.webp)](https://www.youtube.com/watch?v=JNexz3Tbiu8)

**AI Engineer** · 2026-11-22 · 19:56 · relevance 4/5 · [Watch on YouTube](https://www.youtube.com/watch?v=JNexz3Tbiu8)

## Summary

Armin Ronacher of Earendil talks about what a year of running the Pi coding agent, a harness that barely changed, taught him about working with agents. Using his own session data, he shows fewer corrections and P90 task runs growing from about 2.5 to 14+ minutes, while his prompts per day and the number of projects he actually maintains (10–15 out of 141 started) stayed flat. His argument is that human attention is the limiting factor, so builders should put quality, judgment, open formats, durable agents and code mode ahead of sheer output volume.

## Key insights

- Pi's core harness kept the same tools for a year, yet it became much more capable purely because the models improved. Earlier harness tricks, such as the PyAutoResearch goal-driving plugin, are no longer needed with current state-of-the-art models.
  - _Relies on:_ Pi coding agent core tools unchanged since December of the previous year; PyAutoResearch plugin made unnecessary by present-day models _(as of 2026-11-22)_
- In his own sessions, the P90 agent run time per task went from about 2.5 minutes with Opus 4.6 to 14+ minutes with the latest models, and he made fewer corrections with each model generation. Present-day agents also lean on Bash far more than on the other tools provided.
  - _Relies on:_ P90 run ~2.5 min with Opus 4.6 (December prior year); P90 run 14+ min with latest models; Sessions analyzed with a model called 'chef'/'Jeff' _(as of 2026-11-22)_
- Human attention stays flat while agent activity grows exponentially. He sends a steady 120–190 prompts per day, and agent active time went from less than one working day to many times his working day. He started 141 repos but regularly maintains only 10–15, and friends report a similar pattern.
  - _Relies on:_ 120–190 prompts/day; 141 projects started; 10–15 maintained regularly (commits on >5 days) _(as of 2026-11-22)_
- He stopped reading code in many cases and instead hooks into the agent's trajectory around the 70% point, before verification. There he prompts it to produce a short executive summary as a typeset HTML page, which keeps his understanding in sync with the agent.
  - _Relies on:_ Summary checkpoint triggered around 70% of trajectory, before verification _(as of 2026-11-22)_
- Durable agents should be able to suspend and resume, including their sandbox, so they can restart themselves on long overnight runs and take advantage of cheaper flex-scheduled inference, where minutes can pass with no tokens arriving.
  - _Relies on:_ Flex scheduling gives significant discount on raw token costs _(as of 2026-11-22)_
- Code mode, an idea he credits to Cloudflare, gives the agent JavaScript to run in addition to Bash, and tool calls happen through that code instead of through the context window. Combined with cheap, fast classifier or decision models at each branch, an agent can build on-demand workflows, for example triaging 3,000 support requests in a fraction of the time it previously took.
  - _Relies on:_ Code mode originated with Cloudflare; Available in Codex and Pi; Example: 3,000 customer support requests _(as of 2026-11-22)_
- Agents make it trivial to implement any file format, which risks diverging implementations, as in a recent example of a tar archive crafted so different tar implementations read it differently. He argues for shared open protocols and specs that humans agree on, rather than forks.

## Tools, models & APIs mentioned

- **Pi coding agent** (product)
- **Claude Opus** 4.6 (model)
- **PyAutoResearch** (other)
- **Codex** (product)
- **Code mode (Cloudflare)** (other)
- **Jeff/chef classifier model** (model)
- **Rust** (other)
- **GitHub** (product)

## How this applies to AX / design systems

The 70% executive-summary checkpoint is a concrete AX pattern. Parag could design a 'progress digest' component in the AI component library: a typeset summary card surfaced before verification, so supervisors can review the work without reading the code. Durable agents that suspend and resume call for status, pause/resume and long-run (14+ minute) progress UI rather than chat-style babysitting. Code mode with classifier decision points suggests a workflow visualization component that shows the branches and routing decisions, and the open-formats argument supports building framework-agnostic Lit components on shared specs.

_Relevance 4/5: The material on human attention as the bottleneck, executive-summary checkpoints for supervising agents, and suspend/resume durable agents feeds directly into AX patterns for delegation and supervision, though the talk is aimed at engineers rather than designers._

## Best moments

- [1:33](https://www.youtube.com/watch?v=JNexz3Tbiu8&t=93s): Harness unchanged for a year; models drove all the capability gains
- [3:06](https://www.youtube.com/watch?v=JNexz3Tbiu8&t=186s): P90 task duration chart: 2.5 min to 14+ min
- [6:43](https://www.youtube.com/watch?v=JNexz3Tbiu8&t=403s): 141 projects started vs 10–15 maintained
- [10:19](https://www.youtube.com/watch?v=JNexz3Tbiu8&t=619s): Executive summary HTML checkpoint at ~70% of the trajectory
- [17:30](https://www.youtube.com/watch?v=JNexz3Tbiu8&t=1050s): Code mode and classifier models for on-demand workflows
