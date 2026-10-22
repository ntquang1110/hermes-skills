# NOD1/NOD2 Signaling in Swine — Condensed Research Roadmap

> Condensed reference bank: 15 PubMed IDs, 5 Wikipedia pages, pathway architecture, NOD1 vs NOD2 comparison, RIPK2/TAK1/IKK mechanism, feed additive modulation matrix, NOD2-autophagy-ATG16L1 interaction, crosstalk with TLR4/NF-κB/MAPK/NLRP3, Vietnamese terminology, and tested PubMed queries. Created Jul 2026 from multi-angle PubMed + Wikipedia research for KF card generation.

---

## Key PubMed queries (tested Jul 2026)

| Query | PMIDs returned | Notes |
|-------|---------------|-------|
| `NOD2 NOD1 signaling pig intestinal immunity` | 1 (33091794) | Too narrow — influenza + humidity focus |
| `NOD1 NOD2 intestinal barrier swine` | 4 (35921778, 29510469, 27554055, 25915861) | Best hit rate for swine-specific |
| `NOD2 feed additive modulation pig` | 3 (29510469, 26079268, 23739309) | Feed additive articles all in swine |
| `NOD2 RIPK2 signaling pathway inflammatory` | 7 (42213708, 41724227, 41475440...) | Many, mostly non-swine mechanism papers |
| `porcine NOD2 gene expression intestinal` | 6 (37199152, 30310102, 29510469...) | 4 directly relevant to pig gut |
| `tryptophan NOD signaling pig` | 0 | Try additive-specific queries instead |
| `fish oil NOD2 pig` | 2 (23014495, 23739309) | Works well — additive + pathway |
| `NOD2 MDP autophagy RIPK2` | 0 in swine | Human/mouse only |

**Key lesson:** For pathway + feed additive research, the most productive queries combine the additive name, the pathway, and the species (e.g. `tryptophan NOD signaling pig`). Generic pathway queries return mostly non-swine mechanistic papers. If the first round returns poor results, try with specific additive names that are known modulators.

## PMID summary table

| PMID | Journal (Year) | Focus | Key finding / mechanism |
|------|---------------|-------|------------------------|
| 42213708 | PLoS Comput Biol (2026) | NOD1/2-RIP2 structure | **Structural basis of NOD2 tandem CARD association**; NOD1/2-RIP2 hetero-CARD filament assembly elucidated via MD simulations. NOD2CARD forms stable dimers before RIP2 recruitment. |
| 37199152 | Anim Biotechnol (2023) | Tryptophan / LPS pig | Tryptophan **↓ NOD1, NOD2, RIPK2, TLR4, MyD88, TRAF6** mRNA in jejunum of LPS-challenged piglets. ↑ tight junction proteins, ↓ TNF-α, IL-1β, IL-6. |
| 30310102 | Sci Rep (2018) | Glutamate / LPS pig | Glutamate **↓ TLR4, NOD1, NOD2, NF-κB** in weanling pig gut. Maintains phosphorylated mTOR. ↑ villus height/crypt depth, claudin-1. |
| 23014495 | J Nutr (2012) | Fish oil / NOD2 pig | **PIVOTAL** — Fish oil **↓ NOD2 and TLR4 signaling pathways** in weaned pigs after LPS challenge. ↑ intestinal integrity. |
| 29510469 | Mol Nutr Food Res (2018) | Flaxseed oil / TLR4/NOD pig | Flaxseed oil (ALA) attenuates intestinal damage via **regulating necroptosis + TLR4/NOD signaling** after LPS. |
| 27554055 | Innate Immun (2016) | Asparagine / NOD pig | Asparagine **↓ TLR4 and NOD signaling**, restores ODC expression, ↑ claudin-1. Differentially regulates p38 and ERK1/2. |
| 26079268 | Br J Nutr (2015) | Asparagine / hepatic pig | Asparagine **↓ NOD/TLR4** in liver of LPS-challenged piglets. ↓ AST, ALT, ↑ claudin-1. |
| 25915861 | PLoS One (2015) | L. rhamnosus / IPEC-J2 | **L. rhamnosus ↑ NOD1, TLR2; ↓ NOD2, TLR4, TNF-α** in ETEC-infected IPEC-J2 cells. EGFR-independent Akt activation. |
| 35921778 | Int Immunopharmacol (2022) | Niacin / PDCoV pig | Niacin improves barrier, modulates intestinal immunity after PDCoV challenge in weaned piglets. |
| 23739309 | J Nutr (2013) | Fish oil / muscle pig | Fish oil **↓ NOD2**, modulates Akt/FOXO, ↑ muscle protein mass in LPS-challenged weanling pigs. |
| 41724227 | Exp Eye Res (2026) | Berberine / NOD2 | Berberine **inhibits MDP→NOD2→RIPK2→NF-κB**, ↓ oxidative stress, ↓ pyroptosis in corneal epithelium (canine). |
| 40424656 | Int Immunopharmacol (2025) | β-glucan / NOD2 | β-glucan modulates **trained immunity** via NOD2/RIPK2 signaling in osteoclast differentiation. |
| 39519307 | Int J Mol Sci (2024) | RIPK2 / microglia | **RIPK2 is crucial** for microglial inflammatory response to MDP but not to LPS. MDP-specific signaling. |
| 39444201 | J Med Chem (2024) | NOD1-RIP2 inhibitor | First potent **NOD1-RIPK2** signaling pathway inhibitors (4-anilinoquinazoline derivatives) at nanomolar range. |
| 38343714 | Front Microbiol (2024) | L. plantarum / PIE cells | Probiotic strains from swine milk **modulate NOD1/NOD2 and PGRPs** in porcine intestinal epithelial cells. |
| 33091794 | Vet Microbiol (2020) | High humidity / influenza | Nod/RIP2/NF-κB pathway activated in high-humidity + influenza infection model. |

