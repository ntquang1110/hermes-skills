# Viết lại bài kể thất bại của chính mình (failure-story rewrite)

Dùng khi: audit một bài đã đăng bị chê (xem `post-criticism-audit.md`) và user yêu cầu
**"viết lại bài này áp dụng chặt humanizer + sửa theo đề xuất, tự phản biện rồi trả bản cuối"**.

Case mốc: post `DerUNeQgXe9` (peak-end rule), 2026-10-19.
v1 = 14 phần / 5.243 chars / 32.5K views / 57 like / 6 comment ngoài với tổng 83 like,
ba comment chê nặng nhất 82 like (nhiều hơn like của cả bài). Tương tác chết từ phần 3.
v2 = **7 post / 2.773 chars (giảm 47%)**, dấu TV 552, max part 458, unslop PASS, "tôi" 0.

## Công thức 6 bước (thứ tự bắt buộc)

1. **Đảo kết luận nhận trách nhiệm lên phần 2.** Không để ở gần cuối như v1 (phần 11).
   Xoá sạch mọi câu quy kết người đọc/khách ("não khách lười", "khách viết review bằng lần cuối
   gọi support"). Cơ chế tâm lý chỉ còn vai trò giải thích, không còn vai trò biện hộ.
2. **Giữ đúng 2 bằng chứng mạnh nhất**, mỗi cái kèm số (nước lạnh 1993 + 682 bệnh nhân 2003).
   Bỏ phần còn lại: nghiên cứu 1996, khái niệm tiếng Anh dựng riêng (duration neglect),
   vòng xoáy đối xứng "chiều tệ/chiều tốt", ví dụ phụ (kỳ nghỉ mất ví). Thuật ngữ giữ lại thì
   phải có ích cho người đọc, không phải để khoe.
3. **Thiếu số thật thì NÓI THẲNG cái thiếu, đừng bù bằng lý thuyết.** v1 có 0 số cho sự cố thật
   (lỗi gì, chậm bao lâu, SLA) trong khi bằng chứng toàn y khoa → bị soi đúng chỗ đó. v2 viết:
   "Đến giờ mình vẫn không nhớ hôm đó khách chờ bao lâu. Không ghi lại thì không sửa được, nên
   mình bắt đầu ghi." Rồi biến nó thành 2 hành động cụ thể.
4. **Mỗi phần lý thuyết phải kèm 1 số hoặc 1 hành động.** Phần nào không có thì cắt.
5. **Kết bằng câu hỏi CHO NGƯỜI ĐỌC**, không tự hỏi chính mình (v1 kết bằng câu tự vấn).
6. **Đo lại, đừng ước lượng:** `verify_draft.py` + `unslop_check.py`. Mục tiêu: chars giảm ~50%,
   số post ≤ 8, max part ≤ 498.

## Danh sách câu PHẢI xoá khi rewrite (rút từ chính v1, đã bị đọc là "văn Gemini")

| Câu trong v1 | Loại tell | Cách xử lý |
|---|---|---|
| "Giờ tới phần khiến mình phải ngồi lại." | signposting | xoá, vào thẳng nội dung |
| "Nghe vô lý, nhưng đó là cách não làm việc." | signpost + trấn an | xoá |
| "Bản thử nghiệm chí mạng nhất là năm 2003." | dramatic framing | đổi thành mốc trung tính ("Mười năm sau, …") |
| "Não không cố ý làm khổ bạn. Não tiết kiệm năng lượng thôi." | reassurance kicker + câu cụt | xoá |
| "Mình đọc đi đọc lại câu đó." | dựng cảm xúc giả | xoá |
| "Vòng xoáy chạy hai chiều. Chiều tệ: … Chiều tốt: …" | đối xứng máy móc | xoá hoặc gộp một chiều |
| 3 phần liên tiếp mỗi phần kết 1 câu chốt ngắn | punchy kicker mỗi đoạn | gộp 2 câu chốt vào câu chính, giữ 1 nhịp ngắn |
| "Năm 1993, …" rồi "Năm 2003, …" mở 2 phần liền | trùng khuôn mở câu | đổi một cái thành "Mười năm sau, …" |
| "cái tôi trải nghiệm" / "cái tôi ghi nhớ" | chuỗi "tôi" ngoài quote → máy gắn cờ | đổi thành "phần đang trải nghiệm" / "phần ghi nhớ" |
| "ticket" | từ ngoại hành chính | đổi thành "yêu cầu hỗ trợ", "ca gấp" |

Câu tự biện hộ cũng phải đổi: "hiểu nó để sửa, **không phải để bào chữa**" đọc ra như đang thanh minh
→ viết thành khẳng định: "hiểu nó mới sửa được chỗ mình làm sai".

## Tự phản biện trước khi trả bản cuối (5 câu hỏi)

Trả lời được hết rồi mới gửi user:

1. Có bao nhiêu câu chốt ngắn ở cuối phần? Quá 1 nhịp ngắn là dấu hiệu máy.
2. Hai phần liền nhau có mở cùng một khuôn không ("Năm X… Năm Y…", "Điều đáng chú ý là…")?
3. Có câu nào đọc ra như đang tự biện hộ hoặc tự khen không?
4. Đếm "tôi" ngoài quote (kể cả nằm trong "cái tôi") = 0 chưa?
5. Còn từ ngoại nào thay được bằng từ Việt không?

## Khi nào KHÔNG nên cắt thêm

Nếu v2 đã ở ~2.7-2.8K mà user muốn giữ quãng 3-7K theo quy ước: thêm **phần hệ thống/hành động**
(quy trình khép vòng với khách, cách đo lại sau 30 ngày), KHÔNG thêm lại lý thuyết đã cắt.
Mục tiêu là giữ độ dài quen mắt mà không nhồi lại đúng thứ đã làm bài bị chê.
