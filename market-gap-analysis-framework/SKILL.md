---
name: market-gap-analysis-framework
description: "Use when: finding unmet market gaps in an industry."
version: 1.0.0
author: Nguyễn Thành Quang / Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [research, market-gap, strategy, industry-analysis, white-space, competitive-analysis, b2b]
    category: research
    related_skills: [research-overview, research-reporting, web-research, grounded-citations, pubmed-evidence-research]
---

# Market Gap Analysis Framework

## Tổng quan: Tư duy xương sống

File tham chiếu: `VuaKiem_Market_Gap_Chan_Nuoi_Lon_2026.html`

**Nguyên lý #1 — Problem-first, không solution-first.**
Xác định vấn đề kinh tế lớn, chưa được giải quyết tốt — trước khi xét công nghệ/công ty. Nếu bắt đầu bằng "công ty có công nghệ X, bán cho ai?" là sai ngay bước 0.

**Nguyên lý #2 — Evidence hierarchy trên mọi số liệu.**
Mỗi claim quan trọng gắn tag: F (Fact — số liệu nhà nước/doanh nghiệp), E (Evidence — nghiên cứu khoa học/khảo sát), I (Expert interpretation), H (Hypothesis — cần validate), INT (International — không đại diện VN). Đây không phải trang trí — nó quyết định độ tin cậy của toàn bộ kết luận.

**Nguyên lý #3 — Segmentation trước khi nói "thị trường".**
Không có "thị trường chăn nuôi lợn". Có 4 nhóm trại khác nhau về bản chất: quy mô, hành vi mua, người quyết định, pain point. Một giải pháp không thể phủ cả 4.

**Nguyên lý #4 — Từ pain → systemic chain → gap → score → strategy.**
Không nhảy từ "có vấn đề" đến "đây là cơ hội". Phải qua: pain map → causal chain → gap definition → scoring → deep dive → strategy.

**Nguyên lý #5 — Validation plan trước khi đầu tư.**
Mọi gap có giả thuyết giá trị. Mỗi giả thuyết phải có: phương pháp validate, ngưỡng GO, kill criteria. Nếu không thể kill được — đó không phải giả thuyết, là tuyên bố.


## Pipeline: 6 phases, 16 outputs

| Phase | Sections | Outputs |
|-------|----------|---------|
| 0. Setup | Scope, constraints | Project brief, evidence legend |
| 1. Data & Segmentation | S1, S2, S14 | Industry fact sheet, 4-segment table, data contradictions |
| 2. Pain & System | S3, S4 | Pain map (26+ pts), causal chains, intervention points |
| 3. Gaps & Scoring | S5, S6 | 15 market gaps, weighted scorecard, strategic map |
| 4. Deep Dive | S7, S8, S11 | 16-point analysis of top 6, Why Now matrix, competitor blind spots |
| 5. Strategy | S9, S10, S12, S13 | Entry strategy, hero product, strategic map, validation plan |
| 6. Assembly | Report | HTML with all sections, evidence tags, references |


## Phase 0: Project Setup

### Output: Project brief + Evidence legend

**Làm sao ra:**
1. Xác định ngành, địa lý, thời gian (vd: chăn nuôi lợn VN 2026-2030)
2. Xác định phạm vi sản phẩm (vd: lợn thịt, không gồm nái)
3. Xác định ràng buộc (công nghệ hiện có, năng lực, vốn)
4. Tạo evidence legend với 5 tag F/E/I/H/INT — giải thích từng tag

**QA:**
- Phạm vi phải rõ đến mức có thể trả lời "có/không" cho một chủ đề có thuộc phạm vi không
- Ràng buộc viết thành bullet, không viết đoạn


## Phase 1: Data Foundation (Industry Scan)

### Output 1.1 — Industry Fact Sheet (S1)

**Output là gì:** Bảng 15-20 chỉ số ngành, mỗi chỉ số có: tên, giá trị, thời điểm, loại bằng chứng (F/E/I/H/INT), nguồn (link).

**Làm sao ra:**
1. Xác định 6 nhóm dữ liệu cần:
   - Quy mô thị trường (tổng đàn, sản lượng, giá trị)
   - Cơ cấu ngành (phân khúc, tỷ trọng DN vs hộ)
   - Giá cả & chi phí (giá sản phẩm, giá thành, biên)
   - Dịch bệnh & rủi ro (số ổ dịch, thiệt hại)
   - Pháp lý (quy định mới, lộ trình)
   - Nhập khẩu & phụ thuộc (nguyên liệu, phụ gia)
