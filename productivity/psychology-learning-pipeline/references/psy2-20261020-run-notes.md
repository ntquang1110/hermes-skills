# Run notes — psy_2 (slot 10:00) — 2026-10-20 — "Mindfulness và sống trong hiện tại"

## Đường dẫn thật của lượt chạy
- Chủ đề: `D:/Hermes Proj/psy/topics_today.txt`, dòng bắt đầu `2.` → "Mindfulness và sống trong hiện tại".
- Article (nguồn KFlow): `D:/Hermes Proj/psy/drafts/psy_2.txt`
- Thread (CHỜ DUYỆT, tuyệt đối không vào `threads_approved/`): `D:/Hermes Proj/psy/threads_drafts/psy_2_thread.txt`
- Template giọng: `D:/Hermes Proj/psy/threads_template_v2.txt` (mẫu chuẩn psy_6, mình/anh).

## Số đo chốt (đọc để biết target thực tế)
- Article: **446 từ**, 5 nhãn TÊN TRẦN (`Ví dụ` / `Nêu vấn đề` / `Vấn đề gốc rễ` / `First principle` / `Giải pháp`), 0 forbidden.
  - Trim path: bản đầu **500 từ** (vượt 50) → 454 → 446. Chỉ cần 2 lượt: 1 `patch mode=replace` bỏ 1 mệnh đề thừa ở First principle + 1 clause ở Giải pháp. Không phải viết lại cả file.
- Thread: **3 post**, lengths `426 / 406 / 333`, total 1170, diacritics 248 → PASS.
  - Nhịp chuẩn cho bài giảng-nhẹ: post 1 = ví dụ + nêu vấn đề (≈430), post 2 = gốc rễ + cơ chế (≈410), post 3 = 3 việc + câu chốt (≈330).
- Charset: 0 non-Latin, 0 em/en dash, 0 arrow, 0 emoji.

## Ngách cơ chế đã dùng (lần sau PHẢI đổi, chủ đề này đã quay lại ≥3 lần)
- DMN (mạng chế độ mặc định, hạch đai sau + vỏ não trán trong bụng) bật → hạch hạnh nhân bật → trục hạ đồi - tuyến thượng thận tiết cortisol cho mối đe dọa tưởng tượng.
- Vỏ não trước trán bên ức chế DMN; vỏ não đảo (insula) đọc tín hiệu nội tại (hơi thở, hơi nóng, sức nặng bàn chân).
- Thở ra dài hơn hít vào → dây phế vị → nhánh đối giao cảm → hạ nhịp tim, hạ cortisol.
- Ngách đã CHÁY cho chủ đề này: bản 2026-10-04 dùng vụn chú ý (Sophie Leroy 2009) + dopamine prediction error + cortisol (Ulrich, Irle & Davidson 2004) + Mark, Gudith & Klocke 2008 (23 phút). Bản 2026-09-23 dùng ngách khác. Lần tới đi: interoception (Craig), body scan, default mode vs task-positive network, hoặc mindful eating theo cơ chế vị giác.

## Lỗi đã tái phạm trong lượt này (đọc để không lặp lần 9)
1. **Thread viết 5 block cách dòng trống → `posts=5`.** Luật cũ vẫn đúng: TRONG post dùng MỘT `\n` (dòng đơn), GIỮA post mới dùng dòng trống `\n\n`. Viết thẳng 3 block liền ngay từ bản đầu.
2. **Không gọi `verify_psy_plainname.py`, tự chế check `python -c` inline.** Lệnh ngắn (không string dài, không regex nặng) lượt này chạy được qua `terminal`, nhưng vẫn là cái skill cấm — gọi script có sẵn ở skill dir là 1 lệnh duy nhất và in `RESULT PASS|FAIL`.

## Cảnh báo MỚI — job song song ghi cùng file thread
`write_file` vào `threads_drafts/psy_2_thread.txt` trả `_warning: was modified by sibling subagent ... but this agent never read it`. Tên bản thread là CỐ ĐỊNH (`psy_N_thread.txt`), nên khi 2 slot/job cùng chạy sẽ đè lên nhau (last-writer-wins). Xử lý:
- Sau `write_file`, đọc lại file một lần để chắc nội dung là bản của mình trước khi verify.
- Khi trả bài cho Quang, NÊU RÕ tên file trùng giữa `threads_drafts/` và bản cũ cùng tên trong `threads_approved/` (lượt này approved còn `psy_2_thread.txt` từ 28/08) để anh không lẫn bản cũ với bản mới.
