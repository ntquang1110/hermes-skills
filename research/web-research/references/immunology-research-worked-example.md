# Immunology / Veterinary Biology Research — Worked Example

This reference documents the search + card-creation pattern used in the **Th17/Treg balance in swine** research session (Jul 2026). Use it as a template for similar immunology, molecular biology, or veterinary science research.

## Overview of the workflow

```
Phase 1: Topic discovery (check existing KF cards → identify gap)
Phase 2: Wikipedia background (Level 2a — Action API, pageid-based)
Phase 3: PubMed literature (Level 2c — multi-query from 4 angles)
Phase 4: Abstract extraction (scoped per-PMID matching)
Phase 5: Card compilation (structured sections in Vietnamese + English terms)
Phase 6: Final dedup → POST to KF (Pattern D — Python POST script)
```

---

## Phase 1: Topic discovery — comprehensive dedup

**Don't just check the last N cards.** Scan ALL cards with keyword matching:

```bash
# Full card list with indices
curl -s http://localhost:3003/api/cards \
  | python -c "import sys,json; cards=json.load(sys.stdin); \
  print(f'Total: {len(cards)} cards'); \
  [print(f'{i}: {c[\"title\"][:90]}') for i,c in enumerate(cards)]"

# Targeted keyword dedup across ALL cards (not just last 20)
curl -s http://localhost:3003/api/cards \
  | python -c "import sys,json; cards=json.load(sys.stdin); \
  keywords = ['Th17', 'Treg', 'FOXP3', 'RORgt', 'IL-17', 'regulatory T', 'helper 17']; \
  found = False; \
  for c in cards: \
    t = c['title'].lower(); \
    for kw in keywords: \
      if kw.lower() in t: \
        print(f'DUP: {c[\"title\"][:90]} (keyword: {kw})'); found = True; \
  if not found: print('No duplicates found')"
```

**What "novel" means:** A topic is novel if:
- No existing card title has >=60% keyword overlap
- No existing card covers the same mechanistic pathway at the same depth
- Partial overlap with a broader card (e.g. "Interferon, PRRs & JAK-STAT") does NOT block a deeper dive into a specific subtopic (e.g. "cGAS-STING"), but check that the subtopic isn't already a subsection

**Priority topics for swine immunology** (as of Jul 2026):
- T cell subsets: Th17/Treg, NK cells, CD4/CD8 T cell biology, T cell exhaustion
- B cell / humoral immunity (IgA, antibody responses in swine)
- Cytokine networks (IL-1 family, IL-6 family, TNF superfamily)
- Dendritic cell subsets, antigen presentation
- Mucosal immunity, IgA transport, M cells
- Immunometabolism (glycolysis ↔ OXPHOS in immune cells)
- ER stress / UPR / mitochondrial dynamics in immune cells
- Necroptosis, PANoptosis
- Hypoxia/HIF-1α signaling in swine
- Selenium / selenoproteins in immune function
- Trace mineral transporters (ZnT/ZIP family, copper transporters)
- Mycotoxins other than DON (aflatoxin, zearalenone, fumonisin, ochratoxin)
- Specific pathogens: Lawsonia intracellularis, Mycoplasma hyopneumoniae, Streptococcus suis, Haemophilus parasuis, Actinobacillus pleuropneumoniae
- Heat stress / HSP response in swine

---

## Phase 2: Wikipedia background from 3+ angles

Search from multiple keyword angles to catch all relevant pages. The Action API returns clean JSON with `explaintext=1` — no HTML parsing needed.

### Example search queries (Th17/Treg session)

```bash
# Angle 1: Th17 cells
curl -sL --max-time 15 \
  "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=Th17+cell&format=json&srlimit=5" \
  -H "User-Agent: Mozilla/5.0" \
  | python -c "import sys,json,re; d=json.load(sys.stdin); \
  [print(f'[{r[\"pageid\"]}] {r[\"title\"]}: {re.sub(r\"<[^>]+>\",\"\",r.get(\"snippet\",\"\"))[:200]}') \
  for r in d['query']['search']]"

# Angle 2: Regulatory T cell / FOXP3
curl -sL --max-time 15 \
  "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=Regulatory+T+cell+FOXP3&format=json&srlimit=5" \
  -H "User-Agent: Mozilla/5.0" \
  | python -c ...

# Angle 3: Species-specific (interleukin 17 pig)
curl -sL --max-time 15 \
  "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=interleukin+17+pig+immune&format=json&srlimit=5" \
  -H "User-Agent: Mozilla/5.0" \
  | python -c ...
```

