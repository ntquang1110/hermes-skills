---
name: google-sheets-data-fill
description: "Use when filling Google Sheets from PDFs/documents."
version: 1.0.0
metadata:
  hermes:
    tags: [Google, Sheets, API, data-fill, catalog, PDF]
    category: productivity
---

# Google Sheets Data Fill (direct API)

Populate Google Sheets from local documents/PDFs/catalogs via the Sheets API directly (googleapiclient), bypassing the thin CLI when data is large or multi-tab. Proven on the Vua Kiềm product catalog (155MB PDF → 2 tabs → 12 products).

## When to use
- Extract data from a PDF/document and write it into a spreadsheet
- Create a NEW TAB inside an existing spreadsheet (not just a new file)
- Write 20+ rows or long cell text (product specs, thành phần lists)
- Format headers / highlight rows in a newly created tab
- **Create a BRAND-NEW spreadsheet from structured data (JSON/HTML table) + format + share** (e.g. "lập Google Sheet để gửi đối tác/bên thu mua") — see workflow below

## Workflow: New spreadsheet from structured data (data → create → format → share)

Proven on 40-row hoạt chất table (bảng chống tiêu chảy heo con → sheet gửi bên thu mua, 08/2026).

1. **Auth check + refresh token FIRST** — `setup.py --check` writes a refreshed token to `google_token.json`. Raw `urllib` calls with a stale token → 401. Always run `--check` immediately before a raw-API script.
2. **Build values array in Python** — `[header] + [[str(i), ...row] for i, row in enumerate(data, 1)]`, dump to a temp JSON file, then pass via `--values "$(python -c 'json.dumps(...)')"`. Reuses the same ROWS data as the HTML artifact — no retyping.
3. **Create sheet** via `gapi sheets create --title ... --sheet-name "..."`. Response gives `spreadsheetId`.
4. **Write values** — `gapi sheets update <ID> "SheetName!A1:F41" --values '[[...]]'`. Verify `updatedCells` = rows × cols.
5. **Format via raw Sheets API batchUpdate** (gapi CLI has no format commands) — read token from `C:/Users/NTQUANG_DELL/AppData/Local/hermes/google_token.json` (key `token`), call `https://sheets.googleapis.com/v4/spreadsheets/<ID>:batchUpdate` with urllib:
   - Freeze header: `updateSheetProperties` `gridProperties.frozenRowCount: 1`
   - Header bold + yellow: `repeatCell` with `backgroundColor` (1.0, 0.839, 0.0) + `textFormat.bold`
   - Wrap text: `repeatCell` `wrapStrategy: "WRAP"` on data columns
   - Column widths: `updateDimensionProperties` `pixelSize` per column
   - ⚠️ Need the REAL `sheetId` (integer) — fetch via `GET <ID>?fields=sheets.properties(sheetId,title)`.
6. **Append note rows** (FCR assumption, cảnh báo) at the bottom via `gapi sheets update` — important context for người nhận.
7. **Share** — `gapi drive share <ID> --type anyone --role reader` → anyone-with-link can view; user sends link to procurement/partners without permission requests.
8. **Verify** — `gapi sheets get` first rows; confirm link returns HTTP 200.

## Workflow: Drive folder → Inventory spreadsheet (scan → download → extract → OCR → verify → write)

Proven on "Thống kê các trại thử nghiệm Kiềm Saphia" (08/2026): scan 01_Khoa_Học_RnD drive folder → 25 trại → 12 cột sheet (+ Dashboard). Nguồn: một folder Google Drive chứa report .docx/.pdf chia theo năm.

