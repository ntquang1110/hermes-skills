## Calendar — Tab "Lịch họp" (2026-08, tfo web)

Anh Quang yêu cầu: view meeting theo tuần/tháng → ngày → từng meeting → overview + tasks theo người. Đã build:

- Tab bar trên `app/static/index.html`: Dashboard | 📅 Lịch họp — `switchTab('calendar')` → `loadCalendar()`.
- **Week view:** 7 cột ngày (Thứ 2 → CN), mỗi meeting = chip hiển thị `title` + trạng thái task (`has-tasks` viền vàng / `all-done` viền xanh). Nút ◀ ▶ đổi tuần, "Hôm nay" reset.
- **Click ngày** → danh sách meetings; **click meeting** → overview (thời gian, tóm tắt, transcript) + tasks của meeting đó (lọc theo `meeting_id`) + toggle task ngay trong lịch.
- **Meeting có title + meeting_time:** `/api/meetings` nhận thêm `title` + `meeting_time` (datetime-local). UI lịch hiển thị title thay vì session_id. `meeting_time` MẶC ĐỊNH = thời điểm bắt đầu ghi âm/upload nếu user để trống (`setDefaultMeetingTime()` gọi trong record start, file change, drop).
- **Task link meeting:** `create_task` nhận `meeting_id`; `/api/summarize` tự parse dòng chứa "task/việc cần/cần làm/giao/todo/đề xuất" từ DeepSeek result → sinh tasks kèm `meeting_id` + assignee rút từ `Tên:`.
- **Xóa meeting:** nút 🗑 trong Lịch sử cuộc họp + "🗑 Xóa" trong chi tiết calendar. Backend `DELETE /api/meetings/{id}` — xóa meeting + tasks liên quan (`meeting_id` match). Frontend confirm trước khi xóa.
- **Pitfall bug cũ (nút Xem "không có gì"):** `openMeeting` trước hiển thị vào `resultBox` (hộp ẩn đầu trang) + scrollIntoView — user tưởng không hoạt động. Fix: hiện đúng nội dung (title + summary + transcript) + `scrollIntoView({block:'center'})`. Luôn test nút trên browser thật, không chỉ curl API.
- **Pitfall JS async:** trong `mediaRecorder.onstop`, phải lưu `const recSid = sessionId` TRƯỚC khi set `sessionId = null` — nếu không meeting được lưu với id rỗng. Đã dính, đã fix.

## Multi-tenancy (2026-08 — anh Quang chốt: account tách riêng, Quang là admin)

- **CHỐT 15/08 (Quang): "Vẫn dùng chung domain, tách riêng phần lưu trữ — mỗi user 1 folder."** → Kiến trúc hiện tại ĐÃ ĐÚNG yêu cầu từ trước (build 12/08): chung domain `tfo.thefirstonly.com`, mỗi user 1 folder riêng. KHÔNG cần subdomain riêng. Demo isolation PASS ngay trên production (15/08) — không phải chờ build thêm.
- **Demo/verify isolation bằng browser (recipe đã chạy 15/08):** logout (xóa localStorage `tfo_token` + cookie) → login `ntphuong2301@gmail.com` → dashboard phải RỖNG hoàn toàn ("Chưa có task", "Chưa có cuộc họp nào") → logout → login `quang@kiemsaphia.com` → data đầy đủ còn nguyên. PASS = không lẫn data 2 chiều.
- Mỗi user 1 workspace riêng: `tfo_data/users/<email_sanitized>/` — tasks.json, meetings.json, recordings/ — user KHÔNG thấy data nhau.
- Sanitize email: `email.lower().replace("@","_at_").replace(".","_dot_")` → `quang_at_kiemsaphia_dot_com`.
- Mọi API token-scoped: `_resolve_user(token)` → email → `_user_read/_user_write(email, file, default)`. Không token = 401.
- Recording: `/api/record/start` nhận `token` → session lưu email → file ghi vào user dir; `_finalize_recording` lưu meetings vào workspace của email trong session.
- **Admin endpoint:** `/api/admin/users` — chỉ `ADMIN_EMAILS = {"quang@kiemsaphia.com"}` → Quang xem data mọi user để cải tiến product (đã confirm).
- Pitfall migrate: folder cũ đặt theo email thật (`quang@kiemsaphia.com`) vs folder mới sanitized → merge thủ công (gộp tasks/meetings theo id/session_id) rồi xoá folder cũ, đừng để 2 workspace trùng.
- Frontend: mọi `fetch('/api/...')` phải kèm token — GET dùng query `?token=`, POST dùng form field `token` (hoặc `Content-Type: x-www-form-urlencoded` + body).

