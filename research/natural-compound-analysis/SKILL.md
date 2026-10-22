---
name: natural-compound-analysis
description: "7-section template for researching natural compound groups."
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [research, chemistry, natural-products, phytochemistry, analytical-methods]
---

# Natural Compound Analysis — Systematic Research & Documentation

Use when researching and documenting a natural compound group (alkaloids, terpenoids, saponins, flavonoids, tannins, etc.) for systematic knowledge capture.

## Research Template (7 Sections Required)

### 1. TÊN & ĐỊNH DANH
- Tên thông dụng (Việt + Anh), tên IUPAC, danh pháp
- Phân loại (terpenoid, alkaloid, phenolic, glycoside, steroid...)
- Lịch sử phát hiện, vai trò sinh học

### 2. ĐẶC TRƯNG NHẬN DẠNG
- Màu, mùi, vị, trạng thái. Tính tan (nước, ethanol, chloroform, dầu)
- Độ bền (nhiệt, ánh sáng, oxy, pH). Nhận biết nhanh

### 3. CẤU TRÚC HÓA HỌC
- Khung carbon, SMILES, nhóm chức. Biến thể (aglycone, glycone, dẫn xuất)
- KLPT, SAR nếu có

### 4. ĐẶC TÍNH HÓA LÝ THEO DẠNG
- Bột, lỏng, cao chiết, tro, nhũ tương/gel/vi nang
- Ảnh hưởng pH, nhiệt độ, ánh sáng

### 5. CÁC HOẠT CHẤT THÀNH VIÊN
- 10+ chất tiêu biểu: tên, CTPT, KLPT, hoạt tính chính
- Chất marker, chất độc, chất an toàn

### 6. NGUỒN TỰ NHIÊN
- Thực vật (tên KH, họ, bộ phận). Hàm lượng %, mùa vụ
- Ví dụ ở Việt Nam

### 7. PHƯƠNG PHÁP PHÁT HIỆN & ĐỊNH LƯỢNG (3 cấp độ)

**A. Cấp độ đơn giản** (lab cơ bản, chi phí thấp):
- Tạo màu, tạo tủa, tạo bọt. Thuốc thử, hiện tượng dương tính
- TLC: hệ dung môi, thuốc hiện màu, Rf

**B. Cấp độ trung bình** (lab phân tích):
- UV-Vis: bước sóng, phương pháp (Folin-Ciocalteu, vanillin-H2SO4, AlCl3)
- FTIR: dải hấp thụ đặc trưng. Đường chuẩn

**C. Cấp độ cao** (lab chuyên sâu):
- HPLC-UV/DAD, HPLC-ELSD, LC-MS/MS, GC-MS, NMR
- LOD, ứng dụng

## Yêu cầu bổ sung
- Bảng so sánh. Ví dụ số liệu thực tế
- 10 bullet điểm quan trọng nhất
- 3-5 hướng nghiên cứu/ứng dụng tiềm năng

## Interruption recovery

Subagents can be interrupted (timeout ~400-500s waiting for model). The data IS saved — check `data/*.json` in the project directory before assuming failure.

**Recovery pattern:** Re-dispatch with explicit "KHÔNG fetch thêm dữ liệu — build HTML từ dữ liệu có sẵn". The agent then only reads JSON + writes HTML, completing in 5-10 minutes instead of 20-30.

```python
# Example re-dispatch context:
"Dữ liệu đã collect sẵn tại [project]/data/:\n- pubchem.json\n- pubmed.json\n\nKHÔNG fetch thêm. Build HTML + publish."
```

## Multi-Agent Batch Workflow
Khi research nhiều nhóm (>3): chia batch tối đa 3 agent song song. Mỗi agent nhận template + context → PubMed → PubChem → build HTML → publish. Không poll, chờ auto-return.

## Data Sources Priority
1. PubMed (E-utilities: esearch + efetch) — PMID cho mọi claim
2. PubChem (CID, physicochemical properties)
3. DĐVN (Dược điển Việt Nam) cho nguồn VN
4. Patent databases
5. Wikipedia EN/VI + Danh lục cây thuốc VN

