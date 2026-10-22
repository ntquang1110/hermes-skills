---
name: trello-api
description: "Trello REST API via curl: auth (API key + ATTA token), boards/lists/cards CRUD, auth-error diagnosis."
category: productivity
---

# Trello API

Trello REST API via curl. Covers auth setup, common endpoints, and the auth-error diagnostics that cost real time when creds mismatch.

## When to Use

- User says "check board Trello", "có board X chưa", "thêm card", "đồng bộ task ↔ Trello"
- Diagnosing `invalid key` / `invalid token` / `token not found` responses
- Any Trello board read/write (boards, lists, cards)

## Auth — key + token, BOTH required

Trello needs **two** credentials; every request passes both as query params:

```
https://api.trello.com/1/<endpoint>?key=<API_KEY>&token=<TOKEN>
```

| Credential | Format | Where to get it |
|-----------|--------|-----------------|
| `key` (API Key) | 32 hex chars, e.g. `36a4756296b4eae1de268da71f112ea7` | https://trello.com/power-ups/admin → open the integration → API Key |
| `token` | `ATTA` prefix + ~72 hex, e.g. `ATTA6b5b...` | https://trello.com/1/authorize?expiration=never&scope=read,write,account&response_type=token&key=<API_KEY> (logged into the same Trello account) |

**Critical: the token is issued FOR a specific API key.** If you mix a token from app A with a key from app B, the API rejects it. Regenerate the token with the *same* key when this happens.

## Auth-error diagnosis (from real session)

| Request | Response | Meaning |
|---------|----------|---------|
| `?token=<TOKEN>` only | `invalid key` (401) | Token is never enough — key missing |
| `?key=<KEY>` only | `invalid token` (400) | Key is valid; token missing |
| `?key=<KEY>&token=<ATTA>` (mismatched/revoked token) | `invalid key` (401) | **Pair mismatch or revoked token** — key works alone, but key+token fails |
| `GET /1/tokens/<TOKEN>?key=...` | `token not found` (404) | Token itself invalid/revoked — definitive check |
| `key` passed as `token` too | `invalid app token` (401) | Wrong slot |

Diagnostic order: test `key` alone (should give `invalid token`), then test the token endpoint (`/1/tokens/<TOKEN>?key=...`) — `404` means regenerate the token via the authorize URL with the same key.

## Common endpoints

```bash
KEY="<API_KEY>"; TOKEN="<ATTA_TOKEN>"
Q="https://api.trello.com/1"

# Who am I + boards list
curl -sG "$Q/members/me" --data-urlencode "key=$KEY" --data-urlencode "token=$TOKEN"
curl -sG "$Q/members/me/boards" --data-urlencode "key=$KEY" --data-urlencode "token=$TOKEN" --data-urlencode "fields=name,id,url,closed"

# Lists on a board (board id from /members/me/boards)
curl -sG "$Q/boards/<BOARD_ID>/lists" --data-urlencode "key=$KEY" --data-urlencode "token=$TOKEN" --data-urlencode "fields=name,id,closed"

# Cards in a list
curl -sG "$Q/lists/<LIST_ID>/cards" --data-urlencode "key=$KEY" --data-urlencode "token=$TOKEN" --data-urlencode "fields=name,id"

# Create card (name/desc may contain Vietnamese — use --data-urlencode in POST body)
curl -s "$Q/cards" --data-urlencode "key=$KEY" --data-urlencode "token=$TOKEN" \
     --data-urlencode "idList=<LIST_ID>" --data-urlencode "name=<TITLE>" --data-urlencode "desc=<DESC>"

# Attach a local file to a card (multipart)
curl -s -X POST "$Q/cards/<CARD_ID>/attachments" --data-urlencode "key=$KEY" --data-urlencode "token=$TOKEN" \
     -F "file=@path/to/file.docx"

# Move card to another list
curl -s -X PUT "$Q/cards/<CARD_ID>/idList" --data-urlencode "key=$KEY" --data-urlencode "token=$TOKEN" \
     --data-urlencode "value=<LIST_ID>"

# Add comment to card
curl -s -X POST "$Q/cards/<CARD_ID>/actions/comments" --data-urlencode "key=$KEY" --data-urlencode "token=$TOKEN" \
     --data-urlencode "text=<COMMENT>"
```

## Known boards (as of 2026-08-14)

| Project | Board ID | URL | Lists |
|---------|----------|-----|-------|
| Volden - Ops App | `6a6b793f7e5888b26f2ad776` | trello.com/b/l3d1Zx31 | Document, To do, Doing, Testing, Need fixed, Fixing, Done, Cancel |
| Vua Kiềm - Execution | `Rs72dKul` | trello.com/b/Rs72dKul | Project Resources `6a6c46cec81d1c3f8a0c9ff0`, Questions For Next Meeting `...ff1`, To Do `...ff2`, Doing `...ff3`, Blocked `...ff4`, Done `...ff5` |

## Credentials storage convention

Save creds in the Hermes `.env` (NOT in project repos):
```
TRELLO_API_KEY=<key>
TRELLO_TOKEN=<ATTA...>
```
Then `source` or read via Python instead of asking the user each session. Memory entry should reference "creds trong hermes .env" + board IDs, not embed the raw secret.

## Pitfalls

| Issue | Fix |
|-------|-----|
| `invalid key` with both params present | Token belongs to a different app/key. Regenerate token via authorize URL using THIS key |
| `token not found` (404) | Token revoked/expired — get a fresh one |
| User pastes only the ATTA token | That's the *token*, still need the 32-hex *key* — ask for it |
| curl on Windows git-bash | Use `--data-urlencode` for params; keys/tokens are URL-safe hex so plain embedding works, but `--data-urlencode` is safer |
| Card create with Vietnamese name/desc in URL query | Breaks — response is empty/non-JSON. ALWAYS pass `name`/`desc` via `--data-urlencode` in the POST body, never hand-encoded `%20`/diacritics in the query string |
| Card move / comment / attachment | Use POST/PUT with `--data-urlencode` for all text fields (diacritics), `-F file=@...` for attachments |
