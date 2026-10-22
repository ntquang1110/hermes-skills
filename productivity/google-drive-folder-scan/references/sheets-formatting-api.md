# Google Sheets formatting via `googleapiclient` — API quirks

Recovered from a live run (Drive folder -> farm inventory sheet). Covers the
batch-debugging path from `Invalid...` errors to a working formatted sheet.

## Getting the real grid / sheet id
The default hand-written `sheetId: 0` is wrong for a freshly-created sheet.
Fetch the real one:
```python
sp = gs.spreadsheets().get(spreadsheetId=SID,
                           fields="sheets(properties.sheetId,properties.title)").execute()
gid = sp["sheets"][0]["properties"]["sheetId"]   # e.g. 1025531923, never safe to hardcode 0
```
Using `sheetId:0` in batchUpdate `range` objects raises:
`Invalid requests[0].repeatCell: No grid with id: 0`.

## Correct request names (batchUpdate `requests` list)
| Intent | Correct request | Gotcha |
|---|---|---|
| column/row width | `updateDimensionProperties` | Writing `setDimensionProperties` -> `Unknown name "setDimensionProperties" ... at 'requests[2]'` |
| bold/background header | `repeatCell` with `userEnteredFormat.textFormat.bold` + `backgroundColor` | fields: `userEnteredFormat(textFormat.bold,backgroundColor)` |
| enable filters | `setBasicFilter` with `filter.range` | range needs the real `sheetId` |
| wrap long text | `repeatCell` `userEnteredFormat.wrapStrategy:"WRAP"`, `verticalAlignment:"TOP"` | fields: `userEnteredFormat(wrapStrategy,verticalAlignment)` |

## Writing data + links in one pass
- `valueInputOption="USER_ENTERED"` so `=HYPERLINK(...)` formulas evaluate on write.
- Link column value: `=HYPERLINK("https://drive.google.com/drive/folders/<ID>","Folder gốc")`.
- Re-running the same `values().update` over the same range is idempotent (overwrite,
  not append) so the fill script can be re-run safely.

## Verification loop
After update + batchUpdate, read back with `values().get` and inspect a projection
(farm | pháp nhân | liên hệ | status | link present) before reporting done. Confirm:
- leading-zero phone numbers survived (see SKILL.md pitfall — they drop the 0 in
  USER_ENTERED unless written as text)
- hyperlink column actually has the formula (shows "YES" vs empty)
- row count = header + entities expected

## Download-side reminder
Binary files must go through `get_media()` (MediaIoBaseDownload), NOT
`files().export()` which 403s with "Export only supports Docs Editors files." on
.docx/.pdf/.doc. Native files (when the id is a Docs/Sheets app) use `export`.