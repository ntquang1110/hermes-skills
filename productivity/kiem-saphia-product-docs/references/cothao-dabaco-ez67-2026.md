# 3 case detail 2026: Cô Thảo 16 con · DABACO dự toán 1.000 · Protocol EZ67 (12/08)

Dữ liệu đã extract từ file gốc — khỏi đọc lại. Detail pages LƯU LOCAL:
`D:/Hermes Proj/kiem-saphia/detail/co-thao-16-con-2026.html`, `dabaco-du-toan-1000.html`, `protocol-ez67.html`.
Build script: `scripts/build_detail_3cases.py` (generalize build_page() + verify_i18n() cho nhiều case).

## Cô Thảo 16 con — 14 phiếu PCR ASF
- **12 phiếu VETTECH** (`reports/thucte__cothao__*.pdf`) CÓ text layer — pymupdf đọc thẳng được, KHÔNG phải scan (khác InVivo VNUA). Extract full text: `reports/cothao_pdfs_extracted.txt`.
- **2 phiếu FiveLab** (`thucte__cothao__26PCR06183-Mẫu 1.pdf` / `Mẫu 4.pdf`) là SCAN không text layer → OCR RapidOCR (kết quả `reports/cothao_scans_ocr.txt`).
- Trại: Định Văn Việt – Thôn 2, Long Phú, Nho Quan, Ninh Bình (trại Cô Thảo). Khách: Manna Đất Vàng. Người nhận: Mr Dương. Tiêu chí VETTECH: dương Ct≤35, nghi ngờ 35<Ct≤40, âm = không có Ct.
- **⚠️ Phiếu 21/03/2026 (26031211-1) ghi địa chỉ "Trại Việt Thảo – Phú Long"** — khác tên trại các phiếu khác; giữ nguyên như bản gốc, không "sửa".
- Kết quả (ngày | phiếu | lô | loại | Ct | KL):
  - 21/03 | 26031211-1 | Lô 16 TN – Gộp | Máu gộp | 21.88 | Phát hiện
  - 04/04 | 26040198-1 | Lô 16 TN – Gộp 040426 | Máu gộp | 28.48 | Phát hiện
  - 17/04 | 26041019-1 | Lô 16 TN – Gộp 170426 | Máu gộp | 36.84 | Nghi ngờ
  - 07/05 | 26050230-1 | Lô 16 TN | Phân | – | Không phát hiện
  - 20/05 | 26050834-1 | Lô 14 ĐC · con số 1,4 | Máu gộp | 25.21 | Phát hiện
  - 20/05 | 26050834-2 | Lô 14 TN · con số 12,13 | Máu gộp | 27.21 | Phát hiện
  - 20/05 | 26050834-3 | Lô 16 TN – Gộp 200526 | Máu gộp | 35.31 | Nghi ngờ
  - 20/05 | 26050834-4 | Lô 14 – Mẫu phân 200526 | Phân | 36.18 | Nghi ngờ
  - 02/06 | 26060077-1 | Lô 14 ĐC · con số 02,05 | Máu gộp | 28.24 | Phát hiện
  - 02/06 | 26060078-1 | Lô 14 TN · con số 12,13 | Máu gộp | 27.54 | Phát hiện
  - 17/06 | 26060816-3 | Lô 16 TN (con nhỏ) | Máu | – | Không phát hiện
  - 17/06 | 26060816-4 | Lô 16 TN (con to) | Máu | – | Không phát hiện
  - 17/06 | 26PCR06183 Mẫu 1 (FiveLab) | Lô 14 TN – Ăn kiềm, số tai 13 | Máu | – | Âm tính
  - 17/06 | 26PCR06183 Mẫu 4 (FiveLab) | Lô 16 TN (con to) | Máu | – | Âm tính
- FiveLab: phiếu THAY THẾ phiếu cùng số 26PCR06183 ban hành 19/06/2026; xét nghiệm 19/06/2026, trả 23/06/2026. OCR Mẫu 1: "Lo14 TN- An kiem so tai 13" → hiệu đính "Lô 14 TN – Ăn kiềm, số tai 13".
- Diễn biến lô 16 TN: Phát hiện → Nghi ngờ → Không phát hiện (07/05, 17/06) — đúng nội dung hồ sơ "PCR âm tính ASF tại thời điểm kiểm tra". Lô 14 ĐC vẫn Phát hiện (Ct 25,21–28,24) cùng giai đoạn.
- Drive gốc (folder): `https://drive.google.com/drive/folders/1V561qEPMwGOaL0pccftVHyE6QjE9j--G`