1. **Auth** — `setup.py --check` first; confirm token scopes include `spreadsheets` + `drive`.
2. **Recursive scan = source of truth.** Build `drive.v3` from `~/AppData/Local/hermes/google_token.json`; per folder `files().list(q="'{id}' in parents and trashed=false", pageSize=1000)` and recurse. Dump full tree (name + id + mimeType) to a file. Items = trại/chủ thể; sub-folders/files = bằng chứng.
3. **Read README / _INDEX.md** for expected structure, but **never trust labels blindly** — see "Verify labels against content" pitfall.
4. **Download reports:** binary (.docx/.pdf) via `files().get_media` + `MediaIoBaseDownload`; Google-native docs via `files().export(mimeType=text/plain)`. **Do NOT call `.export()` on binary files** — 403 "Export only supports Docs Editors files".
5. **Extract text:** `.docx` → `python-docx` (paragraphs + tables); `.pdf` → `pypdf` `page.extract_text()`. Install deps with `python -m pip` NOT `pip` (pip maps to a different interpreter — silently installs to the wrong site-packages).
6. **OCR scans / image-only docs:** if extraction returns ~0 chars, it's scanned/images. Render PDF pages `pymupdf` `page.get_pixmap(dpi=200)`; pull embedded images from .docx via `zipfile` (`word/media/*.png|jpg`). OCR each PNG with **RapidOCR** (`rapidocr_onnxruntime`, PP-OCR, Vietnamese-capable) — reliable local fallback when `vision_analyze` aux model is down/401 or the subagent lacks vision. `RapidOCR()(path)` → `[box, text, score]`; join `r[1]`. Runs slow on CPU → background.
7. **Build sheet:** `gapi sheets create` or reuse existing; write `values().update(valueInputOption='USER_ENTERED')`; format via batchUpdate (correct request names — see Pitfalls).
8. **Share + verify:** `gapi drive share <ID> --email <owner> --role writer` and/or `--type anyone --role writer`; read back the written range to confirm cell alignment.

## Workflow: Thêm cột TÍNH TOÁN sống (live formulas) + block tham số

Khi user muốn sheet tự tính từ tham số nhập (vd: bảng hoạt chất TĂCN → cột "Lượng mua dự kiến" = số con × cám/con/ngày × số ngày × liều; chốt 15/08/2026 trên sheet 40 chất tiêu chảy heo con).

1. **Thiết kế 2 vùng**: cột dữ liệu tĩnh (liều tính g/kg) + cột công thức (lượng mua) + **block tham số vàng** ở cuối bảng (3-4 ô NHẬP: số con, cám/con/ngày, số ngày → ô TỔNG CÁM tự tính). Người dùng chỉ sửa ô vàng, cả bảng tự tính lại.
2. **Công thức dùng absolute ref vào ô tổng**: `=IF(ISNUMBER(J2),ROUND($K$50*J2/1000,2),"")` — `$K$50` là ô TỔNG CÁM. Viết qua `values().update` với `valueInputOption='USER_ENTERED'` để Sheets parse công thức (không phải 'RAW').
3. **⚠️ PITFALL self-reference #REF!**: công thức trong ô X mà tham chiếu chính ô X (vd `=K48*K49*K50` đặt TẠI K50) → `#REF!`. Phải tham chiếu đúng các ô NHẬP (vd `=K47*K48*K49`). Xác định số dòng chính xác bằng cách đếm: header(1) + N dữ liệu + dòng trống... trước khi viết công thức; kiểm tra lại bằng đọc FORMATTED_VALUE sau khi update.
4. **Hàng đặc biệt bỏ qua công thức**: chất không tính theo cám (vd ORS theo thể trọng) → ghi text literal "— (không trộn cám, tính riêng)" thay vì công thức, tránh IF lằng nhằng.
5. **Verify = đọc lại FORMATTED_VALUE**: `values().batchGet` với `valueRenderOption='FORMATTED_VALUE'` → tổng cám phải = con×cám×ngày, vài dòng mẫu phải = tổng × liều / 1000 (làm tròn ROUND đúng). Ghi chú quy đổi (FCR, premix CFU/g giả định) thành note row cuối bảng.

## Workflow: Điền dữ liệu vào sheet CÓ SẴN (báo giá / tài liệu → cột hiện có)

Proven 10/2026: 7 nguyên liệu từ bảng báo giá của user → tab "Thu mua" (14 cột) trong spreadsheet `1N5DvV0...` (Vua Kiềm - RnD + Lab), sau đó rút tiếp 14 mặt hàng thiếu từ 2 tài liệu R&D. Xem `references/procurement-gap-kiem-saphia.md`.

Khác với workflow "tạo sheet mới": ở đây KHÔNG được tự thiết kế cột — phải khớp vào cấu trúc người khác đã dựng.

