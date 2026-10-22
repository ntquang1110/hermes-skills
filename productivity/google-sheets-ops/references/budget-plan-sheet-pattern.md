# Multi-tab budget / plan sheet pattern

Reusable shape for building or repairing a 6-month budget + execution-plan workbook of the
"Mana Đất Vàng – Budget 6 Tháng" / Vua Kiềm kind. Learned from a full audit-and-deploy session.

## When to use

- User hands you a budget sheet and asks for a critique, a fix, or an extension
- User wants recruitment cost, R&D budget, and a product/registration timeline modelled in one workbook
- Any workbook that needs "baseline vs plan" comparison rather than a flat rewrite

## Tab architecture that worked

| Tab | Role |
|---|---|
| `Tổng quan` | Monthly matrix: rows = cost categories, cols = Tháng 1..6 + Tổng + % Ngân sách + Ghi chú |
| `Chi tiết Tháng N` | Line-item detail behind one month, with a `Ghi chú chi tiết` column |
| `Tham chiếu ngân sách` | Every number's justification + how it was derived ("Khảo sát giá thuê VP nhỏ Long Biên 8-15tr") |
| `Nhân sự` | Position, salary, headcount, total, status, notes; ends with a comparison block vs the old plan |
| `R&D Q4` | Line items × month columns + total; ends with a comparison block vs the old plan |
| `Timeline` | Mốc / Thời gian / Sản phẩm / Người phụ trách / Trạng thái / Ghi chú |

A `Tham chiếu ngân sách` tab is not decoration — it is what makes the budget defensible when the user
challenges a number. Always carry per-line justification, and cite the derivation inline.

## The expansion-row convention (important)

When a plan *supersedes* a baseline, do NOT overwrite the baseline row. Add a sibling row so both coexist:

```
1. Nhân sự (cũ)              35 / tháng          <- original
1b. Nhân sự mở rộng (mới)    43 then 83 / tháng  <- new plan
4. R&D Nguyên liệu & Test    original monthly
```

This preserves the "cũ vs mới" delta the user is actually buying. Highlight expansion rows with a distinct
fill and say so in the `Ghi chú` cell. Numbering `1b` / `4b` beats renumbering everything.

Also: the baseline in an inherited sheet is often **incomplete**. A real case had `5. Sản xuất EZ80`
(385tr over 6 months) missing entirely from `Tổng quan` while it existed in `Chi tiết Tháng 1`. The total
was understated by ~47%. Rewrite the number honestly and lead the report with the reason, because the user
will ask why the total jumped.

## Formula set

```
TỔNG CHI          =SUM(B2:B10)            per column, covers ALL item rows incl. inserted ones
DỰ PHÒNG (15%)    =B12*0.15
TỔNG NGÂN SÁCH    =B12+B13
NGUỒN VỐN         5000000000              (opening balance, first column only)
CÒN LẠI           =B15-B13  =B16-C13  =C16-D13  ...   <- running balance, cell to the LEFT
% Ngân sách       =IF($H$12=0,0,H2/$H$12)             <- absolute ref must point at TỔNG CHI, post-insert
```

Assert `sum(% Ngân sách) == 1.0` after writing. It is the fastest tell that an absolute ref went stale.

## Request-builder helpers

Build all formatting locally then push in ONE `batchUpdate`. Helpers worth re-typing every time:

```python
HDR  = {'red':1.0,'green':0.84,'blue':0.0}   # header vàng đậm
NEW  = {'red':0.85,'green':0.92,'blue':1.0}  # expansion rows
TOT  = {'red':1.0,'green':0.95,'blue':0.72}  # totals
GREY = {'red':0.88,'green':0.88,'blue':0.88} # reference / deferred blocks
REDL = {'red':1.0,'green':0.85,'blue':0.85}  # urgent rows
GRNL = {'red':0.85,'green':1.0,'blue':0.85}  # deadline rows

def hdr_req(sid, endcol):   # header fill+bold+wrap AND frozenRowCount:1 in one go
def width_req(sid, widths): # [220,105,...] pixel widths per column
def money_req(sid,r0,r1,c0,c1,fmt='#,##0')
def pct_req(sid,r0,r1,c0,c1)  # pattern '0.0%'
def bg_req(sid,r0,r1,c0,c1,color)  # also sets bold
```

Frozen header + sensible column widths + wrap on the `Ghi chú` column is the difference between a sheet the
user reads and one they ignore. Budget ~78 requests for a 7-tab workbook; it lands in one call.

## Audit checklist for an inherited budget sheet

Run all five before proposing anything. Every one of these was a real defect found:

1. **Line items present in detail tabs but missing from the summary** (the biggest one — cross-check every
   `Chi tiết Tháng N` section label against the `Tổng quan` row list)
2. **Wrong SUM ranges** — read with `valueRenderOption='FORMULA'` and check each `=SUM(...)` actually spans
   the intended columns/rows. e.g. `=SUM(G10:H10)` where `=SUM(B11:G11)` was meant
3. **Broken running balance** — negative "còn lại" from month 2 onward means the formula was transcribed as
   `prev_total - this_total` instead of a true running balance
4. **Numbering gaps** (4 → 6, so a whole cost line was deleted and its total never removed)
5. **Empty detail tabs** that the summary already sums as if populated

Load the workbook with `openpyxl(data_only=False)` when auditing — formula strings are visible, which is how
defects 2 and 3 get caught.

## Workflow that fits this user

1. **Critique first, code second.** Lead with the defects found, then the proposal, then the questions.
   Do not open by restating what you're about to do.
2. **HTML review page before touching the sheet** when the change is material. Publish via the `publish`
   skill, hand over the preview URL, let the user review. He asked for exactly this: *"đẩy toàn bộ lên html
   trước để anh review"*.
