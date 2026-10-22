# Cron Port Hallucination — Debug Log

## Problem
Cron job `knowledge-researcher` (ID: d43697af1322) produced excellent content but POSTed to **port 6680** instead of **3003**.

## Evidence
Found in cron output file:
`<hermes_home>/cron/output/d43697af1322/2026-07-16_19-51-28.md`

Line 849:
```
📡 Ghi chú kỹ thuật: API server tại port 6680 không hoạt động 
(không có process nào lắng nghe). Kiến thức card đã được soạn đầy đủ 
theo format yêu cầu nhưng chưa thể POST lên /api/knowledge.
```

## The content was EXCELLENT despite the port failure
- 8 scientific citations (Aaronson 2002 Science, Wang 2021 Viruses, etc.)
- Deep mechanism explanation of JAK-STAT pathway
- Table of JAK inhibitors with targets and diseases
- Proper Vietnamese throughout

## Fix
Update cron prompt to explicitly state the port 3 times:
- "API server at http://localhost:3003 (port 3003, NOT port 6680)"
- "Import endpoint: POST http://localhost:3003/api/knowledge"
- "Queue endpoint: http://localhost:3003/api/research-queue"

## Verify cron output
After each cron run, check:
```bash
ls -lt <hermes_home>/cron/output/d43697af1322/ | head -3
tail -20 <hermes_home>/cron/output/d43697af1322/<latest>.md
grep "port\|api/knowledge\|HTTP\|POST\|curl" <hermes_home>/cron/output/d43697af1322/<latest>.md
```

## Manual import of lost card (if cron failed)
Read the full card content from the output file, then POST via Python:
```python
import urllib.request, json
body = {"title": "...", "content": "...", ...}
data = json.dumps(body).encode('utf-8')
req = urllib.request.Request('http://localhost:3003/api/knowledge',
    data=data, headers={'Content-Type': 'application/json', 'Authorization': 'Bearer hermes-knowledge-secret'})
resp = urllib.request.urlopen(req)
```
