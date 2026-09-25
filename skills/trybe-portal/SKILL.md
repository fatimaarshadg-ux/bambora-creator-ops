---
name: trybe-portal
description: Map of Bambora's Trybe brand portal and Brand API. Use this skill for any Trybe task before opening the browser, including approving or rejecting submissions, sample requests and creator join requests, messaging creators, checking a creator's history or earnings, and looking up program commission rates. Also use it when the user names a creator and an action without saying where it lives. Read it first rather than hunting through the portal.
---

# Trybe portal and API

Fatima's brand is **Bambora**, brand id `a8bedbc3-3b30-410d-a09e-2aa3aeb3a8e9`. Every portal URL takes it as `?b=<brand-id>`. Without it the page may 404 or land on the wrong brand.

Base portal: `https://jointrybe.com/brand`
Base API: `https://api.jointrybe.com/v1` (bearer token, see [[trybe-api-key-storage]] in memory for how to load the key)

## Operating rules

These three exist because breaking each one cost real time or caused a real error on 2026-09-20. They are not style preferences.

**1. API first. Browser only for what the API cannot do.**

The API covers submissions, creators, programs, earnings and all three review actions. It answers in seconds and never freezes. The browser is required only for sample requests, creator join requests, and chat. Every slow or fragile stretch of that first session was browser work that the API could have done instantly.

**2. Never click by pixel coordinate in this portal.**

Screenshot dimensions and the reported coordinate frame drift apart here, and the window size changes underneath you. The same tab was targeted three different ways and missed every time, which is also how a click landed on Submissions and how a profile modal opened instead of a chat thread.

Locate the element and click its reference instead. Where a reference click also fails, because the page is mid-freeze, fall back to focusing the element through the DOM and sending a real keypress:

```js
// javascript_tool: focus it
const t = [...document.querySelectorAll('[role="tab"]')].find(e => /inbox/i.test(e.textContent||''));
t.focus();
```

Then `computer` with `action: "key", text: "Return"`. A synthetic `.click()` will not work; the React handler wants a trusted event on a focused element.

**3. Re-locate and verify immediately before any send or approve. Never identify by name alone.**

Element references go stale fast. The chat conversation list re-sorts the moment a message sends, so a reference captured seconds earlier can point at a different row by the time it is clicked. This is exactly how an approval DM went to the wrong one of two identically named Jenasa Prudhomme accounts.

So: re-find the target, then confirm identity from its content before typing a character. For a chat thread that means reading the conversation history, since duplicate accounts share a display name. For a submission or a creator it means checking the full id. Verify before, not after. One extra call prevents a message that cannot be unsent.

**4. A check that failed is not a negative result.**

If a click timed out, a page froze, or a read returned something other than what you asked for, the check did not happen. Report "I could not verify this" rather than "it is not there." Absence of evidence from a broken check is not evidence of absence.

The specific trap: a conversation **list** shows one preview line per thread, which is only the most recent message. It tells you nothing about a thread's history. On 2026-09-20 a click to open Laura Daniels' thread silently failed, the list was read instead, and her introduction was reported as non-existent because the auto welcome that approval had just fired was sitting on top of it. Two separate facts were stated as verified when nothing had been opened at all.

So: before concluding a thread contains nothing, confirm the thread actually opened, by reading its header name and its history. If it did not open, say so.

## Creator messages live in two places

Applicants can attach a message, often a video pitch with a caption, to their join request. Where that message lives depends on their status:

- **Before approval**: Discovery, **Messages** tab. It has its own "Search messages..." box, which is the fastest way to find one person. Only the 50 most recent are listed and there is no pagination.
- **After approval**: it moves into their **DM thread** in `/brand/chat`.

This is the single most important ordering rule in this skill: **read the applicant's message before approving, not after.** Approval moves the message out of the Messages tab, and Fatima's templated welcome goes out to the new creator within a minute or two, pushing their introduction below an outbound message in the chat list preview. Very quickly after approving, the evidence is harder to find in both places at once.

