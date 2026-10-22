# dithi — Vua Kiềm online exam (build transcript, Aug 2026)

Full working example of the pattern. Project at `D:/Hermes Proj/dithi/`, server port 5100, admin password `dithi2026` (env-overridable), domain `dithi.thefirstonly.com` **live** (ingress added via Cloudflare API, config_src=cloudflare — local YAML edit does NOT apply to this token-managed tunnel).

## Question bank (from user's xlsx)

- Latest bank `14.08.2026-vkh_questions_all.xlsx` (bản cuối): **120 questions** (Cô Tâm 58, Cô Minh 48, Cô Dung 14), columns: STT | Nguồn tài liệu (teacher) | Chương/Bài học | STT Gốc | Câu hỏi | Đáp án A-D | Đáp án chuẩn | Giải thích
- Bản 1408 đầu: 121 câu (2 câu sửa Q12/Q14 so với bản gốc). Bản 1408b cuối: xoá 2 câu ("pH của máu người", "mô hình SBI bao gồm các yếu tố theo thứ tự nào"), thêm 1 câu ("Đồng cảm trong huấn luyện") → 120
- **⚠️ Substring-match trap khi diff 2 bank:** 2 câu KHÁC NHAU có thể cùng chứa cụm "mô hình SBI" — check `q.includes('SBI')` sẽ flag nhầm câu còn lại là "removed". Match theo toàn bộ text câu hỏi hoặc STT id, rồi confirm row thực sự không còn trong file mới trước khi báo "đã xóa".
- Per-exam ratio (user-specified): Cô Tâm 20 + Cô Minh 15 + Cô Dung 5 = 40 câu
- Import one-off: `uv run --with openpyxl python import_questions.py` → `data/questions.json`

## Key server decisions

- 36 exams pre-generated at startup (STT_MAX = 36, tự suy từ students.json roster — không hardcode 30), uniqueness via sorted-qid signature, max 200 retries
- Exam question payload to client strips `correct` and `explain` — only `/api/admin/detail` returns them
- `enforceDeadline()` called inside save/submit/overview; deadline = started_at + 50 min
- **Lock semantics (THAY ĐỔI cuối session):** `assigned` (đã nhập STT nhưng CHƯA bấm "Vào thi") → cho chiếm lại NGAY, không 30 phút nữa. User phàn nàn "nhập STT 1 không vào được" khi STT bị giữ bởi người nhập trước chưa vào thi. Code: `if (c.status === 'assigned') delete state.contestants[stt]` rồi tạo mới. Chỉ còn 2 trạng thái chặn: `in_progress` ("đang có người thi") và `submitted` ("đã thi xong"), mỗi cái 1 message + code riêng. Resume token cũ vẫn ok.
- Admin Bearer tokens stored in state; export re-sweeps deadlines before building workbook
- Roster: `data/students.json` (36 HV K02, STT 1-36, tên + CCCD + SĐT + email). Enter STT → ready screen hiện tên "Học viên STT N — Tên" để xác nhận. CCCD chỉ trong hồ sơ admin + export, không phải passcode. Import skip 2 dòng chú thích màu (xanh=bảo lưu, đỏ=bỏ thi).
- **Giờ mở thi (open_at, feature mới):** `state.open_at` ISO / null = tự do. `GET /api/config` public. `POST /api/enter` 403 `chua_den_gio` trước giờ. `POST /api/admin/setting {open_at}` / `{open_at:null}`. Client boot check config → `screenWaiting()` countdown 1s → reload khi đến giờ. **Timezone:** datetime-local gửi `YYYY-MM-DDTHH:mm` local; đừng tạo chuỗi bằng python UTC (lệch offset).

## Test sequence that validated everything

1. Enter STT → assigned + token; second enter with different token → 409 (lock works)
2. Start → exam payload: 40 questions, deadline = now + 50min
3. Save answers → persisted; submit → score computed, submitted_at set
4. Submit again → idempotent; re-enter STT → 409 "đã nộp bài"
5. Deadline test: patch started_at to 51 min ago → overview shows submitted + auto=true, score 0
6. Admin: login wrong → 401; login right → token; overview rows; detail 40 questions with chosen/correct/is_correct; export → 2 sheets, openpyxl-verified (Sheet1 31 rows, Sheet2 120 answer rows)

## Bug 1 — SPA innerHTML wipe (critical, caught by browser test)

Original `renderQ()` called `render()` which did `app.innerHTML = ...` for the question card → destroyed timer div, qnav, prev/next, submit button. Browser snapshot showed only 4 option buttons; curl/API tests all passed.

Fix: render static shell once (`screenExam()` builds timer/qnav/qcard/navrow), then `renderQ()` updates only `document.getElementById('qcard').innerHTML` and re-binds per-question handlers. Also re-attach prev/next/submit handlers inside `renderQ()` because innerHTML swaps replace DOM nodes.

Lesson: always browser-test the interactive screen; API-level tests cannot see client DOM bugs.

## Bug 2 — state file patched externally gets overwritten

Edited `data/state.json` (set started_at back 51 min) while server running → server's in-RAM copy unaffected, and the next `persist()` (triggered by an admin login) wrote the OLD in-RAM state back over the file. Symptom: deadline test silently didn't run.

Fix order: kill server → patch file → restart → call overview. Never patch state.json while the server is alive.

