# Drive folder → Inventory sheet (Kiềm Saphia trại inventory, 08/2026)

Worked example: scan Google Drive folder `01_Khoa_Học_RnD` → Google Sheet "Thống kê các trại thử nghiệm Kiềm Saphia" (25 trại, 12 cột + Dashboard tab).

## Recursive Drive scan (source of truth)
```python
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
svc = build("drive","v3",credentials=Credentials.from_authorized_user_file(
    os.path.expanduser("~/AppData/Local/hermes/google_token.json")))
def children(parent):
    out,page=[],None
    while True:
        r=svc.files().list(q=f"'{parent}' in parents and trashed=false",pageSize=1000,pageToken=page,
            fields="nextPageToken, files(id,name,mimeType)").execute()
        out+=r.get("files",[]); page=r.get("nextPageToken")
        if not page: break
    return out
# recurse; emit "file|<name>|<id>|<mime>" lines; folders recurse
```

## Download
- Binary (.docx/.pdf): `svc.files().get_media(fileId=id)` + `MediaIoBaseDownload(fh, req, chunksize=1<<20)`.
- Google-native (.md/.doc gdoc): `svc.files().export(fileId=id, mimeType="text/plain")`.
- ⚠️ Exporting a binary throws 403 "Export only supports Docs Editors files" — always get_media for binaries.

## Text extraction
- docx: `docx.Document(path)` → paragraphs + `doc.tables` rows (join cells with " | ").
- pdf: `pypdf.PdfReader` → `page.extract_text()`.
- Image-only docx (0 chars): unzip, read `word/media/*.png|jpg`.
- Scanned pdf: render pages via pymupdf `page.get_pixmap(dpi=200).save(...)`.

## OCR fallback (RapidOCR, Vietnamese-capable)
```python
from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()
res,_ = ocr(png_path)          # res = list of [box, text, score]
lines = [r[1] for r in res if r and len(r)>1]
```
- Used because `vision_analyze` returned 401 (aux vision model bad token) and subagents lacked vision. RapidOCR = local, no API key, handles Vietnamese.
- Install with the SAME interpreter that runs the script: `python -m pip install rapidocr-onnxruntime` (plain `pip` maps to a different python and installs to the wrong site-packages — seen live: package landed in Python314 while `python` was 3.11).
- Slow on CPU: 22-page scan ≈ 10–25 min → run in `background=true` + `notify_on_complete`, don't block.
- Batch OCR in a loop over rendered page PNGs; write each page's lines to one output .txt.

## Label verification (critical)
The drive's own `_INDEX.md` and some folder names were wrong. Always read the actual report before naming a row:
- N.V Hưng (Tam Đảo) → GÀ Minh Dư 3, 3000 con (**not** bò sữa)
- Đồng Đức Vọng → GÀ lai chọi 1000 con, Gia Lộc Hải Dương (**not** tôm Cà Mau)
- Dabaco → LỢN thịt 368 con trại Lạc Vệ (**not** 250 gà)
- ĐH Cần Thơ → CÁ TRA *P. hypophthalmus* (**not** tôm)

## Sheets write (correct API names)
- Write values: `values().update(range="Sheet!A1:...", valueInputOption="USER_ENTERED")`.
- Format batchUpdate request names: `repeatCell`, `setBasicFilter`, **`updateDimensionProperties`** (NOT `setDimensionProperties` → 400).
- Real sheetId: `GET ?fields=sheets.properties(sheetId,title)` (default tab often not id 0).
- Single value per range: write one cell per put (a 2-row array into `!C9:L9` → 400 "tried writing to row [10]").

## Useful numbers from this session (expendable)
ĐH Cần Thơ cá tra → tỷ lệ sống: ĐC 35,23% / Virusto 1l·200kg⁻¹ 47,83% / bột kiềm 5kg·t⁻¹ 56,70% / 7kg·t⁻¹ 61,63%.