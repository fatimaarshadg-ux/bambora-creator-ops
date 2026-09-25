#!/usr/bin/env python3
"""Bot forensics — archive every Genesis bot call with provenance, record what
was actually shipped, and mine the difference.

Portable: no project paths. Archive lives at $BOT_FORENSICS_HOME, or
~/.claude/bot-forensics by default, so it is shared across every project and
every Claude session on this machine.

  botlog.py call  <slug[@model]> <prompt-file>        run a bot AND archive it
  botlog.py ingest <slug[@model]> <prompt> <output>   archive a call already made
  botlog.py final <run-id> <final-file>               attach what actually shipped
  botlog.py verdict <run-id> "kept X, cut Y because"  record why
  botlog.py list                                      show the archive
  botlog.py report                                    what you consistently change
"""
import argparse, datetime, difflib, json, os, pathlib, re, subprocess, sys, collections

HOME = pathlib.Path(os.environ.get("BOT_FORENSICS_HOME",
                                   pathlib.Path.home() / ".claude/bot-forensics"))
ARCHIVE = HOME / "archive"


def find_genesis():
    """Locate genesis-stream.mjs without hardcoding any project path."""
    if os.environ.get("GENESIS_STREAM"):
        return os.environ["GENESIS_STREAM"]
    roots = [pathlib.Path.cwd(), pathlib.Path.home() / ".claude", pathlib.Path.home()]
    for r in roots:
        for depth in ("*/genesis-bots/scripts", "*/*/genesis-bots/scripts",
                      "*/*/*/genesis-bots/scripts", "*/*/*/*/genesis-bots/scripts"):
            for p in r.glob(f"{depth}/genesis-stream.mjs"):
                return str(p)
    return None


def new_run(slug):
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    name = re.sub(r"[^A-Za-z0-9_.-]", "-", slug.split("@")[0])[:40]
    d = ARCHIVE / f"{name}-{stamp}"
    # Several ingests can land in the same second; never let one clobber another.
    n = 2
    while d.exists():
        d = ARCHIVE / f"{name}-{stamp}-{n}"
        n += 1
    d.mkdir(parents=True)
    return d


def meta_write(d, **kw):
    p = d / "meta.json"
    m = json.loads(p.read_text()) if p.exists() else {}
    m.update(kw)
    p.write_text(json.dumps(m, indent=2))
    return m


def resolve(run_id):
    d = ARCHIVE / run_id
    if d.is_dir():
        return d
    hits = sorted(ARCHIVE.glob(f"*{run_id}*"))
    if len(hits) == 1:
        return hits[0]
    if not hits:
        sys.exit(f"no run matching '{run_id}'")
    sys.exit("ambiguous:\n  " + "\n  ".join(h.name for h in hits))


# ── words the bots overuse; counted, never auto-removed ──────────────
STOP = set("""the and that have this with what which they them their there here from
been were was are is be being had has for you your yours our we our not but so if then
than into onto about over under again too also very just really much more most some any
all when where who whom how why can could will would shall should may might must does
did doing done get got go going gonna okay yeah yes right now one two three thing things
way ways lot lots kind sort bit little because while during before after between through
against like said says say told tell know knew think thought want wanted need needed
make makes made take takes took come comes came look looks looked feel feels felt even
still back time times same other another each every own such only own down out off up
""".split())

TICS = ["unlock", "elevate", "game-changer", "in today's world", "delve", "realm",
        "testament", "navigate", "landscape", "tapestry", "embark", "moreover",
        "furthermore", "crucial", "vital", "robust", "seamless", "leverage",
        "empower", "transform", "revolutionary", "cutting-edge", "harness"]


def analyse(floor, final):
    fw, nw = floor.split(), final.split()
    sm = difflib.SequenceMatcher(None, fw, nw)
    kept = sum(b.size for b in sm.get_matching_blocks())
    removed, added = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("replace", "delete"):
            removed.append(" ".join(fw[i1:i2]))
        if tag in ("replace", "insert"):
            added.append(" ".join(nw[j1:j2]))
    return {
        "floor_words": len(fw), "final_words": len(nw),
        "survival_rate": round(kept / max(1, len(fw)), 3),
        "removed": [r for r in removed if r.strip()],
        "added": [a for a in added if a.strip()],
        "em_dashes_in_floor": floor.count("—"),
        "tics_in_floor": {t: floor.lower().count(t) for t in TICS if t in floor.lower()},
    }


