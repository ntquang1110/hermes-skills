# QCVN 62:2025/BTNMT — Nước thải chăn nuôi: trích xuất Bảng 1 đã kiểm chứng (08/09/2026)

> Đã đối chiếu chéo 3 nguồn độc lập — khớp 100%. Dùng làm nguồn chuẩn khi hồ sơ pháp lý yêu cầu cập nhật từ QCVN 62-MT:2016 sang 2025.

## 1. Định danh văn bản (đã xác minh)

- **QCVN:** QCVN 62:2025/BTNMT — Quy chuẩn kỹ thuật quốc gia về nước thải chăn nuôi (National Technical Regulation on the Effluent of Livestock)
- **Văn bản ban hành:** **Thông tư số 04/2025/TT-BTNMT ngày 28/02/2025** — Bộ Tài nguyên và Môi trường
  - ⚠️ **Pitfall số hiệu:** Nhiều nguồn/đề bài ghi nhầm `05/2025/TT-BTNMT`. Thực tế `05/2025/TT-BTNMT` là **QCVN 14:2025** (nước thải sinh hoạt & đô thị, khu dân cư tập trung). Cả hai cùng ban hành 28/02/2025, cùng hiệu lực 01/09/2025 nên dễ nhầm. Khi tra cứu phải verify bằng toàn văn vbpl.vn / thuvienmoitruong.vn.
- **Hiệu lực:** **01/09/2025** — thay thế QCVN 62-MT:2016/BTNMT
- **Biên soạn/thẩm định:** Cục Kiểm soát ô nhiễm môi trường biên soạn, Vụ KH&CN trình duyệt; Bộ KH&CN thẩm định

## 2. Thay đổi cấu trúc Bảng 1 so với 2016

| 2016 (2 cột: A/B) | 2025 (3 cột: A/B/C) |
|---|---|
| Phân theo nguồn tiếp nhận đơn giản (A=cấp sinh hoạt, B=còn lại) | **Phân theo chức năng nguồn tiếp nhận gắn QCVN 08:2023/BTNMT** (nước mặt): A=Mức A Bảng 2,3 QCVN 08 hoặc cấp sinh hoạt; B=Mức B QCVN 08; C=các trường hợp còn lại (theo UBND tỉnh). **Không phân theo lưu lượng Q** (khác QCVN 40 công nghiệp). |
| Tổng P: 1 giá trị | **Chia 3 loại nguồn tiếp nhận**: hồ/ao/đầm — sông/suối/khe/kênh/mương/rạch — vùng nước biển |
| Không có TOC | Cho phép **chọn COD hoặc TOC** (TOC: A ≤35 / B ≤70 / C ≤130 mg/L) |
| NH4+/NH3 có thể được hiểu ngầm | **Không có dòng riêng NH4+/NH3** — chỉ còn Tổng Nitơ (T-N). Đã search toàn văn PDF 7 trang = 0 hit cho Amoni/NH4/NH3. |

## 3. Bảng 1 đầy đủ — dự án đầu tư, cơ sở chăn nuôi trang trại (nguồn: PDF tr.4)

| TT | Thông số | ĐV | A | B | C |
|---|---|---|---|---|---|
|1|pH|-|6–9|6–9|6–9|
|2|BOD5 (20°C)|mg/L|≤40|≤60|≤100|
|3|COD|mg/L|≤65|≤150|≤250|
| |*hoặc TOC*|mg/L|≤35|≤70|≤130|
|4|TSS|mg/L|≤40|≤100|≤120|
|5|Tổng Nitơ (T-N)|mg/L|≤20|≤60|≤120|
|6|Tổng Phốt pho (T-P) — hồ/ao/đầm|mg/L|≤2,0|≤3,0|≤4,0|
| |— sông/suối/khe/kênh/mương/rạch|mg/L|≤4,0|≤14|≤30|
| |— vùng nước biển|mg/L|≤4,0|≤14|≤40|
|7|Tổng Coliform|MPN hoặc CFU/100 mL|≤3.000|≤5.000|≤5.000|

Chú thích QCVN: *Tổ chức, cá nhân được lựa chọn áp dụng TOC hoặc COD.*
Mục 2.2: nông hộ mặc định đáp ứng Bảng 1; khi xả ra nguồn B/C được chọn (a) xử lý đạt B/C hoặc (b) thu gom về biogas/bể ủ/bể lắng ≥1,5 m³/đơn vị vật nuôi, chống thấm.

## 4. Đối chiếu nhanh 2016 Cột B → 2025

