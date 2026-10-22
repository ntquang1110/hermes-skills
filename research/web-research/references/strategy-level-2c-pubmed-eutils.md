# Strategy hierarchy — Level 2c: PubMed NCBI E-utilities API (+ Crossref finance, sparse-literature fallback, gap analysis)

### Level 2c: PubMed NCBI E-utilities API — Scientific/medical literature (BEST for peer-reviewed research)

When the research requires **peer-reviewed scientific literature** (medicine, biology, veterinary, chemistry), skip directly to the NCBI E-utilities API. This API is designed for programmatic access, never blocks with CAPTCHAs, and returns clean JSON/XML without JavaScript.

**Why it works:** The NCBI E-utilities API (`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`) is explicitly built for automated queries by third-party tools. It accepts requests without authentication for basic usage, handles 10+ rapid calls without rate-limiting (on `esearch` and `esummary`), and provides structured publication metadata including abstracts, DOIs, authors, and publication dates.

**Three core endpoints:**

| Endpoint | Purpose | Output |
|----------|---------|--------|
| `esearch.fcgi` | Search PubMed for article IDs | JSON/XML list of PMIDs |
| `esummary.fcgi` | Get titles, authors, sources, DOIs by PMID | JSON/XML summaries |
| `efetch.fcgi` | Get full abstracts by PMID | XML with `<AbstractText>` |

**Step 1 — Search for article IDs:**
```python
import urllib.request, json, ssl
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

def pubmed_search(query, max_results=5):
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={urllib.parse.quote(query)}&retmax={max_results}&retmode=json'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=20)
    data = json.loads(resp.read().decode())
    return data.get('esearchresult', {}).get('idlist', [])
```

**Step 2 — Get summaries (titles, journals, DOIs):**
```python
def pubmed_summaries(pmids):
    """Use articleids array for reliable DOI extraction (avoids elocationid prefix issues)."""
    pmid_str = ','.join(pmids)
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid_str}&retmode=json'
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
```

**Step 3 — Fetch full abstracts (per-PMID context matching):**

**⚠️ Pitfall — abstract-scope bug:** A naive `<AbstractText>` regex finds the *first* abstract in the whole XML document for every PMID, silently mapping every article to the first article's abstract. Always scope the match to each article's `<PubmedArticle>` block:

```python
def pubmed_abstracts(pmids):
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={",".join(pmids)}&retmode=xml&rettype=abstract'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=20)
    xml_data = resp.read().decode('utf-8', errors='replace')
    abstracts = {}
    for pmid in pmids:
        # Scope to this article's block — prevents cross-article abstract contamination
        article_pattern = rf'<PubmedArticle>.*?<PMID Version="1">{pmid}</PMID>(.*?)</PubmedArticle>'
        article_match = re.search(article_pattern, xml_data, re.DOTALL)
        if article_match:
            article_xml = article_match.group(1)
            ab_match = re.search(r'<AbstractText[^>]*>(.*?)</AbstractText>', article_xml, re.DOTALL)
            if ab_match:
                abstracts[pmid] = re.sub(r'<[^>]+>', '', ab_match.group()).strip()
    return abstracts
```

**Complete workflow — search, summarize, fetch abstracts:**
```python
query = 'probiotics swine gut health'
pmids = pubmed_search(query, 5)
summaries = pubmed_summaries(pmids)
abstracts = pubmed_abstracts(pmids)
for pmid in pmids:
    s = summaries.get(pmid, {})
    print(f'[{pmid}] {s.get("title", "?")}')
    print(f'  {s.get("source", "")} ({s.get("pubdate", "")})')
    print(f'  DOI: {s.get("doi", "")}')
    if pmid in abstracts:
        print(f'  Abstract: {abstracts[pmid][:500]}')
```

**⚠️ Query specificity trap — broad nutrient/compound topics return noise:**

When researching a **broad nutrient or compound** that appears in many contexts (e.g. an amino acid common in feed, a widely studied mineral, a generic biomarker), generic queries like `"arginine pig growth performance"` or `"copper pig health"` return mostly irrelevant papers — the compound is just one of many variables measured, not the paper's focus. PubMed's FTS will match any paper that mentions the term at all. **Fix:** construct each query around a **specific mechanism or pathway**, not the compound itself. Use terms like `tight junction`, `mTOR`, `iNOS`, `arginase`, `placental angiogenesis`, `CD3ζ`, `autophagy flux` paired with the species. If the first query round returns mostly tangentially relevant papers, the queries are too broad — refine them before fetching abstracts.

| Query type | Example | Result quality |
|-----------|---------|---------------|
| **Too broad** | `arginine pig growth performance` | Mostly irrelevant — arginine is one of many AA in a growth trial |
| **Good** | `arginine nitric oxide intestinal barrier tight junction pig` | Directly relevant mechanism papers |
| **Good** | `arginine mTOR polyamine cell proliferation pig intestine` | Mechanism-focused, filters noise |
| **Best practice** | Start with 1-2 broad probes → if noise > signal, switch to mechanism-specific queries immediately | Saves API calls + context window |

