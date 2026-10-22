# Quercetin (Flavonol) — Swine Phytochemical Roadmap

Created 2026-08-02 (rotation group ⚗️ Hóa học & Dược). KF card `cb64f373-6fdd-4397-9083-4b830a5111fb`.

## Summary table

| Item | Value |
|------|-------|
| Class | Flavonol (flavonoid / polyphenol), C₁₅H₁₀O₇ |
| Core targets | Nrf2/KEAP1, NF-κB/TLR4, tight junctions, Uba1 (ubiquitin), gut microbiota |
| Swine dose (weaned piglets) | 250–750 mg/kg feed; peak 500–750 mg/kg |
| Key in vivo paper | PMID 39139212 (Oxid Med Cell Longev 2024): 48 piglets, 4 doses |
| Bioavailability | <1% oral; glucuronidation + COMT methylation; gut microbiota deglucuronidation (enterohepatic recycling) |
| GRAS (human) | 500 mg/serving (FDA 2010) |
| Card structure used | 12 sections: định nghĩa → PK → Nrf2 → NF-κB → TJ → PRRSV → AMR → microbiota → swine data → human → limits → kết luận |

## Tested PubMed queries

| Query | Result quality |
|-------|---------------|
| `quercetin intestinal barrier tight junction pig` | ✅ Good (38338808, 38133183, 37720305 + 1 tangential) |
| `quercetin weaned piglet growth performance diarrhea` | ✅ Perfect hit (39139212) |
| `quercetin PRRSV antiviral replication` | ✅ Good (42475393, 41472306, 40503831, 39016357, 38709810, 24625230) |
| `quercetin antioxidant feed additive swine` | ✅ OK (42114140, 40994218, 40192035, 39826529, 38501756, 38420856) |
| `quercetin Nrf2 HO-1 heme oxygenase intestinal epithelial cells` | ⚠️ 1 tangential (isorhamnetin 38795598) — mechanism data came from other queries instead |
| `quercetin antibacterial mechanism gram-negative membrane` | ⚠️ Mostly reviews; 41375548 is the keeper |
| `quercetin weaning stress piglet antioxidant enzyme` | ✅ 27021614 (DON+ZEN antioxidant combo) |
| `quercetin bioavailability metabolism gut microbiota` | ⚠️ Noise (cancer reviews); 42196996 + 41762160 relevant |
| `quercetin ETEC IPEC-J2 intestinal epithelial` | ❌ 0 hits — rephrase, don't retry |
| `quercetin Nrf2 NF-kB oxidative stress inflammation pig` | ❌ 0 hits |
| `quercetin zinc oxide alternative weaned piglet` | ❌ 0 hits |
| `quercetin diquat oxidative stress piglet` | ❌ 0 hits |

## PMID table

| PMID | Journal (Year) | Mechanism / contribution |
|------|----------------|--------------------------|
| 39139212 | Oxid Med Cell Longev (2024), DOI 10.1155/2024/5632260 | 250–750 mg/kg: FCR ↓ (500/750), diarrhea rate/index ↓ (all doses), IFN-γ ↓, TGF-β ↑, NF-κB ↓ (750), colonic diversity ↑, Actinobacteria ↑ / Proteobacteria ↓; ⚠️ Escherichia-Shigella ↑ |
| 38338808 | Int J Mol Sci (2024), DOI 10.3390/ijms25031530 | Ussing chamber porcine tissue: TEER ↑, claudin-4 ↑, claudin-2 ↓ in villus epithelium; NO effect in Peyer's patches (FAE difference) |
| 37720305 | Curr Res Toxicol (2023), DOI 10.1016/j.crtox.2023.100122 | DON protection via Nrf2 → NQO1, claudin-4/ZO-1 membrane rescue, TEER restored, FITC-dextran ↓; brusatol (Nrf2 inhibitor) abolishes effect |
| 38133183 | Toxins (2023), DOI 10.3390/toxins15120679 | ZEA 20 µM + LPS 1 µg/mL on IPEC-J2: quercetin 20 µM protective (Nrf2/HO-1/SOD2/NQO1 ↑, claudin/ZO-1/occludin ↑, apoptosis ↓); 40–200 µM cytotoxic |
| 42475393 | PLoS Pathog (2026), DOI 10.1371/journal.ppat.1014425 | NEW mechanism: quercetin binds host Uba1 (ubiquitin-activating enzyme 1, residues Q977/G978), blocks ubiquitin transfer Uba1→Ubc6 → inhibits PRRSV (RNA) + BmNPV (DNA) |
| 41472306 | Viruses (2025), DOI 10.3390/v17121637 | PRRSV inhibition via PI3K/Akt/mTOR autophagy modulation (MARC-145) |
| 39016357 | Vet Med Sci (2024), DOI 10.1002/vms3.1536 | Reduces PRRSV-induced inflammation (short abstract — cite as support only) |
| 40503831 | Microbiol Spectr (2025), DOI 10.1128/spectrum.03107-24 | Hyperoside (quercetin-3-O-galactoside) vs PRRSV via TLR4/NF-κB + p62-Nrf2-Keap1 |
| 41375548 | Animals (2025), DOI 10.3390/ani15233491 | FIC = 0.34375 synergy with polymyxin E vs MCR-1 E. coli; ↑ membrane permeability, ↓ AcrAB-TolC efflux, ↓ LPS genes |
| 27021614 | Mycotoxin Res (2016), DOI 10.1007/s12550-016-0245-y | DON 3.1 + ZEN 1.8 mg/kg: quercetin alone limited effect; vitamin A/C/E + Se/GSH + quercetin combo ↓ MDA plasma/liver/ileum |
| 42196996 | Nutrients (2026), DOI 10.3390/nu18101537 | EubioQuercetin (bioavailability-enhanced) anti-aging via gut microbiota–intestinal barrier axis |
| 41762160 | Biosci Biotechnol Biochem (2026), DOI 10.1093/bbb/zbag032 | Species-specific deglucuronidation of quercetin glucuronides by human gut microbiota (PK) |
| 35883756 | Antioxidants (2022), DOI 10.3390/antiox11071265 | Methylated derivatives (3-O-methylquercetin/isorhamnetin) stronger anti-inflammatory than parent |
| 34964515 | Phytother Res (2022), DOI 10.1002/ptr.7352 | O-glycoside quercetin derivatives: bioactivities + SAR review |

## Key takeaways for future cards

- **Ghost-topic fill:** the Polyphenol card mentions flavonoids but quercetin had no dedicated card → high connective value (same pattern as Berberine/Curcumin).
- **Bioavailability is THE bottleneck:** always pair in vitro mechanism claims with the <1% oral bioavailability caveat; bioavailability-enhanced forms (glycosides > aglycone, nano, micelle, EubioQuercetin) are the active research frontier.
- **Narrow dose window:** 20 µM protective vs 40–200 µM cytotoxic on IPEC-J2 — mention the hormesis/caution angle.
- **Mycotoxin angle works best as combination therapy** (vitamins + Se + quercetin), not single compound (PMID 27021614).
- **PRRSV Uba1 mechanism (2026) is a strong "cutting-edge" section** — targets host enzyme, so lower resistance risk than viral-protein-targeting drugs.
- **Natural follow-up topics** (none have cards as of 2026-08-02): rutin, isoquercitrin, apigenin, luteolin, resveratrol, genistein/isoflavone, phenolic acids (chlorogenic/ferulic), lignan, coumarin, anthraquinone, capsaicin.
