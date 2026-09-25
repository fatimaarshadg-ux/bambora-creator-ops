# Conversation transcript: Ads Library copycat monitor (2026-09-22 to 2026-09-23)

Plain-text export of the session in which the tool was built. Tool calls and their outputs are left out; only what Fatima and Claude said to each other is kept. The full technical export (with tool calls) is `C:\Users\hp\Downloads\session-export-1790106921671.zip` on the PC.

**Fatima** (2026-09-22 16:04):

Hey, can you build me a tool that uses Apify to pull certain keywords from the ads library where it looks for certain kws and reports them to us so we can DMCA

**Claude** (2026-09-22 16:04):

I'll build a keyword monitor for the Meta Ads Library via Apify: it runs a scraper actor for your keywords, flags matching ads, and writes a report you can hand to whoever files the DMCA. First I'll check what's on this machine and confirm the current Apify actor details.

**Claude** (2026-09-22 16:07):

Research done: the official Apify actor takes Ad Library keyword-search URLs and returns ad text, page, dates and creative URLs. Now writing the tool into your claude-setup work folder.

**Claude** (2026-09-22 16:11):

Only arithmetic minus signs remain, no dashes. Syncing to GitHub now.

**Claude** (2026-09-22 16:13):

Pushed. The Mac had added one memory note that the PC didn't have, so I'll copy it over so both machines match, then wrap up.

**Claude** (2026-09-22 16:13):

The tool is built, tested offline, and pushed to your claude-setup repo under [work/ads-library-dmca-monitor](C:/Users/hp/claude-setup/work/ads-library-dmca-monitor/README.md). It has not run against live Apify yet because there is no Apify token on this PC.

**What it does.** It runs the official Apify Facebook Ads Library scraper on keyword searches, throws out ads from Bambora's own page, and flags the rest with one of three kinds of evidence:

- **brand**: a Bambora term appears in the ad text, headline or page name.
- **copy**: a distinctive sentence from bamboraco.com is reused (for example "giving your arms, back and wrists the relief they deserve").
- **visual**: an image or video thumbnail matches one of Bambora's own ad creatives. This is the part that catches stolen footage, which keyword search alone cannot. It uses perceptual hashing, and in the offline test a cropped, re-encoded copy of a creative scored distance 3 against an unrelated image's 26, so the cutoff of 10 is safe.

Every hit gets the Ad Library link and ad ID for the DMCA form, in an HTML report and a CSV. It remembers what it already reported, so later runs mark only what is new.

**Keywords: already loaded, you don't need to add any.** I pulled them from your site into `config.json`: brand terms (bambora, bamboraco, bambora sling, bambora carrier, a couple of misspellings), ten copy phrases from your product page and homepage, and five broad category searches (baby sling carrier, hip carry sling, hip seat carrier, and so on) that exist only to feed the visual check. Edit the file whenever an ad line gets copied. A copycat calling itself "Bambora Outlet" still shows up, because pages are excluded by ID only.

**Cost.** Apify bills per ad returned, roughly half a cent each. The worst case for the current config is about $34 a run, but exact-phrase brand and copy searches return very few ads, so a real weekly run should land at a few dollars. The free plan includes $5 of usage a month, the Starter plan is $19 a month with $19 included, and that should cover weekly runs. Run `python monitor.py --estimate` any time you change the keyword lists.

**Cadence.** Weekly, Monday morning. Copycat ads run for weeks and Meta's DMCA handling is not instant, so daily would just cost more. There is a script that registers a Windows scheduled task for that.

**Slack.** There is no Slack connector in this session, so the tool posts through a Slack incoming webhook, which you can point at your own DM when you create it. Three things only you can do, in this order:

1. Create an Apify account, copy the API token, then run the store script from the tool folder. The prompt hides what you paste.
```bash
powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\hp\claude-setup\work\ads-library-dmca-monitor\store-secret.ps1 -Name apify_api_token
```
2. In Slack, create an app, enable Incoming Webhooks, add a webhook and pick your own DM as the channel, then store the URL the same way with `-Name slack_webhook`.
3. Tell me, and I'll do the first live run, check the field names against real output, and register the weekly task.

