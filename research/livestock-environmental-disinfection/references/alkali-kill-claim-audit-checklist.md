# Auditing an "alkali kills pathogen X" claim

Reusable checklist for any pH 13-14 (or any disinfectant) efficacy claim, human- or document-sourced.
Derived 2026-10-22 from verifying a PEDV claim against `references/pedv-stability-and-alkaline-inactivation.md`.

## The five questions every kill number must answer

A "log reduction" figure is only meaningful with all five of these stated. If a source, an internal doc, or a
sales claim omits any of them, the number is not usable yet.

1. **pH** — plus the *held* pH, not the pH of the concentrate. Organic load drives the on-surface pH down.
2. **Temperature** — alkaline kill is temperature-gated. PEDV at pH 10: no effect at 4 °C, infectivity
   eliminated at room temperature (PMID 26602207 vs Stevens 2018). Never accept a pH without its temperature.
3. **Contact time** — report the wet-contact time, not the spray time.
4. **Matrix** — clean surface vs faeces/serum/slurry/feed. Organic matter neutralises alkali *and* protects
   virus from heat. ASFV in serum survives 7 days at pH 14; PEDV in faeces survives 63 °C/10 min but not 71 °C.
5. **Endpoint** — infectivity assay (bioassay, TCID₅₀, egg inoculation) vs molecular detection (RT-PCR/qPCR).
   These diverge sharply: PEDV in limed slurry showed 10⁵–10⁷ RNA copies/g with **zero** infectivity by swine
   bioassay. A qPCR "kill" claim is not a kill claim.

## Number-integrity checks

- **A reduction cannot exceed the starting titre.** Read the study's inoculum. PEDV's famous
  "8 log₁₀ at pH 9.2 in 30 min" comes from a study whose inoculum was 5.5 log₁₀ TCID₅₀/ml → the 8 log₁₀ figure
  is a **modelled 8D D-value** (extrapolated time for 8 log), not an observed reduction. Say so.
- **D-value ≠ log reduction.** A D-value is time-per-log; "8D < 30 min" means *8 log per that time*, modelled.
- **Check the temperature of the "30-second kill" studies.** A large share were run at 60 °C, not barn
  temperature (e.g. PMID 10208725: NaOH 1.0 M at 15 °C did *not* rapidly inactivate hepatitis A).
- **Resolve every identifier before citing it.** During the PEDV session an identifier was written from memory
  and turned out to be an unrelated paper. Never emit a plausible-looking PMID/DOI from recall — look it up.

## Source-quality flags to carry into the deliverable

- Mark **non-peer-reviewed** items explicitly when they carry a number (diagnostic notes, conference
  proceedings, trade-magazine summaries).
- Do not invent institutional sources. PED is **not** on the WOAH List of Diseases → there is no WOAH
  Terrestrial Manual chapter for it; only the WOAH disease page and factsheet exist.
- Where two sources conflict, record **both** and name the confounder in the note. In this class of work the
  confounder is almost always **temperature** or **matrix**, not a genuine disagreement.
- Genuine evidence gaps must be stated as gaps, with the field left `null`. "No study measures PEDV log
  reduction at pH 13-14" is a finding; a plausible extrapolated number presented as measured is a fabrication.
