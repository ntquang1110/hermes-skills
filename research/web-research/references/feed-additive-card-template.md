# Feed Additive / Phytochemical Card Template

Use this template when creating KF cards about **feed additives, phytochemicals, natural compounds, or nutritional interventions** (essential oils, organic acids, tannins, polyphenols, MCFAs, prebiotics, specific botanicals, etc.).

This template bridges pathway/mechanism research (what a compound DOES) with practical application (how to USE it in swine production). It complements the existing pathway, virus, bacteria, and toxic agent templates.

## Card structure

### Title format
```
🌿 [Compound/Extract Name] — [Vietnamese subtitle with mechanism + species context]
```
Examples:
- `🌿 Tinh dầu (Essential Oils) trong dinh dưỡng heo — Cơ chế kháng khuẩn, chống oxy hóa, kháng viêm & bảo vệ hàng rào ruột`
- `🌿 Tannins trong dinh dưỡng heo — Phân loại, cơ chế tác dụng & ứng dụng thay thế ZnO`
- `🧪 Axit béo chuỗi trung bình (MCFAs/MCTs) — Cơ chế kháng khuẩn, bảo vệ hàng rào và ứng dụng trong dinh dưỡng heo`

### Section order (when all sections are relevant)

1. **Định nghĩa và phân loại**
   - What is it? Chemical family, sources, extraction methods
   - Classification table: type | source | active compound | key property
   - ISO/regulatory definition if applicable

2. **🧬 Thành phần hoạt chất chính**
   - Per active compound: structure formula, molecular weight, physico-chemical properties
   - Mechanism of action paragraph per compound
   - Key PMID citations per compound
   - For multi-compound additives: separate subsection for each major constituent

3. **⚙️ Cơ chế tác dụng**
   - Each mechanism gets its own sub-section with:
     - **Mechanism name**: e.g. "Kháng khuẩn — Phá vỡ màng tế bào"
     - Code-block flow diagram where helpful (→ arrow notation)
     - Molecular target, pathway, downstream effects
     - Species specificity (Gram+ vs Gram-, bacterial targets)
     - PMID citations per mechanism claim
   
   **Common mechanisms to cover (pick relevant ones):**
   - Antimicrobial (membrane disruption, quorum sensing, biofilm inhibition)
   - Antioxidant (Nrf2/KEAP1, SOD/GSH induction, ROS scavenging)
   - Anti-inflammatory (NF-κB, NLRP3, MAPK, cytokine modulation)
   - Gut barrier protection (tight junction upregulation, TEER, ZO-1/occludin/claudin)
   - Microbiota modulation (prebiotic effect, pathogen inhibition, SCFA production)
   - Immune modulation (TRAINED IMMUNITY, Th1/Th2 balance, IgA secretion)
   - Metabolic effects (enzyme inhibition/activation, receptor agonism)

4. **🐷 Ứng dụng trên heo**
   - Organize by production stage:
     - Heo con cai sữa (PWD prevention, growth performance)
     - Heo thịt / vỗ béo (feed efficiency, meat quality)
     - Heo nái (maternal transfer, reproductive performance)
   - Efficacy data: dose-response, comparison to positive controls (ZnO, antibiotics)
   - Table: Application | Dose (mg/kg feed) | Effect | PMID

5. **📊 Liều lượng tham khảo**
   - Table: Compound | Recommended dose | Stage | Main effect | Notes
   - Safety note: upper limits, palatability concerns, mucosal irritation at high doses
   - Formulation notes: microencapsulation, protected forms, synergistic blends

6. **🔄 Tương tác hiệp đồng (Synergistic Interactions)**
   - With organic acids (e.g. thymol/carvacrol + citric/fumaric acid)
   - With probiotics / postbiotics
   - With other phytochemicals
   - With antibiotics (adjuvant effect, resistance reversal)
   - With dietary fibers / prebiotics
   - Table: Blend composition | Synergy mechanism | Effect | PMID

7. **🧪 Ứng dụng thực tế (context-specific)**
   - Relevance to Vietnamese pig farming
   - Cost comparison (VND/kg feed)
   - Regulatory status (EU ban on ZnO, Vietnam roadmap)
   - Commercial products available (if known)
   - Production considerations (storage, mixing, stability)

8. **⚠️ Thách thức và rào cản**
   - Stability (volatility, oxidation, feed processing losses)
   - Palatability (off-flavors, feed intake reduction)
   - Batch-to-batch variability (chemotype, growing conditions)
   - Cost vs. benefit
   - Gap in in vivo studies (many compounds tested in vitro only)

