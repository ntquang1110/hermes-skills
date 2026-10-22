---
name: authority-validator
description: Tests whether each authority cited in a document actually supports the proposition it is cited for, remains good law, and is binding or merely persuasive in the forum the document is directed at — a substantive validity check, beyond confirming a citation exists and is quoted accurately. Use for "does this case actually support what we're citing it for", "is this authority still good law", "check whether these citations are binding on this court or just persuasive", or "stress-test the authorities in this opinion before we rely on them". Distinct from citation-integrity-checker (existence/accuracy only) and precedent-mapper (maps a body of authorities' relationships, not a specific document's citations for a specific use). Fires on any document whose citations need substantive validation before reliance.
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

# Authority Validator

## Purpose

Go beyond confirming a citation exists and is quoted accurately, to test whether it actually does the work the document asks of it: does the authority stand for the proposition cited, is it still good law, and does it bind (or merely persuade) the forum the document is directed at. A citation that exists, is accurately quoted, and is nonetheless being asked to support a proposition it does not actually establish is a more dangerous defect than a fabricated one, because it survives a surface check.

## Required inputs

Obtain the document containing the citations to be validated, and the forum the document is directed at (which court, tribunal, or regulator, and its position in the relevant hierarchy) — blocking, since binding-versus-persuasive status cannot be assessed without knowing the forum.

Where research tools or retrieval are available this session, use them to retrieve the actual text of each authority. Where they are not, or a specific authority cannot be retrieved, say so explicitly and produce a structured checklist of what needs manual verification rather than asserting a validation result that was not actually performed.

## Method

1. Extract every citation the document relies on for a substantive proposition — not a mere passing reference — and state, for each, exactly what proposition the document is citing it for, in the document's own words.
2. Where the authority can be retrieved, read enough of it to determine what it actually holds, distinguishing ratio from obiter, and compare that against the proposition the document cites it for. State plainly whether the authority supports the proposition as cited, supports a narrower or different proposition, or does not support it.
3. Check whether the authority remains good law — whether it has been overruled, distinguished in a way that undermines its application here, or superseded by a later statute or authority. Where this cannot be confirmed this session, flag it as an open verification point rather than assuming currency.
4. Determine the authority's status relative to the forum the document is directed at: binding (same or superior court in the same hierarchy), persuasive (a different jurisdiction, a lower court, or an international/foreign authority), or of uncertain status — and flag any authority the document treats as binding that is, on this analysis, only persuasive.
5. Where a statute or regulation is cited rather than a case, check that the cited provision is in force, unamended in the material respect, and actually says what the document asserts — the same substantive-support test applies to statutory citations, not only case law.
6. Distinguish a genuine misapplication (the authority does not support the proposition) from a defensible but arguable reading (the authority could support the proposition on one reasonable reading but not the only one) — state which the analysis has found for each citation, since the two call for different fixes.
7. Where multiple authorities are cited together for the same proposition, check whether they are actually consistent with each other, or whether the document has cited conflicting authorities as though they agreed.

## Output

1. **Header.** Document reviewed, forum the document is directed at, date, and which authorities could be retrieved this session versus flagged for manual verification.
2. **Authority validation table.** Citation | Proposition cited for | Actually supports (yes/partially/no) | Good-law status | Binding or persuasive for this forum | Note.
3. **Misapplications.** Every citation found not to support its cited proposition, with what the authority actually holds instead.
4. **Binding/persuasive mismatches.** Any authority treated as binding in the document that is only persuasive for this forum.
5. **Unretrievable authorities.** A checklist of what must be manually verified, with why it could not be checked this session.
6. **Points requiring verification.** Anything resting on currency or good-law status that could not be confirmed this session.

## Guardrails

- Do not validate an authority that could not actually be retrieved this session. List it as unretrievable and say what needs manual checking rather than asserting a result.
- Do not treat "the case exists and is quoted accurately" as sufficient. The test is whether it supports the specific proposition it is cited for, in this document.
- Do not assert that an authority remains good law without checking for a later overruling, distinguishing, or superseding development where retrieval tools allow it, and flag the question where they do not.
- Do not assume binding status from a citation's placement or prominence in the document. Determine it from the forum's actual hierarchy.
- Do not resolve an arguable reading as though it were a clear misapplication, or a clear misapplication as though it were merely arguable. State which the analysis found, plainly.
