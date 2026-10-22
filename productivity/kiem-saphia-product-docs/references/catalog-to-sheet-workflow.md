# Catalog PDF → Google Sheet danh mục sản phẩm (đã verify 10/08/2026)

Pipeline dùng khi anh đưa file catalog PDF (thường lớn, 100MB+) và muốn lưu toàn bộ thông tin sản phẩm ra sheet để nắm/lưu được.

## Bước 1 — Extract text PDF

- Dùng **pymupdf** (`import pymupdf` — cài `pip install pymupdf` nếu thiếu). KHÔNG dùng pdfplumber (chưa cài).
- **Chạy qua terminal, KHÔNG qua execute_code**: sandbox interpreter của execute_code không có pymupdf → `ModuleNotFoundError`. Viết script ra file rồi `python script.py` qua terminal.
- Viết text ra .txt bằng python (mở file `encoding='utf-8'`); KHÔNG dùng read_file để đọc file đã extract — read_file nhận diện nhầm thành binary (`Binary file - cannot display as text`) vì ký tự UTF-8/CRLF. Đọc lại bằng `python -c "... open(path, encoding='utf-8').read() ..."` hoặc grep.
- Code mẫu:
```python
import pymupdf
doc = pymupdf.open(src)  # src = "D:/VuaKiem/Catalog/29042026.pdf"
with open(out_txt, "w", encoding="utf-8") as f:
    for i in range(doc.page_count):
        f.write(f"\n===== PAGE {i+1} =====\n")
        f.write(doc[i].get_text() or "[NO TEXT - image page]")
```
- 155MB / 20 trang extract ~vài giây, output ~26KB text. Trang cuối có thể là ảnh → "[NO TEXT]".

## Bước 2 — Tạo + điền Google Sheet

- Check auth trước: `setup.py --check` → "AUTHENTICATED (partial)" là OK nếu thiếu gmail/calendar (chỉ cần drive+sheets).
- Tạo sheet: `google_api.py sheets create --title "..." --sheet-name "Sản phẩm"` → trả `spreadsheetId`.
- Điền data: dùng python trực tiếp (googleapiclient + token `C:/Users/NTQUANG_DELL/AppData/Local/hermes/google_token.json`) vì GAPI CLI chỉ nhận JSON inline, dữ liệu nhiều dòng phức tạp.

### Pitfall 1 — Tên sheet KHÔNG phải "Sheet1"
`sheets get <id> "Sheet1!A1:F10"` → lỗi `HttpError 400: Unable to parse range: Sheet1!A1:F10`.
Fix: list sheets trước, lấy tên thật:
```python
meta = srv.spreadsheets().get(spreadsheetId=ID).execute()
for sh in meta['sheets']:
    print(sh['properties']['sheetId'], sh['properties']['title'])
```

### Pitfall 2 — sheetId KHÔNG phải 0 khi format header
`batchUpdate` với `"range": {"sheetId": 0}` → `HttpError 400: No grid with id: 0`.
Fix: dùng sheetId thật từ metadata (vd `803430587`), không hardcode 0.
Lưu ý khi **addSheet** (tạo tab mới): `batchUpdate` trả sheetId trong `replies[0]['addSheet']['properties']['sheetId']` — dùng nó cho các lần format/rename sau, đừng đoán.

### Pitfall 3 — Range khai báo PHẢI khớp chính xác số hàng dữ liệu
`values().update` với range `A30:E44` (15 hàng) nhưng gửi 30 rows → `HttpError 400: ... but tried writing to row [45]`.
Fix: **đếm số dòng trước khi khai range** (`range = f'A{start}:E{start+len(rows)-1}'`), hoặc đọc trước vùng để biết dòng trống bắt đầu ở đâu. Chia dữ liệu lớn thành nhiều batch nhỏ (10-30 hàng/lần) tránh stream timeout khi gửi qua heredoc.

### Pitfall 4 — Gửi data nhiều dòng qua terminal heredoc (python <<'PYEOF')
Gọi googleapiclient trực tiếp qua `python - <<'PYEOF'` là chuẩn (sandbox execute_code KHÔNG có google libs/token). Mỗi lệnh giữ dưới ~8K token args — dữ liệu lớn chia batch. Nếu lệnh bị flag "script execution via heredoc" → smart approval tự duyệt, cứ chạy.

### Điền + format header
```python
srv.spreadsheets().values().update(
    spreadsheetId=ID, range="Sản phẩm!A1:H12",
    valueInputOption="RAW", body={"values": values}).execute()
# format header (vàng đậm)
reqs = [{"repeatCell": {"range": {"sheetId": REAL_ID, "startRowIndex": 0, "endRowIndex": 1},
    "cell": {"userEnteredFormat": {"textFormat": {"bold": True},
            "backgroundColor": {"red": 1.0, "green": 0.84, "blue": 0.0}}},
    "fields": "userEnteredFormat.textFormat.bold,userEnteredFormat.backgroundColor"}}]
srv.spreadsheets().batchUpdate(spreadsheetId=ID, body={"requests": reqs}).execute()
```
Verify: `sheets get ID "Sản phẩm!A1:C4"` đọc lại được.

## Bước 3 — Lưu bản tóm tắt local

Viết `catalog-vuakiem-<date>.md` trong `D:/Hermes Proj/kiem-saphia/`: công ty, sở hữu trí tuệ, 11 sản phẩm theo nhóm (cây trồng/chăn nuôi/thủy sản/thực phẩm) kèm giá, quy cách, cách dùng, thành phần. Cập nhật STATE file.

## Kết quả 10/08 (đã chạy)

- Sheet: "Vua Kiềm - Danh mục sản phẩm (Catalog 29042026)" `<SHEET_ID>` — 11 sản phẩm × 8 cột.
- **Sheet làm việc CHÍNH = `<SHEET_ID>`** (anh điền trực tiếp): tab "Sản phẩm" gid=2118893758 (10 cột, cột "Thành phần chính" liệt kê gọn) + tab "Thành phần chi tiết" gid=472640767 (5 cột, 4 nhóm phân loại, 112 thành phần / 12 sản phẩm). Đồng bộ: đọc sheet → MD local → HTML → demo → publish.
- Spec thật: EZ80 = Kiềm EZ Tái sinh 80 (1,25tr/10kg, 5kg/tấn); **EZ67 = SP MỚI dạng nước (can 20L, 3,2tr, pha 1:19, cám cháo) — đã xác nhận 10/08**.
