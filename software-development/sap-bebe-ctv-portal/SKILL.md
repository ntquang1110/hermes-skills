---
name: sap-bebe-ctv-portal
description: "Dùng khi làm dự án SAP Bebe CTV — Affiliate Portal."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [sap-bebe, affiliate, ctv, supabase, design, volden, project-ops]
---

# SAP Bebe CTV System — Project Spec (đã chốt 08/2026)

Hệ thống Cộng tác viên SAP Bebe. CTV = mẹ bỉm sữa bán qua TikTok/Shopee/self-order. Trạng thái: Affiliate Portal đang design (6 vòng cập nhật), backend chưa build. State file: `D:/Hermes Proj/.hermes-state/sap-bebe-ctv.md`.

## Trigger
- Mọi task dự án SAP Bebe CTV (design UI, spec backend, build, review)

## 1. VÌ SAO TỒN TẠI
- Sàn (TikTok Shop/Shopee) chỉ trả 8–10% hoa hồng đơn, chạy tầng cơ bản
- Phần còn lại của chính sách (thưởng target, cây đội ngũ ai-mời-ai, thưởng hỗ trợ thành viên mới, phụ cấp quản lý) sàn KHÔNG hỗ trợ → công ty tự xây
- **Giá trị chiến lược = dữ liệu cây đội ngũ nội bộ (ai mời ai) — nền của mọi tầng thưởng**

## 2. KIẾN TRÚC: 2 CỔNG 1 LÕI
- **ADMIN PORTAL** (công ty, chưa làm): duyệt CTV · đối soát · chi trả · cấu hình rule
- **LÕI CHUNG** (backend Supabase, chưa làm, tách file riêng): Affiliate Registry (cây đội ngũ) · Order Sync · Commission Engine · Zalo OA notification
- **AFFILIATE PORTAL** (CTV, ĐANG LÀM): Thu nhập · Sản phẩm & Link · Đơn hàng · Thi đua · Nhóm · Học viện
- Trình tự: UI Affiliate trước (mock data, tách lớp) → chốt giao diện → backend riêng → Admin Portal. Lý do: CTV đông nhất, UI chốt xong thì hợp đồng dữ liệu ổn định → build backend 1 lần.

## 3. LOGIC NGHIỆP VỤ CỐT LÕI

### 3.1 Ba vị trí và thu nhập
| Vị trí | Điều kiện | Thu nhập |
|---|---|---|
| Cộng tác viên | Đăng ký, gắn link + đăng bài đều | 10% hoa hồng/đơn (sàn ~8–10%) · +2% khi đạt mục tiêu cá nhân 30tr/tháng · 20% khi tự lên đơn |
| Trưởng nhóm KD (ký HĐ) | Mời 3–5 người, bán đều | +4% doanh số tháng đầu mỗi thành viên mới · +2% khi nhóm đạt 150tr/tháng |
| Trưởng phòng KD (ký HĐ) | Phát triển nhiều Trưởng nhóm | 10% thu nhập các Trưởng nhóm trực tiếp · +1% thưởng năm trên doanh số phòng |

### 3.2 Hai loại link — tách tuyệt đối
- **Link bán hàng** = link sản phẩm chính thức TikTok/Shopee. Sàn tự tracking + tự trả hoa hồng. Portal chỉ là "kệ hàng". KHÔNG shortlink riêng cho bán hàng.
- **Link mời thành viên** = link nội bộ duy nhất/CTV kèm mã giới thiệu. Ai đăng ký qua link → vào cây đội ngũ dưới người mời. Cơ chế duy nhất hình thành nhóm, dữ liệu độc quyền của công ty.

### 3.3 Ba nguồn đơn, một doanh số ghi nhận
| Nguồn | Hoa hồng | Ai trả |
|---|---|---|
| TikTok Shop | ~8–10% | Sàn trả trực tiếp |
| Shopee | ~8–10% | Sàn trả trực tiếp |
| 🛒 Tự lên đơn (nhập hàng/giao khách) | 20% (chiết khấu công ty) | SAP Bebe trả kỳ hàng tháng |

**Quy tắc hợp nhất (QUAN TRỌNG NHẤT):** doanh số mọi nguồn cộng vào "doanh số ghi nhận" — dùng tính mục tiêu 30tr, nhóm 150tr, xếp hạng thi đua. Chỉ dòng tiền hoa hồng tách theo nguồn chi trả.

### 3.4 Cấu trúc thu nhập hiển thị — 2 khối
- **Khối A — Sàn chi trả:** hoa hồng đơn TikTok/Shopee (chỉ hiển thị ghi nhận, sàn thanh toán)
- **Khối B — SAP Bebe chi trả:** hoa hồng tự lên đơn 20% + mọi tầng thưởng (+2%, +4%, +2% nhóm, phụ cấp quản lý, thưởng năm). Thuế TNCN 10% khấu trừ CHỈ trên khối B.

