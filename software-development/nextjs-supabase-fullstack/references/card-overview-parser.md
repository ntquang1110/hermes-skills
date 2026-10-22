# Card Overview Parser — Markdown → Visual A-Z

Auto-generates a visual A-Z overview from any knowledge card's markdown content. Used in Knowledge Flow's card detail page with two tabs: Overview + Học thuật.

## What it extracts (v2 — enhanced)

| Field | Extraction | Fallback |
|-------|-----------|----------|
| `essence` | First `**Mô tả bản chất:**`, `**Tên gọi khác:**`, or `>` blockquote | `card.summary` → first 250 chars of content |
| `kpis` | Numeric values from table cells (e.g. `74.9%`, `2.30 Å`, `178 a`) + `tag count` + `section count` | empty array (section always shown: min 2 KPIs) |
| `flow` | First `→` chain match (e.g. `IL-10 → STAT3 → BCL-3 → NF-κB`) | First 6 unique `**bold phrases**` from content |
| `concepts` | Table rows (col 0 = term, col 1 = def) + `**bold** — definition` patterns + tag + summary | fallback to tag + nearby sentence |
| `sectionMap` | `## Heading` regex with body preview | Simple `##` heading list (if regex fails) |
| `interactions` | `**virus/pathogen**` + action keyword (ức chế/kích thích/tăng/gây) | 3 cards from bold patterns |
| `tldr` | Lines starting with `>` (blockquotes) | `card.summary` |

## Parser implementation (key patterns)

### KPI extraction — from table cells
```typescript
const tableRows = content.match(/^\|.+\|$/gm) || [];
for (let i = 1; i < tableRows.length; i++) {
  const row = tableRows[i];
  if (/^\|[-:\s]+\|$/.test(row)) continue;
  const cols = row.split("|").filter(Boolean).map(c => c.trim().replace(/\*{1,2}/g, ""));
  if (cols.length >= 2) {
    const val = cols[1].match(/(\d+[\d.,]*\s*[%°ÅµμgmgkDa]?)/);
    if (val && cols[0].length < 40) {
      kpis.push({ value: val[1], label: cols[0], color: colors[kpis.length % 5] });
    }
  }
}
```
Always prepends section count + tag count as first two KPIs (guaranteed non-empty).

### Flow diagram — pathway chain
```typescript
// Try → chain first
const pathwayMatch = content.match(/(.+?)\s*→\s*(.+?)\s*→\s*(.+?)\s*→\s*(.+?)(?:→|$)/);
if (pathwayMatch) {
  pathwayMatch.slice(1, 6).filter(Boolean).forEach((p, i) => {
    flow.push({ icon: icons[i], label: p.replace(/\*{1,2}/g, "").trim() });
  });
}
// Fallback: bold concepts as flow nodes
if (flow.length === 0) {
  const bolds = content.match(/\*\*([^*]{3,40}?)\*\*/g) || [];
  [...new Set(bolds.map(b => b.replace(/\*/g, "")))].slice(0, 6).forEach((b, i) => {
    flow.push({ icon: icons[i], label: b });
  });
}
```

### Section map — with `---` separator handling
```typescript
const sectionRegex = /^##\s+(.+?)$\n([\s\S]*?)(?=^##\s|\n---|\n$)/gm;
while ((m = sectionRegex.exec(content)) !== null) {
  const title = m[1].replace(/\*{1,2}/g, "").trim();
  const body = m[2]?.replace(/\*{1,2}/g, "").trim() || "";
  const preview = body.replace(/\|.+\|/g, "").replace(/\n+/g, " ").slice(0, 100).trim();
  if (title && !title.startsWith("📚") && !title.startsWith("Tài liệu")) {
    sectionMap.push({ title, preview: preview || "..." });
  }
}
// Fallback: if regex failed, use simple ## headings
if (sectionMap.length === 0) {
  const headings = content.match(/^##\s+(.+)$/gm) || [];
  headings.forEach(h => {
    const title = h.replace(/^##\s+/, "").replace(/\*{1,2}/g, "").trim();
    if (title && !title.startsWith("📚") && !title.startsWith("Tài liệu")) {
      sectionMap.push({ title, preview: "..." });
    }
  });
}
```

