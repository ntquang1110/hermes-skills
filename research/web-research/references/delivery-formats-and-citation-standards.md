# Delivery formats, HTML KB recipe, citation standards, multi-pass protocol refinement

### Output format matrix

| Format | When | Structure | Tooling |
|--------|------|-----------|---------|
| **HTML encyclopedia** | Broad, multi-branch, permanent reference | TOC anchors, dark theme, responsive tables, embedded citations, sidebar banners | write_file(html) + upload-online-link for Gist preview |
| **Markdown .md** | Medium depth, version control, import to Notion/Obsidian | Headings, tables, code blocks, inline citations | write_file |
| **Inline structured** | Quick overview, 3-5 key facts | Tables, bullet lists, citations inline | Direct reply |
| **API card (JSON POST)** | Knowledge-base ingestion, cron research output, auto-indexing | Structured sections, gene-expression tables, references with DOIs, Vietnamese+emoji content | Pattern D — Python POST (see KF pipeline above) |

### HTML knowledge base pattern (lightweight recipe)

```
<section> per branch:
  <h2> — Title
  <div.def> — Definition with citation
  <table> — Term | Definition | Evidence (Author, Year)
  <div.formula> — Centered serif formula
  <div.milestone data-year="YYYY"> — Historic event
  <div.banner> — Critical note / summary

CSS colour tokens:
  --bg: #0f0f1a        /* base background */
  --bg2: #1a1a2e       /* section background */
  --bg3: #252540       /* table/code background */
  --accent: #7c7cf0    /* headers, links */
  --green: #7cf0a0     /* verified claims */
  --yellow: #f0e07c    /* sub-headings */
  --accent2: #f07c7c   /* alternate accent */

.cite — inline citation (smaller, muted)
.def — definition block with left accent border
.tag — inline tag/keyword badge
.flag.verified — confirmed result
.flag.controversial — contested/uncertain
.flag.theory — unproven theory
```

### Citation standards for research deliverables

| Source type | Citation format |
|-------------|----------------|
| **Textbook** | [Author, Title, Edition, Year] |
| **Peer-reviewed paper** | [Author(s), Journal Vol., Page (Year)] |
| **Experimental collaboration** | [Collaboration, Publication (Year)] |
| **Data/Review** | [Source, Year, e.g. Particle Data Group 2024] |
| **Unconfirmed theory** | Flag with <span class="flag theory"> or ⚠️ |
| **Competing views** | Give each the space its evidence supports — not equal time for disproven ideas |

### Pitfalls for research deliverables

- **Outline too shallow → user asks for more in one area**: Keep the outline modular; expand naturally per approved branch.
- **Missing definitions**: Every specialist term (QFT, QCD, GR, BCS, ΛCDM…) gets a definition on first appearance. Do not assume prior knowledge.
- **Fabricated citations**: Never cite a source you haven't read. Stick to well-known textbooks and major published results. For niche claims, note "verify with primary source."
- **Over-citation**: One citation per key concept suffices. Group minor claims under a section-level citation.
- **HTML too large for inline reply**: 90KB+ HTML files should be delivered via file path or Gist preview, not pasted into chat.
- **The "both sides" fallacy**: When presenting competing theories, weigh them by evidence, not by paragraph count. A disproven hypothesis does not merit equal space.

### Multi-pass protocol refinement pattern

When the task involves designing a chemical/mechanical protocol (e.g. contamination removal, extraction, processing), **do not** deliver a single final protocol on first try. The user will correct constraints you missed. Follow this iteration rhythm:

```
Pass 1 → Deliver reasonable first approach
  → User rejects. Identify WHICH constraint drove it (e.g. "must be dry")
  → Update protocol
Pass 2 → Deliver revised approach
  → User rejects again. Identify new constraint (e.g. "preserve minerals")
  → Update again
Pass N → User says "OK, giờ tổng hợp"
  → Produce comprehensive final deliverable with:
     • Multiple option paths (dry / wet / hybrid) side-by-side
     • Comparison table (cost, effectiveness, complexity per option)
     • Decision guide per soil condition / budget
     • Cost estimates per ton and per batch
     • Google Sheet for structured budget data (use google-workspace skill)
```

**Key signals that trigger iteration:**
- "giữ nguyên X" or "không hóa chất" → they want to PRESERVE something. Ask what.
- "ưu tiên đơn giản" → strip to the cheapest method first
- "dự tính chi phí" → needs practical cost breakdown, not just method
- After protocol is approved → user may want lab setup budget with equipment specs

**The "giữ nguyên khoáng quý" constraint** — when working with soil/sediment/geological materials, always check whether the user wants to PRESERVE the original mineral/chemical composition. If yes, use **dry physical separation only** (gravity, magnetic, thermal, adsorption). Never default to wet chemistry without explicit confirmation.

**Budget/Sheet delivery pattern** — after protocol approval, the user may request detailed lab setup budgeting:
1. Create comprehensive spreadsheet (google-workspace sheets create)
2. Include 5-6 sheets: equipment, glassware/consumables, chemicals, safety gear, test kits, summary+standards
3. Include Vietnamese standards table (e.g. QCVN 03:2023), dilution instructions, running cost/mẻ
4. Structure by work phase, not vendor

**See also:** `references/heavy-metals-soil-remediation.md` — full case study of the 3-pass iteration (wet→wash→dry) for As/Pb/Hg/Cd removal.

