#!/bin/bash
# Per-stream tracker (built 2026-09-24 after Discovery went unreviewed all night while chat sweeps ran).
# Every stream records when it last ran:  bash streams.sh done chat samples partnership submissions discovery ledger
# Show ages:                             bash streams.sh status
# Stale streams (older than N minutes):  bash streams.sh stale 60   (prints names, exit 1 if any)
DIR="$HOME/claude-setup/work/sweep/streams"; mkdir -p "$DIR"
ALL="chat samples partnership submissions discovery ledger"
cmd=$1; shift
case "$cmd" in
  done) for s in "$@"; do date +%s > "$DIR/$s"; done; echo "streams done: $* ($(date '+%H:%M'))" ;;
  status) now=$(date +%s); for s in $ALL; do l=$(cat "$DIR/$s" 2>/dev/null || echo 0); echo "$s: $(( (now-l)/60 )) min ago"; done ;;
  stale) max=${1:-60}; now=$(date +%s); out=""; for s in $ALL; do l=$(cat "$DIR/$s" 2>/dev/null || echo 0); [ $(( (now-l)/60 )) -ge "$max" ] && out="$out $s"; done; if [ -n "$out" ]; then echo "STALE:$out"; exit 1; fi; echo "all streams fresh" ;;
esac
