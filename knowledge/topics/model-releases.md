# Model releases

> New model launches, capabilities, versions, deprecations, API changes.

_15 active · 0 stale · synthesis updated 2026-11-22_

## Current best understanding

**Frontier, as of Nov 2026.** Long-horizon, "Fable class" agentic models are now the frontier. Simon Willison (2026-11-17) defines them as models that, given a clear goal and the right tools, will grind through roughly 12-hour runs until the goal is solved. He places Claude Fable 5–5.2, GPT-6 Astra and Gemini 4 Carbon in this class, and calls Claude Opus 5.5 his "cheap Fable" daily driver. The design implication for agentic UX is that the human's main job shifts to defining the problem, provisioning tools and supervising long runs.

- **Gemini 4 family:**
  - Carbon is claimed #1 on Cursor Bench at 3.3x lower cost than the runner-up, and on Zapier Automation Bench at 2x lower cost per task. That makes cost-per-task a headline metric.
  - Argon targets long-horizon work, with Teamwork Preview (teams of subagents) and /boost (linear, spins up subagents ad hoc).
  - Hydrogen (2026-11-18) is the fast tier: about 60% vs about 20% for Gemini 3.8 Flash on Terminal Bench 4, at about 3x the speed, across the API, the Gemini app, Search and Antigravity.
- **OpenAI:** Ultrafast mode for GPT-6.1 Sol and GPT-6 Astra (Dev Day, Oct 2026) is about 8x faster at 6x the cost. It suits UI iteration against a hot-reloading dev server with light reasoning effort, and helps little when build or test time dominates.

**On-device and browser.** This matters for Lit / Web Component AI libraries. Gemma 4 (Nov 2026) ships in 2B, 4B, 12B, 26B MoE (4B active) and 31B sizes; only 2B and 4B accept audio. LiteRT.js (general ML such as embeddings) and LiteRT-LM.js (LLMs, Gemma-focused) run on WebGPU and Wasm as a plain JS import, needing fewer than 20 lines to run Gemma 4. Models up to 31B have been run in the browser, and WebNN (NPU access) is in preview. Dynamic, layer-aware quantization (e.g. Unsloth) keeps 4-bit models usable: GLM 5.3 at 4-bit retains about 94% accuracy, against 76.1% for DeepSeek 3.1 a year earlier.

**Context and caveats.**
- **Benchmarks:** public benchmarks saturate fast. Gemini 3.1 Pro and Gemini 4 Carbon aced the pelican-on-bicycle SVG test, including held-out variants. Broad-knowledge probes such as the land-vs-water map eval show Opus 5.5 far ahead of Opus 4.6.
- **Restricted releases:** Anthropic's Mythos, a vulnerability-finding model, was released only to selected companies via Project Glasswing, a sign that gated releases for risky capabilities are becoming normal.
- **History:** Willison dates the coding-agent inflection to November 2025 (Opus 4.5, GPT 5.1). Anthropic's founders attribute Claude's rise to compute scaling plus algorithmic "compute multipliers" (Claude 3 Opus, then Sonnet 3.5).

## Latest active insights

