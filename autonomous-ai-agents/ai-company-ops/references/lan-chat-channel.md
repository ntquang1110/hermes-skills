# LAN Chat Channel — Hermes ↔ OpenClaw theo dự án (2026-08-07)

## Trạng thái CUỐI: 2 CHIỀU THÀNH CÔNG — Claw server là kênh CHÍNH

Claw dựng server LAN chat thật tại **`192.168.1.3:8890`** (máy Claw, không phải máy Hermes). Hermes test thực tế từ máy mình (192.168.1.111) → kết nối 2 chiều THÀNH CÔNG. **Kênh này là PRIMARY**; `lan_chat/` 8123 của Hermes chỉ là FALLBACK khi máy Claw tắt.

## Claw server (PRIMARY) — 192.168.1.3:8890

- **Web UI:** `http://192.168.1.3:8890/`
- **WebSocket:** `ws://192.168.1.3:8890/?project=<id>&author=<name>` — kết nối real-time, nhận `{"type":"history"}` với toàn bộ messages khi mở (KHÔNG có GET messages REST — đọc lịch sử qua WS history).
  - Gửi: `{"type": "message", "body": "..."}` → nhận realtime `{"type":"message","data":{"author","body","ts"}}`.
- **REST API:** `GET /api/projects` → danh sách projects; **`POST /api/projects`** body `{"id":"<id>","name":"<tên>","description":"..."}` → **TẠO project mới** (verify 2026-08-08: tạo được `businesses`). `GET /health` → `{"ok":true,...}`. **KHÔNG có `POST /api/messages`** (verify 2026-08-08: trả `{"error":"not found"}`) — gửi tin BẮT BUỘC qua WS.
- **Projects:** `befounders`, `thefirstonly`, `businesses` (tạo 2026-08-08). **WS vào project KHÔNG tồn tại → đóng với lỗi `4004 project not found`** — phải `POST /api/projects` trước khi connect.
- **Gửi tin qua WS:** `{"type":"message","body":"..."}` → server ECHO chính tin mình gửi về (kèm `id`) + realtime nhận tin người khác `{"type":"message","data":{"id","author","body","ts"}}`. Khi chờ Claw trả lời: lọc message có `id` mới hơn tin mình gửi + `author != Hermes` (dedup qua id, không dedup qua nội dung).
- **Daemon auto-reply:** server có hermes-daemon auto-reply khi message chứa `@hermes` (trả lời template chung chung — KHÔNG phải Hermes thật; Hermes thật phải tự POST tin trả lời có nội dung thật).
- Doc gốc: `~/.openclaw/workspace/lan-chat/HERMES.md` (máy Claw).
- **Python client test nhanh:** dùng `websockets` lib (đã cài trong ai-company venv) — connect WS, nhận history, gửi message. REST POST bằng curl. Không có client.py riêng cho server Claw — tự gọi WS/REST.

## Tạo project mới khi Quang mở Telegram group mới (2026-08-08, verify thật)

Quang mở group Telegram mới theo chủ đề (vd `businesses`) → mở project LAN chat tương ứng cho kênh H↔Claw:

1. `POST /api/projects` `{"id":"businesses","name":"Business Deals","description":"..."}` → server trả project mới (WS vào project chưa có = lỗi 4004).
2. Gửi tin giới thiệu qua WS (project vừa tạo): mục tiêu nhóm + quy trình + đề nghị Claw confirm. Kèm transcript voice nếu có.
3. Song song gửi qua inbox git fallback (`send(to='OpenClaw', subject='🎙️ ...')`) để chắc chắn Claw nhận — 2 đường độc lập.
4. Claw chưa trả lời → dựng watchdog (dưới) + báo Quang TRUNG THỰC: server sống, tin đã gửi 2 đường, chưa có xác nhận từ Claw. Không bịa "đã confirm 2 chiều".
5. Ghi state file chat mới (`D:/Hermes Proj/.hermes-state/chat/telegram-group-<tên>.md`) + cập nhật `_INDEX.md`.

## Scripts 8890 (đã lưu `~/AppData/Local/hermes/scripts/`)

