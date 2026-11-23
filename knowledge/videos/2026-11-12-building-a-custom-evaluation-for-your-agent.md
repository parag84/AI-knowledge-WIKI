---
title: Building a custom evaluation for your agent
channel: Google Cloud Tech
url: https://www.youtube.com/watch?v=GatM9XV0gOw
video_id: GatM9XV0gOw
published: '2026-11-12'
duration: '13:02'
topics:
- evals
- agents
- mcp-tools
- infra-cost
relevance: 3
status: active
superseded_by: []
---

# Building a custom evaluation for your agent

[![Building a custom evaluation for your agent](../assets/thumbs/GatM9XV0gOw.webp)](https://www.youtube.com/watch?v=GatM9XV0gOw)

**Google Cloud Tech** · 2026-11-12 · 13:02 · relevance 3/5 · [Watch on YouTube](https://www.youtube.com/watch?v=GatM9XV0gOw)

## Summary

A Google Cloud Tech tutorial by Annie Wang showing how to define, build, validate and automate a custom evaluation for an AI agent using Google's Agent Development Kit (ADK). Using a group dinner-planning agent as the example, it contrasts comparators (match against reference answers in a golden dataset) with checkers (verify per-person requirements), and deterministic code with LLM-as-judge, then builds an 'everyone eats' Python metric wired into ADK eval, ADK Web and pytest. The main takeaway is to define success per task, test the evaluator itself on known answers, and make the eval a required CI/CD gate before deployment.

## Key insights

- For tasks with many valid outputs, use requirement-based checkers instead of reference comparators: encode each constraint as a check so any plan satisfying all constraints passes without enumerating every acceptable answer.
  - _Relies on:_ Comparators score against a golden dataset of trusted reference answers; Checkers apply requirements to plans not listed in advance _(as of 2026-11-12)_
- What you evaluate against (reference vs requirements) is a separate decision from how you evaluate (deterministic code vs LLM judge); use code when facts are structured yes/no and an LLM judge with a rubric for interpretive qualities like explanation clarity, validated against reviewed examples.
  - _Relies on:_ ADK includes rubric-based model judges for responses, tool use and multi-turn conversations _(as of 2026-11-12)_
- ADK's built-in metrics include wording-overlap against a reference, LLM semantic comparison, and tool trajectory matching of actual vs expected tool calls including arguments, with configurable call-order strictness.
  - _Relies on:_ Agent Development Kit (ADK) built-in evaluation metrics; Trajectory = sequence of tool calls _(as of 2026-11-12)_
- The custom 'everyone eats' metric scores the fraction of group members whose diet, allergy, budget, distance, spice and timing requirements are met, with threshold 1.0; missing or invalid fields in the agent's JSON output fail outright so the evaluator never fills gaps.
  - _Relies on:_ 6-person group, 3 satisfied = 0.5 score, fails threshold of 1; Custom metric is a Python function returning an EvaluationResult; per-person reasons go to a separate detail file; Registered via an evaluation config JSON with criteria and custom metrics sections _(as of 2026-11-12)_
- Test the evaluator before trusting it: feed known cases (partial plan should score 0.5 and fail, two different valid plans should both score 1, incomplete answers fail).
- Run the same eval set and config via adk eval CLI, ADK Web's Eval tab, or pytest calling ADK's agent evaluator, and add the pytest command as a required CI/CD check so failing versions don't deploy; repeat important cases since one run doesn't show consistency.
  - _Relies on:_ adk eval command takes agent, eval config JSON and eval set JSON; ADK Web browser interface lists registered custom metrics; pytest with ADK AgentEvaluator _(as of 2026-11-12)_

## Tools, models & APIs mentioned

- **Agent Development Kit (ADK)** (framework)
- **ADK Web** (product)
- **adk eval** (other)
- **pytest** (framework)

## How this applies to AX / design systems

The comparator-vs-checker framing and per-person failure reasons map well to an eval-results UI component in an AI component library: score, threshold, pass/fail, and expandable per-requirement explanations. ADK Web's Eval tab (metric picker, threshold, inspect evaluated conversation) is a reference pattern for designing eval dashboards in a developer portal. The 'define what success means' step is also a useful AX exercise for specifying what supervisors need to see to trust an agent's trajectory.

_Relevance 3/5: Solid background on how agent success is defined and checked, which informs AX trust and developer-portal eval docs, but it is engineering-focused rather than about UX or design systems._

## Best moments

- [0:31](https://www.youtube.com/watch?v=GatM9XV0gOw&t=31s): Restaurant example framing what 'success' means, including trajectory and multi-turn tracking
- [5:09](https://www.youtube.com/watch?v=GatM9XV0gOw&t=309s): Clear separation of what-to-check (comparator/checker) vs how-to-check (code/LLM judge)
- [6:12](https://www.youtube.com/watch?v=GatM9XV0gOw&t=372s): 'Everyone eats' metric definition and scoring
- [8:19](https://www.youtube.com/watch?v=GatM9XV0gOw&t=499s): Validating the evaluator itself with known-outcome answers
- [10:25](https://www.youtube.com/watch?v=GatM9XV0gOw&t=625s): ADK Web Eval tab UI for running and inspecting evaluations
