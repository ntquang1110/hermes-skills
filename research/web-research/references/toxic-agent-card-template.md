# Toxic Agent / Contaminant Research Card — Template

Use this template when creating Knowledge Flow cards about **mycotoxins, heavy metals, environmental contaminants, or feed-borne toxicants** that affect swine health. Complements the pathway card template (`references/pathway-card-template.md`) — toxicant cards focus on **xenobiotic metabolism, toxicokinetics, and mitigation** rather than endogenous signaling.

## When to use

- Mycotoxins: aflatoxin, fumonisin B1, ochratoxin A, T-2 toxin, DON (already done), ZEA (already done)
- Heavy metals: cadmium, lead, mercury, arsenic
- Feed contaminants: dioxin, PAH, pesticide residues
- Anti-nutritional factors: trypsin inhibitors, gossypol, tannins
- Pharmaceutical residues in feed

## 10-section outline

### 1️⃣ Overview (Tổng quan)
- What is this toxicant? Source organisms (if mycotoxin: which fungal species)
- **IARC carcinogenicity classification** (Group 1/2A/2B/3)
- Why it matters for pig farming (tropics vs temperate, feed raw materials affected)
- **Key message box** (1-2 sentences of practical importance)

### 2️⃣ Chemical Structure & Types (Cấu trúc hóa học & phân loại)
- Chemical family (e.g., difurocoumarin for aflatoxin, sphinganine analog for fumonisin)
- Table of major subtypes with toxicity ranking:
  | Type | Source | Relative toxicity | Key feature |
  |------|--------|-------------------|-------------|
  | AFB1 | A. flavus | ++++ | C8-C9 double bond → epoxide |
  | AFB2 | A. flavus | ++ | No 8,9-double bond |
- **Structure-toxicity relationship**: which chemical moiety determines bioactivation

### 3️⃣ Sources & Growth Conditions (Nguồn gốc & điều kiện phát triển)
- **Producing organisms**: table of species, their preferred substrates, geographic distribution
- **Environmental triggers**: temperature range (optimum), moisture/aw, pH
- **Crops most affected**: specific raw materials in swine feed (maize, peanut meal, rice bran, etc.)
- **Climate change impact**: expanding geographic range, shifting seasons
- **Vietnamese context**: specific crops and regions most at risk

### 4️⃣ Toxicokinetics (Hấp thu, chuyển hóa, thải trừ)
```
Toxicant (in feed)
    │
    ▼ GI tract absorption (site, mechanism)
    │
    ▼ Portal vein → Liver (FIRST PASS)
    │
    ├── Phase I (CYP450): BIOACTIVATION (if relevant)
    │     └──→ Reactive metabolite → Damage
    │
    └── Phase II (GST/UGT/SULT): DETOXIFICATION
          └──→ Conjugate → Bile/Urine
```
- **ADME table**: Absorption (site, %, mechanism), Distribution (plasma protein binding, tissue affinity), Metabolism (CYP isoforms, Phase II enzymes), Excretion (bile vs urine, half-life)
- **Bioactivation vs detoxification balance** — critical parameter determining species susceptibility
- **Species comparison**: pig vs poultry vs cattle vs human (why pig is sensitive/resistant)
- **Maternal transfer**: placental barrier, colostrum/milk transfer
- **Key biomarker**: what to measure (urine, serum, tissue adduct)

### 5️⃣ Molecular Toxicity Mechanisms (Cơ chế gây độc phân tử)
- **Primary mechanism** (the main mode of action):
  - Direct DNA damage (adduct → mutation pattern → p53 hot spot)
  - Protein synthesis inhibition
  - Enzyme inhibition (ceramide synthase for fumonisin)
  - Oxidative stress / glutathione depletion
  - Mitochondrial dysfunction
- **Signal pathway diagram** (markdown code block):
  ```text
  Compound → CYP → Epoxide → DNA adduct → p53 mutation → HCC
  ```
