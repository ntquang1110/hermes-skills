---
name: knowledge-researcher
description: "Build and operate a Knowledge Flow app — Next.js + Supabase knowledge management system with TikTok-style feed, book reader, research queue, and auto-research cron"
tags:
  - knowledge-management
  - research
  - nextjs
  - supabase
  - notion-import
  - cron
  - vietnamese
domain: research
---

# Knowledge Researcher

Build and operate a **Knowledge Flow** web app — a personal knowledge management system with three views (Feed / Book / Research), Notion import, and auto-research cron.

## Architecture

```
Next.js 16 (App Router) + Supabase PostgreSQL + Tailwind v4
Port: 3003
Design System: Premium Dashboard v1.0 (Black/White/Yellow #FFD600)
```

**Three core views:**
- **Feed** (`/`) — Infinite scroll, preview cards, topic filter dropdown, click title/Đọc tiếp → card detail page
- **Book** (`/book`) — Sequential reader with collapsible TOC sidebar (mobile hamburger), groups by tags/topics
- **Research** (`/research`) — Research Queue UI: add topic → pending → researching → done with card_id link

## Database Schema

### `knowledge_topics`
```sql
id UUID PK, title TEXT, slug TEXT UNIQUE, emoji TEXT, color TEXT, description TEXT,
card_count INT, sort_order INT, is_archived BOOLEAN, created_at TIMESTAMPTZ
```

### `knowledge_cards`
```sql
id UUID PK, topic_id UUID FK, title TEXT, content TEXT, summary TEXT,
source TEXT (hermes|notion|manual), source_url TEXT, tags TEXT[], reading_time_sec INT,
is_bookmarked BOOLEAN, order_index INT, notion_page_id TEXT, session_id TEXT,
created_at TIMESTAMPTZ
```

## Feed View — UX Patterns

Chi tiết: `references/feed-view-ux.md` — card preview (inline), infinite scroll, read status (đã đọc / chưa đọc), live search dropdown (TopBar), hydration-safe time display, nút delete card, nút share (native share + preview link), preview URL + OG tags qua host-based redirect, Next.js 16 route handler (`params` là `Promise`), schedule page UI, card page không được return `Response`, card detail 2-tab, mobile responsive rules.

---

## Book View

### Navigation
- TOC sidebar (left) lists all cards grouped by their first tag
- Click any TOC item → updates `currentId` state → content changes
- Uses `key={currentId}` on content `<article>` to force React re-render
- Progress bar: `currentIdx / total`
- Prev/Next buttons at bottom of content

### Grouping logic
```
if (c.topics) name = c.topics.title; else if (c.tags[0]) name = c.tags[0]; else name = default
```

## Research Queue — Auto-Research Cron

### Queue API (file-based JSON)
- `GET /api/research-queue` — list all items
- `POST /api/research-queue` — add `{topic, detail, topic_slug}` → status `pending`
- `DELETE /api/cards?id=xxx` — delete a card by ID (added in session 2026-07-18)
- `DELETE /api/cards?ids=id1,id2,id3` — bulk delete multiple cards
- `PATCH /api/research-queue` — update `{id, status, card_id}`
- `DELETE /api/research-queue?id=xxx` — remove item
- File: `data/research-queue.json` in Next.js project root

### Cron job (`knowledge-researcher`)
- **Schedule:** `every 240m` (4 tiếng, từ 2026-07-29 — mục tiêu ~8 bài/ngày tỷ lệ 2-2-2-2)
- **Skills:** `web-research`
- **Priority:** Process pending queue items first → nếu queue rỗng → xoay vòng 4 nhóm chủ đề
- **Rotation (4 nhóm, file `data/research-rotation.json` chứa `last_index`):** đọc file → chọn nhóm kế tiếp theo vòng 0→1→2→3→0:
  - `0` → 💰 **Tài chính**: CFA (portfolio/fixed income/derivatives/risk) HOẶC Quant (factor investing/statistical arbitrage) HOẶC M&A (deal structuring/valuation)
  - `1` → 🔧 **Công nghệ thế giới (ưu tiên AI)**: AI/LLM paper mới (cơ chế/benchmark/ứng dụng) HOẶC chip/semiconductor/robotics
  - `2` → 🧬 **Sinh học (Heo + Người)**: miễn dịch & bệnh học heo (cytokine/PRRSV/ASFV/PEDV) HOẶC dinh dưỡng & hệ vi sinh ruột (probiotic/postbiotic/axit amin)
  - `3` → ⚗️ **Hóa học & Dược (Heo + Người)**: hợp chất thiên nhiên & dược lý (saponin/polyphenol/alkaloid/dược động học) HOẶC hóa phân tích & xử lý môi trường (KLN As/Pb/Hg/Cd, biochar)
  - Sau khi tạo card: ghi `{"last_index": <index vừa dùng>}` vào file rotation
- **Overview block BẮT BUỘC:** mọi card mới phải chèn `<!--OVERVIEW-->{json}<!--/OVERVIEW-->` ở ĐẦU content (xem mục "Overview Block (Structured Overview)" bên dưới)
- **Retry on failure:** Don't mark "failed" on first attempt — leave status, next cron retries

### Cron flow

**Step 0 — Server readiness check:**
Before any queue processing, verify the API server is running:
- `GET http://localhost:3003/api/research-queue` (or `/api/health`)
- If reachable (200/JSON response): proceed with normal flow → research → POST to KFlow
- If unreachable (exit code 7, connection refused, or empty response): the Next.js server is down. Cron CANNOT start it (no user to approve background process). **Do NOT stop — proceed with research anyway** and deliver as HTML via preview.thefirstonly.com:
  1. Research the topic as normal (Wikipedia + PubMed multi-query + abstract deep-dive)
  2. Compile into comprehensive HTML (dark theme, tables, citations with PMIDs, pathway diagrams)
  3. POST to `https://preview.thefirstonly.com/api/store` via curl (NOT Python urllib — that endpoint returns 403). Use `write_file(payload.json)` then `curl -s -X POST "https://preview.thefirstonly.com/api/store" -H "Content-Type: application/json" -d @C:/Users/.../payload.json`
  4. Deliver the preview URL as the cron output alongside a summary of findings
  5. The research is NOT lost — it can be re-POSTed to KFlow when the server is back, or the user reads it from the preview URL directly

