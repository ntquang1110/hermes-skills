# CEO Operating Plan — session 08/09/2026 (C-Lev Development)

Quang: "Dựng cho anh plan để run company as ceo đi". Kết quả: plan 8 mục, publish link
https://preview.thefirstonly.com/qzv4a1rmp747 , master file `D:/Hermes Proj/ai-company/shared/ceo-operating-plan.md`
(+ .html). CHƯA commit vào git shared/ (chờ Quang duyệt).

## Workflow đã chạy (verify đúng)

1. skill_view ai-company-ops → đọc state `D:/Hermes Proj/.hermes-state/ai-company.md` (đọc bằng `cat` vì read_file báo binary do encoding), `shared/launch_plan.md`, `store/goals.json` + `store/okrs.json`, head `shared/workspace.md`.
2. Đếm task thật từ state: 32 completed / 9 paused / 4 planning (#43-46) / 1 in_progress (#8 QA). Goal #3 active deadline 09/08 đã quá hạn.
3. Viết plan 8 mục (cấu trúc ở SKILL.md). Giữ số liệu thật, không bịa; ước lượng thời gian anh bỏ ra (30 phút/ngày, 1 buổi sáng cho 6 quyết định) để anh thấy chi phí quyết định.
4. Publish: `md-to-html.py --file plan.md --output plan.html` rồi `content-upload.py --file plan.html --title "..."` → preview URL KV. Verify bằng browser_navigate: snapshot đủ heading/table, browser_console 0 js_errors.
5. Flush state: tạo `chat/telegram-group-c-lev-development.md` + thêm pointer vào `ai-company.md`.

## Queue quyết định chờ Quang (08/09) — mẫu "bảng quyết định NGAY"

| Việc | Trạng thái | Cần anh làm |
|------|------------|-------------|
| #43-46 | planning, LẶP #35-42 đã đóng | chốt ĐÓNG |
| #8 QA | in_progress | test meeting thật 2 thiết bị, 10 phút |
| deepseek-v4-pro | disabled trên OpenCode Go (401) | bật pro / đổi GLM-5.3, Kimi K3 / kệ flash |
| Pilot CEO #2 | chờ email | cung cấp email, mở tài khoản |
| H1 voice end-to-end | chờ test thật | ghi 1 cuộc họp thật mic → RAG → giọng Thanh Bình |
| Goal #3 | deadline 09/08 quá hạn | giữ hay thay goal mới |

## Bài học

- Mở đầu plan bằng "3 câu anh chỉ cần nhớ" (read báo cáo sáng / tin bằng chứng / đèn xanh mới launch) — Quang đọc 10 giây là nắm được.
- Mục "phản biện plan" là bắt buộc trong mọi plan cho Quang (trade-offs, rủi ro, bottleneck thật).
- Plan CEO ≠ plan kỹ thuật: không task 2-5 phút, không code. Là operating system cho CEO: việc nào máy lo, việc nào anh chốt.