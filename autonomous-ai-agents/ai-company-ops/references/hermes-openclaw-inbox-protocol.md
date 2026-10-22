## Giao tiếp Hermes ↔ OpenClaw (2 máy riêng)

Cơ chế: **Git shared files**. Mỗi bên ghi vào file riêng theo hướng — KHÔNG dùng 1 file chung (gây merge conflict liên tục).

```python
from shared.inbox import send, read, sync_pull
send(to='OpenClaw', subject='...', body='...')   # tự ghi to_claw.json + push
msgs = read()                                    # pull trước, đọc to_hermes.json
```

**Inbox Protocol v3 — ACK bắt buộc (2026-08, sau khi Claw báo "Hermes không phản hồi" nhưng thực ra tin bị lệch sync):**
- Message có `status: sent|read` + `sent_at` + `read_at`; `read()` mặc định trả tin `status=="sent"` (chưa xử lý).
- **`ack(message_id)`** — bên nhận xử lý xong → đánh dấu read + gửi tin `✅ ACK: <subject>` ngược lại người gửi (msg_type="ack", ref=id gốc). Người gửi coi tin đã giao CHỈ KHI nhận ACK.
- **PITFALL ACK SPAM VÔ HẠN (2026-08-06, watchdog spam Telegram mỗi phút):** `ack()` đánh dấu `status="read"` nhưng ban đầu QUÊN `_git_push(my_file)` → trạng thái read không lên git → mỗi lần `sync_pull()` kéo bản cũ `status="sent"` → watchdog ACK lại → pull lại vẫn "sent" → lặp vô hạn, spam "✅ Đã xử lý + ACK" hàng chục cái/phút. **Fix: sau khi `_write_file(my_file, data)` trong `ack()` PHẢI gọi `_git_push(my_file)`** — trạng thái read phải lên remote, nếu không bên kia (và chính watchdog) sẽ thấy tin vẫn chưa đọc mãi.
- **Watchdog cron phải SILENT khi xử lý bình thường:** script `ai-inbox-sync.py` KHÔNG print `"✅ Đã xử lý + ACK: ..."` cho từng tin (stdout của cron no_agent = delivered → spam mỗi phút). Chỉ output khi có VẤN ĐỀ: ACK fail, tin stale >5p chưa đọc, hoặc error. ACK thành công = im lặng.
- **`find_stale(older_than_minutes=5)`** — tìm tin mình gửi mà bên kia chưa read > 5 phút.
- **Watchdog cron mỗi 1 phút** (`shared/inbox_watchdog.py` → copy sang `~/AppData/Local/hermes/scripts/ai-inbox-sync.py`): pull → đọc + ack tin mới → nếu có stale → gửi cảnh báo Telegram beFounders. State file `.watchdog_state.json` chống spam (mỗi tin báo 1 lần).
- **Triệu chứng "bên kia không nhận" thường là lệch sync git, KHÔNG phải tin chưa gửi:** check cả 2 file (`to_hermes.json` vs `to_claw.json`) + `git pull --rebase` + trạng thái từng tin. Khi 2 bên kết luận khác nhau → đọc raw file trước khi tin lời báo cáo.
- **Pitfall script cron path:** script trong `~/AppData/Local/hermes/scripts/` KHÔNG import được `shared.*` → chèn `sys.path.insert(0, "D:/Hermes Proj/ai-company")` + STATE_FILE trỏ về `AI_COMPANY/shared/.watchdog_state.json`.
- **⚠️ ACK LOOP (2026-08-07, phát hiện khi Quang hỏi "2 em tương tác thành công chưa"):** `ack()` vừa mark read vừa gửi tin `✅ ACK: <subject>` ngược cho NGƯỜI GỬI — nếu bên kia cũng ack tin ACK đó → 2 bên ack lẫn nhau vô hạn, subject tích lũy "✅ ACK:" hàng chục lần (tin #41 trong to_hermes.json thực tế dính). **Fix: không ack tin có `msg_type == "ack"`** (tin ack chỉ cần read, không gửi ACK ngược). Check nhanh: đếm `subject.count("ACK") > 2` trong cả 2 files.
- **Verify kênh hoạt động (trả lời "2 em tương tác thành công chưa"):** đọc raw cả 2 files rồi đếm theo chiều — Hermes→Claw = tin `from=="Hermes"` trong `to_claw.json`; Claw→Hermes = tin `from=="OpenClaw"` trong `to_hermes.json`. Kênh OK = cả 2 chiều có tin status `read` + không còn tin `sent` (chưa xử lý) mới. Báo SỐ LIỆU cụ thể (vd "65 tin Hermes→Claw đọc hết, 22 tin Claw→Hermes") — không nói chung chung "hoạt động tốt". Thực tế verified 2026-08-07: 65 + 22, toàn bộ read.
- **KHÔNG báo "thành công 2 chiều" khi mới test 1 chiều (Quang hỏi "2 em xác nhận kết nối thành công nhé" 2026-08-07):** Hermes tự test localhost + IP LAN (1 chiều) KHÔNG phải bằng chứng 2 chiều. Khi chưa có tin gửi từ máy Claw → báo trung thực: "phía Hermes 100% sẵn sàng + test pass, phía Claw chưa có xác nhận, chờ Claw gửi tin test" + nhắc Claw qua inbox (#66, #67). Không bịa "đã kết nối thành công" để làm vừa lòng — Quang đánh giá cao báo cáo chính xác hơn báo cáo đẹp.

Pitfalls:
- **Merge conflict inbox**: từng dùng `shared/inbox.json` chung → 2 máy push cùng lúc = conflict mỗi lần. Fix: tách `to_claw.json` / `to_hermes.json`.
- **Kênh LAN chat theo dự án (2 CHIỀU THÀNH CÔNG 2026-08-07, mở rộng 2026-08-08):** kênh CHÍNH = Claw server `192.168.1.3:8890` — WS `ws://.../?project=<id>&author=<name>` gửi/nhận realtime (`{"type":"message","body":...}`), history qua WS (KHÔNG có GET messages REST, KHÔNG có POST /api/messages — verify 2026-08-08). REST: `GET /api/projects` + **`POST /api/projects` = TẠO project mới** (WS vào project chưa có → lỗi `4004 project not found`; Quang mở group TG mới → tạo project tương ứng, đã tạo `businesses` 2026-08-08). Scripts + watchdog 8890: `~/AppData/Local/hermes/scripts/lanchat_{probe,send,watch}.py` (cron no_agent 5m `watchdog-lanchat-claw-businesses` aec14931d594; follow_claw.py cũ KHÔNG phủ 8890). Fallback = `lan_chat/` 8123 (máy Hermes, `send/read/health`, đã push main). **QUY TẮC PHẢN HỒI (Quang chốt): Claw sống → Claw phản hồi anh; Claw chết → Hermes thay; bình thường 2 đứa phản biện qua kênh trước, chốt xong mới báo anh.** Chi tiết endpoint + test + mẫu phản biện → xem `references/lan-chat-channel.md`.
- **Keyword filter nuốt tin**: cron sync từng chỉ output tin có keyword "chốt/approved/..." → Claw gửi "PLAN" + "Phản biện" bị nuốt im, anh thấy delay. Fix: output TẤT CẢ tin mới, mỗi tin 1 dòng snippet.
- **Git rebase/HEAD detached**: sau conflict, `git pull --rebase` dính lỗi rebase-merge directory → `rm -rf .git/rebase-merge` rồi retry, hoặc `GIT_EDITOR=true git rebase --continue`. Dùng `git push origin HEAD:main` khi detached.
- Sau mỗi lần `git add/commit`, nếu push bị rejected → pull --rebase trước, hoặc stash → pull → pop → push.
