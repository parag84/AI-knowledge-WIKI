---
title: Building the Claude API for the frontier
channel: Claude
url: https://www.youtube.com/watch?v=p2xvJAbF-i4
video_id: p2xvJAbF-i4
published: '2026-11-12'
duration: '18:30'
topics:
- agents
- infra-cost
- evals
- model-releases
- ai-security
- agent-memory
- mcp-tools
relevance: 3
status: active
superseded_by: []
---

# Building the Claude API for the frontier

[![Building the Claude API for the frontier](../assets/thumbs/p2xvJAbF-i4.webp)](https://www.youtube.com/watch?v=p2xvJAbF-i4)

**Claude** · 2026-11-12 · 18:30 · relevance 3/5 · [Watch on YouTube](https://www.youtube.com/watch?v=p2xvJAbF-i4)

## Summary

A conversation between two Anthropic Claude Platform staff, Jake Dejno and Lucca Siaudzionis, about how the Messages API evolves alongside each model release. They cover how research and customer requests become API knobs, how to change effort and system prompts mid-conversation without breaking prompt caching, how model strings act as implicit versioning with soft deprecations, how to think about cost per task rather than cost per token, and how Mythos and Fable share weights but carry different safeguards. The main takeaway is that developers should put prompt caching first, re-run their own evals and re-examine their harness on every model upgrade, and lean on API knobs rather than prompting alone.

## Key insights

- Changing effort or the system prompt mid-conversation used to break prompt caching. The API now lets agentic flows lower effort for an easier next step without losing the cache.
  - _Relies on:_ Changing effort mid-conversation is in beta; Applies to effort and system prompts in the Messages API _(as of 2026-11-12)_
- Prompt caching is the first cost recommendation given to every customer, and the target is to get cache rates up to about 90%. Agentic turns that append to prior requests reuse the blocks that already ran.
  - _Relies on:_ Target prompt caching rate of up to 90% _(as of 2026-11-12)_
- Measure cost per task, which includes intelligence per token, rather than cost per token alone. A pricier, smarter model can use far fewer tokens or solve tasks a cheaper model can't, and over time a lower tier may become good enough for a workflow.
  - _Relies on:_ Examples given: Haiku, Sonnet, Opus 5, Fable 5 _(as of 2026-11-12)_
- The model string works as an implicit version. Deprecations are softened by keeping the old behaviour toggleable for a model or two and by offering beta headers for rollback, as was done when moving from extended thinking to adaptive thinking.
  - _Relies on:_ Migration from extended thinking to adaptive thinking; Beta headers allow rolling back to previous behaviour _(as of 2026-11-12)_
- Re-evaluate your harness with your own evals on every model upgrade, because scaffolding built for weaker models can become a limitation on much smarter ones. Anthropic itself re-tests shelved features against each new model to see whether they now clear its quality bar.
- Mythos and Fable use the same model weights but run with different classifier safeguards. Mythos access goes through a KYC-style Cyber Verification Program, and new thinking protections were added to prevent distillation.
  - _Relies on:_ Claude Mythos access is through the Cyber Verification Program; Fable is available without KYC; Thinking protections were documented as anti-distillation measures _(as of 2026-11-12)_
- Claude Managed Agents is built on top of the Messages API. Anthropic also provides client-side tools such as bash and text editor that developers can use in place of their own.
  - _Relies on:_ Claude Managed Agents is in beta; Client-side tools include bash and text editor _(as of 2026-11-12)_

## Tools, models & APIs mentioned

- **Claude Messages API** (api)
- **Claude Managed Agents** (product)
- **Claude Mythos** (model)
- **Fable** 5 (model)
- **Claude Opus** 5 (model)
- **Claude Haiku** (model)
- **Claude Sonnet** (model)
- **Claude Code** (product)
- **Computer use tool** (api)
- **Bash tool** (api)
- **Text editor tool** (api)

## How this applies to AX / design systems

For developer portals, the video suggests doc pages that frame model strings as versions, explain soft deprecations and beta-header rollbacks, and include a cost-per-task explainer that places prompt caching up front. In AX, an effort control that changes mid-conversation implies a UI where users or agents can step effort down for easy steps, so it is worth prototyping an effort or cost indicator on agent runs. Overall it is mostly platform context and has limited direct impact on component or design-system work.

_Relevance 3/5: This is useful background on API knobs, versioning and agent abstractions that sit behind AI developer portals and agent UI, but it covers no UX or design-system patterns directly._

## Best moments

- [2:32](https://www.youtube.com/watch?v=p2xvJAbF-i4&t=152s): Changing effort and the system prompt mid-conversation without breaking the cache
- [6:43](https://www.youtube.com/watch?v=p2xvJAbF-i4&t=403s): Implicit versioning and the soft migration from extended thinking to adaptive thinking
- [8:48](https://www.youtube.com/watch?v=p2xvJAbF-i4&t=528s): Prompt caching explained and the target of a 90% cache rate
- [9:20](https://www.youtube.com/watch?v=p2xvJAbF-i4&t=560s): Cost per task versus cost per token, and intelligence per token
- [12:24](https://www.youtube.com/watch?v=p2xvJAbF-i4&t=744s): Mythos versus Fable: same weights, different safeguards