1. **Read tab + header TRƯỚC khi map.** `values().get('Tab!A1:N30')` → biết tên cột thật và câu chuyện của sheet (đang là wishlist chưa điền, hay bảng đã có data). Không đoán cột từ tên file hay từ mô tả user.
2. **Đọc HẾT các tab khác, không chỉ tab đích.** Bước dễ bỏ qua nhưng quyết định chất lượng: sheet này có tab **"Tham chiếu"** chứa đúng **từ vựng trạng thái** hợp lệ của cột Trạng thái (`Chưa đặt → Đang chào giá → Chờ duyệt → Chờ đặt hàng → Đã đặt hàng → Đang giao → Đã nhận đủ → QC đạt → Đã nhập kho`). Ghi giá trị ngoài danh sách này phá dropdown/data-validation và làm lệch báo cáo sau. Tương tự: tab legend, tab quy ước đặt tên, tab lookup.
3. **Map item → dòng: khớp dòng cũ + append dòng mới.** Với bảng wishlist sẵn có: item trùng tên → điền vào dòng đó (giữ nguyên tên dòng để không phá cấu trúc quy hoạch); item chưa có → append cuối sheet. Ghi rõ trong báo cáo dòng nào match, dòng nào mới thêm.
4. **Chia VAT theo từng mặt hàng và verify tổng khớp nguồn.** User thường gửi tổng VAT gộp 1 dòng. Tính VAT/item = giá × tỷ lệ, cộng lại phải **đúng bằng** tổng user gửi. Làm phép tay trước khi ghi (vd 5.750.000 × 8% = 460.000 ✓; 5.750.000 + 460.000 = 6.210.000 ✓). Lệch 1 đồng = sai mapping, không phải làm tròn.
5. **Công thức tổng phải sống (SUMPRODUCT/SUM), không gõ số tĩnh** — user sửa giá là cả bảng tự tính lại. Dùng `valueInputOption='USER_ENTERED'` để Sheets parse công thức. Kiểm chứng bằng `valueRenderOption=FORMATTED_VALUE` sau khi ghi.
6. **Re-read range đích NGAY TRƯỚC mỗi lần ghi.** User thường mở sheet và tự sửa giữa lượt: điền cột STT, đổi trạng thái, xoá block. Snapshot vài phút trước → ghi đè mất data của họ. Đây là quy tắc bắt buộc, không phải tuỳ trường hợp. Nếu phát hiện họ đã sửa, dừng lại và cập nhật mapping trước khi tiếp.
7. **Không viết lại nội dung user đã xoá.** Họ xoá block tổng → đừng "tốt bụng" dựng lại. Có thể hỏi một lần ở cuối báo cáo, nhưng không tự làm.
8. **Không bịa NCC / COA / giá / nguồn gốc.** Nguồn không có thì để trống và nói rõ trong báo cáo. Số không nguồn = không số.
9. **Spec quan trọng ghi kèm trong cột "Tên cần"** khi sheet không có cột ghi chú — dạng `Tên hoạt chất  [liều — công thức dùng]`. Giữ tên gọn, đưa đầy đủ rationale vào reply.
10. **Format số + freeze header sau khi ghi xong.** `repeatCell` số `#,##0` cho cột giá; `updateSheetProperties` freeze hàng 1 — check trước, nếu đã frozen thì bỏ qua request thừa.