def cmd_call(a):
    gs = find_genesis()
    if not gs:
        sys.exit("genesis-stream.mjs not found. Set GENESIS_STREAM=/path/to/genesis-stream.mjs")
    d = new_run(a.slug)
    prompt = pathlib.Path(a.prompt_file).read_text()
    (d / "prompt.md").write_text(prompt)
    out = d / "floor.md"
    cmd = ["node", gs, a.slug, str(d / "prompt.md"), str(out)]
    if a.temperature is not None:
        cmd.append(str(a.temperature))
    print(f"→ {' '.join(cmd[:3])} …", flush=True)
    r = subprocess.run(cmd)
    slug, _, model = a.slug.partition("@")
    meta_write(d, bot=slug, model=model or "(bot default)", source="bot",
               temperature=a.temperature, called=datetime.datetime.now().isoformat(),
               exit_code=r.returncode, prompt_words=len(prompt.split()))
    if out.exists():
        meta_write(d, floor_words=len(out.read_text().split()))
        print(f"archived {d.name}  ({len(out.read_text().split())} words)")
    else:
        print(f"archived {d.name} (no output produced — exit {r.returncode})")


PROBE_PROMPT = """Product: {product}

That is all the information you are being given. Proceed with your normal task.
"""


def cmd_probe(a):
    """Minimal-input call. Whatever comes back is mostly the bot's HIDDEN system
    prompt rather than our brief, which is as close to reading the recipe as we
    can get. Also the cheapest call available - tiny input."""
    gs = find_genesis()
    if not gs:
        sys.exit("genesis-stream.mjs not found. Set GENESIS_STREAM=/path/to/it")
    d = new_run(a.slug)
    prompt = PROBE_PROMPT.format(product=a.product)
    (d / "prompt.md").write_text(prompt)
    out = d / "floor.md"
    r = subprocess.run(["node", gs, a.slug, str(d / "prompt.md"), str(out)])
    slug, _, model = a.slug.partition("@")
    meta_write(d, bot=slug, model=model or "(bot default)", source="bot",
               probe=True, product=a.product, exit_code=r.returncode,
               called=datetime.datetime.now().isoformat(),
               prompt_words=len(prompt.split()))
    if out.exists():
        t = out.read_text()
        meta_write(d, floor_words=len(t.split()))
        print(f"probe archived {d.name} ({len(t.split())} words from "
              f"{len(prompt.split())} words of input)")
        print("Everything in that output beyond the product name came from the "
              "bot's hidden prompt.")
    else:
        print(f"probe failed (exit {r.returncode})")


def cmd_ingest(a):
    d = new_run(a.slug)
    prompt = pathlib.Path(a.prompt_file).read_text()
    floor = pathlib.Path(a.output_file).read_text()
    (d / "prompt.md").write_text(prompt)
    (d / "floor.md").write_text(floor)
    slug, _, model = a.slug.partition("@")
    meta_write(d, bot=slug, model=model or "(unrecorded)", ingested=True,
               source=a.source,
               called=datetime.datetime.now().isoformat(),
               prompt_words=len(prompt.split()), floor_words=len(floor.split()))
    print(f"archived {d.name}  ({len(floor.split())} words)")


def cmd_final(a):
    d = resolve(a.run_id)
    final = pathlib.Path(a.final_file).read_text()
    (d / "final.md").write_text(final)
    floor = (d / "floor.md")
    if not floor.exists():
        sys.exit(f"{d.name} has no floor.md to compare against")
    st = analyse(floor.read_text(), final)
    meta_write(d, **{k: v for k, v in st.items() if k not in ("removed", "added")})
    (d / "delta.json").write_text(json.dumps(st, indent=2))
    print(f"{d.name}: {st['survival_rate']*100:.0f}% of the floor survived "
          f"({st['floor_words']} → {st['final_words']} words)")


def cmd_verdict(a):
    d = resolve(a.run_id)
    with open(d / "verdict.md", "a") as f:
        f.write(f"\n## {datetime.datetime.now().isoformat(timespec='minutes')}\n\n{a.text}\n")
    print(f"verdict recorded on {d.name}")