1. GET /api/research-queue → check for pending
2. If pending: PATCH `{id: item.id, status: "researching"}`, use item.topic
3. If empty: pick from focus topics (luân phiên, không lặp)
   - **Rotation logic:**
     a. `session_search()` with no args (browse mode) to see the 5 most recent cron sessions by title — session titles like `"knowledge-researcher · Jul 28 02:52"` reveal the domain without needing to read the full session
     b. If the browse titles are ambiguous, drill into a recent session with `session_search(session_id=...)` (scroll mode) to check which `topic_slug` was used
     c. Pick the domain not covered in the last 2 runs (e.g., if last 2 were chan-nuoi, pick sinh-hoc or nghien-cuu)
     d. Then run **Systematic Gap Analysis** (below) to find the specific topic within that domain
   - **Topic slug mapping:** `chan-nuoi` = HEO (chăn nuôi lợn), `sinh-hoc` = SINH HỌC, `nghien-cuu` = Y HỌC/dược lý. New topic slugs (e.g. `y-hoc`) can also be used — the API creates topics on the fly from the `topic_slug` field. See the Topic slugs table below for all defined slugs.
4. Web research (3-4 sources), deep dive into mechanisms — use **multi-angle PubMed search** (see `references/pubmed-multi-angle-search.md` for the 16-query two-phase pattern: 8 broad searches covering generic topic, virus interactions, mechanism, model systems, and adjuvants + 8 specific searches for markers, cytokines, receptors, and individual viruses → merge results, deduplicate) plus Wikipedia API for background
5. Write card: **2000–20000 chars markdown** (deep mechanistic cards with 8+ sections, 20+ PMIDs, tables, code-block diagrams, and pathway diagrams regularly exceed 4000 chars — prioritize substance; the target reading time of 5-15 min / 300-900 sec is the better size heuristic), MUST pass ALL quality gates
6. POST /api/knowledge → import with source_url
7. If 201: PATCH `{id: item.id, status: "done", card_id: result.id}`
8. If not 201: leave status → next cron retries

**Temp file cleanup note:** In cron mode, `rm -f /tmp/*` or `rm -f /c/Users/.../hermes-temp/*` is blocked as "delete in root path". Cleanup will silently fail. This is acceptable — stale temp files are overwritten by subsequent cycles. Do NOT spend tool calls trying to work around this block.

---

## ⚠️ QUALITY GATES (CRITICAL)

Every research card MUST pass ALL checks BEFORE delivery:

### [Q1] Tiếng Việt có dấu đầy đủ
- Title: "Điều trị trầm cảm bằng Psilocybin" NOT "Dieu tri tram cam"
- Content: "cơ chế tác dụng" NOT "co che tac dung"
- **Check:** Count high-ASCII chars (>127). If <20 in first 500 chars → reject
- **Root cause:** Cron LLM skips diacritics. Prompt MUST explicitly demand full diacritics.

### [Q2] Emoji thật — KHÔNG shortcode
- ✅ `🧬🐷🔬🧠⚕️` (actual Unicode emoji)
- ❌ `:dna:` `:warning:` `:heavy_check_mark:` `:x:` (render as raw text)
- **Check:** Scan content for `:word:` pattern → if found → reject

### [Q3] Source URL bắt buộc
- Every card MUST have `source_url` pointing to original reference
- Cron prompt: "Ghi lại URL nguồn tham khảo chính và gửi trong field source_url"

### [Q4] Đi sâu bản chất
- Not listing facts — explain MECHANISM: pathway, proteins, genes, interactions
- Include: mechanism name → components → step-by-step → significance
- Deep = has citations, has named pathways, explains causation not just correlation
- **Depth checklist:** Does the card have (a) a historical timeline or discovery story? (b) a classification table of subtypes? (c) a step-by-step signaling cascade? (d) at least one comparison table? (e) ≥10 PMIDs with specific mechanism findings? (f) a practical/clinical significance section? If ≤3 of 6, the card is too shallow.
- See `references/successful-card-example.md` for **four worked examples** covering four distinct card styles:
  - **Example 1:** β-glucan → Dectin-1 → NF-κB (table + numbered steps style, single linear pathway)
  - **Example 2:** ENS + SCFAs/Butyrate ở heo (flow diagrams + multi-pathway style)
  - **Example 3:** Hàng rào ruột heo (clinical/solutions-driven style — problem first, then layers, then intervention comparison table, then decision guide)
  - **Example 4:** PRRSV virus-host interaction (layered deep-dive: virus structure → replication → immune evasion mechanisms → clinical significance)

### [Q5] Encoding — Không dùng Node.js; Cron: ưu tiên Python script, fallback pipe

**Never use Node.js fetch to POST Vietnamese text.** It mangles Unicode on MSYS2.

**Preferred — Pattern D (Python POST script) — works in cron mode:**

### [Q6] BẮT BUỘC: Mọi card PHẢI có source paper/báo

- KHÔNG research tin tức suông (news without scientific paper)
- KHÔNG tạo card nếu không tìm được bài báo/paper tham khảo
- Source URL PHẢI là DOI, PubMed, hoặc link báo uy tín
- Nội dung PHẢI phân tích paper: cơ chế, phương pháp, số liệu, kết quả
- Chủ đề AI News / Công nghệ mới / Tài chính: BẮT BUỘC có paper kèm phân tích kỹ
- Checkbox trước khi POST: "Có paper gốc không?" Nếu KHÔNG → hủy, chọn chủ đề khác
\`\`\`python
import urllib.request, json

card_content = """## 🧬 Nội dung card...

Nguồn: [Tên, năm, Journal]
"""

payload = {
    "title": "🐷 Title with emoji and dấu tiếng Việt",
    "content": card_content,
    "summary": "Short summary",
    "tags": ["tag1", "tag2"],
    "topic_slug": "chan-nuoi",
    "source_url": "https://en.wikipedia.org/wiki/Topic"
}

data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
req = urllib.request.Request(
    "http://127.0.0.1:3003/api/knowledge",
    data=data,
    headers={
        "Authorization": "Bearer hermes-knowledge-secret",
        "Content-Type": "application/json"
    },
    method='POST'
)
resp = urllib.request.urlopen(req, timeout=30)
result = json.loads(resp.read().decode())
print(f"SUCCESS! Card ID: {result.get('id', 'N/A')}")
\`\`\`

**How to use in cron mode** (when \`execute_code\` is blocked but \`write_file\` and \`python\` work):
1. \`write_file(path="card.py", content=script_text)\` — handles all Unicode natively
2. \`terminal(command='python card.py')\` — executes without shell escaping issues
3. Full HTTP response (including status code, card ID, errors) is captured and visible
4. Works on every platform — no MSYS path translation bugs, no heredoc escaping, no Unicode corruption

**✅ Pattern D advantages over curl/heodoc:**
- \`json.dumps(ensure_ascii=False)\` preserves Vietnamese characters natively
- Full exception handling (HTTP errors, network timeouts, JSON decode errors)
- Response status code available programmatically (200/201 vs 400/500)
- Card ID extracted from response for queue tracking
- No shell escaping issues with apostrophes, backticks, or special characters

### Cron: pipe/heredoc fallback (when Pattern D not available)

When \`execute_code\` and \`python -c\` are blocked in cron mode, and even \`write_file + python script\` is unavailable, fall back to \`write_file\` + \`cat | curl\` to preserve UTF-8:

```bash
write_file(path="/tmp/card.json", content=json_string)
cat /tmp/card.json | curl -sL -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer hermes-knowledge-secret" \
  -d @- \
  http://localhost:3003/api/knowledge
