---
name: media-watcher-installed
description: claude-media-watcher (video frames + Whisper transcript tool) is installed on this PC at ~/claude-media-watcher with its own Python, ffmpeg and yt-dlp; how to run and update it
metadata:
  type: project
---

Installed by `install.ps1` from the copy in `~/claude-setup/tools/claude-media-watcher` (same code as the public repo https://github.com/fatimaarshadg-ux/claude-media-watcher, commit 0216b35).

- Everything lives in `~/claude-media-watcher`: static ffmpeg and ffprobe plus yt-dlp in `bin\`, a private Python 3.12 in `.venv` with faster-whisper and Pillow, and the Whisper `small` model cached under `~/.cache/huggingface`.
- **Run it** from Git Bash (Claude's shell): `~/claude-media-watcher/watch "<file or link>"`. From PowerShell: `& "$env:USERPROFILE\claude-media-watcher\watch.cmd" "<file or link>"`. Links (TikTok, Instagram, YouTube, Loom) work directly.
- Output: `report.md` first (metadata, transcript, silence map), then every `sheets/sheetNNN.jpg`, then single frames where needed. `--every 0.5` for fine detail, `--zoom 12.5 --crop x,y,w,h` for small text.
- Skill: `~/.claude/skills/media-watcher/SKILL.md` (the Bambora version from this repo, with the Trybe submission note).
- **Update:** rerun `powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\claude-setup\tools\claude-media-watcher\install.ps1"`, then reinstall the Bambora skill copy by rerunning `install.ps1` from the repo (the tool's own installer writes a generic skill).
- For a Trybe submission, fetch a fresh signed `asset.url` from the Brand API first; it expires in about 20 minutes.

**Why:** Claude Code has no other way to watch creator videos. Submission reviews, applicant reviews and inspo research all depend on it. Related: [[bambora-trybe-submission-review]], [[trybe-brand-api]], [[tiktok-no-browser-tool]].

History: built on Fatima's Mac and PC (2026-09-22), made public and installable on bare machines on 2026-09-25. The Windows installer was parsed and its helper tested in PowerShell 7 on the Mac, but the first real Windows run is this PC's install.
