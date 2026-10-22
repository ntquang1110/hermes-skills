---
name: heavy-metal-soil-remediation
description: "Remove As, Pb, Hg, Cd from soil while preserving mineral content — dry physical separation (density, magnetic, thermal, mechanochemical, biochar-magnetic) + wet chemical + hybrid approaches. Covers lab setup, cost estimation, and purchase workflows."
tags: [soil, heavy-metals, arsenic, lead, mercury, cadmium, dry-treatment, remediation, lab-setup]
---

# Heavy Metal Soil Remediation — Dry + Wet + Hybrid

## Trigger

Use this skill when the user asks to:
- Remove arsenic (As), lead (Pb), mercury (Hg), or cadmium (Cd) from soil
- Treat contaminated soil while preserving valuable minerals
- Set up a lab for heavy metal testing/treatment
- Estimate costs, equipment, or purchase orders for a soil remediation lab
- Compare dry vs wet treatment methods
- Research **electrokinetic remediation (EKR)** for heavy metal removal
- Look up **patents** related to soil heavy metal remediation
- Design a treatment process using electric fields, soil washing, bioremediation, phytoremediation, chemical immobilisation, or thermal desorption

## Core Principle

**Dry methods FIRST. Wet methods only if needed.**

Why: Wet chemical treatment (acid washing, sulfide precipitation) dissolves or alters valuable minerals in the soil. Dry physical separation (density, magnetic, thermal, mechanochemical) removes heavy metals while keeping every mineral grain intact.

The user's constraint is: soil must stay **solid, fine, and dry** after treatment — ready for the next processing step.

## Heavy Metal Quick Reference

| Metal | Density (g/cm³) | Boiling point | Best dry method | Best wet method | Gotcha |
|---|---|---|---|---|---|
| **As (Arsenic)** | 5.7 (FeAsS: 6.0) | 193°C (As₂O₃ sublimes) | Thermal 450°C + high magnetic | H₂O₂ + FeCl₃ pH 5 | As(III) much harder than As(V) — must oxidise first |
| **Pb (Lead)** | 11.3 (galena PbS: 7.4) | 1749°C | Gravity separator (air table) + biochar-magnetic | Ca(OH)₂ pH 8.5 + phosphate | PbSO₄ (anglesite) hard to treat — not magnetic, high density only if separate grains |
| **Hg (Mercury)** | 13.5 (cinnabar HgS: 8.1) | **357°C** | **Thermal 400-500°C: >95% removal** | KI/I₂ complexation or Na₂S | Hg⁰ elemental mercury doesn't precipitate — only volatilises or complexes |
| **Cd (Cadmium)** | 8.7 (CdS: 4.8) | 767°C | Biochar-magnetic + mechanochemical S | Ca(OH)₂ pH ≥8.5 (Cd(OH)₂↓) | **Hardest to remove dry** — density not high enough, non-magnetic, won't volatilise below 700°C |

## Six Dry Methods (Priority Order)

### 1. Size classification (mandatory first step)
Dry sieve at 2mm (discard gravel) and 63μm (separate fines). Heavy metals concentrate in the <63μm fraction. Removing this cuts load by 20-50%.

### 2. Gravity separation (air table / fan + vibrating sieve)
Uses density difference: heavy metal minerals (4.5-8.2 g/cm³) vs soil matrix (2.0-2.8 g/cm³). DIY construction: vibrating sieve + 1HP axial fan + 3 collection hoppers. Heavy fraction (metal minerals) falls near, light fraction (clean soil) blows far. Cost: ~100-200K VND/tonne.

### 3. High-gradient magnetic separation
Hematite/goethite (Fe-oxides) that adsorb As, Pb, Cd are paramagnetic. Use N52 rare-earth magnets or high-intensity magnetic separator (0.5-2T). Removes 30-60% As, 20-40% Pb, 20-40% Cd. Arsenopyrite (FeAsS) is also magnetic.

### 4. Mechanochemical treatment (ball milling with additives)
**Key method for treating all 4 metals in one step.** Add 2-5% sulfur powder (S⁰) + 1% iron powder (Fe⁰) to dry soil, ball mill 30-60 min at 200-400 rpm. Mechanical impact causes solid-state reactions:
- S + metals → metal sulfides (high density, easy to gravity-separate)
- Fe⁰ + As/Pb → reduction to less mobile forms
Cost: ~300K VND/tonne. Equipment: DIY ball mill (motor + 2L drum + ceramic balls, ~1.5M VND).

