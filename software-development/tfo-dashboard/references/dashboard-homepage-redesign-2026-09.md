# TFO Dashboard homepage — ĐÃ TRIỂN KHAI (13/09/2026, live trên 8100)

Bản trước của file này là kế hoạch chờ duyệt. Quang duyệt "triển khai toàn bộ" → đã làm xong. Đây là record thực thi + kỹ thuật dùng lại được.

## Kết quả
Dashboard từ 5647px (5.4 màn) → action bar + 4 sub-tab, mỗi sub-view 1-2 màn. Verify browser: chuyển sub-tab được, list giới hạn 5 + Xem thêm, liveCard overlay nổi được từ mọi sub-tab.

## Cấu trúc triển khai
- **Action bar** `.dash-actions` > 3 `.dash-action` (id `dashRecordBtn`/`dashLiveBtn`). Nút gọi `document.getElementById('recordBtn').click()` — nút thật nằm trong `#dashMeeting` (display:none) nhưng DOM tồn tại nên `.click()` chạy handler có sẵn, KHÔNG viết lại logic.
- **Sub-tab bar** `.subtab-bar` > `.subtab-btn` (id `subtabOverview/Meeting/Work/System`) → `switchSubTab(st)` toggle display 4 container + class active + localStorage `tfo_subtab`; restore trong `initApp()` sau `switchTab(saved)`.
- **Containers**: `#dashOverview` (KPI row1 + Mục tiêu tuần + Hôm nay + Cần chú ý), `#dashMeeting` (Nói chuyện + Ghi âm/Upload + Lịch sử + meTelligent), `#dashWork` (Task & Quyết định), `#dashSystem` (KPI row2 C-level + Inbox + Tool list).
- **Overlay PHẢI là con trực tiếp của #viewDashboard**, không nằm trong container display:none: `#liveCard` (class `.live-float`, position:fixed bottom, hiện khi nói chuyện từ MỌI sub-tab) + `#taskOverlay` popup. Element fixed trong parent display:none = biến mất vĩnh viễn.
- **Limit record**: `meetingsCache`/`meetingsShowAll` + `toggleMeetings()` (5 + Xem thêm); `metShowAll` + `toggleMetMeetings()` (`done.slice(0,5)`); `toolCache`/`toolShowAll` + `toggleToolList()` (`rows.slice(0,8)`); today/attention `slice(0,5)` + dòng note.
- **Sync action bar**: record handler cập nhật `dashRecordLabel` + class `recording`; live handler cập nhật `dashLiveLabel` + class `live` (guard `if (el)` vì action bar mới thêm sau).

## Kỹ thuật: transform script cho file HTML 3.7k dòng
Không patch tay 186 dòng HTML (rủi ro sai old_string). Dùng python script:
1. `cp app/static/index.html app/static/index.html.bak-dash-tabs`
2. Cắt block `#viewDashboard` theo marker comment duy nhất (`<!-- KPI 4 thẻ`, `<!-- Inbox 2 chiều`, `<!-- Tool list -->`, ...), slice từng phần theo cặp marker kế tiếp → sắp xếp lại thứ tự → wrap vào container sub-tab → ghi đè.
3. **Sanity check bắt buộc**: đếm `out.count('id="<id>"')` cho MỌI id quan trọng — bắt lỗi double-wrap (id xuất hiện 2 lần vì wrap 2 tầng, getElementById trả phần tử đầu → sub-tab chết).
- Script mẫu: `C:/Users/NTQUANG_DELL/httptmp/tfo_restructure.py`.

## Restart server 8100 — lệnh cũ ĐÃ HỎNG (lifecycle guard)
`taskkill //PID` fail trong git-bash; `nohup .venv/Scripts/python.exe run_tfo_v2.py > tfo_server_v2.log 2>&1 &` crash lifecycle guard `open: embedded null character in path` (guard đọc path có dấu cách "Hermes Proj" + file script). Cách chạy được (verify 13/09):
1. Kill: `powershell -NoProfile -Command "Stop-Process -Id <PID> -Force"` — PID qua `netstat -ano | grep ":8100" | grep LISTENING`.
2. Wrapper script ở thư mục KHÔNG dấu cách: `C:/Users/NTQUANG_DELL/httptmp/tfo_start_server.py` (nội dung: `sys.path.insert(0, r'D:\Hermes Proj\ai-company')` + `uvicorn.run('app.main:app', host='0.0.0.0', port=8100)`).
3. Start background: `cd "/d/Hermes Proj/ai-company" && "/d/Hermes Proj/ai-company/.venv/Scripts/python.exe" "C:/Users/NTQUANG_DELL/httptmp/tfo_start_server.py" > "C:/Users/NTQUANG_DELL/httptmp/tfo_server_v2.log" 2>&1` — redirect log cũng phải path không dấu cách.
4. Verify: `curl -s http://127.0.0.1:8100/api/health` → HTTP 200.

## Pitfalls khi patch file này
- **Patch tool escape-drift**: old_string chứa regex JS có `\"` / `\\[` (vd `replace(/[{}\"\\[\\]]/g, '')`) bị từ chối "Escape-drift detected". Workaround: patch NHỎ quanh dòng regex (thêm global, sửa slice trước/sau), không đụng dòng regex.
- **Không dùng `rowsAll.split('\n').slice()`** để giới hạn tool rows — template literal mỗi row có newline nội bộ, cắt theo dòng = vỡ row. Phải build array rồi `rows.slice(0, 8)`.
- **`check_inline_js.js` nằm trong skill dir** (`C:/Users/NTQUANG_DELL/AppData/Local/hermes/skills/software-development/tfo-dashboard/scripts/`), KHÔNG có trong repo — `node scripts/check_inline_js.js` từ repo fail MODULE_NOT_FOUND. Chạy: `node "<skill dir>/scripts/check_inline_js.js" app/static/index.html`.
