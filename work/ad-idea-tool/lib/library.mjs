import { readFileSync } from "node:fs";
import path from "node:path";

const DATA_DIR = process.env.DATA_DIR || path.resolve("data");

export function readJson(name) {
  return JSON.parse(readFileSync(path.join(DATA_DIR, name), "utf8"));
}

// Small CSV parser that handles quoted fields, escaped quotes and newlines inside quotes.
export function parseCsv(text) {
  const rows = [];
  let row = [], field = "", inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inQuotes) {
      if (c === '"' && text[i + 1] === '"') { field += '"'; i++; }
      else if (c === '"') inQuotes = false;
      else field += c;
    } else if (c === '"') inQuotes = true;
    else if (c === ",") { row.push(field); field = ""; }
    else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(field); field = "";
      if (row.some((f) => f.trim() !== "")) rows.push(row);
      row = [];
    } else field += c;
  }
  row.push(field);
  if (row.some((f) => f.trim() !== "")) rows.push(row);

  const [header, ...body] = rows;
  const keys = header.map((h) => h.trim().replace(/^﻿/, ""));
  return body.map((r) => Object.fromEntries(keys.map((k, i) => [k, (r[i] || "").trim()])));
}

export function loadAds() {
  const text = readFileSync(path.join(DATA_DIR, "ads.csv"), "utf8");
  return parseCsv(text).filter((ad) => ad.id && (ad.hook_spoken || ad.hook_onscreen));
}

export function shuffle(list) {
  const a = [...list];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// Picks the examples most relevant to the requested slots, plus a few unrelated
// ones so the model sees patterns from outside the obvious bucket.
export function selectExamples(ads, slots, { relevant = 8, wildcard = 4 } = {}) {
  const formats = new Set(slots.map((s) => s.format));
  const frameworks = new Set(slots.map((s) => s.framework));
  const angles = new Set(slots.map((s) => s.angle));

  const scored = shuffle(ads).map((ad) => {
    let score = 0;
    if (formats.has(ad.format)) score += 3;
    if (frameworks.has(ad.framework)) score += 2;
    if (ad.angle && angles.has(ad.angle)) score += 2;
    if (score > 0 && ad.source === "bambora") score += 1;
    return { ad, score };
  });

  const top = scored.filter((s) => s.score > 0).sort((a, b) => b.score - a.score).slice(0, relevant);
  const chosen = new Set(top.map((s) => s.ad.id));
  const rest = scored.filter((s) => !chosen.has(s.ad.id)).slice(0, wildcard);
  return [...top, ...rest].map((s) => s.ad);
}
