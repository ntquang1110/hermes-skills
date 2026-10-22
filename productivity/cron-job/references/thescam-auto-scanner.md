# TheScam Auto Scanner — Architecture & Patterns

A `no_agent` cron script that scrapes scam warnings from Bing News / YouTube / Reddit every hour and imports structured posts to a Supabase database (theliems.com).

## Scam Relevance Filter

Without keyword filtering, the scanner imports non-scam articles (e.g. war news, politics) that happen to appear in search results. Filter by Vietnamese scam keywords:

```python
SCAM_KEYWORDS = [
    'lua dao', 'lừa đảo', 'canh bao', 'cảnh báo', 'scam', 'chiếm đoạt',
    'chien doat', 'thu doan', 'thủ đoạn', 'bat doi tuong', 'bắt đối tượng',
    'khoi to', 'khởi tố', 'bat tam', 'tạm giam', 'trieu tap',
    'gian mao', 'giả mạo', 'mao danh', 'mạo danh', 'sim rac', 'sim rác',
    'da cap', 'đa cấp', 'tinh cam', 'tình cảm', 'viec lam', 'việc làm',
    'vay tien', 'vay tiền', 'tai khoan', 'tài khoản', 'chuyen tien',
    'dau tu', 'đầu tư', 'tien ao', 'tiền ảo', 'crypto',
    'mat tien', 'mất tiền', 'canh giac', 'cảnh giác', 'bao mat',
    'gian lan', 'gian lận', 'bat giu', 'bắt giữ', 'doc quyen',
]

def is_scam_relevant(title, desc=''):
    t = (title + ' ' + desc).lower()
    return any(kw in t for kw in SCAM_KEYWORDS)
```

Apply **before** dedup check — no point generating a slug for a non-scam article. This filter is the primary gating mechanism.

## Structured Content Generator (build_content)

The `build_content()` function produces a **rich, user-facing post** — not just a link dump. Every post has:

```
# 🚨 CẢNH BÁO: {title}

![Scam Alert](og_image_url)          ← thumbnail if available

**Mô tả:** {meta description}        ← excerpt from source article

**🔍 Thủ đoạn:**                       ← _gen_modus_operandi()
{context-aware scam technique description}

**🛡️ Cách tránh:**
- ✅ Luôn kiểm tra thông tin qua kênh chính thống
- ✅ Không chuyển tiền cho người lạ qua điện thoại/internet
- ✅ Báo ngay cho cơ quan công an nếu nghi ngờ

📎 **Nguồn:** [link](url)
📡 **Phát hiện từ:** {source name}
---
*Bài viết được tự động tổng hợp...*
```

### _gen_modus_operandi() — Context-Aware Scam Description

Generates a Vietnamese paragraph describing the specific scam technique based on detected keywords:

| Keyword match | Description generated |
|--------------|----------------------|
| crypto/dau tu | "Kẻ gian mời chào các gói đầu tư tài chính/crypto với lợi nhuận cao bất thường..." |
| ngan hang/tai khoan | "Giả mạo nhân viên ngân hàng gọi điện yêu cầu cung cấp OTP..." |
| cong an/canh sat | "Giả danh cơ quan công an/toà án thông báo có liên quan đến vụ án..." |
| viec lam/viec nhe | "Đăng tin tuyển dụng việc nhẹ lương cao, yêu cầu đóng phí hồ sơ..." |
| tinh cam/hen ho | "Tạo hồ sơ giả trên ứng dụng hẹn hò/mạng xã hội..." |
| vay tien/vay online | "Cho vay tín dụng đen qua app, lãi suất cắt cổ..." |
| None of above | Generic fallback: "Đối tượng sử dụng nhiều thủ đoạn tinh vi..." |

## YouTube OEmbed (no API key needed)

```python
def fetch_youtube_desc(video_id):
    """Fetch YouTube metadata via oembed — no API key required"""
    resp = requests.get(
        f'https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json',
        timeout=5
    )
    data = resp.json()
    return data.get('title',''), data.get('author_name',''), data.get('thumbnail_url','')
    # → (video title, channel name, hqdefault thumbnail URL)
```