**On Bustem.** This covers the Meta Ads Library slice of what they do (keyword sweeps plus image matching, with you as the human verifier). It does not cover marketplaces like Amazon, Temu or AliExpress, fake storefronts, or the enforcement side. Those would be separate scrapers on the same pattern if you want them later.

Pushed to GitHub: the tool, a memory note about it, and I also pulled the Mac's new media-watcher note onto this PC so both machines match.

**Fatima** (2026-09-22 16:13):

great job keeping that in mind

**Claude** (2026-09-22 16:13):

Thanks. Whenever the Apify token and Slack webhook are stored, say the word and I'll do the first live run and set up the Monday schedule.

**Fatima** (2026-09-22 16:13):

give me step by step instructions on what you want me to do

**Claude** (2026-09-22 16:14):

Here is everything on your side, in order. Steps 1 and 2 are required. Step 3 is only for Slack DMs.

**Step 1: Get an Apify token**

1. Go to https://console.apify.com/sign-up and create an account. The free plan is fine to start.
2. Once you're in, open https://console.apify.com/settings/integrations.
3. Under "Personal API tokens", copy the token shown (or click "Create a new token" and copy that).

**Step 2: Store the token on this PC**

Run this. It will prompt "Paste the value for apify_api_token". Paste the token and press Enter. Nothing shows on screen while you paste, that's expected.

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\hp\claude-setup\work\ads-library-dmca-monitor\store-secret.ps1 -Name apify_api_token
```

**Step 3 (optional): Slack DMs**

1. Go to https://api.slack.com/apps and click "Create New App", then "From scratch".
2. Name it something like "Ads Monitor", pick the Bambora workspace, click Create.
3. In the left menu click "Incoming Webhooks" and switch the toggle to On.
4. Scroll down and click "Add New Webhook to Workspace".
5. In the channel picker, choose yourself (your own name under Direct Messages) so it lands in your DMs, then click Allow.
6. Copy the Webhook URL that appears (starts with `https://hooks.slack.com/services/...`).
7. Store it here. Same hidden prompt as before:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\hp\claude-setup\work\ads-library-dmca-monitor\store-secret.ps1 -Name slack_webhook
```

**Step 4: Tell me you're done**

Just reply "done". I'll then:

- run the first live scan (it also builds the reference set from your own ads),
- check the real Apify output matches what the tool expects,
- send a test Slack message so you can confirm it reached your DM,
- register the Monday 09:00 scheduled task.

One note for later: the scheduled task runs on this PC, so it needs to be on or asleep (not shut down) on Monday mornings.

**Fatima** (2026-09-22 16:16):

can you just not do it all on your own

**Claude** (2026-09-22 16:16):

I can't do two parts, and it's a rule rather than a capability gap: I'm not allowed to create accounts on your behalf, or to paste API tokens, passwords or webhook URLs into anything. Everything else in this project I did or will do myself.

The minimum you need to do is about two minutes:

1. Sign up at https://console.apify.com/sign-up.
2. Copy the token from https://console.apify.com/settings/integrations.
3. Run this and paste the token when prompted:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\hp\claude-setup\work\ads-library-dmca-monitor\store-secret.ps1 -Name apify_api_token
```

Then reply "done" and I take over: the first live scan, checking the output, and the Monday schedule.

Slack is optional. If you'd rather skip creating the Slack app for now, the reports still save to disk every Monday and I can read you the new hits whenever you ask. We can add the DM later.

**Fatima** (2026-09-22 16:16):

using my extension

**Claude** (2026-09-22 16:17):

Even in your logged-in Chrome the same rule applies: I can't create accounts or handle tokens and passwords, so the sign-up and the token paste stay with you. What I can do is get you to the exact page so it's just clicks. Let me open it.

