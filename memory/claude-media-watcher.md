---
name: claude-media-watcher
description: "The tool that lets Claude watch videos and listen to audio (frames + contact sheets + local Whisper transcript); where it comes from and how the operator expects to use it"
metadata:
  type: reference
---

Built 2026-09-22 at Fatima's request. Public repo: https://github.com/fatimaarshadg-ux/claude-media-watcher (a copy is vendored in `~/claude-setup/tools/claude-media-watcher`). Installed on this PC at `~/claude-media-watcher`; see [[media-watcher-installed]] for how to run it.

**How it is used:** the operator (or Claude during a routine) drops an mp4 or any video, audio file or link into the chat and expects Claude to analyse it frame by frame and quote the audio, without being told which tool to run. The `media-watcher` skill covers that; load it whenever a media file shows up.

**Known platform facts:** ffmpeg drawtext crashes on Windows without an explicit font, so the script stamps timestamps with Pillow instead. Claude Cowork and cloud sessions cannot see this install; use the Claude Code tab on this PC.

This supersedes the hand-rolled ffmpeg recipe in [[bambora-trybe-submission-review]]. For Trybe reviews, fetch a fresh signed `asset.url` via [[trybe-brand-api]] and pass it straight to the tool.