### Fetch extracts — pageid-based (avoids Greek/Unicode encoding issues)

```bash
# Save to JSON file (avoids pipe truncation for large extracts)
curl -sL --max-time 30 \
  "https://en.wikipedia.org/w/api.php?action=query&pageids=PAGEID&prop=extracts&explaintext=1&format=json" \
  -H "User-Agent: Mozilla/5.0" \
  -o "C:/Users/NTQUANG_DELL/hermes-temp/topic.json"

# Parse extract from saved JSON
python -c "
import json
with open('C:/Users/NTQUANG_DELL/hermes-temp/topic.json') as f:
    d = json.load(f)
pg = list(d['query']['pages'].values())[0]
ext = pg.get('extract', '')
print(f'--- {pg[\"title\"]} ({len(ext)} chars) ---')
print(ext[:5000])
"
```

**Key pages fetched for Th17/Treg session:**
- [pageid 13506996] T helper 17 cell (11519 chars)
- [pageid 1171686] Regulatory T cell (35331 chars)
- [pageid 1920949] FOXP3 (10770 chars)

---

## Phase 3: PubMed — search from 4 angles minimum

Cast a wide net. Each angle targets a different facet. Merge results and deduplicate.

### Example query angles for immunology research

```bash
# Angle 1: Core topic + species
curl -sL --max-time 15 \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=Th17+Treg+swine+pig&retmax=10&retmode=json" \
  -H "User-Agent: Mozilla/5.0"

# Angle 2: Related mechanism + species + context
curl -sL --max-time 15 \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=interleukin+17+pig+intestinal+immunity&retmax=10&retmode=json" \
  -H "User-Agent: Mozilla/5.0"

# Angle 3: Regulatory mechanism + species
curl -sL --max-time 15 \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=regulatory+T+cell+FOXP3+swine+weaning&retmax=10&retmode=json" \
  -H "User-Agent: Mozilla/5.0"

# Angle 4: Narrower mechanism + species + disease context
curl -sL --max-time 15 \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=Th17+Treg+balance+gut+piglet&retmax=10&retmode=json" \
  -H "User-Agent: Mozilla/5.0"
```

### Get summaries in bulk

```bash
pmid_str='39985783,38367809,37961849,34881888,40742129'
curl -sL --max-time 15 \
  "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=${pmid_str}&retmode=json" \
  -H "User-Agent: Mozilla/5.0" \
  | python -c "
import sys,json
d=json.load(sys.stdin)
for uid in d['result']['uids']:
    info = d['result'][uid]
    authors = [a.get('name','') for a in info.get('authors',[])[:2]]
    print(f'PMID {uid}: {info.get(\"title\",\"?\")}')
    print(f'  {info.get(\"source\",\"\")} ({info.get(\"pubdate\",\"\")})')
    print(f'  Authors: {\", \".join(authors)}')
    print()
"
```

### Fetch abstracts with scoped per-PMID extraction (⚠️ critical: avoid cross-article contamination)

Use the per-PMID `PubmedArticle` scoping pattern:

```python
# The naive <AbstractText> regex finds the FIRST abstract in the whole XML
# for every PMID. Always scope to each article's <PubmedArticle> block:
for pmid in pmids:
    article_pattern = rf'<PubmedArticle>.*?<PMID Version=\"1\">{pmid}</PMID>(.*?)</PubmedArticle>'
    article_match = re.search(article_pattern, xml_data, re.DOTALL)
    if article_match:
        article_xml = article_match.group(1)
        ab_match = re.search(r'<AbstractText[^>]*>(.*?)</AbstractText>', article_xml, re.DOTALL)
        if ab_match:
            abstracts[pmid] = re.sub(r'<[^>]+>', '', ab_match.group()).strip()
```

### PMIDs found for Th17/Treg in swine (reference)

