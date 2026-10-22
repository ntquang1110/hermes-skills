---
name: research-reporting
description: "Structure and present research findings as comprehensive HTML documents: multi-level explanations, patent deep-dive analysis, scientific reviews. Covers the authoring shape AFTER web-research gathers data and BEFORE html-publishing distributes it."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [research, reporting, html, analysis, patent-deep-dive, educational, multi-level]
    related_skills: [web-research, html-publishing]
---

# Research Reporting

Use this skill when you need to present research findings in a structured, multi-layered HTML document — after web-research has gathered the data, before html-publishing distributes the artifact.

## When to Use

- User asks for a "deep dive" into one or more topics (patents, scientific evidence, comparative analysis)
- User wants "từ ngu đến PhD" — explanations spanning beginner to expert level
- You're analyzing patents, technologies, or scientific evidence with multiple dimensions
- The output needs to be visually structured (tables, flow diagrams, stats cards) not just plain text
- User says "dựng lý thuyết và mô hình ở dạng biểu đồ" — they want visual understanding

## Default Workflow (HARD DEFAULT — do not skip, do not ask)

**Rule confirmed by user: "mặc định là yêu cầu research xong sẽ xuất ra html nhé"** and **"những gì anh yêu cầu em research thì em đẩy lên f-flow hết"**

After EVERY research task, automatically:

0. **Recall the pipeline before answering** — for research-group requests the deliverable is ALWAYS published HTML + KFlow link, never a chat-only text summary. State file `D:/Hermes Proj/.hermes-state/chat/telegram-group-hermes-research.md` records the pipeline; read it (or session_search) if unsure. Answering with plain text only = skipped deliverable (user will say "quên hết skill r, đọc lại session cũ đi").
1. **Compile data** (from web-research, Wikipedia API, or existing knowledge)
2. **Author HTML** following the structural patterns below
3. **Design** — see "Design System" below. **Default for Vietnamese research reports is Say Briefly (cream paper, forest green, yellow marker), NOT Premium B/W/Y.** User said so explicitly (01/10/2026: *"dùng say-briefly dựng design nhé"*). Copy `templates/say-briefly-report.html` and swap the body — do not retype the CSS block. Premium B/W/Y (`#FFD600` / `#0D0D0D` / `#1B1B1D` / `#242428`, dark, 28px radius) stays available for dashboards and dark-mode artifacts.
4. **Publish** to `preview.thefirstonly.com` via POST /api/store with JSON `{"content": "<html>", "title": "..."}` — use curl, NOT Python urllib (preview API returns 403 to urllib). For files >50KB write the JSON payload to a temp file, then `curl --data-binary @payload.json`.
5. **Save to KFlow** — passcode login required: Python `http.cookiejar` → POST `http://localhost:3003/api/passcode` with `passcode=<PASSCODE>` (307 redirect expected, cookie persists) → then POST `/api/knowledge` with `Authorization: Bearer hermes-knowledge-secret` AND the jar cookie. Localhost KFlow accepts urllib; only preview.thefirstonly.com rejects it.
6. **Report** all links back to user (preview URL + KFlow ID)

This is a HARD DEFAULT. Do not wait for the user to ask. Never skip steps 4 or 5.

## Confirm-before-execute (brief lớn, nhiều đầu việc)

**Rule confirmed by user (2026-09, brief bệnh lợn VN):** *"Em tổng hợp lại cho anh. Thì đầu tiên là em confirm với anh đã. Sau đó mới thực thi sau."* và *"em confirm trước sau đó thì mới làm"*.

Phân biệt 2 chế độ:

| Brief | Hành vi đúng |
|---|---|
| 1 câu hỏi / 1 chủ đề rõ | Làm luôn → publish → báo link (default flow ở trên) |
| Brief lớn: ≥3 đầu việc, hoặc user nói "research rất sâu", hoặc brief có nhiều phần rời (dịch tễ + danh mục + bảng + phản biện) | **Confirm TRƯỚC, không viết HTML** |

Khi confirm, trả về đúng 2 khối, KHÔNG viết HTML, KHÔNG research sâu trước:

1. **Em hiểu bài toán của anh như sau** — đánh số lại từng deliverable (1, 2, 3…), mỗi cái 1 khối gọn. Nêu rõ đầu ra (1 trang HTML? nhiều trang? bảng? diagram?).
2. **Question block** — 2-4 câu hỏi chặn thật sự cần trả lời trước khi bắt tay. Hỏi về: phạm vi (bao nhiêu mục), mức chi tiết (phân vùng sâu hay chỉ Bắc/Trung/Nam), nguồn lực/ngân sách, và mục đích dùng (để trình bày? để chọn sản phẩm?).

Câu hỏi phải **cụ thể và có lựa chọn sẵn** ("anh muốn top 5-7 hay danh sách đầy đủ 15-20 bệnh?") — không hỏi chung chung kiểu "anh muốn gì nữa không".

Sau khi user trả lời (thường bằng voice hoặc "Ok triển khai đi") → chạy thẳng, không confirm lần 2.

**Đừng** nhầm chế độ: brief ngắn mà đi confirm là làm phiền (user sẽ nói "triển khai đi"). Brief lớn mà chạy luôn là sai hướng cả bài.

## Structural Patterns

### Pattern A: Multi-Level Explanation ("Từ ngu đến PhD")

For when the user wants a concept explained from ground zero to expert depth.

Structure:
- **Level 0 — Ngu (cơ bản nhất):** No technical terms. Pure analogies (DNA=blueprint, RNA=photocopy). One sentence core: "DNA là bản thiết kế gốc, RNA là bản copy tạm đi làm việc."
- **Level 1 — Cấp 3:** Basic structure tables (components, differences). What is it made of?
- **Level 2 — Đại học:** Process flow (Central Dogma). Types and classifications. The standard curriculum.
- **Level 3 — Master:** Molecular mechanisms, chemistry, enzymes. WHY it works that way.
- **Level 4 — PhD:** Current research, cutting-edge applications, controversies. Technology implications.
- **Level 5 — Nobel/Origin:** The deepest layer. Origin of life, fundamental theories, the "big picture."

Each level MUST cite at least 1-2 scientific refs (PMID, journal, year).

Implementation:
```html
<div class="level-section" id="level0">
  <h2 class="level-title level-0">🐣 Level 0: Ngu</h2>
  <div class="analogy-box">...</div>
</div>
```

Color coding: Level 0=green, Level 1=blue, Level 2=orange, Level 3=red, Level 4=purple, Level 5=yellow.

Navigation: Sticky nav bar at top with anchor links to each level.

### Pattern B: Patent/Technology Deep-Dive

For analyzing one or more patents, technologies, or methods in detail.

