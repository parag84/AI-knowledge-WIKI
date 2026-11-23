---
title: 'Gemini 4 Argon demo: Remixing 3D apps & Firebase in Google AI Studio'
channel: Google Cloud Tech
url: https://www.youtube.com/watch?v=yQADxQU0trc
video_id: yQADxQU0trc
published: '2026-11-15'
duration: '5:32'
topics:
- coding-agents
- ux-for-ai
- model-releases
- mcp-tools
relevance: 3
status: active
superseded_by: []
---

# Gemini 4 Argon demo: Remixing 3D apps & Firebase in Google AI Studio

[![Gemini 4 Argon demo: Remixing 3D apps & Firebase in Google AI Studio](../assets/thumbs/yQADxQU0trc.webp)](https://www.youtube.com/watch?v=yQADxQU0trc)

**Google Cloud Tech** · 2026-11-15 · 5:32 · relevance 3/5 · [Watch on YouTube](https://www.youtube.com/watch?v=yQADxQU0trc)

## Summary

A short segment from The Google Cloud Show where three Google builders remix existing apps from the Gemini 4 Argon Builders Showcase inside Google AI Studio. They use voice-to-text prompts to add rank/file labels and neon pieces to a 3D chessboard, then prompt Argon to add Firebase Authentication and a shared Firestore leaderboard to a 3D racing game, accepting an in-chat card that enables Firebase. The takeaway is that a remix-from-gallery workflow plus one-click backend provisioning lets non-specialists add features like auth that a presenter says once took about two weeks.

## Key insights

- Google AI Studio lets users fork ('remix') an existing showcase app and change it with one natural-language prompt, including voice-to-text input. This positions a gallery of working apps as the starting point instead of a blank prompt.
  - _Relies on:_ Gemini 4 Argon; Google AI Studio remix feature; Gemini 4 Argon Builders Showcase; voice-to-text prompting _(as of 2026-11-15)_
- When a prompt requires backend services, AI Studio shows an inline card that asks the user to enable Firebase and Firestore before the agent provisions them. This is a mid-task approval step for adding infrastructure.
  - _Relies on:_ Firebase Authentication; Cloud Firestore; inline enable card in Google AI Studio _(as of 2026-11-15)_
- A single prompt produced user authentication plus a real-time shared leaderboard in a 3D racing game. A presenter contrasted this with auth previously taking 'two weeks of my life'.
  - _Relies on:_ Gemini 4 Argon; Firebase Auth; Firestore leaderboard _(as of 2026-11-15)_
- Broad style prompts such as 'make them neon' are followed literally but generically. The presenters note that naming specific colors would give more controlled results, so prompt specificity drives the quality of visual edits.
- Running two remixes of the same app side by side, one for functional labels and one for aesthetic colors, shows that parallel divergent variants of one base app are a cheap way to explore features.

## Tools, models & APIs mentioned

- **Gemini Argon** 4 (model)
- **Google AI Studio** (product)
- **Firebase Authentication** (product)
- **Cloud Firestore** (product)

## How this applies to AX / design systems

The inline 'enable Firebase/Firestore' card is a good reference for a resource-provisioning approval component in an AI component library: a scoped consent prompt the agent raises mid-task. The remix-from-showcase pattern suggests developer portals could offer forkable example apps with a prompt box, so users start from intent instead of reading docs first. A useful experiment would be prototyping a 'remix this sample' entry point on an API docs page that shows the agent's diff and any service-enablement approvals.

_Relevance 3/5: This is a light demo, but the remix-from-showcase flow and the inline 'enable Firebase' consent card are agentic UX patterns Parag works next to._

## Best moments

- [0:31](https://www.youtube.com/watch?v=yQADxQU0trc&t=31s): A feature request turns into a remix of the showcase app in AI Studio.
- [1:04](https://www.youtube.com/watch?v=yQADxQU0trc&t=64s): Voice-to-text prompt and the result of the parallel side-by-side remixes.
- [2:39](https://www.youtube.com/watch?v=yQADxQU0trc&t=159s): Inline card asking to enable Firebase and Firestore, an approval UI pattern.
- [4:10](https://www.youtube.com/watch?v=yQADxQU0trc&t=250s): The 'auth used to take two weeks' claim and a recap of the generated features.
