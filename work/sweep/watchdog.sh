#!/bin/bash
# Sweep watchdog (2026-09-23, per-stream check added 2026-09-24).
# Run in the background from the live Claude session. It exits, which wakes Claude, as soon as
# the last sweep is MAX minutes old OR any stream (chat, samples, partnership, submissions,
# discovery, ledger) hasn't run for STREAM_MAX minutes. Claude then runs routines/full-run.md,
# marks each stream with streams.sh done, runs mark.sh, and starts this watchdog again.
STAMP="$HOME/claude-setup/work/sweep/last_sweep"
MAX=${1:-30}
STREAM_MAX=${2:-60}
while true; do
  now=$(date +%s)
  last=$(cat "$STAMP" 2>/dev/null || echo 0)
  age=$(( (now - last) / 60 ))
  if [ "$age" -ge "$MAX" ]; then
    echo "SWEEP DUE: last sweep ${age} min ago. Run routines/full-run.md (ALL streams) now, then restart the watchdog."
    exit 0
  fi
  st=$(bash "$HOME/claude-setup/work/sweep/streams.sh" stale "$STREAM_MAX")
  if [ $? -ne 0 ]; then
    echo "$st (not run for ${STREAM_MAX}+ min). Run those streams now per routines/full-run.md, then restart the watchdog."
    exit 0
  fi
  sleep 60
done
