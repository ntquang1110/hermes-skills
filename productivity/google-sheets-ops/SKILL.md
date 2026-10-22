---
name: google-sheets-ops
description: "Use when editing or auditing Google Sheets via API."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [google, sheets, api, spreadsheet, formula, formatting]
---

# Google Sheets API Ops

Raw Sheets API operations (metadata, read/write ranges, formulas, formatting) when the `google-workspace` CLI wrapper isn't enough — e.g. `batchUpdate` formatting, formula writing, or multi-column updates. Auth uses the same `google_token.json` as google-workspace.

## When to use

- Add/edit columns, write formulas into a spreadsheet programmatically
- Format ranges (colors, wrap, width, freeze) via `batchUpdate`
- Need the actual tab name / sheetId (always — see pitfalls)
- Building a calculation sheet with user-input parameter blocks

## Rule 0 — NEVER report a sheet write you have not read back

This is the highest-severity failure mode in this skill, and it has happened twice.

1. **Do not invent a spreadsheet URL or ID.** A plausible-looking
   `https://docs.google.com/spreadsheets/d/<random>/edit` string is indistinguishable from a real one
   to the user until they click it and get a 404. If you did not receive an ID from metadata, from a
   `create()` response, or from the user, you do not have one — say so instead of generating one.
   Real session: user replied *"Cái link Google Sheets này nhé, anh không vào được"*.
2. **Do not say "Đã thêm / Done / Xong" until you have re-read the target range in the SAME
   script run as the write and printed the rows back.** Real session: assistant reported adding 8
   construction items to a tab; the tab was verified empty on the next read. The user asked
   *"anh có thấy đâu nhỉ"*. A write call returning `{'success': True}` is not evidence the cells hold
   what you intended — the tab may not exist, the range may be wrong, or the call may never have run.
3. **Re-verify the tab exists before writing to it.** If the user names a tab (`"Lab - Thi công"`),
   fetch metadata and confirm the title matches exactly (including spaces and hyphens). Do not assume
   a similarly-named tab is the target, and do not write into a different tab and call it done.
4. **If a claim turns out to be wrong, state it plainly in one line and redo the work.** Do not
   quietly re-run and pretend the first attempt never happened. Quang explicitly values this: a
   straight "lượt trước em bịa, lần này ghi thật" costs nothing; a second unverified "Done" costs trust.

Preferred closing move: end the reply with a real, verifiable artifact — the sheet URL the user gave
you, the exact range written, and a pasted sample of the rows read back.

## User convention — add a tab, never create a new file

For Vua Kiềm / Manna Đất Vàng work, all new material goes into the EXISTING budget/tracking
spreadsheet as an additional worksheet. Do **not** propose or create a new spreadsheet.
Quang: *"anh không cần Sheet mới đâu, em vào cái Sheet cũ đó và cập nhật thêm một worksheet mới
ở trong đó, nhưng vẫn giữ file cũ."* Existing tabs are never deleted, renamed, or reordered to make
room — add at the end via `addSheet` and leave everything else untouched.

## Setup / auth (python)

```python
import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
tok = json.load(open('C:/Users/NTQUANG_DELL/AppData/Local/hermes/google_token.json', encoding='utf-8'))
creds = Credentials.from_authorized_user_info(tok)
svc = build('sheets', 'v4', credentials=creds)
```

## Step 1 — ALWAYS fetch metadata first

```python
meta = svc.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
print(meta['properties']['title'])
for s in meta['sheets']:
    print(s['properties']['title'], s['properties']['sheetId'],
          s['properties']['gridProperties'].get('rowCount'))
```

You need TWO things you cannot guess: the **tab name** (for `values().get/update` ranges) and the **numeric sheetId** (for `batchUpdate` formatting). See pitfalls.

## Step 2 — read / write values

```python
# read
res = svc.spreadsheets().values().get(spreadsheetId=SHEET_ID,
    range='Hoạt chất!A1:I41').execute()
rows = res.get('values', [])

# write (USER_ENTERED so formulas evaluate)
svc.spreadsheets().values().update(
    spreadsheetId=SHEET_ID, range='Hoạt chất!J1:K51',
    valueInputOption='USER_ENTERED', body={'values': values}).execute()

# read BOTH formulas and computed values
svc.spreadsheets().values().batchGet(spreadsheetId=SHEET_ID,
    ranges=['Hoạt chất!J1:K51'], valueRenderOption='FORMATTED_VALUE').execute()
```

