# In-vivo biosensor resolution layers — verified PMID bank (18/10/2026)

Verified evidence bank for the fixgby series doc `07a-research-cam-bien-invivo-theo-do-phan-giai.md`
(repo `D:/Hermes Proj/fixgby`). Companion to `03a-research-heo-vs-nguoi-findings.md` (101 PMID)
and `06a-research-do-trung-khop-co-quan.md` (62 PMID). **101 PMIDs, all batch-validated.**

Question answered: *"device nằm trong cơ thể đọc tín hiệu tế bào bằng cách nào, và làm sao biết
VẤN ĐỀ ĐANG NẰM Ở ĐÂU trong cơ thể của từng người?"* — a question about **physical/biological
limits**, not about product features. Reuse this bank for the same ladder in later docs.

## The grading axis: tri-state (I)/(A)/(R)

Distinct from the `evidence_level` (Mạnh/Vừa/Sơ bộ) used for compound×effect rows. For
**capability/device** research the useful axis is where the thing physically exists:

- **(I)** = already commercial / already done ON HUMANS
- **(A)** = done on LARGE ANIMALS (non-human primate, pig, dog)
- **(R)** = in-vitro / in-silico only

Write all three per layer even when two are empty — `(I) KHÔNG TỒN TẠI` is a finding.

## Layer ladder — the numbers that carry the argument

| Layer | Highest verified state | Key numbers | PMID |
|---|---|---|---|
| 1 Whole-body / skin wearable | **(I)** commercial, FDA-clear | Apple Watch living meta 82 studies / 430,052 participants; HR bias −0.27 bpm (LoA −7.19..6.64); AF sens 0.79 / spec 0.91; SpO2 bias −0.04% but LoA −4.00..3.94 | 41513748, 42218208, 42551497, 41812085, 41413090 |
| 1 — limitation | pigmentation confound | pulse-ox confounded by skin pigmentation; occult hypoxemia | 42028256, 42105110 |
| 2 ISF / transdermal microneedle | **(I)** short windows only | lactate 21 participants, r=0.94, AUC 0.95, bias −0.028 mmol/L, range 0.7–22.9 mmol/L, 4 h; phase I n=5 lag 5 min (IQR −4..11); levodopa MARD 9.64%; first-in-human penicillin 6 h; cytokine response 1–4 h (LOD 0.54 pg/mL) | 41636637, 40979517, 42687276, 33323208, 36857411 |
| 2 — animal / frontier | **(A)** | E-AB in ISF (rat), methotrexate R²=0.85, BICEP dual blood+ISF kanamycin with **individualized** delays, hydrogel-protected E-AB | 35653647, 42312165, 42160425, 37703911, 42480443 |
| 2 — reviews / limit | small accessible dermal ISF volume, slow turnover | protein monitoring in ISF = unsolved; E-AB long-term only week-scale | 42654043, 42776934, 41725414, 37128505, 42801709 |
| 3 CGM (glucose, ISF) | **(I)** commercial — **highest continuous MOLECULAR layer on humans** | measures glucose in **ISF of subcutaneous fat, NOT inside cells**; enzyme-electrode; lag **9.5 min (SD 3.7)**, median 9; MARD 8.66%, 15 days; biofouling MARD 16.75% vs 9.69% coated | 33359497, 26243773, 42823091, 35929159, 26958100, 40014948 |
| 4 Organ implant | **(I)** | CardioMEMS: CHAMPION n=550 RCT, HFH 0.31 vs 0.44; COAST n=304 / 37 centres / 6 countries / 2 yr, 98.3% success, 0 DSRC, HFH 517→144 (−69%). Cerebral microdialysis (CMD): 33 studies, glucose/lactate/pyruvate/LPR/glutamate/glycerol in **brain ISF**. Sensor stent = (R) only. | 21315441, 41929392, 42733577, 41975464, 40055196, 38385936, 41912492 |
| 5 Optical in-tissue (fiber photometry / FRET) | **(A)** only — **NOT on humans** | fiber photometry + fluorescent dopamine sensor in **monkey** striatum; GCaMP/FRET rodent; photoacoustic FRET mouse. Genetically encoded ⇒ needs gene transfer ⇒ no human path. | 40080638, 42785985, 34533889, 36471162 |
| 6 **Intracellular molecular, in-vivo, human** | **KHÔNG TÌM THẤY** | Document the negative queries (S6a–S6f; 0 in-vivo-human hits). Nearest work is all **(R)**: nanopipette intracellular pH / superoxide / glutathione in cultured cells. | 32542257, 39821328 (+0-result queries) |
| 7 Neuron electrical | **(I)** but ACUTE (operating room) | Neuropixels: **685 neurons / 9 sites** human STG; 56 patients intraoperative, tungsten gets 1–2 neurons, Neuropixels +1 order; first-in-human probe (explicitly NOT yet approved as a research device). Stentrode vECoG chronic: 2 ALS, low-gamma DoM 125.41±17.53% (P1) vs 22.77±4.09% (P2), SNR min 1.72 dB. **Neuropixels intraoperative is the ONLY 0-order-of-magnitude spatial result — and it is ELECTRICAL, never molecular.** | 38093008, 40882239, 37697108, 40048825, 36639237 |
| 7 — electrical ≠ molecular | structural proof | The existence of a dedicated **512-channel dual-mode** microchip for simultaneous electrophysiology + neurochemistry proves a normal electrode does both by default — it does not. | 37232863 |
| 8 cfDNA/cfRNA/proteomics from blood | **(I)** commercial, NOT continuous | Sun et al PNAS 2015 methylation tissue mapping; cfSort deep learning = **29 tissue types**, 521 samples; nucleosomal size deconvolution; 10 mL blood → 4–5 mL plasma → 5–10 ng/mL ctDNA, half-life 16 min – 2.5 h; organ-specific plasma proteomics aging. Achieves **TISSUE** resolution, never cell resolution. | 26392541, 37399400, 42103785, 42016306, 41136388, 36915242, 39477866 |

