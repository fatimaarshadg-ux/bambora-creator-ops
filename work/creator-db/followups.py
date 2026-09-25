#!/usr/bin/env python3
"""Follow-up ledger for Bambora creators.

Every promise, check-in and nudge we owe a creator lives in followups.json next to
this script. The 2-hourly routine runs `due` and works through what it prints, so
nothing depends on anyone remembering.

Usage:
  followups.py due                      # open items due today or earlier
  followups.py list                     # every open item, soonest first
  followups.py add "<creator>" <type> <due YYYY-MM-DD|+Nd> "<note>"
  followups.py done "<creator>" <type> ["<outcome>"]
  followups.py snooze "<creator>" <type> <due YYYY-MM-DD|+Nd>

Types and their default timing (Fatima's rules, 2026-09-23):
  inspo_checkin      after inspo: +3d if they have the sling, +7d if not
  sample_checkin     about 14 days after a sample is approved
  sample_nudge       accepted, but no sample request after about 1 day
  applicant_followup our ask to an applicant, no reply after 1 working day
  promise            something Fatima said she would do (ideas, Discord, inspo)
  quiet_checkin      no submission for 14+ days
"""
import datetime as dt
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding='utf-8')  # emoji and names print on Windows consoles
except Exception:
    pass
import json
import os
import sys

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "followups.json")


def load():
    if not os.path.exists(PATH):
        return []
    with open(PATH, encoding='utf-8') as f:
        return json.load(f)


def save(items):
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)


def parse_due(s):
    today = dt.date.today()
    if s.startswith("+") and s.endswith("d"):
        return (today + dt.timedelta(days=int(s[1:-1]))).isoformat()
    dt.date.fromisoformat(s)
    return s


def show(items):
    for i in sorted(items, key=lambda x: x["due"]):
        print(f'{i["due"]}  {i["creator"]:<28} {i["type"]:<19} {i["note"]}')
    print(f"({len(items)} item(s))")


def find(items, creator, typ):
    return [i for i in items if i["status"] == "open" and i["creator"].lower() == creator.lower() and i["type"] == typ]


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    cmd, items = argv[1], load()
    today = dt.date.today().isoformat()
    if cmd == "due":
        show([i for i in items if i["status"] == "open" and i["due"] <= today])
    elif cmd == "list":
        show([i for i in items if i["status"] == "open"])
    elif cmd == "add":
        creator, typ, due, note = argv[2], argv[3], parse_due(argv[4]), argv[5]
        if find(items, creator, typ):
            print(f"already open: {creator} {typ} (use snooze to move it)")
            return 0
        items.append({"creator": creator, "type": typ, "due": due, "note": note,
                      "status": "open", "created": today})
        save(items)
        print(f"added {creator} {typ} due {due}")
    elif cmd == "done":
        creator, typ = argv[2], argv[3]
        hits = find(items, creator, typ)
        for i in hits:
            i["status"], i["closed"] = "done", today
            if len(argv) > 4:
                i["outcome"] = argv[4]
        save(items)
        print(f"closed {len(hits)}")
    elif cmd == "snooze":
        creator, typ, due = argv[2], argv[3], parse_due(argv[4])
        hits = find(items, creator, typ)
        for i in hits:
            i["due"] = due
        save(items)
        print(f"moved {len(hits)} to {due}")
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
