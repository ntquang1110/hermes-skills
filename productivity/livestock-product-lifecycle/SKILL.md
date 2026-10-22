---
name: livestock-product-lifecycle
description: Map livestock life to product lines from a base additive.
version: 1.0.0
author: Hermes Agent (Quang)
license: MIT
metadata:
  hermes:
    tags: [livestock, pig, feed-additive, product-strategy, vua-kiem]
    related_skills: [livestock-trial-protocol, vietnam-herbal-research, kiem-saphia-product-docs, product-brief, dashboard-design-system]
---

# Livestock Product Lifecycle

Use when the user (typically Vua Kiềm / Manna Đất Vàng) wants to design a feed-additive product range that fits a livestock species' full life ("đời con lợn", gà, bò, tôm) — from an existing base product (e.g. EZ80) into stage-specific lines, and/or wants a master product-strategy document.

## Method (reusable across species)

1. **Split the lifecycle by ngày tuổi + khối lượng.** Use the species' real production standard (for pig: cai sữa 21–28d, xuất chuồng ~85–110kg, tổng ~20–24 tuần). Group into discrete stages.
2. **Per stage, list the vấn đề đặc trưng** the animal actually meets (disease, stress, nutritional bottleneck). Not generic — stage-specific (PWD only appears at cai sữa, táo bón + MMA at nái, PSE/DFD at vỗ béo).
3. **List what market products already solve each problem.** Categories: AGP antibiotics, ZnO liều cao, organic acids, probiotic, prebiotic (MOS/FOS/β-glucan), botanicals, enzymes, mycotoxin binders, immunostimulants, vaccines, antioxidants (E/Se), disinfectants, hormones. Note which are banned/being restricted.
4. **Map base product → stage-specific lines.** Keep the base as the "vạn năng" family; split variant lines to hit the highest-pain stage first. For EZ80 the split is Start (cai sữa) > Sow (nái) > Grow (vỗ béo) > Repro (tái phối) + an ASF biosecurity bundle.
5. **Pricing/business model:** shift from "sell a bag" to a lifecycle Stage-Pack sold by head/lứa (head-based), price anchored to feed + vet cost per kg tăng trọng. Use real trial numbers (FCR/ADG/PCR) as the pull.
6. **Expansion 3 tầng:** A. by stage within species → B. by species (heo → gà/bò/tôm) → C. by value (evidence service + feed-mill + farmer network). Only open B once stage-A has evidence + revenue base.

## Regulatory anchor (critical, pig 2026)
- **Vietnam bans antibiotics in feed entirely from 01/01/2026** (Nghị định 211/2026/ND-CP) — both phòng bệnh tập thể and growth promotion. Tailwind for natural additives; it is the main strategic hook to lead with.
- **Claim gate:** all sales material must say only "thức ăn bổ sung". CẤM claim phòng/điều trị. Internal strategy docs may map market needs but never market claims.
- EU banned ZnO liều cao (2022) and ractopamine is banned in VN → these are open-market gaps.

## Delivery rules (learned 14/09/2026 — user corrections, MUST follow)

1. **NO loss / NO cutting when restyling.** When converting design (e.g. IBM Plex theme → newsprint), copy content verbatim and only swap CSS tokens. After restyle, verify by counting: sections present, RFI count, MoSCoW 4 blocks, scorecard rows, competitor rows. Report counts to user.
2. **One product = one full brief.** When user asks for briefs of N products, write EACH product with the full 21-section structure (reference HTML is the checklist). If a product is HOLD/short, say so explicitly in Executive Summary — do not silently shorten.
3. **One agent per product for parallel briefs.** When writing ≥2 product briefs, dispatch one subagent per product (max 3 parallel via delegate_task tasks array). Each agent writes its own HTML file under token limit, can run long. Merge afterwards with a python script. Pattern proven 14/09/2026: 3 agents × ~500s each → Sow/Grow/Repro HTML.
4. **Reference-HTML review gate.** When user provides a reference brief HTML, use it as the review checklist after finishing: every section in the reference must exist in the output. Missing section → DATA GAP or supplement, never skip silently.
5. **Design: newsprint (light mode).** Approved 16/09/2026. Use `references/newsprint-brief-workflow.md` for full design tokens and verification checklist. Key tokens: bg #F9F9F7, Playfair Display + Lora fonts, zero radius, dot grid texture, blockquote 4px solid black, inverted section (#111111 bg, white text, red accent), marquee ticker.

