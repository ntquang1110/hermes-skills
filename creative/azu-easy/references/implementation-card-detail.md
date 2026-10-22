# Card Detail Implementation Reference

## Overview Tab — Auto-generated 3-tier Azu-Easy

File: `src/app/card/[id]/card-detail-client.tsx`

### Tab state
```typescript
type Tab = "overview" | "hoc-thuat";
const [tab, setTab] = useState<Tab>("overview");
```

### Parser runs in useMemo
```typescript
const azu = useMemo(() => parseAzuEasy(card), [card]);
```

### Azu-Easy data structure
```typescript
return {
  oneLiner: string,       // Summary or first paragraph
  analogy: string,        // "nhu..." metaphor or ""
  kpis: { value, label, context? }[], // Max 3, from tables
  bullets: string[],      // Max 5, from intro section
  glossary: { term, def, example? }[], // Max 8, from tables + bold-defs
  svgDiagram: string,     // SVG markup or ""
  deepBlocks: { title, body, example? }[], // Max 12, from ## sections
};
```

### Key regex patterns

| Purpose | Regex | Group Returns |
|---------|-------|---------------|
| Table separator (skip) | `/^\|[-:\s]+(\|[-:\s]+)*\|$/` | — |
| Hyphen-only (skip) | `/^[\-–—\s]+$/` | — |
| Bold-def extraction | `/\*\*(.{3,35}?)\*\*\s*[—–\-:]\s*(.{5,100}?)(?:[.;\n]|$)/g` | m[1]=term, m[2]=definition |
| One-liner blockquote | `/^>\s*(.{20,200}?)[.。]$/m` | m[1]=text |
| Analogy (Vietnamese) | `/[Nn]hư\s+(một\|một cái\|việc\|khi\|người)\s+[^.]{10,80}[.]/` | match[0] |
| Section heading | `/^##\s+(.+?)$\n?([\s\S]*?)(?=^##\s|\n---|\n$)/gm` | m[1]=title, m[2]=body |
| Content intro | `/##\s+([\s\S]*?)(?:##|$)/` | m[1]=content |
| Search highlight | `new RegExp("(" + escapedQuery + ")", "gi")` | — |

### Glossary filtering order

1. Separator skip: `/^\|[-:\s]+(\|[-:\s]+)*\|$/`
2. Split by `|`, filter(Boolean), trim, strip `**`
3. Push if ALL pass:
   - `cols.length >= 2`
   - `cols[0].length >= 4 && cols[0].length < 35`
   - `!cols[0].match(/^\d/)`
   - `!cols[0].match(/^[\-–—\s]+$/)`
   - `cols[1].length > 3`
   - `!blocklistedHeader(cols[0])`
   - Not already added
4. Bold-def patterns add more (deduped): `/\*\*(.{3,35}?)\*\*\s*[—–\-:]\s*(.{5,100}?)(?:[.;\n]|$)/g`

Blocklisted column headers: Đặc tính, Giá trị, Tiểu phần, Tên gen, Chức năng, Nhóm, Mô tả, Cơ chế, Loại, Kết quả, Ảnh hưởng, Thành phần, Phương pháp, Tác nhân

### Dashboard (Knowledge Flow)
The `/dashboard` page is a client-side React component (`dashboard-client.tsx`) that:
- Fetches compound data from `GET /api/dashboard` (one endpoint, not N+1)
- Displays: **KPI badges** (total/done/unread/topics), **Topic breakdown** (horizontal bars + progress), **Unread priority** (7 newest unread), **Topic grid** (4-column grid with dynamic buttons)
- Topic emoji detection: `codePointAt(0)` range check (NOT regex `\u{...}` — build failure pitfall)

### Markdown rendering

Two renderers at bottom of `card-detail-client.tsx`:

**`renderMarkdown(md)`** — FULL renderer. Handles code blocks, inline code, blockquotes, bold/italic, headings, lists, tables. Usage: deep-dive bodies.

**`renderInline(text)`** — LIGHTWEIGHT renderer. Handles bold, italic, inline code, links, HTML-escaped `<`/`>`. Usage: bullets, glossary defs, example boxes.

### Deep-dive body (full content, no truncation)
```typescript
body = body.replace(/\n{3,}/g, "\n\n");  // Only normalize triple newlines
// NO .replace(/\|.+\|/g, "") — keep tables
// NO .slice(0, 500) — no truncation
```

