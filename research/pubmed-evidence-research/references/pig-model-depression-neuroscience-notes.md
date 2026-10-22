# Pig as a translational model for human depression — verified PMID bank

Session 18/10/2026. Deliverable: `D:/Hermes Proj/hostcore/docs/03a-research-heo-vs-nguoi-findings.md`
(84 KB, 102 PMIDs, 5 preprints flagged, 35 `KHÔNG CÓ NGUỒN` entries). Project continues —
reuse this bank for 03b/03c rather than re-searching. **All PMIDs below were verified by
reading the real abstract via Europe PMC `resultType=core`** (see
`references/europepmc-rest-verification.md` for the working recipe).

**Screening rule applied throughout (critical):** `guinea pig` = chuột lang (*Cavia
porcellus*) ≠ heo (*Sus scrofa*). Many "piglet depression" hits are guinea-pig pups —
PMIDs 37529896, 27374759, 35191529, 40059538, 30666192 are **guinea pig, EXCLUDE**.
Also `guinea pig` poisoned the cortisol/corticosterone queries.

## Verified bank by mechanism

**Gyrification / why pig > rodent (CAO)**
- 17445892 — pig brain gyrencephalic, resembles human more than rodents (landmark review)
- 31115245 — 6 human-homologous resting-state networks (DMN, executive control, SMN, visual, auditory, cerebellar) + DTI; explicit "gyrencephalic… vs rodents"
- 39912370 — porcine cingulate sulcus cytoarchitecture; **gigantopyramidal neuron** (human/NHP subtype) in sulcus fundus; "not seen in the smooth, lissencephalic brain of rodents"
- 40633711 — gyrencephalic (ferret/NHP) vs lissencephalic (rat) BBB after blast: ferret showed Evans-blue extravasation, **rat did not**

**Regional homology (CAO for anatomy, THẤP cho functional-depression)**
- 17027768 — minipig PFC defined by thalamocortical (MD) projections; PFC ≈ 24% neocortex, 10% brain vol; **lacks granular layer IV of primate PFC** (key limitation)
- 39340562 — minipig subgenual cortex = **BA25/BA33/IG homologue** (the human DBS-for-depression target)
- 27994542 — minipig NAcc core/shell + retrograde inputs (mPFC, BA25, amygdala, CA1, thalamus, VTA, raphe)
- 42133082 — minipig ventral striatum/ventral capsule; "paralleling human nigrostriatal and mesolimbic circuits"
- 27778106 — Göttingen minipig telencephalon cytoarchitecture (brain ~69 g, 55×47×36 mm at 1 yr)
- 32246243 — minipig limbic tractography closely resembles human
- 34798047 — snRNA-seq human/macaque/pig hippocampo-entorhinal: **neurogenesis in pig & macaque but NOT human** → reverse-direction species difference, do NOT extrapolate pig→human neurogenesis
- 10466025 — stereotaxic atlas of the pig brain
- 42679942 — porcine rsfMRI TBI (ECN/CN down, SMN preserved)
- 42178066 — swine connectome Kuramoto model (sFC vs eFC r=0.61)
- 22444844 — pig in brain imaging/neurosurgery review

**Depression-like models (11 total; 1 negative) — TRUNG BÌNH**
- 37876629 — **the canonical pig depression model**: 24-h restraint + food/water deprivation, Bama pigs; ↓sucrose preference, ↑serum COR, ↓hippocampal 5-HT; authors' own model score 0.57 ("reliability… requires further verification")
- 31379533 — **strongest model**: psychosocial chronic stress (isolation+impoverishment+unpredictability) ± fluoxetine; ↑resignation, ↑salivary cortisol, ↓hippocampal neuron density/proliferation, ↓BDNF (p=0.056) & ↓5-HT1A (p=0.007); MRS+fMRI+fecal SCFA
- 15318328 — tethered housing 5 months: flattened cortisol rhythm, hypercortisolemia, cortisol inversely correlated with dentate gyrus volume/neuron number
- 20193701 — tethered vs loose sows; authors: "chronically stressed pigs develop depression-like symptoms" **BUT** "it can be questioned whether… an animal model of major depression" (self-critique, cite for limitations)
- 14651945 — repeated early isolation piglets: ↑hippocampal IL-1β, ↑GR binding, ↓CRH hypothalamus / ↑CRH amygdala
- 11240005 — very early weaning (d6): ↓urinary NE and epinephrine ~3×
- 16271354 — early weaning + isolation: ↓GR/MR/11β-HSD1/2 mRNA hippocampus + frontal cortex
- 15961089 — prenatal social stress (sow mixing): offspring ↑CRH mRNA PVN + amygdala, abnormal maternal behaviour
- 10985416 — prenatal ACTH to restrained sows → altered offspring HPA
- 34795321 — in utero heat stress → altered postnatal HPA; **also the DST + CRH-challenge source**
- 33370353 — pig psychosocial chronic stress + phMRI (Synacthen challenge) → BOLD in hippocampus/cingulate
- **17991496 — NEGATIVE RESULT, cite prominently:** repeated social defeat in female pigs does NOT induce depression-like neuroendocrine effects (no GR/MR change, no 5-HT turnover change) — only behavioural adaptation

