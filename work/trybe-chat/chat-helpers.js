// Trybe chat helpers for Claude in Chrome (built 2026-09-23).
// Load in the chat tab with:
//   eval(await fetch('http://127.0.0.1:8765/chat-helpers.js').then(r => r.text()))
// after serving this folder with cors_srv.py, or paste the file into javascript_tool.
// Every send is guarded: the right thread is open, the text isn't already there, the composer
// was empty, and nothing new has arrived from the creator since the draft was checked.

window.root = () => [...document.querySelectorAll('[role=dialog]')].find(d => /Chat\nBack|Conversations/.test(d.innerText)) || document.querySelector('main');
window._thread = () => { const t = root().innerText; const i = t.lastIndexOf('Back\n'); return i < 0 ? 'NO THREAD' : t.slice(i + 5); };
// Header may start with initials (no avatar photo); use the first line ending in "(DM)".
window.dThread = () => { const t = _thread(); if (t === 'NO THREAD') return t; const L = t.split('\n'); const k = L.findIndex(l => /\(DM\)\s*$/.test(l)); return k > 0 && k < 3 ? L.slice(k).join('\n') : t; };
window.goBack = () => { const b = [...root().querySelectorAll('button')].find(x => /^back$/i.test((x.innerText || x.getAttribute('aria-label') || '').trim())); if (!b) return 'no back'; b.focus(); return 'focused back'; };
window.focusSearch = () => { const i = root().querySelector('input[placeholder="Search Chat"]'); if (!i) return 'no search'; i.focus(); i.select(); return 'ok'; };
window.dPick = (name) => { const re = new RegExp('^' + name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\s+\\(DM\\)$', 'i'); const rows = [...root().querySelectorAll('[role=button],button')].filter(r => [...r.querySelectorAll('span')].some(s => re.test(s.textContent.trim()))); if (rows.length !== 1) return 'matches:' + rows.length; rows[0].focus(); return 'focused'; };
window.dShort = () => dThread().replace(/Heyy! Fatima here from Bambora[\s\S]*?Product page, for reference only[^\n]*\n?(https?:\S*)?/g, '[V3 WELCOME]').replace(/\n+/g, ' | ').replace(/Add reaction \| Reply in thread \| /g, '');
window.ta = () => [...root().querySelectorAll('textarea[placeholder="Type a message..."]')].pop();
// Robotic-phrase gate (skill human-messages, 2026-09-23). Keep in sync with lint_message.py BANNED.
window.BANNED = ["quick favor","quick favour","just wanted to","just a quick","hope this message finds you","hope this finds you","reaching out","i wanted to let you know","touching base","circling back","per my last","as per","kindly","please be advised","don't hesitate to","do not hesitate to","feel free to reach out","at your earliest convenience","i hope this helps","exciting opportunity","valued creator","we appreciate your","rest assured","in order to","leverage","moving forward,","going forward,","i hope you're doing well","i hope you are doing well","dear ","don't stress","honestly,","which says a lot","that says a lot","in no time","only because we","good question!","great question","totally normal","completely normal","you've got this covered","have it down","get the hang of it in no time","the more you film","so close","no rush","following up again","just following up","today please","on board","so much content","strict rule","us too","we too","me and the team","we're so","we are so","we can't wait","we cant wait","we love","we'd love","we're excited","we are excited","on our side","on our end","our team","we'll","we will","we're","we are ","all of us","both of us"];
// Chat replies over 220 chars (links excluded) read like a letter. Inspo packs: set window.LONG_OK = true for that send only.
window.MAX_REPLY = 220;
window.robotic = (text) => { const t = text.toLowerCase(); const hits = BANNED.filter(b => t.includes(b)); const noUrl = text.replace(/https?:\/\/\S+/g, ''); if (/\u2014|\u2013| - |--/.test(noUrl)) hits.push('dash'); if (!window.LONG_OK && noUrl.length > MAX_REPLY) hits.push('too long (' + noUrl.length + ' chars), say one thing like a text'); return hits; };
window.dFill = (name, text) => { const rb = robotic(text); if (rb.length) return 'ROBOTIC, REWRITE: ' + rb.join(', '); const h = dThread().split('\n')[0].trim(); if (!new RegExp('^' + name + '\\s+\\(DM\\)$', 'i').test(h.replace(/\s+/g, ' '))) return 'HEADER MISMATCH: ' + h; if (dThread().includes(text.slice(0, 60))) return 'ALREADY SENT'; const t = ta(); if (!t) return 'no ta'; if (t.value) return 'composer not empty'; Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set.call(t, text); t.dispatchEvent(new Event('input', { bubbles: true })); return 'filled'; };
window.clearComposer = () => { const t = ta(); Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set.call(t, ''); t.dispatchEvent(new Event('input', { bubbles: true })); };
window.dArm = (name, text) => { const h = dThread().split('\n')[0].trim(); if (!new RegExp('^' + name + '\\s+\\(DM\\)$', 'i').test(h) || ta().value !== text) { document.activeElement.blur(); return 'NOT ARMED'; } const b = [...root().querySelectorAll('button')].filter(x => /send message/i.test((x.getAttribute('aria-label') || '') + x.innerText)).pop(); if (!b) { document.activeElement.blur(); return 'no send'; } b.focus(); return 'armed'; };
window.dVerify = (text) => ({ count: dThread().split(text.slice(0, 60)).length - 1, composer: ta().value });
// The creator's most recent message line (name | time | text), used to spot anything new.
window.lastTheirLine = () => { const segs = dShort().split(' | '); let last = ''; for (let i = 1; i < segs.length; i++) { if (/(Today|Yesterday|\w{3} \d+),? \d+:\d+ [AP]M/.test(segs[i]) && !/Bambora Admin/.test(segs[i - 1])) last = segs.slice(i - 1, i + 2).join(' | '); } return last; };
// Batch sending of pre-approved texts held in window.V2 = {name: text}.
window.openV2 = (n) => { window.cur = n; return dPick(n); };
window.prep = (n) => { window.cur = n; window.snap = lastTheirLine(); return { h: dThread().split('\n')[0].trim(), last: snap.slice(0, 160), fill: dFill(n, V2[n]) }; };
window.armV2 = () => { if (lastTheirLine() !== snap) { clearComposer(); document.activeElement.blur(); return 'NEW MESSAGE, HOLD'; } if (/\| Today, /.test(snap)) { clearComposer(); document.activeElement.blur(); return 'HOLD, wrote today: ' + snap.slice(0, 200); } return dArm(cur, V2[cur]); };
window.verV2 = () => [cur, dVerify((window.N2 && N2[cur]) || (window.V2 && V2[cur]))];
'helpers loaded';
// Open a thread by search. Matches the row's text, so rows whose name isn't in its own span (initials avatars) still match.
window.openT = async (n, q) => { const b = [...root().querySelectorAll('button')].find(x => /^back$/i.test((x.innerText || x.getAttribute('aria-label') || '').trim())); if (b) { b.click(); await new Promise(z => setTimeout(z, 1000)); } const fs = root().querySelector('input[placeholder="Search Chat"]'); Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(fs, q || n); fs.dispatchEvent(new Event('input', { bubbles: true })); await new Promise(z => setTimeout(z, 1500)); const rows = [...root().querySelectorAll('[role=button],button')].filter(r => r.innerText.split('\n').some(l => l.replace(/\s+/g, ' ').trim().toLowerCase() === n.toLowerCase() + ' (dm)')); const leaf = rows.filter(r => !rows.some(o => o !== r && r.contains(o))); if (leaf.length !== 1) return 'rows:' + leaf.length; leaf[0].click(); await new Promise(z => setTimeout(z, 2200)); return 'open'; };
// Reactions: rx1() focuses the newest "Add reaction", press Return; await rx2('🥰') focuses that emoji (the search only knows short names, so it searches "heart"), press Return.
window.rx1 = () => { const a = [...root().querySelectorAll('button')].filter(x => /add reaction/i.test((x.getAttribute('aria-label') || '') + x.innerText)); if (!a.length) return 'no react btn'; a[a.length - 1].focus(); return 'focused react'; };
window.rx2 = async (emo) => { const i = document.querySelector('input[placeholder^="Search emoji"]'); if (!i) return 'no emoji search'; Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(i, 'heart'); i.dispatchEvent(new Event('input', { bubbles: true })); await new Promise(z => setTimeout(z, 600)); let p = i.parentElement; for (let k = 0; k < 3; k++) p = p.parentElement; const b = [...p.querySelectorAll('button')].find(x => x.innerText.trim() === emo); if (!b) return 'not found'; b.focus(); return 'focused ' + emo; };
// Unanswered-question scan (2026-09-24: Abbey Way's questions sat 5 days, Jena's music question got "Love that!").
// qCheck() on an open thread: finds the creator's latest message with a "?" and what we sent after it.
// Flags it when nothing we sent afterwards is longer than a quick reaction line, so a real answer is owed.
window.qCheck = () => {
  const segs = dShort().split(' | '); const msgs = []; let who = null;
  for (let i = 0; i < segs.length; i++) { if (/^(Today|Yesterday|\w{3} \d+),? \d+:\d+ [AP]M$/.test(segs[i])) { who = /Bambora Admin/.test(segs[i - 1]) ? 'us' : 'them'; continue; } if (segs[i] === 'Today' || segs[i] === 'Yesterday' || /^\w{3} \d+$/.test(segs[i])) { who = 'us'; continue; } if (who) msgs.push({ who, t: segs[i] }); }
  let qi = -1; msgs.forEach((m, i) => { if (m.who === 'them' && /\?/.test(m.t)) qi = i; });
  if (qi < 0) return null;
  const UI = /^(Edit message|Delete message|Attach file|Send message|Add reaction|Reply in thread|Scroll to bottom|New messages)$/;
  const after = msgs.slice(qi + 1).filter(m => m.who === 'us' && !UI.test(m.t)).map(m => m.t);
  // Answered = one of our later messages shares a real word (5+ letters) with the question.
  const words = new Set((msgs[qi].t.toLowerCase().match(/[a-z]{5,}/g) || []).filter(w => !/^(there|their|would|could|should|about|thank|thanks|which|these|those|where|while|really|video|videos)$/.test(w)));
  const answered = after.some(t => (t.toLowerCase().match(/[a-z]{5,}/g) || []).some(w => words.has(w)));
  return answered ? null : { question: msgs[qi].t.slice(0, 200), ourRepliesAfter: after };
};

// open2: the most reliable thread opener (2026-09-24). Whitespace-normalised name match (some names carry a trailing space,
// e.g. "Samantha bumstead  (DM)"), waits up to 6s for search results, refuses duplicates.
window.open2 = async (n, q) => { const b = [...root().querySelectorAll('button')].find(x => /^back$/i.test((x.innerText || x.getAttribute('aria-label') || '').trim())); if (b) { b.click(); await new Promise(z => setTimeout(z, 1000)); } const fs = root().querySelector('input[placeholder="Search Chat"]'); Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(fs, q || n); fs.dispatchEvent(new Event('input', { bubbles: true })); const want = n.toLowerCase() + ' (dm)'; let row = null; for (let w = 0; w < 12 && !row; w++) { await new Promise(z => setTimeout(z, 500)); const spans = [...root().querySelectorAll('span')].filter(s => s.textContent.replace(/\s+/g, ' ').trim().toLowerCase() === want); if (spans.length === 1) row = spans[0].closest('[role=button],button'); else if (spans.length > 1) return 'DUPLICATE ' + spans.length; } if (!row) return 'rows:0'; row.click(); await new Promise(z => setTimeout(z, 2200)); return dThread().split('\n')[0].replace(/\s+/g, ' ').trim().toLowerCase() === want ? 'open' : 'header mismatch'; };
// Send guard (2026-09-24: Savanna's "expecting baby #9" and Baili's excited reply were skipped because open and send ran in one step).
// theirLastUnanswered(): the creator's newest message when nothing of ours came after it (the thread is waiting on us).
// g2 refuses to arm while that's true unless window.ACK[name] === true, which is set ONLY after reading that message
// and writing a reply that answers it first.
window.ACK = window.ACK || {};
window.theirLastUnanswered = () => { const segs = dShort().split(' | ').filter(s => !/^(Edit message|Delete message|Attach file|Send message|Add reaction|Reply in thread|Scroll to bottom|New messages)$/.test(s)); let lastWho = null, lastText = ''; for (let i = 0; i < segs.length; i++) { if (/^(Today|Yesterday|\w{3} \d+),? \d+:\d+ [AP]M$/.test(segs[i])) { lastWho = /Bambora Admin/.test(segs[i - 1]) ? 'us' : 'them'; lastText = segs[i + 1] || ''; } else if (/^(Today|Yesterday|\w{3} \d+)$/.test(segs[i])) { lastWho = 'us'; } } return lastWho === 'them' ? lastText : null; };
window.g2 = async (n, q) => { window.cur = n; const o = await open2(n, q); if (o !== 'open') return o; window.snap = lastTheirLine(); const un = theirLastUnanswered(); if (un && !window.ACK[n]) return 'READ FIRST, unanswered: ' + un.slice(0, 200); const f = dFill(n, N2[n]); if (f !== 'filled') { document.activeElement.blur(); return f; } return [snap.slice(0, 70), dArm(n, N2[n])]; };
// Conversation list scan (2026-09-24). Run on the chat list (DMs tab, search cleared). Reads every DM row's
// last-message preview and age, so nothing depends on the Unread filter.
//   convoScan() -> { needsUs: rows where THEY sent the last message (answer these, oldest first),
//                    waiting: rows where WE sent the last message 2+ days ago with no reply (one gentle follow-up each) }
// Only the last 14 days count (older threads are pre-V3 programs; ignore-list names are skipped by the caller).
// Age strings look like "3m", "5h", "2d", "Now", "Yesterday", "Sep 12". Fixed 2026-09-25: "Yesterday"/"Now" used to parse as 99 days, so yesterday's unanswered messages vanished from needsUs after midnight (Jen Smith).
window.convoScan = () => {
  const rows = [...root().querySelectorAll('[role=button]')].filter(r => /\(DM\)/.test(r.innerText));
  const days = (a) => { if (/^(now|just now)$/i.test(a) || /^\d{1,2}:\d{2}\s?[AP]M$/i.test(a)) return 0; if (/^yesterday$/i.test(a)) return 1; if (/^(mon|tue|wed|thu|fri|sat|sun)/i.test(a)) return 3; const m = a.match(/^(\d+)([mhdw])$/); if (m) return { m: 0, h: 0, d: +m[1], w: 7 * m[1] }[m[2]]; const d = new Date(a + ', ' + new Date().getFullYear()); return isNaN(d) ? 99 : Math.floor((Date.now() - d) / 864e5); };
  const out = { needsUs: [], waiting: [] };
  for (const r of rows) {
    const L = r.innerText.split('\n').map(s => s.trim()).filter(Boolean); const i = L.findIndex(l => /\(DM\)$/.test(l)); if (i < 0) continue;
    const name = L[i].replace(/\s*\(DM\)$/, '').replace(/\s+/g, ' ').trim(); const age = L[i + 1] || ''; const prev = L.slice(i + 2).join(' ');
    const ours = /^You( replied|:)|^Welcome to the Bambora family|^Welcome to our creator program|^Hey! 💙 Just checking in|^Heyy! Fatima here|wanted to check in and share a few changes/.test(prev);
    if (ours) { if (days(age) >= 2 && days(age) < 14) out.waiting.push({ name, age, last: prev.replace(/^You:\s*/, '').slice(0, 90) }); }
    else if (prev && days(age) < 14) out.needsUs.push({ name, age, last: prev.slice(0, 90) });
  }
  return out;
};
