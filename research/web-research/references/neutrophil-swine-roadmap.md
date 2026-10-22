# 🧬 Neutrophil (Bạch cầu trung tính) ở heo — Condensed Research Roadmap

**Generated:** 2026-07-21 | **Next cron topic:** Innate Lymphoid Cells, T cell signaling, or Interferons
**Sources:** Wikipedia (Neutrophil, Granulocyte, NETs, Chemotaxis) + 13 PMIDs (2020–2026)

## PubMed queries tested (Jul 2026)

| Query | Result quality | Returned PMIDs |
|-------|---------------|----------------|
| `porcine neutrophil innate immunity mechanism` | ✅ High — review on S. suis, NETosis papers | 10 hits (42253328..34835517) |
| `swine neutrophil recruitment chemotaxis chemokine` | ⚠️ Low — mostly old (pre-2000) | 5 hits (31988368..8276881) |
| `porcine neutrophil extracellular trap netosis swine` | ✅ High — NETosis in pig models | 5 hits (41888164..38887281) |
| `porcine neutrophil + Actinobacillus pleuropneumoniae` | ✅ Good — scRNA-seq lung fibrosis | 5 hits (42262353..40875191) |
| `swine bacterial pneumonia neutrophil lung` | ✅ Good — TBI+lung, lactobacilli papers | 5 hits (42262353..40875191) |
| `porcine neutrophil extracellular vesicle exosome` | ⚠️ Single hit (42274632) | 1 hit |
| `ASFV neutrophil chemotaxis` | ✅ Key paper (34481273) | 1 hit |

## Core PMID reference table

### S. suis — Neutrophil interaction
| PMID | Year | Journal | Finding | Key mechanism |
|------|------|---------|---------|---------------|
| 34835517 | 2021 | Microorganisms | Review: S. suis → neutrophilic leukocytosis, neutrophil = host defense + pathology driver | Exacerbated inflammation via neutrophil cytokine production |
| 41294351 | 2026 | Microbiol Spectr | SodA (superoxide dismutase) promotes immune evasion | SodA → suppresses ROS + GSDMD-mediated mitochondrial disruption → reduces NETosis |
| 39742898 | 2025 | Microb Pathog | Surface protein + polysaccharide capsule → neutrophil resistance | Capsule prevents opsonization and phagocytosis |
| 42253328 | 2026 | Transbound Emerg Dis | Comprehensive S. suis review: farm-to-fork control | Covers neutrophil interactions |

### Lung inflammation & A. pleuropneumoniae
| PMID | Year | Journal | Finding | Key mechanism |
|------|------|---------|---------|---------------|
| 41843736 | 2026 | Virulence | scRNA-seq piglet lung: A. pleuropneumoniae | Monocyte, neutrophil, pDC enrichment; TGFB1/HIF1A → fibrosis |
| 31988368 | 2020 | Sci Rep | Porcine CXCR1/2 antagonist (pG31P) | Inhibits neutrophil chemotaxis, reduces TNF-α/IL-1β in LPS pneumonia |
| 41829035 | 2026 | Animals | Oral Lactobacillus → improves lung neutrophil response | Gut-lung axis; probiotics prime respiratory innate immunity |

### NETosis in pigs
| PMID | Year | Journal | Finding | Key mechanism |
|------|------|---------|---------|---------------|
| 40722882 | 2025 | Antioxidants | Swine NETosis in neutrophil-spermatozoa co-cultures | BHT, PGE₂, seminal plasma inhibit NETosis (34.5%→12–14%); aggNETs + sprNETs |
| 42274632 | 2026 | Cells | ADSCs-Exo inhibit NET in pig liver IRI model | NADPH/MAPK pathway → reduced NET → reduced ferroptosis |

### Virus interactions
| PMID | Year | Journal | Finding | Key mechanism |
|------|------|---------|---------|---------------|
| 34481273 | 2021 | Vet Microbiol | ASFV transcriptome in PAMs | Enhanced neutrophil chemotaxis despite general immune suppression |
| 36341362 | 2022 | Front Immunol | PRRSV transcriptomics + metabolomics | Differential neutrophil involvement in HP-PRRSV response |

### Trauma & Neutrophil dysfunction
| PMID | Year | Journal | Finding | Key mechanism |
|------|------|---------|---------|---------------|
| 42262353 | 2026 | Crit Care Med | TBI in pigs → lung neutrophil dysfunction | TBI impairs PMN bacterial clearance; murine + porcine + human data |

