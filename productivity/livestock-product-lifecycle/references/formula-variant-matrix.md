# Formula Variant Matrix — R&D Pipeline Design

Captured 17/09/2026 — after writing 5 product briefs × 23 formula variants for Kiềm Saphia TĂCN.

## When to use

When Quang asks for R&D planning with multiple formula variants per product line, or when designing an experiment pipeline for feed additive development. This pattern was proven across 5 product lines (respiratory, diarrhea, metritis, growth, growth+sleep).

## The variant matrix pattern

Each product line gets 4–5 formula variants, organized in a table where each row changes exactly 1–2 parameters from the baseline:

| CT | Core Ingredient | Modifier 1 | Modifier 2 | Note |
|----|----------------|------------|------------|------|
| XX-01A | Base dose | - | - | Công thức nền (baseline) |
| XX-01B | Higher dose | - | - | Test dose response |
| XX-01C | Base dose | Alternative source | - | Compare sources |
| XX-01D | Base dose | - | Add/remove component | Cost reduction / enhancement |
| XX-01E | Alternative | Different synergy | - | Novel combination |

### Design principles

1. **One variant = one hypothesis.** Each row tests exactly one thing — higher dose, different source, add/remove a component. Never change two things at once in a single variant.

2. **Baseline is always variant A.** XX-01A is the "nền" (foundation) formula — simplest, cheapest, most proven. All other variants branch from it.

3. **4–5 variants per line.** Fewer than 4 leaves gaps in the search space. More than 5 is wasteful at the screening stage.

4. **Cost-down variant always included.** One variant removes the most expensive ingredient to test if the market can accept a cheaper version (e.g. GT-01E removes berberine, GR-01E removes betaine).

5. **Source-comparison variant included.** One variant swaps a key ingredient source (e.g. chestnut tannin → quebracho tannin, thymol → carvacrol, Ích mẫu → Huyết dụ).

6. **Coding convention:**
   - Product prefix: RS (respiratory), GT (gut/diarrhea), MT (metritis), GR (growth), GS (growth+sleep)
   - Product number: 01 (first product in the line)
   - Variant letter: A–E

## Screening pipeline (G1→G3)

| Gate | Activity | Criteria | Budget |
|------|----------|----------|--------|
| G1 | Research: source materials, pricing, lead time, stability data | All ingredients available within 4 weeks | ~2–3 tr/CT |
| G2 | Lab: mix test, pH, solubility, sensory (≥30 blind panel) | pH 8–9, no off-flavor, homogeneous ±5% | ~5–8 tr/CT |
| G3 | Animal: 10–20 pigs/variant, measure FCR/ADG/diarrhea rate | Top 2 variants advance to G4 | ~8–15 tr/CT |

**Budget estimate:** ~15–25 triệu/CT × 4–5 CT/dòng = ~60–125 triệu/dòng for G1–G3.

## Output format

The R&D plan should be published as a standalone HTML page (use `playful-design` for visual appeal — confirmed preference 17/09/2026). Include:

1. Summary KPI cards (number of lines, variants, budget)
2. Per-line card with variant table
3. Master summary table
4. G1–G3 screening criteria with gate cards
5. Budget callout

## Example (from this session)

```markdown
| CT | L-Tryptophan | Mg | Betaine | Enzyme | Ghi chú |
|----|-------------|-----|---------|--------|---------|
| GS-01A | 0.15% | MgO 0.1% | 0.1% | Phytase+Xylanase | Baseline |
| GS-01B | 0.25% | MgO 0.1% | 0.1% | Phytase+Xylanase | Higher Trp |
| GS-01C | 0.15% | Mg chelate | 0.1% | Phytase+Xylanase | Source swap |
| GS-01D | 0.15% | MgO 0.1% | - | Phytase+Xylanase | Cost down |
| GS-01E | 0.15% | MgO 0.1% | 0.15% | +Protease | Enhanced |
```

## Pitfalls

- **Don't make all variants too similar.** Each should represent a genuinely different hypothesis about what drives efficacy.
- **Don't skip the cost-down variant.** Real-world adoption often depends on price, not just efficacy.
- **Don't test more than 5 variants per line.** At screening stage, more than 5 is diminishing returns. Save combinatorial exploration for G4–G5 after the top 2 are identified.
- **Label variants clearly with codes** (RS-01A, GT-01B, etc.) so lab technicians and trial managers can reference them unambiguously.
