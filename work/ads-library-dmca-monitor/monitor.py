#!/usr/bin/env python3
"""
Meta Ads Library keyword and creative monitor for DMCA follow-up.

What it does, in order:
  1. Builds Ad Library search URLs for every keyword in config.json.
  2. Runs the Apify actor apify/facebook-ads-scraper on those URLs.
  3. Drops Bambora's own ads, then flags each remaining ad with evidence:
       brand   : a brand term appears in the ad text, headline or page name
       copy    : a distinctive phrase from Bambora's own copy appears in the ad
       visual  : an image or video thumbnail matches one of Bambora's own creatives
  4. Remembers every ad it has reported (state/seen.json) so re-runs mark what is new.
  5. Writes reports/<timestamp>.html and .csv with the Ad Library link for each hit.

Usage:
  python monitor.py                 full run (keyword searches + visual match)
  python monitor.py --no-visual     keyword searches only
  python monitor.py --new-only      report only ads not seen on a previous run
  python monitor.py --refresh-reference   re-download Bambora's own creatives for visual matching
  python monitor.py --from-json file.json  skip Apify, score records from a saved dataset
  python monitor.py --estimate      print the worst-case Apify cost and exit

  python monitor.py --slack         also post the summary to Slack (config.json can turn this on by default)

Secrets: APIFY_TOKEN and SLACK_WEBHOOK_URL env vars, or store each once with
         store-secret.ps1 -Name apify_api_token / -Name slack_webhook (Windows, DPAPI),
         or  security add-generic-password -a "$USER" -s apify-api-token -w  (Mac Keychain, also slack-webhook).
Only standard library plus Pillow (for visual matching) is required.
"""

import argparse
import csv
import html
import io
import json
import os
import platform
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONFIG_PATH = HERE / "config.json"
STATE_DIR = HERE / "state"
REPORT_DIR = HERE / "reports"
SEEN_PATH = STATE_DIR / "seen.json"
REFERENCE_PATH = STATE_DIR / "reference_hashes.json"
LAST_DATASET_PATH = STATE_DIR / "last_dataset.json"
DIGEST_SEEN_PATH = STATE_DIR / "digest_seen.json"

APIFY_BASE = "https://api.apify.com/v2"
AD_LIBRARY = "https://www.facebook.com/ads/library/"
PRICE_PER_AD_USD = 0.0058  # free-tier price for apify/facebook-ads-scraper, worst case

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36"


# --------------------------------------------------------------------------- helpers

def log(msg):
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    try:  # also keep a log file so scheduled runs can be inspected afterwards
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        with open(STATE_DIR / "last_run.log", "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass


def load_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def fetch_bytes(url, timeout=60):
    """Download a URL. Local paths and file:// URLs are allowed for offline tests."""
    if url.startswith("file://"):
        return Path(urllib.request.url2pathname(urllib.parse.urlparse(url).path)).read_bytes()
    if not url.startswith("http"):
        return Path(url).read_bytes()
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


# --------------------------------------------------------------------------- token

def load_secret(name, env_var, required=True):
    """Read a secret from the environment, else Windows DPAPI (~/.claude/secrets/<name>.dpapi),
    else the macOS login Keychain (service name = <name> with hyphens)."""
    val = os.environ.get(env_var, "").strip()
    if val:
        return val
    system = platform.system()
    if system == "Windows":
        blob = Path.home() / ".claude" / "secrets" / f"{name}.dpapi"
        if blob.exists():
            ps = (
                f'$s = Get-Content "{blob}" | ConvertTo-SecureString; '
                "$b = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($s); "
                "[System.Runtime.InteropServices.Marshal]::PtrToStringAuto($b)"
            )
            out = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                                 capture_output=True, text=True)
            val = out.stdout.strip()
        hint = f"set {env_var} or run: powershell -ExecutionPolicy Bypass -File store-secret.ps1 -Name {name}"
    elif system == "Darwin":
        out = subprocess.run(["security", "find-generic-password", "-a", os.environ.get("USER", ""),
                              "-s", name.replace("_", "-"), "-w"], capture_output=True, text=True)
        val = out.stdout.strip()
        hint = f'set {env_var} or run: security add-generic-password -a "$USER" -s {name.replace("_", "-")} -w'
    else:
        hint = f"set {env_var}"
    if val or not required:
        return val
    sys.exit(f"No {name} found: {hint}")


