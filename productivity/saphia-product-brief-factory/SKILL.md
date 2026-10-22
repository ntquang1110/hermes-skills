---
name: saphia-product-brief-factory
description: "Build a Saphia TPBVSK product brief for a new condition."
version: 1.0.0
author: Hermes Agent (Saphia brief framework distilled from 05 briefs 05/09/2026)
license: internal
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [saphia, product-brief, tpbvsk, mlm, kiem-thao-duoc, research, strategy]
    related_skills: [design-critique, web-research, pubmed-evidence-research, grounded-citations, vietnam-corporate-research, kiem-saphia-product-docs, humanizer, xlsx, docx]
---

# Saphia Product-Brief Factory

Reusable factory that turns ONE target condition (e.g. "đau nửa đầu", "đái tháo đường", "viêm gan") into a complete, decision-ready **Product Development Brief** on the **Saphia Kiềm Thảo Dược** platform — the same class of brief as the 5 already produced (Tim mạch CV-01, Xương khớp MS-01, Giấc ngủ–Stress, Thận–Tiết niệu, Gan–Mật–Tiêu hóa; ngày 05/09/2026). Lets Quang scale to any new indication without re-deriving the structure.

## When to use
- User wants a new health-condition product brief for Saphia ("làm brief cho bệnh X", "scale ra thêm ngách Y").
- User drops a new Drive folder of briefs to be read/distilled/benchmarked.
- User asks "mình nên làm sản phẩm gì tiếp trên nền Kiềm Thảo Dược".
- Don't use for: general research without a product/deployment lens, or non-Saphia platforms.

## Core principle (same as the source briefs)
Every brief is a **systematic critique → decision** document, NOT a sales memo. It must name where the platform claim is weak, pick ONE hero door, and give R&D the exact formula/liều/legal/RFI. Critique-first, evidence-leveled, MLM-retention-aware (khách phải cảm nhận được trong 2–4 tuần hoặc có chỉ số đo được).

## INPUT SPEC — what the user must provide (or you must fetch)
Before writing, establish ALL of these. Gap any you cannot get and say so (DATA GAP), don't fabricate.

1. **Target condition** (the disease group / cluster requested).
2. **Platform facts** — Kiềm Thảo Dược: patent #41442, base composition (khoáng Ca/Na/K/Mg + thảo dược Xạ đen/Hoàn ngọc/Tía tô/Chè dây), thành phẩm pH 12–14, dạng dung dịch/TPCN. (Pull from `kiem-saphia-product-docs` + memory if not stated.)
3. **Channel & financials** — kênh MLM Saphia, 24 tháng đầu; trần giá/tháng; trần giá vốn; kích cỡ tệp khách.
4. **Available evidence** — epidemiology for VN, competitor price survey, existing platform studies (VNUA 2022 InVitro+InVivo — chỉ lợn), any prior lab data.
5. **Output target** — HTML brief (B/W/Y Premium per memory), ngôn ngữ VI (mặc định; EN/ZH nếu được yêu cầu rõ).

## ORCHESTRATION — smaller skills to feed data (call in this order)
| Data need | Skill to invoke |
|---|---|
| VN epidemiology, market sizing TAM/SAM/SOM, competitor prices/positions | `web-research`, `vietnam-corporate-research` |
| Verified actives evidence (PMID/DOI per thành phần × chỉ định) | `pubmed-evidence-research` (KHÔNG bịa PMID; evidence level A/B/C/D/GL) |
| Inline citations + Sources ledger | `grounded-citations` (sources.py add → cite → verify) |
| Source briefs from Drive (nếu input là folder) | `google-drive-folder-scan` |
| Output spreadsheets/sheets for product catalog | `xlsx` |
| VN-facing claims text | `humanizer` (bắt buộc trước khi gửi duyệt) |
| Packaging of the brief to a link | `publish`/KV preview.thefirstonly.com (bắt buộc publish link — máy Quang không Hermes) |

Load `design-critique` philosophy throughout: critique the plan before writing, expect trade-offs and gaps.

## OUTPUT — the brief skeleton (one HTML, project-coded e.g. CV-01)
Follow `templates/brief-framework.md` exactly. Full section list is in `references/framework-structure.md`. The non-negotiable spine (present in all 5):

