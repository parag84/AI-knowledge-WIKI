---
title: Your SKILL.md Is 70% Stuff the Model Already Knows - Nikolay Petrov, Intel
channel: AI Engineer
url: https://www.youtube.com/watch?v=yzx4IuEh_tU
video_id: yzx4IuEh_tU
published: '2026-11-11'
duration: '14:01'
topics:
- evals
- agent-memory
- coding-agents
- mcp-tools
- model-releases
- infra-cost
relevance: 3
status: active
superseded_by: []
---

# Your SKILL.md Is 70% Stuff the Model Already Knows - Nikolay Petrov, Intel

[![Your SKILL.md Is 70% Stuff the Model Already Knows - Nikolay Petrov, Intel](../assets/thumbs/yzx4IuEh_tU.webp)](https://www.youtube.com/watch?v=yzx4IuEh_tU)

**AI Engineer** · 2026-11-11 · 14:01 · relevance 3/5 · [Watch on YouTube](https://www.youtube.com/watch?v=yzx4IuEh_tU)

## Summary

A short AI Engineer talk by Nikolay Petrov (Intel) on measuring what an agent skill (SKILL.md) actually teaches a model versus what the model already knows. He splits a skill into ~25–30 checkable items (propositions or contracts with Q&A pairs), runs each with and without the skill, and uses an LLM judge to sort items into already-known, harmful, newly taught, or still-missed. The takeaway: most skill content is redundant general knowledge, while the real value sits in exact details (keys, parameters, values), so use this novelty map as a starting vector for trimming, then confirm with task-level evals.

## Key insights

- Evaluate a skill with two arms (no skill vs skill loaded) on deterministic task evals, comparing tasks solved plus token and time cost. In the example, the skill lifted results from 3/5 to 5/5 tasks.
  - _Relies on:_ example: 3/5 tasks solved without skill, 5/5 with skill _(as of 2026-11-11)_
- Decompose a skill into roughly 25–30 FactScore-style items, each a question/answer pair, either a general proposition or a stricter 'contract'. Ask each question with and without the skill and grade with a judge from a different model family, or a panel, while making sure questions don't leak answers.
  - _Relies on:_ ~25-30 items per skill; based on FactScore item idea; judge ideally a different model family or panel _(as of 2026-11-11)_
- Results form a 2x2 matrix: known without the skill (redundant), correct without but wrong with the skill (harmful), wrong without but correct with (actual teaching), and wrong in both (poorly written). Harmful items are the easiest fix and are rare in popular skills, about 1 of roughly 400 items in Anthropic's skills, but more common in smaller ones.
  - _Relies on:_ ~1 harmful item out of ~400 items in Anthropic skills _(as of 2026-11-11)_
- The first skill tested was about 70% knowledge the model already had. Lenient grading (general idea) and strict grading (exact details) diverge sharply: Opus understood about 70% of a skill's content at the general level but only about 22% of its specific details. So keep exact parameters and values and cut generic explanation.
  - _Relies on:_ Opus: ~70% lenient vs ~22% strict understanding; first tested skill ~70% already-known content _(as of 2026-11-11)_
- The novelty analysis is cheap. Running it for 29 skills cost about $14 in Sonnet and Haiku calls, with Sonnet as the judge.
  - _Relies on:_ 29 skills for ~$14; Sonnet and Haiku as subjects, Sonnet as judge _(as of 2026-11-11)_
- Novelty is only a starting vector for optimization. After removing already-known items, re-run the task evals, and keep the shorter skill only if scores hold, which saves tokens and context. Smaller models know less of a skill's content, so test across model families.

## Tools, models & APIs mentioned

- **Claude Sonnet** (model)
- **Claude Haiku** (model)
- **Claude Opus** (model)
- **Anthropic Skills (SKILL.md)** (other)
- **FactScore** (other)
- **AGENTS.md** (other)
- **MCP** (protocol)
- **docume (comparison framework, name as transcribed)** (framework)

## How this applies to AX / design systems

If Parag's team writes skills or AGENTS.md files that teach coding agents the design system (Lit component APIs, token names, usage rules), this method shows which lines matter. Those are likely the exact token keys, attribute names and prop values, while generic accessibility or Web Components advice is probably already known to the model. A concrete experiment: split a design-system skill into Q&A items, run it with and without the skill on Sonnet/Haiku, and trim the redundant parts. The same with/without approach could also check whether developer-portal docs written for agents are actually adding knowledge.

_Relevance 3/5: Useful method for anyone authoring agent skills or AGENTS.md-style context (including design-system skills for coding agents), but it is eval methodology rather than AX or UI design._

## Best moments

- [1:34](https://www.youtube.com/watch?v=yzx4IuEh_tU&t=94s): Two-arm eval setup, with vs without the skill
- [4:12](https://www.youtube.com/watch?v=yzx4IuEh_tU&t=252s): Splitting a skill into FactScore-style items: propositions vs contracts
- [5:47](https://www.youtube.com/watch?v=yzx4IuEh_tU&t=347s): The four-quadrant knows/doesn't-know matrix
- [9:25](https://www.youtube.com/watch?v=yzx4IuEh_tU&t=565s): Lenient vs strict grading; Opus drops from 70% to 22%
- [12:03](https://www.youtube.com/watch?v=yzx4IuEh_tU&t=723s): Using novelty to trim a skill, then validating with evals
