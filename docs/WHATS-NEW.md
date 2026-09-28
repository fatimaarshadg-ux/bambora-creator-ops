# What's new (2026-09-28)

Everything Fatima decided between 2026-09-25 and 2026-09-28. Claude already follows all of it (it's in memory and the routines); this page is so you know too.

## The big ones

1. **Send window: nothing to creators before 12 PM US Eastern** (9 PM Pakistan time; 10 PM after the US clocks change on Nov 1). That includes messages, accepts, approvals and rejections, because each one notifies the creator. Before 12 PM ET, sweeps still check everything and put what they'd send in `work/send-queue/<date>.md`. The first sweep after 12 PM ET sends the queue. Claude checks the US time with `work/common/us-time.ps1`.
2. **Nothing goes to Liam anymore.** Approved videos are filed in Google Drive, Main Media > Trybe, and that's the whole job. No Liam sheet, no copy to his folder, no Slack message.
3. **Claude accepts some applicants on its own now.** Every fit question answered yes (baby or toddler 10 to 50 lbs to film with, OK showing faces, 3 to 5 videos a week) + confident talking-to-camera videos + lives in the US, Canada, UK, Australia, New Zealand or Ireland = accept, onboarding, and it tells you. Asked for a talking video and never sent one (after one follow-up) = reject. Conditional answers and borderline cases still come to you.
4. **Existing creators' videos:** clear-cut approvals (all 6 checklist points, not sale-led) go ahead on their own and show up under Done. Unsure ones come to you. **Revisions and rejections wait until Fatima has watched them herself.**
5. **Sweeps keep running until you type `stop the routines`.** Always type it at the end of your shift, then message Fatima. Keep-awake starts by itself with "start the routines" and stops with "stop the routines".

## Messages

- **Volume is now 3 to 5 videos a week** (was 4 to 5). Never excuse it; frame support as helping them hit it, with one natural line about the help they get (weekly inspo, hooks, help when stuck).
- **Follow-ups must read as follow-ups.** Claude reads the last 3 messages first (`ctx(name)`; the chat helper refuses to send otherwise) and writes the next line of that conversation.
- **No double follow-ups:** our last message unanswered and under about 48 hours old means no new nudge. Sample and Meta access nudges can go after 15 to 20 hours.
- **Sample nudges sell their benefit:** "your free sample", "the sooner it arrives, the sooner you can start making videos". Never a favor to us.
- **Polite but firm**, reply in the thread when answering a specific message, say "baby" (not "little guy").
- **Partnership ads never post on the creator's profile.** They only run as paid ads from her handle.
- **Creators who want to post their videos elsewhere too:** that's fine; kindly ask what they had in mind.
- **Unsure how Trybe works?** Trybe's help guides first, then Trybe support ("Chat Now" in the top-right help dropdown). Don't guess.

## Safety and reviews

- **Cooking and stairs are fine** with one hand on the baby. A baby chewing the straps is not a safety issue. Only flag what the rules say.
- For ads, Claude uses the **deep watch** (`adwatch`: every cut, music, pacing) and says how it watched.

## Who to ignore (new)

- **Labourgeoise Bynum:** ignore completely, never approve her sample.
- **Reese** (asked $200 a video): ignore.

## For your PC

- The video watcher now installs the deep-watch tool too (it was missing from the Windows installer).
- Claude in Chrome can end up in Fatima's Mac browser because it's the same account. Claude picks the browser on THIS PC; if tabs vanish or clicks stop working, tell it "list the connected browsers and use the one on this Windows PC".
