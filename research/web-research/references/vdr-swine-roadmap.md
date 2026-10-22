# 🧬 VDR (Vitamin D Receptor) Signaling in Swine — Condensed Reference Bank

> Generated: 2026-07-21 from cron research session. Sources: Wikipedia Action API + PubMed multi-query (12 queries, 18 unique PMIDs).

## Key PubMed Queries Tested (Jul 2026)

| Query | Results | Quality |
|-------|---------|---------|
| `vitamin D receptor pig intestine` | ✅ 5 hits — highly relevant | Excellent: VDR-FXR, PEDV, calcium absorption |
| `VDR pig immune cell` | ✅ 5 hits | Good: PRV replication, maternal interface |
| `25-hydroxyvitamin D3 pig growth performance immunity` | ✅ 5 hits | Excellent: multiple dose-response trials |
| `vitamin D3 pig weaned intestinal barrier` | ✅ 2 hits | Directly relevant |
| `vitamin D immune regulation pig macrophage` | ⚠️~50% noise | Refine with mechanism terms |
| `VDR antimicrobial peptide cathelicidin pig` | ❌ 0 hits | Try `vitamin D cathelicidin pig intestinal` instead |
| `vitamin D cathelicidin pig intestinal` | ✅ 1 hit | PMID 27174720 — directly relevant |

## PMID Table — VDR in Swine

| PMID | Year | Journal | Key Finding |
|------|------|---------|-------------|
| **41952052** | 2026 | J Agric Food Chem | **VDR-FXR heterodimer in pig liver** (AlphaFold3 + Co-IP). Vitamin D3 metabolite enhances VDR-FXR binding → downregulates CYP7A1/CYP8B1, upregulates BSEP/MRP2 → restores BA homeostasis → alleviates diarrhea. **Novel mechanism.** |
| **36142545** | 2022 | Int J Mol Sci | 1,25(OH)2D3 **suppresses PEDV-induced inflammation** in IPEC-J2: ↓p-NF-κB, ↓p-STAT1/3, ↑IκBα, ↑SOCS3, ↓IL-19, ↓CCL20. Does NOT affect viral replication. |
| **39475231** | 2024 | mBio | **PRV exploits VDR** for replication. PRV upregulates VDR via p53 → VDR enhances Ca2+ absorption → activates PI3K/AKT/mTORC1 and AMPK/mTORC1 → lipid synthesis. VDR knockdown impairs PRV. |
| **36139824** | 2022 | Antioxidants | 25(OH)VD3 vs VD3 (2000 IU) in weaned piglets. **25(OH)VD3 superior**: ↑tight junction (occludin, claudin, ZO-1), ↑host defense peptides, ↑acetate/butyrate in ileum, ↑antioxidase. |
| **33063320** | 2021 | J Sci Food Agric | 25OHD3 dose-response in piglets. Improved: growth, immunity, antioxidant (GPx, T-SOD), intestinal morphology (↑VH:CD), bone quality. |
| **34148242** | 2022 | J Sci Food Agric | 25OHD3 in weaned piglets on low Ca-P diet. ↑performance, serum Ca/P, altered fecal microbiota. |
| **31274343** | 2019 | Arch Anim Nutr | 25(OH)D3 (43-155 μg/kg) in weaned pigs. ↑serum 25(OH)D3 linearly, ↓CD3+CD4+/CD8+ T cells, ↑GPx at 80.5-118 μg/kg. |
| **37316951** | 2023 | Porcine Health Manag | 1,25(OH)2D from plant extract (100 ppm) in Iberian piglets. ↑ADG, FCR, IgA, IgG, improved intestinal histopathology. |
| **27174720** | 2016 | J Steroid Biochem Mol Biol | Vitamin D3 (5000 IU/kg) alleviates **Rotavirus** in pigs. ↑LC3-II/LC3-I (autophagy), ↑PR-39 mRNA. 25(OH)D3 ↓RV antigen & NSP4 in IPEC-J2. |
| **31290004** | 2019 | J Bone Miner Metab | Maternal 25-OH-D3 (50 μg/kg) in lactation sows. ↑bone density/strength, ↑Ca absorption via ↑CYP27B1, VDR, TRPV6, CaBP-D9k. |
| **29088291** | 2017 | PLoS One | VDR system at **maternal-conceptus interface** in pigs. CYP2R1, CYP27B1, CYP24A1, GC, VDR expressed in endometrium; stage-specific. Calcitriol highest in early pregnancy. |
| **39057937** | 2024 | Toxins | 25(OH)D3 + Vitamin E + C against **DON mycotoxin** in piglets. ↓oxidative stress, ↑antioxidant enzymes, restored vitamin D status. |
| **36847163** | 2023 | Br J Nutr | Systematic comparison: D3 vs 25(OH)D3 in pigs. 25(OH)D3 superior for growth, immunity, bone mineralization. |
| **24665105** | 2014 | J Anim Sci | Review: novel roles of vitamin D in animal immunity. Comparative immunology perspective, HyD (25(OH)D3) in swine. |

## VDR Pathway Architecture