### 3.5 Vòng đời hoa hồng
Tạm tính (đang chạy) → Chốt sổ (sau khi đơn quá hạn hoàn trả) → Thanh toán (ngày cố định hàng tháng). Đơn hoàn/hủy: hoa hồng gạch ngang, loại khỏi tổng — áp đồng nhất đơn sàn + đơn tự lên.

### 3.6 Từ ngữ — tránh nhận diện đa cấp (CẤM toàn app)
- CẤM: cấp/thăng cấp, tuyến trên/dưới, F1/F2, hệ thống/mạng lưới/cây/tầng, mở khóa cấp, tuyển người
- THAY: vị trí/vai trò, lộ trình phát triển, đội ngũ/nhóm, thành viên nhóm, mời cộng tác, thưởng hỗ trợ thành viên mới, phụ cấp quản lý
- Chân trang Nhóm & Lộ trình dòng cố định: "Thu nhập đến từ doanh số bán hàng thực tế. Tham gia hoàn toàn miễn phí."
- ⚠️ Đổi chữ giảm rủi ro nhận diện; bản chất pháp lý vẫn cần luật sư rà +4% và phụ cấp quản lý theo Nghị định 40/2018

## 4. BẢN ĐỒ MÀN HÌNH (design hiện tại)
Bottom nav 5 tab: Tổng quan · Sản phẩm & Link · Thi đua · Nhóm · Cá nhân + menu ☰ đầy đủ mọi khu (≤2 chạm tới mọi nơi).

| Màn | Nội dung chính |
|---|---|
| Tổng quan | Thu nhập tạm tính + breakdown, tiến độ mục tiêu 30tr, tiến độ thăng tiến, đơn gần nhất, xếp hạng mini, banner Chương trình đặc biệt |
| Thu nhập của tôi | 2 tab: Kỳ hiện tại (2 khối A/B, dòng thời gian tiền về, biểu đồ 6 tháng, gợi ý tăng thu nhập, học từ Top CTV) · Lịch sử chi trả |
| Sản phẩm & Link | FOMO: dải thống kê + feed + badge + "Cơ hội tuần này" đếm ngược; thẻ sản phẩm hoa hồng bằng TIỀN; chi tiết = Bộ công cụ review 8 khối |
| Đơn hàng | Thanh tổng kết 3 nguồn, tab lọc nguồn, mỗi đơn ghi ai trả hoa hồng, "＋ Lên đơn mới" (3 bước), theo dõi vận đơn |
| Thi đua | Xếp hạng theo từng vị trí, chương trình đang chạy, huy hiệu |
| Nhóm | Link mời + mã, tiến độ thăng tiến, danh sách thành viên chấm sức khỏe 🟢🟡🔴🔵, hồ sơ kinh doanh thành viên (coaching) |
| Học viện | Hiểu sản phẩm & kỹ năng bán · Lộ trình 3 chặng game hóa, khóa quản lý mở theo vị trí 🔒 |
| Chương trình đặc biệt | Chiến dịch (vd "Tuần lễ ăn dặm"), chi tiết: thể lệ, người tham gia, tiến độ chung + của tôi |
| Cá nhân | Hồ sơ, ngân hàng, hợp đồng & vị trí, Zalo OA toggle 4 nhóm, hỗ trợ |

