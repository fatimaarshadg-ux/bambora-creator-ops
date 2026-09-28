# First message to every new applicant (Fatima approved 2026-09-26)
Send from Discovery (profile > Open chat) to every NEW applicant whose card shows "5% commission" (V3 or Grandparents), before any accept. Only accept after they answer. Then follow the standing rule (memory feedback-auto-accept-applicants and applicant-accept-reject-rule-0927): all yes + confident talking-to-camera + English-speaking country = accept without asking; anything conditional or borderline waits for a go.

hey {first}! thank you so much for applying, I'd love to have you 💗 I invest a lot in my creators (weekly inspo, feedback on every video, and putting real ad spend behind the ones that work), so before I accept, I want to make sure it's a good fit for you too:
1. do you have a baby or toddler (10 to 50 lbs) you could film with in the sling?
2. are you comfortable having them on camera? videos where baby's face shows tend to do best
3. my top creators usually post 3 to 5 videos a week, and that's where the commissions really add up. would that work for you?
no pressure at all, just let me know and I'll take it from there 🥰

Rules: skip anyone messaged in the last 48h; replies to applicants always include the next step (never a bare "congrats").

## Welcome note after accepting (Fatima's wording, 2026-09-26, Breanna)
Send as a REPLY IN THREAD on their answers message (not a standalone message), right after the accept, once the automated V3 welcome has landed (send with LONG_OK=true / lint --long):
hey {first}, love to hear that!! 💗 I've just accepted you into the program, so welcome in 🥳 the message above is just an automated welcome, no need to worry about that one 😊 to help you do 3 to 5 videos a week, I'll keep sharing weekly inspo with you that you can replicate or put your own spin on. my goal is to help you earn as many commissions as possible, so let's keep in touch! first step is requesting your free sample on Trybe, the sooner it arrives, the sooner you can start filming. I also sent you a partnership ads request to accept on Instagram whenever you get a sec. I'm really excited to work with you, I hope you're excited too 🥰
(Drop the partnership line if their roster cell shows "--" and ask them to connect Instagram instead. Grandparents mix-ups: say the welcome may show twice / they were moved to the right program.)

When they answer question 3, record it right away: `py -3 ~/claude-setup/work/creator-db/commitments.py add "<name>" --agreed "<what they agreed to>" --quote "<their exact words>" --verified`.
