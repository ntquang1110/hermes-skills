# IL-1 Family Cytokines in Swine — Condensed Research Roadmap

**Generated:** 2026-07-22 (cron session)
**Status:** Posted to KF as card #0 (111 cards total)
**Card ID:** b30d8361-5a0f-43af-9003-f01ad17b0585
**Reading time:** 20 min

---

## Topic overview

The Interleukin-1 family (11 cytokines) is the central cytokine system regulating inflammation, fever, and innate immunity. In swine, it controls macrophage activation, neutrophil recruitment, Th1/Th2/Th17 polarization, intestinal barrier integrity, and vaccine adjuvant response.

### 11 members

| Category | Members | Receptor | Key function |
|----------|---------|----------|-------------|
| Pro-inflammatory agonists | IL-1α, IL-1β | IL-1RI + IL-1RAcP | Fever, inflammation, neutrophil recruitment |
| Pro-inflammatory agonist | IL-18 | IL-18Rα/β | IFN-γ induction, Th1/NK activation |
| Pro-inflammatory agonist | IL-33 | ST2 + IL-1RAcP | Th2, ILC2, mast cell, alarmin, allergy |
| Pro-inflammatory agonists | IL-36α/β/γ | IL-36R + IL-1RAcP | Skin/epithelial inflammation, psoriasis |
| Antagonists | IL-1Ra, IL-36Ra | IL-1RI, IL-36R | Competitive inhibition |
| Anti-inflammatory | IL-37 | IL-18Rα + IL-18BP | Homodimer, nuclear factor, suppresses inflammation |
| Anti-inflammatory | IL-38 | soluble IL-1RI | Regulates innate and adaptive immunity |

### Core signaling pathway

```
IL-1α/β → IL-1RI + IL-1RAcP → TIR domain → MyD88 → IRAK4 → IRAK1/2 → TRAF6 → TAK1 → IKK + MAPK → NF-κB + AP-1 → pro-inflammatory genes
```

- IL-1R and TLR share **MyD88** and **TIR domain** — fundamental signaling convergence (PMID 23608822)
- **IL-1α:** dual-function (cytokine + DAMP + nuclear factor), precursor is active, calpain cleavage
- **IL-1β:** requires 2 signals (TLR→NF-κB for transcription + NLRP3→caspase-1 for cleavage), precursor inactive
- **IL-18:** similar to IL-1β (caspase-1 cleavage), induces IFN-γ, synergizes with IL-12
- **IL-33:** dual-function (alarmin + nuclear factor), **caspase-1 INACTIVATES** it (opposite of IL-1β/IL-18), activated by neutrophil proteases (cathepsin G, elastase)
- **IL-36:** skin/epithelium-focused, activated by neutrophil proteases

---

## Key PubMed queries tested (Jul 2026)

### Round 1: Broad topic discovery

| Query | Hits | Best PMIDs |
|-------|------|-----------|
| `IL-1β pig intestinal inflammation mechanism` | 5 | 42424947, 42264247, 42191074 |
| `interleukin-1 family swine immune response` | 5 | 41638206, 41485223, 37351955 |
| `IL-1α IL-1β porcine macrophage NLRP3` | **0** | — (too narrow) |
| `IL-18 pig interferon gamma Th1` | 5 | 27067203, 23331903, 22754326 |
| `IL-33 pig gut barrier Th2 mast cell` | **0** | — (too narrow) |
| `IL-1Ra anakinra pig inflammation` | 5 | 41562410, 39565032, 38087374 |
| `IL-36 pig skin inflammation` | **0** | — |
| `IL-37 anti-inflammatory pig` | 1 | 34445530 |

### Round 2: Mechanism-specific queries

| Query | Hits | Best PMIDs |
|-------|------|-----------|
| `porcine IL-1β caspase-1 inflammasome weaning` | 2 | 37358571, 29851202 |
| `porcine IL-18 IFN-γ NK cell Th1` | 2 | 36439124, 10901174 |
| `porcine IL-1 receptor MyD88 IRAK signaling` | 2 | 28783736, 23608822 |
| `pig IL-1 family cytokine gene expression intestine` | 5 | 40622657, 37199152, 28872975 |