### 4.1 Bộ công cụ review 8 khối (trang chi tiết sản phẩm)
6 rào cản review: hiểu → có hàng → nói gì → quay gì → tư liệu → trả lời bình luận. Thêm: chứng nhận an toàn (vũ khí chốt đơn #1 ngành mẹ & bé), 3 con đường có hàng (mua 20% / nhận mẫu / dùng tư liệu), khối ✅/❌ tuân thủ quảng cáo.

### 4.2 Lịch sử quyết định (6 vòng)
- Brief gốc: mobile-first, brief theo 6 nhu cầu người dùng (không theo spec màn hình) → Claude Design sáng tạo
- #01: tách 2 loại link; thêm menu/Thi đua/Cá nhân/Học viện + lộ trình (sàn tự track bán hàng — giá trị ở cây đội ngũ; lộ trình game hóa, học quản lý = phần thưởng thăng tiến)
- #02: FOMO; hoa hồng quy ra TIỀN (89.000đ/đơn mạnh hơn 10%); thông báo qua Zalo OA (CTV không mở portal hàng ngày)
- #03: Thu nhập bóc tách từng dòng; dòng thưởng = 0 vẫn hiện kèm cách mở khóa; gợi ý quy ra tiền + nút; hồ sơ kinh doanh thành viên với badge sức khỏe (gọi ai trước trong 5 giây); riêng tư: thấy doanh số, KHÔNG thấy thu nhập & chi tiết đơn
- #04: Thi đua theo vị trí; tách 2 khối A/B; màn Lên đơn 20%; phân loại 3 nguồn; thưởng chưa đủ điều kiện hiện số mờ; Chương trình đặc biệt; gộp Thu nhập; thay từ ngữ đa cấp
- #05: chi tiết sản phẩm → Bộ công cụ review 8 khối
- #06: gộp Lên đơn vào Đơn hàng; chọn sản phẩm có tìm kiếm + tab "Hay lên đơn"; địa chỉ chuẩn 2 cấp (sau sáp nhập 7/2025, bỏ quận/huyện — kho bắn đơn tự động sang vận chuyển); sổ khách theo SĐT; thanh toán QR/COD; theo dõi vận đơn

### 4.3 Nguyên tắc thiết kế xuyên suốt
1. Mobile-first 390px; kem–teal–cam đất, "ấm áp mẹ & bé", mỗi màn 1 CTA cam
2. Mọi con số động lực quy ra tiền mặt, không dùng %
3. FOMO phải THẬT khi production (số liệu thật) — CẤM bơm số ảo, phát hiện 1 lần sụp niềm tin
4. Thưởng chưa đủ điều kiện: số ước tính MỜ + điều kiện + nút hành động — không ẩn, không 0đ khô
5. Mọi gợi ý = tiền cụ thể + nút dẫn đúng nơi làm
6. Minh bạch tuyệt đối đơn hàng + nguồn chi trả — "mọi đơn từ mọi kênh đều được ghi nhận"
7. Công cụ Trưởng nhóm = kèm cặp, KHÔNG giám sát — ranh giới riêng tư khóa cứng
8. Dữ liệu mock tách lớp khỏi giao diện → nối backend không đập UI

## 5. CHƯA LÀM — SỔ GHI NỢ BACKEND & ADMIN PORTAL
- **Attribution đơn sàn → người (KHÓ NHẤT):** ghép doanh số TikTok/Shopee về đúng CTV (CTV khai tài khoản affiliate sàn; TikTok có API theo creator, Shopee yếu hơn — có thể export AMS thủ công giai đoạn đầu)
- **Commission Engine:** chạy cuối kỳ theo rule cấu hình được (chính sách sẽ đổi — KHÔNG hardcode); màn duyệt trước khi chốt
- **Nghiệp vụ đơn tự lên:** kho, vận đơn, COD thu hộ + đối trừ công nợ CTV vào kỳ chi trả, đối soát tồn
- **Thuế TNCN:** khấu trừ 10% khối B (thu nhập vãng lai ≥2tr/lần), chứng từ khấu trừ
- **Zalo OA:** gửi notification theo toggle người dùng
- **Chính sách nhận mẫu:** điều kiện + ngân sách — TP chốt trước khi công bố
- **Gợi ý thông minh:** rule-based trước (đủ đúng, build nhanh); AI thật khi có 3–6 tháng dữ liệu hành vi
- **Pháp lý:** luật sư rà cấu trúc thưởng Nghị định 40/2018 + wording hợp đồng CTV/Trưởng nhóm
- **Admin Portal:** duyệt CTV, cây đội ngũ toàn hệ, cấu hình rule, đối soát, bảng chi trả, chống gian lận (tự mua, tài khoản ảo)

## 6. LỘ TRÌNH
1. ĐANG Ở ĐÂY: hoàn thiện UI Affiliate Portal qua các vòng cập nhật → chốt giao diện
2. Viết spec backend (schema Supabase + hợp đồng dữ liệu khớp UI chốt) — tách riêng theo quyết định TP
3. Nối backend vào UI (lớp mock đã tách sẵn)
4. Admin Portal
5. Vận hành chuyển tiếp: TikTok native + tầng thưởng tính bán thủ công tới khi hệ thống live

## Pitfalls
- **Đọc state trước khi làm:** `D:/Hermes Proj/.hermes-state/sap-bebe-ctv.md`
- Khi thiết kế/bổ sung màn hình: LUÔN kiểm tra 3.6 (từ ngữ cấm) + 4.3 (nguyên tắc) trước khi duyệt
- Mọi con số % trong UI phải quy ra tiền; mọi FOMO phải dữ liệu thật
- Không được phá "tách lớp mock" — UI không được gọi thẳng backend khi chưa có spec
- VTP/247/MISA trong Volden: OUT OF SCOPE, không đụng (anh chốt 09/08/2026)
