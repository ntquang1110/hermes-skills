# Threads Posting Mechanism — Lexical Editor Workarounds

> Threads web uses Meta's **Lexical** editor framework. Different input areas accept different input methods. Using the wrong one causes SILENT FAILURE: the script prints "Posted!" but content NEVER appears.

## Editor Compatibility Matrix

| Editor Type | Input Method | Works? | Notes |
|-------------|-------------|--------|-------|
| Main composer (visible on /) | `editor.fill(text)` | ✅ ALWAYS | Then `Ctrl+Enter` to submit |
| Main composer | `page.evaluate(textContent)` | ❌ | Silent failure |
| Main composer | `keyboard.type(delay=5)` | ✅ but slow | Use fill() instead |
| Reply editor | `keyboard.type(text, delay=5)` | ✅ ALWAYS | Delay=5 is CRITICAL — without delay, characters get swallowed |
| Reply editor | `editor.fill(text)` | ❌❌ | Lexical IGNORES fill on reply editors — this is the #1 bug |
| Reply editor | `page.evaluate(textContent + dispatchEvent)` | ❌ | Also ignored by Lexical |

## The Fix History (why this matters)

This bug consumed ~50 iterations and 3+ days of debugging. The root cause was subtle:

1. **fill() works on the main composer** because it's a visible, primary input
2. **fill() silently fails on reply editors** — Lexical's reply component doesn't register Playwright fill() events
3. **evaluate(textContent) also fails** — dispatching input/change events isn't enough for Lexical
4. **keyboard.type(delay=5) works** — typing character-by-character triggers the correct React/Lexical event chain

**Lesson learned**: Never assume fill() works everywhere. Always test with keyboard.type() as fallback for different editor instances.

## Post Flow (verified working)

### Main Post
```python
compose = page.locator('[aria-label*="Type to compose"]').first
compose.click()
page.wait_for_timeout(2000)
editor = page.locator('[contenteditable="true"]').first
editor.fill(text)
page.wait_for_timeout(500)
page.keyboard.press("Control+Enter")
page.wait_for_timeout(5000)
```

### Reply
```python
reply_btn = page.locator('div[role="button"]:has-text("Reply")').first
reply_btn.click()
page.wait_for_timeout(4000)
# CRITICAL: Use keyboard.type, NOT fill
page.keyboard.type(text, delay=5)
page.wait_for_timeout(500)
page.keyboard.press("Control+Enter")
page.wait_for_timeout(5000)
```

## Verification (BAT BUOC)

After posting, ALWAYS verify by navigating to the post URL or checking the profile:
```python
page.goto(profile_url)
# Look for key phrases from the posted content
if "key_phrase" in page.text_content("body"):
    print("CONFIRMED")
else:
    print("NOT FOUND — likely silent failure")
```

## Reply composer must be OPEN before typing (2026-08-24, burned a thread)

A reply-editor fail that repeats *identically* for the same post is usually NOT transient flake — it means the reply composer isn't actually open/focused, so `type()` goes nowhere.

- On a thread page the reply `contenteditable` exists hidden/low in the DOM. Clicking it directly fails with `Locator.click: Element is outside of the viewport`.
- **You must click a Reply button first** (`div[role="button"]:has-text("Reply")`) to open the composer, which then materializes the *visible* editor to type into. Then scroll, focus the editor, verify text landed.
- Per-post **verify the text landed** before submitting: read back `contenteditable` innerText and compare the first ~20 chars. Submit only on match.

## 🔴 Dangerous retry anti-pattern: pressing Enter/Ctrl+Enter "to activate the editor" (2026-08-24)

When a reply keeps failing, DO NOT "help" the editor by sending `keyboard.press("Enter")` (or extra `Ctrl+Enter`) before typing — and never submit unless text is verified in the editor.

That extra Enter/Ctrl+Enter submits an *empty* (or half-typed) reply as a **NEW STANDALONE POST**, xé (splitting) the thread into fragments. Seen live: retrying one failed reply with an `append_reply` variant that pressed Enter first turned thread `DcarQIyESr6` (Cô đơn ở đỉnh) into 11 containers — 7 junk standalone fragments of the same sentence.

The ORIGINAL `fill_reply` guard is the safe pattern: it clicks/focuses editor, `keyboard.type(delay>=5)`, reads back, and returns False (abort) if the first 25 chars didn't match — it never submits on unknown state. Keep that guard; do not "improve" it by adding raw Enter presses.

If a reply fails after 1-2 honest retries, STOP and report it to the user. Do not keep spawning new retry scripts. When a thread gets xé, headless DELETE does not persist reliably on Threads (script reports deleted, reload shows containers still present) → tell the user to delete the orphan thread from the app (deleting the root post removes the whole thread).

## Session Cookie Persistence

- Login once via `threads_login.py` saves cookies to `~/.hermes/threads_state.json`
- Scripts must `context.add_cookies(state["cookies"])` at startup
- If redirected to login page on load, session expired → re-run login
- Cron jobs use the same cookie file
