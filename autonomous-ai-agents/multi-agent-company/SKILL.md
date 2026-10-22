---
name: multi-agent-company
description: Operate the AI Company — 10 role-based agents with personalities/frameworks/skills, OKR→KR→task hierarchy, strict plan→review→approve→implement→test workflow, and cross-machine agent-to-agent communication (Hermes ↔ OpenClaw) through a shared git repo inbox.
---

# Multi-Agent Company (AI Company)

## When to use
- Anything about "AI Company", "ai-company", team agents (CTO/Dev1/CMO/Content/QA...), OKR, proposals, agent inbox
- Coordinating Hermes with OpenClaw/Claw running on another machine
- TheFirstOnly MVP (`tfo.thefirstonly.com`)
- User says "team", "triển khai đi", "agents", "OKR", "workspace"

## Locations
- Project: `D:/Hermes Proj/ai-company/`
- venv: `.venv` (Python 3.11 — NOT system 3.14)
- Company dashboard server: `python server.py` (port 8090) + `company.thefirstonly.com`
- TFO MVP (FastAPI): port 8100 → `tfo.thefirstonly.com`
- Git: `github.com/ntquang1110/ai-company` (main, remote shared with OpenClaw)

## Architecture map
```
agents/
  base_agent.py     # BaseAgent.think() → DeepSeek; format_system_prompt() merges base + profile
  profiles.json     # per-agent: personality, framework (SOP steps), skills (1-5)
hub/
  store.py          # ALL data ops: tasks, proposals, OKRs, goals, messages, org, cost + DeepSeek wrapper
  process.py        # NLP route: user message → keyword match → wake agents
  run.py            # CLI: process | agent <name> | status | standup | proposals
  aggregate.py      # → dashboard JSON (agents+okrs+tasks+proposals+activity+cost+messages)
shared/
  workspace.md      # shared context / vision / decisions (source of truth)
  inbox.py          # send/read/mark_read/reply + git pull/push
  to_hermes.json    # Claw→Hermes mailbox (Hermes reads)
  to_claw.json      # Hermes→Claw mailbox (Claw reads)
store/*.json        # gitignored live data
dashboard/index.html  # B/W/Y premium dashboard
app/                # TFO MVP FastAPI + static frontend
```

## Key commands
```bash
cd /d/Hermes\ Proj/ai-company
python company.py status        # team + tasks + proposals + cost
python company.py okr           # OKR tree with linked tasks
python hub/run.py agent cto     # run an agent (auto-picks its tasks)
python hub/aggregate.py         # dashboard data JSON
# MVP server:
.venv/Scripts/python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8100
# Company dashboard server:
python server.py                # port 8090
```

## Progress report & goal-vs-progress (Quang: "update tiến độ công ty", "đối chiếu với goal")
Evidence-first recipe, run in this order, every number from real files, never from memory:
1. `python company.py status` — team + tasks + proposals + cost (live)
2. `python company.py okr` — OKR tree (may legitimately be empty)
3. `store/goals.json` — current_goal_id, deadline, status. A goal can sit **active + overdue for weeks**; flag it and offer close-and-reopen vs keep-and-push instead of treating it as current
4. `git log --oneline --all -i --grep="<goal keyword>"` (tenant/pilot/demo/...) — map each goal component to a commit as proof
5. Filter `store/tasks.json` by phase planning/in_progress/testing — print done_criteria presence (N = invalid task per DoD, that is why it stalls)
6. `store/features.json` — status + progress % per feature; compare against launch_plan phase gates
7. `shared/launch_plan.md` — Phase 1 lõi / Phase 2 sẵn sàng ra mắt / Phase 3 GTM. "Sẵn sàng ra mắt" means Phase 2 items exist: onboarding flow, pricing ẩn, landing, load test 5-10 user, passcode policy

Verdict pattern: separate **CODE-DONE** from **REAL-USAGE-PROVEN**. Recurring case: pilot CEO #2 account created + isolation verified ≠ pilot actually used the product. Code-complete ≠ goal-complete when the goal's real intent is "2 CEO pilot dùng ổn định". Report % per phase, name the single remaining gate (often a task needing Quang to test on real devices), end with the exact decision needed.

### Pitfall: cron standup output files read as binary
`~/AppData/Local/hermes/cron/output/<job_id>/<timestamp>.md` for ai-company-standup can be 100KB+ because the whole skill prompt is embedded; `read_file` flags it binary. Decode with python (`utf-8`, errors=replace) and slice from the `## Response` marker to skip the prompt. Standup job id: `9b6eb3205750` (09:00 daily, unsloth local model).

## Task workflow (non-negotiable)
Phase chain: **planning → review → approved → in_progress → testing → completed**
1. planning: agent writes plan_doc (spec, variants, sample size, timeline, cost)
2. review: auto-sends review_request message to routing reviewer (technical→CTO, marketing→CMO, design→Design, cost→CFO)
3. approved: reviewer PASS → notify Quang → ONLY after "triển khai đi" → implement
4. in_progress → testing → QA PASS → completed; FAIL → back to in_progress

