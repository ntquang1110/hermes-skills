# Processing Protocol Evaluation — Herbal Feed Additives

## When to use

When a user has an existing or proposed processing protocol for a herbal feed additive and needs:
1. Scientific evidence review (PubMed, patents) for the process
2. Risk identification (pH, moisture, microbial, chemical interactions)
3. Protocol improvement recommendations backed by evidence

## Workflow

1. **Understand the current process** — ingredients, ratios, steps, observed problem
2. **Identify the core problem** — mold, efficacy, stability, palatability
3. **Research each component**:
   - Plant material — active compounds, known issues (PubMed)
   - Processing method — patents, industry standards
   - Preservatives — pH requirements, efficacy conditions
   - Target species — dosage, safety data
4. **Cross-reference with patent landscape** — Google Patents XHR or Espacenet
5. **Identify risks and rank** (Cao / TB / Thấp) with evidence
6. **Propose improvements** — practical, implementable changes

## Key risk categories

| Risk | What to check | Evidence source |
|---|---|---|
| pH compatibility | Preservatives (K-sorbate needs pH < 6.0; Na-benzoate needs pH < 4.5) | PMID 41427128 |
| Moisture control | Dry powder < 10% moisture for mold safety | General food science |
| Sugar type | Refined sucrose != raw sugar — pure sucrose lacks nutrients for fungi | User correction (09/2026) |
| Active compound stability | Berberine stable to 150°C; sorbate/benzoate stable to 120°C | PubChem |
| Ingredient interactions | Berberine has antifungal activity in pig feed (PMID 42646776) | PMID 42646776 |
| Dosage safety | Start low, increase gradually — berberine can stimulate peristalsis | PMID 34358871, 32204369 |
| Storage | Vietnam humidity (70-85%) needs moisture-proof packaging + desiccant | — |

## Common pitfalls

- Assuming all sugars feed mold — refined sucrose (>= 99.9%) has negligible nutrients for fungi. The real mold risk is water + plant fiber, not sugar.
- Assuming preservatives work at any pH — K-sorbate and Na-benzoate are nearly inactive at neutral pH. Always check/adjust pH.
- Overlooking that berberine itself has antifungal activity — PMID 42646776 shows berberine inhibits Fusarium in pig feed. This helps preservation but is not sufficient alone.
- Not drying after adding liquid — any water added to plant material creates mold risk. Must re-dry to < 10% moisture.
- Ignoring the plant's own chemistry — hoang dang contains CYP3A4 inhibitors (PMID 17994707) — relevant for drug interaction at high doses.

## Patent search patterns (Google Patents XHR)

Sleep >= 3s between queries to avoid throttle. If 503, fall back to Espacenet browser.

## Verified patents (berberine feed processing)

| Patent | Title | Relevance |
|---|---|---|
| CN109362953A | Coating type berberine additive for feed for piglets | Direct: berberine dry powder for pig feed |
| KR20260056394A | Composition comprising extract of Akar Kuning (Fibraurea tinctoria) | Same plant species |
| AU2024213117B2 | Berberine alkaloid formulations for animal disease | Berberine in animal feed |
| WO2021072473A1 | Antimicrobials as feed preservatives (berberine-based) | Berberine as preservative |

## Output format

Write a structured review with:
1. Summary of user's current process
2. Verified evidence (PubMed + patents) for each step
3. Risk table with severity (Cao/TB/Thap)
4. Practical improvement recommendations
5. Full reference list with verified PMIDs
