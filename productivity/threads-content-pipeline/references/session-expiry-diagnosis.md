# Threads Session Expiry — Diagnosis & Recovery

Verify 2026-08-22. The auto-poster cron (`youtube-scheduler.py` → `threads_poster.py`)
reported a confusing failure that turned out to be a plain expired session.

## Symptom

Cron delivery shows:

```
POSTER FAILED rc=1: ... playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 10000ms
```

The 10000ms timeout is `compose.wait_for(timeout=10000)` for
`[aria-label*="Type to compose"]` in `post_main()`.

## Root cause

The saved session cookies in `~/.hermes/threads_state.json` had expired. A logged-out
Threads **homepage does NOT land on /login** — the URL stays `https://www.threads.com/`.
So the poster's pre-check `if "login" in page.url.lower()` returns False and it proceeds
into the composer wait, which times out because the composer only exists when logged in.

This is why you must NOT trust the URL substring as the logged-in signal.

## Diagnose (read-only, posts nothing)

Run a short Playwright probe against the live page with the saved cookies and read the signs:

| Probe | Logged in | Logged out (expired) |
|-------|-----------|----------------------|
| `[aria-label*="Type to compose"]` count | 1 | 0 |
| `[contenteditable="true"]` count | 1+ | 0 |
| page body has "Log in"/"Sign up" button | no | yes |
| profile links `a[href*="/@ntquang1110"]` | many (your posts) | 0 (shows other users' posts) |

Diagnostic sketch (safe — only reads, never submits):

```python
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

state = json.load(open(Path.home() / ".hermes" / "threads_state.json"))
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context()
    ctx.add_cookies(state["cookies"])
    pg = ctx.new_page()
    pg.goto("https://www.threads.com", wait_until="domcontentloaded", timeout=30000)
    pg.wait_for_timeout(6000)
    print("URL:", pg.url)
    print("compose:", pg.locator('[aria-label*="Type to compose"]').count())
    print("contenteditable:", pg.locator('[contenteditable="true"]').count())
    print("my-post-links:", pg.evaluate("() => document.querySelectorAll('a[href*=\"/@ntquang1110\"]').length"))
    b.close()
```

`compose == 0` + `contenteditable == 0` + no user links  → session expired, not a selector
change and not a network hiccup.

## Fix

1. Re-login: `python threads_login.py` (reads `THREADS_CREDS_B64` from
   `~/AppData/Local/hermes/.env`, base64 `user:pass`; overwrites `threads_state.json`).
   On the first failure it may print a confusing backslash-mangled path when called with
   backslash paths through git-bash — use forward-slash paths and run the script from a
   neutral dir if the Hermes lifecycle guard interferes with the scripts-dir path.
2. Re-run the probe; `compose` must become 1.

## Catch-up of missed posts

The scheduler (`youtube-scheduler.py`) only marks an item `posted` on real success
(returncode 0 + a `https://www.threads.com` URL in stdout). On a session-expiry failure
it does NOT mark posted, so the overdue item stays `pending` and the schedule is consistent.

To catch up an overdue pending item after re-login:
1. Pull its `content` from `youtube-schedule.json`.
2. Write it to `temp_thread_post.txt` (UTF-8 via write_file/open).
3. Run `threads_poster.py --file <tempfile>`; confirm a post URL in stdout.
4. Flip that id's `status` to `posted` + set `posted_date`, bump `last_posted_date`, and
   `json.dump(..., ensure_ascii=False)` back to `youtube-schedule.json`.

## Hardening applied 2026-08-22

`threads_poster.py` `main()` now checks composer presence AFTER the URL check, waits 4s for
late render, and if still absent prints `"Session expired: no composer visible (need
re-login via threads_login.py)."` and exits 1 — a clear signal instead of a 10s timeout.
