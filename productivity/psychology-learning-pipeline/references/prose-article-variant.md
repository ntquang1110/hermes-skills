# Format variant thứ tư — bài "số trên tổng" viết PROSE không nhãn

Gặp lần đầu 2026-09-29 (bài 2/4 và 3/4). Một cron riêng yêu cầu bài tâm lý dạng prose
liên tục, KHÔNG nhãn phần, KHÔNG giới hạn từ. Đây là format thứ tư, khác:
- v3 (Case → 3 lớp cơ chế → kịch bản lời thoại → gốc rẻ)
- 5-phần first-principles (`1. Ví dụ` … `5. Giải pháp`, ≤450 từ, file `D:/Hermes Proj/psy/drafts/psy_N.txt`)
- bản thread (post ≤500 ký tự, `threads_drafts/`)

Output của variant này: `~/drafts/bai-<N>-4-<slug>.md` (máy Quang, KHÔNG phải D:/).

## KHÔNG dùng verify_psy_outputs.py cho bài này

Script đó đòi labels `^[1-5]\. ` và words ≤450. Bài prose không có nhãn nên **luôn FAIL**,
và cũng không có ý nghĩa khi bài dài 3.000-4.000 ký tự. Dùng script riêng bên dưới.

## Cấu trúc 4 phần — mỗi phần là 1-3 đoạn văn liền, KHÔNG viết header

1. **Mở đầu = ĐÚNG 2 câu.** Gây tò mò bằng hành vi quen thuộc hoặc câu chốt ngược đời.
   KHÔNG hỏi (`?`) ở mở đầu — câu hỏi dành cho dòng kết.
   VD bài 3/4: "Bạn đóng laptop, đứng dậy rót cà phê, và não bạn thì không đóng theo. Ai hỏi bạn
   đang nghĩ gì, câu trả lời đúng là bạn không nghĩ gì cả, trong khi chương trình cũ vẫn chạy nền."
2. **Cơ chế** — khái niệm khoa học + tác giả + năm, giải thích VÌ sao não làm vậy.
   Đoạn dài nhất của bài.
3. **Hệ quả thực tế** — chuyện người đọc sẽ gặp, kèm nghiên cứu định lượng.
   NÊN có một chỗ lật ngược lời đồn phổ biến. Bài 3/4 đảo "gián đoạn mất 23 phút" bằng
   phát hiện Mark, Gudith & Klocke 2008: làm xong NHANH HƠN, chất lượng không giảm, cái trả
   bằng là stress (đúng tên bài: "more speed and stress"). Chỗ lật ngược làm bài có trọng lượng
   hơn hẳn phần liệt kê liên tục.
4. **Kết luận** — khoảng 2 đoạn: 1 đoạn rút bài học + 1 đoạn kết bằng CÂU HỎI cụ thể.
   KHÔNG "tóm lại". KHÔNG mở đầu kiểu "vậy câu hỏi là".

## 🔴 BẮT BUỘC CHỨA GIẢI PHÁP

Yêu cầu đứng từ 2026-09-17 (Quang phản biện bài David Epstein: "không gợi ý giải pháp gì à").
Áp cho MỌI bài tâm lý kể cả bài prose này. Bài 3/4 có đoạn riêng "Giải pháp không cần tập
trung tốt hơn, cần buông đúng lúc" + 1 đoạn áp dụng cụ thể. Phần cơ chế và hệ quả không thay
thế được phần này.

## Giọng variant này = "bạn" (độc giả), KHÔNG phải mình/anh

Luật mình/anh trong SKILL.md viết cho bài 5-phần + thread, KHÔNG áp cho series này.
Quy tắc thực dụng: **đọc lại bài anh vừa viết trong cùng thư mục (`ls -t ~/drafts`) và bắt
chước xưng hô của nó.** Bài 2/4 (choice overload) dùng "bạn" xuyên suốt không có "mình"/"anh";
bài 3/4 viết "bạn" cho khớp. Dùng mình/anh vào series này sẽ lệch giọng, anh sẽ thấy không
liền.

## Độ dài: 3.000-7.000 ký tự

Bài 2/4 = 3.022, bài 3/4 = 3.789. Dưới 3.000 là cụt, trên 7.000 là dài dòng — Quang đọc nhanh.
Mục tiêu dễ đạt nhất: 3.500-4.500.

