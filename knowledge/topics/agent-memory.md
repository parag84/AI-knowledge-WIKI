# Agent memory & context

> Persistent cross-session memory, context compaction and context engineering for agents.

_27 active · 0 stale · synthesis updated 2026-11-23_

## Current best understanding

**Curate context rather than dumping everything into it. This matters most for AX and portal design.** As of November 2026, sources agree that exhaustive context hurts more than it helps:

- A cited Anthropic post found that giving agents every table and dbt file raised accuracy by less than 1% while greatly increasing time spent.
- When a model was allowed to load everything, it invented a pricing check simply because prices were visible. The recommended fix is that the runtime, not the model, decides what enters context, passing validated handles for large data.
- For MCP, *progressive disclosure* is emerging as the pattern. Neo4j's agent-memory server cut 16 exposed tools to a 6-tool core, with extended tools revealed on demand. Its rubric: model-chosen actions are tools, reusable context is a resource, procedures are skills, mandatory steps are invisible plumbing, and who-may-act is authorization.
- Context can also come from the UI itself. MCP app methods such as *update model context* and *send message* turn a user's selection in a side panel into conversational context. A user's own agent calling WebMCP tools can bring personal memory into third-party apps.
- Datasets exposed to agents should carry description, schema and lineage cards. Without lineage, agents "hallucinate badly".

**Memory is becoming a visible, governed product surface.** Observed patterns (Nov 2026):

- A memory viewer in Settings where users can delete items, with expiration dates in a tiered memory design.
- Memory updates bundled with the agent's reply.
- A hybrid store: SQL for exact facts and vectors for meaning, with long memory work kept off the live path.
- A separate "dreaming" consolidation pass. Anthropic reports it fixes poisoned memories and builds wikis that beat raw search.

Memory gains scale with model capability: Sonnet 4.6 barely benefited, while Sonnet 5 and Opus did. Two further practices recur:

- Send a snapshot of the state being edited with each request so edits stay surgical; in one case this stopped the agent from rewriting a whole week to change one day.
- Re-validate cached or reused answers against current data. In one demo, deduplication corrected 14 minutes of usable video to 11. Reusing versioned datasets cut a ~30-minute compute to ~3 minutes.

**Compaction and orchestration are moving into the harness.** As of November 2026:

- **Codex** compacts by default; threads have run about 3 months. A running work log in AGENTS.md lets the agent resume after interruptions.
- **Claude Code projects (beta)** manages context automatically. A practitioner recommends Fable 5.2 as the judging orchestrator and Opus 5.5 for the threads; Fable leads can also delegate to Sonnet subagents, each with its own context.
- Harnesses also need durable state so sessions survive deploys and failures.

For instruction files, keep CLAUDE.md and AGENTS.md lean: include only what the model cannot see in the code, and avoid emphatic "IMPORTANT" phrasing, which derails Opus 5.5. Skills tend to be largely redundant:

- One tested skill was about 70% content the model already knew.
- Opus grasped about 70% of a skill's general ideas but only about 22% of its exact details.
- The advice is to keep precise parameters, cut generic explanation, and re-run evals across model families before shipping a trimmed skill.

On cost, the recommended prompt-cache hit-rate target is about 90%. KV-cache efficiency still constrains shared state across parallel subagents and non-linear memory designs.

## Latest active insights

