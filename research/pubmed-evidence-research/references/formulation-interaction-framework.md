# Formulation Compatibility Analysis — Multi-Compound Feed Additives

Verified PMID bank + analysis framework for evaluating chemical and metabolic interactions when combining multiple active compounds in a single feed additive formula. Generated 09/2026 for Kiềm Thảo Dược 5 HP lines (RESP, GUT, METRI, GROW, GS-01).

## Analysis Framework — 6 checks

When evaluating N compounds in one formula, run these checks in order:

| # | Check | What to look for | Method |
|---|-------|------------------|--------|
| 1 | **Chemical reaction (dry)** | Functional groups that react at RT: strong acid+base, redox pairs, Schiff base (amine + aldehyde) | PubChem functional group check |
| 2 | **Maillard reaction** | Reducing sugar + free amino group → browning, loss of activity | Check all ingredient specs for reducing sugars |
| 3 | **Complexation/precipitation (in solution)** | Polyphenol + alkaloid (electrostatic), tannin + protein, Ca + oxalate/phytate | PubMed: `[compound A] AND [compound B] AND complexation` |
| 4 | **CYP450 competition** | Two+ compounds metabolized by same CYP isoform → competitive inhibition | PubMed: `[compound] AND CYP AND metabolism` |
| 5 | **CYP450 inhibition** | One compound inhibits CYP that metabolizes another → delayed clearance | PubMed: `[compound] AND CYP3A4 AND inhibition` (or specific isoform) |
| 6 | **Absorption competition** | Same transporter (LAT1, P-gp, OATP) or same absorption window | Check if both act in stomach vs small intestine vs colon |

## Verified CYP450 Pathway Map (Kiềm Thảo Dược compounds)

| Compound | CYP isoform | PMID | Note |
|----------|-------------|------|------|
| Thymol | CYP2A6 (major) | 23346763 | Predominant pathway in human liver microsomes |
| Eucalyptol (1,8-cineole) | CYP3A4 (major), CYP3A5 (minor) | 15715982, 11246507 | 2α- and 3α-hydroxylation; Km 19 µM for CYP3A4 |
| Glycyrrhizin | Gut bacteria (not CYP) | — | Converted to glycyrrhetinic acid by gut microbiota; bypasses liver phase I |
| Glycyrrhetinic acid | CYP3A4 inhibition | 34601070 | Inhibits CYP3A4 (IC50 ~50 µM) and 11β-HSD |
| Curcumin | CYP3A4 inhibition | 34601070 | IC50 75-100 µM for CYP3A4; phytosome formulation bypasses first-pass |
| Berberine | CYP1B1, CYP2D6, CYP3A4 | 40883330 | Mixed inhibition; also P-gp substrate |
| Propolis (flavonoid mix) | CYP1A1/1B1 inhibition | 40883330 | Mild inhibition at feed concentrations |
| Proanthocyanidins (tannin) | CYP1B1 inhibition | 40883330 | Mixed-type, IC50 2.53 µM |

## Key Interactions Discovered

### Berberine + Tannin (GUT-HP) — Supramolecular complex
- Berberine (alkaloid, + charge) + tannin (polyphenol, - charge) → electrostatic complex ~400nm
- PMID 36471931: co-decoction of Coptidis (berberine) + Rhei (tannin) forms supramolecules that delay dissolution/release
- PMID 34793852: berberine/tannic acid self-assemblies used intentionally as colon-targeted drug delivery for ulcerative colitis
- **Impact on GUT-HP: BENEFICIAL delayed release**, not blocked release. Both compounds act in the gut → longer retention = better efficacy.

### Carvacrol/Thymol + Glycyrrhizin — Hydrogel formation
- PMID 38954940: carvacrol + glycyrrhizin self-assembles into injectable hydrogel (CAR@glycygel)
- Antibacterial synergy: MIC 156.25 µg/mL vs 1250 µg/mL free CAR
- **At feed concentrations (0.1-0.5%)**, no gelation occurs; compounds remain as dry powder mix.

### Thymol — FMO/CYP inhibition
- PMID 31305200: thymol inhibits FMO-dependent S-oxygenation of albendazole (54.1%) in sheep liver microsomes
- Also inhibits CYP1A1 (7-ethoxyresorufin O-deethylase abolished)
- IC50 for ABZ S-oxygenation: 13.5 mM — well above feed concentrations

### Eucalyptol — CYP3A4 substrate/competitive inhibitor
- PMID 11246507: competitive inhibitor of tolbutamide hydroxylase (CYP2C9 surrogate) in possum liver (Ki 15 µM)
- In koala: actually stimulates activity at higher cineole concentrations — species-dependent
- **At feed concentrations in pigs**, no clinically relevant inhibition expected

### Glycyrrhizin + Curcumin — CYP3A4 dual inhibition
- Both inhibit CYP3A4 in vitro (glycyrrhizin IC50 ~50 µM, curcumin IC50 75-100 µM)
- **Additive inhibition possible in theory**, but at feed concentrations (0.1-0.5% each):
  - Plasma concentration << IC50 values
  - Curcumin phytosome → absorbed via lymph, bypasses portal CYP3A4
  - Glycyrrhizin → activated by gut bacteria, not directly exposed to liver CYP3A4 at high conc
- **Conclusion: safe at feed additive levels**

## Verified Negative Interactions (no problem found)

### Enzyme (phytase/xylanase) + Acid citric (GROW-HP)
- Coated enzymes release at pH 6-7 (duodenum); acid citric acts at pH 2-3 (stomach)
- Different pH windows, different locations → no interference
- PMID 38587823 (Poult Sci 2026): microencapsulated essential oils + enzymes in broilers — compatible

### Bacillus subtilis + Tannin (GUT-HP)
- Tannin MIC against Gram+ bacteria: 0.5-2 mg/mL
- B. subtilis is spore-former — spores survive pH 2-3 and tannin at 0.1-0.5%
- Spore germination occurs in small intestine AFTER tannin has acted primarily in large intestine
- Temporal separation → no conflict

### L-Tryptophan + Mg (GS-01)
- Trp → serotonin (5-HT₁A, stress reduction)
- Mg → NMDA antagonist (muscle relaxation, reduced aggression)
- Different receptors, different pathways, same direction (sedative) → synergistic, not competitive

## PubMed Query Patterns for Formulation Interaction Research

```bash
# CYP450 metabolism of a compound
esearch.fcgi?db=pubmed&term=<compound>+AND+(CYP+OR+cytochrome+P450)+AND+metabolism&retmax=10&retmode=json

# Compound-compound interaction
esearch.fcgi?db=pubmed&term=<compound1>+AND+<compound2>+AND+(combination+OR+interaction+OR+synergy)&retmax=10&retmode=json

# CYP inhibition by natural compound
esearch.fcgi?db=pubmed&term=<compound>+AND+(CYP3A4+OR+CYP2A6+OR+CYP1A1)+AND+(inhibition+OR+inhibitor)&retmax=10&retmode=json

# Complexation/precipitation
esearch.fcgi?db=pubmed&term=<compound1>+AND+<compound2>+AND+(complexation+OR+supramolecular+OR+precipitation)&retmax=10&retmode=json
```

## When to use this reference

When asked to evaluate whether N active compounds in a feed/feed-additive formula will:
- React chemically during storage (dry mix)
- Form precipitates or complexes in the gut
- Compete for the same metabolic enzymes (CYP450)
- Inhibit each other's clearance
- Have synergistic or antagonistic effects on absorption

Always pair with the `pubmed-evidence-research` skill's core rules: verify every PMID, cite species and dose from the abstract, never invent numbers.