**HPA / cortisol — CAO**
- 27543093 — stress biomarkers in swine (HPA/sympathetic/HPG/immune) review
- 34795321 — dexamethasone suppression test + CRH challenge work in pigs → dexamethasone negative feedback IS intact
- 42057944 — salivary biomarker panel after ACTH (cortisol, cortisone, total esterase rise; chromogranin A/α-amylase/oxytocin unchanged)
- 41395546 — many vertebrates make BOTH cortisol and corticosterone; don't assume a single GC across species
- 38945307 — porcine vs human carbonyl reductases in corticosteroid/neurosteroid metabolism
- 42175714 — glucocorticoids in pregnancy (GC biology reference)

**Monoamines / BDNF — TRUNG BÌNH–CAO**
- 36913918 — **best behavioural-correlate source**: minipigs high vs low tolerance to humans differ in hypothalamic 5-HT, SN 5-HT/5-HIAA/DA/DOPAC, striatal DA, hippocampal NA, TPH2/HTR7 mRNA
- 40823320 — low sanitary conditions + dietary amino acids in piglets: ↓platelet 5-HT, ↓hippocampal/PFC Trp, kynurenine, 5-HT, DA, NE, HVA + ↓play behaviour
- 28685616 / 26825776 — pig brain 5-HT microdialysis ↔ [11C]AZ10419369 (5-HT1B) / [11C]Cimbi36 (5-HT2A) PET
- 20347936 — STN DBS → striatal dopamine release in pig, measured by fast-scan cyclic voltammetry; optimum 120–180 Hz **matches the human therapeutic range**
- 20920780 — 2-h transport → ↑cortisol, ↓hippocampal BDNF mRNA; curcumin reverses
- 40884090 — oral tryptophan to suckling piglets → hypothalamic 5-HT/5-HIAA + behaviour under mixing stress
- 41371546 — dietary Trp → brain-region Trp metabolites in Göttingen minipig
- 42748216 — serotonin in **porcine and human tears** via contact-lens sensor (translatable peripheral biomarker)
- 20604989 — blood BDNF reflects brain BDNF "across species"

**Neuroinflammation — TRUNG BÌNH (khoảng trống lớn nhất)**
- 14651945 — ↑hippocampal IL-1β in isolated piglets (the only direct pig IL-1β+limbic+HPA link found)
- 42827140 — pig sepsis (Yorkshire, E. coli) snRNA-seq: vascular cell + glial activation, TNF signalling up, neurons minimally changed; authors cite "rodent models have limited translational applicability"
- 40146000 — pig cardiac arrest: hippocampal BBB disruption + neuroinflammation (scRNA-seq)
- 41206528 — 2-week piglets + cardiopulmonary bypass: microglial activation, BM-MSC intervention (randomised) → precedent for intervention/control neuroinflammation studies in piglets
- 27927261 — TNF-α + chromogranin A + cortisol as stress biomarkers in growing pigs
- 42606317 — porcine coronavirus PHEV → NLRP3/PANoptosis neuroinflammation
- **GAP: IL-6 in pig brain = KHÔNG CÓ NGUỒN.** Also no pig study uses neuroinflammation as the mediating mechanism for depression-like outcome.

**Gut–brain axis — CAO (mạnh nhất, khớp với SP tiêu hoá cho heo)**
- 31379533 — the stress model above is explicitly multidisciplinary at gut-brain + behaviour levels (fecal SCFA)
- 35027884 — germ-free piglets: region-specific ↓white-matter volume, ↓oligodendrogenesis
- 36211510 — human milk vs infant formula in Yucatan minipiglets: microbiota α-diversity, permeability, tryptophan metabolism
- 38029169 — porcine social stress model: 32 taxa changed (Treponema, Clostridium enriched; Prevotella depleted); explicitly framed as "a model for human health"
- 41713032 — heat-killed *B. fragilis* + FMT mouse model + weaning pig model
- 38539945 — multistrain probiotic to sows: **cortisol −50%, plasma serotonin +11%**, better human-animal relationship
- 42032216 — piglet-derived FMT/FVT given to mice: altered anxiety behaviour, ↑GABAR/BDNF, ↓CRHR1 (recipients are mice)
- 42051340 — maternal DHA → offspring microbiota → gut-brain (sow-piglet model)

**Neuromodulation — DBS/VNS mạnh, TMS mô phỏng, tDCS trống**
- DBS: 22967832 (STN + EN/GPi DBS → BOLD, pigs), 31697455 (NAcc DBS → prefrontal/limbic/thalamic BOLD), 32372021 (BOLD pattern classification), 40653083 (human stereotactic system in swine — title/DOI only, no abstract), 39340562 + 42133082 + 27994542 (target anatomy)
- TMS: 34891576 — **coil-design modelling only**; no in vivo pig rTMS study found
- tDCS: **KHÔNG CÓ NGUỒN** for pig brain (23636191/10543493/30608501 are spinal-cord MEP, aortic clamping, brain indentation — not tDCS)
- VNS: 41469406 (kilohertz HF block in swine, size-selective), 39183636, 40360488, 37276858, 42735697; 31354119 notes chronic VNS in pig

