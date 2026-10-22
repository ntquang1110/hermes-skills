# Wnt/β-catenin Signaling in Swine — Condensed Research Roadmap

> "Con đường tín hiệu then chốt điều hòa tế bào gốc ruột, hàng rào niêm mạc và tái tạo biểu mô ở heo"
> Created: Jul 2026 · 16 PMIDs · 1 Wikipedia page · KF card ID: b1732d4d-fd7f-449c-b87e-a9fd6252ed84

## Key PubMed Queries Tested (Jul 2026)

| # | Query | Returns high-signal |
|---|-------|---------------------|
| 1 | `Wnt beta-catenin signaling intestinal stem cell pig` | ✅ ISC, organoid, FZD7 papers |
| 2 | `Wnt signaling porcine intestinal barrier tight junction` | ✅ Barrier protection via β-catenin |
| 3 | `Wnt beta-catenin swine weaning intestinal homeostasis` | ✅ Nutritional modulation (Glu, Zn) |
| 4 | `Wnt beta-catenin pathway pig intestine regeneration repair` | ✅ Virus-triggered repair (TGEV, PDCoV) |
| 5 | `R-spondin LGR5 intestinal stem cell pig Wnt` | ✅ RSPO1-LGR5 amplification loop |
| 6 | `Wnt signaling piglet intestinal crypt stem cell niche` | ✅ Stem cell niche, organoid models |
| 7 | `Wnt beta-catenin inhibitor DKK1 pig intestine` | ✅ Antagonists, regulation |
| 8 | `Frizzled receptor porcine intestine beta-catenin` | ✅ FZD7 as key receptor for ISC |

## Pathway Architecture

```
                    Feed Additives (Glu, Zn, Morin, Butyrate)
                              │
                              ▼
    ┌────────────────────────────────────────┐
    │           Frizzled7 + LRP5/6           │
    └────────────────────────────────────────┘
                              │
                              ▼
    ┌────────────────────────────────────────┐
    │              Dishevelled (Dsh)         │
    └────────────────────────────────────────┘
                              │
            ┌─────────────────┴─────────────────┐
            ▼                                   ▼
    ┌───────────────┐                 ┌─────────────────┐
    │Destruction    │                 │  Noncanonical   │
    │Complex (OFF)  │                 │  PCP / Ca²⁺     │
    │Axin/APC/GSK3β │                 └─────────────────┘
    │CK1α/PP2A      │
    └───────┬───────┘
            │ Wnt signaling ON
            ▼
    ┌───────────────┐     ┌────────────┐     ┌───────────┐
    │  β-catenin    │◄────│  PI3K/AKT  │◄────│ R-Spondin │
    │  accumulates  │     │  (pSer552) │     │ /LGR5     │
    └───────┬───────┘     └────────────┘     └───────────┘
            │
            ▼
    ┌───────────────────────┐
    │ β-catenin + TCF/LEF   │──── NF-κB crosstalk
    │ in nucleus            │──── TGF-β/SMAD
    └───────┬───────────────┘──── YAP/TAZ
            │
            ▼
    ┌───────────────────────────────────────────────┐
    │ c-Myc │ Cyclin D1 │ LGR5 │ Axin2 │ ASCL2 │ ...│
    └───────────────────────────────────────────────┘
            │
            ▼
    ┌───────────────────────────────────────────────┐
    │ ISC self-renewal │ Crypt proliferation │       │
    │ Goblet cell diff. │ Barrier repair │  EMT     │
    └───────────────────────────────────────────────┘
```

## Three Wnt Pathways

| Pathway | β-catenin? | Co-receptor | Effectors | Function |
|---------|-----------|-------------|-----------|----------|
| **Canonical (Wnt/β-catenin)** | ✅ Yes | LRP5/6 | β-catenin → TCF/LEF | Gene transcription, ISC self-renewal |
| **Noncanonical PCP** | ❌ No | ROR2/RYK | RhoA→ROCK, Rac1→JNK | Cytoskeleton, cell polarity |
| **Noncanonical Wnt/Ca²⁺** | ❌ No | G-protein | PLC→IP3→Ca²⁺→PKC, CaMKII | Intracellular Ca²⁺, ventral patterning |

## Destruction Complex (OFF state)

| Protein | Function | Notes |
|---------|----------|-------|
| **Axin** | Scaffold | Binds APC, GSK3β, CK1α, β-catenin |
| **APC** | Scaffold | Mutated in colorectal cancer |
| **GSK3β** | Kinase | Phosphorylates β-catenin at Thr41/Ser37/Ser33 |
| **CK1α** | Kinase | Priming phosphorylation at Ser45 |
| **PP2A** | Phosphatase | Dephosphorylates Axin |

