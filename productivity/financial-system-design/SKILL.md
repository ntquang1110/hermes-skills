---
name: financial-system-design
description: "Use when setting up financial tracking for SME companies."
---

# Financial System Design for SMEs

## When to use

- CEO needs financial numbers but has limited accounting resources
- Setting up tracking from scratch for a new or existing company
- Accountant is a bottleneck (wants perfect process, delays output)
- Need numbers fast for decisions, not just end-of-period reports
- Multiple companies need consistent financial tracking

## Core framework: The 2-Layer Approach

```
                    ┌──────────────────────┐          ┌──────────────────────────┐
                    │  LAYER 1             │          │  LAYER 2                 │
                    │  CEO Dashboard       │  data →  │  Accounting Reports      │
                    │  (daily ops input)   │  EOM     │  (accountant verifies)   │
                    │                       │          │                          │
                    │  80% accurate today   │          │  100% accurate EOM       │
                    │  15 min/day input     │          │  3-5 day turnaround      │
                    └──────────────────────┘          └──────────────────────────┘
```

**Layer 1** is for the CEO. Simple, fast, good enough to decide.
**Layer 2** is for the accountant. Proper, verified, audit-ready.

## Accounting First Principles (for CEOs)

### 1. Double Entry (Ghi sổ kép)
Every transaction has two sides: Debit (Nợ) and Credit (Có). Total Debit = Total Credit always. If it doesn't balance, something is missing.

**CEO takeaway:** When accountant says "không cân" — it's missing data, not a crisis.

### 2. Accrual Basis (Cơ sở dồn tích)
Record when the transaction happens, not when cash moves. Revenue in January even if paid in March.

**CEO takeaway:** Company can show profit on P&L but have no cash. Always check Cash Flow too.

### 3. Matching (Phù hợp)
Record expenses in the same period as the revenue they generated. Buy inventory in Jan → record as asset. Sell in Feb → record as expense.

**CEO takeaway:** A month where you buy a lot but haven't sold will look more profitable than it is.

### 4. Materiality (Trọng yếu)
Small items can be estimated. 1-2% error on totals is acceptable.

**CEO takeaway:** When accountant wants perfect precision on a 50k item — push back.

## Three Core Financial Statements

| Statement | Question it answers | Trap |
|-----------|-------------------|------|
| **P&L (KQKD)** | Are we profitable? | Profit ≠ cash in bank |
| **Balance Sheet (CĐKT)** | What do we own? What do we owe? | Bad debt hides in "Receivables" |
| **Cash Flow (LCTT)** | Where did the money go? | Negative for too long = death |

CEO instinct is to watch P&L. Must watch Cash Flow too.

## Chart of Accounts (quick reference)

```
TK 1xx — Assets (cash, receivables, inventory, fixed assets)
TK 2xx — Liabilities (payables, taxes, loans)
TK 3xx — Equity
TK 4xx — Revenue
TK 5xx — Expenses (COGS, labor, overhead, selling, admin)
```

**CEO takeaway:** Don't need to memorize account codes. Just classify: Revenue / Expense / Receivable / Payable / Cash.

## Standard Sheet Structure

Build a Google Sheet with these tabs:

### Data tabs (daily input by ops staff, 15 min/day):

1. **DOANHTHU** — Daily revenue log
   Columns: Ngày, Mã đơn, Khách hàng, Sản phẩm, Nhóm SP, SL, Đơn giá, Thành tiền, Đã thu (C/K), Ngày thu, Ghi chú

2. **CHIPHI** — Daily expense log
   Columns: Ngày, Mô tả, Nhà cung cấp, Nhóm CP, Số tiền, Hình thức (Tiền mặt/CK), Hóa đơn (C/K), Ngày TT, Ghi chú

3. **CONGNO** — Receivables & Payables
   Columns: Đối tác, Loại (Phải thu/Phải trả), Số HĐ, Số tiền, Ngày PS, Hạn TT, Ngày TT, Trạng thái, Ghi chú

### Summary tab (auto-calculated, no input needed):

4. **DASHBOARD** — CEO overview
   - Total revenue, collected vs uncollected
   - Total expenses, paid vs unpaid
   - Gross profit + margin
   - Receivables / Payables summary
   - Revenue by product group (SUMIF)
   - Expenses by category (SUMIF)

### Accounting tab (handoff to accountant):

5. **KETOAN** — General journal format
   Columns: Ngày, Chứng từ số, Diễn giải, TK Nợ, TK Có, Số tiền, Nguồn, Ghi chú

## Handling Accountant Bottlenecks

### Common accountant stalls and how to reply:

| Accountant says | Translation | Your reply |
|----------------|-------------|------------|
| "Cần quy trình hoàn chỉnh" | Wants to delay | "Quy trình tối thiểu trước. Hoàn chỉnh sau." |
| "Thiếu nhiều dữ liệu" | Hasn't specified what | "Thiếu cái gì? Lấy ở đâu? Ai lấy? Bao giờ có?" |
| "Phải có chứng từ gốc" | Won't start without perfect docs | "Số tạm trước. Chứng từ bổ sung cuối tháng." |
| "Cần làm đúng nguyên tắc" | Fear of being wrong | "80% đúng hôm nay > 100% đúng tháng sau." |

### Key principle: Accountant is a resource, not a manager

- Do NOT involve accountant in designing the data collection system
- Give them data at end of period, set a firm deadline (3-5 days)
- Do not discuss process — discuss output only

## Implementation checklist

- [ ] Identify who inputs data daily (ops staff, 15 min/day)
- [ ] Set up Google Sheet with all tabs
- [ ] Define product groups and expense categories for SUMIF formulas
- [ ] Train input person (no accounting knowledge needed — just type numbers)
- [ ] Week 1: start tracking. Don't wait for perfect data.
- [ ] End of month: hand off to accountant with 3-5 day deadline
- [ ] Review dashboard weekly with CEO

## Pitfalls

1. **Letting accountant design the system** — they'll make it too complex. CEO designs the tracking, accountant just verifies.
2. **Waiting for perfect data** — start with what you have. 80% today beats 100% next month.
3. **One person both inputs and analyzes** — separate collection (ops) from verification (accountant).
4. **Not freezing the accountant's deadline** — without a hard deadline, EOM reports drift to mid-next-month.
5. **Over-engineering the sheet** — start simple. Add columns only when you actually need them.
6. **Forgetting Cash Flow** — P&L can show profit while the company runs out of money.

## References

See `references/manna-dat-vang-example.md` for a concrete implementation example with actual product categories, formulas, and formatting used for Vua Kiềm / Manna Đất Vàng.