## Task Board — 10 task đầu + "Xem thêm" popup infinite scroll (2026-08-15)

Dashboard Company (`dashboard/index.html`, serve qua `upload.thefirstonly.com/company`) KHÔNG render hết task lên board — chỉ 10 task đầu, còn lại popup:

- Board: `visible = filtered.slice().reverse().slice(0, TASKS_PER_PAGE)` (10) + nút `<button class="task-more-btn" onclick="openTaskModal('${filter}')">Xem thêm N task →` nếu hiddenCount > 0.
- Popup: overlay `.task-overlay` + `.task-modal` (bottom sheet mobile, `max-height:85vh`, list `.task-modal-list` scroll riêng). `openTaskModal(filter)` mở → `loadMoreTasks()` render batch `POPUP_BATCH=30`, scroll gần đáy (`scrollTop+clientHeight >= scrollHeight-120`) load tiếp, marker "— hết N task —" khi xong.
- **State global (không closure):** `popupTasks/popupFilter/popupRendered/popupLoading` + `window.__tasks` set trong `render()` để popup dùng chung data mọi filter. `taskItemHtml(t)` phải GLOBAL (khai báo ngoài `render()`) vì popup function gọi nó — nếu nằm trong scope `render()` → ReferenceError.
- Đóng popup: nút ✕ + click nền `onclick="if(event.target===this)closeTaskModal()"`; nhớ `document.body.style.overflow='hidden'` khi mở, restore khi đóng.
- Test: inject 120 task giả vào `window.__tasks` → openTaskModal → verify batch1=30, scroll → 60 → 120 + end marker. Reload sau test để reset.

### TFO web — Task & Quyết định: 10 task + popup infinite scroll (app/static/index.html, 2026-08-15)

Cùng pattern với dashboard, khác file: `app/static/index.html` (tab Dashboard, `#taskList`). `loadTasks()` render 10 task + nút "Xem thêm N task →" → `openTaskListModal()` bottom sheet, batch 30, scroll gần đáy load tiếp. `taskItemHtml(t)` dùng chung board + popup (giữ onclick gốc). State global `popupTasks/popupRendered/popupLoading`; `loadTasks()` set `popupTasks = tasks.slice().reverse()`.
- **PITFALL CHẾT NGƯỜI — xung đột tên hàm với popup EDIT TASK đã có (đã dính 15/08):** TFO web ĐÃ CÓ SẴN `openTaskModal(taskId, source)` (mở modal sửa task, ~line 2845) và `closeTaskModal()` (~line 2877). Khai báo `function openTaskModal()` cho popup task-list → **định nghĩa SAU CÙNG thắng** (function declaration hoisting theo thứ tự) → nút "Xem thêm" gọi nhầm hàm edit task → popup mới không bao giờ mở, và `closeTaskModal()` đóng sai modal. Triệu chứng: click nút không có gì xảy ra, console KHÔNG báo lỗi (vì hàm tồn tại, chỉ là hàm khác). **Fix: đặt tên riêng `openTaskListModal()` / `closeTaskListModal()` + cập nhật onclick trong HTML.** Trước khi đặt tên hàm mới trong index.html: `grep -n "function <tên>" index.html` phải = 0.
- **Test login TFO (browser test cần):** ALLOWED_EMAILS = `quang@kiemsaphia.com` (KHÔNG phải <EMAIL> — email đó bị 403), passcode `<PASSCODE>`, token key localStorage = `tfo_token`. Đăng nhập nhanh bằng JS: POST `/api/login` form-encoded `email=quang@kiemsaphia.com&passcode=<PASSCODE>` → lưu `localStorage.setItem('tfo_token', token)` → navigate `/app`.

