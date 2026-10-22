# 🧬 IL-17 Family (Interleukin-17) — Condensed Reference Bank for Swine Research

**Created:** 2026-07-23 cron session · **KF Card ID:** c66c50a0-d19f-4e22-b812-361eb6c5a586

## Family members

| Member | Alias | Homology vs IL-17A | Key feature |
|--------|-------|-------------------|-------------|
| IL-17A | IL-17 (classic) | 100% | Pro-inflammatory strongest; produced by Th17, γδ T, ILC3, NKT |
| IL-17F | — | 55% | Weaker agonist; broader tissue expression; heterodimer with IL-17A |
| IL-17B | — | 29% | Poorly studied; peripheral tissue expression |
| IL-17C | — | 23% | Epithelial-derived; upregulated in inflammation |
| IL-17D | — | 25% | Neural/skeletal muscle expression |
| IL-17E | IL-25 | 17% | Most divergent; Th2 response (IL-4/5/13); anti-helminth |

## Receptor pairing

| Ligand | Receptor complex | Notes |
|--------|-----------------|-------|
| IL-17A, IL-17F, IL-17A/F | IL-17RA + IL-17RC | Canonical pro-inflammatory |
| IL-17C | IL-17RA + IL-17RE | Epithelial response |
| IL-25 (IL-17E) | IL-17RA + IL-17RB | Th2/ILC2 activation |
| IL-17B | IL-17RB (possible) | Poorly characterized |
| IL-17RD | Unknown | Most ancient; from Amphioxus |

## Signaling architecture

```
IL-17A/F → IL-17RA/RC → Act1 (SEFIR-SEFIR) → TRAF6 → TAK1
    ├──→ IKK → NF-κB (p50/RelA) → cytokines, chemokines, AMPs
    ├──→ MKK3/6 → p38; MKK4/7 → JNK; MEK → ERK → AP-1
    ├──→ C/EBPβ/δ → IL-6, LCN2, S100A8/9
    └──→ Act1→TRAF2/5→HuR→mRNA stabilization (ARE-containing: CXCL1, CXCL8)
```

**Unique features:**
- SEFIR motif (similar to TIR but Act1 instead of MyD88)
- TILL domain (TIR-like loop, inhibitory)
- CBAD domain (C/EBPβ activation, unique to IL-17RA)
- mRNA stabilization — IL-17's hallmark synergy mechanism with TNF-α

## Key downstream products

- **Neutrophil chemotaxis:** CXCL1, CXCL2, CXCL5, CXCL8 (IL-8), G-CSF
- **AMP:** β-defensins (DEFB4, DEFB103), S100A7/8/9 (calprotectin), LCN2, mucins, REG3
- **MMPs:** MMP1, MMP3, MMP9, MMP13 — tissue remodeling
- **RANKL** — osteoclastogenesis
- **Synergy:** TNF-α (10-100x amplification), IL-1β, IL-22

## Porcine-specific PMIDs

| PMID | Contribution | Journal (Year) |
|------|-------------|-----------------|
| 26490738 | F4+ ETEC → IL-17A, IL-17F, IL-21 response in piglets; Th17 protects gut | Vet Res (2015) |
| 20591504 | Ultra-early weaning ↓ IL17A mRNA in MLN; ↓ serum IgA | Vet Immunol Immunopathol (2010) |
| 18760299 | Review: Th17 discovery opens feed-additive research in pigs | Dev Comp Immunol (2009) |
| 23365350 | β-glucan (Laminaria, Saccharomyces) ↓ IL-17A in porcine colon | J Anim Sci (2012) |
| 37688970 | LAB-fermented milk regulates IL-17 pathway in weaned piglet colon | Animal (2023) |
| 39857392 | L. reuteri ZY15 → AKT/mTOR/HIF-1α/RORγt → ↓ IL-17 in ETEC-challenged | Antioxidants (2025) |
| 36377452 | Anisodamine hydrobromide → Th17/Treg balance in resuscitated pigs | Zhonghua Wei Zhong Bing (2022) |
| 27020282 | Oral L. casei vaccine → Th2 → regulates IL-17 in TGEV challenge | Appl Microbiol Biotechnol (2016) |

## PubMed queries tested (Jul 2026)

```python
queries = [
    'IL-17 interleukin-17 pig swine Th17 intestinal',       # 5 PMIDs
    'IL-17A IL-17F porcine mucosal immunity',                # 6 PMIDs
    'IL-17 signaling pig gut health inflammation',           # 3 PMIDs
    'IL-17 signaling Act1 TRAF6 mechanism',                  # 5 PMIDs (general)
]
```

## Pathway crosstalk with existing KF cards

| KF Card | Connection |
|---------|-----------|
| Th17/Treg balance | RORγt drives IL-17; IL-17 is effector of Th17 |
| NF-κB | IL-17 → Act1/TRAF6 → TAK1 → IKK → NF-κB (core signaling) |
| MAPK/ERK | IL-17 → TAK1 → MKK → p38/JNK/ERK |
| IL-1 family | IL-1β from NLRP3 → Th17 → IL-17 (positive feedback) |
| IL-6/gp130 | IL-17 → IL-6 expression; IL-6 + TGF-β → Th17 differentiation |
| IL-22 | Co-expressed with IL-17; synergistic AMP production |
| TNF/TNFR | TNF + IL-17 synergy (10-100x via mRNA stabilization) |
| NLRP3 | IL-1β from NLRP3 → ↑ IL-17 |
| VDR | Calcitriol ↓ IL-17A/F via VDR-RORγt inhibition |
| HIF-1α | L. reuteri → AKT/mTOR/HIF-1α/RORγt → IL-17 |

## Clinical/therapeutic relevance

- **Anti-IL-17 drugs:** Secukinumab (anti-IL-17A), Ixekizumab (anti-IL-17A), Brodalumab (anti-IL-17RA), Bimekizumab (anti-IL-17A+F)
- **Vitamin D:** Calcitriol severely impairs IL-17A/F production
- **β-glucan:** Dietary ↓ IL-17A in porcine colon (IBD protection)
- **Probiotics:** L. reuteri modulates IL-17 via HIF-1α/RORγt axis

## Vietnamese terminology

| English | Tiếng Việt |
|---------|-----------|
| Interleukin-17 family | Họ Interleukin-17 |
| Cystine knot | Nút cystine |
| Th17 cell | Tế bào Th17 |
| Neutrophil recruitment | Tuyển mộ bạch cầu trung tính |
| Antimicrobial peptide | Peptide kháng khuẩn |
| Signaling pathway | Con đường tín hiệu |
| Mucosal immunity | Miễn dịch niêm mạc |
