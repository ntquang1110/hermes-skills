# Hippo/YAP/TAZ Signaling Pathway — Swine Research Roadmap

> Generated 2026-07-24 from cron research session
> Card ID: 7cd56442-2054-495e-8f93-ed61fa8f2ff4

## Core Pathway Architecture

```
Mechanical cues (ECM stiffness, stretch, shear stress)
GPCR (GPR43/SCFA, LPA, etc.) ──┐
Contact inhibition ─────────────┤
                                ▼
        ┌─ MST1/2 (STK4/3) ── MAP4Ks ──┐
        │     │              │         │
        │  SAV1 (scaffold)    │         │
        │     │              │         │
        └───► LATS1/2 ◄── MOB1A/B ◄────┘
                    │
        (phosphorylate YAP/TAZ)
                    ▼
        YAP/TAZ ─► 14-3-3 (cytoplasmic)
        [Hippo ON = growth OFF]

        When Hippo OFF:
        YAP/TAZ → Nucleus → TEAD1-4
        → CTGF, CYR61, AREG, BIRC5, AXIN2
        → Cell proliferation, tissue regeneration
```

## Key PubMed Queries Tested (Jul 2026)

| Query | Results | Key PMIDs |
|-------|---------|-----------|
| `Hippo+signaling+pathway+swine+pig+intestinal` | 5 | 37257635, 37183705, 34880865, 34737761, 34418579 |
| `YAP+pig+intestine+swine` | 5 | 30889135, 30137679, 29792306, 28719764, 9664577 |
| `Hippo+pathway+intestinal+epithelial+regeneration` | 5 | 42477345, 42425393, 42150849, 42135816, 42099526 |
| `YAP+TAZ+intestinal+stem+cell+homeostasis` | 5 | 42456186, 42150849, 41064361, 40865852, 40821111 |
| `YAP+TAZ+mechanotransduction+intestine` | 5 | 42211053, 42135816, 41064361, 38927855, 38300738 |
| `YAP+intestinal+barrier+function` | 5 | 42310292, 41854525, 41011940, 40395982, 39849698 |
| `YAP+intestinal+stem+cell+ISC+regeneration` | 5 | 42317040, 41015323, 40651470, 40201327, 39794306 |
| `Hippo+pathway+YAP+TAZ+cell+proliferation+apoptosis` | 5 | 42437161, 42381366, 42310011, 42269786, 42150849 |
| `Hippo+YAP+viral+infection+innate+immunity` | 5 | 42275403, 40701343, 39271776, 35503798, 34113355 |
| `YAP+TAZ+butyrate+short+chain+fatty+acid` | 3 | 39510146, 34944770, 34112743 |

## Core PMID Table

