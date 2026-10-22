# Rare-earth elements in pig feed — verified source bank (NHÓM 3 research, 2026-08-12)

Condensed knowledge bank for the ongoing rare-earth-in-pig-feed research project
(parent workspace: `D:/Hermes Proj/rare-earth-pigs/`). All 23 PMIDs were efetch-verified
this session; regulatory facts carry their own verification trail. Do NOT re-cite a PMID
without re-verifying ("verified before" is not "verified now").

## Project output schema (each line = 1 topic × 1 effect/regulation)

```json
{"id":"...","element":"...","element_vi":"...","name_en":"...","effect":"...","group":"...",
 "mechanism":"...","evidence_level":"Mạnh|Vừa|Sơ bộ|Không có bằng chứng trực tiếp",
 "dosage_ref":"...","side_effects":["..."],
 "references":[{"type":"paper","label":"...","pmid":"","doi":"","note":"..."},
               {"type":"patent","number":"","title":"","note":""}],
 "verification":"..."}
```
Hard rules: no fabricated PMID/patent; regulations/standards have no PMID → leave `pmid`
empty and put source/URL in `note`; patents only when verified via Google Patents XHR.
Output written with `ensure_ascii=False` (Vietnamese diacritics) + a re-parse validator
that asserts every required key. Example file: `data/group3_mix_regulation.json` (21 lines).

## Verified PMIDs by topic (efetch-confirmed 2026-08-12)

**REE mix on pigs (growth):**
- 11686799 He 2001 J Anim Physiol Anim Nutr — 300 mg/kg REE-chloride (La/Ce/Pr): ADG +19% (p<0.05), FCR −11%, T3 lowered, very low La/Ce accumulation in muscle/liver/kidney
- 11852679 Schuller 2002 Berl Munch Tierarztl Wochenschr (DE) — 75–300 mg/kg: pigs +19% ADG/+11% FCR; poultry NO effect; NAA: minute REE in liver/bone; REE used at scale in China ~20 yrs prior
- 16958792 Kraatz 2006 J Anim Physiol Anim Nutr — **NEGATIVE trial**: 200 mg/kg REE-citrate (La/Ce/Pr/Nd), 112 weaned piglets, 6 wk; no growth difference (p>0.05), late-phase FCR +8% (p=0.01); no fecal microbiota change — the "not reproducible in Europe" caution
- 31480174 Tariq 2020 Asian-Australas J Anim Sci (review) — inconsistent results; negligible residues in edible tissue; mechanism unclear (poor absorption, Ca-similarity, local gut action); anti-inflammatory/antioxidant/immune
- 33141264 Tommasi 2021 Arch Environ Contam Toxicol (review, knowledge-gap) — hormesis in plants; outside China REE ag/zootechnical use not practiced; feed-additive evidence positive at some doses but needs work

**China additive RECC (稀土壳糖胺螯合盐 = rare earth-chitosan chelate):**
- 40141053 Hao 2025 Int J Mol Sci — RECC 0/200/400/600 mg/kg, 80 nursery pigs, 28 d; 200 mg/kg best: tibia trabecular quality, IgM/IgA/IgG/IL-10 ↑, TNF-α ↓, ADG/FCR ↑, diarrhea ↓
- 31569383 Xiong 2019 Animals (Basel) — maternal REE late gestation/lactation: sow + offspring performance/health/fecal microbiota
- 16027965 Liang 2005 Environ Geochem Health — "Changle" REE microfertilizer (brand); no distinct REE residue in grains

**Dose/mechanism in rats & poultry:**
- 12752829 He 2003 J Anim Physiol Anim Nutr — rats: LaCl3 or REE mix (38% LaCl3/52% CeCl3/3% PrCl3) 75–150 mg/kg: BWG +5–9%, FCR −8–11%, AP/ALT ↑, glucose ↓
- 19364383 He 2010 J Anim Physiol Anim Nutr — broilers: REE-citrate 70–100 mg/kg: BWG +5.0%, FCR −3.4%; residues La/Ce liver 0.11–0.76 mg/kg, muscle 0.02–0.30 mg/kg

