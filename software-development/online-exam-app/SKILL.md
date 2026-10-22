---
name: online-exam-app
description: "Timed online exam apps: unique exams, admin, Excel export."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [exam, quiz, contest, node, excel, admin-dashboard, countdown]
---

# Online Exam App (pattern proven on dithi — Vua Kiềm contest)

## When to use

User wants an online exam/quiz/contest system:
- Contestants enter a code / STT / passcode, take a timed multiple-choice test
- Exams auto-generated per person (teacher/lesson ratios, shuffled options, no duplicates between people)
- Auto-submit when time runs out; resume after refresh; answers hidden from contestants
- Admin dashboard: who is taking / done, start & submit times, scores, detail view of answers, Excel export
- Deployed behind a public subdomain (Cloudflare tunnel) so phones can reach it remotely

## Architecture (zero-build, proven)

- **Node plain `http` server + JSON file store** (`data/*.json`). No framework, no DB. Fine up to ~100 contestants.
- Static frontend in `public/`: `index.html` (contestant), `admin.html` (admin). Single page each, inline CSS+JS.
- Excel export via `exceljs` (the only npm dependency): `npm install exceljs --no-audit --no-fund`
- Deploy: add subdomain to an existing Cloudflare tunnel (see `cloudflare-tunnel` skill) or new tunnel.

## Data model

- `questions.json`: `[{id, teacher, lesson, q, options[4], answer:'A'..'D', explain}]`
- `exams.json`: N pre-generated exams × 40 questions, each option array already shuffled, `correct` = new index
- `state.json`: `{contestants: {stt: {token, exam_id, status: assigned|in_progress|submitted, created_at, started_at, submitted_at, answers, score, auto}}, admin_tokens: [], exams}`

## Core rules (non-negotiables)

1. **Server enforces the deadline, never trust the client countdown.** On every save / submit / admin-overview call, if `now > started_at + duration` → mark submitted (`auto=true`) with whatever answers were saved. Client timer is UX only.
2. **Pre-generate all exams at startup** with a uniqueness check: signature = sorted question-id list; regenerate until no duplicate (loop with max attempts ~200). Each entrant gets the next *unused* exam → no repeats between people.
3. **Shuffle answer options per exam** (randomize A/B/C/D order) and store the NEW correct index. Never return the original letter as the answer key.
4. **Resume via localStorage token.** Server stores a per-STT token; re-entering with the same token returns exam + saved answers + `remaining_ms`. Refresh / lost connection does not lose progress.
5. **Lock STT while in use — CHỈ chặn khi đã bắt đầu hoặc đã nộp.** `assigned` (nhập STT nhưng CHƯA bấm "Vào thi") → **cho phép chiếm lại ngay, không chặn, không cần chờ expire**: người chưa xem đề thì không có gì để bảo vệ, và user explicitly complained khi STT bị giữ 30 phút ("nhập STT 1 mà không vào được"). Implementation: `delete state.contestants[stt]` rồi tạo mới (exam cũ trả về pool). `in_progress` (đã bấm "Vào thi") → 409. `submitted` → 409 vĩnh viễn. Resume qua token cũ vẫn hoạt động (người cũ quay lại được, kể cả sau khi bị chiếm — họ tạo session mới).
6. **Client auto-saves drafts every 15s** via `/api/save`; server persists each time.
7. **Score computed server-side at submit**, never shown to the contestant (configurable; default "chúc mừng" screen only).

## Minimal API surface

| Method | Path | Purpose |
|--------|------|---------|
| POST | /api/enter | {stt, token?} → assign exam + new token, resume, or 409 |

