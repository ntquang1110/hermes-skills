# Successful Card Examples — Reference Library

This file documents the structure of successful knowledge cards that passed all quality gates (201 Created, reading time 240-720s).

Current examples:
- **Example 1:** β-glucan → Dectin-1 → NF-κB (table + numbered steps, single linear pathway)
- **Example 2:** ENS + SCFAs/Butyrate ở heo (flow diagrams + multi-pathway, parallel mechanisms)
- **Example 3:** Intestinal Barrier in Swine (clinical/solutions-driven, problem-first, intervention comparison)
- **Example 4:** PRRSV — Virus-host interaction (layered deep-dive: structure → immune evasion → clinical)
- **Example 5:** Iron Metabolism in Swine (component catalog + regulation matrix + PMID contribution reference table)

---

## Example 1 — β-glucan → Dectin-1 → NF-κB

## Card Structure

Every card should follow this template:

```
## 🧬 [Emoji] [Mechanism/Pathway name]

**Mô tả bản chất:** [3-4 sentence explanation of the core mechanism]

### Thành phần chính:
[Table: Component | Role]

| Thành phần | Vai trò |
|------------|---------|
| **Protein A** | Description |
| **Gene B** | Description |
| **Pathway C** | Description |

### Quy trình [N] bước:

1. **Bước 1** — Description with emoji
2. **Bước 2** — ...
3. **Bước 3** — ...

### Ứng dụng cụ thể:

- **Application 1:** Detail with citation [PMID: NNNNNNNN, Journal Year]
- **Application 2:** Detail with citation

### Yếu tố ảnh hưởng:

- **Factor 1:** Explanation
- **Factor 2:** Explanation

### Nghiên cứu mới nhất (YEAR-YEAR):

1. Study 1 description [PMID: NNNNNNNN, Journal Year]
2. Study 2 description [PMID: NNNNNNNN, Journal Year]
3. Study 3 description

> 🔬 **Bản chất cốt lõi:** [One-line insight summarizing the mechanism]

**Nguồn tham khảo:**
- Wikipedia — [Topic]
- PMID NNNNNNNN — [Journal], [Year]
- PMID NNNNNNNN — [Journal], [Year]
```

### Key Success Factors

1. **Deep mechanism first:** Start with molecular detail (pathway, proteins, genes), not surface facts
2. **Tables for components:** Component | Role table is more readable than bullet lists
3. **Numbered step-by-step:** Pathways read as numbered sequences, not paragraphs
4. **Applications with evidence:** Each application claim backed by a specific PMID
5. **Recent studies section:** Shows currency (2025-2026 studies demonstrate active research)

---

## Example 2 — ENS + SCFAs/Butyrate ở heo (flow diagrams + multi-pathway format)

Posted: 2026-07-17
Topic: heo (pig farming / gut-brain axis)
Card ID: `ba8ce3dd-cc2f-42d2-a278-d9542e2f16e8`
Title: 🧠 Hệ thần kinh ruột (ENS) ở heo — "Bộ não thứ hai" điều hòa nhu động ruột, hàng rào niêm mạc và tương tác vi sinh vật
Reading time: 480s (8 minutes)
Sources: Wikipedia + 8 PubMed articles (PMID 39440960, 41955110, 41740169, 41155135, 40937500, 35607985, 38536635, 41684539)

### Key differences from Example 1 (table-driven style)

| Aspect | Example 1 | Example 2 |
|--------|-----------|-----------|
| Structure | Tables + numbered steps | Flow diagrams + pathway sections |
| Pathways | Single (β-glucan → Dectin-1 → NF-κB) | Three parallel (HDAC, GPCR, β-oxidation) |
| Diagrams | None | ASCII arrow flow diagrams |
| Evidence per claim | Grouped in "Recent studies" | Inline under each pathway |
| Disease coverage | One application (trained immunity) | Multiple (ETEC, PEDV, glyphosate, ammonia) |

### Alternate card template (flow-diagram style)

```markdown
## 🧠 [Emoji] [Topic title]

**Mô tả bản chất:** [Core explanation with comparative biology]

### 📋 Anatomy / Classification table
[2-3 column table for structural overview]

### 🔬 [N] pathways of [Topic]

**Pathway 1 — [Name]:** [Description]
```
[ASCII arrow flow diagram]

