---
name: vietnam-corporate-research
description: "Research Vietnamese legal entities: companies (ownership, shareholders) and public institutions (báo chí, đơn vị sự nghiệp — legal identity for contracts/MOUs)."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, vietnam, finance, ownership, shareholders, stock, m-and-a, room-ngoai]
    related_skills: [web-research, grounded-citations, research-reporting, vietnam-legal-advisory]
---

# Vietnam Corporate Research

Use when researching Vietnamese companies, their ownership structures, shareholders, foreign ownership (room ngoại), restructuring and M&A — e.g. Vingroup, Vinhomes, VinFast, Vincom Retail, Masan. Primary sources: vietstock (finance.vietstock.vn), cafef, vietnamnet, kenh14, vnexpress, theleader.vn, Wikipedia VI.

## Search strategy (validated 8/2026 on Vingroup research)

1. **Bing News via curl/python — PRIMARY for Vietnamese queries.**
   `https://www.bing.com/news/search?q=<urlencoded>&setlang=vi&count=14` with a browser UA. Parse `<a class="title">` for title+URL and the following `<div class="snippet">` for the summary. Returns current VN finance news reliably. Use `scripts/bing_news_search.py`.
   - PITFALL: **Bing *web* search (`bing.com/search`) is useless for Vietnamese**: it tokenizes diacritics badly ("Phạm Nhật Vượng" → results about the surname "Phạm"), and the browser variant can serve a consent/blank page. Always use the News endpoint.
   - English queries on Bing News often return zero/few hits — prefer Vietnamese queries + `setlang=vi`; use English only as a supplement for Reuters-derived deals.
2. **DuckDuckGo HTML via curl GET — works (validated 9/2026).** `curl -s -L "https://html.duckduckgo.com/html/?q=<urlencoded>" -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"` returns results reliably for exact-phrase Vietnamese/English queries; parse by grepping `<a rel="nofollow" class="result__a"` (title) and `class="result__snippet"` (summary), then strip tags with sed. Use GET with a desktop browser UA. PITFALL: `lite.duckduckgo.com/lite/` returns empty via curl; earlier failures were curl POST — avoid POST.
3. **Direct site access:**
   - vietstock finance: curl works for static overview pages, but **shareholder tables (cổ đông lớn) and the "% NN sở hữu" figure (actual foreign-ownership %) are JS-rendered → use browser_navigate** and read the snapshot. Overview URL pattern: `finance.vietstock.vn/CODE-ctcp-<name>.htm` (e.g. `/VHM-ctcp-vinhomes.htm`); the same page shows vốn hóa, P/E, dividend/event history.
   - cafef: `s.cafef.vn` shareholder-page URL patterns often 404; instead find cafef article URLs via Bing News.
   - Wikipedia VI: excellent starting point for ownership structure (e.g. the Vingroup article lists major shareholders incl. the parent holding company). CAVEAT: the numbers are frequently historical/undated — cross-check with dated news before citing.
4. **Article body extraction** — VN news sites (vietnamnet, kenh14, 24h) are nav-heavy: find the `<h1>`, then take subsequent `<p>` tags. Whole-page tag-stripping returns nav/footer junk. Use `scripts/extract_vn_article.py`.

## Public institutions & báo chí — legal identity for MOUs/contracts (validated 9/2026)

Use when the subject is a Tạp chí/Báo/đơn vị sự nghiệp công lập (public service unit) and the deliverable is the exact legal name for a contract/MOU. Different rules than companies:

1. **Exact registered name comes from 3 documents, in order of authority:**
   - **Quyết định thành lập** by the parent ministry (e.g. `QĐ-BNNMT`) — names the unit and states it is "đơn vị sự nghiệp công lập trực thuộc Bộ …";
   - **Giấy phép hoạt động báo chí** issued by Bộ VH-TT&DL (number format `GP-BVHTTDL`, e.g. 23/GP-BVHTTDL) — covers Tạp chí in + Tạp chí điện tử, valid 10 years; also Giấy phép trang TTĐT tổng hợp (`GP-CBC-BVHTTDL`);
   - **VJOL registry** (vjol.info.vn) for scientific journals — lists tên, cơ quan chủ quản, ISSN, địa chỉ tòa soạn, giấy phép.
   The unit's own "Thông tin tòa soạn"/"Giới thiệu" page (often `/trang/thong-tin-toa-soan`) restates all of the above verbatim — fastest single check. Footer of the official site also carries Tổng biên tập, address, phone — scrape it.