```

**⚠️ Do NOT use `curl -d @file`** — error 26 on Windows git-bash (MSYS path translation). Pipe (`-d @-`) works reliably and preserves UTF-8.

**Alternative — heredoc to stdin (no temp file):** Use a quoted heredoc to feed JSON directly to curl's stdin. This avoids the write_file step entirely and preserves diacritics and emoji:

```bash
curl -sL -X POST "http://localhost:3003/api/knowledge" \
  -H "Authorization: Bearer hermes-knowledge-secret" \
  -H "Content-Type: application/json" \
  -d @- <<'JSONEOF'
{
  "title": "🐷 Title with emoji and dấu tiếng Việt",
  "content": "## 🔬 Nội dung...",
  "tags": ["chan-nuoi", "sinh-hoc"],
  "topic_slug": "chan-nuoi",
  "source_url": "https://..."
}
JSONEOF
```

**Key:** The `'JSONEOF'` must be *quoted* so the shell does NOT interpret variables, backticks, or special chars inside the JSON. Works reliably on Windows git-bash and Linux.

### CRITICAL: Cron hallucinates port number

The cron model sometimes invents a wrong port (6680 instead of 3003). **The prompt MUST repeat the port 3 times:**

> API server at **http://localhost:3003** (port 3003, NOT port 6680)
> Import endpoint: **POST http://localhost:3003/api/knowledge**
> Queue endpoint: **http://localhost:3003/api/research-queue**

Check cron output at `<hermes_home>/cron/output/<job_id>/` to verify the URL used.

---

## Knowledge Import API

```bash
POST http://localhost:3003/api/knowledge
Authorization: Bearer hermes-knowledge-secret
Content-Type: application/json

{
  "title": "title with emoji",
  "content": "markdown content, Vietnamese with diacritics",
  "summary": "1-2 sentence summary",
  "tags": ["topic_slug", "research"],
  "topic_slug": "chan-nuoi|sinh-hoc|y-hoc|nghien-cuu|vat-ly|xet-nghiem|ai-ml|tong-hop",
  "source_url": "original URL (REQUIRED)"
}
```

### Delete cards
```bash
# Single card
curl -s -X DELETE "http://localhost:3003/api/cards?id=<card-uuid>"