2. Thu thập từ 3 loại nguồn:
   - Báo chí/ tin tức (VnEconomy, Báo Chính phủ, pig333)
   - Nghiên cứu khoa học (PubMed, Sciencedirect)
   - Báo cáo thương mại (Mordor Intelligence, công ty chứng khoán)
3. Tag mỗi số liệu bằng evidence tag
4. Ghi nguồn cụ thể (URL, PMID, tên báo cáo)

**QA:**
- Ít nhất 15 chỉ số, mỗi chỉ số có nguồn
- Tối đa 3 chỉ số ở mức H (hypothesis) — nếu nhiều hơn, báo cáo quá yếu
- Mỗi nguồn là link click được hoặc PMID
- Không có "theo các chuyên gia" — phải ghi tên cụ thể hoặc tổ chức

### Output 1.2 — Data Contradictions & Gaps (S14)

**Output là gì:** Bảng các số liệu mâu thuẫn giữa các nguồn, giải thích tại sao khác nhau, và danh sách dữ liệu chưa tìm được.

**Làm sao ra:**
1. Trong quá trình thu thập S1, ghi lại mọi chỗ hai nguồn cho số khác nhau
2. Với mỗi mâu thuẫn: tìm nguyên nhân (khác thời điểm? khác định nghĩa? khác phương pháp?)
3. Liệt kê dữ liệu quan trọng không tìm được từ nguồn công khai

**QA:**
- Mỗi mâu thuẫn có diễn giải tại sao, không chỉ đặt hai số cạnh nhau
- Dữ liệu chưa tìm được phải cụ thể (không "thiếu dữ liệu chung chung")
- Phần này là input cho validation plan (Phase 5)


## Phase 2: Customer Segmentation & Pain Mapping

### Output 2.1 — Segment Table (S2)

**Output là gì:** Bảng 4-5 nhóm khách hàng, mỗi nhóm 8-10 thuộc tính: pain point chính, economic loss, hành vi mua, người quyết định, giải pháp hiện tại, unmet need, willingness to pay, rào cản, market gap nổi bật.

**Làm sao ra:**
1. Xác định tiêu chí phân nhóm (quy mô, mô hình kinh doanh, kênh bán)
2. Với mỗi nhóm, trả lời 8 câu hỏi:
   - Pain point chính là gì? (3-5 cái)
   - Thiệt hại kinh tế điển hình? (số cụ thể hoặc H)
   - Họ mua như thế nào? (ai quyết định, ai dùng, kênh nào)
   - Giải pháp hiện tại là gì?
   - Unmet need thật sự?
   - Chịu trả bao nhiêu? (thấp/trung bình/cao)
   - Rào cản gia nhập?
   - Gap nào nổi bật nhất?

**QA:**
- Tiêu chí phân nhóm phải rõ ràng (không mập mờ)
- Mỗi nhóm có economic loss bằng số (dù là H)
- Cột "hành vi mua" phải phân biệt economic buyer vs user
- Xu hướng của mỗi nhóm (đang tăng/giảm) được ghi rõ

### Output 2.2 — Pain Map (S3)

**Output là gì:** Dọc theo chuỗi giá trị, liệt kê 20-30 pain point. Mỗi pain point có: khâu trong chuỗi, pain cụ thể, economic impact (kèm bằng chứng), giải pháp hiện tại, unmet need.

**Làm sao ra:**
1. Vẽ chuỗi giá trị từ đầu đến cuối (vd: giống → nhập heo → sau cai sữa → grower → finisher → xuất chuồng)
2. Tại mỗi khâu, brainstorm 2-5 pain point
3. Mỗi pain point cần economic impact bằng số (F/E/H)
4. Mỗi pain point có giải pháp hiện tại (dù tệ)
5. Mỗi pain point có unmet need — câu "giá như có..."

**QA:**
- Ít nhất 20 pain point
- Mỗi pain có economic impact (dù là H)
- Không có pain nào unmet need = "không có giải pháp" — luôn có giải pháp hiện tại, dù không hiệu quả
- Các pain ở ngoài phạm vi được đánh dấu rõ (oos)


