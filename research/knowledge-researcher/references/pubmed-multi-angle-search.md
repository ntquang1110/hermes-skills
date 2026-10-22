# PubMed Multi-Angle Search Pattern

Use this pattern when researching a topic for a KF card. Instead of one broad query, search from **multiple angles** to catch articles a single query misses.

## Two-Phase Strategy

### Phase 1: Broad coverage (8 queries)
Cover the topic from broad perspectives:
- Generic query: `"topic porcine pig"`
- Virus/disease interactions: `"topic PRRSV infection immune modulation"`
- Pathogen-specific: `"pathogen topic porcine modulation immune evasion"`
- Mechanism queries: `"topic migration chemokine CCR7 porcine"`
- Subtopic queries: `"topic tolerance cross-presentation pig"`
- Model system queries: `"MoDC monocyte-derived dendritic cell pig LPS maturation"`
- Cell-type specific: `"plasmacytoid dendritic cell interferon pig antiviral"`
- Applied: `"topic vaccine adjuvant porcine"`

### Phase 2: Specific mechanism / subset queries (8 queries)
Narrow the focus:
- Markers: `"topic subtypes porcine CD1 CD172 SLA-DR"`
- Tissue-specific: `"topic pig Langerhans cell skin respiratory"`
- Cytokine: `"topic cytokine IL-12 IL-10 porcine Th1 Th2"`
- Receptor: `"topic toll-like receptor activation maturation pig"`
- Niche: `"follicular topic pig germinal center B cell"`
- Virus-specific: `"porcine topic CSFV classical swine fever"`
- Virus-specific: `"PCV2 topic immune modulation"`
- Virus-specific: `"swine influenza topic immune response"`

## Merging Results

```python
# After both phases:
all_pmids = set()
for query in phase1_queries + phase2_queries:
    pmids = pubmed_search(query, 5)
    all_pmids.update(pmids)
    time.sleep(1.5)

# Get summaries → select core → fetch abstracts
pmid_str = ','.join(all_pmids)
url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid_str}&retmode=json'
```

## Pacing Rules

- `time.sleep(1.5)` BETWEEN each query (not between individual API calls within a batch)
- For `efetch` (abstracts): `time.sleep(0.3)` between individual PMID fetches
- Total pacing: 16 queries × 1.5s = ~24s for Phase 1+2; ~5s for abstract batch

## When to Use

- Complex topics spanning subtopics (mechanism + barrier function + antimicrobial effects + species)
- When the first 2-3 queries return mostly noise → the queries are too broad; switch to mechanism-specific queries immediately
- For KF cards targeting 15-25 PMIDs across 5+ subtopics

## Example: Dendritic Cells in Swine (this pattern)

This pattern yielded **53 unique articles** from 16 queries (8 broad + 8 specific), narrowed to **17 core abstracts** for a 25-PMID card with 8 sections covering:
- DC subsets (cDC, pDC, MoDC, FDC)
- TLR ligand activation (TLR3, TLR7, TLR9, synergy)
- Virus interactions (PRRSV, PCV2, ASFV, PEDV, CSFV, SIV)
- Vaccine development (adjuvants, mRNA, nanoparticles)
- Age-dependent responses (pDC IFN-I in piglets vs adults)
