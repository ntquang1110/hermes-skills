# Kynurenine Pathway (Con đường Kynurenine) — Swine Research Roadmap

> Created: 22 Jul 2026 | 10 PMIDs | 5 Wikipedia pages | Card ID: `58326d7f-6d00-4a52-b6bc-91173467a0a5`

## Quick-reference — key PubMed queries (tested Jul 2026)

| Query | Result quality | PMIDs found |
|-------|---------------|-------------|
| `kynurenine pathway tryptophan metabolism pig intestinal immune` | ✅ Good | 36521060, 34748328, 30924357 |
| `IDO1 indoleamine 2,3-dioxygenase swine pig` | ✅ Good | 42004958, 40459260, 38814067, 30279361, 29930558 |
| `tryptophan kynurenine metabolic pathway pig gut microbiota` | ✅ Good | 40896477, 40588192, 36521060, 36263410, 32744096 |
| `TDO tryptophan 2,3-dioxygenase liver pig` | ⚠️ Partial | 31443750, 25810902, 22558963 (functional only) |
| `kynurenine IDO aryl hydrocarbon receptor pig intestine weaning` | ❌ Empty | — (too narrow; try splitting) |
| `kynurenic acid AhR ligand intestinal barrier pig` | ❌ Empty | — |

## Wikipedia pages consulted

| Pageid | Title | Notes |
|--------|-------|-------|
| 22276398 | Kynurenine pathway | Main pathway; metabolites, disorders |
| 8142356 | Indoleamine 2,3-dioxygenase (IDO1) | Heme enzyme, IFN-γ-inducible, immunosuppressive |
| 56340345 | Indoleamine 2,3-dioxygenase 2 (IDO2) | 43% homologous to IDO1, limited tissue, Treg role |
| 14144679 | Tryptophan 2,3-dioxygenase (TDO) | Liver-specific, tetrameric, systemic Trp regulation |
| 14045659 | Kynurenine 3-monooxygenase (KMO) | FAD-dependent, branch point → 3-HK/QUIN vs KYNA |
| — | Kynureninase (KYNU) | PLP-dependent (B6), cleaves KYN to AA |
| — | Kynurenine—oxoglutarate transaminase (KAT) | Produces kynurenic acid (KYNA) |
| — | Quinolinic acid | NMDA-R agonist, neurotoxic, NAD+ precursor |

## PMID table — mechanism-focused

| PMID | Year | System | Key finding | Journal |
|------|------|--------|-------------|---------|
| 38814067 | 2024 | PK-15 cells | CSFV → IDO1↑ → NF-κB↓ → viral replication ↑ | Microbiol Spectr |
| 36521060 | 2022 | Pig (LPS ileum) | Trp → AMPK-SIRT1-autophagy → barrier protection | J Agric Food Chem |
| 34748328 | 2021 | IPEC-J2 cells | Trp → CaSR → pBD1/pBD2↑ → epithelial defense | Cells |
| 36263410 | 2022 | GF pigs | Microbiota → Trp metabolism direction (KP vs indole) | Anim Nutr |
| 30279361 | 2018 | Pig (LPS shock) | 1-MT (IDOi) → Trp↑, KYNA↑, inflammation↓ | Shock |
| 40459260 | 2025 | Weaned pigs | PRRSV-2 NADC34-like → IDO1↑, immune checkpoint↑ | Front Immunol |
| 42004958 | 2025 | Pig cells | IRF1-IDO1 conserved human→pig; anti-Toxoplasma | bioRxiv |
| 40896477 | 2025 | Piglets | IPA (Trp metabolite) → PI3K-mTOR → glycolytic myofiber | Anim Nutr |
| 30924357 | 2020 | Review | Trp → AhR → IL-22/IL-17 → gut homeostasis | Crit Rev Food Sci |
| 36677028 | 2023 | Nursery pigs | KP altered in thermally oxidized oil → liver stress | Metabolites |
| 29930558 | 2018 | Oncopig model | IDO1 expression in TME, immune infiltration | Cancer Immunol Res |

## Pathway architecture (text diagram)

```
L-Tryptophan (Trp)
     │
     ├── IDO1/IDO2 (extralepatic) — IFN-γ inducible, heme
     └── TDO (liver) — tetrameric, systemic pool regulation
     │
     ▼
N-Formylkynurenine
     │
     ▼
Kynurenine (KYN) ◄──── 95% of Trp catabolism
     │
     ├── KMO (FAD) ──► 3-Hydroxykynurenine (3-HK)
     │                    │
     │                    ├── KYNU (PLP/B6) ──► 3-Hydroxyanthranilate (3-HAA)
     │                    │                        │
     │                    │                        ├── HAAO (Fe²⁺) ──► Quinolinic acid (QUIN)
     │                    │                        │                    │
     │                    │                        │                    ├── QPRT ──► NAD⁺
     │                    │                        │                    └── NMDA-R agonist → neurotoxicity
     │                    │                        │
     │                    └── KAT ──► Xanthurenic acid (XA)
     │
     ├── KAT I-IV ──► Kynurenic acid (KYNA) → NMDA antagonist, GPR35 agonist
     │
     └── KYNU (PLP/B6) ──► Anthranilic acid (AA) → 3-HAA → QUIN → NAD⁺
```

