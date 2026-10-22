#!/usr/bin/env python
"""Safely append/update columns on a LIVE Google Sheet the user may have edited.

Why this exists: rewriting a full block from an in-memory snapshot silently destroys
whatever the user changed in the meantime. This script always re-reads first, resolves
column letters from the live header, and writes only the targeted columns.

Usage (import):
    from append_columns_live import SheetOps
    ops = SheetOps(SHEET_ID, 'DS VP cho thuê')
    print(ops.header())                 # always eyeball this first
    ops.set_column('Người liên hệ', ['Anh Phú', 'C. Khanh'])
    ops.set_column('SĐT', ['0983 668 ***', '0365 698 ***'])
    ops.set_dropdown('Trạng thái',
                     ['Chưa contact', 'Đã contact', 'Hẹn xem', 'Đã xem', 'Đã chốt'])

Usage (CLI):
    python append_columns_live.py <SHEET_ID> <TAB>
"""
import json
import os

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def col_letter(i: int) -> str:
    """0 -> 'A', 25 -> 'Z', 26 -> 'AA'."""
    s, i = '', i + 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def col_index(s: str) -> int:
    n = 0
    for ch in s.upper():
        n = n * 26 + (ord(ch) - 64)
    return n - 1


class SheetOps:
    def __init__(self, spreadsheet_id, tab, token_path=None):
        self.sid = spreadsheet_id
        self.tab = tab
        path = token_path or os.path.expanduser(
            '~/AppData/Local/hermes/google_token.json')
        tok = json.load(open(path, encoding='utf-8'))
        self.svc = build('sheets', 'v4',
                         credentials=Credentials.from_authorized_user_info(tok))
        self._header = None

    # ---------- structure ----------
    def sheet_id(self):
        meta = self.svc.spreadsheets().get(spreadsheetId=self.sid).execute()
        for s in meta['sheets']:
            if s['properties']['title'] == self.tab:
                return s['properties']['sheetId']
        raise KeyError('tab %r not found' % self.tab)

    def read(self, width=200):
        res = self.svc.spreadsheets().values().get(
            spreadsheetId=self.sid,
            range="'%s'!A1:%s" % (self.tab, col_letter(width - 1))).execute()
        return res.get('values', [])

    def header(self, refresh=True):
        if self._header is None or refresh:
            rows = self.read()
            self._header = rows[0] if rows else []
        return self._header

    def index_map(self, refresh=True):
        """Column name -> 0-based index, from the LIVE header row."""
        return {n.strip(): i for i, n in enumerate(self.header(refresh)) if n.strip()}

    # ---------- writes ----------
    def ensure_column(self, name):
        """Return the letter for `name`, appending the header if absent. Idempotent."""
        idx = self.index_map()
        if name in idx:
            return col_letter(idx[name])
        col = col_letter(len(self.header()))
        self._write('%s1' % col, [[name]], raw=True)
        self._header = self.header() + [name]
        return col

    def set_column(self, name, values, data_start_row=2):
        """Write one column's data. Never touches any other column.

        values[0] lands on `data_start_row` (default 2, i.e. under the header).
        """
        col = self.ensure_column(name)
        # Rectangular payload; a ragged list trips the API's width check.
        body = [[('' if v is None else str(v))] for v in values]
        end = data_start_row + len(body) - 1
        self._write('%s%d:%s%d' % (col, data_start_row, col, end), body, raw=True)
        return col

    def set_dropdown(self, name, options, max_rows=50):
        idx = self.index_map()
        if name not in idx:
            raise KeyError('create the column first: %r' % name)
        col_idx = idx[name]
        self.svc.spreadsheets().batchUpdate(
            spreadsheetId=self.sid,
            body={'requests': [{
                'setDataValidation': {
                    'range': {'sheetId': self.sheet_id(),
                              'startRowIndex': 1, 'endRowIndex': max_rows,
                              'startColumnIndex': col_idx,
                              'endColumnIndex': col_idx + 1},
                    'rule': {
                        'condition': {'type': 'ONE_OF_LIST',
                                      'values': [{'userEnteredValue': o}
                                                 for o in options]},
                        'inputMessage': 'Chọn ' + name.lower(),
                        'showCustomUi': True,
                    },
                }
            }]}).execute()

    def _write(self, rng, values, raw=True):
        self.svc.spreadsheets().values().update(
            spreadsheetId=self.sid,
            range="'%s'!%s" % (self.tab, rng),
            valueInputOption='RAW' if raw else 'USER_ENTERED',
            body={'values': values}).execute()

    # ---------- verify ----------
    def verify(self, n_rows=3):
        last = col_letter(max(self.index_map().values(), default=0))
        res = self.svc.spreadsheets().values().get(
            spreadsheetId=self.sid,
            range="'%s'!A1:%s%d" % (self.tab, last, n_rows)).execute()
        out = res.get('values', [])
        for r in out:
            print(r)
        return out


if __name__ == '__main__':
    import sys
    sid, tab = sys.argv[1], sys.argv[2]
    ops = SheetOps(sid, tab)
    meta = ops.svc.spreadsheets().get(spreadsheetId=sid).execute()
    print('TABS:', [s['properties']['title'] for s in meta['sheets']])
    print('HEADER:', ops.header())
    print('MAP:', ops.index_map())
