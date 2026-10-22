# Appending columns to a LIVE, user-edited sheet (without destroying data)

## The trap

You build a payload at time T. The user then edits the sheet — fills a cell, adds a column,
renames a header, pastes a phone number in. You come back and run:

```python
# WRONG — this is a full-block overwrite from a stale snapshot
svc.spreadsheets().values().update(
    spreadsheetId=SHEET_ID, range='DS VP cho thuê!A1:N13',
    valueInputOption='USER_ENTERED', body={'values': new_rows}).execute()
```

Every change the user made since T is gone, with no error. Real damage from this session: a
12-row property-shortlist sheet lost its entire `Link` column, because `new_rows` was
assembled from the original hand-built list rather than from a fresh read. The user's reaction
was the correct lesson: *"sao mất hết link của anh r, em phải xem lại trước khi thực thi chứ"*.

## Decision rule

| Situation | Safe action |
|---|---|
| Sheet you created, nobody else has opened it | Full-block rewrite is fine |
| User has edited it (any time) | Read fresh → write ONLY the new/changed cells |
| Adding columns the user didn't ask for | Append by resolved column letter, never by index |
| You need to reorder/restyle | `batchUpdate` requests touch formatting only, values survive |

## Recipe

```python
import json, os, re
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

tok = json.load(open(os.path.expanduser(
    '~/AppData/Local/hermes/google_token.json'), encoding='utf-8'))
svc = build('sheets', 'v4',
            credentials=Credentials.from_authorized_user_info(tok))

TAB, SHEET_ID = 'DS VP cho thuê', '1Kgt...'

def col_letter(i):                      # 0 -> A, 25 -> Z, 26 -> AA
    s = ''
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s

# 1) READ FRESH — same script run as the write, never cached.
res = svc.spreadsheets().values().get(
    spreadsheetId=SHEET_ID, range=f'{TAB}!A1:ZZ200').execute()
rows = res.get('values', [])
header = rows[0]

# 2) MAP column names -> letters from the LIVE header.
idx = {name.strip(): i for i, name in enumerate(header)}
print('live header:', header)            # sanity-check before touching anything

# 3) APPEND only what is missing; UPDATE in place what already exists.
new_cols = ['Người liên hệ', 'SĐT', 'Trạng thái']
start = len(header)
for k, name in enumerate(new_cols):
    if name not in idx:                  # append
        col = col_letter(start + k)
        svc.spreadsheets().values().update(
            spreadsheetId=SHEET_ID, range=f'{TAB}!{col}1',
            valueInputOption='RAW',
            body={'values': [[name]]}).execute()
        idx[name] = start + k
    else:                                 # already exists -> address by name
        col = col_letter(idx[name])

# 4) Write DATA per column (not per block), never over other columns.
c_name, c_phone = col_letter(idx['Người liên hệ']), col_letter(idx['SĐT'])
contacts = ['', 'Anh Phú', 'Trần Đức Tương', 'Trần Đức Tương', 'C. Khanh']
phones   = ['', '0983 668 ***', '0962 948 ***', '0962 948 ***', '0365 698 ***']
for col, vals in ((c_name, contacts), (c_phone, phones)):
    body = [v if isinstance(v, str) else str(v) for v in vals]
    svc.spreadsheets().values().update(
        spreadsheetId=SHEET_ID, range=f'{TAB}!{col}2:{col}{len(body)+1}',
        valueInputOption='RAW', body={'values': [[v] for v in body]}).execute()
```

## Pitfalls confirmed in this session

- **Off-by-one with a lookup list.** `links = ['', url_a, url_b, ...]` zipped as `links[i]` against
  `rows[i]` where `rows[0]` is the header → row 1 gets `''` and the final link is dropped.
  Index with `i + 1`, or keep the lookup headerless and use `links[i - 1]`.
- **Ragged payloads.** A row with more cells than the declared range width throws
  `tried writing to column [H]`. Pad every row to the same width, or compute the end column
  from `max(len(r) for r in block)`.
- **`'RAW'` vs `'USER_ENTERED'` for text.** Phone numbers, names, and status labels should be
  written with `valueInputOption='RAW'` so a string like `0983 668 ***` or `5trieu` is never
  coerced to a number or parsed as a formula. Use `USER_ENTERED` only when you intend formulas.
- **Data validation survives value writes but not tab recreation.** Re-attach dropdowns AFTER the
  final value write, and re-check that the validation range still lines up with the resolved column.
- **The dropdown range is a separate 400.** `setDataValidation` on the wrong column fails with
  `Invalid data[n]` even when the value write succeeded. Resolve the sheetId and column index from
  metadata, not from your assumption.

## Verify before declaring done

```python
check = svc.spreadsheets().values().get(
    spreadsheetId=SHEET_ID, range=f'{TAB}!A1:{col_letter(max(idx.values()))}3').execute()
for r in check.get('values', []):
    print(r)
```

Confirm: (1) the pre-existing `Link` column is still populated on every row, (2) the new columns
landed on the columns you intended, (3) the header row has no duplicate names.