## Target Genes of β-catenin/TCF

| Gene | Function | Notes |
|------|----------|-------|
| **c-Myc** | Proliferation, metabolism | G1→S cell cycle |
| **Cyclin D1** | Cell cycle | G1→S transition |
| **LGR5** | ISC marker | R-spondin receptor |
| **Axin2** | Negative feedback | Rebuilds destruction complex |
| **ASCL2** | ISC transcription factor | TCF/LEF target |
| **MMP7** | Matrix remodeling | EMT, tissue repair |
| **CD44** | Cell adhesion | Stemness marker |

## PMID Reference Table

| # | PMID | Year | Journal | Key Finding | Swine Relevance |
|---|------|------|---------|-------------|-----------------|
| 1 | **36121491** | 2022 | Cell Mol Life Sci | L-glutamate → FZD7 → β-catenin → ISC expansion in weaned piglets | **Direct nutritional intervention** for post-weaning ISC support |
| 2 | **32155551** | 2020 | Environ Pollut | Zn L-Aspartate → Wnt/β-catenin → ISC renewal, barrier vs DON | **Zn supplementation** mechanism for weaned piglets |
| 3 | **35997221** | 2022 | J Agric Food Chem | Porcine RSPO1 → ISC expansion along crypt-villus via Wnt | **Recombinant pRSPO1** as feed additive candidate |
| 4 | **38651967** | 2024 | J Agric Food Chem | Mulberry morin → binds FZD7 → activates β-catenin → ISC proliferation | **Plant-derived FZD7 agonist** for gut health |
| 5 | **36073923** | 2022 | J Virol | TGEV infection → Wnt/β-catenin → ISC proliferation → repair | Virus co-opts Wnt for **epithelial regeneration** |
| 6 | **40135895** | 2025 | J Virol | PDCoV → Wnt/β-catenin → ISC expansion in chicken organoids | **Cross-species Wnt activation** by coronavirus |
| 7 | **40797223** | 2025 | Vet Res | PEDV → suppresses Wnt + activates Notch → goblet cell loss | **Wnt suppression as PEDV pathogenesis** mechanism |
| 8 | **33373490** | 2021 | Stem Cells | ETEC STp → inhibits Wnt/β-catenin → ISC disruption | **Bacterial toxin inhibits Wnt** → diarrhea |
| 9 | **31960439** | 2020 | J Cell Physiol | Heat stress → inhibits Wnt → reduces ISC proliferation | **Heat stress mechanism** via Wnt suppression |
| 10 | **39912727** | 2025 | Elife | *Akkermansia muciniphila* → ↑Wnt/β-catenin → barrier vs ETEC | **Probiotic mechanism** via Wnt activation |
| 11 | **41072880** | 2025 | Free Radic Biol Med | β-catenin preserves gut vascular barrier in ETEC piglets | **Gut vascular barrier** protection |
| 12 | **38896938** | 2024 | Vet Microbiol | Benzoic acid → ↑ISC differentiation → goblet cells | **Feed additive** improves barrier via ISC |
| 13 | **37159340** | 2023 | FASEB J | LGR5 reporter pig model | **Tool** for ISC research in swine |
| 14 | **41321503** | 2025 | Anim Nutr | Terpine-4-ol → epithelial homeostasis → protects vs LPS | **Tea tree oil compound** for gut health |
| 15 | **41442918** | 2026 | Poult Sci | Butyrate → modulates ISC homeostasis | **Butyrate-Wnt** axis (poultry, but translatable) |
| 16 | **35852392** | 2022 | Cell Cycle | Berberine → Wnt pathway involvement in gut protection | **Herbal compound** mechanism |

## Feed Additive Modulation Table

| Agent | Mechanism (Wnt-related) | Effect | PMID |
|-------|------------------------|--------|------|
| **L-Glutamate** | ↑FZD7 → ↑β-catenin | ISC expansion, gut growth in weaned piglets | 36121491 |
| **Zn L-Aspartate** | ↑Wnt/β-catenin → ↑Lgr5 | ISC renewal, barrier vs DON | 32155551 |
| **R-Spondin 1 (porcine)** | LGR5 ligand → amplify Wnt | ISC expansion along crypt-villus | 35997221 |
| **Morin** (mulberry leaf) | Binds FZD7 → activate β-catenin | ISC proliferation | 38651967 |
| ***Akkermansia muciniphila*** | ↑Wnt/β-catenin | Barrier protection vs ETEC | 39912727 |
| **Butyrate** | Modulate ISC homeostasis | Balance crypt differentiation | 41442918 |
| **Benzoic acid** | ↑ISC differentiation (Wnt?) | ↑Goblet cells, mucus barrier | 38896938 |
| **Terpine-4-ol** | Intestinal epithelial homeostasis | Protects vs LPS injury | 41321503 |
| **Berberine** | Wnt pathway involvement | Gut protection (review) | 35852392 |

