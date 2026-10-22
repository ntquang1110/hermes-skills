---
name: arbitral-award-analyst
description: Reads an arbitral award and produces a neutral map of jurisdiction, issues, findings, reasoning, operative relief, interest, costs, compliance dates, corrections, and enforcement dependencies. Use when a user asks what an award decided, why a party won or lost, what must now be paid or done, whether the dispositive section matches the reasoning, or what practical enforcement issues appear. Distinct from award-challenge-analyst, which assesses set-aside or enforcement-resistance grounds rather than explaining the award itself.
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

# Arbitral Award Analyst

## Purpose

Explain exactly what the award decided and what follows from it, separating the tribunal's holdings from party submissions, factual background, inference, and later legal assessment.

## Required inputs

Obtain the complete signed award, all separate or dissenting opinions, correction or interpretation decisions, relevant procedural orders, arbitration agreement, applicable rules, and any known enforcement or challenge context. Ask for the award date, receipt or service date, seat, status of payment or performance, and whether the user needs a neutral briefing, compliance plan, accounting, or enforcement orientation.

If pages, annexes, schedules, signatures, or operative portions are missing, proceed only to the extent possible and label affected conclusions `Unreviewable`.

## Method

1. Classify the decision: final, partial, interim, consent, costs, correction, interpretation, or other. Record tribunal composition, seat, institution, date, parties, claims, and stated procedural basis.
2. Build an issue-disposition matrix. For every claim, defence, counterclaim, jurisdictional objection, and requested remedy, record the tribunal's holding, principal reasoning, evidence relied on, and paragraph reference.
3. Distinguish majority reasoning, separate opinion, obiter observation, party submission, and factual finding. Do not attribute a submission to the tribunal as a finding.
4. Reconcile the reasons with the dispositive section. Flag omitted claims, inconsistent figures, ambiguous commands, unresolved interest, unclear currency, duplicate recovery, conditions, or relief that cannot be implemented from the text alone.
5. Recalculate the award arithmetically without changing it. Map principal, currency, pre-award interest, post-award interest, costs, tax, credits, set-offs, compounding, rate changes, and payment date assumptions. Show formulas and label interpretive choices.
6. Extract every obligation and deadline: payment, transfer, delivery, injunction, confidentiality, return of material, costs, reporting, and action needed to preserve a right.
7. Identify correction, interpretation, or additional-award mechanisms from the applicable rules and seat law. Verify current deadlines from authoritative sources using the actual receipt date; do not assume the award date starts time.
8. Create an enforcement-readiness map: assets or conduct targeted, proof of finality, originals or certified copies, translations, service, interest calculation, non-monetary implementation, and jurisdictions requiring separate advice.
9. Identify potential due-process, jurisdiction, public-policy, or reasoning concerns only as watchpoints. Route a merits assessment of challenge or resistance grounds to `award-challenge-analyst`.

## Output

Produce:

1. **Executive result** — winner by issue, net relief, immediate action, and critical dates.
2. **Issue-disposition matrix** with pinpoint award references.
3. **Reasoning summary**, organised by issue rather than page order.
4. **Operative-relief and calculation table**.
5. **Compliance and deadline ledger**.
6. **Ambiguities, omissions, and correction questions**.
7. **Enforcement-readiness watchlist**, expressly not a challenge opinion.

## Guardrails

- Do not infer an omitted holding or rewrite an ambiguous dispositive order as though it were clear.
- Do not state that an award is valid, final, enforceable, or immune from challenge without the governing law and procedural record.
- Do not calculate interest silently; show dates, rate, basis, compounding, currency, and assumptions.
- Do not disclose confidential award content beyond the user's authorised purpose.
- Do not treat factual or legal disagreement with the tribunal as itself a challenge ground.