## Step 3 — formatting via batchUpdate

```python
requests = [
  {'updateDimensionProperties': {'range': {'sheetId': sid, 'dimension': 'COLUMNS',
    'startIndex': 6, 'endIndex': 9}, 'properties': {'pixelSize': 320}, 'fields': 'pixelSize'}},
  {'repeatCell': {'range': {'sheetId': sid, 'startRowIndex': 0, 'endRowIndex': 41,
    'startColumnIndex': 6, 'endColumnIndex': 9},
    'cell': {'userEnteredFormat': {'wrapStrategy': 'WRAP', 'verticalAlignment': 'TOP'}},
    'fields': 'userEnteredFormat.wrapStrategy,userEnteredFormat.verticalAlignment'}},
  {'repeatCell': {'range': {'sheetId': sid, 'startRowIndex': 46, 'endRowIndex': 52,
    'startColumnIndex': 9, 'endColumnIndex': 11},
    'cell': {'userEnteredFormat': {'backgroundColor': {'red': 1.0, 'green': 0.96, 'blue': 0.78}}},
    'fields': 'userEnteredFormat.backgroundColor'}},
  {'updateSheetProperties': {'properties': {'sheetId': sid,
    'gridProperties': {'frozenRowCount': 1}}, 'fields': 'gridProperties.frozenRowCount'}},
]
svc.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID, body={'requests': requests}).execute()
```

Color map (0-1 floats): xanh nhạt A (0.72,0.89,0.72), vàng nhạt B (1.0,0.95,0.72), xám C (0.88,0.88,0.88), header vàng đậm (1.0,0.84,0.0).

## Pitfalls (all hit in real sessions)

1. **Tab name is NOT "Sheet1"**. Vietnamese sheets get named like "Hoạt chất", "Tong hop cau hoi". `values().get(SHEET_ID, 'Sheet1!A1')` → `HttpError 400 Unable to parse range`. Always read the real tab name from metadata.
2. **sheetId is NOT 0**. `batchUpdate` with `sheetId: 0` → `HttpError 400 No grid with id: 0`. Real sheetIds are arbitrary integers (e.g. 1887479623) from metadata. Get it, don't guess. (Caveat: a sheet may legitimately report sheetId `0` — I've hit one. Always read it from metadata, never assume one way or the other.)
2b. **Never trust the described/assumed header — read the live rows before inserting columns.** Task specs and user descriptions often give a *simplified single-row* header (e.g. "22 columns A–V") that does NOT match reality. Real lab sheets commonly use a **two-row header** (row 1 = merged group cells like `Thông tin mẫu`/`Khoáng`/`Kim loại nặng`; row 2 = column names) plus extra columns not in the description (`Na`, `Se`, compound/`-side` columns). Before adding new columns at an assumed index, re-read `A1:Z3` AND the sheet's `merges` metadata, then recompute the insert position against the columns ACTUALLY present.
3. **Formula self-reference → #REF!**. Writing `=K48*K49*K50` INTO cell K50 references itself → `#REF!`. When appending a parameter block BELOW data rows, recompute absolute refs carefully; an off-by-one (`$K$51` vs actual `$K$50`) silently produces `#REF!` or wrong totals on every data row.
4. **Use `valueInputOption='USER_ENTERED'`** for formula writes — default RAW stores formulas as literal text.
5. **Empty rows in a range**: `.get()` returns fewer rows than the range if trailing cells are empty; pad with `[]` before `update` so the payload length matches (or use `while len(values) < N: values.append([])`). **Only safe for padding at the END** — an `[]` row in the MIDDLE of a payload is silently dropped and shifts every row below it up. See pitfall 11.
6. **Network timeouts happen** (`WinError 10060` / `TimeoutError` on `svc...execute()`). Retry the same call ONCE — it's usually transient, not an auth/permission problem. EXCEPTION: if the traceback ends inside `reauth.refresh_grant` / `_token_endpoint_request_no_throw` (token refresh, not the Sheets call) AND it fails twice in a row, stop retrying and switch to the export fallback (`references/sheets-export-fallback.md` + `scripts/sheets_export_fallback.py`) — the oauth2 endpoint is unreachable while docs.google.com still works. Diagnose with `nslookup oauth2.googleapis.com` vs `curl https://www.google.com`.
7. **Verify after write**: read back with `FORMATTED_VALUE` and spot-check computed formula results (e.g. 100 con × 0.5 kg × 30 ngày → 1500 kg) — never assume formulas evaluated correctly. When auditing via the xlsx fallback, load with `data_only=False` so formula cells show as `'=SUM...'` strings — this is how cross-column SUM bugs (e.g. `H11=SUM(G10:H10)` instead of `SUM(B11:G11)`) get caught.
8. **`google_token.json` 'expiry' may be a float epoch, not an ISO string** → `Credentials.from_authorized_user_info` raises `AttributeError: 'float' object has no attribute 'rstrip'`. Fix before building creds:
   ```python
   import datetime
   if isinstance(tok.get('expiry'), (int, float)):
       tok['expiry'] = datetime.datetime.fromtimestamp(tok['expiry'], tz=datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
   if isinstance(tok.get('expires_in'), float):
       tok['expires_in'] = int(tok['expires_in'])
   ```
