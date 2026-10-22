# Antigen Processing & Presentation in Swine — MHC/SLA System

**Topic card:** created as KF card `2bd8feaa-603f-42eb-9c3c-360abd4722f0`
**Domain:** Porcine immunology, molecular mechanisms
**Virus evasion:** ASFV, PRRSV, PEDV, PRV, CSFV, TGEV, PDCoV
**Reading time:** ~21 minutes

## Quick reference: SLA (Swine Leukocyte Antigen) system

| Class | Classical genes | Non-classical | Expression |
|-------|----------------|---------------|------------|
| **SLA-I** | SLA-1, SLA-2, SLA-3 | SLA-6, -9, -11 (Ib) | All nucleated cells |
| **SLA-II** | SLA-DR (DRA/DRB1), SLA-DQ (DQA/DQB), SLA-DP (DPA/DPB) | SLA-DM (DMA/DMB), SLA-DO (DOA/DOB) | Professional APCs |

**Location:** SSC7p1.1, 2.4 Mb region, homologous to HLA and BoLA.

## Core pathway summary

### MHC-I (Endogenous / Cytosolic)
1. **Proteasome/Immunoproteasome** — degrades ubiquitinated cytosolic proteins into 8-16 aa peptides
2. **TAP (TAP1/TAP2)** — ABC transporter, translocates peptides into ER lumen
3. **Peptide Loading Complex (PLC)** — tapasin + calreticulin + ERp57 + MHC-I:β2M; tapasin performs peptide editing
4. **pMHC-I** — exported via Golgi to cell surface → CD8+ T cell recognition

### MHC-II (Exogenous / Endocytic)
1. **Endocytosis** → phagolysosome (cathepsins, low pH) → 15-24 aa peptides
2. **Invariant chain (CD74/Ii)** — blocks MHC-II groove in ER, directs to MIIC compartment, leaves CLIP fragment
3. **SLA-DM** — catalyzes CLIP→antigen peptide exchange; **SLA-DO** — negative regulator
4. **pMHC-II** → cell surface → CD4+ T helper cell recognition

### Cross-presentation
- cDC1 dendritic cells present exogenous antigen on MHC-I
- Two mechanisms: cytosolic diversion (endosome → cytosol → proteasome → TAP) and vacuolar pathway

## Master regulators

| Regulator | Target | Induced by | Notes |
|-----------|--------|-----------|-------|
| **NLRC5** | MHC-I + TAP1/2 + LMP2/7 + tapasin | IFN-γ → STAT1 → IRF1 | NOD-like receptor family CARD domain 5 |
| **CIITA** | MHC-II + CD74 + DM | IFN-γ | 4 promoters (pI-pIV), tissue-specific |

## Virus immune evasion — tested PubMed query patterns

### ASFV
```
"African swine fever virus MHC class I immune evasion porcine"
```
- SLA-I subversion via ER structure disruption (PMID: 40073098)
- TGN dispersal slows pMHC-I transport (PMID: 16956944)
- Requires SLA-DM for replication (PMID: 37604847)

### PRRSV
```
"PRRSV MHC downregulation antigen presentation pig"
"PRRSV Nsp12 proteasome"
```
- Nsp12 targets PSMA2 → inhibits proteasome (PMID: 41475191)
- miR-451→PSMB8 (LMP7) → promotes PRRSV (PMID: 39194214)
- Infects DCs → compromises antigen presentation (PMID: 17031757)

### PEDV
```
"PEDV MHC class I NLRC5 porcine"
```
- nsp1 inhibits NLRC5 translation → ↓MHC-I (PMID: 39480087)

### PRV (Pseudorabies)
```
"pUS6 pseudorabies virus antigen presentation swine"
```
- pUS6 inhibits PLC assembly → ↓SLA-I presentation (PMID: 39379944)

### TGEV / PDCoV (upregulate MHC-I — opposite evasion)
```
"TGEV RIG I NLRC5 SLA class I porcine"
```
- TGEV activates RIG-I→IFN-β→STAT1→NLRC5→↑SLA-I (PMID: 41803964)
- PDCoV activates RIG-I→IRF1→NLRC5→↑MHC-I (PMID: 35311551)

## Key PubMed PMIDs for swine antigen presentation

| PMID | Journal (Year) | Focus |
|------|---------------|-------|
| 42399753 | Cell Mol Biol Lett (2026) | SLA-I structure, peptide-binding groove |
| 41803964 | Vet Res (2026) | TGEV→RIG-I→NLRC5→SLA-I upregulation |
| 40073098 | J Immunol (2025) | ASFV disrupts ER→SLA-I subversion |
| 39480087 | J Virol (2024) | PEDV nsp1 inhibits NLRC5 translation |
| 39379944 | BMC Vet Res (2024) | PRV pUS6 blocks PLC assembly |
| 41475191 | Vet Microbiol (2026) | PRRSV Nsp12 targets PSMA2 proteasome |
| 39194214 | J Virol (2024) | miR-451→PSMB8→PRRSV promotion |
| 17031757 | Arch Virol (2007) | PRRSV infects DC→compromised presentation |
| 35311551 | J Virol (2022) | PDCoV→RIG-I→IRF1→NLRC5→↑MHC-I |
| 37604847 | Sci Rep (2023) | SLA-DM required for ASFV replication |
| 38962826 | Anim Model Exp Med (2024) | CIITA knockout in pigs for xenotransplant |
| 16555068 | Immunogenetics (2006) | Alternative splicing of porcine TAP1 |
| 10630293 | Immunogenetics (1999) | SLA-DRB1/DQB1 allelic diversity |
| 33996967 | Front Genet (2021) | SLA class I+II diversity in commercial pigs |
| 34028065 | HLA (2021) | SLA diversity in European farmed pigs |
| 30173748 | Dev Comp Immunol (2019) | cDC1/cDC2 response to PRRSV in trachea |

## Wikipedia page IDs for reference

| PageID | Title |
|--------|-------|
| 6548283 | Antigen presentation |
| 1892376 | MHC class I |
| 6564132 | MHC class II |
| 2170901 | Cross-presentation |
| 7516542 | Immunoproteasome |
| 211950 | Major histocompatibility complex |

## Feed additive modulation

| Compound | Effect on antigen presentation |
|----------|-------------------------------|
| IFN-γ (via CpG, β-glucan) | ↑CIITA, ↑NLRC5 → ↑MHC-I/II, ↑immunoproteasome |
| Butyrate | HDAC inhibition → ↑MHC-I/II (indirect) |
| Vitamin A (RA) | RAR/RXR → ↑MHC-I, ↑DC maturation |
| Vitamin D | ↑MHC-II on macrophages, ↑DC differentiation |
| Zn (zinc) | ↑DC maturation, ↑MHC-II |
| β-glucan | Dectin-1 → ↑DC maturation → ↑cross-presentation |
| CpG-ODN | TLR9 → ↑DC → ↑cross-presentation |
| Cortisol/stress | ↓CIITA → ↓MHC-II |
| DON mycotoxin | ↓protein synthesis → ↓MHC-I/II |
| ZEA mycotoxin | ER stress → ↓PLC |
