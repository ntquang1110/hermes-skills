# Worked example: Vua Kiềm catalog → Google Sheets (10/08/2026)

Session pattern: user handed a 155MB catalog PDF and wanted product data in a
spreadsheet, with a demo tab approved before full rollout.

## Steps that worked
1. **PDF extraction**: `pip install pymupdf` then `doc[i].get_text()` per page →
   `catalog-29042026-extracted.txt` (26KB from 20 pages). Run via terminal, NOT
   execute_code (sandbox interpreter lacks the package even after pip install).
2. **Auth**: `setup.py --check` returned `AUTHENTICATED (partial)` missing
   gmail/calendar scopes — still fine for sheets (drive+sheets present).
3. **Metadata first**: `spreadsheets().get()` to list tabs. First attempt with
   `Sheet1!A1` failed HttpError 400 "Unable to parse range" — real tab was named
   "Sản phẩm". Always list tabs before reading/writing.
4. **Create tab**: `batchUpdate` with `addSheet` → reply carries the new sheetId
   (e.g. 1134790297). Capture it for formatting later.
5. **Chunked fill**: one `values().update` per product group (3-5 products each)
   via `python - <<'PYEOF'` heredoc through terminal. Quoted delimiter preserves
   Vietnamese diacritics. Never one giant update (stream timeout).
6. **Format**: `repeatCell` bold + yellow header using the REAL sheetId.
   Sheet id 0 fails: "No grid with id: 0".
7. **Verify**: read back range, print STT | name | price per row before reporting.

## Domain facts (Vua Kiềm / Kiềm Saphia)
- Catalog PDF: `D:\VuaKiem\Catalog\29042026.pdf` (20 trang, 11 sản phẩm)
- EZ80 = "Kiềm EZ Tái sinh 80" (bột, 1.250.000đ/10kg, gia súc 5kg/tấn TĂ)
- EZ67 = sản phẩm MỚI chưa vào catalog, DẠNG NƯỚC, điều trị dịch tả
  (Quang xác nhận 10/08). Closest catalog item is KIỀM EZ 300 (2.000.000đ/10kg,
  gia súc 7kg/tấn, gia cầm 10kg/tấn, điều trị 7-10 ngày) but EZ67 ≠ EZ 300.
- 4 nhóm thành phần khi phân loại:
  1. Hoạt chất thiên nhiên: Saponin, Polyphenol, Flavonoid, Glycosid,
     Polysaccharide, Triterpenoid, Alkanoid
  2. Khoáng: Ca, Fe, Mg, K, Mn, Zn, Cu, P, Đạm, Bor, Na, Al
  3. Thảo dược: bột thảo mộc hoạt hóa (mần trầu, bướm trắng, cỏ voi, xuyên chi,
     cỏ tranh, cỏ gân gà), chiết xuất thảo mộc
  4. Khác: độ ẩm, chất hữu cơ tổng số, chất mang (Talc, Diatomite, cao lanh,
     vỏ hàu, nước RO), pH

## Sheet IDs in play
- Spreadsheet cũ (tài liệu bán hàng): `<SHEET_ID>`
  - Tab "Sản phẩm" gid 2118893758 (12 sản phẩm, EZ67 hàng 13)
  - Tab DEMO "Thành phần chi tiết" gid 472640767
- Spreadsheet mới (catalog 29042026): `<SHEET_ID>`
  - Tab "Sản phẩm" (8 cột) + tab "Danh mục chi tiết" sheetId 1134790297

## Google token (Windows)
- Path: `C:/Users/NTQUANG_DELL/AppData/Local/hermes/google_token.json`
- Credentials.from_authorized_user_info + refresh(Request()) when expired.
