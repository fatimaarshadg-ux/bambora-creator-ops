"""Polite HTTP: per-host rate limiting, adaptive backoff, and a circuit breaker.

The goal here is to never become a problem for the services this tool reads
from. That is partly courtesy — Arctic Shift and PullPush are volunteer-run
archives that nobody is paying for — and partly self-interest, because a
client that backs off when asked keeps working, while one that hammers through
429s gets blocked and stays blocked.

Three mechanisms, in increasing order of severity:

  throttle       a minimum gap between requests to the same host
  adaptive delay when a host signals overload, that gap widens for the rest of
                 the session and only narrows again after sustained success
  circuit break  after repeated failures a host is left alone entirely for a
                 cooldown, so a struggling service is not kept under load

What this deliberately does NOT do is rotate user agents, cycle proxies, or
otherwise disguise the client. Those techniques exist to defeat blocking
rather than to avoid causing it, they violate the terms of every service
involved, and in practice they escalate a temporary rate limit into a
permanent ban. Identifying honestly and slowing down is both the ethical
option and the one that keeps working.
"""
from __future__ import annotations

import gzip
import json
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_DELAY = 1.1
DEFAULT_RETRIES = 4

# How far the adaptive delay is allowed to stretch before we conclude the host
# simply does not want our traffic right now.
MAX_DELAY = 20.0
BREAKER_THRESHOLD = 6      # consecutive failures before a host is cut off
BREAKER_COOLDOWN = 120.0   # seconds to leave it alone

UA = "voc-miner/0.1 (personal customer-research script; +stdlib urllib)"

_last_hit = {}
_extra_delay = {}
_fail_streak = {}
_blocked_until = {}


class FetchError(Exception):
    def __init__(self, status, url, body=""):
        self.status = status
        self.url = url
        self.body = body
        # A bare "HTTP -2 for host" tells the reader nothing actionable, and
        # these errors surface directly in run output.
        if status == -2:
            super().__init__(body or "host temporarily unavailable")
        elif status == 422:
            super().__init__("archive overloaded (422) — retry shortly")
        elif status == 429:
            super().__init__("rate limited (429) — retry shortly")
        else:
            super().__init__("HTTP %s for %s" % (status, url))


class CircuitOpen(FetchError):
    """Raised when a host has been failing enough that we stop contacting it."""


def host_status():
    """Snapshot of what the throttler currently believes about each host."""
    out = {}
    now = time.time()
    for h in set(list(_last_hit) + list(_extra_delay) + list(_blocked_until)):
        out[h] = {
            "extra_delay": round(_extra_delay.get(h, 0.0), 2),
            "fail_streak": _fail_streak.get(h, 0),
            "cooling_off_for": max(0, round(_blocked_until.get(h, 0) - now)),
        }
    return out


def _throttle(host, delay):
    wait_until = _blocked_until.get(host, 0)
    if wait_until > time.time():
        secs = int(wait_until - time.time())
        raise CircuitOpen(
            -2, host,
            "%s is being left alone for another %ds after repeated failures "
            "— it is overloaded, not broken; retry shortly" % (host, secs),
        )
    gap = delay + _extra_delay.get(host, 0.0)
    prev = _last_hit.get(host)
    if prev is not None:
        wait = gap - (time.time() - prev)
        if wait > 0:
            time.sleep(wait)
    _last_hit[host] = time.time()


def _punish(host, retry_after=None):
    """A host pushed back: widen its gap and count the failure."""
    streak = _fail_streak.get(host, 0) + 1
    _fail_streak[host] = streak
    cur = _extra_delay.get(host, 0.0)
    bump = float(retry_after) if retry_after else max(0.75, cur * 0.6 + 0.75)
    _extra_delay[host] = min(MAX_DELAY, cur + bump)
    if streak >= BREAKER_THRESHOLD:
        _blocked_until[host] = time.time() + BREAKER_COOLDOWN
        _fail_streak[host] = 0
        sys.stderr.write(
            "  [%s] too many failures in a row — pausing this host for %ds\n"
            % (host, int(BREAKER_COOLDOWN))
        )


def _reward(host):
    """Sustained success slowly returns the host to normal speed."""
    _fail_streak[host] = 0
    cur = _extra_delay.get(host, 0.0)
    if cur > 0:
        _extra_delay[host] = max(0.0, cur - 0.15)


def fetch(url, headers=None, data=None, delay=DEFAULT_DELAY,
          retries=DEFAULT_RETRIES, timeout=45):
    """GET (or POST when data is given) with backoff. Returns decoded body text."""
    host = urllib.parse.urlparse(url).netloc
    hdrs = {"User-Agent": UA, "Accept-Encoding": "gzip", "Accept": "application/json"}
    if headers:
        hdrs.update(headers)

    body = None
    if data is not None:
        body = urllib.parse.urlencode(data).encode() if isinstance(data, dict) else data

    last = None
    for attempt in range(retries + 1):
        _throttle(host, delay)
        req = urllib.request.Request(url, data=body, headers=hdrs)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                if resp.headers.get("Content-Encoding") == "gzip":
                    raw = gzip.decompress(raw)
                _reward(host)
                return raw.decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            last = e
            detail = ""
            try:
                raw = e.read()
                # Error bodies honour Accept-Encoding too. Skipping this made
                # every failure message from these APIs render as binary noise,
                # which is a miserable way to debug a run at 2am.
                if e.headers and e.headers.get("Content-Encoding") == "gzip":
                    try:
                        raw = gzip.decompress(raw)
                    except (OSError, EOFError):
                        pass
                detail = raw.decode("utf-8", errors="replace")[:400]
            except Exception:
                pass
            # 429/5xx are transient, and arctic-shift returns 422 "Timeout.
            # Maybe slow down" under load. Back off on those. Everything
            # else is a real answer from the server, so stop and surface it.
            if e.code in (422, 429, 500, 502, 503, 504):
                # A server that tells us how long to wait knows better than
                # any formula we could invent, so prefer Retry-After.
                ra = e.headers.get("Retry-After") if e.headers else None
                try:
                    ra = float(ra) if ra else None
                except (TypeError, ValueError):
                    ra = None
                _punish(host, ra)
                if attempt < retries:
                    sleep_for = ra if ra else min(60, (2 ** attempt) * 2) + random.uniform(0, 1.5)
                    sys.stderr.write(
                        "  [%s] HTTP %d, backing off %.1fs (attempt %d/%d)\n"
                        % (host, e.code, sleep_for, attempt + 1, retries)
                    )
                    time.sleep(sleep_for)
                    continue
            raise FetchError(e.code, url, detail)
        except (urllib.error.URLError, TimeoutError) as e:
            last = e
            _punish(host)
            if attempt < retries:
                time.sleep(min(30, (2 ** attempt) * 2))
                continue
            raise FetchError(0, url, str(e))
    raise FetchError(0, url, str(last))


def fetch_json(url, **kw):
    txt = fetch(url, **kw)
    try:
        return json.loads(txt)
    except ValueError:
        raise FetchError(-1, url, "non-JSON response: " + txt[:300])


def qs(base, **params):
    """Build a URL, dropping None values."""
    clean = {k: v for k, v in params.items() if v is not None and v != ""}
    return base + ("&" if "?" in base else "?") + urllib.parse.urlencode(clean)