2. **Mã số thuế of public units is often NOT public.** Query masothue.com (`https://masothue.com/search/?q=<name>`); it returns a "Không tìm thấy dữ liệu 404" page when the unit isn't in their DB — that means not indexed, not that the entity doesn't exist. Do NOT invent a number; report "không công khai" and tell the user to ask the unit directly (needed for hóa đơn/contracts).
3. **Signing authority = Tổng biên tập (editor-in-chief)** for journals — verify current name via ministry news article (e.g. mae.gov.vn) + official site footer, not just one source.
4. **Name-conflation trap: Tạp chí ≠ Báo.** After the 2025 ministry merger, Báo Nông nghiệp Việt Nam became "Báo Nông nghiệp và Môi trường" (nongnghiep.vn) while a SEPARATE entity "Tạp chí Nông nghiệp và Môi trường" (nnmt.net.vn) was formed by merging two journals. Always confirm which entity the MOU is with; cite address (e.g. Số 10 Nguyễn Công Hoan, Hà Nội) to disambiguate.
5. **Verify domain claims from task context.** User context may cite a domain that doesn't exist (e.g. "masic.vn" → HTTP 000, dead; the real ministry portal is mae.gov.vn). Probe with `curl -sL -o /dev/null -w "%{http_code}"` before trusting it.

Worked example + verified fact base: `references/bao-chi-public-institutions.md`.

## Tra cứu pháp nhân công ty / MST (legal entity lookup) — validated 9/2026

For "tên công ty đầy đủ, MST, địa chỉ, người đại diện pháp luật, ngành nghề đăng ký" lookups of VN companies (xác nhận pháp nhân của thương hiệu trước khi soạn MOU/hợp đồng):

1. **DDG exact-phrase via camsearch.py (Camofox) trước tiên** — `'"<tên công ty>" TNHH'` (có dấu tiếng Việt OK) trả các trang mirror đăng ký kinh doanh ngay; có MST sẵn thì search `"<mst>"`. Kết quả đầu tiên thường là masothue + thuvienphapluat + vài mirror.
2. **masothue.com** — nguồn tốt nhất qua Camofox page_text: MST, "Địa chỉ Thuế", "Tên quốc tế"/"Tên viết tắt", "Người đại diện", "Quản lý bởi" (chi cục thuế), "Ngành nghề chính", ngày hoạt động, tình trạng. Đôi khi 503 lần đầu → DELETE session (`DELETE /sessions/<user>`) + retry là OK.
3. **doanhnghiep.biz** — danh mục "Ngành nghề KD" đầy đủ (mã VSIC + tên), ngày cấp, ĐT/email đăng ký.
4. **topcv.vn company page** — trang công ty liệt kê website chính thức → dùng để verify link thương hiệu ↔ pháp nhân (vd Manna Đất Vàng ↔ vuakiem.com).
5. **tratencongty.com** — mirror dự phòng; cảnh giác dữ liệu địa chỉ/phường cũ (lệch 1 nguồn vs 3-4 nguồn mới hơn).
6. **Bị chặn/kém tin cậy (9/2026):** thuvienphapluat.vn (Cloudflare "you have been blocked"), fliphtml5 (Cloudflare verification), masic.vn (HTTP 000 — không verify trực tiếp được; masothue là bản mirror dữ liệu Cục Thuế).
7. **Cross-verify ≥3 mirror + website chính thức** — footer "© <year> Công ty..." và trang giới thiệu thường xác nhận pháp nhân + hệ sinh thái thương hiệu (vd vuakiem.com/gioi-thieu liệt kê các pháp nhân trong hệ sinh thái). Địa chỉ lệch giữa các mirror (phường cũ/mới sau sáp nhập) → báo cả hai, ghi nguồn đa số, không tự chọn.
8. MST prefix = mã tỉnh (01 = Hà Nội); "Đang hoạt động" + ngày cập nhật gần = còn hiệu lực.
9. **Trước khi ký MOU:** đối chiếu Giấy chứng nhận ĐKKD gốc — mirror có thể lệch; đặc biệt xác nhận loại hình (TNHH vs Cổ phần — founder thường đoán sai kiểu pháp nhân của chính công ty mình; người đại diện pháp luật đăng ký có thể KHÁC người sáng lập/nhà khoa học nổi tiếng của thương hiệu).
10. **Tên chung chung (vd "Trung tâm Hỗ trợ Phát triển KH&CN") có thể có NHIỀU pháp nhân cùng tên** (case 9/2026: 2 MST khác nhau cùng tên này ở Hà Nội). Liệt kê HẾT ứng viên (tên, MST, địa chỉ, người đại diện, nguồn), KHÔNG tự chọn 1 cái — yêu cầu người dùng hỏi đối tác lấy MST/giấy phép để chốt tên ghi vào văn bản.
11. **Đơn vị sự nghiệp công lập / khối hội (VUSTA, Liên hiệp Hội...):** dấu hiệu trên infodoanhnghiep.com = "Năm tài chính: 2000" + "Cấp Chương Loại Khoản: 755-xxx" (mã ngân sách); masothue ghi "Loại hình: Các tổ chức kinh tế khác". Brand ≠ tên pháp nhân trên giấy tờ thuế (vd "STTDC" = "Trung tâm Hỗ trợ Phát triển KH&CN"); nối brand→MST bằng DDG `"<brand>" "<tên đầy đủ>" địa chỉ` (hạng kết quả thường trỏ đúng MST). Tin tuyển dụng trên ybox.vn: body bài KHÔNG render qua page_text (chỉ nav + feed), nhưng SLUG URL chứa tên trực thuộc đầy đủ (vd `...-truc-thuoc-lien-hiep-cac-hoi-khoa-hoc-ky-thuat-viet-nam-...`) → dùng title/slug làm bằng chứng.
12. **Loại trừ giả thuyết "trực thuộc Sở KH&CN tỉnh":** search DDG chính xác cụm tên + từng tỉnh nghi ngờ — các Sở KH&CN tỉnh thường KHÔNG có trung tâm tên kiểu "Hỗ trợ Phát triển KH&CN" (tên thật của họ: "Trung tâm Ứng dụng tiến bộ KH&CN", "Trung tâm Thông tin và Thống kê KH&CN", "Trung tâm Phát triển và Giao dịch Công nghệ"...).

