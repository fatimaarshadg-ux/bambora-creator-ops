---
name: feedback-never-mix-metric-scopes
description: Don't put metrics of different scope or different attribution source in the same table row. Fatima caught this in the Trybe non-sale creator ranking
metadata:
  type: feedback
---

When building a table where one column is a **filtered subset** (e.g. "sales from
non-sale ads only"), every other column in that row must be filtered the same way.
I shipped a top-10 table where "non-sale sales" was a computed subset but ROAS and
Spend were the creator's lifetime totals across all their creatives. Fatima spotted
it immediately: "how do these numbers make sense".

Two distinct errors, both worth checking for:

1. **Scope mismatch**: subset column next to whole-population columns. Cambria
   showed $18.9K spend (all 39 creatives) beside $15,670 sales (3 classified ones).
2. **Attribution mismatch**: ROAS was Meta purchase value ÷ spend; "sales" was
   Trybe-attributed GMV. Meta reports ~1.9x Trybe's figure ($171K vs $93K lifetime),
   so ROAS 1.79 appeared next to sales below spend and looked impossible. Trybe's
   own API docs say of these two figures: "never add the two."

**Why:** a reader assumes one row = one consistent measurement. Mixing scopes or
sources silently invents a contradiction, and it destroys trust in the whole table
even where the analysis underneath is sound.

**How to apply:** before presenting any table, state the scope of each column out
loud and confirm they match. If a column can't be computed at the same scope, either
omit it, or label it explicitly ("lifetime, all ads") rather than leaving it bare.
Name the attribution source whenever two exist. Related: [[trybe-api-capabilities]]
