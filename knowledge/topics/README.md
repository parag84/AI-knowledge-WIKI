# Topics

| Topic | Active | Stale | Updated |
|---|---|---|---|
| [Agents](agents.md) | 167 | 0 | 2026-11-23 |
| [Evals](evals.md) | 85 | 0 | 2026-11-23 |
| [RAG & retrieval](rag.md) | 15 | 0 | 2026-11-23 |
| [MCP & tools](mcp-tools.md) | 73 | 0 | 2026-11-23 |
| [Coding agents](coding-agents.md) | 139 | 0 | 2026-11-23 |
| [UX for AI](ux-for-ai.md) | 124 | 0 | 2026-11-23 |
| [Infra & cost](infra-cost.md) | 83 | 0 | 2026-11-23 |
| [Model releases](model-releases.md) | 27 | 0 | 2026-11-23 |
| [Startups & product](startups-product.md) | 23 | 0 | 2026-11-23 |
| [Agent memory & context](agent-memory.md) | 27 | 0 | 2026-11-23 |
| [AI security](ai-security.md) | 56 | 0 | 2026-11-23 |

## Proposed topics (awaiting approval in `config/topics.yaml`)

- `local-ai` Local & on-device AI: Running models on owned hardware (quantization, inference engines, consumer GPUs) is a recurring theme not captured by infra-cost alone.
- `on-device-ai` On-device / Web AI: Client-side inference in browsers and devices (WebGPU, WebNN, LiteRT) is a recurring theme with distinct UX, privacy and cost tradeoffs that no current topic covers.
- `ai-safety-governance` AI safety & release governance: Covers staged or restricted model releases, safety research publication and corporate governance structures like PBCs, which none of the existing slugs capture.
- `semantic-layer-grounding` Semantic layers & data governance for agents: Grounding agents on governed business definitions, lineage and PII policies is a distinct enterprise-data theme not well covered by RAG or tools alone.
- `i18n-accessibility` Internationalization & accessibility for AI: Multiple talks (MCP i18n SEP, multilingual voice-first users, GBV survivors' coded language) treat language and accessibility as first-class agent design concerns not covered by ux-for-ai alone.
- `agent-experience-dx` Agent experience for tools (AX for CLIs/APIs): Several talks treat agents as the primary users of CLIs, MCP servers and docs (pipe tax, agent mode, skill.md as interface), a design discipline distinct from UX for human users of AI.
- `decision-models` Decision / system-one models: Several talks centre on a new class of single-forward-pass classifier models (Jev, Clef, Cleric, Gemini Decisions API) that are distinct from generative LLMs and drive routing, judging and intent-detection patterns.
- `spec-driven-development` Spec-driven development: Writing and verifying specs/requirements as the primary artifact handed to coding agents is a recurring theme not cleanly covered by coding-agents or evals.
- `realtime-multimodal` Real-time multimodal agents: Live voice/vision streaming agents with interruption and frame handling are a distinct architectural and UX theme not fully covered by agents or ux-for-ai.
- `voice-agents` Voice agents: Full-duplex voice interfaces over agent backends are a distinct design and engineering area that the current taxonomy only partly covers.
