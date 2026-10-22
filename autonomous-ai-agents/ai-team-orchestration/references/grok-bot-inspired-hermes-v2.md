# Grok Bot → Hermes Multi-Agent 2.0 (2026-09-21)

Phân tích Grok Bot (x.ai/bot) và mapping sang Hermes. Source: x.ai homepage + grok.com API docs, verified qua curl.

## Grok Bot — bản chất

- "AI teammates that finish the work" — mỗi bot có máy tính riêng trên cloud, chạy 24/7, dùng apps như người.
- **Shared persistent cloud computer**: mọi bot của 1 user share 1 máy (files, browser, logins). Isolation per user, không per bot.
- Parallel: nhiều bot chạy đồng thời, collaborate trong cùng thread.
- **Routines**: "Show a Bot how it's done" — demo workflow 1 lần → bot lưu thành routine, tự chạy lần sau.
- Memory: bots keep context và học từ nhau.
- Preset bots: Sales Outbound, Talent Scout, Paid Media, Expense Manager, Product Performance, Bug Reproduction, Account Health, Chief of Staff.
- Pricing: Cursor Pro/Pro+/Ultra hoặc SuperGrok/SuperGrok Plus/Heavy hoặc Cursor Teams Standard/Premium; weekly usage cap + pay-per-token overage.
- Access: desktop (macOS/Windows) + iOS app; bot login vào tools qua "Log Grok Bot in once".

## Hermes Multi-Agent 2.0 — architecture đã design

Single Hermes instance + Agent Registry (không cần nhiều Hermes profiles). Quyết định: giữ một gateway, stateless agents.

```
User (Quang) → CEO Agent (Hermes default) → Agent Pool (registry: sales, dev, qa, research, cmo, +8) → Infrastructure (Message Bus, Agent Registry SQLite, Memory per-agent, Skill Library role-based, Routine Store, Credential Vault namespaced)
```

### Layers

1. **Agent Registry** — mỗi agent là 1 definition trong JSON/SQLite: persona, skills, memory pointer, tools. Dispatch = load definition + skills + memory → chạy → save state (ngủ đông giữa các task).
2. **Message Bus** — file-based queue `~/ai-company/messages/{inbox,outbox,archive}/<agent_id>.json`. Thay Git-based (v1: `shared/to_hermes.json` + `to_claw.json`). Local machine → không cần git push/pull. Watchdog (inotify / ReadDirectoryChanges) + polling fallback 5s. Cron sync 1 phút/lần `no_agent=true`.
3. **CEO Orchestrator** — nhận task từ user → phân tích → bẻ nhỏ → dispatch qua Message Bus (via `delegate_task` batch max 3 parallel + background process + notify_on_complete cho task dài).
4. **Teach by demonstration** — 3 giai đoạn để tránh over-engineering:
   - V1: manual skill (đã có `skill_manage`).
   - V2.1: semi-auto — model suggest SKILL.md từ conversation history.
   - V2.2: full auto — record mode watch tool calls → generate SKILL.md.
5. **Communication protocol** — JSON với from/to/type/task{ id, title, context, deadline, requires[], output }.
6. **Dashboard** — extend `company.thefirstonly.com` hiện có (B/W/Y theme, passcode <PASSCODE>), không rebuild.

### Self-critique (7 risks → mitigation)

1. Single Hermes = SPOF → chấp nhận V1, Windows service uptime 99%+, stateless restart.
2. Không thực sự parallel (Hermes tuần tự) → `delegate_task` batch 3 + background.
3. Agent chỉ tồn tại khi chạy → đủ tốt, SQLite persist persona/memory/skills.
4. Message bus latency → local file queue + watchdog, không qua Git.
5. "Teach" khó → chia 3 giai đoạn.
6. Per-agent credentials = attack surface → Hermes credential store namespaced + encrypt-at-rest.
7. Dashboard đã có → extend, không rebuild.

### Roadmap validated

P1 (4h): Registry + Message Bus + 3 pilot agents (Sales, Research, Dev) — visible end-to-end.
P2 (3h): Inter-agent comm + task chaining + watchdog.
P3 (4h): Per-agent memory + Record Routine.
P4 (2h): Dashboard + credential vault + health-check cron 5m. Total ~13h.

### Khi nào dùng pattern này

Trigger: user muốn "tạo nhiều agent mỗi agent là 1 nhân viên, skill riêng, giao tiếp với nhau" hoặc hỏi "áp dụng Grok Bot với Hermes thế nào". Ưu tiên single-instance + registry thay vì tạo nhiều Hermes profiles.

### Pitfalls đã gặp khi research

- `x.ai` và `x.ai/bot` là Next.js SPA — curl trả pre-rendered HTML không có body content; phải strip tags và grep sau khi fetch, hoặc dùng browser thật. Google/Bing chặn curl → fallback DuckDuckGo qua Camofox (xem web-research skill).
- Grok Bot docs không public chi tiết "tạo custom bot" — chỉ preset bots + "Create a Bot" marketing copy.
