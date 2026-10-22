# Wikipedia MediaWiki Action API — Research Reference

## Overview

The MediaWiki Action API (`/w/api.php`) is Wikipedia's primary API for programmatic access. Unlike the REST API (`/api/rest_v1/`), it supports **keyword search**, **multi-language queries**, and **plain-text extracts** without HTML parsing.

## Core Functions

### wiki_search() — Find pages by keyword

```python
import urllib.request, json, ssl, urllib.parse

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

def wiki_search(query, lang='en', limit=10):
    """Search Wikipedia by keyword, return matching pages with snippets."""
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
            'size': r.get('size', 0),
            'timestamp': r.get('timestamp', '')
        })
    return results
```

### wiki_extract() — Get plain-text page content

```python
def wiki_extract(titles, lang='en'):
    """Get plain-text extracts for one or more page titles (pipe-separated)."""
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

## Research Patterns

### 1. Find deal/transaction data inside page extracts

```python
def extract_transaction_context(text, search_terms):
    """Find and return context around transaction-related keywords."""
    import re
    contexts = {}
    for term in search_terms:
        idx = text.lower().find(term.lower())
        if idx >= 0:
            start = max(0, idx - 300)
            end = min(len(text), idx + 1200)
            # Extract dollar amounts
            segment = text[start:end]
            amounts = re.findall(r'\$[\d,\.]+\s*(?:billion|million|B|M|tỷ|triệu)', segment)
            contexts[term] = {
                'context': segment,
                'amounts': amounts
            }
    return contexts
```

### 2. Multi-angle search — find pages from different query angles

```python
def multi_search(queries, lang='en', limit=5):
    """Search multiple queries, deduplicate results by title."""
    seen = set()
    all_results = []
    for q in queries:
        results = wiki_search(q, lang=lang, limit=limit)
        for r in results:
            if r['title'] not in seen:
                seen.add(r['title'])
                all_results.append(r)
    return all_results
```

### 3. Batch extract — get content from many pages in one go

```python
def batch_extract(titles_list, lang='en'):
    """Get extracts for multiple pages in batches (API: pipe-separated)."""
    # API accepts pipe-separated titles, max ~50 per call
    batch_size = 20
    all_extracts = {}
    for i in range(0, len(titles_list), batch_size):
        batch = titles_list[i:i+batch_size]
        titles_str = '|'.join(batch)
        extracts = wiki_extract(titles_str, lang=lang)
        all_extracts.update(extracts)
    return all_extracts
```

### 4. Vietnamese Wikipedia search

```python
def search_vietnamese(query, limit=10):
    """Search Vietnamese Wikipedia."""
    return wiki_search(query, lang='vi', limit=limit)

# Example usage
results = search_vietnamese('bằng sáng chế dược phẩm')
for r in results:
    print(f"{r['title']}: {r['snippet'][:100]}")
```

**⚠️ Vietnamese Wikipedia redirect issue:** Vietnamese Wikipedia uses redirect pages extensively for biomedical/scientific terms (e.g., "Bạch cầu ái toan" → "Bạch cầu ưa acid", "Tế bào tua" → "Tế bào đuôi gai"). When you pass a redirect title to `wiki_extract()` via `titles=`, the API returns a page with **0-char extract** — no error, no warning, just an empty result. **Detection:** after `wiki_extract(titles="Bạch cầu ái toan", lang='vi')`, check if the returned extract is empty. If so, the title was a redirect. **Fix:** use `wiki_search()` first (which follows redirects in search results) to get the canonical pageid, then extract by pageid. Or try alternative name conventions for the same concept and extract the one that returns content. See the section above on "Pageid-based extraction (avoids title encoding issues)" for the recommended approach.

### 5. Full research workflow — collect and compile

```python
# Step 1: Search for relevant pages
query = '"license agreement" OR "licensing deal" pharmaceutical billion'
hits = wiki_search(query, limit=10)

# Step 2: Get full extracts
titles = [h['title'] for h in hits]
extracts = wiki_extract('|'.join(titles[:5]))

# Step 3: Find transaction data in each page
deal_data = {}
for title, text in extracts.items():
    ctx = extract_transaction_context(text, 
        ['billion', 'acquired', 'license', 'upfront', 'milestone', 'royalty'])
    if ctx:
        deal_data[title] = ctx

