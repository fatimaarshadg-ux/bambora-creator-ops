#!/usr/bin/env python3
"""Rank Bambora creators on non-sale-heavy ads.

Usage:  python3 rank.py [creative-classification.tsv]

Input TSV columns: rank, creator, sales, spend, verdict, evidence
Verdicts:
  CLEAN        - no sale/discount language anywhere in the video
  SALE-AT-END  - organic ad, sale named only in the closing seconds
  SALE-HEAVY   - sale carried through a substantial part of the ad
  SALE-LED     - the hook itself is the sale (Kia-style)
"""
import csv, sys, collections

PATH = sys.argv[1] if len(sys.argv) > 1 else 'creative-classification.tsv'
HEAVY = {'SALE-LED', 'SALE-HEAVY'}

clean, endm, heavy = collections.Counter(), collections.Counter(), collections.Counter()
for r in csv.DictReader(open(PATH), delimiter='\t'):
    s, v, c = float(r['sales']), r['verdict'].strip(), r['creator'].strip()
    (heavy if v in HEAVY else endm if v == 'SALE-AT-END' else clean)[c] += s

creators = set(clean) | set(endm) | set(heavy)
total = {c: clean[c] + endm[c] + heavy[c] for c in creators}

def table(title, counter, n=14):
    print(f"\n=== {title} ===")
    for i, (c, v) in enumerate(counter.most_common(n), 1):
        bits = []
        if endm[c] and counter is combo: bits.append(f"incl. ${endm[c]:,.0f} end-mention")
        if heavy[c]: bits.append(f"${heavy[c]:,.0f} sale-heavy excluded")
        note = '  (' + '; '.join(bits) + ')' if bits else ''
        print(f"{i:>2}. {c:<24} ${v:>9,.0f}{note}")

combo = collections.Counter({c: clean[c] + endm[c] for c in creators})
table("TOP CREATORS - non sale-heavy ads (end-mention allowed)", combo)
table("STRICT - any sale mention excluded", clean, 10)

print("\n=== SALE-HEAVY sales by creator ===")
for c, v in heavy.most_common():
    print(f"  {c:<24} ${v:>9,.0f}  = {v/total[c]*100:.0f}% of their classified sales")

cov = sum(total.values())
print(f"\nclassified: {cov:,.0f} across {len(creators)} creators"
      f"  ({cov/91900*100:.0f}% of $91,900 lifetime)")