def load_token():
    return load_secret("apify_api_token", "APIFY_TOKEN")


# --------------------------------------------------------------------------- slack

def post_to_slack(webhook_url, text, blocks=None):
    payload = {"text": text}
    if blocks:
        payload["blocks"] = blocks
    req = urllib.request.Request(webhook_url, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status


def slack_digest_messages(digest, stamp, per_message=20):
    """Picture digest of new sling-category ads: one section per ad with its thumbnail on the right.
    Returns a list of (text, blocks) messages, because Slack caps a message at 50 blocks."""
    if not digest:
        return [(f"Picture digest {stamp}: no new baby-sling ads this week.", None)]
    messages = []
    for start in range(0, len(digest), per_message):
        chunk = digest[start:start + per_message]
        head = (f"*Picture digest {stamp}*: {len(digest)} new baby-sling ad(s) from other pages. "
                f"Scroll and shout if any of them is the Bambora sling." if start == 0 else f"*Picture digest, continued* ({start + 1} to {start + len(chunk)} of {len(digest)})")
        blocks = [{"type": "section", "text": {"type": "mrkdwn", "text": head}}]
        for a in chunk:
            dest = a["links"][0] if a["links"] else ""
            line = (f"*{a['page_name']}* · started {a['start']}\n"
                    f"<{a['ad_url']}|Open in Ad Library>" + (f" · <{dest}|Their store>" if dest else "")
                    + (f"\n_{a['text'][:140]}_" if a["text"] else ""))
            block = {"type": "section", "text": {"type": "mrkdwn", "text": line}}
            if a["images"]:
                block["accessory"] = {"type": "image", "image_url": a["images"][0], "alt_text": a["page_name"][:60]}
            blocks.append(block)
            blocks.append({"type": "divider"})
        messages.append((head.replace("*", ""), blocks[:50]))
    return messages


def slack_summary(rows, stamp, notify):
    picked = [r for r in rows if r["new"]] if notify == "new" else rows
    new_count = sum(1 for r in rows if r["new"])
    head = f"*Ads Library monitor, {stamp}*: {len(rows)} flagged ad(s), {new_count} new."
    if not picked:
        return head + (" Nothing new to look at." if notify == "new" else "")
    lines = [head, ""]
    for r in picked[:20]:
        tag = "NEW " if r["new"] else ""
        lines.append(f"• {tag}*{r['evidence']}* <{r['page_url']}|{r['page_name']}> "
                     f"<{r['ad_url']}|ad {r['ad_id']}> ({r['start']}) {r['why'][:120]}")
    if len(picked) > 20:
        lines.append(f"... {len(picked) - 20} more in the report")
    return "\n".join(lines)


# --------------------------------------------------------------------------- apify

class Apify:
    def __init__(self, token):
        self.token = token

    def _call(self, method, path, body=None, params=None):
        params = dict(params or {})
        params["token"] = self.token
        url = f"{APIFY_BASE}{path}?{urllib.parse.urlencode(params)}"
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, method=method,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")[:500]
            raise RuntimeError(f"Apify {method} {path} -> HTTP {e.code}: {detail}") from None

    def run_actor(self, actor, actor_input, poll_every=15, max_wait=3600):
        run = self._call("POST", f"/acts/{actor}/runs", body=actor_input)["data"]
        run_id, dataset_id = run["id"], run["defaultDatasetId"]
        log(f"Apify run {run_id} started (https://console.apify.com/actors/runs/{run_id})")
        started = time.time()
        while True:
            status = self._call("GET", f"/actor-runs/{run_id}")["data"]["status"]
            if status in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
                break
            if time.time() - started > max_wait:
                raise RuntimeError(f"Apify run {run_id} still {status} after {max_wait}s")
            time.sleep(poll_every)
        if status != "SUCCEEDED":
            raise RuntimeError(f"Apify run {run_id} ended with status {status}")
        return self.dataset_items(dataset_id)

    def dataset_items(self, dataset_id):
        items, offset, limit = [], 0, 1000
        while True:
            page = self._call("GET", f"/datasets/{dataset_id}/items",
                              params={"clean": "true", "offset": offset, "limit": limit})
            items.extend(page)
            if len(page) < limit:
                return items
            offset += limit


# --------------------------------------------------------------------------- searches

def keyword_search_url(term, country, active_status, exact):
    q = {
        "active_status": active_status,
        "ad_type": "all",
        "country": country,
        "is_targeted_country": "false",
        "media_type": "all",
        "q": term,
        "search_type": "keyword_exact_phrase" if exact else "keyword_unordered",
    }
    return AD_LIBRARY + "?" + urllib.parse.urlencode(q)


def page_ads_url(page_id, country="ALL", active_status="all"):
    q = {
        "active_status": active_status,
        "ad_type": "all",
        "country": country,
        "is_targeted_country": "false",
        "media_type": "all",
        "search_type": "page",
        "view_all_page_id": page_id,
    }
    return AD_LIBRARY + "?" + urllib.parse.urlencode(q)


def build_search_plan(cfg):
    """One entry per search URL, tagged with why we are searching it."""
    plan = []
    for country in cfg.get("countries", ["ALL"]):
        for term in cfg.get("brand_terms", []):
            plan.append({"kind": "brand", "term": term,
                         "url": keyword_search_url(term, country, cfg["active_status"], exact=True)})
        for term in cfg.get("copy_phrases", []):
            plan.append({"kind": "copy", "term": term,
                         "url": keyword_search_url(term, country, cfg["active_status"], exact=True)})
        for term in cfg.get("category_searches", []):
            plan.append({"kind": "category", "term": term,
                         "url": keyword_search_url(term, country, cfg["active_status"], exact=False)})
    return plan


# --------------------------------------------------------------------------- normalise records

def _get(d, *keys, default=None):
    """First non-empty value among several possible key spellings."""
    for k in keys:
        v = d.get(k) if isinstance(d, dict) else None
        if v not in (None, "", [], {}):
            return v
    return default


def _text(v):
    if isinstance(v, dict):
        return _text(_get(v, "text", "markup", default=""))
    if isinstance(v, list):
        return " ".join(_text(x) for x in v)
    return str(v or "")


def unwrap(items):
    """The actor returns a wrapper {inputUrl, results: [...], totalCount} for some searches; flatten it."""
    out = []
    for rec in items:
        if isinstance(rec, dict) and "results" in rec and "adArchiveID" not in rec:
            for inner in rec.get("results") or []:
                if isinstance(inner, dict):
                    out.append({**inner, "inputUrl": inner.get("inputUrl") or rec.get("inputUrl", "")})
        else:
            out.append(rec)
    return out


def normalise(rec):
    snap = rec.get("snapshot") or {}
    cards = snap.get("cards") or []
    texts = [
        _text(_get(snap, "title")),
        _text(_get(snap, "body")),
        _text(_get(snap, "linkDescription", "link_description")),
        _text(_get(snap, "caption")),
    ]
    images, videos, links = [], [], []
    for img in snap.get("images") or []:
        u = _get(img, "originalImageUrl", "original_image_url", "resizedImageUrl", "resized_image_url", "url")
        if u:
            images.append(u)
    for vid in snap.get("videos") or []:
        thumb = _get(vid, "videoPreviewImageUrl", "video_preview_image_url")
        src = _get(vid, "videoHdUrl", "video_hd_url", "videoSdUrl", "video_sd_url")
        if thumb:
            images.append(thumb)
        if src:
            videos.append(src)
    for card in cards:
        texts += [_text(_get(card, "title")), _text(_get(card, "body")), _text(_get(card, "linkDescription", "link_description"))]
        u = _get(card, "originalImageUrl", "original_image_url", "resizedImageUrl", "resized_image_url")
        if u:
            images.append(u)
        thumb = _get(card, "videoPreviewImageUrl", "video_preview_image_url")
        src = _get(card, "videoHdUrl", "video_hd_url", "videoSdUrl", "video_sd_url")
        if thumb:
            images.append(thumb)
        if src:
            videos.append(src)
        lu = _get(card, "linkUrl", "link_url")
        if lu:
            links.append(lu)
    lu = _get(snap, "linkUrl", "link_url")
    if lu:
        links.insert(0, lu)

    ad_id = str(_get(rec, "adArchiveID", "adArchiveId", "ad_archive_id", "id", default=""))
    page_id = str(_get(rec, "pageID", "pageId", "page_id", default=_get(snap, "pageId", "page_id", default="")))
    page_name = _get(rec, "pageName", "page_name", default=_get(snap, "pageName", "page_name", default=""))
    start = _get(rec, "startDateFormatted", "startDate", "start_date", default="")
    if isinstance(start, (int, float)):
        start = datetime.fromtimestamp(start, tz=timezone.utc).strftime("%Y-%m-%d")
    elif isinstance(start, str) and "T" in start:
        start = start[:10]

    def dedupe(seq):
        out = []
        for x in seq:
            if x not in out:
                out.append(x)
        return out

    return {
        "ad_id": ad_id,
        "ad_url": f"{AD_LIBRARY}?id={ad_id}" if ad_id else "",
        "page_id": page_id,
        "page_name": str(page_name),
        "page_url": _get(snap, "pageProfileUri", "page_profile_uri", default=f"https://www.facebook.com/{page_id}" if page_id else ""),
        "start": str(start),
        "active": bool(_get(rec, "isActive", "is_active", default=False)),
        "platforms": ", ".join(_get(rec, "publisherPlatform", "publisher_platform", default=[]) or []),
        "text": " | ".join(t for t in texts if t).strip(),
        "images": dedupe(images),
        "videos": dedupe(videos),
        "links": dedupe(links),
        "search_url": _get(rec, "inputUrl", "input_url", default=""),
    }


# --------------------------------------------------------------------------- matching

def contains_phrase(corpus, phrase):
    """Case-insensitive match that ignores punctuation and whitespace differences."""
    norm = lambda s: re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
    return norm(phrase) in norm(corpus)


def link_domain(url):
    host = urllib.parse.urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def is_own(ad, cfg):
    """Bambora's own ads, plus creator or partnership ads that send traffic to Bambora's site."""
    if ad["page_id"] and ad["page_id"] in set(cfg.get("own_page_ids", [])):
        return True
    own_domains = set(cfg.get("own_domains", []))
    if own_domains and any(link_domain(l) in own_domains for l in ad["links"]):
        return True
    name = ad["page_name"].lower()
    return any(p.lower() in name for p in cfg.get("own_page_name_patterns", []))


def score_text(ad, cfg):
    corpus = f'{ad["page_name"]} {ad["text"]} {" ".join(ad["links"])}'
    brand = [t for t in cfg.get("brand_terms", []) if contains_phrase(corpus, t)]
    copy_ = [t for t in cfg.get("copy_phrases", []) if contains_phrase(corpus, t)]
    return brand, copy_


# --------------------------------------------------------------------------- visual matching (dHash)

def dhash(image_bytes, size=8):
    """Difference hash: robust to resizing, recompression and small colour edits."""
    from PIL import Image
    img = Image.open(io.BytesIO(image_bytes)).convert("L").resize((size + 1, size), Image.LANCZOS)
    px = list(img.tobytes())  # 8-bit greyscale, row-major
    bits = []
    for row in range(size):
        for col in range(size):
            left = px[row * (size + 1) + col]
            right = px[row * (size + 1) + col + 1]
            bits.append("1" if left > right else "0")
    return f"{int(''.join(bits), 2):016x}"


def hamming(a, b):
    return bin(int(a, 16) ^ int(b, 16)).count("1")


def hash_urls(urls, cache, limit=None):
    """Return {url: hash} for the given image URLs, using and filling the cache."""
    out = {}
    for u in (urls[:limit] if limit else urls):
        if u in cache:
            if cache[u]:
                out[u] = cache[u]
            continue
        try:
            cache[u] = dhash(fetch_bytes(u))
            out[u] = cache[u]
        except Exception as e:  # unreachable CDN URL, expired signature, not an image
            cache[u] = None
            log(f"  could not hash {u[:80]}... ({e.__class__.__name__})")
    return out


def build_reference(cfg, apify, force=False, own_ads=()):
    """Hashes of Bambora's own ad creatives, cached in state/reference_hashes.json.
    Own ads already present in the current scan are hashed for free and merged in;
    Apify is only called when there is no cache and no own ads in hand."""
    ref = load_json(REFERENCE_PATH, {})
    hashes = dict(ref.get("hashes") or {}) if not force else {}
    if own_ads:
        cache, before = {}, len(hashes)
        for ad in own_ads:
            for u, h in hash_urls(ad["images"], cache).items():
                hashes.setdefault(h, {"ad_id": ad["ad_id"], "url": u})
        if len(hashes) > before:
            save_json(REFERENCE_PATH, {"built": datetime.now().isoformat(timespec="seconds"), "hashes": hashes})
        log(f"Reference set: {len(hashes)} creative hashes ({len(hashes) - before} new from {len(own_ads)} own ads in this scan)")
    if hashes:
        return hashes
    if apify is None:
        try:
            apify = Apify(load_token())
        except SystemExit:
            log("No Apify token and no cached reference set; visual matching skipped.")
            return {}
    v = cfg["visual"]
    urls = [{"url": page_ads_url(pid)} for pid in v["reference_page_ids"]]
    log(f"Downloading Bambora's own ads for the visual reference set ({len(urls)} page(s))...")
    items = apify.run_actor(cfg["actor"], {"startUrls": urls, "resultsLimit": v["reference_results_limit"],
                                           "activeStatus": ""})
    hashes, cache = {}, {}
    for rec in unwrap(items):
        ad = normalise(rec)
        for u, h in hash_urls(ad["images"], cache).items():
            hashes[h] = {"ad_id": ad["ad_id"], "url": u}
    save_json(REFERENCE_PATH, {"built": datetime.now().isoformat(timespec="seconds"), "hashes": hashes})
    log(f"Reference set built: {len(hashes)} creative hashes from {len(items)} own ads")
    return hashes


def visual_matches(ad, reference, cache, max_distance, per_ad_limit=6):
    hits = []
    for u, h in hash_urls(ad["images"], cache, limit=per_ad_limit).items():
        best = None
        for rh, meta in reference.items():
            d = hamming(h, rh)
            if d <= max_distance and (best is None or d < best[0]):
                best = (d, meta["ad_id"], u)
        if best:
            hits.append({"distance": best[0], "own_ad_id": best[1], "url": best[2]})
    return hits


# --------------------------------------------------------------------------- reporting

def write_reports(rows, stamp, cfg, digest=()):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = REPORT_DIR / f"{stamp}.csv"
    html_path = REPORT_DIR / f"{stamp}.html"

    fields = ["new", "evidence", "page_name", "page_url", "ad_url", "start", "active", "platforms",
              "brand_hits", "copy_hits", "visual_hits", "destination", "text", "images", "videos"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})

    def esc(s):
        return html.escape(str(s or ""))

    def links(urls, label):
        return " ".join(f'<a href="{esc(u)}" target="_blank">{label}{i + 1}</a>' for i, u in enumerate(urls))

    body_rows = []
    for r in rows:
        cls = "new" if r["new"] else ""
        body_rows.append(f"""
<tr class="{cls}">
  <td>{"NEW" if r["new"] else ""}</td>
  <td><b>{esc(r["evidence"])}</b><br><small>{esc(r["why"])}</small></td>
  <td><a href="{esc(r["page_url"])}" target="_blank">{esc(r["page_name"])}</a></td>
  <td><a href="{esc(r["ad_url"])}" target="_blank">{esc(r["ad_id"])}</a><br><small>{esc(r["start"])} {"active" if r["active"] else "inactive"}<br>{esc(r["platforms"])}</small></td>
  <td class="text">{esc(r["text"][:600])}</td>
  <td>{links(r["images_list"], "img")}<br>{links(r["videos_list"], "video")}<br><small>{esc(r["destination"][:80])}</small></td>
</tr>""")

    doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>Ads Library monitor {esc(stamp)}</title>