## Phase 3: Systemic Analysis

### Output 3.1 — Causal Chains (S4)

**Output là gì:** 2-3 chuỗi nhân quả dạng A → B → C → D, với điểm can thiệp giá trị nhất được đánh dấu.

**Làm sao ra:**
1. Từ pain map, chọn các pain có quan hệ nhân quả
2. Sắp xếp theo thứ tự: nguyên nhân gốc → trung gian → hậu quả
3. Xác định điểm can thiệp: chỗ nào trong chuỗi nếu tác động sẽ phá vỡ toàn chuỗi
4. Với mỗi điểm can thiệp, trả lời: hiện thị trường đang bán gì ở điểm này, thiếu gì

**QA:**
- Mỗi chain có ít nhất 5 mắt xích
- Điểm can thiệp được khoanh rõ
- Phải có câu "khoảng trống" cho mỗi chain (thị trường đang thiếu gì)
- Các chain phải KHÁC nhau về cơ chế


## Phase 4: Market Gap Generation & Scoring

### Output 4.1 — 15 Market Gaps (S5)

**Output là gì:** Bảng 15 gap. Mỗi gap có: tên theo format "Thiếu [X] cho [Y] để [Z]", customer, pain, economic impact, current solution, unmet need, competition level, opportunity level.

**Làm sao ra:**
1. Từ pain map + unmet need + systemic intervention points, brainstorm gaps
2. Format mỗi gap: "Thiếu [sản phẩm/dịch vụ] cho [đối tượng] để [kết quả mong muốn]"
3. Với mỗi gap: xác định customer, pain gốc, economic impact, current solution, unmet need
4. Sơ bộ đánh giá competition (đông/ít/trống) và opportunity (cao/trung bình/thấp)

**QA:**
- Format tên gap chuẩn: "Thiếu [X] cho [Y] để [Z]" — không lệch
- Mỗi gap có ít nhất 1 pain trong pain map làm gốc
- Không gap nào là "làm một cái app" — phải gắn với pain kinh tế
- Có thể có gap ở nhiều mức (product/service/business model)

### Output 4.2 — Gap Scoring (S6)

**Output là gì:** Bảng xếp hạng 15 gap theo 4 tiêu chí có trọng số. Điểm 1-5. Trọng số: Market Attractiveness 35%, Competitive White Space 25%, Company Fit 20%, Execution 20%. Kèm phân loại (Enter/Build/Defend/Explore).

**Làm sao ra:**
1. Xác định 4 tiêu chí con cho mỗi nhóm:

   **Market Attractiveness (35%):**
   - Quy mô thị trường (TAM/SAM)
   - Tăng trưởng
   - Urgency (có driver pháp lý/thời vụ không)
   - Economic pain (thiệt hại bằng số)

   **Competitive White Space (25%):**
   - Số lượng đối thủ
   - Mức độ đáp ứng nhu cầu hiện tại
   - Khoảng trống khác biệt hóa

   **Company Fit (20%):**
   - Công nghệ hiện có
   - Năng lực sản xuất
   - Kênh phân phối

   **Execution (20%):**
   - Time to market
   - Rào cản gia nhập
   - Scalability

2. Chấm điểm 1-5 cho mỗi tiêu chí con, tính trung bình nhóm
3. Tính tổng có trọng số
4. Phân loại: Enter (≥3.5 và Fit ≥3.5), Build (≥3.0, Fit thấp hơn), Defend (Market cao nhưng khó khác biệt), Explore (còn quá sớm)

**QA:**
- Điểm là công cụ xếp hạng, không thay thế phân tích định tính
- Fit chỉ được chấm sau khi gap đã xác định độc lập
- Ghi rõ mỗi điểm là I (expert interpretation)
- Nếu gap có Market Attractiveness cao nhưng xếp cuối — phải giải thích tại sao (vd G11)


## Phase 5: Deep Dive Top Gaps

### Output 5.1 — 16-Point Analysis (S7)