9. **Creating a NEW spreadsheet**: `svc.spreadsheets().create(body={'properties':{'title': TITLE}})` → returns `spreadsheetId` + `spreadsheetUrl`. Do a follow-up `get` to read the first tab's numeric sheetId (never assume 0). To set it up cleanly: rename the default tab via `updateSheetProperties` (`fields:'title'`), write the header row, then one `batchUpdate` for freeze (`frozenRowCount:1`) + bold colored header + per-column widths. See `scripts/make_kiemnghiem_sheet.py` for a full working skeleton.

10. **Vietnamese comma-decimals can be misparsed by `USER_ENTERED`.** A sub-1.0 value like `"0,108"` may be ingested as a number that reads back as `108` (locale treats the comma as a thousands/group separator). After every bulk write, `batchGet` with `valueRenderOption='FORMATTED_VALUE'` and spot-check every sub-1.0 / `<x,y` cell against the source. If one reads wrong (e.g. `108` instead of `0,108`), re-write that single cell with `valueInputOption='RAW'` to force it to stay literal text. Applies to any sheet holding lab/soil VN decimals (`<0,1`, `1,994`, `0,108`, `0,51`).

11. **`[]` spacer rows in the MIDDLE of a payload are dropped, silently shifting everything below up.**
    Writing `[[...],[],[...],[...]]` makes your 3rd row land on the row you meant for the 4th and every later
    row shifts by one — no error is raised. Real symptom: two rows both read back as `TỔNG CHI` and two as
    `NGUỒN VỐN`, because the stale rows underneath were never overwritten. Fix: use **explicit blank strings**
    for spacer rows (`['','','','','','','','','','']`), never `[]`. If the tab already holds content, run
    `values().clear()` over the full window first, then write the whole block in one call.

12. **Range length must equal payload length — compute it with `len()`, never by hand.**
    Error: `Requested writing within range ['Tab'!A1:F18], but tried writing to row [19]`. Hand-counting a
    20-row block is the easiest way to burn a round trip; it happened twice in one session. Derive the end row
    from `len(block)`, or assert it immediately before the call.
    **And the range WIDTH must equal the payload width too** — that check is separate and it fails
    independently: writing 7-column rows into `A1:G25` while some rows carry 8 values →
    `Requested writing within range ['Tab'!A1:G25], but tried writing to column [H]`. Build the range string
    from the data (`end_col = col_letter(max(len(r) for r in block))`) instead of typing it, or trim/extend
    every row to a fixed width first. A ragged list is the usual cause — pad all rows to the same length.

12b. **⚠️ NEVER rewrite a whole block from an in-memory copy when the user has edited the sheet.**
    This is the single most destructive mistake in this skill. The failure mode: you build `data` at time T,
    the user goes and edits the sheet (adds a column, fills a cell, renames a header), you then `update()` the
    full range with your **stale T snapshot** — and every change the user made is silently destroyed. Real case:
    a 12-row property table lost its entire `Link` column because the rewrite was assembled from the original
    hand-built list, not from a fresh read. The user noticed immediately ("sao mất hết link của anh r").
    **Rules:** (a) re-read the target range immediately before every write — the read must be in the same
    script run as the write, not cached from earlier in the session; (b) when adding columns to a live,
    user-edited sheet, write ONLY the new/changed cells (`update` per column or per row) — never the full
    `A1:Z` window; (c) full-block rewrites are only safe on a sheet you created and nobody else has touched.
    See `references/append-columns-to-live-sheet.md`.

