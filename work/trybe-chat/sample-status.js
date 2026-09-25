// Sample status gate (built 2026-09-23 after Alison Boutwell was told to "request your sample"
// when she already had a pending request).
// RULE: no message that mentions a sample (request, approve, arrive, ship) is sent until this
// has been run for that creator in the SAME sweep, and the message matches what it returns.
//
// Use it in the Samples tab (/brand/creators?...&tab=samples). Load it with
//   eval(await fetch('http://127.0.0.1:8765/sample-status.js').then(r => r.text()))
// NOTE: the Approved list shows the newest 20 only, so "none" for an OLD creator may just mean off-page; check the creator profile modal (sample history) for anyone accepted over 2 weeks ago.
// then:  await sampleStatus(['Alison Boutwell', 'Kristen Smith'])
// It returns {name: [{status, date, row}]}; status is pending, approved or none. Watch for
// duplicate names (two Kristen Smiths): check the date and the account before acting.

window.sampleStatus = async (names) => {
  const click = async (label) => {
    const b = [...document.querySelectorAll('main button')].find(x => x.innerText.trim() === label);
    if (!b) throw new Error('filter button not found: ' + label + ' (is this the Samples tab?)');
    b.click();
    await new Promise(z => setTimeout(z, 2500));
    return [...document.querySelectorAll('main tbody tr')].map(r => r.innerText.replace(/\s+/g, ' ').trim()).filter(t => /\d{4}/.test(t));
  };
  const pending = await click('Pending');
  const approved = await click('Approved');
  const out = {};
  for (const n of names) {
    const re = new RegExp(n.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i');
    const hits = [];
    pending.filter(t => re.test(t)).forEach(t => hits.push({ status: 'pending', date: (t.match(/\w{3} \d\d, \d{4}/) || [''])[0], row: t.slice(0, 80) }));
    approved.filter(t => re.test(t)).forEach(t => hits.push({ status: 'approved', date: (t.match(/\w{3} \d\d, \d{4}/) || [''])[0], row: t.slice(0, 80) }));
    out[n] = hits.length ? hits : [{ status: 'none' }];
  }
  // A read that finds no rows at all is a FAILED check, not "none".
  if (!pending.length && !approved.length) return { error: 'no rows read; the check failed, do not message' };
  return out;
};
'sample-status loaded';