Genomic pathway (hours):
  Vitamin D3 → (CYP2R1) → 25(OH)D3 → (CYP27B1) → 1,25(OH)2D3
                                                       |
                                                       ▼
                                                   VDR + RXR
                                                       |
                                                       ▼
                                                    VDRE
                                                       |
                                              ┌────────┴────────┐
                                              |                 |
                                        Transactivation   Transrepression
                                              |                 |
                                        Cathelicidin       NF-κB↓
                                        β-defensin         STAT↓
                                        TRPV6              IL-19↓
                                        CaBP-D9k           CCL20↓
                                        Occludin           TNF-α↓
                                        Claudin-1

Non-genomic (seconds):
  1,25(OH)2D3 → VDR membrane → Ca2+ flux → PI3K/AKT/mTORC1 → lipid synthesis
                                         → AMPK/mTORC1 → energy metabolism
                                         → MAPK/ERK → proliferation

## VDR-FXR Cross-talk (Novel 2026 Finding)

PMID 41952052:

  Vitamin D3 metabolite
         |
         ▼
  VDR ─── FXR (physical binding, AlphaFold3 + Co-IP)
         |
    ┌────┴────┐
    |         |
CYP7A1↓   BSEP↑
CYP8B1↓   MRP2↑
    |         |
    └────┬────┘
         ▼
  ↓7-ketoLCA in ileum
  ↓BA-induced diarrhea
  ↑intestinal barrier integrity

## Key Crosstalk Pathways

| Partner | Mechanism | Effect | PMIDs |
|---------|-----------|--------|-------|
| **NF-κB** | VDR ↑IκBα → ↓p65 nuclear translocation | Anti-inflammatory | 36142545 |
| **JAK-STAT** | VDR ↑SOCS3 → ↓p-STAT1/3 | ↓Cytokine signaling | 36142545 |
| **PI3K/AKT/mTORC1** | VDR → Ca2+ → PI3K → AKT → mTORC1 | Lipid synthesis; PRV exploitation | 39475231 |
| **AMPK/mTORC1** | VDR → Ca2+ → AMPK activation | Energy metabolism | 39475231 |
| **Nrf2** | VDRE/ARE crosstalk; both ↑GST, NQO1, GPx | Synergistic antioxidant | (inferred) |
| **FXR** | VDR-FXR heterodimer → BA homeostasis | ↓Diarrhea, liver protection | 41952052 |
| **Autophagy** | VDR ↑LC3-II, Beclin-1 | Anti-Rotavirus | 27174720 |

## VDR in Viruses — Dual Role

| Virus | VDR Role | Exploited? | Therapeutic? | PMID |
|-------|----------|-----------|-------------|------|
| **PRV** | **Pro-viral**: virus ↑VDR → ↑Ca2+ → ↑PI3K/AKT/mTORC1 → ↑lipid → replication | ✅ Yes (VDR KD ↓virus) | ❌ VDR agonists may worsen | 39475231 |
| **PEDV** | **Anti-inflammatory**: VDR agonist ↓NF-κB/STAT → ↓IL-19/CCL20 | ❌ No effect on replication | ✅ May reduce pathology | 36142545 |
| **Rotavirus** | **Anti-viral**: VDR agonist ↑autophagy (LC3-II) + PR-39 | ❌ | ✅ 5000 IU D3 protective | 27174720 |

## 25(OH)D3 vs Vitamin D3 in Swine

| Parameter | D3 | 25(OH)D3 | Advantage |
|-----------|-----|----------|-----------|
| Hydroxylation needed | Liver (CYP2R1) | None — pre-formed | 25(OH)D3 faster |
| Bioavailability | Lower | Higher (3-5x) | 25(OH)D3 |
| Tight junction | Moderate | Strong | 25(OH)D3 (PMID 36139824) |
| AMP induction | Moderate | Strong | 25(OH)D3 |
| Bone mineralization | Adequate | Superior | 25(OH)D3 (PMID 36847163) |
| Antioxidant (GPx) | Baseline | ↑↑ at 80-118 μg/kg | 25(OH)D3 (PMID 31274343) |
| Cost | Lower | Higher | D3 cheaper |

**Practical dose**: 25(OH)D3 50-80 μg/kg feed for weaned piglets; D3 2000-5000 IU/kg as baseline.

## Related KF Cards

See existing Knowledge Flow cards for connected pathways:
- `🧬 Nrf2/KEAP1` — antioxidant crosstalk with VDR
- `🧬 NF-κB` — VDR transrepresses via IκBα
- `🧬 Antimicrobial Peptides (AMPs)` — VDR drives cathelicidin/β-defensin
- `🧬 Axit mật và tín hiệu FXR/TGR5` — VDR-FXR interaction
- `🧬 Autophagy` — VDR upregulates LC3-II/Beclin-1
- `🧬 PI3K/AKT/mTOR` — VDR activates via Ca2+
- `🧬 Hàng rào ruột` — tight junction regulation by VDR
- `🐷 PEDV` — 1,25(OH)2D3 suppresses inflammation
