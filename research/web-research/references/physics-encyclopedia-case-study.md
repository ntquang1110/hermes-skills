# Physics Encyclopedia — Knowledge Base Case Study

## Task
User asked for "tổng quan ngành vật lý học" — a comprehensive overview of physics with all terms, definitions, and citations.

## Workflow applied

| Phase | Duration | Steps |
|-------|----------|-------|
| **Sườn** | 1 exchange | Created 12-branch outline with 7 sections per branch. User approved. |
| **Chi tiết** | 1 exchange | Expanded to full HTML encyclopedia. User approved workflow and output format. |
| **Output** | 1 exchange | 93KB self-contained HTML → Gist preview via upload-online-link skill. |

## Deliverable structure

- **File**: `physics_encyclopedia.html` — 93KB, single file
- **Branches**: 12 (Mechanics → Thermodynamics → Electrodynamics → Fluids/Plasma → Quantum → Condensed Matter → Nuclear → Particle → Relativity → Cosmology → AMO → Computational/Theoretical)
- **Terms**: 500+ across all branches
- **Citations**: 19 textbook + paper references in final section
- **Format**: HTML with dark theme, TOC anchors, responsive tables, milestone timelines, definition blocks, formula blocks

## Key HTML patterns used

```html
<section id="sN">
  <h2>Section Title <span>English Name</span></h2>
  <div class="def"><strong>Định nghĩa:</strong> ... <span class="cite">[Source]</span></div>

  <h3>Subsection</h3>
  <table>
    <tr><th>Thuật ngữ</th><th>Định nghĩa</th><th>DC</th></tr>
    <tr><td><strong>Term</strong></td><td>Definition text</td><td>Author, Year</td></tr>
  </table>

  <div class="formula">E = mc² — description</div>

  <div class="milestone" data-year="1905">Event description</div>

  <div class="banner"><strong>Summary:</strong> Key takeaway.</div>
</section>
```

## CSS palette (dark theme)

```css
--bg: #0f0f1a;     --bg2: #1a1a2e;    --bg3: #252540;
--text: #e8e8f0;   --text2: #b0b0c0;
--accent: #7c7cf0; --accent2: #f07c7c;
--green: #7cf0a0;  --yellow: #f0e07c;
--border: #333350;
```

## Gist preview

The HTML was uploaded to a private GitHub Gist. The `upload-online-link` skill provides:
- **Preview URL**: `https://htmlpreview.github.io/?{raw_gist_url}`
- **Gist URL**: `https://gist.github.com/{user}/{gist_id}`

## Lessons learned

1. **Sườn first always** — user rejected depth-first, wanted breadth-first with all terms in each branch.
2. **Evidence column** in tables — having a dedicated "DC" (dẫn chứng) column forces citation discipline. Every key term gets a source.
3. **HTML single-file is best** for lossless knowledge transfer — markdown loses formula formatting and CSS layout.
4. **Batching terms by branch** in tables is more scannable than prose paragraphs.
5. **Define every acronym on first use** — QFT, QCD, GR, SR, BEC, HTS, etc. should never appear undefined.
6. **Verify citation before writing** — only cite sources the agent has actually read or verified. Fabricated citations damage trust.

## When to reproduce this pattern

- User asks for tổng quan / comprehensive overview of any broad field
- Topic has clear branching structure (sub-disciplines)
- User wants "lossless" knowledge — nothing omitted
- Output will be read on both desktop (HTML) and mobile (responsive)
