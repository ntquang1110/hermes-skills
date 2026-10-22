# Dedup context-scan: ngưỡng chuỗi KHÔNG đủ + kỷ luật mutation (15/10/2026)

## 1. Phát hiện: similarity threshold không tách được trùng thật

Đo 15/10 trên 24 draft context-scan đang mở (#43-66, 6 thế hệ):

| Phương pháp | Script | Kết quả |
|---|---|---|
| `seq(title) >= 0.62` (đúng như spec PA-A) | `docs/qa/measure_dedup_active.py` | 13 nhóm |
| Nhóm theo CHỦ ĐỀ (map từ khoá) | `docs/qa/dedup_topic_map.py` | **8 nhóm** |

4 cặp **cùng 1 việc** mà ngưỡng 0.62 bỏ sót:
`#63~#43 = 0.604` · `#64~#44 = 0.565` · `#65~#46 = 0.579` · `#66~#45 = 0.301`.

Cặp thấp nhất gom được = 0.625 (#56~#60), cặp cao nhất không gom được = 0.604 (#43~#63)
→ **khe hở 0.021 và CẢ HAI ĐẦU đều là trùng thật ⇒ không tồn tại ngưỡng nào tách đúng.**

**Kết luận áp dụng:** chặn trùng phải theo **chủ đề** (chuẩn hoá title → bộ khoá chủ đề), ngưỡng chuỗi chỉ là lớp phụ trong cùng chủ đề. LLM diễn đạt lại tự do nên cùng một việc có thể rơi xuống sim 0.30.

## 2. Thế hệ trùng tái sinh thế nào (đừng chẩn "loop vô hạn")

`context_scan_push.py` cổng bằng `sha256(brief)`; brief dựng từ **workspace user** (`tfo_data/users/<email>/`), KHÔNG phải `store/tasks.json`. Nên:
- Thêm task vào `store/tasks.json` **không** làm brief đổi → không tự nuôi vòng lặp.
- Chỉ khi data user đổi (meeting/task/project) mới gọi LLM. Nếu lúc đó chain LLM chết → `json.dump(state)` không chạy → **hash tồn đọng**; chain sống lại là bản scan chạy ngay.
- Ca thật: chain nối lại 14/10 09:19 → scan tồn đọng chạy **14/10 11:42** → sinh #63-66. Bằng chứng: `~/context_scan_push_log.json` → `last = {source: 2026-10-14 11:42:11, count: 3}` + `created_at` của task.

## 3. Backfill `done_criteria` cho thế hệ mới: copy từ task CÙNG CHỦ ĐỀ

`docs/qa/backfill_dc_2026-10-15.py` — copy tiêu chí của task chuẩn cùng chủ đề (không tự nghĩ tiêu chí mới), assert **không bump `updated_at`** + chỉ 4 task mục tiêu bị sửa + STALE giữ nguyên. Verify: 13 assertion PASS, guard NO_DC 4→0 mà STALE vẫn 21.

## 4. ⚠️ Mutation phải nhắm ĐÚNG mục tiêu (đã dính)

M2 đầu tiên bump `updated_at` của **#63** để kỳ vọng STALE 21→20 → **FAIL** vì #63 mới tạo 14/10, CHƯA nằm trong STALE. Mutation nhắm task không thuộc tập đo = mutation vô nghĩa (tưởng verify yếu). **Phải nhắm task ĐANG stale thật (#47)** thì mới chứng minh được "bump = che STALE".

## 5. ⚠️ Test rot: mutation script hardcode kỳ vọng

`mutation_dedup_active.py` cũ hardcode "20 task → 11 việc" → khi lô trùng lớn lên (24 task/13 việc) nó tự FAIL, trông như "repo sai". Đã viết lại: **derive kỳ vọng từ chính lần đo baseline** (`parse()` output của script đo), thêm M3 chứng minh 4 cặp trùng thật < 0.62. Nguyên tắc: mutation test không được chứa số cứng của dữ liệu.

## 6. ⚠️ Line-ending: detect trước khi ghi đè file văn bản

`briefing.md` = CRLF, `shared/spec-dedup-context-scan-2026-10.md` = **LF**. `assert "\r\n" in raw` làm script append chết. Luôn `NL = "\r\n" if "\r\n" in raw else "\n"` rồi mới ghi. Anchor patch đa dòng trên file CRLF cũng fail → dùng **anchor 1 dòng** hoặc python replace.

## 7. Chân OpenRouter free tier: hạ `max_tokens` KHÔNG cứu được

`docs/qa/probe_openrouter_max_tokens.py` (đo 2 lượt 15/10): `/api/v1/credits` = `total_credits 0`, `total_usage 0.1999`; `max_tokens` 2000/1000/512/256/128 → **402 toàn bộ** (1 lần 128 trả 200 nhưng **content rỗng** = không dùng được). Message 402 ghi "can only afford 9 tokens". ⇒ không có tham số nào cứu; phải nạp credit / cấp lại key Ark. Khi standup 5/5 báo cáo mà log toàn `[OK] Gemini fallback` ⇒ **công ty đang chạy bằng 1 chân free tier**, đừng báo "chain ổn".
