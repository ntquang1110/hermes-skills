# Lark Approval API — duyệt phiếu hàng loạt (key KSP)

Tested 09/08/2026 với app KSP (tenant_access_token). MCP preset mặc định KHÔNG expose tool approval, nhưng package `@larksuiteoapi/lark-mcp` có sẵn `approval.v4.*` (xem `dist/mcp-tool/tools/en/gen-tools/zod/approval_v4.js`). Dùng thẳng REST qua curl/python nhanh hơn, không cần restart gateway.

## Lấy token

```bash
POST https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal
body: {"app_id": <KSP_MCP_APP_ID>, "app_secret": <KSP_MCP_APP_SECRET>}  # từ ~/AppData/Local/hermes/.env
```

## ⚠️ PITFALL #1 — `tasks/search` là BẪY, dùng `tasks/query` mới đúng

`POST /approval/v4/tasks/search` trả về **TOÀN BỘ task lịch sử của user** (5.350 task, gồm cả phiếu đã kết thúc từ >1 năm), không phải danh sách đang chờ. Approve các task này → lỗi `1390001 "Current approval process has ended"`.

**Endpoint ĐÚNG cho "to do" (đang chờ duyệt):**

```bash
GET https://open.larksuite.com/open-apis/approval/v4/tasks/query?user_id=<open_id>&topic=1&page_size=100&user_id_type=open_id
```

- `topic=1` = TodoApproval (待办审批). Các topic khác: 2=DoneApproval, 3=InitiatedApproval, 17=UnreadNotice, 18=ReadNotice.
- Chỉ trả task THẬT đang chờ user xử lý (09/08: 38 task, không phải 5.350).
- Response nằm ở `data.tasks[]` (KHÔNG phải `task_list`), paginate bằng `page_token`.
- Field mapping (KHÁC tasks/search):
  - `definition_code` → dùng làm `approval_code` khi approve
  - `process_code` → dùng làm `instance_code` khi approve
  - `definition_name` → loại phiếu (vd "Yêu cầu duyệt chi", "Phiếu bán hàng")
  - `task_id`, `initiator_names`, `status` (1 = pending)

## Approve 1 phiếu

```bash
POST https://open.larksuite.com/open-apis/approval/v4/tasks/approve?user_id_type=open_id
body: {"approval_code": <definition_code>, "instance_code": <process_code>, "user_id": "ou_...", "task_id": "...", "comment": "..."}
```

- `accessTokens: ['tenant']` — tenant token OK.
- `form` chỉ cần nếu process có conditional branch (JSON serialized string).
- Success → `{"code": 0, "msg": "success"}`.

## ⚠️ PITFALL #2 — lỗi thường gặp

| Lỗi | Ý nghĩa | Cách xử |
|-----|---------|---------|
| `1390001 Current approval process has ended` | Task đã duyệt/đã kết thúc trước đó | Bỏ qua — dùng tasks/query topic=1 thì không gặp |
| `230001 invalid receive_id` | Email không match user trong tenant | Dùng email domain công ty hoặc open_id (xem lark-mcp-2026-08.md) |
| `99992402 field validation failed` | Thiếu param bắt buộc (instances/search cần approval_code + start_time + end_time) | Dùng tasks/query thay thế |
| `99991663 invalid access token` | GET /approval/v4/approvals không chạy với tenant token | Không dùng endpoint này, lấy loại phiếu từ tasks/query response |
| `60001 request param miss` | Body thiếu field (instances/search thiếu user_id/offset/limit/sort_asc) | Dùng tasks/query |

## Batch pattern đã chạy (09/08)

- Script: `~/AppData/Local/hermes/scripts/collect_lark_approvals.py` — paginate hết, lọc pending + loại trừ theo tên phiếu, lưu `cache/lark_to_approve.json`.
- Lần chạy đầu: dùng sai tasks/search → 5.350 task, approve phần lớn fail "process ended". **Sửa lại bằng tasks/query topic=1 → 38 task thật, approve 15+8+2+1 = 26 phiếu OK (Phiếu bán hàng + Yêu cầu nhập/xuất kho), loại trừ 23 "Yêu cầu duyệt chi".**
- Phiếu bán hàng MỚI xuất hiện liên tục khi đang duyệt (cùng user tạo) — sau khi approve xong 1 đợt nên query lại 1 lần nữa để bắt phiếu mới, hoặc đề xuất cron.

## Lưu ý an toàn (bắt buộc)

- Approve KHÔNG hoàn tác được — phiếu chuyển ngay sang bước duyệt kế tiếp.
- User có thể yêu cầu LOẠI TRỪ loại phiếu nhất định (vd "Yêu cầu duyệt chi" = chi tiền) — lọc theo `definition_name` TRƯỚC khi approve, và báo cáo số liệu + phân loại cho user duyệt TRƯỚC khi approve hàng loạt.