Each patent gets its OWN HTML page with this structure:

```
I. TỔNG QUAN (Overview)
   - Stats grid: year, cost/m³, duration, efficiency
   - One-paragraph description of what it does
   - Link to original patent/source
   - "Dễ nhất" vs "Khó nhất" comparison card
   
II. FLOW TỔNG QUAN (7-Bước Process)
   - Arrow diagram showing the full process
   - Numbered flow steps, each with:
     * What to do (làm gì)
     * Requirements/Setup (yêu cầu)
     * Easy parts (✅ Dễ)
     * Hard parts (⚠️ Khó)
     * Cost estimate (💰 $)

III. DEEP DIVE — PhD (Chi tiết như PhD)
   - 3-5 deep dive boxes per patent
   - Each box = 1 key concept/innovation/mechanism
   - Include specific: specs, chemical formulas, equipment prices, failure modes

IV. CHECKLIST (Triển khai)
   - What to buy, where, how much
   - Total budget estimate
   - Timeline estimate
```

When analyzing MULTIPLE patents in a category, create:
- 1 overview page (table of ALL patents with columns: patent#, name, process, efficiency, country)
- 1 detailed page PER patent following Pattern B
- Link each row in the overview table → detailed page

### Pattern C: Scientific Evidence Review

For evidence-based health/medical/biological analysis.

Structure:
```
I. Tác dụng có lợi / hữu ích (proven benefits)
II. Tác dụng không hiệu quả (claimed but disproven)
III. Tác dụng không mong muốn & tại sao (adverse effects + mechanism)
IV. Tác động sinh học / tế bào (biological mechanism at cellular level)
V. Ảnh hưởng đến cuộc sống (real-life impact)
```

Each claim MUST have: mechanism explanation + at least 1 peer-reviewed reference (PMID).

## Visual Elements to Include

1. **Stats Grid** (numbers in boxes): `display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr))`
2. **Comparison Cards** (two-column): Benefits vs Harms, Easy vs Hard
3. **Flow Diagrams** (ASCII art in `<pre>` tags): Use colored spans for clarity
4. **Progress/Success bars**: For efficiency comparisons between methods
5. **Tables** with striped rows and hover highlight
6. **Ref boxes**: Blue-left-border boxes for citations
7. **Summary boxes**: Yellow-left-border boxes for key takeaways
8. **Sticky nav**: For multi-level pages, a top nav that follows scroll

## Design System

### Say Briefly (DEFAULT — Vietnamese research/analysis reports)

Cream paper, forest green backbone, yellow marker highlights. Source of truth is the
live gallery `https://preview.thefirstonly.com/13hh7gfof9xq` (54 design systems; read a
theme's token card with `curl -s <url> | python -c "..."` grepping the 500-char window
before `theme-slug\"><name><`). Ready-to-copy starter: `templates/say-briefly-report.html`.

Tokens:

```css
:root{--cream:#fcfaf5;--green:#1a3300;--yellow:#ffe95c;--teal:#a8e5e5;
      --ink:#1a1a1a;--gray:#7a7a72;--line:rgba(26,51,0,.12);--red:#b30000}
```

Fonts (Google CDN): `Bricolage Grotesque` 700/800 for display, `DM Sans` 400-700 body,
`JetBrains Mono` 400/500 for labels/meta. Display headings are **UPPERCASE, letter-spacing
.02em, weight 800**. Body 14px/1.7.

Background: cream plus a faint dot grid `radial-gradient(circle, rgba(26,51,0,.03) 1px,
transparent 1px); background-size:20px 20px`. Max width 840-860px.

Component kit (class names to reuse):

| Class | Purpose |
|---|---|
| `.hero` + `.label` / `h1` / `.sub` / `.meta` | Masthead. Label = `Say Briefly · <context>` in mono caps. Meta line carries source count ("13 PMID"). Ends with `border-bottom:3px solid var(--green)`. |
| `.sec` + `h2` | Section. h2 gets `border-bottom:2px solid var(--yellow)` and is `display:inline-block` so the rule hugs the text. |
| `.hl-box` (+ `.yellow` / `.teal` / `.red`) | Callout with 4px left rule. `.hll` = tiny caps label inside. This is the workhorse for "the point" of each section. |
| `.tw` + `.tb` | Table wrapper (`overflow-x:auto`) + table. `th` = green bg, cream text, 10px caps. `.fn` = bold first cell. |
| `.dia` + `.dl` + `.flow` / `.fn` / `.arrow` | Diagram frame + labelled arrow flow. `.fn` boxes are `max-width:155px` centred; `<small>` inside gives a grey sub-label. |
| `.bar` / `.bl` / `.bt` / `.bf` / `.bv` | Horizontal comparison bar (16px, `.bf.hi` turns red). |
| `.stat2` / `.st` / `.sn` / `.sl` | 4-up stat cards. |
| `.badge` + `.badge-y` / `-r` / `-g` | Tiny mono verdict chips inside tables. |
| `.footer` | Mono caps, `border-top:2px solid var(--yellow)`, left = brand, right = source tally. |

Humanizer rules still apply to the prose (no em/en dash, no emoji in headings, vary
sentence length, no rule-of-three padding).

### Premium B/W/Y (dashboards, dark artifacts)

```css
:root {
  --yellow: #FFD600;
  --black: #0D0D0D;
  --bg: #1B1B1D;
  --card: #242428;
  --card2: #2A2A2F;
  --text: #FFFFFF;
  --muted: #8B8B8B;
  --green: #44C767;
  --red: #FF4B4B;
  --orange: #FF9100;
  --blue: #448AFF;
}
```

Key rules: Dark background, yellow accent, rounded cards (28px radius), no shadows, border instead. Responsive via `@media(max-width:768px)`.

## Publishing & Distribution

After authoring the HTML:
1. Save to `D:/Hermes Proj/<filename>.html`
2. POST to `https://preview.thefirstonly.com/api/store` with JSON body `{"content": "<html>...", "title": "..."}` — dùng curl `--data-binary @payload.json` cho file >50KB (viết payload ra file trước, đừng nhúng inline)
3. Save structured summary to KFlow:
   - API: `POST http://localhost:3003/api/knowledge`
   - Auth: `Bearer hermes-knowledge-secret`
   - Fields: title, content (2-3 paragraphs), summary (one-liner), tags, topic_slug, source_url
4. **Verify KFlow đã lưu**: `GET /api/knowledge/<id>` trả 404 (API không hỗ trợ GET theo id) → verify bằng `GET /api/cards` (cùng Bearer + cookie passcode) rồi tìm card có id bắt đầu bằng ID vừa POST. Chưa verify thì chưa báo done.
5. Report all links back to user

### Pattern D: Multi-Group Comparison

For comparing two or more technologies/agents/methods side by side in depth.

Structure:
- **TỔNG QUAN**: Who/What each side is (stats grid)
- **KIẾN TRÚC**: Feature-by-feature table comparing all dimensions
- **CƠ CHẾ CỐT LÕI**: Two-column format highlighting the fundamental architecture differences
- **ĐIỂM MẠNH & YẾU**: Two-column grid showing what each side does better
- **KẾT LUẬN**: Verdict box with "chọn cái nào nếu bạn..."

### Pattern F: Easy Understand Companion ("đơn giản hóa")

When the user wants both detailed research AND a simplified version that anyone can read:

1. **Create the detailed research page** (full depth, all citations, PhD level)
2. **Create a companion "Easy Understand" page** with:
   - **ASCII art flow diagrams** (arrow-based, 3-7 step flows)
   - **3-key-results summary** at the top (what happened → why)
   - **"Kể cho người không chuyên" analogy section** (tòa nhà, cỗ máy, câu chuyện)
   - **Color-coded "lớp áo giáp" / layered defense diagrams** for multi-mechanism topics
   - **No jargon without explanation** define every term in plain language
3. **Link the two pages together** — Easy page links to the detailed page at the bottom
4. **Publish both** and **save both to KFlow**

File naming: `topic.html` (full) + `topic-easy.html` (simplified).

### Pattern G: Multi-Article Cross-Linking

When a research session produces multiple related HTML pages (e.g., overview table + N individual patent pages, or research + easy version + shopping list):

1. **Create a "hub" page** that lists all related articles with descriptions
2. **Link each article's preview URL** in the hub
3. **Add a "See also" section** at the bottom of each individual article linking back to the hub and to sibling articles
4. **Publish all pages** — the user can navigate the entire knowledge cluster

Example: Patent overview hub → patent #1, #2, #3... individual pages, each linking back to hub.

### Pattern H: Multi-Compound Catalog (mobile-first, 1 file HTML)

Khi user muốn "list đầy đủ các chất + mỗi chất bấm vào 1 trang chi tiết" (catalog tra cứu trên điện thoại — ví dụ: catalog hoạt chất trị tiêu chảy heo con 08/2026):

1. **Chia research theo nhóm, mỗi nhóm 1 subagent song song** (max 3 concurrent): groupA botanicals, groupB probiotics/acid, groupC khoáng/kháng thể. Mỗi subagent ghi JSON riêng vào `data/groupX_*.json` theo schema dùng chung (xem `references/catalog-data-schema.md` — có HAI schema: compound cho "mỗi chất 1 object" và row-level cho "mỗi dòng = 1 chất × 1 tác dụng"). Truyền schema đầy đủ + PMID gợi ý đã verify trong context — subagent tự efetch lại.
2. **Build = template.html + build.py**: template self-contained với placeholder `__DATA__` + JS render (list/filter/search/hash routing `#/ct/<id>`), build.py gom JSON → inject → 1 file final (~200KB). Publish preview chỉ nhận 1 file HTML nên không tách nhiều trang.
3. **PITFALL build.py đa key**: subagent JSON dùng key khác nhau tùy thằng (`compounds`/`lines`/`rows`/`items`/`data`). Script gom phải thử tuần tự tất cả và in count từng file; nếu thiếu key → 0 rows âm thầm (đã dính 2 lần: groupC dùng `lines`). Sau build luôn chạy check field: đủ summary/mechanism/evidence/references/mold_prevention.
4. **User preference (chốt 12/08, bản v3): bảng chia cột + cột CƠ CHẾ RỘNG + cột REF GỌN.** Bảng 4 cột (Nguyên tố | Tác dụng | Cơ chế | Ref) + search realtime highlight từ khóa (mark vàng) + click dòng mở modal chi tiết. **Cột Cơ chế là cột chính: RỘNG** (mobile min-width 240px, desktop ~333px, font 13px, màu sáng #D6D6D6) — user từng phản hồi "cho cột cơ chế to hơn". **Cột Ref NHỎ (~90px): chỉ hiện badge số lượng "6 refs →"** (kèm số patent nếu có "6 refs · 1 patent →"), bấm vào mới mở modal danh sách refs + link PMID ra PubMed — user chốt "ghi số lượng cũng được, bấm vào show ra sau", KHÔNG xếp PMID chips ngay trong bảng. Mobile: bảng min-width ~640px cuộn ngang trong `.table-wrap{overflow-x:auto}`; desktop full width. Card list chỉ dùng khi user không yêu cầu bảng.
5. **TAB DASHBOARD thứ 2 (kiểu Obsidian)**: bottom nav 2 tab (Bảng | Dashboard). Dashboard gồm: stats grid (tổng dòng, số chất/dạng riêng, bằng chứng Mạnh, không bằng chứng) + lưới "số tác dụng theo từng chất" (click chọn) + **mindmap SVG**: 1 chất trung tâm → nhánh tác dụng. Màu node: xanh dương = có PMID, xanh lá = có patent, xám = chưa ref. Click node tác dụng mở modal, click tâm đổi chất. Chi tiết kỹ thuật: `references/catalog-table-dashboard.md`.
6. **Verify browser**: camofox chặn file:// → serve HTTP bằng `python -m http.server` (xem skill camofox-browser). Model không vision (deepseek-v4-flash) → verify bằng JS đo overflow trên viewport mobile + test search/filter/modal qua playwright-core `.cjs` (browser_console trên Camofox đôi khi 500 → retry 1 lần hoặc dùng playwright evaluate).
7. **PITFALL claim pháp lý viết sớm**: đừng viết claim thực trạng pháp lý ("chưa được EU công nhận") vào template TRƯỚC khi data về — subagent có thể lật ngược (REE: EU ĐÃ phê duyệt Lancer 2020/1370, TQ phê duyệt RECC). Chờ data, kiểm tra phát hiện chính, rồi sửa note-warn cho đúng.
8. **Chống mốc / ổn định là section bắt buộc** cho chất chiết xuất dạng lỏng — user có case thật (extract bị mốc). Công thức chuẩn: cồn ≥20-25%, pH ≤4.5, kali sorbat + natri benzoat, lọc 0.22µm, bao kín tối màu, kho 15-25°C (chi tiết trong reference).

### Pattern I: Quy trình + Bản chất (2-tab process flow, "bỏ bước thì sao")

Khi user muốn hiểu SÂU một quy trình công nghiệp theo từng bước — mỗi bước đóng vai trò gì, tại sao dùng cách đó, bỏ bước thì sao. Ví dụ đã chốt 12/08: xử lý chất thải heo công nghiệp (Xuân Thiện 2000 m³/ngày: lên men vi sinh → biogas → NaOH tăng pH → H2SO4 giảm pH).

User yêu cầu 2 DẠNG rõ ràng: "1 dạng overview flow rất dễ hiểu về quy trình + bước cơ bản, thứ 2 đi sâu học thuật tại sao dùng như thế, đi về bản chất của vấn đề". Cấu trúc:

1. **2 tab trong 1 file HTML**: `① Overview Flow` + `② Học thuật sâu` (tabbar trên đầu + bottom nav, giống catalog dashboard).
2. **Tab Flow**: timeline dọc, mỗi bước 1 card với số thứ tự node. Mỗi card BẮT BUỘC có 3 dòng tag màu: `Đầu vào` (xanh dương) / `Đầu ra` (xanh lá) / `Bỏ thì` (đỏ) — user hỏi "nếu bỏ bước ấy đi thì sao" cho MỌI bước, không được thiếu cái nào. Kèm mức bằng chứng + số refs.
3. **Tab Bản chất (học thuật)**: mỗi chủ đề 1 card có `detail` (giải thích sâu: phương trình, chủng vi sinh, điều kiện vận hành) + box vàng `Tại sao cần bước này` + box đỏ `Nếu bỏ / thiếu` + refs (PMID link PubMed, patent link Google Patents/Espacenet) + verify box.
4. **Nhiệm vụ quan trọng của research**: so quy trình user kể với quy trình CHUẨN của ngành — chỉ ra bước họ THIẾU (vd Xuân Thiện thiếu nitrification/denitrification SBR/MBBR → BOD + N-NH4 vượt QCVN; "tăng pH NaOH" phải có tháp stripping + hấp thụ H2SO4 mới thực sự khử N, chỉ tăng pH rồi hạ lại thì NH3 tan về nước). Đây là giá trị cốt lõi user cần khi đối tác kể quy trình — không chỉ mô tả mà phải phản biện.
5. Schema JSON row-level: `{id, step|topic, phase|sub, purpose, mechanism|detail, why, if_skip, input, output, evidence_level, references[], verification}`. File nhóm: `group1_overview.json` (các bước flow), `group2_*.json` + `group3_*.json` (chủ đề bản chất).

For user asking "cần mua gì, để làm gì, dùng cho test nào".

Structure:
- **Product table** with 7 columns: #, Tên hàng, Quy cách, Tác dụng, Test nào, Giá (USD), Mua ở đâu
- **3 categories**: Hóa chất, Dụng cụ thủy tinh, Thiết bị hỗ trợ
- **Total budget box** at the end
- **Safety notes** as two-column grid (cực kỳ nguy hiểm vs an toàn)
- **Local supplier list** (where to buy in Vietnam)

## Batch Flow for Multiple Patent Categories

When analyzing many patents across categories (EKR, washing, chemical, biological, etc.):

1. **Create overview page** listing ALL patents across ALL categories
2. **Process each category** — create individual HTML pages per patent
3. **Link overview → detail pages** — add `📄 Phân tích` links to each row
4. **Re-publish overview** after adding all links
5. **Save to KFlow** with tags for each patent group

See `references/patent-batch-analysis.md` for the exact workflow used in the 24-patent soil remediation session.

See `references/patent-examination-opinion.md` when the deliverable is a **judgement** on a proposed solution (chủ đơn hỏi "tổ hợp kỹ thuật này có nộp đơn được không?" / FTO) rather than a "clone lại patent này" deep-dive — khung báo cáo thẩm định tiếng Việt: đọc claim gốc trước, bảng chỉnh lệch hồ sơ, ma trận novelty bước × tài liệu, problem-and-solution, bộ claim mẫu (gồm claim sản phẩm có tham số định lượng), bảng objection ↔ đối đáp, mục "hạn chế tra cứu", chiến lược GPHI dự phòng.

See `references/founder-strategy-profile.md` for founder-strategy profiles (research EN → output VI): 4-block structure per dimension, reusable 8-dimension Musk frame, source hierarchy, Wikipedia/Jina extraction tips.

### Pattern J: Research JSON → 2-tab (Visualize + Học thuật) — không qua KFlow card

Khi research từ subagents ghi JSON (không có card KFlow gốc): 3 subagents song song mỗi nhóm 1 file `group{N}.json` (schema topics/facts/PMID, xem `references/research-json-to-2tab.md`) → generator script `build_{project}.py` đọc JSON render 2 tab (Visualize: hero + flow 8 fnode + goal vàng; Học thuật: h2/summary/facts/PMID/mechanism) → publish preview → KFlow. Mẫu chạy OK: `D:/Hermes Proj/wssv-research/build_wssv.py` (21 topics, 73 PMID). Pitfall chính: subagent hay hết iteration trước khi ghi file → prompt yêu cầu flush JSONL sau mỗi 2-3 topic, parent đọc file thật (không tin summary) + verify lại vài PMID.

**BẮT BUỘC trình bày 2 tab theo 2 pattern đã chốt 16-17/08/2026** (user phản hồi trực tiếp trên trang premix-heo và berberine-tannin):

1. **Tab Visualize = card grid + MODAL POPUP, KHÔNG cắt thông tin.** User: "visualize đang bị cắt, chưa đủ thông tin... làm dạng popup để bấm vào xem cho đủ chữ". Card chỉ hiện: tên + badge bằng chứng + liều + tóm tắt ~110 ký tự + dòng vàng "Bấm xem chi tiết →". Bấm card mở modal đầy đủ: tên khoa học, nhóm, liều, summary, từng mechanism (kèm PMID), bằng chứng (type + mức + PMID), bệnh liên quan, an toàn, references. Đóng modal: nút ×, bấm ra ngoài, hoặc Esc. `body overflow:hidden` khi modal mở.
2. **Tab Học thuật = ACCORDION + FACT CARDS, KHÔNG đoạn văn dài.** User: "học thuật có cách nào dễ nhìn dễ đọc hơn ngoài các đoạn văn không". Mỗi topic = 1 accordion (số tròn vàng + tiêu đề + mũi tên gấp/mở, `toggleAcc`); mỗi fact = 1 card nhỏ (`.fc`) có **badge màu theo loại nguồn**: PAPER vàng (PMID), PATENT xanh lá, DỮ LIỆU xám (industry). Box tóm tắt xám `.acsum` đầu mỗi topic. Callout quy trình thực hành `.accmd` (viền vàng trái) tách khỏi lý thuyết. Mặc định mở hết accordion (`document.querySelectorAll('.acc').forEach(a=>a.classList.add('open'))`).
3. CSS/JS pattern sẵn dùng (đã chạy OK trên `D:/Hermes Proj/premix-heo-research/build_premix.py` và `berberine-tannin-extraction/build_extraction.py`): xem `references/2tab-modal-accordion.md`.

### Pattern K: Chiến lược + Phản biện + Bảng dữ liệu lớn (brief ra quyết định)

Khi user đưa một brief dài nhiều phần và chốt bằng *"em phản biện cho anh… em tự phản biện lại. Để làm cho mình có cái tư duy sắc nhất. Và về mặt khoa học là đúng nhất"* (điển hình: bản đồ bệnh lợn VN → 2 hàng rào phòng bệnh):

Cấu trúc trang (mục 1→8), thứ tự KHÔNG đổi:

1. **Bối cảnh / lifecycle** — mốc thời gian hoặc giai đoạn, bệnh/tác nhân nào xuất hiện ở đâu. Kèm callout "điểm yếu nhất là khâu nào và tại sao".
2. **Phân vùng địa lý/dịch tễ** — tối đa 3 vùng, mỗi vùng 1 card: khí hậu + bệnh nổi bật + **nguyên nhân gốc rễ**. User hỏi "tại sao nó lại sinh ra cái gì thế" chứ không chỉ "có gì" — nguyên nhân là phần bắt buộc, không phải phụ lục.
3. **Danh mục tác nhân** — card grid, mỗi tác nhân có: tên + loại (badge VIRUS/VI KHUẨN) + **cơ chế tế bào** + **cơ quan tấn công** + tỉ lệ phổ biến + tỉ lệ chết + chi phí. Cơ chế phải ở cấp phân tử/thụ thể (thụ thể nào, độc tố nào, tế bào nào), không mô tả triệu chứng.
4. **Chiến lược 2 nhánh** — mỗi nhánh 1 card lớn: nguyên lý + cơ chế + tần suất/liều + **giới hạn an toàn**.
5. **Bảng so sánh sortable** — 20 tác nhân sort theo mức nghiêm trọng giảm dần, cột: # | Tác nhân | Loại | Cơ quan | Phổ biến | Chết | Chi phí. Kèm **short list 3 nhóm ưu tiên** (chết cao / phổ biến-dễ can thiệp / chi phí cao) để user chọn mục tiêu.
6. **Bảng thị trường** — cột: Đối tượng | Giải pháp hiện dùng | **Hiệu quả %** | **Vì sao đúng mức đó** | Chi phí | Tần suất. Cột "Vì sao" là cột giá trị nhất (đề kháng, chủng không khớp vaccine, tồn dư) — không được để trống. Kèm biểu đồ quy mô thị trường + tổng.
7. **PHẢN BIỆN SÂU** (mục user yêu cầu riêng, đừng gộp vào phần khác). Cho MỖI hàng rào/giải pháp, đúng 3 khối theo thứ tự:
   - **Bằng chứng khoa học: ĐÃ CÓ** — 3-4 nghiên cứu thật (PMID + tên tạp chí + năm + số liệu cụ thể). Phải là nghiên cứu gần đúng đối tượng, không phải suy luận.
   - **Phản biện: N rủi ro & giới hạn thực tế** — đánh số. Đây là khối user đọc kỹ nhất. Phải có giới hạn CƠ HỌC (chất hữu cơ vô hiệu hóa), giới hạn AN TOÀN (bỏng kiềm/niêm mạc), giới hạn VẬN HÀNH (ăn mòn thiết bị), và giới hạn PHẠM VI (không chặn được đường lây nào).
   - **Hiệu quả dự kiến** — thanh `.eff-bar` định lượng từng mức (bề mặt sạch 95% vs bề mặt bẩn 40% vs lây qua không khí 15%). Tách "in vitro" khỏi "thực địa" — khoảng cách giữa hai con số này chính là phần kết luận.
8. **Hệ phân tầng + Bước tiếp theo** — diagram nhiều tầng, mỗi tầng 1 mục tiêu %. Kèm callout đỏ **cảnh báo khoa học**: nói rõ số liệu nào là ước lượng từ in vitro/loài khác, chưa có thử nghiệm đối chứng trên đối tượng thật, và liệt kê 3 bước validate cần làm (độc tính cấp/bán cấp, thử có nhóm đối chứng ≥100 mẫu, chỉ số đo cụ thể).

**Luật phản biện:** mỗi claim có lợi PHẢI đi kèm 1 dòng giới hạn của chính nó. Nêu rõ khoảng trống chưa ai làm ("chưa có nghiên cứu nào đánh giá tổ hợp 5-7 chất này trên lợn") — khoảng trống đó là cơ hội, đừng giấu. Không có mục nào chỉ toàn điểm mạnh.

**Không được:** viết "theo các chuyên gia" mà không có PMID; bỏ qua rủi ro an toàn; trình bày hiệu quả in vitro như hiệu quả thực địa.

CSS component + spec cột bảng: `references/strategy-critique-and-data-tables.md`.

### Pattern L: Tiered Concept Glossary ("list cho anh toàn bộ thuật ngữ X")

Khi user không hỏi về một chủ đề mà yêu cầu **dạy cả một mảng kiến thức** ("giải thích cho anh toàn bộ thuật ngữ sinh học ... protein, enzyme, cytokine ... Và tại sao"):

**Luật đầu tiên: sửa giả định trước.** Câu hỏi thường chứa một tiền đề sai (ở đây: các thuật ngữ là một danh sách phẳng cần học thuộc). Chúng là **một chồng tầng**, tầng dưới là nền cho tầng trên. Tổ chức lại theo tầng chính là câu trả lời — nói rõ điều đó ngay dòng đầu ("Cách sắp xếp: 6 tầng, không phải danh sách").

**Schema BẮT BUỘC cho mọi mục** — trả lời đúng 4 câu, cùng thứ tự:
`Nằm ở đâu` (vị trí; vị trí quyết định chức năng) → `Cơ chế` → `Tại sao có` (giải bài toán gì — câu sâu nhất) → `Thiếu thì sao` (tô nền đỏ). Card: header số + tên VI + thuật ngữ EN mono caps, rồi 4 dòng label; dòng "thiếu" `background:rgba(179,0,0,.035)`.

Thứ tự mục: (1) nguyên tắc sắp xếp + grid tầng; (2) **bản đồ không gian TRƯỚC khi vào thuật ngữ** (với sinh học: grid 8 vùng tế bào, mỗi vùng ghi cấu trúc nào nằm đó); (3) mỗi tầng 1 section, mở đầu bằng bảng phân biệt các loại dễ lẫn (ai gửi / đi đường nào / tới ai); (4) chain diagram cho quan hệ một chiều; (5) **bảng tra nhanh** toàn bộ thuật ngữ mỗi cái 1 câu; (6) N điểm chính dạng `<ol>`; (7) kết.

**Kết bằng một quy luật xuyên suốt, KHÔNG phải tóm tắt.** Ví dụ đã dùng: "hầu hết cơ chế sinh học đều có hai chiều đều gây bệnh" → rồi reframe "câu hỏi đúng không phải tốt hay xấu, mà là đâu là điểm cân bằng".

**Nối mỗi tầng về vận hành thật của user** trong dòng "thiếu thì sao" (TLR bị kích hoạt bởi nội độc tố bụi chuồng → viêm mạn → giảm tăng trọng; thiếu coenzyme → enzyme còn nguyên nhưng không chạy). Đây là chỗ biến tài liệu giáo dục thành thứ dùng được.

### Pattern M: Cùng công thức, khác cấu trúc (chemistry explainer)

Trigger: "tại sao chỉ khác nhau về số lượng mà cơ chế khác được". Cấu trúc có xương sống kể chuyện, đi đúng thứ tự:

1. **Sửa tiền đề** rồi ra một câu: công thức là bảng chữ cái, cấu trúc là câu. (Sự thật mạnh hơn câu hỏi: cùng số nguyên tử y hệt vẫn khác hoàn toàn.)
2. **Ví dụ sắc nhất trước: C2H6O** — ethanol (sôi +78°C, uống được) vs dimethyl ether (sôi −25°C, khí đẩy bình xịt). 9 nguyên tử, khác một chỗ nối, **chênh 100°C nhiệt độ sôi**. Cơ chế sạch: donor 1 vs 0 → ethanol tạo liên kết hydro. Bảng 2 cột, không viết văn.
3. **Bốn kiểu đồng phân**, mỗi kiểu 1 ví dụ: cấu tạo (C3H6O) · vị trí (theophylline vs theobromine — cùng công thức, cùng MW, cùng complexity, khác vị trí 1 methyl) · lập thể (thalidomide, kèm chi tiết hai dạng **tự chuyển hóa lẫn nhau in vivo** nên không thể tách an toàn) · trạng thái oxy hóa.
4. **Bằng chứng mạnh nhất: glucose vs galactose** — cùng C6H12O6, PubChem cho **mọi chỉ số lý hóa GIỐNG HỆT** (XLogP −2.6, TPSA 110, donor 5, acceptor 6, complexity 151), chỉ khác chiều xoay 1 nhóm OH, mà sinh học khác hoàn toàn (GALT/galactosemia). Chốt: **cơ thể không đọc công thức, cơ thể đọc hình dạng.**
5. Cơ chế vì sao đọc được hình dạng: khe 3D + 3 tầng nhận dạng (hình dạng / nhóm chức / chiều xoay; khe protein cũng bất đối).
6. **Ca lâm sàng chênh 1 nguyên tử**: morphine vs codeine — 1 CH3 bịt nhóm OH, donor 2 → 1, codeine thành **tiền chất** cần CYP2D6. Kèm hệ quả di truyền (chuyển hóa kém → không giảm đau; siêu nhanh → ngộ độc).
7. **Chốt tổ hợp**: C30H62 có **4.111.846.763** cách xếp. Thêm nguyên tử = thêm **thông tin**, không phải thêm khối lượng.
8. **Land vào việc của user**: avicularin và guaijaverin cùng công thức (quercetin + arabinose, khác dạng vòng) → **không thể định lượng chất này suy ra chất kia**, mỗi chất phải có chất đối chiếu riêng.

Fetch PubChem 1 call cho cả cặp: `/rest/pug/compound/cid/<CID1>,<CID2>/property/MolecularFormula,MolecularWeight,XLogP,TPSA,HBondDonorCount,HBondAcceptorCount,Complexity/JSON`. **Pitfall:** `CanonicalSMILES` trong danh sách property trả 400 với vài CID → bỏ ra, các trường số trên đủ dùng.

Chi tiết đầy đủ (schema card, CID list, checklist verify, pitfall `<tr>` trong cấu trúc div, pitfall đường dẫn `~` khi cwd khác ổ đĩa): `references/concept-explainer-patterns.md`

## Pitfalls

1. **Don't stop at description** — user wants actionable detail: "có thể clone lại cái patent này cho anh làm được". Each step must include: what, how, why, cost, difficulty.
2. **Don't skip hard parts** — "cái gì khó nhất, cái gì đơn giản nhất" must be explicitly called out in every analysis.
3. **Cost estimates required** — every flow step needs a `$` tag. Total project budget at the end.
4. **Flow diagrams matter** — user wants "vẽ flow từng bước" with arrows. Use ASCII art in `<pre>`, don't just describe in prose.
5. **KFlow is not optional** — after publishing, always save to KFlow. This is a DEFAULT step, not a "nice to have." The user explicitly said "những gì anh yêu cầu em research thì em đẩy lên f-flow hết."

   **Phạm vi KFlow (user chốt 2026-09):** KFlow chỉ nhận **research sâu**. KHÔNG đẩy bài tâm lý hàng ngày vào KFlow — bài tâm lý đi kênh Threads theo lịch riêng (20:00 tâm lý, 20:30 MIT, 21:00 HLL). Nếu thấy cron/agent nào đang đẩy bài tâm lý vào KFlow: đó là luồng sai, pause nó (cron `KFlow Push Tâm lý`) và báo user — đừng để KFlow bị pha loãng. Rule "research → KFlow" chỉ áp dụng cho đầu ra research.
6. **Memory about the format is not enough** — if the user explicitly confirmed a format ("anh có thấy em làm đúng rồi"), capture the format in this skill, not just in memory. Memory tracks preferences; skills track workflows.
7. **Hard default means do it always** — never skip publish + KFlow saving even for "quick" research. Speed it up by automating the curl/API calls, don't skip the step.
8. **Plain-text answer = skipped deliverable.** If a research question is answered only as chat text without preview URL + KFlow ID, the user flags it immediately ("quên hết skill r, em đọc lại session cũ đi"). The pipeline is fixed: research → HTML (Premium B/W/Y) → publish preview → KFlow (passcode + bearer) → report links. When in doubt, re-read the chat state file before responding.
9. **Google Patents hay bị throttle 503** khi gọi liên tục (xhr/query API). Nếu 503: sleep 45-60s rồi retry; nếu vẫn chặn, đừng bịa patent number — ghi `number=''` + `note='chưa verify'` trong reference. Chỉ đưa patent thấy được nội dung thật.
10. **PMID phải efetch verify từng cái** — không dùng PMID từ trí nhớ/chủ quan. Subagent phải chạy esearch + efetch, chỉ giữ bài có abstract đúng chủ đề. Reference không verify được thì ghi rõ "chưa verify" thay vì bỏ trống im lặng.
11. **Subagent hết iteration trước khi ghi JSON — recovery bắt buộc.** Đã xảy ra 2/3 subagent trong session 12/08 (báo "hit tool-call cap / max_iterations" nhưng research đã verify xong). Khi delegation báo completed mà file `groupX_*.json` MISSING: (a) đọc full summary file `C:/Users/NTQUANG_DELL/AppData/Local/hermes/cache/delegation/subagent-summary-*.txt` — nhiều subagent nhúng toàn bộ JSON inline trong markdown code block (extract bằng regex ```json ... ``` rồi json.loads validate); (b) nếu chỉ có dữ liệu rải rác + helper scripts, tự assembly JSON từ PMID verified + QCVN/PDF đã tải. Đừng re-dispatch — dữ liệu đã xong, chỉ thiếu bước ghi file.
12. **Đọc CLAIM gốc = curl trang chi tiết Google Patents (verify 24/09/2026 — sửa lại ghi chú cũ "detail page bị chặn").** `curl -s -A "Mozilla/5.0 … Chrome/120" -o p.html "https://patents.google.com/patent/<PN>/en"` → HTTP 200, HTML server-rendered chứa **claim nguyên văn**; strip tag bằng Python rồi cắt từ mốc `Claims (` (hoặc `What is claimed`). Script sẵn: `scripts/patent_claims.py` trong skill `vietnam-herbal-research`. Chỉ **XHR search** (`/xhr/query?url=q%3D…`) mới throttle sớm (~3–5 request → `<title>Sorry...</title>`) → sleep 45–60s rồi retry, hoặc dùng `browser_navigate` + `browser_console` (`document.body.innerText.slice(innerText.indexOf('Claims ('))`; **layout mới KHÔNG còn `section[itemprop="claims"]`** nên selector đó trả rỗng). **Espacenet = fallback CUỐI** khi cả curl lẫn browser đều 503: `https://worldwide.espacenet.com/patent/search?q=<keyword>` bằng browser_navigate + đọc publication number từ DOM (CN210855757U, CN101654321A, US10329206B2, JP2017029893...). FreePatentsOnline cũng chặn; WIPO Patentscope cần thư viện brotli. Luật: chỉ ghi số patent THẤY được nội dung thật (claim tải được / DOM Espacenet) hoặc ghi `number:''` + note "chưa verify" — không bịa.
13. **Tiêu chuẩn/quy chuẩn VN bị Cloudflare chặn trên site pháp lý** (thuvienphapluat, luatminhkhue, Wayback CDX rỗng). Cách đã chạy được: tải PDF gốc qua browser (vd `qcvn62_2025.pdf`) rồi đọc bằng pymupdf/fitz (API `fitz` deprecated — dùng `import pymupdf`). Nếu không lấy được số cụ thể thì khai báo trung thực trong verification, KHÔNG nhớ số liệu bảng từ trí nhớ.

14. **KHÔNG tin secondary description của patent — đọc CLAIM gốc, luôn.** Secondary summaries (R&D notes, literature reviews, even your own earlier analysis) routinely contain critical errors: wrong assignee, wrong solvent, wrong key step, wrong purity numbers. This session found 4/4 patent descriptions in the user's own document were wrong when verified against actual claim text. The worst: EP2022343B1 was described as "Taisho + maltodextrin + spray drying" — actual claim 1 is "Yakult Honsha + water 90-98°C → Brix 20-30 → freeze drying (lyophilization)." No maltodextrin. No spray drying. The spray drying mentioned in the description was a COMPARATIVE EXAMPLE that was taught away from. This single error would have invalidated the entire novelty/inventive step analysis. **Always:** curl the patent HTML from Google Patents (`curl -s -A "Mozilla/5.0" -o p.html "https://patents.google.com/patent/<PN>/en"`) → extract claims via regex from `Claims (` to next section → compare against any secondary description before proceeding. Document discrepancies in a correction table.

15. **Multi-agent cross-validation for patentability opinions.** When the user asks "can I patent this combination?", do NOT answer from a single pass. Delegate 2+ parallel sub-agents with different expertise: (1) patent examiner / IP specialist (legal + prior art), (2) domain technical expert (chemistry/process feasibility). Each reads actual patent claims independently. Then synthesize their findings. The cross-validation consistently finds issues a single agent misses: the chemist spots "this IPA phase separation won't work because guava leaf extract lacks the ionic strength of tanning liquor" while the patent examiner spots "claim 17 extends to any natural tannin extract, not just tanning waste." Neither alone catches both. See `references/multi-agent-patent-cross-validation.md` for the protocol template.

16. **Nhãn rõ ĐO ĐƯỢC vs NGOẠI SUY cho mọi con số hiệu năng/benchmark — và KHÔNG để số ước lượng vào kết luận.** User yêu cầu bằng chứng, nên một con số ngoại suy đứng cạnh một con số đo thật mà không ghi nguồn là lỗi nặng: nó trông có thẩm quyền như nhau nhưng độ tin khác hẳn. Quy tắc (rút ra từ session 25/09/2026, báo cáo LLM router phải publish lại 2 lần):
    - Mỗi số trong bảng/card ghi rõ `đo trực tiếp trên máy này` hoặc `ngoại suy từ <nguồn> theo hệ số <x>` — ngay trong card, không ẩn xuống footnote.
    - **Kết luận/verdict không được chứa số ngoại suy không nhãn.** Nếu buộc phải dùng, nói thẳng "ước khoảng X, chưa đo".
    - Có số đo thật thì THAY con số cũ, và nói rõ số nào vừa đổi từ ngoại suy sang đo được (user đọc kỹ mục này, đây là chỗ tạo niềm tin chứ không phải chỗ giấu).
    - Trước khi kết luận "không đo được", kiểm tra file tải về thật: 8 part × 287.841.982 byte khớp đúng `content-length` 2.302.735.855 nghĩa là checkpoint ĐÃ đủ, chỉ bước nối file hỏng. Lỗi ở bước assembly trông y hệt lỗi tải hỏng — phân biệt trước khi báo user là "không có số".
    - Nếu dự đoán trước đó lệch với đo thật, nói rõ lệch bao nhiêu (vd dự đoán 1,0-1,1 s, đo 823 ms → lệch ~25%, đúng hướng nhưng cao hơn). Đừng lặng lẽ cập nhật số.
    - Chỉ đổi số suông là chưa đủ: HTML đã publish phải **publish lại bản mới** và gửi link mới; user đã mở link cũ.

17. **Subagent báo "đã ghi file, verified" là self-report, KHÔNG phải bằng chứng — luôn đọc lại từ disk.** Session 25/09/2026 (product portfolio 15 gaps): cả 3 subagent đều kết luận "xuất JSON ... verified", nhưng **1 file bị file-mutation verifier từ chối** (`danh-muc-nhom-dich-vu.json` — JSON sai cú pháp; lỗi chỉ hiện ở chân summary). Parent đọc disk mới thấy file không tồn tại, phải tự dựng lại 10 dịch vụ từ phần text trong summary. Quy tắc: (a) sau delegation, `read_file` từng file được nhắc tới — đừng tin summary; (b) file JSON bị `write_file` từ chối vì lint fail thì đừng bắt subagent làm lại, tự ghép lại từ dữ liệu đã có trong summary (nhiều subagent nhúng nguyên JSON trong code block). Cùng lớp lỗi với #11 nhưng khác hình thức: #11 là hết iteration, #17 là **báo cáo thành công cho việc đã thất bại**.

18. **Mọi lớp kiểm chứng bằng code phải được test bằng fixture CỐ TÌNH SAI — không thì không biết nó có hoạt động không.** Đây là bài học lớn nhất khi xây deterministic layer (session 25/09/2026, KB luật VN + QA gate output). Một QA gate chạy trên file đúng rồi báo PASS chưa chứng minh được gì — nó có thể pass mọi thứ. Bắt buộc 2 fixture: file sai → FAIL (exit ≠ 0), file đúng → PASS. Ba lỗi sau chỉ lộ ra nhờ fixture sai, không lộ ra khi chỉ test happy path:

    - **Matching quá lỏng làm giả pass lên giả thất bại.** Substring match khiến số hiệu SAI (`78/2024/QH15`) khớp số hiệu ĐÚNG (`98/2024/QH15`) → hệ thống báo OK cho một trích dẫn sai. Sửa: exact-match trước, prefix-match (≥ 8 ký tự, hai bên không bằng nhau) sau.
    - **Chuỗi tiếng Việt có/không dấu không match nhau.** Registry lưu tên không dấu (JSON an toàn), truy vấn của user có dấu → so khớp rỗng → giả định "văn bản không tồn tại". Luôn `strip_diacritics()` ở **cả hai phía** mọi phép so sánh.
    - **Match theo thuộc tính không đặc trưng.** Match tên văn bản theo "năm + cơ quan" (`2024`, `qh15`) khớp nhầm mọi văn bản cùng năm. Loại năm/cơ quan khỏi từ khóa, chỉ match khi có từ khóa riêng.

    **Assert trên exit code, không đọc stdout.** Warning đi ra **stderr** và trả 0; blocking đi ra stderr và trả 1. Đọc stdout rồi kết luận "không chặn" là sai khi thực tế đã chặn — đã dính lỗi này ở case văn bản hết hạn nhưng có bản thay thế.

    **Sau mỗi fix phải chạy lại TOÀN BỘ regression suite**, không chỉ case vừa sửa. Ở đây fix bug substring làm lộ bug match-theo-năm; test đúng 1 case thì bug thứ ba lọt.

    **Viết bảng regression bằng Python `subprocess.run`, không dùng bash `${var%%:*}`.** Ký tự `:` trong số hiệu (`62-MT:2016`) làm bash cắt sai chuỗi → test báo FAIL giả, tưởng code hỏng.

19. **Publish: đừng gọi helper payload bằng `~` khi cwd ở ổ đĩa khác (MSYS/Windows).** Chạy `python ~/AppData/Local/hermes/scripts/make_payload.py ...` từ cwd `D:/Hermes Proj` resolve thành `D:\c\Users\...` → `can't open file ... No such file or directory` (exit 2). Luôn dùng đường dẫn Windows đầy đủ: `python "C:/Users/<user>/AppData/Local/hermes/scripts/make_payload.py" in.html "Title" out.json`. Payload ghi UTF-8 `ensure_ascii=False`; POST bằng `curl --data-binary @payload.json` (urllib bị 403). Sau khi publish luôn fetch lại và kiểm tra dấu tiếng Việt có + mojibake 0 + số `<h1>`/`<section>`/`<table>` khớp bản local.

20. **Quét MÂU THUẪN NỘI BỘ sau mọi lượt sửa hàng loạt — và tự công bố GIỚI HẠN của chính phép verify ngay trong tài liệu.** Hai việc của LỚP BÁO CÁO, không cổng verify/citation nào bắt được (rút ra 18/10/2026, tài liệu `07b` fixgby sau khi áp 67 edit tự động):
    - **Bảng tóm tắt cuối tài liệu thường còn bản CŨ** khi phần thân đã sửa, vì edit chạy từng dòng độc lập. Ca thật: `F.2` trong **cùng một câu** vừa nói "6/6 cạnh có bằng chứng" vừa kết "4/6"; bảng tra nhanh vẫn ghi 4/6 trong khi bảng cạnh `A.4.3` đã thành 5/6; mục kết luận dùng "**đã chứng minh**" cho một vòng xoáy mà chính tài liệu ghi là chưa ai chứng minh.
    - **Checklist 5 bước:** (1) grep mọi con số đếm (`N/M`, `k/N nguồn`, `tag H`) → liệt kê hết chỗ xuất hiện rồi so nhau; (2) đối chiếu bảng tóm tắt cuối vs thân bài theo từng dòng chủ đề; (3) soát **động từ khẳng định** ở phần kết (`đã chứng minh`, `xác nhận`, `rõ ràng`) — chúng thường mạnh hơn mức bằng chứng thật, hạ về `có bằng chứng riêng lẻ` / `chứng minh một phần` / `giả thuyết heuristic`; (4) mọi `tag H` ở thân phải **xuất hiện lại** ở kết luận/bảng cuối — tag H bị mất khi đi qua bảng tóm tắt = che giấu khoảng trống; (5) mục "còn mở / chưa có nguồn" phải liệt kê **đủ** các khoảng trống đã ghi rải rác.
    - **`verified N/N` rất dễ bị đọc thành "tài liệu này đã đúng".** Vì vậy phần validate phải có khối **"GIỚI HẠN CỦA CHÍNH PHÉP VALIDATE NÀY"** nói thẳng nó kiểm cái gì và **không** kiểm cái gì, kèm **danh sách đánh số các chỗ đã sửa** ở lượt QC. Người đọc sau cần biết *cái gì đã kiểm và cái gì chưa*, không chỉ biết "đã verify".
    - Nguyên mẫu khối giới hạn + checklist đầy đủ: skill `pubmed-evidence-research` → `references/citation-attribution-audit.md` §5–§6. Chi tiết cùng lớp lỗi ở dòng số liệu: pitfall #16 ở trên.