**Output là gì:** Cho mỗi gap trong top 5-6, phân tích 16 điểm:
1. Problem (vấn đề cụ thể)
2. Customer (economic buyer + user)
3. Economic loss (bằng số)
4. Why current solutions fail (tại sao giải pháp hiện tại không đủ)
5. Market gap (câu chuẩn "Thiếu X cho Y để Z")
6. White space (tại sao đây là khoảng trống)
7. Potential solution (mô tả giải pháp)
8. Product/service (cụ thể bán gì)
9. Business model (bán thế nào, giá bao nhiêu)
10. Competitive landscape (ai đang làm, ai chưa làm)
11. Regulatory barrier (cao/trung bình/thấp + lý do)
12. Company fit (cao/trung bình/thấp + rủi ro kỹ thuật)
13. Entry barrier (thấp/cao để vào, thấp/cao để thắng)
14. Time to market (tháng)
15. Scalability (cao/trung bình/thấp + logic)
16. Key risks (3-5 cái)

**Làm sao ra:**
1. Chọn top 5-6 gap từ scoring
2. Cho mỗi gap, research sâu từng điểm
3. Điểm 1-5: từ pain map + phỏng vấn/desk research
4. Điểm 6 (white space): từ competitor analysis + competitive landscape
5. Điểm 7-9: brainstorm solution độc lập (chưa gắn công ty)
6. Điểm 10-16: đối chiếu với năng lực thực tế

**QA:**
- Mỗi gap có ít nhất 3 điểm có số liệu F hoặc E
- Điểm 4 (why current solutions fail) phải cụ thể, không "không ai làm"
- Điểm 16 (key risks) phải có ít nhất 3 risks thật, không risks giả
- Nếu gap có regulatory barrier cao — ghi rõ bước cần làm
- Economic loss phải bằng số (dù H) — không "thiệt hại lớn"


### Output 5.2 — Why Now Matrix (S8)

**Output là gì:** Ma trận 9-12 driver × 6 gap. Mỗi ô đánh giá mức độ tác động (●●●/●●/●/–). Kèm bằng chứng cho mỗi driver.

**Làm sao ra:**
1. Xác định 9-12 driver bên ngoài (pháp lý, dịch bệnh, thị trường, công nghệ, khí hậu...)
2. Mỗi driver có bằng chứng (F/E/H)
3. Với mỗi gap, đánh giá driver đó có tạo urgency không
4. Tổng hợp: gap nào có nhiều ●●● nhất là cơ hội timing tốt nhất

**QA:**
- Mỗi driver có ít nhất 1 bằng chứng
- Driver phải là sự kiện/thay đổi thực tế, không phải xu hướng mơ hồ
- Timing analysis phải trả lời: "tại sao bây giờ, không phải 3 năm trước hay 3 năm sau"

### Output 5.3 — Competitor Blind Spots (S11)

**Output là gì:** Bảng 8-10 nhóm đối thủ. Mỗi nhóm: ví dụ, đang giải quyết vấn đề gì, chưa giải quyết gì (blind spot).

**Làm sao ra:**
1. Phân loại đối thủ theo nhóm (không theo từng công ty)
2. Mỗi nhóm: xác định họ đang bán gì, cho ai
3. Blind spot = cái họ không làm hoặc không thể làm vì cấu trúc kinh doanh
4. Phân biệt: blind spot vì không muốn vs blind spot vì không thể

**QA:**
- Mỗi blind spot phải có lý do (cấu trúc kinh doanh, kênh phân phối, đối tượng khách hàng)
- Không chê đối thủ "không biết làm" — phân tích khách quan
- Blind spot của đối thủ = cơ hội cho mình


## Phase 6: Strategy

### Output 6.1 — Entry Strategy (S9)

**Output là gì:** Ma trận 3 Option (Product / Solution / Platform) cho mỗi gap. Khuyến nghị chọn option nào.

**Làm sao ra:**
1. Với mỗi gap, xác định 3 mức:
   - Product: bán một SKU
   - Solution: SKU + protocol/procedure
   - Platform: solution + dịch vụ + dữ liệu
2. Đánh giá: mức nào khả thi nhất (time to market, năng lực, rào cản)
3. Khuyến nghị: Option A/B/C và lộ trình (vd B ngay, C từ năm 2)

**QA:**
- Option A phải là bước nhỏ nhất có thể bắt đầu
- Option C phải là tầm nhìn 2-3 năm, không phải mơ mộng
- Mỗi option phải realistic về năng lực hiện tại

### Output 6.2 — Hero Product Opportunity (S10)

**Output là gì:** Bảng so sánh các gap theo 9 tiêu chí: customer, pain, job-to-be-done, desired outcome, value proposition, proof of efficacy cần có, KPI farm đo được, reason to believe, competitive differentiation.