**Electrophysiology — TRUNG BÌNH (khả thi, chưa có biomarker trầm cảm)**
- 30959126 — **best**: pig EEG recorded cranially epidurally + wirelessly during human interaction; belly rubbing → ↓total power, ↑median/spectral-edge frequency = positive affective state
- 42604611 — UBE3A-deletion pig reproduces the human Angelman **delta-power** EEG biomarker → proves pig can replicate a human quantitative EEG biomarker
- 39133034 — **intracranial ERPs in pigs** across an LTP/cortical-excitability protocol (closest precedent for serial ERP in pig)
- 40876936 — piglet visual ERP (N1/P2, source localisation)
- 42243171 — kainic acid pig hippocampal epilepsy
- 41039113 — 1024-channel minimally invasive cortical array in **porcine models and cadavers**
- 37163609 — ECoG with soft robotic actuator
- **GAP: no EEG/LFP index validated to discriminate depression-like vs healthy pigs.**

**Limitations (all sourced)**
- 17027768 (no granular PFC layer IV); 34798047 (neurogenesis pig≠human); 17991496 (social defeat fails); 20193701 (authors doubt MDD validity); 37876629 (model score 0.57)
- 42615812 — "No single model captures the complexity of depression; reliance on isolated paradigms may contribute to translational failure"
- 40336488 — "significant challenges… complex psychiatric symptoms in non-human animals"
- 42600672 — face/construct/predictive/translational validity framework (rodent models)
- 42821421 — pig as underused large-animal model + full list of ethical/practical/infrastructure barriers (housing, handling, regulatory, surgical support, growth-related design constraints)
- 31354119 — "critical conclusion will brush the limitations of neurocognitive studies in the pig model… ethical concerns"
- 37626662 — pig as translational model for biobehavioural/neurotrauma research
- 38937838 (MIR137 KO minipig) and 25063429 (transgenic HD minipig) — precedent for pig genetic models, **but none for depression**
- 42375345 — unresolved xenotransplantation immune barriers

**Preprints (flag as NOT peer-reviewed, cite DOI only)**
- 10.64898/2026.04.22.720235 — Comparative mapping of pig/human brain homologies
- 10.1101/2020.10.13.337436 — Opening the Pig to Comparative Neuroimaging (common space)
- 10.21203/rs.3.rs-105759/v1 — Pig white matter atlas / common connectivity space
- 10.64898/2026.03.22.713463 — Germ-free piglets, prefrontal cortical microglia
- 10.1101/2025.10.21.683618 — BRD1 haploinsufficiency minipig

## Confirmed KHÔNG CÓ NGUỒN (do not invent these)
Pig gyrification index vs human · pig dexamethasone-resistance depression model · pig
learned-helplessness model · pig olfactory bulbectomy · pig depression gene knockout ·
IL-6 in pig brain · pig brain tDCS · in vivo pig rTMS · neuromodulation with a
depression-behaviour outcome in pig · validated depression EEG/LFP biomarker in pig ·
IL-1β/IL-6/TNF-α in pig brain as a microbiota→depression mediator · limbic
optogenetic/chemogenetic control in pig · quantitative CBG difference pig vs human ·
thalamic cytoarchitecture atlas pig vs human · pig model of DSM core MDD symptoms ·
any sensitivity/specificity validation of a pig model against human MDD.

## Research gaps worth occupying (stated in the deliverable)
1. Build a **DST non-suppression model in pigs** — DST + CRH challenge already works (34795321), nobody has published this as a depression model.
2. Develop a **depression-like EEG biomarker in pigs** — wireless epidural EEG is proven (30959126) and a human EEG biomarker was already replicated in pig (42604611).
3. Test **microbiota → SCFA → permeability → kynurenine → brain monoamine → behaviour** as one chain in pigs with a GI product — every link is separately measurable (31379533, 40823320, 38539945, 38029169, 35027884).
4. **Measure IL-6/TNF-α in pig brain** alongside the existing IL-1β (14651945).
5. Avoid extrapolating pig neurogenesis → human (34798047) and avoid social defeat in pigs (17991496).

## Deliverable shape used (reuse for 03b/03c)
Structured Q&A markdown, not the JSON row schema: checklist table up front → one `##`
section per question with inline `[PMID:...]` / `[DOI:...]` → confidence ratings
(CAO/TRUNG BÌNH/THẤP) with reasons → final cross-mechanism comparison table → numbered
`## References` → `## PHỤ LỤC` table listing every confirmed `KHÔNG CÓ NGUỒN` claim.
The appendix of honest gaps was the most-valued part; keep it.
