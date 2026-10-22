# Tế bào hình đài (Goblet Cells) ở heo — Roadmap

## PubMed queries tested Jul 2026

| Query | PMIDs returned | Quality |
|-------|---------------|---------|
| `goblet cell pig intestine differentiation Notch` | 5 | Good — Notch articles |
| `goblet cell porcine intestinal barrier mucin MUC2` | 5 | Good — barrier + mucin |
| `goblet cell swine weaning piglet nutrition` | 5 | Good — nutrition modulation |
| `goblet cell pig butyrate probiotic nutrition` | 2 | Sparse — use broader terms |
| `goblet cell pig weaning stress intestinal barrier post-weaning` | 3 | Good — 38672341, 34926538, 30483907 |
| `goblet cell ATOH1 Math1 intestinal stem cell differentiation porcine` | 0 | Too narrow — drop "porcine" for human literature on mechanism |
| `mucin MUC2 glycosylation sulfomucin sialomucin pig intestine` | 0 | Try shorter: `sulfomucin sialomucin pig` |
| `butyrate goblet cell differentiation pig colon SCFA` | 0 | Try: `butyrate goblet cell pig intestine` |
| `tryptophan AHR goblet cell pig intestine` | 0 | Try: `AHR goblet cell pig` |
| `goblet cell mucin MUC2 pig colon butyrate SCFA` | 1 (33065992) | Beet pulp article |
| `goblet cell zinc oxide pig intestine` | 4 | Good — ZnO + goblet articles |

## Key PMIDs with specific mechanisms

| PMID | Year | Journal | Mechanism |
|------|------|---------|-----------|
| **42436183** | 2026 | NPJ Biofilms Microbiomes | *L. plantarum* → indole-3-lactic acid (ILA) → AHR → CYP1A1 → goblet cell differentiation in piglets. Co-culture with ileal organoids validated mechanism. |
| **42284521** | 2026 | J Agric Food Chem | GOS → core 1/3 O-glycan↑ + α2,3-sialylation↑ + α2,6-sialylation↓ → mucin barrier development. C1GALT1, GALNTs, ST3GALs ↑, ST6GALNACs ↓. |
| **41366543** | 2025 | Sci Rep | IPEC-J2 differentiates into MUC2+ cells (~8%) under ALI / 5PSAg conditions. Validated as mucus model. |
| **41138499** | 2025 | Vet Microbiol | **PRRSV → Notch → goblet cell metaplasia** in nasal cavity. ↑ mucin production, disrupted TJ, ↑ inflammatory cytokines. *Novel pathogenesis: Notch-driven goblet cell hyperplasia → mucus hypersecretion → respiratory distress.* |
| **41151508** | 2025 | J Hazard Mater | Low-dose cadmium suppresses goblet cell differentiation → ↑ ACE2 → enhanced coronavirus infectivity. |
| **40797223** | 2025 | Vet Res | **PEDV → Notch↑ + MAPK↑ + Wnt/β-catenin↓ → HES1↑ → ATOH1↓ → ↓ goblet cells** in newborn piglets. ORF3 protein is key Notch activator. |
| **38896938** | 2024 | Vet Microbiol | Benzoic acid → ↑ goblet cells + MUC2 → protects against PEDV infection in piglets. Transcriptome: ↑ cell vesicle transport genes. |
| **38672341** | 2024 | Animals | Phosphatidylethanolamine → regulates mucus secretion → improves postnatal growth retardation. |
| **37289083** | 2023 | J Virol | **PDCoV → Notch → HES1↑, ATOH1↓ → ↑ISC differentiation to goblet cells inhibited.** Villus atrophy, crypt deepening, ↓ MUC2. |
| **34651635** | 2021 | Food Funct | Inulin → SCFA → sulfomucin↑ (Gal3ST1, Gal3ST2↑) → colonic barrier↑. Ileum: sialomucin-dominant; colon: sulfomucin-dominant. |

## Signaling pathway architecture

```
            ┌─────────┐
            │  ISC    │ (LGR5⁺ tế bào gốc ruột)
            └────┬────┘
                 │
      ┌──────────┼──────────┐
      │ Notch ON │ Notch OFF│
      ▼          │          ▼
   HES1↑         │       ATOH1/Math1↑ (master regulator)
      │          │          │
      ▼          │     ┌────┼────┬─────┐
  Enterocyte     │  Goblet Paneth EEC Tuft
  (hấp thu)      │  (SPDEF) (Sox9)(Neurog3)(POU2F3)
                 │
            Virus modulation:
            PEDV/PDCoV → Notch↑ → HES1↑ → ATOH1↓ → ↓Goblet
            PRRSV (nasal) → Notch↑ → ↑Goblet metaplasia
```

## Binary fate decisions