# Bulk delete
curl -s -X DELETE "http://localhost:3003/api/cards?ids=id1,id2,id3"
```

## 🔍 Systematic Gap Analysis — When Queue Is Empty

**Why domain rotation alone isn't enough:** Rotating between `chan-nuoi` → `sinh-hoc` → `nghien-cuu` still leaves the question — which specific topic within the domain? With 50+ cards per domain, randomly picking a topic risks wasting a card slot on low-value overlap or inadvertently creating a duplicate.

### The gap-finding workflow

When `GET /api/research-queue` returns empty (all done), the best topics fill structural gaps in the KB rather than repeat covered ground.

**Step 1 — Enumerate the full card list:**
```bash
curl -s http://localhost:3003/api/cards | python -c "
import sys,json
cards=json.load(sys.stdin)
[print(f'{i}: {c[\"title\"][:90]}') for i,c in enumerate(cards)]
"
```

**Step 2 — Identify ghost topics (highest-value gaps):**
A "ghost topic" is a pathway, protein, cytokine, or pathogen that is:
- **Referenced by 3+ existing cards** (in crosstalk sections, comparison tables, mechanism descriptions)
- But **NOT independently covered** as its own card

Scan the enumerated list and look for:
- Cytokine families mentioned in multiple cards (check IL-, IFN-, TNF-prefixed entries) that lack a dedicated card
- Signaling pathways cited as "crosstalk" in 5+ cards but without their own deep-dive
- Receptors referenced in mechanism sections across different disease cards
- Feed additives / phytochemicals discussed in multiple contexts but not treated individually

**Heuristics to score gap priority:**

| Signal | What it means | Example from 158-card KB |
|--------|--------------|-------------------------|
| 🔴 **High** (5+ crosstalk links) | Referenced across many cards; fills a missing network node | A major cytokine family, virus, or additive discussed in multiple comparison tables |
| 🟡 **Medium** (3-4 links) | Referenced in context; would strengthen connections | A pathogen mentioned as "related to" covered diseases |
| 🟢 **Low** (1-2 links) | Mentioned once; limited connective value | Niche compound or pathway variant |

> **💡 Practical pattern:** For automated candidate scanning against the full card list, see `references/gap-keyword-scanning.md`. Define a keyword dictionary per candidate and let Python check titles + content — produces a clean GAP/COVERED list without manual scanning.

**Step 3 — Check symmetry in existing card families:**
If the KB has cards for most members of a family but is missing one, fill the gap:

| Family | Covered | Missing gaps |
|--------|---------|-------------|
| IL cytokines | IL-1, IL-2/γc family (IL-2/4/7/9/15/21), IL-6, IL-10, IL-12/23, IL-17, IL-22, Type 2/Th2 (IL-4/5/13) | IL-3, IL-11, IL-31, IL-35 |
| Viruses | PRRSV, PCV2, PEDV, TGEV, PDCoV, PRV, CSFV, SIV, ASF (partial) | PPV, HEV, JEV, TTV, Seneca Valley (SVA), Nipah |
| Bacteria | ETEC, Salmonella, S. suis, M. hyopneumoniae, APP, Lawsonia | Brachyspira, Clostridium perfringens, H. parasuis, Bordetella bronchiseptica |
| Nutrients/Minerals | Arginine, Lysine, Leucine/BCAA, Methionine/Cys, Threonine, Glutamine, Zn/ZnO, Cu, Se, Fe, Iron metabolism, Polyphenols, Essential oils, Tannins, MCFAs, Butyrate/SCFA | Choline, Valine, Isoleucine, Betaine, Carnitine, Vit C, Vit B12/Biotin/Folic, Omega-3 DHA/EPA |
| Mycotoxins | Aflatoxin B1, DON, Zearalenone, Fumonisin B1, Ochratoxin A | T-2 toxin, Patulin, Citrinin, Ergot alkaloids |
| Cell death | Apoptosis, Pyroptosis, Necroptosis, Ferroptosis, Autophagy | — (all covered) |
| Cell types | T cells (CD8+, γδ T, Th17/Treg), B cells, NK, Macrophage (M1/M2), Dendritic, Mast, Neutrophil, Goblet, Paneth, ILCs, ISC | Eosinophils, Basophils, Fibroblasts, Endothelial, Myeloid-derived suppressor cells |
| Feed additives | Butyrate, MCFAs, Essential oils, Tannins, Polyphenols, Probiotics, Prebiotics, β-glucan, SCFA receptors | MOS, FOS, GOS, COS, Postbiotics, Bacteriophages, Organic acids (formic/propionic), NSP enzymes (xylanase/β-glucanase), Phytase |

**Step 4 — Evaluate downstream practicality:**
A gap topic scores higher if it:
- Connects to **feed additive modulation** (practical for swine nutrition)
- Explains a **disease mechanism** not well-covered by existing cards
- Bridges **multiple existing cards** through pathway crosstalk
- Has **good PubMed literature** (≥10 relevant papers in swine context)

**Step 5 — Dedup check (see next section) before committing.**
Even for gap topics, verify no existing card partially covers it via keyword overlap.

### Using gap analysis in the cron rotation

When the queue is empty:
1. Check session history for which domains were recently covered (`session_search()` browse mode)
2. Pick the under-served domain (not covered in last 2 runs)
3. Run gap analysis within that domain using Steps 1-5 above
4. Select the highest-scoring gap topic
5. Research + create card

**This replaces random topic selection when the queue is empty.** Domain rotation ensures coverage breadth; gap analysis ensures depth within each domain.

---

## 🚫 Duplicate Prevention (CRITICAL)

### Why duplicates happen
The cron researcher runs independently every 2h. It can re-research the same topic (e.g. "Hệ vi sinh đường ruột heo") if the cron prompt doesn't account for what's already been posted, resulting in 3-5+ similar cards on the same topic.

### Checklist — BEFORE any research

**Step 1: Fetch existing cards**
```bash
curl -s http://localhost:3003/api/cards | python -c "
import sys,json
cards=json.load(sys.stdin)
for c in cards: print(c['title'][:70])
"
```

**Step 2: Compare candidate title against every existing card**
- **Exact match** (case-insensitive) → DUPLICATE, skip
- **One title contains the other** (long title has the short title as a substring, e.g. "🐷 PRRSV — Cơ chế..." contains "PRRSV") → DUPLICATE, skip
- **≥60% keyword overlap** (split both titles into words, count common words) → DUPLICATE, skip
- **Same topic + same core content** (e.g. both are about "Kẽm oxit (ZnO) phòng tiêu chảy heo con" but titled slightly differently) → DUPLICATE, skip

**Step 3: If in doubt, check content first 200 chars**
If titles differ but the first 200 characters of content are essentially the same structure, it's a duplicate.

### Utility script
Location: `~/AppData/Local/hermes/scripts/check_kflow_duplicate.py`
```bash
python check_kflow_duplicate.py "🐷 Tên bài cần research"
# → UNIQUE  (no duplicate found)
# → DUPLICATE:<card-id>  (existing card)
```

### Cron prompt anti-duplicate injection
Every research cron job should include:
1. The full list of **đã làm (already covered)** topics as a blacklist
2. A step: "Trước khi research: gọi `curl -s http://localhost:3003/api/cards` và so sánh title"
3. The instruction: "Nếu trùng lặp → BỎ QUA, chọn chủ đề khác"

### Cleanup duplicates
```bash
# Find title-similar cards, delete the older one
# In cron prompt or manual:
curl -s http://localhost:3003/api/cards | python -c "
import sys,json
cards=json.load(sys.stdin)
# Group by first 30 chars of title
groups = {}
for c in cards:
    key = c['title'][:30].lower()
    groups.setdefault(key, []).append(c)
for key, dupes in groups.items():
    if len(dupes) > 1:
        dupes.sort(key=lambda x: x['created_at'])
        keeper = dupes[-1]  # newest
        for d in dupes[:-1]:
            print(f'DELETE {d[\"id\"][:8]} ({d[\"created_at\"][:10]}) - keep {keeper[\"id\"][:8]}')
"
```

### Topic slugs
| Slug | Focus | Emoji |
|------|-------|-------|
| `chan-nuoi` | Pig farming, feed, diseases | 🐷 |
| `sinh-hoc` | Cell biology, virus, immunology | 🧬 |
| `y-hoc` | Human medicine, clinical, cell death, signaling | ⚕️ |
| `nghien-cuu` | Pharmacology, clinical research, psychedelics | 🔬 |
| `vat-ly` | Physics, soil treatment, minerals | ⚛️ |
| `xet-nghiem` | ELISA, PCR, diagnostics | 🧪 |
| `ai-ml` | AI & Machine Learning | 🤖 |
| `tong-hop` | General knowledge | 📚 |
| `tai-chinh` | Finance, economy, investing | 💰 |
| `ai-news` | AI News (must have source paper) | 🤖 |
| `cong-nghe-moi` | New technology (must have paper) | 🔧 |

**Note:** `nghien-cuu` and `y-hoc` both serve medical research. Use `y-hoc` for fundamental cell/molecular medicine (signaling, cell death, immunity) and `nghien-cuu` for pharmacology, drugs, clinical trials, and novel therapies. The API creates topics on the fly from any `topic_slug` value.

## Notion Import

Full pattern in `references/notion-import-pattern.md`. Steps:
1. Search Notion for "Kiến thức" database (ID: `38aee73e-673a-800e-b564-c2fc25c58097`)
2. Query all pages via `POST /v1/databases/{id}/query`
3. Map Chuyên ngành → topic_slug, fetch HTML from GitHub Gist, extract text
4. POST to `/api/knowledge`

## Pitfalls

### `PATCH /api/research-queue` — dùng `status`, không dùng `action`

Khi cập nhật queue item, field `"status"` mới là field chính xác để thay đổi trạng thái:
```json
✅ {"id": "...", "status": "done", "card_id": "..."}
```

