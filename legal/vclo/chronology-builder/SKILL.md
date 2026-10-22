---
name: chronology-builder
description: >-
  Build source-linked litigation chronologies from pleadings, correspondence,
  records, evidence, filings, and testimony. Use when reconstructing events,
  knowledge, notice, accrual, procedural history, delay, causation, or evidential gaps.
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

# Chronology Builder

Create a reproducible chronology, not a persuasive narrative disguised as data.
Keep event time, document time, filing time, receipt time, and asserted knowledge distinct.

## Intake

Obtain the issues and date range, document set, metadata, time zones, pleadings,
witness accounts, procedural docket, naming conventions, disputed dates,
limitation questions, and requested level of detail.

## Building method

1. Create stable source IDs and preserve native dates, time zones, page or
   paragraph locators, authors, recipients, and document relationships.
2. Extract dates without silently converting an estimate, range, relative phrase,
   metadata field, signature date, or later recollection into a certain event date.
3. Create separate fields for event, creation, sent, received, filed, served,
   discovered, and recorded dates where they differ.
4. Normalise display dates and times while retaining the source value.
5. Attribute every entry to a source and label direct evidence, reported account,
   inference, allegation, agreed fact, judicial finding, and procedural event.
6. Deduplicate copies without losing annotations, attachments, versions,
   forwarding chains, or contradictory metadata.
7. Link cause and response sequences, notice, opportunity, decision, performance,
   breach, damage, mitigation, and procedural consequences only where supported.
8. Record conflicting dates and accounts side by side. State the basis and
   confidence of any proposed resolution.
9. Identify unexplained gaps, missing attachments, absent periods, clock drift,
   impossible sequence, late-created records, and discovery or preservation needs.
10. Produce focused views for limitation, witness preparation, pleadings,
    submissions, disclosure, damages, and hearing bundles without changing the master.

## Output

Provide a master chronology with date, event, actor, source, locator, status,
confidence, issue tags, and notes; plus conflict, gap, and key-date schedules.

## Guardrails

Do not infer that a document was sent, received, read, agreed, or acted on merely
because it exists. Do not overwrite uncertainty or privilege labels. Protect
personal and confidential data and ensure exported chronologies remain traceable
to preserved sources.