**Multi-query research pattern — search from multiple angles:**

For complex topics spanning subtopics (mechanism, barrier function, antimicrobial effects), search PubMed from several angles and merge results into a single deduplicated set. This catches articles a single query would miss:

```python
queries = [
    'zinc oxide intestinal barrier tight junction pig',
    'zinc oxide antimicrobial mechanism gut microbiota swine',
    'pharmacological zinc piglet diarrhea mechanism',
]
all_articles = {}
for i, query in enumerate(queries):
    pmids = pubmed_search(query, 5)
    summaries = pubmed_summaries(pmids)
    for pmid in pmids:
        if pmid not in all_articles:
            all_articles[pmid] = summaries.get(pmid, {})
    time.sleep(1.5)  # pace between query groups

# Fetch abstracts for the merged set
merged_pmids = list(all_articles.keys())[:8]
abstracts = pubmed_abstracts(merged_pmids)
for pmid in merged_pmids:
    s = all_articles[pmid]
    print(f'[{pmid}] {s.get("title","")}')
    if pmid in abstracts:
        print(f'  {abstracts[pmid][:500]}')
```

This pattern ensures you capture articles about each mechanism facet without relying on a single query to cover everything. Always pace with `time.sleep(1.5)` between query groups — `efetch` is more rate-sensitive than `esearch`.

**⚠️ "No-review" workaround — when mechanism-specific queries return zero results:**

When researching a **porcine-specific pathway, protein family, or molecular system** that lacks dedicated review papers in the swine literature, even tight mechanism-specific queries like `"chemokine receptor pig"` or `"CXCL8 pig intestinal barrier"` may return zero or nearly zero results. This is **different from the "noise" problem above** — here the issue is absence of dedicated literature, not irrelevant matches. The porcine immunology literature is organized around **disease models** (PRRSV, ASFV, PEDV, PDCoV, ETEC, S. suis), not around individual pathway components. Each disease paper profiles multiple chemokines/cytokines, so your pathway appears as one readout among many, not the paper's central focus.

**Fix:** switch from mechanism-specific queries to **disease/virus-specific queries**:

| Problem pattern (returns 0) | Better approach (returns results) |
|----------------|-----------------------------------|
| `chemokine system pig review` → 0 hits | `PRRSV chemokine pig` → relevant papers |
| `CXCR1 CXCR2 pig expression` → 0 hits | `CXCL8 pig lung inflammation` → hits |
| `CCL20 pig porcine Th17` → 0 hits | `PEDV CCL20 pig intestinal` → hits |
| `chemokine receptor pig T cell` → 0 hits | `porcine CXCL10 IFN gamma Th1` → hits |

**Workflow:**
1. Start with mechanism-specific queries (standard approach) — if they return 3+ relevant hits, proceed
2. If they return 0-2 results after 3 attempts with different phrasing, switch to **disease-specific queries**
3. Collect articles from multiple disease contexts → merge → deduplicate → fetch abstracts
4. Wikipedia API (Level 2a) fills in the fundamental pathway biology; PubMed provides porcine-specific expression/function data from disease models. You combine both sources: Wikipedia for the mechanism, PubMed for species-specific data.

**Terminal quick probe (curl + python -c):**
```bash
# Search PubMed
curl -sL --max-time 15 \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=probiotics+swine&retmax=3&retmode=json" \
  | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('esearchresult',{}).get('idlist',[]))"

# Get summaries
curl -sL --max-time 15 \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=42450761,42287552&retmode=json" \
  | python -c "import sys,json; d=json.load(sys.stdin); [print(d['result'][k].get('title','')) for k in d['result']['uids']]"
```

