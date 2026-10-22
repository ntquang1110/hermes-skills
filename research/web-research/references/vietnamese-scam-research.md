# Vietnamese Scam Research

Platform-specific search patterns for collecting scam reports, phone numbers, bank accounts, and scam methods in Vietnam.

## Platform coverage

| Platform | Search via DDG | Data quality | Notes |
|----------|---------------|--------------|-------|
| **Twitter/X** | site:x.com or site:twitter.com | High — real user reports | Scam-specific posts visible; dedicated scraping tools (snscrape) dead since 2025. DDG snippets are your best bet. |
| **Reddit** | site:reddit.com | Medium — discussion threads | snscrape/PushShift dead. DDG indexes some threads. PRAW (official API) works with free Reddit account. |
| **Telegram** | site:t.me | Low — only public channels | Most scam groups are private. snscrape only works for channels with search indexing enabled. Telethon needs API credentials. |
| **Threads** | site:threads.net | Very low | DDG barely indexes Threads. Almost no results. |
| **Facebook** | site:facebook.com | Low — only public Pages | facebook-scraper requires Selenium + logged-in session. Facebook actively bans. |
| **YouTube** | site:youtube.com | Medium | Video titles/descriptions visible in DDG. Playwright works well for YouTube search. |
| **Bao chi** | Direct Vietnamese keywords | High | Most Vietnamese news sites render properly in DDG. Cloudflare blocks direct page scraping though. |

## Scraping tools status (2025-2026)

All major social media scraping tools fail as of 2025-2026. Do NOT install them expecting to get data:

| Tool | Fate | Alternative |
|------|------|-------------|
| snscrape Twitter | Dead (GraphQL 404) | Playwright YouTube/Bing News or DDG Lite site:x.com |
| snscrape Reddit | Dead (PushShift gone) | PRAW (Reddit API, free) or Playwright www.reddit.com |
| snscrape Telegram | Works only for indexed public channels | Telethon (needs API ID) |
| twscrape | Dead (same as snscrape) | N/A |
| facebook-scraper | Brittle (needs browser) | Facebook API (needs approval) |
| TikTok-Api | Brittle (frequent breakage) | N/A |
| social-analyzer | Username lookup only, not content search | Use Playwright instead |
| URS (Universal Reddit Scraper) | Large repo, clone may timeout | PRAW directly (same engine, simpler) |

**Working alternatives:**
- **Playwright** (`pip install playwright && python -m playwright install chromium`): Browser automation. Works for **YouTube**, **Bing News**, **Reddit** (www) without login. See Level 1d in SKILL.md.
- DDG Lite: Still indexes public social posts. Best for Twitter/X and Reddit content.
- PRAW (`pip install praw`): Official Reddit API. Free tier with a Reddit account.
- Telethon (`pip install telethon`): Telegram client API. Needs API ID from my.telegram.org.

## What Works (tested Jul 2026)

| Method | Platforms | Login needed? | Results |
|--------|-----------|--------------|---------|
| Playwright (headless + stealth) | **YouTube** | No | **20+ videos/query** — extract title, URL, channel, views |
| Playwright (headless + stealth) | **Bing News** | No | **15-20 news/query** — Vietnamese scam news headlines |
| Playwright (headless + stealth) | **Reddit www** | No | **8-10 posts/query** — text extraction, duplicates common |
| Playwright (headless + stealth) | **TikTok** | No | ❌ "Something wrong with server" |
| Playwright (headless + stealth) | **Facebook** | No | ❌ Returns empty page |
| Playwright (headless + stealth) | **X/Twitter** | No | ❌ Login wall |
| Playwright (headless + stealth) | **DuckDuckGo** | No | ❌ Captcha on all endpoints |
| Playwright (headless + stealth) | **Google News** | No | ❌ 0 articles |
| DDG Lite (urllib POST) | General web | No | ⚠️ Rate-limited after ~4 queries |

## Data import pipeline (Playwright → DB)

For importing scan results into a Supabase project:

```python
# 1. Scan with Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
    page.goto('https://www.bing.com/news/search?q=lừa+đảo+Việt+Nam&setlang=vi', timeout=15000)
    page.wait_for_timeout(2000)
    articles = page.eval_on_selector_all('a.title', """els => els.map(el => ({
        t: el.textContent?.trim() || '', u: el.href || ''
    }))""")
    browser.close()

# 2. Store in database
import psycopg2
conn = psycopg2.connect(DB_URL)
cur = conn.cursor()
for a in articles:
    cur.execute("INSERT INTO posts (title, content, ...) VALUES (%s, %s, ...)", ...)
conn.commit()
```

