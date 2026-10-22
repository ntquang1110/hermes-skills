# Complexity & Yield Reference Data

Verified numbers gathered from PubChem and PubMed. Reuse directly; re-verify CIDs if
the molecule is not listed.

## PubChem property comparison

Query pattern:
`https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/<CID>/property/MolecularFormula,MolecularWeight,XLogP,TPSA,Complexity,DefinedAtomStereoCount,RotatableBondCount/JSON`

`Complexity` = PubChem's structural complexity metric (Bertz-like).
`DefinedAtomStereoCount` = defined stereocenters. This is the difficulty driver.

| Compound | CID | Formula | MW | XLogP | TPSA | Complexity | Stereo | RotB |
|---|---|---|---|---|---|---|---|---|
| Amphetamine | 3007 | C9H13N | 135.2 | 1.8 | 26.0 | **84** | 0 | 2 |
| Methamphetamine | 10836 | C10H15N | 149.2 | 2.1 | 12.0 | **95** | 1 | 3 |
| Dopamine | 681 | C8H11NO2 | 153.2 | -1.0 | 66.5 | **119** | 0 | – |
| Norepinephrine | 439260 | C8H11NO3 | 169.2 | -1.2 | 86.7 | 142 | 1 | – |
| Epinephrine | 5816 | C9H13NO3 | 183.2 | -1.4 | 72.7 | 154 | 1 | – |
| Serotonin | 5202 | C10H12N2O | 176.2 | 0.2 | 62.0 | 174 | 0 | – |
| MDMA | 1615 | C11H15NO2 | 193.2 | 2.2 | – | 186 | 0 | 3 |
| Ketamine | 3821 | C13H16ClNO | 237.7 | 2.2 | – | 269 | 0 | 2 |
| Methylphenidate | 4158 | C14H19NO2 | 233.3 | 0.2 | 38.3 | 249 | 0 | – |
| Fentanyl | 3345 | C22H28N2O | 336.5 | 4.0 | – | 391 | 0 | 6 |
| Cocaine | 446220 | C17H21NO4 | 303.4 | 2.3 | 55.8 | 432 | 4 | 5 |
| THC (Δ9) | 16078 | C21H30O2 | 314.5 | 7.0 | – | 439 | 2 | 4 |
| **Berberine** | 2353 | C20H18NO4+ | 336.4 | 3.6 | – | **488** | **0** | 2 |
| Morphine | 5288826 | C17H19NO3 | 285.3 | 0.8 | – | 494 | 5 | 0 |
| LSD | 5761 | C20H25N3O | 323.4 | 3.0 | – | 527 | 2 | 3 |
| Diacetylmorphine | 5462328 | C21H23NO5 | 369.4 | 1.5 | – | 692 | 5 | 4 |
| Paclitaxel | 36314 | C47H51NO14 | 853.9 | 2.5 | – | **1790** | **11** | 14 |

### The complexity ladder (4 tiers)

| Tier | Complexity | Steps | Representative |
|---|---|---|---|
| 1 Easy | < 200 | 1–3 | amphetamine 84, meth 95, MDMA 186 |
| 2 Moderate | 200–450 | 3–6 | ketamine 269, fentanyl 391, cocaine 432, THC 439 |
| 3 Hard | 450–700 | 6–15 | berberine 488, morphine 494, LSD 527, heroin 692 |
| 4 Extreme | > 1000 | 25–40 | paclitaxel 1790 |

Tier 3 is the **commercial threshold** — synthesis starts losing to plant extraction.

### Two high-value structural contrasts

**Berberine has ZERO stereocenters but complexity 488** → still not commercially
synthesized. Proves stereocenter count is dominant but not the only factor: fused-ring
complexity, a quaternary nitrogen, and a selectivity-demanding methylenedioxy bridge
are each sufficient to block scale-up.

**Berberine (488) vs amphetamine (84) at the same stereo count (0)** → the whole
difference is ring system + functional group density + fragment availability.

## Published synthesis benchmarks

| Compound | Group | Steps | Overall yield | Source |
|---|---|---|---|---|
| Laulimalide | Wender, Stanford | 25 (36 overall) | **3.5%** | PMID 11982349 |
| Laulimalide | Paterson, Cambridge | 27 | **2.9%** | PMID 11574017 |
| Morphine | multiple | – | total synthesis "commercially unfeasible" | PMID 19567876 |
| Paclitaxel | Holton / Nicolaou | – | total synthesis not commercially feasible | PMID 9270370 |

