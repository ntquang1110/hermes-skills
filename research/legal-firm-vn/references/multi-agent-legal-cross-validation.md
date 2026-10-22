# Multi-Agent Cross-Validation cho vụ việc pháp lý

Áp dụng khi: case ảnh hưởng > 50 triệu đồng, hoặc mang tính tiền triệu tỷ, hoặc kết luận sẽ dùng làm căn cứ ký kết.

## Tại sao cần

Một lượt phân tích bỏ sót điểm mà chỉ lộ ra khi đọc ngược. Cross-validation luôn tìm ra thứ một agent bỏ sót — đó là lý do làm, không phải thói quen.

Hai agent đọc **cùng một case nhưng đóng vai khác nhau**, rồi đối chiếu điểm mà mỗi bên tìm ra.

## Protocol

### Bước 1 — Chuẩn bị input

Mọi bên nhận CÙNG một gói:
- Toàn văn case / hợp đồng / tình huống pháp lý
- Kết quả `legal_kb.py check` cho các văn bản liên quan
- Danh sách câu hỏi cần trả lời (giống nhau cho cả 2 bên)

**Không** đưa kết luận của bên kia cho bên kia. Phá vỡ tính độc lập là phá vỡ toàn bộ giá trị của phương pháp.

### Bước 2 — Phân vai

| Bên | Vai trò | Tìm gì |
|------|---------|---------|
| **A — Bên bị can** | Đại diện lợi ích mà mình muốn bảo vệ | Điểm yếu pháp lý của chính mình, điều khoản bất lợi, rủi ro bị truy trách, thiếu sót trong lập luận mình dự kiến đưa ra |
| **B — Bên đối phương** | Lập luận ngược lại, mạnh nhất có thể | Cách lập luận mà đối phương dùng để đẩy bản lợi cho mình, điểm yếu trong hồ sơ, căn cứ pháp lý bất lợi cho mình, phương án tốt nhất cho họ |

Bên nào cũng phải trả lời: "Điểm mạnh nhất của phe đối diện là gì?" — bắt buộc, không bỏ.

### Bước 3 — Chạy song song

Dùng `delegate_task` với `tasks=[...]` (2 task, tối đa 3 của hệ thống). Mỗi task là 1 vai.

Mỗi subagent nhận:
- Đầy đủ input như Bước 1
- Chỉ dẫn rõ vai trò của mình
- Yêu cầu output theo format cố định để so sánh được

### Bước 4 — Đối chiếu

Lập bảng:

| Nội dung | Bên A nói | Bên B nói | Đánh giá | Ai đúng / ai thiếu |
|----------|-----------|-----------|----------|--------------------|
| Căn cứ pháp lý | | | | |
| Điểm rủi ro | | | | |
| Phương án khả thi | | | | |
| Mức chắc chắn | | | | |

3 loại phát hiện cần chú ý:

1. **Một bên nói, bên kia không nói** → điểm mới, thường là điểm yếu thật
2. **Hai bên nói khác nhau về cùng một vấn đề** → phải tra lại nguồn gốc, không bên nào được phép thắng bằng ý kiến
3. **Hai bên nói giống nhau** → phần đó khó, đã cân nhắc từ cả 2 góc

### Bước 5 — Tổng hợp

Output cuối cùng gồm 3 phần:

1. **Điểm hai bên đồng ý** — nền chắc nhất, viết thành kết luận chính
2. **Điểm hai bên bất đồng** — trình bày cả 2 lập luận, đánh dấu cái nào đã verify được
3. **Điểm chỉ một bên thấy** — đây là phần có giá trị cao nhất, cần đưa vào phần tự phản biện của `legal-critique-vn`

## Pitfalls

1. **Cho bên kia thấy kết luận của bên này** — mất tính độc lập, phương pháp vô nghĩa.
2. **Chạy tuần tự thay vì song song** — bên thứ hai bị nhiễu kết quả bên thứ nhất dù không cố ý.
3. **Chỉ so sánh điểm khác biệt** — điểm chung là phần đã an toàn, ghi vào kết luận chính, đừng bỏ qua.
4. **Bên nào có "tiếng to hơn" thì thắng** — không có tiếng to. Bên nào có căn cứ verify được mới thắng.
5. **Bỏ qua điểm chỉ một bên thấy** — đây chính là phần lỗi bỏ sót, đưa vào Phần 6 của critique.
6. **Dùng cho case nhỏ** — case < 50tr dùng một lượt là đủ. Cross-validation tốn thời gian, chỉ dùng khi kết luận sẽ dùng làm căn cứ.