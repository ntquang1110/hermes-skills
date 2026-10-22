# Chuyên luận Dược điển Việt Nam VI — đã đọc nguyên văn

Knowledge bank dùng lại được. **Nguồn**: `nhathuocngocanh.com/duoc-dien-viet-nam/<slug>/` — bản DĐVN VI theo **Quyết định 3960/QĐ-BYT ngày 26/12/2025**. Mọi con số dưới đây đã đọc từ trang, không phải suy đoán.

## BẪY NGHIÊM TRẬN: slug đoán sai trả HTTP 200

`/duoc-dien-viet-nam/cam-thao/` → **Cam thảo NAM (Scoparia dulcis)**, KHÔNG phải Cam thảo. Chuyên luận đúng: `cam-thao-re-va-than-re-glycyrrhizae-radix-et-rhizoma/`. Trang trả 200 + parse sạch → rất dễ ship nhầm mà không có tín hiệu cảnh báo.

**Luật:** sau khi tải slug bất kỳ, đọc dòng `<title>` / phần đầu chuyên luận để xác nhận **tên khoa học** khớp loài. Đừng tin HTTP 200.

## Cách tra slug (không đoán)

```python
# 1) Tra theo từ khoá — lọc bỏ "Phụ lục*"
GET https://nhathuocngocanh.com/wp-json/wp/v2/search?subtype=duocdienvn&per_page=8&search=<từ+khoá>
#    -> [{id, title:{rendered}, url, ...}]
# 2) Liệt kê toàn bộ chuyên luận (1100 posts, 11 trang)
GET https://nhathuocngocanh.com/wp-json/wp/v2/duocdienvn?per_page=100&page=N&_fields=link,title
```

**Lỗi JSON shape:** endpoint `search` trả `title` là **string**, khác endpoint `duocdienvn` trả `title` là dict → `it["title"]["rendered"]` ném `TypeError: string indices must be integers`. Dùng:
```python
ti = it["title"]["rendered"] if isinstance(it.get("title"), dict) else str(it.get("title"))
```

## Slug đã verify (8 chuyên luận, đọc đầy đủ)

| Dược liệu | Latin | Slug đã verify |
|---|---|---|
| Cam thảo | Glycyrrhiza glabra / uralensis / inflata | `cam-thao-re-va-than-re-glycyrrhizae-radix-et-rhizoma` |
| Nhân sâm | Panax ginseng | `nhan-sam-than-re-va-re` |
| Tam thất | Panax notoginseng | `tam-that-re-cu` |
| Sài hồ | Bupleurum chinense | `sai-ho-re` |
| Hoàng kỳ | Astragalus membranaceus | `hoang-ky-re` |
| Tục đoạn | Asparagus cochinchinensis | `tuc-doan-re` |
| Ngưu tất | Achyranthes bidentata | `nguu-tat-re` |
| Hoàn bổ trung ích khí | Cirsium + Radix Glycyrrhizae | `hoan-bo-trung-ich-khi` |

Cũng có: `tao-meo-qua`, `tao-hat`, `ba-kich-re`, `giao-co-lam`, `ngai-cuu`, `mach-mon-re`, `dang-sam-re`.
**Trả 404 (đừng dùng):** `cam-thao-nam` *(là URL hợp lệ nhưng trỏ sang Scoparia — khác loài!)*, `dat-quyen-ngoc-bat`, `bun-chi`, `tu-lan`, `tao-mo`, `tao-du-dau`, `hoang-sam`, `ngoc-truc-than-re`, `mien-pha`, `bach-kich`.

Pattern: slug thật là **tên Latin đầy đủ + Latin bộ phận dùng** khi dược liệu có nhiều bộ phận; hoặc tên VN không dấu khi tên đó là duy nhất.

## Trích phần Định tính / Định lượng

Menu điều hướng chiếm ~9 500 ký tự đầu file, chứa từ khoá gây nhiễu (`Tính chất`, `Chất chiết`) → **đừng `find()` trên toàn text**:

```python
i = t.find("Định tính")          # fallback: "Tính chất" → "Chất chiết"
j = t.find("Tài liệu tham khảo", i)
excerpt = t[i:j if j > i else i+6000]
# bản dài (Cam thảo, Nhân sâm, Tam thất): cắt theo mốc "Độ ẩm" vì định tính nằm sớm hơn hẳn
```

