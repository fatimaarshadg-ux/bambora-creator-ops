"""Credential loading that works in every context, not just your terminal.

Shell config files are the obvious place to put an API key, and they are the
wrong one for a tool you might schedule: `~/.zshrc` is read by interactive
shells only, so a command that works when you type it silently loses its
credentials under cron, a launchd job, or any script. That failure is
particularly nasty because the tool keeps running — it just quietly drops the
sources it can no longer authenticate.

So the environment is checked first (it still wins, which keeps one-off
overrides easy), and a config file is the fallback that works everywhere.
"""
from __future__ import annotations

import os

CONFIG_PATHS = [
    os.path.expanduser("~/voc-data/credentials.env"),
    os.path.expanduser("~/.voc-miner.env"),
]

_cache = None


def _load_file():
    """Parse simple KEY=value lines. Quotes optional, # comments ignored."""
    global _cache
    if _cache is not None:
        return _cache
    _cache = {}
    for path in CONFIG_PATHS:
        if not os.path.exists(path):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k = k.strip().lstrip("export ").strip()
                    v = v.strip().strip('"').strip("'")
                    if k and v and k not in _cache:
                        _cache[k] = v
        except OSError:
            continue
    return _cache


def get(name, default=None):
    """Environment first, then the config file."""
    val = os.environ.get(name)
    if val:
        return val
    return _load_file().get(name, default)


def where(name):
    """Report where a credential came from, for diagnostics."""
    if os.environ.get(name):
        return "environment"
    if _load_file().get(name):
        for p in CONFIG_PATHS:
            if os.path.exists(p):
                return p
    return None
