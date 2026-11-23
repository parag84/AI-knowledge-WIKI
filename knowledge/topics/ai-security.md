# AI security

> Agent containment and sandboxing, prompt injection, credentials for agents, AI-driven vulnerability discovery.

_56 active · 0 stale · synthesis updated 2026-11-23_

## Current best understanding

**Enforce agent boundaries in code, not prompts.** This is the strongest consensus of November 2026. Several separate signals point the same way:

- **Human approval is weak.** In Anthropic's August study, humans caught only about 14% of clearly dangerous commands. Claude Code's auto mode, the default permission mode since August, uses a separate classifier configured in plain English and blocked 89%. Anything that must never happen therefore needs a deny rule, which is checked before the classifier sees the call.
- **Reversibility should decide what gets enforced.** Mistakes you can undo can be left to the model. Irreversible ones need rules plus OS-level sandboxing or isolated cloud sessions, because permissions alone can't stop a script from reading .env or SSH keys.
- **Payments split decide, authorize and execute.** Korapay's Trustline lets the LLM only propose an intent. PIN entry happens in a WhatsApp Flow the model never sees, and settlement requires a scoped, signed token. Deterministic referees (no LLM) arbitrate conflicting agent plans and send ties to a human.
- **Narrow agents beat broad ones.** A Gmail-only agent is more trustworthy than a Gmail skill loaded into a general agent.

For Parag's AX work, this means approval UI should be a last resort layered on deterministic gates. It should not be the primary safety mechanism. Handovers between modes should be explained transparently, as in GRIT's multi-turn Zuzie risk routing.

**MCP auth and supply chain (as of Nov 2026).** The spec's auth evolved in stages:

- The initial November 2024 spec left auth to developers.
- The March 2025 spec adopted OAuth 2.1.
- The June spec let servers delegate the authorization server to enterprise IdPs such as Okta and Entra ID.
- The July spec added issuer validation, alongside per-client consent and a token passthrough ban. The next revision is planned for March.

Other identity work is moving alongside the spec:

- Enterprise-managed authorization (EMA/ID-JAG), live in Claude, removes consent prompts across an organization.
- WAG proposes short-lived agent tokens carrying policy claims.
- DPoP and workload identity federation replace static secrets.
- Servers must still check identity and scope on every request and deny tools by default.
- Managed servers such as Looker's only offer instance-wide tool toggles, so per-agent scoping has to come from roles.

Tool descriptions are a high-authority injection vector. A poisoned description leaked credentials 10 out of 10 times with Claude Haiku, and regex scanners caught only 20 of 45 scenarios. The registry is risky too: an audit of about 47k servers found ~30% had no findable source, the average OpenSSF Scorecard was 3.9 and 91% of releases were unsigned. Pin versions, use Sigstore and SBOMs, and grant least access.

**AI vulnerability discovery is scaling fast and producing reusable UX patterns.**

- **Model results:** OpenAI reports GPT-6 Cyber at 52% on ExploitGym versus ~38% for Mythos 5.2. Through Mozilla it found 81 new high-severity Firefox bugs and re-rated known bugs upward by chaining them, so findings need re-prioritizing whenever models improve.
- **Access tiers:** Claude Mythos is gated behind a KYC-style Cyber Verification Program, while Fable runs the same weights without KYC. OpenAI's Daybreak Blue requires business verification and per-role or per-project enablement.
- **Verification:** Mozilla requires every finding to pass a deterministic verifier and a cheat-checking judge agent. Duolingo closes any PR that touches non-test files, defending against agents reward-hacking toward green CI. Agent-written patches are treated as evidence rather than landable fixes.
- **UX patterns:**
  - Findings are presented as summary, attack path and evidence, with a 'Generate fix' handoff.
  - Scans run in visible stages and accept free-text scope intent.
  - Red Team campaign specs are drafted conversationally.
  - A live campaign view lets users adjust scope mid-run.
  - Users choose between background fixes and steering the fix in the foreground.

## Latest active insights

