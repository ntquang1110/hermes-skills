# Pathway/Mechanism Research Card — Template

Use this template when creating Knowledge Flow cards about **signaling pathways, molecular mechanisms, or cytokine families** in swine/veterinary research. Complements the virus/pathogen card template (`references/virus-pathogen-card-template.md`).

## 10-section outline

### 1️⃣ Overview (Tổng quan)
- What is this pathway? One-paragraph plain-language intro
- **Family/Component table** listing all members with receptor, co-receptor, and primary function
- Keep 3-5 key takeaway bullet points at the very top

### 2️⃣ Molecular Structure (Cấu trúc)
- Protein/coding gene details (length, kDa, chromosome)
- Domain architecture (conserved motifs, catalytic domains, binding sites)
- Isoforms or splice variants (if relevant)
- Glycosylation / post-translational modification sites

### 3️⃣ Signaling Mechanism (Con đường tín hiệu)
- **Canonical pathway** (step by step: ligand → receptor → adaptor → kinase → TF → gene target)
- **Non-canonical / alternative pathways** (if any)
- **Classical vs alternative signaling distinction** (e.g., IL-6 classical vs trans-signaling)
- Use text diagrams (``` ) for complex cascades:
  ```
  Ligand → Receptor → JAK → STAT3 dimer → Nucleus → Gene X
  ```
- **Negative regulation** (SOCS, PIAS, phosphatases, decoy receptors)
- **Sub-cellular localization** if relevant

### 4️⃣ Biological Function (Chức năng sinh học)
- **Normal physiological role** — what does this pathway do in a healthy animal?
- **Organ/tissue-specific effects** (gut, liver, lung, immune cells, brain)
- **Acute vs chronic** — different responses depending on context
- **Acute phase response** (for cytokines): APP proteins induced, time course

### 5️⃣ Developmental & Temporal Aspects (Theo giai đoạn)
- **Neonate** (first week): colostrum, innate immunity development
- **Weaning** (21-35d): stress response, intestinal adaptation
- **Grower/finisher**: adult baseline, homeostatic regulation
- **Sow**: pregnancy, lactation, colostrum composition
- Use a table comparing IL-6/CRP/Hp etc. levels across stages

### 6️⃣ Disease Relevance (Bệnh lý)
- **Viral infections**: PRRSV, CSFV, PEDV, PCV2, SIV — how does the pathway change?
- **Bacterial infections**: ETEC, Salmonella, Lawsonia, S. suis
- **Mycotoxin exposure**: DON, ZEA, aflatoxin
- **Metabolic/inflammatory disease**: obesity, heat stress, lameness
- **Mechanism** column: specific molecular interaction with pathogen protein
- Use a table: | Disease | Pathway change | Mechanism | Consequence |

### 7️⃣ Nutritional & Pharmacological Modulation (Điều hòa qua dinh dưỡng)
- **Feed additives that DOWN-regulate** this pathway (anti-inflammatory)
- **Conditions/compounds that UP-regulate** (pro-inflammatory triggers)
- Use a table: | Compound | Direction | Mechanism (specific) | PMID |
- Include: probiotics, prebiotics, organic acids, Zn/Cu/Se, vitamins, plant extracts (curcumin, quercetin, anthocyanin, etc.), amino acids
- Also include stressors: heat, LPS, toxins, crowding

### 8️⃣ Related Family / Isoform Details (Các thành viên liên quan)
- If this is a family (e.g., IL-6 family, MAPK family), list all members
- Each member: receptor, tissue expression, primary function in swine
- Specialized roles (e.g., LIF in embryo implantation, OSM in thyroid)
- Cross-species comparison if relevant (pig vs human vs mouse)

### 9️⃣ Pathway Crosstalk (Tương tác với các con đường khác)
- How does this pathway connect to NF-κB, JAK-STAT, MAPK/ERK, PI3K/AKT, Nrf2, NLRP3, autophagy, apoptosis?
- **Positive feedback loops**: Pathway A → Pathway B → Pathway A (amplification)
- **Negative crosstalk**: Mutual inhibition or compensatory activation
- Use a table: | Interacting pathway | Direction | Mechanism | Biological significance |

### 🔟 Summary Tables + References
- **Key biomarker table**: | Biomarker | Source | IL-6 regulated? | Up in | Diagnostic use |
- **Complete PMID reference table**: | PMID | Contribution | DOI |
- **Wikipedia pages** used for background
- Ensure every mechanistic claim has at least one PMID anchor

## Card conventions

- **Title**: `🧬 Pathway name — Vietnamese subtitle (emoji + English + Vietnamese)`
- **Content**: Vietnamese with English technical terms preserved
- **Tags**: 15-31 tags covering: pathway name, family members, species, related pathways, feed additives, disease associations
- **Reading time target**: 300-1020 seconds (5-17 minutes)
- **topic_slug**: `chan-nuoi-heo` for swine nutrition/immunology
- **source_url**: primary Wikipedia page or DOI

## Research workflow (for pathway cards)

1. **Wikipedia**: Search 5-8 queries covering pathway basics + family members
2. **PubMed Round 1**: 8 mechanism-specific queries, 6 results each, collect unique PMIDs
3. **PubMed Round 2** (if needed): 8 additional query angles for disease relevance + nutrition
4. **Fetch abstracts**: top 20 PMIDs, scope each to its PubmedArticle block
5. **Compile**: follow 10-section outline above
6. **Final dedup**: multi-keyword check before POST
7. **POST**: Pattern D (Python urllib script) — not curl heredoc
