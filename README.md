# Bambora creator ops: the handover

> **PRIVATE REPO. Keep it private.** It names real creators, their messages and their sales. Never make it public, never share the link outside Bambora, never paste parts of it anywhere public.

This repo lets you do Fatima's whole daily Bambora creator job (Trybe chat, samples, partnership ads, video reviews, new applicants, follow-ups, inspo, Drive filing) on a **Windows PC** with **Claude Code** doing the heavy lifting. Claude already knows every rule, every creator and everything that is owed; you just start it each work day and say yes or no to the few things that need a human.

You need about **1 hour** for the setup below. After that, starting a work day takes 2 minutes.

> **ONE COMPUTER AT A TIME.** Only one machine may run the routine ("start the routines") at any moment: this PC **or** Fatima's Mac, never both. Both use the same Trybe account, so two running at once would message the same creators twice, approve the same samples twice and overwrite each other's follow-up list. Agree with Fatima who is on shift, and tell her when you start and stop.

---

## Before you start: have these ready

| What | Where you get it |
|---|---|
| A Windows 10 or 11 PC, with internet | yours |
| Fatima's Bambora Google login (fatima@bamboraco.com) | Fatima gives it to you. This gets you into Trybe, Google Drive, Notion and Slack as her. |
| The **Trybe API key** | Fatima sends it to you privately. You paste it once into a hidden box. **Never paste it into the Claude chat.** |
| A **GitHub** account that can see this private repo | github.com (free). Fatima (or whoever owns this repo) invites your username. |
| A **Claude** account with Claude Code (Pro or Max plan) | claude.ai. Ask Fatima which account to use. |

---

## Step 1. Open PowerShell

1. Click the **Start** button (Windows logo, bottom left).
2. Type `PowerShell`.
3. Click **Windows PowerShell** (the blue icon). A window with a blue or black background opens. This is where you paste the commands below.

To paste into PowerShell: copy the command, then **right-click** inside the PowerShell window (or press Ctrl+V). Then press **Enter**.

## Step 2. Install Git

Paste this and press Enter:

```powershell
winget install -e --id Git.Git --accept-package-agreements --accept-source-agreements
```

- If Windows asks "Do you want to allow this app to make changes?", click **Yes**.
- If it says `winget` is not recognized: open the **Microsoft Store**, search **App Installer**, click **Get** or **Update**, then try again. Or download Git by hand from https://git-scm.com/download/win and click Next through the installer (the defaults are fine).

When it finishes, **close PowerShell and open it again** (Step 1), so Windows notices Git.

## Step 3. Download this repo to the right place