## Key porcine neutrophil phenotype markers

| Marker | Porcine expression | Difference from human |
|--------|-------------------|---------------------|
| **CD16 (FcγRIII)** | Present on neutrophils | Humans: CD16 only on NK cells |
| **CD8α** | Variable on activated neutrophils | Humans: absent |
| **CXCR1/CXCR2** | Both expressed; targetable | Homologous to human; antagonist pG31P validated |
| **CD11b/CD18 (Mac-1)** | Strong expression; activation marker | Similar to human |
| **CD62L (L-selectin)** | Shed upon activation | Same mechanism |
| **TLR4** | Present | Functionally similar |
| **MHC-II (SLA-II)** | Reported on activated neutrophils | Humans: not expressed on neutrophils |

## NETois pathway in swine

```
PMA / IL-8 / LPS / Bacteria
    ↓
NADPH oxidase (NOX2: gp91phox + p22phox)
    ↓
O₂⁻ → H₂O₂ → HOCl (MPO)
    ↓
NE + MPO → nuclear translocation → histone cleavage
    ↓
PAD4 → Citrullination histone H3 (CitH3)
    ↓
Chromatin decondensation → nuclear membrane rupture
    ↓
aggNETs (dense clusters) OR sprNETs (fine fibers)
```

## Feed additive / compound effects on swine neutrophils

| Compound | Effect | Mechanism | PMID |
|----------|--------|-----------|------|
| Zn (zinc) | ↑ phagocytosis, ↑ ROS | Cu/Zn-SOD cofactor, membrane stabilization | — |
| Butyrate | ↓ excessive inflammation | HDAC inhibitor, ↓ pro-inflammatory cytokines | — |
| Lactobacillus (oral) | ↑ lung neutrophil function | Gut-lung axis priming | 41829035 |
| β-glucan | ↑ trained immunity in neutrophils | Dectin-1 → ROS, phagocytosis | — |
| BHT | ↓ NETosis (34.5%→12.2%) | Antioxidant, ↓ peroxynitrite | 40722882 |
| PGE₂ | ↓ NETosis (34.5%→14.5%) | cAMP/PKA pathway | 40722882 |
| Seminal plasma (20%) | ↓ NETosis (34.5%→16.8%) | Multiple factors | 40722882 |
| ADSCs-Exo | ↓ NET formation | NADPH/MAPK pathway inhibition | 42274632 |

## Vietnamese terminology

| English | Tiếng Việt |
|---------|------------|
| Neutrophil | Bạch cầu trung tính / Neutrophil |
| Granulocyte | Bạch cầu hạt |
| PMN / Polymorphonuclear leukocyte | Bạch cầu đa nhân trung tính |
| Phagocytosis | Thực bào |
| Chemotaxis | Hóa hướng động |
| Degranulation | Giải phóng hạt |
| NETosis | Hình thành bẫy ngoại bào (NET) |
| Respiratory burst | Bùng nổ hô hấp |
| NADPH oxidase | NADPH oxydase |
| Myeloperoxidase (MPO) | Myeloperoxidase |
| Neutrophil elastase | Elastase neutrophil |
| Opsonization | Opsonin hóa |
| Band cell / Stab cell | Neutrophil non (hình chữ U) |
| Pus | Mủ |
| Acute inflammation | Viêm cấp tính |
| Granulopoiesis | Tạo hạt / Sinh granulocyte |
| G-CSF | Yếu tố kích thích tạo hạt |
| Swarming | Di chuyển bầy đàn |
| Diapedesis | Xuyên mạch |

## Suggested next cron topics (not yet in KF)
1. **Innate Lymphoid Cells (ILCs) in swine** — ILC1/ILC2/ILC3, the innate counterparts of T cells
2. **T cell receptor signaling in swine** — TCR→CD3→ZAP-70→LAT→SLP-76→PKCθ→NFAT/AP-1
3. **Type I Interferons & ISGs in swine** — IFN-α subtypes, IFN-β, ISG15, Mx1, OAS, PKR
4. **B cells & humoral immunity in swine** — B cell development, antibody classes, IgA structure, colostral immunity
5. **Interleukin-1 family in swine** — IL-1α, IL-1β, IL-18, IL-33, IL-36–38, receptor signaling
6. **Acute phase response in swine** — CRP, haptoglobin, SAA, pig-MAP, diagnostic value