Because that welcome goes out on its own, a new creator already has a reply. Do not offer to draft one without checking the thread first.

These messages are worth reading. They carry the credentials and context that decide whether someone is a good fit. One applicant introduced herself as a pediatric physical therapist who evaluates baby wearing and infant positioning professionally, which for a sling carrier brand is about as strong a signal as exists, and it was invisible from her roster card.

## Pre-flight checklists

Work through these before the irreversible click. Each line exists because skipping it caused a real error.

**Approving a creator join request**
1. Discovery, Messages tab, search their name, read their message in full.
2. Check the card for which program and rate they applied to. Applicants land in different programs.
3. Judge them against her criteria in [[bambora-creator-acceptance-criteria]]: English speaker in an English-speaking country, then yapper-style content (check Trybe card featured videos, their TikTok and IG, and any video in their application message) OR 10K+ TikTok likes/followers or 10K+ IG followers (no yapper = DM to ask, not accept). GMV is ignored.
4. Report what the message says and your verdict with the reason to Fatima, then approve.
5. Never touch Accept All or Reject All unless she asks in those words.

**Approving or rejecting a submission**
1. Confirm the full `submission_<uuid>` and the creator name on it. `trybe_id` alone is not enough, and creator names collide.
2. If the request named a creator and an id, check they match. On 2026-09-20 an id belonged to Jacob Hatch while the message named Jason Lindley, who had no submissions at all.
3. Run the content checklist if visual review is expected.

**Approving a sample request**
1. Expand the row and read product, variant, quantity, shipping address, and the creator note.
2. If the count Fatima named does not match what is pending, show her the list and ask.

**Sending a DM**
1. Re-find the conversation immediately before clicking, never reuse an earlier reference.
2. Open it, read the header name and the history, and confirm identity from content. Duplicate accounts share display names.
3. Only then type.

## Reaching for the right tool

Use the browser only for actions the API does not expose, which currently means sample requests, join requests, and chat.

## Where everything lives

| Task | Location |
|---|---|
| Review, approve, reject a submission | `/brand/submissions`, or the API |
| Sample requests | `/brand/creators` then **Samples** tab then **Pending** filter |
| Creator join requests (applications) | `/brand/discovery` then **Inbox** tab |
| DM a creator | `/brand/chat` |
| Creator roster, stats, per-creator history | `/brand/creators` then **Roster** tab |
| Program list and commission rates | `/brand/creators` then **Programs** tab |
| Creators you invited | `/brand/discovery` then **Invited** tab |
| Sales, GMV, ad performance | `/brand/analytics` |
| Shopify, Meta connections | `/brand/integrations` |

Left nav badges are a quick health check: Submissions, Chat, Creators (pending samples) and Discovery each show a pending count.

## Programs and their rates

Bambora runs several programs at once, and a creator's rate depends on which one they are in. Confirm the rate before saying anything to a creator about money.

| Program | Rate |
|---|---|
| Bambora Affiliates V3 | 5% of GMV, videos only |
| The Bambora Affiliate Program! | 12% of GMV, videos only |
| Ambassador Program! | 10% commission |
| Bambora Affiliates v1 | legacy, still has members |

"The 5% program" means **Bambora Affiliates V3**, id `creator_program_f7523ebb-8206-4da5-9997-4464f77aec58`.

## API endpoints and their traps

- `GET /v1/creators` lists active creators, cursor paginated. `GET /v1/creators/{id}` adds `programs[]` with enrollment status and commission text, plus `avatar_url` (null means the UI shows initials rather than a photo).
- `GET /v1/submissions` filters on `status`, `creator_id`, `group_id`, `angle`, `program_id`, `product_id`, `transcript_language`, `query`, `limit`.
- `POST /v1/submissions/{id}/approve` `|reject` `|request-revision`. Real side effects: approve releases earnings, all three notify the creator. `request-revision` needs a non-empty `comment`.

Traps worth remembering, each one cost time before:

