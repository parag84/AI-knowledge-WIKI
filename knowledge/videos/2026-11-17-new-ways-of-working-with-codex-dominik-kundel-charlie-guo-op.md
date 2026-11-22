---
title: New Ways of Working with Codex — Dominik Kundel & Charlie Guo, OpenAI
channel: AI Engineer
url: https://www.youtube.com/watch?v=IPh9YsWvDQk
video_id: IPh9YsWvDQk
published: '2026-11-17'
duration: '58:03'
topics:
- coding-agents
- agents
- ux-for-ai
- mcp-tools
- model-releases
- infra-cost
relevance: 4
status: active
superseded_by: []
---

# New Ways of Working with Codex — Dominik Kundel & Charlie Guo, OpenAI

[![New Ways of Working with Codex — Dominik Kundel & Charlie Guo, OpenAI](../assets/thumbs/IPh9YsWvDQk.webp)](https://www.youtube.com/watch?v=IPh9YsWvDQk)

**AI Engineer** · 2026-11-17 · 58:03 · relevance 4/5 · [Watch on YouTube](https://www.youtube.com/watch?v=IPh9YsWvDQk)

## Summary

A CODE Summit 2026 workshop from OpenAI's developer experience team (Dominik Kundel and Charlie Guo) catches up on Codex features shipped between July and November. It demos context gathering (plugins, plugin extensions, Appshots, computer use and history, ChatGPT Space), fast UI iteration with Ultrafast and annotations, Codex Cloud v2 environments, shipping with ChatGPT Sites (including the internal Cutroom video-editing workflow), code review, voice as a control plane, Dots and the Agents API. The main takeaway is that the Codex harness now runs across many surfaces with shared context, so the work shifts to supplying good context, staying in fast iteration loops and delegating to the right agent form factor.

## Key insights

- Plugin extensions let you add sidebar entries, side panels, full-page views and custom file viewer and composer behaviour across the Codex desktop app and ChatGPT. Dom built a design-system browser plugin from one prompt; it has an 'add to composer' button and @-mention autocomplete that inject component context so the agent doesn't have to search for it.
  - _Relies on:_ Plugins bundle MCP servers, skills and resources, and mostly use remote MCPs; Plugin extensions can modify sidebar, side panel, full page, file viewer and composer; Built-in features such as Sites, code review and security are themselves plugins; A plugin connected once is shared across all Codex harness surfaces (web, desktop, Slack @ChatGPT) _(as of 2026-11-17)_
- The annotations API lets you declare which DOM elements are selectable in the in-app browser's annotate mode. For example, you can make individual design-system components selectable while excluding the Storybook frame or an emulator chrome.
  - _Relies on:_ The in-app browser has an annotate button (top left) and a live-tweak settings control; By default, annotation hover targets are based on the DOM _(as of 2026-11-17)_
- Appshots (pressing both Command keys on Mac, or both Alt keys on Windows) capture a screenshot plus the page's accessibility tree, including content beyond the fold. This gives the agent far richer context than a plain screenshot.
  - _Relies on:_ Shortcut: left and right Command on macOS, both Alt keys on Windows; The captured text is visible via 'view text' _(as of 2026-11-17)_
- Ultrafast is described as 8x faster at 6x the cost and works best for UI iteration with a hot-reloading dev server and light reasoning effort. It brings little benefit when build or test time dominates the task.
  - _Relies on:_ Ultrafast launched at Dev Day in October for GPT-6.1 Sol and GPT-6 Astra; 8x faster at 6x cost; Recommended reasoning effort: light; high for nuanced tasks _(as of 2026-11-17)_
- Computer history learns your app habits from macOS event streams rather than screenshots, which makes it more token-efficient. Its privacy controls include pause, retroactive clearing of recent history and per-app or per-site exclusion, and private browsing is excluded by default.
  - _Relies on:_ Computer history is macOS-only; Computer use runs in the background with its own cursor; A Chrome extension provides browser context on Windows, Linux and macOS _(as of 2026-11-17)_
- Codex Cloud v2 sets up environments automatically from one or more repositories, working out dependencies, keys and dev commands itself. Environments are snapshotted and kept warm, and they can reach private services through OIDC or Tailscale.
  - _Relies on:_ Multi-repository selection; Linux VMs today, with bring-your-own environments in progress; The CLI command 'codex remote control start' exposes the app server so a phone can connect _(as of 2026-11-17)_
- For delegation, run a default model on medium effort and let it spin up stronger sub-agents for hard problems or cheaper ones for tedious work. Peer sub-agents that coordinate with each other suit interdependent work such as a web app and a mobile app.
  - _Relies on:_ Example setup: Sol on medium, Astra sub-agents on high, Luna sub-agents on high for tedious work; This is not always better or cheaper _(as of 2026-11-17)_

## Tools, models & APIs mentioned

- **Codex** (product)
- **Codex Cloud** V2 (product)
- **ChatGPT Space** (product)
- **ChatGPT Sites** (product)
- **Dots** (product)
- **Agents API** beta (api)
- **GPT-6.1 Sol** 6.1 (model)
- **GPT-6 Astra** 6 (model)
- **Luna** (model)
- **MCP** (protocol)
- **Annotations API** (api)
- **Tailscale** (product)
- **DaVinci Resolve** (product)
- **Figma plugin** (product)
- **Daybreak** Blue (other)

## How this applies to AX / design systems

Prototype a design-system plugin, or a Lit component catalog panel, that exposes components through @-mention autocomplete and an 'add to composer' action, so agents get token and component context directly. Use the annotations-API idea in your Storybook or developer-portal previews: mark only the Lit components as selectable targets for agent feedback. The ChatGPT Space pattern of per-page assistant instructions ('agents.md for pages') and Dots as a proactive safety net are useful AX references for approval UI and delegation surfaces in AI component libraries.

_Relevance 4/5: Several patterns (plugin extensions that surface a design system in the composer, the annotations API for marking which components are selectable, Appshots built on the accessibility tree, voice as a control plane, Dots as a proactive safety net) are concrete AX and design-system interaction patterns worth testing, though the talk is mostly a product feature tour._

## Best moments

- [10:49](https://www.youtube.com/watch?v=IPh9YsWvDQk&t=649s): Plugin extensions demo: a design-system browser injected into the composer
- [13:05](https://www.youtube.com/watch?v=IPh9YsWvDQk&t=785s): Appshots with the accessibility tree compared with plain screenshots
- [22:31](https://www.youtube.com/watch?v=IPh9YsWvDQk&t=1351s): Rapid UI iteration with Ultrafast via voice and queued prompts
- [27:22](https://www.youtube.com/watch?v=IPh9YsWvDQk&t=1642s): Annotations API for choosing which elements are selectable, e.g. design-system components vs the Storybook frame
- [49:13](https://www.youtube.com/watch?v=IPh9YsWvDQk&t=2953s): Dots as a proactive safety net and delegation sink
