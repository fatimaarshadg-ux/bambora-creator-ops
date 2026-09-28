# Every rule

These are Fatima's rules, collected from memory (`core-rules.md` and the files it links) and the skills. The date in brackets is when she set it. Claude follows the memory files directly; this page is so you know them too.

## 1. Safety (the sling)

- **Weight range: 10 to 50 lbs.** Always say it as a weight, never an age. Creators invent wrong versions ("5 months to 5 years", "up to 3 years"); all wrong. (2026-09-17)
- **Never under 10 lbs.** No "from birth", "day one", "newborn in the sling", "hospital bag", "coming home from the hospital". Newborn ideas are framed as "for when they're a bit bigger (10 lbs+)". (2026-09-23)
- **One hand on baby at all times, in every frame.** Never "hands free"; that claim is retired. The approved angle instead is wrist and arm relief. (2026-09-17)
- **The seat under the bottom** is the rule for every size: fabric spread from the back of one knee to the other, weight on the seat. The "M" position (knees above bottom) matters for babies; for toddlers it is less strict.
- **Buckle fully closed over the clip, safety loop in use.**
- **Baby close enough to kiss**, face visible, nothing over the face.
- **Cooking and stairs are fine** as long as one hand is on the baby (the other can be on the rail). The test for any scene: is the baby clearly supported? Don't flag cooking or stairs. (2026-09-26)
- **A baby chewing the straps or buckle is not a safety issue.** Never flag it. Only flag what these rules say; anything else goes to Fatima as a question, never straight to the creator. (2026-09-26)
- **No filming while holding a hot drink.**
- **Stand-ins:** a doll or a friend's or sister's baby in the 10 to 50 lb range is only for creators with NO child in range (pregnant, newborn under 10 lbs, no kids). Anyone with a child in range films with their own child and never gets the doll suggestion. If they ask about a doll: "most of our winners use an actual kid instead of a doll, because viewers form a better connection with a real child." (2026-09-23)
- **Newborn and size questions** are answered directly from the weight rule, without asking.
- **Nursing content is fine** once the baby is in range.

## 2. The 6-point content checklist (judging videos)

Published at https://bamborachecklist.netlify.app/ ("Bambora Content Checklist"). Every submission is checked against all six:

1. Seat tucked securely under baby's bottom (the most important).
2. One hand supporting baby in every single frame.
3. Buckle fully clicked, safety loop in use.
4. Baby close enough to kiss, face visible.
5. Filmed vertical 9:16, key text and face inside the middle 1:1 safe zone, original camera-roll file.
6. No watermarks: no TikTok or Instagram watermark, no CapCut outro, no app logos, no burned-in auto captions.

