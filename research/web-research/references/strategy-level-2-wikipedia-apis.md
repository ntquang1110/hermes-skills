# Strategy hierarchy — Level 2a/2b: Wikipedia MediaWiki Action API + REST API

### Level 2a (preferred): Wikipedia MediaWiki Action API — Full search + extracts (BEST for topic discovery)

The MediaWiki Action API (`/w/api.php`) is **more powerful** than the REST API for research because it supports **keyword search**, not just title-based fetch. Use this when you need to discover topics by keyword, get structured plain-text extracts, or query multiple pages in one call.

**Advantages over REST API:**
- **Search by keyword** — the REST API has no search endpoint; Action API does
- **Multi-language** — query `https://vi.wikipedia.org/w/api.php` for Vietnamese content
- **Plain text extracts** with `explaintext=1` — no HTML parsing needed
- **Batch titles** — comma-separated in one call
- **Snippet highlights** — FTS5-like `<span class="searchmatch">` markers in snippets

**Use cases:**
- Discovering company transaction/deal details by searching "license agreement", "acquisition", "patent deal"
- Finding Vietnamese content via `vi.wikipedia.org`
- Researching biomedical/biotech topics with scientific terminology
- Compiling structured data tables from multiple related pages

**Core search + extract pattern:**

```python
import urllib.request, json, ssl, urllib.parse
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

def wiki_search(query, lang='en', limit=10):
    """Search Wikipedia by keyword, return list of matching pages with snippets."""
    params = urllib.parse.urlencode({
        'action': 'query', 'list': 'search',
        'srsearch': query, 'srlimit': limit, 'format': 'json'
    })
    url = f'https://{lang}.wikipedia.org/w/api.php?{params}'
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=15)
    data = json.loads(resp.read().decode())
    results = []
    for r in data.get('query', {}).get('search', []):
        results.append({
            'title': r['title'],
            'pageid': r['pageid'],
            'snippet': re.sub(r'<[^>]+>', '', r.get('snippet', '')),
            'size': r.get('size', 0)
        })
    return results

def wiki_extract(titles, lang='en'):
    """Get plain-text extracts for one or more page titles (comma-separated)."""
    params = urllib.parse.urlencode({
        'action': 'query', 'titles': titles,
        'prop': 'extracts', 'explaintext': 1, 'format': 'json',
        'exlimit': 20
    })
    url = f'https://{lang}.wikipedia.org/w/api.php?{params}'
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=15)
    data = json.loads(resp.read().decode())
    pages = data.get('query', {}).get('pages', {})
    result = {}
    for pid, pg in pages.items():
        if 'extract' in pg:
            result[pg['title']] = pg['extract']
    return result
```

**Terminal quick probe (curl + python -c):**

```bash
# Search Wikipedia for pharma patent deals
curl -sL --max-time 15 \
  "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=%22license+agreement%22+OR+%22licensing+deal%22+pharmaceutical+billion&format=json&srlimit=5" \
  -H "User-Agent: Mozilla/5.0" \
  | python -c "import sys,json,re; d=json.load(sys.stdin); [print(f\"  {r['title']}: {re.sub(r'<[^>]+>','',r['snippet'])[:200]}\") for r in d['query']['search']]"

# Get extract of a specific page
curl -sL --max-time 15 \
  "https://en.wikipedia.org/w/api.php?action=query&titles=Arrowhead_Pharmaceuticals&prop=extracts&explaintext=1&format=json" \
  -H "User-Agent: Mozilla/5.0" \
  | python -c "import sys,json; d=json.load(sys.stdin); pg=list(d['query']['pages'].values())[0]; print(pg.get('extract','')[:2000])"

# Extract specific sections by keyword (search page text for a deal value)
curl -sL --max-time 15 \
  "https://en.wikipedia.org/w/api.php?action=query&titles=Hanmi_Pharm&prop=extracts&explaintext=1&format=json" \
  -H "User-Agent: Mozilla/5.0" \
  | python -c "import sys,json; d=json.load(sys.stdin); t=list(d['query']['pages'].values())[0].get('extract',''); idx=t.lower().find('sanofi'); print(t[max(0,idx-200):idx+1000] if idx>=0 else 'Not found')"
```