## Pitfalls
- **Token chết giữa phiên — `setup.py --check` lại TRƯỚC MỖI batch ghi.** Đừng refresh một lần rồi chạy cả loạt script. Phiên dài 10/2026 gặp 401 "Request had invalid authentication credentials" **hai lần**, mỗi lần đều ngay giữa lúc đang ghi. Nhận biết: JSON hợp lệ nhưng HTTP 401 — không phải lỗi mapping. Fix: chạy `python setup.py --check` rồi chạy lại **nguyên script** (script idempotent nên an toàn).
- **Ô chứa chuỗi bắt đầu bằng `=` bị Sheets hiểu là công thức → `#ERROR!`.** Text chú thích/legend kiểu `"= 2 kg / 5 kg per tấn"` nổ ngay. Viết thành `"2 kg premix : 5 kg/tan = 400 kg cam"` — **không bao giờ để ký tự đầu là `=`**. Triệu chứng: ô cùng hàng các ô khác vẫn đúng, chỉ ô đó `#ERROR!` → gần như chắc chắn là lỗi này.
- **Pattern số `#,##0.###` in ra dấu chấm thừa cho số nguyên (`28.`), không phải `28`.** Hai nguyên nhân cộng dồn: (a) nhiễu float từ `/100*2000` sinh `28.000000000000004`; (b) pattern có phần thập phân tuỳ chọn. Phải sửa CẢ HAI: bọc công thức trong `ROUND(x,3)` **và** đặt `numberFormat.pattern = "General"`. Đã thử và đo 10/2026 — `General` → `28`; `#,##0.###`, `0.###`, `#,##0.##`, `0.0##` đều ra `28.`/`28.0`. Lưu ý `ROUND` một mình KHÔNG đủ: pattern vẫn in dấu chấm.
- **`values:batchUpdate` bị 400 khi nhét `valueInputOption` + `data` vào body** ("Unknown name ... Cannot find field"). Đường bền: **PUT từng range** `values/{range}?valueInputOption=USER_ENTERED` với body `{"range": ..., "values": [...]}`. Đã verify 10/2026 trên 5 range liên tiếp (3 range×10 ô + 1 range×52 ô), `updatedCells` khớp đúng số ô mong đợi.
- **`updateDimensionProperties` is the correct batchUpdate request name** — `setDimensionProperties` → HTTP 400 "Unknown name ... Cannot find field". (Likely sibling: `updateSheetProperties` for freeze.)
- **Values vượt range → 400 "tried writing to row [N]".** A `!C9:L9` range given a 2-row values array fails because rows exceed the range. Write each cell separately (`!C9`, `!L9`) or size the array exactly to the range.
- **Export ≠ download.** `files().export()` throws 403 on binary .docx/.pdf ("Export only supports Docs Editors files"). Always `get_media` + `MediaIoBaseDownload` for binaries.
- **Verify folder/INDEX labels against report CONTENT.** In the Kiềm Saphia drive, INDEX (and some folder names) were stale/wrong: N.V Hưng listed "bò sữa" but the report is GÀ 3000 con; Đồng Đức Vọng "tôm Cà Mau" but actually GÀ lai chọi 1000 con at Gia Lộc, HD; Dabaco "250 gà" but actually LỢN thịt 368 con trại Lạc Vệ; ĐH Cần Thơ "tôm" but actually CÁ TRA. Read the actual report before trusting a name — a stale label silently corrupts the inventory.
- **RapidOCR is slow on CPU** — a 22-page scanned PDF took ~10-25 min. Run OCR in `background=true` + `notify_on_complete` and continue other work; don't block on it.
- **execute_code sandbox ≠ terminal python.** `pip install pymupdf` in terminal does NOT make it importable inside execute_code. Run extraction/write scripts via terminal heredoc, not execute_code.
- **Quoted heredoc preserves Vietnamese diacritics.** Use `python - <<'PYEOF'` (single-quoted delimiter). Unquoted heredoc strips/expands content.
- **⚠️ But an APOSTROPHE inside the heredoc kills the whole script before Python runs.** Content like `Xi'an Rongsheng` → bash `unexpected EOF while looking for matching '` and *nothing* executes (silent-looking: the error arrives as a shell error, not a Python traceback). Same class of failure for other shell metacharacters in payload text (supplier names, quoted phrases). **When the payload contains apostrophes, stop using the heredoc: `write_file` the script to a `.py` file and run `python <path>`.** This also sidesteps the occasional diacritics mangling the heredoc suffers. Cost: one wasted call; the fix is instant once recognised.
- **Writing past `columnCount` fails.** A tab whose grid is 14 columns rejects a write to column O — the error names the range, not the grid, so it reads like a mapping bug. Widening is a separate call first: `batchUpdate` → `{"appendDimension":{"sheetId":SID,"dimension":"COLUMNS","length":6}}`. Always read the real grid via `?fields=sheets.properties(sheetId,title,gridProperties(rowCount,columnCount))` before adding analysis columns to a sheet built by someone else.
- **Nested batchUpdate bodies: assign the dict to a variable, never inline it.** A hand-nested `{"requests":[{"addSheet":{"properties":{...}}}]}` literal miscounted a brace → `SyntaxError: closing parenthesis ']' does not match opening parenthesis '{'`, which wastes a round trip and looks like an API error. Write `body = {...}` across lines, then `call(url, body, "POST")`.
- **A dict keyed by row number is an off-by-one waiting to happen — always read back and cross-check TWO columns.** When mapping sheet rows → values, one skipped/mis-indexed key silently mislabels *every* row after the gap. Seen 10/2026: a Vitamin E row got the RS-01 flags, a sodium-ascorbyl-phosphate row got another material's, and the shift ran 9 rows to the end of the block. Detection that actually caught it: after writing, read the range back and assert the *name* column pairs with the intended *marking* column for a handful of known rows — `assert g(38, name_col).startswith("Vitamin E") and g(38, MT01_col) == "THIẾU"`. Then recount each column independently in Python and compare to the sheet's own formulas; a mismatch localises the shift immediately. **Never trust a mapping dict you wrote without this check.**
- **Diacritics sneak in as ASCII.** A payload authored ASCII-first ("Mat hang", "Uu tien") writes clean, wrong text into the sheet and violates the hard requirement that Vietnamese always carries dấu. `write_file` + run-file avoids the encoding loss, but the real guard is the final verification step: read back a few *text* columns and eyeball the dấu, not just the counts. Renaming a tab to fix it is a one-liner (`updateSheetProperties` `fields: "title"`), but the cell payload needs a full re-write.
- **Large write_file → stream timeout.** Do NOT retry the same big call; chunk into smaller writes or inline heredoc.
- **Sheet IDs**: a spreadsheet with custom tab names has no grid id 0; always fetch the real sheetId.
- **fields param syntax**: `GET ?fields=sheets(sheetId,properties.title)` → HTTP 400 "Cannot find matching fields for path 'sheets.sheetId'". Correct: `?fields=sheets.properties(sheetId,title)`.
- **Token path (Windows)**: load creds from `C:/Users/NTQUANG_DELL/AppData/Local/hermes/google_token.json` via `Credentials.from_authorized_user_info`; refresh with `creds.refresh(Request())` when expired.

