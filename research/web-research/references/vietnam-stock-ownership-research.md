# Vietnam stock ownership research (cổ đông lớn / cơ cấu sở hữu)

Techniques + verified knowledge bank for researching ownership/shareholding structure of Vietnamese listed companies (HOSE/HNX). Built from the Vingroup (VIC) shareholders session (17/08/2026).

## Nguồn & cách lấy dữ liệu

| Nguồn | URL pattern | Cách lấy | Ghi chú |
|---|---|---|---|
| Vietstock Finance | `https://finance.vietstock.vn/<MA>/co-dong-lon.htm` | **browser bắt buộc** (JS SPA; curl chỉ trả shell HTML) | Bảng cổ đông lớn (≥5%) theo mốc năm (31/12/2023, 2024, 2025...); mốc cũ bị mask `***` nếu chưa đăng nhập |
| Vietstock Finance | `/<MA>/co-cau-so-huu.htm` | browser | Cơ cấu sở hữu theo nhóm: CĐ >5% trong nước/ngoài, CĐ khác trong nước/NN, CĐ sáng lập, cổ phiếu ưu đãi — nhiều mốc năm, kèm số CP |
| Vietstock Finance | `/<MA>/ho-so-doanh-nghiep.htm` | browser | Tóm tắt cổ đông lớn kèm số CP + ngày cập nhật; khối lượng lưu hành; vốn điều lệ; lịch sử tăng vốn |
| Vietstock Finance | `/lanh-dao-doanh-nghiep/<slug>/<id>.htm?code=<MA>` | browser | Hồ sơ lãnh đạo: chức vụ, bảng "Cá nhân có liên quan" (quan hệ gia đình: vợ/chồng, anh/chị/em — rất hữu ích để xác định nhóm gia đình), giao dịch nội bộ; số CP đang nắm thường bị mask `******` |
| Vietstock Finance | `/<MA>/giao-dich-noi-bo.htm?tab=5` | browser | Tab cổ phiếu quỹ: "Chưa có dữ liệu" = không có giao dịch mua lại |
| Cafef | `cafef.vn/<bài viết>` | curl + regex (HTML tĩnh, không cần browser) | Bài phân tích sở hữu rất giàu số liệu kèm ngày (vd: "Khối tài sản gần 500.000 tỷ của gia đình tỷ phú Phạm Nhật Vượng", "Gần 600 triệu cổ phiếu VIC đã rời tài khoản cá nhân...") |
| DDG HTML | `html.duckduckgo.com/html/?q=...` | curl + UA | Rate-limit 202 sau 2–3 query nhanh → chèn `sleep 5–8` giữa các query; trích kết quả bằng regex `class="result__a"` + `uddg=` (URL thật trong tham số `uddg`) |
| Bing | `bing.com/search?q=...` | browser + browser_console JS | Query tiếng Việt có dấu bị phân tích sai (vd "Phạm Nhật Vượng" → kết quả rác về "pham") → dùng **query tiếng Anh**; kết quả render lazy (title rỗng trong accessibility tree) → trích bằng JS `#b_results li h2 a`; URL kết quả là redirect chứa `u=a1<base64>` → decode base64 để lấy URL thật |

## Quy tắc verify (dự án cấu trúc vốn — KHÔNG bịa số)
- Mọi con số phải kèm URL + ngày. Không tìm được → ghi `chưa xác định` + lý do.
- Kiểm tra chéo %: tỷ lệ = số CP / khối lượng lưu hành (≈ vốn điều lệ / 10.000).
- **Bẫy tăng vốn**: sự kiện thưởng cổ phiếu 1:1 làm NHÂN ĐÔI số CP và giảm 1/2 mọi tỷ lệ %. Luôn phân biệt số liệu trước/sau sự kiện (tra "lịch sử tăng vốn" trong hồ sơ doanh nghiệp).
- Vietstock mask `******` khi chưa đăng nhập → bù bằng số từ báo (cafef, markettimes, vietstock tin) kèm ngày; bài kiểu "top tỷ phú sàn chứng khoán" (vietstock/fili) thường nêu số CP cụ thể.
- Cổ đông tổ chức kiểu "công ty gia đình" (VIG, VMI, Vinspeed...) rất quan trọng: tỷ lệ sở hữu của người lãnh đạo phải tính cả trực tiếp + gián tiếp qua các pháp nhân.