**Làm sao ra:**
1. Chọn 4-6 gap cho bảng hero
2. Mỗi gap: điền 9 ô
3. Job-to-be-done phải là câu nói của khách hàng (trích dẫn giả định)
4. KPI phải là thứ chủ trại có thể đo được, không phải thứ phòng lab mới đo được

**QA:**
- Job-to-be-done là câu ngắn, như khách hàng nói (vd "Giúp tôi qua 4 tuần đầu mà không mất con")
- Proof of efficacy phải cụ thể (pilot đa trại, đối chứng, bên thứ ba)
- Reason to believe không được là "chúng tôi tin" — phải có cơ sở kỹ thuật

### Output 6.3 — Strategic Opportunity Map (S12)

**Output là gì:** Biểu đồ scatter (Market Attractiveness × Ability to Differentiate) với 15 bubble, chia 4 góc: Enter / Build / Defend / Explore. Kèm chú thích.

**Làm sao ra:**
1. Trục X: Market Attractiveness (từ scoring)
2. Trục Y: Ability to Differentiate = avg(White Space, Company Fit)
3. Kích thước bubble: Economic value/market potential
4. Vẽ SVG hoặc dùng CSS grid

**QA:**
- 4 góc phải có nhãn rõ
- Kích thước bubble phản ánh đúng quy mô cơ hội
- Các bubble không chồng lấn

### Output 6.4 — Validation Plan (S13)

**Output là gì:** Bảng 5-7 câu hỏi cần validate. Mỗi câu hỏi: phương pháp, ngưỡng GO, kill criteria. Kèm timeline.

**Làm sao ra:**
1. Từ các giả định H trong toàn bộ báo cáo, chọn 5-7 quan trọng nhất
2. Mỗi giả định: thiết kế phương pháp kiểm chứng
3. Xác định ngưỡng GO (số cụ thể) và kill criteria (số cụ thể)
4. Sắp xếp theo thứ tự ưu tiên

**QA:**
- Mỗi câu hỏi phải có kill criteria — nếu không kill được thì không phải giả thuyết
- Ngưỡng GO và kill criteria phải là số hoặc % cụ thể
- Timeline phải thực tế (không 90 ngày cho pilot 2 lứa nếu 1 lứa 6 tháng)


## Phase 7: Report Assembly & QA

### Evidence Tag System (bắt buộc cho mọi số liệu quan trọng)

```html
<span class="tag F">F</span> — Fact: số liệu cơ quan nhà nước/doanh nghiệp công bố
<span class="tag E">E</span> — Evidence: nghiên cứu khoa học/khảo sát thực địa
<span class="tag I">I</span> — Expert interpretation: diễn giải chuyên gia
<span class="tag H">H</span> — Hypothesis: giả thuyết/mô hình cần validate
<span class="tag INT">INT</span> — International evidence: không đại diện Vietnam
```

### HTML Structure

File HTML tự đứng một mình (single-file), không phụ thuộc external resources.

```
header.hero — kicker + title + description + date + evidence legend
nav.toc — mục lục với anchor links
S0 — Executive Summary (trả lời 7 câu hỏi chiến lược) + KPI grid
S1 — Industry Fact Sheet (bảng)
S2 — Segment Table
S3 — Pain Map (bảng)
S4 — Causal Chains (flow diagrams)
S5 — 15 Market Gaps (bảng)
S6 — Gap Scoring (bảng có trọng số + xếp hạng)
S7 — Deep Dive TOP 6 (mỗi gap 1 deep div với 16-point KV)
S8 — Why Now Matrix (bảng)
S9 — Entry Strategy (ma trận Option A/B/C)
S10 — Hero Product Opportunity (bảng 9 tiêu chí)
S11 — Competitor Blind Spots (bảng)
S12 — Strategic Opportunity Map (SVG scatter)
S13 — Kết luận + Validation Plan (bảng)
S14 — Data Contradictions & Gaps (bảng)
S15 — References (ol với links)
footer
```

### CSS Components cần có