3. **"triển khai đi" means go — do not re-ask.** Deploy to the sheet, then state the assumptions you had to
   make at the END as a short list he can correct. Re-asking after a green light is friction.
4. **Re-publish the HTML after deploying** if the numbers moved. Leaving a stale total in a published review
   page is worse than never publishing it — the doc and the sheet must agree.
5. Reuse the same preview id when republishing a revision, or hand over the new one explicitly; don't leave
   two links in play without saying which is current.

## Pitfall: exhaust read fallbacks before reporting a blocker

The user pushed back with *"tại sao em k đọc được, em là người tạo sheet này mà"* after being told the API
was timing out. The public-export read path (`references/sheets-export-fallback.md`) worked the whole time.
When the user hands you a sheet link they expect you to already know, work the fallbacks and only report a
blocker if every path is dead. "I can't read it" reads as "I didn't try" when the sheet is link-shareable.

## Content rules for this user

- Vietnamese with full diacritics everywhere, including `Ghi chú` cells and headers. Numerals as digits
  (`15/10`, `30tr`), not spelled out.
- **No em dash / en dash** in sheet text or HTML. Use `.` `,` `:` or a plain hyphen.
- Currency presentation: keep the sheet in raw đồng with `#,##0`; present summaries in `tr`/`tỷ` in prose.
- State the month mapping explicitly (`Tháng 1 = 10/2026`) — inherited sheets are ambiguous and the whole
  timeline hinges on it.

## Re-grouping a budget by cost nature (nhóm chi phí)

Asked to turn a department-by-month budget into "nhóm chi phí", you are re-cutting the SAME money. The
group totals must sum to the summary tab's `TỔNG CHI`. Two failures inside one session, both caught only
by asserting equality:

- first attempt read **12 triệu high** — the office deposit exists in `Chi tiết theo tháng` but was never
  carried into `Tổng ngân sách`;
- after removing it, the total read **8 triệu low** — the `Bao bì` and `Vận chuyển` lines were missed.

Rules:

1. **A `Bỏ?` ("drop") column with `TRUE` means the row is EXCLUDED from the summary totals.** The
   workbook's arithmetic depends on it (it excludes `Nguyên liệu sản xuất 40tr`, `Nhân công 5tr`,
   `Quảng cáo online 20tr` in the Manna Đất Vàng book). Read that column and honour it. Do not decide
   for yourself which lines count, and do not "fix" the summary to include the flagged rows.
2. `assert sum(groups) == summary_total` **in the same script** and print both numbers. Do not write the
   table before they match.
3. Then diff `set(detail_rows)` vs `set(summary_rows)` and **report** rows present in one and absent from
   the other (the deposit case) as a finding. Silently absorbing the difference is the failure;
   surfacing it is the deliverable.
4. **Carry explicit units.** Write `M = 1_000_000` and multiply rather than bare `5+15+5` meant as
   "triệu". Bare ints produced `102,500,075` where `177,500,000` was intended — a 1.000× error whose only
   symptom was an odd-looking total. The equality assert is what catches it.

A grouping that reconciles for the Vua Kiềm Q4/2026 book (8 groups, in this order — group by NATURE, not
by department): Nhân sự / Mặt bằng và kho bãi / R&D và Lab / Kinh doanh và thị trường / Sản xuất (bao bì,
vận chuyển) / Chăn nuôi thử nghiệm / Pháp lý và chứng nhận / Dự phòng. Presenting it this way surfaced the
insight the department view hides: the top department "Kinh doanh 520tr" is mostly 343tr of trial-farm
feed cost, not selling cost, so it is a variable cost that can be stopped.

## Approving-limit proposal to the Chairman (đề xuất hạn mức)

Deliverable when Quang says "làm bản đề xuất hạn mức với chủ tịch". Two artifacts, same numbers:

- a new worksheet tab **`Đề xuất hạn mức`** added at the END of the existing file (never a new file), and
- a formal HTML report for the Chairman (see the `corporate-executive-html-report` skill for the visual
  tokens and section pattern; the sheet is the source of truth and the HTML must agree with it).

Tab block layout that worked (55 rows, six lettered blocks, headers `A.`..`F.` in a filled band):

| Block | Contents |
|---|---|
| `A` | Hạn mức theo phòng ban và theo tháng — dept rows × Tháng 10/11/12 + Tổng Q4 + % |
| `B` | Dòng tiền — Tồn đầu kỳ / Dự kiến thu tiền / Tổng chi / Tồn cuối kỳ / Runway (tháng) |
| `C` | Nhóm chi phí — Nhóm / Định kỳ tháng / Tổng Q4 / % |
| `D` | Đề xuất trần phê duyệt — Phòng ban / Trần tháng / Trần Q4 / Điều kiện kèm theo |
| `E` | Kiến nghị — numbered, each an action with a trigger |
| `F` | Điểm cần lưu ý — numbered, each a risk with the evidence |

Everything must ladder to one headline number the Chairman can hold in his head. The killer two derived
figures are **định kỳ/tháng** (the recurring, non-cuttable cost = the operating break-even revenue) and
**runway** (quỹ ÷ chi). Lead the report with those, not with the grand total.

Chunk the writes: build the header row, then 3–5 rows per `update` call, deriving each range from
`len(block)`. A 48-row bilingual block inline in one `execute_code` call times out mid-stream — see
pitfall 16 in SKILL.md.

Formatting pass that mattered: `#,##0` on every money column, `0.00` (not `#,##0`) on the Runway row, a
filled band on each block header, pixel width ~230 on the label column and ~420 on the `Điều kiện` column.
**Write Runway as text (`'6,58'`) with `valueInputOption='RAW'`** — a numeric `6.58` renders with a dot,
and Vietnamese convention is the comma.