## Product formulation analysis — 5-criteria method

Khi thiết kế công thức sản phẩm (sau khi đã có danh sách hoạt chất), bắt buộc phải phân tích mỗi công thức qua **5 tiêu chí**:

1. **Tương thích (Compatibility):** Các hoạt chất có phản ứng với nhau không? Có tách pha, kết tủa, trung hòa lẫn nhau không? Nếu cần chất hỗ trợ (nhũ hóa, chất mang), ghi rõ.
2. **Ổn định (Stability):** Hạn dùng dự kiến? Điều kiện bảo quản? Yếu tố làm giảm chất lượng (ánh sáng, nhiệt, ẩm, oxy hóa)?
3. **An toàn (Safety):** Tương tác với cơ thể lợn? LD50 tham khảo? Nồng độ gây hại? Cảnh báo cho đối tượng nhạy cảm (heo con <7kg, nái mang thai)?
4. **Hiệu quả (Efficacy):** % giảm bệnh dự kiến? Dẫn chứng (PMID, thực địa, in vitro)? So sánh với giải pháp hiện có?
5. **Rủi ro (Risk):** Side effect cụ thể? Nồng độ không an toàn? Nguy cơ quá liều? Ảnh hưởng đến chất lượng thịt? Khả năng sản xuất (nguyên liệu khan hiếm, thiết bị đặc biệt)?

### Quy tắc formulation (learned 21/09/2026)

1. **Mỗi sản phẩm tối thiểu 2-3 công thức** — không bao giờ chỉ đưa 1. CT.1 = giá rẻ/dễ sản xuất; CT.2 = hiệu quả cao hơn/giá cao hơn. Người đọc (chuyên gia dược) sẽ chọn.
2. **Output ưu tiên Google Sheet** — cấu trúc: (a) tab Hướng dẫn (giới thiệu cấu trúc, ký hiệu, cách chọn CT), (b) tab Danh mục hoạt chất (master table), (c) mỗi sản phẩm 1 tab riêng.
3. **Cột bắt buộc trong tab sản phẩm:** Chất | % pha | Vai trò | Ghi chú (kèm PMID nếu có). Sau đó bảng 5 tiêu chí.
4. **Master table hoạt chất cần cột:** # | Hoạt chất | Nguồn (TN/TH/Cả hai) | Cơ chế chính | Xử lý (MT/FCR/TC/HH/ĐN) | Mức chứng minh | PMID | Giá VNĐ/kg | Ghi chú.
5. **Ký hiệu nguồn:** TN = Thiên nhiên, TH = Tổng hợp, TN+TH = Cả hai.
6. **Mức chứng minh:** Mạnh (in vivo lợn, có đối chứng), Vừa (in vitro hoặc trên chuột), Yếu (sơ khởi).
7. **Tên sheet = tiếng Việt có dấu, dễ hiểu.** Không dùng tiếng Anh. Ví dụ: "A1 — Sát khuẩn không khí" thay vì "A1-KhongKhi".
8. **Hướng dẫn đọc (guide sheet):** tab đầu tiên, ngắn gọn, dành cho chuyên gia dược. Nội dung: cấu trúc sheet, cách đọc tab sản phẩm, cách chọn công thức, ký hiệu.

