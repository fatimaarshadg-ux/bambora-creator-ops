#!/usr/bin/env python3
"""Find quiet creators and put them in the follow-up ledger (Fatima's rule, 2026-09-23).

A creator is quiet when their last video is more than 14 days old and they joined at least
14 days ago. Every quiet creator gets a `quiet_checkin` item in followups.json, due today,
unless one of these is true:
  - they're dropped (retainer askers from the 5% migration)
  - they already have an open quiet_checkin or inspo_checkin (someone is already on it)
  - they have an open reply_owed (answer that first; ideas on top of an unanswered
    question read badly)

The check-in itself (updated 2026-09-24): first message only notices the gap, asks how they are and offers ideas; after they reply, send
her point that creators posting 20 to 30 videos a month do best, plus 3 or 4 inspo picks
that fit them (from the pack's tags.tsv), the "just inspo, make it your own" line and the
checklist P.S. For this run every message goes to Fatima first.

Run after build_db.py:  py -3 ~/claude-setup/work/creator-db/quiet_creators.py
"""
import datetime as dt
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding='utf-8')  # emoji and names print on Windows consoles
except Exception:
    pass
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "db", "creators.json")
LEDGER = os.path.join(HERE, "followups.json")
DROPPED = {"kia layton", "krystal camacho", "andrew pagliara", "tasha clay", "madison grove", "emily seitz", "madison tanefski"}  # retainer askers: ignore (Fatima, 2026-09-23)
QUIET_DAYS = 14


def main():
    today = dt.date.today()
    creators = json.load(open(DB, encoding='utf-8'))
    creators = creators if isinstance(creators, list) else list(creators.values())
    ledger = json.load(open(LEDGER, encoding='utf-8')) if os.path.exists(LEDGER) else []
    open_items = {}
    for i in ledger:
        if i["status"] == "open":
            open_items.setdefault(i["creator"].lower(), set()).add(i["type"])

    added, skipped = [], []
    for c in creators:
        name = c["name"]
        key = name.lower()
        perf = c.get("performance") or {}
        last = ((perf.get("activity") or {}).get("last_submission_at") or "")[:10]
        joined = (((perf.get("creator") or {}).get("joined_at")) or c.get("joined_at") or "")[:10]
        if not last or not joined:
            continue
        days = (today - dt.date.fromisoformat(last)).days
        tenure = (today - dt.date.fromisoformat(joined)).days
        if days <= QUIET_DAYS or tenure < QUIET_DAYS:
            continue
        if key in DROPPED:
            continue
        types = open_items.get(key, set())
        if types & {"quiet_checkin", "inspo_checkin"}:
            skipped.append(f"{name} (already has {', '.join(sorted(types))})")
            continue
        if "reply_owed" in types:
            skipped.append(f"{name} (reply owed first)")
            continue
        gmv = ((perf.get("performance") or {}).get("trybe_gmv_cents") or 0) / 100
        note = (f"no video for {days} days (last {last}), GMV ${gmv:.0f}, group {c.get('group')}; "
                "check-in with the 20 to 30 videos a month point plus fitting inspo")
        subprocess.run([sys.executable, os.path.join(HERE, "followups.py"), "add", name,
                        "quiet_checkin", today.isoformat(), note], check=True, capture_output=True)
        added.append(f"{name}: {days} days, ${gmv:.0f}")

    print(f"quiet check-ins added: {len(added)}")
    for a in added:
        print("  +", a)
    if skipped:
        print(f"skipped: {len(skipped)}")
        for s in skipped:
            print("  -", s)


if __name__ == "__main__":
    main()