- Cited stats motivate the problem: PagerDuty reports ~70% of orgs run 2+ agents in production and 85% want better error detection; a Cloud Security Alliance survey is cited as attributing 65% of production incidents to AI agents. ([Multi-Agent SRE: What Happens When Your Agents Want Opposite Things - Aditi Mewada, Apple](../videos/2026-11-22-multi-agent-sre-what-happens-when-your-agents-want-opposite.md), 2026-11-22, relevance 3/5)
- Suggested priority order: safety/security > availability/SLO > performance > cost, plus domain pre-checks like minimum headroom (e.g., two AZs always up), incident freezes, and cost caps (e.g., block if over $500/hour). ([Multi-Agent SRE: What Happens When Your Agents Want Opposite Things - Aditi Mewada, Apple](../videos/2026-11-22-multi-agent-sre-what-happens-when-your-agents-want-opposite.md), 2026-11-22, relevance 3/5)
- The referee should be pure deterministic code with no LLM, performing three steps: detect conflicts, rank by priority, and lease the target. Stale plans (base version ≠ current state version) are sent back to re-plan, outranked proposals are deferred, and ties go to the on-call human. ([Multi-Agent SRE: What Happens When Your Agents Want Opposite Things - Aditi Mewada, Apple](../videos/2026-11-22-multi-agent-sre-what-happens-when-your-agents-want-opposite.md), 2026-11-22, relevance 3/5)
- MCP supply-chain risk is real: a spoofed postmark-mcp npm package was clean for 15 versions then added a hidden BCC. An audit of the MCP registry (~47,000 servers) found ~30% had no findable source, and among 400 scanned repos the average OpenSSF Scorecard was 3.9 with 91% unsigned releases; builders should sign (Sigstore), publish SBOMs and users should pin versions and grant least access. ([20 Nov - MCP Dev Summit Nairobi 2026 Livestream](../videos/2026-11-20-20-nov-mcp-dev-summit-nairobi-2026-livestream.md), 2026-11-20, relevance 4/5)
- Keyword-triggered, single-turn guardrails that hard-stop and refer out fail vulnerable users (missed implicit danger, over-firing on a stubbed toe); GRIT's proposed Zuzie architecture classifies risk over several turns, stores risk metadata in state, routes to normal vs high-risk personas, explains handovers transparently and keeps the conversation going. ([20 Nov - MCP Dev Summit Nairobi 2026 Livestream](../videos/2026-11-20-20-nov-mcp-dev-summit-nairobi-2026-livestream.md), 2026-11-20, relevance 4/5)
- Trustline (Korapay) separates deciding, authorizing and executing: the LLM only proposes a payment intent with a summary, the fare is held ~15 minutes, PIN entry happens in a WhatsApp Flow the model never sees, and a scoped Kora payment token (single merchant, amount bounds, signed) is required before settlement; payment states map to completed/pending/failed/unchanged-on-unknown. ([20 Nov - MCP Dev Summit Nairobi 2026 Livestream](../videos/2026-11-20-20-nov-mcp-dev-summit-nairobi-2026-livestream.md), 2026-11-20, relevance 4/5)
- Policy must be enforced in MCP server code, not left to the model: check identity and scope on every request, deny tools by default, and decode JWT scopes against the tool name passed in the request header. ([19 Nov - MCP Dev Summit Nairobi 2026 Livestream](../videos/2026-11-19-19-nov-mcp-dev-summit-nairobi-2026-livestream.md), 2026-11-19, relevance 3/5)
- Tool descriptions are injected into model context with high authority, so a poisoned description (e.g., hidden instruction to read a credentials file and not tell the user) leaked dummy credentials 10/10 times with Claude Haiku on Bedrock; regex description scanners caught only 20 of 45 scenarios at 7.2% false positives. ([19 Nov - MCP Dev Summit Nairobi 2026 Livestream](../videos/2026-11-19-19-nov-mcp-dev-summit-nairobi-2026-livestream.md), 2026-11-19, relevance 3/5)
- In the FHIR + MCP clinical demo, read-only MCP resources (missed-appointment policy, SMS templates, lab catalog, clinician directory) constrain the agent, and a communication request passes gates for authorization, consent and recipient validity, with an option for human review before sending. ([19 Nov - MCP Dev Summit Nairobi 2026 Livestream](../videos/2026-11-19-19-nov-mcp-dev-summit-nairobi-2026-livestream.md), 2026-11-19, relevance 3/5)
- An agent's ability to act should not automatically confer authority to act; agentic standards should define scoped permissions, mandatory human-in-the-loop decisions, traceability of every action, and reversibility when systems fail. ([19 Nov - MCP Dev Summit Nairobi 2026 Livestream](../videos/2026-11-19-19-nov-mcp-dev-summit-nairobi-2026-livestream.md), 2026-11-19, relevance 3/5)
- Over the last two weeks the system raised 242 PRs, of which 84 merged and 29 closed, at an organization of ~10,000 developers; the team says it is open sourcing the code flow solver, MCP and observability stack. ([We Built AI Agents To Fix Security Findings in Production](../videos/2026-11-19-we-built-ai-agents-to-fix-security-findings-in-production.md), 2026-11-19, relevance 3/5)
- Gate before opening a PR: verify a working baseline build first, run on an isolated copy, require no new findings and a reduced finding count, and cap retries by budget/time/runs, reverting everything if gates fail; enforce agent boundaries in code rather than prompts because prompts are easier to circumvent. ([We Built AI Agents To Fix Security Findings in Production](../videos/2026-11-19-we-built-ai-agents-to-fix-security-findings-in-production.md), 2026-11-19, relevance 3/5)
- Pre-computing ranked candidate fix locations through taint-analysis source/sink reasoning and handing them to the agent via an MCP, instead of letting it patch every reported sink, cut LLM-generated code about 3x per vulnerability class per repo. ([We Built AI Agents To Fix Security Findings in Production](../videos/2026-11-19-we-built-ai-agents-to-fix-security-findings-in-production.md), 2026-11-19, relevance 3/5)
- The workload authorization grant (WAG) is positioned as the path to agent identity: agents get short-lived tokens with embedded policy claims, such as Slack workspace and channel, so downstream services can make authorization decisions instead of relying on a human's borrowed token. ([MCP Security, Two Years In - Den Delimarsky, Anthropic](../videos/2026-11-16-mcp-security-two-years-in-den-delimarsky-anthropic.md), 2026-11-16, relevance 4/5)
- DPoP binds bearer tokens to a device key, for example one generated by a TPM chip, so a stolen token is unusable. Workload identity federation replaces vault-stored static secrets with short-lived, platform-issued credentials. ([MCP Security, Two Years In - Den Delimarsky, Anthropic](../videos/2026-11-16-mcp-security-two-years-in-den-delimarsky-anthropic.md), 2026-11-16, relevance 4/5)
- Security is enforced through SDK conformance tests rather than guidance alone. Roughly a third of about 116 conformance scenarios are authorization- or security-related, and SDK tiers set expectations for how quickly security issues get fixed. ([MCP Security, Two Years In - Den Delimarsky, Anthropic](../videos/2026-11-16-mcp-security-two-years-in-den-delimarsky-anthropic.md), 2026-11-16, relevance 4/5)
- Production incidents drove specific spec mitigations: per-client consent against confused-deputy attacks, a ban on token passthrough, and validation of both token audience and issuer to block mix-up attacks. ([MCP Security, Two Years In - Den Delimarsky, Anthropic](../videos/2026-11-16-mcp-security-two-years-in-den-delimarsky-anthropic.md), 2026-11-16, relevance 4/5)
- Enterprise-managed authorization (EMA, also called ID-JAG or XAA) lets an admin connect an MCP server once so that nobody in the organization ever sees a consent prompt. It also prevents users from accidentally connecting personal accounts such as a personal Gmail. ([MCP Security, Two Years In - Den Delimarsky, Anthropic](../videos/2026-11-16-mcp-security-two-years-in-den-delimarsky-anthropic.md), 2026-11-16, relevance 4/5)
- MCP deliberately dropped free-form auth (API keys, certificates) in favour of OAuth 2.1. Later spec revisions let servers delegate the authorization server to enterprise IdPs such as Okta or Entra ID instead of implementing one themselves, so that every client connects to every server the same way. ([MCP Security, Two Years In - Den Delimarsky, Anthropic](../videos/2026-11-16-mcp-security-two-years-in-den-delimarsky-anthropic.md), 2026-11-16, relevance 4/5)
- Real-time AI security monitoring is argued to be feasible because detecting misbehavior is easier than doing it; the blocker is that monitors haven't been fast, cheap and reliable enough to run inline. (["Where is all the automation?" — Diogo Almeida, TypeSafe AI](../videos/2026-11-15-where-is-all-the-automation-diogo-almeida-typesafe-ai.md), 2026-11-15, relevance 3/5)
- Agent-generated patches are usually not landable as is, because they are often too narrow or miss codebase context. Expert engineers use them as evidence and write the final fix, and the team kept pace with an approximately 8x increase in discovery and fixes from 2025 to 2026. ([How Mozilla uses GPT-6 Cyber to find and fix Firefox vulnerabilities](../videos/2026-11-13-how-mozilla-uses-gpt-6-cyber-to-find-and-fix-firefox-vulnera.md), 2026-11-13, relevance 3/5)
- GPT-6 Cyber rediscovered bugs that had been rated sec-moderate or sec-low and showed they were actually sec-high by bypassing architectural hardening the team had thought was bulletproof. This prompted re-prioritization and more defense-in-depth work. ([How Mozilla uses GPT-6 Cyber to find and fix Firefox vulnerabilities](../videos/2026-11-13-how-mozilla-uses-gpt-6-cyber-to-find-and-fix-firefox-vulnera.md), 2026-11-13, relevance 3/5)
- Deduplicating findings is unexpectedly hard because similar crash stacks can hide different bugs. Mozilla gives an agent the findings database to decide, then sets reminders to re-verify a finding marked as a duplicate once the original bug's fix lands. ([How Mozilla uses GPT-6 Cyber to find and fix Firefox vulnerabilities](../videos/2026-11-13-how-mozilla-uses-gpt-6-cyber-to-find-and-fix-firefox-vulnera.md), 2026-11-13, relevance 3/5)
- Variant scans give an agent a known bug, fixed or open, and ask it to hunt for the same pattern across the codebase. In September they were the majority of bugs found, and they tended to produce fewer duplicates. ([How Mozilla uses GPT-6 Cyber to find and fix Firefox vulnerabilities](../videos/2026-11-13-how-mozilla-uses-gpt-6-cyber-to-find-and-fix-firefox-vulnera.md), 2026-11-13, relevance 3/5)
- Target selection began with an LLM scoring each file for risk, such as exposure to web content and memory-safety traits, enriched with Mozilla's own threat-model docs. It later moved to a coding agent querying a SQLite database of runs, bugs and engineer comments to propose the next scan batch, which a human approves. ([How Mozilla uses GPT-6 Cyber to find and fix Firefox vulnerabilities](../videos/2026-11-13-how-mozilla-uses-gpt-6-cyber-to-find-and-fix-firefox-vulnera.md), 2026-11-13, relevance 3/5)

## Open questions

- If humans catch only ~14% of dangerous commands, what role should approval UI play versus deny rules and sandboxing, and how should agent UIs communicate that split?
- Can tool-description poisoning be reliably detected at all, given regex scanners catch under half of scenarios, or must clients treat all descriptions as untrusted?
- Will WAG and EMA/ID-JAG become broadly adopted OAuth standards, and what will the March MCP spec revision change about agent identity?
- How reliable are vendor-reported cyber benchmarks (GPT-6 Cyber vs Mythos 5.2) and cited incident stats like CSA's '65% of production incidents caused by agents'?
- How should managed MCP servers expose per-agent tool scoping, rather than instance-wide toggles plus role workarounds?

## Changelog

_No changes yet._
