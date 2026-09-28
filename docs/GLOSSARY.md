# Glossary

**Bambora** The brand: a baby sling carrier (bamboraco.com). "Made by Parents. Loved by Parents."

**Bombara** The working folder's name, misspelt on purpose so all the notes match. Never write "Bombara" to anyone.

**Trybe** The creator platform (jointrybe.com) where creators join Bambora's programs, request samples, upload videos and chat.

**Brand portal** Trybe's website for brands: https://jointrybe.com/brand?b=a8bedbc3-3b30-410d-a09e-2aa3aeb3a8e9

**Brand API** Trybe's programmatic interface (api.jointrybe.com/v1). Scripts use it for submissions, creators and earnings. Needs the API key.

**API key** The secret that lets scripts use the Brand API. Stored with DPAPI on this PC; never in chat or the repo.

**DPAPI** Windows' built-in encryption tied to your Windows account. Only your account on this PC can decrypt the stored key.

**Operator** You: the person running the job on this PC.

**Creator** Someone who films videos for Bambora (usually a mom, sometimes a dad or grandparent).

**Program** A Trybe commission plan. **V3** = "Bambora Affiliates V3", the 5% program everyone new joins. Also the 12% program, Ambassador (10%), v1 (legacy 10%) and the **Grandparents Program** (5%).

**The 5% migration** September 2026: most creators were asked to move from 10 or 12% to V3 (5%). Some said yes, some asked for retainers (ignored), some never replied.

**Protected creators / "loving creators"** The 10 who keep their old commission: Cambria Reau, Sophia Lease, Ciara Burnett, Carissa Lyman, Cassie Avery Charvat, Tasha Clay, Tayler Raza, Mary Saggau, Myrka Bustillo, Lilly Clark.

**Ignore list** Creators never messaged: retainer askers Kia Layton, Krystal Camacho, Andrew Pagliara, Madison Grove; also Emily Seitz, Madison Tanefski; Abbey Way's questions.

**Retainer** A guaranteed monthly payment. Fatima's model: $400/month base for creators who keep up 20 to 30 videos a month for 30 to 60 days.

**GMV** Gross merchandise value: sales a creator drove. Commission is a % of it. Ignored when judging applicants.

**Submission** A video a creator uploads to Trybe for approval. Has a full id (`submission_<uuid>`) and a short **trybe id** (last 8 characters).

**Approve / reject / request revision** The three decisions on a submission. Approve releases money. All three notify the creator. Always need your go.

**Revision / re-take** Sending a video back with a fix ("one hand on baby"), plus the checklist link.

**The checklist** The 6-point filming standard, https://bamborachecklist.netlify.app/: seat under the bottom, one hand on baby every frame, buckle closed with the safety loop, close enough to kiss, vertical 9:16, no watermarks.

**M position** Baby's knees higher than the bottom, like an M. Required for babies; less strict for toddlers.

**Safety loop** The loop on the buckle that must be used; a common miss.

**Hands free** A claim Bambora no longer makes. One hand on baby always.

**10 to 50 lbs** The sling's weight range. Always a weight, never an age.

**Sale-led** A video that opens on, is built around, or repeats a sale. Not allowed (a short mention at the end is fine).

**Sample** A free sling a creator requests through Trybe to film with.

**SAMPLE GATE** The hard rule: check a creator's real sample status in the Samples tab (this sweep) before saying anything about her sample.

**20-hour nudge** One reminder to request a sample, 20+ hours after acceptance.

**Applicant / join request** Someone asking to join a program, in Discovery > Inbox.

**Discovery** Trybe's section for finding and reviewing creators (Inbox = applicants, Messages = their pitches, Invited = people we invited).

**Yapper / talking head** A creator who talks straight to camera. The main thing we look for.

**Yapper ask** The template DM asking an applicant for talking-to-camera content.

**seen.txt** The list of applicant names already reviewed (`work/trybe-applicant-review/seen.txt`). Anything in the Inbox not on it is NEW. (There is a separate `work/inspo/seen.txt` for inspo items already used.)

**Taste profile** Measurements of Fatima's best yapper creators (pace, energy) used as a benchmark for applicants.

