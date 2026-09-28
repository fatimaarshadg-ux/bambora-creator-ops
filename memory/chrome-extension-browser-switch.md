---
name: chrome-extension-browser-switch
description: "Claude in Chrome can silently switch to Fatima's Windows PC Chrome; symptoms and the fix (select the browser on THIS computer)"
metadata:
  type: reference
---

2026-09-26 ~09:05: mid-sweep the Claude tab group "vanished" and a new tab opened, the page froze, `fetch('http://127.0.0.1:8765/...')` failed and `document.visibilityState` was "hidden". Cause: the extension session had switched to **"Browser 2" (Windows, Fatima's PC)**, which she had open. AppleScript (`front.sh`) still saw the Mac's Chrome with the old tabs.

**Fix:** `list_connected_browsers`, then `select_browser` with the Mac one ("Browser 1", osPlatform macOS, onThisComputer true). The old tab group and tab ids come back.

**How to apply:** when tabs disappear, localhost helpers fail to load, or clicks never register, check `list_connected_browsers` FIRST before retrying anything. Never act in the PC browser from a Mac session. Related: [[claude-in-chrome-standing-permission]], [[core-rules]].

**On the Windows PC (handover):** it is the mirror case. Fatima's Mac Chrome is on the same Claude account, so pick the connected browser with osPlatform Windows and onThisComputer true, and never act in her Mac's Chrome.
