# Báo cáo thẩm định sáng chế (Patent Examination / Patentability Opinion)

Dùng khi deliverable là **ý kiến về khả năng được bảo hộ** của một giải pháp kỹ thuật (quy trình/sản phẩm) trước prior art:
chủ đơn hỏi *"tổ hợp các kỹ thuật đã biết này có tạo ra sáng chế được cấp bằng không?"*, hoặc cần ý kiến FTO (rủi ro xâm phạm).

Đây là **dạng báo cáo KHÁC pattern B (patent deep-dive)**: pattern B = giải thích "clone lại patent này thì làm thế nào";
pattern này = **phán xử** một giải pháp đề nghị so với prior art. Output mặc định tiếng Việt, có thể kèm bản HTML B/W/Y.

Mẫu đã chạy: `C:\Users\NTQUANG_DELL\Proj\guava-tannin-patent\BAO_CAO_THAM_DINH_SANG_CHE_BOT_TANNIN_LA_OI.md` + `.html` (24/09/2026, bột tannin lá ổi — 5 patent, 11 bảng).

---

## 0. Bước 0 bắt buộc trước khi viết: đọc CLAIM GỐC của mọi tài liệu

- Dùng `scripts/patent_claims.py <PN> [...]` của skill `vietnam-herbal-research` (curl + strip tag từ `patents.google.com/patent/<PN>/en` → claim nguyên văn + mô tả đầy đủ thông số %/°C/tỉ lệ/ví dụ).
- **Mô tả prior art trong brief/hồ sơ nội bộ rất hay sai** (case 24/09/2026: 4/4 patent được mô tả sai — sai assignee, sai quy trình cốt lõi, sai hóa chất, gán số liệu của patent được dẫn ở background). ⇒ In **bảng "chỉnh lệch so với hồ sơ" ngay đầu báo cáo**; phân tích dựa trên văn bản gốc, không dựa trên brief.
- Đọc cả **phần mô tả**, không chỉ claim: disclosure trong description vẫn phá **trình độ sáng tạo** (vd mô tả "chiết lá ổi bằng ethanol, tỉ lệ cồn/nước 1–99 %" + "dried … such as lyophilization").
- Đọc thêm **trạng thái pháp lý** (`Status Active` + `Anticipated expiration`) — patent đang hiệu lực ⇒ rủi ro **xâm phạm quyền**, không chỉ rủi ro bị từ chối.
- Tra bổ sung ngoài danh sách brief (từ khoá lĩnh vực + assignee) → gần như luôn tìm được ≥1 tài liệu brief bỏ sót.

## 1. Khung mục lục chuẩn

```
Header      : loại văn bản (KHÔNG phải thẩm định chính thức), ngày, người lập, cơ sở pháp lý,
              phạm vi tra cứu, KẾT LUẬN SƠ BỘ (1 khối, nói thẳng: nộp được hay không, yếu ở đâu)
I.   Đối tượng sáng chế đề nghị   — bảng bước/thông số, dữ liệu R&D nội bộ
     (+ bảng "chỉnh lệch so với hồ sơ" nếu brief sai)
II.  Tình trạng kỹ thuật đối chiếu — mỗi tài liệu: CLAIM NGUYÊN VĂN (quote), thông số mô tả, chủ sở hữu,
     ngày ưu tiên, trạng thái pháp lý, + 1 dòng "⛔ kết luận tài liệu này phá gì"
III. Tính mới                     — MA TRẬN bước × tài liệu (✅ bộc lộ / 🟡 một phần / ❌ không) + kết luận
IV.  Trình độ sáng tạo            — problem-and-solution: giải pháp gần nhất, khác biệt, hiệu quả kỹ thuật,
     yếu tố phi hiển nhiên, và LẬP LUẬN ĐỐI LẬP dự kiến của examiner
V.   Khả năng áp dụng công nghiệp — thiết bị/nguyên liệu VN + lưu ý ATLĐ & dư lượng dung môi
VI.  Bộ claim đề xuất             — claim 1 độc lập (a)(b)(c)…, claim phụ thuộc, claim SẢN PHẨM có tham số
     định lượng, claim chế phẩm, + fallback claim set khi bị phản đối
VII. Bảng ĐIỂM YẾU ↔ CÁCH KHẮC PHỤC  — 1 dòng = 1 objection dự kiến + mức nguy hiểm + cách đối đáp
VIII.Điểm mới mạnh nhất (xếp hạng 🥇🥈🥉)
IX.  HẠN CHẾ TRA CỨU (trung thực)  — bảng: cái gì đã verify ✅ / chưa tra ❌ / một phần 🟡
X.   Kết luận + bảng điểm + việc phải làm ngay (thứ tự ưu tiên)
Phụ lục A: nhật ký tra cứu (URL + nội dung đã đọc + ngày)   B: thông tin pháp lý cần đối chiếu
```

