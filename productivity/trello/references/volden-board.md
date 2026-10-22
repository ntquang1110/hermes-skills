# Volden - Ops App (Trello board)

Live project board for the volden-ops-web development project.

- **Board ID:** `6a6b793f7e5888b26f2ad776`
- **URL:** https://trello.com/b/l3d1Zx31/volden-ops-app
- **Owner:** ntquang1110 (Tee Kwang), email <EMAIL>

## Lists (workflow, in order)

| List ID | Name | Purpose |
|---------|------|---------|
| `6a6f713725189e8127253158` | Document | Docs / process notes |
| `6a6b7945048bf91d79b6e3ea` | To do | Backlog |
| `6a6b794abbaff2499c1c4436` | Doing | In progress |
| `6a6b794c7489177d352244b8` | Testing | QA |
| `6a6b7984660b393096300f15` | Need fixed | Bugs waiting |
| `6a6b798d6e2207053549802e` | Fixing | Bugs being fixed |
| `6a6b7951c8cad25b4a3f3b1b` | Done | Completed |
| `6a6b7953c26e63e9fee443d3` | Cancel | Discarded |

## Worked example (checking boards, Python)

```python
import urllib.request, urllib.parse, json, os, re
env = open(os.path.expanduser('~/AppData/Local/hermes/.env'), encoding='utf-8').read()
key = re.search(r'TRELLO_API_KEY=(.+)', env).group(1)
token = re.search(r'TRELLO_TOKEN=(.+)', env).group(1)
url = 'https://api.trello.com/1/members/me/boards?' + urllib.parse.urlencode(
    {'key': key, 'token': token, 'fields': 'name,id,url,closed', 'filter': 'all'})
boards = json.load(urllib.request.urlopen(url, timeout=15))
for b in boards:
    print(b['name'], b['id'], b['url'])
```

## Card conventions observed

- Cards prefixed `[BUG]` / `[FEAT]`
- Vietnamese descriptions
- Snapshot 2026-07-26: 7 cards — To do (webhook payment bug, VTP + 247 shipping integrations), Doing (auto-payment matching, auto warehouse dispatch), Testing (retail order auto-approve bug)