## Verify

```
python <skill_dir>/scripts/verify_prose_article.py <path>
```

Exit 0 = pass. BẢN CHẠY Ở SKILL DIR:
`C:\Users\NTQUANG_DELL\AppData\Local\hermes\skills\productivity\psychology-learning-pipeline\scripts\verify_prose_article.py`
KHÔNG copy sang `D:/` (pattern gap đã gặp với `verify_thread_draft.py` và
`verify_psy_outputs.py` — file bị liệt kê trong skill nhưng không tồn tại trên D:/).

Script check: 0 em dash, 0 en dash, 0 arrow, 0 bold, 0 markdown heading, 0 nhãn Tầng/Lớp,
0 curly quote, 0 emoji, 0 CJK, 0 codepoint >0x1EF9, dấu tiếng Việt ≥300, 6-14 đoạn,
mở đầu ĐÚNG 2 câu, 0 AI vocab, 0 signposting, 0 negative parallelism, 0 tail negation,
chars trong khoảng, biến thiên chiều dài câu >80.

`execute_code` BỊ CHẶN trong cron mode → verify phải chạy file `.py` qua `terminal`.
Xem mục Pitfalls trong SKILL.md về `python -c` inline bị giữ approval.

## ⚠️ PITFALL — checker regex báo "digit_spelled" giả (2026-09-29)

Regex `[a-zA-Zà-ợ]{3,}\s*\d` bắt cả "năm 1927", "2.473", "0,382" (số đứng sau từ) — tức mọi
số trong bài đều "fail". Số dùng chữ số là ĐÚNG yêu cầu của Quang (memory: "số dùng chữ số
(1,2,3) không viết chữ"). Regex này chỉ có nghĩa khi bắt CHỮ SỐ thay số (một/hai/ba) —
cái đó scan bằng word-list tiếng Việt, đừng dùng regex digit. Đã bỏ khỏi script, đừng thêm lại.

## ⚠️ PITFALL — humanizer tail-negation lọt qua lần viết đầu (2026-09-29)

Cụm gốc: "Một phút có chủ đích, không phải một phút lướt điện thoại." → tailing negation
(humanizer pattern 34) + negative parallelism. Checker bắt được nhưng phải SỬA TAY,
không auto-fix được (đòi thêm nội dung để câu đứng vững).

Cách sửa giữ nhịp:
- Tách thành 2 vế có nội dung: "Một phút đi lại trong nhà cũng được, miễn là không phải một
  phút lướt điện thoại."
- "Vậy cái X không phải A, mà là B" → bỏ vế "Vậy cái", để mệnh đề đứng một mình:
  "Thứ kéo ta về việc dở không phải ký ức."
Không dùng cách xoá hẳn vế sau (làm câu cụt), cũng không thay bằng dấu gạch.

## Chống trùng chủ đề trước khi chọn đề tài

1. Đọc `~/drafts/bai-*.md` — bài trước trong cùng series.
2. Quét title trong `youtube-schedule.json` (hàng trăm bài Threads đã/đang đăng) ở
   `~/AppData/Local/hermes/cache/`, cạnh `auto_post_log.txt`:
```
cd ~/AppData/Local/hermes/cache && python -c "import json;d=json.load(open('youtube-schedule.json',encoding='utf-8'));[print(i.get('status'),'|',str(i.get('title'))[:90]) for i in d['queue']]"
```
Bài 3/4 chọn attention residue sau khi grep thấy 0 hit "residue/Zeigarnik/task switch" trong
cả hai nguồn. Cũng nên check cả `references/topic-mechanism-swaps.md` (ngân hàng tác giả đã
dùng) để tránh dùng lại cặp cơ chế.

## Verify citation bằng API, không đoán

Bài 3/4 verify 6 nguồn qua Crossref + Semantic Scholar + PubMed (không cần ScienceDirect —
bị captcha). Xem `web-research/references/scientific-literature-retrieval.md` cho PubMed
eutils, và mẹo Semantic Scholar `tldr` + trường `abstract` khi publisher chặn (dùng
`/graph/v1/paper/DOI:<doi>?fields=title,abstract,year,venue,tldr,citationCount`).
Metadata (tên tác giả, năm, tập/số/trang, DOI) lấy từ
`api.crossref.org/works?query.bibliographic=...` — luôn chạy trước khi viết tên vào bài.
