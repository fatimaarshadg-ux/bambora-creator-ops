---
name: trybe-portal-tab-clicks
description: "Trybe's Discovery and Creators tabs only respond to a real extension click, not a synthetic JS click, and often need a second click"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 69a3b3e5-e78c-4da3-971b-bbee6481f79a
  modified: 2026-09-28T15:03:31.987Z
---

The tab strips in the Trybe portal (Discovery / Inbox / Invited / Messages, and Roster / Samples / Programs) are Radix tabs, and they behave awkwardly through the Chrome extension. Learned the hard way on 2026-09-28, after a lot of wasted calls.

**What does not work:** a synthetic click from `javascript_tool` (`el.focus(); el.click()`). It sometimes flips `aria-selected` to true and then reverts on the next render, and the panel never loads. `allCards()` and `inboxNames()` then return an empty list, which reads as "no applicants" when the truth is "the tab never opened".

**What works:** `find` for the tab, then a real `computer` `left_click` on that ref, then wait 8 to 10 seconds before reading. **The first click often does nothing at all**; when the panel is still empty, re-run `find` (refs go stale after a re-render) and click again. Two clicks is normal, not a sign something is broken.

The one exception seen so far: the **Messages** tab did open from a synthetic `focus()` + `click()` + an Enter `KeyboardEvent`, after several real clicks had failed. Try the real click first and keep that as the fallback.

**Never conclude a tab is empty from one read.** Check `aria-selected` on the tab strip before believing a zero.

Related: skill `trybe-portal`, [[chrome-browser-to-use]], [[chrome-extension-browser-switch]].
