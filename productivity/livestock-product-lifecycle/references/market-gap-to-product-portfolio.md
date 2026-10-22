# Từ Market Gap → Product Portfolio (danh mục sản phẩm)

Bổ sung cho `market-gap-analysis-framework` Phase 6. Framework gốc dừng ở **hero product** (một sản phẩm tiêu biểu cho mỗi gap). Khi khách hàng muốn **danh mục sản phẩm đầy đủ để đưa vào sản xuất**, chạy thêm bước này.

Đã kiểm chứng 10/2026 (chăn nuôi lợn VN: 15 gap → 21 SKU, 3 nhóm).

---

## Khi nào chạy

| Tình huống | Chạy |
|---|---|
| "Sản phẩm nào nên làm trước?" | Hero product là đủ |
| "Danh mục sản phẩm của tôi nên gồm gì?" | **Chạy portfolio** |
| "Bao nhiêu SKU, giá bao nhiêu, cái nào làm được ngay?" | **Chạy portfolio** |
| Khách vận hành một mình, cần biết cái nào vượt năng lực | **Chạy portfolio** — phần này quyết định nhất |

---

## Bước 1 — Phân nhóm gap thành 3 nhóm sản phẩm

Đừng để 15 gap biến thành 21 SKU lộn xộn. Nhóm theo **bản chất can thiệp**, không theo phân khúc khách hàng:

| Nhóm | Can thiệp ở đâu | Ví dụ (chăn nuôi) |
|---|---|---|
| **TRONG** | Bổ sung qua thức ăn / nước uống | postbiotic, men, điện giải, xử lý nước uống |
| **NGOÀI** | Vệ sinh chuồng, sát trùng, môi trường | chất tẩy rửa, sát trùng, xử lý mùi/phân |
| **DỊCH VỤ** | Protocol, đo lường, audit, outcome-based | đào tạo SOP, test ATP, kiểm toán, hợp đồng KPI |

**Lợi ích:** mỗi nhóm có logic riêng về rào cản pháp lý, kênh bán, vòng đời — xử lý song song được.

**Cách chạy khi gap nhiều:** delegate 3 task song song, mỗi task một nhóm, mỗi task nhận đầy đủ gap của nhóm đó + thông tin năng lực công ty. Output chuẩn hóa để gộp được.

---

## Bước 2 — Mỗi SKU cần 6 trường tối thiểu

Khách ở giai đoạn này **chưa cần công thức/COGS** — cần biết "làm cái gì, để làm gì, giá bao nhiêu, làm được không".

| Trường | Ví dụ |
|---|---|
| Tên SKU | VK-IN-01 START28 Pack |
| Công dụng (1 câu) | Giữ tỷ lệ sống & ADG 28 ngày đầu sau nhập heo |
| Thành phần dự kiến | postbiotic, điện giải, vitamin |
| Cơ chế tác động | Vì sao hiệu quả — cơ chế, không phải mô tả |
| Đơn giá đề xuất | 25.000 đ/con/28 ngày |
| **Fit nguồn lực** | **phù hợp ngay / cần đầu tư / không phù hợp** |

### Trường quan trọng nhất: Fit nguồn lực

Đây là trường **quyết định toàn bộ giá trị** của portfolio. Khách vận hành đơn lẫn thì "làm được ngay" quan trọng hơn "có tiềm năng".

| Mức | Nghĩa là | Ghi kèm |
|---|---|---|
| **Phù hợp ngay** | Dùng công nghệ/năng lực hiện có, không cần đầu tư | — |
| **Cần đầu tư** | Cần thêm vốn, thiết bị, nghiên cứu, đối tác | Nêu cụ thể cần gì |
| **Cần đối tác** | Phải có bên khác (GMP, đăng ký, lab) | Nêu loại đối tác |
| **Ngoài năng lực** | Không nên đề xuất | Nói thẳng, không để trong danh mục |

**Với sản phẩm "cần đối tác", ghi rõ điều kiện đăng ký pháp lý** (vd: hóa chất sát trùng môi trường chăn nuôi = thuốc thú y → cần số đăng ký hoặc đối tác GMP). Đây là thứ quyết định timeline thật.

---

## Bước 3 — Ràng buộc chéo toàn nhóm

Mỗi nhóm có ràng buộc riêng phải kiểm, nếu không SKU sẽ tự mâu thuẫn:

| Nhóm | Ràng buộc phải check |
|---|---|
| **TRONG** | pH mọi SKU uống/ăn (không xung đột nhu cầu acid hóa dạ dày); không pha chung vaccine sống; đường TĂBS tự công bố thì **không được claim phòng/trị bệnh** |
| **NGOÀI** | hóa chất sát trùng = thuốc thú y (cần đăng ký); chất tẩy rửa thì nhẹ hơn; kiềm mạnh (pH > 11,5) không dùng khi có heo trong chuồng |
| **DỊCH VỤ** | cần đội kỹ thuật; nếu khách chưa có đội thì định giá phải nói rõ chi phí thuê người, không giấu vào giá |

**Sai lầm phổ biến:** 3 subagent mỗi thằng tự nghĩ SKU của mình đều hợp lý, nhưng lắp vào nhau thì mâu thuẫn (VD 2 SKU cùng claim về pH dạ dày heo cai sữa). **Luôn chạy đợt ràng buộc chéo sau khi gộp.**

---

## Bước 4 — Thứ tự ưu tiên

```
1. Phù hợp ngay + đường tự công bố        → vài tháng
2. Phù hợp ngay + cần đăng ký thuốc thú y  → 18-24 tháng
3. Cần đầu tư R&D                          → sau khi dòng 1 có dòng tiền
4. Cần đối tác chiến lược                  → sau khi có năng lực đàm phán
```

Nói rõ với khách hàng: **danh mục không phải lộ trình.** 21 SKU trông hấp dẫn nhưng không chia giai đoạn thì trông như mơ. Mỗi SKU phải gắn với 1 giai đoạn.

---

## Pitfalls

1. **Biến gap thành SKU 1-1 rồi bỏ chiều sâu.** Tỉ lệ 15 gap → 21 SKU là đúng, nhưng mỗi SKU chỉ có tên + giá thì vô dụng. Phải có cơ chế + fit nguồn lực.

2. **Giấu điều kiện pháp lý.** "Sát trùng 220-320k đ/L, fit cao" mà không nói cần số đăng ký thuốc thú y là **bán hàng ảo**. Timeline thật dài hơn 18-24 tháng.

3. **Không chia giai đoạn.** Khách thấy 21 SKU và hỏi "làm cái nào trước?" mà không có câu trả lời → portfolio vô dụng.

4. **Bỏ ràng buộc chéo giữa các nhóm.** Ba subagent chạy song song, mỗi thằng đúng, tổng thể sai.

5. **Đưa sản phẩm "ngoài năng lực" vào danh mục** rồi ghi chú nhỏ. Phải nói thẳng không nên làm, không để trong danh mục chính.

6. **Chạy COGS ở giai đoạn này.** Khách chưa cần. COGS cần công thức + giá nguyên liệu + quy mô sản xuất — làm sớm thì toàn bộ số liệu phải sửa lại.

---

## Output format

| Nhóm | Mã | Tên | Công dụng | Thành phần | Cơ chế | Đơn giá | Fit nguồn lực | Điều kiện để làm được |

Kèm:
- Bullet "phù hợp ngay" theo thứ tự ưu tiên
- Mục ràng buộc chéo đã kiểm
- Mục "chưa verify" — những thứ cần thực địa xác nhận