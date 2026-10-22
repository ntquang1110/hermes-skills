#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dump Google Sheets metadata (title, tab names, sheetIds, grid sizes).

Usage:
    python sheets_probe.py <SHEET_ID>
    python sheets_probe.py <SHEET_ID> "<TabName>!A1:F5"   # also dump a range

Auth: uses ~/AppData/Local/hermes/google_token.json (same as google-workspace).
Run BEFORE any values().get/update or batchUpdate so you use the real tab
name and numeric sheetId (both are NEVER guessable: not 'Sheet1', not 0).
"""
import json, sys, os

TOKEN = os.path.expanduser('~/AppData/Local/hermes/google_token.json')
if not os.path.exists(TOKEN):
    # fallback for HERMES_HOME setups
    TOKEN = os.path.join(os.environ.get('HERMES_HOME', ''), 'google_token.json')

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    sheet_id = sys.argv[1]
    tok = json.load(open(TOKEN, encoding='utf-8'))
    creds = Credentials.from_authorized_user_info(tok)
    svc = build('sheets', 'v4', credentials=creds)

    meta = svc.spreadsheets().get(spreadsheetId=sheet_id).execute()
    print('TITLE:', meta['properties']['title'])
    print('URL:  ', meta.get('spreadsheetUrl', ''))
    for s in meta['sheets']:
        p = s['properties']
        print(f"TAB: {p['title']!r}  sheetId={p['sheetId']}  "
              f"rows={p['gridProperties'].get('rowCount')}  "
              f"cols={p['gridProperties'].get('columnCount')}")

    if len(sys.argv) > 2:
        rng = sys.argv[2]
        res = svc.spreadsheets().values().get(
            spreadsheetId=sheet_id, range=rng).execute()
        print(f'\nRANGE {rng}:')
        for row in res.get('values', []):
            print(' | '.join((c or '')[:60] for c in row))

if __name__ == '__main__':
    main()
