# Gap Prioritization Heuristics for Mature KFs

When the research queue is empty and systematic gap detection (see `gap-finding-ghost-topics.md`) produces **multiple candidate gaps**, use these heuristics to pick the most valuable topic to research next.

## Priority tiers (for swine-nutrition domain)

### Tier 1 — Practical feed additives & interventions
Create cards for **compounds and additives the user can actually apply**:
- Organic acids, essential oils, MCFAs, prebiotics, postbiotics
- Directly actionable: dose tables, cost estimates, stage-specific recommendations
- Connect to existing cards about gut health, microbiota, weaning stress
- Usually yield 15-25+ relevant PubMed results (applied research is abundant)

### Tier 2 — Signaling pathways with direct nutritional modulation
- Pathways that feed additives or nutrients directly modulate:
  - Nrf2/KEAP1 (antioxidant), NF-κB (inflammation), mTOR (protein synthesis)
  - AhR (tryptophan metabolism), GPR43 (SCFA sensing)
- These have clear "lever" (what to feed) → "outcome" (what changes) logic

### Tier 3 — Fundamental immunology / cell biology
- Cytokine families, developmental pathways, cell types
- Valuable for deep understanding but harder to translate into daily feeding decisions
- Pick these when Tiers 1-2 are exhausted or when the pathway is referenced in 10+ existing cards

### Tier 4 — Molecular tools & biotechnology
- CRISPR, gene editing, lncRNA, circRNA
- Interesting but rarely connect to existing feed-additive cards
- Lowest priority for a swine-production knowledge base

## Domain-specific priority mapping

| KFlow topic_slug | Example KF | Top priority | Lower priority |
|-----------------|-----------|-------------|----------------|
| `chan-nuoi-heo` | Swine nutrition & health | Feed additives, gut health mechanisms | Developmental biology, molecular tools |
| `sinh-hoc` | Biology & immunology | Signaling pathways, immune cell biology | Applied feed additives |
| `nghien-cuu` | General research | Whatever has strongest paper support | N/A |

## The "NF-κB false alarm" — critical keyword spelling pitfall

When doing title-based gap detection with Python keyword matching, **Greek letters in pathway names cause silent false positives**:

```python
# BAD — misses existing cards:
gap_candidates = {'nfkb': ['nf-kb', 'nfkb']}  # misses "NF-κB" (Greek κ)

# GOOD — catch all spelling variants:
gap_candidates = {'nfkb': ['nf-kb', 'nfkb', 'nf-κb', 'nf kappa', 'nuclear factor']}
```

**Affected pathways with special characters:**

| Pathway | Latin spellings (works) | Greek spellings (silent miss) |
|---------|------------------------|-------------------------------|
| NF-κB | nf-kb, nfkb, nf kappa | nf-κb (κ = U+03BA) |
| TGF-β | tgf-beta, tgf b | tgf-β (β = U+03B2) |
| IL-1β | il-1beta | il-1β |
| JAK-STAT | jak-stat, jak stat | (no Greek, safe) |
| NLRP3 | nlrp3 | (no Greek, safe) |
| Notch | notch | (no Greek, safe) |
| AMPK | ampk | (no Greek, safe) |

**The fix:** always include Latin transliterations in keyword lists. When in doubt, also check the full name (e.g. "nuclear factor kappa B" for NF-κB).

## The "re-verify your gaps" step

After the keyword scan produces a gap list, **re-verify each candidate** with a manual title glance:

```bash
curl -s http://localhost:3003/api/cards | python -c "
import sys,json
cards = json.load(sys.stdin)
# Print titles containing ANY of these character variants
variants = ['nf-kb', 'nfkb', 'nf-κb', 'nf κ', 'nf kappa', 'nuclear factor']
for c in cards:
    t = c['title'].lower()
    for v in variants:
        if v in t:
            print(f'{v}: {c[\"title\"][:90]}')
            break
"
```

This catches false negatives from the initial scan.

## Quick decision matrix

When choosing between two gap candidates, ask:

| Question | Pick A if... | Pick B if... |
|----------|-------------|-------------|
| Which has more PubMed results? | Practical topics (organic acids, probiotics) | Niche pathways (Hedgehog, Notch) |
| Which connects to more existing cards? | Ghost topics (referenced in 5+ cards) | Novel topics (0 existing connections) |
| Which yields actionable output? | Dose tables, cost estimates, feed recommendations | Pathway diagrams, mechanism descriptions |
| Which serves the user's domain? | Swine nutrition & health | General molecular biology |

**Default for swine-nutrition KF with 200+ cards:** Always check Tier 1 (practical feed additives) first. Only go to Tiers 3-4 when Tiers 1-2 are exhausted or explicitly requested.
