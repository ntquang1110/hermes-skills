# Card Overview Parser — `parseOverview()` Reference (SUPERSEDED)

> **2026-07-22:** `parseOverview()` has been replaced by `parseAzuEasy()` in the Azu-Easy 3-tier approach.
> See the `azu-easy` skill (creative category) for the current implementation.
> This file is kept for reference only.

The `parseOverview()` function auto-generated a visual summary from any card's markdown content, producing 7 fields (essence, kpis, flow, concepts, sectionMap, interactions, tldr). It has been superseded by `parseAzuEasy()` which returns a 3-tier structure: oneLiner, analogy, kpis, bullets, glossary, svgDiagram, deepBlocks.

Key differences:
- Old: flat 7-section layout with KF yellow (#FFD600) palette
- New: Azu-Easy 3-tier format (5s/1min/Deep dive) with azulejaria dark design (cobalt #0047AB)
- Old CSS classes prefixed with generic names (`.kpi-row`, `.flow-diagram`, `.section-map`)
- New CSS classes prefixed with `.azu-` (`.azu-kpi-grid`, `.azu-nav`, `.azu-deep-block`)
- Old rendered 7 sequential sections; new renders sticky nav + hero + section + collapsible deep dive

Extraction methodologies (table-to-KPI, bold-def-to-concept, section-heading-to-map) are preserved in `parseAzuEasy` but simplified and reorganized per tier.

CSS classes from old implementation (`.card-overview`, `.kpi-row`, `.flow-diagram`, `.section-map`, `.interaction-card`) still exist in `globals.css` for backward compatibility but are no longer used by the active card detail component.