### ⚠️ PITFALL CHẾT NGƯỜI — template literal đóng sai giết CẢ script block → dashboard "No tasks yet" dù có data

Triệu chứng: dashboard hiển thị "No tasks yet"/"Loading..." MÃI dù `company-data.json` có 16 task. Nguyên nhân (đã dính 15/08): trong Feature Tracker render, `return \`<div class="feature-item">...\` + \`` (backtick THỪA giữa template literal) → HTML thô nằm ngoài template → **SyntaxError ở parse time → TOÀN BỘ `<script>` chết → mọi function undefined → không render gì**.

- **Fix:** xóa backtick giữa template, để template chạy liên tục tới `\` cuối.
- **Verification bắt buộc sau MỌI patch dashboard:** trích script + `node --check`:
  ```bash
  python -c "import re; html=open('dashboard/index.html',encoding='utf-8').read(); scripts=re.findall(r'<script>(.*?)</script>', html, re.S); open('/tmp/chk.js','w',encoding='utf-8').write('\n'.join(scripts))"
  node --check /tmp/chk.js
  ```
  (node --check báo đúng dòng lỗi; nếu lỗi syntax xuất hiện, dashboard chết im — test browser ngay sau mỗi patch lớn.)
- 1 lỗi syntax ở bất kỳ đâu trong 1 `<script>` block = block đó không chạy gì cả. Đã dính 2 lần khác nhau (login TFO 12/08 + dashboard 15/08).

### ⚠️ Mobile overflow ngang (đã dính nhiều lần)
4 thủ phạm + code CSS: `references/mobile-overflow-checklist.md`. **Đo bằng iframe 390px** (`scrollWidth` vs `innerWidth`) — đo desktop KHÔNG phản ánh mobile.

## Feature Tracker (Dashboard Company — 1 trang theo dõi mọi thứ)



Anh Quang muốn Dashboard Company là 1 nơi duy nhất xem team đang chạy gì, ai làm gì — không phải hỏi lại.

- Data: `store/features.json`; API trong `hub/store.py`: `get_features()`, `add_feature()`, `update_feature(id, status=, progress=)`.
- `hub/aggregate.py` thêm `"features": get_features()`; `dashboard/index.html` render section "🚀 Plan & Features Tracker" ở đầu trang (icon trạng thái, priority P0-P2, progress bar, owner, URL ↗).
- Status enum: `live` 🟢 / `done` ✅ / `in_progress` 🔵 / `planned` 🟡 / `blocked` 🔴.
- Sau mỗi feature xong: `update_feature(id, status='done', progress=100)` → dashboard tự cập nhật.
- **Thêm feature/tool mới TRỰC TIẾP vào `store/features.json`** (đã dùng 16/08 khi đẩy meTelligent lên TFO): schema `{id, name, description, status, owner, progress, url, priority, updated_at}` — status enum `live/done/in_progress/planned/blocked`. Server đọc file mỗi request nên ghi thẳng file là đủ, KHÔNG cần API (API yêu cầu token).
- **Pattern "SPIN" (Quang yêu cầu 16/08 — đẩy product thành tool list + theo dõi Kanban):** khi 1 product/feature có vòng phát triển 2 tuần → tạo task cha trong `store/tasks.json` (title "SPIN <tên>", phase `in_progress`, done_criteria bắt buộc, tags, deadline) + 8 sub-task con (parent_id = task cha, sub_status todo/in_progress). Đánh số `[1]..[8]` theo thứ tự tuần; mỗi sub có done criteria riêng. Cập nhật phase/sub_status khi xong từng bước.
- store/features.json có thể push lên git (không nằm trong gitignore như store/*.json khác — nếu bị ignore thì dashboard public không thấy).

### ⏸ GÁC MỘT SPIN / NHÓM TASK BỊ NGƯNG ƯU TIÊN (2026-08-29, Quang "tạm thời bỏ qua các vấn đề android")

Khi Quang hạ ưu tiên/hủy tạm thời cả 1 nhóm task (vd SPIN meTelligent 2 tuần chờ máy Android thật) — KHÔNG xóa task, KHÔNG để treo in_progress mãi (làm nghẽn standup / ops_guard báo stale):

- Flip thẳng trực tiếp trong `store/tasks.json` bằng script loop: `t['phase']='paused'` + `t['status']='paused'` + `t['paused_reason']='<lý do — Quang quyết ngày>'`. Đóng task cha lẫn task con (cả `parent_id` group). Làm bằng python (ghi JSON), KHÔNG qua worker (paused không phải phase mà agent tự chuyển).
- **`paused` là phase hợp lệ, không-terminal** nhưng phải thuộc nhóm "không report trong standup / không tính STALE". ops_guard STALE chỉ so phase không-terminal ≥48h → nhớ đưa `paused` vào watched set nếu muốn nó im (hiện tại các task paused vẫn có thể lọt vào nếu guard đếm mọi phase≠terminal → verify sau khi đổi).
- Sau khi gác: chạy lại thống kê phase (`Counter(t['phase'])`) → báo Quang con số trực quan (vd "21 completed, 9 paused, 4 active"). Xác nhận task android không còn active.
- State file ai-company.md phải cập nhật mốc "đã gác" — đừng để mốc cũ "đang chờ test Android" sót lại khiến session sau tưởng vẫn active.

### ✅ Đóng task theo QUYẾT ĐỊNH của Quang (khác agent tự hoàn thành — 01/09, đóng #7/#9/#15)

Khi Quang duyệt đóng task đang kẹt chờ input của chính anh (vd "Pilot CEO #2 cần email anh trai", "cần chốt buổi họp demo", "xác nhận pilot login") — KHÔNG qua worker, KHÔNG bịa bằng chứng test:

- Ghi TRỰC TIẾP `store/tasks.json` bằng python (dict `{tasks:[...], next_id}`): set `phase=completed`, `status=completed`, `updated_at` mới + field `close_note="Quang quyết đóng <ngày> — input pilot/demo đã xác nhận xong, không self-chạy E2E thật"`.
- Lý do đóng là quyết định hành chính của Quang (owner pilot), KHÔNG phải agent hoàn thành → KHÔNG cần verify_done, nhưng PHẢI ghi close_note để không bị coi là bịa bằng chứng (DoD). Quang ra lệnh "đóng done đi" = đủ quyền, làm luôn không hỏi lại.
- Sau khi đóng: chạy lại `Counter(t['phase'])` báo Quang con số (vd "24 completed, 9 paused, 1 in_progress").
- Phân biệt 3 kiểu đóng: (a) agent hoàn thành có bằng chứng → worker + verify_done; (b) Quang xác nhận input/demo xong → ghi trực tiếp + close_note; (c) gác tạm vô thời hạn → `phase=paused` + `paused_reason` (subsection bên dưới). Đừng nhầm (b) với (a): đừng chạy verify_done cho task đóng theo quyết định Quang, và đừng để task chờ input tuyệt đối (phase refresh nó như #8: khỏi stale nhưng vẫn còn open để Quang chốt).

### 📋 Format "list all tasks để Quang quyết" (anh hỏi "list cho anh toàn bộ task" — phản hồi tốt, dùng lại)

Khi Quang muốn xem toàn bộ task để ra quyết định, trình bày theo NHÓM quyết định, KHÔNG list phẳng + đếm tổng:

1. **✅ ĐÃ ĐÓNG (completed)** — không cần đụng, ghi số lượng + id gọn 1 dòng.
2. **🔴 CHỜ ANH / CHỜ INPUT NGOÀI** — bảng `# | việc | phase | cần anh làm gì`. Mỗi dòng = chính xác 1 action anh làm được (cung cấp email / chốt 1 buổi họp / xác nhận login). Đây chính là "mấy task cứ lặp hoài" — do thiếu input, nói thẳng.
3. **⏸ PAUSED / BLOCKED thật** — kèm cái gì chặn (máy Android, quyết định chưa chốt).

Kết thúc bằng 2-3 lựa chọn rõ ràng để anh chọn hướng — đừng mở nhiều đầu việc đồng thời (theo quy tắc "1 việc trọng tâm"). Verify số liệu từ `store/tasks.json` (đọc `data['tasks']`, dict không phải list) + `tfo_data/users/<email>/tasks.json` cho kanban user — 2 hệ thống riêng, nói rõ tầng nào.