**Multi-language & deal/transaction research patterns** — `multi_lang_search`, `find_deals_in_page`, `extract_transaction_context`, batch extract, Vietnamese search, and pageid-based extraction are all in `references/wikipedia-mediawiki-api-research.md`. Use that file instead of the inline copies below (kept minimal here for quick reference).

**Pitfalls:**
- **Search relevance**: Wikipedia search uses FTS5-like ranking. Multi-word queries default to AND. Use OR for broader recall (`alpha OR beta`), quoted phrases for exact match.
- **No CAPTCHAs**: Unlike DDG Lite, the Action API never blocks automated queries — designed for programmatic access.
- **Rate limits**: ~200 requests/minute unauthenticated. For bulk work, add `time.sleep(1)` between calls.
- **Snippet HTML**: The `snippet` field contains `<span class="searchmatch">` tags. Strip with `re.sub(r'<[^>]+>', '', snippet)`.
- **Redirects**: Search may return redirect pages. Use `titles=` to follow redirects automatically.
- **429 (Too Many Requests)**: If you get HTTP 429, back off with exponential backoff (1s → 2s → 4s). Rare for normal usage.
- **No real-time data**: Wikipedia is not for current prices, stock data, or breaking news.
- **PageIds can resolve to non-article content (⚠️)**: A `pageid` passed to `prop=extracts` may return a file page (image, media), a redirect, or a disambiguation page — none of which have a meaningful `extract` field. Always verify that the returned `pages` dict contains a page with `'extract'` in it. If the extract is empty or the title looks wrong, the pageid was likely not a real article. Use `wiki_search()` to find the correct article by keyword first, then use its pageid, rather than hard-coding pageids. This typically happens with auto-generated or copied page IDs that may have changed after article merges/splits.
- **Large extract timeout (⚠️)**: The `wiki_extract_by_pageid` and `wiki_extract` functions default to `timeout=15`, but large articles (30KB+ extracts like "Autophagy", "Apoptosis") can exceed 15s on slow connections. Bump to `timeout=30` when fetching full-page extracts for major topics. The symptom is an unhandled `urllib.error.URLError: timed out` — the script exits with no extract output but no obvious error in the return buffer either.
- **`exlimit` silently capped to 1 for multi-page queries (⚠️)**: The `exlimit` parameter in `prop=extracts` queries is **silently capped to 1** when you request multiple pages at once via `titles=` with `|` separator or `pageids=` with comma-separated IDs. The API returns a warning `"exlimit was too large for a whole article extracts request, lowered to 1"` and only returns the first page's extract. **Symptom:** `wiki_extract_by_pageid("4438339,14725468")` returns `{}` (empty dict) with zero exit code — no error, no warning in the output, just no extract. The API response exists but subsequent pages silently lack the `extract` key. **Fix:** use `wiki_extract_multi()`, or fetch one page per API call. Use paginated calls (one `curl` or `urllib` request per pageid) rather than batching. This is safe because the Action API handles 5-10 sequential calls easily. Example in cron mode:

  ```bash
  # BAD — exlimit silently capped to 1, only first page returned:
  curl -sL "https://en.wikipedia.org/w/api.php?action=query&titles=NLRP3|Inflammasome&prop=extracts&explaintext=1&format=json&exlimit=10"

  # GOOD — separate calls, each returns full extract:
  for pageid in 6648966 19303923; do
    curl -sL "https://en.wikipedia.org/w/api.php?action=query&pageids=$pageid&prop=extracts&explaintext=1&format=json" \
      -H "User-Agent: Mozilla/5.0" \
      -o "C:/Users/<user>/hermes-temp/wiki_${pageid}.json"
  done
  ```

  In Python, loop over individual pageids rather than passing a comma-separated string:
  ```python
  all_extracts = {}
  for pageid in pageid_list:
      extract = wiki_extract_by_pageid(str(pageid))  # single pageid
      all_extracts.update(extract)
      time.sleep(0.5)  # gentle pacing
  ```

