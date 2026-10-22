# 🧬 NK Cell Research Roadmap — Swine (Heo)

Condensed reference bank for future sessions researching Natural Killer cells in pigs.

## Key Queries (tested Jul 2026)

| # | Query | Results | Notes |
|---|-------|---------|-------|
| 1 | `NK cell porcine pig antiviral immunity` | 5 PMIDs | Best general starter — returns recent (2025-2026) papers on influenza, PRRSV interactions |
| 2 | `NK cell receptor swine pig activating inhibitory` | 5 PMIDs | Covers xenotransplantation (HLA-E/G), Ascaris coinfection effects |
| 3 | `NK cell pig PRRSV ASFV viral infection` | 1-5 PMIDs | Narrower — use as third probe; add `influenza` or `PEDV` for broader coverage |
| 4 | `pig NK cell cytotoxicity ADCC antibody dependent` | 5 PMIDs | Best for ADCC mechanism — returns ASFV E120R, PEDV-N papers |
| 5 | `NK cell pig intestine gut mucosal immunity` | 5 PMIDs | IEL NK cells, probiotics, NKG2D in jejunum |
| 6 | `porcine NK cell training trained immunity` | 0 PMIDs | No results — skip; use `beta-glucan NK pig` instead |
| 7 | `porcine NK cell phenotype CD16 CD56 CD8` | 0 PMIDs | PubMed doesn't index well on phenotype keywords — use Wikipedia instead |
| 8 | `swine NK cell receptor SLA KIR inhibitory activating` | 0-1 PMIDs | Use Wikipedia for receptor biology instead |
| 9 | `NK cell pig vaccine influenza coronavirus` | 1-5 PMIDs | Narrow — add more pathogen names for better recall |
| 10 | `porcine NK cell development bone marrow` | 3-5 PMIDs | Mostly xenotransplantation (human CD34+ engraftment) |

**Best 3-query starter set:**
```
queries = [
    'NK cell porcine pig antiviral immunity',
    'pig NK cell cytotoxicity ADCC antibody dependent',
    'NK cell pig intestine gut mucosal immunity',
]
```

## PMID Table with Specific Findings

| PMID | Year | Journal | Key Finding | Relevance |
|------|------|---------|-------------|-----------|
| **41941497** | 2026 | PLoS Pathog | CD1D-deficient pigs (lack NKT) have altered cellular responses to influenza H3N2 — NKT-NK crosstalk shapes anti-influenza immunity | NK/NKT interaction in respiratory infection |
| **41274080** | 2026 | Virology | PRRSV suppresses NK cells via IL-10 upregulation; downregulates MHC-I | PRRSV immune evasion |
| **41156603** | 2025 | Pathogens | NK cells progressively decline in acute ASF; correlates with viral DNAemia and proinflammatory cytokines | ASF pathogenesis — NK as disease marker |
| **40233683** | 2025 | Vet Microbiol | PEDV-N protein expressed on infected cell surface → anti-N antibodies enable NK-mediated ADCC via CD16 | ADCC mechanism for non-neutralizing antibodies |
| **38918457** | 2024 | Sci Rep | Ascaris suum coinfection completely abolishes IL-12/IL-18-driven IFN-γ production in CD16⁺CD8α⁺perforin⁺ NK cells; blocks perforin and CD107a upregulation | Parasite-induced NK suppression |
| **37529053** | 2023 | Front Immunol | HLA-E + HLA-G on porcine endothelial cells attenuates human NK degranulation — xenotransplantation strategy | Cross-species NK recognition |
| **36072599** | 2022 | Front Immunol | Review: NK activating (NKG2D, DNAM1) and inhibitory (KIR2DL1-4, NKG2A, LIR-1) signaling in xenotransplantation | Receptor signaling review |
| **35746813** | 2022 | Viruses | Anti-pig CD69 monoclonal antibody developed — enables early NK/T cell activation detection by flow cytometry | Tool paper |
| **41012137** | 2025 | Vaccines | ADCC elicited by anti-ASFV E120R antibodies — potential vaccine antigen | ADCC-based vaccine design |
| **28494934** | 2017 | Vet Immunol Immunopathol | NKG2D expression on porcine jejunal IEL varies post-weaning; time-dependent development | IEL NK cells in gut |
| **37041617** | 2023 | Anim Microbiome | Agaricus subrufescens fermented rye increases intestinal NK cells in piglets | Feed additive → NK modulation |
| **25063224** | 2014 | Vet Immunol Immunopathol | Probiotic Bacillus cereus modulates NKG2D⁺ immune cells in pig jejunum | Probiotic-NK interaction |
| **16850939** | 2006 | Can J Vet Res | PRRSV stimulates early IFN-γ response in serum — NK cells as early IFN-γ source | Classic — NK IFN-γ in PRRSV |

## NK Cell Phenotype — Species Comparison

