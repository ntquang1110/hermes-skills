# PubMed NCBI E-utilities API Research Patterns

Working patterns for scientific literature research via the NCBI E-utilities API.
Tested July 2026 — all endpoints return clean JSON/XML with no CAPTCHAs.

## Quick-reference endpoints

| Endpoint | URL | Use case |
|----------|-----|----------|
| Search | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=QUERY&retmax=N&retmode=json` | Get PMIDs for a keyword query |
| Summary | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=PMID1,PMID2&retmode=json` | Get titles, journals, DOIs, authors |
| Fetch | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=PMID1,PMID2&retmode=xml&rettype=abstract` | Get full abstracts in XML |

## Terminal one-liners (all work from bash)

### Search for article IDs
```bash
curl -sL --max-time 15 \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=probiotics+swine+gut+health&retmax=5&retmode=json" \
  | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('esearchresult',{}).get('idlist',[]))"
```

### Get titles + journals for article IDs
```bash
curl -sL --max-time 15 \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=42450761,42439553,42287552&retmode=json" \
  | python -c "
import sys,json
d = json.load(sys.stdin)
for uid in d.get('result',{}).get('uids',[]):
    info = d['result'][uid]
    print(f'[{uid}] {info.get(\"title\",\"?\")}')
    print(f'  {info.get(\"source\",\"\")} ({info.get(\"pubdate\",\"\")})')
    doi = info.get('elocationid','')
    if doi: print(f'  DOI: {doi}')
    authors = [a.get('name','') for a in info.get('authors',[])[:3]]
    if authors: print(f'  Authors: {\", \".join(authors)}')
    print()
"
```

### Fetch abstracts
```bash
curl -sL --max-time 20 \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=42450761&retmode=xml&rettype=abstract" \
  | python -c "
import sys, re
d = sys.stdin.read()
abstracts = re.findall(r'<AbstractText[^>]*>(.*?)</AbstractText>', d, re.DOTALL)
for a in abstracts:
    t = re.sub(r'<[^>]+>', '', a).strip()
    if len(t) > 50:
        print(t[:800])
"
```

## Complete Python workflow (copy-paste ready)

```python
import urllib.request, json, ssl, re
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

def pubmed_search(query, max_results=5):
    """Search PubMed, return list of PMIDs."""
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={urllib.parse.quote(query)}&retmax={max_results}&retmode=json'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=20)
    data = json.loads(resp.read().decode())
    return data.get('esearchresult', {}).get('idlist', [])

def pubmed_summaries(pmids):
    """Get titles, journals, DOIs, authors for PMIDs."""
    ids = ','.join(pmids)
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={ids}&retmode=json'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=20)
    data = json.loads(resp.read().decode())
    result = {}
    for uid, info in data.get('result', {}).items():
        if uid == 'uids':
            continue
        # Extract clean DOI from articleids array (more reliable than elocationid)
        doi = ''
        for aid in info.get('articleids', []):
            if aid.get('idtype') == 'doi':
                doi = aid.get('value', '')
                break
        result[uid] = {
            'title': info.get('title', ''),
            'source': info.get('source', ''),
            'pubdate': info.get('pubdate', ''),
            'doi': doi,
            'authors': [a.get('name', '') for a in info.get('authors', [])[:3]]
        }
    return result

def pubmed_abstracts(pmids):
    """Fetch full abstracts for PMIDs."""
    ids = ','.join(pmids)
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={ids}&retmode=xml&rettype=abstract'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=20)
    xml_data = resp.read().decode('utf-8', errors='replace')
    abstracts = {}
    for pmid in pmids:
        # Use a per-PMID extraction to preserve mapping
        pattern = rf'<PubmedArticle>\s*<MedlineCitation[^>]*>.*?<PMID Version="1">{pmid}</PMID>.*?<Abstract>(.*?)</Abstract>'
        match = re.search(pattern, xml_data, re.DOTALL)
        if match:
            abstract_section = match.group(1)
            texts = re.findall(r'<AbstractText[^>]*>(.*?)</AbstractText>', abstract_section, re.DOTALL)
            abstract_text = ' '.join(re.sub(r'<[^>]+>', '', t).strip() for t in texts)
            if abstract_text.strip():
                abstracts[pmid] = abstract_text
        else:
            # Fallback: find any AbstractText block
            texts = re.findall(r'<AbstractText[^>]*>(.*?)</AbstractText>', xml_data, re.DOTALL)
            if texts:
                abstracts[pmid] = re.sub(r'<[^>]+>', '', texts[0]).strip()[:500]
    return abstracts

# Usage
query = 'probiotics swine gut health'
pmids = pubmed_search(query, 5)
summaries = pubmed_summaries(pmids)
abstracts = pubmed_abstracts(pmids)

for pmid in pmids:
    s = summaries.get(pmid, {})
    print(f'=== PMID {pmid} ===')
    print(f'Title: {s.get(\"title\", \"?\")}')
    print(f'Source: {s.get(\"source\", \"\")} ({s.get(\"pubdate\", \"\")})')
    print(f'DOI: {s.get(\"doi\", \"\")}')
    if pmid in abstracts:
        print(f'Abstract: {abstracts[pmid][:600]}...')
    print()
```

## Query syntax tips

| Pattern | Example | Effect |
|---------|---------|--------|
| AND (default) | `probiotics swine` | Both terms required |
| OR | `probiotics OR prebiotics` | Either term |
| Phrase | `\"gut health\"` | Exact phrase match |
| Field search | `probiotics[title]` | Search only in title |
| Date range | `2024:2026[dp]` | Publications 2024-2026 |
| Boolean grouping | `(probiotics OR prebiotics) AND swine` | Grouped logic |

## Rate limits

| Endpoint | No API key | With API key | Practical limit |
|----------|------------|-------------|-----------------|
| esearch | 3 req/sec | 10 req/sec | Virtually unlimited for normal use |
| esummary | 3 req/sec | 10 req/sec | 10+ rapid calls fine |
| efetch | 3 req/sec | 10 req/sec | Pace with 1s gap for >5 IDs |

Get a free API key: https://www.ncbi.nlm.nih.gov/account/
Use it as: `&api_key=YOUR_KEY` appended to any E-utilities URL.

## When to use PubMed vs. Wikipedia

| Criterion | Use PubMed | Use Wikipedia |
|-----------|-----------|---------------|
| Need peer-reviewed evidence | ✅ | ❌ |
| Quick overview / definitions | ❌ | ✅ |
| Recent discoveries (2025+) | ✅ | ❌ (stale) |
| Historical context / milestones | ❌ | ✅ |
| Clinical trials / RCT data | ✅ | ❌ |
| Mechanisms / pathways | ✅ | ✅ (supplementary) |
| Contact info / suppliers | ❌ | ❌ (use Level 3) |

## Citation format for research deliverables

When citing PubMed results in a knowledge card, use:

```
[Author(s), Journal, Year]
```

Example: [Bacillus subtilis Supplementation in Weanling Piglets, Animals (Basel), 2026]
