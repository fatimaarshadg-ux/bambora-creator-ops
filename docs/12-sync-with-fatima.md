# Staying in sync with Fatima (and taking turns)

This page settles one question: when you and Fatima both do this job, which copy of the work is the real one?

## The decision

- **This repo is the one live copy of the shift work** from handover day on: `fatimaarshadg-ux/bambora-creator-ops`, cloned on your PC at `C:\Users\<you>\claude-setup`. The follow-up ledger, the "already seen" lists, the Drive filing record, the Liam record, the session logs and the creator database all live here.
- **Fatima's own repo (`fatimaarshadg-ux/claude-setup`) stays hers.** It holds the Mac versions of the skills and scripts. It is not used on your PC, and you never push to it.
- **One machine at a time.** Only one computer runs "start the routines" at any moment. Whoever is on shift owns the ledger. Switching is a handoff, below.

Why this way: the two repos hold different versions of the same scripts (Mac and Windows), so merging them would break one side. Only the *data* needs to move between them, and a small script on Fatima's Mac does that (`work/backup/handoff-mac.sh`). Your PC needs nothing extra: `start.ps1` pulls at the start of every shift and `sync.ps1` pushes.

## The handoff, step by step

### You stop, Fatima takes over

1. Tell Claude: **"stop the sweep timer and the watchdog, then run sync.ps1"**. (At the normal end of your day the wrap-up does this for you.)
2. Wait for Claude to say **Pushed**.
3. Message Fatima: "I've stopped and pushed."
4. Fatima, on her Mac: `bash ~/bambora-creator-ops/work/backup/handoff-mac.sh take`, then "start the routines".

### Fatima stops, you take over

1. Fatima tells her Claude to stop the sweeps, then runs `bash ~/bambora-creator-ops/work/backup/handoff-mac.sh give` and messages you.
2. You: open Claude as usual and type **start the routines**. The first lines Claude sees include `last change on GitHub: Fatima, N minutes ago: Handoff from Fatima's Mac shift`. That is how you both know the handoff went through.
3. Claude reads the newest session logs from Fatima's shift (`work/session-logs/`) and saves any new rule into memory before the first sweep.

If Fatima says she is on shift and did not run `give`, **do not start**. Ask her to run it first. Starting without it means working from an old ledger.

## What moves in a handoff, and what does not

| Moves (data) | Does not move (each side keeps its own) |
|---|---|
| `work/creator-db/followups.json` (the ledger) | skills (Mac and Windows versions differ) |
| `work/creator-db/db/` (creator database) | memory files (paths differ) |
| `work/trybe-applicant-review/seen.txt` and the dated verdict notes | scripts |
| `work/trybe-drive-filing/filed.json`, `liam-sent.json`, `liam-links-*.md` | `CLAUDE.md`, settings |
| `work/inspo/seen.txt` | |
| `work/session-logs/*.md` | |
| `skills/fatima-creator-voice/lessons.md` (voice corrections) | |

**New rules travel through the session logs.** Every shift ends with a session log listing the rules that were set. Whoever starts the next shift has Claude read the newest logs and save anything new. Fatima can also say to her Claude: "read the operator's session log for <date> and save the new rules".

## One-time setup on Fatima's Mac

```bash
git clone https://github.com/fatimaarshadg-ux/bambora-creator-ops.git ~/bambora-creator-ops
bash ~/bambora-creator-ops/work/backup/handoff-mac.sh diff
```

`diff` changes nothing; it lists which data files differ between the two repos.

## If both machines ran at once anyway

1. Stop one right away (see `08-troubleshooting.md`, "Fatima's Mac and this PC both running").
2. Tell Claude: "merge Fatima's followups.json into ours: match items by creator plus type, keep an item closed if either side closed it, keep the later due date otherwise". Fatima runs `handoff-mac.sh diff` to see what differs.
3. Claude checks the last few hours of Trybe chat for double replies. A double message can be edited (Trybe: hover, Edit message); ask Fatima before deleting anything.
