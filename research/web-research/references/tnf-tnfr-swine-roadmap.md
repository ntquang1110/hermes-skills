# TNF/TNFR Superfamily Signaling in Swine — Condensed Research Roadmap

> Condensed reference bank: 15 PubMed IDs, 8 Wikipedia pages, pathway architecture, receptor comparison table, disease mechanisms, feed additive interactions, tested PubMed queries. Created Jul 2026 from multi-angle PubMed + Wikipedia research for KF card generation.

---

## Key PubMed queries (tested Jul 2026)

| Query | Results | Notes |
|-------|---------|-------|
| `TNF-alpha signaling intestinal barrier pig` | 5+ relevant | Best for tight junction / IPEC-J2 papers |
| `TNFR1 TNFR2 pig macrophage inflammation` | ⚠️ 0 results | Use `TNF alpha porcine macrophage NF-kB signaling` instead |
| `tumor necrosis factor alpha TNFR1 pig intestine tight junction` | 3 directly relevant | PMID 34445450 is key |
| `TNF-alpha pig weaning stress intestine` | 4 relevant | Fecal biomarkers of inflammation |
| `TNF-alpha feed additive pig gut health` | 5 relevant | Feed additive / probiotic modulation |
| `TNF alpha converting enzyme TACE pig ADAM17` | 5+ relevant | TACE/ADAM17 mechanism |
| `TNF superfamily porcine immune response` | 5 relevant | TRAIL, CD27, broader family |
| `TNFRSF1A TNFRSF1B polymorphism pig` | ⚠️ 0 results | Try species-general queries instead |
| `Fas FasL porcine immune cells apoptosis` | 3+ relevant | Xenotransplantation-related |
| `TRAIL porcine apoptosis virus infection` | 1 relevant | CSFV-related (PMID 19649765) |
| `CD40 CD40L porcine B cell antibody response` | 3+ relevant | Vaccine response context |
| `TNF alpha piglet diarrhea intestinal inflammation` | 5+ relevant | ETEC, microenvironment |

## PMID summary table

| PMID | Journal (Year) | Focus | Key finding / mechanism |
|------|---------------|-------|------------------------|
| 34445450 | Int J Mol Sci (2021) | TNF-α / IPEC-J2 | TNF-α ↑ TNFR1 expression + ↓ TEER + ↓ occludin/claudin-1/3 on porcine enterocytes; dose-dependent TNFR1 upregulation creates positive feedback loop |
| 33242708 | Int Immunopharmacol (2020) | AOS / IPEC-J2 | Alginate oligosaccharide ↑ occludin, ↓ apoptosis rate, ↓ TNF-α and IL-6 on TNF-α-treated IPEC-J2; mucosal protection via barrier reinforcement |
| 40244215 | Int J Mol Sci (2025) | CBD / Peyer's patches | Cannabidiol strengthens barrier of porcine follicle-associated epithelium; tight junction protein modulation in native intestinal tissue |
| 40503831 | Microbiol Spectr (2025) | Hyperoside / PRRSV | Hyperoside ↓ pro-inflammatory cytokines (TNF, IL-1β, IL-6, IL-8) via TLR4/NF-κB; inhibits PRRSV replication in PAMs |
| 40162787 | J Virol (2025) | ASFV S273R / NF-κB | ASFV pS273R antagonizes TNF-α-induced NF-κB activation via IκBα stabilization; blocks canonical pathway independently of protease activity |
| 41939891 | Front Immunol (2026) | ETEC / necroptosis | ETEC induces RIPK3/MLKL necroptosis in jejunal crypt epithelial cells → HMGB1 release → lamina propria immune cell pyroptosis |
| 40074117 | Int J Biol Macromol (2025) | PR-39 / TGR5/NF-κB | Porcine PR-39 AMP ↓ serum TNF, IL-1β, IL-6 via TGR-5/NF-κB/MLCK/MLC pathway; alters bile acid metabolism via gut microbiota |
| 42001834 | Phytomedicine (2026) | EGCG / ILC2 | EGCG ↓ TNF via NMU-NMUR1-ILC2 axis suppression; modulates gut microbiota energy metabolism |
| 26653711 | J Gen Virol (2016) | ADAM17 / PRRSV | PRRSV induces ADAM17-mediated CD16 shedding from neutrophils → ↑ sCD16 as biomarker of PRRSV infection |
| 23389627 | Mol Biol Cell (2013) | GEF-H1/Rac/TACE | TNF-α activates TACE/ADAM17 via GEF-H1 → Rac → p38 → EGFR transactivation → RhoA; mechanism of TNF-induced junction remodeling |
| 24424050 | Endocrinology (2014) | TACE/PKC/porcine | PKC and c-Src activate TACE/ADAM17 in porcine granulosa cells; essential for EGFR/MAPK3/1 signaling and luteinization |
| 25150062 | Am J Physiol Lung Cell Mol Physiol (2014) | PKA/PKC balance | PKA activation ↓ IL-8 release in bronchial epithelial cells exposed to hog dust; counteracts PKC-ε-mediated inflammation |
| 41952052 | J Agric Food Chem (2026) | VDR-FXR/TNF | Vitamin D3 metabolites enhance VDR-FXR binding in porcine liver; ↓ hepatic TNF, ↓ bile acid dysregulation → ↓ weaning diarrhea |
| 19649765 | Arch Virol (2009) | CSFV/TNF/apoptosis | CSFV strains of varying virulence modulate antiviral and apoptotic genes including TRAIL; ↑ TNF correlates with lymphopenia |
| 24518159 | Transpl Immunol (2014) | FasL/porcine | Human FasL + dexamethasone-treated DCs enhance survival of porcine fibroblasts; xenograft protection via Fas/FasL pathway |

