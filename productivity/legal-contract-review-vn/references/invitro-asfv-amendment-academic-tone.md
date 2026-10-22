# Bổ sung Hợp đồng In vitro — Học viện Nông nghiệp (Amendment-on-Template với đối tác học thuật)

## Bối cảnh

- **Bên A:** Công ty CP Manna Đất Vàng
- **Bên B:** Học viện Nông nghiệp Việt Nam (VNUA)
- **Mẫu gốc:** Học viện gửi mẫu "Hợp đồng Phân tích" số 22-HĐPT/2026 (thiếu nhiều điều khoản)
- **Yêu cầu:** Bổ sung điều khoản vào mẫu của Học viện + tô đậm phần bổ sung + tôn trọng đơn vị nghiên cứu

## Chiến thuật: Amendment-on-Template với Tone Học thuật

### 1. Phát hiện điều khoản THIẾU (Quan trọng hơn điều khoản SAI)

| Điều khoản | Trong mẫu Học viện? | Mức độ |
|:----------:|:-------------------:|:------:|
| Sở hữu kết quả nghiên cứu | Không | 🔴 TỬ HUYỆT |
| Cấm reverse engineering | Không | 🔴 TỬ HUYỆT |
| Thời gian cam kết rõ ràng | Không (ghi "theo thực tế") | 🟠 |
| Quyền giám sát/chứng kiến | Không | 🟠 |
| Bảo mật sau chấm dứt | Không có thời hạn | 🟠 |
| Chế tài sai sót | Không | 🟠 |
| Giải quyết tranh chấp cụ thể | "Tòa án có thẩm quyền" (chung chung) | 🟡 |

### 2. Ngôn ngữ phù hợp với đối tác học thuật

| Không dùng | Thay bằng |
|:----------|:----------|
| "Bên A có quyền yêu cầu báo cáo" | "Hai bên cùng cập nhật tiến độ định kỳ" |
| "Quyền giám sát, theo dõi" | "Phối hợp theo dõi và cử người tham gia chứng kiến (nếu cần)" |
| "Bắt buộc" | "Có trách nhiệm" |
| "Yêu cầu" | "Mong muốn" / "Đề nghị" |
| "Cấm" | "Không được" |
| Phạt 200 triệu | Bồi thường thiệt hại thực tế (hoặc phạt nhẹ) |

### 3. Cấu trúc văn bản bổ sung

Giữ nguyên tiêu đề, số HĐ, ngày tháng của đối tác. Thêm "(Bổ sung, sửa đổi lần 1)" vào tên và đánh dấu thay đổi:

```
HỢP ĐỒNG PHÂN TÍCH
Số: 22-HĐPT/2026 – Bổ sung, sửa đổi lần 1
```

### 4. Thêm các điều khoản còn thiếu

| Vị trí | Thêm | Nội dung |
|:------:|:----:|----------|
| Sau phần căn cứ | Luật SHTT | "Căn cứ Luật SHTT 50/2005 (sửa đổi 2022)" |
| Điều 1 | 1.3(c)(d)(e) | Tiến độ 45 ngày, báo cáo 7 ngày/lần, bàn giao 10 ngày |
| Điều 2.1 | (d)(e) | Phối hợp Protocol + chứng kiến thí nghiệm |
| **Mới: Điều 3** | 3.1-3.5 | **SỞ HỮU KẾT QUẢ** — toàn bộ thuộc Bên A, ghi nhận đơn vị thực hiện, cấm RE, tư vấn bài báo |
| **Mới: Điều 4** | 4.1-4.3 | **BẢO MẬT** — thời hạn 5 năm, vi phạm bồi thường thiệt hại thực tế |
| Điều 6 (cũ 5) | 6.1 | Trọn gói, không phát sinh |

### 5. Điều khoản Bổ sung — Tư vấn công bố bài báo (tạo thiện chí)

```text
3.5. Trong trường hợp kết quả nghiên cứu đạt yêu cầu, Bên A mong muốn Bên B hỗ trợ
tư vấn bổ sung các chỉ tiêu chuyên môn để phục vụ công bố bài báo khoa học. Nội dung
tư vấn, phạm vi công việc và kinh phí thực hiện (nếu có) sẽ do hai bên thương lượng
và thống nhất bằng văn bản trên tinh thần hợp tác cùng có lợi.
```

Từ khoá: "mong muốn" (không phải "yêu cầu"), "hỗ trợ tư vấn" (hợp tác), "kinh phí (nếu có)" (không ép miễn phí).

### 6. Xử lý lỗi soạn thảo trong mẫu đối tác

| Lỗi | Sửa |
|:----|:----|
| "Cung cấp cho **Bên B**" (ghi sai bên) | "cho **Bên A**" |
| "15 (mười **năm**) ngày" | "15 (mười **lăm**) ngày" |
| "Bên **Bhịu** trách nhiệm" | "Bên B **chịu** trách nhiệm" |
| Thiếu mục (c) giữa (b) và (d) | Đánh số lại |
| 2 cái Điều 5 | Sắp xếp Điều 3 -> 4 -> 5 |

### 7. Kỹ thuật DOCX — Màu xanh cho bổ sung

```python
BLUE = RGBColor(0, 51, 153)

def multi(parts, indent=0, sb=2, sa=2, align=None):
    """parts = [(text, bold, color_or_None)]"""
    p = doc.add_paragraph()
    ...
    for item in parts:
        if len(item) == 3:
            t, b, c = item
        else:
            t, b = item
            c = None
        r = p.add_run(t); r.bold = b; r.font.size = Pt(13); r.font.name = 'TNR'
        if c: r.font.color.rgb = c
    return p

# Dùng: multi([('Nội dung cũ', False, None), ('Nội dung mới', False, BLUE)])
# None = màu đen mặc định
```

### 8. Ghi chú cuối văn bản

Thêm dòng ghi chú sau Phụ lục để giải thích các bổ sung:

```text
Ghi chú: Các nội dung màu xanh là bổ sung nhằm hoàn thiện Hợp đồng,
trên tinh thần tôn trọng hợp tác nghiên cứu khoa học giữa hai bên.
```
