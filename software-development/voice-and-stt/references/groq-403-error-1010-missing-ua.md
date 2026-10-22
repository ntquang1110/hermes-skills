# Groq 403 error 1010 — Missing User-Agent (verified 2026-09-12)

## The one-line lesson

Groq returns `HTTP 403: error code: 1010` for raw urllib/requests calls that
**omit the User-Agent header** (Cloudflare WAF). It is NOT an account/verification
problem and NOT a dead key. Add a UA header or use the OpenAI SDK and it works.

## Reproduction matrix (same key, same audio file)

| Call | UA header | Result |
|---|---|---|
| `GET /models` | none | 200 OK |
| `POST /audio/transcriptions` (urllib, multipart) | none | **403 error 1010** |
| `POST /audio/transcriptions` (urllib) | `User-Agent: openai-python/1.30.0` | 200 OK |
| `POST /audio/transcriptions` (urllib) | browser UA | 200 OK |
| OpenAI SDK `client.audio.transcriptions.create` | SDK default | 200 OK |
| Hermes `_transcribe_groq()` | SDK default | 200 OK, `success: true` |

Note: `GET /models` returns 200 even without UA, so a models-endpoint check alone
proves the key is alive but does NOT prove audio transcription will work.

## Reproduction script (A/B/C comparison)

```python
import urllib.request, urllib.error, json

key = '<GROQ_API_KEY>'
with open('C:/tmp/groq_test.mp3', 'rb') as f:
    data = f.read()
boundary = '----testT'

def go(ua, model):
    body = b''
    for field in [('model', model), ('language', 'vi')]:
        body += f'--{boundary}\r\nContent-Disposition: form-data; name="{field[0]}"\r\n\r\n{field[1]}\r\n'.encode()
    body += f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="audio.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n'.encode()
    body += data + b'\r\n'
    body += f'--{boundary}--\r\n'.encode()
    h = {'Authorization': f'Bearer {key}', 'Content-Type': f'multipart/form-data; boundary={boundary}'}
    if ua: h['User-Agent'] = ua
    req = urllib.request.Request('https://api.groq.com/openai/v1/audio/transcriptions', data=body, headers=h)
    try:
        resp = urllib.request.urlopen(req, timeout=45)
        return f'OK: {resp.read().decode()[:120]}'
    except urllib.error.HTTPError as e:
        return f'HTTP {e.code}: {e.read().decode()[:200]}'
    except Exception as e:
        return f'ERR {type(e).__name__}: {str(e)[:150]}'

print('A) no-UA  + turbo :', go(None, 'whisper-large-v3-turbo'))   # 403 error 1010
print('B) no-UA  + large :', go(None, 'whisper-large-v3'))         # 403 error 1010
print('C) openai-UA+large:', go('openai-python/1.30.0', 'whisper-large-v3'))  # 200 OK
```

## Fastest verify through Hermes itself (no raw HTTP needed)

```bash
/c/Users/NTQUANG_DELL/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe -c "
import sys; sys.path.insert(0, r'C:\Users\NTQUANG_DELL\AppData\Local\hermes\hermes-agent')
from tools.transcription_tools import _transcribe_groq
import json
print(json.dumps(_transcribe_groq(r'<path-to-audio>', 'whisper-large-v3-turbo'), ensure_ascii=False))
"
# {"success": true, "transcript": "...", "provider": "groq"} → Groq fully alive
```

## When this bites

- A hand-written test script (`urllib`/`requests` without UA) returns 1010 →
  agent wrongly concludes "account chưa verify SMS" / "key dead" and migrates
  STT to local whisper (wasted half a day on 2026-09-12).
- Config drift: `stt.provider` switched to `local` for a non-reason; Groq (free,
  fast, better VI quality) stays idle.

## Decision rule

Before declaring Groq broken: (1) `_transcribe_groq()` success check, or
(2) raw call WITH `User-Agent: openai-python/1.30.0`. Only if both fail with
non-1010 errors (e.g. 401 invalid key, 429 quota) is there a real account issue.
