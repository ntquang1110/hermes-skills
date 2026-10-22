# Dry Treatment Protocol — Heavy Metal Soil Remediation

## Standard Operating Procedure (7 Steps)

### Step 0: Characterisation (3-5 days)
**Send to lab:**
- XRD (mineral forms of As, Pb, Hg, Cd)
- ICP-MS (total concentration)
- Sequential extraction (BCR/Tessier — exchangeable vs carbonate vs Fe-oxide vs residual)
- Dry sieve distribution
- Magnetic separation test

**Decision gate:** If >60% of metals are in exchangeable/carbonate fractions → dry methods will work well. If >50% in residual (lattice-bound) → dry methods will struggle; consider wet or hybrid.

### Step 1: Drying (2-4h)
Dry soil at 105°C to <1% moisture. Critical: moisture interferes with dry separation (clumping, bridging, electrostatic effects). Use oven or repurposed kitchen oven.

### Step 2: Sieving (30min)
**Equipment:** Dry sieve set Φ200mm (2mm + 1mm + 63μm + lid + pan)

| Fraction | Treatment |
|---|---|
| >2mm (gravel) | Discard |
| 63μm-2mm | Main process stream |
| <63μm (silt/clay) | Heavy metals concentrated here. Treat separately with biochar-magnetic or cyclone cascade |

### Step 3: Mechanochemical Treatment (30-60min)
**Additives:** S⁰ powder 2-3% + Fe⁰ powder 1% (w/w of soil)
**Equipment:** Ball mill (DIY: motor 0.5HP + steel drum 2L + ceramic balls Φ10-20mm, 200-400 rpm)
**Process:** Mill 30-60 min. S reacts with all 4 metals → metal sulfides (high density, separable by gravity). Fe⁰ reduces As, Pb to less mobile forms.
**Safety:** Keep soil dry (<1% moisture). S + moisture at high temp can produce SO₂. Work outdoors or in fume hood.

### Step 4: Gravity Separation (30min)
**Equipment:** DIY air table (vibrating sieve + 1HP axial fan + 3 collection hoppers)
**Process:**
- Angle: 5-15° tilt
- Vibration: 3-5mm amplitude
- Fan: directed across sieve surface
- Heavy grains (density >4.5: metal sulfides, galena, cinnabar) → hopper 1 (near)
- Medium grains → hopper 2
- Light grains (clean soil, density 2.0-2.8) → hopper 3 (far)

**Testing:** Sample each hopper → test As, Pb, Hg, Cd. Adjust fan speed + vibration frequency to maximise clean fraction.

### Step 5: High-Gradient Magnetic Separation (15min)
**Equipment:** N52 rare-earth magnets Φ50×10mm (pull force ~30kg each), or high-intensity magnetic separator (0.5-2T)
**Process:** Remove magnetic fraction (Fe-oxides + arsenopyrite) which carries adsorbed As, Pb, Cd.
**Expected:** As 30-60%, Pb 20-40%, Cd 20-40% removal.

### Step 6: Biochar-Magnetic Polishing (30min)
**Biochar production:**
1. Soak rice husk/coffee husk in 5% FeCl₃ solution for 2h
2. Pyrolyse at 500°C for 2h in oxygen-limited environment (sealed metal drum with small vent hole)
3. Crush to <1mm

**Process:** Mix 3% biochar (w/w) with soil from step 5, rotate in drum for 15-30 min. Remove biochar with magnet.
**Expected:** Pb 80-90%, Cd 70-85%, Hg 60-80%.

### Step 7: Thermal Desorption (30-60min)
**Equipment:** Furnace/kiln capable of 450-550°C. Exhaust gas treatment required (activated carbon filter or water-cooled condenser to trap Hg⁰ + As₂O₃ vapour).
**Process:** 450-550°C, 30-60 min, inert atmosphere (N₂) or low-oxygen if preserving organic content.

| Metal | Removal | Notes |
|---|---|---|
| Hg | >95% | Melts at -39°C, boils at 357°C — completely volatilises |
| As | 50-80% | As₂O₃ sublimes at 193°C. Arsenopyrite decomposes 450-600°C. Fe-oxide bound As needs >600°C |
| Pb | None | Boils at 1749°C |
| Cd | None | Boils at 767°C |

**Caution:** Temperatures >300°C burn organic matter. >500°C decomposes CaCO₃ → CaO + CO₂.

## Chemical Recipes (for wet steps when needed)

| Solution | How to prepare (500mL) | Concentration | Uses |
|---|---|---|---|
| HCl 0.1M | 5mL HCl 32% + 495mL water (add acid to water!) | ~0.1M | Acid wash for Pb, Cd |
| H₂O₂ 2% | 33mL H₂O₂ 30% + 467mL water | ~2% | As(III)→As(V) oxidation |
| FeCl₃ 5% | 25g FeCl₃·6H₂O + 475mL water | ~5% | As coprecipitation |
| NaOH 1M | 20g NaOH + 500mL water (exothermic!) | 1M | pH adjustment |
| Na₂S 5% | 12.5g Na₂S·9H₂O + 237.5mL water (use same day) | ~5% | Sulfide precipitation of all 4 metals |
| KI/I₂ | 8.3g KI + 1.25g I₂ + 500mL water (dark bottle) | 0.1M+0.01M | Hg complexation |
| Citric acid 0.1M | 9.6g citric acid + 490mL water | 0.1M | Mild acid wash |

## Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| As still >0.1 ppm | As(III) not fully oxidised | Increase H₂O₂ dose. Check ratio As(III)/As(V) |
| Cd not precipitating at pH 8 | pH too low | Raise to pH 8.5-9.0 (Cd(OH)₂ only precipitates fully above 8.5) |
| Hg not decreasing | Hg⁰ elemental form present | Can't precipitate. Use thermal (450°C) or KI/I₂ |
| Cloudy filtrate | Colloidal precipitate | Add coagulant (PAM 0.1%) or heat to 60°C |
| H₂S smell during Na₂S step | pH dropped below 4 | Keep pH >4. Move outdoors. Wear respirator |
| Less than 70% clean soil recovered | Too much material in heavy fraction | Adjust fan speed. Re-process heavy fraction |