## Technique: status matrix với header tự đếm (live COUNTIF) + conditional formatting

Dùng khi cần cột đánh dấu kiểu "Đã có / THIẾU" mà người dùng sẽ điền tiếp về sau (đối chiếu nguyên liệu theo dòng sản phẩm, checklist tiến độ, gap matrix). Proven 10/2026: 5 cột O–S cho 5 dòng công thức trên tab "Thu mua".

1. **Header tự đếm bằng công thức chuỗi**, ghi với `USER_ENTERED`:
   `'="RS-01 Hô hấp: còn "&COUNTIF(O2:O46,"THIẾU")&" dòng thiếu"'`
   Tự cập nhật khi trạng thái đổi. **Không** gõ số tĩnh — nó lệch ngay sau lần user mua thêm hàng.
2. **Tô màu bằng RULE, không tô tĩnh**: `addConditionalFormatRule` + `booleanRule` + `condition.type` `"TEXT_EQ"` (hoặc `"TEXT_CONTAINS"` nếu ô chứa nhiều biến thể). Format sẽ đi theo giá trị khi ô đổi sau này — `repeatCell` + `backgroundColor` thì không.
   ```python
   {"addConditionalFormatRule": {"rule": {
       "ranges": [{"sheetId": SID, "startRowIndex": 1, "endRowIndex": 46,
                   "startColumnIndex": 14, "endColumnIndex": 19}],
       "booleanRule": {"condition": {"type": "TEXT_EQ",
                                     "values": [{"userEnteredValue": "THIẾU"}]},
                       "format": {"backgroundColor": {...}, "textFormat": {"bold": True}}}},
     "index": 0}}
   ```
   `index` thấp hơn = ưu tiên cao hơn khi nhiều rule chồng nhau.
3. **Tạo tab mới / đổi tên tab**: `addSheet` → `{"requests":[{"addSheet":{"properties":{"title":"Tên tab","gridProperties":{"rowCount":80,"columnCount":9}}}}]}`, lấy `sheetId` từ `replies[0].addSheet.properties.sheetId`. Đổi tên sau: `updateSheetProperties` với `fields: "title"` (dùng khi payload viết thiếu dấu).
4. **Wrap + căn giữa + độ rộng cột** cho khối mới: `repeatCell` `wrapStrategy: "WRAP"` + `horizontalAlignment`, rồi `updateDimensionProperties` `pixelSize` cho từng cột (cột ghi chú cần rộng 350–400px mới đọc được).
5. **Kiểm chứng cuối**: đếm lại từng cột bằng Python từ dữ liệu đọc về, so với con số công thức trong header. Hai nguồn độc lập khớp nhau mới coi là đúng — đây chính là bước bắt được lỗi lệch dòng.

## Support files
- `scripts/list_tabs.py` — print tab titles + sheetIds for a spreadsheet ID (run first).
- `references/vuakiem-catalog-session.md` — worked example: PDF extraction + chunked fill + EZ67 row + product facts.
- `references/drive-folder-inventory.md` — worked example: Drive folder → trại inventory sheet (recursive scan, download, text-extract, RapidOCR, label-verification, sheet write).
- `references/procurement-gap-kiem-saphia.md` — worked example: rút 14 mặt hàng thiếu từ 2 tài liệu R&D (23 công thức + bảng chất chuẩn pH 8–9). **Chứa checklist dạng nguyên liệu** (Berberine HCl ≠ chiết xuất hoàng liên, Na-selenite ≠ Selenium Yeast, propolis glycolic ≠ ethanol, enzyme coated, Vitamin E TPGS, Vitamin C → SAP) — mua nhầm dạng là thiêu công thức, không bù liều được.

## Verification
1. `values().get` the written range; confirm row count matches what was written.
2. Confirm header bold + highlight was applied (read back or visual check).