## Key immune mechanisms

| Mechanism | Mediator | Effector | Consequence |
|-----------|----------|----------|-------------|
| **Trp starvation** | IDO1 | GCN2 kinase | T cell cycle arrest (G₁), anergy |
| **KYN-AhR axis** | KYN | AhR→FoxP3 | Treg differentiation, Th17↓ |
| **NF-κB inhibition** | IDO1 | Trp metabolites | Viral replication ↑ (CSFV) |
| **CaSR-AMP** | Trp | CaSR→pBD1/pBD2 | β-defensin induction, epithelial defense |
| **AMPK-SIRT1** | Trp/KP? | Autophagy | Barrier protection, mucin↑ |
| **QUIN neurotoxicity** | QUIN | NMDA-R | Excitotoxicity, ROS, microglial activation |
| **KYNA neuroprotection** | KYNA | NMDA antagonist, GPR35 | Glutamate block, TNF-α↓ |

## Connections to existing KF cards

| Existing card | Connection |
|-------------|------------|
| **AhR** (card 40) | KYN is the endogenous AhR ligand — core connection |
| **Th17/Treg** (card 29) | KP determines Treg/Th17 balance via KYN-AhR |
| **IL-22** (card 11) | Trp→AhR→IL-22, epithelial barrier protection |
| **NF-κB** (card 48) | IDO1→NF-κB↓ (CSFV hijacking mechanism) |
| **JAK-STAT** (card 71) | IFN-γ→JAK-STAT1→IRF1→IDO1 induction |
| **Autophagy** (card 44) | Trp→AMPK-SIRT1-autophagy in gut protection |
| **Tryptophan→Serotonin** (card 59) | Competition for Trp pool: KP vs 5-HT |
| **Immunometabolism** (card 24) | KP produces NAD+ — central metabolic output |
| **Interferon, PRRs & JAK-STAT** (card 89) | IFN-γ is the primary IDO1 inducer |

## Vietnamese terminology

| English | Tiếng Việt |
|---------|------------|
| Kynurenine pathway | Con đường Kynurenine |
| Tryptophan catabolism | Dị hóa tryptophan |
| Indoleamine 2,3-dioxygenase (IDO) | Indoleamine 2,3-dioxygenase |
| Immune checkpoint | Điểm kiểm soát miễn dịch |
| Tryptophan starvation | Cạn kiệt tryptophan |
| Treg differentiation | Biệt hóa tế bào T điều hòa |
| NF-κB inhibition | Ức chế NF-κB |
| Intestinal barrier | Hàng rào ruột |
| β-defensin | β-defensin |
| NAD+ biosynthesis | Tổng hợp NAD+ |
| Quinolinic acid | Axit quinolinic |
| Kynurenic acid | Axit kynurenic |

## Feed additive / nutritional relevance

| Intervention | KP Effect | Mechanism | PMID evidence |
|-------------|-----------|-----------|---------------|
| **Trp supplementation** | ↑ KP flux → ↑ NAD+, immune modulation | CaSR, AMPK-SIRT1, AhR | 36521060, 34748328, 30924357 |
| **IFN-γ induction** (infection) | ↑ IDO1 → Trp↓, KYN↑ | JAK-STAT1→IRF1 | 38814067, 42004958 |
| **IDO1 inhibitors** (1-MT) | Trp↑, KYNA↑, inflammation↓ | Blocks Trp→KYN | 30279361 |
| **Vitamin B6** | ↑ KYNU activity → → NAD+ flux | PLP cofactor | Biochemistry |
| **Gut microbiota** | ↑/↓ KP vs indole pathway | Microbial Trp metabolism | 36263410 |
| **Probiotics (IPA producers)** | IPA→PI3K-mTOR (muscle) | Trp→IPA by gut bacteria | 40896477 |

## Key research gaps in swine

1. **IDO1 inhibitors in PRRSV/CSFV therapy** — 1-MT tested only in LPS model; no viral challenge study yet
2. **Trp:LNAA ratio optimization during weaning** — increased KP flux during inflammation competes with brain Trp uptake
3. **Vitamin B6 supplementation with high-Trp diets** — KYNU is PLP-dependent; B6 deficiency may bottleneck NAD+ production
4. **KMO as drug target** — KMO inhibitors shift KP from QUIN to KYNA (neuroprotective); not studied in pigs
5. **KP-trained immunity** — does Trp supplementation via KP modulate trained immunity?