Field `"action": "done"` **chỉ cập nhật card_id** mà không thay đổi status. Kết quả: item vẫn ở trạng thái `"pending"` dù đã có card_id. Luôn dùng `"status"` để đồng bộ cả hai.

### Vietnamese encoding with Node.js
Do NOT use Node.js `fetch` to POST Vietnamese — mangles Unicode on MSYS2. Use Python `urllib.request` with `json.dumps(body).encode('utf-8')`.
### `curl -d @file` error 26 trên Windows (cron mode)

Trong cron mode, `execute_code` và `python -c` bị block. Khi dùng curl để POST:
- ❌ `curl -d @/c/Users/.../card.json` → fail error 26 (MSYS path /c/... bị dịch sai)
- ✅ `curl -d @C:/Users/.../card.json` → **hoạt động** nếu dùng Windows-style forward-slash path (`C:/...`, không `/c/...`)
- ✅ `cat /tmp/card.json | curl -d @-` → hoạt động, giữ nguyên UTF-8

**Luật:** `-d @` với đường dẫn Windows (`C:/path/to/file.json`) hoạt động. Chỉ thất bại khi dùng MSYS path (`/c/path/`). Khi nghi ngờ → dùng pipe pattern.

Xem [Q5] cho code mẫu.

### RLS policies needed for new tables
New Supabase tables need explicit INSERT/DELETE policies:
```sql
CREATE POLICY "insert_{table}" ON {table} FOR INSERT WITH CHECK (true);
CREATE POLICY "delete_{table}" ON {table} FOR DELETE USING (true);
```

### Card topic linking
Cards from Notion have `topic_id: null`. Fix: filter by `tags` column instead of FK join: `.contains("tags", ["Vật lý"])`

### Turbopack "Jest worker" crash (Next.js 16.2.x)

**Problem:** Next.js 16.2.x with Turbopack crashes with `Jest worker encountered 2 child process exceptions, exceeding retry limit` — usually triggered by the dev error overlay trying to compile a dynamic route.

**Root cause:** Turbopack attempts to auto-generate static paths for dynamic route segments like `/card/[id]`. When the Supabase/DB call inside `getCard()` fails (e.g. transient network blip), the worker crashes and takes down the dev server.

**Fix — Three steps:**

**Step 1 — Add `dynamic = "force-dynamic"` to problematic dynamic route pages:**
```typescript
// src/app/card/[id]/page.tsx
import { getCard } from "@/lib/supabase/api";
import { notFound } from "next/navigation";
import CardDetailClient from "./card-detail-client";

// Prevent Turbopack from trying to auto-generate static paths
export const dynamic = "force-dynamic";

export default async function CardDetailPage({ ... }) { ... }
```
This prevents Next.js from attempting `generateStaticParams` on the route, which avoids triggering the Turbopack worker at compile time.

**Step 2 — Full `.next` cache clean:**
```bash
rm -rf /path/to/project/.next
```
Then restart the dev server. Partial cache clears (`rm -rf .next/dev/cache`) are insufficient when the error has corrupted the Turbopack build state.

**Step 3 — Verify no stale PID holds the port:**
```bash
netstat -ano | grep 3003 | grep LISTENING
taskkill //PID <stale-pid> //F
```
Stale Node processes survive `npx next dev` restart because the port is still bound. Kill them explicitly.

### `next build` trước khi kết thúc
Always run `npx next build` after making code changes to the KF project. The dev server tolerates TypeScript errors (pre-existing node_modules issues), but production build catches real type mismatches like:
- Props not matching component interface (`Property 'error' does not exist on type`)
- Missing imports (`useRouter is not defined`)
- Wrong prop types

Skip the build only for trivial one-line changes — do it for any structural edit.

### Server restart — `process(action='kill')` silently fails on Windows

**Problem:** Using `process(action='kill', session_id='...')` to kill the Next.js server appears to succeed but the actual port-bound process is a different PID than the tracked session. The old server keeps running, serving stale built code. All subsequent `next start` attempts fail with EADDRINUSE.

**Symptom:** You build, kill, restart, but the browser still shows old code regardless of how many times you repeat the cycle. The new build's `.next` output is correct but the OLD server process is what handles requests.

**Fix — always verify after kill:**
1. List ALL processes on port 3003 via `netstat -ano | grep ":3003 " | grep LISTENING`
2. Kill EACH PID explicitly via `cmd.exe /c "taskkill /F /PID <pid>"`
3. Verify port is clear via `netstat -ano | grep ":3003 " | grep LISTENING || echo "OK"`
4. THEN start new server
5. Verify new server is running (200 response, not EADDRINUSE)

**Bulk kill:** `cmd.exe /c "for /f \"tokens=5\" %p in ('netstat -ano ^| findstr \":3003 \" ^| findstr LISTENING') do (taskkill /F /PID %p)"`

The Hermes tool kills the TRACKED session, not necessarily the OS process on the port. Trust `netstat`, not the tool's success message.

**Common failure scenario:** You have made 5+ builds and restarts, but the browser still shows old code. You check the process list — every new server exited with EADDRINUSE. The ORIGINAL server (PID possibly from hours ago) is still running on the port, serving the very first build's output. ALL subsequent builds were compiled correctly into `.next/` but NEVER DEPLOYED because no new server could bind the port.

**Verify deployment freshness:** After restart, check the server's `.next` chunks modification time (`ls -la .next/server/chunks/ssr/`) — they should be from the current minute, not from hours ago. If they're old, the old server is serving them.

### Next.js dev server auto-refresh loop (HMR blocked via tunnel)

**Problem:** Accessing KF via Cloudflare tunnel (`kflow.thefirstonly.com`) causes the page to refresh every few seconds.

**Root cause:** Next.js dev server blocks HMR WebSocket from cross-origin domains. The browser console shows `[HMR] connected` but then disconnects/reconnects in a loop.

**Fix:** Add `allowedDevOrigins` to `next.config.ts` and restart dev server:

```typescript
// next.config.ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  allowedDevOrigins: [
    "kflow.thefirstonly.com",  // ← tunnel domain
    "localhost",
    "127.0.0.1",
    // Add any other domains that access the dev server
  ],
};

export default nextConfig;
```

Then kill the old process and restart:
```bash
# Find PID on port 3003
netstat -ano | grep 3003
taskkill //PID <pid> //F
npx next dev --port 3003
```

**Prevention:** Add this config before setting up any tunnel-to-dev-server access.