- The filter is `program_id`, not `program`. The forward cursor is `after`, not `cursor`. Wrong names return `400 validation_error: Unknown parameter(s)`.
- The approve endpoint needs an explicit empty JSON body (`-Body "{}"` with `-ContentType application/json`) or it returns `400 Malformed JSON in request body`.
- `program_id` filters by the program a submission was **pinned to at upload**, which is often not the creator's current enrollment. Bambora migrated people between programs, so most submissions are pinned to an older program than the one their creator sits in now. To answer "all submissions from people in program X", enumerate creators, check each `programs[]`, then query by `creator_id`. Filtering submissions by `program_id` will badly undercount.
- Submission ids are not reconstructible from the 8 character `trybe_id`. The `trybe_id` is the last 8 characters of the uuid, but the rest is not derivable. Always carry the full `submission_<uuid>`.
- **The API returns 403 for Python's default `Python-urllib` User-Agent** (curl works). Scripts must send a normal User-Agent header, e.g. `curl/8.7.1`. Auth is `Authorization: Bearer <key>`; `X-API-Key` returns 401.
- `asset.url` is presigned and expires about 20 minutes out. Re-fetch the submission for a fresh one rather than reusing a saved link.

## The Discovery page freezes

`/brand/discovery` renders a grid over 222,000+ creators and regularly locks the renderer. Screenshots, clicks and script injection all time out, and waiting does not reliably clear it.

The workaround that works: focus the tab element through the DOM, then send a real keypress.

```js
// javascript_tool
const t = [...document.querySelectorAll('[role="tab"]')].find(e => /inbox/i.test(e.textContent||''));
t.focus();
```

Then `computer` with `action: "key", text: "Return"`. A synthetic `.click()` does not switch the tab and neither do coordinate clicks; the React handler wants a trusted event on a focused element.

There is no direct route to the inner tabs. `/brand/discovery/inbox` and `?tab=inbox` both fail, the first with a 404 and the second by silently staying on Discovery.

Once Inbox is open, use its **Search creators and niches** box to filter to one name rather than paging. It holds hundreds of requests across dozens of pages. Each card carries the creator's location, age, 30d GMV, submission count, approval rate, niches, and crucially **which program they applied to and at what rate**. Check that before approving; applicants land in different programs.

Beware the **Accept All** and **Reject All** buttons sitting next to the per-card ones. Never use them without Fatima asking in those words.

## Bulk actions in the Discovery Inbox

The **Select All** button does not respond to automated clicks. It has failed across separate sessions, so do not spend time on it. Per-card **Reject** and **Approve** buttons work fine, both by element reference and by a scripted `.click()`.

The reliable pattern for a large, filtered bulk action is a guarded loop that always acts on the **first** card, re-reading the DOM each time. Sort Oldest first so the category you want to keep clusters at the far end, then let the loop stop itself when it reaches one:

```js
function firstCard() {
  const b = [...document.querySelectorAll('button')].find(x => /^\s*Reject\s*$/i.test(x.textContent||''));
  if (!b) return null;
  let el = b;
  for (let i=0;i<8&&el;i++){ el = el.parentElement; if (el && /commission/i.test(el.innerText)) break; }
  const txt = el ? el.innerText : '';
  return { btn: b, name: txt.split('\n')[0].trim(), keep: /Affiliates V3|5% commission/i.test(txt) };
}
let n=0, stopped=null;
for (let i=0;i<40;i++) {
  const c = firstCard();
  if (!c) { stopped='no cards left'; break; }
  if (c.keep) { stopped='hit protected: '+c.name; break; }
  c.btn.click(); n++;
  await new Promise(r=>setTimeout(r,750));
}
({rejected:n, stopped});
```

Two constraints learned the hard way:

- **Keep each batch under 45 seconds**, which is the CDP script timeout. 40 iterations at 750ms is about 30s and safe. At 70 iterations the call times out, though the loop keeps running in the page, so the count still moves and you must re-read state rather than assume nothing happened.
- **The guard is the safety mechanism, not the plan.** Checking the card's own text immediately before clicking it is what makes this safe, because it cannot act on a record it has not just read. Never write this loop without it.

