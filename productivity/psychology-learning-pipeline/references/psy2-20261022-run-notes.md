# Run notes — psy_2 2026-10-22 "Giấc ngủ và ảnh hưởng lên tâm trí"

Slot 2 (cron 10:00), 2-deliverable: bài 5 phần (`drafts/psy_2.txt`) + bản thread chờ duyệt (`threads_drafts/psy_2_thread.txt`).
Tên file giữ ĐÚNG như prompt ghi (không ngày), không đổi sang `psy_2_YYYYMMDD_slug.txt`.

## Số đo (đo bằng checker TỰ CHẾ — không phải `verify_psy_plainname.py`, xem mục Sai lầm)

```
ARTICLE D:/Hermes Proj/psy/drafts/psy_2.txt | labels=5 | words=446 | diacritics=422 | forbidden=none
THREAD  D:/Hermes Proj/psy/threads_drafts/psy_2_thread.txt | posts=7 | lengths=[128, 38, 107, 193, 258, 270, 64] | total=1071 | diacritics=218 | forbidden=none
```

Nhãn dùng: tên trần, mỗi nhãn 1 dòng riêng — `Ví dụ` / `Nêu vấn đề` / `Vấn đề gốc rễ` / `First principle` / `Giải pháp`.

## Sai lầm của lượt này (2 lỗi, cả 2 đã có luật sẵn trong skill)

1. **Không load skill ở lượt đầu.** Đi thẳng vào `topics_today.txt` + `threads_template_v2.txt`. Hệ quả trực tiếp là cả 2 lỗi dưới.
2. **Thread 7 block = 7 post** (prompt ghi 2-3 post). Lý do sai: đọc `threads_approved/psy_2_thread.txt` (bản 28/08) thấy nhiều đoạn cách dòng trống → tưởng là chuẩn. Prompt cron thắng file mẫu.
3. **3 lần tự chế checker** thay vì 1 lệnh `verify_psy_plainname.py`: `psy/scripts/_verify_psy2.py` (trong PROJECT DIR), rồi `%TEMP%/hermes-verify-psy2.py`, rồi `%TEMP%/hermes-verify-psy2-py`. Lệnh đúng có sẵn, không cần đoán tham số.

## Chưa làm: grep chống lặp chủ đề/ngách

Chủ đề "Giấc ngủ và ảnh hưởng lên tâm trí" ĐÃ chạy trước đó ở slot 1 ngày 2026-10-14. Lượt này KHÔNG chạy `grep -ril "giấc ngủ" drafts/ threads_drafts/ threads_approved/` để xem bản cũ dùng ngách nào → rủi ro lặp ngách cơ chế. Lần sau, trước khi viết: grep chủ đề + đọc bản cũ + chọn cặp cơ chế CHƯA dùng.

**Ngách cơ chế lượt 2026-10-22 dùng (đánh dấu là đã cháy):** REM là giai đoạn chưng cất ký ức cảm xúc, trong REM noradrenaline xuống gần bằng không → não tái mã hóa ký ức đau trong trạng thái sạch chất căng thẳng; thiếu ngủ làm lệch cặp amygdala–PFC (amygdala phản ứng mạnh hơn, PFC tụt lại); hai hệ điều khiển giấc ngủ = nhân trên giao thoa thị giác (suprachiasmatic nucleus, đo ánh sáng → melatonin) + áp lực ngủ do adenosine tích tụ, caffeine phong bế thụ thể adenosine.

Ngách CHƯA dùng cho chủ đề này (lần tới nếu chủ đề quay lại): vệ sinh glymphatic (dọn chất thải trong não lúc ngủ sâu sóng chậm), trục HPA và cortisol awakening response, phân mảnh giấc ngủ do rượu (cắt REM mà không cắt tổng thời lượng), mất đồng bộ nhịp sinh học xã hội (social jetlag), hiệu ứng hồi phục giấc ngủ sau một đêm thiếu ngủ ở người chấm điểm/đàm phán.

## Trình tự nên lặp lại

1. `skill_view(psychology-learning-pipeline)` (+ `humanizer` nếu là bài đăng) ở LƯỢT ĐẦU.
2. 2 `read_file` song song: `topics_today.txt` (dòng `2.`) và `threads_template_v2.txt`.
3. `grep -ril "<từ khóa chủ đề>" drafts/ threads_drafts/ threads_approved/` → chọn ngách cơ chế chưa dùng.
4. `write_file` bài 5 phần (nhắm 420-440 từ) → `write_file` thread **3 block** → 1 lệnh verify `verify_psy_plainname.py` cả 2 file.
5. Đọc `posts=N`; `N` phải = 2-3 (không có block ngắn 30-70 ký tự).
6. Trả chat: cả 2 bản + 2 dòng duyệt. KHÔNG ghi vào `threads_approved/`.

## Cảnh báo job song song (tái hiện)

`write_file` vào `threads_drafts/psy_2_thread.txt` trả cảnh báo "modified by sibling subagent ... but this agent never read it". Xử lý đúng đã dùng: đọc lại file trên disk sau khi ghi + verify trên bản disk trước khi dán vào chat. Kiểm `threads_approved/psy_2_thread.txt` có TRÙNG nội dung với bản mới không (lượt này KHÁC → là bản cũ chu kỳ trước, nêu rõ cho Quang để không lẫn khi duyệt).
