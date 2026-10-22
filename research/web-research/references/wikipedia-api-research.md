# Wikipedia REST API — Research Reference

## Overview

Wikipedia's REST API at `https://en.wikipedia.org/api/rest_v1/` is the most reliable structured data source when search engines are blocked. It's designed for programmatic access — no CAPTCHAs, no JavaScript rendering, clean JSON responses.

## Core Endpoints

### `/page/summary/{title}` — Best for quick definitions

Returns structured JSON with extract, thumbnail, and metadata.

```python
import urllib.request, json, ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

def wiki_summary(title):
    url = f'https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=15)
    return json.loads(resp.read().decode())
```

**Key fields in response:**
| Field | Description |
|-------|-------------|
| `title` | Page title |
| `extract` | Plain-text first section (usually 100-300 words) |
| `extract_html` | HTML version of the extract |
| `description` | Short tagline (e.g. "Signaling proteins released by host cells...") |
| `thumbnail.source` | Image URL (if available) |
| `content_urls.desktop.page` | Full Wikipedia page URL |
| `titles.canonical` | Canonical title with underscores (usable in API calls) |

**Redirect handling:** If `title` is a redirect, the API follows it transparently and returns the canonical page data. No 404 for common misspellings.

### `/page/html/{title}` — Full page content

Returns the full rendered HTML of a Wikipedia article. Useful for deep research.

```python
def wiki_full_html(title):
    url = f'https://en.wikipedia.org/api/rest_v1/page/html/{urllib.parse.quote(title)}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 ...'})
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=15)
    return resp.read().decode('utf-8', errors='replace')
```

**Stripping HTML to plain text:**
```python
import re
text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text)
```

### `/page/related/{title}` — Similar topics

Returns a list of related pages with summaries. Good for exploration when you need breadth.

```python
def wiki_related(title):
    url = f'https://en.wikipedia.org/api/rest_v1/page/related/{urllib.parse.quote(title)}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 ...'})
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=15)
    return json.loads(resp.read().decode()).get('pages', [])
```

## Known-Working Research Titles

The following titles were used successfully in the Interferon/innate immunity research session (2026-07-15):

| Search topic | Wikipedia title | Notes |
|-------------|----------------|-------|
| Interferon types & signaling | `Interferon` | Covers all 3 types, JAK-STAT, ISGs |
| JAK-STAT pathway | `JAK-STAT_signaling_pathway` | Covers receptors, STATs, regulation |
| Pattern recognition receptors | `Pattern_recognition_receptor` | TLRs, RLRs, NLRs, CLRs |
| cGAS DNA sensor | `Cyclic_GMP-AMP_synthase` | cGAS-STING cytosolic DNA pathway |
| Interferon-stimulated genes | `Interferon_stimulated_gene` | ISG categories, ~450 genes |
| Toll-like receptors | `Toll-like_receptor` | TLR1-13, membrane vs endosomal |
| RIG-I | `RIG-I` | Cytosolic RNA helicase PRR |
| Innate immune system | `Innate_immune_system` | Broad overview |

## Terminal Quick Probe (curl)

```bash
# Summary (plain text extract)
curl -sL "https://en.wikipedia.org/api/rest_v1/page/summary/Interferon" \
  -H "User-Agent: Mozilla/5.0" | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('extract','')[:1000])"

# Check if a page exists (200 = yes, 404 = no)
curl -s -o /dev/null -w "%{http_code}" \
  "https://en.wikipedia.org/api/rest_v1/page/summary/NonExistentPage"
```

## Pitfalls

1. **404 on unknown titles**: Handled with try/except. Use `content_urls.desktop.page` for user-facing links.
2. **Stale content**: Wikipedia is crowd-sourced. For critical scientific/medical facts, cross-reference with primary literature.
3. **No search**: You must know the title. Discovery still requires DDG or other search.
4. **Rate limits (429 Too Many Requests)**: The `/page/html/` endpoint rate-limits aggressively — as few as 6 sequential requests with 2-second gaps can trigger HTTP 429. The `/page/summary/` endpoint is more permissive but still rate-limited at scale. **Recommended pacing:**
   - `/page/summary/`: `time.sleep(1.5)` between requests (OK up to ~20 pages)
   - `/page/html/`: `time.sleep(3)` between requests (safe up to ~10 pages)
   - **Always implement retry logic** when hitting 429. Use fixed 5-second retry:
     ```python
     def wiki_html(title):
         url = f'https://en.wikipedia.org/api/rest_v1/page/html/{urllib.parse.quote(title)}'
         req = urllib.request.Request(url, headers={'User-Agent': '...'})
         for attempt in range(3):
             try:
                 resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=15)
                 return resp.read().decode('utf-8')
             except urllib.error.HTTPError as e:
                 if e.code == 429:
                     time.sleep(5)
                     continue
                 return f"ERROR: {e}"
         return "ERROR: Rate limited after retries"
     ```
   - If bulk research (>15 pages), prefer `/page/summary/` + `/page/related/` over `/page/html/`.
5. **HTML paragraph extraction**: The naive `re.sub(r'<[^>]+>', ' ', html)` flattens all structure into one blob. For deep research, extract individual `<p>` tags to preserve paragraph boundaries:
   ```python
   import re
   paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
   for p in paras:
       clean = re.sub(r'<[^>]+>', '', p).strip()
       clean = clean.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
       clean = clean.replace('&#39;', "'").replace('&quot;', '"').replace('&nbsp;', ' ')
       if clean and len(clean) > 50:
           content.append(clean)
   ```
   This yields clean, readable paragraphs suitable for structured research output. Discard paragraphs shorter than 50 characters (usually navigation text or captions).
6. **Language variants**: Use `https://en.wikipedia.org` for English. For other languages, use `https://{lang}.wikipedia.org` (e.g., `vi.wikipedia.org` for Vietnamese).
7. **Not for real-time/transient info**: Current events, stock prices, or niche commercial data are poorly covered.
