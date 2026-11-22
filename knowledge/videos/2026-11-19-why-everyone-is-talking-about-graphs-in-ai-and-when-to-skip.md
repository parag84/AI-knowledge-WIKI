---
title: Why everyone is talking about graphs in AI (and when to skip them)
channel: Google Cloud Tech
url: https://www.youtube.com/watch?v=2sS9XS-Fw90
video_id: 2sS9XS-Fw90
published: '2026-11-19'
duration: '10:22'
topics:
- agents
- rag
- ux-for-ai
- mcp-tools
- infra-cost
relevance: 4
status: active
superseded_by: []
---

# Why everyone is talking about graphs in AI (and when to skip them)

[![Why everyone is talking about graphs in AI (and when to skip them)](../assets/thumbs/2sS9XS-Fw90.webp)](https://www.youtube.com/watch?v=2sS9XS-Fw90)

**Google Cloud Tech** · 2026-11-19 · 10:22 · relevance 4/5 · [Watch on YouTube](https://www.youtube.com/watch?v=2sS9XS-Fw90)

## Summary

A Google Cloud Tech explainer by Annie Wang on why graphs show up in AI, split into workflow graphs (orchestrating agent steps) and data/knowledge graphs (GraphRAG for context). Using a customer refund demo, she shows parallel checks, a rule node routing to a paused human-review step built with Google's ADK, and BigQuery Graph queried via GQL to traverse order→payment and customer→refund history. The takeaway is that graphs help when you need explicit control over step relationships or connected facts, but they add build/maintenance cost and aren't needed for simple tasks.

## Key insights

- Telling a single agent in its instructions to wait for human approval does not guarantee it will wait; a deterministic workflow node that pauses execution is needed to enforce human-in-the-loop review.
  - _Relies on:_ Google Agent Development Kit (ADK) graph workflows; ADK human-in-the-loop via tool confirmation _(as of 2026-11-19)_
- Model workflows as nodes (a function, an AI agent, or a wait-for-human step) and edges (dependencies and routing paths); common patterns are parallel, routing, trees (parent/child agents) and loops, and real apps combine them.
- In the refund demo, three checks (order, payment, refund history) run in parallel, join at a rules node, which routes the case to human review; after approval with a reason, a response agent drafts the reply using the facts plus the human decision.
  - _Relies on:_ Google ADK _(as of 2026-11-19)_
- Vector RAG can return a matching record that lacks facts the task needs; GraphRAG starts from a relevant record and follows relationships (order→payment, order→customer→refund history summary) to assemble complete context.
  - _Relies on:_ Demo order: trail running shoes, $60, placed 12 days ago; Payment shows no open dispute; customer has one refund in past 12 months _(as of 2026-11-19)_
- BigQuery Graph lets you define graph relationships over existing BigQuery tables and query connected records with GQL (graph query language); the same facts could be fetched with table joins, but defined relationships make multi-hop queries easier.
  - _Relies on:_ BigQuery Graph; GQL (graph query language) _(as of 2026-11-19)_
- Both graph types carry trade-offs: workflow graphs take work to build and maintain (a few functions or one agent with tools may suffice for small tasks), and traversing more connections adds latency, cost and irrelevant info, so measure separate parallel reads versus one combined query in production.

## Tools, models & APIs mentioned

- **Google Agent Development Kit (ADK)** (framework)
- **BigQuery Graph** (product)
- **GQL (Graph Query Language)** (other)

## How this applies to AX / design systems

The demo's pause-for-review step (add a reason, approve) is a concrete pattern for an approval component in an AI component library: a review card that shows the retrieved facts with their provenance (order, payment, refund history) alongside the routing reason. A workflow graph view could also become a supervision UI showing parallel steps, the join, and where the human sits, worth prototyping as a Lit web component for run visualization. For developer portals, the node/edge vocabulary and trade-off framing ('when to skip graphs') is a good model for docs that help developers pick single-agent vs workflow patterns.

_Relevance 4/5: The workflow-graph model with explicit human-review pause nodes and fact-grounded drafting maps directly onto approval UI and supervision patterns Parag designs for agentic experiences._

## Best moments

- [0:30](https://www.youtube.com/watch?v=2sS9XS-Fw90&t=30s): End-to-end refund demo including human approval with a reason
- [1:32](https://www.youtube.com/watch?v=2sS9XS-Fw90&t=92s): Why instructing an agent to wait doesn't guarantee it will
- [2:34](https://www.youtube.com/watch?v=2sS9XS-Fw90&t=154s): Graph patterns: parallel, routing, trees, loops
- [6:16](https://www.youtube.com/watch?v=2sS9XS-Fw90&t=376s): Traversing order→payment and customer→refund history to fill missing facts
