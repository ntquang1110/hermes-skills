# Hermes Data Sources for Dashboarding

All under `~/AppData/Local/hermes/`.

## state.db (SQLite)

Main Hermes state database. Contains session history and messages.

### Table: sessions

| Column | Type | Notes |
|--------|------|-------|
| id | TEXT PK | Format: `YYYYMMDD_HHMMSS_<random>` or `proc_<random>` for bg processes, `cron_<id>_<date>` for jobs |
| title | TEXT | Session title (user message first line or auto-generated) |
| source | TEXT | `telegram`, `cli`, `tui`, `cron`, `subagent` |
| started_at | REAL (epoch) | Session creation |
| ended_at | REAL | Session end (NULL if still active) |
| message_count | INT | Number of messages |
| tool_call_count | INT | Tool invocations |
| input_tokens | INT | Total input tokens |
| output_tokens | INT | Total output tokens |
| estimated_cost_usd | REAL | Cost estimate ($0.00 on opencode-go provider) |
| archived | INT | 0=active, 1=archived |

Query for recent sessions:
```sql
SELECT id, title, source, started_at, message_count, tool_call_count, estimated_cost_usd
FROM sessions WHERE archived=0 ORDER BY started_at DESC LIMIT 15
```

### Table: messages

| Column | Type | Notes |
|--------|------|-------|
| id | INT PK | Auto-increment |
| session_id | TEXT FK | References sessions.id |
| role | TEXT | `user`, `assistant`, `tool`, `system` |
| content | TEXT | Message body (may be empty for tool calls) |
| timestamp | REAL (epoch) | Message creation |
| token_count | INT | Token count for this message |
| active | INT | 1=visible, 0=compacted (used by context management) |

Query for recent activity:
```sql
SELECT session_id, role, substr(content,1,300) as content, timestamp
FROM messages
WHERE role IN ('user','assistant') AND length(content) > 0
ORDER BY timestamp DESC LIMIT 20
```

### Token aggregation
```sql
SELECT SUM(input_tokens), SUM(output_tokens), SUM(estimated_cost_usd)
FROM sessions WHERE archived=0
```

## processes.json

Running background processes tracked by Hermes process manager.

Location: `~/AppData/Local/hermes/processes.json`
Format: JSON array of process objects

Key fields:
```json
{
  "session_id": "proc_<random>",
  "command": "cloudflared tunnel --url ...",
  "pid": 12345,
  "started_at": 1782923149.576,
  "cwd": "D:\\Project\\path",
  "notify_on_complete": true,
  "watch_patterns": []
}
```

## gateway_state.json

Gateway connection status for all platforms.

Location: `~/AppData/Local/hermes/gateway_state.json`

```json
{
  "pid": 15952,
  "gateway_state": "running",
  "active_agents": 1,
  "platforms": {
    "telegram": {
      "state": "connected",
      "error_code": null,
      "error_message": null,
      "updated_at": "2026-07-01T15:25:30.660659+00:00"
    },
    "feishu": {
      "state": "connected",
      ...
    }
  }
}
```

## cron/jobs.json

Cron job registry.

Location: `~/AppData/Local/hermes/cron/jobs.json`

```json
{
  "jobs": [
    {
      "id": "a83c2349344f",
      "name": "Hỏi tối nay có về không",
      "schedule": { "kind": "cron", "expr": "0 21 * * *" },
      "enabled": true,
      "state": "scheduled",
      "last_run_at": "2026-07-04T21:03:37+07:00",
      "last_status": "ok",
      "next_run_at": "2026-07-05T21:00:00+07:00",
      "repeat": { "completed": 11 }
    }
  ]
}
```

## sessions/sessions.json

Session routing index (NOT the session list — that's in state.db). Only shows gateway sessions.

Format: JSON object keyed by `agent:main:<platform>:<chat_type>:<chat_id>`.

## Tick files (cron/)

- `cron/ticker_heartbeat` — last cron tick time (epoch float)
- `cron/ticker_last_success` — last successful tick time (epoch float)
