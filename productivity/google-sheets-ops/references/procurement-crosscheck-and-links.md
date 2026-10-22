# Cross-check a tick list against a second sheet, then append only the delta

Recurring ask from Quang (Vua Kiềm lab setup): *"Em vào xem còn gì anh đang tick mua trong sheet X
cột [Pick?] chưa có thì em thêm mới dòng vào ngay dưới trong sheet Y. Có link mua hàng thì em đi
tìm xong điền vào nhé."*

Two tabs are involved: a **master list** (many rows, a tick/`Pick?` boolean column) and a **target
sheet** (the actual procurement doc that gets sent to the buyer). The job is the set difference, then
link sourcing.

## Step 1 — read both sides fresh

```python
# master: row, item, qty, supplier, link, pick?
r = svc.spreadsheets().values().get(spreadsheetId=SID, range="'Lab Vật tư'!B2:O49").execute()
ticked = [row for row in r.get('values', []) if str(row[13]).upper() in ('TRUE','X','1','CÓ')]

# target: existing item names
t = svc.spreadsheets().values().get(spreadsheetId=SID, range="'Trang thiết bị phòng lab'!A1:I40").execute()
existing = [row[1] for row in t.get('values', [])[1:] if len(row) > 1 and row[1]]
```

Print both sets with an `X`/blank mark before doing any writing. Confirm the tick-column index by
reading the **live header row** first — do not assume it (this sheet had `Pick?` at index 13 / column O,
but earlier revisions had the tick column elsewhere).

## Step 2 — compute the delta and show it

Match on normalised item name (strip whitespace, lowercase). Report the counts explicitly:
`15 ticked, 10 already present, 5 missing`. Items already present get **nothing** — do not re-add them
under a slightly different name.

## Step 3 — append only the missing rows, at the bottom

Find the last non-empty row, then write the new block starting one row below it. Reuse the target
sheet's existing formula shape for the computed column (e.g. `=E12*D12`), preserving the row offset, and
re-attach data validation to the new rows:

```python
service.spreadsheets().batchUpdate(spreadsheetId=SID, body={'requests': [
  {'setDataValidation': {'range': {'sheetId': SID, 'startRowIndex': 11, 'endRowIndex': 20,
     'startColumnIndex': 7, 'endColumnIndex': 9},
   'rule': {'condition': {'type': 'BOOLEAN'}}}}]}).execute()
```

Do **not** rewrite rows above the insertion point — Quang edits this sheet live.

## Step 4 — link sourcing

Search for a real purchase link per item (`mcp__tinyfish__search` with `location='VN'`,
`language='vi'`). Prefer a supplier category page over a deep product permalink — product URLs rot fast
on VN e-commerce, category pages survive. Reliable supplier sites seen repeatedly:
`labvietchem.com.vn`, `lysonsakylab.vn`, `lysonsaky.com.vn`, `visitech.vn`, `techlab.com.vn`,
`mephalab.com`, `ultratech.vn`, `biologix.vn`, `maydotantien.com`, `tiamo.vn`, `ttlab.vn`.

**Never invent a link.** If no real result was found, leave the cell blank and say which rows are still
unlinked in the reply.

## Step 5 — verify and report

Re-read the target sheet, count rows, assert every item row has a non-empty link, and paste the table
back. Report: rows added, rows already present, rows still unlinked, and any **internal contradiction
between sheets** (this session: target sheet said "Điều hòa 12000BTU" while the construction tab said
24000BTU — flag it and ask the user to pick one rather than silently overwriting either).

## Decision-support column pair (Quang's preferred shape)

When he asks *"cái này có tác dụng gì, hiệu quả thế nào để anh xác định có nên mua"*, add two prose
columns to the master list:

- `Tác dụng trong quy trình` — what the item does, named against the actual process steps
  (pha chế / chiết xuất / sấy khô / đo đạc), not a generic product description.
- `Nếu KHÔNG có thì sao` — the concrete consequence: what breaks, what it costs, what fails inspection.
  This is the column he actually decides on.

Also mark items that should NOT be bought yet (deferrable) and say why — e.g. "trộn tay được, chờ khi
sản xuất batch lớn". He wants the deferral called out, not silently included in the total.

## Budget reality check

Always compare the summed total against the line item already budgeted in the master budget sheet
(this session: "Setup Lab" had 20.000.000 allocated vs ~47.000.000 of real construction cost). State
the overrun in absolute đồng and propose a staged split (đợt 1 / đợt 2) rather than presenting a total
that silently blows the budget.

## Critique the user's OWN list before writing it in

The two sheets are not the only source of error — the list Quang hands you is often incomplete, or carries
a spec copied from an old supplier quote. Run three passes and **state what you changed** before/while
writing:

1. **Completeness — what does the process need that the list omits?** Real case: a lab construction list
   had dọn dẹp / sơn / đèn / thoát nước chậu rửa / điều hoà / vệ sinh but **no air exhaust**, so the fume
   hood and drying oven had no path for hot, solvent-laden air to leave a sealed room. Added as its own
   row and labelled `THIẾU TRONG YÊU CẦU CỦA ANH`.
2. **Wrong technical spec — a rating carried over from an outdated quote.** Real case: "6 đèn 65W" is
   obsolete halogen: 390 W for a ~20 m² room, running at ~200 °C and not genuinely IP65. LED 12 W IP65
   gives equivalent light at 72 W total and ~40 °C. Write the corrected spec into the sheet **and** say
   explicitly which cell to edit to revert (*"sửa ô E5 là xong"*) so the correction is cheap to reject.
3. **Unnecessary scope — a premium option the actual work does not need.** Real case: epoxy wall paint for
   a botanical-extraction room, where acrylic anti-humidity is sufficient. Keep both as labelled
   `lựa chọn A` / `lựa chọn B` rows with the price delta, so the decision stays his.

Never silently "improve" his list. Write the item in, put the reason in the `Ghi chú` cell, and repeat the
delta in the reply — he reviews the delta first, not the prose.

## Report the split, not one number

When a tick list mixes purchase orders and one-off works, close the reply with three figures he can act on
separately: **total ticked**, **newly added this round**, and **overrun vs the budgeted line**, plus the
list of items he should NOT buy yet. One combined total hides the decision.
