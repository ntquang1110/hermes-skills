# PubMed + Wikipedia Combined Scientific Research Workflow

> Tested Jul 2026: pig gut microbiota + immune system (HEO domain)

## Why this works

| API | Endpoint | Rate limit | Output quality |
|-----|----------|-----------|----------------|
| Wikipedia REST API | `/api/rest_v1/page/summary/<title>` | ~6/min on `/page/html/`, ~15/min on `/page/summary/` | Broad background, definitions, cited overviews |
| PubMed E-utilities | `eutils.ncbi.nlm.nih.gov/entrez/eutils/` | ~3/sec unauth, ~10/sec with API key | Peer-reviewed papers, structured metadata, DOIs, abstracts |

No CAPTCHAs, no JavaScript, no blocking — both APIs are designed for programmatic access.

## Recommended order

```
Phase 1: Wikipedia (Context)
  → Fetch 3-5 related topic summaries for broad background
  → Identifies key terms, pathways, concepts
  → Rate: time.sleep(1) between calls

Phase 2: PubMed (Evidence)
  → esearch.fcgi with 3-5 carefully crafted queries
  → esummary.fcgi to get structured data (authors, journals, DOIs, dates)
  → efetch.fcgi for abstracts (XML parsing)
  → Rate: time.sleep(1.5) between queries
```

## Phase 1: Wikipedia background research

```python
import urllib.request, json, ssl, time

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

def wiki_summary(title):
    """Fetch Wikipedia page summary by canonical title."""
    url = f'https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=10)
    data = json.loads(resp.read().decode())
    return data  # keys: extract, titles, content_urls.desktop.page, thumbnail

# Batch related topics with pacing
topics = ['Gut_microbiota', 'Mucosal_immune_system', 'Short-chain_fatty_acid',
          'Intestinal_epithelium', 'Swine']
for topic in topics:
    try:
        data = wiki_summary(topic)
        print(f'=== {topic} ===')
        print(data['extract'][:300])
    except Exception as e:
        print(f'FAIL: {topic}: {e}')
    time.sleep(1)  # critical — avoid 429 on /page/html/ endpoint
```

**Key fields in response:**
- `data['extract']` — plain-text first section (500-2000 chars)
- `data['titles']['canonical']` — canonical title for follow-up
- `data['content_urls']['desktop']['page']` — full URL for human reference
- `data['thumbnail']['source']` — lead image (if exists)

**Pacing rules:**
- `/page/summary/`: `time.sleep(1)` between calls is sufficient
- `/page/html/`: `time.sleep(3)` between calls; implement retry on HTTP 429
- Batch up to 12 summary calls in a single session

## Phase 2: PubMed literature search

### Step 1 — Search for article IDs

```python
def pubmed_search(query, max_results=5):
    url = ('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
           '?db=pubmed'
           f'&term={urllib.parse.quote(query)}'
           f'&retmax={max_results}'
           '&retmode=json')
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=20)
    data = json.loads(resp.read().decode())
    return data.get('esearchresult', {}).get('idlist', [])
```

### Step 2 — Get structured summaries

```python
def pubmed_summaries(pmids):
    """Fetch titles, journals, DOIs, authors for a list of PMIDs."""
    if not pmids:
        return {}
    ids = ','.join(pmids)
    url = ('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
           f'?db=pubmed&id={ids}&retmode=json')
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=20)
    data = json.loads(resp.read().decode())
    result = {}
    for uid, info in data.get('result', {}).items():
        if uid == 'uids':
            continue
        result[uid] = {
            'title': info.get('title', ''),
            'source': info.get('source', ''),
            'pubdate': info.get('pubdate', ''),
            'doi': info.get('elocationid', ''),
            'authors': [a.get('name', '') for a in info.get('authors', [])[:3]]
        }
    return result
```

### Step 3 — Fetch abstracts

```python
import re

def pubmed_abstracts(pmids):
    "Fetch full abstracts for a list of PMIDs (XML parsing). Uses per-PMID scoping to avoid cross-article abstract contamination."
    ids = ','.join(pmids)
    url = ('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
           f'?db=pubmed&id={ids}&retmode=xml&rettype=abstract')
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=20)
    xml_data = resp.read().decode('utf-8', errors='replace')
    abstracts = {}
    for pmid in pmids:
        # Scope extraction to this PMID's article block
        article_pattern = rf'<PubmedArticle>.*?<PMID Version="1">{pmid}</PMID>(.*?)</PubmedArticle>'
        article_match = re.search(article_pattern, xml_data, re.DOTALL)
        if article_match:
            article_xml = article_match.group(1)
            texts = re.findall(r'<AbstractText[^>]*>(.*?)</AbstractText>', article_xml, re.DOTALL)
            if texts:
                abstract_text = ' '.join(re.sub(r'<[^>]+>', '', t).strip() for t in texts)
                abstracts[pmid] = abstract_text
    return abstracts
```

### Complete workflow

