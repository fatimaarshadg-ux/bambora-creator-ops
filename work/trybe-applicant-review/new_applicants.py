#!/usr/bin/env python3
"""Print Inbox names that aren't in seen.txt (new applicants). Usage: new_applicants.py "Name A" "Name B" ...
Add them to seen.txt with --add once their review has started."""
import os, sys
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding='utf-8')  # emoji and names print on Windows consoles
except Exception:
    pass
HERE = os.path.dirname(os.path.abspath(__file__)); SEEN = os.path.join(HERE, "seen.txt")
seen = {l.strip().lower() for l in open(SEEN, encoding='utf-8') if l.strip() and not l.startswith("#")}
args = [a for a in sys.argv[1:] if a != "--add"]
new = [n for n in args if n.strip().lower() not in seen]
if "--add" in sys.argv and new:
    with open(SEEN, "a", encoding="utf-8") as f: f.write("".join(n + "\n" for n in new))
print("NEW: " + ", ".join(new) if new else "no new applicants")
