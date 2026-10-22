# InVivo 2022 — OCR chi tiết + hiệu đính + Cách A (detail page)

Trạng thái cuối session 12/08: **Cách A MẪU CASE InVivo 2022 ĐÃ LÀM XONG** — OCR 7 trang → hiệu đính → dựng trang detail 3 ngôn ngữ → gist riêng → link case trên trang chính trỏ sang. Còn 15 link (InVitro + 6 case Thực nghiệm) chờ anh duyệt mẫu rồi nhân ra.

Bối cảnh quyết định: Quang thử PA2 (link → preview scroll tới case) nhưng chưa hài lòng — "bấm link phải ra bản tiếng Anh, chứa toàn thứ họ đang xem". Scan PDF không dịch tự động được → bản dịch = trang nội dung tự tạo.

## File gốc + OCR

- PDF gốc: `D:/Hermes Proj/kiem-saphia/reports/lab__2022_InVivo_Cong_cuong_do.pdf` (scan 7 trang, phiếu VNUA 21120769.2, trả 17/02/2022)
- OCR bằng RapidOCR (python3.14, upscale 2.2x): `scripts/ocr_invivo_detail.py` → `reports/ocr_invivo_2022.json` (box+tọa độ mỗi line) + `.txt` (text thuần)
- Render trang ra PNG để soi: `scripts/render_pages.py` (pymupdf Matrix 2.5)
- Bản hiệu đính: `reports/invivo_2022_hieudinh.md` (7 trang, đầy đủ)
- **Trang detail đã build: `D:/Hermes Proj/kiem-saphia/invivo-2022.html` (29KB, 3 ngôn ngữ)**
- Gist detail: `d723513bdda22ffe54c277ff3fc4edb6` → preview `https://preview.thefirstonly.com/d723513bdda22ffe54c277ff3fc4edb6`
- Trang chính (gist `3d581a3444296042579d49722d4d85fe`) case-lab-2 link tên case → gist detail, link "Tài liệu gốc (VI)" → Drive scan

## ⚠️ PITFALL RapidOCR v1.2.3 — box format đổi

RapidOCR v1.2.3 trả `result` mỗi item `(box, text, conf)` nhưng **box là list 4 điểm `[[x1,y1],[x2,y2],[x3,y3],[x4,y4]]`, KHÔNG phải flat `[x1,y1,x2,y2,...]`** → `float(box[0])` ném `TypeError: float() argument must be a string or a real number, not 'list'`.

Fix chuẩn trong script:
```python
if isinstance(box[0], (list, tuple)):
    flat = [float(v) for pt in box for v in pt]   # [[x1,y1],...] -> flat 8 số
else:
    flat = [float(v) for v in box]                 # flat đã có sẵn
```

## Kỹ thuật dựng lại bảng từ OCR box (scan lệch làm trộn cột)

OCR text thuần bị trộn cột (sort y đơn thuần không đủ). Dựng lại bằng clustering x-y trên JSON box:

```python
def cx(l): return (l["box"][0]+l["box"][2]+l["box"][4]+l["box"][6])/4.0
def cy(l): return (l["box"][1]+l["box"][3]+l["box"][5]+l["box"][7])/4.0
# cột: cluster theo x (bucket 20px); hàng: cluster theo y (band 18px)
band = round(y/18)*18
```
Gán từng cell vào (colname theo x-range, band theo y) rồi in ra bảng theo band tăng dần. Đã dựng lại được Bảng 3.1 (nhiệt độ 8 lợn × 40 ngày) chính xác theo cách này. Script: `scripts/rebuild_t32.py` (render thử) + `scripts/dump_coords.py` (xuất y/x từng line để đối chiếu tay).

