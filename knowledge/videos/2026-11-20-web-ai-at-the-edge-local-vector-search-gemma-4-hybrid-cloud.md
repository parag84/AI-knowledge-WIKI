---
title: 'Web AI at the Edge: Local Vector Search, Gemma 4, & hybrid cloud routing'
channel: Google Cloud Tech
url: https://www.youtube.com/watch?v=ugmCis5nuF8
video_id: ugmCis5nuF8
published: '2026-11-20'
duration: '27:25'
topics:
- rag
- ux-for-ai
- infra-cost
- model-releases
- agents
- mcp-tools
- evals
relevance: 4
status: active
superseded_by: []
---

# Web AI at the Edge: Local Vector Search, Gemma 4, & hybrid cloud routing

[![Web AI at the Edge: Local Vector Search, Gemma 4, & hybrid cloud routing](../assets/thumbs/ugmCis5nuF8.webp)](https://www.youtube.com/watch?v=ugmCis5nuF8)

**Google Cloud Tech** · 2026-11-20 · 27:25 · relevance 4/5 · [Watch on YouTube](https://www.youtube.com/watch?v=ugmCis5nuF8)

## Summary

A Google Cloud Tech interview in which Aja Hammerly talks with Jason Mayes about Web AI, meaning running ML models and LLMs client-side in the browser via WebGPU, Wasm and the emerging WebNN. Jason covers a fully local RAG pipeline (VectorSearch.js plus a local Gemma 4), the LiteRT.js and LiteRT-LM.js runtimes, and Gemma 4 sizing from 2B to 31B. He also walks through hybrid cloud/local routing built on graceful degradation and progressive enhancement. The main takeaway is to build hybrid by default: benchmark the device, serve from the cloud while the model downloads, then flip to local or offline 'privacy mode', always choosing the smallest model that passes your evals.

## Key insights

- A GPU-executed, fully local vector database can search around 100,000 paragraphs in about 100 ms. Pairing it with a local Gemma 4 gives fully client-side RAG with no data leaving the device and no per-token cost, which suits medical, legal and finance use cases.
  - _Relies on:_ VectorSearch.js library by Jason Mayes; Uses an EmbeddingGemma model (transcript says 'EmbeddingGemini'); ~100,000 paragraphs searched in ~100 ms; Cosine similarity over string embeddings _(as of 2026-11-20)_
- The recommended hybrid flow runs a quick on-device benchmark first and delegates to the cloud if it fails. If it passes, the app still uses the cloud while the model downloads, then switches to local and can expose a toggle such as 'privacy mode now available' or an offline mode.
  - _Relies on:_ Benchmark via matrix-multiplication-style ops; Proposed idea: benchmark using the model architecture with zero weights to measure inferences per second before downloading _(as of 2026-11-20)_
- Graceful degradation means falling back to a preloaded local Gemma when offline, for example browsing cached products and queueing cart items to sync later. Progressive enhancement means unlocking capabilities such as image-based search when the device has more VRAM.
  - _Relies on:_ Gemma 4 used as the local fallback model; Gemini used as the cloud model _(as of 2026-11-20)_
- Gemma 4 comes in 2B, 4B, 12B, 26B MoE (4B active) and 31B sizes. Only the 2B and 4B support audio; 12B and above handle images and text only.
  - _Relies on:_ Gemma 4 2B runs on IoT devices such as Raspberry Pi; Gemma 4 4B uses about 4.5 GB VRAM (speaker's recollection); Gemma 4 26B MoE has 4B active parameters; Gemma 4 31B is the largest; the speaker says it is on par with 'Sonnet 3.5' (transcript: 'Sonic 3.5'); Up to 31B has been run in the browser _(as of 2026-11-20)_
- LiteRT.js runs general ML models such as embedding models, while LiteRT-LM.js runs LLMs. Both delegate ops across WebGPU and Wasm execution backends and are imported as a plain JS library, needing fewer than 20 lines to load and run Gemma 4.
  - _Relies on:_ LiteRT.js; LiteRT-LM.js currently focused on the Gemma family; WebNN (W3C) gives NPU access and is in preview _(as of 2026-11-20)_
- Route queries between local and cloud with a small model trained on a human-labeled golden dataset to predict query complexity, placed in the agent orchestration layer. Small models such as Gemma 2 2B have handled tool-calling agents.
  - _Relies on:_ Gemma 2 2B used for early agents (travel/flight app, Web AI DJ) _(as of 2026-11-20)_
- Start with the smallest model, step up a size only when evals fail, and use fine-tuning or distillation for remaining edge cases. Set a baseline first, so that if the non-AI version was 70% accurate the AI must beat it.
  - _Relies on:_ Example baseline: 70% accuracy; Cross-Origin Storage proposal lets domains share hashed model downloads _(as of 2026-11-20)_

## Tools, models & APIs mentioned

- **Gemma** 4 (model)
- **EmbeddingGemma** (model)
- **VectorSearch.js** (sdk)
- **LiteRT.js** (sdk)
- **LiteRT-LM.js** (sdk)
- **WebGPU** (api)
- **WebAssembly** (other)
- **WebNN** (api)
- **Cross-Origin Storage** (protocol)
- **Gemini** (model)
- **YOLO** (model)
- **COCO-SSD** (model)

## How this applies to AX / design systems

The hybrid flow defines UI states an AI component library should support: a model-download progress indicator, a 'privacy mode / offline mode available' toggle, and a per-message badge showing whether a response came from a local or cloud model. Capability-based progressive enhancement suggests a design-system pattern where an input component such as image search appears only when device capability allows, with a text fallback. For developer portals, a Lit-based 'run in browser' widget using LiteRT-LM.js could offer private, zero-cost interactive samples or local doc search via VectorSearch.js.

_Relevance 4/5: Hybrid local/cloud AI with explicit UX states (privacy mode, offline mode, capability-based enhancement) maps directly onto agentic UX and AI component design, though the video is mostly architectural._

## Best moments

- [1:20](https://www.youtube.com/watch?v=ugmCis5nuF8&t=80s): VectorSearch.js demo claim: 100k paragraphs searched locally in about 100 ms
- [3:57](https://www.youtube.com/watch?v=ugmCis5nuF8&t=237s): Clear definitions of graceful degradation and progressive enhancement for hybrid AI
- [11:47](https://www.youtube.com/watch?v=ugmCis5nuF8&t=707s): Gemma 4 size-by-size guidance, VRAM needs and multimodal support
- [17:29](https://www.youtube.com/watch?v=ugmCis5nuF8&t=1049s): Hybrid routing UX: benchmark, use cloud while downloading, then a privacy-mode toggle
- [23:43](https://www.youtube.com/watch?v=ugmCis5nuF8&t=1423s): Routing queries via a small complexity-prediction model trained on a golden dataset