<style>
body{{font-family:system-ui,Segoe UI,Arial,sans-serif;margin:24px;color:#222}}
table{{border-collapse:collapse;width:100%;font-size:13px}}
th,td{{border:1px solid #ddd;padding:6px 8px;vertical-align:top;text-align:left}}
th{{background:#f3f3f3;position:sticky;top:0}}
tr.new{{background:#fff7e0}}
td.text{{max-width:420px;white-space:pre-wrap}}
small{{color:#666}}
</style></head><body>
<h1>Meta Ads Library monitor</h1>
<p>Run: {esc(stamp)} &middot; {len(rows)} flagged ad(s), {sum(1 for r in rows if r["new"])} new since last run.
Evidence: <b>brand</b> = brand term in ad text or page name, <b>copy</b> = Bambora copy phrase reused,
<b>visual</b> = creative matches one of Bambora's own ad images (lower distance = closer match).</p>
<p>Own pages excluded: {esc(", ".join(cfg.get("own_page_ids", [])))}. Open the ad link to view it in the Ad Library and note the ad ID for the DMCA form.</p>
<table><thead><tr><th></th><th>Evidence</th><th>Advertiser page</th><th>Ad</th><th>Ad text</th><th>Media / destination</th></tr></thead>
<tbody>{"".join(body_rows) if body_rows else '<tr><td colspan="6">Nothing flagged.</td></tr>'}</tbody></table>
<h2>Picture digest: {len(digest)} new baby-sling ad(s) from other pages</h2>
<p>Not flagged by the machine. Scroll and check whether any of them is the Bambora sling.</p>
<div class="grid">{"".join(
    f'<div class="card"><a href="{esc(a["ad_url"])}" target="_blank"><img src="{esc(a["images"][0]) if a["images"] else ""}" loading="lazy"></a>'
    f'<b>{esc(a["page_name"][:40])}</b><br><small>{esc(a["start"])}</small><br>'
    f'<a href="{esc(a["ad_url"])}" target="_blank">ad</a> {("&middot; <a href=%s target=_blank>store</a>" % chr(34) + esc(a["links"][0]) + chr(34)) if a["links"] else ""}</div>'
    for a in digest)}</div>
<style>.grid{{display:flex;flex-wrap:wrap;gap:12px}} .card{{width:200px;font-size:12px}} .card img{{width:200px;height:200px;object-fit:cover;border:1px solid #ddd}}</style>
</body></html>"""
    html_path.write_text(doc, encoding="utf-8")
    return csv_path, html_path


# --------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default=str(CONFIG_PATH))
    ap.add_argument("--from-json", help="score a saved dataset instead of calling Apify")
    ap.add_argument("--no-visual", action="store_true")
    ap.add_argument("--refresh-reference", action="store_true")
    ap.add_argument("--new-only", action="store_true")
    ap.add_argument("--estimate", action="store_true")
    ap.add_argument("--report-dir", help="override the reports folder")
    ap.add_argument("--state-dir", help="override the state folder (seen.json, reference hashes)")
    ap.add_argument("--slack", action="store_true", help="post a summary to the stored Slack webhook")
    ap.add_argument("--no-slack", action="store_true", help="never post, even if config enables it")
    ap.add_argument("--slack-preview", action="store_true", help="print the Slack payloads instead of posting")
    args = ap.parse_args()

    cfg = load_json(args.config, None)
    if cfg is None:
        sys.exit(f"Config not found: {args.config}")
    global REPORT_DIR, STATE_DIR, SEEN_PATH, REFERENCE_PATH, LAST_DATASET_PATH, DIGEST_SEEN_PATH
    if args.report_dir:
        REPORT_DIR = Path(args.report_dir)
    if args.state_dir:
        STATE_DIR = Path(args.state_dir)
        SEEN_PATH, REFERENCE_PATH = STATE_DIR / "seen.json", STATE_DIR / "reference_hashes.json"
        LAST_DATASET_PATH, DIGEST_SEEN_PATH = STATE_DIR / "last_dataset.json", STATE_DIR / "digest_seen.json"
    try:  # fresh log per run
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        (STATE_DIR / "last_run.log").write_text(f"=== run started {datetime.now().isoformat(timespec='seconds')} ===\n", encoding="utf-8")
    except OSError:
        pass

    plan = build_search_plan(cfg)
    per_search = cfg["results_limit_per_search"]
    cat_limit = cfg.get("category_results_limit", per_search)
    if args.estimate:
        n_cat = sum(1 for p in plan if p["kind"] == "category")
        worst = (len(plan) - n_cat) * per_search + n_cat * cat_limit
        ref = cfg["visual"]["reference_results_limit"] if cfg["visual"]["enabled"] and not args.no_visual else 0
        print(f"{len(plan) - n_cat} brand/copy searches x up to {per_search} ads + {n_cat} category searches x up to {cat_limit} ads")
        print(f"Worst case: {worst} ads (+{ref} reference ads on the first run or after --refresh-reference)")
        print(f"Worst-case Apify cost at ${PRICE_PER_AD_USD}/ad: ${worst * PRICE_PER_AD_USD:.2f} per run, ${ref * PRICE_PER_AD_USD:.2f} for the reference set")
        print("Real runs are usually far cheaper: exact-phrase brand and copy searches return few ads.")
        return

    slack_cfg = cfg.get("slack", {})
    slack_on = (args.slack or slack_cfg.get("enabled")) and not args.no_slack
    webhook = load_secret("slack_webhook", "SLACK_WEBHOOK_URL", required=False) if slack_on else ""

    def slack(text, blocks=None):
        """Post if a webhook is stored; with --slack-preview just print the payload."""
        if args.slack_preview:
            print("SLACK PREVIEW:", json.dumps({"text": text, "blocks": blocks}, ensure_ascii=False)[:1500])
            return
        if not slack_on:
            return
        if not webhook:
            log("Slack: no webhook stored (store-secret.ps1 -Name slack_webhook), not posting.")
            return
        try:
            post_to_slack(webhook, text, blocks)
            log("Slack: posted.")
        except Exception as e:
            log(f"Slack: post failed ({e}).")

    apify = None
    if args.from_json:
        items = load_json(args.from_json, [])
        log(f"Loaded {len(items)} records from {args.from_json}")
    else:
        try:
            apify = Apify(load_token())
        except SystemExit as e:
            slack(f"Ads Library monitor could not run: {e}")
            raise
        items = []
        # Category searches get their own (smaller) limit, so they run as a second actor call.
        groups = [([p for p in plan if p["kind"] != "category"], per_search),
                  ([p for p in plan if p["kind"] == "category"], cat_limit)]
        for urls, limit in groups:
            if not urls:
                continue
            log(f"Running {len(urls)} Ad Library searches (limit {limit} each) through {cfg['actor']}...")
            actor_input = {
                "startUrls": [{"url": p["url"]} for p in urls],
                "resultsLimit": limit,
                # The actor wants "" for "both"; the Ad Library URLs themselves still say active_status=all.
                "activeStatus": "" if cfg["active_status"] == "all" else cfg["active_status"],
            }
            if cfg.get("only_ads_newer_than"):
                actor_input["onlyAdsNewerThan"] = cfg["only_ads_newer_than"]
            try:
                items += apify.run_actor(cfg["actor"], actor_input)
            except Exception as e:
                msg = str(e)
                hint = (" The Apify free credit for this month is used up; it resets monthly, or upgrade the plan at console.apify.com."
                        if "hard limit" in msg or "usage" in msg.lower() else "")
                log(f"Apify run failed: {msg}")
                slack(f"Ads Library monitor: this week's scan did not run. Apify said: {msg[:300]}.{hint}")
                sys.exit(1)
        save_json(LAST_DATASET_PATH, items)
        log(f"Got {len(items)} ad records (raw copy saved to {LAST_DATASET_PATH.name})")

    url_kind = {p["url"]: (p["kind"], p["term"]) for p in plan}
    ads = {}
    for rec in unwrap(items):
        ad = normalise(rec)
        if not ad["ad_id"]:
            continue
        kind, term = url_kind.get(ad["search_url"], ("unknown", ""))
        entry = ads.setdefault(ad["ad_id"], {**ad, "found_by": []})
        entry["found_by"].append(f"{kind}:{term}" if term else kind)

    own = [a for a in ads.values() if is_own(a, cfg)]
    ignore_pages = set(cfg.get("ignore_page_ids", []))
    ignore_domains = set(cfg.get("ignore_domains", []))
    ignored = [a for a in ads.values() if not is_own(a, cfg) and (
        a["page_id"] in ignore_pages or any(link_domain(l) in ignore_domains for l in a["links"]))]
    candidates = [a for a in ads.values() if not is_own(a, cfg) and a not in ignored]
    log(f"{len(ads)} unique ads, {len(own)} are Bambora's own, {len(ignored)} ignored (known unrelated), {len(candidates)} to check")

    reference, cache = {}, {}
    do_visual = cfg["visual"]["enabled"] and not args.no_visual
    if do_visual:
        try:
            reference = build_reference(cfg, apify, force=args.refresh_reference, own_ads=own)
        except Exception as e:
            log(f"Visual reference set unavailable ({e}); continuing with text matching only.")
            do_visual = False

    seen = load_json(SEEN_PATH, {})
    now = datetime.now()
    rows = []
    for a in candidates:
        brand, copy_ = score_text(a, cfg)
        visual = visual_matches(a, reference, cache, cfg["visual"]["max_distance"]) if do_visual and reference else []
        if not (brand or copy_ or visual):
            continue
        evidence = "+".join(k for k, v in (("brand", brand), ("copy", copy_), ("visual", visual)) if v)
        why = "; ".join(
            ([f"brand term(s): {', '.join(brand)}"] if brand else [])
            + ([f"copy phrase(s): {', '.join(copy_)}"] if copy_ else [])
            + ([f"visual match to own ad {v['own_ad_id']} (distance {v['distance']})" for v in visual])
        )
        is_new = a["ad_id"] not in seen
        if is_new:
            seen[a["ad_id"]] = {"first_seen": now.strftime("%Y-%m-%d"), "page": a["page_name"], "evidence": evidence}
        if args.new_only and not is_new:
            continue
        rows.append({
            **a,
            "new": is_new,
            "evidence": evidence,
            "why": why,
            "brand_hits": ", ".join(brand),
            "copy_hits": ", ".join(copy_),
            "visual_hits": "; ".join(f"{v['own_ad_id']}@{v['distance']}" for v in visual),
            "destination": a["links"][0] if a["links"] else "",
            "images_list": a["images"],
            "videos_list": a["videos"],
            "images": " ".join(a["images"]),
            "videos": " ".join(a["videos"]),
        })

    order = {"brand+copy+visual": 0, "brand+visual": 1, "copy+visual": 2, "brand+copy": 3, "visual": 4, "brand": 5, "copy": 6}
    rows.sort(key=lambda r: (not r["new"], order.get(r["evidence"], 9), r["page_name"].lower()))

    # Picture digest: every new ad from the broad sling searches that was not flagged. A human decides
    # whether it is a lookalike of the Bambora sling; the machine cannot.
    digest_seen = load_json(DIGEST_SEEN_PATH, {})
    flagged_ids = {r["ad_id"] for r in rows}
    digest = [a for a in candidates
              if a["ad_id"] not in flagged_ids and a["ad_id"] not in digest_seen
              and any(k.startswith("category") for k in a["found_by"])]
    digest.sort(key=lambda a: (a["start"], a["page_name"].lower()), reverse=True)
    for a in digest:
        digest_seen[a["ad_id"]] = {"first_seen": now.strftime("%Y-%m-%d"), "page": a["page_name"]}
    save_json(DIGEST_SEEN_PATH, digest_seen)

    save_json(SEEN_PATH, seen)
    stamp = now.strftime("%Y-%m-%d_%H%M")
    csv_path, html_path = write_reports(rows, stamp, cfg, digest)

    log(f"Flagged {len(rows)} ad(s), {sum(1 for r in rows if r['new'])} new.")
    for r in rows[:25]:
        log(f"  {'NEW ' if r['new'] else '    '}{r['evidence']:<18} {r['page_name'][:40]:<40} {r['ad_url']}")
    if len(rows) > 25:
        log(f"  ... {len(rows) - 25} more in the report")
    log(f"Report: {html_path}")
    log(f"CSV:    {csv_path}")
    log(f"Picture digest: {len(digest)} new sling ad(s) for a human to look at.")

    slack(slack_summary(rows, stamp, slack_cfg.get("notify", "new")))
    if slack_cfg.get("digest", True):
        for text, blocks in slack_digest_messages(digest, stamp):
            slack(text, blocks)


if __name__ == "__main__":
    main()