**Lưu ý dựng bảng 3.3 (hiệu quả)**: bảng này freeform (thể trạng + ghi chú nhiều dòng/cell), không ép được vào grid cột đơn giản — dựng tay từ dump_coords, map từng lợn 80-87 với ngày chết / tỷ lệ / thể trạng / nguyên nhân. OCR mờ chỗ lợn 85-87 đối chứng ("Hôn mê, yếu khi chết — Dịch tả lợn châu phi") — cần anh đối chiếu bản gốc.

## Workflow hiệu đính (Quang yêu cầu, bắt buộc)

Quang: "phải đảm bảo nội dung sau khi OCR đúng bối cảnh và đúng phần text, giữ lại câu đúng y nguyên bản gốc. Nếu bản gốc trình bày đoạn văn thì giữ đoạn văn; bảng/cột thì trình bày đúng bảng/cột."

→ Quy trình:
1. OCR thô → hiệu đính từng lỗi theo bối cảnh (HQC→HỌC, TRi→TRỌNG, kiém→kiềm, dch→đch...)
2. GIỮ NGUYÊN câu chữ + cấu trúc bản gốc (số phiếu, ngày, tên, chữ ký, footer ISO)
3. Bảng dựng lại đúng cột (số lợn, lô, ngày)
4. **TRÌNH BÀY bản hiệu đính cho anh duyệt TRƯỚC khi dựng trang** — anh duyệt xong mới triển khai (pattern "trình bày hiểu/trước đã" lặp lại)

## Nội dung cốt lõi InVivo 2022 (đã hiệu đính, dùng làm nguồn detail page)

- 2 lô: Lô 1 = 5 lợn 15-17kg dùng Kiềm EZ tái sinh bột 1%/1,5%/1,8%/2% theo giai đoạn D0-D5/D5-D10/D11-D20/D21-D30; Lô 2 = 3 lợn đối chứng
- Virus ASFV.VNUA.01 độc lực cao, hiệu giá 7x10² HAD50/ml, liều 5x10² HAD/lợn
- Kết quả: sau 10 ngày lô EZ sống 100% (5/5); đối chứng chết 100% (3/3) sau 9 ngày, Ct 17,59-18,51 ≈ 5x10⁵ HAD50/ml
- Ngày 14: lô EZ 3/5 (60%); lợn 80, 83 chết có E. coli dung huyết + H. parasuis
- Ngày 25: 3/5 (60%), virus mức thấp Ct 26,4-28,86 ≈ 10⁴ HAD50/ml
- Ngày 26: lợn 81, 84 chết Ct 27,58-28,16, cũng bội nhiễm
- Cuối: 1/5 (20%) sống (lợn 82), ghi chú cần lặp lại thí nghiệm vì lợn mang mầm E. coli/H. parasuis serotype 12 độc lực cao từ trại

## Build + push detail page (đã test)

1. `scripts/detail_data.py` — data 3 bảng (T31 nhiệt độ 41 ngày, T32 Ct, T33 hiệu quả) dạng tuple, ô "(Chết)"/"(Sống)"/None
2. `scripts/build_detail.py` — sinh `invivo-2022.html`: i18n dict (vi→en,zh) + applyLang giống trang chính + backlink về gist chính + link "Xem bản gốc scan trên Drive"
3. `scripts/create_gist_detail.py` — tạo gist mới (file `index.html`): **PITFALL đọc `GITHUB_PAT_B64` từ .env rồi base64 decode, KHÔNG phải GITHUB_PAT (401 nếu sai)**
4. `scripts/push_gist_detail.py` — PATCH gist detail giữ nguyên URL
5. Trang chính: đổi href case-link sang gist detail + **đổi `syncCaseLinks` bỏ hardcode `PREVIEW_BASE`** (mỗi link giữ base riêng qua `data-base`)

## Việc còn lại (chờ anh duyệt)

- Anh duyệt mẫu InVivo → nhân ra 15 link còn lại (InVitro + 6 case Thực nghiệm) — mỗi case 1 trang detail 1 gist riêng
- Chỗ OCR mờ cần đối chiếu bản gốc: bảng 3.3 phần thể trạng/ghi chú lợn 85-87