| PMID | Journal | Key finding |
|------|---------|-------------|
| 39985783 | J Anim Sci (2025) | Xylo-oligosaccharides enhance Th17/Treg in LPS-challenged piglets |
| 38367809 | J Nutr (2024) | Glutamine modulates microbiota and Th17/Treg signaling in piglets |
| 37961849 | J Sci Food Agric (2024) | N-carbamylglutamate modulates Th17/Treg balance in piglets |
| 34881888 | J Agric Food Chem (2021) | Chito-oligosaccharides improve Th17/Treg balance in ETEC piglets |
| 40742129 | mBio (2025) | PCV2 infection induces Treg via TGF-β/Smad3 pathway |
| 36377452 | Zhonghua Wei Zhong (2022) | Anisodamine improves Th17/Treg imbalance in resuscitated pigs |
| 36552257 | Biology (Basel) (2022) | Porcine IL-17/22 co-expressed enhance immunity |
| 36865532 | Front Immunol (2023) | Dietary fiber alters immunity in growing pigs |
| 26490738 | Vet Res (2015) | F4+ ETEC infection elicits IL-17-dominated immune response |

---

## Phase 4: Card structure template (immunology topics)

Use this 7-section structure. Each section serves a purpose:

| # | Section | Content | Why |
|---|---------|---------|-----|
| 1 | **Tổng quan** | Comparison table (Th17 vs Treg), key callout quote | Immediate orientation |
| 2 | **Cơ chế biệt hóa** | Transcription factors, cytokines, signaling diagrams | Core mechanism |
| 3 | **Chức năng effector** | Cytokine table, mechanism descriptions | What each cell type does |
| 4 | **Cân bằng trong bệnh lý** | Disease-specific findings table, intervention table | Relevance to pratice |
| 5 | **Tín hiệu phân tử** | ASCII pathway diagram, checkpoints | Molecular detail |
| 6 | **So sánh species** | Pig vs human comparison table | Species-specific context |
| 7 | **Kết luận** | Bullet summary + applications | Takeaways |

### Vietnamese writing conventions for immunology cards:
- **Terms**: Keep English technical terms (pathway, transcription factor) in English with Vietnamese context
- **Tables**: Every table has a header row, alternating content
- **Callouts**: `> 🔑 key concept` or `> ⚠️ pitfall` for emphasis
- **Diagrams**: ASCII/`code-block` for pathway diagrams
- **Citations**: Every factual claim → PMID in references table
- **References section**: PMID + Journal (Year) + contribution description

### Tags: 15-22 specific tags

Cover these categories in your tags:
1. The pathway/protein (Th17, Treg, FOXP3, RORγt)
2. Key cytokines (IL-17, IL-10, TGF-β)
3. Transcription factors (Stat3, Stat5)
4. Species (heo, lợn)
5. Related mechanisms (plasticity, Treg17)
6. Disease/stress (cai sữa, ETEC, PCV2)
7. Interventions (XOS, glutamine, COS)
8. General (dinh dưỡng miễn dịch, chăn nuôi heo)

---

## Phase 5: POST to KF with Pattern D (Python script)

For cards with Vietnamese Unicode, tables, and markdown, use a standalone Python script (Pattern D) — avoids all MSYS/git-bash heredoc escaping issues.

```python
import urllib.request, json

card_content = """## 1️⃣ Section 1

Content with Vietnamese and PMID citations...

| Column | Data |
|--------|------|
| Value  | PMID 39985783 |

...

## 📚 References
| PMID | Journal | Contribution |
|------|---------|-------------|
"""

payload = {
    "title": "🧬 Card Title — Vietnamese subtitle",
    "content": card_content,
    "summary": "Short Vietnamese summary...",
    "tags": ["tag1", "tag2", ..., "tag22"],
    "topic_slug": "chan-nuoi-heo",
    "source_url": "https://en.wikipedia.org/wiki/Topic"
}

url = "http://127.0.0.1:3003/api/knowledge"
headers = {
    "Authorization": "Bearer hermes-knowledge-secret",
    "Content-Type": "application/json"
}

data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
req = urllib.request.Request(url, data=data, headers=headers, method='POST')

try:
    resp = urllib.request.urlopen(req, timeout=15)
    result = json.loads(resp.read().decode())
    print(f"SUCCESS! Card ID: {result.get('id', 'N/A')}")
    print(f"Reading time: {result.get('reading_time_sec', 'N/A')} sec")
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode()[:500]}")
except Exception as e:
    print(f"Error: {e}")
```

**Target reading time:** 300-900 sec (5-15 min). Achievable with 7 sections, 5-8 tables, and ~1000-2000 words of Vietnamese + English technical content.