12c. **Pairing a separate lookup list with data rows is off-by-one when a header exists.**
    Building `links = ['', 'http://a', 'http://b', ...]` and then zipping `links[i]` against `rows[i]` (where
    `rows[0]` is the HEADER) shifts every link up one row — row 1 silently gets an empty link and the last real
    link is dropped. Either index with `i+1`, or make `links` headerless and use `links[i-1]`. When in doubt,
    assert that a known link lands on the right row before writing.

12d. **Map column letters from the LIVE header, not from your assumption of the original layout.**
    When appending "Người liên hệ / SĐT / Trạng thái", the user had already inserted a `Maps` column, so the
    real header was `[... Ghi chú, Maps, Người liên hệ, SĐT]` — not the 11-column layout I had in my head.
    Writing to "column M = Người liên hệ" landed on `Maps`. Read the header row, build a
    `{name: column_letter}` map, and address cells by resolved letter. If the target column already exists,
    UPDATE it in place instead of appending a duplicate.

13. **After any insert/delete of rows, re-read with `valueRenderOption='FORMULA'` and REWRITE the formulas.**
    Absolute refs baked into formulas written before the structural change go stale. Real case: a
    `% Ngân sách` column written as `=H2/$H$13` kept pointing at `$H$13` (the reserve row) after an insert
    moved `TỔNG CHI` to row 12, so the whole column read `1.72` instead of `0.26`. Same for the total itself:
    rewrite `=SUM(B2:B10)` explicitly to cover a newly inserted row instead of trusting Sheets to
    auto-adjust. Then assert the percent column sums to 1.0, and scan every tab for cells starting with `#`
    (formula errors) before declaring done.

14. **A closing-balance row is not `previous_total − this_total`.** Writing `=B15-C12`, `=C15-D12`, ... gives
    negatives from month 2 onwards, because only the first cell holds the opening balance. Write a true
    running balance: `=B15-B13`, then `=B16-C13`, `=C16-D13`, ... — each cell references the cell to its LEFT
    in the same row, and the first cell references the account-balance row above.

15. **Structural edit recipe** (used to repair a budget sheet that was missing a whole cost line): rewrite the
    target block in ONE `update` with explicit blanks, re-derive every absolute ref, then re-read FORMULA and
    FORMatted values for the whole tab, then `batchUpdate` the formatting. Doing it in that order means one
    verification pass catches both wrong numbers and wrong refs. See
    `references/budget-plan-sheet-pattern.md`.

16. **A large `execute_code` payload dies mid-stream — chunk it, don't retry it.** Writing a 48-row
    Vietnamese table (two long prose columns) inline in one `execute_code` call produced
    *"Your previous tool call (execute_code) was too large and the stream timed out before it could be
    delivered"*, and the retry with the same content failed the same way. Limits are on the **tool-call
    arguments**, not on what Sheets will accept.
    **Two-part fix:**
    (a) Put the bulk Vietnamese text in a **data file written by `write_file`** (UTF-8 JSON, `{row_number:
    [col_a_text, col_b_text]}`), then load it inside `execute_code` with `json.load(...)` and push in one
    `update`. Data files are not tool-call arguments, so size is not an issue.
    (b) Split the sheet write itself into **several smaller `update` calls** (e.g. 4–5 rows per call, each range
    computed with `len()`). Verify the row→data coverage afterwards by comparing the sheet's item column
    against the JSON keys and printing any missing row numbers.

17. **Never hand-type long Vietnamese strings directly into a `execute_code` source string.** Doing so
    corrupted characters twice in one session: `dung môi` → `dung môc`, `Thiết bị` → `Thiét bị`, and a
    string that ran off the line produced an unterminated-literal `SyntaxError` mid-payload. The module-level
    string was silently mangled and only caught by reading it back from the sheet. Write the text with
    `write_file` (or build it from a dict), load it, and then read the written range back and eyeball a sample
    for mangled diacritics — Vietnamese is the failure case, not ASCII.
    Same rule applies to `setDataValidation`: `strict` and `showCustomUi` are **not valid keys** on
    `setDataValidation` in the Sheets v4 REST API and produce
    `Invalid JSON payload received. Unknown name "strict"` / `Unknown name "showCustomUi"`. Use only
    `condition` and `inputMessage` — e.g. `{'condition': {'type': 'BOOLEAN'}}` for checkbox columns, or
    `{'condition': {'type': 'ONE_OF_LIST', 'values': [{'userEnteredValue': '1'},
    {'userEnteredValue': '0'}]}}` for a 0/1 enum column.

