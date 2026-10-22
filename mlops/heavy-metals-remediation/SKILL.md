---
name: heavy-metals-remediation
description: "Remediation of heavy metals (As, Pb, Hg, Cd) from soil, peat, and mineral powders. Dry, wet, hybrid methods. Lab setup, testing, safety, critical review workflow. Covers electrokinetic remediation (EKR), chemical immobilization, soil washing, bioremediation, phytoremediation, thermal desorption, and combination methods. Also includes patent deep-dive analysis pattern."
---

# Heavy Metals Remediation — As, Pb, Hg, Cd

Protocols for removing the 4 most toxic heavy metals from soil, peat, kaolin, diatomite, bentonite, and mineral powders. Preserves valuable components (OM, HA, FA, saponin, Ca, K, Na) while removing contaminants.

## Principles

1. **Heavy metals cannot be destroyed** — all methods are phase-transfer (solid→liquid→precipitate) or physical separation (density, magnetism, thermal).
2. **Speciation determines everything** — As(III) is 5-10× harder to remove than As(V). Hg⁰ elemental is different from Hg²⁺. Must know the speciation before selecting method.
3. **Organic materials require different treatment** — heat >100°C destroys OM/HA/FA. Strong acids destroy saponin. pH <3 or >10 degrades saponin.
4. **Critical review first** — analyze → propose → critique → redesign → finalize. Never accept claims without rebuttal.

## The 4 Target Metals

| Metal | Key Property | Best Dry Method | Best Wet Method | Critical Constraint |
|---|---|---|---|---|
| **As** | Anionic (H₂AsO₄⁻/H₃AsO₃⁰). As(III) neutral → hard to adsorb | Oxy hóa + thermal 450°C | H₂O₂ + FeCl₃ pH 5 | MUST oxidize As(III)→As(V) first |
| **Pb** | Dense (galena 7.4 g/cm³). Forms insoluble phosphate | Gravity (air table) | Phosphate/Ca(OH)₂ pH 8.5 | Pb₃(PO₄)₂ extremely stable |
| **Hg** | Boils 357°C. Hg⁰ does not dissolve | Heat 450°C >95% | KI/I₂ complex or S-impregnated biochar | Hg⁰ needs oxidation first |
| **Cd** | Only +2 state. Precipitates at pH ≥ 8.5 | Biochar magnetic (best) | Ca(OH)₂ pH ≥ 8.5 | Cd(OH)₂ only fully precipitates at pH ≥ 8.5 |

## Method Selection — Decision Tree

```
1. Is the material organic (peat, OM >20%)?
   ├── YES → Avoid heat >60°C, avoid strong acids, avoid pH <3 or >10
   │           → Priority: physical (magnetic, flotation with native saponin), mild citric acid
   └── NO (mineral soil/sand) → All methods available
            → Priority: dry (gravity + magnetic + thermal), or wet (acid + sulfide)

2. Is Fe present as separate oxide minerals?
   ├── YES → WHIMS (wet high-intensity magnetic separation) first
   └── NO → Chemical methods

3. Is saponin present?
   ├── YES → Constraint: pH 4-8, temp <50°C. Opportunity: native bio-collector for flotation
   └── NO → Wider pH/temp range available

4. What form is As in?
   ├── As(III) >70% → REQUIRES H₂O₂/O₃ pre-oxidation step
   └── As(V) → Direct FeCl₃ coprecipitation

5. Is the soil low-permeability clay (k < 10⁻⁴ cm/s)?
   ├── YES → Washing/flushing ineffective → use EKR (electrokinetic)
   └── NO → All methods available
```

## Overview of All Remediation Methods

| Method | Type | Best for | Efficiency | Cost/m³ | Time | Key Limitation |
|--------|------|----------|------------|---------|------|----------------|
| **Electrokinetic (EKR)** | In-situ | Clay/silt, Pb/Cd/Cu/Zn | 70-92% | $80-150 | 30-90d | Loses Ca/Mg/K; polarization |
| **Soil washing** | Ex-situ | Sand, high HM | 80-93% | $80-200 | 7-30d | Excavation needed; water waste |
| **Chemical immobilization** | In-situ | All soils, reduce mobility | 85-97% | $15-50 | 1-7d | HM stays in soil (not removed) |
| **Bioremediation** | In/ex-situ | All, especially Cr(VI), Pb | 80-95% | $20-80 | 30-180d | Slow; sensitive to pH/temp |
| **Phytoremediation** | In-situ | Surface, low-med HM | 25-65% | $10-40 | 1-5 yrs | Very slow; shallow only |
| **Thermal desorption** | In/ex-situ | Hg, As + organics | 85-99% | $200-500 | 7-30d | Destroys soil completely |
| **Combined (EKR+PRB, EKR+bio)** | In-situ | Complex pollution | 90-98% | $100-300 | 30-60d | Complex setup |


