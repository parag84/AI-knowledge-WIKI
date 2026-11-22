# Evals

> Evaluating models and agents, benchmarks, LLM-as-judge, regression testing.

_2 active · 0 stale · synthesis updated 2026-11-22_

## Current best understanding

**Evals are now running behind AI code generation (as of Nov 2026).** As agents speed up code output, quality is falling per developer and per PR. The current recommendation has two parts. First, give agents curated "golden examples" instead of letting them learn from the average of the codebase. Second, encode standards at every PDLC checkpoint rather than counting on end-of-pipeline quality gates (2026-11-08). For Parag this maps directly onto design systems. Canonical component examples, token usage rules and governance checks can work as the golden set and as continuous eval criteria for agent-generated UI in Lit and Web Components. That is more reliable than a final review step.

**Measuring impact is the least mature area.** Some organisations are experimenting with using AI itself to score the value and intent of work items, so they can route tokens and compute to the highest-value tasks (2026-11-08). This is an early form of LLM-as-judge applied to prioritisation rather than to output correctness. It is relevant to intent-driven design and to how agentic UX might show value and priority signals to the people supervising agents.

## Latest active insights

- Measuring impact remains the least mature area. Some clients are experimenting with using AI to score the value and intent of work so they can direct tokens and resources to the highest-value items. ([What AI Coding Leaders Do Differently - Martin Harrysson, Shilpa Khatana & Prakhar Dixit, McKinsey](../videos/2026-11-08-what-ai-coding-leaders-do-differently-martin-harrysson-shilp.md), 2026-11-08, relevance 3/5)
- Quality is dropping even per developer and per PR as code generation speeds up. The recommended fix is to feed agents curated 'golden examples' rather than the average of the codebase, and to encode standards at every PDLC checkpoint instead of relying on end-of-pipeline quality gates. ([What AI Coding Leaders Do Differently - Martin Harrysson, Shilpa Khatana & Prakhar Dixit, McKinsey](../videos/2026-11-08-what-ai-coding-leaders-do-differently-martin-harrysson-shilp.md), 2026-11-08, relevance 3/5)

## Open questions

- How should a design system package its golden examples (components, tokens, docs) so coding agents reliably follow them, and how is adherence measured?
- Which PDLC checkpoints, such as design handoff, PR or Storybook, can carry automated design-system conformance evals, and what tools support this for Web Components?
- Can AI scoring of work value and intent be trusted, and how would you validate an LLM-as-judge used for prioritisation rather than correctness?
- What metrics show whether agent-generated code quality is actually improving per PR over time, as regression signals rather than throughput?

## Changelog

_No changes yet._
