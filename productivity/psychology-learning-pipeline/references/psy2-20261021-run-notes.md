# Run notes — psy_2 2026-10-21 "Sự cô đơn của người lãnh đạo"

Slot 2 (cron 10:00), 2-deliverable: bài 5 phần + bản thread chờ duyệt.

## Kết quả đo (script đóng gói, không checker tự chế)

```
ARTICLE D:/Hermes Proj/psy/drafts/psy_2.txt | labels=5 | words=417 | diacritics=416 | forbidden=none
THREAD  D:/Hermes Proj/psy/threads_drafts/psy_2_thread.txt | posts=3 | lengths=[283, 477, 486] | total=1246 | diacritics=274 | forbidden=none
RESULT: PASS
```

Lượt chạy sạch: 2 `write_file` (bài + thread) + 2 `patch` cắt ký tự + 3 lệnh `terminal`. Không viết checker tay, không `execute_code`.

## Trình tự đã dùng (đáng lặp lại)

1. `skill_view(psychology-learning-pipeline)` + `skill_view(humanizer)` ở lượt đầu.
2. Đọc `topics_today.txt` (dòng `2.` = chủ đề) và `threads_template_v2.txt` trong 2 read_file song song.
3. `grep -ril "cô đơn" drafts/ threads_drafts/ threads_approved/` → phát hiện bản cùng chủ đề `drafts/review/psy_1_20261003_con-lon-cua-nguoi-lanh-dao.txt` (4 phần, Kahneman & Miller 2000 + Xu/Toney/Roberts 2014) và bản đã duyệt `threads_approved/codon-o-dinh.txt` (psy_6, amygdala/PFC/cortisol + Coan social baseline).
4. Chọn ngách CHƯA cháy: quyền lực làm mờ việc đọc người khác + não ghi tách nhóm bằng vùng đau.
5. `write_file` bài 5 phần (nhãn tên trần) → `write_file` thread 3 block → `sed -i 's/\r$//'` cả 2 → 1 lệnh verify cả 2 file.
6. Post 3 = 504 ký tự → `patch mode=replace` bỏ 1 phụ từ → `sed` lại (patch ghi lại CRLF) → verify → PASS.
7. Kiểm chống ghi nhầm `threads_approved/`: so NỘI DUNG với `threads_approved/psy_2_thread.txt` (bản cũ 28/08 cùng tên) → khác → đúng, và báo Quang biết có file trùng tên cũ nằm trong thư mục duyệt.

## Tên file (prompt thắng quy ước)

Prompt ghi `drafts/psy_2.txt` (không ngày) và `threads_drafts/psy_2_thread.txt` (cố định). Giữ đúng như prompt, không "sửa" sang `psy_2_YYYYMMDD_slug.txt`.

## Xác minh tác giả bằng Crossref — 1 lệnh cho 5 tên

```bash
for q in "Power and perspectives not taken Galinsky Magee Inesi Gruenfeld" \
         "Power changes how the brain responds to others Hogeveen Inzlicht Obhi" \
         "Does rejection hurt fMRI study of social exclusion Eisenberger Lieberman Williams" \
         "Power approach and inhibition Keltner Gruenfeld Anderson" \
         "Loneliness matters a theoretical and empirical review of consequences and mechanisms Hawkley Cacioppo"; do
  echo "--- $q"
  curl -s -G "https://api.crossref.org/works" \
    --data-urlencode "query.bibliographic=$q" \
    --data "rows=2&select=title,container-title,issued,author" | head -c 900; echo
done
```

Kết quả khớp (dùng để ghi tên trong bài):

| Tác giả | Năm | Tạp chí | Tựa |
|---|---|---|---|
| Galinsky, Magee, Inesi, Gruenfeld | 2006 | Psychological Science | Power and Perspectives Not Taken |
| Hogeveen, Inzlicht, Obhi | 2014 | Journal of Experimental Psychology: General | Power changes how the brain responds to others |
| Eisenberger, Lieberman, Williams | 2003 | Science | Does Rejection Hurt? An fMRI Study of Social Exclusion |
| Keltner, Gruenfeld, Anderson | 2003 | Psychological Review | Power, approach, and inhibition |
| Hawkley, Cacioppo | 2010 | Annals of Behavioral Medicine | Loneliness Matters: A Theoretical and Empirical Review of Consequences and Mechanisms |

Ghi thẳng tên họ trong bài, KHÔNG cần tên bài/tạp chí; nhưng tra trước để chắc tên tồn tại đúng cặp và đúng năm.

## Câu bị cắt khi trim thread (dải 490-500)

- `Ghế càng cao thì dây nối càng mỏng. Mình phải tự nối lại…` → bỏ "Mình" (-5 ký tự).
- `…rồi mới chốt. Cách này phá thế neo vào đầu mình.` → "Phá thế neo vào đầu mình." (-5).
- `…nói thẳng: tuần này mình cô đơn ở chỗ nào.` → "ở đâu." (-3).

Tổng -13 ký tự, từ 504 xuống 486, mỗi lần cắt vẫn kết ở câu hoàn chỉnh (gate đòi ký tự cuối là `.`, `!`, `?`).