### 5. Biochar-magnetic adsorption
Produce magnetic biochar by pyrolysing rice husk/coffee husk + FeCl₃ 5% at 500°C → Fe₃O₄-biochar composite. Mix 3% w/w with dry soil for 15-30 min, then remove with magnet. Pb: 80-90%, Cd: 70-85%, Hg: 60-80%, As: 50-70%. Cost: ~150-300K VND/tonne. Biochar can be regenerated with citric acid pH 3 (3-5 cycles).

### 6. Thermal desorption (furnace/kiln 450-550°C)
**Essential for Hg (>95% removal).** Also removes 50-80% As. Pb and Cd stay in soil. Requires exhaust gas treatment (activated carbon or condenser to capture Hg⁰ + As₂O₃ vapour). Caution: temperatures >300°C burn organic matter; >500°C decomposes CaCO₃. Cost: ~500K VND/tonne.

## Hybrid Routes (When Dry Alone Isn't Enough)

| Route | Approach | All 4 metals | Cost/tonne | Minerals preserved |
|---|---|---|---|---|
| **Hybrid A (recommended)** | Dry: sieve → mechanochemical S → gravity → magnetic → biochar-magnetic → thermal | 85-95% | ~1.5-2.0M VND | >90% |
| **Hybrid B** | Wet: acid wash → FeCl₃ → Na₂S low dose → Ca(OH)₂ | 85-95% | ~2.0-3.0M VND | ~70-80% |
| **Hybrid C (pure dry)** | All dry methods only, no acid | 80-90% | ~1.2-1.8M VND | >95% |

## Lab Setup & Purchase Workflow

- Total initial investment (55 items): **~20-25M VND** (basic lab)
- Key items: analytical balance, sieves, pH meter, ball mill, stirrer/hotplate, vacuum filter, drying oven, 600°C furnace, DIY air table, N52 magnets, PPE, chemical test kits (As/Pb/Cd/Hg)
- Chemical stock: HCl, H₂SO₄, NaOH, H₂O₂, FeCl₃, Ca(OH)₂, CaCO₃, S⁰, KI, I₂, Na₂S, citric acid
- **For in-house QC:** See `references/analysis-equipment-guide.md` for equipment options (Hach DR1900, XRF, electrochemical analyzers), pricing, and payback analysis vs external lab testing
- **Critical safety**: Na₂S + acid → H₂S gas (lethal). MUST use respirator + fume hood/outdoors.

## ⚠️ CRITICAL: Mineral soil vs Organic soil (Peat/Than bùn)

**The existing protocols in this skill were designed for MINERAL SOIL (sand, clay, laterite). PEAT SOIL (than bùn) has fundamentally different properties that require a COMPLETELY different approach.**

### Why peat is different

| Property | Mineral soil | Peat/Than bùn |
|---|---|---|
| Organic matter (OM) | <5% | **30-60%** |
| Humic acid (HA) | negligible | **12-25%** — this is the VALUABLE product |
| Fe form | Fe-oxides (hematite, magnetite) | Fe-organic complexes (non-magnetic) |
| Saponin | absent | **Present** — heat/acid sensitive |
| Thermal behaviour | Min. soil survives 450°C | **OM/HA/FA burn at >200°C** |

### DON'Ts for peat (mistakes from earlier protocol that were caught by critical review)

| Method | Why it FAILS for peat |
|---|---|
| **Thermal 450°C** ❌ | Destroys 100% OM, HA, FA — **product becomes worthless** |
| **Mechanochemical S** ❌ | Fire risk (S ignites at ~190°C, ball milling creates hot spots). Sulfide particles sub-micron → can't gravity-separate. Creates SO₂ in subsequent steps |
| **Air table gravity** ❌ | Only works for particles >100 μm. Post-milling particles <50 μm |
| **Magnetic separation** ❌| Fe in peat is Fe-organic complexes (non-magnetic), not Fe-oxides |
| **Dry biochar mixing** ❌| Biochar adsorbs metals poorly in dry environment. Needs liquid phase + hours |
| **Drying at 105°C** ❌ | Hg starts volatilising at 50-60°C in humid air. Use **60°C max** |

### DOs for peat — Modified Hybrid Protocol (verified by 2 rounds of critical review)

