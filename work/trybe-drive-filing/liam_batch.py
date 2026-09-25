#!/usr/bin/env python3
"""Liam batches (Fatima, 2026-09-25): once 5 or more filed videos haven't gone to Liam yet,
give Fatima a ready-to-forward message for Liam.
  liam_batch.py status        count of unsent videos (exit 0 always)
  liam_batch.py message       print the forward-ready message if 5+ are unsent (prints nothing otherwise)
  liam_batch.py message --any print it for whatever is unsent (end of day, or when she asks)
  liam_batch.py sent          mark every currently unsent video as sent (run after she has the message)
Source of truth: every line in liam-links-*.md (file_approved filing appends there). Sent ids live in liam-sent.json."""
import glob, json, os, re, sys
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding='utf-8')  # emoji and names print on Windows consoles
except Exception:
    pass
HERE = os.path.dirname(os.path.abspath(__file__)); SENT = os.path.join(HERE, "liam-sent.json")
sent = set(json.load(open(SENT, encoding='utf-8'))) if os.path.exists(SENT) else set()
items = []
for f in sorted(glob.glob(os.path.join(HERE, "liam-links-*.md"))):
    for line in open(f, encoding="utf-8"):
        m = re.match(r"-\s*(.+?)\s*\(([0-9a-f]{8})\):\s*(\S+)", line.strip()) or re.match(r"-\s*(.+?),\s*([0-9a-f]{8}):\s*(\S+)", line.strip())
        if m and m.group(2) not in sent and m.group(2) not in [i[1] for i in items]:
            items.append((m.group(1), m.group(2), m.group(3)))
cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
if cmd == "status":
    print(f"{len(items)} unsent video(s) for Liam" + (" (READY: 5+, send Fatima the message)" if len(items) >= 5 else ""))
elif cmd == "message":
    if len(items) >= 5 or "--any" in sys.argv:
        n = len(items)
        print(f"hey Liam, here are {n} more videos you can add to Meta:")
        for name, tid, url in items: print(f"{name} ({tid}): {url}")
elif cmd == "sent":
    json.dump(sorted(sent | {i[1] for i in items}), open(SENT, "w", encoding="utf-8"), indent=0); print(f"marked {len(items)} as sent")