[Reactant → Enzyme/Protein → Intermediate → Product → Effect]
```
> 📚 [Citation] — Key finding

**Pathway 2 — [Name]:** ...
**Pathway 3 — [Name]:** ...

### 🐷 Evidence from pigs (or specific studies)

**🟢 Application 1:**
- Finding
> 📚 [Citation PMID]

### 🧪 Integrated signal diagram

```
[ASCII art showing cross-talk between pathways]
```

### ⚕️ Clinical/Production implications

1. **Recommendation 1** — Reasoning with citation
2. **Recommendation 2** — Reasoning

> ⚠️ **Cảnh báo:** Important caveat or warning

### 📚 Nguồn tham khảo
[Numbered list with full citations]
```

### When to use each style

| Style | Best for |
|-------|----------|
| **Table + numbered steps** (Example 1) | Single linear pathway, small number of components (< 8), simple cause-effect chain |
| **Flow diagram + multi-pathway** (Example 2) | Complex topic with 2-4 parallel mechanisms, cross-talk interactions, multiple disease applications, systems-level view |

### Cross-cutting success factors (both styles)

1. **Every factual claim has a PMID citation** — no orphan statements
2. **Tables use markdown pipe syntax** — renderable in the feed detail page
3. **Flow diagrams use ASCII art** — not images, works in any text renderer
4. **Banner callouts** for key insights (`> 🔬`, `> ⚠️`, `> 🐷`)
5. **Vietnamese diacritics + real emoji** — never shortcodes
6. **Multiple angle research** — search PubMed from 3-5 angles (e.g., ENS + porcine, butyrate + HDAC, SCFA + GPCR, gut-brain axis, tight junction + butyrate) then merge and deduplicate
7. **References section** at bottom with Wikipedia + all PMIDs in consistent format

---

## Example 3 — Intestinal Barrier in Swine (clinical/problem → mechanism → solution format)

Posted: 2026-07-17
Topic: chan-nuoi (pig farming / intestinal health)
Card ID: `44249101-54c3-44e9-9ef2-fadfb0d9bfa3`
Title: 🧱 Hàng rào ruột heo (Intestinal Barrier) — Cấu trúc, chức năng và cơ chế điều hòa
Reading time: 600s (10 minutes)
Sources: Wikipedia (Intestinal mucosal barrier, Tight junction) + 5 PubMed articles (PMID 39337525, 42121259, 42076684, 42039840, 40920374)

### Card template (clinical/solutions-driven style)

```markdown
## 🧱 [Emoji] [Topic title]

**Định nghĩa:** [Definition with clinical context, why it matters in production]

> 🔬 **Bản chất cốt lõi:** [One-sentence insight with practical implication — what happens when this system fails]

---

## 🧬 [Section heading — layers / components]

### Lớp 1 — [First layer name]

| Thành phần | Mô tả |
|-----------|-------|
| **Component A** | Function |
| **Component B** | Function |

> Callout explaining role of this layer

### Lớp 2 — [Second layer]

**Cell types involved:**

| Loại tế bào | Chức năng chính |
|-------------|----------------|
| **Cell type 1** | Function |
| **Cell type 2** | Function |

### 🧩 [Sub-mechanism name] — Description

**Core proteins / molecules:**

| Protein | Vai trò |
|---------|--------|
| **Name** | Role |
| **Name** | Role |

> 🔬 **Cơ chế phân tử:** [Mechanism explanation — what happens at molecular level when stress/pathogens hit]

---

## ⚕️ [Problem domain title]

### [Stress trigger] — Most dangerous phase

[Description of the critical period using emoji bullet points]

**Hậu quả trên [system]:**

| Biến đổi | Cơ chế |
|----------|--------|
| ↓ Change | Pathway description |
| ↑ Change | Pathway description |

> 🔬 **Con đường phân tử:** [Detailed molecular cascade from trigger to outcome]

### [Category of solutions]

#### 🥇 [Solution 1] — Mechanism of action

| Cơ chế | Chi tiết |
|--------|---------|
| Effect A | Description |
| Effect B | Description |

> **Nguồn:** [Author et al., Year, Journal — Title. PMID: NNNNNNNN]

#### 🥈 [Solution 2]

[List with bullet points and source citation]

#### 🥉 [Solution 3]

[List with bullet points and source citation]

#### 🌿 [Solution 4]

| Nhóm | Cơ chế |
|------|--------|
| **Group A** | Description |
| **Group B** | Description |

---

## 📊 Sơ đồ tín hiệu điều hòa

```
TRIGGER (stress, pathogen, diet change)
       ↓
  [Intermediate cell/mediator]
       ↓
  [Transcription factor/Pathway activation]
       ↓
  [Effector molecules ↑]
       ↓
  [Cellular effect → tight junction opened]
       ↓
  [Systemic outcome → disease]

