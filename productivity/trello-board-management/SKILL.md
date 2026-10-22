---
name: trello-board-management
description: Manage Trello boards via REST API — connect with app key + token, read boards/lists/cards/members, create/update/move cards. Use for Quang's Vua Kiềm - Execution board and any Trello project management.
---

# Trello Board Management

## When to use
- User asks to connect to / manage Trello boards (Vua Kiềm - Execution, Nhân sự, Quang)
- Read cards, create tasks, move cards between lists, manage members

## Credentials
- App key: `b87ed042f59f442b9d5f8f12b5a5a5b0`
- Token: `ATTAa1ab4706ad488f94f5feb7870cc439802441f418124f92c618f56977e2bfafcf6F83CAED`
- Owner: Nguyễn Thành Quang (@ntquang_kiemsaphia, <EMAIL>)
- Credentials live in memory entry `Trello VK` — check there first, never ask user again unless token invalid.

## Getting a token (only if missing/invalid)
Open in user's browser (must be logged into Trello):
```
https://trello.com/1/authorize?expiration=never&scope=read,write,account&response_type=token&key=<APP_KEY>&name=HermesAssistant&return_url=https://hermes-agent.nousresearch.com
```
User clicks **Allow** → token shown on screen → paste back. `expiration=never` = permanent token.

## API basics
- Base: `https://api.trello.com/1/<resource>?key=<KEY>&token=<TOKEN>`
- Every call needs `key` + `token` params.
- Board short-links (e.g. `Rs72dKul`) work directly as board ID in API paths.

## Core endpoints
```bash
# Verify connection (returns member profile)
curl -s "https://api.trello.com/1/members/me?key=K&token=T"

# List boards
curl -s "https://api.trello.com/1/members/me/boards?key=K&token=T&fields=name,url,idOrganization,dateLastActivity"

# Lists of a board
curl -s "https://api.trello.com/1/boards/<BOARD>/lists?key=K&token=T&fields=name,closed"

# Cards of a board (include idList, due, labels)
curl -s "https://api.trello.com/1/boards/<BOARD>/cards?key=K&token=T&fields=name,idList,closed,due,labels"

# Members of a board
curl -s "https://api.trello.com/1/boards/<BOARD>/members?key=K&token=T&fields=fullName,username"
```

## Write operations
```bash
# Move card to another list (value = list id)
curl -s -X PUT "https://api.trello.com/1/cards/<CARD_ID>/idList?key=K&token=T&value=<LIST_ID>"

# Add a comment — MUST use --data-urlencode, NOT ?text= in the URL
curl -s -X POST "https://api.trello.com/1/cards/<CARD_ID>/actions/comments?key=K&token=T" \
  --data-urlencode "text=Landing v1 done: https://... (passcode: xyz)"
```
Find card id: list cards, then filter by name with python (don't guess ids).
Parse compactly, never dump raw JSON:
```bash
curl -s "...&fields=name" | python -c "import json,sys; [print(f\"- {l['name']}\") for l in json.load(sys.stdin)]"
```

## Pitfalls
- Response `invalid token` = key is VALID, token missing/expired → re-authorize (key problem would give a different error).
- **Comments with Vietnamese diacritics / `:` / URLs fail in the query string** (`?text=...`) → always `--data-urlencode "text=..."` with `-X POST`. Raw `-d` with special chars also breaks JSON parsing of the response.
- **After moving a card, re-read it to confirm** — the PUT returns the card silently; verify `idList` changed.
- Card API returns raw `idList` — always fetch lists first and map id → name before reporting.
- Filter `closed=false` when listing — closed items pollute output.
- Watch for duplicate cards (same name, same list) — flag to user, don't silently merge.
- Windows shell = git-bash: use single-quoted python strings; `python` (3.11) works, not `python3`.

## Reporting pattern (Quang's preference)
- Report board as Markdown table: `| List | Cards |`.
- Flag anomalies immediately: duplicates, Blocked cards with due dates, empty key lists, board with only 1 member.
- Short, decisive, no fluff. End with a concrete question about what to do next.

## Support files
- `references/vua-kiem-execution.md` — Vua Kiềm - Execution board structure with stable list IDs and known issues.