## Pathway architecture

### TNF → TNFR1 signaling (Complex I → IIa → IIb → III)

```
TNF trimer
    ↓
TNFR1 (CD120a, contains Death Domain)
    ↓  TRADD (adaptor)
    ├──→ Complex I (membrane): TRADD + RIPK1 + TRAF2 + c-IAP1/2 + LUBAC
    │         ↓ TAK1 → IKK → IκBα phosphorylation → NF-κB translocation
    │         → Pro-inflammatory genes: IL-1β, IL-6, IL-8, TNF, COX-2
    │         → Anti-apoptotic: c-FLIP, Bcl-2, c-IAP1/2, A20
    │
    └──→ Complex IIa (cytoplasmic): RIPK1 deubiquitination
            ↓ FADD + Caspase-8
            ├── Caspase-8 active → Caspase-3 → **Apoptosis** (extrinsic)
            └── When Caspase-8 inhibited:
                    ↓ Complex IIb = RIPK1 + RIPK3 + MLKL
                    → MLKL oligomerization → membrane pore → **Necroptosis**
                    → DAMP release (HMGB1, ATP, IL-1α)
```

### TNF → TNFR2 signaling (non-death domain, survival)

```
tmTNF only (not sTNF)
    ↓
TNFR2 (CD120b, NO Death Domain)
    ↓  TRAF2
    ├──→ c-IAP1/2 → K63 ubiquitination → NF-κB (non-canonical, p52/RelB)
    ├──→ PI3K → AKT → mTOR → Survival / proliferation
    └──→ Treg expansion → **Immunosuppression**
```

### TNFR1 vs TNFR2 — core differences

