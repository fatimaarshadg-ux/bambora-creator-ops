---
name: chrome-browser-to-use
description: "Two Chrome browsers are connected on this PC; only the fatima@bamboraco.com one may be used, never the goraya one"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 69a3b3e5-e78c-4da3-971b-bbee6481f79a
  modified: 2026-09-28T13:26:30.097Z
---

Two Chrome browsers report as connected from this Windows PC, both showing `osPlatform: Windows` in `list_connected_browsers`, so the platform field cannot tell them apart. As of 2026-09-28 they are:

- **Browser 1, deviceId `f3752968-6139-4a07-be31-2433abe37b28`: signed in as fatima@bamboraco.com. This is the one to use.**
- Browser 2, deviceId `6da785c6-d2b0-4b33-a09d-0a67c1799fea`: the goraya account. **Never select it, never read from it, never fetch data from it.** Ikra's instruction, 2026-09-28.

**Why:** the second browser is a personal account that has nothing to do with Bambora. Acting in it, or pulling anything out of it, would be reading someone's private browsing and could send a creator message from the wrong identity.

**How to apply:** at the first browser step of a session, call `list_connected_browsers`, then `select_browser` with the fatima deviceId. Device ids can change when Chrome reconnects, so confirm rather than trusting the id: open `https://myaccount.google.com/` and read the account email off the page before doing any Bambora work. If it is not fatima@bamboraco.com, switch and check again.

**Tabs disappearing mid-task** ("No tab with id") means the extension reconnected and the tab ids are stale, not that anything was lost. Re-list the browsers, confirm the fatima one is `inUse`, then navigate again. Seen on 2026-09-28 in the middle of the Discovery Inbox paging. See [[chrome-extension-browser-switch]].

Related: [[claude-in-chrome-standing-permission]], [[windows-machine]].