## Pitfalls
- Don't let one formula cover every stage if the user is expanding — propose the split even if it costs extra RFI.
- Evidence first: need real FCR/ADG/PCR before selling to large farms; numbers are the moat, not the promise.
- QC consistency (seasonal botanical variation) breaks replicable trial results — flag it.
- Don't open too wide (pig + poultry + cattle + shrimp at once); stagger by evidence.
- **Div balancing when merging agent HTML outputs.** Subagent HTML files may have unbalanced <div> tags (e.g. 101 opens / 102 closes). When merging into a single HTML with tabs, unbalanced divs cause tag content to bleed into adjacent tabs. Always run a balance_divs() function on each content fragment before inserting into the template. Verify each tab id appears exactly once (grep id=tab-X).
- **Subagent iteration budget — use leaf role for brief writing.** When dispatching subagents to write product briefs, use role=leaf (default), NOT role=orchestrator. Leaf agents focus purely on writing and publish in ~500-600s. Orchestrator agents consume extra iterations on delegation overhead and risk hitting max_iterations (~800s budget) before writing the output file. Verified 17/09/2026: orchestrator RESP-HP failed at 797s; leaf METRI-HP succeeded at 573s.
- **Keep subagent context focused.** When passing brief-writing instructions to a subagent, put ingredient proposals, disease data, and design tokens directly in the context rather than expecting the subagent to research from scratch. Every web search turn consumes iteration budget. Verified pattern: give enough context for one write+publish cycle, not a research+write+publish cycle.
- **Skill product-brief is user-owned (not curator-managed).** If it needs updates, recommend hermes curator adopt product-brief first, then patch. Content from it is referenced here; keep this skill as the primary umbrella for livestock strategy docs.
- **Vietnamese diacritics: MUST be present on ALL Vietnamese text in every output.** User explicitly corrected this (16/09/2026). Every HTML board, brief, table, and card must have full Vietnamese diacritics. Review before publishing: scan for text missing accents and fix before delivering. This applies to section headers, table cells, card text, buttons, and metadata. Only acronyms (EZ80, FCR, ADG, ASF, PRRS, PMID, AI, R&D) and proper brand names (GreenFeed, CP, Biomin, Kemin) may stay undiacriticized.
- **When building cost-structure boards**, use references/pig-farming-cost-structure.md as the reference data source. The pattern: timeline flow diagram -> per-stage cost tables -> total cost summary -> competitor product comparison -> source classification (FACT/EVIDENCE/INFERENCE/ESTIMATE). Always cite sources with URL and confidence level.
- **Lab equipment: start minimal, iterate.** When planning lab/R&D equipment, propose the cheapest working option first (notre ~20tr cho chiết xuất cơ bản). User will correct if too basic or too complex. Pattern: minimal viable setup -> user feedback -> add if needed. Don't jump to rotavap/sắc ký cột/đông khô without user asking.
- **Pathogen-disinfectant matrix research methodology.** When researching livestock pathogens and disinfectants, follow: (1) list ALL pathogens with structure (envelope/Gram/cell wall/size/pH sensitivity), (2) list market products that kill each one, (3) map kill mechanism (how and why), (4) estimate cost per application, (5) build a pH-sensitivity matrix, (6) identify the intersection/gap. Use dual parallel subagents: one for pathogen data (PubMed + Wikipedia), one for disinfectant data (PubMed + vendor pricing). Build output as HTML matrix table. Reference: `references/swine-pathogen-disinfection-matrix.md`.
- **Cost comparison: compute per-farm-cycle, not per-unit.** Translate unit prices (VND/kg) into per-cycle cost for a standard 1000-head farm (~1100m2 floor). NaOH and glutaraldehyde+QAC are similar cost (~200-400k/cycle). Factor in labor, PPE, corrosion, and re-application frequency.

## Livestock Product Brief Factory (adapted from saphia-product-brief-factory)

Dùng khi cần viết brief phát triển sản phẩm chăn nuôi (TĂCN/thức ăn bổ sung) trên nền Kiềm Saphia (EZ80/EZ67/nguyên liệu Kiềm Khoáng Thảo Mộc). Điều chỉnh từ khung TPBVSK người sang TĂCN lợn.

