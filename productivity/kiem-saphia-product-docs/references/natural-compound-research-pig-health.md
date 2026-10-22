# Natural compound research for pig health products

## Workflow: Disease → Pathogen → Compound → Formulation → Cost

### 1. Disease catalog
Research 15-20 most common pig diseases in Vietnam by lifecycle stage (7kg → market).
For each: pathogen type (virus/bacteria), organ targeted, cellular mechanism,
prevalence %, mortality %, current treatment cost.

### 2. Match natural compounds
For each target (environment, FCR/digestive, diarrhea, respiratory):
- Search PubMed: `(compound) AND (pig/swine) AND (target)`
- Verify evidence level: in vivo on pigs > in vitro > rodent only
- Key compounds database:
  - **Thymol/Carvacrol**: broad-spectrum, environment + gut + respiratory
  - **Tannin**: diarrhea (blocks ETEC fimbriae adhesion), PMID 41056411
  - **Berberine**: APP, biofilm inhibition, PMID 42661110
  - **Inulin**: prebiotic, FCR improvement, PMID 42594272
  - **β-glucan**: immune activation, growth
  - **Allicin (garlic)**: FCR, antimicrobial, PMID 42046680
  - **Curcumin**: anti-inflammatory, PRRSV, respiratory, PMID 42646753
  - **Eucalyptol**: respiratory decongestant
  - **Tea tree oil**: environmental disinfection
  - **Acid citric**: water treatment, pH control

### 3. Evidence quality check
- `PMID` = PubMed indexed (strongest)
- In vivo on pigs with control group = strong
- In vitro only = moderate (flag as needing in vivo validation)
- No PubMed = weak (flag clearly)

### 4. Formulation options
- **Option A: Separate products** — 1 per target (5 SP: air spray, water, FCR, diarrhea, respiratory)
- **Option B: Combined** — 2 SP: environment (air+water) + internal 3-in-1 (FCR+diarrhea+respiratory)

### 5. Cost estimation
- Research raw material prices in VN (VND/kg or /L)
- Calculate cost per pig per month
- Compare with current antibiotic treatment cost
- Target: cheaper than or equal to antibiotics, or slightly more expensive but safer

### 6. Chinese research sources (highly valued)
- **Zhejiang University (PMID 33413687)**: Meta-analysis 10,228 pigs — plant extracts = primary antibiotic substitute. Key reference for any feed additive claim.
- **DSM-Firmenich Bazhou (PMID 40896479)**: Benzoic acid — cornerstone of swine nutrition
- **Chinese Academy of Agriculture Sciences (PMID 35739876)**: Aerosol bacteria in pig houses
- **Huazhong Agricultural University (PMID 41955653)**: ASFV in water, NaDCC inactivation
- **Note**: Few Chinese studies on continuous air disinfection during raising — research gap

### 7. pH 13-14 mechanism against swine pathogens
- **3 mechanisms**: (1) OH- saponifies lipids, (2) protein denaturation, (3) Ca2+/K+ hyperosmotic lysis
- **Coverage**: 82% of 28 major swine pathogens killed at pH 13-14
  - 10/10 enveloped viruses (ASFV, PRRSV, PEDV, CSFV, SIV...) — 100%
  - 8/8 Gram- bacteria — 100%
  - 4/4 Gram+ bacteria — 100% (needs pH >= 13)
  - Mycoplasma — 100% (killed at pH > 9)
  - Non-enveloped viruses (FMDV, PCV2) — partial (needs 30-60 min contact)
  - Oocysts (coccidia, Cryptosporidium) — weakened, not fully killed
- **Key evidence**: PMID 33238521 (FLI Germany — Ca(OH)2 completely inactivates ASFV in soil)
- **pH threshold table**: pH 10 = weak Gram- kill; pH 11 = Gram- + enveloped viruses; pH 12 = Gram+; pH 13 = all bacteria + enveloped viruses; pH 14 = spores (partial)

### 8. 3-route prevention analysis
- **Air**: 54 studies, weakest evidence, research gap. PMID 42671198 (FLI aerosol disinfection on aircraft), PMID 35739876 (CAS China aerosol bacteria)
- **Water**: 18 studies, moderate evidence. PMID 40896479 (DSM China benzoic acid), PMID 42234628 (water as AMR reservoir), PMID 39764372 (meta biosecurity)
- **Feed**: 101+ studies, strongest evidence. PMID 33413687 (Zhejiang meta 10,228 pigs)
- **Cost comparison**: Prevention ROI 2:1-5:1 vs treatment ROI 0.5:1-1:1

### 9. Product brief for sales team (newsprint style)
- Simplified science: explain overall effect, not per-ingredient mechanism
- No cost breakdown — only final selling price
- Ingredients listed as names only, no percentages
- 7 sections: Cong dung -> Co che -> Thanh phan -> Bao che -> Cach dung -> Thoi gian -> Luu y
- Layout: newsprint design (light bg, serif font, sharp corners, 2-column grid)
- Two main tabs: All-in-one (2 products) | San pham don (5 products)

### 10. HTML presentation
- Dark theme with inline SVG diagrams (early stage / technical audience)
- Newsprint design (light theme, serif, sharp corners) for sales-facing documents
- Compound tables with evidence levels + source badges (CN/EU/US/KR)
- Formula cards with 5-criteria analysis (compatibility, stability, safety, efficacy, risk)
- Published to preview.thefirstonly.com