def cmd_list(a):
    rows = sorted(ARCHIVE.glob("*/meta.json"))
    if not rows:
        print(f"archive empty ({ARCHIVE})")
        return
    print(f"{'run':<42} {'bot':<26} {'model':<20} floor  survived")
    for m in rows:
        d = json.loads(m.read_text())
        sr = d.get("survival_rate")
        tag = " [probe]" if d.get("probe") else ""
        print(f"{(m.parent.name + tag):<42} {str(d.get('bot'))[:25]:<26} "
              f"{str(d.get('model'))[:19]:<20} {str(d.get('floor_words','-')):<6} "
              f"{'' if sr is None else f'{sr*100:.0f}%'}")


def cmd_report(a):
    runs = [p.parent for p in ARCHIVE.glob("*/delta.json")]
    if not runs:
        print("No floor+final pairs yet. Attach shipped versions with:\n"
              "  botlog.py final <run-id> <file>")
        return
    tics, removed_terms, survival = collections.Counter(), collections.Counter(), []
    by_source = collections.defaultdict(list)
    em = 0
    for d in runs:
        st = json.loads((d / "delta.json").read_text())
        mj = d / "meta.json"
        src = (json.loads(mj.read_text()).get("source") or "bot") if mj.exists() else "bot"
        by_source[src].append(st["survival_rate"])
        survival.append(st["survival_rate"])
        em += st.get("em_dashes_in_floor", 0)
        for t, c in st.get("tics_in_floor", {}).items():
            tics[t] += c
        for chunk in st["removed"]:
            for w in re.findall(r"[a-z']{4,}", chunk.lower()):
                if w not in STOP:
                    removed_terms[w] += 1
    print(f"# Bot forensics — {len(runs)} floor/final pairs\n")
    print("## Survival by author\n")
    print("How much of each author's draft survived into what Fatima shipped.")
    print("This is the head-to-head. It only means something when both have "
          "several pairs.\n")
    for src in sorted(by_source):
        v = by_source[src]
        print(f"  {src:<8} {sum(v)/len(v)*100:5.0f}%   (n={len(v)})")
    if len([k for k in by_source if k in ("bot", "claude")]) < 2:
        print("\n  Only one author logged so far - no comparison possible yet.")
    print(f"\nEm-dashes in drafts (all banned): {em}\n")
    if tics:
        print("## Bot tics appearing in floors")
        for t, c in tics.most_common(20):
            print(f"  {t}: {c}")
    print("\n## Content words most often cut when editing")
    print("(stopwords filtered; a word here means the bot leaned on it and you did not)")
    shown = [(w, c) for w, c in removed_terms.most_common(40) if c > 1][:25]
    for w, c in shown:
        print(f"  {w}: {c}")
    if not shown:
        print("  nothing recurring yet - needs more pairs")
    print("\nEverything above is descriptive. Turn it into rubric rules only when "
          "Fatima confirms the pattern is real.")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("call"); c.add_argument("slug"); c.add_argument("prompt_file")
    c.add_argument("--temperature", type=float); c.set_defaults(fn=cmd_call)
    i = sub.add_parser("ingest"); i.add_argument("slug"); i.add_argument("prompt_file")
    i.add_argument("output_file")
    i.add_argument("--source", default="bot", choices=["bot", "claude", "gemini", "fatima"],
                   help="who produced this draft - the comparison depends on it")
    i.set_defaults(fn=cmd_ingest)
    f = sub.add_parser("final"); f.add_argument("run_id"); f.add_argument("final_file")
    f.set_defaults(fn=cmd_final)
    v = sub.add_parser("verdict"); v.add_argument("run_id"); v.add_argument("text")
    v.set_defaults(fn=cmd_verdict)
    pr = sub.add_parser("probe", help="minimal-input call to expose a bot's hidden prompt")
    pr.add_argument("slug"); pr.add_argument("product")
    pr.set_defaults(fn=cmd_probe)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    sub.add_parser("report").set_defaults(fn=cmd_report)
    a = ap.parse_args()
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    a.fn(a)


if __name__ == "__main__":
    main()
