# Báo chí / đơn vị sự nghiệp — worked example: Tạp chí Nông nghiệp và Môi trường (9/2026)

Verified fact base for the MOU-drafting task. Reuse instead of re-searching.

## Legal identity (verified 9/2026)
- **Tên đầy đủ:** Tạp chí Nông nghiệp và Môi trường — đơn vị sự nghiệp công lập trực thuộc Bộ Nông nghiệp và Môi trường
- **Thành lập:** Quyết định số 212/QĐ-BNNMT-TCCB, ngày 01/03/2025 của Bộ trưởng Bộ NN&MT — hợp nhất "Tạp chí Nông nghiệp và Phát triển nông thôn" (thành lập 2000) + "Tạp chí Tài nguyên và Môi trường" (thành lập 2002). Nghị định 35/2025/NĐ-CP (cơ cấu Bộ NN&MT).
- **Giấy phép báo chí:** số 23/GP-BVHTTDL, ngày 25/4/2025 (Tạp chí in + điện tử, 8 ấn phẩm, giá trị đến 25/4/2035); thêm 24/GP-CBC-BVHTTDL ngày 9/6/2025 (trang TTĐT tổng hợp)
- **ISSN:** P-ISSN 3093-3382, E-ISSN 3093-3153
- **Trụ sở/tòa soạn:** Số 10 Nguyễn Công Hoan, phường Giảng Võ, Hà Nội
- **Tổng biên tập:** TS. ĐÀO XUÂN HƯNG; Phó TBT: ThS. Kiều Đăng Tuyết, ThS. Vũ Minh Lý
- **Liên hệ:** 024 3771 1072 (điện tử), 024.32321808 / 024.37716634 (khoa học); tapchinnmt@gmail.com, bbtnongnghiep@gmail.com
- **MST:** KHÔNG công khai — masothue.com 404 "Không tìm thấy dữ liệu" cho cả tên mới lẫn 2 pháp nhân cũ; trang chính thức không đăng tải

## Các pháp nhân dễ nhầm (đều trực thuộc Bộ NN&MT, sau hợp nhất 2025)
| Pháp nhân | Website | Ghi chú |
|---|---|---|
| Tạp chí Nông nghiệp và Môi trường | nnmt.net.vn (+ english.nnmt.net.vn, tapchikhoahoc.nnmt.net.vn) | Đối tượng MOU; hợp nhất 2 tạp chí cũ |
| Báo Nông nghiệp và Môi trường | nongnghiep.vn | KHÁC pháp nhân (trước là Báo Nông nghiệp Việt Nam) |
| Bộ Nông nghiệp và Môi trường (cổng) | mae.gov.vn | masic.vn KHÔNG tồn tại (HTTP 000) — đừng tin domain trong task context |

## Nguồn đã xác minh (mở trực tiếp được bằng curl)
- https://www.nnmt.net.vn — footer: TBT, địa chỉ, SĐT
- https://nnmt.net.vn/trang/thong-tin-toa-soan — giới thiệu chính thức: QĐ 212, GP 23/GP-BVHTTDL, 8 ấn phẩm
- https://tapchikhoahoc.nnmt.net.vn/index.php/vjae/about — QĐ 212/QĐ-BNNMT-TCCB, "đơn vị sự nghiệp công lập trực thuộc Bộ"
- https://vjol.info.vn/tcnongnghiepmoitruong-vie/vi/about/ — tên, CQQL, ISSN, địa chỉ, giấy phép (registry chính thức của tạp chí KH)
- https://mae.gov.vn/Pages/chi-tiet-tin-tuc.aspx?ItemID=20651 — Bộ xác nhận TBT Đào Xuân Hưng, "năm 2025 là năm đầu hoạt động sau hợp nhất"
- https://scem.org.vn/vi/tin-tuc-trung-tam/tin-tuc/giay-phep-hoat-dong-tap-chi-nong-nghiep-va-moi-truong-1478.html — chi tiết giấy phép 23/GP-BVHTTDL

## Technique notes từ session này
- DDG HTML search qua **curl GET** + desktop UA hoạt động ổn định; grep `result__a` / `result__snippet`. Bing web search qua curl trả rác (mediaindonesia...), Bing News endpoint không có cho queries này.
- Browser (Camofox) down → toàn bộ flow bằng curl + python strip-tags (`re.sub(r'<[^>]+>',' ',...)` + `html.unescape` + `re.sub(r'\s+',' ',...)`) — đủ cho trang tĩnh VN.
- Trang của đơn vị sự nghiệp thường không công khai MST; tra cứu thuế chính phủ (tracuunnt.gdt.gov.vn) cần captcha — không khả thi tự động.
