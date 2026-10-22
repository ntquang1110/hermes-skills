# meTelligent API Endpoints — Verified

Verified against running server at localhost:8767 (Jul 2026)

## Meeting Module

All endpoints under `/api/meeting/`. Port 8767.

### Create Meeting

```
POST /api/meeting/start-json
Content-Type: application/json
Body: {"title": "Meeting name", "tags": "tag1, tag2"}

Response 200:
{
  "meeting_id": "uuid",
  "title": "...",
  "date": "2026-07-05",
  "status": "recording",
  "tags": "..."
}
```

Also available as Form-data: `POST /api/meeting/start` (form fields `title`, `tags`).

### Upload Chunk

```
POST /api/meeting/chunk
Content-Type: multipart/form-data
Fields: meeting_id=<uuid>, chunk_index=<int>, file=<audio_file>

Response 200:
{"chunk_id": "uuid", "status": "pending"}
```

### End Meeting (trigger Whisper + Groq pipeline)

```
POST /api/meeting/end-json
Content-Type: application/json
Body: {"meeting_id": "uuid"}

Response 200:
{
  "meeting_id": "uuid",
  "status": "done|processing|failed",
  "full_transcript": "...",
  "corrected_text": "..."
}
```

Also Form: `POST /api/meeting/end` with form field `meeting_id`.

### Quick Note (single-shot)

```
POST /api/meeting/quick
Content-Type: multipart/form-data
Fields: file=<audio_file>, tags=<str>

Response 200:
{"text": "transcribed text", "meeting_id": "uuid"}
```

### Get Meeting

```
GET /api/meeting/{meeting_id}
→ full meeting dict
```

⚠️ Route `/{meeting_id}` must be AFTER `/daily-summary` and `/daily/{date}`.

### List Daily

```
GET /api/meeting/daily/{date}
→ [{id, title, tags, status, full_transcript, corrected_text}]
```

### Daily Summary

```
GET /api/meeting/daily-summary
→ {"dates": {"YYYY-MM-DD": [{...}]}}
```

## Health & Info

```bash
curl http://localhost:8767/api/health
# → {"status":"ok","version":"0.1.0"}

curl http://localhost:8767/api/info
# → {"name":"meTelligent Server","version":"0.1.0","features":["stt","summarize","tasks","memory"]}
```

## Through Tunnel

```bash
# Cloudflare Tunnel (trycloudflare.com)
curl https://xxx-yyy-zzz.trycloudflare.com/api/health

# localtunnel (loca.lt)
curl https://metelligent-123.loca.lt/api/health
```

Both should return 200 OK `{"status":"ok","version":"0.1.0"}`

## STT

```
POST /api/stt/transcribe
Content-Type: multipart/form-data
Body: file=<audio_file>

Response (200):
{
  "text": "transcribed text",
  "language": "vi",
  "segments": [...]
}
```

## NLP

```
POST /api/nlp/process
Content-Type: application/json
Body: {"text": "transcript text"}

Response (200):
{
  "summary": "tóm tắt...",
  "tasks": [
    {"title": "task name", "priority": "high|medium|low", "description": "..."}
  ],
  "language": "vi"
}

POST /api/nlp/summarize
Body: {"text": "..."}
→ {"summary": "...", "language": "vi"}

POST /api/nlp/extract-tasks
Body: {"text": "..."}
→ {"tasks": [...], "language": "vi"}
```

## Notion

```
POST /api/notion/tasks
Content-Type: application/json
Body: {"title": "Task name", "status": "Not started"}

Response (200):
{"success": true, "page_id": "390ee73e-..."}

GET /api/notion/tasks
→ {"results": [...]}
```
