---
name: trello-workflow
description: "Trello board ops via REST API + card lifecycle conventions + user Quang's workflow rules (plan-before-code, agent→Testing, tester→Done)."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [trello, kanban, workflow, project-management, api]
---

# Trello Workflow

Manage Trello boards (Volden Ops, Vua Kiềm) via the REST API and follow the user's
card-lifecycle conventions. This is the governing skill whenever a task card is
created/moved/commented on Trello.

## Auth

Credentials live in the Hermes `.env` (NOT in any project `.env`):

- `TRELLO_API_KEY` — 32-char hex API key
- `TRELLO_TOKEN` — ATTA-prefixed token (Atlassian format)

Both are required for every request:
```
https://api.trello.com/1/...?key=<API_KEY>&token=<TOKEN>
```

### Auth failure signatures (diagnose fast)
| Response | Meaning |
|----------|---------|
| `invalid token` (400) with key only | Key OK, token missing |
| `invalid key` (401) with key+token | Token doesn't match this key / revoked — regenerate |
| `token not found` (404 on `/1/tokens/<t>` ) | Token expired/revoked |
| `invalid app token` | Passed key as token — wrong field |

To mint a fresh token for a key:
`https://trello.com/1/authorize?expiration=never&scope=read,write,account&response_type=token&key=<API_KEY>`

## Boards (known)

| Board | ID | URL |
|-------|-----|-----|
| Volden - Ops App | `6a6b793f7e5888b26f2ad776` | trello.com/b/l3d1Zx31 |
| B2B Sale | `6a9e30aa11891777725b9a0e` | trello.com/b/jdP0O9AQ |
| Vua Kiềm - Execution | `Rs72dKul` | — |

Volden lists (canonical order): Document → To do → Doing → Testing → Need fixed → Fixing → Done → Cancel

B2B Sale lists (canonical order, dựng 09/2026): Lead / Khách tiềm năng → Đã liên hệ → Đã báo giá →
Đàm phán → Chốt đơn → Thất bại → Chờ quyết định. Labels: Lợn (blue), Gia cầm (yellow),
Thủy sản (orange), Trâu bò (purple), Đại lý/NPP (red), Trại trực tiếp (green).
Card template (desc, format đã chốt với Quang): `📍 Khách / 👤 Người liên hệ / 📞 SĐT-Zalo /
🏠 Loại khách [Trại trực tiếp | Đại lý | NPP] / 🐖 Vật nuôi + SL chuồng / 📦 Sản phẩm quan
tâm / 🛒 SL dự kiến / 💵 Đơn giá đề xuất / 📝 Nhu cầu-băn khoăn / 📎 Link báo cáo /
🗓 Next step + ngày`. Tiêu đề card: `[Khách] - [Sản phẩm] - [SL] - [Loại]`.

**Dựng board mới từ đầu (bootstrap):** POST /lists theo thứ tự mong muốn nhưng API trả
`pos` theo kiểu nhân đôi ngược (256, 512, ... 16384) → thứ tự hiển thị bị ĐẢO so với thứ tự tạo.
Sau khi tạo hết, phải `PUT /lists/<id> {pos: (i+1)*65536}` theo đúng thứ tự mong muốn.
Khi tạo label có tên qua API, trello GIỮ SẴN 6 label trống (chỉ có màu) → board có thể có
12 label (6 có tên + 6 trống). Dọn: `DELETE /labels/<id>` cho label `name` rỗng.
Cách làm gọn: script python đọc creds từ ~/AppData/Local/hermes/.env, tạo lists + labels,
rồi 1 script verify lại `GET /boards/<id>/lists` theo `pos` + liệt kê labels → sửa trước khi báo xong.

## Card lifecycle — USER RULES (do not deviate)

```
New card (any list)          → READ → LÊN PLAN → present to user → wait "triển khai đi" → code
Bug in "Need fixed"          → fix immediately (no long plan needed) → back to Testing
Code finished                → move card to TESTING (NEVER Done yourself)
Tester / user tests          → only then move to Done
Tester finds bug             → card to Need fixed → fix → Testing again
User says "trừ X"            → exclude those cards/features from scope
```

Key invariants:
- **Never move a card to Done.** That is the tester's/user's call.
- **Never code a new card without presenting a plan first.** Exception: bugs already in Need fixed.
- Move cards strictly along the lifecycle — don't jump lists arbitrarily.
- After finishing a card, comment on it with the commit hash + status so the tester knows what changed.

## API recipes

Move card to a list:
```bash
curl -X PUT "https://api.trello.com/1/cards/<CARD_ID>?key=K&token=T&idList=<LIST_ID>"
```

Add comment:
```bash
curl -X POST "https://api.trello.com/1/cards/<CARD_ID>/actions/comments?key=K&token=T&text=<URL-encoded>"
```

Read board (lists + cards in one pass):
```bash
curl -sG "https://api.trello.com/1/boards/<BOARD_ID>/lists"  -d "key=K" -d "token=T" -d "fields=name,id"
curl -sG "https://api.trello.com/1/boards/<BOARD_ID>/cards" -d "key=K" -d "token=T" -d "fields=name,id,idList,url,desc"
```

## Card triage — Need fixed / Testing re-opens

Khi card đã "fixed" nhưng tester đẩy về Need fixed, đừng chỉ đọc desc — desc thường là template rỗng. Đọc ACTIONS của card để lấy toàn bộ lịch sử:

```bash
curl -sG "https://api.trello.com/1/cards/<CARD_ID>/actions" -d "key=K" -d "token=T" -d "filter=commentCard,updateCard,createCard" -d "limit=30"
```