Lock/409 messages MUST be distinct per status (user explicitly required this so contestants know WHY they're blocked) — after the "assigned is reclaimable" change, only TWO blocking states remain:
- already submitted → `STT X đã thi xong. Không vào lại được.` (code 'submitted')
- in_progress by another → `STT X đang có người thi. Không vào được.` (code 'in_progress')
Include a `code` field alongside `error` so the client could branch on it.
| POST | /api/start | {token} → set started_at, return exam + deadline |
| POST | /api/save | {token, answers} → persist draft |
| POST | /api/submit | {token, answers} → score + submitted_at (+ deadline enforcement) |
| POST | /api/admin/login | {password} → admin Bearer token |
| GET | /api/admin/overview | table of all STTs (status/exam/start/submit/score) |
| GET | /api/admin/detail?stt= | full answers vs correct per question |
| GET | /api/admin/export | .xlsx download (2 sheets: summary + per-question detail) |
| POST | /api/admin/reset | {stt:N} reset 1 thí sinh, {all:true} reset toàn bộ → xóa contestant, STT trống lại. 401 nếu không auth. |

Admin auth: Bearer token stored in `state.admin_tokens`; simple password constant, overridable by env var.

**Admin reset MUST have a confirm modal (user requirement: "modal xác nhận để tránh user bấm nhầm").** Reset toàn bộ kỳ thi là phá dữ liệu thi thật — không được reset ngay khi bấm. Thiết kế: nút đỏ "Reset kỳ thi" ở header + link đỏ "Reset" cạnh "Chi tiết" mỗi hàng đã dùng; cả hai đều mở modal (overlay) có tiêu đề, text cảnh báo rõ ("Xóa dữ liệu thi của TẤT CẢ 36 STT... Chắc chắn reset?"), 2 nút Hủy/Reset. JS pattern: `openResetModal(title, text, action)` giữ action trong biến, `rm-confirm` gọi action khi bấm, `rm-cancel`/click-overlay đóng modal không làm gì. Sau reset gọi `loadOverview()` refresh bảng.

## Giờ mở thi (open_at setting — user requirement: chặn trước giờ, countdown)

Admin set 1 mốc giờ (ví dụ "20:00 tối nay") → trước giờ đó thí sinh vào link thấy màn "Chưa đến giờ vào thi. Còn lại: HH:MM:SS" đếm ngược realtime, **đến giờ tự reload mở trang nhập STT**. Phải enforce ở CẢ 2 lớp:

- **Server (bắt buộc, không chỉ ẩn UI):** `state.open_at` (ISO, null = mở tự do). `GET /api/config` (public) trả `{open_at, server_now}`. `POST /api/enter` check `Date.now() < open` → 403 `{error:'chua_den_gio', open_at, server_now}`.
- **Client:** index.html boot fetch `/api/config` → chưa đến giờ → `screenWaiting(openAt)` với `setInterval` 1s, cập nhật countdown + `location.reload()` khi hết giờ. Server_now giúp client không lệch giờ máy.
- **Admin setting:** `POST /api/admin/setting {open_at}` set, `{open_at:null}` bỏ giới hạn. Admin UI: input `datetime-local` + nút "Lưu giờ mở" + "Bỏ giới hạn" + status line hiển thị giờ hiện tại.
- **⚠️ Timezone pitfall:** `datetime-local` input gửi `YYYY-MM-DDTHH:mm` (local time, không có timezone suffix). Server `new Date(str)` parse theo LOCAL của server — đúng nếu client và server cùng máy/múi giờ (case này: admin máy anh + server máy anh). ĐỪNG dùng python `datetime.now(timezone.utc)` để generate chuỗi rồi gửi — sẽ lệch đúng số giờ UTC offset (test của tôi set "+1h" mà thành quá khứ vì lệnh date -d '+1 hour' theo local nhưng python utc). Kiểm chứng: set giờ tương lai local → `/api/config` trả open_at ISO đúng, enter bị 403, link hiện countdown.

## Pitfalls (learned the hard way — dithi session)

- **SPA innerHTML bug (critical):** a `render()` helper that sets `app.innerHTML` wipes the whole layout. If per-question rendering calls it, the timer, question-nav and submit buttons vanish — everything still passes API tests. Fix: render the static shell (timer / qnav / qcard containers) ONCE, then only update the inner `#qcard` element per question. Always browser-test the exam screen, not just curl.
- **Server keeps state in RAM; editing state.json externally does nothing.** Worse: the next server `persist()` overwrites your external patch (e.g. admin login persists). To test deadline logic: kill server → patch `started_at` → restart → call overview.
- **Killing the Hermes background process does NOT kill the node child (critical for resets).** `process(action='kill')` on a `terminal(background=true)` run only kills the bash wrapper; the real `node server.js` keeps listening and holds old state in RAM. Symptom: you `rm data/state.json` + restart "successfully", but STTs stay locked and old contestants reappear — because the OLD server never died and answered the requests. Fix: find the real PID with `netstat -ano | grep :5100 | grep LISTEN`, then `powershell -Command "Stop-Process -Id <PID> -Force"`. Repeat until `netstat` shows no LISTEN on the port. When in doubt, kill ALL PIDs listening on the port (there can be IPv4 + IPv6 entries). This bites the "reset for the real exam" step the hardest — a stale server mid-exam silently keeps old state.
- **One-off Python with deps on a host venv that has no pip:** use `uv run --with <pkg> python script.py` (e.g. `uv run --with openpyxl python import_questions.py`). Do not attempt `pip install` into the venv.
- **`/tmp` path mismatch on Windows:** git-bash `/tmp/...` is NOT readable by Windows-native python (`FileNotFoundError`). For curl output shared with python, write into the project dir (`ta.json`) instead of `/tmp`.
- **Validate the question bank before building:** count per teacher, verify answer letters ∈ {A,B,C,D}, check bank size ≥ per-exam ratio (need 20 from teacher X → bank must have ≥20). Empty rows / bad answers break generation silently.
- **Verify the exported xlsx content, not just HTTP 200:** after download, open with openpyxl and print sheet names + first rows.
- **Quoted heredoc does NOT substitute shell vars:** `python - <<'PYEOF'` keeps `$TOKEN` / `TOKEN_PLACEHOLDER` literal → auth fails (HTTP 400/401). Write the script to a `.py` file and pass secrets via env (`CF_TOKEN=$(...) python script.py`), or use unquoted heredoc carefully.
- **White screen of death (admin "trang trắng tinh"):** if BOTH login and dashboard views start with class `hidden` and JS must run to reveal them, then any failure before that point — stale/expired admin token, network error on boot fetch, JS exception — leaves the page blank white. User reports "trang chết" while curl/GET returns 200 fine. Fix (both layers): (1) login view is NOT hidden by default in HTML — it renders immediately; (2) boot wrapped in try/catch and every path ends by explicitly showing login or dashboard. Never let a JS failure produce an all-hidden page.
- **HEAD requests → 404 on minimal static servers (proxy "site dead" false positive):** a plain `http` server that only serves `GET` returns 404 for `HEAD`. Browsers/proxies/uptime checks use HEAD → report the site dead even though GET works. Fix: `if (req.method === 'GET' || req.method === 'HEAD')` route to static; in the static handler, when `HEAD` write headers but `res.end()` without body. Diagnose with `curl -s -I https://.../admin.html` (returns 404) vs `curl -s https://...` (200).
- **Check which tunnel config is active before editing:** token-managed Cloudflare service ignores local YAML entirely — create a local-managed tunnel instead (details in `cloudflare-tunnel` skill).

## Steps

1. Collect: question bank file, per-teacher ratio per exam, total exam length, contestant count (N exams = N contestants), duration, passcode scheme (STT vs CCCD), admin password, open-time gate (open_at — user may set it later via admin UI).
2. Import questions → questions.json (one-off script with openpyxl).
3. Server: gen exams (uniqueness + shuffle), API routes, Excel export.
4. Frontends: contest flow (enter → ready screen → exam → done) and admin (login → live table → detail modal → export).
5. Test: API flow with curl/python, UI flow with browser, xlsx content with openpyxl, deadline via the kill→patch→restart trick.
6. Deploy: add subdomain ingress + DNS CNAME, start server, verify via public URL from a phone.

## Student roster (danh sách học viên — import tên + CCCD)

When the user sends a roster Excel (STT + Họ tên + CCCD + SĐT + email):

1. Import → `data/students.json` `{stt: {stt, name, cccd, phone, email}}` (one-off openpyxl script). **STT_MAX tự suy từ roster** (`Math.max(...Object.keys(students).map(Number))`) — không hardcode 30.
2. **Skip color-note rows**: rosters often carry legend rows like `màu xanh` / `màu đỏ` (bảo lưu / bỏ thi) with no STT — filter by missing STT OR name matching those tokens. Verify count + no duplicate STT/CCCD before importing.
3. `/api/enter` trả `name`; contestant ready screen shows **"Học viên STT 13 — Nghiêm Thái Hoa"** before "Vào thi" (confirm correct person). CCCD stays in admin record + Excel export, NOT used as passcode (user chose this: "nhập STT, hiện tên xác nhận").
4. Admin overview + export include name / cccd / phone columns. **KPI "Tổng STT" trong admin.html là HTML hardcode — đổi cùng STT_MAX** (cả text "1 - 30" → "1 - 36" và `max="36"` trong index.html, và JS validate). Dễ quên vì overview API trả đúng nhưng UI cứng.
5. Nếu roster thay đổi giữa chừng (file mới), chỉ cần import lại students.json + restart; contestants cũ trong state.json vẫn giữ.

## Swapping in a NEW question bank (re-import flow)

When the user sends an updated questions Excel (e.g. `14.08.2026-vkh_questions_all.xlsx`):
1. Copy to project dir, diff old vs new bank first (openpyxl: changed questions/answers/options) and report what changed before re-importing. **⚠️ Substring-match trap:** two DIFFERENT questions can share a phrase (e.g. both contain "mô hình SBI") — a `q.includes('SBI')` diff check flags the survivor as "removed". Match on full question text or STT id, then confirm any "removed" row is truly absent from the new file before reporting it deleted.
2. Point the import script's `SRC` at the new file → run `uv run --with openpyxl python import_questions.py` → verify `questions.json` totals + that changed rows carry the new text.
3. Delete `data/state.json` (exams + contestants regenerate from the new bank) → restart server → confirm "Đề: 30 bài x 40 câu" in log and clean overview (done 0 / active 0).
4. Re-check the public URL returns HTTP 200. Note: a question may legitimately not appear in exam #1 (random sampling) — verify the BANK has the change, not a specific exam.

## UI quality gate after design changes (unslop / theme pass)

- After any redesign (theme swap, "tech hơn" pass, emoji cleanup), run the `impeccable` ui-audit detector via `browser_console` (expression = scripts/ui-audit.js) and target **0 tells** on BOTH pages (contest + admin).
- This session's accepted "tech" look: emerald palette (`--emerald:#0f9d76`, bg `#f2f7f5`, text `#0f2e26`), **system-ui font only** (see font warning below), SVG icons (1 stroke) replacing UI emoji (📝⏱️🎉📊⬇💡), radius ramp 8/12/16, progress bar under the countdown going red < 5 min, brand name as real `h1` (not flat span). User green-lit this after the default blue looked generic.
- **⚠️ NO Google Fonts / external font CDN for VN users (critical — caused "30s delay" complaint):** a `<link href="https://fonts.googleapis.com/...">` in `<head>` is render-blocking. Google Fonts is slow/blocked in Vietnam (especially 4G) → the browser waits ~30s (timeout) before rendering the page. User reported "bấm xong 30s sau mới có thay đổi" while localhost was 2ms and tunnel 370ms — the app was fine, the font CDN was hanging. Fix: use `system-ui` only (or self-host the font behind the tunnel). When removing: delete the `<link>` AND every `font-family` reference in CSS/JS (grep `googleapis` + font name). Verify: `performance.getEntriesByType('resource')` shows only the page's own domain, no fonts.googleapis.com. Note: the `impeccable` skill's pitfall #8 recommends Google Fonts — that applies to static publish pages, NOT live apps serving VN users.
- **Emoji cleanup rule:** replace emoji in UI chrome only (nav, buttons, card headers). Keep emoji that is data/contract (status strings the JS compares, content tags).
- **Contestant UI must NOT show teacher names** (user: "bỏ tên giáo viên đi"). Question header shows only "Câu X/40" — no `· Cô Tâm`. Admin detail keeps the teacher column for review. The API returns teacher anyway; just don't render it in `index.html`.
- **Exam title = full two-line header** (user-approved): line 1 small-caps course name (`CTĐT HUẤN LUYỆN VIÊN CÂN BẰNG KIỀM HOÁ CƠ THỂ KHOÁ K02`), line 2 large `PHẦN THI TRẮC NGHIỆM`. Repeat on BOTH the STT-entry screen and the ready screen. Course code changes per cohort (K02, K03...) — ask the user which cohort, and double-check it (user corrected K03 → K02 once).
- Static HTML changes need NO server restart (read per request); a theme pass only touches `public/*.html`.

## Reference

- `references/dithi-architecture.md` — full build transcript: data model, API contract, test sequence, and the exact innerHTML + state-file bugs with fixes.
