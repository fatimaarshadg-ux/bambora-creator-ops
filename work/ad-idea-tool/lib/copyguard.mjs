// Catches hooks that lift wording from the ad library. The prompt tells the model
// not to copy; this is the check that does not rely on the model obeying.

const words = (text) =>
  (text || "").toLowerCase().replace(/[^a-z0-9\s']/g, " ").split(/\s+/).filter(Boolean);

// Longest run of consecutive words shared by both texts.
export function longestSharedRun(a, b) {
  const x = words(a), y = words(b);
  let best = 0, bestEnd = 0;
  let prev = new Array(y.length + 1).fill(0);
  for (let i = 1; i <= x.length; i++) {
    const cur = new Array(y.length + 1).fill(0);
    for (let j = 1; j <= y.length; j++) {
      if (x[i - 1] === y[j - 1]) {
        cur[j] = prev[j - 1] + 1;
        if (cur[j] > best) { best = cur[j]; bestEnd = i; }
      }
    }
    prev = cur;
  }
  return { length: best, phrase: x.slice(bestEnd - best, bestEnd).join(" "), shorter: Math.min(x.length, y.length) };
}

export function isTooClose(candidate, source) {
  const run = longestSharedRun(candidate, source);
  if (run.length >= 5) return run.phrase;
  if (run.length >= 4 && run.length / Math.max(run.shorter, 1) >= 0.6) return run.phrase;
  return null;
}

// Returns [{ slot, field, text, phrase, adId }] for every hook that overlaps a library hook.
export function findCopies(ideas, ads) {
  const sources = ads.flatMap((ad) =>
    [ad.hook_spoken, ad.hook_onscreen].filter(Boolean).map((text) => ({ adId: ad.id, text }))
  );
  const hits = [];
  for (const idea of ideas) {
    const fields = [
      ["hook.spoken", idea.hook?.spoken],
      ["hook.onscreen_text", idea.hook?.onscreen_text],
      ...(idea.alt_hooks || []).map((h, i) => [`alt_hooks.${i}`, h]),
    ];
    for (const [field, text] of fields) {
      if (!text) continue;
      for (const src of sources) {
        const phrase = isTooClose(text, src.text);
        if (phrase) { hits.push({ slot: idea.slot, field, text, phrase, adId: src.adId }); break; }
      }
    }
  }
  return hits;
}