## DABACO dự toán 1.000 con — CSV
- `reports/thucte__DABACO_du_toan_1000.csv` (export Google Sheets qua `files().export(fileId, mimeType='text/csv')`).
- **⚠️ Tên file "du_toan_1000" nhưng nội dung = dữ liệu 184 con/lô, 98 ngày (khớp Lạc Vệ-Dabaco)** — trình bày đúng nội dung file, không tự "scale" lên 1.000 con.
- 25 dòng × 13 cột: Chỉ tiêu | ĐVT | TN1–TN4 | ĐC1–ĐC4 | Tổng TN | Tổng ĐC | Chênh lệch. Giữ NGUYÊN số liệu: dấu phẩy nghìn ("19,585"), ô trống, FCR tổng "3", ADFI tổng "2" (ghi chú "giữ đúng như file gốc").
- Số chính: tiền thuốc TN 1,214,270 vs ĐC 10,660,181 (−9,445,911); kháng sinh/kg tăng trọng 62 vs 553 (−491 ≈ −88,8%); chết 0.54% vs 1.09%; viêm phổi 0.64% vs 0.94%; tiêu chảy 3.0% vs 5.0%; nát phân 40% vs 13%; ADG 0.97/0.977.
- Drive gốc: `https://drive.google.com/file/d/<SHEET_ID>/view`

## Protocol EZ67 — docx 201 paragraphs + 4 bảng
- File: `reports/thucte__Vua_Kiềm___Protocol_thử_nghiệm_Ez67_cho_lợn_0626_docx.doc` (thực chất docx). Full dump: `reports/ez67_protocol_extracted.txt`.
- Hà Nội 24/06/2026. Đơn vị chủ trì: Manna Đất Vàng (1111 Ngô Gia Tự, Việt Hưng, Hà Nội). Phối hợp: trang trại lợn tham gia. Dự kiến 05 tháng.
- Đối tượng: lợn thịt 20–30 kg, PCR dương ASF, còn ăn uống, chưa hấp hối. CRD quy mô 60 con (30 TN + 30 ĐC). Tiêu chuẩn loại trừ: bỏ ăn hoàn toàn, mất vận động, bệnh khác nặng, thiếu dữ liệu.
- Phác đồ (bảng trong docx): EZ80 5 kg/tấn thức ăn, trộn thức ăn, Ngày 0 – xuất bán; EZ67 1 lít/50 lít nước, nước uống, Ngày 0 – 30.
- Thang điểm lâm sàng 0–3: Ăn uống (Bình thường/Giảm nhẹ/Giảm nhiều/Bỏ ăn) · Hoạt động (Bình thường/Chậm/Ít vận động/Nằm) · Hô hấp (Bình thường/Thở nhanh/Khó thở/Rất nặng) · Da (Bình thường/Đỏ nhẹ/Xuất huyết/Tím tái nhiều).
- Lịch lấy mẫu: ngày 0/7/14/21/30/45/60 (ĐC/TN; khám lâm sàng, PCR, Ct, lượng thức ăn). Theo dõi hằng ngày: ăn uống, thân nhiệt, vận động, hô hấp, xuất huyết, tím tái, tiêu chảy, thần kinh, tỷ lệ chết.
- Chỉ tiêu: lâm sàng · dịch tễ (sống/chết/hao hụt, thời gian triệu chứng) · virus học (PCR dương, Ct, tải lượng) · sinh trưởng (khối lượng, ADG, ADFI, FCR) · an toàn. Thống kê: t-test, ANOVA, Duncan, Tukey, Chi-square, Kaplan–Meier, P<0.05.
- Tiêu chí hiệu quả: tỷ lệ sống cao hơn / chết thấp hơn / sống lâu hơn / điểm lâm sàng thấp hơn / ăn uống phục hồi nhanh / tăng trọng tốt hơn / không tác dụng bất lợi đáng kể.
- **Trạng thái: đang triển khai — chưa có kết quả** (ghi rõ trên trang, badge "PROTOCOL · THIẾT KẾ THỬ NGHIỆM").
- Drive gốc: `https://drive.google.com/file/d/126o1zpDClX-23E-9k92uW6ite6i7PenO/view`

## Pitfall mới dính lúc làm 3 case này (12/08)
- **RapidOCR v1.2.3: `conf` là STR không phải float** → `f"{conf:.2f}"` ném `ValueError: Unknown format code 'f' for object of type 'str'` — in `[conf]` trực tiếp.
- **Lifecycle guard Hermes crash "embedded null character in path" khi chạy `python -c` inline dài phức tạp** → viết script ra file (`scripts/dump_*.py`) rồi chạy, không nhồi inline.
- **`file` nhận nhầm file UTF-8 tiếng Việt thành "Par archive data" + read_file từ chối "Binary file"** → đọc bằng python `open(path,'rb').read().decode('utf-8', errors='replace')`.
- **Identity keys cho header nhóm lô**: TN1..TN4 giữ nguyên, ĐC1..ĐC4 → EN "CT1..CT4" / ZH "对照组1..4"; "Ct"/"Chỉ tiêu"/"Ngày" mỗi trang phải có key (verify báo MISSING nếu thiếu).
- File scan không text layer → ghi trên trang: "Bản scan không có text layer — nội dung từ OCR hiệu đính".
