#!/usr/bin/env python
"""Create a blank Google Sheets workbook with a formatted header row.

Verified working skeleton (Sep 2026): token-expiry float fix + create +
rename first tab + header + freeze/bold/colored header + column widths.

Usage:
    python make_kiemnghiem_sheet.py

Edit TITLE/HEADER/column WIDTHS below for your use case.
"""
import json, datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

TOKEN = 'C:/Users/NTQUANG_DELL/AppData/Local/hermes/google_token.json'

TITLE = "Sheet mới"
TAB   = "Dữ liệu"
HEADER = ["Mã mẫu", "Mô tả mẫu", "Ngày lấy mẫu"]   # <-- your columns

# pixel widths, in the same column order as HEADER (None = leave default)
WIDTHS = [140, 300, 110, None, None]


def get_svc():
    tok = json.load(open(TOKEN, encoding='utf-8'))
    # expiry may be a float epoch -> Iso string, or Credentials() raises
    if isinstance(tok.get('expiry'), (int, float)):
        tok['expiry'] = datetime.datetime.fromtimestamp(
            tok['expiry'], tz=datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    if isinstance(tok.get('expires_in'), float):
        tok['expires_in'] = int(tok['expires_in'])
    creds = Credentials.from_authorized_user_info(tok)
    return build('sheets', 'v4', credentials=creds)


def main():
    svc = get_svc()
    created = svc.spreadsheets().create(
        body={'properties': {'title': TITLE}}).execute()
    sid, url = created['spreadsheetId'], created['spreadsheetUrl']
    print("URL:", url)

    # numeric sheetId of the auto-created first tab (never assume 0)
    meta = svc.spreadsheets().get(spreadsheetId=sid).execute()
    sht_id = meta['sheets'][0]['properties']['sheetId']

    # rename first tab
    svc.spreadsheets().batchUpdate(spreadsheetId=sid, body={'requests': [
        {'updateSheetProperties': {'properties': {'sheetId': sht_id, 'title': TAB},
                                   'fields': 'title'}}]}).execute()

    # header row
    ncols = len(HEADER)
    svc.spreadsheets().values().update(
        spreadsheetId=sid, range=f'{TAB}!A1:{chr(64+ncols)}1',
        valueInputOption='USER_ENTERED',
        body={'values': [HEADER]}).execute()

    # freeze header + bold colored header + column widths (one round trip)
    reqs = [{'repeatCell': {'range': {'sheetId': sht_id, 'startRowIndex': 0,
             'endRowIndex': 1, 'startColumnIndex': 0, 'endColumnIndex': ncols},
             'cell': {'userEnteredFormat': {
                 'textFormat': {'bold': True},
                 'backgroundColor': {'red': 1.0, 'green': 0.84, 'blue': 0.0},
                 'verticalAlignment': 'MIDDLE'}},
             'fields': ('userEnteredFormat.textFormat.bold,'
                        'userEnteredFormat.backgroundColor,'
                        'userEnteredFormat.verticalAlignment')}},
            {'updateSheetProperties': {'properties': {'sheetId': sht_id,
             'gridProperties': {'frozenRowCount': 1}},
             'fields': 'gridProperties.frozenRowCount'}}]
    for i, w in enumerate(WIDTHS):
        if w:
            reqs.append({'updateDimensionProperties': {
                'range': {'sheetId': sht_id, 'dimension': 'COLUMNS',
                          'startIndex': i, 'endIndex': i+1},
                'properties': {'pixelSize': w}, 'fields': 'pixelSize'}})
    svc.spreadsheets().batchUpdate(spreadsheetId=sid, body={'requests': reqs}).execute()

    # verify
    res = svc.spreadsheets().values().get(
        spreadsheetId=sid, range=f'{TAB}!A1:{chr(64+ncols)}1').execute()
    print("verify header cols:", len(res.get('values', [[]])[0]))


if __name__ == '__main__':
    main()