## Virus/Wnt Interaction in Swine

| Virus | Effect on Wnt | Consequence | PMID |
|-------|-------------|-------------|------|
| **TGEV** | **↑ Activates** — ↑β-catenin nuclear, ↑c-Myc, Cyclin D1 | ISC proliferation → epithelial repair | 36073923 |
| **PDCoV** | **↑ Activates** — ↑Wnt/β-catenin | ISC expansion (chicken organoids) | 40135895 |
| **PEDV** | **↓ Suppresses** + ↑Notch, MAPK | ↓Goblet cells, barrier disruption | 40797223 |
| **ETEC STp** | **↓ Suppresses** — ↓β-catenin, ↓Lgr5 | ISC disruption, intestinal injury | 33373490 |

## Key Pathway Crosstalk

| Pathway | Interaction with Wnt/β-catenin |
|---------|--------------------------------|
| **NF-κB** | β-catenin can ↑IκBα → inhibit NF-κB; NF-κB can inhibit β-catenin in chronic inflammation |
| **PI3K/AKT** | AKT phosphorylates β-catenin at Ser552 → ↑nuclear translocation via 14-3-3ζ |
| **Notch** | Reciprocal: Wnt ON → ISC renewal; Notch ON → absorptive lineage; PEDV disrupts balance |
| **Hippo/YAP/TAZ** | YAP/TAZ cooperate with β-catenin/TCF → proliferation |
| **TGF-β/SMAD** | SMAD3/4 interact with TCF/LEF → co-regulate target genes |
| **MAPK/ERK** | ERK phosphorylates TCF/LEF → ↑β-catenin binding affinity |
| **mTOR** | Via GSK3 inhibition (β-catenin-independent) or TSC2 activation |

## Practical Applications (Swine Production)

1. **Post-weaning gut health**: Glutamate + Zn → dual Wnt activation → ISC support during mucosal remodeling
2. **PEDV control**: Wnt agonists (RSPO1, Glutamate) may counteract PEDV-induced Wnt suppression
3. **Heat stress mitigation**: RSPO1 can restore Wnt signaling suppressed by hyperthermia
4. **Mycotoxin protection**: Zn + RSPO1 protect ISC from DON via Wnt (see ZEA roadmap for F-2/Wnt)
5. **Probiotic synergy**: *A. muciniphila* → Wnt activation → barrier protection

## Vietnamese Terminology

| English | Tiếng Việt |
|---------|-----------|
| Wnt/β-catenin pathway | Con đường tín hiệu Wnt/β-catenin |
| Canonical Wnt | Wnt kinh điển (phụ thuộc β-catenin) |
| Destruction complex | Phức hợp phân hủy |
| Intestinal stem cell (ISC) | Tế bào gốc ruột |
| LGR5 | Thụ thể LGR5 (marker tế bào gốc ruột) |
| Crypt | Hốc ruột / Crypt Lieberkühn |
| Villus | Nhung mao ruột |
| Frizzled (FZD) | Thụ thể Frizzled |
| Dishevelled (Dsh) | Protein Dishevelled |
| β-catenin | β-catenin (protein liên kết cadherin) |
| TCF/LEF | Yếu tố phiên mã TCF/LEF |
| R-Spondin | R-Spondin (chất khuếch đại tín hiệu Wnt) |
| Goblet cell | Tế bào hình đài / tế bào cốc |
| Tight junction | Kết nối chặt / Tight junction |
| Stress nhiệt | Heat stress |
| Cai sữa | Weaning |
| Hàng rào ruột | Intestinal barrier |
| Tái tạo biểu mô | Epithelial regeneration |

## Key Methodological Tips

- **ISC research model**: Porcine intestinal organoids (enteroids) from jejunal crypts are the gold standard
- **Wnt activation assay**: Measure nuclear β-catenin + target genes (c-Myc, Axin2, LGR5) by qPCR/IF
- **FZD7 inhibitor**: Use specific inhibitor to test FZD7 dependence of nutritional interventions
- **RSPO1 source**: Recombinant porcine RSPO1 is available (expressed in E. coli Rosetta™), see PMID 35997221
- **Heat stress model**: In vitro IPEC-J2 at 41°C for 72h; ex vivo enteroids for ISC activity