## 2. Bộ công cụ phân tích (đừng bỏ mục nào)

| Công cụ | Cách làm | Bẫy |
|---|---|---|
| **Ma trận novelty** | 1 hàng = 1 bước của giải pháp, 1 cột = 1 tài liệu; ký hiệu ✅/🟡/❌; đọc theo hàng để biết bước nào đã bị bộc lộ **trên đúng nguyên liệu** | ✓ cả 6 bước đều biết riêng lẻ nhưng chưa ai bộc lộ **tổ hợp** ⇒ tính mới chỉ còn ở mức tổ hợp → phải nói rõ "novelty yếu về thương mại vì sẽ bị tấn công ở inventive step" |
| **Closest prior art** | chọn tài liệu **cùng mục đích + cùng nguyên liệu**; khác biệt còn lại chính là "problem" | đừng chọn tài liệu "gần nhất về kỹ thuật" mà xa về ứng dụng |
| **Problem-and-solution** | nêu khác biệt cấu tạo → hiệu quả kỹ thuật → so với prior art | phân biệt rõ **khác biệt thực** vs **nhiễu**: nếu prior art đã dạy dải số bao trùm tham số của sáng chế (vd prior art dạy cô đặc "25–70 °C" còn sáng chế nêu "<50 °C") thì đặc trưng đó **KHÔNG phải khác biệt** — phải gạch ngay trong bảng |
| **Unexpected effect** | mỗi đặc trưng giữ lại phải kèm loại dữ liệu chứng minh | nếu chưa có dữ liệu ⇒ ghi rõ "phải làm thí nghiệm X trước khi nộp", không hứa suông |
| **Bảng objection ↔ đối đáp** | mỗi dòng: lập luận examiner + mức nguy hiểm (🔴→🔴🔴🔴) + cách khắc phục cụ thể | đây là phần chủ đơn dùng nhiều nhất — viết như checklist hành động, không phải văn nghị luận |
| **Hạn chế tra cứu** | liệt kê thẳng cái chưa tra (thường: **CNIPA tiếng Trung chưa có bản dịch**, Espacenet, tra cứu chính thức có thu phí) | không được im lặng bỏ qua — sẽ thành rủi ro khôn lường khi nộp |

## 3. Insight tái sử dụng (đã gặp thật, áp dụng cho mọi hồ sơ tương tự)

1. **Dữ liệu R&D của chính chủ đơn có thể phá tính sáng tạo.** Nếu brief ghi thông số được chọn KHÔNG phải tối ưu
   (case: 30 % ethanol 3,228 mg/g > 70 % 2,333 > 96 % 1,253), examiner gọi đó là **"lựa chọn tùy ý, không hiệu quả bất ngờ"**.
   Cách chữa duy nhất: đo chỉ tiêu **chất lượng** (độ tinh khiết hoạt chất, màu L*a*b*, độ đục khi hoàn nguyên, tạp chất)
   chứ không chỉ hiệu suất khối lượng + chuẩn bị **comparative examples** đúng theo dung môi mà prior art dạy.
