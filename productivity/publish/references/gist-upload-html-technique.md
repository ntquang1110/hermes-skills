# Upload HTML to Gist via curl (working technique)

When `execute_code` is blocked (e.g., cron context), use this terminal-based approach:

## Problem
Directly inlining HTML content in a `curl -d` shell command fails because the HTML contains special characters (quotes, newlines, etc.) that break JSON parsing:
```
curl -s -X PATCH "https://api.github.com/gists/$GIST_ID" \
  -H "Authorization: token $PAT" \
  -H "Content-Type: application/json" \
  -d '{"files":{"f.html":{"content":"<!DOCTYPE html>..."}}}'  # ← FAILS
```

## Solution: Write JSON payload to file first

```bash
# Step 1: Read HTML and write JSON payload to temp file using Python
python -c "
import json
with open('/path/to/file.html', 'r', encoding='utf-8') as f:
    content = f.read()
payload = {
    'description': 'My artifact',
    'files': {
        'index.html': {'content': content}
    }
}
with open('/tmp/payload.json', 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False)
print(f'OK: {len(content)} chars')
"

# Step 2: Upload the JSON payload file via curl
curl -s -X PATCH "https://api.github.com/gists/$GIST_ID" \
  -H "Authorization: token $PAT" \
  -H "Content-Type: application/json" \
  -d @/tmp/payload.json

# Step 3: Parse the response to get URLs
python -c "
import sys, json
d = json.load(sys.stdin)
for name, info in d.get('files', {}).items():
    raw = info['raw_url']
    print(f'{name}:')
    print(f'  Preview: https://htmlpreview.github.io/?{raw}')
"

# Step 4: Clean up
rm -f /tmp/payload.json
```

## Key points
- `python -c` with `json.dump` handles all escaping correctly
- `curl -d @file` reads JSON from a file without shell interpretation
- Use `ensure_ascii=False` to preserve Vietnamese characters
- The `json.load(sys.stdin)` in response parsing reads from curl's stdout pipe

## Updating existing Gist
Use `PATCH` (not POST) to update an existing gist. The URL is:
`https://api.github.com/gists/{gist_id}`

## Adding multiple files
Add more entries to the `files` dict in the payload:
```python
payload = {
    'files': {
        'index.html': {'content': html_content},
        'guide.html': {'content': guide_content}
    }
}
```
