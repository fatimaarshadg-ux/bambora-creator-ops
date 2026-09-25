// Roster + samples scan (built 2026-09-24 so a full run needs no hand-holding).
// Load on the Creators roster page (/brand/creators, not the samples tab):
//   eval(await fetch('http://127.0.0.1:8765/roster-scan.js').then(r => r.text()))
// Step 1, on the Samples tab: await collectSamples()  (pages through ALL sample requests, saves to sessionStorage)
// Step 2, on the roster page:  rosterScan()            (uses the saved samples)
// Returns, for V3 creators:
//   canRequest:  partnership ads never requested and the Request button is available -> click Request + tiny note
//   noConnect:   "--" in Partnership Ads = no Instagram/Meta connected to Trybe -> ask them to connect Instagram in their Trybe profile
//   pendingPA:   requested, not yet accepted
//   noSample:    joined in the last 21 days, no sample request on record -> sample nudge (unless they already own a Bambora)
//   oldPending:  sample requests made before 2026-09-17 -> NEVER approve (Fatima's rule); leave for her
window.samplesPage = () => { const r = document.querySelector('main tbody tr'); if (!r) return []; const k = Object.keys(r).find(k => k.startsWith('__reactFiber')); let f = r[k]; for (let d = 0; d < 40 && f; d++) { const p = f.memoizedProps || {}; if (Array.isArray(p.children) && p.children[0]?.props?.request) return p.children.map(c => c.props.request).map(q => ({ cid: q.creatorId, n: (q.shipFirstName + ' ' + (q.shipLastName || '')).trim(), s: q.status, d: (q.createdAt || '').slice(0, 10) })); f = f.return; } return []; };
window.collectSamples = async () => {
  const all = [...document.querySelectorAll('main button')].find(x => x.innerText.trim() === 'All'); if (all) { all.click(); await new Promise(z => setTimeout(z, 2500)); }
  const out = []; for (let pg = 1; pg <= 30; pg++) {
    if (pg > 1) { const btns = [...document.querySelectorAll('main button')]; const i = btns.findIndex(b => b.innerText.trim() === '»»'); const nb = btns[i - 1]; if (!nb || nb.disabled) break; const first = samplesPage()[0]?.cid; nb.click(); let moved = false; for (let w = 0; w < 25; w++) { await new Promise(z => setTimeout(z, 400)); const nr = samplesPage(); if (nr[0] && nr[0].cid !== first) { moved = true; break; } } if (!moved) break; }
    out.push(...samplesPage());
  }
  sessionStorage.setItem('ALLS', JSON.stringify(out)); return { total: out.length, pending: out.filter(x => x.s === 'PENDING') };
};
window.rosterProps = () => { const r = [...document.querySelectorAll('main tbody tr')][0]; const el = r.children[6].querySelector('*') || r.children[6]; const k = Object.keys(el).find(k => k.startsWith('__reactFiber')); let f = el[k]; for (let d = 0; d < 30 && f; d++) { const p = f.memoizedProps || {}; if (p.partnershipStatuses) return p; f = f.return; } return null; };
window.rosterScan = () => {
  const P = rosterProps(); if (!P) return 'roster props not found (clear the search box first)';
  const S = JSON.parse(sessionStorage.getItem('ALLS') || '[]'); const has = new Set(S.map(x => x.cid));
  const v3 = P.filteredCreators.filter(c => /V3/i.test(JSON.stringify(P.creatorProgramMap[c.id] || '')));
  const nm = c => (c.firstName + ' ' + (c.lastName || '')).trim();
  const since = new Date(Date.now() - 21 * 864e5).toISOString().slice(0, 10);
  return {
    v3: v3.length, samplesRead: S.length,
    canRequest: v3.filter(c => c.partnership?.canRequest && c.partnership.status === 'NONE').map(nm),
    noConnect: v3.filter(c => !c.metaConnection?.hasConnection).map(nm),
    pendingPA: v3.filter(c => c.partnership?.status === 'PENDING').map(nm),
    noSample: S.length ? v3.filter(c => !has.has(c.id) && c.joinedAt.slice(0, 10) >= since).map(c => nm(c) + ' (joined ' + c.joinedAt.slice(0, 10) + ')') : 'run collectSamples() on the Samples tab first',
    oldPending: S.filter(x => x.s === 'PENDING' && x.d < '2026-09-17').map(x => x.n + ' ' + x.d),
    newPending: S.filter(x => x.s === 'PENDING' && x.d >= '2026-09-17').map(x => x.n + ' ' + x.d),
  };
};
'roster-scan loaded';
// Left-nav badges: the cheapest "is there anything to do?" check. Run first in every sweep.
window.badges = () => Object.fromEntries([...document.querySelectorAll('a, button')].filter(a => /^(Submissions|Chat|Creators|Discovery)\n/.test(a.innerText.trim())).map(a => a.innerText.trim().split('\n')).filter(x => x.length === 2 && /^\d+\+?$/.test(x[1])).map(x => [x[0], x[1]]));
// Discovery Inbox: names of every applicant card on the current page (run on each Inbox page).
// Compare with ~/claude-setup/work/trybe-applicant-review/seen.txt; any name not there is NEW and gets reviewed THIS sweep
// (start the review in a background agent so chat isn't blocked), then add the names to seen.txt.
window.inboxNames = () => [...document.querySelectorAll('button')].filter(x => /^\s*Reject\s*$/i.test(x.textContent || '')).map(b => { let el = b; for (let k = 0; k < 8 && el; k++) { el = el.parentElement; if (el && /commission/i.test(el.innerText)) break; } const L = el ? el.innerText.split('\n').map(s => s.trim()).filter(Boolean) : []; return (L[0] && L[0].length <= 3 && L[1]) ? L[1] : L[0]; });
