# TGF-β/SMAD Signaling Pathway — Condensed Research Bank (Swine)

> Generated: 2026-07-20 | Sources: Wikipedia Action API + PubMed E-utilities | Total PMIDs collected: 27

## Quick reference: Key PubMed IDs

| PMID | Journal (Year) | Core finding | Mechanism |
|------|---------------|-------------|-----------|
| 28142299 | Innate Immun (2017) | TGF-β1 protects IPEC-J2 barrier after TNF-α | Smads + MAPK, ↑ZO-1/occludin |
| 25170924 | PLoS One (2014) | TGF-β1/Smads changes in weaned pig intestine | Post-weaning adaptation, days 3–14 |
| 34941739 | Toxins (2021) | Zearalenone disrupts cecal barrier via TGF-β1/Smads | ↓TβRII, ↓p-SMAD2/3, ↓goblet cells |
| 26810899 | Br J Nutr (2016) | Whey protein enhances barrier via TGF-β1 | ↑TGF-β1, ↑TER |
| 27189428 | Innate Immun (2016) | Anemonin restores barrier via TGF-β1/EGFR | ↑p-SMAD3, ↑villus height |
| 28958208 | Innate Immun (2017) | Cu/Zn-montmorillonite upregulates TGF-β1 | Anti-inflammatory, ↑TER |
| 37348134 | J Anim Sci (2023) | AKG modulates Th17/Treg via TGF-β | Immune balance in weaned pigs |
| 28638110 | Sci Rep (2017) | Porcine Tregs express IL-10 + TGF-β1 | Xenotransplantation model |
| 41459927 | Reprod Domest Anim (2025) | TGF-β1↓VCAM1 via Smad2 in porcine granulosa | Smad2-specific, not Smad3 |
| 36375269 | Res Vet Sci (2023) | Eleutheroside E protects IPEC-J2 barrier | ↑TGF-β1 signaling |
| 35014099 | J Anim Physiol Anim Nutr (2022) | Eleutheroside E vs. soybean agglutinin | ↑tight junction proteins |
| 36648449 | Biol Reprod (2023) | GDF9 (TGF-β superfamily) essential for folliculogenesis | Pig model |
| 37561570 | Reproduction (2023) | BMP15 in porcine follicular development | TGF-β superfamily |

## Wikipedia page corpus

| PageID | Title | Size (chars) |
|--------|-------|-------------|
| 5725322 | TGF beta signaling pathway | 10,197 |
| 2901165 | Transforming growth factor beta | 26,918 |
| 5695222 | SMAD (protein) | 15,427 |
| 10112524 | Transforming growth factor beta superfamily | 2,893 |
| 5745135 | TGF beta 1 | 3,663 |

## Core pathway architecture

```
Ligands (TGF-β1/2/3, Activins, BMPs, GDFs, Nodal)
  ↓
TβRII dimer (serine/threonine kinase)
  ↓ phosphorylates
TβRI/ALK5 dimer (GS domain, 30 Ser-Gly repeats)
  ↓ phosphorylates SSXS motif
R-SMADs (SMAD2/3 for TGF-β; SMAD1/5/9 for BMP)
  ↓ bind
Co-SMAD SMAD4
  ↓ accumulate in nucleus
R-SMAD/SMAD4 trimer (2:1 ratio) → DNA binding at CAGAC motif
  ↓ recruit
Co-activators (p300/CBP, P/CAF) OR Co-repressors (c-Ski, SnoN, TGIF)
```

## SMAD family table

