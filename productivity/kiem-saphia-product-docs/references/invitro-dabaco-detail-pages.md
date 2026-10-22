# InVitro 2022 + DABACO Lạc Vệ 2022 — detail pages (3 ngôn ngữ)

Build 12/08, ngay sau mẫu InVivo. Cả 2 trang local `D:/Hermes Proj/kiem-saphia/detail/`, KHÔNG push gist — chờ anh duyệt mẫu rồi nhân ra các case còn lại (6 case Thực nghiệm).

## InVitro 2022 — `detail/invitro-2022.html` (20,9KB, 63 key I18N)

- File gốc: `reports/lab__2022_InVitro_Uc_che_Virus.docx` — **DOCX TOÀN ẢNH SCAN (không text layer)**
- **Kỹ thuật OCR docx scan (khác PDF — không có fitz render)**:
  1. Giải nén ảnh: `scripts/extract_invitro.py` (zipfile, `word/media/*` → `ocr_tmp/invitro_image1..9.jpg`)
  2. OCR từng ảnh: `scripts/ocr_invitro_detail.py` (RapidOCR python3.14, xử lý box 4 điểm → flat 8 số, sort y-x) → `reports/ocr_invitro_2022.json` + `.txt`
- Nội dung (phiếu VNUA **21120769.1**, trả 20/01/2022, khách Manna Đất Vàng, mẫu Kiềm EZ):
  - **Kết luận: Kiềm EZ pH 13 ức chế virus DTLCP (ASFV) trên tế bào PAM sơ cấp: tỉ lệ 5:1 → 2,67 log10 · 10:1 → 2,88 log10 · 40:1 → 2,94 log10** (IV. Kết luận, giữ nguyên văn)
  - Phương pháp: nuôi cấy PAM, virus ASFV.VNUA.01 hiệu giá >10⁶ HAD50/ml, Reed-Muench, HAD hằng ngày, ủ 60 phút 25±3°C, pha loãng 10⁻¹..10⁻⁷, 5 giếng/nồng độ, độ giảm so với đối chứng dương
  - Hiệu đính: nồng độ gốc pH 13 gây độc tế bào PAM (bảng 2, ghi chú "a"); pH 12/11 không có trong kết luận — chỉ pH 13
  - Bảng số liệu chi tiết 3.1-3.3 (HAD 5 giếng/dải pha loãng) bị OCR lệch cột nặng → dựng bảng TÓM TẮT (tỉ lệ → log10) + note trỏ phụ lục, KHÔNG bịa hiệu giá virus HAD50/ml từng cột (OCR mơ hồ)
- Drive: `1D9NtAaEyu20MAW-22J5stGnFXqZEJjP3`

## DABACO Lạc Vệ 2022 — `detail/dabaco-lac-ve-2022.html` (21,9KB, 80 key I18N)

- File gốc: `reports/thucte__DABACO_TÓM_TẮT_BÁO_CÁO_docx.doc` (thực chất docx, python-docx đọc được)
- ⚠️ `scripts/read_docx.py` truncate ở 30 paragraphs → dump FULL bằng script riêng (`scripts/dump_dabaco.py`); ⚠️ tên file có dấu/ký tự đặc biệt → lifecycle guard của terminal có thể chặn inline `python3.14 -c` chứa path đó, viết script file cho chắc
- Nội dung (Tóm tắt báo cáo thử nghiệm Kiềm EZ tái sinh thay kháng sinh, 368 lợn = 2 lô × 184, 98 ngày từ 23/12/2022, trại Lạc Vệ–DABACO, liều 10 kg/tấn):
  - a. Sinh trưởng: ADG 0,970 vs 0,977 kg/ngày · FCR 2,514 vs 2,500 (tương đương) · xuất chuồng thấp hơn ~0,7 kg/con (không ý nghĩa thống kê)
  - b. Sức khỏe: viêm phổi 115 vs 167 lần · tiêu chảy 6 vs 9 con · chết 0,54% vs 1,09% (giảm 50,5%) · **nát phân cao hơn ở lô TN** (ghi đúng, không giấu)
  - c. Thịt: móc hàm 86,39% vs 83,36% (+3,03%) · giữ nước tốt hơn · TN mềm/nước luộc trong, ĐC vị ngon đậm hơn
  - d. Kinh tế: kháng sinh 62 vs 553 đ/kg (−88,8%) · thuốc+phụ gia 3.204,5 vs 964,5 đ/kg (TN cao hơn ~+2.240 đ/kg — do chi phí sản phẩm)
  - Kết luận doc: thay thế được kháng sinh, cải thiện sức khỏe đàn, nâng một số chỉ tiêu thịt, NHƯNG hiệu quả kinh tế chưa tối ưu do chi phí sản phẩm cao → trình bày đủ 2 mặt, không chỉ lấy số có lợi
- Drive: `1_vZAXiGeSktTOHl1ovoV8KCIrEfXAZW5`

## Kỹ thuật build chung (`scripts/build_detail_cases.py`)

- 1 script sinh cả 2 trang: dict D (vi→(en,zh)) + `build_page()` dùng placeholder replace (`__KEY__`), KHÔNG f-string — tránh lỗi brace CSS
- `SHARED` dict chứa key dùng chung (header/brand/4 card titles/đơn vị VNUA/địa chỉ...) → `D_X = dict(SHARED); D_X.update({...})`
- ⚠️ **Key I18N phải khớp ĐÚNG 1 text node**: header "Thời gian tác dụng (phút)" phải là 1 key duy nhất — tách "Thời gian tác dụng" + "(phút)" = 2 key sẽ KHÔNG match node thật
- ⚠️ **`<title>` cần key riêng**: nằm NGOÀI body (cơ chế ORIG_TITLE), key title khác key badge, vd "PHIẾU KẾT QUẢ XÉT NGHIỆM 21120769.1 · InVitro 2022" — thiếu key này thì document.title không đổi khi chuyển ngôn ngữ
- **Tái dùng bản dịch ĐÃ DUYỆT trên trang chính**: grep `i18n-dict.json` / `tai-lieu-san-pham-khoa-hoc-v2.html` theo chuỗi VI (vd "553 đ/kg", "86,39%", "ADG (0,970") để lấy EN/ZH khớp sẵn — không dịch lại từ đầu, giữ nhất quán với trang chính

## Verify 0 key thiếu (`scripts/verify_detail_i18n.py`)

- html.parser (KHÔNG regex) trích text nodes (bỏ script/style) → so với dict D, báo missing
- Whitelist node CỐ Ý không dịch: VI/EN/中, "·", "—", "FCR", "25 ± 3°C", số/đơn vị thuần (regex `[\d\s.,:±°⁻⁺₂%–-]+`)
- Đọc dict từ source: exec phần source TRƯỚC marker `# build` (tránh chạy build ghi file); ⚠️ dict dùng `dict(SHARED); update({...})` nên trích bằng AST single-assign eval sẽ RA THIẾU key — phải exec cả khối
- Browser test: Camofox chặn `file://` → `python3.14 -m http.server <port> --bind 127.0.0.1` trong thư mục detail/ (background), test `?lang=en` deep link + click VI→EN→ZH→VI round-trip (bắt bug WeakMap ORIG) + console check, kill server sau
