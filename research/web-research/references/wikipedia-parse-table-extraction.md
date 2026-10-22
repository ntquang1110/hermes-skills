# Wikipedia Parse API — Table & Section Extraction

## Overview

The `action=parse` endpoint (unlike `action=query&prop=extracts`) returns **HTML-structured content** with tables, lists, and section hierarchy preserved. Use this when you need to extract **tabular data** (statistical rankings, production tables, comparison matrices) that `explaintext` flattens into unparseable prose.

## Key endpoint parameters

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `action` | `parse` | Invoke the parse API |
| `page` | `Page_Title` | The Wikipedia page (use underscores for spaces) |
| `section` | `17` | **Numeric section index** — fetch only one section's HTML |
| `prop` | `text` | Return the rendered HTML of the section |
| `format` | `json` | Structured JSON output |

### Finding section indices

Use `prop=sections` to discover section numbers without fetching content:

```
https://en.wikipedia.org/w/api.php?action=parse&page=Rare-earth_element&prop=sections&format=json
```

Each section has an `index` (string) and `toclevel`. Vietnam-specific sections might be nested under "Production by country" at toclevel=3.

### Fetching a specific section's HTML

```python
import urllib.request, json, ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

def wiki_section_html(page, section_index, lang='en'):
    """Get the HTML of a specific section from a Wikipedia page."""
    url = (f'https://{lang}.wikipedia.org/w/api.php?'
           f'action=parse&page={urllib.parse.quote(page)}'
           f'&section={section_index}&prop=text&format=json')
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=15)
    data = json.loads(resp.read().decode())
    return data.get('parse', {}).get('text', {}).get('*', '')
```

## Extracting wikitable data via regex

Wikipedia's `<table class="wikitable">` elements have a consistent HTML structure. This pattern extracts rows and cells:

```python
def extract_wikitable_rows(html):
    """Extract all rows from the first wikitable in HTML."""
    import re
    # Find the first wikitable
    table_match = re.search(
        r'<table[^>]*class="[^"]*wikitable[^"]*"[^>]*>(.*?)</table>',
        html, re.DOTALL
    )
    if not table_match:
        return []
    
    table_html = table_match.group(1)
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table_html, re.DOTALL)
    
    result = []
    for row in rows:
        cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row, re.DOTALL)
        clean_cells = []
        for c in cells:
            c = re.sub(r'<[^>]+>', ' ', c)        # strip HTML tags
            c = re.sub(r'\[\d+\]', '', c)          # strip reference markers [1][2]
            c = re.sub(r'\s+', ' ', c).strip()     # collapse whitespace
            c = c.replace('&#160;', ' ')           # non-breaking space
            clean_cells.append(c)
        result.append(clean_cells)
    return result
```

### Usage: extract a statistical ranking table

```python
# Step 1: Get section indices
url = 'https://en.wikipedia.org/w/api.php?action=parse&page=Rare-earth_element&prop=sections&format=json'
# ... parse and find section 17 = "Production by country"

# Step 2: Fetch that section's HTML
html = wiki_section_html('Rare-earth_element', '17')

# Step 3: Extract the wikitable
rows = extract_wikitable_rows(html)
for row in rows:
    print(' | '.join(row[:8]))

# Output:
# Rank | Country | Reserves (million metric tons) | Reserves per capita (kg)
# — | World | 130 | 15.73
# 1 | China | 44 | 31.07
# 2 | Brazil | 21 | 98.39
# ...
# 6 | Vietnam | 3.5 | 34.45
```

### Usage: filter for specific rows

```python
# After rows = extract_wikitable_rows(html)
for row in rows:
    cells = [c for c in row if c]  # skip empty cells
    if any('Vietnam' in c for c in cells):
        print(' | '.join(cells))
# Output: 6 | Vietnam | 3.5 | 34.45
```

## Terminal quick probes

