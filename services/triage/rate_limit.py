# rate_limit.py - Week 6 Monday, Lesson 6: a small per-user counter that
# answers "and how fast may you go?" — authentication (auth.py) only
# answers "who are you?". Fifteen lines, nothing hidden.
#
# NOTE on scaling: the counter lives in this process's memory. Run two
# copies of a service that imports this behind a load balancer and each
# copy enforces the limit independently — a caller gets roughly double the
# stated budget through. That is the same statelessness lesson as
# clinic_notes_api.py's in-memory NOTES dict; the production fix is a
# shared store (e.g. Redis), not a bigger local dict.

from __future__ import annotations

import time

from fastapi import HTTPException

WINDOW_SECONDS = 60
MAX_REQUESTS = 5
_counters: dict[str, list[float]] = {}


def check_rate_limit(username: str) -> None:
    """Allow at most MAX_REQUESTS per user per WINDOW_SECONDS. Raise 429 if exceeded."""
    now = time.time()
    # Dropping stale timestamps here (on the call path) instead of on a
    # timer is deliberate: the list only ever needs to be accurate at the
    # moment we are about to count, so cleaning happens exactly then — no
    # background thread, no lock, nothing that can silently drift.
    recent = [t for t in _counters.get(username, []) if now - t < WINDOW_SECONDS]
    if len(recent) >= MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Too many requests. Wait a minute and try again.")
    recent.append(now)
    _counters[username] = recent
