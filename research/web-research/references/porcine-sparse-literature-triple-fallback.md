# Triple-fallback pattern: Extremely sparse porcine literature

When researching a porcine-specific pathway, cytokine, or protein that has **very little direct literature in swine** — even after applying the standard "No-review" workaround (switching from mechanism-specific to disease-specific queries) — use this extended triple-fallback pattern.

## When to use this pattern

Apply when ALL of the following return 0-2 relevant hits:

1. **Mechanism-specific queries** — e.g. `interleukin 33 ST2 porcine swine` → 0-2 hits
2. **Disease-specific queries** — e.g. `PRRSV IL-33 pig`, `PEDV IL-33 intestinal porcine` → 0 hits each
3. **Multiple disease angles** — after trying 3+ disease contexts with no direct hits

**Signal:** The pathway/protein has extensive literature in human and mouse but virtually nothing in pig. This happens for niche cytokine members (IL-33, IL-37, IL-38), recently discovered pathways, and pathways that are secondary readouts in disease studies rather than primary research focus.

## Triple-fallback workflow

### Level 1: Broad "OR" query (the salvage probe)

```python
# Broad search — cast the widest net
pmids = pubmed_search('IL-33 porcine OR swine OR pig', 8)
```

This will return ~5-7 papers but **most will be noise** — papers that happen to study something else in pigs and mention your term only incidentally (e.g. a liver enzyme study that measured pig cytokines as a side variable). Expect 1-2 genuinely relevant papers among the noise.

**Filtering technique:** Scan titles manually. A paper is relevant if your target term is in the title, abstract keywords, or represents a major study variable. Incidental mentions in a methods paragraph ("we also measured IL-33 as a control") do not count.

### Level 2: Wikipedia for fundamental pathway biology

Wikipedia typically has robust coverage of cytokines, signaling pathways, and protein families. Use the **Action API** (Level 2a) for comprehensive extracts:

```python
# Search for relevant pages
hits = wiki_search('Interleukin 33 ST2 receptor alarmin', lang='en', limit=5)

# Fetch full extracts (one pageid at a time to avoid exlimit cap)
extracts = wiki_extract_multi([pageid_list], lang='en')

# For pathway-adjacent info, also search Vietnamese Wikipedia
vi_hits = wiki_search('Interleukin 33 ST2', lang='vi', limit=3)
```

The Wikipedia extract provides:
- Gene organization and protein structure
- Canonical signaling mechanism (ligand → receptor → adaptors → transcription factors → target genes)
- Biological functions across tissues
- Clinical significance and disease associations
- Regulatory mechanisms

**This fills the gap** that would otherwise be filled by a dedicated review paper (which doesn't exist for this pig pathway).

### Level 3: General PubMed reviews (human/mouse)

Since swine-specific literature is absent, fall back to human/mouse review papers for mechanism details:

```python
queries = [
    'IL-33 review alarmin cytokine signaling',           # general review
    'IL-33 ST2 signaling NF-kB MAP kinase',              # mechanism
    'IL-33 intestinal mucosal barrier inflammation',     # tissue-specific
    'IL-33 type 2 immunity ILC2 Th2',                    # functional
    'IL-33 alarmin tissue damage DAMP',                  # conceptual
]
```

Fetch 4-5 abstracts per query (pace with `time.sleep(2)`), deduplicate, and select the most comprehensive reviews and the most mechanism-specific research papers.

## Assembling the card from mixed sources

Since no single paper covers the whole topic in swine, the card must be **synthesised** from:

| Content | Source | Appropriateness |
|---------|--------|----------------|
| Gene/protein structure | Wikipedia | ✅ Excellent — well-conserved across mammals |
| Signaling mechanism | Wikipedia + human reviews | ✅ Excellent — pathways are conserved |
| Biological functions | Human/mouse reviews | ✅ Good — core biology is conserved |
| Disease associations | Human clinical literature | ⚠️ Moderate — species-specific pathology differs |
| Swine-specific data | 1-2 PMIDs from Level 1 | ✅ Essential anchor papers |
| Feed additive modulation | Inferred from mechanism + human data | ⚠️ Speculative — flag with caveat |

### Must include caveats

Every extrapolation from human/mouse → swine must be explicitly flagged:

> **⚠️ Cảnh báo ngoại suy:** Cơ chế phân tử IL-33/ST2 được bảo tồn cao giữa các loài có vú (người, chuột, heo) dựa trên phân tích tương đồng gen và protein. Tuy nhiên, hầu hết dữ liệu chức năng chi tiết đến từ mô hình người và chuột. Các nghiên cứu trực tiếp trên heo còn hạn chế [PMID 38980021], đặc biệt trong bối cảnh bệnh đường ruột và virus heo. Các kết luận về ứng dụng trên heo cần được xác nhận bằng thực nghiệm.

## Worked example: IL-33/ST2 axis in swine

This pattern was validated on researching IL-33/ST2 in swine (July 2026).

### Query results

| Query type | Example | Hits | Relevant |
|-----------|---------|------|----------|
| Mechanism-specific | `interleukin 33 ST2 porcine swine` | 2 | 1 |
| Disease-specific #1 | `PRRSV IL-33 pig` | 0 | 0 |
| Disease-specific #2 | `PEDV IL-33 intestinal porcine` | 0 | 0 |
| Disease-specific #3 | `Streptococcus suis IL-33 porcine` | 1 | 1 |
| Broad OR | `IL-33 porcine OR swine OR pig` | 6 | 1 |
| Human/mouse review | `IL-33 review alarmin cytokine signaling` | 5 | 5 |
| Mechanism review | `IL-33 ST2 signaling NF-kB MAP kinase` | 5 | 3 |

**Total swine-specific:** 2 directly relevant papers (PMID 38980021 + context)
**Total human/mouse:** 27 papers used for mechanism + function
**Wikipedia:** 2 pages (Interleukin 33 + IL1RL1/ST2)

### Card created
- Title: 🧬 IL-33/ST2 — Alarmin trung tâm của miễn dịch type 2, tái tạo mô và viêm ở heo
- Reading time: 840 sec, 39 tags, 12 PMIDs cited
- Structure: 10 sections following the pathway-card-template

### Key lessons
1. Wikipedia Action API is essential when literature is sparse — it provides the backbone that would normally come from a review paper
2. Even 1-2 swine-specific papers validates the entire card; without them, the card would be purely extrapolative
3. Explicit flagging of cross-species extrapolation protects against overclaiming
4. The IL-33/ST2 case confirmed that porcine immunology literature on niche cytokines is organized around disease models, not pathway-focused papers — exactly matching the skill's existing "No-review" guidance
