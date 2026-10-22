# Tight Junction (TJ) Proteins — Condensed Reference Bank

> **Tiếng Việt:** Protein kết nối tế bào biểu mô | **Family:** Claudin (27), Occludin, JAM, Tricellulin, Angulin | **Scaffold:** ZO-1/ZO-2/ZO-3 (MAGUK)
> **Cron-created:** Jul 2026 | **KF Card ID:** c5748cff-75c2-4a60-884b-23680424ddff

---

## Pathway Architecture Diagram

```
         Lumen
           │
    ┌──────┼──────┐
    │ TJ   │ TJ   │
    │←Claudin→│   │
    │←Occludin│   │
    │←JAM───→│   │  ← Paracellular space
    │   ↑    │   │
    └───┼────┴───┘
        │ ZO-1/ZO-2/ZO-3
        │ Cingulin
    ┌───┴─────────────────┐
    │   Actin Cytoskeleton │
    │   + Actomyosin Ring  │
    ├──────────────────────┤
    │ Signaling: MLCK, PKC │
    │ RhoA, PI3K, MAPK,AMPK│
    └──────────────────────┘
```

## Core Components

### Transmembrane Proteins

| Component | Members | MW | Function |
|-----------|---------|----|----------|
| **Claudin** | 27 (mammals) | 20-27 kDa | **Backbone of TJ** — charge/size selectivity via ECL1 charged residues |
| **Occludin** | 1 (OCLN) | 60-65 kDa | Stability; **NADH oxidase** regulating glucose uptake, ATP, NF-κB, sirtuins |
| **Tricellulin** | 1 (MARVELD2) | 64 kDa | Seals tricellular contacts |
| **JAM** | ~5 (JAM-A/B/C, JAM4, CAR) | 40-48 kDa | Ig-superfamily; leukocyte transmigration |
| **Angulin** | 3 (LSR, ILDR1, ILDR2) | 50-70 kDa | Tricellular TJ formation |

### Claudin Functional Dichotomy

| 🔒 Barrier-forming (↓ permeability) | 🔓 Pore-forming/channel (selective) |
|-------------------------------------|--------------------------------------|
| CLDN-1, -3, -4, -5, -8, -11, -14, -18, -19 | CLDN-2 (Na⁺, H₂O), -7 (anion), -10a/b, -15 (cation), -17 (anion) |

### Scaffold Proteins (MAGUK Family)

| Protein | Size | Domains | Role |
|---------|------|---------|------|
| **ZO-1** (TJP1) | 220 kDa | 3 PDZ, SH3, GuK | Central organizer: links claudin/occludin/JAM → actin |
| **ZO-2** (TJP2) | 160 kDa | 3 PDZ, SH3, GuK | Nuclear shuttling, transcription regulation |
| **ZO-3** (TJP3) | 130 kDa | 3 PDZ, SH3, GuK | Accessory |

**Scaffold chain:** `Claudin C-term → PDZ1(ZO-1)` | `Occludin C-term → PDZ3(ZO-1) → SH3 → GuK → Actin` | `JAM C-term → PDZ1(ZO-1)`

## Signaling Mechanisms

### MLCK/MLC (primary inflammation pathway)
```
TNF-α/IL-1β/LPS → TNFR1/TLR4 → NF-κB → ↑MLCK → p-MLC (Ser19/Thr18) → Actomyosin contraction → TJ opening
```

### RhoA/ROCK
- Basal: maintains TJ structure
- Excess: actomyosin contraction → TJ opening

### PKC Isoforms
| Isoform | TJ effect |
|---------|-----------|
| PKCα (conventional) | Phosphorylates occludin → strengthens TJ |
| PKCδ (novel) | Stress-induced claudin-1 opening |
| PKCζ (atypical) | Par3/Par6/aPKC polarity complex |

### MAPK/ERK → ↑MLCK + ↓claudin transcription
### Ca²⁺ → CaM → MLCK or calpain → claudin/occludin degradation

## Porcine Intestinal Distribution