| PMID | Journal (Year) | Contribution |
|------|---------------|-------------|
| 42150849 | *Cold Spring Harb Perspect Biol* (2026) | **Key review**: Hippo in intestinal regeneration, fetal reprogramming, revSCs, crosstalk with Wnt/TGF-β/p53 |
| 42477345 | *NPJ Regen Med* (2026) | LATS1/2 inhibitor (NCGC-023) → YAP active → intestinal regeneration after irradiation |
| 42135816 | *J Nanobiotechnology* (2026) | ECM stiffness → YAP mechanosensing → mucosal repair in colitis |
| 42456186 | *Curr Opin Genet Dev* (2026) | Intestine (revSCs/YAP) vs stomach (paligenosis) regenerative strategies |
| 40865852 | *Toxicon* (2025) | DON → Hippo YAP/TAZ dysregulation → ISC damage — review + therapeutic targets |
| 42099526 | *Life Metab* (2026) | FPR2 → PKC/ERK → Wnt + Notch + Hippo → ISC regeneration |
| 40821111 | *Genes Dis* (2025) | Circadian rhythm ↔ BMAL1/CLOCK ↔ Wnt/Notch/Hippo ↔ ISC fate |
| 34112743 | *Mol Cells* (2021) | **GPR43 (SCFA receptor) → Gαq/11 + Gα12/13 → RhoA → YAP/TAZ** |
| 39510146 | *Pharmacol Res* (2024) | Ketogenic diet → BHB → HDAC3 → AMOT-YAP/TAZ → TAN polarization |
| 42425393 | *Eur J Pharmacol* (2026) | Vitamin D3 → normalize YAP phosphorylation → mucosal healing + M2 macrophage |
| 37257635 | *Food Chem Toxicol* (2023) | DON (2000 ng/ml) → **Hippo pathway activation** in IPEC-J2 cells |
| 35503798 | *PLoS Pathog* (2022) | **IAV NS1 hijack YAP/TAZ** → TLR3↓ via HDAC4/6 → immune evasion |
| 42275403 | *PLoS Pathog* (2026) | Hippo-virus interactions review: MST1/2 support antiviral, YAP/TAZ suppress innate immunity |
| 40701343 | *Virol Sin* (2025) | ARRDC3 → lysosomal YAP degradation → broad-spectrum antiviral |
| 41854525 | *FASEB J* (2026) | YAP1↓ → cGAS-STING → MASLD + gut microbiota dysbiosis |
| 42269786 | *Mech Ageing Dev* (2026) | Hippo-YAP/TAZ in cellular senescence — comprehensive review |
| 41015323 | *J Ethnopharmacol* (2026) | Shaoyao decoction → Wnt/β-catenin + YAP1/TAZ → ISC proliferation |
| 40651470 | *Cell Stem Cell* (2025) | Bacterial ADP-heptose → ALPK1-TIFA → TGF-β + YAP → revSC |
| 38879122 | *J Adv Res* (2024) | SelenoM deficiency → Hippo-YAP/TAZ-ROS → metaflammation in obesity |
| 42310292 | *Cell Death Dis* (2026) | BECLIN1 insufficiency → goblet cell loss, YAP-independent |

## Pathway Crosstalk Connections

| Existing KF Card | Connection to Hippo/YAP/TAZ |
|-----------------|---------------------------|
| 🧬 Wnt/β-catenin (card 25) | YAP binds β-catenin → SWI/SNF; AXIN2 is YAP target; destruction complex phosphorylates both |
| 🧬 Notch (card 23) | YAP competes with RBPJ; YAP regulates HES1; circadian clock → both pathways |
| 🧬 TGF-β/SMAD (card 38) | YAP/TAZ bind SMAD2/3; TGF-β activates YAP via RhoA; YAP needed for SMAD nuclear retention |
| 🧬 NF-κB (card 69) | YAP suppresses TLR3 via HDAC4/6; YAP regulates IκBα promoter (YAP/TEAD4 → Nfkbia) |
| 🧬 PI3K/AKT/mTOR (card 62) | YAP target AREG → EGFR → PI3K/AKT; AKT phosphorylates/inhibits LATS1/2 |
| 🧬 AMPK (card 1) | AMPK phosphorylates YAP (S61/94) → inhibition; metabolic stress ↔ Hippo |
| 🧬 cGAS-STING (card 52) | YAP1 deficiency → cGAS-STING activation → senescence + MASLD |
| 🧬 Nrf2/KEAP1 (card 63) | p62-mediated NRF2 ↔ YAP crosstalk via ARE elements |
| 🧬 Butyrate (card 74) | Butyrate → GPR43 → Gαq/11 + Gα12/13 → RhoA → YAP stabilization |
| 🧬 Vitamin D Receptor (card 29) | VD3 → normalizes YAP phosphorylation → barrier repair |
| 🧬 Selen & Selenoprotein (card 42) | SelenoM deficiency → Hippo-YAP/TAZ-ROS signaling |
| 🧬 Tight Junction (card 11) | YAP regulates ZO-1/Claudin-1 expression; VD3→YAP→barrier |
| 🧬 Autophagy (card 65) | BECLIN1 ↔ YAP; autophagy regulates YAP degradation |
| 🧬 Ferroptosis (card 54) | Hippo activation → decreased ferroptosis; YAP/TAZ regulate GPX4/System Xc⁻ |
| 🧬 Cellular Senescence (via Sirtuins card 8) | YAP/TAZ deficiency → p16/p53 → senescence; Hippo → YAP cytoplasmic → senescence |
| 🧬 Hàng rào ruột (card 72) | YAP → ZO-1, Claudin-1; revSCs → epithelial recovery |
| 🧬 IL-1 Family (card 21) | YAP regulates IL-33 (alarmin) in intestinal regeneration (PMID 42477345) |
| 🧬 Interferon-gamma (card 10) | YAP/TAZ suppress TLR3 → IFN ↓; IAV NS1 → YAP → immune evasion |

