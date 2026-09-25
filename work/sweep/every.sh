#!/bin/bash
# Timed extra checks that don't run every sweep (built 2026-09-25).
#   every.sh due metaaccess 300   -> prints DUE (exit 0) if 300+ min since last run, else "not due" (exit 1)
#   every.sh done metaaccess      -> record that it ran now
DIR="$HOME/claude-setup/work/sweep/every"; mkdir -p "$DIR"
case "$1" in
  due) l=$(cat "$DIR/$2" 2>/dev/null || echo 0); age=$(( ($(date +%s)-l)/60 )); if [ $age -ge "${3:-300}" ]; then echo "DUE: $2 ($age min since last)"; exit 0; fi; echo "not due: $2 ($age min)"; exit 1 ;;
  done) date +%s > "$DIR/$2"; echo "$2 done $(date '+%H:%M')" ;;
esac
