# CEO Dashboard Review — góc nhìn C-level + UX (TFO 2026-08)

> Derived from user request (2026-08-05): "em review trang chủ của tfo, xem có phù hợp hay chưa, với góc nhìn của C level và UX sử dụng, em đề xuất cho anh".
> User duyệt: giữ Org Chart + Workflow, Mục tiêu editable, còn lại triển khai toàn bộ.

## Framework review dashboard cho người điều hành (C-level)

Khi được yêu cầu review dashboard của 1 tool quản lý, đặt câu hỏi trước khi nhìn code:

1. **Ai mở app mỗi sáng?** CEO mở app muốn 3 thứ: *hôm nay làm gì, có gì chặn, việc gì quá hạn*. Không phải số liệu thống kê dev.
2. **Có thông tin nào SAI người dùng không?** (VD: Org Chart vẽ CTO/PO/PM khi tổ chức thật là Quang + anh Quân + anh Dương; Mục tiêu tuần hardcode "conversion rate 2.1%→3.5%" khi anh làm chăn nuôi/kiềm). 1 câu sai chủ đề ở trang đầu = mất niềm tin.
3. **Công cụ nhập liệu có chiếm vị trí tốt nhất không?** Upload/ghi âm là INPUT — đừng để hero chiếm giữa trang; đưa xuống cuối + nút nổi.
4. **Trạng thái có màu không?** Task quá hạn phải đỏ, task hôm nay vàng, issue mở đỏ — nếu không user phải tự đọc hết.
5. **Có gì là công cụ kỹ thuật lẫn vào dashboard điều hành không?** Agent Skills, workflow dev, org chart dev → tách sang tab "Hệ thống" (ẩn, opacity thấp) hoặc xóa.

## Layout dashboard CEO-first (đã được user duyệt)

```
1. Hàng KPI 4 thẻ (bấm nhảy tab tương ứng):
   ⏰ Task quá hạn (đỏ nếu >0) | 📅 Meeting tuần | ✅ Task hôm nay | 🔴 Issue mở (đỏ)
2. Mục tiêu tuần — editable (nút ✏️ Chỉnh, prompt, lưu goal.json per user)
3. 📌 Hôm nay: cuộc họp hôm nay + task đến hạn hôm nay (check nhanh tại chỗ)
4. ⚠️ Cần chú ý: task quá hạn + issue mở (đỏ)
5. Upload/Ghi âm thu gọn 1 card + nút nổi 🎤 góc phải (scrollIntoView + focus)
6. BỎ: Agent Skills, Org Chart sai, Workflow dev → tab "Hệ thống" riêng
```

### Điều chỉnh theo yêu cầu cụ thể user
- Org Chart + Workflow: user nói "để xem thêm đi" → **giữ nguyên**, không tự xóa.
- Mục tiêu tuần: "vẫn treo mục tiêu lên, cho phép setup" → giữ trên trang + editable, KHÔNG hardcode.
- KPI thẻ bấm nhảy: onclick switchTab('kanban'/'calendar') — 1 chạm vào việc.

## Backend kèm theo (projects/timeline/kanban — TFO app)

Data model cho view theo dự án + timeline + kanban:
- `projects.json`: `{projects: [{id, name, color, created_at}]}` — seed 2 mặc định theo domain user.
- `issues.json`: `{issues: [{id, project_id, meeting_id, title, status: open|in_progress|resolved}]}` — tách riêng khỏi meeting.
- `tasks.json`: thêm `status: todo|in_progress|done` (giữ `done` bool cho tương thích) + `project_id`.
- Meeting: thêm `project_id` + `notes_url` (link Meeting Notes publish).
- `goal.json` per user: `{goal, updated_at}`.
- Endpoint status: `POST /api/tasks/{id}/status` + `/api/issues/{id}/status` — kanban drag&drop chỉ cần đổi status.
- Frontend kanban: HTML5 drag&drop (ondragstart/ondragover/ondrop), 2 board (Task 3 cột, Issue 3 cột), filter theo project.

### Timeline theo project
Gom meetings + decisions (từ meeting.decisions) + tasks theo `created_at`, sort desc,
render dạng timeline dọc (dot màu phân loại: meeting=blue, decision=yellow, task=green),
mỗi meeting có link "Mở biên bản →" khi có `notes_url`.

## Pitfalls
- ❌ Hardcode nội dung sai chủ đề người dùng (VD mục tiêu conversion rate cho người làm chăn nuôi).
- ❌ Để KPI/stat đếm số trống không có màu trạng thái → user không biết việc gì gấp.
- ❌ Tự xóa Org Chart/Workflow khi user chưa duyệt xóa → hỏi trước hoặc để nguyên.
- ❌ Gửi goal qua bash curl bị mất dấu tiếng Việt (encoding) → test bằng Python requests, không bằng curl -d trong git-bash.
- ❌ Browser tool (camofox) không sẵn sàng → test JS bằng `node --check` (trích <script> blocks) + node mock (mock document/fetch/localStorage) + test API thật bằng Python requests; xác nhận đủ 3 tầng rồi mới go live.
