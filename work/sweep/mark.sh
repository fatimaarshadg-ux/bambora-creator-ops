#!/bin/bash
# Record that a sweep just finished (the watchdog reads this).
date +%s > "$HOME/claude-setup/work/sweep/last_sweep"
echo "sweep marked $(date '+%H:%M')"
