---
name: bambora-grandparents-program
description: Trybe "Bambora Grandparents Program" (5% V3 clone for grandparent creators), live and discoverable since 2026-09-24; brief and welcome text
metadata:
  type: project
---

Fatima asked on 2026-09-24 for a new Trybe program for grandparent creators, identical to Bambora Affiliates V3 except for grandparent-tailored copy. Created as **Bambora Grandparents Program** (5% of GMV, videos only, $100000 cap, weekly, Trybe attribution, Sling Carrier with samples).

- Brief: `~/claude-setup/work/bombara-folder/Bambora-Grandparent-Invite.pdf`, built by `build-grandparent-invite.py` from the V3 invite HTML (same design, grandparent cover, new "Ideas only a grandparent can film" page, inspos reordered granddad first).
- Welcome DM text: `~/claude-setup/work/trybe-grandparent-program/welcome-message.txt` (V3 onboarding text plus grandparent ideas and the 10 to 50 lb / one hand lines).
- Setup finished and verified 2026-09-24 (discoverable, inquiries, join approval on, sender Bambora Admin). Full settings in `~/claude-setup/work/trybe-grandparent-program/STATUS.md`.
- Trybe's program UI tip: the Customize panel's Manage click often fails on the first try; `scroll_to` the ref then click it again. Clicking a niche suggestion leaves the dropdown open, so the next click can add a stray niche; re-read the chips after.

**Why:** there were no grandparents on the roster (transcript search of all 353 submissions found none), so she wants to recruit them. Casting ideas for this role live in [[creator-casting-mindset]]. Safety rules as always: [[bambora-sling-safety-rules]].

**Invites (2026-09-24), Discovery invite with message "Hi {firstname}! Fatima from Bambora here 💙 We're looking for grandparents to film videos with our baby sling, and your content caught my eye. We just opened a program only for grandparents. Would love to have you!"** (first names only, her rule). Only creators with yapper content get invited (her rule): check Trybe portfolio, TikTok, IG with the trybe-applicant-review method first.
- Batch 1 (sent before the yapper rule): Heather Stanfield (borderline, her call), Chantelle Schaan, Jamie Main, Cynthia Pardue, Sheila Wright, Lisa Lirette, Joette Nagle, Christie Howard. Jamie, Sheila and Joette are not yappers: Fatima to cancel (the permission layer blocks Claude from "Cancel All"; there is no per-invite cancel, you tick the rows first).
- Batch 2 (yappers): Christina Garrison, Grandma Lisa, Martha Ruano, Sherry Hicks, Debbie Struck (accepted same day), Deanna Czarsty, Sandra Lynum, Grace Matney, Memaw Talks.

**Discovery invite mechanics when the tab is in the background** (keys and real clicks are dropped): set the search input with the native value setter plus an input event and a synthetic Enter keydown; click the card's Invite button with `.click()`; fill the textarea with the native setter plus input event; open the program select by focusing the combobox and dispatching a keydown ArrowDown, then focus the "Bambora Grandparents Program" option and dispatch keydown Enter; check name, message and program, then `.click()` Send Invite. The program select defaults to the 12% program every time. Some cards start with initials (e.g. "DC"), so match the name against the first 3 lines of the card.