## Full Pipeline (v2 — enriched)

```
Scrape (Playwright, 3 sources)
  ├─ Bing News  → 34-41 items, 3 queries
  ├─ YouTube    → 40 items, 2 queries  
  └─ Reddit     → ~10 items, 1 query
       ↓
Enrich metadata (per item)
  ├─ Bing items → fetch_article_meta (OG img + desc + text)
  └─ YouTube    → fetch_youtube_desc (title + author + thumbnail)
       ↓
Filter relevance (is_scam_relevant)
  └─ Skip if no keyword match → prevents non-scam imports (war, politics)
       ↓
Dedup (slug collision check against DB)
  └─ Skip if slug already exists
       ↓
Generate structured content (build_content)
  ├─ 🚨 Title header + OG thumbnail image
  ├─ Mô tả / excerpt
  ├─ 🔍 Thủ đoạn (ngen_modus_operandi)
  ├─ 🛡️ Cách tránh (3 prevention bullets)
  └─ 📎 Nguồn link
       ↓
Detect severity + tag
  ├─ severity: critical / high / medium / low (heuristic)
  └─ tag: dau-tu-crypto / gia-mao-ngan-hang / ... (keyword map)
       ↓
Import to Supabase
  ├─ INSERT into posts (title, slug, content, excerpt, category_id, is_scam_alert, scam_severity)
  ├─ INSERT into post_scam_tags if tag detected
  └─ UPDATE scam_tags SET post_count
```

```
Scrape (Playwright)
  ├─ Bing News    → 3 queries, `a.title` selector, 34-41 items
  ├─ YouTube      → 2 queries, `ytd-video-renderer`, 40 items
  └─ Reddit       → 1 query, body text split, ~10 items
       │
       ▼
Enrich (requests + regex)
  ├─ For each Bing item: fetch URL → extract og:image, meta description, first <p>
  └─ For YouTube items: oembed API → title, author, thumbnail URL
       │
       ▼
Filter (keyword matching)
  ├─ SCAM_KEYWORDS list (lua dao, canh bao, chiếm đoạt, thu doan, etc.)
  └─ Skip if no keyword matches title+desc → prevents non-scam imports
       │
       ▼
Generate (structured content builder)
  ├─ 🚨 Title as H1
  ├─ Image: ![Scam Alert](og_image_url)
  ├─ Mô tả: meta description or excerpt
  ├─ 🔍 Thủ đoạn: _gen_modus_operandi() — context-aware text
  ├─ 🛡️ Cách tránh: 3-4 bullet points
  ├─ 📎 Nguồn: link
  └─ 📡 Phát hiện từ: source name
       │
       ▼
Import (psycopg2 direct to Supabase PostgreSQL)
  ├─ Category: TheScam (by slug)
  ├─ Severity detection: critical/high/medium/low
  ├─ Tag detection: crypto, bank, police, job, romance, loan, etc.
  ├─ Dedup: check existing slugs
  └─ Update post_count on scam_tags table
```

## Anti-Detection Playwright Setup

```python
browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
ctx = browser.new_context(
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    viewport={'width':1280,'height':720})
page = ctx.new_page()
page.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
```

## Fetching Article Metadata

