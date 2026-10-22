#!/usr/bin/env python3
"""Print tab titles + sheetIds for a Google Spreadsheet.

Usage: python list_tabs.py SPREADSHEET_ID
Run first before any fill: get correct tab names and real sheetIds.
"""
import json
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = "C:/Users/NTQUANG_DELL/AppData/Local/hermes/google_token.json"

if len(sys.argv) < 2:
    print("Usage: python list_tabs.py SPREADSHEET_ID")
    sys.exit(1)

tok = json.load(open(TOKEN_PATH, encoding="utf-8"))
creds = Credentials.from_authorized_user_info(tok)
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
srv = build("sheets", "v4", credentials=creds)

meta = srv.spreadsheets().get(spreadsheetId=sys.argv[1]).execute()
print("TITLE:", meta["properties"]["title"])
for sh in meta["sheets"]:
    p = sh["properties"]
    print("SHEET:", p["title"], "| sheetId:", p["sheetId"],
          "| rows:", p.get("gridProperties", {}).get("rowCount"))
