---
name: bambora-content-checklist
description: "Bambora's 6-point creator content checklist (right way vs wrong way) for reviewing UGC submissions"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 75f786eb-1c63-4035-b9ff-b5c8fb190005
  modified: 2026-09-18T01:28:07.065Z
---

Fatima's creator-facing checklist, published at https://bamborachecklist.netlify.app/ ("Bambora Content Checklist"), is the actual "correct way vs wrong way" standard for judging Trybe submissions (see [[trybe-brand-api]], [[bambora-trybe-submission-review]]). Six checks:

1. **Seat tucked securely under baby's bottom** (most important check). Position baby's bottom first, then drop them into the seat while still supporting them; spread fabric knee-to-knee so they're seated, not dangling. Babies: look for an "M" shape (knees higher than bottom). Toddlers: M is less critical but the seat-under-bottom still matters.
   - Right: seat right under the bottom, deep seat with M shape, knee-to-knee support.
   - Wrong: booty not tucked into the seat, baby hanging/not seated, legs cutting off with fabric bunched instead of spread.
2. **One hand supporting baby in every single frame**. Not most of the video, all of it. If a hand comes off even briefly, re-take that segment. Also: don't film while holding a hot drink. Cooking and stairs are fine as long as one hand stays on the baby (Fatima, 2026-09-26); never flag them.
3. **Buckle fully clicked with the safety loop in use**, closed properly over the clip. Common miss: buckle resting on top of the clip instead of closed over it, safety loop unused. Easy to miss in close-up shots.
4. **Baby close enough to kiss, face properly visible**: high on the chest, roughly two fingers' gap between chin and chest, face visible the whole time without moving fabric. Watch for the sling's top edge riding up, or a hood/scarf/blanket/coat slipping over the face.
5. **Filmed vertical 9:16, key text/face inside the 1:1 safe zone** (1080x1920, portrait, 1080p/4K). Send the original camera-roll file, not a re-download from TikTok/Instagram (quality loss). Keep text and face inside the middle square, because the top/bottom strips can get cropped.
6. **No watermarks anywhere**: no TikTok/Instagram watermark, no CapCut outro, no app logos, no username stamps, no trending stickers/burned-in auto-captions. Fix: export and save to camera roll, send that file directly rather than re-downloading a posted version.

**How to apply:** when reviewing a submission's video (frames via ffmpeg, transcript via Whisper or Trybe's own transcript field; see [[trybe-api-key-storage]]), check frames against all 6 visually, and flag violations by check number. This is Fatima's own standard for her creators, phrased gently ("never a criticism"), so mirror that tone if drafting feedback for a creator, but be direct/precise when reporting findings to Fatima herself.

**No sale-LED videos (Fatima, 2026-09-23, refined):** a brief mention near the END that a sale is on is FINE. Flag to Fatima, recommending revise or reject, only when a video is sale-led: it opens or hooks on the sale, the sale is the premise or reason ("had to order more while they're having their sale"), or it keeps coming back to it. Kia Layton's videos are the example of what NOT to do. How to check: search the transcript AND on-screen text (API `query=sale`/`deal`/`discount` matches on-screen text). If the first mention comes in the first half, or there are 2+ mentions, or the on-screen hook text is about the sale, treat it as sale-led. Videos with no speech need their on-screen text checked by frame.

**Background music (Fatima, 2026-09-24, answer to Jena Swapp):** not required in every video. It can help engagement on some videos, depending on context, but when the voiceover already has good energy it isn't needed. Answer creators with this directly.
