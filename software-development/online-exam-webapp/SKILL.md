---
name: online-exam-webapp
description: "Use when building online exam webapps: STT login, gen đề."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [exam, webapp, node, windows, tunnel, admin-dashboard, excel]
    related_skills: [cloudflare-tunnel, impeccable, html-unslop, design-critique]
---

# Online Exam Webapp (Node + JSON store)

Xây app thi trắc nghiệm online: thí sinh nhập STT → trang sẵn sàng → đếm ngược → auto-submit; admin xem live + export Excel. Đã triển khai thật tại `D:/Hermes Proj/dithi` (dithi.thefirstonly.com, port 5100) cho kỳ thi Kiềm K02 (36 HV, 120 câu hỏi, 36 đề gen sẵn).

## Kiến trúc (đã verify)

- **1 file Node server.js** (`node:http` + fs + crypto + ExcelJS), 0 framework. Static từ `public/`, API `/api/*`, dữ liệu JSON trong `data/`.
- **Dữ liệu**: `questions.json` (ngân hàng câu hỏi), `students.json` (STT→tên/CCCD/SĐT), `state.json` (contestants + exams đã gen + admin_tokens).
- **Gen đề**: server start gen N đề (N = số thí sinh), mỗi đề 40 câu theo tỉ lệ teacher (vd Tâm20/Minh15/Dung5), tráo thứ tự A/B/C/D nhưng giữ đáp án gốc, đảm bảo 2 đề không trùng (signature = sorted qid set).
- **Luồng thi**: `enter` (STT, trả token) → `start` (bắt đầu countdown, trả exam) → `save` (autosave 15s) → `submit` (server chấm, không trả điểm cho TS) → `done`. Token lưu localStorage để resume khi refresh/mất mạng.
- **Admin**: login password → overview (poll 5s) → detail từng TS → export Excel 2 sheet (Tổng hợp + Chi tiết đáp án).
- **Deploy**: Cloudflare tunnel (service token-managed, `config_src: cloudflare` → sửa ingress qua API, KHÔNG sửa YAML local — xem cloudflare-tunnel skill).

## Pitfalls (từng gặp thật, phải tránh)

1. **Google Fonts render-blocking = lag 30s ở VN**. `<link href="fonts.googleapis.com">` trong head làm browser chờ timeout ~30s trước khi render. ISP VN chặn/làm chậm Google Fonts. Fix: bỏ hẳn, dùng `system-ui`. Đo TTFB localhost vs tunnel để phân biệt app chậm vs network.
2. **Kill process Windows: kill wrapper KHÔNG giết node con**. `process(action='kill')`/bash `kill` chỉ giết shell bọc, node server vẫn sống giữ state cũ trong RAM → tưởng reset nhưng thí sinh cũ vẫn "đang thi". Fix: `netstat -ano | grep :PORT | grep LISTEN` lấy PID thật → `powershell Stop-Process -Id <PID> -Force` → verify port free. Luôn làm vậy khi reset/deploy lại.
3. **HEAD request trả 404**. Node static server chỉ xử lý GET → một số proxy/browser preflight HEAD nhận 404. Fix: xử lý `GET || HEAD` và `res.end()` không body cho HEAD.
4. **state.json chỉ persist khi có mutation**. Server giữ state trong RAM; xoá file lúc server đang chạy không có tác dụng. Muốn reset: kill server thật → xoá file → start lại.
5. **STT logic**: trạng thái `assigned` (đã nhập STT chưa bấm "Vào thi") phải CHO phép người khác chiếm lại — người chưa start thì chưa xem đề, giữ chỗ vô nghĩa. Chỉ chặn `in_progress` ("đang có người thi") và `submitted` ("đã thi xong"). Thông báo lỗi phải phân biệt rõ 3 case (user yêu cầu).
6. **Auto-submit phải server-enforce**, không tin client countdown: mọi API call (save/submit/overview) check deadline → tự đánh dấu submitted với đáp án đã lưu.
7. **Export Excel**: exceljs `writeBuffer()` → `res.end(Buffer.from(buf))` với `Content-Disposition: attachment`. Thêm cột Họ tên/CCCD/SĐT từ students.json khi user import danh sách học viên.

## Reset kỳ thi (chuẩn, user tự làm được qua admin)

- Admin UI có nút **Reset kỳ thi** (toàn bộ) + **Reset** từng STT, đều có modal confirm (user yêu cầu: tránh bấm nhầm).
- API: `POST /api/admin/reset {all:true}` hoặc `{stt:N}`, yêu cầu Bearer token.
- Reset toàn bộ thủ công: kill PID thật (pitfall 2) → `rm data/state.json` → `node server.js` → gen lại N đề từ questions.json hiện tại.

## Import dữ liệu mới (câu hỏi / danh sách học viên)

- **Câu hỏi**: user gửi Excel cột `teacher, Chương/Bài học, Câu hỏi, A, B, C, D, Đáp án chuẩn` → import script sinh `questions.json` (id = row-1). So sánh bản cũ/mới bằng signature câu hỏi, báo rõ removed/added/changed trước khi import.
- **Học viên**: Excel có `STT, Họ và tên, CCCD, SĐT` → `students.json` map `String(stt)`. Loại bỏ dòng chú thích màu ("màu xanh" = bảo lưu, "màu đỏ" = bỏ thi). STT_MAX tự tính từ max stt trong students.
- Sau import: restart server + xoá state.json để gen lại đề từ ngân hàng mới.

## Verification checklist

- [ ] Benchmark: localhost TTFB <10ms, qua tunnel <1s (nếu 30s → check Google Fonts/external resources)
- [ ] `performance.getEntriesByType('resource')` không còn googleapis/font request
- [ ] HEAD + GET static đều 200
- [ ] Test 3 case STT: assigned cho chiếm lại / in_progress chặn / submitted chặn
- [ ] Test auto-submit: patch started_at về quá hạn → overview thấy submitted+auto
- [ ] Export Excel mở được, đủ cột, đúng số dòng (N STT × 40 câu)