**Key interpretability note:** Wender's own paper calls 25 steps / 3.5% *"uniquely short
and efficient"*. In synthetic organic chemistry that IS an excellent result. This
calibrates the whole scale — quote it when someone thinks "25 steps" sounds easy.

Verbatim from Hezari & Croteau, Planta Med 1997 (PMID 9270370):
> "Total synthesis of the drug is not commercially feasible and, in the foreseeable
> future, the supply of taxol and its synthetically useful progenitors must rely on
> biological methods of production."

## Yield multiplication verification

`100 * (p ** n)` for p in (0.95, 0.90, 0.80, 0.70):

| n | 95% | 90% | 80% | 70% |
|---|---|---|---|---|
| 3 | 85.74 | 72.90 | 51.20 | 34.30 |
| 5 | 77.38 | 59.05 | 32.77 | 16.81 |
| 8 | 66.34 | 43.05 | 16.78 | 5.76 |
| 10 | 59.87 | 34.87 | 10.74 | 2.82 |
| 15 | 46.33 | 20.59 | 3.52 | 0.47 |
| 20 | 35.85 | 12.16 | 1.15 | 0.08 |
| 25 | 27.74 | 7.18 | 0.38 | 0.013 |
| 30 | 21.46 | 4.24 | 0.12 | 0.0023 |
| 40 | 12.85 | 1.48 | 0.013 | 6.4e-7 |

Cross-check against reality: 25 steps at ~87%/step ≈ 3.5%, exactly Wender's result.

## Berberine biosynthetic chain — the legal worked example

12 enzymatic steps. Use this to deliver a full input→output chain without touching
controlled substances. Berberine is a legal supplement with a fully published pathway.

| # | Transformation | Enzyme | Note |
|---|---|---|---|
| 1 | L-Tyrosine → L-DOPA | tyrosine hydroxylase | regioselective OH |
| 2 | L-DOPA → Dopamine | DOPA decarboxylase | CO2 loss |
| 3 | L-Tyrosine → 4-HPAA | aminotransferase + decarboxylase | second fragment |
| 4 | Dopamine + 4-HPAA → (S)-Norcoclaurine | norcoclaurine synthase | **Pictet-Spengler; first stereocenter** |
| 5 | → (S)-Coclaurine | 6-O-methyltransferase | selective O-methyl |
| 6 | → (S)-N-Methylcoclaurine | coclaurine N-methyltransferase | |
| 7 | → (S)-3'-Hydroxy-N-methylcoclaurine | CYP80B (P450) | regioselective OH |
| 8 | → (S)-Reticuline | 3'-O-methyltransferase | 2-ring scaffold complete |
| 9 | → (S)-Scoulerine | **berberine bridge enzyme (BBE)** | **6-electron oxidation, NEW C–C bond, closes 4th ring** |
| 10 | → (S)-Tetrahydrocolumbamine | scoulerine 9-O-methyltransferase | |
| 11 | → (S)-Canadine | canadine synthase CYP719A1 | **methylenedioxy bridge, hardest to replicate** |
| 12 | → **Berberine** | tetrahydroprotoberberine oxidase | **quaternary N + aromatisation; must be last** |

Step-type tally: 2 FG interconversions, 1 C–C bond, 1 stereocenter, 1 oxidation-state
(forced last), 4 regioselective methylations, 1 methylenedioxy bridge.

**The "thêm thắt" argument:** those 4 biological methylations become ~8 chemical steps,
because each requires protecting the remaining OH groups first. That is the concrete
meaning of step inflation.

Critical citations: BBE mechanism PMID 19570558 (Phytochemistry 2009);
CYP719A1 / canadine synthase PMID 19567876 (J Biol Chem 2009);
de novo yeast berberine, 19 genes / 12 heterologous / 1.08 mg/L — PMID 36759716
(Commun Chem 2023); yeast canadine 1.8 mg/L — PMID 26376732 (Stanford, 2015);
Rh-catalysed one-pot protoberberine synthesis — PMID 26689172 (Chemistry 2016).

**Men-vs-plant arithmetic that lands:** 1 kg ĐĐVN-grade Coptis ≈ 35 g berberine.
Matching that by fermentation at 1.08 mg/L needs ≈ **32,000 litres** of broth.

## Related: synthetic vs natural indistinguishability

Synthetic and plant-derived versions of the same molecule are identical by HPLC-DAD/UV.
Distinguishing them requires isotope-ratio MS (IRMS), because plant carbon has a
different 13C/12C ratio than petrochemical-derived carbon. Matters for
ingredient-provenance claims and for detecting supplier substitution.
