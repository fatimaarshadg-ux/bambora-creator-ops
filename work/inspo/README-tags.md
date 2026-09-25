# Inspo pack tags

## How to use

Every inspo pack folder (`work/inspo/YYYY-MM-DD/`) has a `tags.tsv`. It has one row per item in the pack, is tab separated and starts with a header row. Its job is to let drafts be matched to creators automatically. For example, a pregnant creator only gets rows where `fits_no_baby_creators` is `yes`, and a creator who can't lead with a sale skips rows where `sale_led` is `yes`.

Columns:

| column | values | meaning |
|---|---|---|
| `num` | `01`..`56` for Atria, `yt01`, `ts01`, `tt01`, `ig01`... for social | Atria items use the pack number from `order.txt`. Social items are numbered in file order: YouTube (`ytpicks.txt`), then TikTok Shop (`ttshop.tsv`), then TikTok (`tt.tsv`), then Instagram (`ig.tsv`). Duplicate URLs are dropped. |
| `source` | `atria`, `youtube`, `tiktok`, `tiktokshop`, `instagram` | Where the item came from. |
| `brand_or_creator` | text | The advertiser for Atria (with the real product brand in brackets when the ad page differs, e.g. `Cosmetic Times (Smooche)`), or the channel or handle for social. |
| `link` | URL | Atria: the Drive copy, `https://drive.google.com/file/d/<id>/view`, with the id from `driveids.txt`. Social: the public post URL. |
| `hook` | one line | The opening line or on-screen hook, lightly cleaned up. Brackets hold a short note on what's on screen. |
| `baby_in_shot` | `yes`, `no`, `unclear` | Does a baby or toddler appear anywhere in the video? Older kids (school age) count as `no`. |
| `who_on_camera` | `mom`, `dad`, `grandparent`, `pregnant`, `expert/professional`, `kids only`, `none` | The main person on screen. When there are several people they are joined with `+`, main person first (`grandparent+mom`), so split on `+` when matching. `mom`, `dad` and `grandparent` also stand for an adult woman, adult man or older adult in non parenting ads. `none` means hands only or no person. `pregnant` means a visible bump, or a caption that says so. |
| `baby_age` | `newborn`, `infant`, `toddler`, `none`, `unclear` | The youngest baby seen: newborn is about 0 to 2 months, infant is up to about 12 months and not walking, toddler is walking. It is `none` exactly when `baby_in_shot` is `no`. |
| `format` | `talking head`, `review/tester`, `rating out of 10`, `POV text`, `skit`, `montage`, `list/must-haves`, `comment reply`, `routine/day in the life`, `comparison`, `other` | The format a creator would copy. Try ons count as `review/tester`. Hack compilations count as `montage`. Single hack demos and tutorials count as `other`. |
| `sale_led` | `yes`, `no` | `yes` when the video itself pushes a discount, code, buy one get one, "on sale" or price deal anywhere: in the hook, an overlay, a caption, a spoken line shown in subtitles, or an end card. A deal that only appears in the Atria headline and not in the video counts as `no`. |
| `fits_no_baby_creators` | `yes`, `no` | `yes` when the format can be filmed by a creator with no wearable baby. That covers a pregnant creator, or one whose newborn is still under 10 lbs and can't go in the sling. Newborn only content that doesn't need babywearing counts as `yes`. Anything that needs a baby or toddler worn, held for a demo or starring in the video counts as `no`. |

Example (Python) to pick drafts for a pregnant creator who can't run sales:

```python
import csv
rows = list(csv.DictReader(open('tags.tsv'), delimiter='\t'))
picks = [r for r in rows if r['fits_no_baby_creators'] == 'yes' and r['sale_led'] == 'no']
```

## Every pack run must produce tags.tsv

Every future inspo pack run must write `tags.tsv` into its dated folder, with the same columns in the same order and the same values as above, before any creator drafts are written. Tag it the way the 2026-09-23 pack was tagged:

1. **Atria items: judge from real frames, never from the title.** For each mp4 URL in `details.tsv`, make a new empty folder `tagframes/<num>/` in the session scratchpad. Never reuse a folder, because a reused folder once shifted every label by one. Grab frames at about 2s, 6s and the midpoint (`ffmpeg -ss 2 -i <url> -frames:v 1 -vf scale=360:-1 out.jpg`). Also grab 25%, 75% and the last 1.5s, which catch babies that only show up later and sale end cards. Stamp the item number onto each contact sheet (Pillow, because Homebrew ffmpeg has no drawtext) and read every sheet.
2. **Check the Drive links.** List the pack's Drive folder and confirm that every id in `driveids.txt` belongs to the file whose title starts with the same number.
3. **Social items:** start from the title or caption (`yt-dlp --skip-download --write-info-json --write-thumbnail`). Always pass `--socket-timeout 15`, or TikTok calls can hang forever. When the caption doesn't settle baby, person or age, look at frames. For TikTok and Instagram, download the lowest quality file to scratch, take 4 frames, then delete the file. For YouTube Shorts, get a video only stream URL with `yt-dlp -g -f "bv*[height<=480]"` and run ffmpeg on it. If yt-dlp says a Short is "not available", fall back to the oEmbed title and `https://i.ytimg.com/vi/<id>/hqdefault.jpg`.
4. **Validate before saving:** every value must be in the lists above, `baby_age` must be `none` exactly when `baby_in_shot` is `no`, and there must be no tabs or dashes in the text fields. Mark anything you can't see as `unclear`, not as a guess, and list those items in the run notes.

- `format=reaction_source`: a popular clingy or Velcro baby complaint video that creators with no baby in range can react to or stitch, then pitch the sling as a story (added 2026-09-23).