- **Greek/special characters in titles (⚠️ CRITICAL)**: The Action API `titles=` parameter with `|` separator **silently fails** when titles contain Greek letters (NF-κB, IκBα), subscript/superscript characters (TNFα, IL-1β), or other non-ASCII Unicode. `urllib.parse.urlencode` double-encodes pre-escaped strings (e.g. `NF-%CE%BAB` → `NF-%25CE%25BAB`, which the API cannot decode). **Fix:** always pass **raw Python Unicode strings** to `urlencode` (e.g. `'NF-κB'`, not `'NF-%CE%BAB'`). For maximum reliability, use **pageid-based fetching** — page IDs are numeric and never have encoding problems:

  ```python
  # Full versions of wiki_extract_by_pageid + wiki_extract_multi (Greek/Unicode-safe,
  # exlimit=1 cap workaround) live in references/wikipedia-mediawiki-api-research.md
  ```

  The **REST API** (Level 2b) also handles Unicode titles correctly via `urllib.parse.quote()` — use it for single-page fetches when you already know the title.

**See** `references/wikipedia-mediawiki-api-research.md` for the complete code library including multi-language search, batch extract, deal-finding, and Vietnamese Wikipedia query patterns.

**For structured table extraction** (rankings, production statistics, comparison matrices), use the `action=parse` endpoint with the `section=` parameter instead. This returns HTML with `<table class="wikitable">` elements intact, which you can extract via regex. See `references/wikipedia-parse-table-extraction.md` for the complete workflow: finding section indices, fetching section HTML, wikitable regex extraction, filtering rows, and terminal one-liners. Use parse+section when you need tabular data; use query+extracts when you need descriptive prose.

### Level 2b: Wikipedia REST API — Reliable structured data (FALLBACK when search engines are blocked)

When ALL search engines (DDG Lite included) return CAPTCHAs, skip web search entirely and go directly to Wikipedia's REST API. This is the **most reliable** method because Wikipedia's `/api/rest_v1/` is designed for programmatic access and accepts automated requests without CAPTCHAs.

**Why it works:** Wikipedia's REST API is built for bots, crawlers, and third-party tools. It returns clean JSON with structured extracts, section headers, and metadata — no JavaScript, no CAPTCHAs. Note: the `/page/html/` endpoint has tighter rate limits than `/page/summary/` — see pitfalls below and `references/wikipedia-api-research.md` for pacing and retry patterns.

**Quick access — page summaries:**

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
    data = json.loads(resp.read().decode())
    # data['extract'] = plain-text summary
    # data['titles'] = canonical titles
    # data['content_urls']['desktop']['page'] = full URL
    # data['thumbnail'] = image URL (if exists)
    return data
```

**Full page HTML for deep research (two approaches):**

**Approach A — Inline Python (direct, but rate-limited):**
```python
def wiki_full_html(title):
    url = f'https://en.wikipedia.org/api/rest_v1/page/html/{urllib.parse.quote(title)}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 ...'})
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=15)
    html = resp.read().decode('utf-8', errors='replace')
    return html  # extract paragraphs with <p>-tag regex
```

**Approach B — Save to file + read_file (PRACTICAL for 500KB+ pages):**
For large pages (700KB+ like the NF-κB article), Approach A is impractical because the HTML blows out your context window. Instead:

```bash
# Save full HTML to a file
curl -sL --max-time 20 \
  "https://en.wikipedia.org/api/rest_v1/page/html/NF-%CE%BAB" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
  -o C:/Users/<user>/hermes-temp/page.html