| Feature | TNFR1 (TNFRSF1A / CD120a) | TNFR2 (TNFRSF1B / CD120b) |
|---------|---------------------------|---------------------------|
| Expression | Ubiquitous (all cell types) | Restricted (Treg, monocytes, endothelial, microglia) |
| Death domain | ✅ Yes (cytoplasmic) | ❌ No |
| Ligand affinity | Binds both sTNF and tmTNF | Binds only tmTNF (not sTNF) |
| Primary signaling | TRADD → NF-κB, apoptosis, necroptosis | TRAF2 → PI3K/AKT, non-canonical NF-κB |
| Cell outcome | Inflammation ↔ cell death | Survival, proliferation, immunosuppression |
| Shedding | Cleaved by TACE → soluble TNFR1 (biomarker) | Also shed; sTNFR2 elevated in inflammation |
| Porcine relevance | Intestinal barrier disruption, PRRSV/ASFV pathology | T cell regulation; potential therapeutic target |

### Fas/FasL signaling

```
FasL (TNFSF6) → Fas (CD95/TNFRSF6)
    ↓
FADD → DED → Procaspase-8/10
    ↓
Caspase-8 → Caspase-3 → **Apoptosis**
```

- Key for CTL/NK killing of virus-infected cells
- Fas expressed on porcine hepatocytes, enterocytes, lymphocytes
- FasL on activated T cells and NK cells

### CD40/CD40L — adaptive immunity bridge

```
CD40L (CD154, TNFSF5) → CD40 (TNFRSF5)
    ↓ (on B cells, DCs, macrophages)
TRAF2/3/5/6 → NF-κB, MAPK, PI3K
    ↓
• B cell: Proliferation, Ig class switching, germinal center formation
• DC: Maturation, IL-12 production, cross-presentation
• Macrophage: Pro-inflammatory activation
```

- Essential for T-dependent antibody responses
- CD40L deficiency → hyper-IgM syndrome in humans

### Lymphotoxin (LT) — lymphoid organogenesis

```
LT-α3 (soluble, homotrimer) → TNFR1
LT-α1β2 (membrane, heterotrimer) → LTβR
    ↓
NF-κB (alternative pathway) → Chemokines (CXCL13, CCL21)
    ↓
Lymphoid tissue development: Peyer's patches, lymph nodes, spleen
```

- LT-α knockout → no Peyer's patches, disorganized spleen, no lymph nodes
- Critical for gut-associated lymphoid tissue (GALT) development

## Key porcine signaling connections

| Existing KF card | TNF/TNFR connection |
|-----------------|---------------------|
| NF-κB | TNF → TNFR1 → TRADD → TRAF2 → TAK1 → IKK → IκBα → NF-κB is the canonical activation pathway |
| Apoptosis | TNF → TNFR1 → TRADD → FADD → Caspase-8 → extrinsic apoptosis pathway |
| Necroptosis | TNF → TNFR1 → RIPK1 → RIPK3 → MLKL when Caspase-8 is blocked |
| NLRP3 | TNF primes NLRP3 via NF-κB (signal 1); TNF-induced necroptosis releases DAMPs that activate NLRP3 |
| PRRSV | TNF is central to PRRSV pathology (↑ in PAMs, ADAM17 shedding, apoptosis) |
| ASFV | ASFV S273R antagonizes TNF → NF-κB pathway for immune evasion |
| PEDV | TNF disrupts tight junctions via TNFR1, creating leaky gut |
| Hàng rào ruột | TNF ↓ occludin/claudin-1/3 via TNFR1 → ↑ intestinal permeability |
| ZnO | ZnO ↓ TNF production via NF-κB inhibition; known mechanism |
| Butyrate | HDACi → ↓ NF-κB activity → ↓ TNF transcription in enterocytes |
| Th17/Treg | TNF + IL-6 → Th17 differentiation; TNFR2 → Treg expansion |
| HIF-1α | TNF stabilizes HIF-1α during inflammation |
| Ferroptosis | TNF + IFN-γ synergize to induce ferroptosis in certain contexts |
| MAPK/ERK | TNF → TRAF2 → TAK1 → MKK → ERK/JNK/p38 |

## TNF modulation by feed additives