**Pitfall: never code before approval.** User rule: brainstorm → critique → explicit "triển khai đi" → code → test. Skipping this got a hard correction ("anh đã duyệt gì đâu mà thực thi vậy").

## Cross-machine agent communication (git inbox)
Two agents on different machines share one git repo; each writes ONLY to the other's mailbox file → no merge conflicts:
- Sender appends to recipient's file: Hermes→`to_claw.json`, Claw→`to_hermes.json`
- Sync loop (cron 1m, no_agent script): git pull --rebase → read unread → process → mark read → commit+push ONLY that file
- Message shape: `{id, from, to, subject, body, type, ref, status: unread|read, created_at}`
- Full protocol + script template: `references/git-inbox-protocol.md`
- OpenClaw setup guide: `references/openclaw-setup-mac.md` (npm install, onboard, Telegram, model config)

### Pitfalls
- **Cron keyword filters silently swallow messages.** First sync script only printed messages matching "chốt/done/approved..." — PLAN/Phản biện messages got marked read with no output → user reported delays. Fix: output ALL new messages, no keyword filtering.
- **One agent asks the user, one is backup.** User: "sao 2 đứa đều hỏi anh thế". Designate FRONT (asks + synthesizes to user) and BACK (logic/critique/implementation). Currently: OpenClaw = front, Hermes = back.
- **Keep workspace.md in sync** — decisions/vision live there; both agents update + push.

## DeepSeek via OpenCode endpoint
- Base: `https://opencode.ai/zen/go/v1/chat/completions`
- Key env: `OPENCODE_GO_API_KEY`
- Models: `deepseek-v4-flash` (workers/cheap), `deepseek-v4-pro` (managers/reasoning)
- Empty response → transient rate limit: retry after ~3s

## Cloudflare tunnel remote config
- Tunnel runs as a Windows service with `--token` → config lives in Cloudflare Zero Trust, NOT the local yml
- Update via API: `PUT https://api.cloudflare.com/client/v4/accounts/{account_tag}/cfd_tunnel/{tunnel_id}/configurations`
- **WARNING: PUT replaces the ENTIRE ingress list.** Must re-include every hostname or they 404: tfo→8100, company→8090, upload→8769, bot→9877, me→5099, thefirstonly.com→5099, www→5099, then `{"service":"http_status:404"}` fallback
- DNS record first: POST /zones/{zone}/dns_records CNAME → `{tunnel_id}.cfargotunnel.com` proxied

## STT: Groq Whisper 16MB limit
- >15MB → chunking: 10-min chunks + 15-30s overlap, transcribe each, concatenate
- Compress Opus 16kHz mono; on 413 → smaller chunk + retry
- Model: whisper-large-v3, lang vi

## Resilient audio recording (TFO MVP) — user rule: NEVER lose a recording
User requirement (explicit: "lưu lại context này để em build"): bấm ghi → bấm End → lưu. **Nhưng nếu KHÔNG bấm End mà mất mạng / session bị kết thúc → VẪN PHẢI LƯU bản ghi.**
Implementation (app/main.py + app/static/index.html):
- Client: `MediaRecorder.start(10000)` → `ondataavailable` fires every 10s → POST chunk to server immediately (each chunk is already safe on server before network can drop)
- Server: `POST /api/record/start` → session_id; `POST /api/record/chunk` appends to `tfo_data/recordings/{sid}.webm`; `POST /api/record/end` finalizes + transcribes
- Watchdog thread: any session silent >30s → auto-finalize + save transcript file → recording survives tab close / network drop
- Details + code sketch: `references/resilient-recording.md`

## Founder vision elicitation workflow (workspace.md rounds)
When user is defining product vision (Purpose/Mission/Vision), run **structured rounds**: one question at a time, each answer immediately recorded into `shared/workspace.md` Decisions + pushed. Typical round order used successfully: purpose → mission → target customer → 3 core values → autonomy level → privacy → pricing (M4) → value prop (M5) → reliability (M6) → interface (voice-first) → biggest risk → first users → tech stack (delegate to CTO agent). Role split mandatory: FRONT agent asks the user and synthesizes; BACK agent critiques privately and implements — never both ask the user.

## Environment pitfalls
- System `python` = 3.14.5 → pydantic-core wheel issues. Create venv from Python 3.11 explicitly:
  `/c/Users/NTQUANG_DELL/AppData/Local/Programs/Python/Python311/python.exe -m venv .venv`
- Install deps via `install_deps.py` (subprocess wrapper) — a direct `pip install` in the terminal tool can get mis-flagged as a long-running server.
- Long Vietnamese prompts through `hub/run.py agent <name> "..."` sometimes come back empty due to shell quoting — call `BaseAgent.think()` via `python -c` or a script file instead; retry on empty (rate limit).
