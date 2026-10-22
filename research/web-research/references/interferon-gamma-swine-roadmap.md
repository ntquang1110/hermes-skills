# IFN-γ (Interferon-gamma) / Type II Interferon — Swine Roadmap

**Created:** Jul 2026 — Cron research session  
**Sources:** Wikipedia Action API + PubMed E-utilities (multi-query)  
**KF Card ID:** `e9b1d736-6c24-4e08-8717-f42dbfdba61d` (122 cards)

---

## Quick Reference

| Attribute | Value |
|-----------|-------|
| **Class** | Type II interferon (sole member) |
| **Gene** | *IFNG* (single gene, unlike 13+ type I IFN genes) |
| **Monomer** | 143 aa, 6 α-helix core + C-terminal domain (17 aa heparin-binding) |
| **Active form** | Anti-parallel interlocking homodimer (~34 kDa) |
| **Receptor** | IFNGR1 (α chain, JAK1) / IFNGR2 (β chain, JAK2) |
| **Signaling** | JAK1/JAK2 → STAT1 homodimer (GAF) → GAS elements → ~236 ISGs |
| **Key ISGs** | IRF1, CIITA, iNOS, IDO1, CXCL9/10/11, FcγRI, immunoproteasome, MHC I/II |

---

## Core PubMed Queries (tested Jul 2026)

Query specificity trap: generic queries like `"IFN-gamma pig"` return noise. Use mechanism-specific queries:

```python
queries = [
    'interferon gamma pig immune function mechanism',
    'IFN-gamma porcine macrophage activation Th1',
    'IFN-gamma swine PRRSV immune evasion',
    'IFN-gamma piglet intestinal immunity weaning',
    'interferon gamma porcine NK cell CD8',
    'IFN-gamma swine feed additive modulation',
]
```

**Multi-query strategy:** 6 angles → 29 unique PMIDs → dedup → fetch top abstracts.

---

## Key PubMed Results Table

| PMID | Journal (Year) | Contribution | Query source |
|------|---------------|-------------|-------------|
| 34579246 | Vaccines (2021) | PRRSV-2 antigen → M1 repolarization → Th1/IFN-γ | Macrophage |
| 32062072 | Int Immunopharmacol (2020) | FcγR activation → ↓ IFN-γ in PAMs during PRRSV | PRRSV evasion |
| 27473784 | Dev Comp Immunol (2016) | PRRSV → DC → Th1/Th2 imbalance → ↓ IFN-γ | PRRSV evasion |
| 26792733 | J Virol (2016) | nsp1β motif → IFN-β suppression (also affects IFN-γ) | PRRSV evasion |
| 17031757 | Vet Microbiol (2006) | PRRSV quasispecies + IFN-γ suppression mechanism | PRRSV evasion |
| 42278123 | J Nutr (2026) | Co-feeding sow-piglet → ↑ IFN-γ, ↓ weaning stress | Gut immunity |
| 41375480 | Vet Sci (2026) | *C. butyricum* + OA → ↑ IFN-γ, TGF-β in gut | Gut immunity |
| 41208033 | BMC Vet Res (2026) | EO + SC + IMO → ↑ IFN-γ systemic in weaned pigs | Gut immunity |
| 41064261 | Front Vet Sci (2026) | COS to sows → ↑ IFN-γ in milk → protects piglets | Gut immunity |
| 38897378 | Vet J (2024) | Algae β-glucan → ↑ virus-specific IFN-γ T cells | Feed additive |
| 40459260 | Front Immunol (2025) | NADC34-like PRRSV → IFN-γ modulation in pigs | NK/CD8 |
| 38220489 | J Virol (2024) | PEDV S trimer → IFN-γ response in vaccine | Feed additive |
| 38160508 | Vet Microbiol (2024) | PRRSV → M1 → inhibits CSFV — IFN-γ mediated | Feed additive |
| 37356277 | Vet Microbiol (2023) | E2 T cell epitope → IFN-γ in CSFV | PRRSV evasion |
| 27032496 | Vet Immunol Immunopathol (2016) | CpG DNA → IFN-γ from porcine γδ T cells | NK/CD8 |
| 31316500 | Dev Comp Immunol (2019) | Flow cytometry gating of porcine IFN-γ-producing cells | NK/CD8 |
| 30837028 | Front Immunol (2019) | LFP-20 (lactoferrin) → regulates IFN-γ/inflammation | Feed additive |

---

## Signaling Architecture

```
IFN-γ dimer → IFNGR1/IFNGR2 → JAK1/JAK2 trans-phosphorylation
    ↓
IFNGR1 Tyr docking site → STAT1 recruitment → Tyr701 phosphorylation
    ↓
STAT1-STAT1 homodimer (GAF) → nuclear translocation
    ↓
Binds GAS (TTCNNNGAA) promoter elements
    ↓
Transcriptional activation of ~236 ISGs:
  • IRF1 (master TF) → iNOS, CIITA, MHC II
  • CIITA → MHC class II expression (rate-limiting)
  • iNOS → NO production (antimicrobial)
  • IDO1 → tryptophan depletion (antiparasitic)
  • CXCL9/10/11 → Th1/NK/CD8 chemotaxis
  • Immunoproteasome subunits (LMP2/7, MECL1)
  • FcγRI (CD64) → ADCC enhancement
```

**Other pathways activated:**
- PI3K/AKT/mTOR (translation, growth)
- MAPK/ERK (inflammation, differentiation)
- PKC-δ (Ser727 phosphorylation of STAT1 for full activity)

---

## Porcine-Specific Notes

