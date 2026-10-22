---
name: tfo-dashboard
description: "Build/sửa app TFO tfo.thefirstonly.com (port 8100 + HTML)."
---

# TFO Dashboard — TheFirstOnly (Trợ lý CEO voice-first)

## Khi nào dùng
- Build/sửa feature trên app tfo.thefirstonly.com (SPIN TFO, kanban task 26–34, tool list, inbox Hermes↔Claw, task chat + voice, KPI C-level, timeline).
- App nằm trong repo **D:/Hermes Proj/ai-company/** (KHÔNG phải D:/FirstOnly — đó là website profile cũ, port 3000).

## Bắt đầu: đọc state TRƯỚC
1. `D:/Hermes Proj/.hermes-state/tfo.md`
2. `D:/Hermes Proj/.hermes-state/ai-company.md`
3. Chat state theo nhóm: `D:/Hermes Proj/.hermes-state/chat/telegram-group-befounders.md` (SPIN TFO plan + sub-task status)
4. Repo có graft graph → `graft ask "<câu hỏi>" --source` trước khi grep/đọc file (AGENTS.md bắt buộc).

## Kiến trúc
- **Backend:** `app/main.py` — FastAPI, port 8100, chạy qua `run_tfo_v2.py` (dùng `.venv/Scripts/python.exe`, KHÔNG python hệ thống — thiếu deps).
- **Frontend:** `app/static/index.html` — 1 file HTML duy nhất (~3.7k dòng, 6 tab: Dashboard/Lịch họp/Dự án/Kanban/Agent/Hệ thống). `login.html` riêng. Trang hướng dẫn người ngoài: `guide.html` (sub #34 demo).
- **Dashboard có 3 sub-tab (15/09/2026, gọn từ 4):** action bar 3 nút đầu trang (Ghi âm / Tải lên / Nói chuyện, id `dashRecordBtn`/`dashLiveBtn` — gọi `.click()` lên nút ẩn `recordBtn`/`uploadBtn`/`liveTalkBtn` trong `#dashMeeting`) + sub-tab bar (`switchSubTab('overview'|'meeting'|'work')`, nhớ localStorage `tfo_subtab`). Containers: `#dashOverview`, `#dashMeeting`, `#dashWork` (`#dashSystem` đã xóa 15/09, nội dung chuyển lên tab Hệ thống riêng). Card Ghi âm thu gọn: 1 hàng nút + expand `#recordDetail` qua `toggleRecordDetail()` (tiêu đề/ngày giờ auto-fill trong `setDefaultMeetingTime()`, tiêu đề mẫu `Họp T2 15/9`). Các list giới hạn 5 record + nút Xem thêm (`meetingsCache`/`meetingsShowAll` + `toggleMeetings()`, `toolCache`/`toolShowAll` + `toggleToolList()`; card meTelligent đã chôn 15/09 pivot web, giữ endpoint tương thích). `#liveCard` là floating fixed góc phải, PHẢI là con trực tiếp của `<body>` (để sống qua switchTab; để trong `#viewDashboard` sẽ bị parent display:none giết khi đổi tab) — CSS `.live-float{right:16px;max-width:380px}` + media 480px full-width. `#taskOverlay` giữ trong `#viewDashboard`. Tab Hệ thống riêng (`#viewSystem`) gộp KPI + Inbox + Tool + Org/Skills. Chi tiết: `references/dashboard-homepage-redesign-2026-09.md` + `references/ui-compact-audit-2026-09.md`.
- **Auth:** `/api/login` (email + passcode, mặc định `<PASSCODE>`, env TFO_PASSCODE) → cookie `tfo_token`. Endpoint dùng `_resolve_user(token)`; sai token → 401.
- **Data:**
  - `store/*.json` — AI Company: tasks.json (task agent), features.json (tool list), cost.json, activity.json, comms.json
  - `tfo_data/users/<email-safe>/` — task user kanban (tasks.json), meetings.json, task_messages.json, task_queue.json
  - `shared/inbox.py` + `shared/to_claw.json` (Hermes→Claw), `shared/to_hermes.json` (Claw→Hermes) — inbox 2 chiều, tin unread = status `sent`
- **meTelligent tích hợp (sub #32):** đọc thẳng SQLite `D:/Hermes Proj/meTelligent/server/metelligent/data/meetings.db`, bảng `meetings` (id, title, date, tags, status='done'|'recording', corrected_text, full_transcript, created_at, updated_at).

## Workflow chuẩn (đã verify session 16/08)
1. Đọc state → graft orient.
2. Viết backend endpoint trong `app/main.py` (đặt trước `if __name__`; trả `JSONResponse({"error": ...}, status_code=401/400/404)`).
3. **Curl verify endpoint TRƯỚC khi viết JS** — lấy token mới rồi test:
   ```bash
   TOKEN=$(curl -s -X POST http://localhost:8100/api/login -F "email=quang@kiemsaphia.com" -F "passcode=<PASSCODE>" | python -c "import json,sys; print(json.load(sys.stdin).get('token',''))")
   curl -s "http://localhost:8100/api/<endpoint>?token=$TOKEN"
   ```
4. Thêm JS vào index.html; **kiểm tra cú pháp toàn bộ script inline** (script nằm trong SKILL dir, KHÔNG có trong repo):
   ```bash
   node "C:/Users/NTQUANG_DELL/AppData/Local/hermes/skills/software-development/tfo-dashboard/scripts/check_inline_js.js" app/static/index.html
   ```
5. Restart server (lệnh cũ `taskkill //PID` + `nohup ... run_tfo_v2.py` bị lifecycle guard chặn "embedded null character" do path "Hermes Proj" có dấu cách — xem `references/dashboard-homepage-redesign-2026-09.md`):
   ```bash
   # Kill: PowerShell, không taskkill (git-bash nuốt dấu /)
   powershell -NoProfile -Command "Stop-Process -Id <PID> -Force"   # PID: netstat -ano | grep :8100 | grep LISTENING
   # Start: wrapper script ở thư mục KHÔNG dấu cách, background=true
   cd "/d/Hermes Proj/ai-company" && "/d/Hermes Proj/ai-company/.venv/Scripts/python.exe" "C:/Users/NTQUANG_DELL/httptmp/tfo_start_server.py" > "C:/Users/NTQUANG_DELL/httptmp/tfo_server_v2.log" 2>&1
   # Verify
   curl -s http://127.0.0.1:8100/api/health
   ```
6. Verify lại endpoint + browser test (login → render card mới → console sạch).
7. Commit + đóng task trong `store/tasks.json` (status → done, phase → completed) + cập nhật state files.

## Pitfalls
- **Gõ tiếng Việt có dấu** — mọi output JSON/UI. Heredoc QUOTED giữ dấu.
- **`store/tasks.json`, `store/*.json`, `tfo_data/` bị .gitignore** — đóng task (status→done) là thay đổi DATA trên disk, KHÔNG commit được (`git add` báo ignored). Đừng cố `git add -f`; chỉ commit file code (app/main.py, app/static/*.html). Bằng chứng đóng task = đọc lại file + endpoint trả OK, không phải commit.
- **Đừng vẽ UI trên API chưa tồn tại** — luôn curl verify trước, tránh dựng card chết.
- Voice task: endpoint `/api/tasks/{id}/voice` transcribe qua Groq; file giả/không phải giọng nói → hallucination "Hãy subscribe..." — không phải bug. Có sẵn `_is_silent_audio()` (ffmpeg volumedetect) chặn file câm → không tốn Groq quota.
- TFO sub-task SPIN: track trong `store/tasks.json` (task 26 parent, sub 27–34) + Kanban AI. Đóng sub phải kèm bằng chứng (endpoint trả OK / commit / browser verify).
- `esc()` cho mọi chuỗi user content khi render HTML (tránh vỡ onclick/HTML injection).
- Kanban: task user mode='kanban', task AI mode='agent' (file `_ai_store` tasks.json riêng) — đừng nhầm 2 nguồn.
- Route public (không cần token) như `/guide` phải thêm vào main.py cùng `response_class=HTMLResponse`, không được tự phục vụ từ static.
- Auto-critique sub #30: backend đã có sẵn — khi tạo task agent mode, main.py append critique_prompt (tự hỏi/làm rõ/phản biện) vào thread + enqueue. Verify = giao task → xem agent (CTO) trả lời critique trong `/api/tasks/{id}/messages`, KHÔNG cần viết thêm code.
- **Restructure block lớn trong index.html → dùng transform script, không patch tay**: cắt block theo marker comment duy nhất, sắp xếp lại, ghi đè + sanity check đếm `id="..."` cho MỌI id quan trọng (bắt lỗi double-wrap). Backup `.bak-dash-tabs` trước khi chạy. Chi tiết + script mẫu: `references/dashboard-homepage-redesign-2026-09.md`.
- **Patch tool escape-drift**: old_string chứa regex JS có `\"`/`\\[` (vd `replace(/[{}\"\\[\\]]/g, '')`) bị từ chối. Workaround: patch NHỎ quanh dòng regex, không đụng dòng đó.
- **Giới hạn list theo array, không split('\n')**: template literal của mỗi row có newline nội bộ → `rowsAll.split('\n').slice(0,8)` vỡ row. Build array rồi `rows.slice(0,8)`.
- **Lifecycle guard chặn lệnh chạy server từ path có dấu cách** ("Hermes Proj"): mọi lệnh background trỏ `.py` hoặc redirect `>` vào `D:/Hermes Proj/...` crash "embedded null character in path". Workaround: wrapper script + log ở thư mục không dấu cách (`C:/Users/NTQUANG_DELL/httptmp/`). Kill process bằng PowerShell `Stop-Process`, không `taskkill //PID` (git-bash path-conversion).

- Voice: `app/streaming.py` (StreamSession VAD + cổng tần số FFT 300-3400Hz chống hallucinate tạp âm), `app/router.py` + `app/rag.py` (Phase B: classify chat/rag/execute + RAG answer cite nguồn), `app/tts.py` (VieNeuProvider "Thanh Bình" mặc định via HTTP Mac 8899, edge fallback), `app/turn_manager.py`, `app/voice_lemma.py` (normalize tên riêng VN). Đã tách 2 nút "Nói chuyện trực tiếp" vs "Ghi âm" (07/09). Chi tiết + verify: `references/live-voice-ws.md`.

## Support files
- `scripts/check_inline_js.js` — node script kiểm tra cú pháp toàn bộ `<script>` inline trong file HTML (chạy bằng `node`, không cần npm install).
- `references/dashboard-homepage-redesign-2026-09.md` — redesign homepage 13/09 (ĐÃ TRIỂN KHAI): cấu trúc action bar + 4 sub-tab, kỹ thuật transform script (marker comment + sanity check id), restart server 8100 bị lifecycle guard (wrapper script không dấu cách), pitfalls patch (escape-drift, slice array vs split).
- `references/live-voice-ws.md` — module live-voice WS (streaming.py/tts.py/turn_manager/voice_lemma) + luồng up/down + ngắt lời + quyết định tách nút (07/09): "Nói chuyện" vs "Ghi âm/upload meeting", swap giọng sang VieNeu "Thanh Bình".
- `references/ui-compact-audit-2026-09.md` — audit UI gọn theo 3 câu (list rút ngắn / record gọn / view vấn đề nhanh nhất): checklist grep + lỗi cấu trúc cấm lặp (task 3 nơi, tab trùng tên, dead card sau pivot, live card floating).
- `references/dictation-quick-web-2026-09.md` — pivot all-web 15/09: bỏ Android, dictation thành nút Nói nhanh trong TFO (startQuickDictation → /api/transcribe→summarize), 9 task meTelligent đóng, các kênh voice trong TFO.
- `references/spin-tfo-api.md` — API surface 5 endpoint SPIN TFO 16/08 (/api/inbox, /api/inbox/{id}/read, /api/inbox/read-all, /api/kpi, /api/metelligent/meetings) + schema trả về + cách read thẳng meTelligent SQLite.