- Uniform 4-bit quantization can wreck a model. Dynamic, layer-aware quantization keeps heavily used layers at higher precision, and quantized-model recall has improved sharply as a result. ([What Runs Where? Local AI in Production — Ahmad Osman, Osmantic](../videos/2026-11-21-what-runs-where-local-ai-in-production-ahmad-osman-osmantic.md), 2026-11-21, relevance 2/5)
- LiteRT.js runs general ML models such as embedding models, while LiteRT-LM.js runs LLMs. Both delegate ops across WebGPU and Wasm execution backends and are imported as a plain JS library, needing fewer than 20 lines to load and run Gemma 4. ([Web AI at the Edge: Local Vector Search, Gemma 4, & hybrid cloud routing](../videos/2026-11-20-web-ai-at-the-edge-local-vector-search-gemma-4-hybrid-cloud.md), 2026-11-20, relevance 4/5)
- Gemma 4 comes in 2B, 4B, 12B, 26B MoE (4B active) and 31B sizes. Only the 2B and 4B support audio; 12B and above handle images and text only. ([Web AI at the Edge: Local Vector Search, Gemma 4, & hybrid cloud routing](../videos/2026-11-20-web-ai-at-the-edge-local-vector-search-gemma-4-hybrid-cloud.md), 2026-11-20, relevance 4/5)
- A land-vs-water coordinate eval, plotted as a world map, visualises model knowledge: Opus 4.6 gives a blurry map while Opus 5.5 is almost perfect. This suggests broad general knowledge matters more than frontier benchmark spikes. ([The Sweet Side of the Bitter Lesson — Thariq Shihipar, Independent](../videos/2026-11-19-the-sweet-side-of-the-bitter-lesson-thariq-shihipar-independ.md), 2026-11-19, relevance 4/5)
- Mythos, a model with expert-level ability to find software vulnerabilities and exploits, was released through Project Glasswing only to a limited set of companies, so cyberdefenders could find and patch vulnerabilities while broader safeguards were built. ([The making of Anthropic](../videos/2026-11-19-the-making-of-anthropic.md), 2026-11-19, relevance 2/5)
- The founders say Claude was far behind the frontier at public launch. Competitiveness came from compute plus stacked algorithmic 'compute multipliers', leading to Claude 3 Opus and then Sonnet 3.5, which made models useful for programming. ([The making of Anthropic](../videos/2026-11-19-the-making-of-anthropic.md), 2026-11-19, relevance 2/5)
- Early assistants were built toward 'helpful, harmless, honest'. Helpfulness and harmlessness came first, and honesty lagged badly: early models confidently endorsed an all-potato diet. ([The making of Anthropic](../videos/2026-11-19-the-making-of-anthropic.md), 2026-11-19, relevance 2/5)
- The founding bet was the 'big blob of compute' scaling trend: more compute and data yield predictably more capability and new emergent abilities, without hand-teaching planning or tool use. ([The making of Anthropic](../videos/2026-11-19-the-making-of-anthropic.md), 2026-11-19, relevance 2/5)
- For more hands-off work, Gemini 4 Argon offers two modes. Teamwork Preview uses many teams of subagents, while the /boost command works linearly and spins up subagents ad hoc. The speaker says Gemini 4 Argon is strong at long-horizon tasks. ([Build a "software factory" that doesn’t produce AI Slop](../videos/2026-11-19-build-a-software-factory-that-doesn-t-produce-ai-slop.md), 2026-11-19, relevance 3/5)
- Gemini 4 Hydrogen is the fast tier of the family, roughly tripling Terminal Bench 4 performance over Gemini 3.8 Flash while being about three times faster, and is available across Google surfaces. ([Post-Training Gemini 4 for Real Engineering Work — Melvin Johnson, Google DeepMind](../videos/2026-11-18-post-training-gemini-4-for-real-engineering-work-melvin-john.md), 2026-11-18, relevance 3/5)
- Gemini 4 Carbon is claimed to top several customer benchmarks while being substantially cheaper than the runner-up, making cost-per-task a headline differentiator alongside quality. ([Post-Training Gemini 4 for Real Engineering Work — Melvin Johnson, Google DeepMind](../videos/2026-11-18-post-training-gemini-4-for-real-engineering-work-melvin-john.md), 2026-11-18, relevance 3/5)
- Ultrafast is described as 8x faster at 6x the cost and works best for UI iteration with a hot-reloading dev server and light reasoning effort. It brings little benefit when build or test time dominates the task. ([New Ways of Working with Codex — Dominik Kundel & Charlie Guo, OpenAI](../videos/2026-11-17-new-ways-of-working-with-codex-dominik-kundel-charlie-guo-op.md), 2026-11-17, relevance 4/5)
- Benchmarks get trained against quickly. Gemini 3.1 Pro and later Gemini 4 Carbon aced his pelican-on-bicycle SVG test, including his held-out animal/vehicle variants, which weakened the benchmark. ([2026 in LLMs — Simon Willison](../videos/2026-11-17-2026-in-llms-simon-willison.md), 2026-11-17, relevance 3/5)
- He defines a "Fable class" model this way: if you can state a goal, provide the necessary tools, and the goal is possible, the model will solve it almost by brute force over runs of around 12 hours. Problem definition and tool provisioning become the key human skill. ([2026 in LLMs — Simon Willison](../videos/2026-11-17-2026-in-llms-simon-willison.md), 2026-11-17, relevance 3/5)
- Willison dates the coding-agent inflection point to November 2025. That is when the models became reliable enough to drive coding agents daily rather than as a novelty. ([2026 in LLMs — Simon Willison](../videos/2026-11-17-2026-in-llms-simon-willison.md), 2026-11-17, relevance 3/5)

## Open questions

- Will cost-per-task (as Gemini 4 Carbon claims) replace raw benchmark scores as the main way to compare models, and how should agent UIs surface cost to users?
- How should supervision, progress and approval UI be designed for 12-hour Fable-class agent runs and multi-subagent modes like Gemini 4 Argon Teamwork?
- Is in-browser Gemma 4 via LiteRT-LM.js (WebGPU/Wasm, with WebNN still in preview) production-ready for web-component AI features, and on which devices?
- With public benchmarks like pelican-SVG being trained against, which evals reliably signal real capability gains?
- Will gated releases like Mythos via Project Glasswing become standard for high-risk capabilities, and how will API access change as a result?

## Changelog

_No changes yet._