## Output
- HTML publish lên preview.thefirstonly.com, trả link
- Design: Say Briefly (cream #fcfaf5, green #1a3300, yellow #ffe95c, Bricolage Grotesque 800)

## Pitfalls
- Syntax error trong PubChem fetch script (double comma) — kiểm tra JSON trước khi chạy
- PubMed rate limit 1 req/1.1s — dùng background process
- Memory 1,375 chars — consolidate trước add entry mới
- Kiểm tra live transcript nếu agent không trả kết quả

## Data-driven report build (validated 2026-10)

### Quy trình
1. **Mine, đừng fetch.** Nếu data đã collect sẵn (`data/*.json`), đó là nguồn duy nhất — không gọi API lại. Khai thác hết trước khi viết: corpus stats (số query / bài unique / tạp chí / khoảng năm), per-compound counts, và grep abstract cho số liệu cụ thể (mobile phase, λ, LoD/LoQ, Rs, sinh khả dụng).
2. **Sinh HTML từ Python builder script**, không viết HTML tay. Script đọc JSON → render → tự validate. Giữ output path cố định để publish lại được. Xem `templates/report-builder.py` (skeleton: data-driven table + PMID citation + tự validate).
3. **Số trích dẫn gắn PMID, không gắn số thứ tự.** Điểm then chốt.

Chạy `scripts/validate-report-html.py report.html` trước khi publish.

### Citation numbering: dùng PMID làm khoá
Viết `<span class="refmark">[PMID]</span>` trong nội dung, cuối script đổi thành `[n]`:

```python
_MARK = r'(?:\\?)refmark(?:\\?)">\[(\d{8})\]'
_used = set(_re.findall(_MARK, HTML))
assert not (_used - set(CITED))          # chặn PMID không có trong danh mục
HTML = _re.sub(r'<span class="(?:\\?)refmark(?:\\?)">\[(\d{8})\]</span>',
               lambda m: f'<sup class="refmark">[{CITED.index(m.group(1)) + 1}]</sup>', HTML)
print("uncited refs:", sorted(set(CITED) - _used) or "none")
```

Vì sao: thêm/bỏ tài liệu thì số tự dịch, không bao giờ lệch. Viết `[7]` tay thì sửa một chỗ là mọi con trỏ khác hỏng theo. Marker phải khớp **cả hai** kiểu quote (`"` và `\"`) vì f-string lồng nhau sinh ra cả hai — regex `(?:\\?)` xử lý cả hai.

Refmark sai chỗ là lỗi nghiêm trọng nhất (citation trỏ sang bài khác = sai học thuật). Luôn assert + in `uncited refs` trước khi publish.

### Validate 4 lớp trước khi publish
1. **Tag balance** — `html.parser` với stack, báo vị trí dòng. Bắt được lỗi kiểu `</td>` đóng nhầm khối `<dd>` mà mắt thường bỏ sót.
2. **Citation range** — mọi `[n]` trong khoảng `1..len(refs)`, và không ref nào bị bỏ rơi.
3. **Artifact generator** — `None` / `undefined` / `NaN` / placeholder f-string chưa render. **Phải dùng word boundary**: `morphinan` chứa `nan`, prose có `undefined`. Quét substring thuần sẽ báo động giả.
4. **Structural** — `sections > 0`, `tables > 0`, rows > 0.

### Unslop có thể sửa report
`publish` tự chạy `html-unslop` và có thể đổi text/CSS. Sau khi publish luôn verify lại trên browser: font, màu nền, màu chữ, và JS còn chạy không.

### Browser verify: test TƯƠNG TÁC, không chỉ load
`page loads + 0 JS errors` **không** chứng minh JS hoạt động. Phải:
- set filter input → đếm số dòng hiện ra
- đổi sort select → đọc **dòng đầu tiên** xem đúng thứ tự chưa
- click header → kiểm tra `.sorted` được đánh dấu
- click reset → về trạng thái đầu

Bug loại này đã xảy ra: cột sort dùng sai chỉ số trong mảng `cells` nên fallback về so sánh chuỗi — chọn "giảm dần" vẫn ra tăng dần. Filter vẫn chạy đúng nên test kiểu "load thấy ok" bỏ sót hoàn toàn.

### JS pitfalls
- **Đừng escape Unicode tay trong JS.** `"\u0111\u1ed3ng"` → sai thành `tđồng`. Viết tiếng Việt trực tiếp.
- **`data-*` attribute là nguồn sort duy nhất** (`data-hw`, `data-psa`…). Không parse lại từ text cell — dấu phẩy/spacing trong ô sẽ làm sort sai.
- Mobile: ẩn table + hiện `.mlist` card; filter phải áp cho **cả hai** (`tr` và `.mcard`).
- Tách `<dl>` bằng `<div>` bọc cặp `<dt>/<dd>` — validator nghiêm sẽ báo crossed tags nếu không bọc.

### Windows paths
Script publish cần **native Windows path** (`D:\...\file.html`), không phải MSYS (`/d/...`) — Python `open()` không hiểu kiểu MSYS.