### CRITICAL: Raw HTML content trong card phá vỡ cả feed (2026-08-03)

**Symptom:** Feed chỉ hiện **1 card**, mọi bài báo "chưa đọc" (ví dụ `230/230 chưa đọc`), không scroll được.

**Root cause (2 tầng):**
1. Một số card có `content` = **raw HTML document đầy đủ** (`<!DOCTYPE html>...<style>...` — từ pipeline upload/gist lưu nguyên trang HTML). Feed render `renderMarkdown(card.content.slice(0,300))` → inject thẻ `<style>` KHÔNG đóng vào DOM → trình duyệt chuyển sang raw-text mode, **nuốt toàn bộ phần còn lại của trang** vào bên trong card đầu tiên (kiểm tra: `.space-y-4` chỉ có 1 child, child đó chứa 3MB HTML).
2. Vì DOM sập + hydration script không chạy → `fetch('/api/read-status')` không bao giờ thực thi → readIds rỗng → mọi card hiện "chưa đọc".

**Diagnosis nhanh (browser_console, không cần vision):**
```js
document.querySelectorAll('.card-surface').length        // = 1 (thay vì 20)
document.querySelector('.space-y-4').children.length     // = 1
document.querySelector('.markdown-content').textContent.length  // = 3MB (thay vì ~300)
```

**Fix:** Escape HTML entities **ĐẦU TIÊN** trong `renderMarkdown` (cả `feed-client.tsx` LẪN `card-detail-client.tsx`):
```js
let h = md
  .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")  // ← phải đặt trước mọi regex
  .replace(/```(\w*)\n([\s\S]*?)```/g, ...)
  .replace(/^&gt;\s*(.*)$/gm, "<blockquote>$1</blockquote>")  // blockquote giờ match &gt; vì > đã bị escape
  ...
```
**Lưu ý:** sau khi escape, regex blockquote phải đổi `^>` → `^&gt;`. Các thẻ HTML do renderMarkdown SINH RA (`<pre>`, `<strong>`, `<h2>`...) vẫn hoạt động vì chúng được thêm SAU bước escape.

**Phòng ngừa:** pipeline import HTML (gist/upload) phải convert HTML → markdown trước khi lưu card, hoặc card content phải là markdown thuần. Khi phát hiện card content bắt đầu bằng `<!DOCTYPE` hoặc chứa `<style>` → cần cleanup content.

### Markdown links not rendering (fixed 2026-10-18)

`renderMarkdown` không parse link markdown → tham chiếu hiện raw `[10.1098/rstl.1865.0008](https://doi.org/...)`.
Có **4 bản `renderMarkdown` trùng lặp** phải sửa cùng lúc: `src/app/card/[id]/card-detail-client.tsx`,
`src/app/book/book-client.tsx`, `src/app/feed/feed-client.tsx`, `src/app/feed-client.tsx`.
(`renderInline` thì đã có link — chỉ `renderMarkdown` thiếu.)

Thêm NGAY SAU bước normalize blockquote (`</blockquote>\n<blockquote>` → `<br>`), tức TRƯỚC bold/italic
(nếu đặt sau bước escape & sau inline-code thì URL trong `<code>` được bỏ qua an toàn vì tiền tố là `>`):

```js
h = h.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, "<a href='$2' target='_blank' rel='noopener'>$1</a>");
h = h.replace(/(^|[\s(])(https?:\/\/[^\s<>'")]+)/gm, "$1<a href='$2' target='_blank' rel='noopener'>$2</a>");
```

Vì đã escape `&`→`&amp;` TRƯỚC, URL có query string vào `href` vẫn hợp lệ. Regex URL trần chỉ khớp khi
đứng đầu dòng/sau khoảng trắng/dấu `(` ⇒ không đè lên `href='...'` vừa sinh. CSS kèm theo (globals.css):
`.markdown-content a { color:#7cc4ff; text-decoration:underline; word-break:break-word }` + hover vàng.

Sau khi sửa: `next build` → kill PID theo `netstat` → `next start --port 3003`. Verify bằng browser:
`document.querySelectorAll('.markdown-content a').length` > 0 và `/\]\(https?:/.test(document.body.innerText)` = false.

### Markdown tables not rendering

Custom `renderMarkdown()` function needs explicit table parser. Without it, `| col | col |` shows as raw text. Add BEFORE the paragraph-parsing section:

```javascript
// Tables
h = h.replace(/\|(.+)\|/g, (_, row) => {
  const cols = row.split('|').filter(Boolean).map(c => c.trim());
  if (cols.every(c => /^[-:\s]+$/.test(c))) return '';  // skip separator row
  return `<tr>${cols.map(c => `<td>${c}</td>`).join('')}</tr>`;
});
h = h.replace(/(<tr>.*<\/tr>\n?)+/g, m => `<table>${m}</table>`);
h = h.replace(/<\/table>\n<table>/g, '');
```