## When clicks silently do nothing: check tab visibility FIRST

If a ref click, a coordinate click and focus plus Return all fail on a plain button, run this before trying anything else:

```js
({vis: document.visibilityState, focus: document.hasFocus()})
```

`vis: "hidden"` means the Claude tab is in the background because Fatima is using another Chrome tab or window. While hidden, Chrome delivers mouse movement but drops every mouse press and key press, so nothing can be clicked or typed. JS reads still work, which makes it look like a page bug. On 2026-09-21 this cost about 25 tool calls on the Programs "Manage" button before it was diagnosed. Fix it yourself, do not ask: new tabs from the extension also open hidden. On Windows run `powershell -NoProfile -ExecutionPolicy Bypass -File "$USERPROFILE/claude-setup/work/trybe-chat/front.ps1" cl=1`, which brings Chrome to the front and switches to the tab whose page title or URL marker matches (details in the script header). Add a harmless marker to your tab's URL (`&cl=1`); matching on the marker matters because the operator often has her own Trybe tabs open with near-identical URLs. Re-check `visibilityState` before each irreversible click, since she may switch tabs again mid-run, and simply re-run the script when it flips back to hidden. To prove the diagnosis, add capture listeners for `mousedown`, `click` and `keydown` on `window`, act, and read them back: an empty list with a `mousemove` present is this problem.

Related: this Chrome profile runs at 80% zoom (`devicePixelRatio` 1.6, layout viewport 1875 wide against a 1568 screenshot frame). To click by coordinate, divide page CSS coordinates by 1.195 (1875/1568). Ref clicks handle this themselves.

## Moving a creator to another program

Creators, Programs tab, **Manage** on the creator's current program, search the creator, three dots on the row, **Move to Program**, pick the target, **Move Creator**. The dialog states "X will be moved from A to B. Past earnings are not affected." A toast confirms and the source program count drops by one.

It is a two-step move. The creator then appears at the top of the Programs tab under **Creators needing attention** as "Pending in <target>", with **Accept** and **Reject**. Until Accept is clicked the API shows the creator with no programs at all. Click Accept, then verify with `GET /v1/creators/{id}` that `programs[]` shows the target as `active`.

Welcome messages: each program's automated welcome DM lives at Manage, **Customize**, **Chats**, "Welcome message". There is no on/off switch. Clearing the field and pressing the visible Save (next to Discard; the dialog also contains a hidden, always-disabled Save that scripts find first) is accepted, and the section then reads "Not set". Fatima had the **V3 welcome removed on 2026-09-21** because she now sends personalized manual messages to everyone who joins or is moved; the old text is backed up at `~/claude-setup/work/trybe-5pct-migration/v3-welcome-message-backup.txt`. Do not restore it unless she asks. **WARNING, learned the hard way on 2026-09-22: an empty welcome field does NOT mean silence.** Trybe falls back to its own generic system message ("Welcome to our creator program! You can use this chat to communicate with the Bambora team any time you have questions!"), sent from Bambora Admin the moment a creator is accepted. It is a system message with no Edit or Delete option. Six moved creators got it and Fatima was furious. So the welcome field must always hold text she approves. UPDATE, later on 2026-09-22: Fatima had the ORIGINAL onboarding welcome restored from the backup because she is accepting new applicants again. So the V3 welcome currently says "Heyy! Fatima here from Bambora... order your sample through Trybe now" with the checklist and inspo links. That text is wrong for a migrated creator, so BEFORE moving any existing creator into V3, tell her and ask whether to swap in the migration line first (swap, move, swap back). The Save in this form can silently fail on the first click: wait for the "Chat settings saved" toast and "All changes saved", and click Save again if it still shows "1 unsaved section". Earlier that day the V3 welcome was her own migration line: "Just invited you to the new program, I will keep sending you weekly inspo here to set you up to succeed. Lets do this!!! 💙" (her wording, keep it verbatim). It fires automatically on every Accept into V3, so do NOT also DM that line by hand after a move. It reads as a message for migrated creators; brand new applicants accepted into V3 get it too, so if she wants the old onboarding text with the checklist and inspo links for them, it is in the backup file. Saving this form takes up to 10 seconds to show "All changes saved". Until she has set one, tell her this BEFORE moving or accepting anyone into V3. And whenever a program setting changes, move ONE creator, open their thread, read what actually arrived, and only then continue. The other three programs still have theirs. In that textarea plain Enter is a newline, so multi-paragraph text can be typed directly, and cmd+z restores a cleared field.

