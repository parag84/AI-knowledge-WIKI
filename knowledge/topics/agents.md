# Agents

> Agent architectures, planning, memory, multi-agent orchestration, agent frameworks.

_2 active · 0 stale · synthesis updated 2026-11-22_

## Current best understanding

**Agentic delivery is moving the bottleneck onto design and governance (as of Nov 2026).** As agents compress build and test, constraints move upstream to requirements, downstream to release, and "sideways" to parallel functions such as risk, compliance and design. In one bank's customer-facing app, the color scheme and colorblind-accessibility rules had to be encoded directly into the agents. For Parag, this means design-system rules, tokens and accessibility constraints are becoming machine-consumable inputs to agent loops, not just documentation for humans.

**Operating model: short loops with human validation (Nov 2026).** Leading teams are replacing two-week Scrum sprints with Kanban-style one- to two-day loops. Agents run the "night shift" and humans validate the results. Autonomous loops are expanding from build and test toward product and release stages. Human review checkpoints are removed once a loop has earned confidence. This has direct AX implications: the supervision and approval UI has to support checkpoints that can be added, relaxed and eventually retired as trust grows.

## Latest active insights

- As build and test compress, the bottleneck shifts upstream to requirements, downstream to release, and 'sideways' to parallel teams such as risk, compliance and design. One bank's color-scheme and colorblind-accessibility rules had to be encoded into the agents. ([What AI Coding Leaders Do Differently - Martin Harrysson, Shilpa Khatana & Prakhar Dixit, McKinsey](../videos/2026-11-08-what-ai-coding-leaders-do-differently-martin-harrysson-shilp.md), 2026-11-08, relevance 3/5)
- Leading teams replace two-week Scrum sprints with Kanban-style one- to two-day loops in which agents run the 'night shift' and humans validate. Human review checkpoints are removed once confidence in a loop is established. ([What AI Coding Leaders Do Differently - Martin Harrysson, Shilpa Khatana & Prakhar Dixit, McKinsey](../videos/2026-11-08-what-ai-coding-leaders-do-differently-martin-harrysson-shilp.md), 2026-11-08, relevance 3/5)

## Open questions

- What format works best for encoding design-system and accessibility rules so agents reliably follow them (tokens, lint rules, structured specs, MCP-exposed guidelines)?
- What concrete signals or metrics justify removing a human review checkpoint from an agent loop, and how is that trust revoked when quality regresses?
- How should design, risk and compliance teams participate in one- to two-day agent loops without becoming the new bottleneck?
- As autonomous loops extend into product and release stages, what remains a mandatory human decision point?

## Changelog

_No changes yet._
