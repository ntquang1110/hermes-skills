# Audit một bài Threads bị chê (post-criticism audit)

## Khi nào dùng

User gửi link một post Threads **đã đăng** (thường là bài của chính anh ấy) kèm câu dạng:
"phân tích bài này và giải thích tại sao mn chê lè nhè và đề xuất phương án xử lý".

Đây là việc **chẩn đoán có bằng chứng**, không phải việc viết bài mới. Deliverable là:
số liệu thật → 3 tầng nguyên nhân → lỗ thủng kỹ thuật → phương án xử lý có mục tiêu → câu hỏi
cần user xác nhận.

## Bước 1 — Lấy dữ liệu THẬT trước khi nói gì

1. `curl -sIL <threads share url>` để giải ra URL gốc dạng `threads.com/@user/post/<SHORTCODE>`.
2. `web_extract` URL gốc: **chỉ trả về main post + đếm view/like/reply/repost**. Phần reply bị
   login wall chặn → KHÔNG đủ để kết luận "mn chê".
3. Đọc reply thật bằng script có sẵn (nạp cookies `~/.hermes/threads_state.json`):
   ```bash
   "<hermes venv>/Scripts/python.exe" scripts/read_threads_replies.py "<post_url>" "C:/Users/NTQUANG_DELL/hermes-temp/threads_replies.json"
   ```
   Xem docstring script để biết pitfall python/venv + cách gọi khi terminal tool chặn lệnh.
4. Tách `items` thành **bài của tác giả** (dòng đầu = username mình) và **comment người khác**;
   đếm chars từng phần + trích số like mỗi phần và mỗi comment.

**Số phải có trong báo cáo:** views, like bài, số reply, số comment người ngoài, **like từng phần
của thread** (để thấy tương tác chết ở đâu), **like của từng comment chê** (để so với like bài).

## Bước 2 — Ba tầng chẩn đoán (đọc comment rồi mới gán tầng)

Không phải mọi lời chê là một loại. Phân vào 3 tầng, và đếm tỷ lệ comment rơi vào tầng nào:

1. **Tầng văn phong** — "dài dòng", "như tờ sớ", "văn Gemini", "không đọng lại gì". Dấu hiệu trong
   bản thân bài: nhiều phần liên tiếp toàn dữ liệu/nghiên cứu không có ví dụ đời thường chen vào;
   nhịp câu đều tăm tắp; mỗi phần kết bằng một câu chốt kiểu poster; các câu dẫn kiểu AI
   ("Giờ tới phần khiến mình phải ngồi lại", "Nghe vô lý, nhưng đó là cách não làm việc",
   "Bản thử nghiệm chí mạng nhất là năm..."). Người đọc không gọi tên được nhưng ngửi ra.
2. **Tầng lập luận** (đòn hiểm nhất với bài kể thất bại của chính mình) — tác giả kể một sự cố
   vận hành thật nhưng kết luận lại nghiêng về cơ chế tâm lý, thành ra đọc là *đang lấy khoa học
   để hợp lý hoá lỗi của mình và quy kết người đọc/khách hàng*. Comment điển hình: "kỹ năng viết
   thế này thảo nào mất khách hàng".
3. **Tầng đối tượng** — người đọc Threads phần lớn đứng ở ghế **khách/người mua**, bài lại đứng ở
   ghế **người bán** rồi phân tích đầu người mua → khách đọc thấy mình bị đem ra mổ xẻ.

Kèm **lỗ thủng kỹ thuật**: sự việc thật nhưng không có một con số nào (lỗi gì, chậm bao lâu, SLA,
thiệt hại bao nhiêu), trong khi bằng chứng đưa ra toàn nghiên cứu lĩnh vực khác (y khoa) áp sang
chuyện kinh doanh → người đọc kỹ soi được khoảng cách suy luận.

## Bước 3 — Phương án xử lý (đúng 3 phương án, nêu rõ mục tiêu)