| Segment | Key Claudins | Special notes |
|---------|-------------|---------------|
| Stomach | CLDN-1, -3, -4, -18 | Tightest barrier — pH 2-3 |
| Duodenum | CLDN-1, -2, -3, -5, -7 | CLDN-2 water absorption |
| Jejunum | CLDN-1, -2, -3, -4, -7, -15 | **IPEC-J2 cell model** |
| Ileum | CLDN-1, -3, -4, -8 | Tighter than duodenum |
| Colon | CLDN-1, -3, -4, -7, -8 | Very tight; CLDN-8 blocks Na⁺ back-flux |

## Feed Additive Modulation of TJ (Porcine)

| Compound | TJ Targets | Mechanism | Key PMID |
|----------|-----------|-----------|----------|
| ZnO | ↑ZO-1, Occludin, CLDN-1 | MLCK inhibition, PI3K/Akt | — |
| Butyrate | ↑ZO-1, Occludin, CLDN-3 | HDAC inhibition, GPR109A | 42121259 |
| Glutamine | ↑ZO-1, Occludin, CLDN-1 | HSP70/TLR4/NF-κB | — |
| Arginine | ↑ZO-1, Occludin, CLDN-1 | NO → cGMP → PKG | 41556082 |
| Tryptophan | ↑ZO-1, Occludin | AhR → IL-22 → STAT3 | 37688392 |
| Taurine | ↑ZO-1, Occludin, CLDN-1 | Nrf2 antioxidant | 39394665 |
| Chlorogenic Acid | ↑CLDN-1, Occludin, ZO-1 | TLR4/NF-κB + Nrf2 | 39337442 |
| Isoleucine | ↑CLDN-1, Occludin | Microbiome + metabolomics | 39770598 |
| Emodin | ↑TJ proteins | NF-κB + gut microbiota | 37455790 |
| PGP polysaccharide | ↑TJ proteins | TLR4/MyD88/NF-κB | 41986952 |
| PR-39 (AMP) | ↑ZO-1, Occludin | FXR/TGR5 | 40074117 |
| *L. reuteri* | ↑ZO-1, Occludin | MLCK inhibition | 35911699 |
| SDLactis (AMP) | ↑ZO-1, CLDN-1, Occludin | ETEC killing | 42281266 |
| Niacin+Butyrate | ↑TJ repair | NF-κB + metabolism | 42121259 |

## Pathogen Disruption of TJ in Swine

| Pathogen | Mechanism | Consequence |
|----------|-----------|-------------|
| **ETEC K88** | STa/LT → cAMP → ↑MLCK | Secretory diarrhea + leaky gut |
| **PEDV** | ↓Occludin, CLDN-1, ZO-1 via NLRX1/ERK/MLCK | Enteritis, villous atrophy |
| **PAstV-4** | ↑NLRX1 → mitophagy → ERK/MLCK | TJ disruption (PMID 38891045) |
| **TGEV** | ↓Occludin, CLDN-1 → enterocyte apoptosis | Diarrhea (PMID 41138168) |
| **Rotavirus** | NSP4 → Ca²⁺ → MLCK | Osmotic diarrhea |
| **Salmonella** | T3SS (SopB/SopE) → Rho GTPase | Paracellular invasion |
| **C. perfringens** | Enterotoxin CPE → claudin binding | Necrotic enteritis |

## Pathway Crosstalk

| Pathway | TJ Interaction |
|---------|---------------|
| **NF-κB** | ↑MLCK transcription; ↓CLDN-1 transcription |
| **Nrf2** | ARE on TJ gene promoters → protection |
| **PI3K/Akt** | TJ stability; ↓MLCK |
| **AhR** | IL-22 → STAT3 → TJ transcription |
| **VDR** | ↑CLDN-1, ↑Occludin |
| **FXR/TGR5** | ↑Occludin, ZO-1; ↓MLCK |
| **MAPK/ERK** | ↑MLCK; ↑CLDN-2 |
| **Wnt/β-catenin** | β-catenin → E-cadherin → AJ → TJ |
| **AMPK** | TJ assembly; ATP-dependent |
| **mTOR** | TJ protein synthesis |

## Key PubMed Queries Tested Jul 2026