## Bug 3 — admin "trang trắng tinh" (white screen of death)

Both `login-view` and `dash-view` started with class `hidden`; JS had to run to reveal one. Any failure before that — expired admin token in localStorage (server was restarted with fresh `admin_tokens`), network error on the boot `/api/admin/overview` fetch, JS exception — left the page blank white. curl GET returned 200 (server fine); only the browser showed nothing. User reported "trang này vẫn chết".

Fix (both layers, verified):
1. `login-view` is NOT `hidden` in the HTML — it renders immediately on load.
2. Boot wrapped in `try/catch`; every path (token rỗng, token hết hạn, lỗi mạng, exception) ends with `login-view.classList.remove('hidden')` + `dash-view.classList.add('hidden')`.
Result: page can never be all-white; worst case shows the login form.

## Bug 4 — HEAD requests 404 on minimal static server

The plain http server routed only `GET` to static → `HEAD /admin.html` returned 404 (`curl -s -I`). Browsers/proxies/uptime checks use HEAD → "site dead" false positives while GET is 200. Fix: route `GET || HEAD` to static; in the handler, when `HEAD` write headers then `res.end()` without body.

## Excel export (exceljs)

- Sheet "Tổng hợp": one row per STT — **Họ và tên + CCCD + SĐT + email (từ students.json)** + status/mã đề/bắt đầu/nộp/điểm/auto (37 rows: header + 36 HV)
- Sheet "Chi tiết đáp án": one row per answered question (STT/mã đề/câu/teacher/câu hỏi/đáp án TS/đáp án đúng/kết quả)
- `ws.xlsx.writeBuffer()` → `res.end(Buffer.from(buf))` with Content-Type spreadsheetml
- Verify by re-opening the downloaded file with openpyxl, not by trusting HTTP 200

## Cloudflare tunnel (firstonly) — DEPLOYED

Tunnel TQUANG-DELL (0ce9aa47-7d52-4d6a-9a16-13b48c508cff) **config_src: cloudflare** (token-managed Windows service) — local YAML edit DOES NOT apply. Added `dithi.thefirstonly.com → http://localhost:5100` via **API PUT** to `/accounts/{id}/cfd_tunnel/{tunnel}/configurations` (GET current → merge ingress, insert before catch-all → PUT, version 27→28), then DNS CNAME `dithi` → `0ce9aa47-...cfargotunnel.com` proxied (zone thefirstonly.com = 09a2d553b4c5ce037065260ea1feb732, NOT cert.pem's zoneID). Public URL verified HTTP 200. Token from `~/.cloudflared/cert.pem` (decode JSON). See `cloudflare-tunnel` skill for full API flow + pitfalls.

## UI conventions (user request — emerald "tech" pass after default blue looked generic)

- Emerald palette (`--emerald:#0f9d76`, bg `#f2f7f5`, text `#0f2e26`), **system-ui only — Google Fonts BỎ vì render-blocking ở VN** (link fonts.googleapis.com trong <head> làm browser chờ ~30s mới render; user báo "bấm xong 30s sau mới có thay đổi" dù localhost 2ms/tunnel 370ms; fix: bỏ <link> + mọi font-family "Space Grotesk" còn sót trong CSS/JS), SVG 1-stroke icons replacing emoji, radius ramp 8/12/16, progress bar under countdown (red < 5 min), brand as real `h1`
- Mobile-first, single card layout, contestant flow: STT input → "Bạn đã sẵn sàng chưa?" (hiện tên học viên) → "Vào thi" → exam → "Chúc mừng" (no score shown)
- Confirm modal shows unanswered count before submit
- Admin: KPI cards (tổng/đã nộp/đang thi/chưa vào thi) + table with Họ và tên column + detail modal + export button, polls every 5s
- Quality gate: `impeccable` ui-audit.js qua browser_console → 0 tells on both pages (verified)

## State at end of session

- **Deployed + live**: `https://dithi.thefirstonly.com` (contest) + `/admin.html` (pass `dithi2026`), tunnel API-based, verified HTTP 200
- **Roster**: 36 HV K02 imported (STT 1-36, tên/CCCD/SĐT/email), ready screen hiện tên xác nhận
- **Question bank**: latest `14.08.2026-vkh_questions_all.xlsx` (120 câu: Tâm 58 / Minh 48 / Dung 14; bản 1408b xoá 2 câu + thêm 1 so với bản 1408)
- **Giờ mở thi**: `state.open_at` default null (mở tự do); admin có card setting + input datetime-local; thí sinh trước giờ thấy countdown screen; server 403 chua_den_gio
- **Admin reset**: nút "Reset kỳ thi" (header, đỏ) + "Reset" mỗi hàng, cả hai kèm modal xác nhận; API `POST /api/admin/reset {stt}` / `{all:true}`
- **State reset trước kỳ thi thật**: kill server THẬT (netstat PID → Stop-Process) → xoá `data/state.json` → restart → 36 đề gen lại, overview sạch (done 0 / active 0 / assigned 0). Lưu ý: `process(action='kill')` chỉ giết bash wrapper, node con sống — luôn netstat để tìm PID thật.
- **Run**: `cd D:/Hermes Proj/dithi && node server.js` (background). Reboot máy = server chết, cần bật lại. Đổi mật khẩu admin: `ADMIN_PASSWORD` đầu `server.js`.
