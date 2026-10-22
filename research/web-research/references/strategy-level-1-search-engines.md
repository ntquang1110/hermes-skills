# Strategy hierarchy — Level 1: search-engine fallbacks (delegate_task / DDG Lite / curl / Bing / Playwright)

### Level 1: Direct search via delegate_task (FIRST — when available)

If you have the `delegate_task` tool available, use it with the `web` toolset:

```
delegate_task(
    goal="Tìm kiếm: [your search query]",
    toolsets=["web", "search", "terminal"]
)
```

The web toolset in delegate_task has proper search access that bypasses most CAPTCHA blocks. **Note:** `delegate_task` is not available in all environments. If absent, skip directly to Level 1a.

### Level 1a: DuckDuckGo Lite (Python urllib) — FIRST PROBE (expect CAPTCHA)

**⚠️ As of mid-2026, DDG Lite consistently returns CAPTCHA pages rather than search results.** Try it as a quick probe, but expect to fall through to Level 2a. The code below is preserved for the rare case it works, and as a reference for the scraping pattern.

DDG Lite (`https://lite.duckduckgo.com/lite/`) returns raw HTML results without JavaScript when it works. Use the full HTML output to detect CAPTCHAs early:

**Complete working pattern (with CAPTCHA detection):** `scripts/ddg_lite_search.py` — `ddg_search(query)` returns `{'captcha': bool, 'results': [{title, url, snippet}]}`, detecting the `anomaly-modal` CAPTCHA page early; `batch_search(queries)` paces with `time.sleep(2)` between queries to avoid DDG Lite's silent rate-limiting (~4-6 rapid queries → 0 results, no error).

**Query limits:** DDG Lite struggles with very long queries (>80 chars). Keep queries short and specific (3-6 words). Multi-word phrases work best. If a query returns zero results, shorten it — it's likely hitting the length limit, not missing results.

**Site-specific search gaps:** DDG Lite has poor coverage of certain platforms:
- `site:t.me` — almost no Telegram groups indexed (most scam groups are private). Expect 0 results.
- `site:threads.net` — barely indexed by DDG. Expect 0 results.
- `site:x.com` and `site:twitter.com` — works fairly well for Vietnamese scam posts. Post text visible in snippets.
- `site:facebook.com` — DDG returns only public Pages, not individual posts or groups.

For Telegram/Threads research, fall back to Level 2 (direct URL access) or skip — these platforms are not searchable via DDG Lite.

### Level 1b: Terminal curl as quick probe

For a quick check without Python, use `terminal` with `curl` against DDG Lite:

```bash
curl -sL --max-time 15 \
  -d "q=YOUR_SEARCH_TERMS" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  "https://lite.duckduckgo.com/lite/" 2>/dev/null | grep -oP 'class="result-link">.*?</a>' | head -5
```

### Level 1c: Bing fallback (less reliable)

If DDG Lite fails, try Bing. Bing is sometimes less aggressive at blocking than Google, but often returns poor relevance:

```bash
curl -sL --max-time 15 \
  "https://www.bing.com/search?q=URL_ENCODED_QUERY" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  -H "Accept-Language: vi-VN,vi;q=0.9" | sed 's/<[^>]*>//g' | ...
```

**⚠️ Known issue:** Bing frequently returns dictionary definitions, product pages, or unrelated results instead of actual search results for multi-word queries. Parse carefully.

### Level 1d: Playwright browser automation (BEST fallback for social-media search)

When curl/urllib-based search methods fail (CAPTCHA, 404, rate-limit), Playwright automates a real Chromium browser that looks like a genuine user. This bypasses most anti-bot detection and works for platforms that block HTTP-only scrapers.

**Prerequisites (Windows git-bash):**
```bash
pip install playwright
python -m playwright install chromium
```

**Check if already installed:**
```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    print(p.chromium.executable_path)  # prints path if available
```

**Stealth config (required — bare headless is detected by most sites):**
```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-blink-features=AutomationControlled']
    )
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        viewport={'width': 1280, 'height': 720},
    )
    page = context.new_page()
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
    """)
```

**Platform matrix (tested Jul 2026):**

| Platform | Works? | Method | Notes |
|----------|--------|--------|-------|
| **YouTube** | ✅ Full | `page.goto('https://www.youtube.com/results?search_query=...')` | 20+ results. Extract with `eval_on_selector_all('ytd-video-renderer', ...)` |
| **Bing News** | ✅ Full | `page.goto('https://www.bing.com/news/search?q=...&setlang=vi')` | 15-20 headlines. Extract with `eval_on_selector_all('a.title', ...)` |
| **Reddit (www)** | ✅ Partial | `page.goto('https://www.reddit.com/r/subreddit/search/?q=...')` | Visible text extracts, but full post data needs PRAW API |
| **TikTok** | ❌ Blocked | `page.goto('https://www.tiktok.com/search?q=...')` | Returns "Sorry, something wrong with the server" even with stealth |
| **Facebook** | ❌ Blocked | `page.goto('https://www.facebook.com/search/...')` | Returns empty page (48 chars) or login wall |
| **X/Twitter** | ❌ Blocked | Nitter or direct | Nitter frontends are also mostly dead; X login wall |
| **DuckDuckGo** | ❌ Captcha | Every endpoint | All DDG endpoints (lite/html) serve captcha to headless browsers |
| **Google News** | ⚠️ Limited | `news.google.com/search?q=...` | 0 results from Playwright; better via Bing News |

**YouTube data extraction pattern:**
```python
page.goto('https://www.youtube.com/results?search_query=' + query.replace(' ', '+'), timeout=25000)
page.wait_for_timeout(3000)
videos = page.eval_on_selector_all('ytd-video-renderer', """els => els.map(el => {
    const t = el.querySelector('#video-title');
    const c = el.querySelector('#channel-name');
    const m = el.querySelector('#metadata-line');
    return {
        title: t?.textContent?.trim() || '',
        url: t?.href || '',
        channel: c?.textContent?.trim().replace(/\\s+/g,' ') || '',
        meta: m?.textContent?.trim().replace(/\\s+/g,' ') || '',
    }
})""")
for v in videos[:10]:
    print(f"{v['title'][:80]}")
    print(f"{v['url']}")
```

**Bing News extraction pattern:**
```python
page.goto(f'https://www.bing.com/news/search?q={query.replace(" ","+")}&setlang=vi', timeout=15000)
page.wait_for_timeout(2000)
titles = page.eval_on_selector_all('a.title', """els => els.map(el => ({
    t: el.textContent?.trim() || '',
    u: el.href || ''
}))""")
for t in titles[:5]:
    print(f"{t['t'][:80]}")
    print(f"{t['u']}")
```

**Reddit (www) extraction pattern:**
```python
page.goto(f'https://www.reddit.com/r/{subreddit}/search/?q={query}&sort=new&restrict_sr=1', timeout=20000)
page.wait_for_timeout(3000)
text = page.inner_text('body')
lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 40]
```

**Pitfalls:**
- TikTok/Facebook detect headless Chrome even with stealth. Need cookies from real logged-in session
- Chromium ~200MB RAM per instance. Close context + browser after each session
- No CAPTCHA bypass — if a site shows captcha, Playwright cannot solve it
- YouTube rate-limits after ~4 rapid searches. Add `page.wait_for_timeout(3000)` between queries
- Bing occasionally returns non-Vietnamese search results even with `setlang=vi`. Filter client-side
- Reddit via www returns duplicate entries (each post appears twice in the DOM)