### Round 3: Targeted deep search

| Query | Hits | Best PMIDs |
|-------|------|-----------|
| `IL-1β pig enterotoxigenic Escherichia coli ETEC` | 5 | 41939891, 41547922, 41431396 |
| `porcine IL-18 gene expression PRRSV infection` | 5 | 41786181, 41167014, 38727246 |
| `porcine IL-1β tight junction intestinal barrier LPS` | 5 | 42072019, 41739379, 41484717 |

---

## PMID reference table

| PMID | Journal (Year) | Contribution |
|------|---------------|-------------|
| 40622657 | Sci China Life Sci (2025) | Bacterial infection → NLRP3/IL-1β/pyroptosis → diarrhea in weaned piglets |
| 42191074 | Food Chem Toxicol (2026) | ZEA → IL-1β ↑ via Nrf2/NF-κB in IPEC-J2 cells |
| 37358571 | Eur J Nutr (2023) | Soybean glycinin/β-conglycinin → IL-1β → intestinal barrier damage |
| 40526995 | Vet Microbiol (2025) | PRV dsDNA → NLRP3 → IL-1β → pyroptosis in porcine cells |
| 41485223 | Cell Rep (2026) | GlyT1/SLC6A9 → AKT1/mTOR/NLRP3 → IL-1β in macrophages |
| 41786181 | Int J Biol Macromol (2026) | IL-18 expressed in live-attenuated PRRSV backbone → improved protection |
| 41167014 | Vaccine (2025) | PRRSV vector + porcine IL-18 + CSFV E2 → multivalent vaccine |
| 38727246 | mBio (2024) | Porcine IL-18BP splicing variants in PRRSV infection |
| 37351955 | J Anim Sci (2023) | NLRP3 inflammasome in M. hyopneumoniae infection |
| 28872975 | Immunol Invest (2017) | Inflammasome components in pig intestine, E. faecium effects |
| 29851202 | J Appl Microbiol (2018) | C. butyricum ↓ IL-1β, ↑ barrier function in weaned piglets |
| 23608822 | Innate Immun (2013) | TLR/MyD88/IRAK signaling in porcine alveolar macrophages |
| 41223610 | Int Immunopharmacol (2026) | PR39 AMP ↓ IL-1β via NF-κB/MAPK |
| 41562410 | Am J Sports Med (2026) | Anakinra intra-articular in porcine ACL graft model |
| 41431396 | Food Funct (2026) | Lysophospholipid ↓ IL-1β in ETEC-challenged piglets |
| 10803849 | Immunogenetics (2000) | Cloning porcine IL-18 gene (192 aa, 92% horse/90% dog/89% human) |
| 10901174 | Mol Cells (2000) | Porcine IL-18 expression in E. coli |
| 12396721 | J Interferon Cytokine Res (2002) | Cloning porcine IL-18Rα chain |
| 40052524 | J Food Sci (2025) | Microbe-derived antioxidants ↓ NLRP3/IL-1β in weaned piglets |
| 37199152 | Anim Biotechnol (2023) | Tryptophan ↓ IL-1β via TLR4/NOD in LPS piglets |
| 38087374 | Stem Cell Res Ther (2023) | Adipose MSC therapy ↓ IL-1 in porcine sepsis model |
| 22754326 | Int J Mol Sci (2012) | DNA vaccine co-expressing porcine IL-18 + PRRSV protein |

---

## Wikipedia pages used