First, accept the invitation: GitHub emails you "invited you to collaborate" (or open https://github.com/notifications). Click **View invitation**, then **Accept invitation**. Without this, the download below says "Repository not found".

Paste this, replacing `fatimaarshadg-ux/bambora-creator-ops` with the repo's name from its GitHub page (for example `fatimaarshadg-ux/bambora-ops-handover`):

```powershell
git clone https://github.com/fatimaarshadg-ux/bambora-creator-ops.git "$env:USERPROFILE\claude-setup"
```

- A GitHub sign-in window pops up the first time. Sign in with **your** GitHub account and click **Authorize**.
- It must go to `C:\Users\<you>\claude-setup` exactly, because every note and script points there. The command above does that.

## Step 4. Run the installer (one command)

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\claude-setup\install.ps1"
```

What you will see, in order:

1. It lists the programs it is about to install (Python, Chrome, Node.js, ffmpeg, yt-dlp, Google Drive for desktop, GitHub CLI, the Claude app) and installs them one by one. Click **Yes** whenever Windows asks to allow changes.
2. It sets up Python packages, the working folder `C:\Users\<you>\Bombara`, and the **media watcher** (the tool that lets Claude watch videos). This is the slow part: 3 to 15 minutes.
3. It asks for **your first name** (for the repo history). Type it and press Enter.
4. A small window titled **Trybe API key** opens. Paste the key Fatima gave you (Ctrl+V) and click **OK**. The box hides what you paste. No key yet? Click **Skip for now**.
5. It asks **"Add them now? (Y/n)"** about Claude's permissions. Press **Enter** (yes). This lets the routine run its own scripts without stopping to ask you every time.
6. It finishes with a **self-test table**: every line should say **PASS**.

If anything says **FAIL**, the Fix column says what to do. Usually: close PowerShell, open a new one, and run the same install command again. It skips everything that already worked.

<details>
<summary>If winget cannot install something: the manual download links</summary>

Install these by hand (click Next through each installer; defaults are fine), then run the installer again with `-NoWinget` at the end of the command.

| Program | Link |
|---|---|
| Git (includes Git Bash) | https://git-scm.com/download/win |
| Python 3.12 (tick "Add python.exe to PATH") | https://www.python.org/downloads/windows/ |
| Google Chrome | https://www.google.com/chrome/ |
| Node.js LTS | https://nodejs.org/ |
| ffmpeg | https://www.gyan.dev/ffmpeg/builds/ (the media watcher also brings its own copy) |
| yt-dlp | https://github.com/yt-dlp/yt-dlp/releases/latest (the media watcher also brings its own copy) |
| Google Drive for desktop | https://www.google.com/drive/download/ |
| GitHub CLI | https://cli.github.com/ |
| Claude desktop app | https://claude.ai/download |

</details>

## Step 5. Chrome: sign in as Bambora and add Claude in Chrome

1. Open **Google Chrome**. Click the round profile picture at the top right, then **Add** (a new profile). Choose **Sign in**, and sign in with **fatima@bamboraco.com** and the password Fatima gave you. Use this Chrome profile for all Bambora work, and your own profile for everything else.
   - **Heads-up:** Google will probably say "Verify it's you" or send a prompt to **Fatima's phone**, because it is a new PC. Message Fatima before you start this step so she can tap **Yes** (or read you the code). The same can happen for Slack and Notion.
   - If Chrome asks "Turn on sync?", **Yes** is fine in this Bambora profile (it keeps you signed in).
2. Go to the **Chrome Web Store** (https://chromewebstore.google.com), search **Claude**, open **Claude** by **Anthropic**, click **Add to Chrome**, then **Add extension**.
3. Click the puzzle-piece icon at the top right of Chrome, then the pin next to **Claude**, so its icon stays visible. Click it and sign in with the **Claude** account.
4. In this same Chrome, open and sign in to each of these (keep them signed in):
   - Trybe brand portal: https://jointrybe.com/brand?b=a8bedbc3-3b30-410d-a09e-2aa3aeb3a8e9 (use the same sign-in Fatima uses for Trybe; if you see a **Continue with Google** button, click it and pick fatima@bamboraco.com. If you are not sure, ask her before trying passwords.)
   - Google Drive: https://drive.google.com
   - Notion: https://www.notion.so
   - Slack: https://app.slack.com

## Step 6. Google Drive for desktop

1. Click **Start**, type `Google Drive`, open it.
2. Sign in with **fatima@bamboraco.com**.
3. Open **File Explorer** (the yellow folder icon). On the left you should now see a drive called **Google Drive (G:)** with **My Drive** and **Shared drives** inside. That is how Claude uploads approved videos.

## Step 6b. Stop the PC from sleeping during your shift

A sleeping PC means missed sweeps (Claude, Chrome and the timers all freeze). Claude starts a keep-awake helper every shift, but set these once too:

1. **Start** > **Settings** > **System** > **Power & battery** (Windows 11) or **Power & sleep** (Windows 10). Under **Screen and sleep**, set **"When plugged in, put my device to sleep after"** to **Never**.
2. **Laptop:** Start, type `Control Panel`, open **Hardware and Sound** > **Power Options** > **Choose what closing the lid does**. Under **Plugged in**, set **When I close the lid** to **Do nothing**. Click **Save changes**.
3. Keep the charger in during your shift.

(Why and how it all works: `docs/09-background-machinery.md`.)

## Step 7. Open Claude Code in the Bombara folder

1. Click **Start**, type `Claude`, open the **Claude** app, and sign in.
2. Click the **Code** tab at the top.
3. When it asks for a folder, choose `C:\Users\<you>\Bombara` (it was created by the installer). Always open this same folder: Claude's memory is tied to it.
4. If Claude asks whether to **trust this folder** or **allow the project's MCP server "trybe"**, say **yes** (that is the Trybe tool that lives in this folder).
5. Connect the tools Claude uses. In the Claude app go to **Settings**, then **Connectors**, and connect (sign in with the Bambora account where asked):
   - **Google Drive**
   - **Notion**
   - **Claude in Chrome** (so Claude can use the Chrome you signed in above)
   - **Atria** (the ad library): **Add custom connector**, URL `https://api.tryatria.com/mcp`, then sign in
   - The **Claude Docs** connector, if it is not already there (the Creator Tracker lives in it)

## Step 8. Paste the first prompt

Open the file `C:\Users\<you>\claude-setup\FIRST-PROMPT.md` (right-click, **Open with**, **Notepad**), copy everything in the grey box, paste it into Claude, and press Enter.

Claude reads everything, checks the install, fixes small gaps, asks you a few setup questions (your name, hours, timezone for `OPERATOR.md`), and ends by saying **ready**.

## Step 9. Every work day

In the Claude app, Code tab, folder `Bombara`, type:

```
start the routines
```

Before you type it, make sure Fatima is not running the routine on her Mac right now (one computer at a time, see the box at the top).

That is the whole daily start. Claude starts its 30-minute sweep, works through chat, samples, partnership ads, video submissions, new applicants and follow-ups, and sends you ONE message per sweep: what it did, what needs your yes (each with a recommendation), and real questions only. Keep the Claude app and Chrome open and the PC awake (lid open, charger in) during your work hours.

At the end of your day Claude writes the session log and pushes everything to GitHub by itself.

---

## Where to read more

| File | What it is |
|---|---|
| `docs/README.md` | Start here: ownership, and the index of the manual |
| `docs/FIRST-DAY.md` | Your first day, hour by hour |
| `docs/01-how-the-job-works.md` | The daily loop and the six streams |
| `docs/02-rules.md` | Every rule (safety, messages, samples, applicants, who to ignore) |
| `docs/GLOSSARY.md` | Every word you will hear (yapper, V3, sample gate, Liam links...) |
| `docs/10-shift-checklists.md` | Start-of-shift and end-of-shift checklists, and what runs when |
| `docs/09-background-machinery.md` | The invisible pieces (keep-awake, timers, watchdog, helper server) explained |
| `docs/08-troubleshooting.md` | When something breaks, by symptom |
| `HANDOVER-BUILD-REPORT.md` | How this repo was built from Fatima's Mac setup, and what is still open |