```bash
# Broad TJ + pig
'tight junction claudin occludin pig intestinal barrier' → 6 PMIDs

# Weaning-specific
'tight junction protein pig weaning intestinal permeability' → 6 PMIDs

# Feed additive TJ
'ZO-1 claudin occludin piglet feed additive' → 6 PMIDs

# Pathogen-TJ
'tight junction pig pathogen Escherichia coli Salmonella' → 5 PMIDs

# Regulation mechanisms
'tight junction regulation myosin light chain kinase MLCK pig intestine' → 5 PMIDs
'occludin phosphorylation regulation tight junction pig' → 5 PMIDs
```

## Reference PMID Table

| PMID | Journal (Year) | Contribution |
|------|---------------|--------------|
| 42039840 | Front Microbiol (2026) | *L. reuteri* ↑ TJ function in suckling piglets |
| 42281266 | J Agric Food Chem (2026) | SDLactis ↑ ZO-1/CLDN-1/Occludin in ETEC piglets |
| 42235708 | Microb Pathog (2026) | *Bacillus* ↑ TJ + ISG15 anti-PEDV |
| 42140396 | Fitoterapia (2026) | Bistort extract ↑ TJ integrity IPEC-J2 |
| 42121259 | J Anim Sci Biotechnol (2026) | Butyrate+niacin ↑ TJ repair in ETEC piglets |
| 41986952 | Anim Biosci (2026) | PGP polysaccharide ↑ TJ + NF-κB inhibition |
| 39770598 | Microorganisms (2024) | Isoleucine ↑ colonic TJ in Rotavirus piglets |
| 39337442 | Int J Mol Sci (2024) | CGA ↑ CLDN-1/Occludin/ZO-1 via TLR4/Nrf2 |
| 39170630 | Front Vet Sci (2024) | Taurine ↑ TJ + antioxidant in weaned piglets |
| 41556082 | FASEB J (2026) | Arginine ↑ TJ during PEDV repair |
| 40074117 | Int J Biol Macromol (2025) | PR-39 ↑ TJ via FXR/TGR5 |
| 38891045 | Cells (2024) | PAstV-4 → NLRX1 → ERK/MLCK → ↓TJ |
| 35911699 | Front Immunol (2022) | *L. reuteri* ↑ TJ via MLCK inhibition |
| 34445450 | Int J Mol Sci (2021) | TNF-α → ↓Occludin/CLDN-1/3 in IPEC-J2 |
| 39394665 | J Anim Sci (2024) | Taurine dose-response ↑ TJ in piglets |
| 37455790 | Anim Nutr (2023) | Emodin ↑ TJ via NF-κB + microbiota |
| 42013546 | BBRC (2026) | Claudins in digestive system — Review |
| 24665396 | Tissue Barriers (2013) | ZO-2 scaffold + nuclear signaling — Review |
| 21294657 | Antioxid Redox Signal (2011) | ZO proteins and redox — Review |
| 42181623 | Front Cardiovasc Med (2026) | Occludin NADH oxidase — Review |
| 16215741 | Histochem Cell Biol (2006) | IPEC-J2 cell line characterization |

## Key Porcine IPEC-J2 Cell Model Notes

- Non-transformed jejunal enterocyte line from neonatal pig
- Expresses: CLDN-1, -3, -4, occludin, ZO-1
- Forms monolayer with stable TEER
- Responds to: TNF-α, LPS, ETEC, PEDV, probiotics, feed additives
- Standard *in vitro* model for TJ research in swine

## Vietnamese Terminology

| English | Tiếng Việt |
|---------|-----------|
| Tight junction | Kết nối chặt / Zonula occludens |
| Claudin | Claudin (giữ nguyên) |
| Occludin | Occludin (giữ nguyên) |
| ZO-1 / Zonula occludens-1 | ZO-1 |
| JAM (Junctional Adhesion Molecule) | Phân tử bám dính kết nối |
| Paracellular permeability | Tính thấm cạnh tế bào |
| Intestinal barrier | Hàng rào ruột |
| Leaky gut | Tăng tính thấm ruột |
| Transepithelial electrical resistance (TEER) | Điện trở xuyên biểu mô |
| Weaning stress | Stress cai sữa |
| Scaffold protein | Protein khung |
| Tricellular tight junction | Kết nối chặt 3 tế bào |
