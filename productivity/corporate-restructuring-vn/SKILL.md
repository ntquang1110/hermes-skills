---
name: corporate-restructuring-vn
description: "Tái cấu trúc doanh nghiệp gia đình Việt Nam."
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [corporate, restructuring, family-business, vietnam, sme, governance, succession, org-design]
platforms: [linux, macos, windows]
triggers:
  - tái cấu trúc công ty
  - chuyển giao quản trị
  - family business succession
  - tách mẹ khỏi vận hành
  - đưa người mới vào công ty
  - corporate restructuring
  - cơ cấu tổ chức doanh nghiệp
  - startup từ công ty gia đình
---

# Corporate Restructuring VN

Tái cấu trúc doanh nghiệp gia đình Việt Nam. Dùng khi user muốn chuyển giao quản trị từ thế hệ sáng lập (bố/mẹ) sang thế hệ điều hành mới, đưa đối tác/người nhà vào, và xây dựng hệ thống vận hành chuyên nghiệp.

## Framework — 4 Phase

### Phase 1: Analysis (Hiện trạng)

Trước khi đề xuất gì, phải map được:

| Thành phần | Câu hỏi |
|---|---|
| Pháp nhân | Công ty nào đang đứng? Có mấy pháp nhân? |
| Tiền | Bao nhiêu? Ở tài khoản nào? Của pháp nhân nào? |
| Sản phẩm | Sản phẩm chính thuộc về ai? IP, giấy phép, thương hiệu? |
| Nhân sự chủ chốt | Mẹ/bố (Chủ tịch? Giám đốc?), con cái (chức danh gì?), người ngoài |
| Cổ đông | Đã có cổ đông ngoài chưa? Shareholder agreement? |
| Mối quan hệ | Người trong gia đình: ai là con, ai là cháu, xưng hô thế nào |

**Output:** 1 sơ đồ tổ chức hiện tại + bảng tài chính tóm tắt.

### Phase 2: Design (Thiết kế cấu trúc mới)

Thiết kế dựa trên mục tiêu user muốn. Các mẫu phổ biến:

**Mẫu A — Flat co-founder (2 người điều hành)**
```
Chủ tịch HĐQT (thế hệ sáng lập)
├── Người A: Đại diện PL + Kinh doanh + Kỹ thuật
└── Người B: Phó Giám đốc + Sản phẩm + R&D
```
- Cả 2 báo cáo trực tiếp lên Chủ tịch
- Người A ký pháp lý, Người B được ủy quyền ký mảng của mình

**Mẫu B — Giám đốc điều hành duy nhất**
```
Chủ tịch HĐQT
└── Giám đốc (người mới thuê hoặc con)
    ├── Trưởng KD
    ├── Trưởng R&D
    └── Kế toán
```

**Vấn đề phải giải quyết ngay:**
- **Ủy quyền ký:** Người đại diện PL ủy quyền cho người kia ký hợp đồng, ngân hàng
- **Ngưỡng quyết định:** Định nghĩa "việc lớn" = bao nhiêu tiền? Ai quyết được gì?
- **Quy chế phân công 1 trang:** Ai làm gì, không tự ý vào việc của nhau

### Phase 3: Persuasion (Thuyết phục gia đình)

Đây là phần khó nhất. Nguyên tắc:

1. **Không nói "tách mẹ ra"** — nói "nâng mẹ lên vị trí cao hơn"
2. **Cho thấy bằng hành động trước** — tuyển người, có văn phòng, có kế hoạch
3. **Vai trò mới:** Chủ tịch HĐQT / Cố vấn chiến lược — chốt định hướng, không vận hành
4. **Ngưỡng rõ:** Chi tiêu trên X triệu cần mẹ; dưới thì tự quyết
5. **Trấn an:** Họp hàng tuần báo cáo mẹ; tháng đầu hỏi ý kiến nhiều hơn mức cần
6. **Red flag:** Không để người mới (partner) đối đầu trực tiếp với mẹ — user phải làm cầu nối

**Timeline thuyết phục:**
- Tuần 1-2: Im lặng, làm (tuyển người, có VP, chạy thử)
- Cuối tuần 2: Đề xuất với khung "lên Chủ tịch"
- Tháng 1-2: Chứng minh + giữ kết nối

### Phase 4: Execution (Triển khai 8 tuần)

