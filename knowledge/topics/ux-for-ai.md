# UX for AI

> Interaction design for AI and agentic products, trust, transparency, generative UI, AX.

_44 active · 0 stale · synthesis updated 2026-11-22_

## Current best understanding

**Supervision has replaced reading code as the core AX problem (Nov 2026).** Agent activity grows exponentially while human attention stays flat. One builder sends 120–190 prompts a day and has agents active many times longer than his workday. Devin ran an Android app for 44 days, merging 40–50 PRs on days with no human messages. Teams are moving to 1–2 day loops in which agents work and humans validate. The design response is **evidence-based review**:
- Devin replies in Slack with a PR plus a video of the fix.
- Ramp's Inspect attaches the conversation, tools used, before/after screenshots and a recording of a verification agent to each PR. Sessions are public by default so people learn from each other.
- Some builders request a typeset HTML executive summary at ~70% of the trajectory, before verification.
- Claude Sheets outlines every edit as it lands.
- Claude Data shows certified-query badges on AI-generated charts.
- Antigravity lets you open any subagent's conversation and message it directly.

The bottleneck is moving sideways to design, risk and compliance, whose rules (such as a bank's colorblind-accessibility scheme) must be encoded into agents. A related pattern keeps a human-owned, linted 'spec' folder separate from agent-owned code.

**Approval gates must be structural, not instructional.** Telling an agent to wait does not guarantee it will. Google ADK uses deterministic graph nodes to pause for human review; in its refund demo the reviewer's reason is passed into the drafted reply. Concrete gate patterns:
- Scribant's read-only proposal cards.
- Permission prompts before seeding scripts.
- Audit lists before destructive deletes.
- Claude interactive connectors that run within each user's existing permissions.

Silent wrong answers are the main trust risk, so surface the definitions and assumptions the agent applied. Looker's governed agent hands off to an editable Explore deep link, and PII tags drive redaction. Fabrication can be reduced by grounding summaries in actions actually taken and rewarding honest partial-progress reports. Vibe coding without such structure loses comprehension, because models silently make design decisions.

**Direct-manipulation and context patterns are maturing (Nov 2026).**
- Whiteboard drag-to-select sets the scope Claude works on.
- Codex appshots capture the screenshot plus the accessibility tree.
- The Codex annotations API makes design-system components selectable while excluding Storybook chrome.
- Codex plugins inject component context via @-mentions and 'add to composer'.
- Claude Meetings joins calls as a visible participant.

For building AI UI: use dev-only inspector routes with state presets (welcome, thinking, proposal, error/timeout) and split editable, prop and computed state. Choose output formats for humans, since models now produce HTML, React, Swift or Figma JSON with roughly equal quality. Hybrid apps should benchmark on device, start on the cloud, then switch to local (e.g. Gemma 4) with 'privacy mode' or offline fallbacks. Guided agent flows should pace one step at a time and tolerate console UI drift. Local models also need web search for tools released after their training cutoff.

## Latest active insights

- He stopped reading code in many cases and instead hooks into the agent's trajectory around the 70% point, before verification. There he prompts it to produce a short executive summary as a typeset HTML page, which keeps his understanding in sync with the agent. ([Build the Workshop Before the Software Factory — Armin Ronacher, Earendil](../videos/2026-11-22-build-the-workshop-before-the-software-factory-armin-ronache.md), 2026-11-22, relevance 4/5)
- Human attention stays flat while agent activity grows exponentially. He sends a steady 120–190 prompts per day, and agent active time went from less than one working day to many times his working day. He started 141 repos but regularly maintains only 10–15, and friends report a similar pattern. ([Build the Workshop Before the Software Factory — Armin Ronacher, Earendil](../videos/2026-11-22-build-the-workshop-before-the-software-factory-armin-ronache.md), 2026-11-22, relevance 4/5)
- Local models fail at tasks involving tools or hardware released after their training cutoff unless the harness gives them web search. Adding search let a local Qwen model change GPU fan RGB colors after it had failed without search. ([What Runs Where? Local AI in Production — Ahmad Osman, Osmantic](../videos/2026-11-21-what-runs-where-local-ai-in-production-ahmad-osman-osmantic.md), 2026-11-21, relevance 2/5)
- The agent asked explicit permission before running a seeding script, which loaded 41 canonical exercises into a Firestore exercises collection — an example of an approval gate for side-effecting actions. ([From prototype to real Firebase backend (no code)](../videos/2026-11-21-from-prototype-to-real-firebase-backend-no-code.md), 2026-11-21, relevance 3/5)
- Agent instructions about console UI drifted from the real Firebase Console (e.g., authentication now sits under Security, Firestore under Databases and storage), so guided flows must tolerate UI mismatch. ([From prototype to real Firebase backend (no code)](../videos/2026-11-21-from-prototype-to-real-firebase-backend-no-code.md), 2026-11-21, relevance 3/5)
- Ask the agent to give 'one step at a time' and wait for confirmation, which turns a long setup checklist into a paced, conversational human-in-the-loop guide. ([From prototype to real Firebase backend (no code)](../videos/2026-11-21-from-prototype-to-real-firebase-backend-no-code.md), 2026-11-21, relevance 3/5)
- Graceful degradation means falling back to a preloaded local Gemma when offline, for example browsing cached products and queueing cart items to sync later. Progressive enhancement means unlocking capabilities such as image-based search when the device has more VRAM. ([Web AI at the Edge: Local Vector Search, Gemma 4, & hybrid cloud routing](../videos/2026-11-20-web-ai-at-the-edge-local-vector-search-gemma-4-hybrid-cloud.md), 2026-11-20, relevance 4/5)
- The recommended hybrid flow runs a quick on-device benchmark first and delegates to the cloud if it fails. If it passes, the app still uses the cloud while the model downloads, then switches to local and can expose a toggle such as 'privacy mode now available' or an offline mode. ([Web AI at the Edge: Local Vector Search, Gemma 4, & hybrid cloud routing](../videos/2026-11-20-web-ai-at-the-edge-local-vector-search-gemma-4-hybrid-cloud.md), 2026-11-20, relevance 4/5)
- Trust in agent output comes from attaching provenance to the PR: the full conversation, the tools used, before and after screenshots, and a video of a verification agent clicking through the app in a browser. ([How to build an agent that builds the culture — Zach Bruggeman, Ramp](../videos/2026-11-20-how-to-build-an-agent-that-builds-the-culture-zach-bruggeman.md), 2026-11-20, relevance 4/5)
- Making every agent session public by default replaces formal AI training: people learn by watching teammates' sessions, and can even ask the agent to summarize how a colleague structures prompts or breaks down problems. ([How to build an agent that builds the culture — Zach Bruggeman, Ramp](../videos/2026-11-20-how-to-build-an-agent-that-builds-the-culture-zach-bruggeman.md), 2026-11-20, relevance 4/5)
- Splitting a codebase into agent-owned engine code and a human-owned 'spec/human' folder restores control. The human folder is linted, governed by rules for Claude, reads like English, and uses domain units such as meters instead of magic numbers. ([The Sweet Side of the Bitter Lesson — Thariq Shihipar, Independent](../videos/2026-11-19-the-sweet-side-of-the-bitter-lesson-thariq-shihipar-independ.md), 2026-11-19, relevance 4/5)
- Pure vibe coding caused loss of comprehension and flow: the model silently made many design decisions, such as whether a rock passes through a wall, its speed or its charge. The author no longer knew what his own characters did and made less progress. ([The Sweet Side of the Bitter Lesson — Thariq Shihipar, Independent](../videos/2026-11-19-the-sweet-side-of-the-bitter-lesson-thariq-shihipar-independ.md), 2026-11-19, relevance 4/5)
- Models' smooth interior means output format is no longer constrained: the same mockup can be produced as HTML, React, Swift or Figma's proprietary JSON with roughly equal quality. So choose formats for human needs, not model preference. ([The Sweet Side of the Bitter Lesson — Thariq Shihipar, Independent](../videos/2026-11-19-the-sweet-side-of-the-bitter-lesson-thariq-shihipar-independ.md), 2026-11-19, relevance 4/5)
- Verification should run as an inner loop within a turn (build, lint, type, runtime errors, headless browser exploration) and an outer loop between turns (visitor behaviour, automatic A/B tests, payment conversions) so agents optimise business outcomes, not just code. ([What it takes to set intelligence free — Fabian Hedin, CTO, Lovable](../videos/2026-11-19-what-it-takes-to-set-intelligence-free-fabian-hedin-cto-lova.md), 2026-11-19, relevance 4/5)
- Antigravity's supervision features include clicking into any worker to see its full conversation and messaging subagents directly to steer or stop them. A /learn command lets the agent repair and refine the workers' procedures over time. ([Build a "software factory" that doesn’t produce AI Slop](../videos/2026-11-19-build-a-software-factory-that-doesn-t-produce-ai-slop.md), 2026-11-19, relevance 3/5)
- In the refund demo, three checks (order, payment, refund history) run in parallel, join at a rules node, which routes the case to human review; after approval with a reason, a response agent drafts the reply using the facts plus the human decision. ([Why everyone is talking about graphs in AI (and when to skip them)](../videos/2026-11-19-why-everyone-is-talking-about-graphs-in-ai-and-when-to-skip.md), 2026-11-19, relevance 4/5)
- Telling a single agent in its instructions to wait for human approval does not guarantee it will wait; a deterministic workflow node that pauses execution is needed to enforce human-in-the-loop review. ([Why everyone is talking about graphs in AI (and when to skip them)](../videos/2026-11-19-why-everyone-is-talking-about-graphs-in-ai-and-when-to-skip.md), 2026-11-19, relevance 4/5)
- Interactive connectors open third-party apps in full beside the chat. The user can edit directly or ask Claude to edit, and approves everything Claude does, with Claude operating within each person's existing permissions. ([Five brand new ways to use Claude at work](../videos/2026-11-18-five-brand-new-ways-to-use-claude-at-work.md), 2026-11-18, relevance 4/5)
- Claude Data lets data teams certify queries, and any chart built on a certified query shows a certified badge. The badge acts as a provenance and trust signal on AI-generated visualizations, and live sharing shows up-to-date dashboards to viewers who lack data-source access. ([Five brand new ways to use Claude at work](../videos/2026-11-18-five-brand-new-ways-to-use-claude-at-work.md), 2026-11-18, relevance 4/5)
- In Whiteboards, a user can drag a box around a messy region and ask Claude about only that selection. This spatial-selection-as-scope pattern lets the user set the agent's context through direct manipulation instead of prompting. ([Five brand new ways to use Claude at work](../videos/2026-11-18-five-brand-new-ways-to-use-claude-at-work.md), 2026-11-18, relevance 4/5)
- In Claude Sheets, every edit Claude makes is outlined as it lands while humans edit the same cells. This is a concrete visible-diff pattern for supervising agent changes in multiplayer artifacts. ([Five brand new ways to use Claude at work](../videos/2026-11-18-five-brand-new-ways-to-use-claude-at-work.md), 2026-11-18, relevance 4/5)
- Claude Meetings joins a call from the calendar as a participant everyone can see. It takes notes, answers questions in writing, and builds docs or whiteboards on a shared meeting page during the call, so artifacts are ready when the call ends. ([Five brand new ways to use Claude at work](../videos/2026-11-18-five-brand-new-ways-to-use-claude-at-work.md), 2026-11-18, relevance 4/5)
- Fabrication is reduced by filtering training trajectories with unsupported claims, grounding the agent's final summary in the actions it actually took, and rewarding honest partial-progress reports over faked completion. ([Post-Training Gemini 4 for Real Engineering Work — Melvin Johnson, Google DeepMind](../videos/2026-11-18-post-training-gemini-4-for-real-engineering-work-melvin-john.md), 2026-11-18, relevance 3/5)
- An Android app was built and maintained by Devin over 44 days by mirroring the iOS app, with permanent hooks on the iOS codebase, Slack feedback monitoring and pixel-level live QA. On most days there were no human messages, and Devin merged 40-50 PRs on those days. ([40x More Merged PRs With 2.7x the Engineers — Walden Yan, CPO, Cognition](../videos/2026-11-18-40x-more-merged-prs-with-2-7x-the-engineers-walden-yan-cpo-c.md), 2026-11-18, relevance 4/5)
- The recommended delegation model is 'jobs, not tasks': give an agent a measurable goal such as P99 latency, layout shift or onboarding retention, and let it add telemetry, set alerts, break down work and send daily progress reports. ([40x More Merged PRs With 2.7x the Engineers — Walden Yan, CPO, Cognition](../videos/2026-11-18-40x-more-merged-prs-with-2-7x-the-engineers-walden-yan-cpo-c.md), 2026-11-18, relevance 4/5)

## Open questions

- Which evidence artifact scales best for supervision (video walkthroughs, HTML summaries, live diffs or certified badges), and how should a component library standardize them?
- When is it safe to remove human review checkpoints from a loop, and how is that confidence measured and shown to users?
- How should design-system and accessibility rules be encoded so agents reliably enforce them (Claude rules, linting, annotations APIs or plugins)?
- How should agents surface their assumptions and definitions to prevent silent wrong answers without overwhelming non-expert users?
- Will 'jobs, not tasks' delegation toward measurable goals need new UI for goal setting, progress reports and escalation thresholds?

## Changelog

_No changes yet._