**Claude** (2026-09-22 16:17):

The Chrome extension isn't reachable from this session right now, so I can't open pages in your browser at the moment. Either Chrome is closed or the extension's side panel isn't signed in on this PC.

Even once it connects, the two steps stay with you: creating the Apify account and pasting the token. That's a hard rule for me, not a choice. All I'd be doing with the extension is opening the page for you, so it's just as quick to do it directly:

1. Sign up: https://console.apify.com/sign-up
2. Copy your token: https://console.apify.com/settings/integrations
3. Run this and paste the token at the prompt:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\hp\claude-setup\work\ads-library-dmca-monitor\store-secret.ps1 -Name apify_api_token
```

Reply "done" and I'll run the first live scan and set up the Monday schedule. If you want the Chrome extension working for later tasks, open Chrome, click the Claude side panel, and sign in with the same account as this app.

**Fatima** (2026-09-22 16:17):

done

**Claude** (2026-09-22 16:17):

Running the first live scan now.

**Claude** (2026-09-22 16:18):

Please run it once more. This time paste with a **right-click** in the window (not Ctrl+V), then press Enter. The script now checks the value and tells you if the paste failed.

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\hp\claude-setup\work\ads-library-dmca-monitor\store-secret.ps1 -Name apify_api_token
```

You should see "Saved apify_api_token (NN characters)". Reply "done" again and I'll start the scan.

**Fatima** (2026-09-22 16:18):

i want all the alerts to be in this channel

**Fatima** (2026-09-22 16:18):

[Image: source: C:\Users\hp\AppData\Local\Temp\claude\C--Users-hp--claude-backups\afbb6282-ff80-4a70-8d42-68dd57edb732\images\1.png]

**Claude** (2026-09-22 16:18):

Good, a channel is even better than a DM. Let me check whether the Apify token retry landed before I give you the Slack steps.

**Claude** (2026-09-22 16:18):

The Apify token on disk is still the failed paste, so there are two things to do, and they're independent. Do both, then reply "done".

**1. Apify token again** (paste with a right-click, not Ctrl+V, then Enter):

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\hp\claude-setup\work\ads-library-dmca-monitor\store-secret.ps1 -Name apify_api_token
```

You should see "Saved apify_api_token (NN characters)". If it says the paste failed, run it again.

**2. Slack webhook for #copycat-alerts:**

1. Go to https://api.slack.com/apps and click "Create New App", then "From scratch".
2. Name it "Copycat Monitor", pick your workspace, click Create.
3. In the left menu click "Incoming Webhooks" and turn the toggle On.
4. Scroll down, click "Add New Webhook to Workspace".
5. Choose **#copycat-alerts** as the channel, click Allow.
6. Copy the Webhook URL (starts with `https://hooks.slack.com/services/`).
7. Store it, again pasting with a right-click:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\hp\claude-setup\work\ads-library-dmca-monitor\store-secret.ps1 -Name slack_webhook
```

Once both say "Saved", reply "done". I'll run the first scan, post a test message to #copycat-alerts so you can see it arrive, and register the Monday 09:00 schedule.

**Fatima** (2026-09-22 16:19):

should be done

**Claude** (2026-09-22 16:19):

While the scan runs, on Slack: the webhook route I described is free. The paid wall you likely hit is Slack's own Workflow Builder (the "Automations" or "webhook trigger" inside the Slack app), which is Pro only. The free route is a custom app on the developer site:

1. https://api.slack.com/apps, "Create New App", "From scratch".
2. Name it, pick your workspace, Create.
3. Left menu, "Incoming Webhooks", switch On.
4. "Add New Webhook to Workspace", choose #copycat-alerts, Allow.
5. Copy the URL and store it (right-click paste):

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\hp\claude-setup\work\ads-library-dmca-monitor\store-secret.ps1 -Name slack_webhook
```