## The dilution / identifiability core (Part B of 07a)

- **Total cells in the human body = 3.72 ± 0.81 × 10¹³** (Bianconi, Ann Hum Biol 2013) — the
  denominator that makes "one blood draw → whole-body signal" a 13.6-order-of-magnitude problem. PMID 23829164.
- Body fluid compartments (ICF/ECF/interstitial/plasma split) — PMID 31300092.
- ctDNA absolute vs tumour-fraction **discordance** during therapy = the dilution phenomenon, measured — PMID 42225541.
- **The hard math:** mechanistic pathway models (JAK-STAT / MAPK / NF-κB) are **"NOT IDENTIFIABLE
  even under the strong assumption that ALL system state variables are measurable"** — PMID 19426527.
  ⇒ the intracellular gap is a **mathematical** gap, not an engineering one. Supporting:
  structural identifiability reviews — PMIDs 27792726, 22132135, 29186132, 30472690.
- PET upper bound on in-vivo molecular spatial resolution: 2 µL / 1.2 mm detectors ⇒ ~10⁶ cells per
  voxel — still 6 orders off a cell. PMID 40998724.
- Snapshot-only signalling readouts: phosphoproteomics needs **hundreds of cells** and lysis ⇒
  destroyed tissue ⇒ no continuous human read of kinase activity (benchmarKIN; PhosX; single-cell
  phosphoproteomics on a patient-derived **model**, not a living patient) —
  PMIDs 40404650, 39563468, 41275010, 27070703.

## Quantified conclusions (the reusable headline numbers)

1. Highest **continuous molecular** layer on humans = **Layer 3 (CGM)**: MARD 8.66%, lag 9.5 min,
   15 days. Distance to single cell = **5–7 orders** (10⁵–10⁷ cells → 1 number).
2. Best **whole-body spatial** layer = wearable, **13.6 orders** (3.72×10¹³ cells → 1 number).
   cfDNA deconvolution shortens this to **≈12.1 orders** and **cannot improve further** — bounded
   by the number of tissues with distinct methylation profiles (29).
3. **Intracellular** distance = **infinite / no order defined** — Layer 6 does not exist, and
   PMID 19426527 says more external channels cannot close it.
4. **Electrical** axis has genuinely reached **0 orders** on humans (Neuropixels, 685 neurons) —
   which is why "we already read cellular signals in humans" is *technically true and
   semantically false* if read as "we know what the cell is doing biochemically".
5. **Layers satisfying all 5 conditions (intracellular + continuous + molecular + human + spatial
   coordinates) = 0.**

## Project-conversion answers used in Part D

- Highest layer a 1–2 person project can *touch* in 12–24 months = **Layer 3 (CGM)**, paired with
  **Layer 8 (cfDNA)** for tissue coordinates. Neither gives cell coordinates or intracellular state.
- Going up to Layer 2 self-built needs: cleanroom/microfabrication partner, multi-channel
  potentiostat, IRB + hospital. Evidence that 12–24 months only reaches (R)→(A): the existing
  human studies are explicitly *phase I n=5*, *first-in-human "proof-of-concept"*, and *pilot n=21*.
- Layer 4 is out of reach for 1–2 people on **scale** grounds alone (COAST = 304 patients / 37
  centres / 6 countries / 2 years).
- Any cost figure not sourced from a paper was written `CHƯA CÓ NGUỒN (tag H)` rather than estimated.

## Pitfalls hit while building this doc

- **Neuralink has no peer-reviewed human publication.** Company updates + ClinicalTrials.gov
  registry only. Write that explicitly instead of reaching for a weak citation.
- **`grep 'PMID: [0-9]*'` misses table-cell PMIDs** — see
  `scripts/validate_pmids_batch.py`; this session's own first check validated only 40 of 101.
- A `write_file` call whose content renders as `[truncated]` in the transcript may still have
  written the full payload — verify with `wc -c` + a heading grep before assuming truncation.
