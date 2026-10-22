---
name: trello
description: "Trello API via curl/Python: auth (API key + ATTA token), boards/lists/cards CRUD, credential storage."
category: productivity
---

# Trello API Integration

Query and manage Trello boards/lists/cards via the REST API (curl or Python urllib). Use when the user asks to check Trello boards, sync tasks to Trello, or manage cards.

## Auth — the #1 pitfall

Trello requires **TWO credentials**, always:

1. **API key** — 32-char hex string from https://trello.com/power-ups/admin (per app/integration)
2. **Token** — ATTA-prefixed string (76 chars: `ATTA` + 72 hex). Must be generated FOR THAT KEY.

Pass both as query params on every call:
```
https://api.trello.com/1/<endpoint>?key=<KEY>&token=<TOKEN>
```

### Generating a fresh token
Token must be created while logged into the account, scoped to the key:
```
https://trello.com/1/authorize?expiration=never&scope=read,write,account&response_type=token&key=<API_KEY>
```
→ user clicks Allow → copy the ATTA token. A token generated for app A will NOT work with app B's key.

### Diagnostic matrix (learned the hard way)

| Call | Response | Meaning |
|------|----------|---------|
| key only, no token | `invalid token` (400) | Key is VALID, missing token |
| key + wrong/revoked token | `invalid key` (401) | Token doesn't match this key, was revoked, or never existed |
| key + token from another app | `invalid key` (401) | Same as above — regenerate token with THE SAME key |
| `GET /1/tokens/<TOKEN>?key=...` | 404 `token not found` | Token doesn't exist/revoked — definitive check |
| `key + fresh matching token` | 200 | ✅ Working |
| `GET /1/members/me` 200 BUT `GET /1/boards/<short-id>` → 401 | Token+key fine; that specific board NOT accessible to this account | See board-access note below |

**Key insight:** `invalid key` with key+token does NOT mean the key is wrong — it usually means the TOKEN is bad/mismatched. Verify with `key-only` (should say `invalid token`) and the token-info endpoint. Don't ask the user for a new API key until the token is proven bad.

**Board-level 401 vs auth failure (distinct from above).** When `GET /1/members/me` returns 200 and `GET /1/tokens/<TOKEN>` confirms the token is alive, but `GET /1/boards/<shortId>` throws `HTTP Error 401: Unauthorized`, the credentials are FINE — the board is just not accessible to this account (owned by another Trello account / different workspace, closed, or not shared). Do NOT chase token/key errors. Confirm by listing every board the account can see:
```
GET /1/members/me/boards?filter=all&fields=name,id,url,closed
GET /1/members/me/organizations&fields=name,id
```
If the target board isn't in that list, report "no access to this board" and ask which Trello account owns it / to invite the member — not for a new token.

## Credential storage

Save to `~/AppData/Local/hermes/.env`:
```
TRELLO_API_KEY=<32-hex>
TRELLO_TOKEN=ATTA<...>
```
Then read them in scripts from env. This machine's user (ntquang1110) uses these vars.

## Common endpoints

```bash
KEY="$(grep TRELLO_API_KEY ~/AppData/Local/hermes/.env | cut -d= -f2)"
TOKEN="$(grep TRELLO_TOKEN ~/AppData/Local/hermes/.env | cut -d= -f2)"
```

| Purpose | Endpoint | Notes |
|---------|----------|-------|
| Who am I | `GET /1/members/me` | returns id, fullName, username |
| My boards | `GET /1/members/me/boards?fields=name,id,url,closed` | add `filter=all` to include closed |
| Lists on board | `GET /1/boards/<boardId>/lists?fields=name,id,closed` | |
| Cards in list | `GET /1/lists/<listId>/cards?fields=name,id` | |
| Card detail | `GET /1/cards/<cardId>?fields=name,desc,idList` | |
| Create card | `POST /1/cards` | params: idList, name, desc |
| Move card | `PUT /1/cards/<cardId>` | param: idList |
| Update list | `POST /1/lists` | params: name, idBoard |

Use `curl -sG` with `--data-urlencode "key=..." --data-urlencode "token=..."` to avoid URL-encoding issues. For multi-endpoint loops, Python `urllib.request` + `urllib.parse.urlencode` is cleaner (see worked example in references).

## Pitfalls

- `ATTA` token alone is NOT the API key — user often sends only the token thinking it's enough; you must request the hex key too.
- Rate limits: ~10 req/sec burst, 100/10s sustained. Loop over lists sequentially, not parallel.
- Boards may be named slightly differently than the user remembers (e.g. user says "Volden Ops", actual name "Volden - Ops App"). Report the exact name + URL.
- After storing new creds, verify with one `members/me` call before building on them.
- **Verify board bằng API, KHÔNG dùng browser/mockup HTML.** User chốt 07/09/2026 ("em phải dùng API của Trello chứ, không dùng qua trình duyệt"). Muốn cho user thấy board → trả về danh sách list/label/card + URL trực tiếp từ API, đừng dựng mockup HTML trong trình duyệt/phải login.
- **Tạo list/label hàng loạt dính `RemoteDisconnected` transient** giữa chuỗi (kinh nghiệm: fail ở list thứ 6/7 khi POST liên tiếp). Wrap mỗi POST trong retry exponential backoff (4 lần, sleep 2^i); TRƯỚC khi POST bù, GET lại lists hiện có và tái dùng id đã tạo — không tạo trùng.
- **Thứ tự list `pos` KHÔNG theo thứ tự tạo** — Trello gán pos mặc định (256, 512, 1024...) có thể NGƯỢC mong muốn (list tạo trước = pos lớn nhất). Fix: sau khi tạo xong, `PUT /lists/<id> {"pos": (i+1)*65536}` theo thứ tự canonical rồi GET verify sắp theo pos.
- **POST label kèm màu để lại label THỪA tên trống** (chỉ có màu — Trello tự sinh màu trơn ẩn). Verify `GET /boards/<id>/labels`, xoá mọi label có `name` rỗng bằng `DELETE /labels/<id>`.

## References

- `references/volden-board.md` — Volden - Ops App board (live project board, id, lists, workflow)
- `references/b2b-sale-board.md` — B2B Sale board (pipeline bán hàng Kiềm: 7 lists, 6 labels, template card desc, lý do không dùng Custom Fields)
