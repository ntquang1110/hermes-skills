# 🛑 Immune Checkpoints (PD-1/CTLA-4/CD28) ở heo

Condensed reference bank for immune checkpoint research in swine. Created Jul 2026 from Wikipedia + PubMed multi-angle search.

## Key PubMed queries tested

| Query | Result quality | PMIDs found |
|-------|---------------|-------------|
| `PD-1 PD-L1 pig T cell exhaustion` | ❌ 0 results | — |
| `CTLA-4 CD28 porcine T cell activation` | ✅ Good | 32716497, 22326797, 16337491, 12518898 |
| `PRRSV PD-L1 immune checkpoint swine` | ❌ 0 results | — |
| `porcine T cell exhaustion chronic virus` | ⚠️ 1 result | 41449719 |
| `PD-1 blockade pig vaccine response` | ❌ 0 results | — |
| `porcine CD28 CTLA-4 immune costimulation` | ✅ Good | 32716497, 22326797, 22253710, 16337491, 10843688 |
| `lymphocyte activation gene 3 LAG-3 TIGIT porcine` | ❌ 0 results | — |
| `checkpoint inhibitor pig infectious disease` | ⚠️ 1 result | 38793680 |
| `PD-L1 B7-H1 pig macrophage` | ✅ Good | 25041075 |
| `T cell exhaustion virus pig PRRSV` | ✅ **Best** | 34851149, 34379512, 34046040 |
| `co-stimulation CD28 CD86 pig T cell` | ✅ Good | 22326797, 16337491, 8757955 |
| `CTLA-4 Ig porcine xenotransplantation tolerance` | ✅ Good | 31157670, 27653300, 17175250, 12518898 |
| `porcine CD80 B7-1 costimulation` | ✅ Good | 27175998, 22326797, 16891217, 15807770 |

## Key PMIDs by theme

### PRRSV & T cell exhaustion (HIGHEST VALUE)

| PMID | Title | Journal (Year) | Key finding |
|------|-------|----------------|-------------|
| **34379512** | PRRSV Infection Upregulates Negative Immune Regulators and T-Cell Exhaustion Markers | J Virol (2021) | PRRSV-infected PAMs → ↑PD-1, CTLA-4, LAG-3; bystander PAMs also affected |
| **34046040** | Up-Regulation of Immune Checkpoints in the Thymus of PRRSV-1-Infected Piglets | Front Immunol (2021) | Virulent PRRSV (Lena) → thymus atrophy + checkpoint upregulation (virulence-dependent) |
| **34851149** | Time Series Transcriptomic Analysis of BAL Cells from PRRSV-1 Infected Piglets | J Virol (2022) | Kinetic transcriptional signature, conserved vs virulent strains |
| **41449719** | Metabolic Reprogramming of Adaptive Immunity Induced by Viral Infections | Immunology (2026) | Links metabolism → Th1/Th2/Th17/Treg/CTL differentiation + T cell exhaustion |

### Porcine checkpoint molecules (cloned/expressed)

| PMID | Molecule | Key finding |
|------|----------|-------------|
| **22326797** | Porcine CTLA-4 | Soluble porcine CTLA-4 expressed in *P. pastoris* |
| **16337491** | Miniature swine CD86 | Full-length cDNA, 98.4% homology with domestic pig |
| **10843688** | Porcine B7-1 (soluble form) | Alternatively spliced sB7-1 lacking TM domain; 25% of B7-1 mRNA in alveolar macrophages |
| **8757955** | Porcine CD86 on endothelium | Endothelial cells express CD86 → co-stimulate T cell proliferation |

### Checkpoint manipulation in xenotransplantation