- Each saved dataset is exposed to agents as a simple Markdown-like card with description, dependencies (lineage) and schema; the speaker calls lineage a must-have for agents, saying without it they 'hallucinate badly'. ([Data Agents over S3: Build the Missing Semantic Layer for Files - Dmitry Petrov, DataChain](../videos/2026-11-22-data-agents-over-s3-build-the-missing-semantic-layer-for-fil.md), 2026-11-22, relevance 3/5)
- Citing an Anthropic blog post, the speaker says giving agents access to everything (all tables, all dbt files) raised accuracy by less than 1% while greatly increasing time spent, so context should be curated rather than exhaustive. ([Data Agents over S3: Build the Missing Semantic Layer for Files - Dmitry Petrov, DataChain](../videos/2026-11-22-data-agents-over-s3-build-the-missing-semantic-layer-for-fil.md), 2026-11-22, relevance 3/5)
- Cached knowledge-base answers must be re-validated against the request and current data: in the demo, naive aggregation gave 14 minutes of usable video but deduplication brought the true answer to 11 minutes. ([Data Agents over S3: Build the Missing Semantic Layer for Files - Dmitry Petrov, DataChain](../videos/2026-11-22-data-agents-over-s3-build-the-missing-semantic-layer-for-fil.md), 2026-11-22, relevance 3/5)
- Reusing a previously saved, versioned dataset let the agent answer 'which tasks have the most usable videos' in about 3 minutes versus roughly 30 minutes (10 machines plus extra minutes) when computed from scratch, a ~10x saving that grows to hours at terabyte scale. ([Data Agents over S3: Build the Missing Semantic Layer for Files - Dmitry Petrov, DataChain](../videos/2026-11-22-data-agents-over-s3-build-the-missing-semantic-layer-for-fil.md), 2026-11-22, relevance 3/5)
- Progressive disclosure for MCP: tools/list returns a whole catalog and causes context bloat, token cost and wrong-tool selection; Neo4j's agent memory server cut 16 exposed tools to a 6-tool core profile with extended tools revealed on demand. Rubric: model-chosen actions are tools, reusable context is a resource, procedures are skills, must-always-happen steps are invisible plumbing, and who-may-act is authorization. ([20 Nov - MCP Dev Summit Nairobi 2026 Livestream](../videos/2026-11-20-20-nov-mcp-dev-summit-nairobi-2026-livestream.md), 2026-11-20, relevance 4/5)
- For dependency upgrades, using OpenRewrite as a deterministic upgrade engine plus a computed minimum set of libraries to bump reduced input tokens dramatically, freeing context for fixing build and test errors. ([We Built AI Agents To Fix Security Findings in Production](../videos/2026-11-19-we-built-ai-agents-to-fix-security-findings-in-production.md), 2026-11-19, relevance 3/5)
- Agent designs are constrained by the 'tyranny of the KV cache': shared state across parallel sub-agents, non-O(N) memory via map-reduce over history, and smarter sub-agent routing are open problems because they fight KV cache efficiency. (["Where is all the automation?" — Diogo Almeida, TypeSafe AI](../videos/2026-11-15-where-is-all-the-automation-diogo-almeida-typesafe-ai.md), 2026-11-15, relevance 3/5)
- Living memory: the server bundles memory updates extracted from the chat (equipment, injuries, upcoming events) with the coach's reply. The client updates a local store and a Settings memory viewer, with Firestore sync planned later. Memory items can be deleted and carry expiration dates in a tiered memory design. ([Watch me build a full AI app (no code)](../videos/2026-11-14-watch-me-build-a-full-ai-app-no-code.md), 2026-11-14, relevance 4/5)
- When an agent edit rewrote the whole week instead of one day, the fix was architectural rather than a one-off patch. The client sends a snapshot of the active plan, or the staged proposal it is replying to, with each request, and the coach prompt is hardened for 'surgical preservation'. After that change, adding a core finisher or swapping Thursday and Friday changed only the targeted items. ([Watch me build a full AI app (no code)](../videos/2026-11-14-watch-me-build-a-full-ai-app-no-code.md), 2026-11-14, relevance 4/5)
- Anthropic showed memory quality scales with model capability and benefits from a separate 'dreaming' consolidation pass that reflects over transcripts and notes to fix poisoned memories, fill gaps and build wikis; more dreaming compute made the wiki progressively better than raw search. ([AIE CODE: Google DeepMind, OpenAI, ArtCraft, Cognition, Exa, Anthropic, Amp, et al](../videos/2026-11-13-aie-code-google-deepmind-openai-artcraft-cognition-exa-anthr.md), 2026-11-13, relevance 4/5)
- Claude Code projects (beta) runs one orchestrator session that splits work into thread sessions, verifies what comes back and manages context automatically. She recommends a judging model (Fable 5.2) for the orchestrator and a doing model (Opus 5.5) for the threads, configured separately. ([Rethinking Claude Code Best Practices — Lydia Hallie, Anthropic](../videos/2026-11-12-rethinking-claude-code-best-practices-lydia-hallie-anthropic.md), 2026-11-12, relevance 4/5)
- With current models, emphatic instructions like 'IMPORTANT' or 'never do this!' in CLAUDE.md can push the model off track, causing more tool calls and worse results. CLAUDE.md should hold only what Claude cannot see from the code, such as a legacy service that is never directly referenced. ([Rethinking Claude Code Best Practices — Lydia Hallie, Anthropic](../videos/2026-11-12-rethinking-claude-code-best-practices-lydia-hallie-anthropic.md), 2026-11-12, relevance 4/5)
- Prompt caching is the first cost recommendation given to every customer, and the target is to get cache rates up to about 90%. Agentic turns that append to prior requests reuse the blocks that already ran. ([Building the Claude API for the frontier](../videos/2026-11-12-building-the-claude-api-for-the-frontier.md), 2026-11-12, relevance 3/5)
- The cheapest review happens before the work is done, so bring product, design and engineering conversations into a shared space agents can read. Block's open source projects Buzz and Co-Plan aim to do this. ([Cut The Noise: Building a Code Reviewer You Can Trust - Joah Gerstenberg, Block, Inc](../videos/2026-11-12-cut-the-noise-building-a-code-reviewer-you-can-trust-joah-ge.md), 2026-11-12, relevance 4/5)
- An agent is defined as an LLM in a harness with four design patterns: tool use, reasoning/planning, multi-agent orchestration and state/memory across sessions. Moving from stateless chat calls to stateful agents shifts bottlenecks to context management, orchestration and the tool-execution fabric (sandboxes, containers, tool latency). ([Agentic AI from Cloud to Edge: Building Intelligent Systems on Arm - Sudheera Vanguri, Arm](../videos/2026-11-12-agentic-ai-from-cloud-to-edge-building-intelligent-systems-o.md), 2026-11-12, relevance 2/5)
- Novelty is only a starting vector for optimization. After removing already-known items, re-run the task evals, and keep the shorter skill only if scores hold, which saves tokens and context. Smaller models know less of a skill's content, so test across model families. ([Your SKILL.md Is 70% Stuff the Model Already Knows - Nikolay Petrov, Intel](../videos/2026-11-11-your-skill-md-is-70-stuff-the-model-already-knows-nikolay-pe.md), 2026-11-11, relevance 3/5)
- The first skill tested was about 70% knowledge the model already had. Lenient grading (general idea) and strict grading (exact details) diverge sharply: Opus understood about 70% of a skill's content at the general level but only about 22% of its specific details. So keep exact parameters and values and cut generic explanation. ([Your SKILL.md Is 70% Stuff the Model Already Knows - Nikolay Petrov, Intel](../videos/2026-11-11-your-skill-md-is-70-stuff-the-model-already-knows-nikolay-pe.md), 2026-11-11, relevance 3/5)
- Results form a 2x2 matrix: known without the skill (redundant), correct without but wrong with the skill (harmful), wrong without but correct with (actual teaching), and wrong in both (poorly written). Harmful items are the easiest fix and are rare in popular skills, about 1 of roughly 400 items in Anthropic's skills, but more common in smaller ones. ([Your SKILL.md Is 70% Stuff the Model Already Knows - Nikolay Petrov, Intel](../videos/2026-11-11-your-skill-md-is-70-stuff-the-model-already-knows-nikolay-pe.md), 2026-11-11, relevance 3/5)
- AGENTS.md and SECURITY.md files in the repo act as instruction sets that help Codex understand the repository's nuances during security reviews. ([How to enable PR security reviews with Codex Security](../videos/2026-11-11-how-to-enable-pr-security-reviews-with-codex-security.md), 2026-11-11, relevance 3/5)
- Side-panel widgets share user selection state with the model, so selecting an element (e.g. a molecule region or a page element) becomes conversational context. This uses MCP app methods such as update model context and send message. ([Build What’s Next on the ChatGPT Platform with Plugins | DevDay 2026](../videos/2026-11-11-build-what-s-next-on-the-chatgpt-platform-with-plugins-devda.md), 2026-11-11, relevance 5/5)
- Let the runtime, not the model, decide what goes into context. When the model was allowed to load everything, it invented a pricing check just because prices were visible. For large data, the model passes a short handle that the runtime validates before any write. ([Agents Made Code Free. Maintaining It Didn't Get Cheaper. - Dmitry Buykin, Maersk](../videos/2026-11-11-agents-made-code-free-maintaining-it-didn-t-get-cheaper-dmit.md), 2026-11-11, relevance 4/5)
- The backend can feed the voice model through three streams, each with a different job. Silent context updates change what it knows, speakable commentary gives it something to say aloud, and the instructions stream changes how it behaves (guardrails, conciseness). ([Building with GPT-Live and Image Generation | DevDay 2026](../videos/2026-11-11-building-with-gpt-live-and-image-generation-devday-2026.md), 2026-11-11, relevance 5/5)
- Split agent memory into exact facts stored as structured data (SQL) and meaning/understanding stored in semantic vector memory. Long memory work runs in the background, off the live path. ([Multimodal AI agent architecture: Voice, vision, tools & memory](../videos/2026-11-11-multimodal-ai-agent-architecture-voice-vision-tools-memory.md), 2026-11-11, relevance 4/5)
- For long-running work the harness handles compaction across context windows and durable state so sessions resume after deploys or server failure, including ambiguous cases like a dropped connection during a file edit where replaying could be unsafe. ([Harness-as-a-Service: Building with the Agents API | DevDay 2026](../videos/2026-11-11-harness-as-a-service-building-with-the-agents-api-devday-202.md), 2026-11-11, relevance 4/5)
- Ask the agent to keep a running work log of what it has done and what is left to explore (for example via AGENTS.md) so it can resume after interruptions. Built-in compaction lets a single thread run for months without degrading. ([What Will You Build With Coding Agents That Don’t Quit? | DevDay 2026](../videos/2026-11-11-what-will-you-build-with-coding-agents-that-don-t-quit-devda.md), 2026-11-11, relevance 4/5)

## Open questions

- What is the right UX for user-visible memory (viewer, edit, expiry, provenance), and how should poisoned or outdated memories be surfaced to users versus fixed silently by consolidation passes?
- Will progressive disclosure become a standardized part of MCP (via the working group), and how should developer portals document core versus on-demand tool profiles?
- How can shared state across parallel subagents work without breaking KV-cache efficiency and the ~90% prompt-cache target?
- As built-in compaction and auto-managed context (Codex, Claude Code projects) mature, how much should designers still structure work logs, snapshots and CLAUDE.md/AGENTS.md by hand?
- Do skill and context-trimming results hold across smaller or non-Anthropic models, given that smaller models know less of a skill's content?

## Changelog

_No changes yet._
