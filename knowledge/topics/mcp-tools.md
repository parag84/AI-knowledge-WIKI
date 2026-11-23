# MCP & tools

> Model Context Protocol, tool use, function calling, connectors, agent-to-tool interfaces.

_73 active · 0 stale · synthesis updated 2026-11-23_

## Current best understanding

**MCP is now the UI and permission surface, not just plumbing (as of Nov 2026).** The July 2026 spec (2026-07-28) made the core stateless. `initialize` was replaced by server discover, list responses carry a TTL, and multi-round-trip elicitation works through an encrypted request state. It also added MCP Apps for interactive widgets and moved async tasks and skills into extensions.

OpenAI's plugin extensions for ChatGPT and Codex build directly on MCP and MCP Apps:
- **Entry points:** sidebar, side-panel and full-page entry points.
- **Composer @-mentions:** backed by a read-only search tool.
- **Settings:** rendered from read and update tools.
- **Shared selection:** widget selection state flows to the model through `update model context`.
- **Events:** an upcoming events spec (`events/subscribe` plus signed webhooks) triggers automations.

Other surfaces in the same direction:
- **WebMCP** lets sites expose tools to in-browser agents.
- **Claude's interactive connectors** open apps beside the chat, with the user approving every action.
- **AHP 1.0** (Oct 2026) syncs MCP server health and auth state so clients can show when a server needs attention.

For Parag's AX and design-system work, the consistent pattern is **propose, then approve, then execute**. Agents emit structured proposals, advisory holds or inline enable cards, and a separate executor acts only after a human approves. Tool results should also support a third **'unknown'** state with verifiable IDs, so agents don't retry blindly.

**Tool design for agents.** Keep a server to roughly 50 tools or fewer and use progressive disclosure: a small core profile, with extended tools loaded on demand. Use this rubric:
- **Tools:** actions the model chooses.
- **Resources:** reusable context.
- **Skills:** procedures.
- **Plumbing:** steps that must always happen.
- **Authorization:** who may act.

More practices that held up:
- Prefer fine-grained primitives and empty JSON templates.
- Treat help text, `skill.md` and error messages as the interface. Agents follow stale docs literally, and 97% of real MCP tool descriptions had issues.
- Use MCP tasks for long-running operations instead of polling.
- Grade the trajectory of tool calls, not just the final answer.

On cost, the evidence is split. Arize found MCP and CLI tied on correctness, but MCP cost about 6x more on the hardest tasks. DeepMind found bash-only harnesses about 2x cheaper. MCP still wins in consumer and enterprise settings because OAuth gives users a friendly consent prompt and admins control access. Code mode, where tools are called from code, is the emerging middle path.

**Auth and security matured, but the risk is concrete.** MCP standardised on OAuth 2.1 with external IdPs such as Okta and Entra ID. Enterprise-managed authorization (EMA/ID-JAG) is live in Claude and removes per-user consent prompts. The workload authorization grant (WAG) aims to give agents their own short-lived, policy-scoped tokens. The spec now bans token passthrough and requires audience and issuer validation, and roughly a third of about 116 SDK conformance scenarios are security tests.

The threats are not theoretical. A poisoned tool description leaked credentials 10/10 times with Claude Haiku, and regex scanners caught only 20 of 45 scenarios. The spoofed postmark-mcp package added a hidden BCC, and in the Oct 2026 registry audit about 30% of servers had no findable source. Enforce policy in server code with deny-by-default and per-request scope checks, sign releases (Sigstore), pin versions and sandbox side effects. Next up: SEP-2792 i18n (Accept-Language for localized tool titles and MCP App UI) is expected in the end-of-March 2027 release.

## Latest active insights