## Working search terms

### General
```
canh bao lua dao online Viet Nam 2025
lua dao cong nghe cao canh bao moi nhat
```

### By scam type
```
lua dao dau tu crypto Viet Nam
lua dao gia danh cong an
danh sach so dien thoai lua dao
lua dao ngan hang gia mao
lua dao viec lam online
lua dao tinh cam online
lua dao ban hang da cap
```

### Bing News (best results — 15-20 articles per query)
```
lừa đảo chiếm đoạt tài sản mới nhất
bắt đối tượng lừa đảo Việt Nam
cảnh báo lừa đảo ngân hàng giả mạo
lừa đảo đầu tư chứng khoán
công an triệt phá đường dây lừa đảo
```

## Categorization keywords

| Keyword | Category |
|---------|----------|
| crypto, dau tu, tien ao, bitcoin, usdt, token | Dau tu/Crypto |
| cong an, gia danh, vien kiem sat, toa an | Gia danh CA |
| so dien thoai, dien thoai, sim rac, cuoc goi | SDT Scam |
| ngan hang, chuyen tien, vcb, vietcombank, techcombank | Ngan hang |
| viec lam, tuyen dung, viec nhe, online | Viec lam |
| tinh cam, hen ho, dating | Tinh cam |
| da cap, ban hang | Da cap |
| vay tien, vay online | Vay tien |

## Output structure for Google Sheets

1. Tieu de — title (120 chars)
2. URL — original link
3. Mo ta — snippet (200 chars)
4. Danh muc — classified category
5. Nguon — Twitter/X, Bao chi, Telegram
6. Ghi chu — additional context

## Auto-scanner cron job pattern

To run the Playwright scanner **automatically every hour** and import results into a Supabase database:

### 1. Create the scanner script

Save as `~/.hermes/scripts/<name>.py`. Key components:
- Playwright browser automation with stealth init script
- Bing News + YouTube + Reddit (www) queries
- Triple dedup before DB insert (check by URL, slug, and within same round)
- Tag auto-detection from title keywords

### 2. Register with cronjob

```
cronjob action=create name="Scanner" schedule="0 * * * *" script=<name>.py no_agent=true deliver=origin
```

Parameters explained:
- `no_agent=true` — runs the script directly, no LLM tokens consumed each tick
- `script=filename.py` — must be a filename under `~/.hermes/scripts/`
- `deliver=origin` — output sent to the current Telegram conversation
- `schedule="0 * * * *"` — every hour at minute 0

### 3. Triple dedup strategy

```python
# Level 1: URL dedup — check if source URL already in DB
existing_urls = set()
for (content,) in cur.fetchall():
    for line in content.split('\n'):
        if line.startswith('Nguon: http'):
            existing_urls.add(line.replace('Nguon: ', '').rstrip('/'))

# Level 2: Slug dedup — check if title slug already in DB
existing_slugs = {r[0] for r in cur.fetchall()}

# Level 3: In-round dedup — avoid duplicates within same scan
seen_in_round = set()
for item in articles:
    url = item['u'].rstrip('/')
    if url in seen_in_round or url in existing_urls:
        continue
    seen_in_round.add(url)
    slug = gen_slug(item['t'])
    if slug in existing_slugs:
        continue
```

### 4. Pitfalls

- Script must be in `~/.hermes/scripts/` — cron tool only accepts filenames, not absolute paths
- `no_agent=true` scripts get NO LLM context — all logic must be self-contained in Python
- Playwright uses ~200MB RAM per instance
- Without URL dedup, same articles appear in every hourly scan
- If the script crashes midway, the transaction rolls back

## Known limitations (2025-2026)

- Vietnamese news sites use Cloudflare: snippets visible, full pages blocked.
- Scam phone numbers often embedded as images; regex misses these.
- DDG rate limits after ~4-6 queries. Pace with time.sleep(2).
- Telegram private groups: highest-value data is invisible to all tools.
- Twitter/X: snippets visible; full thread content requires X API.
- All search engines (Bing, Google) block automated queries.
- TikTok/Facebook/Twitter: Playwright headless is detected even with stealth.
- Reddit www via Playwright: duplicates every post in DOM output.
- Bing Web search returns irrelevant/non-Vietnamese results; use Bing News instead.