# Step 4: Compile into structured table
import pandas as pd  # if available
```

## Terminal One-liners

```bash
# Search pages by keyword
curl -sL --max-time 15 \
  "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=pharmaceutical+patent+license+deal&srlimit=5&format=json" \
  -H "User-Agent: Mozilla/5.0" \
  | python -c "import sys,json,re; d=json.load(sys.stdin); [print(f\"{r['title']}: {re.sub(r'<[^>]+>','',r['snippet'])[:150]}\") for r in d['query']['search']]"

# Get extract of a company page to find deal value
curl -sL --max-time 15 \
  "https://en.wikipedia.org/w/api.php?action=query&titles=Gilead_Sciences&prop=extracts&explaintext=1&format=json" \
  -H "User-Agent: Mozilla/5.0" \
  | python -c "import sys,json; d=json.load(sys.stdin); pg=list(d['query']['pages'].values())[0]; t=pg.get('extract',''); i=t.lower().find('pharmasset'); print(t[max(0,i-200):i+800] if i>=0 else 'Not found')"

# Vietnamese Wikipedia search
curl -sL --max-time 15 \
  "https://vi.wikipedia.org/w/api.php?action=query&list=search&srsearch=thu%E1%BB%91c+d%C6%B0%E1%BB%A3c+ph%E1%BA%A9m+b%E1%BA%B1ng+s%C3%A1ng+ch%E1%BA%BF&srlimit=3&format=json" \
  -H "User-Agent: Mozilla/5.0" \
  | python -c "import sys,json,re; d=json.load(sys.stdin); [print(f\"{r['title']}: {re.sub(r'<[^>]+>','',r['snippet'])[:100]}\") for r in d['query']['search']]"
```

## Pitfalls

- **FTS5 search syntax**: AND is default. Use `OR` for broader recall, `"quoted phrase"` for exact match, `prefix*` for wildcards
- **Snippet HTML**: `r['snippet']` contains `<span class="searchmatch">` tags — always strip with `re.sub(r'<[^>]+>', '', snippet)`
- **Redirects**: `titles=` parameter follows redirects automatically, `list=search` does not
- **Rate limits**: ~200 req/min unauthenticated. Add `time.sleep(1)` for bulk work
- **Missing pages**: If title doesn't exist, you'll get a `-1` pageid with `missing: true` — check `'missing' not in pg`
- **Extract length**: `prop=extracts` returns a few thousand chars by default. For full pages, combine with `exintro` for intro only, or no parameter for full content
- **Language codes**: `en`, `vi`, `zh`, `ja`, `ko`, `fr`, `de`, `es` — query any Wikimedia language subdomain
- **Greek/special characters in titles**: The `titles` parameter with `|` separator fails when titles contain Greek letters (NF-κB), subscripts (TNFα), or other non-ASCII Unicode. Use `pageids=` instead (see `wiki_extract_by_pageid()` below) or pass raw Python Unicode strings (never pre-encoded like `NF-%CE%BAB`).

## Pageid-based extraction (avoids title encoding issues)

When titles contain Greek/special characters, use numeric page IDs instead of title strings:

```python
def wiki_extract_by_pageid(pageids, lang='en'):
    \"\"\"Get plain-text extracts by numeric page ID (comma-separated).
    Avoids all title-encoding issues with Greek/special characters.\"\"\"
    params = urllib.parse.urlencode({
        'action': 'query', 'pageids': pageids,
        'prop': 'extracts', 'explaintext': 1, 'format': 'json',
        'exlimit': 20
    })
    url = f'https://{lang}.wikipedia.org/w/api.php?{params}'
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=15)
    data = json.loads(resp.read().decode())
    result = {}
    for pid, pg in data.get('query', {}).get('pages', {}).items():
        if 'extract' in pg:
            result[pg['title']] = pg['extract']
    return result

# Usage: search first, then extract by pageid
hits = wiki_search('NF-kB signaling pathway', limit=5)
pageids = ','.join(str(h['pageid']) for h in hits)
extracts = wiki_extract_by_pageid(pageids)
```

## See Also

- Wikipedia API Sandbox: https://en.wikipedia.org/wiki/Special:ApiSandbox
- Full API docs: https://en.wikipedia.org/w/api.php?action=help
- Skill parent: `web-research` — Level 2a section