- Separate proposing from acting: agents only emit structured proposals (agent identity and owner, verb + target, base version, priority, ETA, evidence) into a queue, and a separate executor performs approved actions. ([Multi-Agent SRE: What Happens When Your Agents Want Opposite Things - Aditi Mewada, Apple](../videos/2026-11-22-multi-agent-sre-what-happens-when-your-agents-want-opposite.md), 2026-11-22, relevance 3/5)
- Code mode, an idea he credits to Cloudflare, gives the agent JavaScript to run in addition to Bash, and tool calls happen through that code instead of through the context window. Combined with cheap, fast classifier or decision models at each branch, an agent can build on-demand workflows, for example triaging 3,000 support requests in a fraction of the time it previously took. ([Build the Workshop Before the Software Factory — Armin Ronacher, Earendil](../videos/2026-11-22-build-the-workshop-before-the-software-factory-armin-ronache.md), 2026-11-22, relevance 4/5)
- Local models fail at tasks involving tools or hardware released after their training cutoff unless the harness gives them web search. Adding search let a local Qwen model change GPU fan RGB colors after it had failed without search. ([What Runs Where? Local AI in Production — Ahmad Osman, Osmantic](../videos/2026-11-21-what-runs-where-local-ai-in-production-ahmad-osman-osmantic.md), 2026-11-21, relevance 2/5)
- Before starting a backend integration, prompt the coding agent to check whether any skills or MCP servers should be installed so it has predefined rules and context for the task. ([From prototype to real Firebase backend (no code)](../videos/2026-11-21-from-prototype-to-real-firebase-backend-no-code.md), 2026-11-21, relevance 3/5)
- Route queries between local and cloud with a small model trained on a human-labeled golden dataset to predict query complexity, placed in the agent orchestration layer. Small models such as Gemma 2 2B have handled tool-calling agents. ([Web AI at the Edge: Local Vector Search, Gemma 4, & hybrid cloud routing](../videos/2026-11-20-web-ai-at-the-edge-local-vector-search-gemma-4-hybrid-cloud.md), 2026-11-20, relevance 4/5)
- MCP supply-chain risk is real: a spoofed postmark-mcp npm package was clean for 15 versions then added a hidden BCC. An audit of the MCP registry (~47,000 servers) found ~30% had no findable source, and among 400 scanned repos the average OpenSSF Scorecard was 3.9 with 91% unsigned releases; builders should sign (Sigstore), publish SBOMs and users should pin versions and grant least access. ([20 Nov - MCP Dev Summit Nairobi 2026 Livestream](../videos/2026-11-20-20-nov-mcp-dev-summit-nairobi-2026-livestream.md), 2026-11-20, relevance 4/5)
- Progressive disclosure for MCP: tools/list returns a whole catalog and causes context bloat, token cost and wrong-tool selection; Neo4j's agent memory server cut 16 exposed tools to a 6-tool core profile with extended tools revealed on demand. Rubric: model-chosen actions are tools, reusable context is a resource, procedures are skills, must-always-happen steps are invisible plumbing, and who-may-act is authorization. ([20 Nov - MCP Dev Summit Nairobi 2026 Livestream](../videos/2026-11-20-20-nov-mcp-dev-summit-nairobi-2026-livestream.md), 2026-11-20, relevance 4/5)
- Tool results need a third state, 'unknown', alongside success/failed: when a write call returns no verifiable handle, reporting 'failed' makes agents retry (duplicate deployments, wasted tokens) and 'success' is a false claim. Write tools should return a unique ID for verification and agents should not retry immediately on failure. ([20 Nov - MCP Dev Summit Nairobi 2026 Livestream](../videos/2026-11-20-20-nov-mcp-dev-summit-nairobi-2026-livestream.md), 2026-11-20, relevance 4/5)
- Not all content should be machine-translated by the model: legal text needs verbatim official-language sources (Irish takes precedence in Irish law) and creative text relies on human localization, so servers should decide per content type whether to ship official translations. ([20 Nov - MCP Dev Summit Nairobi 2026 Livestream](../videos/2026-11-20-20-nov-mcp-dev-summit-nairobi-2026-livestream.md), 2026-11-20, relevance 4/5)
- MCP internationalization (SEP-2792) borrows HTTP Accept-Language/Content-Language negotiation: clients send the user's OS language preferences to every MCP server (header for HTTP, metadata for stdio) and servers reply with localized tool titles, MCP App UI and data where available. Approved by core maintainers; expected in the end-of-March release, with agent support around April. ([20 Nov - MCP Dev Summit Nairobi 2026 Livestream](../videos/2026-11-20-20-nov-mcp-dev-summit-nairobi-2026-livestream.md), 2026-11-20, relevance 4/5)
- Lloyd recommends a layered stack. From the bottom up: factories as code, data and context (record all conversations, artifacts, videos and screenshots), sandboxed multi-platform compute, swappable inference (multiple models and harnesses), orchestration, and an API/MCP-first surface that integrates with Slack, Linear, Jira and GitHub. ([Engineer Your Coding Agents Like Any Other System — Zach Lloyd, Warp](../videos/2026-11-20-engineer-your-coding-agents-like-any-other-system-zach-lloyd.md), 2026-11-20, relevance 3/5)
- For small on-device models, avoid exposing 100+ tools; use contextual or hierarchical tool loading by domain, short categorical schemas, and a pre-routing classifier that calls a tool at high confidence (~0.85) and asks for clarification at low confidence. ([19 Nov - MCP Dev Summit Nairobi 2026 Livestream](../videos/2026-11-19-19-nov-mcp-dev-summit-nairobi-2026-livestream.md), 2026-11-19, relevance 3/5)
- Policy must be enforced in MCP server code, not left to the model: check identity and scope on every request, deny tools by default, and decode JWT scopes against the tool name passed in the request header. ([19 Nov - MCP Dev Summit Nairobi 2026 Livestream](../videos/2026-11-19-19-nov-mcp-dev-summit-nairobi-2026-livestream.md), 2026-11-19, relevance 3/5)
- Tool descriptions are injected into model context with high authority, so a poisoned description (e.g., hidden instruction to read a credentials file and not tell the user) leaked dummy credentials 10/10 times with Claude Haiku on Bedrock; regex description scanners caught only 20 of 45 scenarios at 7.2% false positives. ([19 Nov - MCP Dev Summit Nairobi 2026 Livestream](../videos/2026-11-19-19-nov-mcp-dev-summit-nairobi-2026-livestream.md), 2026-11-19, relevance 3/5)
- In the FHIR + MCP clinical demo, read-only MCP resources (missed-appointment policy, SMS templates, lab catalog, clinician directory) constrain the agent, and a communication request passes gates for authorization, consent and recipient validity, with an option for human review before sending. ([19 Nov - MCP Dev Summit Nairobi 2026 Livestream](../videos/2026-11-19-19-nov-mcp-dev-summit-nairobi-2026-livestream.md), 2026-11-19, relevance 3/5)
- Shipping an MCP server means shipping domain expertise: IHME's Global Burden of Disease MCP encodes methodological guardrails (e.g., not summing comorbid conditions, separating population change from disease trend) so Claude answers with citations and confidence intervals across 15+ queries. ([19 Nov - MCP Dev Summit Nairobi 2026 Livestream](../videos/2026-11-19-19-nov-mcp-dev-summit-nairobi-2026-livestream.md), 2026-11-19, relevance 3/5)
- The July 2026 MCP spec moved to a stateless core: no initialize handshake or session IDs, a server discover API for capabilities, protocol/client info passed per request in a _meta envelope, list responses cacheable via a TTL, and mid-execution elicitation handled by echoing an encrypted request state field. ([19 Nov - MCP Dev Summit Nairobi 2026 Livestream](../videos/2026-11-19-19-nov-mcp-dev-summit-nairobi-2026-livestream.md), 2026-11-19, relevance 3/5)
- The speaker no longer believes 'Bash is all you need' and now prefers MCP to CLIs. He frames Bash dominance as a training remnant, with code mode, skills and progressive disclosure as alternative ways for agents to act. ([The Sweet Side of the Bitter Lesson — Thariq Shihipar, Independent](../videos/2026-11-19-the-sweet-side-of-the-bitter-lesson-thariq-shihipar-independ.md), 2026-11-19, relevance 4/5)
- Pre-computing ranked candidate fix locations through taint-analysis source/sink reasoning and handing them to the agent via an MCP, instead of letting it patch every reported sink, cut LLM-generated code about 3x per vulnerability class per repo. ([We Built AI Agents To Fix Security Findings in Production](../videos/2026-11-19-we-built-ai-agents-to-fix-security-findings-in-production.md), 2026-11-19, relevance 3/5)
- Tools can be included or excluded per subagent. In the demo, the reviewer workers are set to read-only so they can review code but cannot write any. ([Build a "software factory" that doesn’t produce AI Slop](../videos/2026-11-19-build-a-software-factory-that-doesn-t-produce-ai-slop.md), 2026-11-19, relevance 3/5)
- BigQuery Graph lets you define graph relationships over existing BigQuery tables and query connected records with GQL (graph query language); the same facts could be fetched with table joins, but defined relationships make multi-hop queries easier. ([Why everyone is talking about graphs in AI (and when to skip them)](../videos/2026-11-19-why-everyone-is-talking-about-graphs-in-ai-and-when-to-skip.md), 2026-11-19, relevance 4/5)
- Interactive connectors open third-party apps in full beside the chat. The user can edit directly or ask Claude to edit, and approves everything Claude does, with Claude operating within each person's existing permissions. ([Five brand new ways to use Claude at work](../videos/2026-11-18-five-brand-new-ways-to-use-claude-at-work.md), 2026-11-18, relevance 4/5)
- Scribant's execution gate keeps the agent pipeline read-only. It generates proposal cards and nothing touches Google Calendar or Jira until the user clicks Approve, while the agent deliberately stays silent and doesn't interrupt the speaker. ([Why your AI agent keeps forgetting (and getting slower)](../videos/2026-11-17-why-your-ai-agent-keeps-forgetting-and-getting-slower.md), 2026-11-17, relevance 3/5)
- Plugin extensions let you add sidebar entries, side panels, full-page views and custom file viewer and composer behaviour across the Codex desktop app and ChatGPT. Dom built a design-system browser plugin from one prompt; it has an 'add to composer' button and @-mention autocomplete that inject component context so the agent doesn't have to search for it. ([New Ways of Working with Codex — Dominik Kundel & Charlie Guo, OpenAI](../videos/2026-11-17-new-ways-of-working-with-codex-dominik-kundel-charlie-guo-op.md), 2026-11-17, relevance 4/5)
- He predicted a major prompt-injection disaster and it has not happened, which he attributes to models becoming much better at resisting injection tricks. ([2026 in LLMs — Simon Willison](../videos/2026-11-17-2026-in-llms-simon-willison.md), 2026-11-17, relevance 3/5)

## Open questions

- Will MCP beat CLI/bash on cost and latency for developer agents, or will code mode with structured outputs become the default way to call tools?
- Is prompt injection really solved by better models, given the 10/10 tool-poisoning leak with Claude Haiku and weak description scanners?
- Will WAG agent identity and EMA become cross-vendor OAuth standards, or stay specific to Claude, Okta and Slack?
- Will Claude and other clients adopt the MCP events spec and plugin-extension UI patterns that ChatGPT pioneered, or will MCP Apps surfaces fragment by vendor?
- How will SEP-2792 localization interact with MCP App UI and design tokens when it ships around March–April 2027?

## Changelog

_No changes yet._