1. Executive Summary — kết luận 1 dòng (GO/NO-GO + hero + door) + 7 kết luận cốt lõi + 3 điều KHÔNG được làm.
2. Executive Research Framework — 10 câu hỏi quyết định, trả lời ngắn trước.
3. Quy mô vấn đề — phân cụm theo evidence-level (FACT/EVIDENCE/INFERENCE/DATA GAP).
4. Market Sizing TAM/SAM/SOM — MÔ HÌNH ƯỚC TÍNH có giả định, ghi rõ độ tin cậy; KHÔNG đưa TAM vào tài liệu đào tạo NPP.
5. Customer segmentation & scoring — chọn segment mục tiêu, loại segment ngoài phạm vi (kèm lý do).
6. Customer Pain & Jobs To Be Done — Functional/Emotional/Social; xếp pains theo sẵn sàng chi tiền.
7. Competitive landscape + phân tích đối thủ (≥20 sản phẩm đại diện, giá VN thật).
8. Market Gap & Opportunity Matrix + TOP 5 cơ hội.
9. Opportunity Scorecard (14–15 tiêu chí).
10. Đánh giá nền tảng Kiềm Thảo Dược — **đây là phần đối chiếu nền tảng bắt buộc**, xem `references/platform-rules.md`.
11. Hero Product vs Platform quyết định (mặc định: 1 Hero + SKU vệ tinh, không platform 4 SKU).
12. 3 Product Concept + chọn 1.
13. Nguyên lý thiết kế công thức + bảng thẩm định thành phần.
14. Cơ chế tác động.
15. Kiến trúc công thức MoSCoW (MUST/SHOULD/COULD).
16. Công thức đề xuất & liều (đủ liều nghiên cứu hoặc loại bỏ — không liều tượng trưng).
17. An toàn & tương tác thuốc (ưu tiên cao nhất: K với ACEi/ARB & suy thận; tương tác serotonergic; chống đông).
18. Pháp lý & giới hạn công bố (NĐ 15/2018, NĐ 342/2025 hiệu lực 15/02/2026, NĐ 18/2023 MLM, NĐ 46/2026) + bảng ngôn ngữ được/không được.
19. Product Development Brief cho R&D/OEM — kể cả RFI (≥20 câu; 3 mức sản lượng 30k/100k/300k).
20. Lộ trình G1–G7 & tiêu chí nghiệm thu + kế hoạch 90 ngày.
21. Devil's Advocate & risk mitigation.
22. Sources (verified, từ ledger).

## CRITICAL: đối chiếu nền tảng Kiềm Thảo Dược (rút từ 5 brief — KHÔNG bỏ qua)
Load `references/platform-rules.md` (bắt buộc). Bản chất:
- **CẤM** dùng "uống kiềm cân bằng pH nội bào/trung hòa acid dư" làm trục khoa học — y văn 2026 (Frontiers in Medicine) phản bác; cơ thể giữ pH máu 7,35–7,45 qua thận–phổi–đệm. Đây là rủi ro pseudoscience lan cả danh mục.
- **Vai trò đúng**: hệ dẫn khoáng thảo dược sinh khả dụng cao (K, Mg, Ca) + patent #41442 + thương hiệu. Giữ patent & danh mục, chuyển trục khoa học.
- **NGOẠI LỆ duy nhất**: sỏi tiết niệu — pH NƯỚC TIỂU thay đổi được bằng đường uống và đo được tại nhà (liệu pháp citrate kiềm, EAU). Xương khớp: giữ lại calci đã nạp (giảm calci niệu + NTX), KHÔNG cải thiện BMD.
- **pH thành phẩm 12–14 là rủi ro** (kiềm chuyển hóa, phá hủy hoạt chất nhạy kiềm: crocin, withanolides; ảnh hưởng hấp thu thuốc). Hạ về 8,0–9,0 (tim mạch) / pH niệu 6,2–6,8 (thận). Với sản phẩm chứa hoạt chất nhạy kiềm: tách pha (sachet đôi), hạ pH, hoặc vi nang hóa — báo R&D tại G1.
- **An toàn Kali**: khách dùng ACEi/ARB & suy thận (CKD G3–G5) — KDIGO khuyến cáo hạn chế Kali. Chốt ngưỡng an toàn trước khi chốt công thức.