### Điều chỉnh từ saphia-product-brief-factory

| TPBVSK người | TĂCN chăn nuôi lợn |
|---|---|
| Kênh MLM Saphia | Kênh B2B: hộ nhỏ / trại vừa / trại kín |
| Cảm nhận 2-4 tuần | Chỉ số đo: FCR, ADG, tỷ lệ tiêu chảy, PCR ASF |
| NĐ 15/2018 + NĐ 342/2025 (TPBVSK) | NĐ 211/2026/ND-CP (cấm AGP) + Luật Thú y + TCCS TĂCN |
| Claim: "Hỗ trợ cải thiện/duy trì" | Claim: "Thức ăn bổ sung", CẤM phòng/điều trị |
| pH máu là pseudoscience | pH>12 uống trung hòa acid dạ dày heo con (giảm tiêu hóa protein) — CẢNH BÁO |
| Giá: ~1,2-1,7 tr đ/tháng/khách | Giá: ~1,5-1,8 tr đ/10kg, trộn 0,5% TĂ |
| Retention: tái mua hàng tháng | Retention: trộn cám liên tục theo lứa |

### Output format (bắt buộc khi viết brief HTML)

- **Design:** newsprint (light mode). Xem `references/newsprint-brief-workflow.md` cho đầy đủ design tokens. Tóm tắt: bg #F9F9F7, Playfair Display (headings) + Lora (body) + Inter (UI) + JetBrains Mono (data), zero border radius, dot grid texture, blockquote 4px solid black, hard shadow hover, inverted section (#111111), marquee ticker.
- **Preserve content tuyệt đối:** khi đổi style từ theme này sang theme khác, giữ nguyên toàn bộ nội dung (số liệu, bảng, RFI, scorecard, câu hỏi). KHÔNG cắt bớt chữ, không gộp section làm mất detail. Nếu không đủ chỗ, kéo dài HTML chứ không rút gọn.
- **Publish:** luôn publish qua skill `publish` (KV backend, preview.thefirstonly.com). Verify bằng curl hoặc browser trước khi báo done.
- **Skill chuyên biệt:** skill `product-brief` (user-owned, created 14/09/2026) chứa framework 21-section riêng cho TĂCN. Tham chiếu khi cần viết brief đầy đủ. Tên cũ: livestock-product-brief-factory — đã đổi thành product-brief theo yêu cầu.

### Cấu trúc brief (21 phần, rút gọn theo mức độ ưu tiên)

Bắt buộc (MUST) cho mọi brief:
1. **Executive Summary** — kết luận 1 dòng (GO/NO-GO + hero door) + 5-7 kết luận cốt lõi + 3 điều KHÔNG được làm + điều kiện tiên quyết
2. **Quy mô vấn đề** — dịch tễ bệnh lợn VN (tỷ lệ mắc, thiệt hại), TAM/SAM/SOM
3. **Segment khách hàng** — hộ nhỏ (<10 con), trang trại vừa (10-500), trại lớn kín (500+)
4. **Pain & JTBD** — functional/emotional/social + insight mua hàng thật
5. **Cạnh tranh** — bảng đối thủ chính (ZnO, AGP, acid hữu cơ, probiotic, prebiotic, thảo dược)
6. **Đối chiếu nền tảng Kiềm** — 5 câu hỏi bắt buộc (xem platform-rules trong saphia-product-brief-factory)
7. **Công thức MoSCoW** — MUST/SHOULD/COULD + bảng thẩm định thành phần + liều
8. **Pháp lý & giới hạn công bố** — bảng ngôn ngữ được/không được
9. **Lộ trình G1-G7 & 90 ngày**
10. **Devil's Advocate & Risk Mitigation**

### Đối chiếu nền tảng Kiềm Thảo Dược cho chăn nuôi (bắt buộc)

Khác với TPBVSK người, Kiềm Thảo Dược trong chăn nuôi lợn có vai trò thật:

