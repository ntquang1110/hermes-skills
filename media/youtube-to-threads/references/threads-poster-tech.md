# Threads Poster — Technical Reference

## Login Setup

### Credentials
Stored in `.env` as `THREADS_CREDS_B64=<base64(username:password)>`
Encoding: `echo -n "user:pass" | base64 -w0`

### Login Script
`~/AppData/Local/hermes/scripts/threads_login.py`

Flow:
1. Open `https://www.threads.com/login` (note: `.com` not `.net`)
2. Fill `input[placeholder="Username, phone or email"]`
3. Fill `input[placeholder="Password"]`
4. Click `div[role="button"]:has-text("Log in")` (not `input[type="submit"]` — it's hidden)
5. Handle post-login dialogs: "Save info", "Not Now", "Turn on"
6. Save cookies to `~/.hermes/threads_state.json`

### Cookie Storage
- Path: `~/.hermes/threads_state.json`
- Format: `{"cookies": [...], "username": "..."}`
- Session lasts days/weeks, then needs refresh
- CRON WARNING: When session expires, the scheduler silently returns empty output. Add login check before posting.

## Duplicate Tracking

File: `C:\Users\NTQUANG_DELL\AppData\Local\hermes\cache\youtube-processed.json`

```json
{"video_ids": ["YfQ7gm81WbQ", ...], "urls": ["https://youtu.be/...", ...]}
```

Extract video ID: `(?:v=|youtu\.be/|shorts/|embed/|live/)([a-zA-Z0-9_-]{11})`

## Poster Script — Key Technical Details

### Location
- Working copy: `~/AppData/Local/hermes/scripts/threads_poster.py`
- Cron copy: `~/.hermes/scripts/threads_poster.py`

### Lexical Editor — fill() vs textContent (CRITICAL)
Threads uses Facebook's Lexical editor. It has a critical quirk:
- **Playwright `fill()` WORKS** — dispatches proper React synthetic events
- **`el.textContent = t` + `dispatchEvent(new Event('input'))` FAILS** — Lexical ignores textContent changes because it manages its own internal state tree. The text appears in the DOM but React/Lexical doesn't register it, so when Ctrl+Enter is pressed, the post is empty.
- **`editor.evaluate("el => el.textContent = ...")` FAILS** — same reason
- Always use Playwright's native `fill()` method.

### Submit: Ctrl+Enter, NOT Post button
- `editor.press("Control+Enter")` reliably submits the post
- The Post button (`div[role="button"]:has-text("Post")`) conflicts with "Repost" and "Post Options". Clicking it is unreliable even with force=True because overlays intercept pointer events.

### Hidden Editor Fix
After posting 1+ replies, navigating back to the post and clicking Reply creates a `[contenteditable="true"]` element that exists in DOM but is NOT visible (rendered off-screen via CSS/React). Playwright's `fill()` won't work on hidden elements.

Fix — make it visible via JS before fill():
```python
editor = page.locator('[contenteditable="true"]').all()[-1]
page.evaluate("(el) => { el.style.position='static'; el.style.opacity='1'; el.style.visibility='visible'; el.style.display='block'; el.style.width='500px'; el.style.height='auto'; el.style.minHeight='40px'; }", editor)
editor.fill(text)
```

### Content Split — 500-char Limit
Threads limits posts to ~500 chars. Split content into parts:
```python
MAX_LENGTH = 500
parts = []
for block in text.split("\n\n"):
    block = block.strip()
    if not block: continue
    if not parts or len(parts[-1]) + len(block) + 2 > MAX_LENGTH:
        if len(block) > MAX_LENGTH:
            # Split long single-paragraph blocks by sentence
            sents = re.split(r'(?<=[.!?])\s+', block)
            chunk = ""
            for s in sents:
                if len(chunk) + len(s) + 1 <= MAX_LENGTH:
                    chunk = (chunk + " " + s).strip()
                else:
                    if chunk: parts.append(chunk)
                    chunk = s
            if chunk: parts.append(chunk)
        else:
            parts.append(block)
    else:
        parts[-1] += "\n\n" + block
```
**Key**: Simple `split("\n")` or `split("\n\n")` fails when content has no newlines (single paragraph). Always have a sentence-splitting fallback.

### Post URL Detection (Unreliable)
After posting, the script navigates to the profile and takes the first `a[href*="/@ntquang1110/post/"]` link. This is unreliable because:
- Test posts or previous posts may be first (newer)
- Empty/failed posts still generate a URL

A more robust approach: embed a unique marker in the content and search for it on the profile page.

### Reply Editor — keyboard.type() Required (CRITICAL FINDING)

The reply editor on a Threads post page has a **different behavior** than the main composer. This was discovered after hours of debugging and multiple script versions:

- **Main composer**: `editor.fill(text)` WORKS. Lexical accepts Playwright's fill() events.
- **Reply editor**: `editor.fill(text)` FAILS silently. Text appears to fill but doesn't register in Lexical's state tree — the post submits empty.
- **Reply editor**: `evaluate(el => el.textContent = t)` ALSO FAILS — same reason.
- **Reply editor**: `page.keyboard.type(text, delay=5)` WORKS. Typing character-by-character triggers the correct React/Lexical event handlers.

**UPDATE 2026-07-26**: There are now 3 editors on a post page with replies:
1. Main post composer (hidden off-screen, visible=False, width=0)
2. First reply editor (actual reply area, visible=True after clicking Reply)  
3. Second reply editor for subsequent replies

When `editors.count()` returns 2+, always use `editors[-1]` (last one). The first is the off-screen main composer.

**Implementation for reply (FINAL — keyboard.type() is the ONLY working method):**
```python
def fill_reply(page, text):
    editors = page.locator('[contenteditable="true"]').all()
    if not editors: return False
    editor = editors[-1]  # Last one = reply editor
    try:
        editor.click(force=True)
    except:
        page.evaluate("() => {const e=document.querySelectorAll('[contenteditable=\"true\"]'); if(e.length) e[e.length-1].focus();}")
    page.wait_for_timeout(500)
    # Clear existing text via evaluate (keyboard.selectAll+delete is slower)
    page.evaluate("""() => {
        const e=document.querySelectorAll('[contenteditable="true"]');
        if(e.length) e[e.length-1].textContent = '';
    }""")
    page.wait_for_timeout(200)
    # Type character by character — only reliable method for Lexical
    page.keyboard.type(text, delay=5)
    page.wait_for_timeout(500)
    return True
```

**Combined flow (main + replies):**
1. Main composer: `fill()` → `Ctrl+Enter` ✅
2. Reply editor: `click(force=True)` → `clear via evaluate` → `keyboard.type(delay=5)` → `Ctrl+Enter` ✅

### FIX 2026-08-17 — Broken reply chains (orphan posts + reversed order)

Symptoms user reported: recent posts split into multiple standalone short posts
("post đứng riêng lẻ, cụt ngủn") + reply order wrong. Confirmed on Becky Kennedy
(16-08) and Lisa Genova (15-08): each was torn into 3-4 separate threads with
orphan snippets and duplicated mains.

Root causes + fixes in `threads_poster.py`:
1. **Unreliable `links[0]` on profile**: after posting main, profile may not have
   loaded the new post → script replied to an OLD post. FIX: capture post URL via
   `page.wait_for_url(re.compile(r'/post/[A-Za-z0-9_-]{6,}'))` after Ctrl+Enter
   (Threads redirects to the new thread), fallback = diff old vs new IDs.
2. **Scheduler timeout=300s too short**: 29-part posts take >5 min; subprocess
   killed mid-chain → partial posts, item not marked posted → re-ran next day =
   DUPLICATE threads. FIX: `timeout=1800` in `youtube-scheduler.py`.

**CRITICAL LESSON — do NOT "improve" the reply editor logic.** The original
reply flow (goto post_url → scroll bottom → click first `div[role=button]:has-text("Reply")`
→ force-show LAST contenteditable → `keyboard.type(delay=5)` → Ctrl+Enter) is
CORRECT. Two attempted "fixes" both broke it and caused NESTED replies:
- Clicking the "Reply to <user>..." placeholder text: works for reply #1 but after
  that it opens the reply editor of the LAST reply → nested chain.
- Filtering editors by `is_visible()`: reply editor is rendered width=0 (hidden),
  so `is_visible()` returns false and "No visible editor found" drops the reply.
Stick with force-show-by-index + keyboard.type, always target `editors[-1]`.

Post-page menu items are `div[role="menuitem"]`, NOT `div[role="button"]`.
To delete a post programmatically: click the right-edge (x>860) empty button →
click `div[role="menuitem"]:has-text("Delete")` → confirm in `div[role="dialog"]`.
Working deleter: `threads_cleanup_tests.py`.

Post-page menu items are `div[role="menuitem"]`, NOT `div[role="button"]`.
Deleting a post programmatically: click the right-edge (x>860) empty button to
open menu → click `div[role="menuitem"]:has-text("Delete")` → confirm in
`div[role="dialog"]`. See `threads_cleanup_tests.py` for a working deleter.

### Scheduler Behavior
`youtube-scheduler.py` (cron, no_agent=true):
1. Reads schedule JSON
2. Finds pending item with scheduled_date <= today
3. Writes content to temp file
4. Calls threads_poster.py --file temp.txt
5. Marks item as posted (EVEN IF replies fail — main post priority)

**IMPORTANT: Silent session expiry.** When `threads_state.json` cookies expire, the scheduler returns exit code 0 with empty output. NO error is raised. Items continue to be marked as "posted" in the schedule even though nothing was actually posted. Add a session-validity check: verify `page.url` doesn't contain "login" after restoring cookies. If expired, skip posting and alert the user.

## Queue File
`C:\Users\NTQUANG_DELL\AppData\Local\hermes\cache\youtube-schedule.json`

Stats file: `C:\Users\NTQUANG_DELL\AppData\Local\hermes\cache\youtube-stats.json`

## Cron Jobs

| Name | Schedule | Function |
|------|----------|----------|
| Daily Research | `0 6 * * *` | Auto-research, summarize (agent-driven) |
| Schedule Poster | `0 20 * * *` | Post queue to Threads (no_agent script) |