## Nutritional Modulation of Hippo/YAP/TAZ

| Factor | Mechanism | Effect | PMID |
|--------|-----------|--------|------|
| **Butyrate / SCFAs** | GPR43 → Gαq/11 + Gα12/13 → RhoA → YAP/TAZ stabilization | ↑ YAP nuclear → ↑ regeneration | 34112743 |
| **Vitamin D3** | Normalizes YAP1 phosphorylation; reduces Hippo activation | ↑ Barrier (ZO-1, Claudin-1), ↑ M2 macrophage | 42425393 |
| **β-hydroxybutyrate (BHB)** | HDAC3 inhibition → AMOT → YAP/TAZ axis | ↓ N2 TANs, ↓ colorectal cancer | 39510146 |
| **DON (mycotoxin)** | Activates Hippo pathway in IPEC-J2; dysregulates ISC | ↓ Regeneration, ↑ gut injury | 37257635, 40865852 |
| **Zn²⁺** | Modulates LATS/YAP in cancer cells (mechanism unclear in swine) | ↑ Proliferation (context-dependent) | 41896362, 34289746 |
| **SelenoM deficiency** | ↑ Hippo-YAP/TAZ-ROS → metaflammation | ↑ Oxidative stress, ↑ inflammation | 38879122 |
| **Glutamine** | Modulates mTOR/p70S6K which crosstalk with Hippo | ↑ ISC proliferation (indirect) | (inferred) |
| **Adhesive ECM / mechanical load** | Actin cytoskeleton → YAP nuclear translocation | ↑ Regeneration in response to digesta bulk | 42135816 |

## Vietnamese Terminology

| English | Tiếng Việt |
|---------|-----------|
| Hippo signaling pathway | Con đường tín hiệu Hippo |
| YAP (Yes-associated protein) | Protein liên kết Yes (YAP) |
| TAZ (WWTR1) | Đồng hoạt hóa phiên mã với motif PDZ (TAZ) |
| TEAD transcription factor | Yếu tố phiên mã TEAD |
| MST1/2 kinase | Kinase MST1/2 |
| LATS1/2 kinase | Kinase LATS1/2 |
| organ size control | Kiểm soát kích thước cơ quan |
| mechanotransduction | Cảm biến cơ học |
| revival stem cell (revSC) | Tế bào gốc hồi sinh |
| intestinal stem cell (ISC) | Tế bào gốc ruột |
| tissue regeneration | Tái tạo mô |
| contact inhibition | Ức chế tiếp xúc |
| fetal reprogramming | Tái lập trình bào thai |

## Tested PubMed Queries (for reuse)

```python
# Multi-round search strategy
queries = [
    # Round 1: Core pathway + intestine
    'Hippo+signaling+pathway+swine+pig+intestinal',
    'YAP+pig+intestine+swine',
    'Hippo+pathway+intestinal+epithelial+regeneration',
    
    # Round 2: Mechanism + stem cell
    'YAP+TAZ+intestinal+stem+cell+homeostasis',
    'YAP+TAZ+mechanotransduction+intestine',
    'YAP+intestinal+barrier+function',
    
    # Round 3: Virus + immunity
    'Hippo+YAP+viral+infection+innate+immunity',
    
    # Round 4: Nutrition + feed additives
    'YAP+TAZ+butyrate+short+chain+fatty+acid',
    'Hippo+YAP+TAZ+feed+additive+nutrition',
]
```

## Bash Variable Scope Note for PubMed Batch Queries

When iterating PMIDs in a `for` loop with inline `python -c`:

```bash
# ✗ FAILS — bash $pmid not expanded inside single-quoted -c
for pmid in 123 456; do
  python -c '
import re
match = re.search(rf"<PMID>{pmid}</PMID>", xml)  # NameError
'
done

# ✓ FIX — write a standalone .py file (Pattern D)
write_file(path="script.py", content='''
import sys, re
for pmid in sys.argv[1:]:
    match = re.search(rf"<PMID>{pmid}</PMID>", xml)
    print(match)
''')
terminal(command='python script.py 123 456')
```
