# rare-earth-pigs — Group 2 notes (heavy REE + CeO2 NP on pigs)

Context: research for a Vietnamese pig farmer + active-ingredient producer. Output = Vietnamese JSON knowledge base, one row per element/form × effect, evidence-graded, all PMIDs verified. Project data dir: `D:/Hermes Proj/rare-earth-pigs/data/`. Group 2 deliverable: `group2_heavy_nano.json` (27 rows, 46 verified PMIDs, 66 DOIs, 0 patents — Google Patents blocked).

## Verified headline findings (2026-08-12)

### CeO2 NP — gut protection is RODENT-ONLY
- NO direct CeO2-NP-on-pig study exists in PubMed (searched `cerium oxide nanoparticle AND (pig OR swine OR porcine)`, `... AND (piglet OR weaned)`, `cerium AND (piglet OR weaned OR growth performance)`).
- Anti-oxidant/anti-inflammatory gut protection shown only in mouse colitis (DSS/IBD) models: 41949254 (ultrasmall ceria + 5-ASA), 41567735 (hollow CeO2 IBD), 42388783 (triptolide-CeO2 nanozyme), 42548017 (radioprotection of intestine), 41512469 (barrier stabilization UC).
- Caution side: CeO2 NP disrupted gut-liver axis / microbiota / glycolipid metabolism in ZEBRAFISH: 42309249. Two-faced effect — include as warning row.
- Closest pig-relevant data (light-REE premixes, NOT CeO2 NP): EFSA Lancer (lanthanide citrate La+Ce) for weaned piglets — safety NOT concluded: 42109452; REE-citrate 200 mg/kg × 6 wk on 112 weaned piglets — NO growth effect (negative result): 16958792; REE-chitosan chelate nursery pigs (tibia quality, disease resistance, performance): 40141053; sow late-gestation/lactation supplementation: 31569383.

### Gd — strong retention/NSF evidence (human/rodent), zero pig-toxicity data
- Tissue retention (brain/bone/kidney/skin): 28964466, 37058336 (GDD expert opinion), 42511552 (rat kidney/brain), 42217074 (liver fibrosis ↑ retention).
- NSF: 18952698 (meta-analysis), 26768242, 33804005, 42150162 (CJASN 2026).
- In pigs Gd appears ONLY as MRI contrast in imaging studies: 41834943 (swine CMR), 16801371 (MR-guided injection). Mark "Không có bằng chứng trực tiếp" for pig toxicity.

### Ho, Lu — DIRECT pig data, but radiopharmaceutical context (not chemical REE toxicity)
- Ho: 166Ho-microsphere hepatic radioembolization in pigs: 7970432 (SPECT dosimetry), 15690505 (MRI biodistribution live pig), 19789880 (5 pigs, scout 60 mg + treatment 540 mg); coronary: 11083197, 12845188.
- Lu: 177Lu-OPS201 biodistribution/dosimetry in pig model: 27294582, 30733648.

### Yb — direct pig marker data + UCNP in vivo (mice)
- YbCl3 180 mg/day as indigestible fecal marker in 6.5-wk-old pigs: 35051683.
- Yb3+-doped UCNP/NIR-II probes in vivo (mice): 38349065, 32806899 (highly doped Yb/Er/Tm UCNP), 30050096 (HA-based, long-term tracking).

### Sm, Eu, Tb, Dy, Er, Tm — NO direct pig evidence
- Sm/Eu only as fluorescent diagnostic labels on pig samples: 23024456 (Sm/Eu FIA haptoglobin/CRP), 36017365 (Eu LFIA Trichinella in pig blood), 34331087 (EuNPs PRRSV), 34075517 (Eu FIA ASFV).
- Tb/Er/Dy/Tm: trace levels in pork/food + luminescence probes only: 35461107 (REE in Romanian pork), 22840576 (16 REE in Chinese foods), 32227051 (Tb sensor), 35609524 (NaEr0.8Yb0.2F4 NIR-II).
- General REE accumulation/hormesis reviews (use for "no direct evidence" rows): 26164116 (Environ Res 2015), 25679485 (Ecotoxicol Environ Saf 2015), 33141264 (knowledge gap analysis), 35715718 (hormesis in feed additives).

## Working esearch term patterns
- `cerium+oxide+nanoparticle+AND+(pig+OR+swine+OR+porcine)` — mostly imaging/in-vitro; no pig trial.
- `rare+earth+AND+(pig+OR+swine)+AND+accumulation` — feed-additive + pork-meat studies.
- `gadolinium+AND+(pig+OR+swine+OR+porcine)` — MRI contrast studies (false positives for toxicity).
- `holmium-166+AND+(pig+OR+swine+OR+porcine)` — radioembolization (real pig data).
- `<element>+AND+(pig+OR+swine)` — for each heavy REE; expect near-zero relevant hits; fall back to general REE reviews.
- Refinement trick: add `AND (liver OR tissue)` or `AND accumulation` to cut laser/synthesis noise.

## Reusable gotchas hit this session
- PubMed rate limit (3 req/s unauthenticated) → sleep ≥0.7s between esearch calls; batch in one execute_code run.
- Large esummary/efetch responses truncate stdout → `curl -s URL -o <workspace-relative path>` then parse file. Bash `/tmp` is invisible to the execute_code sandbox on Windows.
- DOI extraction: efetch `retmode=xml`, regex `<ELocationID EIdType="doi">([^<]+)</ELocationID>`. Pre-2000 papers (e.g. 7970432, 11852679, 23024456) have no DOI — leave empty.
- Google Patents XHR + browser both return "Sorry..." block → record `chưa verify`, no patent numbers.