| Additive | TNF effect | Mechanism | PMID |
|----------|-----------|-----------|------|
| ZnO (pharmacological) | ↓ TNF, IL-1β, IL-8 | IκBα stabilization → NF-κB inhibition; ↑ A20 | Multiple |
| Butyrate | ↓ TNF, IL-6 | HDACi → ↓ NF-κB → ↓ TNF transcription | Multiple |
| EGCG | ↓ TNF (intestinal) | NMU-NMUR1-ILC2 axis suppression | 42001834 |
| Tannic acid | ↓ TNF, ↑ IL-10 | Gut microbiota modulation | 41056411 |
| Alginate oligosaccharide (AOS) | ↓ TNF on IPEC-J2 | ↑ occludin, ↓ apoptosis | 33242708 |
| PR-39 (AMPs) | ↓ TNF, ↓ IL-1β, IL-6 | TGR-5 → NF-κB/MLCK | 40074117 |
| Vitamin D3 metabolite | ↓ TNF (hepatic) | VDR-FXR heterodimer → ↓ BA dysregulation | 41952052 |
| Hyperoside | ↓ TNF, IL-1β, IL-8 | TLR4/NF-κB inhibition | 40503831 |
| CBD | ↓ inflammation (PP) | ↑ Tight junction proteins in Peyer's patches | 40244215 |
| Probiotics (L. reuteri) | ↓ TNF (systemic + gut) | Microbiota → butyrate → HDACi | 42397592 |

## TACE/ADAM17 — master sheddase of TNF system

| Substrate | Effect of shedding | Relevance to swine |
|-----------|-------------------|--------------------|
| tmTNF → sTNF | Loses ability to activate TNFR2 | Inflammatory amplification |
| TNFR1 | Soluble TNFR1 = TNF decoy + biomarker | ↑ sTNFR1 in inflammation |
| TNFR2 | Modulates TNFR2 signaling | ↑ sTNFR2 in PRRSV (analogous to human) |
| CD16 (FcγRIII) | sCD16 released | ↑ sCD16 is PRRSV biomarker (PMID 26653711) |
| IL-6R | Trans-signaling IL-6 | Inflammatory amplification |
| EGFR ligands (HB-EGF, TGF-α) | EGFR transactivation | Cell proliferation, migration, wound repair |

## Vietnamese terminology

| English | Tiếng Việt |
|---------|------------|
| Tumor Necrosis Factor | Yếu tố hoại tử khối u |
| TNF-α (TNF-alpha) | TNF-alpha |
| TNFR1 (CD120a) | Thụ thể TNF loại 1 |
| TNFR2 (CD120b) | Thụ thể TNF loại 2 |
| Fas receptor (CD95) | Thụ thể Fas |
| Fas ligand (FasL) | Phối tử Fas |
| TRAIL | Chất gây apoptosis liên quan đến TNF |
| CD40 | CD40 (thụ thể trên APC) |
| CD40L (CD154) | CD40 ligand (trên tế bào T) |
| Lymphotoxin (LT-α) | Lymphotoxin-alpha (TNF-β) |
| Death domain (DD) | Vùng gây chết |
| Adaptor protein | Protein tiếp hợp |
| TACE/ADAM17 | Enzyme cắt TNF |
| Shedding | Cắt rụng thụ thể |
| Necroptosis | Chết tế bào hoại tử có chương trình |
| pro-inflammatory cytokine | Cytokine tiền viêm |
| NF-κB | Yếu tố nhân kappa B |
| Apoptosis | Chết tế bào theo chương trình |

## Recommended follow-up topics (not yet in KF as of Jul 2026)

- Fas/FasL signaling — extrinsic apoptosis pathway in viral clearance
- CD40/CD40L axis — B cell activation, vaccine response, germinal center
- TRAIL/DR4/DR5 — tumor immune surveillance in swine
- TACE/ADAM17 — central sheddase, crosstalk between TNF, EGFR, IL-6R
- Endotoxin tolerance — LPS → TNF downregulation after repeated challenge
- sTNFR1/sTNFR2 as biomarkers — inflammatory status in swine disease