| Component | Mô tả |
|-----------|-------|
| `.kpi` | Stats card: số to + label nhỏ |
| `.card` | Content card: border + padding |
| `.callout` | Alert box: left border colored |
| `.callout.warn` | Red alert |
| `.callout.gold` | Yellow alert |
| `.deep` | Deep dive section: border + padding |
| `.tbl` | Table wrapper (overflow-x:auto) |
| `table` | Striped, sticky header |
| `.tag.F/E/I/H/INT` | Evidence badges |
| `.q-enter/build/defend/explore` | Quadrant badges |
| `.chain` | Causal chain: flex row |
| `.kv` | Key-value grid (2-column) |
| `.grid2/.grid3` | Responsive grid |
| `.oos` | Out-of-scope opacity |
| `.score-hi` | Highlight highest score |

CSS phải có dark mode (prefers-color-scheme + data-theme attribute).

### QA Checklist (chạy trước khi publish)

**Toàn bộ report:**
- [ ] Mọi claim quan trọng có evidence tag (F/E/I/H/INT)
- [ ] Mỗi tag H có kill criteria trong validation plan
- [ ] Không có "theo các chuyên gia" không tên
- [ ] Mọi nguồn đều link được hoặc PMID
- [ ] S0 trả lời 7 câu hỏi trực tiếp, không vòng vo
- [ ] S0 có callout phản biện (cảnh báo rủi ro)
- [ ] S14 có mâu thuẫn dữ liệu (nếu không có, chưa research kỹ)

**Số liệu:**
- [ ] Mỗi số trong KPI grid có tag
- [ ] Economic impact của mỗi pain point có số (dù H)
- [ ] Không số nào là "rất lớn", "đáng kể" — phải có ước lượng
- [ ] Các số H được phân biệt rõ với F/E

**Phân tích:**
- [ ] Segment table có hành vi mua và người quyết định
- [ ] Pain map có ít nhất 20 pain point
- [ ] Causal chain có điểm can thiệp được đánh dấu
- [ ] Gap scoring có giải thích nếu gap Market Attractiveness cao nhưng xếp cuối
- [ ] Deep dive 16 điểm đầy đủ (không thiếu điểm nào)
- [ ] Why Now: mỗi driver có bằng chứng
- [ ] Entry strategy: 3 option rõ ràng
- [ ] Validation plan: mỗi câu hỏi có kill criteria

**Format:**
- [ ] Tự đứng một mình (single file HTML)
- [ ] Dark mode hoạt động
- [ ] Responsive (mobile ≤760px)
- [ ] Mục lục link đúng anchor
- [ ] Không có lỗi HTML (unclosed tags, duplicate IDs)


## References & Notes

### Source credibility hierarchy
1. Số liệu chính phủ / cơ quan thống kê (F)
2. Nghiên cứu peer-reviewed (E)
3. Báo cáo doanh nghiệp niêm yết (F)
4. Báo chí chính thống dẫn số liệu gốc (F)
5. Báo cáo thương mại (I)
6. Diễn giải chuyên gia (I)
7. Giả thuyết từ logic (H)

### Related skills
- `web-research` — thu thập dữ liệu ngành
- `pubmed-evidence-research` — verify PMID cho mọi claim E
- `grounded-citations` — đảm bảo mọi nguồn kiểm chứng được
- `research-overview` — first principle nếu cần đào sâu cơ chế
- `research-reporting` — format HTML + publish preview
- `research-html-catalog` — nếu output dạng catalog

### Common pitfalls
1. **Nhảy từ pain → solution:** bỏ qua systemic chain và gap scoring. Luôn qua đủ 6 phase.
2. **Gắn solution sớm:** "công ty có công nghệ X → tìm gap cho X" là sai chiều. Xác định gap độc lập trước.
3. **Scoring giả chính xác:** điểm 3.8 vs 3.7 không quan trọng bằng phân tích định tính. Dùng scoring để xếp hạng, không để quyết định.
4. **Thiếu kill criteria:** mọi H phải có điều kiện để kill. Nếu không, không phải giả thuyết.
5. **Không phân biệt buyer vs user:** đặc biệt quan trọng ở B2B (trại gia công: tập đoàn là buyer, chủ trại là user).
6. **Mỗi segment chỉ 1 giải pháp:** không có một SKU phủ cả 4 segment — nếu nghĩ vậy là segment sai.
7. **Bỏ qua regulatory:** luôn kiểm tra phân loại sản phẩm (TĂBS vs thuốc thú y vs hóa chất) trước khi đề xuất entry.