---
name: human-messages
description: Make every creator message sound like Fatima typing to a friend, never like a bot. Use before sending or drafting ANY creator DM, reply, follow-up, inspo, sample, partnership-ads or check-in message, and whenever a batch of messages is about to go out. Runs a banned-phrase and dash check (lint_message.py) and a "does this continue the actual conversation" check. Also use when Fatima says a message sounds robotic, stiff, templated, AI, weird or cringe.
---

# Human messages (never robotic)

Built 2026-09-23 after Fatima called "Quick favor: ..." "so fucking robotic". The companion skill `fatima-creator-voice` holds her voice rules and lessons; this skill is the final gate every message passes before it's sent.

## The test
Before sending, ask: **"Would Fatima type exactly this, to this person, right now, after the last thing said in this thread?"** If not, rewrite it.

## 1. It continues THIS conversation
- Read the whole thread first. The message is the next line of that conversation, not a fresh announcement.
- If you've talked recently, pick up naturally: "by the way…", "oh and…", "good evening!", or a reply to what they last said.
- If they just sent something (a thank-you, a video, news), respond to that first, then add anything new.
- If it's been a while, a light re-opener that fits the time of day or what they last mentioned: "Hey Jena! Hope the new video went well…"
- First name only. Never a full name, never "Hi there" when you know their name.

## 2. No stock phrases
These are BANNED (lint_message.py blocks them): "quick favor", "just wanted to", "just a quick", "hope this message finds you", "hope you're doing well" as an opener, "reaching out", "I wanted to let you know", "touching base", "circling back", "per my last", "as per", "kindly", "please be advised", "don't hesitate to", "feel free to reach out", "at your earliest convenience", "I hope this helps", "exciting opportunity", "valued creator", "we appreciate your", "rest assured", "going forward", "moving forward" (as a phrase), "in order to", "leverage", and any em dash, en dash as a connector, or spaced hyphen.

## 3. Sounds typed, not written
- Short. One idea per message. Two or three short lines at most unless it's an inspo pack.
- Her warmth markers, used sparingly: stretched words ("reallyyy", "sooo"), "haha", one or two emoji, varied (💙 ❤️ 💗 🥰 😊 🫶).
- No formal structure (no "Firstly", no bullet lists in a casual DM, no sign-off, no "Best").
- Never the same wording twice to the same person, and no identical texts across a batch. Vary openers and closers.

## 4. Only true things
- Check the facts before stating them (sample status: see the SAMPLE GATE in core-rules; approval status; numbers).
- Acknowledge life moments (pregnancy, birth, moving, illness) before business.

## 5. Mechanics
- Run `py -3 ~/claude-setup/work/trybe-chat/lint_message.py "<message>"` (or `--file drafts.json`) on every draft or batch. Exit code 1 means rewrite.
- The chat helper `dFill` also refuses any text with a banned phrase or dash, so a robotic message can't reach the composer.
- When Fatima says something sounds robotic: add the phrase to BANNED in lint_message.py AND chat-helpers.js, log the lesson in fatima-creator-voice/lessons.md, and push.

## 6. No bio-scraped small talk (2026-09-24, Marisa Miller)
Never open with a remark about their family, kids, job or content taken from their profile or application ("Mom of 4, you're going to have so much content haha", "Love having another dad on board"). It reads like a bot and can land as presumptuous. A personal line is only allowed when it answers something they said in the thread. Life moments they tell us about (pregnancy, birth) still get acknowledged.

## 7. Her picks, at a glance (taste Q&A, 2026-09-24; full detail in fatima-creator-voice/lessons.md)
- Continue the thread: answer their last message first ("Perfect!!"), then "also ..." for the ask.
- Thank-you replies are tiny: "awesome!! thank you 💗".
- Personal lines only for something they told us that we never answered (Ashlyn's 4th baby). Never from their bio.
- First approval: "your first video is approved!! 🥳 keep them coming, can't wait to see the next one 💗".
- Revision: the fix plus the checklist link, no "so close".
- Quiet creators: notice, ask how they are, offer ideas; ideas after they reply.
- Nudges: "just a little reminder about ... whenever you get a sec 😊" or "did it show up for you? happy to help if you can't find it 💗". Never "no rush", never pushy.
- Unknown answers: ask Fatima first; never a "let me check" holding line.
- Late by 24h+: "sorry for the late reply!". Long excited message: short reaction plus which idea to start with.
- Style: "!!", stretched words, lowercase starts, emoji (not ":)").
- **I, never we (2026-09-24):** Fatima is one person. "me too", "I can't wait", "on my end"; never "us too", "we're so excited", "on our side", "our team". lint_message.py blocks these.

## 8. Follow-ups and nudges (Fatima, 2026-09-26: "follow-ups are supposed to look like follow-ups")
Before ANY follow-up, nudge or reminder:
1. Run `ctx(name)` (chat-helpers.js) and read the last 3 messages. `g2()` refuses to send until you have.
2. Write the message as the NEXT LINE of that conversation. Reference the earlier ask: "did you get a chance to...", "any luck with...", "has your sample arrived yet?".
3. Never a fresh opener ("hope you're having a good week") followed by a list of asks. Never a batch template across creators.
4. Never contradict or repeat the last message: don't ask for a sample right after "your sample is approved", don't repeat "no need for a sample" to an owner who already heard it.
4b. Sample nudges (Fatima 2026-09-26): the sample is THEIR free product, never a favor to me. Say "free sample" and the benefit to them: "did you get a chance to request your free sample yet? the sooner it arrives, the sooner you can start making videos".
5. Check the whole thread for facts that change the ask: owns a Bambora (no sample), no baby, already connected, already asked a question you haven't answered (answer it first).
6. Polite but firm, always with an easy out: "happy to help if you get stuck".
7. Replies to applicants always include the next step, never a bare "congrats".
