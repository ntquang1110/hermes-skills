# Research Quality Gates (Mandatory)

These gates apply to EVERY research task for this user — including cron-mode research. Violations are not optional.

---

## 1. Paper-first rule

Every research output MUST cite a peer-reviewed paper, textbook, or authoritative scientific source (PMID, DOI, or equivalent).

- News articles WITHOUT a cited paper → **skip the topic entirely**
- Blog posts, press releases, marketing material → NOT scientific sources
- Exception: original research papers on AI/tech topics (conference paper, arXiv with peer review, published journal article)

## 2. Per-paper deep analysis

For each cited paper, extract AND present:
- **Mechanism**: What molecular/cellular mechanism does the paper describe?
- **Methods**: Experimental approach (in vitro, in vivo, model, species, sample size)
- **Key data**: Quantitative results (effect sizes, IC50, fold-change, p-values)
- **Results**: What did they find?
- **Conclusions**: What does this mean for the field/application?

Do NOT just drop a citation and move on — demonstrate you read and understood the paper.

## 3. No news-only research

If the only available sources are news articles without supporting scientific papers:
- **Skip the topic entirely**
- Do not substitute news for science
- Do not fabricate citations to make news look scientific

## 4. Traceable citations

Every mechanism claim must map to a verifiable source:
- PMID (PubMed ID) for biomedical research
- DOI for general science
- Textbook (Author, Title, Edition, Year)
- Wikipedia (acceptable for background, not for primary claims)

Format: `[Author(s), Journal Year. PMID: XXXXXXXX]`

"A study shows" or "According to research" without a verifiable source is NOT acceptable.

## 5. AI / tech research exception

When researching new AI models or technologies:
- The original paper (conference paper, arXiv with peer review, or published journal article) is REQUIRED
- Marketing material, blog posts, press releases are NOT substitutes
- If no paper exists, note "preprint only — not peer-reviewed"

## 6. Vietnamese delivery

All delivered research must be:
- **Vietnamese (có dấu)**
- Scientific terms in both languages (EN + VN) on first mention
- Format: Markdown with tables, headings, emoji section markers
- References table at the end with all PMIDs

## 7. Cron-mode workflow

When running as a cron research job:

```
Step 1: GET /api/research-queue → pick oldest "pending" item
Step 2: If queue empty → gap analysis on existing KF cards
Step 3: Research with Wikipedia API + PubMed E-utilities
Step 4: Create KF card via POST /api/knowledge (Pattern D)
Step 5: PATCH /api/research-queue?id=<id>&action=done
```

### Self-directed cron research (queue empty) — heuristics:

1. **Ghost topics**: Scan existing KF cards for concepts referenced in ≥3 cards but not independently covered
2. **Structural symmetry**: If most members of a family/group are covered, fill the missing one
3. **Downstream connectivity**: Prioritize topics connecting to feed additives, vaccines, disease mechanisms
4. **Swine-specific literature**: Prefer topics with ≥5 swine-specific PubMed results — ensures enough pig data
5. **Multi-angle PubMed**: Use 2-3 query angles per topic (mechanism, disease, species) to catch more papers