## Pathway architecture

### Ligand recognition

```
Gram-negative bacteria (iE-DAP) → NOD1
                                    ↓
Gram-positive & Gram-negative (MDP) → NOD2
                                    ↓
                              LRR domain sensing
                                    ↓
                    ATP-dependent NACHT oligomerization
                                    ↓
                        Exposure of CARD domain(s)
```

### Signal transduction cascade

```
NOD1 (1 CARD) or NOD2 (2 tandem CARDs)
    ↓ Oligomerization
CARD-CARD interaction
    ↓
RIPK2 (RIP2) — serine/threonine kinase
    ↓ Polyubiquitination (K63) by XIAP, cIAP1/2, TRAF6, ITCH
    ↓
TAK1 (MAP3K7) — TAB1/TAB2/TAB3 complex
    ↓
       ┌─────────────────────┐
       ↓                     ↓
     IKKα/IKKβ             MKK3/6, MKK4/7
       ↓                     ↓
    IκBα phos.           p38 MAPK, JNK
       ↓                     ↓
    IκBα degradation     AP-1 activation
       ↓
    NF-κB (p50/p65)
    nuclear translocation
       ↓
Pro-inflammatory genes:
TNF, IL-1β, IL-6, IL-8, COX-2, DEFB4
```

### NOD2-autophagy axis (unique to NOD2, not NOD1)

```
MDP → NOD2
       ↓
RIPK2 ────────── NF-κB (inflammatory)
  ↕
ATG16L1 (direct interaction with NOD2)
  ↓
ATG5-ATG12 complex recruitment
  ↓
LC3 lipidation at bacteria entry site
  ↓
Xenophagy — autophagic clearance of intracellular bacteria
```

**Note:** The NOD2-ATG16L1 interaction is independent of RIPK2 signaling. Loss-of-function NOD2 mutations (R702W, G908R, 1007fs) disrupt this interaction, explaining the strong genetic link between NOD2 and Crohn's disease. This mechanism is distinct from canonical PRR signaling.

### Negative regulation

| Negative regulator | Mechanism | Effect on NOD signaling |
|-------------------|-----------|------------------------|
| A20 (TNFAIP3) | Deubiquitinase → removes K63 from RIPK2 | ↓ NF-κB |
| CYLD | Deubiquitinase → removes K63 from RIPK2 | ↓ NF-κB |
| IRF4 | Competes with NF-κB for DNA binding | ↓ Transcription |
| ERBIN | Direct binding to NOD2 (CARD domain) | ↓ RIPK2 recruitment |
| ATG16L1 | Sequesters NOD2 for autophagy | ↓ Inflammatory signaling |
| NLRP12 | Suppresses NF-κB from NOD2 | ↓ Inflammation |

## NOD1 vs NOD2 comparison

| Feature | NOD1 (NLRC1) | NOD2 (NLRC2 / CARD15 / IBD1) |
|---------|-------------|------------------------------|
| **N-terminal CARDs** | 1 | **2** (tandem) |
| **Ligand** | iE-DAP (γ-D-glutamyl-meso-DAP) | MDP (muramyl dipeptide) |
| **Bacterial source** | Mostly Gram-negative | Both Gram-positive & Gram-negative |
| **Primary CARD partner** | RIPK2 | RIPK2 |
| **ATG16L1 interaction** | Weak | **Strong** (autophagy) |
| **Expression (porcine)** | Intestine, liver, lung, spleen | Intestine (Paneth cells, IEC), PBMCs |
| **Crohn's disease link** | Weak | **Strong** (3 major risk alleles) |
| **Role in apoptosis** | Moderate | Yes (via CARD-only proteins) |
| **Viral sensing** | No | Yes (ssRNA → MAVS → IFN, controversial) |

## Feed additive modulation matrix (swine)

