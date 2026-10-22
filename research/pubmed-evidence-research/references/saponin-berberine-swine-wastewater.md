# Saponin + berberine DIRECT dosing into swine wastewater — verified bank (2026-09-09)

Deliverable: `D:/Hermes Proj/ez80-saponin-berberine-nuocthai/data/saponin_berberine_nuocthai_heo.json` (11 rows, 18 PMID all efetched) + `_abstracts_audit.txt`.
Context: KIỀM EZ TÁI SINH 80, Saponin ≥1.500 mg/kg. Question was DIRECT dosing into swine wastewater (COD/BOD/NH3/coliform), not via feed.

## Core conclusion (verified negative)
NO direct evidence on PubMed for dumping herbal saponin or berberine DIRECTLY into swine wastewater. All evidence is indirect:
(a) Yucca saponin VIA FEED reduces manure NH3; (b) tea saponin as EK-assist panel agent on URBAN sludge (heavy metals); (c) berberine in wastewater is a POLLUTANT that inhibits anaerobic methanogenesis ≥100 mg/L — direct dosing into a working biogas pit risks killing methanogens.

## Verified PMIDs (all esearch→esummary→efetch 2026-09-09)
| # | PMID | DOI | What abstract showed |
|---|---|---|---|
| Yucca sow manure NH3 (feed) | 34368272 | 10.3389/fvets.2021.676324 | 80 sows, 0.06–0.24% YSE, reduced total-N/urea-N/ammonia-N manure loss |
| EcoCare swine (feed, industry) | 19897627 | 10.2527/jas.2009-2348 | Saponin+AA+Bacillus feed; −18% NH3 volatilization/45d pit simulation; −14% solids, −22% viscosity |
| Yucca NULL low dose | 16825449 | 10.2134/jeq2005.0411 | Yucca 0/62.5/125 mg/kg feed pigs: NO effect on manure N or NH3 rate |
| Yucca nursery air (feed) | 11811465 | 10.2527/2001.79123096x | 125 ppm Yucca nursery pigs: wk-4 air NH3 lower but manure N/pH + plasma urea unchanged |
| Yucca tilapia water (feed, fish) | 41432999 | 10.1007/s10695-025-01607-7 | Yucca 0.2 g/kg + B. subtilis 1.0 g/kg: lowest unionized NH3 in water (closest to 'water quality') |
| Yucca review | 42589018 | 10.3390/ani16152376 | Steroidal saponin/polyphenol; Nrf2/ARE, NF-κB, ammonia-N metabolism; effects vary by species/dose; lacks standardization + commercial validation |
| Yucca gilt | 39682320 | 10.3390/ani14233356 | 0.25 g/kg YE gilts: ↑digestibility, T-AOC; ↓MDA, Proteobacteria/Streptococcus |
| Yucca combo pigs | 37662989 | 10.3389/fvets.2023.1095877 | Amino-Zn+YE 0.07%+mannanase 22 wk: ↑BW/ADG, gas reduction only trend (p>0.05), can't isolate Yucca |
| Yucca poultry review | 30368697 | 10.1007/s11356-018-3546-1 | Yucca via feed reduces poultry NH3/odor via microbiota+digestion |
| Yucca in-vitro panel | 37760368 | 10.3390/ani13182969 | 11 herbals in-vitro; YE reduced cecal NH3; strongest was astragalus −26.76% via ↓urease/uricase |
| Sheep saponin weak | 12553689 | 10.1080/00039420215633 | Yucca saponin 2–30 mg/kg DM lambs: only slight rumen NH3 reduction |
| Tea saponin EK sludge | 36113240 | 10.1016/j.watres.2022.119016 | Tea saponin 1 of 5 EK-assist agents on urban sewage sludge; panel −52–59% HM, P retained; NO per-agent split, NOT swine |
| Tea saponin nano antibacterial | 34382988 | 10.1039/d1fo01943k | TS/CTS@DMY-lips vs E. coli/S. aureus in vitro (266 nm, EE 41.93%); nano formulation, not crude powder |
| Berberine inhibits AD ⚠️ | 37926228 | 10.1016/j.envres.2023.117590 | BBR20 +4.2% CH4; BBR100 −17.3%; BBR500 −83.2%; Methanosaeta suppressed, VFA accumulates; 88–99% BBR partitions to sludge |
| Berberine removal MIL-101 | 33163779 | 10.1021/acsomega.0c03422 | MIL-101(Fe) 163.93 mg/g at pH 7, pseudo-second-order, π–π; berberine = toxic/poorly biodegradable pollutant |
| Berberine removal Mn-biochar | 39083888 | 10.1016/j.jcis.2024.07.147 | Mn-biochar from tea waste, chemisorption/monolayer; dosage > conc > pH (RSM) |
| Berberine E. coli biofilm ⚠️ | 40746958 | 10.3389/fcimb.2025.1565714 | 1/2-MIC induction → MIC >32×, biofilm 1.3/1.51/1.98× at 24/48/72h via csgD; csgD-OE MIC 100 µg/mL |
| Matrine+Berberine reversal | 38849633 | 10.1007/s00203-024-04021-4 | Mat+Ber 15d reversed gentamicin resistance 39.67%, MIC ↓128×; COMBO on poultry MDREC, not Ber alone in wastewater |

## Query patterns + counts (negative-evidence method)
- `saponin AND (swine OR pig OR porcine) AND (wastewater OR manure OR slurry)` → count=1 (19897627, via feed). Absence IS the finding; record the count.
- `Yucca extract ammonia manure` → 5, all via-feed.
- `saponin biosurfactant wastewater COD removal` → 0; `saponin urease inhibition ammonia` → 0.
- `berberine AND (wastewater OR water disinfection)` → 20, ALL berberine-as-pollutant/removal — direction inversion to state explicitly.
- `berberine anaerobic digestion sludge` → 1 (37926228); `berberine removal wastewater MIL-101` → 1 (33163779).

## Pitfalls specific to this territory
- **Quillaja trap**: `Quillaja saponin AND (wastewater OR water treatment OR manure)` → 16 hits but ALL vaccine adjuvant/emulsion/antigen — screen out at title, don't efetch, state exclusion reason in honest_gaps.
- **Tea-saponin noise**: `tea saponin AND wastewater` → 21 hits dominated by extraction/purification/nano-drug papers — only 36113240 (EK sludge) and 34382988 (nano antibacterial) are water/antibacterial-adjacent.
- **Feed-dose → pit-dose fallacy**: every Yucca dose is mg/kg FEED (0.06–0.25%, 62.5–125 mg/kg, 125 ppm). Never convert to mg/L wastewater. Row 1 of JSON states this explicitly.
- **Berberine direction**: default assumption 'berberine treats water' is backwards — literature treats berberine as the contaminant to REMOVE. State the inversion or the deliverable misleads.
- **Safety thresholds to reuse**: berberine AD: 20 mg/L slightly pro-methanogenic vs 100/500 mg/L inhibitory; Yucca null at 62.5–125 mg/kg feed (16825449) — cite both whenever a product claims pit-dosing efficacy without jar-test.

## Trial recommendation carried in deliverable
No direct dosing into working anaerobic pit without jar-test on real pit sludge (gas, VFA, pH). If testing saponin: (a) via feed at verified doses then measure air-NH3 + manure N; (b) jar-test direct dosing ONLY post-biogas (aerobic/settling stage) vs QCVN 62:2025 (COD/BOD/TSS/T-N/NH3/coliform).