| Page | PageID | Size | Key content |
|------|--------|------|-------------|
| Interleukin-1 family | 29871617 | 21KB | Full overview, signaling, clinical significance |
| Interleukin 1 beta | 5080276 | 11KB | Pro-IL-1β processing, caspase-1, two-signal model |
| Interleukin 1-alpha | 3215002 | 8.5KB | Dual-function, calpain, DAMP, nuclear localization |
| Interleukin 18 | 7801897 | 5.4KB | IFN-γ induction, IL-18BP, caspase-1, Th1 synergy |
| Interleukin 33 | 7807476 | 8.3KB | ST2 receptor, Th2, alarmin, caspase-1 INACTIVATES |
| Interleukin 36 | 39362636 | 3.9KB | Epithelial/skin, psoriasis, neutrophil protease activation |
| MYD88 | 6256274 | 3.6KB | TIR-domain adaptor, shared TLR/IL-1R |
| Interleukin-1 receptor associated kinase | 46332876 | 15KB | IRAK1/2/4/IRAK-M, serine-threonine kinases |

---

## Key mechanism diagrams (as text)

### IL-1β two-signal model in intestinal inflammation
```
Signal 1 (TLR/NF-κB): LPS, DON, ZEA → TLR4 → NF-κB → pro-IL-1β transcription
Signal 2 (NLRP3): ATP, ROS, crystals, bacterial toxins → NLRP3 → caspase-1 → mature IL-1β
                                                                                    ↓
                                                              IL-1R → NF-κB → IL-6, TNF, IL-8, COX-2
                                                                                    ↓
                                                                  Tight junction disruption, neutrophil infiltration, diarrhea
```

### IL-33 alarmin function in gut
```
Epithelial cell necrosis (weaning stress, pathogen) → IL-33 release
                                                           ↓
                                              ST2 on ILC2, mast cell, Th2
                                                           ↓
                                          IL-5, IL-13, IL-4, amphiregulin
                                                           ↓
                                              Eosinophil recruitment, tissue repair, goblet cell hyperplasia
```

### IL-18 + IL-12 synergy for Th1
```
IL-18 (from NLRP3) + IL-12 (from DC/macrophage)
                    ↓
               T cell / NK cell
                    ↓
              T-bet → IFN-γ
                    ↓
        Macrophage activation, antiviral state
```

---

## Practical implications for swine nutrition

| Feed additive | IL-1 family target | Mechanism | References |
|--------------|-------------------|-----------|------------|
| Butyrate | ↓ IL-1β | HDACi → ↓ NF-κB | 29851202 |
| ZnO (pharm.) | ↓ IL-1β | ↓ ROS → ↓ NLRP3 | KF card #49-51 |
| Tryptophan | ↓ IL-1β | AhR → ↓ NF-κB | 37199152 |
| Glutamate | ↓ IL-1β | TLR4/NOD modulation | 28783736 |
| C. butyricum | ↓ IL-1β | Butyrate, barrier | 29851202 |
| PR39 AMP | ↓ IL-1β | NF-κB/MAPK | 41223610 |
| Lysophospholipid | ↓ IL-1β | Barrier function | 41431396 |
| Berberine | ↓ IL-1β | ↓ NLRP3 | 41131200 |
| Microbe antioxidants | ↓ NLRP3/IL-1β | ↓ ROS | 40052524 |
| Anakinra (rIL-1Ra) | IL-1RI antagonist | Competitive inhibition | 41562410 |

---

## Vietnamese terminology

| English | Tiếng Việt |
|---------|-----------|
| Interleukin-1 family | Họ Interleukin-1 |
| IL-1β / IL-1 beta | IL-1 beta |
| Pro-inflammatory cytokine | Cytokine tiền viêm |
| Endogenous pyrogen | Chất gây sốt nội sinh |
| Alarmin / DAMP | Tín hiệu báo động tổn thương |
| Inflammasome | Thể viêm (inflammasome) |
| Caspase-1 | Caspase-1 (enzyme cắt) |
| MyD88 | Protein thích ứng MyD88 |
| NF-κB | Nhân tố phiên mã NF-κB |
| Intestinal barrier | Hàng rào ruột |
| Weaning stress | Stress cai sữa |
| Tight junction | Kết nối chặt (tight junction) |
| Pyroptosis | Chết tế bào viêm (pyroptosis) |
| IL-1Ra / Anakinra | Chất đối kháng thụ thể IL-1 |
| Dual-function cytokine | Cytokine hai chức năng |