**⚠️ Cron-mode note:** `python -c` may be blocked in strict cron approval configs. Try it first; if it fails, use `curl -o results.json` + `read_file` (Pattern A).
```

**Best for:** Peer-reviewed scientific literature, medical/biological research, veterinary science, clinical studies, systematic reviews, and any task requiring credible published evidence.

**Pitfalls:**
- **No full text**: The API returns abstracts only (except open-access articles). For full text, note the DOI and access via the publisher's site.
- **Query syntax**: Use `+` for AND, `OR` for alternatives, `[title]` for field-specific searches. Standard PubMed query syntax applies.
- **Rate limits**: `esearch` and `esummary` handle ~10 rapid calls easily. `efetch` is more conservative — pace with `time.sleep(1)`. For bulk (>50 IDs), use the batch endpoint (`/entrez/eutils/efetch.fcgi?retmax=50`).
- **⚠️ NCBI `RemoteDisconnected` on rapid sequential calls (tested Jul 2026)**: after ~8–10 back-to-back `esearch` calls, NCBI can forcibly close the connection (`http.client.RemoteDisconnected: Remote end closed connection without response`) — not a 429, a connection reset. **Fix:** wrap EVERY E-utilities call in a retry helper with backoff (`sleep 5*(attempt+1)`, 3-4 tries) and pace query groups with `time.sleep(3)` between searches. Full pattern: `references/kf-large-kb-and-pubmed-pitfalls.md`.
- **⚠️ Verify remembered PMIDs before citing (never trust memory)**: when a classic paper comes to mind (e.g. "Shoba 1998 — piperine increases curcumin bioavailability ~20×"), do NOT write its PMID into a card from memory. Run a 2-second `esearch` on the remembered title/author to confirm the ID, then `esummary` to capture journal/year/DOI. Tested 2026-08: confirmed PMID 9619120 (Shoba G, Planta Med 1998) this way before including it — the resulting 20-PMID reference table had zero fabricated citations. This also yields the DOI needed for the card's reference table in the same call.
- **No CAPTCHA ever**: Unlike DDG Lite, the E-utilities API never blocks automated requests. If you get empty results, check your query syntax, not blocking.
- **API key optional**: Without an API key, the rate limit is ~3 requests/second. With a free NCBI API key, it increases to ~10/second. Sign up at https://www.ncbi.nlm.nih.gov/account/.
- **⚠️ Field-tag brackets + extra parentheses crash inline python**: When running `curl ... "https://eutils.ncbi.nlm.nih.gov/...?term=...&retmode=json" | python -c "import sys,json; ..."` from bash, wrapping a PubMed field tag (`[Title]`) inside extra parentheses — e.g. `(leucine[Title])` — can cause the NCBI server to return a non-JSON error page. The `python -c` then crashes with `JSONDecodeError: Expecting value: line 1 column 1 (char 0)`. **Fix:** do NOT wrap field-tagged terms in extra parentheses. The `[Title]` brackets are already the grouping operator. Write `leucine[Title]+AND+...` not `(leucine[Title])+AND+...`. Extra parentheses around plain terms (no brackets) are fine: `(mTOR+OR+mTORC1)` works correctly. The crash shows as an empty output with a JSON parse error — the same symptom as an empty response but the root cause is a malformed query, not missing data.
- **⚠️ F-string + `.join()` syntax error in terminal**: The `pubmed_summaries` and `pubmed_abstracts` functions above use `{",".join(pmids)}` inside f-strings with double-quoted commas. This works in standalone `.py` files but **crashes with `SyntaxError: f-string: expecting '}'` when the same code is pasted into a `python -c "..."` single-quoted context** (because the `'` in `.join()` breaks the outer quoting). **Fix:** always assign the comma-joined string to a variable first:
  ```python
  pmid_str = ','.join(pmids)
  url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid_str}&retmode=json'
  ```
  This avoids the nested-quote conflict entirely and works identically in `.py` files and inline `python -c` commands.
- **⚠️ Bash loop + `python -c` variable scoping**: When using a bash `for pmid in 12345 67890; do ... python -c "..." ; done` loop to fetch per-PMID data from PubMed, the `pmid` loop variable is **not accessible** inside the `python -c "..."` single-quoted string — bash expands shell variables inside double quotes but NOT inside single quotes. The `python -c "..."` body sees `pmid` as a Python variable name, not the shell variable's value. **Symptom:** `NameError: name 'pmid' is not defined` crashes the python one-liner but bash continues the loop, producing empty output for every iteration with no visible error. **Fix:** pass the shell variable as a Python command-line argument:  
  `python -c "import sys; pmid=sys.argv[1]; ..." "$pmid"`  
  Or better, avoid bash loops entirely and loop in Python where variable scoping is native.

**See** `references/pubmed-wikipedia-scientific-workflow.md` for the complete workflow.

**For a full worked example** of multi-angle immunology research (Th17/Treg in swine) covering topic discovery, Wikipedia+PubMed API usage, and KF card creation, see `references/immunology-research-worked-example.md`.

**Finance/economics (💰 Tài chính rotation: CFA/Quant/M&A): PubMed useless → Crossref REST. 4 verified DOI banks — factor/quant (12), fixed-income/CFA (12), options (9), VaR/ES risk (10) — + worked-example scripts: `references/crossref-finance-doi-bank.md` + `scripts/duration_convexity_calc.py` + `scripts/black_scholes_calc.py` + `scripts/var_es_calc.py`.**

**Triple-fallback for extremely sparse literature:** When both mechanism-specific AND disease-specific PubMed queries return 0-2 results (for very niche porcine targets), see `references/porcine-sparse-literature-triple-fallback.md` for the extended pattern: broad OR query → Wikipedia pathway biology → general PubMed reviews → extrapolation with caveats.

**Gap analysis:**

```bash
# DETECT mode — scan all cards, report structural gaps
python <skill_path>/scripts/kf-gap-analysis.py

# CHECK mode — verify specific candidate topics
python <skill_path>/scripts/kf-gap-analysis.py --candidates "Th2,IL-5,eosinophil,IgE"

# Point at a different KF instance
python <skill_path>/scripts/kf-gap-analysis.py --url http://192.168.1.100:3003 --candidates "colostrum,maternal,adjuvant"
```

Output gives coverage levels: FULL (word-boundary title match), PARTIAL (substring match), GAP (no match). Use this when the research queue is empty to find what topic to research next.