**Lanthanum carbonate (human drug → veterinary additive):**
- 21332344 Damment 2011 Ren Fail — pharmacology review: most potent of the phosphate binders (vs Al(OH)3, CaCO3, sevelamer); no adverse secondary pharmacology
- 17570622 Damment 2007 Toxicol Lett — oral bioavailability of La = 0.0007%; 97.8% fecal recovery in 24 h; biliary excretion; renal <2% — the basis for "low residue risk"
- 35233256 EFSA 2022 EFSA J 20(2):e07168 — lanthanum carbonate octahydrate (Lanthan One) cats: safe 7,500 mg/kg feed, efficacious P-binding from 1,500 mg/kg
- 38601863 EFSA 2024 EFSA J 22(4):e8729 — same for dogs; already authorized for cats

**Yttrium & Scandium (no direct pig-nutrition data exists):**
- 17845245 Vhile 2007 J Anim Physiol Anim Nutr — Y2O3 inert digestibility marker (dogs/foxes/mink), 94.4% fecal recovery
- 20487094 Malde 2010 J Anim Physiol Anim Nutr — yttrium as indicator in Ca-digestibility study in growing pigs
- 41360343 Jiang 2026 Environ Pollut — HREE (Gd/Y/Dy/Tb) oral: fecal excretion, liver+femur accumulation, hippocampal neuron loss; human RfD Y = 0.236 ng/kg/day — far below China's unified HREE RfD (70 µg/kg/day)
- 23011662 Kitamura 2012 Biol Trace Elem Res — Y/Sc/Eu chlorides: urinary excretion <2%; colloidal conjugates → reticuloendothelial + glomerular accumulation
- 19221697 Tanida 2009 Biol Trace Elem Res — ScCl3 IP in rats: nephrotoxicity (urinary Sc 0.0063%, NAG & β2-MG ↑)

**Context:**
- 24034214 Thacker 2013 J Anim Sci Biotechnol — REE among AGP alternatives; inconsistent results, rarely equal to antibiotics
- 35461107 Cristea 2022 Meat Sci — La and Ce in pork discriminate feeding regime (97.8% correct) — baseline REE in meat is natural, useful for provenance
- EFSA Lancer opinions: 42109452 (2016 — safe ≤250 mg/kg for weaned piglets; consumer/environment NOT concluded: La developmental-neurotoxicity concern, no long-term/ repro data, no tissue-residue data) and 32626202 (2019 — additional data: no consumer/environment concern at 250 mg/kg up to 120 days; neurotoxicity NOAEL still not identified)

## Regulatory facts (with verification trail)

- **EU**: Lancer (lanthanide citrate, La+Ce, Treibacher) authorized for weaned piglets by
  Commission Implementing Regulation (EU) 2020/1370 (1 Oct 2020) — NOT "not authorized",
  a common misstatement; lanthanum carbonate octahydrate: dogs EU 2025/313, cats EU
  2025/647 (1500–7500 mg/kg feed); 4 lanthanum-containing feed additives approved in EU
  register; EU has no limit values for REE in food (Eurofins WEJ article 2026-04-28
  "The analysis of rare earth elements in food and feed" summarizes all of this).
- **US**: grep of full 21 CFR Part 573 (eCFR API XML) → 0 hits for
  lanthanum/cerium/yttrium/scandium/rare earth/lanthanide → not permitted as feed
  additive; no GRAS status → illegal as feed additive in the US.
- **China**: GB 2762-2005 had REE limits (稀土限量; tea 2.0 mg/kg confirmed via snippet);
  GB 2762-2012 carried them per 2005; **GB 2762-2017 deleted REE limits** (dietary
  exposure assessment) → no REE residue limit in meat today (GB 2762-2022/2025). MOA
  Announcement 288 (2005) approved RECC (稀土壳糖胺螯合盐) as a feed additive — via
  secondary news source (gdswine.com), flag as such; enterprise standard Q/SQA007-2019
  exists for the commercial product.
- **Vietnam**: AGP ban since 2018. Vietnamese field trial (Tạp chí Phân tích Hóa, Lý và
  Sinh học, T30, số 2A/2024, vjol.info.vn/TCPTHLS/article/download/99331/83828): REE
  citrate 200 mg/kg feed in chicken — diarrhea −33.58%, respiratory disease −26.73%,
  weight gain +5.51%, FCR −5.7%; REE ascorbate 200 mg/kg in catfish — +12% gain (p<0.05),
  FCR −7%, survival +7%; residues ≈ control.