## Knowledge bank: Vingroup (VIC, HOSE) — verified 17/08/2026

**Cổ đông lớn tại 31/12/2025** (https://finance.vietstock.vn/VIC/co-dong-lon.htm):
- CTCP Tập đoàn Đầu tư Việt Nam (VIG — công ty đầu tư cá nhân của Phạm Nhật Vượng): 2.520.265.316 cp = **32,59%**
- CTCP Đầu tư & PT Đường sắt Cao tốc Vinspeed: 834.212.369 cp = **10,79%** (đầu 2026: 455,1 triệu cp = 11,7%)
- Phạm Nhật Vượng (trực tiếp): 703.848.781 cp = **9,10%**
- CTCP Quản lý & Đầu tư BĐS VMI (tên cũ Hưng Long): 243.462.578 cp = **6,28%**
- Khối lượng lưu hành: 7.762.186.429 cp; vốn điều lệ 77.621,86 tỷ đồng (07/2026)

**Gia đình** (cafef 12/10/2025, số liệu 10/10/2025; vietstock 19/02/2026):
- Phạm Thu Hương (vợ Vượng, Phó CTHĐQT, sinh ~1969): ~170 triệu cp (~4,4%)
- Phạm Thúy Hằng (em gái bà Hương, Phó CTHĐQT): >228 triệu cp (11/02/2026)
- Phạm Nhật Quân Anh (con trai): 150.000 cp (~0,002%)
- Gia đình + công ty liên quan kiểm soát ~65,9% vốn VIC (2,55 tỷ cp, 10/10/2025)

**Cơ cấu sở hữu theo nhóm** (https://finance.vietstock.vn/VIC/co-cau-so-huu.htm):
- 31/12/2025: CĐ trong nước >5% 52,48%; CĐ khác trong nước 43,77%; CĐ khác NN 3,04%; CĐ sáng lập 0,36%; cổ phiếu ưu đãi 0,36%
- 31/12/2024 & 31/12/2023: CĐ trong nước >5% 56,59%; CĐ NN >5% 5,97% (SK Group); CĐ khác NN: 2,62% (2024) / 11,94% (2023)
- Sở hữu nước ngoài thực tế: 3,21% (17/08/2026)

**SK Group (Hàn Quốc)** (cafef 27/03/2025): 2019 đầu tư ~1 tỷ USD (154,3 triệu cp riêng lẻ + 51,4 triệu cp từ VinCommerce) → ~6,1%; cuối 2023: 6,1%; T1–2/2025 bán 50,8 triệu cp → 4,72% (hết vai trò cổ đông lớn); báo cáo thường niên SK 2024 ghi 0 — thoái toàn bộ cuối 2024.

**Biến động quan trọng**:
- 12/2025: thưởng cổ phiếu 1:1 (vốn điều lệ 38.804,76 → 77.334,91 tỷ) — mọi số CP cũ ×2, tỷ lệ % không đổi.
- 2022–2025: Vượng chuyển ~600 triệu cp cá nhân góp vốn: GSM (nắm 1,3% VIC), VMI/Hưng Long (6,28%), VinEnergo (~165,6 triệu cp), Vinspeed — lý do sở hữu trực tiếp giảm dần.

## Pitfalls
- Windows: python không đọc được `/tmp` của git-bash → lưu file tải về vào đường dẫn Windows rõ ràng (vd `D:/.../tmp/`).
- PDF broker: nếu thư viện PDF (pypdf/PyPDF2) lỗi trong venv, fallback trích text bằng regex `stream...endstream` + `zlib.decompress` trên file PDF thô.
- Các endpoint `/data/...` của Vietstock trả shell HTML chứ không phải JSON — đừng mất thời gian gọi API bằng curl.