| Câu hỏi | Kết luận |
|---|---|
| Có bằng chứng gì cho cơ chế này? | Kiềm khoáng (Ca/Na/K/Mg) + thảo dược (Xạ đen, Hoàn ngọc, Tía tô, Chè dây) có bằng chứng hỗ trợ tiêu hóa, kháng viêm, điện giải. Thảo dược từ research nội bộ 4 loại (PMID verified). |
| Claim nào có bằng chứng, claim nào marketing? | Có: ổn định pH ruột non (heo con pH ruột ~6-7.5). Cảnh báo: pH>12 uống trung hòa acid dạ dày, giảm pepsin, giảm tiêu hóa protein — phải hạ pH hoặc phối liều đúng. |
| Vai trò thật của Kiềm Thảo Dược? | Hệ dẫn khoáng + thảo dược sinh khả dụng cao; bù điện giải khi tiêu chảy; ổn định pH ruột non. pH>12 chỉ dùng ngoài (Virusto). |
| pH thành phẩm có phá hủy hoạt chất? | Tannin, berberine, butyrate đều ổn định ở pH 7-9. pH>12 có thể thủy phân butyrate và một số thảo dược — cần tách pha hoặc hạ pH. |
| Bột khô thì sao — khoáng Ca/K có làm đổi pH tổng không? | **Bột khô KHÔNG có pH** (pH chỉ định nghĩa khi có dung dịch) nhưng **không có nghĩa là không phản ứng**. Khoáng dạng oxide/hydroxide tự hút ẩm từ không khí, tạo màng nước siêu mỏng ở **pH 11–12,5** — đúng các phản ứng của bảng chất chuẩn xảy ra ở đó, chỉ khác quy mô (vi điểm). Bốn dòng bột (RS/GT/GR/GS) phải đánh giá theo **nước hoạt động aw (< 0,6)**, không phải pH; bảng chất chuẩn pH 8–9 hiện tại **chỉ đúng cho dòng nước (MT-01)**. Enzyme trong bột hỏng vì **aw**, không phải vì pH. Xem `references/dry-blend-vs-aqueous-stability.md`. |
| Có rủi ro an toàn? | Kali với heo con CKD không phải vấn đề chính. Nguy cơ chính: pH>12 làm giảm hiệu quả tiêu hóa nếu uống trực tiếp. |

### Nguồn tham khảo
- `references/pig-disease-vietnam.md` — knowledge bank bệnh lợn VN (data từ research 14/09/2026)
- `references/pig-lifecycle-map.md` — lifecycle map + EZ80 expansion
- saphia-product-brief-factory references: `platform-rules.md`, `framework-structure.md`, `cross-cutting-rules.md`

