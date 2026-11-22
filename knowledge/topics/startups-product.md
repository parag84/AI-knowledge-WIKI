# Startups & product

> Product strategy, go-to-market, case studies, building AI companies.

_12 active · 0 stale · synthesis updated 2026-11-22_

## Current best understanding

**Building with agents: simple, shared and spec-driven beats clever (Nov 2026).** Lovable (formerly GPT Engineer) found that its 2023 multi-agent setup, an orchestrator spawning front-end and back-end specialists, made the product worse. In late 2024 it reverted to one main LLM plus small retrieval LLMs, which was more responsive and reliable. Multi-agent only paid off once model intelligence caught up.

Ramp runs one shared, company-wide coding agent, Inspect, started about a year ago. It now writes and ships about 75% of Ramp's code. Because improvements reach everyone invisibly and nobody pays a per-person setup cost, Ramp never had to mandate it. This argues for platform-level agent baselines over per-user configuration, and the same logic applies to design-system tooling and developer portals.

A counter-risk: agents make it trivial to implement any file format, which invites divergent implementations, such as a tar archive that different tar tools read differently. The argument is for shared, human-agreed open protocols and specs instead of forks.

**Productivity and org shape.** Reported gains vary widely:
- A McKinsey survey (cited Nov 8, 2026) found the top 20–25% of large enterprises report about 2x end-to-end gains from AI in software development, while most report only 10–20%.
- Outlier firms claim far more. Cognition reports merged PRs up 40x in about 12 months against 2.7x headcount growth, which it frames as more than 10x per engineer.
- Google says AI writes about 75% of its new code. Its release cadence (six Gemini releases in 16 weeks) comes from serving post-training candidates to 100k+ engineers via blind battles and silent routing in Antigravity, then feeding failures back as training tasks.

Teams are collapsing into pods of 2–4, with product roles becoming 'definers' and dev/QA roles becoming 'builders'.

**Frontier-lab context (Nov 19, 2026).** Anthropic is a public benefit corporation (since Jan 2021), so its mission can outrank profit. It says it caught up from behind the frontier through compute plus algorithmic multipliers (Claude 3 Opus, then Sonnet 3.5). It released the vulnerability-finding model Mythos only to selected defenders via Project Glasswing, and reports Claude-assisted biology discoveries.

## Latest active insights

- Agents make it trivial to implement any file format, which risks diverging implementations, as in a recent example of a tar archive crafted so different tar implementations read it differently. He argues for shared open protocols and specs that humans agree on, rather than forks. ([Build the Workshop Before the Software Factory — Armin Ronacher, Earendil](../videos/2026-11-22-build-the-workshop-before-the-software-factory-armin-ronache.md), 2026-11-22, relevance 4/5)
- Running one shared, company-wide coding agent as a solid baseline spreads improvements to everyone invisibly and removes per-person setup cost, so Ramp never needed to mandate its use. ([How to build an agent that builds the culture — Zach Bruggeman, Ramp](../videos/2026-11-20-how-to-build-an-agent-that-builds-the-culture-zach-bruggeman.md), 2026-11-20, relevance 4/5)
- Anthropic reports using Claude in biology work, including what looks like a newly discovered gene-editing mechanism, and expects dozens of such discoveries per month within a few months. ([The making of Anthropic](../videos/2026-11-19-the-making-of-anthropic.md), 2026-11-19, relevance 2/5)
- Mythos, a model with expert-level ability to find software vulnerabilities and exploits, was released through Project Glasswing only to a limited set of companies, so cyberdefenders could find and patch vulnerabilities while broader safeguards were built. ([The making of Anthropic](../videos/2026-11-19-the-making-of-anthropic.md), 2026-11-19, relevance 2/5)
- The founders say Claude was far behind the frontier at public launch. Competitiveness came from compute plus stacked algorithmic 'compute multipliers', leading to Claude 3 Opus and then Sonnet 3.5, which made models useful for programming. ([The making of Anthropic](../videos/2026-11-19-the-making-of-anthropic.md), 2026-11-19, relevance 2/5)
- Anthropic chose to incorporate as a public benefit corporation so that the mission can outrank profit or shareholder value in specific decisions. ([The making of Anthropic](../videos/2026-11-19-the-making-of-anthropic.md), 2026-11-19, relevance 2/5)
- Lovable's 2023 multi-agent framework (orchestrator spawning specialist front-end/back-end agents) made the product worse; reverting to one main LLM plus small retrieval LLMs in late 2024 was more responsive and reliable. Multi-agent only worked once model intelligence caught up. ([What it takes to set intelligence free — Fabian Hedin, CTO, Lovable](../videos/2026-11-19-what-it-takes-to-set-intelligence-free-fabian-hedin-cto-lova.md), 2026-11-19, relevance 4/5)
- Release speed comes from serving post-training candidates to 100,000+ Google engineers via blind battles and silent routing to experimental models, feeding failures back as new training tasks. ([Post-Training Gemini 4 for Real Engineering Work — Melvin Johnson, Google DeepMind](../videos/2026-11-18-post-training-gemini-4-for-real-engineering-work-melvin-john.md), 2026-11-18, relevance 3/5)
- Cognition reports merged PR throughput grew 40x over roughly 12 months while engineering headcount grew 2.7x, which the speaker frames as each engineer being more than 10x more productive at equal or higher PR quality. ([40x More Merged PRs With 2.7x the Engineers — Walden Yan, CPO, Cognition](../videos/2026-11-18-40x-more-merged-prs-with-2-7x-the-engineers-walden-yan-cpo-c.md), 2026-11-18, relevance 4/5)
- Treating the assistant as a season-long companion, combined with tracking everything, produced a protocol she plans to reuse in future years, plus an earlier harvest from stronger planting material. ([A season on the farm with AI](../videos/2026-11-17-a-season-on-the-farm-with-ai.md), 2026-11-17, relevance 1/5)
- Teams are shrinking to pods of two to four people with collapsed roles. Product roles move toward a 'definer' role and dev/QA roles toward a 'builder' role. In the short term, halving pod size and doubling the team count while keeping the same planning math gives a quick acceleration 'cheat code'. ([What AI Coding Leaders Do Differently - Martin Harrysson, Shilpa Khatana & Prakhar Dixit, McKinsey](../videos/2026-11-08-what-ai-coding-leaders-do-differently-martin-harrysson-shilp.md), 2026-11-08, relevance 3/5)
- The top 20–25% of surveyed large enterprises are reporting 2x end-to-end improvements from AI in software development. Most companies still report modest 10–20% gains. ([What AI Coding Leaders Do Differently - Martin Harrysson, Shilpa Khatana & Prakhar Dixit, McKinsey](../videos/2026-11-08-what-ai-coding-leaders-do-differently-martin-harrysson-shilp.md), 2026-11-08, relevance 3/5)

## Open questions

- Are 10x+ per-engineer claims (Cognition) and ~75% AI-written code (Ramp, Google) reproducible beyond AI-native firms, given McKinsey's finding that most enterprises see only 10–20%?
- When do multi-agent architectures beat a single strong LLM plus retrieval for product UX, now that models have improved since Lovable's 2024 reversal?
- Will shared company-wide agents become the default over individual tool choice, and what governance or design-system role does that create?
- How will 'definer' vs 'builder' roles in 2–4 person pods reshape where UX and design-system work sits?
- Can open specs and protocols keep pace when agents make bespoke format implementations nearly free?

## Changelog

_No changes yet._