| Tuần | Việc |
|---|---|
| 1 | Họp 3 bên thống nhất cơ cấu mới. Bổ nhiệm chức danh. Điều lệ HĐQT. |
| 2 | Tuyển kế toán. Kiểm kê tiền. Phân bổ ngân sách tạm. Ủy quyền ký. |
| 3-4 | Product roadmap: chọn hero claim cho sản phẩm chính, xác định 2 hướng mới |
| 4-6 | Setup VP riêng + lab (nếu có R&D). Lý do thuyết phục: "có lab riêng để chạy nhanh, không làm phiền mẹ" |
| 6-8 | Vận hành: KD campaign chạy, R&D chạy, họp tuần với mẹ |

### Budget Planning & Tracking

Mỗi lần tái cấu trúc, phải tạo ngay **bảng ngân sách 6 tháng** chi tiết từng tháng. Output mặc định là Google Sheet (có công thức, số liệu tự động cập nhật).

**Cấu trúc sheet khuyến nghị:**

| Sheet | Nội dung |
|---|---|
| Tổng quan | 8 hạng mục chi x 6 tháng + tổng + dự phòng 15% + số dư còn lại |
| Chi tiết Tháng 1-N | Từng món chi nhỏ: số tiền, đơn vị (tháng/1 lần), ghi chú |
| Tham chiếu ngân sách | Từng con số có giải thích tại sao lại là giá trị đó |

**8 hạng mục chi tiêu chuẩn:**
1. Nhân sự (lương + BH)
2. Mặt bằng & VP (thuê, điện nước, VP phẩm)
3. Lab Equipment (1 lần)
4. R&D nguyên liệu & test
5. Sản xuất (nguyên liệu, bao bì, nhân công)
6. Marketing & bán hàng
7. Pháp lý & giấy phép
8. Chi phí khác (đi lại, đối tác, phát sinh)

**Công thức quan trọng trong sheet:**
- Tổng chi từng tháng = SUM các hạng mục
- Dự phòng = tổng chi * 15%
- Số dư còn lại = nguồn vốn - tổng ngân sách (lũy kế theo tháng)
- Cột % ngân sách = tổng 6 tháng / tổng nguồn vốn

**Tham chiếu cho từng con số:** Mỗi khoản mục trong sheet "Tham chiếu ngân sách" phải ghi rõ:
- Giá trị cụ thể
- Cơ sở tham chiếu (khảo sát thị trường, báo giá NCC, % giá thành SP, mặt bằng lương ngành)
- Cách tính (VD: BHXH = 20% lương cơ bản; Autoclave = báo giá thiết bị lab)

## Tài liệu cần chuẩn bị

Khi trình cổ đông hoặc gia đình:
1. **Business Plan 1 trang** — mô hình, đội ngũ, thị trường
2. **Bảng phân bổ tiền** — chi tiết từng khoản
3. **Sơ đồ tổ chức mới** — ai ở đâu, báo cáo ai
4. **KPI 6 tháng đầu** — doanh thu, số lượng sản phẩm, team size

## Common Pitfalls

1. **Nói "tách" thay vì "nâng lên"** — mẹ/bố sẽ coi là phản bội
2. **Để partner nói chuyện với mẹ trước khi user mở đường** — người lạ chưa có trust
3. **Đốt cháy — tuần 1 đã đòi tách** — phải cho thấy kết quả trước
4. **Quên gia đình sau khi tách** — họ cảm thấy bị bỏ rơi, sẽ quay lại phá
5. **Không phân định ranh giới** — người đại diện PL ký vào việc của người kia
6. **Flat nhưng không có quy chế** — ai cũng làm việc của ai, conflict leo thang lên mẹ
7. **Quên ủy quyền ký** — mọi hợp đồng đều phải qua 1 người, bottleneck
8. **Không lập ngân sách từ đầu** — 5 tỷ trong tài khoản nhưng không biết tiền đi đâu, về đâu. Cần sheet ngân sách chi tiết ngay tuần 1.
9. **Không tính số dư còn lại** — chỉ biết chi bao nhiêu mỗi tháng mà không biết còn bao nhiêu sau 6 tháng. Công thức = nguồn vốn - tổng ngân sách lũy kế.
10. **Không ghi tham chiếu cho từng con số ngân sách** — đến lúc cổ đông hỏi "sao lại 18tr/tháng?" thì không có cơ sở trả lời.

## References

- `references/restructuring-plan-2026-09.md` — Session detail: Mana Đất Vàng restructuring case (September 2026)
