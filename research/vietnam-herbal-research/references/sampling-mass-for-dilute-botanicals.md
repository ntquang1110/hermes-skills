# Sampling mass for detecting a diluted botanical

Minimum sample mass when a botanical is blended into a product at a low percentage
(e.g. 1–2% raw leaf powder) and must be detected analytically.

## The principle

**Missing mass is set by particle-count statistics (homogeneity), NOT by detector
sensitivity.** This is the trap, because everyone reaches for LOD first.

Detector sensitivity is usually a non-issue by orders of magnitude. The binding
constraint is whether your weighed portion actually contains a statistically
representative number of particles of the dispersed botanical.

## Worked case — 1% raw guava leaf in a tannin product (10/2026)

Question asked: "how many grams minimum to run the instrument and identify the guava leaf?"

**Sensitivity check — never the constraint:**

| Quantity | Value | Source |
|---|---|---|
| Avicularin in guava leaf extract | 1,37 mg/g | PMID 40835425 (J Vet Med Sci 2025) |
| Quercetin-3-O-glucuronide in extract | 6,85 mg/g | same |
| Total phenolics per g raw leaf | 16–45 mg/g | PMID 38202668 (Molecules 2023) |
| HPLC-DAD detection limit (quercetin glycosides) | ~0,2 µg | instrument class |

1 g of product × 1% leaf → ~100 µg avicularin, against a ~0,2 µg detection limit.
A **~500× margin**. Even a 10 mg portion would read. So sensitivity says "any amount".

**Particle-count check — the actual constraint:**

| Portion | Leaf at 1% | Particles (sieved 355 µm) |
|---|---|---|
| 1 g | 10 mg | ~210 |
| 500 mg | 5 mg | ~107 |
| 100 mg | 1 mg | **~21 — the threshold** |
| 20 mg | 0,2 mg | **~4 — unreliable** |

Particle mass basis: a plant particle at 355 µm sieve has volume ≈ 2,34×10⁻⁴ cm³;
at bulk density ~0,4 g/cm³ that is ≈ **0,094 mg per particle**.

Statistical representativeness needs **≥ 20–30 particles**, which puts the floor at
**~100 mg** for a 1% inclusion rate.

**Milling finer helps a lot.** Through a 180 µm sieve, particle mass drops to ≈ 0,012 mg
(~5× more particles per gram), permitting a 30–50 mg portion.

## Recommended answer

**0,5–1,0 g.** Not because of detection limits, but because:

- Labs normally require ≥ 0,5 g as a working minimum.
- Replicates must run in parallel to establish RSD < 5%.
- A repeat test needs reserve material.
- Sampling a heterogeneous blend at 100 mg invites irreproducible results.

## Corollary for tannin-rich matrices

**Polyamide SPE cleanup is mandatory** before injection. Highly polar tannins swamp the
chromatogram and mask the target flavonoid peaks. Catch and retain the tannin fraction,
collect the flavonoid-containing eluate.

## Corollary — raw leaf powder carries its own risks

Adding unextracted plant powder to a finished product introduces:
- **Aflatoxin** — assay per ĐĐVN Phụ lục 12.21 whenever dried plant material is used.
- **Microbial load** — dry at 60 °C and verify before blending.
- **Moisture/aw** — control aw < 0,60, not just moisture content (see the aw pitfall in
  `references/ddvn-vi-alkaloid-monographs.md`).

## The provenance limitation — say this out loud

Blending 1–2% raw leaf proves **plant material is present**. It does **not** prove the
active compound came from that material. Anyone can add 1% leaf powder to any bulk
powder. If the goal is demonstrating genuine origin, the correct move is:

**Fingerprint the incoming raw material at goods-in**, per ĐĐVN Phụ lục 12.23
(≥ 5 lots × 2 replicates = 10 data points), rather than doctoring the finished product.
See `references/ddvn-vi-alkaloid-monographs.md` section 7 for the 12.6 vs 12.23
distinction: 12.6 measures *how much*, 12.23 establishes *what it is*.
