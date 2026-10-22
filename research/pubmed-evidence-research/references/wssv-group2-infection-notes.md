# WSSV Group 2 — Infection / Replication / Immunity (verified PMID bank)

Session 2026-08-16. Deliverable: `group2_infection.json` (7 topics, 44 facts, **32 unique PMIDs**, all efetch-verified).
Complements `references/wssv-group3-survival-notes.md` (survival/transmission/epidemiology). Reuse for Groups 4+.

## Classic-paper mapping corrections (briefs cite wrong metadata — verify, don't trust)
- "Huang 2014 (clathrin)" → actually **Huang J et al. 2015, Virology, PMID 26397221** (clathrin-mediated endocytosis in crayfish HPT cells; CPZ inhibits, genistein doesn't) AND **Huang ZJ et al. 2013, Fish Shellfish Immunol, PMID 23747417** (hemocytes; MβCD/cholesterol blocks entry → caveolae route).
- "Yi 2004 (VP28)" → **Yi G et al. 2004, J Biochem Mol Biol, PMID 15607033** (VP28-EGFP binds shrimp cells; anti-VP28 neutralizes; competition ELISA).
- "Flegel 2007" → **Flegel TW 2007, Dev Comp Immunol, PMID 16970989** (viral accommodation).

## Working query patterns (esearch, retmax=8–10)
- `Huang[Author] AND clathrin AND "white spot syndrome virus"`
- `Yi[Author] AND VP28 AND shrimp`
- `Flegel[Author] AND accommodation`
- `Robalino[Author] AND "double-stranded RNA"`
- `whispovirus[Title]` (→ Leu 2009 review, PMID 19216439)
- `Corteel[Author] AND WSSV`, `Panyim[Author] AND (RNAi OR silencing) AND WSSV`
- `cholesterol AND "white spot syndrome virus" AND entry`
- `"white spot syndrome virus" AND (per os OR waterborne OR oral) AND transmission`

## Verified PMID bank (by subtopic)
**Entry routes:** 19201551 (Corteel 2009, Vet Microbiol — molt stage + cuticle damage ↑ immersion susceptibility; IM route unaffected), 33097672 (De Gryse 2020, PNAS — antennal gland/nephrocomplex = major portal, cuticle-free regions), 37766231 (Cox 2023, Viruses — peroral → death ≤78 h; shedding from 6 h post-onset, peak 12 h after death; water/feces/molts infectious), 31019127 (Blaylock 2019, DAO — oral vs injection in blue crabs, 2.6×10⁹ copies/mg tissue), 17432037 (Escobedo-Bonilla 2007, DAO — oral route, first infected cells 12–18 hpi).
**Clathrin/VP28 entry:** 26397221, 23747417 (above), 27385304 (Chen 2016, Sci Rep — multiple endocytic routes: CME + macropinocytosis + caveolae all required; Cq-GABARAP facilitates CME), 26988289 (Wang XF 2016, FSI — clathrin coat AP17/σ-AP-2 in L. vannamei), 15607033, 11437657 (van Hulten 2001, Virology — VP28 surface envelope, antiserum neutralizes dose-dependently), 39537865 (Sudsat 2024, Sci Rep — VP28 binds PmRab7, Kd 22.5 nM WT, nucleotide-state-independent), 18214608 (Ongvarrasopone 2008, Mar Biotechnol — dsRNA-PmRab7 inhibits WSSV + YHV).
**Nuclear replication:** 19216439 (Leu 2009 — ~300 kbp dsDNA, replicates in nucleus, lytic, ≥181 ORFs), 35638850 (Li DL 2022, J Virol — actin nucleation + CME, endosome fusion, microtubule transport, importin α1/β1 + Ran nuclear import), 19596390 (Attasart 2009, Virus Res — dsRNA vs ie1/ie3/pol/rr2/vp26/vp28; protection rr2>ie3>vp26,vp28>ie1>pol), 37108688 (Huang HJ 2023, IJMS — TEM/Cryo-EM: stout-oval virion, portal cap + closed base, C14 symmetry), 18086030 (Escobedo-Bonilla 2008, J Fish Dis review — since 1992, >$7B losses).
**VP28 vaccine/RNAi:** 21345339 (Mejía-Ruíz 2011, JIP — dsRNA vp28 LT50 145 h @10 dpt, 765 h consecutive; survivors less susceptible), 14747570 (Witteveldt 2004, J Virol — oral VP28, relative survival 61% vs control), 16875404 (Witteveldt 2006, DAO — oral VP28 ↓ cumulative mortality in L. vannamei), 40414471 (Choi 2025, FSI — rSHRV-VP28: ~30% vs 100% mortality, 10⁴× lower viral load).
**Innate immunity + RNAi:** 41305485 (Iftehimul 2025, Viruses — shrimp lack adaptive immunity; innate insufficient), 28501515 (Tassanakajon 2018, DCI — Toll/Imd/NF-κB, AMPs, melanization), 23059654 (Tassanakajon 2013, FSI — immune molecule inventory, hemocytes/hemolymph), 16970989, 19725947 (Flegel 2009, Biol Direct — heritable antiviral immunity via EVE in host genome; tolerance is virus-specific), 30227218 (Ho 2019, DCI — argonaute suppression compromises viral infection — from search triage, verify before citing).
**Pathology:** 38739679 (Wang XX 2024, PLoS Pathog — WSSV ↑ chitinase Chi2 in sub-cuticle epidermis → ↓ cuticle chitin → exoskeleton/white-spot damage via lipid metabolism), 38793694 (Cox 2024, Viruses — mass mortality up to 100%; no continuous shrimp cell lines), 37238106 (Kim 2023, Animals — shedding threshold G1 3.1×10³ copies/mg, mortality threshold G2 8.5×10⁴ copies/mg; min infective dose 10¹ copies/mL waterborne).
**Stress:** 37865676 (Rakhshaninejad 2023, Sci Rep — behavioral fever: 94% mortality @ fixed 27 °C vs 28% with 27–33 °C gradient), 39370017 (Valladares 2024, FSI — 24 °C vs 31 °C × β-1,3-glucan affects WSSV/WSD incidence in PL25, GLM odds ratios).

## Incident log (parallel-session race)
A sibling group session deleted my `data/_abstracts/` dir (all 48 fetched abstracts) between two execute_code calls → FileNotFoundError on the next read. Recovery: re-fetched all 26 remaining abstracts in-memory (no disk) in 2 batched calls (~13 each, sleep 0.8 s), printing ≤1150 chars per abstract to stay under the 50 KB stdout cap, then wrote the JSON with write_file (real FS). Also: an execute_code write test file (`_fs_test.txt`) appeared on the real FS — execute_code writes DO land on the real filesystem here, so the deletion was a genuine concurrent-session action, not a sandbox artifact.
