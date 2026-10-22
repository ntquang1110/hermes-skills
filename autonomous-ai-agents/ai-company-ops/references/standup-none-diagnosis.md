# Chẩn đoán standup trả None cho tất cả agents

Khi `python hub/run.py standup` trả `(LLM trả None)` cho 5/5 agents:

## Bước 1 — Kiểm tra OpenCode Go key
```python
import json, urllib.request, os, re
key = os.environ.get('OPENCODE_GO_API_KEY','')
if not key:
    env = open(os.path.expanduser('~/AppData/Local/hermes/.env'), encoding='utf-8').read()
    m = re.search(r'OPENCODE_GO_API_KEY=(\S+)', env)
    if m: key = m.group(1)
req = urllib.request.Request(
    'https://opencode.ai/zen/go/v1/models',
    headers={'Authorization': f'Bearer {key}', 'User-Agent': 'Mozilla/5.0',
             'Origin': 'https://opencode.ai', 'Referer': 'https://opencode.ai/'}
)
resp = urllib.request.urlopen(req, timeout=10)
data = json.loads(resp.read())
print(f"Models: {len(data.get('data',[]))}")
```

## Bước 2 — Test LLM call ngắn
```python
body = json.dumps({'model':'deepseek-v4-flash','messages':[{'role':'user','content':'1+1=?'}],'max_tokens':50}).encode()
req = urllib.request.Request('https://opencode.ai/zen/go/v1/chat/completions', data=body,
    headers={'Authorization':f'Bearer {key}','Content-Type':'application/json',
             'User-Agent':'Mozilla/5.0','Origin':'https://opencode.ai','Referer':'https://opencode.ai/'})
resp = urllib.request.urlopen(req, timeout=15)
content = json.loads(resp.read())['choices'][0]['message']['content']
```

## Phân biệt 2 trường hợp

| Triệu chứng | Chẩn đoán | Xử lý |
|---|---|---|
| `/v1/models` trả 401 `Insufficient balance` | **Hết credit** | Báo Quang nạp credit (opencode.ai/workspace/.../billing) |
| `/v1/models` trả 200 (35+ models), LLM test OK nhưng standup vẫn None | **Transient trong hub/run.py path** | Retry standup 1-2 lần cách 10s. Báo "standup None — transient LLM dù key OK" |

## Lưu ý
- KHÔNG copy-paste chẩn đoán "hết credit" từ hôm trước nếu hôm nay key đã hoạt động trở lại.
- Hai hiện tượng khác nhau — cần test key thực tế, không suy luận từ lịch sử.
- Nếu retry vẫn None → vẫn báo cáo trung thực (standup không chạy được), không bịa số liệu.
