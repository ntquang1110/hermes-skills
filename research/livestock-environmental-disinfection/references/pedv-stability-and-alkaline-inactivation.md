# PEDV — Stability & Alkaline Inactivation (verified evidence bank)

Compiled 2026-10-22 while building `D:/Hermes Proj/virology-asf-ped/data/pedv.json`.
Every figure below was pulled from the primary source (Europe PMC `fullTextXML` / publisher PDF), not from a
secondary citation. Use this when defending an alkali-product claim against PEDV.

---

## 1. The claim to defend, and its verdict

> Internal doc: *"PEDV is NOT inactivated at pH 9.2 at 4 °C; the 8 log₁₀-in-30-min figure only holds at ≥40 °C
> (PMID 26602207)."*

**VERDICT: the claim is CORRECT and the PMID is REAL.** Verified verbatim from the abstract:

- **PMID 26602207** — *Sensitivity of porcine epidemic diarrhea virus (PEDV) to pH and heat treatment in the
  presence or absence of porcine plasma.* Vet Microbiol 2015. DOI 10.1016/j.vetmic.2015.10.010
  - *"Irrespective of presence of plasma, PEDV was not sensitive to pH 7.2–10.2 at 4 °C."* ← **the key sentence**
  - *"Virus-spiked plasma required heat treatment of 40 °C and alkalinization to pH 9.2 to achieve 8 log₁₀
    reduction within such time."* ← 8D < 30 min at pH 9.2 **only with ≥40 °C**
  - At pH 10.2 + 48 °C: 8D = 4.6 min (plasma), 15.2 min (MEM)

### ⚠️ Caveat you MUST attach to the 8 log₁₀ figure
The pH/heat study's inoculum was **5.5 log₁₀ TCID₅₀/ml**. A measured reduction can never exceed the starting
titer, so "8 log₁₀" is a **modelled 8D D-value** (time for 8 log reduction, extrapolated), **not an observed
reduction**. Anyone quoting "pH 9.2 → 8 log kill" as a measured number is misquoting the paper.

---

## 2. What actually kills PEDV with alkali (the decisive paper)

- **Stevens et al. 2018**, *Alkaline stabilization of manure slurry inactivates porcine epidemic diarrhea virus.*
  J Swine Health Prod 2018;26(2):95-100. DOI 10.54846/jshap/1059
  - **pH 10** (1.5 g hydrated lime/L slurry) for **1 h at room temperature → infectivity ELIMINATED**
    (swine bioassay: 0/3 pigs infected, no shedding) even though **RT-qPCR still detected 10⁵–10⁷ RNA copies/g**.
  - **pH 12** (2.5 g/L) for 12 h → RNA below detection.
  - RNA reduction: **2.16 log₁₀ (pH 10 / 1 h) → 4.66 log₁₀ (pH 12 / 1 h)**. Control un-limed = 9.16 log₁₀/g, 3/3 pigs infected.
  - All control pigs infected; bioassay is the validity anchor.
  - Mechanism proposed: alkaline pH compromises envelope integrity → released RNA hydrolysed.
  - Procedure/wastewater context: US EPA approves alkaline stabilization when **pH 12 is held ≥30 min**.
- **PMID 30389049** (France 2014 PED outbreak): liming **liquid manure to pH 12** → PEDV **undetectable by RT-PCR
  after 7 days**. ⚠️ RT-PCR endpoint only (RNA), not an infectivity endpoint.
- Cross-class support: **PMID 15350737** (Rabenau 2004) — SARS-CoV completely inactivated at **pH 12 and pH 14 for 1 h**;
  pH 5–9 had little effect regardless of temperature. **PMID 34455219** — strongly alkaline electrolysed water
  (chlorine-free) gave 2.9–5.5 log₁₀ in **30 s** against enveloped viruses incl. HCoV (not PEDV itself).

### ⛔ What is NOT known (do not invent)
No study was found that measures a **log₁₀ reduction of PEDV specifically at pH 13–14**. Any pH 13–14 PEDV claim is
**extrapolation** from (a) the pH ≥10 threshold above, (b) SARS-CoV pH 12/14 data, (c) envelope-lysis mechanism.
State it as inference and leave the number `null`.

---

## 3. pH window — the temperature gate

| Condition | Result | Source |
|---|---|---|
| 4 °C, pH **5.0–9.0** | stable | Hofmann & Wyler 1989, **PMID 2549681** |
| **37 °C, only pH 6.5–7.5** | stability window narrows sharply | **PMID 2549681** |
| 4 °C, pH 7.2–10.2 | **no inactivation** | PMID 26602207 |
| ~RT, pH 10, 1 h, manure slurry | infectivity gone | Stevens 2018 |
| pH < 4 and > 9 | complete loss of infectivity (reporting) | **PMID 25841898** |
| pH 1.6 (simulated gastric fluid) | **still infectious** — explains oral transmission | **PMID 42330810** |

