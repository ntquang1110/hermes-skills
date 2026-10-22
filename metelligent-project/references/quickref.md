# meTelligent — SKILL.md Reference

## Live Status (exported)
- **Server:** port 8767, running via `run.py`
- **Tunnel:** https://metelligent-123.loca.lt
- **Notion:** Enabled (key OK, schema fixed)
- **GitHub:** ntquang1110/meTelligent (last commit 2b56f15)

## Key Config
```
NOTION_API_KEY=ntn_64...
### API Endpoints
| GET /api/health | Health check |
| POST /api/notion/tasks | Create task in Notion |
| POST /api/stt/transcribe | STT (multipart audio) |
| POST /api/nlp/process | Full NLP pipeline |

## Quick Commands
```bash
# Start server
cd /d/Hermes\ Proj/meTelligent/server && source venv/Scripts/activate && python run.py

# Start tunnel
node /c/Users/NTQUANG_DELL/AppData/Roaming/npm/node_modules/localtunnel/bin/lt.js --port 8767 --subdomain metelligent-123

# Test
curl http://localhost:8767/api/health
curl https://metelligent-123.loca.lt/api/health
```

## Project Structure
```
D:\Hermes Proj\meTelligent\
├── server/               FastAPI backend (Python)
│   ├── run.py            Entry point (base64 key)
│   ├── main.py           Alt entry point (.env loader)
│   └── metelligent/      App package
├── android_app_new/      Flutter Android app
├── EXPORT-meTelligent.md Full docs (1,435 lines)
├── SKILL-meTelligent.md  Quick reference
├── meTelligent-design.md Original design
└── meTelligent-android.apk Pre-built APK
```

## Notion Database Schema (Tasks)
| Property | Type | Notes |
|----------|------|-------|
| Task | title | Primary field |
| Status | status | "Not started", "In progress", "Done" |
| Deadline | date | Optional |
| Kết quả | rich_text | Description field |
