---
name: google-drive-doc-inventory
description: "Build a Sheet inventory from a Drive folder of report docs."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [Google Drive, Sheets, OCR, docx, pdf, inventory, Windows]
---

# Google Drive → Document Extraction → Sheet Inventory

End-to-end pipeline: turn a Google Drive folder full of report documents into a
structured Google Sheet (per-farm, per-trial, per-item inventory). Proven on
Windows against the Vua Kiềm "01_Khoa_Học_RnD" trial-farm folder (Aug 2026).

## When to use
- User drops a `drive.google.com/drive/folders/<ID>` link and wants a survey / catalog / tracking sheet built from the docs inside.
- You need to pull result numbers out of a pile of .docx/.pdf reports and aggregate them.

## Workflow

### 1. Auth & scopes
```bash
GSETUP="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/setup.py"
$GSETUP --check
```
Token lives at `~/AppData/Local/hermes/google_token.json`. You need the `drive` and `spreadsheets` scopes. Drive reads of a *shared* folder work with the exporting account; the folder owner email is returned by `files().get()` → `owners[].emailAddress`.

### 2. Recursive folder scan (tree dump)
Use the Drive API directly (googleapiclient) — the `gws`/`google_api.py` `drive search` wrapper is too limited for recursion into a deep tree.

```python
q = f"'{parent}' in parents and trashed=false"
svc.files().list(q=q, pageSize=1000, pageToken=page,
    fields="nextPageToken, files(id,name,mimeType,size,modifiedTime,parents)").execute()
```
Walk depth-first, print every `DIR <name> <id> <mime>` / `file <name> <id> <mime>`, write the whole tree to a `.txt`. This tree is your source of truth for the inventory rows.

### 3. Read the folder's README/INDEX — but VERIFY it
Most Drive folders contain `README.md`, `_INDEX.md`, `CLAUDE.md` describing structure. Read them first (download via `files().export(..., mimeType='text/plain')` for Google-native md). **They are frequently STALE or WRONG** — treat as a hint, never as fact.

> Real case: the folder INDEX said "N.V Hưng (Tam Đảo) = bò sữa", "Đồng Đức Vọng = tôm Cà Mau", "Dabaco = 250 con gà". The actual reports showed N.V Hưng = **gà Minh Dư 3 (3000 con)**, Đồng Đức Vọng = **gà lai chọi (Gia Lộc, Hải Dương)**, Dabaco = **lợn thịt 368 con**. Always confirm species/count/site from the document contents, not the folder name/INDEX.

### 4. Download documents — binary vs Docs-Editors split
```text
application/vnd.google-apps.document   → files().export(..., mimeType="text/plain")  OK
.docx / .doc / .pdf / .xlsx (binder)   → files().get_media() + MediaIoBaseDownload   REQUIRED
```
`files().export()` on a binary .docx throws `HttpError 403 "Export only supports Docs Editors files."`. For binder files you MUST use `get_media()` and save the bytes.

### 5. Extract text
- `.docx`: `python-docx` — `[p.text for p in d.paragraphs]` **plus** table cells (`for t in d.tables: for row in t.rows: " | ".join(c.text for c in row.cells)`); most trial numbers live in tables.
- `.pdf`: `pypdf` `PdfReader(...).pages[i].extract_text()`.
- **Image-based .docx** (scanned pages stuffed into Word): python-docx returns 0 chars and size is large. Extract embedded images directly:
  ```python
  import zipfile
  z = zipfile.ZipFile(path)
  imgs = [n for n in z.namelist() if n.startswith("word/media/") and n.lower().endswith((".png",".jpg",".jpeg"))]
  ```
- **Scanned PDF**: `page.get_text()` returns empty. Render to PNG first, then OCR (step 6).

### 6. OCR on Windows without tesseract — RapidOCR (PP-OCR, supports Vietnamese)
`vision_analyze` may be unavailable/unauthenticated in child agents or the aux vision model returns `401 Invalid token payload`. The reliable local fallback is RapidOCR:
```bash
python -m pip install rapidocr-onnxruntime   # pulls onnxruntime + opencv + models (~150MB)
```
```python
from rapidocr_onnxruntime import RapidOCR
eng = RapidOCR()
res, _ = eng(path)          # path = image or PDF (it reads images best)
lines = [r[1] for r in res if r and len(r)>1]
```
- Vietnamese text works out of the box (PP-OCR vi).
- Render PDF pages first: `import pymupdf; pix=page.get_pixmap(dpi=200); pix.save("p.png")`.
- CPU-only is SLOW (~30–60s per large page). Run OCR as a background process (`terminal(background=True, notify_on_complete=True)`) and keep working; finish the sheet when it lands.
- Expect imperfect accents from OCR (`Kiem`, `thuoc`, `S6 nha`) — you read meaning through it; do not let missing diacritics block comprehension.

### 7. Build / update the Google Sheet
- Create: `spreadsheets().create` → id + url.
- Write values: `values().update(range="Sheet1!A1:Ln", valueInputOption="USER_ENTERED")`.
  **Pitfall:** the `values` array's row count must equal the range's row count — otherwise `HttpError 400 "Requested writing within range [...], but tried writing to row [N]"`. Update one cell at a time (`'Sheet1!C9'` with `[[val]]`) when patching scattered cells, or pass a full grid.
- Formatting via `batchUpdate`:
  - **Correct request name is `updateDimensionProperties`** (NOT `setDimensionProperties`) for column widths.
  - Grid `sheetId` is **not always 0** — discover it: `spreads().get(fields="sheets(properties.sheetId,properties.title)")` and use the real id in all `range.sheetId`.
  - Bold header + wrap + `setBasicFilter` + `repeatCell(wrapStrategy="WRAP")` make it readable and filterable.
- Hyperlinks into source folders: write `=HYPERLINK("https://drive.google.com/drive/folders/<id>","Folder gốc")` with USER_ENTERED.
- Share: `drive share <SID> --email <owner> --role writer` and/or `--type anyone --role writer`.

### 8. Structure by idempotency
Keep the write script **idempotent** (values.update overwrites the same range), so re-running after a structural change is safe. If the user reorders columns mid-task, RE-READ the sheet headers first and map the target column by header name, not by the old A1 assumption.

## Pitfalls (Windows / this machine)
- **Native Windows Python cannot open MSYS-style paths** (`"/d/Hermes Proj/..."`). Use native `r"D:\Hermes Proj\..."` in Python; MSYS paths only in shell commands.
- **`pip` may point at a different interpreter than `python`** (here `pip`→python3.14, `python`→3.11). Always `python -m pip install <pkg>` so it lands in the interpreter that runs your scripts.
- Cache/index files in a Drive folder (`_INDEX.md`) are nice-to-have orientation but are **not authoritative** — trust documents over indexes.
- Respect confidentiality flags in folder CLAUDE.md (e.g. "Công_Thức_Bí_Mật", raw PCR = secret): never paste secret content into a shared sheet; record only name + status.

## Support files
- `references/drive-sheet-recipe.md` — session detail: the working recursion/download/extract/OCR code shapes, sheets batchUpdate gotchas, and the Vua Kiềm inventory example.