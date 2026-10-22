# Notch Signaling Pathway in Swine — Condensed Research Roadmap

> "Con đường tín hiệu tiếp xúc tế bào điều hòa biệt hóa biểu mô ruột, phát triển tế bào T và tương tác virus ở heo"
> Created: Jul 2026 · 15 PMIDs · 1 Wikipedia page (38KB) · KF card ID: e9c1ac40-ff3f-4f68-a85b-cadaf013ec82

## Key PubMed Queries Tested (Jul 2026)

| # | Query | Returns high-signal |
|---|-------|---------------------|
| 1 | `Notch signaling swine intestinal` | ✅ PRRSV↑Notch, PEDV↓goblet, lactic acid goblet, PDCoV ISC |
| 2 | `Notch signaling goblet cell differentiation intestine pig` | ✅ PEDV, PDCoV, PRRSV, Cd, benzoic acid goblet cell papers |
| 3 | `Notch pathway intestinal epithelial cell proliferation pig` | ✅ Maternal supplement, C. butyricum, TGEV |
| 4 | `Notch1 Notch2 Hes1 intestinal crypt pig` | Low hits — use broader queries for swine-specific Notch papers |
| 5 | `Hes1 Atoh1 intestinal secretory absorptive lineage` | ✅ Lawsonia (pig), Math1/Atoh1 fate determination |
| 6 | `Notch signaling T cell lineage development thymus` | ✅ T cell specification, E2A-Notch feedback |
| 7 | `Notch Delta-like Jagged ligand intestine epithelial` | ✅ M1 macrophage→Notch in epithelial cells (Crohn's) |
| 8 | `Notch signaling TH17 Treg differentiation CD4` | ✅ RBPJ inhibition→IL-17; Ikaros-Th17/Treg; MLL1→Notch in T cells |
| 9 | `Notch regulatory T cell Foxp3 induction` | ✅ CRISPR screen FOXP3, Jagged1→Treg expansion |
| 10 | `Notch signaling intestinal Paneth cell antimicrobial` | ✅ Paneth cell niche review; B. subtilis→secretory lineage |
| 11 | `Notch signaling intestinal barrier tight junction claudin occludin` | ✅ Notch/IL33/ST2→tight junction; asiatic acid→Notch2 |

## Pathway Architecture

```
    Signal-sending cell                    Signal-receiving cell
    ┌───────────────────┐                 ┌──────────────────────┐
    │  DLL1/DLL4/JAG1/2 │──── trans ────►│  NOTCH1/2/3/4        │
    │  (transmembrane)   │    interaction │  (transmembrane)     │
    └───────────────────┘                 │  EGF repeats 11-12   │
                                          │  bind DSL + MNNL     │
                                          │                      │
                                          │  ADAM10 (S2) ─── NECD│
                                          │  γ-secretase (S3) ── │
                                          │    → NICD released   │
                                          │         │            │
                                          │         ▼            │
                                          │  ┌─────────────┐    │
                                          │  │  NICD       │    │
                                          │  │  + CSL/RBPJ │    │
                                          │  │  + MAML     │    │
                                          │  │  + p300     │    │
                                          │  └──────┬──────┘    │
                                          │         ▼            │
                                          │  Target genes:       │
                                          │  HES1, HEY1, c-MYC  │
                                          │  Cyclin D1, DTX1     │
                                          │                      │
                                          │  HES1 ──X──► Atoh1   │
                                          │  (absorptive fate)   │
                                          │  (secretory fate)    │
                                          └──────────────────────┘
```

## Notch Receptors (4 in mammals)

| Receptor | Gene | EGF Repeats | Key Expression | Key Function |
|----------|------|-------------|----------------|--------------|
| **NOTCH1** | `NOTCH1` | 36 | T cell progenitors, ISC, endothelium | T cell development (thymus), ISC maintenance |
| **NOTCH2** | `NOTCH2` | 36 | Kidney, liver, ISC | ISC niche, kidney development, osteoclast |
| **NOTCH3** | `NOTCH3` | 34 | Vascular smooth muscle, CNS | Arterial specification, pericyte function |
| **NOTCH4** | `NOTCH4` | 29 | Endothelium | Angiogenesis, vascular development |

## Notch Ligands

| Ligand | Family | Expression | Effect on Target |
|--------|--------|------------|------------------|
| **DLL1** | Delta | Paneth cell, thymus epithelium | T cell specification, ISC maintenance |
| **DLL3** | Delta | Somites, CNS | Somitogenesis (DLL3 mutations → spondylocostal dysostosis) |
| **DLL4** | Delta | Tip cells, thymus epithelium | Angiogenesis, T cell commitment, Th1/Th17 polarization |
| **JAG1** | Serrate/Jagged | Stromal cells, DCs | Treg/Th2 induction, M2 macrophage, B cell development |
| **JAG2** | Serrate/Jagged | Thymus, keratinocytes | T cell development, skin differentiation |

## Core Signaling Machinery

| Enzyme | Cleavage Site | Function | Notes |
|--------|--------------|----------|-------|
| **Furin** | S1 (Golgi) | Maturation — creates NECD+NTM heterodimer | Constitutive, non-regulated |
| **ADAM10** | S2 (juxtamembrane) | Releases NECD + ligand complex | Ligand-dependent; requires mechanical force from trans-endocytosis |
| **ADAM17/TACE** | S2 (alternative) | Backup for ADAM10 in some contexts | Also cleaves TNF-α (TACE = TNF-α converting enzyme) |
| **γ-secretase** | S3 (intramembrane) | Releases NICD into cytoplasm | Complex of PSEN1/2, NCSTN, APH1, PEN2; also cleaves APP |

## "Fringe" Effect — Glycosylation Tuning

| Fringe Enzyme | Glycosylation | Effect on DLL | Effect on JAG | Tissue |
|--------------|---------------|---------------|---------------|--------|
| **Lunatic Fringe (LFNG)** | GlcNAc to O-fucose | ↑ Notch activation | ↓ Notch activation | Somites, thymus |
| **Manic Fringe (MFNG)** | GlcNAc to O-fucose | ↑ Notch activation | ↓ Notch activation | T cells, epithelial |
| **Radical Fringe (RFNG)** | GlcNAc to O-fucose | ↑ Notch activation | ↓ Notch activation | CNS, sensory organs |

## NOTCH1 → T Cell Development (Thymus)

```
CLP (common lymphoid progenitor)
  │
  │ DLL4 on thymic epithelium → NOTCH1
  ▼
Early T cell progenitor (ETP)
  │
  ├── NOTCH1 strong + DLL4 │ ├── αβ T cell (CD4⁺ or CD8⁺)
  │   HES1 represses GATA3 │
  │   E2A + Notch feedback │
  │                         │
  └── NOTCH1 weak ────────→ γδ T cell
      (less HES1, more E47)
```

## Intestinal Binary Fate (HES1 vs Atoh1)

```
            Lgr5⁺ ISC
                │
        (Wnt → proliferation)
        (Notch → maintenance)
                │
         Transit-Amplifying (TA)
                │
        ┌───────┴───────┐
        │               │
    NOTCH ON         NOTCH OFF
    HES1↑ Atoh1↓    HES1↓ Atoh1↑
        │               │
        ▼               ├──────────────┬─────────────┐
   Enterocyte        Goblet cell    Enteroendocrine  Tuft cell
   (absorptive)      (MUC2)         (hormones)       (IL-25)
   Paneth cell       Secretory Lineages
   (NOTCH+WNT)
```

**Paneth cell as ISC niche:** Paneth cells produce DLL1 and DLL4 → maintain Notch signaling in adjacent ISC → prevent premature differentiation. TGEV targets Paneth cells (via APN) → causes Paneth cell loss → DLL4/HES5 drop → ISC fail → villus atrophy (PMID 31959773).

## PMID Reference Table

| # | PMID | Year | Journal | Key Finding | Swine Relevance |
|---|------|------|---------|-------------|-----------------|
| 1 | **41138499** | 2025 | Vet Microbiol | PRRSV→↑Notch→↑goblet cell→excess mucin→nasal barrier disruption | **PRRSV pathogenesis** — Notch activation in nasal mucosa |
| 2 | **40797223** | 2025 | Vet Res | PEDV→↑Notch, MAPK + ↓Wnt→↓goblet cell→barrier loss | **PEDV pathogenesis** — Notch activation blocks secretory lineage |
| 3 | **38896938** | 2024 | Vet Microbiol | Benzoic acid→↑Notch→↑goblet cell/ISC diff→mucus barrier vs PEDV | **Feed additive** — benzoic acid protects via Notch |
| 4 | **37289083** | 2023 | J Virol | PDCoV→↓goblet cell→barrier disruption; Notch suppression | **PDCoV** — Notch dysregulation in enteric coronavirus |
| 5 | **28323899** | 2017 | PLoS One | *Lawsonia intracellularis*→↑Wnt+↑Notch1→crypt hyperplasia, blocked diff. | **Bacterial pathogenesis** — Lawsonia hijacks Wnt + Notch |
| 6 | **34988308** | 2022 | Anim Nutr | Neonatal piglet jejunum: ↑Smoc2(Sparc), ⬆Wnt signaling, Notch changes | **Developmental biology** — ISC/Notch maturation in neonates |
| 7 | **31959773** | 2020 | Cell Death Dis | TGEV→NSP10/16→↓Notch→Paneth cell loss→ISC failure→villus atrophy | **TGEV** — Notch suppression via Paneth cell targeting |
| 8 | **41151508** | 2025 | J Hazard Mater | Cd→↓Notch/ISC→↑APN→↑PDCoV infectivity in piglets | **Environmental toxin** — Cd aggravates PDCoV via Notch |
| 9 | **38946904** | 2024 | Front Microbiol | *Clostridium butyricum* CBX 2021→↑Notch→gut health | **Probiotic** — CBX 2021 activates Notch pathway in pigs |
| 10 | **36170821** | 2022 | Cell Rep | *Bacillus subtilis*→programs secretory lineage via Notch→↓Salmonella | **Probiotic** — B. subtilis uses Notch for protection |
| 11 | **29321062** | 2018 | Cell Commun Signal | DLL4→Notch→impedes M2 macrophage diff, promotes apoptosis | **Macrophage** — DLL4 drives M1 polarization |
| 12 | **37397914** | 2023 | Toxicol Res | Resveratrol→↓AhR/Notch→↑Foxp3→Th17/Treg balance in purpura | **Natural compound** — Resveratrol modulates Notch → T cell balance |
| 13 | **39341834** | 2024 | Cell Death Discov | p21→DREAM/MMB/Rb-E2F1→Wnt-Notch balance→ISC homeostasis | **ISC regulation** — p21 controls Wnt-Notch equilibrium |
| 14 | **39976915** | 2025 | Cell Mol Biol | Notch/IL33/ST2→tight junction maintenance after LPS | **Barrier function** — Notch regulates tight junction via IL33/ST2 |
| 15 | **36969191** | 2023 | Front Immunol | Paneth cell: birth→death in small intestine microenvironments | **Review** — Paneth cell lifecycle and niche function |

## Feed Additive / Intervention Modulation of Notch

| Agent | Effect on Notch | Downstream | Phenotype | PMID |
|-------|----------------|------------|-----------|------|
| **Benzoic acid** | ↑ Notch signaling | ↑ HES1, ISC diff → goblet cells | ↑ Mucus barrier vs PEDV | 38896938 |
| **Clostridium butyricum** CBX 2021 | ↑ Notch (mechanism) | Gut epithelial proliferation | Improved piglet health | 38946904 |
| **Resveratrol** | ↓ AhR/Notch axis | ↑ Foxp3, ↓ Th17 | Corrects Th17/Treg imbalance | 37397914 |
| **Bacillus subtilis** | Programs secretory lineage via Notch | ↑ Paneth & goblet cell diff | ↓ Salmonella infection | 36170821 |
| **Hydrogen gas** | Protects ISC via Notch maintenance | Preserved ISC in ischemia | ↓ Intestinal injury after I/R | 36632117 |
| **GSI (γ-secretase inhibitor)** | ↓ All Notch signaling | ↓ target gene expression | Experimental tool — use with caution | — |
| **Cadmium (toxin)** | ↓ Notch → ↓ ISC self-renewal | ↑ APN, microvilli damage | ↑ PDCoV susceptibility | 41151508 |

## Virus/Pathogen — Notch Interaction in Swine

| Pathogen | Effect on Notch | Mechanism | Disease Consequence | PMID |
|----------|----------------|-----------|---------------------|------|
| **PEDV** | **↑ Activates** Notch + MAPK; ↓ Wnt | ↓ Atoh1 → goblet cell differentiation blocked | ↓ MUC2 → barrier disruption, diarrhea | 40797223 |
| **PRRSV** | **↑ Activates** Notch → goblet cell diff | Excess mucus, tight junction disruption, ↑ cytokines | Nasal barrier dysfunction, respiratory disease | 41138499 |
| **TGEV** | **↓ Suppresses** Notch → Paneth cell loss | NSP10/16 complex → Paneth mito damage → ROS → Notch factor loss | ISC failure → villus atrophy | 31959773 |
| **PDCoV** | **↓ Suppresses** (goblet cell) | Reduced MUC2, tight junction disruption | Severe diarrhea | 37289083 |
| **Lawsonia intracellularis** | **↑ Activates** Notch1 + Wnt | Crypt hyperplasia, blocked secretory lineage | Proliferative enteropathy (PE) | 28323899 |

## Key Crosstalk with Other Pathways

| Pathway | Interaction with Notch | Context |
|---------|----------------------|---------|
| **Wnt/β-catenin** | Antagonistic in ISC fate: Wnt→growth, Notch→absorptive lineage; synergistic in crypt hyperplasia (Lawsonia) | Intestinal stem cell, PEDV |
| **PI3K/AKT/mTOR** | NICD→c-MYC→PI3K/AKT; mTOR feedback→Numb→inhibits Notch | Cell growth, metabolism |
| **NF-κB** | NICD→IKK→NF-κB; NF-κB→NOTCH1/3/HES1 → **positive feedback** | Inflammation, T cell activation |
| **MAPK/ERK** | ↑c-MYC→↑ERK; ERK phosphorylates NICD→stability | Proliferation |
| **AhR** | AhR regulates Notch/HES1; AhR→Atoh1 in intestine | Xenobiotic sensing, Th17/Treg |
| **Hippo/YAP** | YAP/TAZ cooperate with NICD in some contexts | Organ size, regeneration |
| **IL33/ST2** | Notch maintains IL33/ST2 → tight junction integrity | Barrier function after LPS | 39976915 |

## Practical Applications (Swine Production)

1. **Post-weaning gut barrier support**: Benzoic acid → ↑Notch → ↑goblet cells → ↑mucus barrier → ↓PEDV susceptibility
2. **PRRSV respiratory management**: GSI or Notch inhibitor could reduce PRRSV-induced goblet cell hyperplasia and excess mucus
3. **TGEV prevention**: NOTCH agonists (benzoic acid, probiotics) could counteract TGEV-induced Notch suppression → protect Paneth cells
4. **Probiotic mechanism**: *Clostridium butyricum* and *Bacillus subtilis* both modulate Notch for gut protection — screening tool
5. **Wnt-Notch balance**: Interventions should maintain equilibrium — too much Notch blocks secretory lineage; too little leads to ISC failure
6. **γ-secretase inhibitor risk**: GSI blocks all Notch → causes goblet cell metaplasia, immune suppression — not practical for feed

## Vietnamese Terminology

| English | Tiếng Việt |
|---------|-----------|
| Notch signaling pathway | Con đường tín hiệu Notch |
| NICD (Notch Intracellular Domain) | Vùng nội bào Notch (NICD) |
| NECD (Notch Extracellular Domain) | Vùng ngoại bào Notch (NECD) |
| Ligand (DLL/JAG) | Phối tử (DLL/JAG) |
| POFUT1 | Enzyme POFUT1 (O-fucosyl hóa Notch) |
| γ-secretase | γ-secretase (enzyme cắt S3) |
| ADAM10 | ADAM10 (metalloprotease cắt S2) |
| HES1 | Yếu tố phiên mã HES1 |
| Atoh1/Math1 | Yếu tố phiên mã Atoh1 (quyết định dòng chế tiết) |
| Fringe effect | Hiệu ứng Fringe (điều chỉnh glycosyl hóa) |
| Lateral inhibition | Ức chế bên (Notch-mediated) |
| Intestinal stem cell (ISC) | Tế bào gốc ruột |
| Paneth cell | Tế bào Paneth (cung cấp DLL cho ISC) |
| Goblet cell | Tế bào hình đài / tế bào cốc |
| Binary fate decision | Quyết định số phận nhị phân (hấp thu vs chế tiết) |
| MUC2 | Mucin 2 (chất nhầy do goblet cell tiết) |
| Juxtacrine signaling | Tín hiệu tiếp xúc trực tiếp tế bào |
| γ-secretase inhibitor (GSI) | Chất ức chế γ-secretase |
| Trans-endocytosis | Nội hóa qua tế bào gửi tín hiệu |

## Methodological Tips

- **Pig-specific Notch research**: Few direct papers on Notch in pigs. Broaden to mammalian literature, then validate relevance to swine pathophysiology
- **Notch activation assay**: Measure NICD nuclear translocation by IF/ICC; target genes (HES1, HEY1) by qPCR; γ-secretase activity by Western blot (NICD vs full-length)
- **GSI use**: DAPT or DBZ (γ-secretase inhibitors) are standard tools — use at 10-50 µM in vitro; in vivo dosing is more complex due to GI toxicity
- **ISC niche model**: Porcine enteroids ± Paneth cell co-culture to study Notch-DLL signaling in vitro
- **Goblet cell quantitation**: Alcian Blue/PAS staining for mucin + qPCR for MUC2, TFF3, KLF4 in intestinal tissue
- **Flow cytometry**: Anti-cleaved NOTCH1 (NICD) and HES1 for single-cell Notch activity readout in T cells and epithelial cells