| Additive | NOD1 | NOD2 | RIPK2 | NF-κB | TLR4 | mTOR | PMID |
|----------|------|------|-------|-------|------|------|------|
| **Tryptophan** | ↓↓ | ↓↓ | ↓ | ↓↓ | ↓↓ | — | 37199152 |
| **Glutamate** | ↓ | ↓ | — | ↓ | ↓ | ↑↑ | 30310102 |
| **Fish oil (ω-3)** | — | ↓↓ | — | ↓ | ↓↓ | — | 23014495, 23739309 |
| **Flaxseed oil (ALA)** | ↓ | ↓ | — | ↓ | ↓ | — | 29510469 |
| **Asparagine** | ↓ | ↓ | — | ↓ | ↓ | — | 27554055, 26079268 |
| **Niacin (B3)** | — | — | — | — | — | — | 35921778 (indirect) |
| **L. rhamnosus** | ↑↑ | ↓↓ | — | — | ↓↓ | ↑ | 25915861 |
| **Berberine** | — | ↓↓ | ↓↓ | ↓↓ | — | — | 41724227 (canine) |
| **β-glucan** | — | ↑↑ | ↑↑ | ↑ | — | — | 40424656 |
| **Nano-Se** | — | — | — | ↓ | — | — | 42070668 |

↓ = suppresses (beneficial in over-inflammation context)
↑ = activates (beneficial in immune training context)

## Pathway crosstalk

| Pathway | Interaction with NOD1/NOD2 | Consequence |
|---------|---------------------------|-------------|
| **TLR4** | Synergy — TLR4+NF-κB signal 1 + NOD2 signal 2 | Amplified cytokine production |
| **NF-κB** | Direct downstream target of NOD1/2/RIPK2 | Transcription of pro-inflammatory genes |
| **MAPK (p38/JNK)** | Via TAK1 → MKK3/6, MKK4/7 | AP-1 activation, mRNA stabilization |
| **Autophagy** | NOD2 → ATG16L1 (RIPK2-independent) | Xenophagy, bacterial clearance |
| **NLRP3** | NOD2 provides signal 1 (pro-IL-1β via NF-κB) | IL-1β maturation + pyroptosis |
| **Necroptosis** | Shared TAK1/RIPK1 axis | Flaxseed oil co-regulates both (PMID 29510469) |
| **PI3K/AKT/mTOR** | Glutamate maintains mTOR, suppresses NOD | Barrier protection (PMID 30310102) |
| **RIG-I/MAVS** | NOD2 → MAVS → IFN response (controversial) | Anti-ssRNA viral |
| **Nrf2** | Berberine: NOD2↓ + Nrf2↑ balance | Oxidative stress regulation (PMID 41724227) |

## Vietnamese terminology

| English | Tiếng Việt |
|---------|------------|
| NOD1/NOD2 | Thụ thể NOD1/NOD2 |
| NOD-like receptor (NLR) | Thụ thể giống NOD |
| Peptidoglycan | Peptidoglycan (thành tế bào vi khuẩn) |
| Muramyl dipeptide (MDP) | Muramyl dipeptide |
| iE-DAP | axit meso-diaminopimelic |
| RIPK2 (RIP2) | Kinase RIPK2 |
| CARD domain | Vùng CARD (tuyển dụng caspase) |
| Leucine-rich repeat (LRR) | Vùng lặp giàu leucine |
| NACHT/NOD domain | Vùng NACHT (liên kết nucleotide) |
| NF-κB | Yếu tố nhân kappa B |
| TAK1 | Kinase TAK1 |
| IKK | Phức hợp IKK |
| IκBα | Chất ức chế NF-κB |
| Autophagy | Tự thực bào |
| ATG16L1 | Protein ATG16L1 |
| Xenophagy | Tự thực bào tiêu diệt vi khuẩn |
| Pattern recognition receptor (PRR) | Thụ thể nhận dạng mẫu |
| Innate immunity | Miễn dịch bẩm sinh |
| Crohn's disease | Bệnh Crohn |
| Peptidoglycan recognition protein (PGRP) | Protein nhận dạng peptidoglycan |

## Recommended follow-up topics (not yet in KF as of Jul 2026)

- **NOD2 and Paneth cells** — α-defensin production, intestinal homeostasis
- **ATG16L1/IRGM/NOD2 autophagy axis** — fine mechanism of xenophagy
- **NOD1-specific signaling** — TAK1 vs alternate pathways, fewer studies
- **NLR family beyond NODs** — NLRC3, NLRC4, NLRC5, NLRX1 in swine
- **RIPK2 as therapeutic target** — small molecule inhibitors (GSK'583, WEHI-345)
- **MDP as innate adjuvant** — mifamurtide (NOD2 agonist) in vaccines
- **NOD2 trained immunity** — β-glucan→NOD2→epigenetic reprogramming
