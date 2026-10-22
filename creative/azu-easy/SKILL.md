---
name: azu-easy
description: Giai thich 3 tang (5 giay - 1 phut - Deep Dive) x thiet ke Azulejaria Digital Moderna (dark, cobalt). Dung cho Overview tab cua Knowledge Flow cards.
tags: [explain-easy, azulejaria, design-system, overview, 3-tier, knowledge-flow, flowchart, svg]
domain: creative
---

# Azu-Easy — Explain Easy × Azulejaria Digital Moderna

Logic 3 tang cua `explain-easy` + thiet ke dark/geometric cua `azulejaria-html-design`. Trien khai trong Knowledge Flow overview tab (`card-detail-client.tsx`), parser auto-generates tu markdown card content.

## Core Principles

- **Don gian hoa ≠ Sai.** Thay jargon bang an du doi thuong, giu nguyen ban chat.
- **3 tang, 1 trang**: ⚡️5 giây → 📖1 phút → 🔬 Deep dive, ai cung tim duoc do sau phu hop.
- **Moi deep-dive block DOC LAP** — doc 1 block khong can doc block khac.

## Design Tokens

```
Dark #1a1a1a · Surface #242424 · Cobalt #0047AB · Yellow #FFD700 · Green #2ECC40 · Red #FF6F61
Font: system-ui, sans-serif · Mono: JetBrains Mono
Border: rgba(255,255,255,0.08)
```

## Parser (parseAzuEasy)

Input: card object (title, content, summary, tags). Output: 3-tier overview data.

### One-liner extraction priority
1. Summary (strip label prefix)
2. Blockquote (first `>` line)
3. First paragraph (20-200 chars, non-heading)
4. Card title (strip leading emoji)

### KPI extraction
From table rows: first col = label, second col = numeric value (match `/(\d+[\d.,]*\s*[%°ÅµμgmgkDa]?)/`). Skip header rows, separator rows, and hyphens-only rows.

### Glossary extraction (2 sources)
1. **Table rows**: Split by `|`, filter headers & separators, dedupe. Blocklisted headers: Đặc tính, Giá trị, Tiểu phần, Tên gen, Chức năng, Nhóm, Mô tả, Cơ chế, Loại, Kết quả, Ảnh hưởng, Thành phần, Phương pháp, Tác nhân.
2. **Bold-def patterns**: `**term** — definition` regex.

**Pitfalls**: (a) Separator regex must be `/^\|[-:\s]+(\|[-:\s]+)*\|$/` (handles 3+ pipes), (b) Filter out hyphens-only cols with `/^[\-–—\s]+$/`, (c) Require `cols[1].length > 3`.

### SVG Flowchart (from → arrows)
Takes the FIRST arrow chain found (auto-detects continuation lines across blank lines and code blocks). Layout: ≤4 nodes → vertical, ≥5 nodes → horizontal scrollable.

**CRITICAL**: Arrow lines inside ``` code blocks ARE real signaling pathway data, NOT code. Use `inCodeBlock && !hasArrow` skip, NOT just `inCodeBlock`.

### Deep-dive blocks (from ## headings)
Filter: skip sections with `body.length < 30` AND skip sections where body stripped of punctuation has `< 10` significant chars (catches ":"-only sections). Full content rendered via `renderMarkdown()`.

## Markdown Renderers

### renderMarkdown (full)
Tables wrapped in `<div class="table-wrap">` for horizontal scroll. Handles: code blocks, inline code, blockquotes, bold/italic, headings H2-H3, lists, tables. CSS: `.azu-deep-content` needs `overflow-x: auto` for table scroll.

### renderInline (lightweight)
Bold, italic, inline code, links only. HTML-escapes `<` and `>`. Used for bullets, glossary defs, example boxes.

## CSS Classes
`.azu-nav`, `.azu-hero`, `.azu-hero-title`, `.azu-analogy`, `.azu-kpi-grid`, `.azu-kpi-card`, `.azu-kpi-num`, `.azu-section`, `.azu-bullet`, `.azu-glossary-grid`, `.azu-gloss-card`, `.azu-diagram-wrap`, `.azu-deep-block`, `.azu-deep-summary`, `.azu-toggle`, `.azu-deep-body`, `.azu-deep-content`, `.azu-example-box`, `.azu-footer`.
## Search (real-time)

Client-side fetch all cards → filter by title/summary/tags/content as user types → highlight `<mark>`. No Enter key. See `search-client.tsx`.

### Live Search Dropdown (TopBar)
The TopBar has a live autocomplete dropdown (separate from the `/search` page). Results appear below the search bar as user types. See `src/components/TopBar.tsx` and `knowledge-researcher` skill's "Live Search Dropdown" section.

## Infinite Scroll (Feed)
IntersectionObserver-based batch rendering with `BATCH_SIZE = 20`. See `src/app/feed-client.tsx` and `knowledge-researcher` skill's "Infinite Scroll" section.

## Hydration-safe Time Display
`Date.toLocaleString("vi-VN", {hour, minute})` causes SSR/client mismatch (timezone → 6+ exceptions/page). Fix: `.toLocaleDateString("vi-VN") + " " + .toISOString().slice(11,16)`. Applied in feed-client.tsx, card-detail-client.tsx, feed/feed-client.tsx, book/book-client.tsx, search-client.tsx.

## Build + Deploy (Windows CRITICAL)
`process(action='kill')` can silently target wrong PID on Windows. The old server keeps running; new `next start` fails with EADDRINUSE; user sees OLD code.  

**Fix**: Use `netstat -ano | grep ':3003'` to find ALL PIDs, `taskkill /F /PID` each one, verify port free, THEN `npx next start --port 3003`. Never trust the process tool alone.

See `references/implementation-card-detail.md` for regex details, SVG dimension formulas, dashboard API, emoji detection, delete button, and full deployment recovery sequence.