| PMID | Approach | Model |
|------|----------|-------|
| **25041075** | PD-L1 overexpression | Pig→rat transplantation, reduced immune response |
| **27175998** | LEA29Y (CTLA4-Ig) transgenic pigs | Ubiquitous expression blocks CD28 co-stimulation |
| **27653300** | Costimulation blockade → Treg induction | Tolerance to porcine islet xenografts |
| **11267061** | B7-CD28 + CD40-CD40L dual blockade | Eliminates human anti-porcine T-cell response |
| **15807770** | CD154 + CD28/B7 blockade | Modulates antibody response in baboon cardiac xenograft |

### Checkpoint blockade in chronic infection (veterinary relevance)

| PMID | Finding |
|------|---------|
| **38793680** | Anti-PD-L1 improves virus control without augmenting tissue damage (LCMV model) |
| **38900430** | PD-1 blockade + therapeutic vaccine → enhanced T cell responses |

### Pathway modulation by feed additives (indirect checkpoint effects)

| PMID | Compound | Effect |
|------|----------|--------|
| **22253710** | Astragalus polysaccharide (APS) | Modulates porcine PBMC responses to PRRSV/CSFV |
| **37199152** | Tryptophan | ↓TLR4/NOD signaling → ↓intestinal inflammation |
| **30310102** | Glutamate | ↑mTOR, ↓TLR4/NOD → barrier protection |
| **23014495** | Fish oil (n-3 PUFA) | ↓TLR4 + NOD2 signaling |
| **35921778** | Niacin | ↓PDCoV damage via GPR109a/NF-κB |

## Signaling architecture

### PD-1 signaling
```
PD-L1 → PD-1 → ITIM (Y223) → ITSM (Y248) → SHP-2
  → TCR dephosphorylation (CD3ζ, Zap70)
  → PI3K/AKT dephosphorylation
  → ↑CBL-b/c-CBL (TCR ubiquitination)
  → ↓NF-κB, ↓NFAT, ↓AP-1, ↓IL-2, ↓IFN-γ
```

### CTLA-4 mechanism
- **Competition**: binds CD80/86 with higher affinity than CD28
- **Trans-endocytosis**: captures CD80/86 from APC membrane → lysosomal degradation
- **Signaling**: SHP-2 + PP2A → dephosphorylation of CD3 and LAT

### CD28 co-stimulation
- **YMNM motif**: Tyr170 → PI3K/AKT/mTOR (Bcl-xL, IL-2)
- **Asn172 → Grb2/Gads**: IL-2 mRNA stability
- **Proline-rich motifs → SH3 (Itk, Lck, Tec)**: immune synapse formation

## Dedup keywords for KF card check

Use these with the word-boundary regex pattern to avoid false positives:
```
['checkpoint', 'PD-1', 'PD-L1', 'CTLA-4', 'immune checkpoint',
 'T cell exhaustion', 'costimulation', 'B7-1', 'CD80', 'CD86',
 'ICOS', 'TIGIT', 'LAG-3', 'TIM-3', 'BTLA']
```

**Avoid** using short fragments like `CD` or `IL` alone — they match every card with CD4+/CD8+/IL-1/IL-6 etc.

## Vietnamese terminology

| English | Tiếng Việt |
|---------|-----------|
| Immune checkpoint | Điểm kiểm soát miễn dịch |
| T cell exhaustion | Kiệt sức tế bào T |
| Co-stimulation | Đồng kích thích |
| Checkpoint blockade | Phong tỏa điểm kiểm soát |
| PD-1 (Programmed cell death protein 1) | Protein chết tế bào theo chương trình 1 |
| CTLA-4 (Cytotoxic T-Lymphocyte Antigen 4) | Kháng nguyên tế bào T độc 4 |
| T cell anergy | Dung nạp tế bào T |
| Immune synapse | Khớp thần kinh miễn dịch |

## Wikipedia pages used

- Programmed cell death protein 1 (PD-1)
- PD-L1
- Cytotoxic T-lymphocyte associated protein 4 (CTLA-4)
- CD28
- Immune checkpoint
- T cell
- T cell exhaustion
- Checkpoint inhibitor