**Lesson: alkaline kill of PEDV is temperature-gated.** pH 10 does nothing at 4 °C and everything at room temperature.
Never quote a pH for PEDV without its temperature + contact time.

---

## 4. Envelope / physicochemical

- **PMID 2549681** (Hofmann & Wyler 1989, Vet Microbiol): pleomorphic **enveloped** RNA virus, **~100–200 nm**,
  buoyant density 1.18; **lost infectivity on treatment with lipid solvents**; moderately stable at 50 °C;
  infectivity **depends on trypsin**. → PEDV is a **lipid-enveloped virus: sensitive to soap, detergents, chloroform/ether**.
- Pospischil et al. 2002 (J Swine Health Prod 10(2):81-85) — ⚠️ **non-peer-reviewed diagnostic note, flag it**:
  ether- and chloroform-sensitive; 90–190 nm; club-shaped projections ~20 nm; growth depends on trypsin.
- **PMID 25841898** (Jung & Saif 2015) lists inactivating agents: **2 % sodium hydroxide**, **sodium carbonate
  4 % anhydrous / 10 % crystalline + 0.1 % detergent**, bleach, Virkon S, phenolic compounds, formaldehyde,
  glutaraldehyde, iodophors in phosphoric acid, ionic/non-ionic detergents, **chloroform**.
- **PMID 26072369** (Baker 2015, Vet Microbiol) — 5 disinfectant classes (phenol, QAC, sodium hypochlorite 0.17–2.06 %,
  potassium peroxymonosulfate 0.5 %, QAC+glutaraldehyde) at 37/4/−20 °C with and without 10 % swine faeces:
  **no infectious PEDV recovered in any group**; hypochlorite + peroxymonosulfate best at degrading RNA.

---

## 5. Heat

| Matrix | Condition | Outcome | Source |
|---|---|---|---|
| Feed ingredients (D-value, per log) | 60 °C 4.4 min · 70 °C 3.7 · 80 °C 2.4 · 90 °C 2.3 | max 3.9 log at 90 °C/30 min | **PMID 28932412** |
| Feces on metal surface | **71 °C / 10 min** OR **20 °C / 7 days** | sufficient | Thomas 2015, JSHAP 23(2):84-90 |
| Feces on metal surface | **63 °C / 10 min** | **NOT sufficient** | Thomas 2015 |
| Heated water | ≥76 °C / 10 s | inactivates | **PMID 32289093** |
| Complete feed | 58 d at 23.9 °C | no infection | **PMID 38338036** |

⚠️ Conflict to note: generic coronavirus guidance ("60 °C for 10–15 min", e.g. PMID 15350737 for SARS-CoV) is
**not sufficient for PEDV in faeces** — the organic matrix protects it. Organic matter is the confounder.

---

## 6. Environmental persistence

| Matrix | Persistence | Source |
|---|---|---|
| Earthen manure storage / lagoon | **up to 9 months**; survival independent of temperature and pH within pH 6.6–8.3; ~1.1×10⁵ copies/ml | **PMID 27014197** |
| Pig slurry | long-term survival, warm + cold seasons | **PMID 34357980** |
| Seawater 24 °C | infectivity lost after 7 days | **PMID 37395665** |
| Seawater 4 / 8 °C | ~5 % / 12 % drop by day 16 | **PMID 37395665** |
| Water (systematic review) | median ~22 days; outliers to 1095 days | **PMID 41229689** |
| Fresh faeces | >7 d; slurry 14 d RT, 28 d at 4 °C | Goyal 2013, cited in **PMID 27014197** |

---

## 7. Comparative notes (TGEV / PDCoV) — for the "beta vs alpha" framing

- PEDV, TGEV, PDCoV all share the same clinical endpoint (villous atrophy → watery diarrhoea) but PEDV is
  **Alphacoronavirus**, PDCoV is **Deltacoronavirus** — relevant because alkaline/envelope sensitivity tracks
  envelope class, not genus.
- APN/CD13 (porcine aminopeptidase N, 150 kDa) was identified as the **TGEV** receptor (Delmas 1992, **PMID 1350661**)
  and was proposed for PEDV, but **porcine APN may not be the major PEDV receptor** (**PMID 32502552**) — don't
  state APN as settled fact for PEDV.
- Genogroups: **G1 (classical, incl. S-INDEL G1b, milder)** vs **G2 (non-S-INDEL G2b, epidemic, highly virulent;
  mortality up to 100 % in neonates)** — PMID 41653521, 32502552.

---

## 8. Reporting convention that triggered this work

`data/` holds one JSON per pathogen with a fixed schema; every number carries `nguon` (PMID/DOI/WOAH/URL + year),
unverifiable numbers are `null`, and conflicting sources are both recorded with the conflict named in `ghi_chu`.
`PMID 41557730` was **guessed** during that session and turned out to be an unrelated paper — it was dropped.
**Always resolve a PMID with a lookup before citing it; never write a plausible-looking one from memory.**