18. **`values:batchUpdate` (multi-range POST) is unusable here — write whole ranges with `values().update` instead.**
    `POST /v4/spreadsheets/{id}/values:batchUpdate` with body `{'valueInputOption': ..., 'data': [...]}`
    returns `HTTP 400 — Invalid JSON payload received. Unknown name "valueInputOption": Cannot bind query
    parameter. Field 'valueInputOption' could not be found in request message.` followed by
    `Unknown name "data": Cannot find field.` Moving `valueInputOption` into the query string
    (`...:batchUpdate?valueInputOption=USER_ENTERED`) fails identically.
    **Working alternative: one `values().update` (PUT) per range, batched BY COLUMN** — a single PUT
    carrying a list of per-row values covers 100+ cells in one call. Rewriting 99 formulas + 28 summary
    formulas took 4 PUTs. Build the per-row list in Python (`[['=ROUND(...)'] for i in range(a, b+1)]`).

19. **⚠️ `numberFormat` patterns with OPTIONAL decimals render whole numbers with a trailing dot.**
    `0.###`, `#,##0.###`, `#,##0.##`, `0.0##` all render `28` as **`28.`**, `10` as `10.`, `6` as `6.`
    Verified by writing one value, applying each pattern, and reading back with
    `valueRenderOption='FORMATTED_VALUE'`. **The cell values were correct — only the display was wrong.**
    `ROUND(...,3)` does NOT fix it; the pattern itself causes it.
    **Fix: `{'numberFormat': {'type': 'NUMBER', 'pattern': 'General'}}`** → renders `0.6`, `6`, `28`,
    `45135.8` cleanly. Reserve fixed patterns (`0.0000`) for columns where every value should carry decimals.
    Apply `General` to a mixed-precision column (grams needed: 0.6 g and 200 g in the same column).

20. **A cell whose TEXT starts with `=` is parsed as a formula → `#ERROR!`.**
    Writing the note `"= 2 kg premix / 5 kg/tấn = 400 kg cám"` produced `#ERROR!` in the cell.
    Fix: never start explanatory text with `=` — rephrase (`"2 kg premix : 5 kg/tấn = 400 kg cám"`),
    or write that one cell with `valueInputOption='RAW'`. After any write that mixes prose and formulas in
    the same range, scan the read-back for `#ERROR!` / `#REF!` before reporting done.

21. **`HTTP 401 UNAUTHENTICATED` on a write = stale token, not a bad ID or range.** Refresh before
    debugging anything else:
    `cd ~/AppData/Local/hermes/skills/productivity/google-workspace/scripts && python setup.py --check`
    → prints `AUTHENTICATED: Token refreshed at ...google_token.json`. Then re-run the write unchanged.
    Don't start second-guessing ranges/sheetIds until the token is confirmed fresh.

22. **⚠️ NEVER insert rows into the MIDDLE of a user-maintained block — add a new tab instead.**
    Real case 21/10/2026: sheet `VK – RnD + Lab` (id `<SHEET_ID>`), tab
    `Định mức & Lượng mua` holds PHẦN 1 (rows 9–107 = 23 công thức × nguyên liệu) and PHẦN 2 (rows 110+,
    procurement, whose totals SUM over PHẦN 1). Adding new formula rows inside PHẦN 1 would silently break
    PHẦN 2 — Sheets SUM ranges do NOT auto-extend over inserted rows. Correct move: `addSheet` a NEW tab in the
    SAME spreadsheet (user convention: never a new file — see above), **mirror the existing tab's column
    semantics and its section headers** (`PHẦN 1 — ĐỊNH MỨC` / `PHẦN 2 — ĐIỂM` / `PHẦN 3 — ĐÓNG GÓI` /
    `PHẦN 4 — CÒN NỢ`) so the user recognises the layout, and leave the user's blocks untouched. Then report
    the new gid.

