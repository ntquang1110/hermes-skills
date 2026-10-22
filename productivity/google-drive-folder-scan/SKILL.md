---
name: google-drive-folder-scan
description: Inventory a Google Drive folder into a list or sheet.
version: 1.0.0
platforms: [windows, linux, macos]
---

# Google Drive Folder Scan

Turn a Google Drive folder into a usable inventory (farm list, trial catalog, doc register, etc.). Works for "scan folder X and build me a list/sheet of what's in it".

## When to use
- User drops a `drive.google.com/drive/folders/<ID>` link and asks for an overview, a summary, list of entities, or a structured sheet/CSV built from the folder.
- You need to know the full recursive structure of a Drive folder before deciding what to extract.

## Steps

### 1. Authenticate and confirm the folder
Load `google-workspace` skill (bundled) for the `google_api.py` wrapper (`GAPI`), and check auth first:
```bash
GSETUP="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/setup.py"; $GSETUP --check
GAPI="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/google_api.py"
$GAPI drive get "<FOLDER_ID>"   # confirms name/mimeType/owner, proves access
```
Expected mimeType for a folder: `application/vnd.google-apps.folder`.

### 2. Walk the tree with the Drive API (not many `drive search` calls)
A single `drive search` with `--raw-query` only returns **direct children of one folder**. For a full tree, use a recursive script against the REST API (see `scripts/walk_drive.py`). Its query per folder:
```
q = "'<FOLDER_ID>' in parents and trashed=false"   (paginated, pageSize=1000)
```
Don't hand-loop; use the script. It dumps `DIR/file name \t id \t mimeType` indented by depth to a file.

### 3. Read the semantic index files, not just names
Folder names alone rarely carry enough meaning. At the root (and sometimes in subfolders) there are usually `README.md`, `_INDEX.md`, `CLAUDE.md`, `HUONG_DAN_*.md`. Download with `--export-mime text/plain` and read them. They encode:
- what each subfolder actually contains
- the entity list you're meant to extract (e.g. which operation ran at which site)
- naming conventions
- **security/classification rules** — e.g. CLAUDE.md may mark subfolders BÍ MẬT (secret) vs Nội bộ (internal). Respect them: never paste secret content (formulas, raw lab data) into your output; only state names/status.

### 4. Extract entities, skip media noise
When building the inventory, ignore pure-media subfolders (`Hình ảnh`, `Video`, `Ảnh`, `Thử nghiệm`) — they bloat the tree with thousands of jpg/mp4 lines. The entity is the parent folder (the farm/site/client).

### 5. Deliver + confirm
If the user asked you to *confirm understanding first* (common pattern: "Em confirm đã hiểu trước"), present: what the folder contains, the entity list you identified, the sheet/column plan, and — importantly — a **gap analysis** (columns the drive CANNOT fill, e.g. phone numbers, capacity, internal owner names) that you'll need from the user or leave blank. Get the green light before writing anything.

## After green light — fill detail & build the sheet

The confirm step above is "read what's there and plan". After the user says proceed, you usually must do TWO more things: pull each entity's source documents to fill detail columns (results, contacts, loads), and write the results into a real Google Sheet. `google-workspace` (bundled) handles single-file ops, but for batch download + sheet writes use the raw `googleapiclient` (token at `~/AppData/Local/hermes/google_token.json`, scopes `drive` + `spreadsheets`).

### A. Download the entity's source documents
Each entity folder holds report files (`Báo cáo`, `Hồ sơ`, `TÓM TẮT KẾT QUẢ`, `Kết quả`) — read them to fill the detail columns. Batch via a script (see `scripts/download_docs.py`) that maps `(file_id, out_name)` per entity and:
- **Native Google files** (Docs/Sheets/Slides): `svc.files().export(fileId=id, mimeType="text/plain")` → bytes.
- **Binary files** (`.docx`, `.doc`, `.pdf`): `svc.files().get_media(fileId=id)` + `MediaIoBaseDownload`, save bytes as-is.

Extract text from what you downloaded: python-docx (`Document(path)` → paragraphs + **tables**, which carry the real numbers) and pypdf (`PdfReader(path)` → `page.extract_text()`). Flag empty results — those are image/scanned docs (.docx full of photos, scanned PDFs) where `extract_text()` returns nothing; note "báo cáo dạng ảnh/scanned" rather than leaving a misleading blank.

### B. Build / update the Google Sheet
- Create: `gs.spreadsheets().create(body={"properties":{"title":...}})`. Or `google_api.py sheets create`.
- Write rows with `gs.spreadsheets().values().update(..., valueInputOption="USER_ENTERED")` — **USER_ENTERED so `=HYPERLINK("url","label")` formulas evaluate**.
- Format via `gs.spreadsheets().batchUpdate`: header `repeatCell` (bold + background), `setBasicFilter`, `updateDimensionProperties` (widths), `repeatCell` `wrapStrategy:"WRAP"` on the long-text columns.
- **Always read the sheet back after writing** (`values().get`) to verify rows/columns landed and phone/links survived — never report done from what you *intended* to write.

## Pitfalls

- **`files().export()` fails on binary files.** Export only works for Google-native Editors files. Calling it on a `.docx`/`.pdf`/`.doc` returns `403: "Export only supports Docs Editors files."` Use `get_media()` + `MediaIoBaseDownload` for anything binary.
- **Sheets grid id is NOT always 0.** The first sheet's id is usually a large integer (e.g. `1025531923`), fetched via `spreadsheets().get(spreadsheetId=..., fields="sheets(properties.sheetId,properties.title)")`. Using `sheetId:0` in `batchUpdate` range objects throws `No grid with id: 0` (after the data already wrote).
- **`setDimensionProperties` is the WRONG request name** — the correct Sheets batchUpdate request is `updateDimensionProperties` (same shape). Wrong name → `Invalid JSON payload received. Unknown name ... at 'requests[2]'`.
- **Leading-zero phone numbers lose the zero in USER_ENTERED.** Writing `"<PHONE>"` via USER_ENTERED coerces it to the number `985964583`. To preserve the leading 0, write it as literal text (prefix `'`, or write `=TEXT(...)` / set the column/cell number format to `@`).
- **Scanned/binary report docs extract to `[]`.** When `extract_text()` returns ~0 chars, treat it as "needs OCR / view source", not as "no result".
- **Native Python on Windows does NOT understand MSYS/git-bash paths.** Inside a Python script, `open("/d/Hermes Proj/out.txt", "w")` is misinterpreted and either errors or silently writes a stray file elsewhere. Always use native Windows paths (`r"D:\Hermes Proj\out.txt"`) or relative paths inside `.py` files. The shell understands `/d/...`; the interpreter does not.
- **Google-native files** (Docs, Sheets, Slides) have no byte content — `drive download` needs `--export-mime` (text/plain for docs, csv/xlsx for sheets). Don't try to `read_file` on a folder's native id.
- **`--raw-query` children search** silently returns `[]` if the query isn't passed correctly; the reliable form is `--raw-query "'<ID>' in parents"`.
- Output on this host goes under `D:\Hermes Proj\` (drive D is the standard for data), not under C:.

## Support files
- `scripts/walk_drive.py` — recursive Drive folder tree walker (paginated API), prints indented tree to a file.
- `scripts/download_docs.py` — batch-download entity report docs (native export vs binary get_media).
- `references/sheets-formatting-api.md` — Google Sheets batchUpdate API quirks (real sheetId, `updateDimensionProperties`, verification loop).