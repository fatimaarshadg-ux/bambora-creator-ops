# Why Fatima had to hand-hold on 2026-09-23/24, and what changed

Goal: she opens the laptop, says "run the routines", and everything runs with only real decisions coming back to her.

## Root causes (in order of cost)

1. **Messages didn't sound like her** (Jen's comfort essay, Marisa's "Mom of 4" opener, Katherine's over-explained approval, "by the way" openers). I optimised for "personal" and "thorough" instead of "what would she actually type". The lint only caught phrases, not habits.
   Fix: four rounds of taste Q&A turned into a cheat sheet (human-messages section 7) plus lessons. Lint now blocks comfort phrases, "no rush", "just following up", "on board", "so much content", and any chat reply over 220 characters. New rules: answer their last line first, then "also"; no remarks built from bios; thank-yous stay tiny.

2. **I reported work as "left to do" instead of doing it.** Cheylene, the sample nudges, the "--" investigation and the applicant follow-ups were listed back to her when rules already covered them.
   Fix: `routines/full-run.md`, one ordered checklist that does every stream in one pass. Only true decisions come back, in ONE message with a recommendation each.

3. **Creator questions went unanswered for days.** Abbey Way's questions from Sep 19 and Jena's background-music question were missed. Sweeps looked at Unread threads, and a quick "love that!" made a thread look handled.
   Fix: `qCheck()` in chat-helpers.js flags a creator question when nothing we sent afterwards shares a real word with it. It runs on every thread the full run opens, and unanswered questions go in the end-of-run list.

4. **Stale state.** I listed Sam Macsai after she'd already been rejected, and the page ran an old copy of the helpers without the new checks.
   Fix: always re-check live state before reporting it. The helper server now serves straight from the repo folder, so the page always gets the current code.

5. **Rules she had to state in the moment:** her 5 PM to 5 AM day; dolls only for creators with no kid in range; creators who own a Bambora need no sample; never approve sample requests from before Sep 17; partnership ads are accepted on Instagram or Facebook; "--" means no Instagram connected; the casting mindset; Nivaro in inspo; ideas replicated for our creators.
   Fix: every one is now in core-rules, a skill or full-run.md. Once written down, each one applies automatically.

6. **Tool friction ate time and made me go quiet.** The search helper missed some rows, the emoji search only knows short names, background tabs throttle, and long scripts timed out.
   Fix: open2/openT with retries, rx1/rx2 for reactions, front.sh before every batch, and loops run in the page with polling. Short progress lines while working.

7. **I didn't know how the "--" status worked**, so partnership ads looked half-done.
   Fix: `roster-scan.js` reads the roster data directly. It returns who can be requested, who has no Instagram connected, who is pending, who has no sample, and which sample requests are old. One call instead of guesswork.

## What still needs her (by design)
Approve, reject or revise submissions; accept applicants; answers to questions no rule covers (money, commission, her assets); anything that ships product outside the delegated rule.
