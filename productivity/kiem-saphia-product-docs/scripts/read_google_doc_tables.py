"""Đọc Google Doc KHÔNG public (kể cả bảng) qua Docs API — dùng khi cần full chỉ tiêu
TCCS / phiếu kiểm nghiệm / bảng số liệu. `google_api.py docs get` BỎ SÓT BẢNG
(chỉ trả đoạn văn, số liệu trong table mất hết) — script này walk cả TABLE.

Usage: python read_google_doc_tables.py <DOC_ID>
Token: C:/Users/NTQUANG_DELL/AppData/Local/hermes/google_token.json (tự refresh)
"""
import sys
sys.path.insert(0, r'C:/Users/NTQUANG_DELL/AppData/Local/hermes/skills/productivity/google-workspace/scripts')
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN = r'C:/Users/NTQUANG_DELL/AppData/Local/hermes/google_token.json'
DOC_ID = sys.argv[1] if len(sys.argv) > 1 else input('DOC_ID: ')

creds = Credentials.from_authorized_user_file(TOKEN, ['https://www.googleapis.com/auth/documents.readonly'])
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
    with open(TOKEN, 'w') as f:
        f.write(creds.to_json())

service = build('docs', 'v1', credentials=creds)
doc = service.documents().get(documentId=DOC_ID).execute()

out = []

def para_text(para):
    return ''.join(run.get('textRun', {}).get('content', '')
                   for run in para.get('elements', []))

def walk_content(content):
    for el in content:
        if 'paragraph' in el:
            txt = para_text(el['paragraph'])
            if txt.strip():
                out.append(txt.rstrip('\n'))
        elif 'table' in el:
            out.append('=== TABLE START ===')
            for row in el['table'].get('tableRows', []):
                cells = []
                for cell in row.get('tableCells', []):
                    celltxt = ''
                    for ce in cell.get('content', []):
                        if 'paragraph' in ce:
                            celltxt += para_text(ce['paragraph'])
                        elif 'table' in ce:
                            celltxt += '[nested-table]'
                    cells.append(celltxt.strip())
                out.append(' | '.join(cells))
            out.append('=== TABLE END ===')

walk_content(doc.get('body', {}).get('content', []))
print('\n'.join(out))