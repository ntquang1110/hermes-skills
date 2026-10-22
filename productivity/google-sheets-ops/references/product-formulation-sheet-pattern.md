# Product Formulation Sheet Pattern (for Google Sheets API)

Worked example created 21/09/2026: pig health products with 9 tabs, 14 formulas, 32 compounds.
Full sheet: https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit

## Tab structure for product documentation

1. **Hướng dẫn** (guide) — first tab, for pharmaceutical professionals. Short: structure, how to read, how to choose formula, notation.
2. **Danh mục hoạt chất** (master table) — all compounds in one table with source, mechanism, evidence level, PMID, price.
3. **Product tabs** — one per product. Each tab has:
   - Product name + form (dung dịch/bột)
   - 2-3 formula variants (CT.1 = giá rẻ, CT.2 = cao cấp)
   - Each variant: ingredient table + 5-criteria analysis table

## Google Sheets API workflow

```python
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import json, datetime

# Auth
tok = json.load(open('C:/Users/NTQUANG_DELL/AppData/Local/hermes/google_token.json', encoding='utf-8'))
if isinstance(tok.get('expiry'), (int, float)):
    tok['expiry'] = datetime.datetime.fromtimestamp(tok['expiry'], tz=datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
if isinstance(tok.get('expires_in'), float):
    tok['expires_in'] = int(tok['expires_in'])
creds = Credentials.from_authorized_user_info(tok)
svc = build('sheets', 'v4', credentials=creds)

# 1. Create
created = svc.spreadsheets().create(body={'properties':{'title': TITLE}}).execute()
SHEET_ID = created['spreadsheetId']

# 2. Get metadata (tab names + sheetIds)
meta = svc.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
sid_map = {s['properties']['title']: s['properties']['sheetId'] for s in meta['sheets']}

# 3. Rename default tab
svc.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID, body={'requests': [{
    'updateSheetProperties': {
        'properties': {'sheetId': 0, 'title': 'Hướng dẫn'},
        'fields': 'title'
    }
}]}).execute()

# 4. Add tabs
for tname in ['Danh mục hoạt chất', 'A1 - Sản phẩm X']:
    svc.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID, body={
        'requests': [{'addSheet': {'properties': {'title': tname}}}]
    }).execute()

# 5. Write data (RAW mode for text, USER_ENTERED for formulas)
svc.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range="'Tab Name'!A1:E20",
    valueInputOption='RAW',
    body={'values': [['header1','header2'], ['data1','data2']]}
).execute()

# 6. Format: freeze row, bold header, set widths
requests = [
    {'updateSheetProperties': {
        'properties': {'sheetId': sid, 'gridProperties': {'frozenRowCount': 1}},
        'fields': 'gridProperties.frozenRowCount'
    }},
    {'repeatCell': {
        'range': {'sheetId': sid, 'startRowIndex': 0, 'endRowIndex': 1},
        'cell': {'userEnteredFormat': {'textFormat': {'bold': True},
                 'backgroundColor': {'red': 1.0, 'green': 0.84, 'blue': 0.0}}},
        'fields': 'userEnteredFormat.textFormat.bold,userEnteredFormat.backgroundColor'
    }},
    {'updateDimensionProperties': {
        'range': {'sheetId': sid, 'dimension': 'COLUMNS', 'startIndex': 0, 'endIndex': 1},
        'properties': {'pixelSize': 200},
        'fields': 'pixelSize'
    }},
]
svc.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID, body={'requests': requests}).execute()
```

## Pitfalls (specific to product sheets)

- **Tab names MUST be Vietnamese with diacritics** — user explicitly corrected this. "A1 - Sát khuẩn không khí" not "A1-KhongKhi".
- **Vietnamese comma-decimals** — `valueInputOption='RAW'` may misparse `"0,108"` as `108`. After bulk write, spot-check sub-1.0 cells and re-write problematic ones with RAW mode.
- **Sheet names change after creation** — always re-read metadata before batchUpdate to get current sheetIds. Do NOT cache them.
- **First tab should be Hướng dẫn** — short, professional, for domain experts. Not a tutorial, just orientation.
- **Format header after writing** — if you format before writing, the data overwrites the formatting on the header row. Write first, then format.
