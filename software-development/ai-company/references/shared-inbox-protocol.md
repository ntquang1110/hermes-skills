# Shared Inbox Protocol — Hermes ↔ OpenClaw

Cơ chế giao tiếp giữa Hermes (máy Dell, Windows) và OpenClaw (máy khác) qua Git repo chung. Cả 2 chạy trên 2 máy riêng biệt → không có shared filesystem, dùng GitHub làm kênh.

## Vấn đề đã gặp và fix

**V1 (thất bại):** 1 file `shared/inbox.json` cho cả 2 → merge conflict liên tục khi 2 bên push cùng lúc, mất tin nhắn, rebase vỡ.

**V2 (đang dùng):** mỗi bên 1 file riêng → không bao giờ conflict:
```
shared/to_hermes.json   # OpenClaw ghi → Hermes đọc
shared/to_claw.json     # Hermes ghi → OpenClaw đọc
```
Mỗi bên chỉ ghi vào file của người nhận → 2 bên không bao giờ chạm cùng file.

## File layout & API (shared/inbox.py)

```python
from shared.inbox import send, read, ack, mark_read, find_stale, sync_pull

send(to="OpenClaw", subject="...", body="...")   # ghi vào to_claw.json + git push, status='sent'
msgs = read()                                     # pull + đọc to_hermes.json (chỉ tin status='sent' chưa xử lý)
ack(msg_id)                                       # đánh dấu read + GỬI ACK ngược lại cho người gửi (bắt buộc sau khi xử lý)
mark_read(msg_id)                                 # đánh dấu đọc + push (không gửi ACK)
find_stale(older_than_minutes=5, me="Hermes")     # tin mình gửi mà bên kia chưa đọc quá X phút
sync_pull()                                       # git pull --rebase
```

Message format (V3): `{id, from, to, subject, body, type: direct|review_request|reply|ack, ref, status: sent|read, sent_at, read_at}`

## Inbox Protocol V3 — ACK bắt buộc (build 03/08)

**Bối cảnh:** user hỏi "sao claw báo em k phản hồi" — hóa ra kênh lệch sync: tin Claw gửi không tới Hermes, tin Hermes gửi không bao giờ được đọc. Không ai biết bên kia nhận chưa.

**Cơ chế mới:**
```
GỬI: Hermes ghi tin (status=sent, sent_at) → push
ĐỌC: Claw cron 1 phút pull → thấy tin → xử lý
ACK: Claw gửi "✅ ACK: <subject>" ngược lại → push
VERIFY: Hermes thấy ACK → coi như đã giao
WATCHDOG: tin nào sent > 5 phút chưa read → TỰ ĐỘNG báo Telegram beFounders
```

- **Gửi mà không có ACK = chưa giao = watchdog báo.** Không im lặng được nữa.
- Watchdog script: `shared/inbox_watchdog.py` (chạy cron 1 phút, copy sang `~/AppData/Local/hermes/scripts/ai-inbox-sync.py`).
  - Lưu ý path: script chạy từ `~/AppData/Local/hermes/scripts/` → phải `sys.path.insert(0, "D:/Hermes Proj/ai-company")` cho `shared.inbox`, và `sys.path.insert(0, "D:/Hermes Proj/ai-company/app")` cho `tg_push` import.
  - Chống spam: state file `shared/.watchdog_state.json` — mỗi tin stale chỉ báo 1 lần.
- Yêu cầu bên kia: sau mỗi tin gửi xong phải confirm "đã gửi + đã push"; sau khi đọc phải `ack()`.

## PITFALL: kênh lệch sync — đừng đoán, CHECK FILE

Triệu chứng: một bên tưởng đã gửi, bên kia không nhận; tin cũ đọc rồi nhưng status vẫn không đúng; cron chạy đều nhưng không có output.

Khi user hỏi "sao em không phản hồi / 2 em chưa chốt được gì":
1. `cat shared/to_hermes.json` + `cat shared/to_claw.json` — đếm tin, xem status/sent_at thực tế (KHÔNG đoán theo lời bên kia)
2. Xác định hướng nào lệch: tin gửi đi không có read_at? tin nhận không thấy?
3. `git pull --rebase` + `git status` — kiểm tra push có tới không
4. Yêu cầu bên kia pull + xác nhận từng tin
5. Đánh dấu đọc tin cũ (mark_read/ack) để watchdog không báo nhiễu

## Sync cron (1 phút)

- Script: `shared/sync.py` (bản Hermes) — bản OpenClaw tương tự nhưng đọc `to_claw.json`
- Hermes cron: `no_agent=True`, script path relative tới `~/AppData/Local/hermes/scripts/`
- **Quan trọng:** script chỉ `print` khi có tin mới → stdout rỗng = Hermes cron im lặng (không spam Telegram). Có tin mới → output → Hermes deliver lên Telegram.

## PITFALL: đừng lọc tin theo keyword

Bản sync đầu tiên chỉ output tin có keyword "chốt/approve/reject/triển khai" → tin "PLAN" và "PHẢN BIỆN" từ Claw bị **nuốt im lặng** (đánh dấu read nhưng không báo user). User phàn nàn "sao hay bị delay".

**Fix:** output TẤT CẢ tin mới, mỗi tin 1 dòng + snippet body. Chi phí token nhỏ, nhưng không bao giờ mất tin.

## Vai trò trong workspace (user chốt)

- **OpenClaw = front**: hỏi user, chốt định hướng, tổng hợp, phản hồi
- **Hermes = back**: logic, phản biện kín, build, deploy, giữ hạ tầng
- User: "sao 2 đứa đều hỏi anh thế" → chỉ 1 giọng hỏi từ front. Hermes không hỏi user trực tiếp khi đã có Claw.

## Git hygiene

- `git pull --rebase` có thể dính rebase-merge directory cũ: `rm -rf .git/rebase-merge` rồi pull lại
- Detached HEAD sau rebase vỡ: `git checkout main && git pull --rebase origin main`
- `GIT_EDITOR=true git rebase --continue` để không mở editor
- Push lỗi "rejected fetch first" = bên kia vừa push → pull --rebase rồi push lại
- **store/*.json trong .gitignore** (dữ liệu live) — chỉ shared/ + code là tracked
- CLOUDFLARE_API_TOKEN mất khỏi env → tìm trong `~/.cloudflared/cert.pem` (decode base64) hoặc cache terminal results

## Quy trình brainstorm 2 agent

1. Claw (front) soạn câu hỏi → gửi Hermes
2. Hermes relay lên Telegram cho user (chỉ forward, không tự hỏi thêm)
3. User trả lời → Hermes ghi `shared/workspace.md` (source of truth) → gửi Claw
4. Claw tổng hợp/phản biện → gửi lại → Hermes trình user

Workspace.md là bối cảnh duy nhất — luôn pull trước, cập nhật, push sau. Không 2 agent cập nhật cùng lúc (vẫn conflict nếu cùng sửa workspace.md — ghi theo lượt).
