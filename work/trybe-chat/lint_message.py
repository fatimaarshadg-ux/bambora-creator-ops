#!/usr/bin/env python3
"""Block robotic creator messages (skill: human-messages). Exit 1 if any problem is found.
Usage:  lint_message.py "message text" | draft.txt | --file drafts.json ({name: text})   [--long for inspo packs]
"""
import json, re, sys
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding='utf-8')  # emoji and names print on Windows consoles
except Exception:
    pass

BANNED = [
    "quick favor", "quick favour", "just wanted to", "just a quick", "hope this message finds you",
    "hope this finds you", "reaching out", "i wanted to let you know", "touching base", "circling back",
    "per my last", "as per", "kindly", "please be advised", "don't hesitate to", "do not hesitate to",
    "feel free to reach out", "at your earliest convenience", "i hope this helps", "exciting opportunity",
    "valued creator", "we appreciate your", "rest assured", "in order to", "leverage", "moving forward,",
    "going forward,", "i hope you're doing well", "i hope you are doing well", "dear ",
    # AI comfort-template phrases (Jen Smith, 2026-09-23: "this is shit")
    "don't stress", "honestly,", "which says a lot", "that says a lot", "in no time", "only because we",
    "good question!", "great question", "totally normal", "completely normal", "you've got this covered",
    "have it down", "get the hang of it in no time", "the more you film", "so close",
    # Q&A 2026-09-24
    "no rush", "following up again", "just following up", "today please", "on board", "so much content",
]
MAX_REPLY = 220  # a chat reply longer than this reads like a letter; inspo packs pass --long
# Fatima speaks as ONE person (2026-09-24, 'yayy us too' to Chris and Alicia): feelings, plans and actions are I/me, never we/us.
WE_BANNED = ["strict rule", 'us too', 'we too', 'me and the team', "we're so", 'we are so', "we can't wait", 'we cant wait', 'we love', "we'd love", "we're excited", 'we are excited', 'on our side', 'on our end', 'our team', "we'll", 'we will', "we're", 'we are ', 'all of us', 'both of us']
DASHES = re.compile("|".join([chr(0x2014), chr(0x2013), " " + chr(45) + " ", chr(45) * 2]))  # em dash, en dash, spaced hyphen, double hyphen

def problems(text, long_ok=False):
    t = text.lower()
    out = [f'banned phrase: "{b}"' for b in BANNED if b in t]
    out += [f'we/us voice: "{b}" (Fatima is one person, say I/me)' for b in WE_BANNED if b in t]
    if not long_ok and len(re.sub(r"https?://\S+", "", text)) > MAX_REPLY:
        out.append(f"too long for a chat reply ({len(text)} chars, max {MAX_REPLY}); say one thing, like a text")
    for line in text.splitlines():
        if DASHES.search(re.sub(r"https?://\S+", "", line)):
            out.append(f"dash in: {line[:60]}")
    return out

def main():
    import os
    args = sys.argv[1:]
    long_ok = "--long" in args
    args = [a for a in args if a != "--long"]
    if len(args) > 1 and args[0] == "--file":
        items = json.load(open(args[1], encoding='utf-8'))
    elif len(args) == 1 and os.path.isfile(args[0]):
        # a path to a plain-text draft: lint its CONTENTS (bug found 2026-09-23: the path itself was linted)
        items = {"message": open(args[0], encoding='utf-8').read()}
    else:
        items = {"message": " ".join(args)}
    bad = 0
    for name, text in items.items():
        p = problems(text, long_ok)
        if p:
            bad += 1
            print(f"REWRITE {name}: " + "; ".join(p))
    print("ok" if not bad else f"{bad} message(s) need rewriting")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
