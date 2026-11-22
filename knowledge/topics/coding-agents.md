# Coding agents

> AI coding assistants and agents (Claude Code, Codex, Gemini CLI, etc.), dev workflows.

_6 active · 0 stale · synthesis updated 2026-11-22_

## Current best understanding

**Where the bottleneck moves (as of Nov 2026):** As coding agents compress build and test, the constraint shifts upstream to requirements, downstream to release, and sideways to parallel functions like risk, compliance and **design**. One bank had to encode its customer-app color-scheme and colorblind-accessibility rules directly into its agents. For Parag, design standards and tokens become agent inputs, not just human guidelines. Quality is also dropping per developer and per PR as generation speeds up. The recommended fix is to feed agents curated **golden examples** rather than the codebase average. Teams should also encode standards at every PDLC checkpoint instead of relying on end-of-pipeline gates. That is a strong argument for well-governed reference components and machine-readable design-system rules.

**Curation over availability:** Skills are abundant but noisy. One client found about 1,700 downloadable skills just for writing a PRD. The advice is for organizations to curate a small set that fits their context, a governance problem much like component-library curation.

**Workflow and org shape (McKinsey, Nov 2026):** The top 20–25% of surveyed large enterprises report about 2x end-to-end gains from AI in software development. Most still see 10–20%. Leading teams swap two-week sprints for Kanban-style one- to two-day loops in which agents run the "night shift" and humans validate. Review checkpoints are removed once confidence in a loop is established. Autonomous loops are expanding from build and test into the product and release stages. Pods shrink to 2–4 people with collapsed roles: product moves toward "definers" and dev/QA toward "builders". Halving pod size and doubling team count is cited as a short-term acceleration trick.

## Latest active insights

- As build and test compress, the bottleneck shifts upstream to requirements, downstream to release, and 'sideways' to parallel teams such as risk, compliance and design. One bank's color-scheme and colorblind-accessibility rules had to be encoded into the agents. ([What AI Coding Leaders Do Differently - Martin Harrysson, Shilpa Khatana & Prakhar Dixit, McKinsey](../videos/2026-11-08-what-ai-coding-leaders-do-differently-martin-harrysson-shilp.md), 2026-11-08, relevance 3/5)
- Quality is dropping even per developer and per PR as code generation speeds up. The recommended fix is to feed agents curated 'golden examples' rather than the average of the codebase, and to encode standards at every PDLC checkpoint instead of relying on end-of-pipeline quality gates. ([What AI Coding Leaders Do Differently - Martin Harrysson, Shilpa Khatana & Prakhar Dixit, McKinsey](../videos/2026-11-08-what-ai-coding-leaders-do-differently-martin-harrysson-shilp.md), 2026-11-08, relevance 3/5)
- Skill curation is now the hard part, not skill availability. One client found about 1,700 downloadable skills just for writing a PRD. Organizations should curate a handful that fit their context. ([What AI Coding Leaders Do Differently - Martin Harrysson, Shilpa Khatana & Prakhar Dixit, McKinsey](../videos/2026-11-08-what-ai-coding-leaders-do-differently-martin-harrysson-shilp.md), 2026-11-08, relevance 3/5)
- Teams are shrinking to pods of two to four people with collapsed roles. Product roles move toward a 'definer' role and dev/QA roles toward a 'builder' role. In the short term, halving pod size and doubling the team count while keeping the same planning math gives a quick acceleration 'cheat code'. ([What AI Coding Leaders Do Differently - Martin Harrysson, Shilpa Khatana & Prakhar Dixit, McKinsey](../videos/2026-11-08-what-ai-coding-leaders-do-differently-martin-harrysson-shilp.md), 2026-11-08, relevance 3/5)
- Leading teams replace two-week Scrum sprints with Kanban-style one- to two-day loops in which agents run the 'night shift' and humans validate. Human review checkpoints are removed once confidence in a loop is established. ([What AI Coding Leaders Do Differently - Martin Harrysson, Shilpa Khatana & Prakhar Dixit, McKinsey](../videos/2026-11-08-what-ai-coding-leaders-do-differently-martin-harrysson-shilp.md), 2026-11-08, relevance 3/5)
- The top 20–25% of surveyed large enterprises are reporting 2x end-to-end improvements from AI in software development. Most companies still report modest 10–20% gains. ([What AI Coding Leaders Do Differently - Martin Harrysson, Shilpa Khatana & Prakhar Dixit, McKinsey](../videos/2026-11-08-what-ai-coding-leaders-do-differently-martin-harrysson-shilp.md), 2026-11-08, relevance 3/5)

## Open questions

- How should design-system rules (tokens, accessibility, brand) be packaged so coding agents reliably apply them? Options include skills, golden examples and lint checkpoints.
- When human review checkpoints are removed from agent loops, what supervision and audit UX keeps trust and catches quality regressions?
- Where do designers sit in 2–4 person definer/builder pods? Are they definers, or a 'sideways' bottleneck function?
- Will the 2x gains reported by top enterprises spread, or do the declining per-PR quality trends cap them?
- Who curates and governs organizational skill libraries, and will standard registries emerge?

## Changelog

_No changes yet._