Unattended scheduled tasks that send DMs, move creators or send email are refused by the permission layer. Schedule read-only runs that classify replies and write a report with proposed messages, then do the actions live when Fatima says go.

Before that removal, the side effect was: accepting a creator into V3 fired the program's automated welcome DM ("Heyy! Fatima here from Bambora... order your sample through Trybe now"), even for creators who have been with Bambora for months. Several creators can be moved in one visit to the program page and then accepted together from the pending list; re-find the Accept buttons after each click because the list re-renders. If a full-name search on the program page returns no rows, search the surname alone (it failed for "katherine bodie" and worked for "bodie"). 11 creators were moved this way on 2026-09-21, all confirmed by API.

The program page URL is `...&tab=programs&programId=<program uuid>`, but loading that URL directly shows the program list, not the detail page. The detail page only opens from the Manage click. Program ids: V3 `f7523ebb-8206-4da5-9997-4464f77aec58`, 12% program `61bd031b-c09e-4ede-acaa-37157ab52be2`, Ambassador `735c3c87-5b63-499c-9fb2-83a40d3f414f`, v1 `ccfda98c-c69f-48e3-8c06-f5659853264a`.

## Mass DMs through chat (71 sent in about 35 minutes, zero errors, 2026-09-21)

There is no chat API, and the Announcements feature sends to a whole program with no way to exclude people. For a personalised DM to a filtered list, build the list from the API first (creators, `programs[]`, submissions by `creator_id`), then run this guarded routine in the chat page. Roughly 30 seconds per creator, six creators per `browser_batch`.

Facts that make it work:
- Sidebar conversation items are `div[role="button"]` inside `main`, not `<button>`. The name sits in a `span` as `Name (DM)`. Search results take up to 4 seconds to render.
- The open thread's text starts at the last `Back\n` in `main.innerText`; the next line is the header `Name (DM)`.
- The composer is a textarea (`[placeholder="Type a message..."]`). Setting its value with the native setter plus an `input` event is accepted by React, so a multi-paragraph message goes in with one call and no shift+Enter typing.
- Opening a thread and pressing Send both need a trusted event: `.focus()` the element from JS, then send a real `Return` keypress.

Per creator: click the search box ref, type the full name, wait 4s, then `pick` (focus the item only if exactly one span equals `Name (DM)`), Return, wait 3s, `fill` (only if header matches, the thread contains no `5%`-style duplicate marker, and the composer is empty), `arm` (only if header still matches and composer value equals the expected text exactly, then focus Send), Return, wait 3s, `verify` (message appears exactly once, composer empty). Every guard that fails moves focus to the search box, so the following Return is harmless. Install the four helpers on `window` once; a page reload wipes them, which makes later calls throw and stops the batch safely.

Expect these leftovers: duplicate display names (pick sees 2 matches, so open the right one by its preview and history, then set the picked flag by hand), creators with no DM thread at all (search returns nothing), and threads whose last message is an unanswered request from the creator (hold those and ask Fatima rather than landing a broadcast on top of it).

## Chat gotchas learned 2026-09-22

