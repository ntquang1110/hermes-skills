---
name: transaction-tracer
description: >-
  Reconstruct flows of funds across bank accounts, ledgers, entities,
  instruments, currencies, and blockchains. Use for asset tracing, fraud,
  insolvency, sanctions, AML, disputes, or source-linked transaction paths.
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

# Transaction Tracer

Make each funds-flow edge traceable to a source. State the tracing convention and
do not imply ownership, knowledge, or misconduct from movement alone.

## Inputs

Obtain the objective, jurisdiction, accounts, wallets, entities, period,
currencies, native statements, ledger, invoices, contracts, blockchain hashes,
addresses, networks, opening balances, FX sources, relationships, and limitations.

## Tracing method

1. Preserve raw records and build a normalised ledger with stable source IDs,
   timestamps, time zones, currencies, signs, counterparties, networks, tokens,
   and transaction identifiers.
2. Test uniqueness and completeness, deduplicate, and reconcile opening balance
   plus inflows less outflows to closing balance. List differences.
3. Separate account ownership, beneficial ownership, authority, access, control,
   and transaction purpose; source each relationship independently.
4. Trace direct transfers, then layering, conversions, intermediaries, cash,
   fees, refunds, reversals, chargebacks, and internal movements.
5. Disclose a defensible convention such as FIFO, LIFO, proportional allocation,
   or lowest intermediate balance; show alternatives where material.
6. Apply dated, sourced FX rates; retain original amounts and isolate valuation.
7. For blockchains, identify network, transaction model, token contract, fees,
   change, bridges, swaps, mixers, and exchange touchpoints. Separate on-chain
   observation from third-party attribution.
8. Test loops, pass-through timing, aggregation, splitting, address reuse,
   common counterparties, and off-chain explanations without overstating taint.
9. Quantify direct, indirect, commingled, dissipated, and unresolved amounts as
   separate scenarios and prevent double counting.
10. Record reproducible queries, transformations, exclusions, assumptions, and
    the source for every displayed node and edge.

## Output

Provide a source inventory, reconciliations, chronological ledger, funds-flow
table and map, relationship table, traced scenarios, gaps, and reproducibility
appendix.

## Guardrails

Do not access accounts or wallets, move funds, obtain credentials, or evade legal
process. Do not assume an address belongs to a person, attribution is certain, or
exposure proves control or guilt. Protect financial data and exculpatory paths.
