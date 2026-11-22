# UX for AI

> Interaction design for AI and agentic products, trust, transparency, generative UI, AX.

_2 active · 0 stale · synthesis updated 2026-11-22_

## Current best understanding

As of November 2026, agentic software delivery is moving the bottleneck away from build and test. Leading teams are replacing two-week Scrum sprints with Kanban-style loops of one to two days. Agents run the "night shift" and humans validate the results. Once a team trusts a loop, it removes the human review checkpoints. Autonomous loops are also spreading beyond build and test into the product and release stages.

For Parag, the key point is that design becomes a "sideways" constraint that has to be encoded into agents. One bank had to put its color-scheme and colorblind-accessibility rules into its agents for a customer-facing app (2026-11-08). This makes machine-readable design systems, tokens and accessibility rules part of the agent's working context. They are no longer just documentation for humans. It also makes supervision UX central: how people validate agent output overnight, and how they decide when a loop has earned enough trust to drop a checkpoint.

## Latest active insights

- As build and test compress, the bottleneck shifts upstream to requirements, downstream to release, and 'sideways' to parallel teams such as risk, compliance and design. One bank's color-scheme and colorblind-accessibility rules had to be encoded into the agents. ([What AI Coding Leaders Do Differently - Martin Harrysson, Shilpa Khatana & Prakhar Dixit, McKinsey](../videos/2026-11-08-what-ai-coding-leaders-do-differently-martin-harrysson-shilp.md), 2026-11-08, relevance 3/5)
- Leading teams replace two-week Scrum sprints with Kanban-style one- to two-day loops in which agents run the 'night shift' and humans validate. Human review checkpoints are removed once confidence in a loop is established. ([What AI Coding Leaders Do Differently - Martin Harrysson, Shilpa Khatana & Prakhar Dixit, McKinsey](../videos/2026-11-08-what-ai-coding-leaders-do-differently-martin-harrysson-shilp.md), 2026-11-08, relevance 3/5)

## Open questions

- How should design-system rules, such as tokens and accessibility constraints, be packaged so agents reliably follow them? Options include linters, MCP resources or prompt context.
- What signals or metrics justify removing human review checkpoints from an agent loop, and how should that trust threshold be shown in the UI?
- How do design and compliance teams keep up with one- to two-day cycles without becoming the new bottleneck?
- What does an effective review surface look like for humans validating overnight agent output?

## Changelog

_No changes yet._