### Virus/pathogen interaction cards
```typescript
const virusPatterns = content.match(/\*\*(.{2,30}?)\*\*[\s\S]{0,200}?(?:ức chế|kích thích|tăng|gây|bảo vệ|khai thác|trốn)/gi) || [];
virusPatterns.slice(0, 8).forEach(vp => {
  const nameMatch = vp.match(/\*\*(.{2,30}?)\*\*/);
  const name = nameMatch ? nameMatch[1] : "";
  if (name && !seen.has(name)) {
    seen.add(name);
    const desc = vp.replace(/\*{1,2}/g, "").trim().replace(name, "").trim().slice(0, 120);
    interactions.push({ name, desc: desc.slice(0, 100), mech: "..." });
  }
});
```

### Essence — multi-source fallback chain
```typescript
const essenceLine = lines.find(l =>
  l.startsWith("**Mô tả") || l.startsWith("Mô tả") ||
  l.startsWith("**Tên gọi") || l.startsWith("Tên gọi") ||
  (l.startsWith(">") && l.length > 20)
);
const essence = essenceLine
  ? essenceLine.replace(/^>\s*/, "").replace(/\*{1,2}/g, "").trim()
  : summary || content.replace(/^#+\s*/gm, "").replace(/\*{1,2}/g, "").trim().slice(0, 250);
```

## Rendering order

```
1. 📌 Bản chất       → accent-border box, single paragraph
2. 📊 Thông số chính  → KPI row (auto-fill grid, colored numbers)
3. 🔄 Con đường tín hiệu → vertical flow diagram (node → arrow → node → ...)
4. 🔑 Khái niệm chính → 2-col gloss-card grid
5. 📋 Cấu trúc bài viết → numbered section list with preview
6. 🦠 Tương tác       → interaction cards (name + desc + mechanism)
7. 🎯 TL;DR           → yellow-tinted box
```

Each section is conditionally rendered: if `array.length > 0` or `string` is truthy.

## CSS structure

```css
/* KPI row */
.kpi-row { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 10px; }
.kpi-num { font-size: 2rem; font-weight: 800; line-height: 1; }
.c-orange { color: var(--color-accent); }
.c-blue { color: #38bdf8; }
.c-green { color: #34d399; }

/* Flow diagram — vertical chain */
.flow-diagram { display: flex; flex-direction: column; align-items: center; }
.flow-node { border-radius: 12px; padding: 14px 20px; text-align: center; max-width: 400px; width: 100%; }
.flow-arrow { font-size: 1.2rem; color: var(--color-accent); padding: 6px 0; opacity: 0.7; }

/* Section map — numbered list */
.section-map-item { display: flex; gap: 12px; padding: 12px 14px; }
.section-map-num { width: 24px; height: 24px; border-radius: 50%; background: accent-dim; }

/* Interaction cards */
.interaction-card { padding: 12px 14px; border-radius: 10px; }
.interaction-name { font-weight: 700; color: var(--color-accent); }
```

## Edge cases handled

- **No `**Mô tả bản chất:**` marker** → falls back to `**Tên gọi khác:**` → blockquote → summary → first 250 chars
- **No tables** → KPI section still shows from tag count + section count (min 2 KPIs)
- **No `→` chain** → flow falls back to bold concepts (guaranteed non-empty when content has bold text)
- **Section regex fails** (multiline edge cases on some content) → fallback to flat heading list with `"..."` previews
- **No virus interaction patterns** → interactions array empty → section hidden
- **Duplicate concepts** → checked via `find()` before push
- **Tags unreachable** → first 6 tags used as concepts with nearby-sentence defs
- **Section filter** — titles starting with `📚` or `Tài liệu` excluded (reference sections)
- **Content with `---` separators** — section regex includes `\n---` in lookahead, handles dashed section separators
