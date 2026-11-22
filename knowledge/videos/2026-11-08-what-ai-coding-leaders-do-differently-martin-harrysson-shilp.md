---
title: What AI Coding Leaders Do Differently - Martin Harrysson, Shilpa Khatana &
  Prakhar Dixit, McKinsey
channel: AI Engineer
url: https://www.youtube.com/watch?v=21tuT-e4NVo
video_id: 21tuT-e4NVo
published: '2026-11-08'
duration: '20:28'
topics:
- coding-agents
- agents
- startups-product
- evals
- ux-for-ai
- mcp-tools
- infra-cost
relevance: 3
status: active
superseded_by: []
---

# What AI Coding Leaders Do Differently - Martin Harrysson, Shilpa Khatana & Prakhar Dixit, McKinsey

[![What AI Coding Leaders Do Differently - Martin Harrysson, Shilpa Khatana & Prakhar Dixit, McKinsey](../assets/thumbs/21tuT-e4NVo.webp)](https://www.youtube.com/watch?v=21tuT-e4NVo)

**AI Engineer** · 2026-11-08 · 20:28 · relevance 3/5 · [Watch on YouTube](https://www.youtube.com/watch?v=21tuT-e4NVo)

## Summary

A McKinsey talk at AI Engineer on what large enterprises seeing real gains from AI coding agents do differently across operating model, talent, tech and change management. The speakers argue that the top 20 to 25% of surveyed companies get roughly 2x end-to-end improvements by redesigning the flow: one- to two-day agent loops, pods of two to four people with merged definer and builder roles, standardized artifacts, curated skills, and encoded quality, design and compliance rules. The main takeaway is that tools are largely solved, so the advantage now comes from context, curation, trust layers, shifting bottlenecks to requirements and release, and still-immature impact measurement.

## Key insights

- The top 20–25% of surveyed large enterprises are reporting 2x end-to-end improvements from AI in software development. Most companies still report modest 10–20% gains.
  - _Relies on:_ McKinsey surveyed a few hundred clients a few months before the talk; Top 20–25% of companies are seeing ~2x end-to-end improvement; An earlier survey at the end of the prior year showed meager gains _(as of 2026-11-08)_
- Leading teams replace two-week Scrum sprints with Kanban-style one- to two-day loops in which agents run the 'night shift' and humans validate. Human review checkpoints are removed once confidence in a loop is established.
  - _Relies on:_ Cycle length is one to two days instead of two-week sprints; Autonomous loops have expanded from build and test toward the product and release stages _(as of 2026-11-08)_
- Teams are shrinking to pods of two to four people with collapsed roles. Product roles move toward a 'definer' role and dev/QA roles toward a 'builder' role. In the short term, halving pod size and doubling the team count while keeping the same planning math gives a quick acceleration 'cheat code'.
  - _Relies on:_ Pod size is 2–4 people _(as of 2026-11-08)_
- Skill curation is now the hard part, not skill availability. One client found about 1,700 downloadable skills just for writing a PRD. Organizations should curate a handful that fit their context.
  - _Relies on:_ ~1,700 skills were found for the single task of writing a PRD _(as of 2026-11-08)_
- Quality is dropping even per developer and per PR as code generation speeds up. The recommended fix is to feed agents curated 'golden examples' rather than the average of the codebase, and to encode standards at every PDLC checkpoint instead of relying on end-of-pipeline quality gates.
- As build and test compress, the bottleneck shifts upstream to requirements, downstream to release, and 'sideways' to parallel teams such as risk, compliance and design. One bank's color-scheme and colorblind-accessibility rules had to be encoded into the agents.
  - _Relies on:_ Example: a bank's customer-facing app had color-scheme and colorblind accessibility rules _(as of 2026-11-08)_
- Measuring impact remains the least mature area. Some clients are experimenting with using AI to score the value and intent of work so they can direct tokens and resources to the highest-value items.

## How this applies to AX / design systems

The 'sideways bottleneck' argument supports making design-system rules (color tokens, contrast and accessibility constraints, component usage) machine-readable so coding agents can consume them. In practice that means publishing tokens and Lit component guidance as agent-facing context or skills, plus a curated set of golden-example components. The definer/builder role shift and the human-review-checkpoint pattern can inform AX dashboards where supervisors decide when to remove approval steps. For developer portals, consider a curated skills catalog page rather than an open marketplace, given the 1,700-skills paralysis example.

_Relevance 3/5: This is useful organizational background on agentic PDLC patterns, and its points on encoding design and accessibility rules and curating golden examples touch design systems, but it is high-level consulting content rather than AX design guidance._

## Best moments

- [2:38](https://www.youtube.com/watch?v=21tuT-e4NVo&t=158s): Survey data: top 20–25% of companies seeing 2x end-to-end gains
- [5:15](https://www.youtube.com/watch?v=21tuT-e4NVo&t=315s): Shift from two-week sprints to one- to two-day agent loops with human review guardrails
- [10:24](https://www.youtube.com/watch?v=21tuT-e4NVo&t=624s): Skill curation problem and the 1,700 PRD skills anecdote
- [11:58](https://www.youtube.com/watch?v=21tuT-e4NVo&t=718s): Quality decline and the use of curated golden examples
- [16:47](https://www.youtube.com/watch?v=21tuT-e4NVo&t=1007s): Design and accessibility rules as a sideways bottleneck that must be encoded into agents
