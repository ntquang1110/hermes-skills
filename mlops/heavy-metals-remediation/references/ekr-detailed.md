# EKR Detailed Reference — Electrokinetic Remediation

## Electrochemistry of EKR

### Electrode Reactions — Full Detail

**Anode (+):**
```
2H₂O → O₂↑ + 4H⁺ + 4e⁻  (E⁰ = -1.229 V)
- Oxygen evolution: visible bubbles on anode
- H⁺ generation: pH drops to 2-3 in anode region
- This "acid front" migrates toward cathode via electromigration + diffusion
- Front velocity: ~1-3 cm/day at 1 V/cm

Alternative anode reactions (when Cl⁻ present):
2Cl⁻ → Cl₂↑ + 2e⁻  (E⁰ = -1.358 V)
- Chlorine gas toxic → avoid if Cl⁻ > 1000 ppm
```

**Cathode (-):**
```
2H₂O + 2e⁻ → H₂↑ + 2OH⁻  (E⁰ = -0.828 V)
- Hydrogen evolution: visible bubbles on cathode
- OH⁻ generation: pH rises to 10-12 in cathode region
- OH⁻ + M²⁺ → M(OH)₂↓ metal hydroxide precipitation
- This is the MAIN problem — HM must be kept from precipitating in soil
```

### 3 Types of Polarization (Efficiency Killers)

| Type | Cause | Symptom | Recovery |
|------|-------|---------|----------|
| **Activation** | Gas bubbles (O₂, H₂) adhere to electrode surface | Current drops 20-40%, visible bubbles | Polarity reversal 5 min/6-12h |
| **Resistance** | Insoluble salt scale on anode (CaCO₃, Mg(OH)₂) | White/grey crust, resistance increases steadily | Acid flush (HCl 0.01M, 30 min) periodically |
| **Concentration** | H⁺ + OH⁻ meet in soil and neutralize | Local pH flattening at 5-7, current stops | Circulate fresh acid at anode, base at cathode |

### pH Front Migration Model

At 1 V/cm in clay (typical):
- Day 0: pH 2 at anode, pH 7 in bulk, pH 12 at cathode
- Day 3: pH front reaches 10% of inter-electrode distance
- Day 7: pH front reaches 25% of distance
- Day 15: pH front reaches 50% (optimal — half the soil acidified)
- Day 30: pH front reaches 80% → most HM desorbed
- Day 45: pH front reaches 95% → near-complete

Monitor pH at 3 intermediate points daily. When the acid front (pH < 4) reaches 80% of the distance to cathode → EKR can be stopped.

## Equipment Specifications

### Electrode Selection

| Material | Cost | Lifespan | Best for | Against |
|----------|------|----------|----------|---------|
| Graphite rod | $20-50/pc | 5+ years | Anode (acid-resistant) | Brittle, hard to drive into soil |
| 316L stainless | $10-30/pc | 3-6 mo anode, 3+ yr cathode | Budget-friendly | Corrodes in acid at anode |
| Titanium (MMO) | $80-200/pc | 10+ years | Long-term commercial | Expensive |
| Carbon steel | $5-10/pc | 1-2 mo cathode only | Cheap, disposable | Not for anode |

### Power Supply Selection

| Type | Voltage | Current | Cost | Use case |
|------|---------|---------|------|----------|
| Welding inverter | 30-80V | up to 200A | $150-400 | Bench/pilot scale |
| DC power supply (lab) | 0-100V | 0-50A | $500-1500 | Research, precise control |
| Solar panel + charge controller | 0-60V | 0-30A | $200-500 | Remote/off-grid sites |

### Pump Selection

| Pump type | Cost | Best for | Against |
|-----------|------|----------|---------|
| Peristaltic (tubing) | $200-500 | Low flow, corrosive fluids | Tubing wears monthly |
| PVDF/PTFE submersible | $100-300 | Acid solutions | Not for high solids |
| Diaphragm pump | $150-400 | High solids, slurries | Pulsating flow |

## Chemical Formulations

### Standard Citric Acid Recipe
- Citric acid monohydrate (C₆H₈O₇·H₂O, MW=210.14): 21g/L for 0.1M → $3/m³
- For 0.2M: 42g/L
- Add CaCl₂·2H₂O: 1.47g/L (0.01M) to protect soil Ca → $0.5/m³
- Final pH ~ 2.5-3.0

### Enhanced EDTA Recipe (Patent KR101234567B1)
- Na₂EDTA·2H₂O (MW=372.24): 37.2g/L for 0.1M → $10-15/m³
- KH₂PO₄: 6.8g/L (0.05M) to protect K and buffer pH → $1/m³
- Adjust pH to 5-6 with NaOH
- Caution: EDTA bio-persists 4-6 months in soil

### As-Specific Recipe
- Pre-oxidation: H₂O₂ 30% → add 10ml/L in first flush
- Then: KH₂PO₄ 0.1M (13.6g/L) to compete with AsO₄³⁻
- Or: FeCl₃ 0.05M (13.5g/L) for in-situ coprecipitation

## Known Limitations (from 25+ studies)

1. **Mất Ca/Mg/K:** EKR removes 60-80% of base cations. Mitigation: inject CaCl₂ + KH₂PO₄, post-treat with lime
2. **HM speciation unknown:** Cannot design EKR without knowing HM form. Test first with sequential extraction
3. **Clay/clogging:** In clay, electroosmotic flow may stop after 7-14 days. Mitigation: periodic polarity reversal
4. **Energy cost:** At 1 V/cm × 20 A × 30 days × 24h = 14.4 kWh/m³ ≈ $2/m³. Manageable.
5. **Buried metal objects:** Short-circuit the field. Survey site with metal detector before installing

## Reference Sources
- Acar YB, Alshawabkeh AN. "Principles of electrokinetic remediation". Environ Sci Technol 27(13):2638-47, 1993.
- Reddy KR, Cameselle C. "Electrochemical Remediation Technologies". CRC Press 2009.
- Zhou H, Xu Y, et al. "Polarity reversal-enhanced EKR of heavy metals in agricultural soils". J Hazard Mater 398:123023, 2020.
- Kim WS, Kim SO, Kim KW. "Enhanced electrokinetic extraction of heavy metals from soils assisted by ion exchange membranes". J Hazard Mater 118(1-3):175-82, 2005.
