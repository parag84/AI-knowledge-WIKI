# RAG & retrieval

> Retrieval-augmented generation, embeddings, search, context engineering over documents.

_10 active · 0 stale · synthesis updated 2026-11-22_

## Current best understanding

**Plain vector RAG is no longer enough on its own (as of Nov 2026).** Several independent demos show where naive retrieval breaks. An agent writing raw SQL against BigQuery tables missed business rules (for example, the 'under 50' bracket means ages 31–50). It burned turns inspecting schemas and silently guessed wrong. Grounding it in a governed semantic layer (Looker + Knowledge Catalog) fixed the answer with fewer turns and tokens.

Other demos point the same way:
- **GraphRAG over BigQuery Graph (GQL):** vector RAG can return a matching record that lacks needed facts. GraphRAG follows relationships (order→payment, order→customer→refund history) to assemble complete context.
- **Vertex AI Memory Bank:** vector search over chat history can't tell which of two conflicting facts is current (moved NY→SF). Memory Bank runs asynchronously and does extraction, deduplication and conflict resolution. It stores timestamped facts and injected ~24 tokens versus ~1,400 for raw RAG.

**Context engineering and trust signals matter for AX design.** Keep the full task history (tool calls, outcomes, events) separate from the prompt, then render prompts per model so compaction can vary by context length (Nov 2026). Provenance UI is emerging as a pattern. In Claude Data (formerly Claude Dashboards, out of beta Nov 2026), charts built on data-team-certified queries show a certified badge. Certified queries and live sharing are still in beta. Knowledge Catalog + Knowledge Studio can index PDFs and LookML and render a visual context graph with lineage (dashboard → Explore → view → BigQuery tables) for impact analysis.

**Client-side RAG is viable.** Jason Mayes' VectorSearch.js uses EmbeddingGemma on the GPU to search ~100k paragraphs in ~100 ms. Paired with local Gemma 4, no data leaves the device and there is no per-token cost, which suits medical, legal and finance work. This is relevant to browser-delivered Web Component libraries and developer portals with doc search.

## Latest active insights

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

## Open questions

- When does GraphRAG or a semantic layer justify its modeling cost over improved vector RAG with metadata filters?
- How should agent UIs surface provenance (certified badges, lineage graphs, memory timestamps) without overwhelming users?
- Does client-side RAG (VectorSearch.js + Gemma 4) hold up for larger corpora and lower-end devices, e.g. developer-portal doc search?
- How transparent and correctable should managed memory layers like Vertex AI Memory Bank be when they resolve conflicting facts automatically?
- Will certified-query style trust signals become a cross-vendor pattern or stay product-specific?

## Changelog

_No changes yet._