**Partnership ads / PA / Meta access** Permission for Bambora to run a creator's video as an ad from her own Instagram or Facebook. Requested on the Creators roster; the creator accepts on Instagram. Needs a PUBLIC Instagram (or Facebook).

**"--" (on the roster)** The creator has no Instagram or Meta connected to Trybe, so partnership ads can't be requested yet.

**canRequest / noConnect / pendingPA / noSample** The groups `rosterScan()` returns: can be requested now / needs to connect Instagram / request pending / no sample request yet.

**Sweep** One full pass of all six streams, every 30 minutes.

**The six streams** chat, samples, partnership (ads), submissions, discovery, ledger.

**Stream stamp** A tiny file recording when a stream last ran (`work/sweep/streams/`).

**Watchdog** A background script that wakes Claude when a sweep or stream is late.

**Keep-awake** The background program that stops Windows sleeping during the shift (the Mac's "caffeinate").

**Helper server** `cors_srv.py` on port 8765, serving the JavaScript helpers to the Trybe page.

**Helpers** `chat-helpers.js`, `roster-scan.js`, `sample-status.js`: JavaScript Claude runs inside the Trybe page.

**g2() / ACK** The guarded send. g2 refuses to send while the creator's newest message is unanswered, until Claude has read it and set `ACK[name]=true`.

**qCheck()** Finds unanswered creator questions in a thread.

**convoScan()** Lists who is waiting on us (needsUs) and who we are waiting on (waiting).

**cl=3 / cl=1 / cl=4** Harmless URL markers on Claude's own Trybe tabs: chat, Discovery, Creators.

**front.ps1** Brings Chrome and the Trybe tab to the front (Chrome ignores clicks in background tabs).

**Ledger** `followups.json` + `followups.py`: every follow-up, check-in and promise owed, with due dates.

**due / add / done / snooze** The ledger commands.

**Quiet creator** No video in 14+ days (and with us 14+ days). Gets a "noticed you haven't posted, how are you, happy to share ideas" check-in.

**Inspo** Inspiration: example videos and ideas sent to creators ("just inspo, put your own spin on it").

**Inspo pack** The every-3-days research bundle in Drive "Bambora Inspo / Week of ...", tagged in `tags.tsv`.

**Atria** An ad-library service (tryatria.com) used to find top-performing ads for inspo.

**Nivaro** A brand in Atria whose ads Fatima rates; 3 to 5 of theirs go in every pack.

**Reaction / stitch** A format where a creator reacts to someone else's viral video (for pregnant creators with no baby in range).

**Casting** Seeing each creator as roles she can play (pediatrician, mom of 5, grandma, aunt, babysitter), never pretend doctors or nurses.

**Example videos (Video 1 to 7)** Anonymous example videos from our creators in Drive; the map of whose is whose is private (`work/inspo/example-videos-map.md`). Never name the creator.

**Liam** A media buyer. You don't send him anything: since 2026-09-27 approved videos only go into the Drive Trybe folder.


**Main Media** The media buyers' shared Drive. Only approved Trybe videos go there (Main Media > Trybe).

**Creator database** One profile per creator in `work/creator-db/db/` (facts, style notes, DMs, frame sheets).

**Creator Tracker** The Claude Doc where the ledger and profiles are shown for humans.

**Media watcher** The tool that lets Claude "watch" a video: timestamped frames plus a transcript.

**tt.py** The TikTok checker (never the browser for TikTok).

**Session log** The end-of-day note in `work/session-logs/`: done, new rules, open items.

**sync.ps1** Pushes the repo to GitHub with a secret check.

**MCP / connector** A plug-in that gives Claude tools: Trybe (local), Google Drive, Notion, Claude Docs, Atria, Claude in Chrome.

**Claude in Chrome** The Chrome extension that lets Claude use your signed-in Chrome.

**Allowlist** The list of commands Claude may run without asking; prevents unattended runs from freezing.

**Scheduled task** A saved recurring job in the Claude app; can only draft, never send.

**PKT** Pakistan time (UTC+5), Fatima's timezone.
