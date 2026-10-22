## Card Detail — 2-Tab System (Visualize + Học thuật) — từ 13/08/2026

Every article/card at `/card/[id]` has **two viewing tabs** controlled by local `useState<Tab>("visualize")`.

| Tab | Purpose | Content |
|-----|---------|---------|
| 🎨 **Visualize** | Hiểu nhanh bản chất | Hero (one-liner + analogy + 3 KPI vàng), bản đồ dòng chảy (flowNodes từ arrow chains), cơ chế từng bước + mini-flow chips (từ OVERVIEW JSON), khái niệm chính (glossary), ứng dụng + hạn chế (OVERVIEW), deep dive blocks, card vàng **Mục tiêu** (3 actions từ applications), footer chips |
| 🎓 **Học thuật** | Đọc chi tiết | Full markdown content with tables, code blocks, references |

**CHUẨN MỚI (13/08/2026 — thay thế tab Overview cũ):** tab `📚 Overview` (azu-easy 3 tầng 5s/1ph/deep) đã bị BỎ. Không còn "overview" trong Tab type. CSS classes mới: `.viz-*` trong `globals.css` (Premium B/W/Y: bg #0D0D0D, surface #1B1B1D, vàng #FFD600).

**⚠️ PITFALL — OVERVIEW block lộ ra ngoài:** mọi nơi render `card.content` (feed preview, book view, card detail) PHẢI strip `<!--OVERVIEW-->[\s\S]*?<!--/OVERVIEW-->\s*` trước khi renderMarkdown, nếu không JSON thô lộ ngay trên feed. Files đã fix: `feed-client.tsx`, `book/book-client.tsx` (2 chỗ), `feed/feed-client.tsx`, `card/[id]/card-detail-client.tsx`.

### Structured Overview block (đọc bởi parseAzuEasy → Visualize tab)

The Overview tab content is **auto-generated client-side** from the card's existing markdown — no extra API calls, no separate content authoring required.

**Parser function (`parseOverview` in `card-detail-client.tsx`):**

Returns 7 sections from card content:

```typescript
return {
  essence,       // string — first "Mô tả bản chất:" paragraph or fallback
  kpis,          // array — numeric values extracted from tables
  flow,          // array — signaling pathway from bold patterns
  concepts,      // array — key concepts from tables + bold definitions
  sectionMap,    // array — sections from ## headings with preview
  interactions,  // array — virus/pathogen interactions
  tldr,          // string — > blockquote lines or card summary
};
```

**Extraction logic for each field:**

| Field | Extraction strategy | Fallback |
|-------|-------------------|----------|
| `essence` | First line `**Mô tả bản chất:**`, `**Tên gọi khác:**`, or `>` | `card.summary` or first 250 chars |
| `kpis` | Table rows where 2nd column has numeric value (`\d+[\d.,]*\s*[%°ÅµμgmgkDa]?`) | Tag count + section count |
| `flow` | Content matching `→ → →` pathway pattern (split by arrows) | Top 6 unique bold terms |
| `concepts` | Table first-two-columns (col1=term, col2=def) | `**bold** — def` patterns → tag fallback |
| `sectionMap` | `^##\s+(.+?)$` sections with body preview (tables stripped) | Plain `##` heading list |
| `interactions` | `**Name**` + nearby Vietnamese verbs (ức chế, kích thích, tăng, gây, bảo vệ, khai thác, trốn) | Empty |
| `tldr` | Lines starting with `>` >30 chars | `card.summary` |

**Rendering order in Overview tab:**
1. 📌 **Bản chất** — essence strip with yellow left border
2. 📊 **Thông số chính** — KPI cards in `kpi-row` grid
3. 🔄 **Con đường tín hiệu** — flow diagram (vertical stacked nodes with ↓ arrows)
4. 🔑 **Khái niệm chính** — glossary grid of term-definition cards
5. 📋 **Cấu trúc bài viết** — numbered section map with preview snippets
6. 🦠 **Tương tác với tác nhân** — interaction cards (name, description, mechanism)
7. 🎯 **TL;DR** — summary box with yellow background

**CSS classes needed:** `card-overview`, `kpi-row`, `flow-diagram`, `flow-step`, `flow-node`, `flow-arrow`, `section-map`, `section-map-item`, `section-map-num`, `interaction-card`, `interaction-name`, `interaction-desc`, `interaction-mech`. All defined in `globals.css`.

### Known limitation: empty sections on sparse content

Cards with minimal markdown (no `##` headings, no tables, no bold definitions) will have empty arrays for KPI, flow, concept, sectionMap, and interactions. Empty sections are simply omitted from the render. Essence and tldr always have at least a fallback value.

### 2026-07-22 update: `parseOverview` superseded by Azu-Easy

`parseOverview()` has been replaced by `parseAzuEasy()` which generates a 3-tier visual (5s / 1min / Deep dive) instead of 7 flat sections. The Azu-Easy approach is defined in the `azu-easy` skill (creative category) and implemented in `card-detail-client.tsx`.

Key differences:
- `parseAzuEasy` returns `{ oneLiner, analogy, kpis, bullets, glossary, svgDiagram, deepBlocks }` instead of the 7 fields from `parseOverview`
- The Azu-Easy rendering uses azulejaria design tokens (dark #1a1a1a, cobalt #0047AB) vs the old KF yellow (#FFD600) palette
- Tier 1 = hero with analogy + KPI grid, Tier 2 = bullets + glossary + SVG diagram, Tier 3 = collapsible deep dive blocks
- The old `references/card-overview-parser.md` still documents `parseOverview` for reference but is superseded

See `azu-easy` skill and its implementation in `card-detail-client.tsx` for the current approach.

### Overview Block (Structured Overview) — 2026-07-29

Card MỚI (từ cron) và card backfill có **overview JSON chèn ngay đầu content** — parser đọc block này để render 6 khối overview đúng bản chất thay vì cắt-dán heuristics.

**Format (HTML comment bọc JSON):**
```html
<!--OVERVIEW-->{"what":"...","why":"...","mechanism":["..."],"players":["..."],"applications":["..."],"limits":"...","analogy":"..."}<!--/OVERVIEW-->
```

**Schema 7 fields:**
| Field | Nội dung |
|-------|----------|
| `what` | Định nghĩa 1-2 câu đúng trọng tâm (render làm 1-liner tầng 5 giây) |
| `why` | Vì sao quan trọng (heo/người) |
| `mechanism` | 3-5 bước cơ chế chính (array string, render có số thứ tự) |
| `players` | 3-6 thành phần/chủ thể chính (render dạng chip) |
| `applications` | 2-4 ứng dụng thực tế |
| `limits` | 1-2 câu hạn chế/tranh cãi (render màu đỏ) |
| `analogy` | 1 câu ví von dễ nhớ |

**Parser (`parseAzuEasy` trong `card-detail-client.tsx`):**
- Regex: `<!--OVERVIEW-->\s*(\{[\s\S]*?\})\s*<!--\/OVERVIEW-->`
- Nếu có overview block → dùng `overview.what` làm oneLiner, `overview.why/mechanism/players` làm bullets, render các khối `.azu-ov-block` (CSS `azu-ov-*` trong `globals.css`)
- **BẮT BUỘC strip block khỏi hiển thị:** `content.replace(/<!--OVERVIEW-->[\s\S]*?<!--\/OVERVIEW-->\s*/g, "")` — dùng cả trong parseAzuEasy (content local) LẪN tab Học thuật (`renderMarkdown(card.content.replace(...))`) nếu không JSON thô sẽ lộ ra
- Card cũ chưa có block → fallback heuristics (1-liner từ summary, KPI từ table...)

**Backfill script:** `scripts/backfill-overview.py` — sinh overview cho N card gần nhất qua LLM opencode-go:
- Gọi `POST https://opencode.ai/zen/go/v1/chat/completions` (model `deepseek-v4-flash`, `max_tokens: 2500`, `temperature: 0.3`, key từ `OPENCODE_GO_API_KEY` trong `~/AppData/Local/hermes/.env` — nhớ strip quotes `strip('"\'')`)
- **PITFALL LLM JSON:** LLM hay sinh trailing comma (`,"}` `,]`) hoặc cắt cụt JSON khi max_tokens thấp → cleanup `raw_json.replace(",}", "}").replace(",]", "]")` + validate + **3 lần retry** + `max_tokens ≥ 2500`
- **Progress file** `data/backfill-progress.json` (`{"done": [ids]}`) → chạy lại resume, không xử lý lại card đã có overview
- Update card qua `PATCH /api/cards?id=xxx` với `{content: new_content}` (PATCH endpoint thêm 2026-07-29 — chỉ update các field có mặt, tự tính lại `reading_time_sec` từ content)

**PITFALL — backfill cần PATCH endpoint mới:** `/api/cards` route thêm `export async function PATCH` (Next 16, params dạng `Promise`). Nếu server cũ đang chạy (không có PATCH) → nhận HTTP 405. Luôn verify PATCH hoạt động trước khi chạy backfill: `curl -X PATCH "http://localhost:3003/api/cards?id=test"` phải trả lỗi UUID (tức route chạy), không phải 405.