Also add CSS in `globals.css` for table borders, header styling (#FFD600), zebra stripes.

### Book TOC not responding

Use card ID-based navigation not index-based:
```tsx
const [currentId, setCurrentId] = useState(cards[0]?.id || "");
const currentCard = cards.find(c => c.id === currentId);
```
Render content with `key={currentId}` to force React re-render:
```tsx
<article className="..." key={currentId}>...</article>
```
This is more reliable than `flatCards[currentIdx]` because the card identity is stable even when the component recalculates grouping.

### Mobile header overflow
Use `flex-col sm:flex-row` on header container. Separate search for mobile vs desktop.

### Hydration mismatch after file edits

**Symptom:** After editing a `"use client"` component (like `feed-client.tsx` or `card-detail-client.tsx`) while the dev server is running, the browser shows "Hydration failed because the server rendered HTML didn't match the client".

**Root cause:** Turbopack hot-reloads only the client-side JS bundle. The server-side HTML (SSR) is NOT recompiled until the next full page request. The old HTML has different class names / structure from the new client code.

**Fix:** Do a hard page refresh (F5) in the browser. This triggers a new server render with the recompiled server bundle. If the problem persists, kill and restart the dev server. The error is harmless — React recovers by re-rendering on the client, but the dev overlay may trigger subsequent "Jest worker" crashes (see below).

**Prevention:** For major structural edits to client components, restart the dev server cleanly:
```bash
# Kill old process
netstat -ano | grep 3003 | grep LISTENING
taskkill /F /PID <pid>
# Clear cache and restart
rm -rf .next/dev/cache
npx next dev --port 3003
```

## Research → KFlow sync (job `da7c6b38c7d9`, 00:00 daily) — 2026-09-23

Chi tiết: `references/kflow-sync-pipeline.md` — gap mà job này tồn tại để lấp, script tái dùng (`html2md.py`, `kf_push_backlog.py`, `kf_verify.py`), recipe tách 2 tab từ HTML (không dựa vào panel id cố định), passcode cookie, PITFALL viết tiếng Việt qua `curl -d`, diacritics gate trước khi push, dedup false positives.
Lịch sử từng lần chạy (2026-09-25 → 2026-10-19, bài học xương máu từng run): `references/kflow-sync-run-log.md`

---

## Card Detail — 2-Tab System (Visualize + Học thuật) — từ 13/08/2026

Chi tiết: `references/card-detail-2tab.md` — hai tab làm gì, chuẩn mới 13/08/2026 (bỏ tab `Overview` cũ), PITFALL OVERVIEW block lộ ra ngoài feed/book/card, Structured Overview block (đọc bởi `parseAzuEasy` → Visualize tab), known limitation khi content thưa, update 2026-07-22 `parseOverview` bị Azu-Easy thay thế.

---

## Dashboard View (`/dashboard`)

A proper analytics dashboard with 4 sections:

### Section 1 — KPI Badges
4 compact badges: tổng bài, đã đọc, chưa đọc, chuyên mục. Below: overall reading progress bar.

### Section 2 — Topic Breakdown
Horizontal bar per topic showing `read/total` with % color-coded (green/yellow/red). Click → filtered feed.

### Section 3 — Unread Priority
Top 7 recent unread cards. Each row: emoji + title + topic tag + time. Link to card detail.

### Section 4 — Topic Grid
4-column card grid (2-col mobile): emoji + name + count + progress + action button ("Bắt đầu" / "Đọc tiếp" / "Ôn tập").

**Data source:** `GET /api/dashboard` — compound endpoint with all metrics.
**Categorization:** topics.title or keyword fallback over 9 categories.
**CSS:** azulejaria tokens (#1a1a1a bg, #0047AB accent).

---

## Real-Time Search

The search page (`/search`) uses **client-side real-time filtering**: no Enter key needed, results appear as you type.

**Implementation (`search-client.tsx`):**
```typescript
const [query, setQuery] = useState("");
const [cards, setCards] = useState<Card[]>([]);
const [loading, setLoading] = useState(true);

// Fetch ALL cards on mount (only ~115, fast enough for client-side filtering)
useEffect(() => {
  fetch("/api/cards")
    .then(r => r.json())
    .then(data => { if (Array.isArray(data)) setCards(data); })
    .catch(() => {})
    .finally(() => setLoading(false));
}, []);

// Filter as user types — useMemo for performance
const results = useMemo(() => {
  if (!query.trim()) return [];
  const q = query.toLowerCase().trim();
  return cards.filter(c =>
    c.title.toLowerCase().includes(q) ||
    (c.summary || "").toLowerCase().includes(q) ||
    (c.tags || []).join(" ").toLowerCase().includes(q) ||
    c.content.toLowerCase().slice(0, 500).includes(q)
  );
}, [query, cards]);
```

**Highlight matching text:**
```typescript
function highlightMatch(text: string, q: string): string {
  const escaped = q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const regex = new RegExp(`(${escaped})`, "gi");
  return text.replace(regex,
    '<mark style="background:rgba(255,214,0,0.3);color:#FFD600;border-radius:2px">$1</mark>');
}
```

**UX features:**
- 🔍 icon inside the input (absolute positioned)
- ✕ clear button when query is non-empty
- `X kết quả cho "từ khóa"` counter
- Empty state: "Gõ từ khóa để tìm kiếm" before typing
- No results: "Không tìm thấy kết quả" with suggestion to try other keywords
- Auto-focus on input (`autoFocus` prop)
- `search/page.tsx` is server component that just renders `<SearchClient />` with `dynamic = "force-dynamic"`

**No more server-side search:** The old server-component pattern with `searchCards()` and `searchParams` was replaced. The server page no longer receives `searchParams` props.

## Research Queue — Button Fix

**Problem (2026-07-22):** The "Thêm vào queue" button stayed `[disabled]` even after typing text in the topic input. Root cause: `disabled={!topic.trim() || adding}` was always true because `topic` state didn't update during React hydration or the `onChange` handler wasn't triggering.

**Fix:** Removed the `disabled` prop entirely. The form submission handler (`addItem`) already has `if (!topic.trim()) return;` as a guard. The button is always clickable; if the topic is empty, the handler silently no-ops.

Additionally, the `adding` state was already managed correctly with `try/catch/finally` — `finally { setAdding(false); }` ensures the button text reverts even on error.

Button label changed from `"Thêm vào queue"` to `"➕ Thêm vào queue"` (with emoji) and `"Đang thêm..."` to `"⏳ Đang thêm..."` for better visual feedback.

## Passcode gate (2026-07-31) — ⚠️ ảnh hưởng cron import

KFlow nằm sau gate passcode `<PASSCODE>` (cookie `tfo_auth` = sha256):
- Files: `src/proxy.ts` (Next 16 — `middleware.ts` đã đổi tên thành `proxy.ts`), `src/app/passcode/page.tsx`, `src/app/api/passcode/route.ts`
- Proxy cho qua: `/passcode`, `/api/passcode`, `/favicon.ico`, `_next/static`; mọi route khác (GỒM `/api/*`) redirect `/passcode` nếu thiếu cookie
- Build output phải có `ƒ Proxy (Middleware)` + `ƒ /passcode`; recipe: skill `web-passcode-gate`

**⚠️ PITFALL — cron auto-research có thể gãy:** cron POST `http://localhost:3003/api/knowledge` (kèm Bearer token, KHÔNG có cookie `tfo_auth`) sẽ bị proxy redirect 307 sang `/passcode` → import thất bại. Fix khi gặp: thêm `/api/` vào allowlist trong `proxy.ts` (chỉ gate trang, không gate API), HOẶC cron gửi kèm cookie. Kiểm tra cron output nếu research gần đây không vào được KFlow.

**Debug browser-side:** nếu UI báo `230/230 chưa đọc` + API redirect 307, kiểm tra cookie: `curl -s -b "tfo_auth=1d1e977a218bfa01fe61106c360c8acf667047e35f17fdb0f1a8484e06cfdb55" http://localhost:3003/api/read-status` phải trả readIds (không phải redirect). Cookie 30 ngày, host-only, httpOnly — nếu trình duyệt mất cookie → mọi `/api/*` fetch redirect `/passcode` → `res.json()` fail → readIds rỗng → "tất cả chưa đọc".

### OVERVIEW `players` / `applications` PHẢI là ARRAY (nếu là string → `/card/<id>` trả **500**)

`POST /api/knowledge` vẫn trả **201** nhưng trang chi tiết chết: `card-detail-client.tsx` (~dòng 436)
chạy `overview.players.slice(0, 5).join(", ")`. Guard chỉ kiểm `.length`, nên một **string dài lọt qua**
rồi `.join` không tồn tại → TypeError lúc SSR → HTTP 500 (`mechanism` thì code tự bọc string, `players` thì không).

```python
"players": ["LHC — vòng 27 km, chùm proton 6,8–7 TeV", "1.232 nam châm lưỡng cực 8,33 T"],  # ✅ array, mỗi phần tử ngắn
"applications": ["Nguồn sáng synchrotron cho tinh thể học", "..."],                         # ✅ array
"players": "LHC: vòng 27 km, ..."                                                           # ❌ 6/7 gate khác vẫn PASS
```

**Hệ quả cho verify:** 6 điều kiện còn lại (OVERVIEW parse được, dấu, `\ufffd`, shortcode, tags, source_url)
đều PASS trong khi trang vẫn 500 ⇒ **luôn gọi thật `GET /card/<id>` và bắt == 200**, đừng chỉ kiểm content.
Sửa card đã POST: PATCH `/api/cards?id=<uuid>` với content mới, **assert phần body sau block OVERVIEW giữ
nguyên byte-for-byte** trước khi gửi (`hermes-temp/fix_acc_overview.py`).

**Lưu ý phụ:** `GET /api/cards?id=<uuid>` có thể trả 500 (`statement timeout`) → đọc nội dung từ file payload
local hoặc full list khi cần PATCH. Chi tiết run 20/10/2026: `references/kflow-sync-run-log.md`.

### Card bị cắt cứng ở 5.000 ký tự (data loss importer tháng 7) — dấu vết & cách khôi phục

Dấu vết: `len(content) == 5000` **chính xác** + câu đứt giữa chừng + `source_url` là gist raw hoặc Wikipedia.
Nguyên nhân thật (tìm được 22/10): `knowledge-flow/scripts/import-notion.js:174` —
`content = extracted.text.slice(0, 5000)` — và payload tháng 7 tự viết `content[:5000]` đọc từ `*.md` trong
`C:/Users/<user>/`. **Không phải lỗi API hiện tại** (`/api/knowledge` không cắt).
Khôi phục: gist raw → `html2md.BLOCK |= {"html","body"}` → `html_to_md`; hoặc tìm file nguồn thật bằng cách
đọc **`tool_calls`** của message ngày import (`json.loads(tool_calls)[i]["function"]["arguments"]` — đoạn bị
cắt KHÔNG nằm trong `content` của message). Gate so khớp: **đối chiếu tập GIÁ TRỊ SỐ** (bỏ `.`/`,`) giữa bản cũ,
nguồn và md — `old - nguồn = 0` nghĩa là đúng tài liệu; thiếu vài giá trị nằm trong `<svg><text>` thì chấp nhận.
Đã đóng hết 17/17 card (0 card còn ở 5.000) — log: `references/kflow-sync-run-log.md`, mục Sync run 2026-10-22.

### state.db của Hermes có 2 bản — bản ở `D:\Hermes\hermes-home\state.db` là bản CHẾT

Cron cwd là junction (`~/AppData/Local/hermes` ↔ `D:\Hermes\hermes-home`) nên đọc nhầm rất dễ: bản sống là
`C:/Users/<user>/AppData/Local/hermes/state.db` (vài GB). Bản dưới `D:\Hermes\hermes-home` cứng ở 10/08/2026 →
query ra "0 session hôm qua, 0 preview key mới" (tưởng yên nhưng sai). **Luôn in `max(timestamp)` trước khi
kết luận "không có gì mới".** `search_files`/rg KHÔNG đọc được path xuyên junction (báo *cannot find the path*)
— dùng `grep` qua terminal.

## Deployment — Production Mode

Chi tiết runbook: `references/deployment-production-mode.md` — start production server, update sau khi sửa code (workflow đã verify), vì sao không dùng dev mode. Bản ghi ngắn cũ hơn: `references/production-deployment.md`.

---

## Verification

After changes:
1. `curl http://localhost:3003/` → 200
2. `curl http://localhost:3003/book` → 200
3. `curl http://localhost:3003/research` → 200
4. `curl http://localhost:3003/card/{id}` → 200
5. `POST /api/knowledge` (valid body) → 201
6. `GET /api/research-queue` → `[]`
7. Navigate to `/card/{id}` in browser — both Overview and Học thuật tabs render correctly
8. Browser console: 0 errors, 0 hydration warnings

## References — chi tiết tách riêng

- `references/feed-view-ux.md` — toàn bộ UX pattern của Feed (+ card preview, scroll, read-status, search dropdown, share, OG redirect, route handler, schedule page, responsive).
- `references/kflow-sync-pipeline.md` — job đồng bộ Research → KFlow hằng ngày: script, recipe tách tab HTML, passcode cookie, diacritics gate, dedup.
- `references/kflow-sync-run-log.md` — log/bài học từng lần sync (2026-09-25 → 2026-10-19).
- `references/card-detail-2tab.md` — Card Detail 2-tab (Visualize + Học thuật), Structured Overview, parseAzuEasy, lịch sử thay đổi.
- `references/deployment-production-mode.md` — runbook deploy production mode (kill PID, clean cache, verify, why-not-dev-mode).
- `references/production-deployment.md` — bản ghi deployment ngắn hơn (trước đó).
- `references/design-system-v1.md` — design tokens Premium Dashboard v1.0 (màu, spacing, radius, button, typography) — spec bắt buộc cho mọi UI.
- `references/cron-port-hallucination.md` — debug log vụ cron POST sai port 6680 + cách verify cron output và import lại card bị mất.
- `references/pubmed-multi-angle-search.md` — pattern 16 query PubMed 2 pha cho multi-angle search.
- `references/gap-keyword-scanning.md` — keyword dictionary scan để tìm GAP tự động.
- `references/notion-import-pattern.md` — pattern import từ Notion.
- `references/successful-card-example.md` — 4 card mẫu đạt chuẩn (4 kiểu card khác nhau).
- `references/card-overview-parser.md` — `parseOverview` đời cũ (đã bị Azu-Easy thay thế, giữ để tham chiếu).