Worked example + verified fact base: `references/manna-dat-vang-vua-kiem-legal.md`; trung tâm/đơn vị sự nghiệp: `references/trung-tam-ho-tro-phat-trien-khcn-2026.md`.

## Output discipline (parent-project convention for research JSON)
- Separate DATA from ANALYSIS in every deliverable: facts carry `fact` + `source` (URL) + `date`; analysis is labeled explicitly (e.g. `(PHÂN TÍCH)` in Vietnamese outputs) and kept in its own field.
- Verify each number from ≥2 independent sources when possible; every % must be time-stamped (ownership changes fast — e.g. PNV's VIC stake went 13,86% → 11,6% within weeks in 6/2025).
- Mark gaps explicitly ("không tìm thấy nguồn xác nhận") instead of inventing. Example: "Kuwait Investment Authority invested in Vingroup/Vinhomes" could NOT be verified (8/2026) → recorded as a gap, no numbers invented.
- Watch for name-conflation in VN press: e.g. SK Group bought 16,3% of **VinCommerce** in 2021 (after it moved to Masan/The CrownX) — many Vietnamese articles mislabel this as "Vincom Retail" (VRE). Verify which entity a deal actually hit.
- Vietnamese numeric convention: comma = decimal separator (23,5% = 23.5%), dot = thousands.

## References
- `references/vingroup-ownership-facts-2026.md` — verified fact base (Vingroup/Vinhomes/VRE/VinFast/Vinpearl ownership %, room ngoại, SK/GIC/KKR deals, restructuring timeline) with URLs & dates; reuse for the vingroup-structure project or follow-up questions instead of re-searching.
- `references/bao-chi-public-institutions.md` — verified legal-identity fact base for public institutions/báo chí (worked example: Tạp chí Nông nghiệp và Môi trường — QĐ 212/QĐ-BNNMT, GP 23/GP-BVHTTDL, TBT Đào Xuân Hưng, nguồn URLs, MST-không-công-khai pattern, Tạp chí≠Báo conflation table).
- `references/manna-dat-vang-vua-kiem-legal.md` — verified legal-entity fact base (worked example: Công ty CP Manna Đất Vàng / thương hiệu Vua Kiềm — MST 0109767318, trụ sở 1111 Ngô Gia Tự Long Biên, ĐDPL Nguyễn Long Quân, ngành C1080, hệ sinh thái Thành Phương/Saphia/Manna, nguồn URLs).
- `references/trung-tam-ho-tro-phat-trien-khcn-2026.md` — verified fact base (2 ứng viên MST cùng tên "Trung tâm Hỗ trợ Phát triển KH&CN" tại Hà Nội + liên kết brand STTDC ↔ VUSTA qua ybox/Facebook, nguồn URLs & ngày; dùng lại cho MOU Vua Kiềm hoặc follow-up thay vì search lại).

## Scripts
- `scripts/bing_news_search.py` — query → JSON results (title/url/snippet) from Bing News (VN-first).
- `scripts/extract_vn_article.py` — h1 + `<p>` body extraction from saved VN news HTML files.