## Ngưỡng chất lượng đã verify

| Dược liệu | Chất đánh dấu | Ngưỡng | λ | Cột / số đĩa tối thiểu | RSD |
|---|---|---|---|---|---|
| **Cam thảo** | Acid glycyrrhizic | **≥ 2,0 %** | 254 nm | C18 25×4 mm / ≥ 5000 | ≤ 2,0 % |
| **Nhân sâm** | Tổng Rg1+Re; Rb1 | **≥ 0,3 %; ≥ 0,2 %** | 203 nm | C18 25×4,6 / ≥ 6000 | ≤ 2,0 % |
| **Tam thất** | NGR1; tổng Rg1+Rb1+NGR1 | **≥ 0,4 %; ≥ 5,0 %** | 203 nm | C18 25×4,6 / ≥ 4000 | ≤ 2,0 % |
| **Sài hồ** | Saikosaponin A | **≥ 0,16 %** | 210 nm | C18 25×4,6 / ≥ 4000 | ≤ 5,0 % |
| **Hoàng kỳ** | Astragalosid IV | **≥ 0,04 %** | — | / ≥ 4000 | — |
| **Hoàng kỳ** | Calycosin-7-O-β-D-glucosid | ≥ 0,02 % | — | / ≥ 3000 | — |
| **Tục đoạn** | Asperosaponin VI | **≥ 2,0 %** | 212 nm | — | — |
| **Ngưu tất** | β-Ecdysteron | **≥ 0,03 %** | 250 nm | — | — |
| **Táo mèo** | Acid chlorogenic | ≥ 0,1 % | 327 nm | / ≥ 6000 | ≤ 2,0 % |
| **Ba kích** | Monotropein | ≥ 0,6 % | 237 nm | / ≥ 5000 | — |

### Ba chi tiết kỹ thuật hay bỏ sót

1. **Cam thảo dùng CHUẨN LÀ MUỐI**: chuẩn = **amoni glycyrrhizinat**, quy đổi `khối lượng acid glycyrrhizic = khối lượng amoni glycyrrhizinat ÷ 1,0207`. Bỏ phép quy đổi = sai hệ thống 2,07 %.
2. **Sài hồ giải trích KIỀM**: amoni hydroxyd trong methanol (1 thể tích NH₃ 25 % : 4 thể tích methanol), siêu âm 30 phút, ly tâm, **chiết lặp 3 lần**. Chuẩn nhiều mức: 25, 50, 100, 300 µg/ml. Yêu cầu thêm độ phân giải ≥ 1,5.
3. **Bắt buộc tách pha n-butanol để loại đường** (Nhân sâm, Hoàng kỳ): hồi lưu n-butanol bão hòa nước → **rửa nhiều lần bằng nước** → bốc cắn. Bỏ bước này thì đường hòa tan cùng mẫu, hấp thụ UV 203 nm, kết quả thành toàn carbohydrate chứ không phải saponin/chất đánh dấu. Nhân sâm còn phải Soxhlet **cloroform 3 h** trước để loại chất tan trong mỡ.

### Độ ẩm giới hạn (điểm chất lượng, KHÔNG phải an toàn)

Sài hồ & Hoàng kỳ ≤ 10,0 % · Nhân sâm & Cam thảo ≤ 12,0 % · Táo mèo ≤ 13,0 % · Tam thất ≤ 14,0 %.

## Ghi chú pháp lý/dân gian đáng cite

- **Cam thảo**: "Tránh nhầm Cam thảo với rễ Thổ cam thảo (cây ở Cao Bằng) có vị ít ngọt, có mùi lợm." — chứng tỏ DĐVN VI tự cảnh báo nhầm lẫn loài.
- **Cam thảo chế biến**: rửa phải **nhanh** ("rửa lâu giảm tác dụng") → hàm ý mất thành phần tan trong nước.
- **Nhân sâm**: củ mất cuống (thân rễ) thì "ít có giá trị vì cuống là để biết số năm tuổi"; trồng đặc biệt để trưng bày có tuổi 4–6 năm.
- **Kiêng kỉ cam thảo**: "Cam thảo kỵ với cam toại cấm dùng."