| Factor | Favors enterocyte | Favors goblet cell |
|--------|-------------------|-------------------|
| Notch | ON (↑HES1) | OFF (↓HES1 → ↑ATOH1) |
| ATOH1/Math1 | ↓ (repressed by HES1) | ↑ (master regulator) |
| SPDEF | — | Promotes goblet maturation |
| Gfi1 | — | Suppresses enteroendocrine → favors goblet+Paneth |
| EGF/MAPK | Promotes enterocyte | Inhibits goblet (via ATOH1 repression) |
| AHR ligands (ILA, FICZ) | — | Promotes goblet differentiation |
| Wnt/β-catenin | High → maintains ISC | Moderate → allows secretory lineage |

## Feed additive modulation table

| Additive | Goblet effect | Mechanism evidence | PMID |
|----------|--------------|-------------------|------|
| *L. plantarum* | ↑ Number + MUC2 | ILA → AHR → CYP1A1 → differentiation | 42436183 |
| GOS | ↑ Number + MUC2 | Core 1/3 O-glycan↑, α2,3-sialylation↑ | 42284521 |
| Inulin | ↑ MUC2 + sulfomucin | SCFA → Gal3ST↑; sialomucin→sulfomucin shift | 34651635 |
| Benzoic acid | ↑ Number + MUC2 | ISC→GC differentiation; vesicle transport↑ | 38896938 |
| Beet pulp | ↑ Number | Pectin→SCFA→butyrate→GC stimulation | 33065992 |
| Proanthocyanidins | ↑ MUC2 | ↓NF-κB → ↓inflammation → barrier protection | 40646724 |
| Anthocyanin | ↑ MUC2 | ↓ROS, ↓NF-κB → GC protection | 40410595 |
| Linarin | ↑ MUC2 | ↑beneficial bacteria; ↓ETEC | 41208957 |
| PEDV infection | ↓↓ Number + MUC2 | Notch↑ → HES1↑ → ATOH1↓ | 40797223 |
| PDCoV infection | ↓↓ Number + MUC2 | Notch↑ → HES1↑ → ATOH1↓ | 37289083 |
| PRRSV (nasal) | ↑↑ Number | Notch↑ → goblet metaplasia (harmful) | 41138499 |

## Pathway crosstalk summary

| Pathway | Goblet cell relevance |
|---------|----------------------|
| **Notch** | CENTRAL — determines enterocyte vs secretory fate via HES1/ATOH1 |
| **Wnt/β-catenin** | Maintains ISC pool; high Wnt blocks differentiation, moderate Wnt allows secretory |
| **EGF/MAPK** | Represses ATOH1 → inhibits goblet differentiation |
| **AHR** | L. plantarum → ILA → AHR → promotes goblet via CYP1A1 |
| **NF-κB** | Inflammation (↓in NF-κB = protects goblet cells) |
| **SCFA/FFAR2/3** | Butyrate → promotes goblet differentiation and sulfomucin |
| **ENS/ACh** | Cholinergic signaling → mucin secretion (merocrine → apocrine) |
| **IL-22/STAT3** | Promotes goblet cell restitution and mucus production |
| **PI3K/AKT** | Modulates Notch signaling → indirect goblet effects |
| **MAPK** | PEDV uses MAPK + Notch synergistically to suppress goblet cells |

## Vietnamese terminology

| English | Tiếng Việt |
|---------|------------|
| Goblet cell | Tế bào hình đài |
| Mucin | Chất nhầy / mucin |
| Mucus layer | Lớp nhầy |
| Goblet cell metaplasia | Chuyển sản tế bào hình đài |
| Mucus hypersecretion | Tăng tiết nhày bệnh lý |
| Notch signaling | Tín hiệu Notch |
| ATOH1/Math1 | Yếu tố phiên mã quyết định dòng tiết |
| Intestinal stem cell | Tế bào gốc ruột |
| Secretory lineage | Dòng tế bào tiết |
| Mucin O-glycosylation | O-glycosyl hóa mucin |
| Sulfomucin | Mucin sulfat hóa |
| Sialomucin | Mucin acid sialic |
| Air-liquid interface (ALI) | Giao diện không khí - lỏng |

## Existing KF card connections

This topic connects to ≥15 existing KF cards:
- Tight Junction, Paneth Cell, Notch, Wnt/β-catenin, AhR, Th17/Treg, IL-22, AMPs, Hàng rào ruột, ENS, Butyrate, Hệ vi sinh vật, ZnO, Necroptosis, Pyroptosis, NF-κB, MAPK/ERK

## GAPs (Goblet cell-associated antigen passages) — strategic keyword

Goblet cells can act as **antigen-sampling cells** in the small intestine. GAPs are MUC2-dependent transcytosis conduits that deliver luminal antigens from the gut lumen to CD103⁺ dendritic cells in the lamina propria. This is a bridge between the mucus layer and adaptive mucosal immunity. Important for oral tolerance and vaccine delivery research in swine.
