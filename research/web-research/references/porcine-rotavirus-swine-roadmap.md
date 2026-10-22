# Porcine Rotavirus A (PoRVA) — Swine Research Roadmap

Created Aug 2026 from a full research run (card `7483af4f-6fde-4c92-83b9-f5237fcd928c`, POST 201, 900s read time). Gap identified: KF had PEDV/TGEV/PDCoV cards but no rotavirus — PoRVA belongs to *Reoviridae* (dsRNA, non-enveloped), a completely different family from coronaviruses, so it deserves its own card.

## Tested PubMed queries (Aug 2026)

### ✅ Working (use these)
| Query | Result |
|---|---|
| `porcine rotavirus piglet diarrhea pathogenesis` | 8 hits — reassortants, VP6 mAbs, CRISPR detection |
| `rotavirus NSP4 enterotoxin calcium chloride secretion` | 8 hits — NSP4 mechanism core |
| `rotavirus NSP1 interferon IRF degradation innate immunity` | 3 hits — evasion |
| `porcine rotavirus vaccine passive immunity colostrum piglet` | 2 hits — vaccine |
| `porcine rotavirus prevalence pig herd` | 8 hits — epidemiology |
| `rotavirus NSP4 viroporin calcium` | 8 hits — viroporin waves, necroptosis |

### ❌ Returned 0 silently (do NOT retry — query construction problem, not missing literature)
- `porcine rotavirus genotype G P pig` (5 concepts)
- `group A rotavirus piglet prevalence epidemiology Asia` (6 concepts)
- `rotavirus viroporin calcium enterocyte review` (5 concepts)

**Lesson:** PubMed `esearch` returns empty `idlist` with no error for 4-5+ space-separated concepts. Cut to 2-4 highest-signal terms. Drop stopwords like "review", "prevalence", "epidemiology", "Asia". This is the single most common silent failure in PubMed cron research.

## Wikipedia titles

- `wiki_extract('Rotavirus A')` → **NO EXTRACT** (silent). Genus page `Rotavirus` → full article. REST `/page/summary/Rotavirus A` → works. For species-level titles: REST summary first, then genus page with section-keyword windows (`== Proteins ==`, `== Replication ==`, `== Disease mechanisms ==`, `== Immune responses ==`, `== Prevention ==`).

## Key mechanisms (with PMIDs)

| Mechanism | Protein | PMID |
|---|---|---|
| Viral enterotoxin #1 ever described; NSP4(114-135) alone causes diarrhea in newborn mice | NSP4 | 11300798, 14550638 |
| Viroporin domain is a genuine Ca²⁺-conducting ion channel | NSP4 | 28256607 |
| Glucose ENHANCES NSP4-stimulated Cl⁻ secretion (ORS caution) | NSP4 | 28488023 |
| Intercellular Ca²⁺ waves via IP₃R prime uninfected cells; viroporin necessary | NSP4 | 38112482, 39823322 |
| Usurps RIPK1-RIPK3 → MLKL necroptosis | NSP4 | 38719029 |
| Degrades IRF3/5/7 via IAD domain targeting | NSP1 | 23824805 |
| Mimics pLxIS motif to hijack IRF machinery | NSP1 | 27302953 |
| Host counter: miR-525-3p targets NSP1 3'UTR, restores IFN | host | 28890396 |
| Rotavirus Cl⁻ secretion differs mechanistically from bacterial enterotoxins | NSP4 | 17376232, 17961806 |

## Key epidemiology numbers (China surveillance 2022-2024, n=5425, PMID 41616680)

- Positivity 36-68%/month, peak winter-spring
- VP7: G5 43.69%, G4 23.39%, G9 15.53%
- VP4: P[13] 68.93%, P[6] 10.68%, P[23] 9.71%
- 3-day-old colostrum-deprived piglets: mortality 40% (G9P[23]) and 20% (G5P[13])
- Human-porcine reassortants G9P[7]/G1P[7] replicate in lungs (PMID 42458604) — One Health angle

## Diagnostics (2026 state of the art)

- CRISPR-Cas12a + LAMP multiplex: PEDV/TGEV/PDCoV/PoRV-G9, visual detection from 1 copy/µL (PMID 42001168)
- cELISA vs VP4 (mAb16): AUC 0.995, sens 96%, spec 98.28%, r=0.846 with NT (PMID 41946388)
- bELISA vs VP6: cutoff 23.23% inhibition (PMID 42134695); VP6 conserved epitopes 43NDFQTGG49, 208EHVVPLR214 (PMID 42140294)

## Control reality

Non-enveloped → survives 9-19 days in environment; standard bacterial sanitation does NOT control it. Pillars: colostrum (passive immunity), correct-spectrum disinfectants (chlorine/aldehyde), bivalent inactivated vaccine (2026, PMID 41616680), live OSU/6 sow vaccine (PMID 1668214, historic).

## Card delivery notes (for reuse)

- topic_slug: `chan-nuoi-heo`; title pattern `🐷 Porcine Rotavirus A (PoRVA) — ...`
- 32 PMIDs in references table; every mechanism claim anchored inline
- Mermaid flowchart for replication cycle (VP4 → endocytosis → Ca²⁺ drop → DLP → viroplasm → ER → lysis)
- Vietnamese terms: nhung mao (villi), tiêu chảy nước (watery diarrhea), sữa đầu (colostrum), "bình trộn" (mixing vessel)