- **Secondary/tertiary mechanisms**: oxidative stress, ER stress, apoptosis, ferroptosis, autophagy dysregulation
- **Key molecular targets**: specific proteins, genes, transcription factors affected
- **Mutational signature** if known (e.g., GC→TA transversion at p53 codon 249)

### 6️⃣ Effects on Pig Health (Ảnh hưởng lên sức khỏe heo)
- **Acute toxicity** (high dose, short exposure):
  - Clinical signs, LD50 (oral), target organ damage
  - Pathological findings (gross + histopathology)
- **Chronic/subchronic toxicity** (low dose, long exposure):
  - Growth performance: ↓ ADG, ↓ FI, ↑ FCR with dose-response data
  - Organ-specific: liver (AST/ALT/GGT), kidney (BUN/creatinine), lung, brain
  - Immune suppression: ↓ IgG, ↓ lymphocyte proliferation, ↓ NK activity, ↓ vaccine response
  - Intestinal barrier: tight junction proteins, permeability, gut microbiota dysbiosis
- **Reproductive toxicity** (if relevant): boar semen quality, sow fertility, fetal development, piglet birth weight
- **Interactions with pathogens**: does this toxicant increase susceptibility to PRRSV, PCV2, PEDV, ETEC, Salmonella?
- **Use tables** for dose-response data:
  | Dose (ppb) | Duration | ↓ ADG (%) | ↑ AST | ↑ ALT | PMID |
  |------------|----------|-----------|-------|-------|------|

### 7️⃣ Toxic Doses & Safety Limits (Liều độc & ngưỡng an toàn)
- **Acute toxicity**: LD50 by species (table)
  | Species | LD50 oral (mg/kg BW) | Route | Notes |
  |---------|---------------------|-------|-------|
  | Pig | 0.6 | oral | Most sensitive |
  | Rat | 7.2-17.9 | oral | 12-30x less sensitive |
- **No Observed Effect Level (NOEL)** / Lowest Observed Effect Level (LOEL) for pigs
- **Regulatory limits table**:
  | Jurisdiction | Feed type | Limit (μg/kg) | Reference |
  |-------------|-----------|---------------|-----------|
  | EU | Pig feed | 5-50 (AFB1) | EC 574/2011 |
  | FDA | Pig feed | 100-300 (total) | 21 CFR |
  | Vietnam (QCVN) | Piglet feed | 20 (AFB1) | QCVN 01-190:2020 |
  | Vietnam (QCVN) | Pork feed | 50 (AFB1) | QCVN 01-190:2020 |
- **Maximum tolerable daily intake** (if established)
- **Practical monitoring**: typical ELISA test strip cut-offs, HPLC reference method

### 8️⃣ Prevention & Mitigation (Giải pháp phòng ngừa & giảm độc)
- **Pre-harvest**: resistant varieties, irrigation, biocontrol (e.g., A. flavus AF36 for aflatoxin)
- **Post-harvest**: drying (<13% moisture), sorting/grading, proper storage (temp, humidity)
- **Physical decontamination**: thermal degradation, irradiation, washing/nixtamalization
- **Chemical detoxification**: ammoniation, ozonation — but may affect nutritional quality
- **Adsorbents** (bind in GI tract, reduce bioavailability):
  | Adsorbent | Binding capacity | Dose | Efficacy in pigs | PMID |
  |-----------|-----------------|------|------------------|------|
  | Bentonite | High (AFB1) | 0.5-2% | ↓50-70% | |
  | Zeolite | Moderate | 1-2% | ↑ growth, ↓ AST | |
  | Yeast cell wall | Moderate (AFB1) | 0.1-0.5% | ↓ absorption | |
  | Humic substances | Broad | 0.5% | ↓ TNF-α, ↑ IgG | |