─────── PROTECTIVE FACTORS ───────
       ↑
  Solution 1 → [Mechanism: description]
  Solution 2 → [Mechanism: description]
  Solution 3 → [Mechanism: description]
```

---

## 🔬 Kết luận và ý nghĩa thực tiễn

| Chiến lược | Hiệu quả | Lưu ý |
|-----------|---------|-------|
| **Strategy A** | 🟢 Best outcome | ⚠️ Caveat |
| **Strategy B** | 🟡 Moderate | Caveat |
| **Strategy C** | 🟢 Multi-target | Limitation |

> 💡 **Insight chính:** [Key takeaway — what ties everything together]

---

## 📚 Nguồn tham khảo

1. [Full citation with DOI for each source]
2. [Wikipedia — Topic. URL]
```

### When to use this style

| Style | Best for | Example |
|-------|----------|--------|
| **Table + numbered steps** (Ex. 1) | Single linear pathway, < 8 components | β-glucan → Dectin-1 → NF-κB |
| **Flow diagram + multi-pathway** (Ex. 2) | 2-4 parallel mechanisms, cross-talk | ENS + SCFAs/butyrate pathways |
| **Clinical/solutions-driven** (Ex. 3) | Production problem with multiple interventions, need decision guide | Intestinal barrier + weaning diarrhea |

### Key features of Example 3 style

1. **Problem-first framing:** Opens with clinical/production challenge, not just biology
2. **Layer-by-layer anatomy:** Breaks system into physical layers (mucus → epithelium → immunity)
3. **Stress → mechanism chain:** Links practical trigger (weaning) to molecular cascade (NF-κB → MLCK → tight junction opening)
4. **Comparison table of solutions:** Side-by-side evaluation of all available interventions (ZnO, butyrate, probiotics, plant extracts) with efficacy rating 🟢🟡 and caveats ⚠️
5. **Decision guide at bottom:** "Chiến lược | Hiệu quả | Lưu ý" table for practical decision-making
6. **Signal diagram with protective factors:** ASCII flow showing both disease pathway AND where each intervention blocks it
7. **Clinical caveats:** Always mentions regulatory status (e.g., EU cấm ZnO từ 2022)

---

## Example 4 — PRRSV Virus-Host Interaction (layered deep-dive: structure → immune evasion → clinical)

Posted: 2026-07-18 16:00
Topic: chan-nuoi (pig farming / virology)
Card ID: `484bd06b-8ce5-4e4e-95e3-f8ffe0368a9c`
Title: 🐷 PRRSV — Cơ chế tương tác virus - vật chủ, né tránh miễn dịch và bệnh sinh
Reading time: 720s (12 minutes)
Sources: Wikipedia (PRRSV-2, Betaarterivirus suid 1) + 7 PubMed articles (PMID 40796041, 39264156, 41070967, 41251350, 42075672, 41775077, 42153738)

### Card template overview

This style is designed for **virus-host interaction** topics — virus structure, replication cycle, immune evasion mechanisms, and clinical significance. It combines:
- Wikipedia for virus taxonomy, structure, and replication overview
- PubMed (3-4 query angles) for immune evasion mechanisms and recent research
- A "redundant antagonism" framing to explain why the virus is hard to control

### Template skeleton

