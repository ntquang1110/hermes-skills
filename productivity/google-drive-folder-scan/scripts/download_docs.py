"""Batch-download Google Drive files (native export + binary get_media) for inventory detail.

Maps (file_id, out_name) per entity, downloads each into outdir. Native Google
Docs/Sheets texts are exported to .txt; binary .docx/.pdf/.doc are saved as-is
via get_media so python-docx / pypdf can parse them after.

Run with:  python download_docs.py   (edit DOCS + OUTDIR at bottom first)
"""
import io, os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload

def service():
    creds = Credentials.from_authorized_user_file(
        os.path.expanduser("~/AppData/Local/hermes/google_token.json"))
    return build("drive", "v3", credentials=creds)

def download(svc, file_id, out_path):
    meta = svc.files().get(fileId=file_id, fields="mimeType,name").execute()
    mime = meta["mimeType"]
    if mime.startswith("application/vnd.google-apps"):
        # native Docs/Sheets/Slides -> export to text
        r = svc.files().export(fileId=file_id, mimeType="text/plain").execute()
        with open(out_path + ".txt", "wb") as f:
            f.write(r)
        return out_path + ".txt"
    # binary (.docx/.doc/.pdf) -> get_media; export would 403
    req = svc.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    dl = MediaIoBaseDownload(fh, req, chunksize=1 << 20)
    done = False
    while not done:
        _, done = dl.next_chunk()
    with open(out_path, "wb") as f:
        f.write(fh.getvalue())
    return out_path

if __name__ == "__main__":
    svc = service()
    OUTDIR = r"D:\Hermes Proj\_reports"
    DOCS = [
        # (file_id, "entity_reports/report_name.docx")
        ("<FILE_ID>", "sample.docx"),
    ]
    for fid, name in DOCS:
        os.makedirs(OUTDIR, exist_ok=True)
        try:
            print(name, "->", download(svc, fid, os.path.join(OUTDIR, name)))
        except Exception as e:
            print(name, "ERR", e)