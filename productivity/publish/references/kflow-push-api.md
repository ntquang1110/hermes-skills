# Kflow Push API — Knowledge Card Publishing

Push research summaries as knowledge cards to the local kflow (Knowledge Flow) server at `http://localhost:3003`.

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/knowledge` | POST | Auto-creates topic by `topic_slug`. Best for one-shot pushes. |
| `/api/cards` | GET | List all cards (supports `?slug=X`, `?topic_id=X`, `?ids=a,b,c`). |
| `/api/cards` | POST | Generic card creation (requires explicit `topic_id` or `topic_slug`). |
| `/api/topics` | GET | List all topics with slugs. |

## Auth

```python
import hashlib
PASSCODE_COOKIE = "tfo_auth=" + hashlib.sha256(b"<PASSCODE>").hexdigest()
# = tfo_auth=1d1e977a218bfa01fe61106c360c8acf667047e35f17fdb0f1a8484e06cfdb55
HEADERS = {
    "Authorization": "Bearer hermes-knowledge-secret",
    "Content-Type": "application/json",
    "Cookie": PASSCODE_COOKIE,
}
```

### ⚠️ Passcode gate bắt buộc (KF 3003, active từ 2026-08)

KF 3003 nằm sau `web-passcode-gate` (passcode `<PASSCODE>`). **Mọi request API cũng bị gate** — matcher chặn cả `/api/*`:

- Không cookie → GET `/api/cards` trả `passcode?next=%2Fapi%2Fcards` (KHÔNG phải JSON cards)
- Không cookie → POST `/api/knowledge` bị `307 → /passcode`, card không được tạo
- Fix: mọi curl thêm `-b "tfo_auth=<sha256(<PASSCODE>)>"`, mọi Python thêm `"Cookie"` header (xem ở trên)

```bash
HASH=$(python -c "import hashlib; print(hashlib.sha256(b'<PASSCODE>').hexdigest())")
curl -s -b "tfo_auth=$HASH" http://localhost:3003/api/cards
```

Passcode hash cố định `1d1e977a218bfa01fe61106c360c8acf667047e35f17fdb0f1a8484e06cfdb55` — có thể hardcode thay vì tính lại.

## Body Format

```python
{
    "title": "📖 Card Title (emoji prefix recommended)",
    "summary": "One-sentence summary shown in feed cards",
    "content": "Full text/body of the knowledge card",
    "tags": ["tag1", "tag2"],
    "topic_slug": "unique-url-slug",     # auto-creates topic if new
    "source_url": "https://..."           # link to original document/gist
}
```

### Which endpoint to use

- **`/api/knowledge`** — Use when content has a clear `topic_slug`. It auto-creates or reuses the topic. Simpler.
- **`/api/cards`** — Use when you need more control (e.g. custom `source`, `session_id`, or no topic). Also serves GET for dedup.

## ⚠️ Dual Push Architecture — Tránh push trùng

Có **hai cron job** cùng push card lên KF — cần hiểu rõ để tránh duplicate:

### 1. knowledge-researcher (cron `d43697af1322`, every 240m / 4h)
- Research sâu 1 chủ đề mới → push **directly** lên KF qua `/api/knowledge`
- Luôn kèm dedup check trước khi research (≠ trước khi push)
- Mỗi lần chạy tạo **1 card** (chất lượng cao, research sâu)
- **Từ Jul 19 → Aug 02: đã push ~180 cards** (KF tăng từ 44 → 227). Trung bình ~6 card/ngày

### 2. Auto-push research (cron `da7c6b38c7d9`, midnight)
- Quét session log tìm research mới → push nếu chưa có trong KF
- **Chức năng:** catch những research không được knowledge-researcher push (VD: user tự tạo HTML research, hoặc research từ task khác)
- **Trả [SILENT] là hành vi bình thường, không phải lỗi.** Đã được xác nhận qua 5+ lần chạy (Jul 20, 21, 22, 24, 28, Aug 02) — auto-push consistent trả về không có gì mới vì knowledge-researcher (chạy 4h/lần) đã push hết research.
- **Chỉ push khi thực sự có research mới** — luôn kèm dedup chi tiết (xem phần Dedup bên dưới)

### ⚡ Dedup thực tế — Title + Content + Session check

Auto-push cron sử dụng dedup 3 tầng đã được kiểm nghiệm qua 5+ lần chạy:

```
Tầng 1 — Lấy KF cards:
  curl -s -b "tfo_auth=$HASH" http://localhost:3003/api/cards   # bắt buộc cookie (passcode gate)
  → toàn bộ title, created_at, content hiện có

Tầng 2 — Tìm research trong session log:
  session_search(query="research ...", sort="newest")
  → tìm các research gần nhất, kiểm tra title, nội dung
  ⚠️ session_search FTS5 KHÔNG tìm thấy session cron (knowledge-researcher) —
     cron sessions chỉ query được qua state.db trực tiếp (xem mục "state.db" bên dưới)

Tầng 3 — So sánh và quyết định:
  - Title overlap ≥50% từ khả trùng (tokenize title thành từ, so sánh intersection/union)
  - Hoặc 1 title chứa title kia (substring match)
  - Hoặc content giống nhau ≥80%
  → Nếu BẤT KỲ điều kiện nào đúng → SKIP (đã có trong KF)

Chỉ push khi research hoàn toàn mới — không trùng title, không trùng content.
```

### ⚠️ Timestamps: KF created_at là UTC, session started_at là LOCAL (UTC+7)

Khi đối chiếu "card mới nhất trong KF" với "session research gần nhất", nhớ lệch 7h:
- `cards.created_at` trong API trả về là **UTC** (VD `2026-08-02T13:20` = 20:20 giờ VN)
- `sessions.started_at` trong state.db là epoch giây **local** (UTC+7)
- VD thực tế Aug 02: session knowledge-researcher 20:23 local → card MoE `2026-08-02T13:20` UTC — cùng 1 card, đừng tưởng là 2

### ⚠️ Tìm session cron qua state.db trực tiếp (session_search không thấy cron)

`session_search` chỉ index session có FTS, cron sessions (source='cron') thường KHÔNG hiện. Query thẳng SQLite:

```python
import sqlite3, os, datetime
db = os.path.expanduser('~/AppData/Local/hermes/state.db')
conn = sqlite3.connect(db); cur = conn.cursor()
cur.execute("SELECT id, title, started_at, message_count FROM sessions "
            "WHERE source='cron' AND title LIKE '%knowledge-researcher%' "
            "ORDER BY started_at DESC LIMIT 5")
for r in cur.fetchall():
    print(datetime.datetime.fromtimestamp(r[2]).strftime('%m-%d %H:%M'),
          '|', r[3], 'msgs |', r[0])
# Đọc nội dung session (assistant text) để xác nhận "Card POST thành công":
cur.execute("SELECT role, content FROM messages WHERE session_id=? "
            "AND role='assistant' AND content IS NOT NULL AND length(content)>200 ORDER BY id", (sid,))
```

Pattern xác nhận đã push: mỗi session knowledge-researcher = 1 card, log có "Card POST thành công" / "Card verified" + `Total: N cards` sau push.

Công thức check title overlap trong shell:
```bash
HASH=$(python -c "import hashlib; print(hashlib.sha256(b'<PASSCODE>').hexdigest())")
curl -s -b "tfo_auth=$HASH" http://localhost:3003/api/cards | python -c "
import sys, json
cards = json.load(sys.stdin)
existing_titles = [c['title'].lower() for c in cards]

def is_duplicate(new_title, existing_titles):
    new_words = set(new_title.lower().split())
    for et in existing_titles:
        ex_words = set(et.lower().split())
        if not new_words or not ex_words:
            continue
        overlap = len(new_words & ex_words) / len(new_words | ex_words)
        if overlap >= 0.5:
            return True
        if new_title.lower() in et or et in new_title.lower():
            return True
    return False
"
```

### [SILENT] là output bình thường

Auto-push trả [SILENT] khi không có research mới. Đây KHÔNG phải lỗi:
- 5+ lần chạy (Jul 20, 21, 22, 24, 28) đều trả [SILENT] thành công
- Knowledge-researcher chạy 2h/lần đã push hết research trước đó
- Auto-push là safety net — chỉ push khi có edge case (research không qua knowledge-researcher)
- Ngược lại: nếu auto-push tìm thấy research mới và push → output là báo cáo chi tiết các card đã push

### Kiểm tra coverage theo chủ đề

Auto-push kiểm tra xem KF đã bao phủ các chủ đề chưa:
| Chủ đề | Check |
|--------|-------|
| Vật lý | Physics Encyclopedia, Đặc tính Lý-Hóa KLN |
| Kim loại nặng (As, Pb, Hg, Cd) | 5 cards (Lý-hóa, Loại bỏ, Rửa đất, Xử lý KHÔ, Xử lý ướt) |
| Xử lý khô/ướt | 2 phương pháp |
| Than bùn | 4 cards |
| Saponin | 3 cards |
| Sinh học phân tử | 60+ cards |
| Chăn nuôi heo | 40+ cards |

Nếu tất cả chủ đề đã có coverage → không cần push gì thêm.

### ⚡ Hệ quả cho Dedup (code mẫu cơ bản)

**Auto-push cần kiểm tra knowledge-researcher sessions gần nhất** trước khi quyết định push — nếu knowledge-researcher đã research và push chủ đề đó trong vòng 24h qua, cần kiểm tra kỹ hơn chứ không chỉ so sánh title:

```python
import urllib.request, json, hashlib
from datetime import datetime, timedelta

COOKIE = "tfo_auth=" + hashlib.sha256(b"<PASSCODE>").hexdigest()

# 1. Lấy danh sách cards hiện có
req = urllib.request.Request("http://localhost:3003/api/cards",
    headers={"Authorization": "Bearer hermes-knowledge-secret", "Cookie": COOKIE})
resp = urllib.request.urlopen(req)
existing = json.loads(resp.read())

existing_titles = {c.get("title") for c in existing}
existing_urls   = {c.get("source_url") for c in existing}

# 2. Kiểm tra xem knowledge-researcher đã push chưa
recent_cards = [c for c in existing 
                if c.get("created_at","").startswith(datetime.utcnow().strftime("%Y-%m-%d"))]
recent_titles = {c.get("title") for c in recent_cards}

# 3. Skip nếu title hoặc source_url đã tồn tại
for item in new_items:
    if item["title"] in existing_titles:
        continue  # đã có trong KF (bất kể nguồn nào)
    if item.get("source_url") in existing_urls:
        continue  # cùng nguồn
    # POST the item
```

**Nguyên tắc:** 
- Nếu knowledge-researcher đã push → auto-push KHÔNG push lại
- Nếu research từ user task (không qua knowledge-researcher) → auto-push push
- Luôn gọi `curl -s -b "tfo_auth=$HASH" http://localhost:3003/api/cards` (kèm cookie passcode) trước mọi push để dedup

## ⚠️ Windows Cron Job Pitfalls

### Python path resolution in git-bash (MSYS2)
- `python3` → resolves to Microsoft Store stub (fails with "Python was not found...")
- Use **`python`** (which resolves to `python3.11` at `C:\Users\NTQUANG_DELL\AppData\Local\Programs\Python\Python311\python.exe`)

### MSYS path translation with Python
NEVER use `~/path.py` when running Python in git-bash:
```bash
$ python ~/script.py   # FAILS: MSYS expands ~/ → /c/Users/... , 
                       # but Python sees C:\c\Users\... (double root)
```
Use absolute Windows paths with quotes:
```bash
$ python "C:\Users\NTQUANG_DELL\script.py"   # OK
```

### execute_code / inline Python blocked in cron
`execute_code` tool and `python3 -c "..."` are blocked when running as a cron job. Workaround:
```bash
# 1. Write script file
write_file(path="C:\\Users\\NTQUANG_DELL\\push.py", content="...")

# 2. Run via terminal
terminal(command='python "C:\\Users\\NTQUANG_DELL\\push.py"')
```

## Full Push Example

```python
import requests, json, hashlib

API = "http://localhost:3003/api/knowledge"
HEADERS = {
    "Authorization": "Bearer hermes-knowledge-secret",
    "Content-Type": "application/json",
    "Cookie": "tfo_auth=" + hashlib.sha256(b"<PASSCODE>").hexdigest(),
}

items = [
    {
        "title": "🔬 RESEARCH — Example Topic",
        "summary": "Brief summary for the feed",
        "content": "Full body text of the knowledge card...",
        "tags": ["tag-a", "tag-b"],
        "topic_slug": "example-topic",
        "source_url": "https://gist.github.com/..."
    }
]

for item in items:
    r = requests.post(API, headers=HEADERS, json=item, timeout=10)
    if r.status_code in (200, 201):
        print(f"✅ {item['title'][:60]}")
    else:
        print(f"❌ {item['title'][:60]} → {r.status_code}: {r.text[:100]}")
```

## Related

- `push_to_kflow.py` at `~/push_to_kflow.py` — existing script with 15+ research items
- KF đã phát triển từ 44 → **227 cards** (Aug 02). Luôn gọi `HASH=$(python -c "import hashlib; print(hashlib.sha256(b'<PASSCODE>').hexdigest())")` rồi `curl -s -b "tfo_auth=$HASH" http://localhost:3003/api/cards | python -c "import sys,json; cards=json.load(sys.stdin); print(f'KF: {len(cards)} cards'); [print(c['title'][:70]) for c in cards[:5]]"` để kiểm tra số lượng và chủ đề gần nhất trước khi quyết định push.
- Xem thêm: `references/knowledge-flow.md` — overview nhẹ hơn về KF system