9. **🔬 Hướng nghiên cứu tương lai**
   - Microencapsulation / targeted delivery
   - Epigenetic mechanisms (DNA methylation, miRNA)
   - Metagenomics / metabolomics approaches
   - Long-term safety and tissue residues
   - Combination therapy optimization

10. **📚 Bảng tham khảo (References)**
    - Columns: PMID | Journal (Year) | Key finding
    - Minimum 15-20 PMIDs for a deep card
    - Sort by relevance, not chronologically
    - Each mechanism claim in sections 1-5 should map to a PMID here

### When to shorten

If the additive has limited literature (<15 relevant PMIDs), merge sections:
- Combine 1+2 → **Giới thiệu và thành phần**
- Combine 5+6+7 → **Liều lượng và ứng dụng thực tế**
- Omit section 8 or 9

If the additive has a single dominant mechanism (e.g. MCFAs = primarily antimicrobial), expand that mechanism in section 3 and condense the others.

## Research workflow for feed additive cards

### Step 1 — Multi-angle PubMed search
Use 6-8 queries covering different aspects:
```
Query 1: [compound] swine intestinal barrier tight junction
Query 2: [compound] pig gut microbiota antimicrobial
Query 3: [compound] pig growth performance feed additive
Query 4: [compound] pig anti-inflammatory NF-kB
Query 5: [compound] pig antioxidant Nrf2
Query 6: [compound] antimicrobial mechanism Gram-positive bacteria membrane
Query 7: [compound] piglet diarrhea weaning
Query 8: [compound] synergism organic acid pig
```

Merge results, deduplicate, aim for 15-25 unique PMIDs.

### Step 2 — Wikipedia background
Search for the compound class (e.g. "Essential oil", "Tannin", "Polyphenol") to get:
- Chemical classification
- Biosynthesis / natural sources
- Historical use
- Basic mechanism descriptions

### Step 3 — Identify porcine-specific data
Not all papers are in pigs. Flag PMIDs that used:
- IPEC-J2 cells (porcine intestinal epithelial line) → strongest in vitro evidence
- In vivo pig trials (weaned piglets, grower-finisher, sows) → strongest practical evidence
- Other species (mice, poultry, humans) → use for mechanism support only

Prioritize porcine-specific papers in section 4 (Ứng dụng trên heo).

### Step 4 — Synergy search
Search `[compound] + organic acid pig` and `[compound] + probiotic pig` to identify synergistic blends. Feed additives are rarely used in isolation; synergy data is more valuable for practice.

## Example card structure (from Essential Oils card)

```
## 🌿 Định nghĩa và phân loại
→ Classification table: 5 groups (phenolic, phenylpropanoid, alcohol, ketone, sesquiterpenoid)

## 🧬 Thành phần hoạt chất chính
→ Carvacrol: mechanism, PMIDs
→ Thymol: mechanism, PMIDs  
→ Cinnamaldehyde: mechanism, PMIDs
→ Eugenol: mechanism, PMIDs

## ⚙️ Cơ chế tác dụng
→ Kháng khuẩn (màng tế bào, quorum sensing, biofilm)
→ Chống oxy hóa (Nrf2/ARE, SOD, GSH)
→ Kháng viêm (NF-κB, NLRP3, cytokine)
→ Bảo vệ hàng rào ruột (tight junction, TEER)
→ Điều hòa hệ vi sinh vật

## 🐷 Ứng dụng trên heo
→ PWD, tăng trưởng, chất lượng thịt

## 📊 Liều lượng tham khảo
→ Table: 6 compounds × dose/stage/effect

## 🔄 Tương tác hiệp đồng
→ +organic acids, +probiotics, +fiber, +antibiotics

## 🧪 Ứng dụng thực tế Việt Nam
→ Replace ZnO, cost estimates

## ⚠️ Thách thức
→ Volatility, palatability, cost

## 🔬 Hướng nghiên cứu tương lai
→ Microencapsulation, epigenetics, metagenomics

## 📚 References (25 PMIDs)
→ PMID | Journal | Key finding table
```

## Pitfalls

- **Do not over-promise**: Feed additives rarely match the efficacy of pharmacological ZnO or antibiotics in well-controlled trials. Acknowledge effect sizes and statistical significance.
- **Dose matters**: Many in vitro studies use concentrations that are not achievable in vivo (millimolar vs micromolar). Flag this discrepancy.
- **Formulation matters**: Pure compound vs. crude extract vs. encapsulated form. State which was used in each cited study.
- **Confounding effects**: Many feed additive studies also change diet formulation (reduced protein, added fiber). The observed effect may not be solely from the additive.
- **Publication bias**: Negative results are under-reported. A literature review that finds "mostly positive" effects may reflect this bias.
