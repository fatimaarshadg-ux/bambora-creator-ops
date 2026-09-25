---
name: trybe-5pct-replies-report
description: Read-only: read replies to Bambora's 5% commission DM on Trybe, classify them, and write a report with draft messages for Fatima to approve. Sends nothing and changes nothing.
---

You are working for Fatima (fatima@bamboraco.com), who runs the creator program for the brand Bambora on the Trybe platform. This run is unattended and STRICTLY READ-ONLY. Do not send any message, do not move any creator, do not click Accept, Reject, Approve, Send or Save anywhere, do not send any email, and do not change any setting. Your only outputs are a report file and your final summary. If something would require an action, write it in the report as a proposed action for Fatima to approve.

WRITING RULE for everything you write: never use em dashes, en dashes as connectors, double hyphens, or spaced hyphens. Use two sentences, a comma, a colon, or a connecting word instead.

## Before you start
1. Invoke the `trybe-portal` skill and read it. Also read these memory files in ~/.claude/projects/<PROJECT>/memory/: `bambora-protected-creators.md`, `trybe-verify-dm-recipient.md`, `trybe-api-key-storage.md`.
2. The Trybe API key is stored with Windows DPAPI; load it with `py -3 ~/claude-setup/work/common/trybe_key.py --print` only inside a command substitution, never echo it. API base https://api.jointrybe.com/v1, header `Authorization: Bearer <key>`. Use GET requests only. Never print the key. Back off on HTTP 429.
3. Use the Claude in Chrome browser tools for reading chat. Bambora's brand id is a8bedbc3-3b30-410d-a09e-2aa3aeb3a8e9 and every portal URL needs `?b=<that id>`. Reading page text works even when the tab is hidden. Opening a thread to read it is fine and wanted (it marks it read).
4. The working record is ~/claude-setup/work/trybe-5pct-migration/sendlist-2026-09-21.json: the 74 creators targeted with the 5% commission DM on 2026-09-21, each with `id`, `name`, `first`, `rate`, `program`, `status`. A status containing "moved to V3" means already done. Statuses starting "held" or "no DM thread" mean the DM was never sent. Ignore both groups.

## Background
On 2026-09-21 Fatima DMed these creators that Bambora is moving from 10% or 12% commission to a 5% GMV program (Bambora Affiliates V3), with a retainer planned for top performers and weekly inspo. The message starts "Hi <first>, wanted to check in and share a few changes" and ends "Let me know if this sounds good to you and I'll invite you to the new program". 13 creators who said yes were already moved that day.

## Step 1: collect and classify replies
Go to https://jointrybe.com/brand/chat?b=a8bedbc3-3b30-410d-a09e-2aa3aeb3a8e9. For every creator in the sendlist whose status starts with "sent" and does not contain "moved to V3", find their DM thread (search the full name; if nothing, the surname), open it, confirm the header reads "<Name> (DM)" and the thread contains the 5% message, then read everything the creator wrote after it. A list preview is not enough, open the thread.

Classify each into exactly one group: YES (unambiguous agreement to join; a yes with a question still counts, note the question), QUESTION (asks something without clearly agreeing), UPSET (unhappy, pushing back, declining), OPTING OUT (stepping away for their own reasons), NO REPLY. When unsure, do not classify as YES.

Known earlier states to re-check: Kia Layton, Danielle Corbin and Krystal Camacho asked retainer questions. Ali Fannin was disappointed. Vanessa Hargrove is stepping back but offered creators from her agency. Georgie Alex was chasing a pending post confirmation. katherine bodie was moved, then asked whether it is OK that she is pregnant with no baby to film with yet.

## Step 2: draft, do not send
For each YES creator, write a proposed personalized DM in Fatima's voice (warm, casual, stretched words like "reallyyy" and "Let's do thisss" are her style) based on this:

"Perfect, I've just added you to the new program! 🎉

Over the next few days I'll start sending you weekly inspo and a few angles that are working really well for us right now.

We've seen that creators who make 20-30 videos every month tend to hit at least three winners, and that can turn into a really nice commission. I will definitely help you get there.

If you ever want to confirm anything with me before filming, please do. Let's do thisss ❤️"

Personalize: open with their first name and react in one short line to what they actually wrote. Start the 20-30 sentence with "Like I said," ONLY if their thread already contains an earlier Bambora message mentioning 20-30 or "20 to 30" videos. If their yes came with a question about retainer amount, criteria or dates, add a line saying Fatima will get back to them on that. Never include retainer amounts, thresholds, dates, or any commission figure other than 5%.

## Step 3: write the report
Write ~/claude-setup/work/trybe-5pct-migration/report-<YYYY-MM-DD-HHMM>.md, formatted as an email to Fatima with the subject line "Trybe 5% move: <N> creators agreed", in this order:
1. One line: how many creators have agreed in total (13 moved earlier plus new YES replies), and how many new ones are waiting to be moved.
2. New YES creators: name, current program (confirm with `GET /v1/creators/{id}`), what they said, and the proposed DM for each.
3. Questions waiting for Fatima, retainer questions first.
4. Upset or opting out: creator and the gist. Note that their threads were opened (marked read) and nothing was sent, as she asked, because she has decided not to chase creators who are unhappy about the change.
5. No reply yet: a count and the names.
6. Anything you could not verify, stated plainly as "could not verify", never as "not there".

Do not run git and do not send the email. End with a short summary giving the report path and the headline numbers, and say that the moves and DMs are ready to run as soon as Fatima says go.