2. **Điểm mới mạnh nhất thường không phải "đổi dung môi" mà là TƯƠNG TÁC giữa 2 bước** (synergy).
   Case: "cô đặc đến Brix 25–30" không phải lựa chọn tùy ý — prior art cho thấy đó là **ngưỡng chức năng để IPA 1:1 tách pha
   sạch mà không cần thêm muối/bisulfit**. ⇒ đặt tương tác đó vào claim 1.
3. **Trật tự bước + vị trí bước có thể là điểm mới** (case: phân lớp IPA TRƯỚC → than hoạt tính SAU; prior art dùng than ở
   giai đoạn khác ⇒ lập luận giữ được hoạt chất). Luôn đối chiếu **vị trí bước**, không chỉ sự có mặt của bước.
4. **Claim sản phẩm phải có THAM SỐ ĐỊNH LƯỢNG khác biệt**, nếu không sẽ bị đọc vào claim sản phẩm chung của prior art
   (case: "bột dịch chiết lá ổi" của prior art claim 2) ⇒ bắt buộc thêm ẩm %, cỡ hạt D50, hàm lượng hoạt chất, màu.
5. **Chủ sở hữu/bối cảnh có thể bị brief gán sai** → luôn đọc tên assignee + inventor thật trên trang patent; xác định
   "đối thủ lớn nhất trong không gian công nghệ" bằng cách xem assignee chiếm tỉ lệ cao trong kết quả tra cứu.

## 4. Đặc thù Việt Nam (cần đối chiếu bản hợp nhất khi soạn đơn — số điều có thể thay đổi)

- Điều kiện bảo hộ: **tính mới + trình độ sáng tạo + khả năng áp dụng công nghiệp** (sáng chế);
  **giải pháp hữu ích** chỉ cần **tính mới + khả năng áp dụng công nghiệp** → **đây là đường lui chiến lược** khi trình độ
  sáng tạo yếu (bảo hộ quy trình, thời hạn 10 năm thay vì 20 năm).
- Đối tượng **bị loại trừ**: bao gồm **phương pháp chữa bệnh cho người và động vật** ⇒ wording claim phải tránh
  ("chế phẩm hỗ trợ", "phụ gia thức ăn chăn nuôi", KHÔNG "điều trị/phòng bệnh").
- Đối tượng bảo hộ là **sản phẩm / quy trình / thiết bị** ⇒ claim dạng **"Sử dụng X để…" nên chuyển thể** thành
  claim quy trình, claim sản phẩm hoặc claim chế phẩm chứa sản phẩm đó.
- Trình độ sáng tạo đánh giá theo **tổ hợp tài liệu** (kết hợp 2–3 tài liệu cùng lĩnh vực, cùng mục đích, không có
  teaching-away ⇒ dễ bị coi là hiển nhiên) ⇒ luôn viết sẵn phần đối đáp cho tình huống này.
- Lưu ý triển khai (không ảnh hưởng bảo hộ): dư lượng dung môi hữu cơ cho sản phẩm thực phẩm/TĂCN; an toàn cháy nổ với ethanol/IPA.
- Kết quả tra cứu VN phải qua **tra cứu chính thức tại Cục SHTT** khi nộp — ghi rõ trong mục "hạn chế tra cứu".

## 5. Bảng điểm cuối báo cáo (giữ đúng format này — chủ đơn đọc con số trước)

| Tiêu chí | Điểm hiện tại | Sau khi bổ sung dữ liệu |
|---|---|---|
| Tính mới | x/10 | … |
| Trình độ sáng tạo | x/10 (ghi rõ YẾU/TRUNG BÌNH) | … |
| Khả năng áp dụng công nghiệp | x/10 | … |
| Rủi ro xâm phạm ở nước ngoài | CAO/TRUNG BÌNH/THẤP | … |

Kèm 3 câu trả lời trực tiếp: (a) có nộp được không; (b) có được cấp bằng không (kèm % ước lượng bị từ chối);
(c) đường lui (GPHI) + danh sách thí nghiệm phải làm ngay.
