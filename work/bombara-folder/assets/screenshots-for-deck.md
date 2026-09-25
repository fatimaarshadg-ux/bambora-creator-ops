# Deck images

All four are now live in the deck. `build-deck.js` picks them up from this
folder by filename, so replacing a file and re-running `node build-deck.js`
re-renders the deck with the new image.

| File | Slide | Source |
|---|---|---|
| `haus-team.jpg` | 3 — Haus playbook | HAUS "Our Story" hero, gohaus.com/pages/about-us |
| `histrips-1.jpg` | 5 — Hi Strips playbook | Instagram, `xavi_b9` (8 Sep) |
| `histrips-2.jpg` | 5 — Hi Strips playbook | Instagram, `manuel_valero_` / Alfou Padel Club (8 Sep) |
| `trybe-top-creators.jpg` | 10 — The ten we keep | TRYBE, Creative Performance grouped by creator |
| `ugc-page.jpg` | 16 — Instagram feeds TRYBE | `@bamboraugc` profile, 2,930 followers |

Originals left untouched on the Desktop / in Downloads; these are copies,
downscaled to keep the .pptx small (deck is ~1MB).

## How each one is placed
- **Slide 3** — the HAUS shot is a 3:1 panorama, so it sits in a landscape
  frame on the right (3.8" x 2.85", centre-cropped) rather than a full-height
  column, which would have sliced it to a sliver. Crop keeps the HAUS
  wordmark, "Our Story" and the sponsor wall.
- **Slide 5** — both phone grabs are 738x1600, placed as two portrait frames
  at their native aspect, so nothing is cropped. Caption: "Creators at any
  scale, posting anyway."
- **Slide 10** — the leaderboard gets its own slide at 6" wide so the rows
  stay readable. Squeezing it beside the four-step plan made it unreadable.

## Charts (no image needed)
- **Slide 11** is a native PowerPoint bar chart built from the leaderboard
  numbers, not a picture — editable in PowerPoint. Hue `#2F6C9E`, a deeper step
  of the brand blue chosen because Bambora's own `#B7CCDF` reads as grey in a
  chart; it passes lightness, chroma and contrast checks.
- **Slide 14** has a proportion bar for the 25/75 male-female split, drawn as
  shapes with both ends labelled.

Note: `build-deck.js` repairs a bug in pptxgenjs that writes an extra axis ID
into the bar chart — PowerPoint can discard a chart that has it. Leave that
step in if you edit the script.

## Not used
Two more WhatsApp screenshots from the same batch are in `~/Downloads`
(`...09.17.36 (2).jpeg` and `(3).jpeg`) — not reviewed, not in the deck.
Say the word if they belong on slide 5 too.

## Note before this goes anywhere public
The HAUS photo is HAUS's own, and the Instagram grabs show real handles and
faces. Fine for an internal strategy deck; not for customer-facing or
published use.
