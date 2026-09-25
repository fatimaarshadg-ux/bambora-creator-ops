---
name: trybe-applicant-review
description: Review new creator applications (join requests) in Bambora's Trybe Discovery Inbox and sort every applicant into accept, DM-to-ask, borderline, or reject using Fatima's criteria. Use when she says "review the inbox", "check new applicants", "who applied", "go through join requests", or names an applicant and asks whether to accept them. Not for reviewing video submissions from existing creators (that's the content checklist).
---

# Trybe applicant review

This is the method, not a record of any one batch. The criteria live in memory: `bambora-creator-acceptance-criteria` (decision grid, accent rule, energy definition, DM templates). Pending DMs live in `trybe-applicant-followups`. Load the `trybe-portal` skill for portal navigation. Read all three before starting.

Work on your own and report once, with evidence. Fatima wants little hand-holding. The only things that wait for her go are the irreversible ones: approve, reject, send.

## 0. Before anything
- Check `trybe-applicant-followups` first. Open each thread, read replies, and settle those people before starting the new batch.
- Make sure the keep-awake from `start.ps1` is running if the operator has stepped away from the PC.
- Open your own Chrome tab (add `&cl=1` to the URL so front.ps1 can bring it forward). Chrome drops clicks in background tabs; see the trybe-portal skill.

## 1. Collect every applicant (fast, no per-card clicking)
1. Discovery, Inbox tab (the dropdown on narrow windows). Set **Per page** to 100.
2. Walk each card's Reject button up the React fiber to the prop holding `creatorProfile`: country, `instagramUrl`, `tiktokUrl`, `languagesSpoken`, program.
3. Featured videos (`portfolioItems`) only load in the profile modal. Open each modal by a scripted `.click()` on the name, read the fiber, then dispatch Escape. Run the loop in the page without awaiting it, using a **MessageChannel sleep** (background tabs throttle setTimeout to 1s or worse), and poll a `window._prog` counter.
4. Export: javascript_tool output truncates at about 1,000 characters. Prepend an `<article>` holding the text, read it with get_page_text, then remove it.
5. Discovery, **Messages** tab: the full text of each pitch is in the row's second `td`. Only the 50 most recent are listed, so older applicants show "no message found (could not verify)", never "sent nothing". Video pitches need the row opened and looked at.

## 2. Watch the Trybe featured videos
`scripts/yap.py` takes the first 25s of audio plus 3 frames from each creator's first 2 portfolio videos (public cdn.jointrybe.com URLs, no auth) and transcribes them with faster-whisper `small`. `scripts/sheet.py` builds contact sheets; read them. `scripts/energy.py` gives words per second plus loudness and pitch variation. Adjust the paths at the top of each script to your working folder.

**Yapper = speaking straight to camera for at least part of the video.** Voiceover over lifestyle footage does not count. Neither does lip-sync, or text overlays with music.

## 3. Social numbers and engagement
- **TikTok: never use the browser** (it gets a 403 within minutes). Use `py -3 ~/claude-setup/work/social-tools/tt.py <handle> --videos 4 --comments 10`. For likes and follower totals, one profile page load each at a normal pace is fine; the data-e2e selectors are in `tiktok-no-browser-tool`.
- `scripts/cscore.py` counts **real** comments per video: not the creator's own, not spam, at least two real words.
- **Instagram:** her logged-in Chrome. Profile `og:description` gives followers; each post's `og:description` gives likes and comment counts. Keep a 3 second pace.
- For creators with the numbers but no yapper video on Trybe, **check their TikTok for yapper content before drafting any DM**: download the 3 most-viewed recent videos with yt-dlp, then take frames and a transcript.

## 4. Decide: the ONE rule (Fatima, 2026-09-23; replaces the numbers-first grid)
Ask one question first: **can we see this person on camera, talking to camera?** Check their Trybe featured videos, their application video, and (only if both are empty) their TikTok.
- **Yes, and the delivery is confident and clear with a clear English accent → ACCEPT.** No socials, numbers or comments needed (Alison Boutwell, Judith Coronel).
- **No on-camera talking anywhere** (text and music, product-only, faceless voiceover, no videos) → **HOLD or REJECT**. There's nothing to judge (Jimmy Ralph).
- **No on-camera talking, but 10K+ numbers → yapper-ask DM.**
- **On camera but weak** (hesitant, stiff, heavy accent) → **REJECT.**
- Existing customers are a plus; GMV is ignored; bilingual never counts against anyone; their other content never counts against them.
Never send a socials ask to someone whose Trybe videos already show them talking to camera. That mistake was made with Alison on 2026-09-23.

## 4b. Old grid details (kept for reference)
- Country and accent first. A heavy accent, or non-English content with no English videos, means reject. If there's real potential, send the English-content DM instead.
- Yapper + numbers: accept. Yapper under numbers: needs confidence against the taste profile AND 3-4 real comments per recent video.
- No yapper + numbers: DM asking for yapper content. No yapper + no numbers: reject.
- Existing Bambora customers: strong plus, accept.
- Applicants she has already messaged: wait for the reply.
- Her other content never counts against a creator. GMV is ignored.

**Taste:** `taste-profile.md` in this folder, built from her top-selling and recently approved **yapper** videos. Rebuild it every month or two with `scripts/taste_metrics.py` (Trybe API: send a normal User-Agent or it 403s), because her taste and her winners change. Confidence can be calm or bubbly. What fails is hesitant, stiff, or poorly spoken.

## 5. Report, then act on her go
Report counts per bucket with names and a one-line reason each, flagging the weakest accepts and genuine judgement calls. Keep it short.

On her go:
1. Accept **one** first, open the thread, and read what the automatic V3 welcome actually sent.
2. Accept the rest.
3. Send DMs one at a time from the profile modal's **Open chat** button (applicants have no /brand/chat thread yet). Before sending: the header must match the exact name, the thread must NOT already contain the message (skip if it does), and the composer must be empty. After sending: confirm the message appears exactly once. Write drafts in the voice rules from `feedback-creator-dm-voice`, and label any style examples you show her as "example only, not sending".
4. Reject.
5. Log every DM in `trybe-applicant-followups` with a follow-up date of the next working day.
6. Push memory and skill changes to claude-setup.

## Traps learned the hard way
- A check that failed is not a negative result. Say "could not verify".
- Never overwrite claude-setup's `memory/MEMORY.md`. Add lines only.
- Two identical failures means stop and find another route (see think-before-grinding).

## Trybe portfolio rule (Fatima, 2026-09-23)
Before any reject, count the applicant's videos on Trybe (the card's submission count and featured videos). If they have a lot of Trybe videos and those are yapper / talking-head style, weak TikTok or IG engagement is NOT grounds to reject. Put them under "Worth checking, leaning accept" with the evidence (video count, a note on their delivery and accent) for her decision. Being bilingual never counts against anyone; a clear, pleasant English accent is what matters.
