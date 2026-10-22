# Budget approving-limit report for the Chairman (đề xuất hạn mức)

Variant of this skill's formal-report pattern, for when Quang asks for
*"bản đề xuất hạn mức với chủ tịch"* built from existing budget sheets. Companion artifact is the
`Đề xuất hạn mức` worksheet tab in the same file — sheet is the source of truth, HTML must agree with it.
Sheet-side recipe: `google-sheets-ops` → `references/budget-plan-sheet-pattern.md`.

## Section order that worked

1. **Masthead** — company + document type + `Trình: Chủ tịch Hội đồng quản trị`, hairline below.
2. **H1 one-liner + lede.** Lead with the total AND the dead-cost share, then name the worst month.
   Phrasing that landed: *"Tổng chi Quý 4 là 1,46 tỷ đồng, trong đó 23% là chi phí chết mỗi tháng"*.
3. **KPI strip (4)** — Tổng chi kỳ · Định kỳ mỗi tháng · Chi tháng nặng nhất · Runway. Each with a
   `note` line carrying the comparison (e.g. `29,2% vốn 5 tỷ`).
4. **`01` Hạn mức theo phòng ban và theo tháng** — dept × month table + Tổng + % column, then a
   **dòng tiền** table beneath it (Tồn đầu kỳ / Dự kiến thu / Tổng chi / Tồn cuối kỳ / Runway).
5. **`02` Nhóm chi phí** — group table (Định kỳ/tháng, Tổng, %, Bản chất) + inline bar chart + two cards:
   *"ba nhóm chiếm X% ngân sách"* and *"đòn bẩy nếu cần siết ngân sách"*.
6. **`03` Đề xuất trần phê duyệt** — per-department ceiling + `Điều kiện kèm theo`, then flow chips
   `Định kỳ 325tr/tháng → Thu tối thiểu 325tr/tháng → Hòa vốn vận hành → Runway không giảm`.
7. **`04` Rủi ro và kiến nghị** — a `warn` card holding *decisions the Chairman must make*, then a plain
   card holding numbered recommendations each with a trigger.
8. **Footer** — người lập, **nguồn số liệu (name the source tabs)**, đơn vị, tháng.

Use the skill's design tokens as-is. Numbers in prose as `1,46 tỷ` / `325 triệu`; exact separators only
inside tables. This document is a decision aid — "kết quả trước", never a methodology narrative.

## Hard rules

- **Never invent a preview URL.** Publish, read the returned `preview_url`, and use that exact string.
  A plausible-looking id is indistinguishable from a real one until the Chairman clicks it and gets a 404.
- **Every figure traces to a named source tab** — name them in the footer. Any derived total (a
  re-grouping, a sum of sums) must be reconciled against the summary tab before it is written down.
- **Surface cross-tab discrepancies as a callout rather than silently picking one number.** Real case: a
  12.000.000 office deposit existed in the detail tab but was never carried into the summary tab, so the
  honest total was 1.473.976.000, not 1.461.976.000. Report it; don't absorb it.
- The two derived figures that carry the argument are **định kỳ/tháng** (the recurring, non-cuttable cost
  = operating break-even revenue) and **runway** (quỹ ÷ chi). Lead with these, not the grand total.
- Vietnamese decimal comma in prose and in the sheet. `#,##0` for money. No em dash / en dash.

## Verification after editing the HTML

Run these every time a section is patched in — they are cheap and each has caught a real defect:

- **Tag balance.** `<div>` count must equal `</div>` (same for `table`, `tr`). Patching a block in once
  silently swallowed a closing `</div>`; the page still "rendered", only the layout was wrong.
- **f-string vs backslash.** `f"{len(re.findall(r'<div\b', t))}"` raises
  `SyntaxError: f-string expression part cannot include a backslash`. Assign counts to variables first,
  then interpolate.
- **Live assertions on the published page** (via `browser_console` with an `expression`):
  `jsErrors == 0`, `document.documentElement.scrollWidth <= window.innerWidth` (no horizontal overflow),
  expected `table`/`h2` counts, and `(document.body.innerText.match(/[—–]/g) || []).length == 0`.
- **Re-read every number in the HTML against the sheet after any edit.** A stale total in a published
  report is worse than never publishing it.
- `browser_vision` may be unavailable — the `browser_console` assertions above are the substitute, and
  they are stricter than eyeballing a screenshot.

## Closing the reply

End with the two links (preview URL + the sheet URL the user gave you), the headline table, and then a
short list of the items you could **not** verify and need him to confirm. Quang reads the unverified list
first — it is what tells him whether the document is safe to forward.
