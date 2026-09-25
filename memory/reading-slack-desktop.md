---
name: reading-slack-desktop
description: How to read Slack on this Windows PC (Chrome with the Bambora account); the Mac's desktop-app trick was not ported
metadata:
  type: reference
---

No Slack connector is set up. On Fatima's Mac, Claude drove the Slack desktop app with screenshots, AppleScript keystrokes and a small Swift clicker (Chrome was not signed in to Slack there). That trick is Mac-only and was **not ported**.

**On this PC:** the operator signs in to Slack in Chrome (app.slack.com) with the Bambora account herself. Then read it with the Claude in Chrome tools (get_page_text, find, read_page), like any other logged-in site. Rules that still apply:
- Never type a password or sign in for her.
- Never press Enter in a message composer (drafts may be sitting there), and never post, react or send in Slack unless the operator asks for that exact message.
- Liam (the media buyer) gets the Drive links for approved videos through Slack; the operator forwards them. Claude prepares the text (see [[routine-liam-batches-and-meta-access]]).

Related: [[claude-in-chrome-standing-permission]].