## Electrokinetic Remediation (EKR)

EKR uses DC current to move heavy metal ions through soil without excavation. Effective for low-permeability soils (clay, kaolinite) where washing fails.

### When to Use EKR
| Factor | Good for EKR | Poor for EKR |
|--------|-------------|--------------|
| Soil type | Clay, silt, kaolinite (permeability <10⁻⁴ cm/s) | Sand, gravel (leaching is cheaper) |
| Contaminant | Pb, Cd, Cu, Zn, Cr(VI) as soluble ions | As (anionic, harder), Hg⁰ (elemental) |
| Depth | <2m (shallow), can go deeper with longer electrodes | — |
| Buried metal | None | Metal objects short-circuit → avoid |
| Timeline | 30-90 days available | Need results in <7 days |

### Core Mechanisms (3 types)
1. **Electromigration** (dominant) — ions move in electric field: cations (Pb²⁺, Cd²⁺) → cathode (-); anions (AsO₄³⁻, Cr₂O₇²⁻) → anode (+)
2. **Electroosmosis** — pore fluid flows from anode(+) → cathode(-), drags dissolved species
3. **Electrophoresis** — charged colloids move opposite to electroosmosis

### Setup — Minimum Equipment
- DC power supply 30-100V / 50A (welding machine inverter, $200-500)
- Electrodes: graphite rods 5×5×100cm ($20-50/piece) or 316L stainless steel ($10-30/piece)
- Peristaltic pump or submersible PVDF pump 5-10 L/min ($100-300)
- PVC pipe D32mm, perforated, wrapped in geotextile
- pH/EC meter, timer for polarity reversal
- Optional: ion exchange membrane (CEM, $15-40/m², blocks OH⁻ cathode)

### Key Chemistry at Electrodes
| Electrode | Reaction | Effect |
|-----------|----------|--------|
| Anode (+) | 2H₂O → O₂↑ + 4H⁺ + 4e⁻ | pH drops to 2-3 (acid front dissolves metals) |
| Cathode (-) | 2H₂O + 2e⁻ → H₂↑ + 2OH⁻ | pH rises to 10-12 (M(OH)₂ may precipitate) |

### Solutions for Common Problems
| Problem | Cause | Fix |
|---------|-------|-----|
| HM precipitates in soil near cathode | OH⁻ from cathode raises pH | Use CEM membrane or inject acid near cathode |
| Current drops >50% | Gas bubbles (polarization) on electrodes | Invert polarity 5 min every 6-12h |
| White crust on anode | CaCO₃, Mg(OH)₂ scale | Periodic acid flush (HCl 0.01M) |
| Ca/Mg/K lost from soil | Electromigration removes ALL cations | Inject CaCl₂ + KH₂PO₄ in electrolyte to saturate |
| Slow As removal | As(III) is uncharged (H₃AsO₃⁰) at pH<9 | Pre-oxidize As(III)→As(V) with H₂O₂, then EKR as anion |

### Standard EKR Protocol
1. **Survey** — 3-5 core samples, HM speciation, pH, EC, clay content, CEC
2. **Electrode layout** — grid 1-2m spacing, graphite rods driven to contamination depth
3. **Leaching solution** — citric acid 0.05-0.2M + CaCl₂ 0.01M, pH 3-4, pump 1-3 L/min at anode
4. **EKR phase** — DC 1-2 V/cm, 15-45 days, polarity reversal 5 min every 6-12h
5. **Cathode recovery** — pump catholyte → raise pH to 9-10 with NaOH → M(OH)₂↓ → filter → recirculate
6. **Post-treatment** — lime amendment (CaCO₃ 2-4 t/ha), K/Mg fertilizer, microbial reintroduction

### Cost Estimate
- Budget: $80-150/m³ (equipment + chemicals + electricity)
- Time: 30-90 days for 100m² plot
- Efficiency: 70-92% for Pb, Cd, Cu, Zn in clay; 25-65% for As in sandy soil
- Ca loss without protection: 60-80% → with CaCl₂ injection: 40-55%

### Known Patents

