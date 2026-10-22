---
name: google-docs-tabs
description: "Tạo Google Docs nhiều tab qua Docs API (addDocumentTab)."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [google-docs, api, tabs, google-workspace, drive]
---

# Google Docs API — Multi-tab documents

Dùng khi cần tạo Google Docs chia nhiều tab (tính năng tabs gốc của Google Docs, không phải Sheets), điền nội dung theo tab, hoặc sửa doc có tabs.

## Key facts
- Google Docs (không phải Sheets) hỗ trợ tabs trong 1 document.
- Docs API request type là `addDocumentTab` — KHÔNG phải `createTab` (lỗi `Unknown name "createTab"`).
- Đổi tên tab: `updateDocumentTabProperties` với `fields: "title"`.
- Insert text vào tab cụ thể: `insertText` với `location.tabId`.
- Đọc danh sách tabs: `documents.get(fields='tabs(tabProperties(tabId,title,index))')`.
- ⚠️ `documents.get()` KHÔNG có fields trả về body kiểu cũ, KHÔNG thấy tabs (TOTAL TABS: 0). Luôn dùng `fields='tabs(...)'` mới thấy tabs.
- Token: `C:\Users\NTQUANG_DELL\AppData\Local\hermes\google_token.json` (scopes gồm spreadsheets + drive; tạo docs vẫn OK).
- CLI wrapper `google_api.py` (skill google-workspace) CHƯA hỗ trợ tabs — phải dùng google-auth + google-api-python-client trực tiếp.

## Recipe
```python
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN_PATH = r"C:\Users\NTQUANG_DELL\AppData\Local\hermes\google_token.json"
creds = Credentials.from_authorized_user_file(TOKEN_PATH)
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
    json.dump(json.loads(creds.to_json()), open(TOKEN_PATH, "w"), indent=2)
docs = build("docs", "v1", credentials=creds)
drive = build("drive", "v3", credentials=creds)

# 1. Tạo doc
doc = docs.documents().create(body={"title": "Title"}).execute()
doc_id = doc["documentId"]

# 2. Đổi tên tab mặc định (t.0) + thêm tabs
requests = [
    {"updateDocumentTabProperties": {"tabProperties": {"tabId": "t.0", "title": "Tab1"}, "fields": "title"}}
]
for t in ["Tab2", "Tab3"]:
    requests.append({"addDocumentTab": {"tabProperties": {"title": t}}})
docs.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()

# 3. Lấy map tabId (mỗi tab mới có tabId ngẫu nhiên dạng t.xxx)
res = docs.documents().get(documentId=doc_id, fields="tabs(tabProperties(tabId,title,index))").execute()
tab_map = {t["tabProperties"]["title"]: t["tabProperties"]["tabId"] for t in res["tabs"]}

# 4. Insert text vào tab — index mặc định 1 (sau paragraph trống đầu)
body = {"requests": [{"insertText": {"location": {"tabId": tab_map["Tab2"], "index": 1}, "text": content}}]}
docs.documents().batchUpdate(documentId=doc_id, body=body).execute()

# 5. Share ai có link đọc được
drive.permissions().create(fileId=doc_id, body={"type": "anyone", "role": "reader"}).execute()
```

## Verify sau khi điền
- Đọc lại: `docs.documents().get(documentId=doc_id, fields='tabs(tabProperties(tabId,title,index),documentTab(body))').execute()` rồi duyệt `body.content` lấy textRun; in số chars/tab + dòng đầu để chắc nội dung đã vào đúng tab.

## Pitfalls
- `insertText` index: mặc định 1 = sau paragraph trống đầu tiên của tab mới (tab mới luôn có 1 paragraph trống).
- ⚠️ Field path khi verify: `tabs(tabProperties(...),body(...))` LỖI `Cannot find matching fields for path 'tabs.body.content.startIndex'` — phải dùng `documentTab(body)`, tức `tabs(tabProperties(tabId,title,index),documentTab(body))`. Tab = `tabProperties` + `documentTab` (body nằm trong documentTab, KHÔNG phải `body` trực tiếp dưới tabs).
- Share: dùng Drive API `permissions().create` với `{"type": "anyone", "role": "reader"}`.
- Google Docs tabs là tính năng UI mới (2024+); client lib cũ của `google_api.py` chưa có, phải gọi `build("docs","v1")` trực tiếp.
- `pip install google-auth google-auth-oauthlib google-api-python-client` nếu chưa có.
- Dọn file script temp (`scripts/tmp-*.py` / thư mục temp) sau khi dùng — không để lại credential-adjacent scripts.