- **Trybe chat HTML-escapes `<`.** A message containing `<3` is stored and shown to the creator as `&lt;3`. Use emoji hearts instead. A sent message can be repaired: hover it, **Edit message**, set the `Edit message...` textarea, click **Save changes**. The edit shows in the thread with no "edited" mark.
- **Narrow windows open the thread as a slide-over panel** with a second `Type a message...` textarea and its own Send button. The page-level composer underneath still exists and comes first in the DOM, so `querySelector` fills the wrong one. Fill the visible textarea (the one whose bounding rect sits at the bottom of the panel) and click its own **Send message** button by ref; a focus + Return on the hidden one does nothing. Screenshot once before sending to see which layout you are in.
- The sidebar name span carries a double space: `Jennifer Thomas  (DM)`. Match with a regex or `find`, not exact string equality.

## Other portal quirks

- Clicking the avatar in a chat thread header opens the creator profile modal rather than switching threads. Escape closes it. The modal is worth knowing for its own sake: it shows submission history, sample history and earnings together in one view.
- Chat search matches conversation names, not message text. There is no way to search message contents from the UI.
- Discovery, Messages lists only the 50 most recent applicant notes, with no pagination. Approving a request appears to drop its note off that list, so read the note before approving if it matters.
- See [[trybe-verify-dm-recipient]] in memory for the duplicate-account case behind rule 3.

## Before any consequential action

Approving a submission releases money. Approving a sample ships physical product. Approving a join request adds someone to a paying program. All three notify a real person and none are cleanly reversible.

Confirm the target by id and owner before acting, and say what you are about to do. When the count Fatima names does not match what is actually pending, show her the list and ask rather than guessing. Related: [[trybe-sample-request-workflow]], [[bambora-trybe-submission-review]], [[bambora-content-checklist]].