## R&D + MLM principles (from the summary sheet — load `references/cross-cutting-rules.md`)
1. Mỗi công dụng phải được gánh bởi MỘT thành phần có bằng chứng đúng chỉ định, đúng liều nghiên cứu.
2. Không đủ liều thì LOẠI, không đưa liều tượng trưng. Công thức 5 thành phần đủ liều > 15 thành phần dưới liều.
3. Mọi sản phẩm cần LỚP LỢI ÍCH CẢM NHẬN ĐƯỢC trong 2–4 tuần HOẶC chỉ số đo được tại nhà (huyết áp kế, que thử pH niệu, sức nắm tay, men gan). Rơi rụng số 1 của MLM là tháng 2 không cảm nhận được.
4. Hệ che vị là SỐNG CÒN (nền khoáng liều cao vị kim loại/chát/đắng). Thử cảm quan mù ≥30–50 người = điều kiện nghiệm thu.
5. Pháp lý: kịch bản bán hàng hiện hành đang vi phạm testimonial "khỏi bệnh" — phải sửa. Cấm chứng thực bác sĩ/nhân viên y tế, cấm "khỏi bệnh", cấm "điều trị", "thay thế thuốc", "giảm liều thuốc".

## Workflow
1. **Confirm the frame first** (design-critique gate): trình 1 trang — condition, clusters, candidate hero door(s), data gaps, đối chiếu nền tảng sơ bộ. Được 'triển khai đi' mới viết.
2. **Load inputs** (source briefs from Drive via `google-drive-folder-scan`, or user paste).
3. **Gather data** via orchestration table above; run `grounded-citations` ledger; run `pubmed-evidence-research` for actives.
4. **Đối chiếu nền tảng** (`platform-rules.md`) — xác định vai trò kiềm thật, cảnh báo pseudoscience, pH, Kali safety.
5. **Write brief** to `templates/brief-framework.md` structure → render HTML (B/W/Y Premium) → publish KV preview.thefirstonly.com → verify HTTP 200 → báo link.
6. **Humanize** claim text before sending for approval (bắt buộc): no em dash, no emoji in heads, no AI vocab, varied sentence length, đúng claim pháp lý.

## Pitfalls
- **Bỏ qua đối chiếu nền tảng** — viết brief mà không kiểm chứng luận điểm "kiềm" cho chính condition đó = tái phạm pseudoscience. Luôn chạy `platform-rules.md`.
- **Số liệu TAM vào tài liệu NPP** — cấm; là số ước tính gây kỳ vọng ảo.
- **Bịa PMID/nghiên cứu** — bài research phải verify thật (`pubmed-evidence-research`), KHÔNG bịa số liệu/tên/quote.
- **Không kể tên nghiên cứu mà paraphrase mơ hồ** ("các chuyên gia cho rằng") — vi phạm grounded-citations + humanizer.
- **Duy nhất 1 SKU không có lớp cảm nhận nhanh** — churn MLM tháng 2 (bài học MS-01: phải 2 SKU CORE+RELIEF hoặc 2 tầng).
- **pH 12–14 bỏ qua** với công thức chứa hoạt chất nhạy kiềm — điểm chặn G1/G2 phải giải trước mọi thứ.
- **Quên publish link** — Plan/TL/báo cáo bắt buộc publish preview.thefirstonly.com.

## Verification checklist
- [ ] 1 trang confirm được duyệt trước khi viết full brief
- [ ] Đối chiếu nền tảng chạy (phần 10 + platform-rules.md) — ghi rõ vai trò kiềm thật vs claim
- [ ] Mọi PMID/nghiên cứu verified; claim có cite (grounded-citations verify pass)
- [ ] Hero door + 3 concept + MoSCoW + công thức đủ liều có trong brief
- [ ] Bảng pháp lý ngôn ngữ được/không được cho condition này
- [ ] RFI ≥20 câu + G1–G7 + 90 ngày present
- [ ] HTML B/W/Y xuất ra, publish KV, HTTP 200 verify
- [ ] Claim text đã humanize

## Support files
- `references/framework-structure.md` — full 20+ section template with per-section content spec + example from the 5 briefs.
- `references/platform-rules.md` — Kiềm Thảo Dược đối chiếu nền tảng (bắt buộc đọc): bằng chứng, ngoại lệ, pH, Kali, định vị.
- `references/cross-cutting-rules.md` — R&D + MLM + pháp lý principles xuyên suốt.
- `templates/brief-framework.md` — markdown skeleton để điền.