```markdown
## 🐷 [Emoji] [Virus name] — [Slogan/subtitle]

**Mô tả bản chất:** [2-3 sentence overview — virus classification, key pathogenic feature, economic/production impact]

### 🧬 Đặc điểm virus

[Table: Classification | Genome | Key proteins | Host | Stability]

### 🏗️ Cấu trúc bộ gen và protein

[ASCII genome map showing ORF/NS regions]
[Table: Viral proteins with Function + Immune evasion mechanism]

> 🔬 **Bản chất cốt lõi:** [One-sentence insight on the virus's core pathogenic strategy]

### ⚙️ Vòng đời nhân lên

[Numbered step-by-step: 1️⃣ Entry → 2️⃣ Uncoating → 3️⃣ Translation → 4️⃣ Replication → 5️⃣ Assembly → 6️⃣ Release]

### 🛡️ Cơ chế tương tác virus — vật chủ

[ASCII pathway diagram showing virus-host interaction — viral proteins on left, host pathways on right, X marks where virus blocks them]

#### 🎯 [Viral proteins and their cellular targets table]

[Table: Viral Protein | Host Target | Mechanism | Consequence]

#### 🧊 Other evasion mechanisms

[Table: Mechanism | Description]

### 📋 Bệnh sinh và triệu chứng

[Acute phase vs chronic phase]
[Table: Symptoms by host category]

### 🔬 Đáp ứng miễn dịch của vật chủ

[Innate immunity — why it fails]
[Adaptive immunity — why it's slow/weak]

### ⚕️ Prevention/Control strategies

[Table: Method | Description | Effectiveness | Limitations]

### 🧪 Recent research — Antiviral directions

[Table: Direction | Mechanism | Stage]

> 🔬 **Bản chất cốt lõi:** [Summary insight — why existing vaccines fail, what future solutions look like]

**Nguồn tham khảo:**
[Numbered list with Wikipedia + all PMIDs]
```

### Research workflow for virus-host topics

| Step | Source | Query pattern |
|------|--------|---------------|
| 1. Virus structure & taxonomy | Wikipedia (`srsearch`) | `"[virus full name]" OR "[virus acronym]"` |
| 2. Host-pathogen interaction | PubMed `esearch` | `"[virus] immune evasion mechanism interferon antagonism"` |
| 3. Pathogenesis & immunology | PubMed `esearch` | `"[virus] pathogenesis immunology review"` |
| 4. Structure & replication | PubMed `esearch` | `"[virus] structure replication nonstructural proteins"` |
| 5. Therapy & vaccines | PubMed `esearch` | `"[virus] vaccine therapy antiviral"` |
| 6. Cross-protection | PubMed `esearch` | `"[virus] cross-protection vaccine design"` |

**Key:** Use 3-5 different PubMed query angles, merge results, deduplicate by PMID. Pace queries with `time.sleep(1.5)` between groups to avoid rate limits.

### Key features of Example 4 style

1. **Layered structure:** Virus structure (foundation) → genome/proteins → replication cycle (mechanism) → immune evasion (depth) → clinical (application)
2. **ASCII pathway diagram:** Shows the multi-target attack (e.g., viral proteins hitting every node of the interferon pathway)
3. **"Redundant antagonism" framing:** Positions the virus's immune evasion as a key insight — multiple viral proteins targeting the same host pathway at different nodes, making traditional single-target vaccines ineffective
4. **Detailed viral protein table:** One row per protein with four columns (Protein | Host Target | Mechanism | Consequence)
5. **Phenomenon → mechanism → clinical:** Maps each clinical sign to its molecular cause (e.g., "reproductive failure → PAM destruction → weak immune response → persistent viremia")
6. **Recent research table:** New antiviral strategies (TRIM29, GP2a inhibitors, gene-edited CD163-knockout pigs)
7. **Economic context:** Opens with production impact (panzootic, billions in losses) to establish relevance

### Five-card style decision guide

| Style | Best for | Core structure |
|-------|----------|---------------|
| **Table + numbered steps** (Ex. 1) | Single linear pathway, < 8 components | Table → Numbered steps → Applications |
| **Flow diagram + multi-pathway** (Ex. 2) | 2-4 parallel mechanisms, cross-talk | Diagrams → Parallel pathways → Integrated diagram |
| **Clinical/solutions-driven** (Ex. 3) | Production problem + multiple interventions | Problem → Layers → Interventions → Decision guide |
| **Virus-host interaction** (Ex. 4) | Virus structure + immune evasion + clinical | Structure → Genome → Replication → Immune evasion → Clinical |
| **Component catalog + regulation matrix** (Ex. 5) | Metabolism/nutrition with 10+ components, multi-factor regulation, species-specific differences | Table catalog → Regulation axes → Disorders → PMID contribution table |

---

## Example 5 — Iron Metabolism in Swine (component catalog + regulation matrix + PMID reference table)

