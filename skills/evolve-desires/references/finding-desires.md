# Where desires are actually found

`voc-miner` covers Reddit and YouTube, which is the bulk of the work. This file
covers the rest of the landscape and how to read what comes back.

---

## Reddit protocol

Beyond the standard `discover` → `search` flow, three query shapes surface
complaint language that a plain category search misses:

- `"[category] sucks"` — unfiltered frustration, no brand loyalty performance
- `"[problem] solution"` — people mid-search, describing what they want in
  their own words before any brand has framed it for them
- `"anyone else [problem]"` — the phrasing of a desire someone thinks is theirs
  alone. Almost always the most emotionally vivid material in the corpus.

Prioritise upvoted complaints with heavy comment counts. The comments matter
more than the post: the post is one person's problem, the comments are the
market confirming it in a dozen different phrasings.

---

## Review mining

Search **negative reviews** in the category, not just the brand's own.

The highest-value pattern is **"I love this BUT…"**. The clause after the "but"
is a desire the customer holds strongly enough to complain about a product they
otherwise like — which means it survived their own goodwill. That's a stronger
signal than a one-star rant, which is often about shipping or a defective unit.

Also look for:

- Repeated frustrations that appear across *different* brands. A complaint that
  recurs regardless of who made the product is a Mass Technological Problem, and
  a category-wide opening.
- Seasonal complaint patterns — the same frustration spiking at the same time
  each year points to a Force of Change worth timing creative against.

**Amazon specifically:** the Q&A section outperforms reviews for this purpose.
A question is a desire that hasn't been satisfied yet, phrased as a request.
Reviews are post-purchase; questions are pre-purchase, which is the mindset the
ad has to meet.

---

## Google Trends as a rising-desire signal

Trends won't give you language, but it will tell you which desires are growing.
Four indicators that a desire is on the way up:

- Search volume up 50%+ year over year
- Related queries shifting from *"what is"* to *"how to get"* — the move from
  curiosity to intent
- Geographic spread outward from urban centres
- Growth sustained across seasons rather than spiking and collapsing

The second one is the most useful and the least used. A term whose related
queries are still "what is" is education-stage; the desire exists but isn't
purchasable yet.

---

## The rest of the landscape

| Platform | What it's good for |
|---|---|
| **YouTube** | Comment patterns, creator pain points, engagement signals — covered by voc-miner |
| **Amazon** | Q&A mining, review analysis, wishlist trends |
| **Facebook groups** | Discussion threads, marketplace needs, social proof validation |
| **TikTok** | Emerging desires, comment-to-view ratio, cultural shift detection |
| **Quora / Stack-style Q&A** | Common questions and frustrations, stated plainly |
| **Answer The Public** | Question clustering, search-intent evolution |
| **Scientific studies and blogs** | Evidence-based validation, expert predictions |

Cross-platform validation is the quality bar: a desire that appears on one
platform is a platform artifact. A desire that appears on three, in different
words each time, is a market.

---

## Customer interviews

When live customers are available, these five questions excavate deeper than a
survey does:

1. "What keeps you up at night about [problem area]?"
2. "When you imagine the perfect solution, what would your life look like?"
3. "What have you tried before that disappointed you?"
4. "If money wasn't an issue, what would you do about this?"
5. "When friends complain about [problem], what do they say exactly?"

Question 5 does something the others can't: it routes around self-presentation.
People describe their friends' frustrations more honestly than their own,
because there's no admission of weakness in it. It reliably returns the most
usable verbatim language of the five.

### What to listen for

- **Emotional words** — frustrated, excited, worried, proud, embarrassed
- **Extreme language** — always, never, hate, love. Extremity marks intensity,
  and intensity is Urgency in the power ranking.
- **Time pressure** — finally, immediately, constantly
- **Social proof references** — "everyone's doing," "nobody has"

---

## Red flags — signals that waste time

**Complaints about price alone.** Price objections are almost never a desire.
They're a value-communication failure, and they'll pollute a power ranking with
something no angle can fix.

**Logistics and fulfilment complaints.** Shipping speed, customs, packaging,
wrong address. Structurally expected for any dropshipping brand and never a
creative-strategy finding. For Flown this is an explicit brand rule — filter
them out entirely.

**Single-voice intensity.** One extremely articulate, extremely angry customer
can generate enough vivid language to look like a pattern. Check that a desire
appears across several distinct accounts before ranking it.

**Brand-loyalist praise.** Glowing reviews from existing advocates describe
satisfaction, not desire. Desire lives in the gap, so it concentrates in the
unsatisfied and the not-yet-bought.

---

## Quality bar

The research is good enough to write from when:

- Every desire in the ranking carries at least one exact quote and a link
- The top three desires each appear across more than one platform
- At least one desire found was **not** on the brand's existing angle list —
  if everything you found confirms what's already running, the mining was too
  narrow, not the market too small
- Shipping, price, and defect complaints have been excluded rather than ranked
- The language in the document is the customer's, not yours
