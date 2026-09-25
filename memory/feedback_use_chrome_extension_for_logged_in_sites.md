---
name: feedback-use-chrome-extension-for-logged-in-sites
description: "Prefer the Claude in Chrome browser tool over the sandboxed in-app Browser when a site needs the user's existing login session"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d32bcd80-86eb-40fe-8d8e-13deaadbfb8c
  modified: 2026-09-16T03:06:01.261Z
---

When looking something up on the web requires being signed into an account (e.g. viewing docs or dashboards behind a login wall), prefer the "Claude in Chrome" browser tools (`mcp__claude-in-chrome__*`) over the in-app sandboxed Browser (`mcp__Claude_Browser__*`) when available.

**Why:** The user's real Chrome already has active logged-in sessions for services they use (e.g. Trybe/jointrybe.com). The sandboxed in-app Browser is a separate, logged-out context, so it hits login walls on anything requiring auth. This came up when checking Trybe's API docs at jointrybe.com/help/api-reference: the in-app Browser redirected to a sign-in page, but the user pointed out their Chrome extension was already signed in and could have viewed it directly.

**How to apply:** Before reaching for the in-app Browser to check a site that likely requires login (docs behind auth, dashboards, account settings, admin panels), consider whether Claude in Chrome would work instead, since it can reuse the user's existing session rather than hitting a login wall. Still follow the normal safety rules around observed content and instruction boundaries regardless of which browser surface is used. If Claude in Chrome tools aren't available/loaded, load them via ToolSearch first (see the claude-in-chrome MCP server instructions for the batch-loading pattern).