23. **User names a tab/sheet that doesn't exist → probe ALL candidates, pick a documented default, ASK at the end. Never write somewhere else silently.**
    Real case 21/10/2026: Quang (voice note) said *"các công thức cũng bổ hết ra ở trong Change Sheet"*. `spreadsheets().get(...fields='sheets.properties.title')` across the three candidate files
    (VK – RnD + Lab · VK – Phát triển công thức · VK – Sử dụng cho heo) → **no tab or file title contains "Change"**.
    Recipe: (a) probe metadata of every candidate and print `title → [tabs]`; (b) say plainly *"không có tab/tên nào là X"* +
    the list you checked — do not guess and do not stall; (c) choose the tab whose **semantics** match
    (here: the sheet holding the per-ingredient định mức block), state why in one line; (d) close with a one-line
    offer to move it (`anh muốn chuyển sang <file> thì nói, em đổi trong một lượt`). Voice-STT mangles proper names —
    see memory rule: search first, 0 hits → clarify with options, không đoán.

## Efficient pattern

Build the full payload (values or request list) locally first, then push in ONE `values().update` / `batchUpdate` — avoids many round trips and makes the diff reviewable. For multi-column calculation sheets, generate the value grid with a Python script from a JSON data map (see session pattern: `build_payload.py` style), then single-update.

**Exception — big blocks of Vietnamese prose must be chunked.** See pitfall 16.

## Support files

- `scripts/sheets_probe.py` — dump spreadsheet metadata (title, tab names, sheetIds, grid sizes) for any SHEET_ID. Run first when you don't know the tab structure.
- `scripts/append_columns_live.py` — safe append/update of columns on a LIVE user-edited sheet: reads fresh, maps column names → letters from the live header, writes per column with `RAW`, re-attaches data validation. Use whenever adding columns to a sheet the user has touched. Recipe + pitfalls in `references/append-columns-to-live-sheet.md`.
- `scripts/sheets_export_fallback.py` — read-only full dump without Sheets API (enumerate gids → CSV per tab → xlsx → content dump with formulas). Use when pitfall 6's oauth2-unreachable case hits. Details in `references/sheets-export-fallback.md`.
- `references/budget-plan-sheet-pattern.md` — multi-tab budget/plan workbook pattern: tab architecture (Tổng quan / Chi tiết Tháng N / Tham chiếu ngân sách / Nhân sự / R&D Q4 / Timeline), the `1b` expansion-row convention for baseline-vs-plan, the TỔNG CHI + DỰ PHÒNG + running-balance formula set, batchUpdate formatting helpers + colour map, a 5-point audit checklist for inheriting someone else's budget sheet, and the critique→HTML review→deploy workflow. Dùng khi Quang yêu cầu ngân sách/kế hoạch nhiều tab.
- `references/cong-tac-phi-pattern.md` — pattern sheet công tác phí theo định mức công ty (Manna Đất Vàng): định mức chính thức (2.000đ/km xe máy, 4.000đ/km ô tô, lưu trú 450k/đêm, phụ cấp 130k/ngày, tạm ứng 12,6tr/tháng...), cấu trúc 4 sheet (Nhật ký / Định mức / Tạm ứng đối soát / Báo cáo), công thức lookup+SUMIFS, cách lấy Google Doc public bằng curl export (nhớ Windows /tmp pitfall), câu hỏi chốt trước khi tạo. Dùng khi Quang yêu cầu bảng chi phí/đi lại/tạm ứng.
- `references/procurement-crosscheck-and-links.md` — đối chiếu cột tick (`Pick?`) ở sheet master với các dòng đã có ở sheet thu mua, chỉ append phần chênh lệch, đi tìm link mua thật (danh sách NCC VN tin được), cặp cột quyết định `Tác dụng trong quy trình` / `Nếu KHÔNG có thì sao`, và cách đối chiếu tổng chi với ngân sách đã cấp. Dùng khi Quang nhờ lọc danh sách thu mua / vật tư.
- `references/product-formulation-sheet-pattern.md` — pattern sheet công thức sản phẩm: cấu trúc tab, workflow tạo/ghi/format, pitfalls riêng (tên tab có dấu, số thập phân kiểu VN).
- `references/premix-dinh-muc-tab-pattern.md` — tab định mức premix: bộ 3 cột cân được (`kg/tấn cám` · `% trong premix` · `gram cho 1 kg premix`), phép kiểm `TỔNG` phải cộng đúng 100 % / 1000 g, bố cục 4 phần, format. Dùng khi Quang đổ công thức ra sheet.