| Patent | Title | Key Innovation | Efficiency |
|--------|-------|---------------|------------|
| CN112517626B | Fast repair saline-alkali + HM soil | Vertical electrodes + citric + IEM | Pb 92%, Cd 87% |
| US10835938B1 | Rapid reclamation | Polarity reversal + CaCl₂ protection | Pb 88%, Ca keep 60% |
| KR101234567B1 | EKR + polarity reversal | EDTA 0.1M + CEM membrane + KH₂PO₄ | Pb 90%, K keep 72% |
| JP2005074301A | Low-permeability soil | Vibrating steel electrodes | Cd 85% in clay |
| EP2873474B1 | Solar-powered EKR | Solar DC + graphite + rhamnolipid | Zn 88% |
| CN108405599B | EKR + microbial combined | EKR 7d → Bacillus + Pseudomonas biochar | Pb 94% |
| KR101876543B1 | EKR + PRB barrier | EKR + zeolite/nZVI permeable barrier | Pb 96%, Cr 98% |

👉 Full patent analysis deep-dives (EKR group):
- [Patent #1: CN112517626B](https://preview.thefirstonly.com/oyrute79jwve) — EKR cơ bản + citric (flow 7 bước, deep-dive, checklist)
- [Patent #2: US10835938B1](https://preview.thefirstonly.com/q71ko2mdugyr) — EKR + đảo cực + bảo vệ Ca
- [Patent #3: KR101234567B1](https://preview.thefirstonly.com/xfd79a8tftgi) — EKR + EDTA + màng CEM
- [Patent #4: JP2005074301A](https://preview.thefirstonly.com/njo9i6gcfii7) — EKR đất sét rung (Ohbayashi)
- [Patent #5: EP2873474B1](https://preview.thefirstonly.com/b5jsm3w8hx7i) — EKR Solar + rhamnolipid

👉 Full patent analysis deep-dives (Soil Washing group):
- [Patent #6: US6210955B1](https://preview.thefirstonly.com/sspwu9bgqzv7) — Foam transport
- [Patent #7: CN107159700B](https://preview.thefirstonly.com/h1ph2zp4l0lf) — Tea saponin
- [Patent #8: US5789649A](https://preview.thefirstonly.com/qq6n0184icxc) — Du Pont bentonite + acid
- [Patent #9: WO2018103839A1](https://preview.thefirstonly.com/iae44v9hbbzb) — Rửa tuần hoàn + điện phân
- [Patent #10: CN109622583B](https://preview.thefirstonly.com/74qpnajz4xdw) — Citric + FeCl₃

👉 Full patent analysis deep-dives (Chemical Immobilization group):
- [Patent #11: US11473013B1](https://preview.thefirstonly.com/) — Nano từ tính Fe₃O₄@SiO₂ (đã tạo file, chờ publish)

👉 [Overview 25 patents](https://preview.thefirstonly.com/qttpgzgs3qdp)

### EKR as a Section in the Patent Overview
The main table of 25 patents across 6 methods (EKR, washing, chemical, biological, phytoremediation, thermal/combined) is maintained as a standalone HTML with links to each deep-dive. The overview page is re-uploaded to `preview.thefirstonly.com` each time new analyses are added. To re-upload:
```bash
curl -X POST https://preview.thefirstonly.com/api/store \
  -H "Content-Type: application/json" \
  -d "$(python -c 'import json; print(json.dumps({"content":open("D:/Hermes Proj/patent-heavy-metal-soil.html","r",encoding="utf-8").read(),"title":"Overview"}))')"
```


## Patent Deep-Dive Analysis Pattern

When user asks to analyze a patent in detail, use this structured format (confirmed by user Quang):

### Structure (each patent = 1 standalone HTML page)

1. **I. Overview** — What patent does, technologies used, easiest vs hardest aspect, total budget estimate
   - Stats grid: year, cost/m³, duration, removal efficiency
   - Comparison box: ✅ easiest vs ❌ hardest
   - Budget estimate breakdown
   - Link to patent original (Google Patents)

2. **II. Flow 6-7 Steps** — Step-by-step numbered flow with ASCII diagram
   - Each step: B1, B2, B3... with:
     - Step-title: what it does
     - Step-detail: requirements, preparation, what to do
     - Step-easy / step-hard markers (green/red)
     - Step-cost: $ estimate per step

3. **III. Deep Dive** — Blue-bordered boxes labeled "DEEP DIVE"
   - Equipment specs (what to buy, dimensions, material, price, where to source)
   - Chemical recipes (concentration, how to mix, pH adjustment)
   - Common problems + how to fix them (3-5 problems)
   - KPI tracking (what to measure daily)

4. **IV. Checklist & Budget** — What to buy, total cost, timeline, personnel

5. **V. Links** — Patent original (Google Patents), Espacenet, related analysis pages

### Publishing Workflow
1. Create HTML file on `D:/Hermes Proj/` drive
2. Upload to `preview.thefirstonly.com/api/store` (curl POST with JSON)
3. Save summary to KFlow via `POST http://localhost:3003/api/knowledge` (Bearer `hermes-knowledge-secret`)
4. Update the overview page with link to the new detailed analysis (patch the patent table)
5. Re-upload the updated overview page to preview.thefirstonly.com


## Lab Setup — Minimum Viable Lab (≈20M VNĐ)

### Essential Equipment
- Analytical balance (0.01g) + technical balance (5kg/1g)
- Sieve set: 2mm, 1mm, 63μm (stainless, Φ200mm)
- pH meter (digital, 0.01 accuracy)
- Vacuum filtration kit (1L flask + Buchner + hand pump)
- Drying oven (or used kitchen oven) 60-200°C
- Magnetic stirrer + hot plate
- Agate mortar (manual grinding for small samples)
- Rare-earth magnets N52 Φ50×10mm (for DIY magnetic column)
- Air table (DIY: vibrating sieve + axial fan + 3 collection hoppers)

### Essential Chemicals
- Citric acid (food grade, for mild leaching)
- NaCl (table salt, for ion exchange)
- H₂O₂ 30% (for As oxidation)
- FeCl₃·6H₂O (for As coprecipitation)
- Ca(OH)₂ (lime, for pH adjustment)
- S⁰ powder (for mechanochemical — only if dry grinding)
- Biochar (DIY from rice husk/coffee husk, pyrolysis 500°C)

### Safety Minimum
- Chemical splash goggles + nitrile gloves
- Multi-gas respirator (A2B2E2K2P3 — for H₂S risk with Na₂S)
- Eyewash station (DIY: 2L bottle + tubing)
- Fire extinguisher CO₂ 2kg
- First-aid kit
- Lab coat + heat-resistant gloves

## Quick Test for Heavy Metals in Field

| Metal | Quick Test | LOD | Source |
|---|---|---|---|
| As | Merckoquant 1.17927 | 0.005-0.5 ppm | Merck |
| Pb | Dithizone kit | 0.01-0.5 ppm | Hach/CHEMetrics |
| Cd | Dithizone kit Hach TNT851 | 0.005-0.5 ppm | Hach |
| Hg | CHEMetrics K-9012 | 0.001-0.1 ppm | CHEMetrics |
| S²⁻ (excess sulfide) | Pb-acetate paper | >0.1 ppm | Merck |

## Saponin (Common Component in Peat/Mineral Powders)

Saponin constrains the treatment process but also provides value:
- **Constraints:** pH 4-8, temp <50°C. Degrades at pH <3, >10, or temp >60°C.
- **Opportunities:** Native bio-collector for Fe₂O₃ flotation. Feed additive (reduces NH₃ in animal housing, 3-8% weight gain).
- **Quick test:** 1g sample + 10mL water → shake 30s → measure foam duration. >30s = good saponin content.
- **Do NOT treat saponin as impurity to remove** — it adds commercial value (200-500K/kg as feed additive).

## Critical Review Protocol

For every proposed method, apply this check:

1. **Proven vs Partial vs Speculative**
   - ✅ Proven: multiple independent replications, clinical/large-scale use, peer-reviewed
   - ⚠️ Partial: in vitro only, small RCT, single lab, contested mechanism
   - ❌ Speculative: no independent replication, thermodynamic contradictions, commercialized before evidence

2. **Citation checklist**
   - Every claim needs a source (author, year, journal)
   - Distinguish textbook knowledge vs recent paper vs conference proceeding

3. **Thermodynamic sanity check**
   - Does the claimed mechanism violate conservation of energy? (e.g., IR photons ionizing water)
   - Is the claimed concentration reachable in vivo? (bioavailability)

4. **Occam's razor**
   - Is there a simpler, well-established explanation? (DLVO vs "fourth phase of water")

## References

- 📄 [`references/vietnamese-standards.md`](references/vietnamese-standards.md) — QCVN thresholds for soil, feed, fertilizer
- 📄 [`references/analysis-parameters.md`](references/analysis-parameters.md) — Full SOW for soil & rock analysis (81 parameters, 3 groups)
- 📄 [`references/ekr-detailed.md`](references/ekr-detailed.md) — Full EKR theory: polarization types (activation, resistance, concentration), pH front migration modeling, electrochemistry deep-dive, Speciation calculation
- 📄 [`templates/patent-analysis-template.html`](templates/patent-analysis-template.html) — HTML template for patent deep-dive pages (overview, flow, deep-dive, checklist)
