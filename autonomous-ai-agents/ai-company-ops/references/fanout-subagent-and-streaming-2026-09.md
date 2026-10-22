# Triển khai toàn bộ plan nhiều hướng qua fan-out subagent (verify 03/09)

Khi Quang duyệt plan lớn nhiều hướng ("xịt khai toàn bộ", "làm hết, chia subagent"),
đây là pattern đã chạy thật và verify.

## Fan-out
- `delegate_task` batch, mỗi subagent 1 hướng SONG SONG (tối đa `max_concurrent_children`).
- Chỉ fan-out các hướng KHÔNG đụng file nhau. 03/09: H2 (app/main.py + index.html +
  context_scan) và H3 (chỉ thêm scripts/hub mới) → an toàn song song. Nếu 2 hướng sửa
  cùng file → serialize, đừng fan-out.
- Context của con PHẢI self-contained (con không thấy lịch sử chat): venv path đúng,
  pitfall guard terminal (path space "Hermes Proj"/uvicorn bị chặn → execute_code +
  subprocess), nơi có GROQ_/OPENCODE_/TELEGRAM key (~/AppData/Local/hermes/.env),
  git rule (store/*.json gitignored, chỉ `git add` code), ổ D policy, verify-bằng-chứng,
  ngôn ngữ, deadline ưu tiên nào trước. Xem lời dispatch trong session 03/09 làm mẫu.

## Hội tụ — KHÔNG tin lời subagent "xong" (self-report = chưa chứng thực)
Verify ngoài người gỡ, đây là thứ thực tế dính 03/09:
1. `git status --short` — subagent hay để dở file modified chưa push. Thực tế: H2 C3
   endpoint code xong nhưng `app/main.py` + `server.py` còn `M` chưa commit, chưa restart
   server, chưa có nút frontend. Tự hoàn tất phần dở, không coi là xong.
2. `git log --oneline` dose cúi — mỗi claim commit phải có hash thật trên git log.
3. **Endpoint mới trả 404/405 = server đang chạy code CŨ.** Subagent sửa file nhưng không
   restart: approve endpoint 8100 trả 404, 8090 trả 405 (server.py chưa load). Restart:
   kill PID port 8100 → watchdog_8100 (L1 cron every 1m) TỰ dậy code mới sau ~1.6s, hoặc
   chạy `python hub/watchdog_8100.py` 1 lượt nếu muốn nạp ngay.
4. Cron do subagent tạo → `cronjob action=list` verify, không tin "đã đăng ký". 03/09:
   3 cron H3 (f7472b8f65de watchdog 8100, 52d54c138bee uptime probe, f474aeee7e71 backup)
   verify có trong list + `last_status: ok` + enabled.

## Tự hoàn tất phần dở (C3 03/09)
- Endpoint approve đôi (main.py 8100 + server.py 8090): server 8090 (SimpleHTTPRequestHandler)
  ban đầu CHỈ đọc JSON body, frontend dashboard gửi form-urlencoded → 400 "thiếu task_id".
  Fix: chấp nhận cả 2 — thử `json.loads` nếu body starts `{`, else `parse_qsl` nếu
  `Content-Type: ...form`.
- Cập nhật Feature Tracker (store/features.json) + state file `.hermes-state/ai-company.md`
  sau mỗi hướng xong. Xoá trùng (2 record cùng tên feature) — giữ 1.

## Stream VAD server-side — 2 pitfall khó bắt (build `/ws/stream` 03/09)
1. **`feed()` phải lặp qua MỌI frame trong 1 message WS.** Bug: chỉ xử lý frame đầu
   (`raw[:FRAME_BYTES]`) khi client gửi cả cụm >1 frame trong 1 send → chưa đủ frame để
   flush → 0 message về, client "no close frame". Đúng:
   `for off in range(0,len(raw),FRAME_BYTES): self._feed_frame(raw[off:off+FRAME_BYTES])`.
2. **Slice index phải int.** `OVERLAP_S * FRAME_SAMPLES` = `1.0*1600` = float 1600.0 →
   `pcm[-s*4:]` ném `slice indices must be integers` → kill kết nối WS. Ép `int(...)`.
   Triệu chứng: log server `⚡ WS ... err: slice indices must be integers`.
- Chia feed()/frame sao cho 1 message nhiều frame được xử lý tuần tự; test unit offline
  trước (mock groq_caller trả text: speech+silence→flush, chỉ silence/nhiễu→0 flush),
  rồi test WS thật bằng client gửi sine PCM giả. Groq hallucinate trên sine (ra
  "La La La School") = audio không phải giọng, KHÔNG phải lỗi pipeline.

## Trang preview meeting PHẢI 2-tab, không chỉ transcript (Quang 03/09)
- `_publish_preview()` (app/main.py) từng chỉ `<pre>{transcript}</pre>` · Quang phản hồi
  "trang trên chỉ có transcript thôi". PHẢI build 2 tab (Tổng quan + Transcript) từ
  **summary JSON** đã lưu `{summary, issues, decisions, tasks}`.
- Parse summary JSON → render: Bối cảnh, KPI cards (heuristic rút từ context có trong
  text, KHÔNG bịa số liệu), Vấn đề & Blockers, Quyết định, Action Items (bảng
  Việc cần làm | Người | Hạn). Transaction thêm param `summary`:
  `_publish_preview(transcript, title, summary)`; chỗ share truyền `m.get("summary","")`.
- Tab switch dùng `data-tab` + `b.dataset.tab===n` (tránh escape lỗi `'` trong f-string).
- Verify: `ast.parse` nếu build từ f-string (bắt lỗi `{{}}`); publish → fetch URL thật:
  có `switchTab`, `Action Items`, `Quyết định`; click tab → pane chuyển, transcript đủ.