## Reading every DM thread (learned 2026-09-23)
- Reading all 94 creator threads through the normal chat screen took about 50 minutes with one agent (search by name, open, capture from the last `Back\n`, open the header avatar for the profile modal's sample history, Escape). Opening threads can clear their unread state; say so in the report.
- The portal's own chat backend (`/backend/api/channels`, `/backend/api/channels/<id>/messages`) answers only with her session token. Calling it and exporting the result was refused by the safety check twice, even after she approved. Use the chat screen instead.
- `/v1/creators` (Brand API) does not list every creator. Look up known ids directly (`/v1/creators/<id>` includes `programs[]` with status and enrolled date). `/v1/creator-performance` answers to `start_date=2026-06-01` but not 2025 dates.

## Learned 2026-09-23 (evening sweep)
- **Trybe MCP review tools drop the note.** `trybe_reject_submission` sent the reason under the wrong field, so the rejection went through with `review_comment: null`, and `trybe_request_revision` failed with `comment: Required`. Until the MCP is fixed, call the API directly: `POST /v1/submissions/<id>/request-revision` (or `/reject`) with body `{"comment": "..."}`, a curl User-Agent and the DPAPI-stored key, then confirm `review_comment` in the response. If a rejection went out without a note, explain it in the creator's DM.
- **Slide-over chat layout:** when the window is narrow, the conversation list and thread open in a `[role=dialog]` sheet with its own "Search Chat" box, rows, Back button and composer. Scope every selector to that dialog, since the page-level copies underneath are hidden. Focusing a row (or Back, Send, "Add reaction", or the emoji result) and sending a real Return works for all of them.
- **Reactions by keyboard:** focus the last "Add reaction" button in the thread (that's the creator's newest message when it's theirs), press Return, focus `input[placeholder^="Search emoji"]` (the placeholder ends in a Unicode ellipsis, so `"Search emoji..."` misses it), type "blue heart", focus the 💙 button, press Return. Check that "💙 1" shows under their message.
- **Creators without a photo:** the thread header begins with their initials ("CD") on the line above "Name (DM)". Match the first line ending in "(DM)", not line 0.
- **Samples tab in a narrow window** sits in the "Roster" dropdown (pick "Samples (N)"). "Toggle details" opens one row at a time. The row's "Approve N item(s)" button works with a scripted `.click()`. Status filter buttons also take a scripted click when the tab is hidden. Pending clears at once, and the "Samples (N)" count isn't a reliable check, so verify by reading the Pending filter.
- **Chrome in the background** (the operator on another app) makes `visibilityState` hidden even when our tab is active. `front.ps1` (work/trybe-chat) brings Chrome forward and fixes it.
- **Re-read right before sending (2026-09-23, Aubri Tranel).** She wrote "expecting my first born any day" at 7:46pm. Her thread had been read a few minutes earlier, so her sample message went out at 7:50 without mentioning it. The composer guard checks only the header and the composer, not new incoming messages. Before arming Send, compare the thread's last creator message with the one captured when drafting. If anything new arrived, stop, read it and redraft. Big life moments (pregnancy, birth, a new baby, illness, loss) are always acknowledged, even in a template message; that isn't parroting.
- **Replacing a program brief (2026-09-23).** Programs, program Manage, Customize, "Brief & angles". Setting the hidden file input with `file_upload` stages nothing useful, because no Save appears. What worked on the Mac: focus "New brief" from JS, send a REAL Return from the OS, then type the path in the native picker. On Windows: focus "New brief" from JS, run `front.ps1` then `work/trybe-drive-filing/sendkeys.ps1 -Keys "{ENTER}"`, then in the Windows file dialog type the full file path in the File name box and press Enter (sendkeys.ps1 -Text "<path>" -Keys "{ENTER}"). A "Replace brief" row appears with Save; click it and wait for the "Brief saved" toast (PUT .../briefs/replace, 200). Stage the file alone in its own folder first.
- **Thread replies:** a creator's message with "N replies" opens a Thread sheet with its own "Reply to thread..." textarea and Send button. Fill that textarea and use the Send inside the same dialog. The reply count can lag after a delete, so read the thread itself to verify.
- **Where creators accept partnership ads (Fatima, 2026-09-24):** the request shows up in the creator's Instagram, and they accept it there. If a creator asks "on Instagram?", the answer is yes.
- **Partnership ads need a PUBLIC Instagram (2026-09-24, Jena Swapp):** Trybe won't link a private Instagram account, so a private creator shows "--" and can't be requested. TikTok linking alone doesn't enable it. Answer (Fatima): it needs a public Instagram, maybe make a new public one; a Facebook account works too; TikTok doesn't work with Trybe for this.
- **Chat names with a trailing space** ("Samantha bumstead  (DM)"): always compare whitespace-normalised; use open2() in chat-helpers.js.

- **Applicant follow-ups are sent from Discovery:** Inbox search, click the name to open the Creator profile, then click `button[aria-label="Open chat"]` (icon-only, no text). The chat box placeholder is "Message <first name>...". Follow up only 24h+ after our last message; check the thread time first.

## Sample tracking numbers are NOT in Trybe (learned 2026-09-24)
Every approved sample request (218 checked, July to September) shows `shippingStatus: PENDING` with no `trackingNumber`, carrier or `shippedAt`, even months later. Trybe only creates the Shopify order (`shopifyOrderNumber`, e.g. #187115). So when a creator asks for tracking, read the order number from the Samples tab (React fiber `request` object) and bring it to Fatima; the tracking lives in Shopify. Never tell a creator "it hasn't shipped" from Trybe's status.

## Wrong-program applicants (Grandparents Program mix-up, learned 2026-09-24)
Moms keep applying to the **Bambora Grandparents Program** by mistake (Dounia Nasrallah, Cassie Kay, Kristin Crane, Kaitlin Duncan on 9/24). Accepting one fires the Grandparents welcome ("so happy to have a grandparent with us... your grandkids") and then, after Move to Program + Accept into V3, the V3 welcome fires too: two automated messages, the first one wrong. System messages can't be deleted. What was done for Cassie Kay: accept, move to V3, accept the move, then a short personal note ("ignore that first message about grandparents haha, you'd applied to that program by accident so I moved you over to the right one 💗"), then partnership ads request + tiny note. To avoid the wrong welcome, ask Fatima whether to temporarily blank/swap the Grandparents welcome text before accepting a batch of moms (remember the empty-field fallback warning above: an empty welcome sends Trybe's generic message, so swap in approved text instead of clearing).
