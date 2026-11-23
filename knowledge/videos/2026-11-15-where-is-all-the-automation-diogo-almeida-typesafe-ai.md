---
title: '"Where is all the automation?" — Diogo Almeida, TypeSafe AI'
channel: AI Engineer
url: https://www.youtube.com/watch?v=Cyt3LU8TyNc
video_id: Cyt3LU8TyNc
published: '2026-11-15'
duration: '23:20'
topics:
- agents
- agent-memory
- ux-for-ai
- ai-security
- evals
- model-releases
relevance: 3
status: active
superseded_by: []
---

# "Where is all the automation?" — Diogo Almeida, TypeSafe AI

[!["Where is all the automation?" — Diogo Almeida, TypeSafe AI](../assets/thumbs/Cyt3LU8TyNc.webp)](https://www.youtube.com/watch?v=Cyt3LU8TyNc)

**AI Engineer** · 2026-11-15 · 23:20 · relevance 3/5 · [Watch on YouTube](https://www.youtube.com/watch?v=Cyt3LU8TyNc)

## Summary

A CODE Summit 2026 talk by TypeSafe AI cofounder Diogo Almeida (who says he co-created ChatGPT, RLHF and InstructGPT) asking why AI is superhuman at some tasks yet fails at simple automation. He argues RLHF optimizes models for human-in-the-loop assistance rather than reliable background automation, and pitches their model Jev as 'machine native' AI that acts like a fourth 'semantic logic gate' inside software. The takeaway is that reliability, not benchmark peaks, unlocks automation, and engineers should do 'software research' with real decomposition, verification, state management, semantic types and real-time security rather than bolting chatbots onto apps.

## Key insights

- Jagged AI is explained by task type: things like deep research are intrinsically human-in-the-loop and models excel, while correctness-critical automation (accounting, drive-throughs) fails because models were optimized for pleasing a human, not doing the task.
  - _Relies on:_ Speaker claims 100% of LLMs today are optimized for assistance; RLVR models are described as bad to interact with unless also RLHF'd _(as of 2026-11-15)_
- Reliability is framed as 'Einstein 95% of the time, Mr. Bean 5%': if you can't tell which output is which, you can't automate, so narrow, extremely reliable intelligence beats occasional brilliance that must be verified.
- The 'bitterest lesson' is choosing the right training task: the RLHF paper showed a GPT-2-sized model with instruction-following training matched what would need roughly 'GPT-7 to 9' scale pretraining alone.
  - _Relies on:_ Claim from RLHF/InstructGPT work: GPT-2 sized model with RLHF vs. GPT-7 to 9 equivalent pretraining on instruction following _(as of 2026-11-15)_
- Treat LLM calls as a fourth 'semantic logic gate' embedded in software's inner loop (e.g., 'is this a real-looking Gmail address' instead of a regex) rather than a chatbot to the side that can't make costly decisions.
- Agent designs are constrained by the 'tyranny of the KV cache': shared state across parallel sub-agents, non-O(N) memory via map-reduce over history, and smarter sub-agent routing are open problems because they fight KV cache efficiency.
- Real-time AI security monitoring is argued to be feasible because detecting misbehavior is easier than doing it; the blocker is that monitors haven't been fast, cheap and reliable enough to run inline.
  - _Relies on:_ References an OpenAI / Hugging Face sandbox incident _(as of 2026-11-15)_
- Slop stems from unreliability: since AI can't be trusted with decisions that cost the operator, its costs get externalized onto recipients; reliable models could curb things like 'inbound hell'.

## Tools, models & APIs mentioned

- **Jev** (model)
- **ChatGPT** (product)
- **InstructGPT** (model)
- **o3** (model)
- **GPT-2** (model)
- **GPT-3** (model)
- **BERT** (model)
- **TypeSafe AI** (product)

## How this applies to AX / design systems

The assistance-vs-automation split is a useful lens for AX: classify each agent task by whether a human verifies output and design approval/review UI accordingly, rather than assuming chat. The 'semantic logic gate' idea suggests embedding small inline AI checks inside components (e.g., semantic form validation in a Lit input component) instead of a side chatbot. Semantic typing/lint ideas could inspire AI-based design-token or component-usage linting in the design system.

_Relevance 3/5: Useful framing on assistance vs. automation and reliability that informs how much human supervision AX should design for, but it is a conceptual pitch with no concrete UX patterns._

## Best moments

- [2:38](https://www.youtube.com/watch?v=Cyt3LU8TyNc&t=158s): Framing of jagged AI: superhuman at math, useless at accounting
- [4:10](https://www.youtube.com/watch?v=Cyt3LU8TyNc&t=250s): Argument that RLHF builds in human-in-the-loop dependence
- [9:27](https://www.youtube.com/watch?v=Cyt3LU8TyNc&t=567s): Einstein 95% / Mr. Bean 5% reliability framing
- [16:16](https://www.youtube.com/watch?v=Cyt3LU8TyNc&t=976s): Tyranny of the KV cache, shared agent memory and sub-agent routing ideas
- [17:05](https://www.youtube.com/watch?v=Cyt3LU8TyNc&t=1025s): Semantic logic gate example and LED analogy payoff