### Empty section filter
After cleaning body, filter out sections whose content is only punctuation/whitespace:
```typescript
const cleanBody = body.replace(/[\s\:\;\,\.\-]+/g, "").trim();
if (cleanBody.length < 10) continue;  // Skip sections that are just ":" etc
```

### Table horizontal scroll in deep-dive
CSS in `globals.css`:
```css
.azu-deep-content { overflow-x: auto; }
.azu-deep-content table { display: block; overflow-x: auto; white-space: nowrap; }
.azu-deep-content .table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; }
```
This enables horizontal scrolling for wide tables inside collapsible deep-dive blocks.

### Time display (hydration-safe)

**PITFALL**: `Date.toLocaleString("vi-VN", {hour:"2-digit", minute:"2-digit"})` causes SSR/client hydration mismatch because Node.js and browser produce different formats for the vi-VN locale (e.g., `"03:47"` vs `"10:47"` due to timezone). The error is silently caught by React boundary but logs 6+ exceptions per card page.

**Fix**: Use `.toLocaleDateString("vi-VN")` for the date part and `.toISOString().slice(11,16)` for the time (always UTC, consistent across server and client). This shows UTC time but eliminates hydration errors completely.

```jsx
<span>📅 {new Date(card.created_at).toLocaleDateString("vi-VN")} {new Date(card.created_at).toISOString().slice(11,16)}</span>
```

### Delete card button
Added at bottom of card detail page (both tabs), next to read-status toggle:
```typescript
const handleDelete = async () => {
  if (!card) return;
  if (!window.confirm(`Xoá "${card.title.slice(0, 60)}"?`)) return;
  await fetch(`/api/cards?id=${card.id}`, { method: "DELETE" });
  window.location.href = "/";
};
```
Button: 🗑 Xoá, red border (rgba(255,100,100,0.3)), cursor-pointer.

### Search real-time (Knowledge Flow)
Search at `/search` uses client-side fetching: load all cards once via `fetch("/api/cards")`, filter with `useMemo` by title/summary/tags/content as user types. Highlight matches with `<mark>`. No Enter key needed. The `search/page.tsx` is simplified (no server searchParams). `search-client.tsx` is self-contained.

### Emoji detection (build-safe)
**PITFALL**: `\u{...}` unicode escapes in regex literals inside JSX/TSX files get mangled by the patch tool (becomes `\\u{...}` which causes build failure). Use `codePointAt(0)` range check instead:
```typescript
function hasEmojiPrefix(s: string): string | null {
  const code = s.codePointAt(0);
  if (!code) return null;
  if ((code >= 0x1F000 && code <= 0x1FFFF) ||
      (code >= 0x2600 && code <= 0x27BF) ||
      (code >= 0x1F300 && code <= 0x1F9FF) ||
      code === 0xFE0F) return String.fromCodePoint(code);
  return null;
}
```

### SVG Flowchart — first arrow chain (handles continuation)

Takes the FIRST chain found in card content (skips code-block non-arrow lines, but DOES process arrow lines inside code blocks).

```text
For each line:
  if line has → or ➔ → accumulate into mergedLine
  if next line starts with → OR is blank → keep accumulating
  if next line is non-arrow, non-blank → break (chain complete)

Split mergedLine on →/➔, clean each segment, filter stop-words, take top 7.
```

Layout: ≤4 nodes → vertical (400px). ≥5 nodes → horizontal (max 900px, scrollable).

**CRITICAL: Arrow lines in code blocks are REAL pathways, not code.** The skip condition must be `inCodeBlock && !hasArrow`, NOT just `inCodeBlock`.

### One-liner extraction order
1. Summary (strip label prefix)
2. Blockquote (first `>` line)
3. First meaningful paragraph (non-heading, 20-200 chars)
4. Card title (strip leading emoji)

### Build failures & port management

**Symptom**: Source changes compiled but not reflected in browser. `process(action='kill')` returns success but old server still runs.

**Root cause**: The PID tracked by Hermes `process(action='kill')` may differ from the actual server PID on Windows. Multiple server processes accumulate, and newer ones silently fail with EADDRINUSE while the OLD one continues serving the OLD code.

**Fix sequence**:
1. `netstat -ano | grep ":3003" | grep LISTENING` — find ALL PIDs on port 3003
2. `taskkill /F /PID <PID>` for EACH pid found
3. Repeat netstat until port is free
4. `rm -rf .next`
5. `npx next build`
6. `npx next start --port 3003`