**Core constraint: max 60°C, pH 4-8, no strong acids/bases, preserve OM/HA/FA/saponin/Ca/K/Na.**

```
B1. Sấy 60°C (Hg safe, HA preserved) → 6-12h
B2. Sàng 2mm → discard coarse
B3. Rửa acid citric 0.05M pH ~3, 1:3 w/v, 60 ph → removes Pb (50-70%), Cd (60-80%)
B4. H₂O₂ (oxy hóa AsIII→AsV) + FeCl₃ pH 5, 30 ph → removes As (>90%)
B5. Biochar 5% w/w, khuấy 4h trong pha lỏng → removes Hg (70-85%), Cd (70-85%), Pb dư
B6. Lọc → sấy 60°C → đóng gói
```

| Metal | Expected removal | Method |
|---|---|---|
| As | >90% | H₂O₂ + FeCl₃ pH 5 (not biochar — biochar can't adsorb As!) |
| Pb | 70-85% | Citric acid wash + biochar polishing |
| Hg | 70-85% | Biochar (use S-impregnated if Hg >5 ppm) |
| Cd | 75-85% | Citric acid wash + biochar polishing |

**Cost: ~1.5-3M VND/tonne (lab scale). Equipment: ~7-13M VND (standard lab, not DIY).**

### Peat quality control indicators (33 metrics)

See `references/peat-quality-standards.md` for the full table, but critical thresholds:

| Parameter | Feed use | Fertilizer use | Method |
|---|---|---|---|
| As | ≤2 ppm | ≤10 ppm | ICP-MS |
| Pb | ≤5 ppm | ≤50 ppm | ICP-MS |
| Hg | ≤0.1 ppm | ≤1 ppm | Hg analyzer |
| Cd | ≤0.5 ppm | ≤2 ppm | ICP-MS |
| Humic acid (HA) | ≥15% | ≥12% | TCVN 8569:2010 |
| OM | ≥30% | ≥22% | Walkley-Black |
| Salmonella | KPH/25g | KPH | TCVN 4829:2005 |

**Regulatory ref:** QCVN 01-190:2020/BNNPTNT (feed), QCVN 01-189:2019/BNNPTNT (fertilizer), QCVN 03:2023/BTNMT (soil).

## Pitfalls
2. **As(III) must be oxidised to As(V)** before any treatment — As(III) (H₃AsO₃) is neutral, doesn't adsorb on Fe(OH)₃, doesn't ion-exchange. Use H₂O₂ or O₃.
3. **Hg⁰ doesn't precipitate** — it's liquid metal. Only thermal (vapour capture) or KI/I₂ complexation works.
4. **htmlpreview.github.io may be blocked in Vietnam** — fall back to raw Gist URL or send file directly via MEDIA: path.
5. **Google multi-account**: Token files stored at `~/AppData/Local/hermes/google_token_*.json`. Switch by copying the target token to `google_token.json`. Always backup first.
6. **Dry methods fail when heavy metals are chemically adsorbed in clay lattice** — only wet acid leaching can reach those. Always test 100-500g sample first.

## Verification

- **DIY / onsite:** Hach DR1900 portable spectrophotometer + reagent kits (~40-47M VND investment, see `references/analysis-equipment-guide.md`)
- **Test kits:** As (Merckoquant 0.005-0.5 ppm), Pb (dithizone), Cd (dithizone), Hg (CHEMetrics K-9012)
- **Definitive analysis:** ICP-MS / AAS (~200-800K VND/sample at external lab)
- QCVN 03:2023/BTNMT thresholds: As ≤15, Pb ≤70, Hg ≤1, Cd ≤2 ppm (agricultural soil)

## References

- `references/analysis-equipment-guide.md` — analytical equipment comparison (Hach DR1900, XRF, electrochemical), pricing, payback analysis, and suppliers in Vietnam
- `references/dry-treatment-protocol.md` — full 7-step dry protocol with equipment setup, chemical recipes, and troubleshooting
- `references/peat-quality-standards.md` — full peat quality standards table (33 metrics, regulatory thresholds)
- `references/electrokinetic-remediation.md` — EKR theory, mechanisms, critical problems (polarisation, precipitation, mineral loss), key patents and literature
- `references/soil-remediation-patents.md` — 25+ key patents across 6 method families with effectiveness data and country of origin