| Feature | Human | Mouse (C57BL/6) | Pig |
|---------|-------|-----------------|-----|
| Canonical marker | CD56⁺CD3⁻ | NK1.1⁺CD3⁻ (NK1.1 = NKR-P1C) | CD16⁺CD8α⁺perforin⁺CD3⁻ |
| CD56 expression | Yes (bright/dim subsets) | No (use NK1.1/NKp46) | No — pigs lack CD56 ortholog |
| CD8α expression | Subset (CD56dimCD16⁺) | Subset | Majority of pig NK are CD8α⁺ |
| CD16 (FcγRIII) | CD56dim subset | Yes (CD16⁺ subset) | Expressed on most NK — ADCC-capable |
| NKp46 (NCR1) | Yes | Yes | Yes — reliable pan-NK marker across species |
| KIR family | Primary inhibitory receptors | Absent | Absent (functional) — pigs lack diverse KIR |
| Ly49 family | One pseudogene (killed by retroelement) | Primary inhibitory receptors | Functional Ly49 — more mouse-like than human |
| NKG2A/CD94 | Yes | Yes | Yes — conserved |
| NKG2D | Yes | Yes | Yes — expressed on IEL |
| Perforin | Intracellular, in lytic granules | Intracellular | Intracellular — used as marker in flow |
| Blood frequency | 5–20% of lymphocytes | 2–10% | 5–15% |

## Pathway Summary

```
NK cell activation = SUM(Activating signals) - SUM(Inhibitory signals)

Inhibitory signals (healthy cells):
  KIR/Ly49 + MHC-I → ITIM → SHP-1/SHP-2 → dephosphorylate Vav1/LAT/PLCγ → NO KILL

Activating signals (stressed/infected cells):
  Missing MHC-I → loss of inhibitory signal → UNLEASH
  NKG2D + stress ligands (MIC-A/B, ULBP) → DAP10 → PI3K → Vav1
  NCR (NKp46/NKp30/NKp44) + viral ligands → ITAM → Syk/ZAP70
  CD16 + IgG-opsonized target → ITAM → Syk → degranulation (ADCC)

Effector mechanisms:
  1. Granule exocytosis: Perforin → Granzyme B → Caspase-3 → Apoptosis
  2. Death receptors: FasL → Fas, TRAIL → DR4/DR5 → Caspase-8
  3. ADCC: CD16 + IgG-coated target cell → degranulation
  4. Cytokine production: IFN-γ, TNF-α, GM-CSF
```

## Vietnamese Terminology Quick Reference

| English | Tiếng Việt |
|---------|-----------|
| Natural Killer cell | Tế bào NK / Tế bào diệt tự nhiên |
| Innate lymphoid cell (ILC) | Tế bào lympho bẩm sinh |
| Missing self | Cơ chế "thiếu dấu hiệu bản thân" |
| ADCC | Gây độc tế bào phụ thuộc kháng thể |
| Inhibitory receptor | Thụ thể ức chế |
| Activating receptor | Thụ thể hoạt hóa |
| Degranulation | Sự giải phóng hạt |
| Immunological synapse | Khớp thần kinh miễn dịch |
| Perforin | Protein tạo lỗ (perforin) |
| Granzyme | Protease gây chết tế bào (granzyme) |
| Intraepithelial lymphocyte (IEL) | Tế bào lympho trong biểu mô |
| Swine Leukocyte Antigen (SLA) | Kháng nguyên bạch cầu heo |
| Xenotransplantation | Ghép xuyên loài |

## Topic Discovery Strategy

Start with **Wikipedia** (Level 2a) for NK cell background, then **PubMed** (Level 2c) with the 3-query starter set above.

**Wikipedia pages to fetch:**
- `Natural killer cell` (pageid=211955) — 20KB+ extract, covers history, types, receptors, signaling, clinical
- `Killer-cell immunoglobulin-like receptor` (pageid=8998654) — KIR family details
- `Antibody-dependent cellular cytotoxicity` (pageid=4355092) — ADCC mechanism
- `NKG2D` (pageid=35036168) — Activating receptor details
- `CD16` (pageid=10535441) — FcγRIII details

## Related Cards in KF (avoid duplication)

Cards already in KF that neighbor NK cell biology:
- `🧬 Tế bào tua (Dendritic Cells) ở heo` — DC-NK crosstalk
- `🧬 Apoptosis` — granzyme/caspase pathway overlap
- `🧬 JAK-STAT Signaling` — IFN-γ/IL-12/IL-15 signaling downstream
- `🧬 NF-κB` — inflammatory signaling in NK activation
- `🧬 Hệ thống miễn dịch niêm mạc ruột heo` — IEL NK cells in gut
- `🔬 Cơ chế phòng thủ nội bào — Interferon, PRRs & JAK-STAT` — overlaps with NK cytokine production

**Dedup keywords for NK cell card:**
```python
keywords = ['nk cell', 'natural killer', 'cd16', 'adcc', 'killer cell', 'cytotoxic lymphocyte', 'nk cells']
```
