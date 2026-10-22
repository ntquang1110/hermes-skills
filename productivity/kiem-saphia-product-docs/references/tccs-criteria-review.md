# Đánh giá TCCS / chỉ tiêu công bố sản phẩm TĂCN (heo, gia súc)

Quang gửi Google Doc TCCS (tiêu chuẩn cơ sở) hoặc bảng chỉ tiêu công bố và hỏi: "chỉ tiêu này có ảnh hưởng đến sinh trưởng của lợn con không?" / "có hợp quy không?". Đây là bài toán lặp lại mỗi lần soạn/duyệt TCCS sản phẩm.

## 1. Đọc doc — KHÔNG dùng google_api.py docs get cho doc có bảng

- `export?format=txt` fail (login page) với doc không public → dùng Google API OAuth token có sẵn.
- **`google_api.py docs get` BỎ SÓT BẢNG** — body chỉ còn đoạn văn, mọi số liệu chỉ tiêu trong table đều mất. Dùng `scripts/read_google_doc_tables.py <DOC_ID>` (walk cả PARAGRAPH lẫn TABLE, xuất ` | `).

## 2. Khung đánh giá "chỉ tiêu có hại sinh trưởng không"

Với sản phẩm trộn vào TĂ (VD EZ80: 5kg/tấn = 0,5%):

1. Lấy từng chỉ tiêu chất lượng (Ca, Fe, Mg, K, Mn, Zn, hoạt chất...) đơn vị mg/kg SP.
2. Nhân tỷ lệ trộn (0,005 với 5kg/tấn) → mg/kg trong TĂ hoàn chỉnh.
3. So với:
   - **Nhu cầu heo con** (mg/kg TĂ): Ca ~8.000-9.000; Fe ~100 (ngưỡng độc ~3.000); Mg ~400-500; K ~2.000-3.000; Mn ~20-40; Zn ~80-100.
   - **Liều hiệu quả hoạt chất** (saponin trên heo cai sữa: 300-750 mg/kg TĂ mới có đáp ứng — Ilsley 2005 PMID 15583046; quinoa hull 100-500 mg/kg PMID 21392128; sensory additives PMID 24668952). Berberin liều thử ~200+ mg/kg TĂ.
   - Phần đóng góp << nhu cầu/lợi ích → "không hại nhưng cũng không có tác dụng sinh học đáng kể ở liều công bố". Đừng overclaim hoạt chất.
4. **Chỉ tiêu an toàn** (As, Pb, Cd, Hg, Salmonella) — trần QCVN 01-190:2020/BNNPTNT (SĐ1:2021):
   - **TĂ hoàn chỉnh / đậm đặc (Phụ lục III, vật nuôi khác):** As ≤2, Cd ≤0,5, Pb ≤5, Hg ≤0,1 mg/kg; E.coli 0/1g; Salmonella 0/25g; Aflatoxin B1 ≤20 µg/kg.
   - **Thức ăn bổ sung Premix (Phụ lục II mục 1):** As ≤30, Cd ≤15, Pb ≤200 mg/kg; Salmonella 0/25g.
   - **Thức ăn bổ sung hỗn hợp khác (Phụ lục II mục 2):** As ≤4, Pb ≤10 mg/kg; Aflatoxin B1 ≤30 µg/kg; Salmonella 0/25g.
   - Nguyên liệu đơn khoáng: CaCO3 As≤15/Pb≤20; photphat As≤10/Cd≤10/Pb≤15; MgO As≤20/Cd≤2; ZnO As≤100/Cd≤30/Pb≤400; MnO As≤100/Cd≤30/Pb≤200.
   - Tính ngược: trần SP → nhân tỷ lệ trộn → so với trần TĂ hoàn chỉnh để kết luận "dù ở mức max vẫn an toàn".
5. **Cạm bẫy phân loại:** bộ As 30/Pb 200/Cd 15 trong TCCS EZ80 khớp ĐÚNG trần **Premix** — nếu cơ quan phân loại SP là "thức ăn bổ sung hỗn hợp khác" thì Pb 200 vượt trần (10). Luôn đối chiếu mức công bố với đúng nhóm sản phẩm.

## 3. Điều rút ra từ case KIỀM EZ TÁI SINH 80 BABY (TCCS 06:2025/MNĐV, 05/12/2025)

- Công bố: Ca 49.000, Fe 15.000, Mg 8.500, K 5.300, Mn 750, Zn 50, Berberin 20, Saponin 1.500 (mg/kg, min); độ ẩm ≤12%; As ≤30, Pb ≤200, Cd ≤15, Salmonella 0/25g. Trộn 5kg/tấn.
- Quy ra TĂ: Ca +245, Fe +75, Mg +42, K +26, Mn +3,75, Zn +0,25, Berberin +0,1, Saponin +7,5 mg/kg → tất cả dưới nhu cầu và ngưỡng độc → **KHÔNG ảnh hưởng xấu sinh trưởng lợn con ở liều chuẩn**.
- Kim loại nặng ở mức max: As 0,15 / Pb 1,0 / Cd 0,075 mg/kg TĂ — đều dưới trần hoàn chỉnh.
- Lưu ý bán hàng: Zn/berberin/saponin quá thấp để gây tác dụng sinh học — chỉ là điểm cộng nhãn, không phải cơ chế tăng trưởng. Rủi ro thật nằm ở việc trại lạm dụng liều (kiềm mạnh → trung hòa dạ dày lợn con → tiêu hóa kém) — khuyến cáo ghi "không tăng liều".
- Nguồn QCVN lấy từ luatvietnam.vn (thuvienphapluat bị Cloudflare chặn curl trực tiếp).