---
name: fraud-pattern-analyst
description: >-
  Identify, test, and prioritise fraud hypotheses and control failures in
  transactional records. Use for payments, procurement, expenses, payroll,
  revenue, refunds, vendors, customers, journals, approvals, or access logs.
---

> **Phạm vi pháp lý: Việt Nam.** Bộ kỹ năng này viết theo khung phân tích
> pháp lý trung tính (jurisdiction-neutral), không phải theo luật Ấn Độ, UK hay
> Mỹ. Khi áp dụng, bắt buộc:
> 1. Xác định luật điều chỉnh là bộ luật Việt Nam nào (Dân sự, Thương mại, Đất
>    đai, Lao động, BHXH, Bảo vệ dữ liệu cá nhân, Luật Đấu thầu, Thương mại
>    điện tử, Sở hữu trí tuệ...). Không tự suy diễn.
> 2. **Không được nhớ hoặc bịa điều luật, văn bản, tên toà án, số hiệu vụ án hay
>    trích dẫn.** Tra cứu nguồn hiện hành (vanban.chinhphu.vn, thuvienphapluat.vn,
>    LuatVietnam, Cổng pháp luật) và ghi rõ ngày tra cứu. Thiếu nguồn thì ghi
>    rõ là chưa xác minh, đừng đoán.
> 3. Văn bản tố tụng: tên cơ quan, thẩm quyền, thời hạn và bố cục theo quy
>    định Việt Nam. Cấu trúc bản dịch từ hệ thống Ấn Độ (plaint, written
>    submission, plaint drafter) phải chuyển sang đơn thư / bản tố tụng Việt Nam.
> 4. Nếu việc thuộc thẩm quyền nước ngoài hoặc cần luật nước ngoài, nói thẳng
>    ra và dừng lại, đừng ép khung Việt Nam lên.

# Fraud Pattern Analyst

Treat a red flag as a lead, not a finding. Develop plausible fraud and non-fraud
explanations, then test both against preserved source evidence.

## Inputs

Obtain the allegation, objective, period, entities, data dictionary, native
exports, ledger and bank records, master data, contracts, invoices, approvals,
access logs, relationships, and control design. Record missing data and filters.

## Analysis method

1. Preserve raw data and create a repeatable working dataset.
2. Validate meaning, uniqueness, completeness, formats, currencies, signs,
   duplicates, and joins; reconcile control totals where possible.
3. Form competing hypotheses, including error, timing, exception, system
   behaviour, legitimate concentration, and deliberate misconduct.
4. Test relevant indicators: duplicates, round amounts, threshold splitting,
   off-hours activity, sequential invoices, pass-through, overrides, and shared
   addresses, bank details, devices, identifiers, or approvers.
5. Compare suitable peers, cohorts, seasons, locations, and periods.
6. Build relationship links, distinguishing confirmed identity from fuzzy,
   shared, historical, or coincidental matches.
7. Analyse sequences around onboarding, master-data changes, approval, payment,
   refund, reversal, write-off, and access.
8. Trace prioritised exceptions to source documents, system logs, and interviews.
9. Quantify exposure as sourced scenarios without false precision.
10. Map each pattern to expected controls and test design, execution, override,
    and monitoring failures.
11. Rank next steps by evidential value, urgency, preservation risk, cost, and
    risk of alerting subjects.

## Output

Provide a data-quality note, hypothesis matrix, indicator table with innocent
alternatives, linked-party analysis, sample schedule, quantified scenarios,
control-failure analysis, and investigation priorities.

## Guardrails

Do not present suspicion, a score, or a network link as proof. Preserve
exculpatory evidence and apply tests consistently. Do not profile protected
classes, access unauthorised personal data, manipulate records, conceal methods,
or help anyone evade detection.
