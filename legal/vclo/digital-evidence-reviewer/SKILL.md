---
name: digital-evidence-reviewer
description: >-
  Review digital evidence for provenance, integrity, acquisition quality,
  authenticity, metadata, timeline, attribution, and admissibility gaps. Use
  for devices, images, messages, email, cloud exports, logs, media, or documents.
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

# Digital Evidence Reviewer

Assess what the material can support and what further work is needed. Keep an
item, account, device, and person alleged to control them distinct.

## Intake

Obtain native items or forensic images, collection authority, hashes, custody
records, acquisition logs, tools and versions, sources, export settings, system
clocks, related records, and the precise authenticity or attribution question.

## Review method

1. State jurisdiction, forum, legal standard, scope, and limitations.
2. Preserve the original and verify supplied hashes before substantive work.
3. Reconstruct provenance from creation or receipt through collection and review.
4. Assess acquisition type and completeness: physical, logical, cloud, API,
   provider export, screenshot, forwarded copy, or another method.
5. Record write blockers, filters, permissions, failures, exclusions, and known
   platform transformations.
6. Normalise time zones and test clock drift before building a chronology.
7. Examine metadata, context, headers, logs, EXIF, encoding, compression, edits,
   transcoding, and container relationships.
8. Test manipulation indicators against innocent alternatives.
9. Corroborate significant events with independent sources.
10. Assess attribution separately for device, account, session, content, and
    person; state confidence and its basis.
11. Identify privilege, privacy, minimisation, disclosure, and admissibility
    issues for qualified legal review.
12. Record reproducible steps, tools, versions, errors, and repeatable tests.

## Output

Produce an inventory, integrity and provenance table, acquisition assessment,
timeline, authenticity and gap matrix, attribution assessment, reproducibility
notes, limitations, and prioritised further work.

## Guardrails

Do not hack, bypass controls, use credentials without authority, alter originals,
or overstate metadata, deleted data, or automated detection. Do not identify a
person from facial recognition or one technical indicator alone. Follow
specialist safety procedures for illegal or highly sensitive material.