- **Biotransformation**: enzymes/bacteria that degrade the toxicant (Flavobacterium, Bacillus, Lactobacillus)
- **Dietary modulation** (support liver/immune function):
  | Compound | Mechanism | Dose | Efficacy | PMID |
  |----------|-----------|------|----------|------|
  | Silymarin | ↑ GST/GSH, ↓ CYP | | Hepatoprotection | |
  | Curcumin | Antioxidant, anti-inflammatory | | ↓ hepatic injury | |
  | Grape seed extract | ↑ GST, ↓ oxidative stress | 8% in feed | In vivo pig | |
  | Selenium/Vitamin E | ↑ GPx, ↓ lipid peroxidation | | General protection | |
  | SDPP | ↑ IgG, ↓ inflammation | | Support for AFB1-challenged piglets | |
  | Folic acid | Methyl donor for DNA repair | | ↓ genotoxicity? | |
- **Combined strategies**: bentonite + botanical additives (multi-pronged)
- **Practical monitoring**: ELISA strip tests at feed mills, regular HPLC confirmation

### 9️⃣ Interactions with Other Toxicants (Tương tác với các độc tố khác)
- **Co-contamination patterns**: which toxicants co-occur in the same raw materials
- **Synergistic vs additive effects** table:
  | Co-contaminant | Interaction type | Animal effect | PMID |
  |---------------|-----------------|---------------|------|
  | AFB1 + DON | Synergistic | ↑ liver damage + ↑ barrier disruption | |
  | AFB1 + ZEA | Additive | Liver + reproductive damage | |
  | AFB1 + FB1 | Synergistic | ↑ HCC risk | |
- **Combined exposure from feed**: realistic field scenarios with multiple mycotoxins
- **Interaction with drugs/vaccines**: does the toxicant affect drug metabolism (CYP induction/inhibition)?

### 🔟 Summary & References (Kết luận & Tài liệu tham khảo)
- **Key takeaways for pig farming** (table format):
  | Message | Detail |
  |---------|--------|
  | Risk level | How dangerous in Vietnamese context |
  | Lowest effect dose | Practical threshold to watch |
  | Most affected category | Piglet, grower, or sow? |
  | Primary raw material risk | Which ingredient to monitor |
  | Best mitigation strategy | Cost-effective, proven solution |
- **Map to existing KF cards**: which cards this topic connects to (crosstalk)
- **Complete PMID table**:
  | PMID | Journal (Year) | Contribution |
  |------|---------------|-------------|
  | 12345678 | Toxins (2025) | Mechanistic study in IPEC-J2 cells |
  | 87654321 | J Anim Sci (2020) | Growth trial on pigs |
- **Wikipedia sources** for background chemistry/toxicology
- **Regulatory documents**: QCVN references, EU/US standards

## Card conventions

- **Title**: `🧪 Toxicant name — Vietnamese description with practical context (emoji + English technical name + Vietnamese)`
- **Tags**: 15-25 specific tags covering:
  - Toxicant name (Vietnamese + English + abbreviation)
  - Producing organisms
  - Affected organ systems (liver, kidney, gut, immune)
  - Mitigation strategies used (bentonite, enzyme, botanical)
  - Related mycotoxins/diseases
  - Geographic relevance (Vietnam, tropical)
- **topic_slug**: `chan-nuoi-heo` for swine
- **source_url**: primary Wikipedia page or comprehensive review DOI
- **Reading time**: 300-900 seconds (5-15 minutes)

## Comparison: Toxicant card vs Pathway card

| Aspect | Toxicant card | Pathway card |
|--------|---------------|-------------|
| **Core focus** | Xenobiotic metabolism, toxicokinetics, mitigation | Endogenous signaling, cell biology |
| **Sections unique** | Toxicokinetics, regulatory limits, prevention, adsorbents | Negative regulation, crosstalk with other pathways |
| **Pathway crosstalk** | How the toxicant HIJACKS pathways | How pathways INTERACT endogenously |
| **Regulatory** | QCVN/FDA/EU limits — REQUIRED | Not applicable |
| **Mitigation** | Adsorbents, biotransformation, dietary — REQUIRED | Feed additive modulation |
| **LD50** | REQUIRED for every toxicant | N/A |
| **Bioactivation** | Phase I→damage vs Phase II→detox — central tension | N/A (this is endogenous regulation) |
| **Examples in KF** | Aflatoxin, DON, ZEA | TGF-β/SMAD, NF-κB, Wnt/β-catenin |