| SMAD | Type | Function | Regulated by |
|------|------|----------|-------------|
| SMAD1 | R-SMAD (BMP) | BMP signaling, osteogenesis | BMPRI kinases |
| SMAD2 | R-SMAD (TGF-β) | Gut barrier, VCAM1 in ovary | TβRI → C-terminal SSXS |
| SMAD3 | R-SMAD (TGF-β) | Stronger DNA binding than SMAD2 | TβRI → C-terminal SSXS |
| SMAD4 | Co-SMAD | Universal partner | Forms heterotrimer with R-SMADs |
| SMAD5 | R-SMAD (BMP) | BMP signaling | BMPRI kinases |
| SMAD6 | I-SMAD | BMP-specific inhibitor | Induced by BMP |
| SMAD7 | I-SMAD | Universal TGF-β inhibitor | Induced by TGF-β (negative feedback) |
| SMAD9 | R-SMAD (BMP) | BMP signaling (also called SMAD8) | BMPRI kinases |

## SMAD7 negative feedback loop

1. TGF-β signaling → transcription of SMAD7
2. SMAD7 binds TβRI → blocks R-SMAD phosphorylation
3. SMAD7 recruits Smurf1/2 ubiquitin ligases → TβRI degraded via proteasome
4. In IPEC-J2 cells, reducing SMAD7 enhances TGF-β protection [PMID 28142299]

## Non-canonical TGF-β pathways

- MAPK/ERK: TβRI → Shc → Grb2 → Ras → Raf → MEK → ERK
- p38 MAPK: TAK1 → MKK3/6 → p38 (confirmed in IPEC-J2 [PMID 28142299])
- JNK: TAK1 → MKK4/7 → JNK
- PI3K/AKT/mTOR: TβRII → p85 → PI3K → AKT
- Rho-like GTPases: RhoA, Rac1, Cdc42

## Cross-talk with other pathways

- NF-κB: TGF-β/SMAD3 inhibits NF-κB in macrophages (anti-inflammatory)
- JAK-STAT: TGF-β inhibits IFN-γ/STAT1 (Th1 suppression)
- Wnt/β-catenin: SMAD3 + β-catenin regulate intestinal stem cells
- MAPK cross-talk: Phosphorylates SMAD linker region, modulating SMAD activity

## Post-weaning intestinal adaptation timeline

| Day | TGF-β1 | Receptors | SMADs | Gut state |
|-----|--------|-----------|-------|-----------|
| 3 | ↑↑ | TβRI/II ↑ | p-SMAD2/3 ↑ | Villus atrophy, ↑permeability |
| 7 | ↑↑↑ | TβRI/II ↑↑ | p-SMAD2/3 ↑↑ | Crypt proliferation, restructuring |
| 14 | Baseline | Baseline | SMAD7 ↑ (feedback) | Barrier restored |

Source: [PMID 25170924]

## Feed additives that modulate TGF-β/SMAD in pigs

| Compound | Effect on TGF-β axis | Application |
|----------|---------------------|-------------|
| Anemonin | ↑TGF-β1, ↑p-SMAD3, ↑EGFR | LPS-injured intestine [27189428] |
| Whey protein concentrate | ↑TGF-β1 (natural source) | Post-weaning [26810899] |
| Cu/Zn-montmorillonite | ↑TGF-β1 mRNA | Inflammation control [28958208] |
| Eleutheroside E | ↑TGF-β1 signaling | Barrier protection [36375269, 35014099] |
| Alpha-ketoglutarate | ↑Th17/Treg balance via TGF-β | Immune modulation [37348134] |
| Zearalenone (toxin) | ↓TGF-β1, ↓Smads | Barrier disruption [34941739] |

## Research queries used (for reproducibility)

```
1. TGF-beta SMAD signaling intestinal barrier pig
2. TGF-beta1 immune regulation regulatory T cell pig
3. TGF-beta porcine intestinal epithelial cell tight junction
4. TGF-beta SMAD7 inflammation pig intestine
5. TGF-beta1 weaning stress pig intestinal health
6. TGF-beta SMAD2 SMAD3 phosphorylation pig intestine
7. TGF-beta1 regulatory T cell FoxP3 pig immune
8. SMAD7 TGF-beta negative feedback pig
9. TGF-beta bone morphogenetic protein pig growth
10. TGF-beta superfamily porcine reproductive
```

## Wikipedia search queries used

```
TGF beta signaling pathway
SMAD protein family
TGF beta superfamily
```