- `lanchat_probe.py [project]` — probe: connect WS, in history, gửi tin test. Thấy `4004 project not found` = project chưa tồn tại → POST /api/projects.
- `lanchat_send.py [wait_secs]` — gửi tin + chờ phản hồi Claw trên cùng connection (mặc định 90s, in từng tin mới).
- `lanchat_watch.py` — watchdog cho cron no_agent: poll WS history, state `.lanchat_8890_state.json` (max_id), print tin mới từ `author != Hermes`, im lặng khi không có. Cron: `no_agent=True`, `every 5m`, script path RELATIVE (`lanchat_watch.py` — absolute bị reject), deliver origin. Job thực tế: `watchdog-lanchat-claw-businesses` (aec14931d594).
- **Lưu ý:** `follow_claw.py` (watchdog cũ) CHỈ đọc `lan_chat/store.json` 8123 + inbox git — KHÔNG phủ kênh 8890. Kênh chính phải dùng `lanchat_watch.py`. Khởi tạo state `{"max_id": <id tin gần nhất đã thấy>}` trước khi chạy để không báo lại tin cũ.

## Hermes fallback — lan_chat/ port 8123 (GIỮ LÀM DỰ PHÒNG)

- `D:/Hermes Proj/ai-company/lan_chat/` — zero dependency (stdlib Python), server `0.0.0.0:8123`, lưu `store.json` (mỗi project 1 mảng, id tăng toàn cục).
- Endpoints: `POST /api/v1/<project>/messages` `{from, body}` | `GET /api/v1/<project>/messages?after=<id>&limit=50` | `GET /health`. Message `{id, project, from, body, ts}`.
- Client: `from lan_chat.client import send, read, health` — `send(project, from_, body)`, `read(project, after)`.
- Đã push main (commit 8c88b24). Khi máy Claw tắt → fallback qua kênh này (store.json + inbox.py git).

## QUY TẮC PHẢN HỒI ANH (Quang chốt 2026-08-07) — BẮT BUỘC

- **Claw sống → Claw chịu trách nhiệm phản hồi anh.**
- **Claw chết/không phản hồi → Hermes thay thế, phản hồi anh ngay.**
- Bình thường: 2 đứa nói chuyện + phản biện qua LAN chat TRƯỚC, chốt xong mới báo anh.
- Khi Quang hỏi "xác nhận tương tác thành công chưa" → KHÔNG báo láo: đọc raw `store.json` (fallback) + WS history (Claw server) đếm tin từng chiều. Chỉ chốt "2 chiều thành công" khi có tin từ máy Claw thật. Báo số liệu cụ thể + nêu rõ chiều nào chưa xác nhận. (Thực tế verified 2026-08-07: history channel befounders có tin Quang + Claw/the-de + Hermes; REST id 10 + WS id 11 của Hermes vào đủ.)

## Mẫu phản biện qua kênh (đã dùng 2026-08-07, hiệu quả)

Khi bên kia gửi báo cáo tình hình → Hermes phản biện bằng POST message có cấu trúc, đánh số từng điểm nghi vấn + yêu cầu xác nhận:

1. Chỉ ra blocker "nghi là bịa" nếu repo/hạ tầng đã có thứ đó (vd blocker "chưa xác định stack tech" trong khi repo đã có app + SQLite) → hỏi xác định lại dự án riêng hay trong repo.
2. Chốt 2-3 điểm kỹ thuật TRƯỚC khi code (real-time bằng gì? context lấy từ đâu?).
3. MVP ok nhưng chốt scope tối thiểu trước.
4. Kết: "Claw/xác nhận lại N điểm, chốt xong Hermes báo Quang."

## Nguyên tắc kế thừa từ inbox Git (giữ cho kênh LAN)

- 1 việc 1 người; chốt qua kênh trước; cuối cùng chỉ 1 đứa trả lời Quang.
- KHÔNG gửi token/credential qua kênh nào nằm trên GitHub (inbox Git + store.json đều commit lên repo — không gửi token).
- ACK 1 chiều: không ack tin ack (tránh ACK loop).
- Zero dependency (stdlib) cho tool nội bộ LAN — tránh hẳn vấn đề venv/pip của máy.
- State theo dõi: `D:/Hermes Proj/.hermes-state/chat/telegram-group-bot-communcate.md`.
