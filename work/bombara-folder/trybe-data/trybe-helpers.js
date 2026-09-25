/* Bambora / Trybe creative-audit helpers.
 * Paste into the Chrome devtools console on:
 *   jointrybe.com/brand/analytics  (lifetime range set, "Group by Creative", 48/page)
 *
 * Why this exists: Trybe's creative table is a windowing virtualiser (it throws
 * rows away as you scroll) and the sale copy in the ads is BURNED-IN CAPTION,
 * not speech - so transcripts miss it. You have to scrub the video.
 */
(function () {
  const scroller = () => { let n = document.querySelector('table'); for (let i = 0; i < 4; i++) n = n.parentElement; return n; };
  const ROW_H = 72.6;

  /* --- 1. scrape the virtualised table ------------------------------- */
  window.__acc = window.__acc || new Map();
  window.__reset = () => { window.__acc = new Map(); return 'reset'; };

  const grab = () => {
    for (const tr of document.querySelectorAll('table tbody tr')) {
      const c = [...tr.querySelectorAll('td')].map(td => td.innerText.trim().replace(/\s+/g, ' '));
      if (c.length < 4) continue;
      window.__acc.set(c.slice(1).join('|'), c.slice(1));
    }
  };

  // Fire-and-forget: the extension's JS bridge times out on awaited calls,
  // but the work keeps running. Poll __acc.size, don't await this.
  window.__sweep = async (from = 0, to = 3400, step = 55) => {
    const sc = scroller();
    for (let y = from; y <= to; y += step) {
      sc.scrollTop = y;
      sc.dispatchEvent(new Event('scroll', { bubbles: true }));
      await new Promise(r => setTimeout(r, 110));
      grab();
    }
    return window.__acc.size;
  };

  // Run __sweep 2-3x with different step sizes; one pass misses ~25% of rows.
  window.__rows = () => [...window.__acc.values()];
  window.__tsv = () => window.__rows().map(r => r.join('\t')).join('\n');

  /* --- 2. open one creative's modal ----------------------------------- */
  // idx is the 0-based rank in the sales-sorted table, used to scroll it into
  // view before clicking. creator+sales disambiguate duplicate sales strings.
  window.__open = (creator, sales, idx) => {
    const sc = scroller(), want = Math.max(0, idx * ROW_H - 200);
    if (Math.abs(sc.scrollTop - want) > 30) {
      sc.scrollTop = want;
      sc.dispatchEvent(new Event('scroll', { bubbles: true }));
    }
    const r = [...document.querySelectorAll('table tbody tr')]
      .find(tr => tr.innerText.includes(creator) && tr.innerText.includes(sales));
    if (!r) return 'not-rendered@' + sc.scrollTop;
    r.click();
    return 'ok';
  };

  window.__closeModal = () => {
    const b = [...document.querySelectorAll('button')]
      .find(x => x.offsetParent && /close/i.test(x.getAttribute('aria-label') || ''));
    if (b) { b.click(); return 'closed'; }
    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
    return 'esc';
  };

  /* --- 3. scrub the video -------------------------------------------- */
  // NOTE: the modal contains TWO <video> elements. The first is 0x0 and
  // seeking it does nothing. Always pick the largest visible one.
  window.__vid = () => [...document.querySelectorAll('video')]
    .map(v => ({ v, b: v.getBoundingClientRect() }))
    .filter(o => o.b.width > 50 && o.b.height > 50)
    .sort((a, b) => b.b.width * b.b.height - a.b.width * a.b.height)[0];

  window.__seek = (frac) => {
    const o = window.__vid(); if (!o) return 'no-visible-video';
    const v = o.v; if (!v.duration || isNaN(v.duration)) return 'no-duration';
    v.pause();
    v.currentTime = Math.max(0.05, Math.min(v.duration - 0.15, v.duration * frac));
    return { at: +v.currentTime.toFixed(1), dur: +v.duration.toFixed(1), box: window.__box() };
  };

  // Screenshot tools use a different coordinate frame than CSS pixels.
  // Multiply by 1568/innerWidth to get the region to crop.
  window.__box = () => {
    const o = window.__vid(); if (!o) return null;
    const k = 1568 / window.innerWidth, b = o.b;
    return [Math.round(b.x * k), Math.round(b.y * k),
            Math.round((b.x + b.width) * k), Math.round((b.y + b.height) * k)];
  };

  return 'trybe helpers ready: __sweep __rows __tsv __open __closeModal __seek __box __reset';
})();
