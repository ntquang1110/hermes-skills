# Heavy Metals Remediation — Domain Knowledge Reference

> As, Pb, Hg, Cd removal from soil. Captured from a research session focused on peat (than bùn) for animal feed and fertilizer applications. Dry + wet + hybrid methods; cost analysis; equipment specs; quality standards.

## 1. Four Target Metals — Quick Reference

| Metal | Density (g/cm³) | Vapor/decomp (°C) | Key mineral | Best dry method | Best wet method |
|-------|----------------|--------------------|-------------|-----------------|-----------------|
| **As** | 5.73 | 193 (As₂O₃ sublimes) | FeAsS (arsenopyrite), As₂S₃ | O₃ oxidize → H₂O₂/FeCl₃ | 
| **Pb** | 11.34 (galena 7.4) | 1749 (non-volatile) | PbS (galena), PbCO₃ | Gravity (density 7.4) | Phosphate ppt at pH 7 |
| **Hg** | 13.53 (cinnabar 8.1) | **357** (volatile) | HgS (cinnabar) | **Thermal >400°C >95%** | KI/I₂ complex, Na₂S |
| **Cd** | 8.65 (greenockite 4.8) | 767 (needs high heat) | CdS, CdCO₃ | Biochar-magnetic | Ca(OH)₂ pH ≥8.5 |

## 2. Critical Protocol Design Lessons

### 🔴 Peat vs Inorganic Soil — Never Confuse Them

| Property | Inorganic soil (cát, sét) | Peat (than bùn) |
|----------|--------------------------|-----------------|
| Organic matter | <5% | **30-60%** |
| Humic acid value | None | **Primary value driver** |
| Thermal tolerance | Can handle 450°C | **Destroys OM above 200°C** |
| Iron form | Fe-oxides (magnetic separable) | Fe-humic complexes (non-magnetic) |
| Separation behavior | Particles >100µm common | **Grinds to <50µm easily** |

**Cardinal rule for peat:** Never design a process that exceeds 100°C unless you've confirmed the user doesn't need OM/HA/FA. For animal feed grade, HA≥15% is a hard requirement.

### 🔴 Mechanochemical + Sulfur — Not Ready for Practice

- Sulfur autoignition ~190°C; ball mill impacts create localized temperatures >200°C → **explosion risk**
- Sulfide particles formed are sub-micron → **cannot be separated by air table**
- Most literature uses 2-4h milling in Ar atmosphere, not 30 min in air
- Residual S burns to SO₂ at any subsequent thermal step

**If mechanochemical is essential:** Use CaO instead of S (no explosion risk), or Fe⁰ powder (creates separable Fe-KLN alloy, though also not cheap).

### 🔴 Cost Estimation Rule

First-pass operation cost × **3 minimum** for realistic estimate. Sources of the multiplier:

| Factor | Multiplier |
|--------|-----------|
| Energy (real efficiency vs ideal) | 1.3-1.5× |
| Waste treatment (often omitted) | 1.2-2× |
| Labor + overhead (often omitted) | 1.5-2× |
| Equipment depreciation (often omitted) | 1.2-1.5× |
| QC testing + rework (always omitted) | 1.2-1.5× |
| **Typical cumulative** | **3-5×** |

### Equipment Cost Reality Check

| Item | "Self-built" price | Industrial equivalent | Delta |
|------|-------------------|----------------------|-------|
| Ball mill | 1.5M VND (DIY motor+can) | 20-30M (VND, 5kg) | 15-20× |
| Furnace 600°C | 2.5M (5L, mini) | 30-80M (50L lab) / 500M-2B (rotary kiln, 1t/d) | 10-800× |
| Air table | 5-15M (DIY sieve+fan) | 50-200M (industrial) | 10-40× |

## 3. Recommended Protocol: Mild Wet Wash for Peat

For peat to be used in animal feed or organic fertilizer, the following protocol keeps OM/HA/FA intact:

| Step | Method | Temp | Time | Removes |
|------|--------|------|------|---------|
| 1 | Dry 60°C (not 105°C — Hg loss) | 60°C | 4-8h | — |
| 2 | Sieve 2mm (remove gravel, debris) | RT | 30min | — |
| 3 | Citric acid 0.05M pH~3 wash (1:3 w/v) | RT | 1h | Pb 50-70%, Cd 60-80% |
| 4 | FeCl₃ 0.1% + NaOH to pH 5 | RT | 1h | As >90% (must oxidize AsIII first) |
| 5 | Biochar 5% slurry, contact 4h | RT | 4h | Hg 70-85%, Cd 70-85% |
| 6 | Vacuum filter → dry 60°C | 60°C | 4h | — |

**Wastewater:** Contains citric acid, Fe, and trace KLN. Treat with Na₂S (sulfide ppt) before discharge.

**Budget:** Lab startup ~10-15M VND. Pilot (100kg/day) ~50-100M VND. Operating ~1.5-3M VND/ton.

## 4. Quality Standards Reference (Vietnam)

### QCVN 01-190:2020/BNNPTNT — Animal Feed (TĂCN)

| Metal | Limit (ppm) |
|-------|------------|
| As | ≤ 2 |
| Pb | ≤ 5 |
| Hg | ≤ 0.1 |
| Cd | ≤ 0.5 |
| Cr(VI) | ≤ 1 |

### QCVN 01-189:2019/BNNPTNT — Organic Fertilizer

| Metal | Limit (ppm) |
|-------|------------|
| As | ≤ 10 |
| Pb | ≤ 50 |
| Hg | ≤ 1 |
| Cd | ≤ 2 |
| Cr(VI) | ≤ 5 |

### Peat Quality Index (Key for commercial value)

| Parameter | Good | Marginal | Poor |
|-----------|------|----------|------|
| Humic acid (HA) | ≥15% | 8-15% | <8% |
| HA/FA ratio | 2-5 | 1-2 or 5-8 | <1 or >8 |
| Organic matter | ≥30% | 22-30% | <22% |
| CEC (meq/100g) | ≥30 | 20-30 | <20 |

## 5. Testing Labs in Vietnam

| Lab | Location | Service |
|-----|----------|---------|
| Viện Thổ nhưỡng Nông hóa | Hà Nội | Full soil + fertilizer |
| QUATEST 1, 2, 3 | HN, ĐN, HCM | Certified QA |
| ĐH Cần Thơ — Viện CNSH&MT | Cần Thơ | Research + analysis |
| SGS Vietnam | HN, HCM | International standard |
| Bureau Veritas | HN, HCM | International standard |

Full panel (KLN 8 metals + nutrition 17 parameters + microbiology 7 tests): **~5-10M VND/sample**.