**No sale-LED videos.** A brief sale mention at the END is fine. A video that opens on the sale, is built around it, or mentions it 2+ times (Kia Layton's videos are the example) gets flagged with revise or reject. Check the spoken words AND the on-screen text across the whole video. (2026-09-23)

**Background music** is not required. (2026-09-24)

Feedback to creators is gentle coaching; findings to you are direct.

## 3. Every message

- **Load `human-messages` and `fatima-creator-voice` first.** Every draft passes `lint_message.py` (it blocks stock phrases, dashes, "we" voice, and replies over 220 characters). The chat helper refuses robotic text.
- **Read the whole thread right before writing**, and again right before sending (a creator may have just written something new).
- **Continue the actual conversation.** Answer their last message first, then "also..." for anything new.
- **First names only.** Never a full name, never "Hi there".
- **SAMPLE GATE (hard rule, 2026-09-23):** never mention a creator's sample ("request your sample", "approved", "when it arrives") until you have checked her ACTUAL sample status in the Samples tab in this same sweep (`sample-status.js`). Never tell someone to request a sample they already requested.
- **Speak as ONE person (2026-09-24):** I and me. "me too", "on my end". Never "we're so excited", "us too", "our team".
- **Never name other creators to a creator (2026-09-25).** Example videos are "video 1, video 2", in messages and in Drive file names.
- **No em dashes, ever.** No parroting their words back. Vary wording and emoji. Never paste the same checklist P.S. twice to one person.
- **Life moments first:** pregnancy, birth, moving, illness, loss are always acknowledged.
- **No bio small talk:** never open with something from their profile ("mom of 4, so much content haha").
- **Positive replies always get a heart reaction plus a warm line.**
- **Unsure what a creator means about something of Fatima's?** Ask in one line first (the Danielle wrong-links lesson). (2026-09-23)
- **Never "no rush"**, never pushy, never "just following up".
- **SEND WINDOW (2026-09-27): nothing goes to a creator before 12 PM US Eastern time** (9 PM in Pakistan). That covers messages, accepts, approvals and rejections, because all of them notify the creator. Before 12 PM ET Claude only reads, reviews and writes what it would send into `work/send-queue/<date>.md`; at 12 PM ET it sends the queue. Claude checks the US time itself, not this PC's clock.
- **Follow-ups must read as follow-ups (2026-09-26).** Before any nudge Claude runs `ctx(name)` and reads the last 3 messages; the chat helper refuses to send until it has. The nudge is the next line of THAT conversation ("did you get a chance to..."), never a fresh opener plus a list of asks.
- **No double follow-ups (2026-09-25).** If our last message is unanswered and under about 48 hours old, don't nudge again. New moms, moves, pregnancies: give it a week. Exception: sample-request and Meta access nudges can go 15 to 20 hours after our last message about it.
- **Polite but firm (2026-09-26).** Please, thank you, "feel free", "or put your own spin on it". Never bare orders.
- **Volume is 3 to 5 videos a week (2026-09-27, was 4 to 5).** Never excuse it ("don't worry about volume"); frame support as helping them hit it, with one natural line about the help they get (weekly inspo, hooks, help when stuck).
- **Reply in the thread** (Trybe's "Reply in thread") when answering a creator's specific message, like her answers to the fit questions. (2026-09-26)
- **Say "baby"** (or the child's name if the creator used it), never nicknames like "little guy". (2026-09-26)

## 4. Samples

- Approve on your own (then message): **V3** creators, requested **on or after 2026-09-17**, shipping to an **English-speaking country** (US, Canada, UK, Australia, New Zealand, Ireland). Multi-item requests from new V3 creators are fine. (2026-09-24)
- **NEVER approve a request made before 2026-09-17.** Old pending ones (Jasmyn, Kayse, Kristen, Aurora, Megan Devine, Autumn Bailey, Sara, Skyler) stay untouched. (2026-09-24)
- **Approve and message in the same step** (Jordan Murray's approval message was missed once).
- **Sample nudges sell THEIR benefit (2026-09-26):** it's a free product for them, never a favor to us. "did you get a chance to request your free sample yet? the sooner it arrives, the sooner you can start making videos".
- Creators who **already own a Bambora** need no sample and get no sample nudge: tell them to start filming with theirs.
- **Sample nudge:** accepted, no request yet: one natural nudge 15 to 20 hours after our last message about it.
- **2-week check-in** after approval: "hope it arrives soon if it hasn't, let me know when it does so I can share some ideas".
- **Tracking numbers are not in Trybe.** Trybe only creates the Shopify order number. If a creator asks for tracking, read the order number from the Samples tab and bring it to you (Fatima/Shopify has tracking). Never say "it hasn't shipped" from Trybe's status.
- Watch for duplicate names (two Kristen Smiths): match by date and account.

## 5. Applicants (Discovery Inbox)

**THE deciding rule (2026-09-23): can we see this person on camera, talking to camera?**
1. On camera, talking, confident clear delivery (calm or bubbly), clear English accent → **ACCEPT**. No socials or numbers needed.
2. Nothing on camera talking (text and music, product only, faceless voiceover, lip-sync, no videos) → **HOLD / REJECT**.
3. Big numbers (10K+ TikTok likes or followers, or 10K+ Instagram followers) but no on-camera talking → **DM the yapper ask**.
4. On camera but hesitant, stiff, poorly spoken, or a heavy accent → **REJECT**.

**Standing go to ACCEPT without asking you (2026-09-26 and 2026-09-27):** every fit question answered yes (a baby or toddler 10 to 50 lbs to film with, OK showing faces on camera, 3 to 5 videos a week) AND confident talking-to-camera videos AND lives in the US, Canada, UK, Australia, New Zealand or Ireland. Claude accepts, does the onboarding (move to V3 if they applied to Grandparents, welcome note in the thread, partnership ads request or connect-Instagram ask, sample nudge for the next day) and tells you in the sweep message.
**Standing go to REJECT:** Claude asked for a talking video, the answers were yes, and they never sent one (after one follow-up).
**Still yours:** conditional answers (hide faces, fewer videos, pay questions), borderline delivery, and anything no rule covers.

Also:
- Must speak English and live in an English-speaking country (hard requirements: otherwise reject).
- Talking to camera but small numbers: accept only with great energy on camera AND 3 to 4 real comments on recent TikToks (real people, not bots or emoji spam). Claude judges this itself and shows the evidence.
- **Automatic reject:** no message with the application AND no talking-to-camera videos AND weak engagement.
- After accepting: no extra personal DM (the automatic V3 welcome is enough); rejected applicants get no message.
- A big Trybe portfolio of talking-head videos overrides weak TikTok numbers (leaning accept, never auto-reject).
- Bilingual never counts against anyone. Their other content never counts against them. GMV is ignored. Existing Bambora customers are a strong plus.
- Accept into **Bambora Affiliates V3 (5%) only.**
- Every new applicant first gets the fit-questions message (`work/trybe-applicant-review/first-message.md`).
- Never ask for socials from someone whose Trybe videos already show them talking.
- Before any reject, show what each person sent (pitch plus what's on their videos) unless you've seen it.
- Applicants we asked for a talking video: one follow-up after a full day; still nothing 3 days later → reject or hold (your call).
- Moms who applied to the **Grandparents Program** by mistake: accept, move to V3, accept the move, then a short note ("ignore that first message about grandparents haha...").

## 6. Who to ignore (never message them)

- **Retainer askers:** Kia Layton, Krystal Camacho, Andrew Pagliara, Madison Grove. Kia is the #1 seller and is still ignored ("drop kia too, just ignore her").
- Also **Emily Seitz** and **Madison Tanefski**.
- **Abbey Way:** ignore her questions (2026-09-24).
- **Labourgeoise Bynum:** ignore completely; never approve her sample request (2026-09-26/27).
- **Reese** (Discovery inquiry asking $200 a video): ignore (2026-09-27).
- **Shelby Pinedo and Harley Haas:** never replied to the migration message; no follow-up until Fatima says.
- Upset creators (about the 5% change): open their messages so they are read, list them for Fatima, do not reply.

**Not ignored, but settled (do not reopen):** Tasha Clay accepted 10% and Fatima moved her herself on 2026-09-25. The move is DONE; never bring it up again. Answer her replies normally. Don't use her videos as inspo examples (bad thumbstop rate; Videos 3 and 4 in the example set are hers).

## 7. The 10 protected creators ("our loving creators")

Cambria Reau, Sophia Lease, Ciara Burnett, Carissa Lyman, Cassie Avery Charvat, Tasha Clay (12% program), Tayler Raza, Mary Saggau, Myrka Bustillo, Lilly Clark (v1, 10%).

- They keep their old commission. Never message them about commission or program changes; never move them.
- They DO get inspo, but read the context first: an unanswered money or retainer question comes first (to Fatima).
- They (plus Jennifer Thomas) make the best **non-sale** ads: use their videos as examples, never Kia's.

## 8. Money

- **Base retainer offer (2026-09-25):** creators who keep up 20 to 30 videos a month for 30 to 60 days get a guaranteed **$400 a month** base; "the real magic is in the commissions". Creators posting 20 to 30 videos a month usually hit 2 to 3 winners. No deadline, no per-product quota. Don't mention the dropped "$300 at $1,000 GMV" idea.
- Tasha Clay: accepted 10% and was moved on 2026-09-25 (settled; see section 6). A new question from her about money still goes to Fatima.
- Anything else about money: to you, and you check with Fatima.

## 9. Inspo

- Only for creators who **already have the sling**. New creators get the sample check-in first.
- **Cast every creator** like a casting director: their role (pediatrician, mom of 5, grandma, twin mom, dad) decides the formats. Creators can play roles they don't hold (older creator as a grandparent, young woman as aunt or babysitter), except **no pretend doctors or nurses**.
- Every inspo message says it's **just inspiration, put your own spin on it** (creators who do, do really well), includes the checklist link as a P.S. (reworded for repeats), and ends warmly.
- No baby in range: tester, rating, authority, pregnancy haul, "best baby shower gift", "the gift I'm saving for when baby's 10 lbs", or a reaction/stitch video (always with a specific link to react to, found last). Never a hospital bag.
- Replicate every idea for our people: for each inspo item, how could one of OUR creators film their own version, and who fits it.
- **Nivaro** (Atria): 3 to 5 top video ads every run; AI ones labelled "AI video"; creators film their own version (never make AI videos).
- Never send a creator her own video. Check `work/inspo/example-videos-map.md` before sending Video 1 to 7.
- After inspo: no reply in 2 days → "hey [name]! what did you think of the inspo I sent? need any help? really looking forward to seeing what you put together 💗" (varied).
- Inspo drafts go to you before sending, until you say they can go straight out.

## 10. Autonomy and irreversible actions

- Approve, reject and accept **only on your go**, per creator, even clear-cut ones. Exception: the standing accept and reject goes for applicants in section 5.
- **Existing creators' submissions: revisions and rejections HOLD until Fatima has watched the videos herself** (2026-09-27). Bring them to her; don't send them on your own yes alone.
- **Sweeps keep running when you're silent** (2026-09-25): past any stated end time, until you type `stop the routines`. So always type it at the end of your shift, then tell Fatima (one computer at a time).
- Except: eligible samples (section 4), which Claude approves and then tells you.
- **If your words could mean "discuss" instead of "act", Claude asks one line first** ("let's do the 8" was once read as "reject the 8"). (2026-09-24)
- **Test one before the batch:** after any change that affects outgoing messages (like a program welcome message), do one real case and read the thread before continuing. An empty V3 welcome once sent Trybe's generic default to six creators.
- Never touch **Accept All** or **Reject All** unless asked in those words.
- **Sweeps are never skipped because Claude is busy.** It tells you in one line and runs the sweep right after the current step.
- Status is always **live**: re-check the portal before reporting (Sam Macsai was listed after Fatima had already rejected her).
- **Anything new becomes a routine** in the same step (skill, routines, ledger), then pushed.
- **Solve from the data first**; ask only about taste and real decisions.
- **Unsure how Trybe works?** Check Trybe's help guides (top-right "Creators help" / "Discovery help" dropdown), then ask Trybe support via "Chat Now" in that dropdown. Don't guess. (2026-09-26)
- **Partnership ads never post to the creator's profile.** They only run as paid ads from her handle. Creator-friendly answer: "no need to post anything! the partnership ads run from your handle but they don't show up on your profile or feed 😊" (Trybe support, 2026-09-26)
- **Creators asking to post their videos elsewhere too:** fine, the program is sharing videos on Trybe so they can run as ads; kindly ask what they had in mind. (2026-09-26)

## 11. Drive

- Approved videos go to Drive folder **Trybe** (Main Media > Trybe, the media buyers' drive) right after approval, named `CreatorNameNoSpaces/fatima/trybe=<8-char id>` (the "fatima" part stays; it is the naming convention the media buyers use).
- Inspo and example videos go to **My Drive > Bambora Inspo**, never Main Media.
- **Nothing goes to Liam anymore (2026-09-27).** The Liam links messages (09-25) and then Liam's ad-launcher sheet were both retired. Filing in Main Media > Trybe is the whole job. Ignore any older Liam step you see in a routine file.
- Fatima's "Bambora_Trybe_DM_History" and "Tasks for Trybe Management" Google Docs are not for Claude to use.

## 12. Meta (partnership ads) access check (2026-09-25)

- Every ~5 hours (`every.sh due metaaccess 300`) Claude goes through every V3 creator who still lacks partnership ads access: clicks **Request** where it is available (then a tiny note), asks "--" creators to connect a **public** Instagram or Facebook in their Trybe profile (not if asked in the last 2 days), and nudges requests pending 3+ days once. Same message rules as always, logged in the ledger.

## 13. One machine at a time

- **Only ONE computer runs the routine at a time**: either this PC or Fatima's Mac, never both. Both are signed in to the same Trybe account, so two sweeps would reply to the same creators twice, approve the same samples twice and overwrite each other's follow-up ledger. Before you type "start the routines", make sure Fatima is not running hers, and tell her when you stop.