- **γδ T cells** are a major IFN-γ source in pigs (unlike humans/mice where they're minor). Respond to IL-12+IL-18 without TCR signaling. CpG DNA is a potent trigger (PMID 27032496).
- **PRRSV** has 4+ mechanisms to suppress IFN-γ: nsp1β/2 → IRF3/NF-κB inhibition, M2 macrophage skewing, FcγR-mediated downregulation, DC IL-10↑/IL-12↓.
- **CSFV C-strain** protection correlates with IFN-γ-producing T cells. E2 protein has T cell epitopes (PMID 37356277).
- **PEDV** S protein trimer vaccines require IFN-γ response for efficacy (PMID 38220489).
- **γδ T cells + β-glucan** (Dectin-1) → IFN-γ production → trained immunity (PMID 38897378).

---

## Feed Additive Modulation of IFN-γ

| Additive | Effect | Mechanism | PMID |
|----------|--------|-----------|------|
| β-glucan (algae/yeast) | ↑ | Dectin-1 → NF-κB → ↑ IFN-γ from T/γδ T cells | 38897378 |
| Chitosan oligosaccharide (COS) | ↑ (maternal) | ↑ IFN-γ in sow milk → piglet protection | 41064261 |
| *C. butyricum* + organic acids | ↑ | ↑ IFN-γ, TGF-β in intestine | 41375480 |
| Essential oils + yeast + IMO | ⇔ Balanced | ↓ excess TNF-α, maintains IFN-γ | 41208033 |
| *Lactobacillus* EPS | ↑ | ↑ IFN-γ, anti-inflammatory via NF-κB | 42264247 |
| Sanguinarine | ⇔ | ↓ excessive inflammation, preserves IFN-γ | 35843190 |
| CpG DNA (TLR9) | ↑↑ | Potent IFN-γ from NK/γδ T cells | 27032496 |
| LFP-20 (lactoferrin peptide) | ⇔ | Regulates IFN-γ/inflammation balance | 30837028 |

---

## Pathway Crosstalk (connection to existing KF cards)

| Connected KF card | Interaction with IFN-γ |
|-------------------|----------------------|
| JAK-STAT | IFN-γ → JAK1/JAK2 → STAT1 — canonical signaling |
| NF-κB | Synergy: IFN-γ ↑ iNOS, TNF-α in macrophages |
| TNF/TNFR | IFN-γ + TNF-α = potent macrophage activation, apoptosis |
| IL-12 family | IL-12 → STAT4 → T-bet → IFN-γ; IFN-γ → ↑ IL-12 from APCs |
| IL-10 | IL-10 ↓ IFN-γ; counter-regulation |
| TGF-β/SMAD | TGF-β ↓ T-bet → ↓ IFN-γ; Th1 vs Treg balance |
| Macrophage M1/M2 | IFN-γ drives M1; M2 ↓ IFN-γ response |
| NK cells | NK cells = major early IFN-γ source |
| CD8+ T cells | CTL produce IFN-γ; IFN-γ ↑ MHC I |
| Th17/Treg | IFN-γ ↓ Th17 differentiation |
| IDO/Kynurenine | IFN-γ ↑ IDO1 → Trp depletion → T cell suppression |
| AhR | Kynurenine → AhR → Treg (negative feedback) |
| NF-κB | Synergy with IFN-γ on iNOS, inflammatory cytokines |

---

## Vietnamese Terminology

| English | Tiếng Việt |
|---------|-----------|
| Interferon-gamma | Interferon-gamma (IFN-γ) |
| Type II interferon | Interferon lớp II |
| IFNGR (interferon gamma receptor) | Thụ thể interferon gamma |
| JAK-STAT pathway | Con đường tín hiệu JAK-STAT |
| STAT1 homodimer (GAF) | Đồng dimer STAT1 |
| Gamma-activated sequence (GAS) | Trình tự GAS |
| Interferon-stimulated genes (ISGs) | Gen kích thích interferon |
| IRF1 | Yếu tố phiên mã IRF1 |
| CIITA | Điều hòa phiên mã MHC class II |
| iNOS / Nitric oxide | NO synthase cảm ứng / Oxit nitric |
| IDO1 (indoleamine 2,3-dioxygenase) | Indoleamine 2,3-dioxygenase |
| M1 macrophage (classical activation) | Đại thực bào M1 (hoạt hóa cổ điển) |
| Th1 differentiation | Biệt hóa Th1 |
| T-bet | Yếu tố phiên mã T-bet |
| γδ T cells | Tế bào T gamma-delta |
| Granuloma formation | Hình thành u hạt |
| Correlate of protection | Chỉ thị bảo vệ |
| Antiviral state | Trạng thái kháng virus |
| Feed additive modulation | Điều biến bằng phụ gia thức ăn |
| Immune evasion | Né tránh miễn dịch |

---

## Dedup Keywords (for KF card creation)

When checking for existing cards before creating a new IFN-γ card, search for:

```bash
curl -s http://localhost:3003/api/cards | python -c "
import sys,json,re
cards = json.load(sys.stdin)
keywords = ['ifn-γ', 'ifn-gamma', 'interferon gamma', 'type ii interferon', 'ifng']
for c in cards:
    t = c['title'].lower()
    for kw in keywords:
        if re.search(r'\b' + re.escape(kw) + r'\b', t):
            print(f'MATCH [{kw}]: {c[\"title\"]}')
"
```

Use word-boundary regex (`\b`) to avoid false-positives: `IFN-γ` should NOT match `IFNGR`, `IFNAR`, or `TNF`.