```python
def fetch_article_meta(url):
    """OG image, meta description, first paragraph from news article (3 fallback layers each)"""
    meta = {'img': '', 'desc': '', 'text': ''}
    try:
        resp = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        if resp.status_code != 200:
            return meta
        html = resp.text
        # OG image (3 fallback layers)
        m = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', html)
        if m: meta['img'] = m.group(1)
        if not meta['img']:
            m = re.search(r'<meta[^>]+name="twitter:image"[^>]+content="([^"]+)"', html)
            if m: meta['img'] = m.group(1)
        if not meta['img']:
            m = re.search(r'<img[^>]+src="(https?://[^"]+\\.(?:jpg|jpeg|png|webp))"', html)
            if m: meta['img'] = m.group(1)
        # Meta description (3 fallback layers)
        m = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html)
        if m: meta['desc'] = m.group(1)[:300]
        if not meta['desc']:
            m = re.search(r'<meta[^>]+property="og:description"[^>]+content="([^"]+)"', html)
            if m: meta['desc'] = m.group(1)[:300]
        # First meaningful paragraph
        m = re.search(r'<p[^>]*>([^<]{50,300})</p>', html)
        if m:
            meta['text'] = re.sub(r'<[^>]+>', '', m.group(1)).strip()[:300]
    except:
        pass
    return meta
```

⚠️ **Always wrap fetch_article_meta in try/except** — some news sites are slow, return 4xx/5xx, or have malformed HTML. Without the wrapper, a single failing URL crashes the entire batch.

⚠️ **Be gentle with rate limits** — add `time.sleep(0.5)` between fetches when processing 40+ items. Some Vietnamese news sites (VnExpress, Tuoi Tre, thanhnien) will throttle or block rapid sequential requests.

## YouTube OEmbed API (no API key needed)

```python
resp = requests.get(
    f'https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json',
    timeout=5
)
data = resp.json()  # → title, author_name, thumbnail_url, type
```

## Supabase DB Connection with Special Characters in Password

When the password contains special characters (`"`, `(`, `)`, `#`, `$`, `%`, `^`, `[`, `]`), **do NOT use a URL-style DSN** (escaping nightmare). Use keyword arguments instead:

```python
# ✅ SAFE — keyword args, no escaping issues
conn = psycopg2.connect(
    host='db.projectref.supabase.co',
    port=5432,
    dbname='postgres',
    user='postgres',
    password=')XXj8_cqXV+nMeRF_O#mCP5$oSTZ7aN(.z^%w5[2mc-4giR8#V'
)
# ❌ UNSAFE — URL string with special chars needs careful URL-encoding
```

## Severity Detection Heuristic

```python
def detect_severity(title, desc=''):
    t = title.lower() + ' ' + desc.lower()
    if any(w in t for w in ['ty dong', 'nguy hiem', 'tu vong', 'chet nguoi']):
        return 'critical'
    if any(w in t for w in ['bat', 'trieu tap', 'khoi to', 'tam giam']):
        return 'high'
    if any(w in t for w in ['canh bao', 'canh giac', 'dau hieu', 'thu doan']):
        return 'medium'
    return 'low'
```

## Tag Detection Map

Maps Vietnamese scam keywords to `scam_tags.slug` in Supabase:

| Keyword | Tag slug |
|---------|----------|
| dau tu, crypto, bitcoin, tien ao | `dau-tu-crypto` |
| ngan hang, tai khoan, chuyen tien | `gia-mao-ngan-hang` |
| cong an, canh sat, toa an | `gia-danh-cong-an` |
| viec lam, viec nhe, tuyen dung | `viec-lam-online` |
| tinh cam, hen ho | `lua-tinh-cam` |
| vay tien, vay online | `vay-tien-online` |
| da cap, multilevel | `ban-hang-da-cap` |
| sim rac, cuoc goi, dien thoai | `sim-rac-cuoc-goi-la` |
| thuong hieu, nhan hieu | `gia-mao-thuong-hieu` |

## Modus Operandi Generator

The `_gen_modus_operandi()` function produces a context-aware description of the scam technique based on keywords in the title. Each pattern generates a Vietnamese description explaining:
- What the scammers do
- How they approach victims
- The end goal (asset theft)

If no keyword matches, it falls through to a generic warning.

## Cron Job Config

- Schedule: `0 * * * *` (every hour)
- Script: `thescam_auto_scanner.py`
- `no_agent: True` — stdout is delivered verbatim
- DB migrated from hardcoded URL to keyword-arg conn params for reliability
