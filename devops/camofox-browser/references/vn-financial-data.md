# Research dữ liệu tài chính & cấu trúc sở hữu doanh nghiệp Việt Nam (cafef.vn, vietstock)

Verified 17/08/2026 trong task research cấu trúc công ty con/liên kết của Vingroup (VIC). Dùng Camofox browser + camsearch.py (xem SKILL.md). Công dụng: tra "ai sở hữu bao nhiêu % công ty nào", cơ cấu công ty con/liên kết theo BCTC hợp nhất, phát hiện thoái vốn.

## cafef.vn — hồ sơ công ty (nguồn tốt nhất cho "Công ty con & liên kết")

URL: `https://s.cafef.vn/hose/<TICKER>-<slug>.chn` (VD `VIC-ctcp-tap-doan-vingroup.chn`). Redirect về `https://cafef.vn/du-lieu/hose/<ticker>-<slug>.chn` (đôi khi thành `/du-lieu/du-lieu/...` — kỳ lạ nhưng render OK; navigate thẳng URL canonical cho sạch).
curl tải được HTML (~350KB) nhưng bảng dữ liệu nằm trong JS (`$.ajax` → `result.Data.Subsidiaries/AssociatedCompanies/OtherCompanies`) → PHẢI dùng browser + browser_console.

### Trích bảng "Công ty con & liên kết" (browser_console)
1. `browser_navigate` trang hồ sơ công ty.
2. Click tab: `document.querySelectorAll('.owner-tab')[1].click()` (index 0 = "Cơ cấu sở hữu", 1 = "Công ty con & liên kết").
3. Chờ ~3s (setTimeout trong Promise), trích:
```js
(() => new Promise(res => setTimeout(() => {
  const rows = [...document.querySelectorAll('#owner_content-subsidiaries tr')]
    .map(tr => [...tr.querySelectorAll('td')].map(td => td.innerText.trim()));
  res(JSON.stringify({rows, count: rows.length}));
}, 3000)))()
```
- Header: Loại hình | Đơn vị | Vốn điều lệ (tỷ đồng) | Vốn góp (tỷ đồng) | Tỷ lệ sở hữu (%) | Ghi chú.
- Có nhóm "Công ty con (N)" và "Công ty liên kết (N)" — phân biệt thẳng.
- Dữ liệu lớn (90+ dòng) → trả JSON rồi lưu file ngay.

### Trích "Danh sách cổ đông" (xác định ai nắm bao nhiêu % một công ty)
URL: `https://s.cafef.vn/du-lieu/hose/<ticker>-ban-lanh-dao-so-huu.chn` (VD `tcb-ban-lanh-dao-so-huu.chn`).
- Page có tab "Ban lãnh đạo | Danh sách cổ đông | Đang sở hữu | GD CĐ nội bộ & CĐ lớn". Click h2 có text "Danh sách cổ đông" (không phải `.owner-tab` — tab này dùng class khác), chờ ~2.5s.
- Đọc `document.body.innerText` quanh keyword công ty muốn tìm.
- Cột: Cổ đông | Số lượng cổ phiếu | Tỷ lệ (%) | Tính đến ngày.
- **Cách phát hiện thoái vốn:** nếu công ty mẹ KHÔNG còn trong list → đã thoái. VD 17/08/2026: VIC không còn trong cổ đông TCB tại 31/12/2025 (Masan Group 14,8% là lớn nhất; nhóm Hồ Hùng Anh ~18,8%) → kết luận Vingroup đã thoái toàn bộ Techcombank.

## ⚠️ Pitfall: dữ liệu cafef có thể STALE (trộn nhiều kỳ BCTC)

Bảng "Công ty con & liên kết" KHÔNG phải lúc nào cũng là kỳ mới nhất — có thể lệch 1-2 kỳ sau các sự kiện tăng vốn/thoái vốn, và trộn tỷ lệ của các kỳ khác nhau. VD 17/08/2026 trên bảng VIC: vẫn ghi Vinpearl 99,97% (thực tế ĐKCCĐ 3/2024 đã là 85,51%), vẫn còn Vincom Retail (đã thoái 11/2024) — nhưng lại có VinFast 51,15% (chỉ tồn tại sau IPO 8/2023). → **LUÔN cross-verify từng tỷ lệ quan trọng với tin bài** (cafef.vn, vietstock.vn, znews.vn, vnexpress.net, vietnambiz.vn, dantri.vn) và ghi rõ ngày + URL cho từng số. Không bao giờ chép nguyên bảng cafef vào output mà không ghi chú kỳ dữ liệu.

## Đọc bài báo VN (page_text)

