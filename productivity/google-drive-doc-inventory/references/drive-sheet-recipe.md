# Drive → Sheet recipe (session detail, Aug 2026)

Concrete shapes that worked for scanning the Vua Kiềm `01_Khoa_Học_RnD` trial-farm folder and building a 25-farm inventory sheet.

## Recursive Drive tree walk (googleapiclient direct)
```python
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
creds = Credentials.from_authorized_user_file(os.path.expanduser("~/AppData/Local/hermes/google_token.json"))
svc = build("drive","v3",credentials=creds)
ROOT = "<folder_id>"
def children(parent):
    items, page = [], None
    while True:
        q = f"'{parent}' in parents and trashed=false"
        res = svc.files().list(q=q, pageSize=1000, pageToken=page,
            fields="nextPageToken, files(id,name,mimeType,size,modifiedTime,parents)").execute()
        items += res.get("files",[]); page = res.get("nextPageToken")
        if not page: break
    return items
```
`mimeType == "application/vnd.google-apps.folder"` → recurse. Write a flat `DIR/file name<TAB>id<TAB>mime` dump.

## Download: binder vs Docs Editor
```python
meta = svc.files().get(fileId=fid, fields="mimeType,name").execute()
if meta["mimeType"] == "application/vnd.google-apps.document":
    r = svc.files().export(fileId=fid, mimeType="text/plain"); open(dst+".txt","wb").write(r.execute())
else:  # .docx/.doc/.pdf/.xlsx
    fh = io.BytesIO(); dl = MediaIoBaseDownload(fh, svc.files().get_media(fileId=fid), chunksize=1<<20)
    done=False
    while not done: _,done = dl.next_chunk()
    open(dst,"wb").write(fh.getvalue())
```
`files().export()` on a binary .docx fails with 403 "Export only supports Docs Editors files." — must use `get_media()`.

## docx → text including tables
```python
import docx
d = docx.Document(path)
parts = [p.text.strip() for p in d.paragraphs if p.text.strip()]
for t in d.tables:
    for row in t.rows:
        cells=[c.text.strip() for c in row.cells]
        if any(cells): parts.append(" | ".join(cells))
```
Trial metrics (weights, FCR, mortality, "Số con chết") live in Word tables, not paragraphs.

## Image-based .docx → extract media PNGs
```python
z = zipfile.ZipFile(path)
pngs = [n for n in z.namelist() if n.startswith("word/media/") and n.lower().endswith((".png",".jpg",".jpeg"))]
```

## Scanned PDF → PNG then OCR
```python
import pymupdf
doc = pymupdf.open("report.pdf")
for i,page in enumerate(doc):
    page.get_pixmap(dpi=200).save(f"page{i+1}.png")
```

## RapidOCR (Vietnamese)
```python
from rapidocr_onnxruntime import RapidOCR
eng = RapidOCR()
res,_ = eng("page1.png")
lines = [r[1] for r in res if r and len(r)>1]
```
Install for the active interpreter: `python -m pip install rapidocr-onnxruntime`. Slow on CPU; run in background.

## Sheets formatting batchUpdate gotchas
- Column width request name is `updateDimensionProperties` (NOT `setDimensionProperties`).
- Grid `sheetId` is not necessarily 0 — get it:
  `spreads().get(spreadsheetId=SID, fields="sheets(properties.sheetId,properties.title)")`
- `values().update` range row-count must equal the values array row-count; patching scattered cells → one `'Range!C9'` update per cell with `{"values":[[val]]}`.

## User-preferred column shape (Vua Kiềm trial-farm inventory)
Tên trại | Chủ trại | Liên hệ | Đối tượng thử nghiệm (loài) | Pháp nhân (Cá nhân/Công ty) | Bối cảnh | Tổng chuồng có thể chứa | Dự kiến/đã thử nghiệm bao nhiêu con | Người phụ trách | Trạng thái | Quá trình | Kết quả | Link folder gốc.

## Domain corrections discovered (trust docs over INDEX)
- N.V Hưng Tam Đảo = GÀ Minh Dư 3, 3000 con (INDEX said bò sữa).
- Đồng Đức Vọng = GÀ lai chọi 1000 con, Gia Lộc, Hải Dương (INDEX said tôm Cà Mau).
- Dabaco = LỢN thịt 368 con, trại Lạc Vệ (INDEX said 250 con gà).
- Nguyễn Như Tư = VỊT bơ 1000/2000 con (not lợn).
- Đinh Văn Việt xlsx = ASF Protocol A trial, ~266 con, EZ67 1:30 + EZ80 trộn cám (internal Manna Đất Vàng), daily tracking to 24/06/2026.