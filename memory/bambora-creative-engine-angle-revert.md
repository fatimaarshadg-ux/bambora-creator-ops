---
name: bambora-creative-engine-angle-revert
description: "RESOLVED - Bambora's Notion \"Monthly Concepts\" database was rebuilt with full names for Angle/Framework/Promo and a fresh SEP001 counter"
metadata: 
  node_type: memory
  type: project
  originSessionId: be9809c7-84b5-41b6-8176-aaeeb812fd1e
  modified: 2026-09-13T16:08:00.723Z
---

**Status: done (2026-09-13).** The Monthly Concepts database (Central Operating Hub → Systems → 🎨 Creative Engine → Monthly Concepts) was fully rebuilt as a brand-new Notion database/collection (url https://app.notion.com/p/8ba7e1c609374af382650b5d1532cb4c), data source `collection://10059968-9003-423e-bc1d-a9710ed0b388`. The old database (with the broken ID counter and short-code-only Angle) was trashed.

What changed:
- **Angle, Framework, and Promo** dropdowns now show full descriptive names (not short codes), which matches the user's explicit request ("angle names should not be in short" + later "I NEED FULL FORMS OF FRAMEWORK" + "SAME GOES FOR PROMO"). Each has its own hidden helper formula column ("Angle Code", "Framework Code", "Promo Code", all `ifs()`, described "Helper - do not edit") that derives the short code used only inside the Concept Code naming formula.
- **ID counter now truly starts at 1** (SEP001) since it's a genuinely new collection, not a recreated property on the old one.
- **Concept Code formula rewritten to be empty-safe**: each optional segment is wrapped as `if(length(x)==0, "", concat("_", x))` so blank fields no longer produce strings of stray underscores in the auto-generated page title (this was the "SEP008________" bug).
- Added **"Ready to Execute"** Status option, and three new views: Pending Strategist Review (Status = Awaiting Strategist Feedback), Editor To-Dos (Status = Sent to Video Editor), Media Buyer's Queue (Status IN Forwarded to Media Buyer / Ready to Execute), alongside Default view and Pipeline (by Status).
- Rebuilt the Notion Automation (Page added → Concept = `Trigger page.Concept Code`) on the new database and verified live: creating a page produced a clean title "SEP001" with no stray characters, and setting Angle = "Velcro Baby" correctly updated the code to "SEP001_VB".
- Removed the now-redundant Angle/Framework/Promo legend text blocks from the Creative Engine page (no longer needed since the dropdowns show full names directly).

No outstanding action needed on this. If the user ever asks to simplify Angle/Framework/Promo back to short-code-only dropdowns, that would just be reversing this same helper-column pattern (delete the "X Code" helper, point Concept Code straight at `prop("X")`, as was done earlier in this project's history).
