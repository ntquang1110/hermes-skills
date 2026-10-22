# Threads Playwright Automation Reference

## Login Flow (one-time)

Navigate to `threads.com/login` (not threads.net). The login form uses:

- `input[placeholder="Username, phone or email"]` — username field
- `input[placeholder="Password"]` — password field
- `div[role="button"]:has-text("Log in")` — login button (not `input[type="submit"]` which is hidden)
- After login, Instagram auth redirect may appear. Click "Continue"/"Save"/"Confirm" buttons if present.
- Save cookies to `~/.hermes/threads_state.json`

## Posting Flow

### Post Main (Part 1)

1. Go to threads.com
2. Click `[aria-label*="Type to compose"]` (the "What's new?" button)
3. Wait for `[contenteditable="true"]` to appear
4. Click and `fill(text)`
5. Submit with `press("Control+Enter")` — DO NOT click the Post button (unreliable)

### Get Post URL

After posting, navigate to `threads.com/@ntquang1110` and get the first `a[href*="/@ntquang1110/post/"]` link.

### Post Reply (Parts 2+)

1. Navigate to the main post URL
2. Click `div[role="button"]:has-text("Reply")` — use Playwright's `click()`, not JS `dispatchEvent()`
3. Wait for `[contenteditable="true"]` to appear (count >= 1 or >= 2)
4. On second+ reply, the editor may be hidden (visible=False but exists in DOM). Fix:

```python
# Make editor visible via JS before fill()
page.evaluate("""() => {
    const editors = document.querySelectorAll('[contenteditable="true"]');
    if (editors.length === 0) return;
    const editor = editors[editors.length - 1];
    editor.style.position = 'static';
    editor.style.opacity = '1';
    editor.style.visibility = 'visible';
    editor.style.display = 'block';
    editor.style.width = '500px';
    editor.style.height = '100px';
}""")
```

5. Then use Playwright `click(force=True)` + `fill(text)` + `press("Control+Enter")`

### Reply Editor: use keyboard.type, NOT fill() (Lexical editor)

DISCOVERED 2026-07-24: Threads uses the Lexical editor for replies. `fill()`, `evaluate(textContent)`, and JS make-visible do NOT reliably register text in the reply box — the post can confirm "Posted!" while content never lands, or text silently drops.

The method that WORKS for replies (empirically verified, 17/17 backlog posts):

```python
# Click Reply, wait for contenteditable, then:
editor.click(force=True)
page.keyboard.type(text, delay=5)   # delay=5 is critical; delay=0 drops characters
page.keyboard.press("Control+Enter")
```

- `keyboard.type(delay=5)` is the reliable path for reply editor. `fill()` is OK for the MAIN compose box only.
- For the main post (part 1): `fill()` + `Ctrl+Enter` works fine.
- Keep the JS make-visible step only as a fallback when the editor is hidden; prefer keyboard typing over fill for replies.
- After posting, always verify on the profile that the reply text actually appears (silent content-drop is the classic failure mode).

### Reply Button Behavior

- On first reply attempt: clicking Reply opens a visible editor. `editors[-1]` maps to the reply box.
- On subsequent replies: clicking Reply opens a hidden editor (exists in DOM but `visible=False`). Must make visible via JS.
- After posting a reply, the page stays on the same URL (no redirect).

## Common Failures and Fixes

| Problem | Symptom | Fix |
|---------|---------|-----|
| Post button not working | "Posted!" but no post appears | Use Ctrl+Enter instead |
| Editor not found (2nd reply) | `Visible editors: 0` after Reply click | Check DOM for hidden editor, make visible via JS |
| Session expired | Redirected to login page | Re-run threads_login.py |
| fill() fails on hidden element | `element is not visible` | Use `force=True` on click, make visible via JS |
| Ctrl+Enter doesn't submit | Page stays, no new post created | Try clicking the visible Post button |
| Reply confirmed but content missing | evaluate sets textContent but React doesn't register | Use `keyboard.type(text, delay=5)` on the reply editor — do NOT use fill()/evaluate for replies (Lexical) |

## Key Selectors

| Element | Selector |
|---------|----------|
| Compose button | `[aria-label*="Type to compose"]` |
| Text editor | `[contenteditable="true"]` |
| Reply button | `div[role="button"]:has-text("Reply")` |
| Login username | `input[placeholder="Username, phone or email"]` |
| Login password | `input[placeholder="Password"]` |
| Profile posts | `a[href*="/@ntquang1110/post/"]` |
