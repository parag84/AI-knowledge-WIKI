---
title: 'Data Agents over S3: Build the Missing Semantic Layer for Files - Dmitry Petrov,
  DataChain'
channel: Agentic AI Foundation
url: https://www.youtube.com/watch?v=0o93aKBvuYQ
video_id: 0o93aKBvuYQ
published: '2026-11-22'
duration: '26:59'
topics:
- agents
- agent-memory
- rag
- infra-cost
- ux-for-ai
- evals
- coding-agents
relevance: 3
status: active
superseded_by: []
---

# Data Agents over S3: Build the Missing Semantic Layer for Files - Dmitry Petrov, DataChain

[![Data Agents over S3: Build the Missing Semantic Layer for Files - Dmitry Petrov, DataChain](../assets/thumbs/0o93aKBvuYQ.webp)](https://www.youtube.com/watch?v=0o93aKBvuYQ)

**Agentic AI Foundation** · 2026-11-22 · 26:59 · relevance 3/5 · [Watch on YouTube](https://www.youtube.com/watch?v=0o93aKBvuYQ)

## Summary

A conference talk by Dmitry Petrov (creator of DVC, founder of DataChain) on building a semantic/context layer so data agents can reason over millions of unstructured files in S3-style object storage. He frames three problems (context window limits, compute to extract information, and trusting saved results) and demos a Slack-fronted Claude Code agent that reuses a previously computed, versioned dataset to answer a video-quality question in about 3 minutes instead of ~30 minutes of compute. The takeaway is that agents should continuously populate a typed, lineage-aware knowledge base and pair it with 'trust machinery' that verifies cached results against current data before answering.

## Key insights

- Reusing a previously saved, versioned dataset let the agent answer 'which tasks have the most usable videos' in about 3 minutes versus roughly 30 minutes (10 machines plus extra minutes) when computed from scratch, a ~10x saving that grows to hours at terabyte scale.
  - _Relies on:_ Demo: ~3 minutes with reuse vs ~23-32 minutes compute from scratch; Original job used 10 machines; Bucket size: a few gigabytes _(as of 2026-11-22)_
- Cached knowledge-base answers must be re-validated against the request and current data: in the demo, naive aggregation gave 14 minutes of usable video but deduplication brought the true answer to 11 minutes.
  - _Relies on:_ 14 minutes naive vs 11 minutes after removing duplicates _(as of 2026-11-22)_
- DataChain's private benchmark of Claude vs Codex on storage tasks found agents err in up to ~50% of cases when underlying data changes, either answering from stale cache without checking sync or rescanning remote storage when a valid local cache exists.
  - _Relies on:_ Benchmark is private, not yet released; Compared Claude and Codex; Up to ~50% error rate when storage changed _(as of 2026-11-22)_
- Citing an Anthropic blog post, the speaker says giving agents access to everything (all tables, all dbt files) raised accuracy by less than 1% while greatly increasing time spent, so context should be curated rather than exhaustive.
  - _Relies on:_ Anthropic blog post on structured-data agents; <1% accuracy gain from full access _(as of 2026-11-22)_
- Each saved dataset is exposed to agents as a simple Markdown-like card with description, dependencies (lineage) and schema; the speaker calls lineage a must-have for agents, saying without it they 'hallucinate badly'.
- Basic plumbing is a real agent failure mode: listing a multi-million-object bucket with AWS CLI or rclone can take minutes to an hour, and an agent session left cloud instances running, adding about $1,000 overnight.
  - _Relies on:_ AWS CLI / rclone listing of millions of objects: minutes to ~1 hour; ~$1,000 unexpected bill from instances not shut down _(as of 2026-11-22)_

## Tools, models & APIs mentioned

- **DataChain** (product)
- **DVC** (product)
- **Claude Code** (product)
- **Codex** (product)
- **Slack** (product)
- **Amazon S3** (product)
- **AWS CLI** (other)
- **rclone** (other)
- **Postgres** (product)
- **Snowflake** (product)
- **SQLite** (other)
- **MCP** (protocol)
- **YOLO** (model)

## How this applies to AX / design systems

The 'trust machinery' idea suggests an AX pattern: when an agent answers from prior work, show a provenance chip (source dataset, version, lineage) plus a 'verified against current data' state and any corrections made (e.g., duplicates removed, 14 to 11 minutes). A reusable 'dataset/context card' component in the AI component library (description, dependencies, schema, freshness) could mirror the Markdown cards agents read, making the same artifact human-inspectable. Cost and time-saved indicators ('reused prior result: 3 min vs ~30 min') and resource warnings (running instances) are also worth prototyping in agent supervision UI or a developer portal.

_Relevance 3/5: Mostly data-infrastructure for agents, but its ideas about agents reusing prior work, surfacing lineage and verifying cached answers map onto trust and supervision patterns in agentic UX._

## Best moments

- [2:35](https://www.youtube.com/watch?v=0o93aKBvuYQ&t=155s): Ideal 'chat with your data' UI framing and the three problems: context, compute, trust
- [7:17](https://www.youtube.com/watch?v=0o93aKBvuYQ&t=437s): Benchmark slide: Claude vs Codex error rates when storage changes
- [13:29](https://www.youtube.com/watch?v=0o93aKBvuYQ&t=809s): Slack + Claude Code demo setup and question
- [16:07](https://www.youtube.com/watch?v=0o93aKBvuYQ&t=967s): Cached answer verification: duplicates change 14 to 11 minutes
- [18:26](https://www.youtube.com/watch?v=0o93aKBvuYQ&t=1106s): What the knowledge-base dataset card looks like: description, dependencies, schema
