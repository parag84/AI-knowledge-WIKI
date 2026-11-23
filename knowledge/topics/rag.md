# RAG & retrieval

> Retrieval-augmented generation, embeddings, search, context engineering over documents.

_15 active · 0 stale · synthesis updated 2026-11-23_

## Current best understanding

_No synthesis yet._

## Latest active insights

- Each saved dataset is exposed to agents as a simple Markdown-like card with description, dependencies (lineage) and schema; the speaker calls lineage a must-have for agents, saying without it they 'hallucinate badly'. ([Data Agents over S3: Build the Missing Semantic Layer for Files - Dmitry Petrov, DataChain](../videos/2026-11-22-data-agents-over-s3-build-the-missing-semantic-layer-for-fil.md), 2026-11-22, relevance 3/5)
- Citing an Anthropic blog post, the speaker says giving agents access to everything (all tables, all dbt files) raised accuracy by less than 1% while greatly increasing time spent, so context should be curated rather than exhaustive. ([Data Agents over S3: Build the Missing Semantic Layer for Files - Dmitry Petrov, DataChain](../videos/2026-11-22-data-agents-over-s3-build-the-missing-semantic-layer-for-fil.md), 2026-11-22, relevance 3/5)
- A GPU-executed, fully local vector database can search around 100,000 paragraphs in about 100 ms. Pairing it with a local Gemma 4 gives fully client-side RAG with no data leaving the device and no per-token cost, which suits medical, legal and finance use cases. ([Web AI at the Edge: Local Vector Search, Gemma 4, & hybrid cloud routing](../videos/2026-11-20-web-ai-at-the-edge-local-vector-search-gemma-4-hybrid-cloud.md), 2026-11-20, relevance 4/5)
- Keep the full task history (every tool call, success/failure, platform event) separate from the prompt, then render prompts per model so compaction/summarization can differ by context length. ([What it takes to set intelligence free — Fabian Hedin, CTO, Lovable](../videos/2026-11-19-what-it-takes-to-set-intelligence-free-fabian-hedin-cto-lova.md), 2026-11-19, relevance 4/5)
- BigQuery Graph lets you define graph relationships over existing BigQuery tables and query connected records with GQL (graph query language); the same facts could be fetched with table joins, but defined relationships make multi-hop queries easier. ([Why everyone is talking about graphs in AI (and when to skip them)](../videos/2026-11-19-why-everyone-is-talking-about-graphs-in-ai-and-when-to-skip.md), 2026-11-19, relevance 4/5)
- Vector RAG can return a matching record that lacks facts the task needs; GraphRAG starts from a relevant record and follows relationships (order→payment, order→customer→refund history summary) to assemble complete context. ([Why everyone is talking about graphs in AI (and when to skip them)](../videos/2026-11-19-why-everyone-is-talking-about-graphs-in-ai-and-when-to-skip.md), 2026-11-19, relevance 4/5)
- Claude Data lets data teams certify queries, and any chart built on a certified query shows a certified badge. The badge acts as a provenance and trust signal on AI-generated visualizations, and live sharing shows up-to-date dashboards to viewers who lack data-source access. ([Five brand new ways to use Claude at work](../videos/2026-11-18-five-brand-new-ways-to-use-claude-at-work.md), 2026-11-18, relevance 4/5)
- Vertex AI Memory Bank runs asynchronously outside the main loop and handles entity extraction, deduplication, conflict resolution and fact updates, storing distilled facts with created/updated timestamps. In the demo it injected ~24 tokens of memory versus ~1,400 tokens for a raw RAG approach. ([Why your AI agent keeps forgetting (and getting slower)](../videos/2026-11-17-why-your-ai-agent-keeps-forgetting-and-getting-slower.md), 2026-11-17, relevance 3/5)
- Naive vector-DB RAG over chat history fails at stateful facts: given 'moved from New York to San Francisco' it retrieves both statements and the model can't tell which is current. A memory layer needs deduplication and conflict resolution, not just retrieval. ([Why your AI agent keeps forgetting (and getting slower)](../videos/2026-11-17-why-your-ai-agent-keeps-forgetting-and-getting-slower.md), 2026-11-17, relevance 3/5)
- Integrating Looker with Knowledge Catalog auto-indexes LookML models, explores, views and dashboards. An exploration agent in Knowledge Studio can then build a visual context graph with upstream lineage to BigQuery tables, which supports impact analysis before schema changes. ([Ground AI Agents with Looker and Knowledge Catalog on Google Cloud](../videos/2026-11-17-ground-ai-agents-with-looker-and-knowledge-catalog-on-google.md), 2026-11-17, relevance 2/5)
- Unstructured documents uploaded to Cloud Storage and indexed in Knowledge Catalog can be combined with live Looker metrics. In the demo, a grant policy PDF was used to compute eligibility and payout per athlete. ([Ground AI Agents with Looker and Knowledge Catalog on Google Cloud](../videos/2026-11-17-ground-ai-agents-with-looker-and-knowledge-catalog-on-google.md), 2026-11-17, relevance 2/5)
- An agent writing raw SQL against raw tables lacked business rules (the 'under 50' team bracket means ages 31–50), burned multiple turns inspecting schemas, and silently guessed wrong. Grounding the agent in a semantic layer fixed the answer and used fewer turns and tokens. ([Ground AI Agents with Looker and Knowledge Catalog on Google Cloud](../videos/2026-11-17-ground-ai-agents-with-looker-and-knowledge-catalog-on-google.md), 2026-11-17, relevance 2/5)
- Exa argues agent search must be semantic and token-dense: agent queries average ~12 words (10% are 17+), so keyword search underperforms, and returning extracted ~500-character excerpts instead of whole pages cuts tokens ~16x. ([AIE CODE: Google DeepMind, OpenAI, ArtCraft, Cognition, Exa, Anthropic, Amp, et al](../videos/2026-11-13-aie-code-google-deepmind-openai-artcraft-cognition-exa-anthr.md), 2026-11-13, relevance 4/5)
- Toolbox currently has a wider catalog of pre-built tools than the managed server. It can combine governed LookML metrics with external sources such as Knowledge Catalog or Spanner in one agent flow. ([Decide which Looker MCP integration is right for you?](../videos/2026-11-13-decide-which-looker-mcp-integration-is-right-for-you.md), 2026-11-13, relevance 3/5)
- Split agent memory into exact facts stored as structured data (SQL) and meaning/understanding stored in semantic vector memory. Long memory work runs in the background, off the live path. ([Multimodal AI agent architecture: Voice, vision, tools & memory](../videos/2026-11-11-multimodal-ai-agent-architecture-voice-vision-tools-memory.md), 2026-11-11, relevance 4/5)

## Open questions

_None recorded._

## Changelog

_No changes yet._