Posted: 2026-07-25
Topic: chan-nuoi (pig farming / mineral metabolism)
Card ID: `86b36ab1-2dad-4aa6-aec4-5ba25407697d`
Title: 🧬 Chuyển hóa Sắt (Iron Metabolism) ở heo — Hepcidin/Ferroportin axis, hấp thu ruột, dự trữ và điều hòa toàn thân
Reading time: 900s (15 minutes)
Sources: Wikipedia (7 pages: Human iron metabolism, Hepcidin, Ferroportin, Transferrin, Ferritin, Iron-deficiency anemia, Iron overload) + 18 PubMed articles

### Card structure pattern

Optimized for **metabolism/nutrition topics** with 10+ components, multiple regulatory layers, species-specific differences, and practical applications.

**Section sequence:**
1. 🔬 **Tổng quan** — generic biology → species-specific hook
2. 🧬 **Cơ chế hấp thu / vận chuyển / dự trữ** — one emoji-marked section per mechanism
3. 🎯 **Điều hòa trung tâm** — master regulator with upstream regulation table
4. 🧬 **Điều hòa nội bào** — post-transcriptional control (e.g., IRP/IRE)
5. 🐷 **Đặc thù loài** — what makes this topic unique in pigs
6. 🛡️ **Tương tác với hệ miễn dịch** — nutritional immunity
7. 🔗 **Tương tác vi chất** — competitive antagonism table
8. 📋 **Rối loạn** — deficiency + overload with diagnostics
9. 📊 **Bảng tổng hợp protein chủ chốt** — Protein | Gene | Function | Regulation
10. 🧪 **Ứng dụng thực tiễn** — actionable numbered recommendations
11. 📚 **Tài liệu tham khảo** — PMID contribution table

**Key structural innovations:**

**A) PMID contribution reference table:**
```
| PMID | Bài báo | Đóng góp chính |
|------|--------|----------------|
| 12345678 | Author, Journal (Year). | Key finding contributed to section X |
```
Instead of a flat reference list, each PMID has a "Đóng góp chính" column describing what specific finding that paper contributed. Prevents future re-research by documenting why each citation was used.

**B) Regulation matrix tables (Factor | Effect | Molecular mechanism):**
```
| Yếu tố | Tác động | Cơ chế phân tử |
|--------|----------|----------------|
| Factor A | 🔺 Increase | Receptor → Pathway → Transcription factor → Gene |
| Factor B | 🔻 Decrease | Factor → Inhibitor → Target |
```
Cleaner than prose for multi-input regulation. Use one table per regulatory axis.

**C) Nutrient interaction table (mandatory for metabolism cards):**
```
| Vi chất | Cơ chế tương tác |
|---------|-----------------|
| Mineral A | Competition for transporter X (mechanism detail) |
```
Essential for metabolism cards because feed formulation requires knowing competitive antagonism.

**D) Summary protein table (glanceable reference):**
```
| Protein | Gene | Function | Regulation |
|---------|------|----------|------------|
| Name | Gene1 | Core function | Regulated by X (↑), Y (↓) |
```
Makes the entire topic glanceable in one table.

### Research workflow for metabolism cards

| Step | Source | Query pattern |
|------|--------|---------------|
| 1. Core pathway overview | Wikipedia (`page/summary`) | Topic by title |
| 2. Key protein details | Wikipedia (`action=query`, one per protein) | Individual protein titles |
| 3. Species + metabolism (Phase 1) | 6 broad PubMed queries | Different angles: metabolism, deficiency, regulation, immunity, microbiota, intervention |
| 4. Mechanism refinement (Phase 2) | 6 targeted PubMed queries | Specific mechanisms identified from Phase 1 abstracts |
| 5. Compilation | Merge PMIDs → dedup → assign to sections → write PMID contribution table | Every PMID cited in contribution column |

**Phase 1 queries should cover:** species+metabolism, species+deficiency, species+regulator, species+immunity, species+microbiota, species+intervention. Pace with 1.5s between query groups.

**Phase 2 queries emerge from** scanning Phase 1 abstracts for gaps. For iron: DMT1 expression, IRP/IRE system, BMP/SMAD-hepcidin, ETEC-iron interaction, erythroferrone, weaning intestinal development.

**Every source** (Wikipedia + PubMed) should be cited at least once in the main content before appearing in the reference table.