| Chỉ tiêu | 2016 B | 2025 B | 2025 C |
|---|---|---|---|
|BOD5|≤100|≤60 (−40%)|≤100|
|COD|≤300|≤150 (−50%)|≤250|
|TSS|≤150|≤100 (−33%)|≤120|
|Tổng N|≤150|≤60 (−60%)|≤120|
|pH|5,5–9,0|6–9 (siết dưới)|6–9|

## 5. Workflow trích xuất đã kiểm chứng (Windows, curl)

1. **DDG HTML search** (`html.duckduckgo.com/html/?q=`) với UA Chrome + `--compressed` → surface đúng URL QCVN (luatvietnam/thuvienmoitruong/nguoichannuoi) — Bing/Mojeek không surface.
2. **Curl text extraction:** `curl -sL --compressed -A 'Mozilla/5.0' -H 'Accept-Language: vi-VN' <url>` → strip `<script>/<style>` → `re.sub(r'<[^>]+>',' ',...)` → `html.unescape` → `re.sub(r'\s+',' ',...)`. Đủ để lấy Bảng 1 từ luatvietnam.vn (23KB text) và thuvienmoitruong.vn (11KB text).
3. **Cloudflare handling:** `thuvienphapluat.vn/TCVN/.../QCVN-62...` bị Cloudflare "Just a moment" (raw 5,8KB challenge), không trích được qua curl — phải fallback sang thuvienmoitruong.vn + luatvietnam.vn. `vbpl.vn` render bằng JS (SPA, tiêu đề là `<span>` React, không phải `<a>`), curl chỉ trả khung — cần browser hoặc bỏ qua.
4. **PDF verify:** `https://nguoichannuoi.vn/.../QCVN-62-2025-BTNMT-ve-nuoc-thai-chan-nuoi.pdf` (444KB, 7 trang) — tải bằng curl, trích bằng `pymupdf` (`fitz.open` → `page.get_text()`), Bảng 1 ở trang 4. Khớp tuyệt đối với text. PDF ký số Lang Sơn (`trangdinh.langson.gov.vn/...Signed...pdf`) tồn tại nhưng curl lần 2 không trả (cần trình duyệt) — dùng bản nguoichannuoi làm bằng chứng chính.
5. **Verify số hiệu TT:** luôn check `Thông tư số.*2025/TT-BTNMT` trong toàn văn thuvienmoitruong.vn/luatvietnam.vn — không tin đề bài. 04/2025=QCVN 62, 05/2025=QCVN 14.
6. **Đối chiếu chéo bắt buộc:** text luatvietnam + text thuvienmoitruong + PDF pymupdf — phải khớp số học trước khi đưa vào hồ sơ.

## 6. URLs đã truy xuất thành công (08/09/2026)

| Nguồn | URL | Ghi chú |
|---|---|---|
|thuvienmoitruong.vn (khuyến nghị dẫn đầu)|https://thuvienmoitruong.vn/qcvn-622025-btnmt-quy-chuan-ky-thuat-quoc-gia-ve-nuoc-thai-chan-nuoi/|11KB text, ghi rõ TT 04/2025 28/02/2025, hiệu lực 01/09/2025, Bảng 1 đầy đủ|
|luatvietnam.vn|https://luatvietnam.vn/tai-nguyen/quy-chuan-qcvn-622025-btnmt-nuoc-thai-chan-nuoi-391868-d3.html|23KB text, khớp PDF|
|PDF gốc (nguoichannuoi)|https://nguoichannuoi.vn/wp-content/uploads/2025/03/QCVN-62-2025-BTNMT-ve-nuoc-thai-chan-nuoi.pdf|444KB 7 trang, tr.4|
|thuvienphapluat.vn|https://thuvienphapluat.vn/TCVN/Tai-nguyen-Moi-truong/QCVN-62-2025-BTNMT-Nuoc-thai-chan-nuoi-921506.aspx|Cloudflare chặn curl|
|congbao.chinhphu.vn (loại trừ nhầm lẫn)|https://congbao.chinhphu.vn/van-ban/thong-tu-so-05-2025-tt-btnmt-44496.htm|Đây là QCVN 14, không phải QCVN 62 — dùng để chứng minh 05/2025 ≠ QCVN 62|

## 7. Khuyến nghị hồ sơ

- Xác định phân vùng A/B/C theo QCVN 08:2023 + quyết định UBND tỉnh trước khi chọn cột; nếu chưa rõ, trình cả 3 cột.
- Hồ (ao, đầm): T-P khắt khe nhất (A ≤2,0) — cần xử lý P riêng.
- pH siết cận dưới 5,5→6,0; bổ sung phương án TOC thay COD nếu có lợi.
- Bỏ NH4+ riêng khỏi Bảng 1; ghi chú "không quy định trong QCVN 62:2025, chỉ quản lý qua Tổng N" nếu HĐQT yêu cầu.