- **A. 48 giờ đầu: im, KHÔNG xoá, KHÔNG đối đáp.** Mục tiêu: không đẩy comment chê lên top thêm
  lần nữa. Việc duy nhất nên làm là **ghim 1 reply nhận lỗi vận hành** để lấy lại khung câu chuyện
  mà không tranh luận. Chỉ trả lời 1 lần, 1 comment. Cấm dùng chữ "não", cấm nhắc lại lý thuyết,
  cấm "mình chỉ muốn chia sẻ".
  Mẫu: "Đúng. Khách đi vì mình xử lý chậm, không phải vì khách khó tính. Mình đã siết lại
  [SLA cụ thể] và bù [cụ thể]. Mình viết lại chuyện này để không lặp lại, không phải để giải thích
  tại sao khách đi."
- **B. Viết bản v2, KHÔNG xoá bản v1.** Mục tiêu: vá đúng chỗ bị đánh. Cắt số phần (14 → 5-6),
  cắt tổng chars khoảng 1/2-1/3, đảo kết luận lên 2 phần đầu thành nhận trách nhiệm của mình,
  giữ đúng 1-2 bằng chứng mạnh nhất, mỗi phần lý thuyết phải kèm một con số hoặc một hành động,
  bỏ hết câu dẫn kiểu AI, kết bằng câu hỏi **cho người đọc** (không tự hỏi mình).
- **C. Tách thành 2 bài** (bài kiến thức thuần + bài quy trình/hệ thống của doanh nghiệp có số đo).
  Chỉ chạy sau khi A/B đã lắng 3-5 ngày, đừng đăng chồng.

Cuối báo cáo luôn hỏi user **dữ liệu còn thiếu để viết v2 cho đúng** (lỗi gì, chậm bao lâu so với
cam kết). Không có số thật thì bản v2 lại thành lý thuyết và bị chê y hệt.

## Case tham chiếu — 2026-10-19, post `DerUNeQgXe9` (peak-end rule)

Số liệu: 32.5K views, 57 like bài, 19 reply (13 là reply của chính tác giả), **6 comment người
ngoài, tổng 83 like**. Like từng phần: P1 **57** → P2 7 → P3 3 → P4 1 → P5 2 → P8 2 → P11 2 →
P14 3 → tương tác **chết từ phần 3** (11 phần còn lại gần như không ai chạm).
Ba comment chê nặng nhất: 34 + 30 + 18 = **82 like, hơn cả 57 like của bài**.

Nội dung chê: (a) "Lè nhà lè nhè, viết dài dòng như tờ sớ, 'đội support xử lý chậm' là khách hàng
100 năm cũng cút" (34); (b) "Kỹ năng viết thế này thảo nào mất khách hàng" (30); (c) "Kể dài dòng
như văn Gemini mà không đọng lại được gì" (18); (d) hỏi thẳng SLA/bao lâu là nhanh (1);
(e) "người ta không đòi bồi thường còn lên mạng lè nhà lè nhè"; (f) "Dài dòng thật".

Chẩn đoán: 4/6 comment vào tầng văn phong (P3→P6 là 4 phần liên tiếp toàn nghiên cứu, không có ví
dụ đời thường chen vào), 2/6 vào tầng lập luận + đối tượng. Lỗ thủng kỹ thuật: không có một con số
nào cho sự cố thật; bằng chứng toàn thí nghiệm y khoa (nước lạnh 1993, nội soi Redelmeier 1996,
682 bệnh nhân 2003) áp sang chuyện khách rời bỏ.

## Cổng chặn TRƯỚC khi đăng (áp cho mọi bài kể thất bại của chính mình)

Trả lời 3 câu, sai một câu là viết lại:

1. Kết luận **nghiêng về trách nhiệm của mình** hay đang nghiêng về cơ chế bên ngoài / quy kết
   người đọc? (phải nghiêng về mình, và phải nằm ở **đầu bài**, không phải phần 11)
2. Có **con số thật** cho sự việc không (thời gian, tỷ lệ, thiệt hại, cam kết)?
3. Câu kết **hỏi người đọc** hay tự hỏi chính mình?

Đây là lỗi hệ thống của loại bài "tôi thất bại rồi rút ra quy luật", không phải lỗi một bài.