- page_text trả về nhiều nav text; tìm đoạn bài bằng cách locate keyword tiêu đề, đoạn bài kết thúc trước "Copy link" / "Xem tất cả".
- File lưu có thể bị detect binary (UTF-16/encoding lỗi) → đọc lại bằng python: `raw.decode('utf-8', errors='replace')`; nếu thấy `\x00` trong 500 ký tự đầu thì `raw.decode('utf-16', errors='replace')`.
- Ngày đăng: cafef ID cuối URL có format `188<YYMMDD>...` (VD `188260627...` = 27/06/2026), hoặc dòng "Theo ... | dd-mm-yyyy" trong bài.

## Nguồn BCTC chính thức (đều JS-rendered qua curl)

- Vingroup: `vingroup.net/quan-he-co-dong/bao-cao-tai-chinh` + `/2024` (curl chỉ ra shell ~5.7KB → cần browser hoặc tìm PDF trực tiếp).
- vietstock: `finance.vietstock.vn/<TICKER>/tai-tai-lieu.htm` (bài viết vietstock.vn thì curl OK).
- techcombank.com: `/nha-dau-tu/bao-cao-thuong-nien/<năm>/co-cau-co-dong` (JS-rendered — curl tải 214KB nhưng không có text Vingroup; dùng cafef thay thế).

## Worked example: cấu trúc sở hữu Vingroup (VIC) — verified 17/08/2026

Áp dụng recipe trên, kết quả đã verify (ngày + nguồn):

| Công ty | Mã | VIC nắm | Ngày | Nguồn |
|---|---|---|---|---|
| Vinhomes | VHM | 73,51% (bảng cafef mới nhất); 69,3% (10/2024) → dự kiến 75,7% sau buyback → 71,70% (sau chuyển 15,2tr cp 25/6/2025) | 2024-2026 | cafef table; vietcap 11/10/2024; cafef 27/06/2026 |
| Vincom Retail | VRE | **Đã thoái**: bán 41,5% qua SDI/Sado (39.100 tỷ, hoàn tất Q3/2024), còn 18,8% trực tiếp — không còn công ty con | 07/11/2024 | cafef; dantri 24/01/2025 |
| Vinpearl | VPL | 85,51% (sau tăng vốn 2/2024, vốn điều lệ 17.232 tỷ); ĐKCCĐ 15/3/2024; HOSE chấp thuận niêm yết ~1,79 tỷ cp | 2024-2026 | vietnam.vn; vietnambiz 10/12/2024; thitruongtaichinhtiente |
| VinFast | VFS | VIC 1,19 tỷ cp VFS (~50,8%); nhóm PNV (VIC+VIG 769,6tr cp+Asian Star 334tr cp) = 97,8% tại 18/3/2026; 61,06% tại VinFast VN sau chia tách 11/2024 | 14/11/2024 + 18/03/2026 | znews 01/04/2026; dantri 14/11/2024 |
| Vinmec | - | 100% (vốn điều lệ 1.200 tỷ); mô hình phi lợi nhuận từ 27/9/2016 | 2026 | cafef table; nhandan |
| VinCommerce/VinMart | - | Đã bán/hợp nhất vào Masan cuối 2019 (hoán đổi toàn bộ cổ phần; Masan nắm chi phối; nay là WinMart/WinMart+) | 2019 | vietnambiz 28/06/2024 |
| Techcombank | TCB | **Đã thoái toàn bộ** — không còn trong DS cổ đông lớn 31/12/2025 (Masan 14,8% là lớn nhất) | 31/12/2025 | cafef TCB danh sách cổ đông; phunuvietnam 16/11/2025 |
| VinAI → Movian AI | - | VIC 65% → bán toàn bộ cho Qualcomm 1/4/2025 (tách VinAI cuối 11/2024); phần VinAI gốc còn lại vẫn là công ty con | 02/04/2025 | vnexpress; znews 03/04/2025 |
| VinBrain | - | VIC 49,74% (Q3/2024, ~126 triệu USD) → NVIDIA mua 5/12/2024; sau đổi TNHH vốn 627,7 tỷ | 06/12/2024 | vietstock; znews |
| VinBigData | - | 69,2% (30/9/2024); vốn điều lệ 535 tỷ (3/2024) | 2024 | znews 03/04/2025 |
| VinCSS | - | 80% | 2026 | cafef table |
| VinSmart | - | 62,03% (đã ngừng sản xuất điện thoại 2021) | 2026 | cafef table |

Ghi chú bổ sung từ bảng cafef VIC (90 công ty con + 4 liên kết): Vinmec 100%, Vinschool 100%, VinAcademy (VinUni) 99,37%, Vinpearl Air 79,97%, Vingroup USA/Nhật/Hàn/Ru 80%, CTCP Đầu tư KCN Vinhomes 90%, One Mount Group/OneID/Adayroi 51,22%. Liên kết: Việt Thắng 40%, Giống vật nuôi HN 37,63%, In sách VN 35%, Du lịch Phú Quốc 30%.