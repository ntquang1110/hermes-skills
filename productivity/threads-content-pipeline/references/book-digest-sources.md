# Book-digest sources (kênh review sách tiếng Việt)

Khi user gửi link từ kênh **review/diễn giải sách** (vd ABooks, PsychToons, và các kênh "tóm tắt sách" khác), transcript là
bản **tiếng Việt** của một cuốn ngoại văn. Tiêu đề video hiếm khi nêu tên tác giả, và transcript là lời kể ngôi thứ nhất
do người dẫn chuyện đọc lại sách. Việc BẮT BUỘC trước khi viết draft: xác định SÁCH GỐC.

Lý do: rule "VERIFY NGUỒN GỐC VIDEO" — nhận sai nguồn hoặc bịa tên tác giả làm mất uy tín cả bài. Đồng thời transcript
ASR bóp méo tên riêng rất nặng (xem case bên dưới), nên phải đối chiếu nguồn ngoài.

## Case đã xử lý: `3uCBSauM-P8` (ABooks, 2026-10-07)

| Thứ | Giá trị |
|---|---|
| Tiêu đề video | "Phương Pháp Socrates: Cách Rèn Luyện Tư Duy Phản Biện & Logic" |
| Kênh | ABooks (@ABookschannel) |
| Sách gốc | *The Socratic Way of Questioning: How To Use Socrates' Method To Discover The Truth And Argue Wisely* |
| Bộ | Critical Thinking & Logic Mastery |
| Tác giả | **Thinknetic** (nhóm biên soạn / collective authorship) |
| Transcript | 28.246 chars, 761 segments, tiếng Việt |

### Cách tìm ra (thứ tự đã chạy đúng)

1. **Lấy description bằng yt-dlp** — không cần transcript, rẻ và nhanh:
   ```bash
   python -m yt_dlp --skip-download --print "%(title)s|||%(uploader)s|||%(upload_date)s|||%(description)s" "URL"
   ```
   Description của ABooks liệt kê sẵn dàn ý video và **nêu thẳng tên nhân vật gốc**: "Bi kịch 'Lái tự động': Cái chết
   của Dave". Transcript ASR chỉ nghe ra "Đếp"/"Grass"/"Brad" → description là nguồn xác nhận tên chuẩn (**Dave**).
   (yt-dlp có thể warning "No supported JavaScript runtime" — warning này vô hại, metadata vẫn ra.)

2. **Dịch tiêu đề Việt → Anh rồi web_search khớp tựa sách.** Khớp chính xác nhờ bộ đề "Critical Thinking & Logic
   Mastery" xuất hiện trong kết quả tìm kiếm (Scribd, bargainbooksy, readnrate đều liệt kê
   "The Socratic Way Of Questioning … (Critical Thinking & Logic Mastery) by Thinknetic").

3. **Xác nhận chương/khái niệm khớp** giữa transcript và sách trước khi kết luận: transcript có "Phương pháp Socrates
   là nền tảng", "kinh nghiệm truyền miệng", "khao khát sự thật / cởi mở / sáng suốt" — khớp mục lục bộ sách.

### Bài học về attribution

- **Thinknetic = nhóm biên soạn**, không phải một người. Nhiều sách của Thinknetic mở đầu bằng một câu chuyện cá nhân
  ngôi thứ nhất do ghostwriter dựng. KHÔNG suy ra tên tác giả cá nhân từ "tôi" trong transcript.
- Cách viết an toàn đã dùng: "Dave là anh trai của **người viết cuốn sách này**"; "**tác giả** kể lý do sâu thẳm nhất…".
- Trong reply duyệt vẫn nêu tên sách + bộ + nhóm tác giả để user biết nguồn thật.

## ASR bóp méo tên riêng trong transcript tiếng Việt — bảng đối chiếu case này

Transcript tiếng Việt do auto-caption sinh ra sai rất nhiều tên riêng nước ngoài. Phải sửa trước khi đưa vào draft:

| ASR nghe ra | Đúng |
|---|---|
| Gostp / Flab | Gustave Flaubert |
| Luis Scet | Louise Colet |
| Scress / Socr / Scress | Socrates |
| Athons | Athens |
| Van Gốc | Van Gogh |
| Savad Dali | Salvador Dalí |
| Đếp | Dave |
| Grass | Brad |
| Cly / Cle | Cly |
| Zimbabe / Nam Zodesia | Zimbabwe / Nam Rhodesia |
| khuôn mẫu "giác" (bãi biển) | rác |

Nguyên tắc: tên người/tổ chức lấy từ transcript ASR **phải verify bằng web_search** hoặc bằng description/nội dung sách;
không verify được thì bỏ tên, dùng chức danh.

## Checklist rút gọn trước khi viết draft từ nguồn sách

- [ ] yt-dlp description → tên nhân vật/sự kiện gốc
- [ ] web_search khớp tiêu đề Việt ↔ tựa sách Anh (dùng cả tên bộ nếu có)
- [ ] Xác định tác giả là cá nhân hay nhóm biên soạn
- [ ] Đối chiếu toàn bộ tên riêng trong transcript với bảng trên + web_search
- [ ] Báo user nguồn thật trong reply duyệt
- [ ] Ngân sách cắt TỪ ĐẦU (sách nhiều chuyện → draft tự nhiên 9-10K, vượt ngưỡng 3-7K)