```bash
# Find section indices
curl -sL --max-time 15 \
  "https://en.wikipedia.org/w/api.php?action=parse&page=Rare-earth_element&prop=sections&format=json" \
  -H "User-Agent: Mozilla/5.0" \
  | python -c "import sys,json; d=json.load(sys.stdin); [print(f\"{s['index']}: {s['line']} (toclevel={s['toclevel']})\") for s in d['parse']['sections']]"

# Fetch section 17 and extract table rows
curl -sL --max-time 15 \
  "https://en.wikipedia.org/w/api.php?action=parse&page=Rare-earth_element&section=17&prop=text&format=json" \
  -H "User-Agent: Mozilla/5.0" \
  | python -c "
import sys,json,re
d=json.load(sys.stdin)
html = d['parse']['text']['*']
t = re.search(r'<table[^>]*class=\"[^\"]*wikitable[^\"]*\"[^>]*>(.*?)</table>', html, re.DOTALL)
if t:
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', t.group(1), re.DOTALL)
    for r in rows:
        cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, re.DOTALL)
        clean = [re.sub(r'<[^>]+>',' ',c).strip() for c in cells]
        print(' | '.join(clean[:8]))
"

# Multi-section exploration — fetch sections 15-18 in sequence
for i in 15 16 17 18; do
  echo "=== Section $i ==="
  curl -sL --max-time 15 \
    "https://en.wikipedia.org/w/api.php?action=parse&page=Rare-earth_element&section=$i&prop=text&format=json" \
    -H "User-Agent: Mozilla/5.0" \
    | python -c "import sys,json,re; d=json.load(sys.stdin); h=d['parse']['text']['*']; t=re.sub(r'<[^>]+>',' ',h)[:500]; print(t)"
done
```

## Combined workflow: section → table → explaintext context

For research pages with both statistical tables and descriptive prose:

```python
def wiki_section_context(page, section_index, lang='en'):
    """Get both the structured HTML and plain-text of a section."""
    # HTML (for table extraction)
    html = wiki_section_html(page, section_index, lang)
    tables = extract_wikitable_rows(html)
    
    # Plain text (for context)
    import urllib.parse
    params = urllib.parse.urlencode({
        'action': 'query', 'titles': page,
        'prop': 'extracts', 'explaintext': 1,
        'format': 'json'
    })
    url = f'https://{lang}.wikipedia.org/w/api.php?{params}'
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=15)
    data = json.loads(resp.read().decode())
    pages_data = data.get('query', {}).get('pages', {})
    pid = list(pages_data.keys())[0]
    text = pages_data[pid].get('extract', '')
    
    return {'tables': tables, 'text': text}
```

## When to use Parse API vs Query+Extracts

| Need | Use | Why |
|------|-----|-----|
| **Statistical tables** (rankings, production, reserves) | `action=parse` + `section=` | HTML preserves `<table>` structure for regex extraction |
| **Descriptive prose** (company history, deal terms, mechanisms) | `action=query&prop=extracts&explaintext=1` | Clean plain text, no HTML to strip |
| **Nested lists with values** | Try `action=parse` first | `explaintext` may flatten bullet hierarchies |
| **Infobox data** (right-side summary boxes) | `action=parse` on the full page | Infoboxes are `<table>` elements too |
| **Discovery/overview** | `action=query&list=search` | Keyword search is only available via the Query API |

## Pitfalls

- **Section indices are string-typed** — The API returns `"17"` as a string, but accepts both string and integer in the request.
- **Sections change when pages are edited** — Section indices can shift. Always fetch `prop=sections` at the start of a session; don't hardcode section numbers from memory.
- **Nested sections** — A section at `toclevel=2` may contain subsections at `toclevel=3` with their own indices. Use the index of the *header* section (lowest index among siblings) to fetch the subsection group.
- **No explaintext on parse** — The parse API always returns HTML. To get plain text from the same section, use `intestaction=parse` with `prop=text` stripped, or query with `prop=extracts` on the full page and search within.
- **Rate limits** — Parse API is slightly more expensive than query. Pace with `time.sleep(1)` for batch section fetching.
- **Reference markers** in table cells look like `[12][45]`. Strip with `re.sub(r'\[\d+\]', '', cell)`.
- **HTML entities** — `&#160;` (non-breaking space) appears frequently in tables. Replace with regular space before stripping.
- **Multi-wikitable pages** — Some pages have multiple `<table class="wikitable">`. Always extract from the correct one by index: `re.finditer(...)` and pick the [N]th match.
