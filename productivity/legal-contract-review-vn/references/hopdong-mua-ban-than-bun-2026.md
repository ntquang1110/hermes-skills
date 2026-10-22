# Ví dụ: Rà soát Hợp đồng Mua bán Đất than bùn

**Hợp đồng số:** 01/07/HĐMB-TG-MĐV/2026  
**Bên Mua:** Công ty CP Manna Đất Vàng (Hà Nội)  
**Bên Bán:** Công ty CP Thiên Giang (An Giang)  
**Hàng hóa:** Đất than bùn — 100 tấn

## Cấu trúc phân tích đã dùng

### Phát hiện chính (10 rủi ro)

| Mức | Điều khoản | Vấn đề |
|:---:|:----------:|--------|
| ⚠️ | 1.2 | Chỉ tiêu chất lượng bỏ trống — tử huyệt |
| 🔴 | 3.1 | Đặt cọc 50% quá cao |
| 🔴 | 1.4 | Công thức bù độ ẩm sai — thiệt ~1.250 kg chất khô/100 tấn |
| 🔴 | 11.2 | Thẩm quyền Tòa án An Giang — bất lợi cho Bên Mua HN |
| 🔴 | 8.4 | Chế tài cọc khó áp dụng — "mục đích giao kết không đạt" mơ hồ |
| 🟠 | 1.5 | Từ chối hàng không cơ chế xử lý chi phí lưu kho/vận chuyển ngược |
| 🟠 | 4.3 | Một mốc giao hàng duy nhất 31/07 — dễ dồn 100 tấn vào 1 ngày |
| 🟠 | 4.4 | Trách nhiệm thông báo thuộc Bên Mua (đáng lẽ Bên Bán phải báo trước) |
| 🟡 | 8.1 | Phạt chậm giao 0.05%/ngày (~67.500đ/ngày) — thấp, không răn đe |
| 🟡 | 10.1 | Zalo là phương thức thông báo chính thức |

### Công thức phát hiện sai

**Công thức sai (trong hợp đồng):**
```
Khối lượng bù = Khối lượng thực nhận × (Độ ẩm thực tế - 20%)
```
-> Không quy đổi về chất khô → luôn thiệt cho Bên Mua.

**Công thức đúng:**
```
M_quy_chuẩn = M_thực_nhận × (100% - Ẩm_thực_tế) / (100% - 20%)
```

### Đề xuất sửa đổi mẫu

```markdown
> *"Trường hợp độ ẩm thực tế vượt quá 20% nhưng không vượt quá 30%, 
> khối lượng thanh toán được quy đổi về độ ẩm chuẩn 20% theo công thức:
> M_quy_chuẩn = M_thực_nhận × (100% - Ẩm_thực_tế) / 80%"*
```

### Đầu ra đã giao

- File .md local → Gist (private) → htmlpreview.github.io
- Notion standalone page dưới "Blog của Quang"
- 4 nhóm ưu tiên (Cấp bách → Quan trọng → Nên sửa → Giữ nguyên)