```python
# 1. Search
queries = [
    'pig gut microbiota immune system review',
    'swine microbiome intestinal immunomodulation SCFA',
    'porcine gut microbiota probiotics growth performance',
    'piglet gut microbiota development immune maturation'
]

all_papers = {}
for q in queries:
    print(f'=== {q} ===')
    pmids = pubmed_search(q, 4)
    if pmids:
        summaries = pubmed_summaries(pmids)
        for pmid in pmids:
            s = summaries.get(pmid, {})
            all_papers[pmid] = s
            print(f'  PMID:{pmid} | {s.get("pubdate","?")}')
            print(f'  {s.get("title", "?")[:100]}')
            print(f'  {s.get("source", "")} | DOI: {s.get("doi", "")}')
    time.sleep(1.5)  # critical pacing

# 2. Export as structured data for knowledge card
for pmid, s in all_papers.items():
    print(f'{s.get("title")} [{s.get("source")}, {s.get("pubdate")}]')
```

## Query crafting tips

| Goal | Query pattern | Example |
|------|--------------|---------|
| Broad review | `[topic] review` | `pig gut microbiota immune system review` |
| Mechanism | `[topic] [mechanism] [pathway]` | `swine microbiome intestinal immunomodulation SCFA` |
| Application | `[topic] [intervention] [outcome]` | `porcine gut microbiota probiotics growth performance` |
| Development | `[stage] [system] [process]` | `piglet gut microbiota development immune maturation` |
| Molecular | `[molecule] [species] [effect]` | `short chain fatty acids pig intestinal immune GPR43` |

## Vietnamese knowledge card format

When compiling research into a knowledge card (posted to an API or saved as markdown), use this structure:

```markdown
## 🧬 [Mechanism/Overview]

**Mô tả bản chất:** [Deep explanation of the core mechanism]

### [Component/Section 1]:
- **Entity** → role/molecular mechanism

### [Section 2]:
| Column1 | Column2 | Column3 | Column4 |
|---------|---------|---------|---------|
| Data    | Data    | Data    | Data    |

> 🔬 **Bản chất cốt lõi:** [One-sentence insight that captures the essence]

### [Application section]:
- Practical recommendation 1
- Practical recommendation 2

## 📚 Tài liệu tham khảo
1. Author A, Author B (Year). 'Title.' *Journal*, Vol(Issue):Pages.
2. ...

## 🔗 Nguồn trực tuyến
- Wikipedia: Topic — https://en.wikipedia.org/wiki/Topic
```

**Rules:**
- Vietnamese with full diacritics (dấu đầy đủ)
- Real emoji (🐷🧬🦠⚕️🧪🔬), NOT :shortcode: style
- Every factual claim needs a citation (Author, Year, Publication)
- Tables for comparative data (SCFA types, probiotic classes, bacterial phyla)
- Blockquotes for core insights (> 🔬)
- Include practical application section for translational value
- source_url should point to the primary reference (Wikipedia page or review paper)

## Pacing cheat sheet

| API | Endpoint | Calls allowed | Sleep between | Recovery on 429 |
|-----|----------|---------------|--------------|-----------------|
| Wikipedia Action API | /w/api.php | ~20/min | 2s | Retry after 30s |
| Wikipedia REST API | /api/rest_v1/page/summary/ | ~15/min | 2s | Retry after 30s |
| Wikipedia REST API | /api/rest_v1/page/html/ | ~6/min | 3s | Retry after 30s |
| PubMed esearch | eutils.ncbi.nlm.nih.gov | ~30/min (unauth) | 1s | Retry after 5s |
| PubMed esummary | eutils.ncbi.nlm.nih.gov | ~30/min (unauth) | 1s | Retry after 5s |
| PubMed efetch | eutils.ncbi.nlm.nih.gov | ~15/min (unauth) | 1.5s | Retry after 10s |

**Warning: Wikipedia Action API and REST API share the same rate limit bucket.**
Getting a 429 from /w/api.php means /api/rest_v1/ will also 429 for the cooldown period (~20-30s), and vice versa. They are NOT independent APIs for rate-limiting. Do NOT try to work around a 429 by switching from Action API to REST API - wait the full cooldown instead. Pace ALL Wikipedia calls (across both APIs) under a single throttle: 2s between any Wikipedia API call.

## Pitfalls encountered

1. **f-string with comma separator**: f'...id={",".join(pmids)}...' causes SyntaxError on Python 3.11. Fix: pre-assign the joined string to a variable.
2. **Wikipedia 429 on /page/html/**: More aggressive rate limiting than /page/summary/. Use /page/summary/ for quick probes.
3. **Wikipedia Action API + REST API share rate limits**: Getting 429 from one means the other will also 429 for 20-30s. Pace ALL Wikipedia calls under a single 2s throttle. Do not treat Level 2a and Level 2b as independent rate-limit pools.
4. **PubMed empty results**: If esearch returns 0 results, check query syntax - especially field-specific terms like [title] or [MeSH].
5. **MSYS path conversion on Windows**: Running python /c/tmp/script.py fails because git-bash converts /c/tmp/ to C:\c\tmp\. Use explicit Windows paths instead.
6. **delegate_task lag**: The subagent may not return before the main agent finishes. Design the workflow so the main agent can complete without waiting for the delegated subagent.