If step 4 shows "Request to install" instead of "Allow", your workspace requires an admin to approve apps. Then the workspace owner approves it in Slack admin settings, or you skip Slack and the reports stay on disk. The scan is running in the background; I'll report what it finds when it finishes.

**Claude** (2026-09-22 16:20):

The actor rejects "all" for its status field; it wants an empty string. Checking its full input schema so there's no second surprise, then fixing and rerunning.

**Claude** (2026-09-22 16:20):

Fixed and rerunning. The scan is in progress on Apify; I'll report the results as soon as it finishes.

**Fatima** (2026-09-22 16:21):

i ddont get it

**Claude** (2026-09-22 16:22):

Sorry, I buried it. Here's where things stand, in plain terms.

**Apify: done.** Your token works, and the first scan is running right now on Apify's servers. It will take a few minutes. I'll post what it finds when it's done.

**Slack: one thing left.** The tool needs a "webhook", which is just a special URL that lets it post into #copycat-alerts. Slack gives these out for free. To get one:

1. Open this link: https://api.slack.com/apps/new (it may ask you to sign in to Slack).
2. Click **From scratch**. Type any name, pick your workspace, click **Create App**.
3. On the next page click **Incoming Webhooks** (left side), then flip the switch to **On**.
4. Scroll down, click **Add New Webhook to Workspace**.
5. Pick **#copycat-alerts**, click **Allow**.
6. You'll now see a long URL starting with `https://hooks.slack.com/...`. Click **Copy**.
7. Run this, right-click in the window to paste, press Enter:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\hp\claude-setup\work\ads-library-dmca-monitor\store-secret.ps1 -Name slack_webhook
```

Then tell me and I'll send a test message into the channel. If you get stuck on a specific screen, paste a screenshot and I'll tell you what to click.

**Claude** (2026-09-22 16:26):

Re-scoring is running in the background. Here is the last Slack step:

1. Go to https://api.slack.com/apps and click **Bambora Copy Cat Hunter**.
2. In the left menu click **Incoming Webhooks**.
3. Scroll to the bottom. There's a table with one row for #copycat-alerts and a long URL starting with `https://hooks.slack.com/services/`. Click **Copy** next to it.
4. Click **Run** on the command below. A small popup window appears. Press Ctrl+V in the box, click OK.

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\hp\claude-setup\work\ads-library-dmca-monitor\store-secret.ps1 -Name slack_webhook
```

It should print "Saved slack_webhook". Tell me when it does, and I'll send a test message to the channel.

**Claude** (2026-09-22 16:27):

Quick status while that runs: the first scan alone used up Apify's free $5 for the month (it pulled about 880 ads, and more than half were Bambora's own and creator ads, which we had to pay to see). I'm now doing the image matching from the data already downloaded, so no extra spend, and I'll come back with the hits, the cost picture and what plan makes sense.

**Fatima** (2026-09-22 16:29):

dont gey it, please explain like i am 5 and you didnt say how much it would end up costing me

**Claude** (2026-09-22 16:30):

Simple version.

**How the money works**

Apify is like a vending machine for ads. Every ad it hands us costs about half a cent. Slack costs nothing.

Apify gives you $5 of free ads every month. That's roughly 850 ads.

**What happened today**

The first scan was a big one on purpose. It looked back 90 days and pulled about 880 ads, so it ate the whole free $5 in one go. That means no more scans until the free $5 comes back, around the 22nd of next month. If you don't want to wait, the Starter plan is $19 a month and lifts the cap straight away.

**What it costs from now on**

Weekly scans are much smaller. They only look at ads that started in the past week. In today's data only 26 ads were that new, so a weekly scan should cost around 15 cents. That's under $1 a month, which the free $5 covers. I've already set the tool to run that way.

| Item | Cost |
|---|---|
| Today's big first scan | about $5 (already spent, from the free credit) |
| Each weekly scan from now on | roughly $0.15 to $0.60 |
| Slack channel alerts | free |
| Monthly total on the free plan | $0 |

**What the first scan found**

After filtering out Bambora's own ads and your creators' ads (they all send people to bamboraco.com), only one ad mentioned Bambora from an unrelated page, a Chilean company called Green Brands Chile. The picture-matching step, which looks for your stolen footage, is finishing in the background right now. I'll post the results once it's done.

**What you still need to do**

Only the Slack webhook URL step from my previous message. Nothing else.

**Fatima** (2026-09-22 16:31):

show me the chilian add mentioned Bambora from an unrelated page, a Chilean company called Green Brands Chile. The picture-matching step, which looks for your stolen footage, is finishing in the background right now. I'll post the results once it's done.

**Claude** (2026-09-22 16:31):

Here is the ad: https://www.facebook.com/ads/library/?id=1419241293448866

It's not a copycat. Green Brands Chile sells bamboo face towels under the name "Bambora" (their site is bambora.cl) and the ad is in Spanish about skincare. It got flagged only because the word matched. I've told the tool to ignore that page and site from now on, so it won't show up again.

The picture-matching pass is still running in the background. It is hashing several hundred images from the scan, which takes a few minutes. I'll post what it finds as soon as it finishes.

**Fatima** (2026-09-22 16:33):

so what would be the best way to do this? like i wanna see copy cats using my exact product, obviusly they wouldnt be naming their product the same as me

**Claude** (2026-09-22 16:33):

Good question, and it changes what the tool should do. Straight answer: a keyword search can never find a copycat that avoids your name. It finds ads that *say* Bambora. So the three tiers of copycat need three different methods.

**1. They stole your actual photos or videos.** This is the most common copycat move, because your creatives already convert. It's also the only one you can DMCA, since copyright covers your footage, not your product. The tool already handles this: it takes a fingerprint of every image and video thumbnail in your own ads, then checks every new baby-sling ad against them. That's the picture-matching pass that's running now. No keywords involved.

**2. They sell a lookalike sling with their own photos.** No name, no stolen footage. A computer can't reliably tell "same product" from "similar product" with simple fingerprints, and honestly neither can Meta's DMCA form: a similar product with original photos isn't a copyright violation. You'd need a trademark or design registration for a takedown. What you can do is *see* them. The tool can post a weekly digest into #copycat-alerts: every new baby-sling or hip-carrier ad that appeared that week, with its picture. In today's scan that was around 26 ads, so it's a two-minute scroll for you, and you'd know instantly which ones are your product. That's free and I can add it now.

**3. They use your name or copy.** Covered by the keyword search, which stays in as a cheap extra check.

**What I'd do**

Run tiers 1 and 3 automatically with alerts only when something hits, and add the tier 2 weekly picture digest so you're the judge on lookalikes. If the digest gets too long later, a next step is having Claude look at each image and score "is this the Bambora sling design", about a cent per image, but that needs a Claude API key, so I'd hold off unless the digest becomes a chore.

Say "go" and I'll add the digest. The picture-matching results from today's scan will land as soon as the background job finishes.

**Fatima** (2026-09-22 16:36):

Yes, let me show you examples of what another tool found

**Claude** (2026-09-22 16:36):

Go ahead, paste or drop the screenshots here. Seeing what the other tool flagged will tell me which of the three tiers those copycats fall into, and whether the digest or the picture matching would have caught them.

**Fatima** (2026-09-22 16:38):

store context here, and when I am ready to pick this task back up, remind me

**Claude** (2026-09-22 16:39):

The secret scanner tripped on Facebook image URLs inside the scan data, which is gitignored anyway. Making the scanner respect .gitignore, then pushing.

**Claude** (2026-09-22 16:39):

Saved and pushed. When you come back and mention copycats, the ads monitor, or DMCA, I'll pick up from this exact point. One honest caveat: I can't send you a reminder at a time of my choosing, so the reminder fires when you open the topic, not on a clock.

**What's stored in memory**

- The tool, how it works, and what the first scan showed.
- The cost picture: the free $5 is used up until around October 22, weekly runs afterwards cost about 15 cents.
- The three copycat tiers we agreed on, and that the weekly picture digest is planned but not built.
- Your Slack channel and app exist; only the webhook URL step is left.

**Pending when you return**

1. Your screenshots of what the other tool found.
2. "Go" on the weekly picture digest.
3. Storing the Slack webhook URL.
4. Registering the Monday schedule.

The picture-matching pass on today's scan is still running in the background. Its report will be waiting in the reports folder, and I've noted where to look.

Pushed to GitHub: the tool updates, the memory note, and a fix to the sync script so it stops flagging Facebook image links as secrets.

**Fatima** (2026-09-22 16:41):

okay wait, maybe we are going about it in the wrong way, and maybe we dont need apify at all, since you can watch images, why dont you try running this manually? look for other stores selling this same product

**Claude** (2026-09-22 16:41):

Worth trying. Let me first look at your product so I know what I'm matching, then browse the Ads Library myself for sling ads.

**Fatima** (2026-09-22 16:41):

[Image: original 2304x4096, displayed at 1125x2000. Multiply coordinates by 2.05 to map to original image.]

**Fatima** (2026-09-22 16:41):

[Image: original 2304x4096, displayed at 1125x2000. Multiply coordinates by 2.05 to map to original image.]

**Claude** (2026-09-22 16:42):

Harvest works but returned nested duplicates. Deduplicating, loading more of the 760 results, and pulling bigger thumbnails.

**Claude** (2026-09-22 16:46):

Working through the sheets. Some sling ads are already visible, including three different page names running what looks like the same kitchen video. Loading the remaining nine sheets.

**Claude** (2026-09-22 16:47):

Going through all 349, I've marked about thirty ads that show a crescent-shaped hip sling. Pulling those up larger, with each one's destination site and ad text, so I can judge them properly.

**Claude** (2026-09-22 17:02):

Writing the findings and memory files with the file tool instead, then pushing.

**Claude** (2026-09-22 17:04):

Your instinct was right. Looking at the pictures myself found what the keywords missed, and it cost nothing extra.

**Found one real thief: explicitn.com**

- Their Facebook ad is your 56-second video of the woman in the brown sling, frame for frame. Ad link: https://www.facebook.com/ads/library/?id=2128834464362109
- Their product page is a copy of yours. Same 13 colours in the same order, and 21 of their 25 photos are your photos, including your "don't fall for knock-offs" graphic and your testimonial collages.
- They sit behind Cloudflare, so there are two places to file: Meta's copyright report form for the ad and page, and abuse.cloudflare.com for the store. Reporting them to PayPal can also kill their checkout.
- One thing to sort out first: their ad started on 7 August and the Bambora ad I found with that video started on 24 August. Find the original video file or the creator's first post so you can prove it's yours.

**Everything else was not theft**

- About a dozen anonymous dropship stores sell a lookalike sling with their own or AI-made pictures (one operator runs the same kitchen video under three store names). Annoying, but not a copyright case.
- Mabē, Qookie, Lune & Littles, Senarah and Wildride are real competitors with a similar design. Nothing to do.

**On "do we need Apify?"**

Not for reviews like this one. The data from today's scan is already on the PC, and I can go through it by eye any time. Apify only matters for *new* ads each week, and that costs about 15 cents a run, so I'd keep the cheap weekly pull. The automatic picture check did catch Explicitn on its own, so the theft cases will surface without anyone looking. Lookalikes still need a human eye, which is where the weekly digest into your Slack channel comes in.

The full write-up with evidence is saved in the repo under [findings/2026-09-22-first-scan.md](C:/Users/hp/claude-setup/work/ads-library-dmca-monitor/findings/2026-09-22-first-scan.md) and pushed to GitHub. A slower automatic pass over all 351 ads is still running in the background. If it finds any other exact copies I'll tell you.

Still on your side: the Slack webhook URL step, and "go" for the digest.

**Claude** (2026-09-22 17:08):

The automatic pass finished: it confirmed Explicitn and flagged one more, a home decor page called BO-HA. That looks like a false alarm from a plain image, so checking it before saying anything.

**Claude** (2026-09-22 17:08):

The BO-HA flag is a false alarm: a lamp on a plain wall got matched to one of your plain-background ads. I'll tighten the matching threshold so that stops happening. Here is the full list.

**Claude** (2026-09-22 17:09):

**Theft: your video and your product photos (file this one)**

- Explicitn-ea, ad started 7 Aug 2026
  Ad: https://www.facebook.com/ads/library/?id=2128834464362109
  Store: https://www.explicitn.com/products/toddler-sling-carrier

**Lookalike cluster A: one kitchen video, three store names, AI product pictures**

- Zenovap Baby Co., 11 Jul
  Ad: https://www.facebook.com/ads/library/?id=879349015237004
  Store: https://shopzenovap.com/products/zenovap%E2%84%A2-snugnest-baby-sling
- Movexas SnugNest Baby Sling, 27 Jun
  Ad: https://www.facebook.com/ads/library/?id=1643626853409013
  Store: https://shopwindlore.com/products/windlore%E2%84%A2-snugnest-baby-sling
- Movexas SnugNest Baby Sling, 25 Jun
  Ad: https://www.facebook.com/ads/library/?id=1724320778569294
  Store: https://windlore.com/products/windlore%E2%84%A2-snugnest-baby-sling

**Lookalike cluster B: generic mesh one-shoulder sling, dropship funnels**

- Cajatesoro, 21 Aug
  Ad: https://www.facebook.com/ads/library/?id=932209959363562
  Store: https://m.eigoods.com/funnel/news-lightw-eight-baby-car-riers-sync-1787280883008
- Luckinwish-official, 22 Aug
  Ad: https://www.facebook.com/ads/library/?id=1589802162766456
  Store: https://m.luckinwish.co.uk/funnel/news-lightw-eight-baby-car-riers-sync-1787280883008
- Outrer buy, 25 Aug
  Ad: https://www.facebook.com/ads/library/?id=1994469337717765
  Store: https://www.outrerbuy.shop/ul50gkocg400
- Dodoradoya, 17 Sep
  Ad: https://www.facebook.com/ads/library/?id=1112739058076870
  Store: https://m.eigoods.com/funnel/news-lightw-eight-baby-car-riers
- Scarfloft.LT13, 7 Sep
  Ad: https://www.facebook.com/ads/library/?id=2509368192878071
  Store: https://www.pagemindvibe.com/products/adjustable-single-shoulder-portable-strap-lightweight-and-breathable-mesh-hip-strap-1
- Mark Grace Smith, 2 Sep
  Ad: https://www.facebook.com/ads/library/?id=1395664061969443
  Store: https://fluxraa.com/products/adjustable-baby-sling-carrier
- Munichsunny, 18 Aug
  Ad: https://www.facebook.com/ads/library/?id=3101237180062326
  Store: https://munichsunny.com/products/baby-carriers-wwse-1
- Skiipshop, 3 Sep
  Ad: https://www.facebook.com/ads/library/?id=1091294146620398
  Store: https://skiip.in/products/adjustable-baby-sling-carrier
- G-Shopping.lk, 11 May
  Ad: https://www.facebook.com/ads/library/?id=1855634978452929
  Store: none, the ad only links to a Facebook page
- Sir John, 2 Jun
  Ad: https://www.facebook.com/ads/library/?id=1300864788835976
  Store: none, links to Shopee and Lazada listings in the ad text

**Real competitors with a similar design, own photos, nothing to file**

- Mabē Carriers: https://www.facebook.com/ads/library/?id=4638759623113653, https://www.facebook.com/ads/library/?id=3283076535227401, https://www.facebook.com/ads/library/?id=1566267788410444
  Store: http://mabeproducts.com/
- Qookie: https://www.facebook.com/ads/library/?id=1074095468510210, https://www.facebook.com/ads/library/?id=1386996590069391
  Store: https://qookie.com/en/products/qookie-go-sling-babytrage-huefttrage-salvia
- Senarah: https://www.facebook.com/ads/library/?id=2820801111612530, https://www.facebook.com/ads/library/?id=2168311940626734, https://www.facebook.com/ads/library/?id=1984676929088962, https://www.facebook.com/ads/library/?id=1710815589940469
  Store: https://senarah.com/products/senarah-child-sling
- Lune & Littles: https://www.facebook.com/ads/library/?id=1723441518914103
  Store: https://www.luneandlittles.com.au/

Note that most of these are not Shopify. Explicitn runs on a Cloudflare-fronted platform, and the cluster B funnels are custom shop builders. Only Zenovap, Skiip, Fluxraa, Munichsunny and the competitors are on Shopify.

The full automatic pass over all 351 ads finished and found no other exact copies of your creatives. I've tightened the picture-matching threshold after the lamp false alarm and pushed that to GitHub.

**Claude** (2026-09-22 17:09):

Good news from the slow pass: it found an earlier Bambora ad running the same video, started 31 July, a week before Explicitn's copy. That settles the date question. Updating the write-up.

**Claude** (2026-09-22 17:09):

The date problem is gone. Your ad https://www.facebook.com/ads/library/?id=1343534694113082 ran the same video from 31 July, a week before Explicitn's copy went live on 7 August. When you file with Meta, cite that ad ID as the original alongside the copy's ID 2128834464362109.

The write-up and memory are updated and pushed. Nothing else is running in the background now.

**Fatima** (2026-09-22 17:14):

i love this, can you run these checks on a weekly basis and send a message inside my slack?

**Claude** (2026-09-22 17:14):

Yes. The automatic checks can run on a schedule from this PC, and the weekly Slack message can carry both the alerts and a picture digest of every new sling ad for you to eyeball. Let me build the digest into the tool and register the schedule.

**Claude** (2026-09-22 17:16):

Offline test passes, including the digest and Slack previews. Now registering the weekly schedule on this PC and pushing.

**Claude** (2026-09-22 17:18):

My log edit put a global reference before the declaration. Fixing that and retesting.

**Claude** (2026-09-22 17:20):

Done. The weekly run is scheduled on this PC and tested.

**What happens every Monday at 9am**

1. The tool pulls every Meta ad from the past week for your brand terms, your copy phrases, and the sling category searches.
2. It drops your own and your creators' ads, then checks the rest for your name, your copy, and your exact images or video frames.
3. It posts two things to #copycat-alerts. First, an alert list of anything flagged, with Ad Library links. Second, a picture digest: every new baby-sling ad from other pages with its thumbnail, so you can scroll it in a minute and spot lookalikes yourself.
4. If the scan can't run, it posts a plain note saying why instead of going quiet.

**Two things to know**

- Apify's free credit is used up until around 22 October. Until then the Monday message will say the scan didn't run. If you want it working next Monday, upgrade to Apify's $19 Starter plan at console.apify.com. After that, each weekly run costs pennies.
- The PC needs to be on, or asleep rather than shut down, on Monday mornings. If it's off, the task runs as soon as the PC is next on.

**The one step still yours**

Nothing reaches Slack until the webhook URL is stored. In Slack's app settings, open the Bambora Copy Cat Hunter app, go to Incoming Webhooks, copy the URL at the bottom, then click Run below. A small window pops up. Paste with Ctrl+V and click OK.

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\hp\claude-setup\work\ads-library-dmca-monitor\store-secret.ps1 -Name slack_webhook
```

Tell me when it says "Saved" and I'll send a test message to the channel straight away.

Everything is pushed to GitHub, and the memory note records where things stand.

**Fatima** (2026-09-22 19:55):

okay save our comvo histroy
