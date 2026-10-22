# Heavy Metals in Soil — Protocols & Reference Bank

## The domain
As (arsenic), Pb (lead), Hg (mercury), Cd (cadmium) in soil.  
**Core constraint:** These metals cannot be destroyed — only separated (dry) or precipitated (wet).

## Quick reference: 4 metals

| Metal | Density | Boil point | Magnetic | Best dry method | Best wet method | Notes |
|-------|---------|-----------|----------|----------------|----------------|-------|
| As | 5.73 | 193°C (subl.) | Weak in FeAsS | Heat 450°C + O₃ pre-oxidize | FeCl₃ pH 5 coprecipitation | As(III) must be oxidized to As(V) first — critical |
| Pb | 11.34 | 1749°C | None (PbS) | Gravity (PbS=7.4) + biochar magnet | Phosphate / Ca(OH)₂ pH 8.5 | Anglesit (PbSO₄) hard — not magnetic, doesn't boil |
| Hg | 13.53 | 357°C | None | Thermal 450°C >95% removal | KI/I₂ complex → HgI₄²⁻ | Hg⁰ element won't precipitate — needs adsorption or amalgamation |
| Cd | 8.65 | 767°C | None | Biochar magnetic + milling with S | Ca(OH)₂ pH ≥8.5 (critical) | Cd(OH)₂ only precipitates at pH ≥8.5 — at pH 7-8, 30-50% stays dissolved |

## Protocol design: dry-only approach

When the user says "giữ nguyên khoáng quý", "xử lý khô", "không hòa tan":
→ **Physical separation only** — gravity (air table), magnetic, thermal volatilization, biochar adsorption
→ No acid, no water, no dissolution

### Dry flowsheet (verified)

```
Input: raw soil (solid, fine, <2mm)
  1. Dry at 105°C → <1% moisture
  2. Sieve 2mm → reject gravel. Sieve 63μm → fines (KLN-concentrated) separate
  3. Mechanochemical grind + S 2% (30 min ball mill) → convert KLN to sulfides
  4. Air table (fan + vibrating screen) → split by density. Heavy fraction (KLN sulfides) → reject
  5. High magnetic (0.5-2T) → remove Fe-oxides carrying As/Pb/Cd
  6. Magnetic biochar 3% → adsorb Pb+Cd → separate magnetically
  7. Thermal 450°C → Hg >95% vaporizes, As 50-80% vaporizes
Output: clean soil + preserved minerals, dry, fine, solid
```

### Hybrid A (recommended for most cases)
Same as above but with a light citric acid rinse (pH 4) at the end for Cd polishing. Uses ~20% of wet chemistry.

## Wet approach (when dry isn't enough)

| Step | Reagent | Removes | Note |
|------|---------|---------|------|
| 1. Oxidize | H₂O₂ 2% | As(III)→As(V) | Mandatory — As(III) won't precipitate |
| 2. Fe coprecipitation | FeCl₃ pH 4.5-5.5 | As | Fe:As = 30:1 |
| 3. Sulfide | Na₂S 0.1% pH 4-6 | ALL 4 | Single step catches all but H₂S is toxic — use fume hood |
| 4. Lime | Ca(OH)₂ pH 8.5 | Pb, Cd, Hg | Cd needs pH ≥8.5 |
| 5. Polish | Biochar/zeolite column | Traces ppb | Final safety step |

## Lab setup (minimum, ~23M VNĐ)

| Category | Items | Cost (VNĐ) |
|----------|-------|-----------|
| Equipment | Balance, sieves (2mm/1mm/63μm), mortar, ball mill DIY, pH meter, stirrer, drying oven, furnace 600°C, vacuum filter, air table DIY, magnets N52 | 15.1M |
| Glassware | Beakers 250-1000mL, graduated cylinders, funnels, tubing, filter paper Whatman #1 & #42 | 2.6M |
| Chemicals | HCl, H₂SO₄, H₂O₂, FeCl₃, Ca(OH)₂, CaCO₃, S⁰, KI, I₂, Na₂S, citric acid | 0.7M |
| Safety | Goggles, nitrile gloves, heat gloves, N95 mask, multi-gas respirator, lab coat, CO₂ fire extinguisher, first aid kit, eyewash station, DIY fume hood | 2.1M |
| Test kits | As (Merckoquant), Pb, Cd (dithizone), Hg (CHEMetrics), pH paper, Pb-acetate paper | 2.4M |

**Key safety hazards:** H₂S from Na₂S+acid (toxic gas, use respirator + outdoor/ fume hood), I₂ vapor (toxic), 450°C furnace (burns), acid spills (eye wash nearby).

## Decision guide

| Condition | Recommend |
|-----------|-----------|
| KLN as separate mineral grains | Dry gravity + magnetic — cheap, simple |
| KLN adsorbed on clay/organic | Mechanochemical S grind → convert to sulfide, then gravity |
| Mainly Hg + As | Thermal 450°C — one step removes both |
| Mainly Pb + Cd | Magnetic biochar 3% + gravity |
| All 4, high conc. | Full hybrid A sequence |
| Must preserve ALL minerals | Dry-only (hybrid C) — no chemicals at all |
| Must pass strict standards | Hybrid B (wet with controlled acid) — highest removal |
| Minimal budget | Gravity table only + heat if Hg present → ~300-500K/tấn |
| As(III) dominant | Pre-treat with O₃ or H₂O₂ BEFORE any step |

## Cost per ton

| Method | Cost (VNĐ/tấn) | Notes |
|--------|---------------|-------|
| Dry gravity only | ~100-200K | DIY device, no chem |
| Full dry (gravity + magnetic + thermal) | ~1.2-1.8M | All physical |
| Hybrid A (dry + light wet polish) | ~1.5-2.0M | Recommended |
| Hybrid B (wet with full acid) | ~2.0-3.0M | Highest removal |
| Mechanochemical S only | ~300K | One-step conversion |

## Standards reference (QCVN 03:2023/BTNMT — agricultural soil)

| Metal | Limit (ppm) |
|-------|------------|
| As | ≤ 15 |
| Pb | ≤ 70 |
| Hg | ≤ 1 |
| Cd | ≤ 2 |

## History of protocol evolution
This session went through **3 major iterations** as user clarified constraints:
1. ❌ Wet acid extraction (dissolved soil → lost all minerals) — user rejected
2. ❌ Soil washing (kept solid but used water + chemicals) — user rejected
3. ✅ Dry-only physical separation (preserved everything) — final approval
→ **Always confirm the "giữ nguyên khoáng quý" constraint first.**

## Reference papers used
- Smedley & Kinniburgh, As in groundwater, *Appl. Geochem.* 17:517 (2002)
- Mohan & Pittman, As removal review, *J. Hazard. Mater.* 142:1 (2007)
- Clarkson & Magos, Toxicology of mercury, *Crit. Rev. Toxicol.* 36:609 (2006)
- Bolan et al., Remediation of Cd-contaminated soils, *Adv. Agron.* 141:183 (2017)
- Kumpiene et al., Stabilization of As/Cu/Pb/Cr in soil, *Crit. Rev. Environ. Sci.* 38:123 (2008)