```

Then use `read_file` to browse the HTML by section. The Wikipedia REST HTML has semantic section IDs in `data-mw-section-id` attributes. Search for `<h2>` tags to find section boundaries:

```python
# After saving with curl -o, read the file and find sections
read_file(path="C:/Users/<user>/hermes-temp/page.html", offset=1, limit=200)
# Look for <h2 id="Signaling">, <h2 id="Clinical_significance">, etc.
# Then read around those offsets to extract section content
# <p> tags contain the paragraph text (strip HTML with regex)
```

**Key sections to search for in biomedical research pages:**
- `Signaling` — signaling pathways and activation mechanisms
- `Structure` — protein domains and subunit composition
- `Clinical_significance` — disease associations (cancer, inflammation)
- `Inhibition` — known inhibitors and regulatory mechanisms
- `Members` — family members and their functions

**Tip:** Topic discovery via search still matters — use the page title from a DDG snippet (if any made it through), or guess the canonical Wikipedia page title. Wikipedia's redirect system resolves common variations automatically (e.g. "JAK-STAT" → "JAK-STAT_signaling_pathway").

**Terminal quick probe (curl + node for environments without python3):**
```bash
# Using python3 (Linux/macOS)
curl -sL --max-time 15 \
  "https://en.wikipedia.org/api/rest_v1/page/summary/Interferon" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('extract','')[:1000])"

# Using node (Windows git-bash where python3 is blocked by App Execution Aliases)
curl -sL --max-time 15 \
  "https://en.wikipedia.org/api/rest_v1/page/summary/Interferon" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
  | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{const j=JSON.parse(d);console.log(j.extract?.substring(0,1000)||'No extract')})"

# Fetch full page HTML and extract paragraphs (node)
curl -sL --max-time 15 \
  "https://en.wikipedia.org/api/rest_v1/page/html/AlphaFold" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
  | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{const ps=d.match(/<p[^>]*>([\s\S]*?)<\/p>/g)||[];ps.forEach((p,i)=>{const t=p.replace(/<[^>]+>/g,'').trim();if(t.length>50)console.log((i+1)+':',t.substring(0,500))})})"
```

**⚠️ Cron-mode note:** `python -c` may be blocked in some strict cron approval configs. Try it first; if it fails (empty output or "can't open file"), use Pattern A (curl -o + read_file) instead.
```

**Best for:** Scientific/medical/technical research where Wikipedia content is authoritative and structured. Supplements (or replaces) raw search results when search engines are blocked.

**Pitfalls:**
- **Stale pages**: Wikipedia content is crowd-sourced; verify critical facts against primary literature
- **No search**: You need to know the topic title to fetch it — discovery still requires Level 1-1b
- **Rate limits (429)**: The `/page/html/` endpoint rate-limits after ~6 rapid requests even with 2s gaps. The `/page/summary/` endpoint is more forgiving. Always pace with `time.sleep(3)` for `/page/html/` and implement retry logic on 429. See `references/wikipedia-api-research.md` for the full pattern.
- **⚠️ Wikipedia Action API and REST API share the same rate limit bucket** (CRITICAL): Getting a 429 from `/w/api.php` (Action API, Level 2a) means `/api/rest_v1/` (REST API, Level 2b) will also 429 for 20-30s, and vice versa. They are NOT independent for rate-limiting. Do NOT try to work around a 429 by switching from Action API to REST API or vice versa — wait the full cooldown (~30s) instead. Pace ALL Wikipedia calls (across both APIs) under a single 2s throttle. This was tested Jul 2026: 3 sequential Action API calls at 0.8s delays triggered a 429 that also blocked REST API calls 15s later for another 20s.
- **No real-time info**: Current events, prices, or transient data are poorly covered
- **404 on unknown titles**: The API returns HTTP 404 for non-existent pages (not a redirect). Handle gracefully with try/except.
- **⚠️ Action API `titles=` may resolve to disambiguation pages (0-char extract)**: When querying short protein/gene names like `LCK`, `ZAP70`, `CD4`, `CD3`, the Action API may resolve them to **disambiguation pages** that return empty/0-character extracts (the `extract` key is missing or contains only `(no extract)`). This is silent — no error, no warning. **Detection:** after `wiki_extract(titles="LCK|ZAP70")`, verify each returned entry has a non-empty `extract`. If a title's extract is empty or ~12 chars, the API hit a non-article page. **Fix:** fall back to the REST API `/page/summary/<title>` (Level 2b) which resolves canonical article titles correctly via `urllib.parse.quote()` (e.g. `ZAP70` → ZAP-70 works). The REST API handles redirects that the Action API `titles=` parameter misses for these short names.