Parse theo thứ tự thời gian → thấy: ai tạo (createCard), ai move qua list nào (updateCard listAfter/listBefore), comment fix cũ (kèm commit hash), comment mô tả lỗi THẬT của tester (thường là comment cuối cùng sau move về Need fixed). Comment của tester là nguồn chân lý — đôi khi họ tự hỏi "đây có phải bug hay tính năng?" → cần chốt logic nghiệp vụ với user TRƯỚC khi code, không tự ý sửa theo giả định.

Có sẵn script python gọn hơn (parse sẵn card + actions, strip `\r`, không dính bash-loop pitfall): `scripts/fetch_card.py <shortLink_or_id>` — chạy trực tiếp từ skill scripts dir, không cần copy.

Lưu ý: fix code PASS build KHÔNG đồng nghĩa tester chấp nhận — card vẫn có thể bị trả về vì root cause ban đầu sai (fix nhầm tầng) hoặc vì UX không đúng kỳ vọng (vd button scroll thay vì redirect như yêu cầu card).

**Re-open LẦN 2 (card đã fix ĐÚNG vẫn về Need fixed lần nữa — gặp 3 card cùng lúc 2026-08-11):** comment tester mới thường mô tả LỖI KHÁC trên cùng card, không phải lỗi cũ chưa hết (vd NPP button đã redirect đúng nhưng ẩn khi count=0; phiếu xuất kho hết lỗi cũ nhưng dính 403 role). Đừng giả định lỗi giống lần trước — đọc comment mới nhất, triage lại từ đầu. **Một comment tester có thể chứa NHIỀU lỗi (2-3 issue trên 1 card)** — liệt kê từng cái và fix đủ, đừng bỏ sót cái nào.

**Card không tái hiện được từ code — hỏi tester mã đơn TRƯỚC khi fix (2026-08-12):** Khi BUG không tìm ra nguồn trong code/rules/DB (vd card "tặng nhầm bục trưng bày": rà toàn bộ rules_config + engine + frontend compute + production bundle, không rule nào tặng bục) → **ĐỪNG fix theo giả định**. Quy trình: 1) quét nguồn dữ liệu trước (rules DB → engine → frontend compute → production bundle → data đơn thật; gift không khớp rule = thêm tay); 2) không ra nguồn → move card sang list **Need explanation** (Volden board id `6a734f50c60866066bbb8d99`) + comment hỏi tester **order ID** + bước tái hiện đầy đủ; 3) có mã đơn mới trace được nguồn chính xác rồi fix. Tránh fix nhầm tầng gây vòng lặp Need fixed.

## Watchdog pattern (new-card notifications)

To auto-notify when a card is created, use a Hermes cron job with `no_agent=true` and a
poll script (watchdog pattern: empty stdout = silent, non-empty stdout = message):

- Script must live in `~/.hermes/scripts/` and the cron `script` field takes just the filename.
- Script polls the tracked lists, diffs against a JSON state file, prints only when a new card appears.
- First run = baseline (record state, don't spam existing cards).
- Schedule `*/15 * * * *`, deliver to origin chat.

See `scripts/trello_watch.py` in this skill for a working implementation (Volden board,
tracks To do / Need fixed / Document / Testing).

## Pitfalls

- **Batch API tạo lists/labels dễ dính `RemoteDisconnected` giữa chừng (transient).** Loop nhanh POST liên tiếp 5+ request → request giữa chừng bị đứt ("Remote end closed connection"). KHÔNG chạy lại từ đầu (nhân đôi dữ liệu). Pattern: script retry với backoff 2^i, và TRƯỚC khi POST từng item thì GET danh sách hiện có để bỏ qua phần đã tạo (idempotent bootstrap). Cuối cùng verify `GET /boards/<id>/lists` theo `pos` — thứ tự thật chứ không theo thứ tự tạo.
- **`GET /boards/<shortId>` trả 401 → board chưa được share cho account này, KHÔNG phải token hỏng.** Khi user đưa link board mới: chạy `GET /members/me/boards?filter=all&fields=name,id,url` trước — thấy board trong danh sách thì mới gọi trực tiếp. 401 + "board không có trong members/me/boards" = user chưa add member; báo lại chờ user add rồi check lại (verified: B2B Sale 09/2026 — add member xong là 200, không cần đổi token).
- **Windows `.env` CRLF: values có trailing `\r`.** Đọc creds qua `grep | cut -d= -f2-` giữ nguyên `\r` ở cuối → card ID/board ID dính `\r` làm URL sai + JSON parse fail (curl lỗi, python json.loads fail). LUÔN strip: thêm `tr -d '\r'` vào pipeline đọc .env, hoặc dùng python `v.rstrip()`. Dấu hiệu: request chạy nhưng trả lỗi không giải thích được, hoặc ID in ra trông có dấu xuống dòng dính.
- Cron script paths must be relative to `~/.hermes/scripts/` — absolute or
  `~/AppData/...` paths are rejected by the cron tool.
- On Windows git-bash, `/tmp` resolves oddly for scripts; write test scripts inside the
  project `scripts/` dir instead.
- Card descs from the API use markdown; strip newlines before putting them in a message.
- Khi user nói "naughty" / "bắn về cho em" / "bắn notification" → nghĩa là watch/notification
  báo card mới, KHÔNG phải list "Need fixed". Trả lời bằng cách xác nhận cơ chế watch đang chạy.
- Watch chỉ bắn card THỰC SỰ mới (chưa từng xuất hiện trong state); card move giữa các list
  không bị bắn lại — nếu cần theo dõi sự thay đổi list thì script phải so sánh list mỗi tick.
- Attachment preview download từ Trello có thể 401 dù gửi key+token (board private, preview URL
  cần quyền riêng) — đừng mất thời gian tải ảnh tester đính kèm; comment text + đọc source code
  thường đủ để xác định root cause, ảnh chỉ để confirm UI nếu tải được.