## Files
- `references/market-gap-to-product-portfolio.md` — **Từ market gap → product portfolio** (kiểm chứng 10/2026, 15 gap → 21 SKU): chia 3 nhóm TRONG/NGOÀI/DỊCH VỤ theo bản chất can thiệp; 6 trường bắt buộc mỗi SKU (tên, công dụng, thành phần, cơ chế, đơn giá, **fit nguồn lực**); ràng buộc chéo giữa các nhóm (pH uống/ăn, claim TĂBS, hóa chất sát trùng = thuốc thú y); thứ tự ưu tiên theo điều kiện pháp lý; 6 pitfalls (giấu điều kiện đăng ký, không chia giai đoạn, chạy COGS quá sớm). Dùng khi khách hỏi "danh mục sản phẩm nên gồm gì / làm cái nào trước".
- `references/pig-lifecycle-map.md` — full pig map (thịt 4 giai đoạn + nái 6 giai đoạn), market-product groups, EZ80 expansion lines. Use as the concrete worked example.
- `references/pig-disease-vietnam.md` — knowledge bank bệnh lợn VN (verify 14/09/2026): tỷ lệ mắc từng bệnh, thiệt hại kinh tế, chi phí xử lý, quy mô thị trường, nguồn chính, hướng sản phẩm EZ80-Start/Sow/ASF + pitfalls fetch nguồn VN (danviet utf-16 byte-swap, nhachannuoi 502). Dùng khi cần bản đồ bệnh + chi phí để định hướng sản phẩm.
- `references/newsprint-brief-workflow.md` — design tokens, content structure, duplicate detection pattern, design verification checklist, and parallel generation workflow for livestock product briefs. Bắt buộc đọc khi viết brief HTML mới.
- `references/mma-sow-product-formula.md` — MMA (Metritis-Mastitis-Agalactia) product formula knowledge bank. Thành phần, liều, cơ chế, lưu ý kỹ thuật dạng nước trên EZ67 base cho sản phẩm hỗ trợ nái sau đẻ. Dùng khi thiết kế sản phẩm mới cho nái hoặc tham chiếu công thức METRI-HP (MT-01).
- `references/formula-variants-rd-planning.md` — Formula variant matrix template + worked example (5 product lines, 23 formulas). Dùng khi user yêu cầu R&D direction cùng brief: tạo bảng biến thể công thức (3-5 CT/dòng) + tiêu chí sàng lọc G1-G3 + ngân sách tham chiếu.
- `references/ngoai-biosecurity-portfolio.md` — Nhóm NGOÀI (vệ sinh/sát trùng/môi trường, G2+G3+G4+G10+G14): luật 2 đường pháp lý TCCS-vs-OEM/GMP, quy tắc ASFV×pH×hữu cơ (PMID 29778187/40006911), súc ống 2 pha (PMID 42774681), Yucca/NH3 (PMID 34368272/16825449), hiểu chỉnh QĐ 779 + NĐ 06, portfolio 6+2 và thứ tự triển khai. Dùng khi thiết kế sản phẩm ngoài chuồng trại trên nền kiềm #41442.
- `references/swine-pathogen-disinfection-matrix.md` — Swine pathogen structure (10 viruses + 12 bacteria), envelope/Gram/cell wall, pH sensitivity at which each is inactivated, high-pH (NaOH/CaOH2) kill mechanism, cost comparison, and universal disinfection protocol. Dùng khi cần ma trận tác nhân gây bệnh heo + cơ chế diệt chung.
- `references/vn-feed-additive-suppliers.md` — **NCC nguyên liệu TĂCN VN đã verify (10/2026)**: Dalosa (thymol 99%, có SĐT + MST), Kim Mã (Betaine HCl 98%), Hóa chất Bách Khoa (L-Tryptophan 98% Ajinomoto/CJ/Evonik), Ánh Dương Khang (Silvafeed tannin Ý, ≥75%), ICFOOD (enzyme Angel Yeast — **phải hỏi dạng coated**), Acare (β-glucan). Kèm nhóm nhập khẩu (Vitamin E TPGS, glycyrrhizin, SAP, Mg chelate), nhóm tự chiết tại lab (lá hẹ, huyết dụ), phương pháp tra NCC ngành (từ khoá TV hiệu quả hơn EN; tra theo tên thương mại của hàng nhập thì mới ra nhà phân phối VN), và cách xếp ưu tiên mua để **tối thiểu hoá số món mở khoá nhiều công thức**.
- `references/dry-blend-vs-aqueous-stability.md` — **Bột khô vs dung dịch: đánh giá bằng aw, không phải pH.** Khoáng oxide/hydroxide hút ẩm → màng nước vi điểm pH 11–12,5; ba cơ chế vẫn chạy trong bột khô (aw, phản ứng xúc tập, acid-base rắn — calcium ascorbate từ CN1112418A); phân loại yên tâm/theo dõi; bảng đổi trục pH → aw (< 0,6) cho bốn dòng bột; 3 câu hỏi phải hỏi user; khung trả lời 6 bước. Dùng khi user hỏi về ổn định/tương tác hoạt chất trong thành phẩm bột.