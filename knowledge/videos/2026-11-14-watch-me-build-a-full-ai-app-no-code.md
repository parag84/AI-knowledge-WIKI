---
title: Watch me build a full AI app (no code)
channel: Google Cloud Tech
url: https://www.youtube.com/watch?v=-nRo5q63b2Y
video_id: -nRo5q63b2Y
published: '2026-11-14'
duration: '55:12'
topics:
- coding-agents
- ux-for-ai
- agent-memory
- agents
relevance: 4
status: active
superseded_by: []
---

# Watch me build a full AI app (no code)

[![Watch me build a full AI app (no code)](../assets/thumbs/-nRo5q63b2Y.webp)](https://www.youtube.com/watch?v=-nRo5q63b2Y)

**Google Cloud Tech** · 2026-11-14 · 55:12 · relevance 4/5 · [Watch on YouTube](https://www.youtube.com/watch?v=-nRo5q63b2Y)

## Summary

An episode of Google Cloud Tech's Build It series in which Devin hands a phase-gated, spec-driven implementation plan to Google Antigravity and builds a smart personal trainer app milestone by milestone, with Gemini doing the coding. The core demo covers gated milestones (setup, backend, workout tracker, AI coach chat with staged proposals, living memory) and shows troubleshooting through the browser console, a dummy 'banana' API key, and asking 'should this be working?' before asking for fixes. The main takeaway is that a non-coder gets better results by building a mental model of the architecture and directing system-level changes, such as passing context from the client and hardening the prompt for surgical edits, instead of repeatedly hitting enter for one-off fixes.

## Key insights

- Structure an agent build as gated milestones. Each milestone ends with a summary table of the tests that were specified earlier, plus a Git checkpoint, and the human approves it explicitly (for example 'gate one approved') before the agent moves on.
  - _Relies on:_ Google Antigravity; Milestone 1 took about 6 minutes, milestone 2 about 3 minutes, milestone 4 about 15 minutes; Checks run: TypeScript compiler, ESLint, build, Git commit checkpoint _(as of 2026-11-14)_
- When an agent edit rewrote the whole week instead of one day, the fix was architectural rather than a one-off patch. The client sends a snapshot of the active plan, or the staged proposal it is replying to, with each request, and the coach prompt is hardened for 'surgical preservation'. After that change, adding a core finisher or swapping Thursday and Friday changed only the targeted items.
  - _Relies on:_ Before the fix, the server fetched plan context from Firebase Firestore, which was not hooked up yet; Passing context from the client was judged faster than a database lookup _(as of 2026-11-14)_
- The coach should pick its response format by intent. A plain question ('what is hypertrophy') should get a text answer with no card, a single-day edit should get a day card, and a weekly plan should get a week card. The day card had to be added because returning the full week for a one-day change was confusing.
- A Modify button attaches the current proposal as a context chip. Free-typed requests without that chip generated a brand-new plan, and the chip should clear on send by calling the same function as the chip's close (x) control, so the logic isn't reimplemented.
- Debug agent apps by checking whether the system 'should be working' before asking for a fix, which avoids sending the agent on a wild goose chase. The presenter verified environment loading by temporarily setting the API key to the word 'banana' and logging it, which showed the app was not reading the env file.
  - _Relies on:_ Gemini API key and model name were set in an environment local file; The model used was stated as Gemini 3.8 Flash instead of the default Gemini 2.5 Flash _(as of 2026-11-14)_
- Living memory: the server bundles memory updates extracted from the chat (equipment, injuries, upcoming events) with the coach's reply. The client updates a local store and a Settings memory viewer, with Firestore sync planned later. Memory items can be deleted and carry expiration dates in a tiered memory design.
  - _Relies on:_ Firebase Firestore; In-memory local fallback stood in for Firestore _(as of 2026-11-14)_

## Tools, models & APIs mentioned

- **Google Antigravity** (product)
- **Gemini Flash** 3.8 (model)
- **Gemini Flash** 2.5 (model)
- **Firebase Firestore** (product)
- **Firebase Admin SDK** (sdk)
- **TypeScript** (other)
- **ESLint** (other)
- **Git** (other)

## How this applies to AX / design systems

The proposal-card lifecycle shown here could each become a documented component in an AI component library with explicit states: staged, accept or plan applied badge, modify, and context chip with clear-on-send. A good AX experiment is a response-type contract that lets the agent return text, a day card or a week card based on intent, with design guidance for each. The Settings memory viewer, with deletable items that expire, is a reusable pattern for making agent memory transparent and editable. The gated-milestone summary tables are also a useful model for approval UI in developer portals.

_Relevance 4/5: The build is a vibe-coding demo, but it surfaces concrete agentic UX patterns: staged proposal cards with accept and modify, context chips, choosing a day card or a week card or text-only answers, and a user-visible living memory viewer, all of which map onto an AI component library._

## Best moments

- [2:32](https://www.youtube.com/watch?v=-nRo5q63b2Y&t=152s): Gated milestone approval with a summary of automated checks and a Git checkpoint
- [16:01](https://www.youtube.com/watch?v=-nRo5q63b2Y&t=961s): Banana API key trick for diagnosing env loading instead of burning tokens
- [19:26](https://www.youtube.com/watch?v=-nRo5q63b2Y&t=1166s): Agent answers a question with text instead of a card, and Modify vs free-typed behaviour
- [39:49](https://www.youtube.com/watch?v=-nRo5q63b2Y&t=2389s): Deciding to pass context from the client and harden the prompt for surgical edits
- [48:33](https://www.youtube.com/watch?v=-nRo5q63b2Y&t=2913s): 'Should it be working?' approach applied to living memory, plus the memory viewer UI
