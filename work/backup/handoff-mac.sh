#!/usr/bin/env bash
# Shift handoff between Fatima's Mac (~/claude-setup, her own repo) and the operator's repo
# (fatimaarshadg-ux/bambora-creator-ops, cloned on the Mac at ~/bambora-creator-ops).
# This script runs on FATIMA'S MAC only. The operator's PC needs nothing: start.ps1 pulls and sync.ps1 pushes.
#
#   bash ~/bambora-creator-ops/work/backup/handoff-mac.sh take   # before Fatima starts a shift on her Mac
#   bash ~/bambora-creator-ops/work/backup/handoff-mac.sh give   # after Fatima ends that shift
#   bash ~/bambora-creator-ops/work/backup/handoff-mac.sh diff   # just show which state files differ
#
# take: pull the operator's repo, then copy the live state files (ledger, seen lists, filing records,
#       Liam records, session logs, applicant verdicts, creator database, voice lessons) INTO ~/claude-setup.
# give: copy the same files from ~/claude-setup back INTO the operator's repo, commit and push.
# Only the files listed in STATE are touched. Skills, memory and scripts are never copied, because the
# two repos hold Mac and Windows versions of those.
# One machine at a time: the operator must have stopped her sweeps (and run sync.ps1) before "take".
set -u
OPS="${OPS:-$HOME/bambora-creator-ops}"
MINE="${MINE:-$HOME/claude-setup}"
STATE=(
  work/creator-db/followups.json
  work/creator-db/db
  work/trybe-applicant-review/seen.txt
  work/trybe-drive-filing/filed.json
  work/trybe-drive-filing/liam-sent.json
  work/inspo/seen.txt
  skills/fatima-creator-voice/lessons.md
)
GLOBS=(
  'work/trybe-drive-filing/liam-links-*.md'
  'work/session-logs/*.md'
  'work/trybe-applicant-review/20*/*.md'
)

die() { echo "handoff: $*" >&2; exit 1; }
[ -d "$OPS/.git" ] || die "no clone at $OPS (git clone https://github.com/fatimaarshadg-ux/bambora-creator-ops.git \"$OPS\")"
[ -d "$MINE/.git" ] || die "no repo at $MINE"

copy_state() {  # copy_state FROM TO
  local from="$1" to="$2" p f rel
  for p in "${STATE[@]}"; do
    [ -e "$from/$p" ] || continue
    mkdir -p "$(dirname "$to/$p")"
    if [ -d "$from/$p" ]; then rsync -a "$from/$p/" "$to/$p/"; else cp -p "$from/$p" "$to/$p"; fi
  done
  for p in "${GLOBS[@]}"; do
    for f in $from/$p; do
      [ -f "$f" ] || continue
      rel="${f#$from/}"
      mkdir -p "$(dirname "$to/$rel")"
      cp -p "$f" "$to/$rel"
    done
  done
}

case "${1:-}" in
  take)
    git -C "$OPS" pull -q --rebase --autostash || die "pull of $OPS failed; sort it out first"
    echo "last change on the operator's side: $(git -C "$OPS" log -1 --format='%an, %ar: %s')"
    copy_state "$OPS" "$MINE"
    git -C "$MINE" status --short -- work skills | head -40
    echo "State copied into $MINE. Tell the operator you are on shift, then start your routine."
    ;;
  give)
    copy_state "$MINE" "$OPS"
    git -C "$OPS" add -A -- work skills/fatima-creator-voice/lessons.md
    if git -C "$OPS" diff --cached --quiet; then echo "nothing new to hand over"; exit 0; fi
    git -C "$OPS" commit -q -m "Handoff from Fatima's Mac shift" || die "commit failed"
    git -C "$OPS" pull -q --rebase --autostash || die "pull failed; nothing pushed"
    git -C "$OPS" push -q || die "push failed"
    echo "Handed over and pushed. Tell the operator she can start."
    ;;
  diff)
    for p in "${STATE[@]}"; do
      if [ -e "$OPS/$p" ] || [ -e "$MINE/$p" ]; then
        diff -rq "$OPS/$p" "$MINE/$p" >/dev/null 2>&1 && echo "same   $p" || echo "DIFFER $p"
      fi
    done
    ;;
  *) sed -n '2,15p' "$0"; exit 1 ;;
esac
