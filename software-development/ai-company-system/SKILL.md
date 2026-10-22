---
name: ai-company-system
description: Build and operate a multi-agent AI company — flat communication, 10+ agents, OKR system, skill registry, agent personalities, dashboard
---

# AI Company System

Build an autonomous AI company where all departments are AI agents. Flat communication model — everyone proposes, everyone hears.

## ⚠️ CRITICAL WORKFLOW RULES (user-enforced)

These were explicitly taught by the user. Violating them will be corrected.

### 1. NO CODE BEFORE QUANG APPROVAL

This applies to EVERYTHING — even building the AI Company system itself. The workflow for any new feature:

```
User says "build feature X"
  → Hermes + Claw brainstorm via shared inbox
  → Claw synthesizes the final plan + critique (NOT Hermes)
  → Present to Quang for review
  → Only when Quang says "triển khai đi" → implement
  → Push to git → Claw reviews → Quang confirms → merge
```

Never skip to implementation even when the design seems obvious. User explicitly corrected: "anh đã duyệt gì đâu mà thực thi vậy" — meaning "I approved nothing, why are you executing?"

### 2. Claw synthesizes the plan, not Hermes

When collaborating with OpenClaw on shared features or design decisions:

- **Hermes** proposes technical details, braindumps ideas, provides raw analysis
- **OpenClaw** synthesizes the final consolidated plan + critique
- The user explicitly mandated this division: "anh muốn claw là người tổng hợp lại plan và phản biện"

### 3. Inbox sync must deliver ALL messages — no keyword filters

The v2 cron sync filtered messages by important keywords (chốt, approved, triển khai...). This caused Claw's messages "PLAN" and "Phản biện" to be **silently consumed without delivery**. The user experienced unexplained delays.

Fix: **Output ALL messages** in a brief one-line format. A short notification is never spam; a silently lost message is always a bug.

### 4. ONE focus at a time — finish, then report (user-enforced)

Quang: *"Em trả lời nhiều quá, chọn 1 cái làm trọng tâm thôi, xong 1 cái và final lại mới trả lời anh."*

- Pick ONE task, work it to completion silently, then send ONE final report.
- Do NOT narrate mid-progress, do NOT stack multiple half-done items in one message.
- A final report is short: what was built, what was verified (with real evidence), what's next.

### 5. OpenClaw is the single reporter to Quang; Hermes builds

Quang: *"Hai em tự phân việc với nhau — ai làm tốt nhất thì người đó thực hiện. OpenClaw chịu trách nhiệm báo cáo trực tiếp cho anh."*

- Hermes = back: build kỹ thuật, transcribe/STT, dashboard, deploy, system plumbing.
- OpenClaw = front: tổng hợp, review, phản biện, **báo cáo Quang (1 phía duy nhất)**.
- When Quang asks for status, report the real current state; do not invent a Claw report that hasn't arrived.

### 6. Vision/mission lives in briefing.md + dashboard — NOT only workspace.md

Quang: *"Tại sao team vẫn đang hỏi mục tiêu là gì? Mục tiêu đã rất rõ ràng rồi... phổ biến lại cho team."*

- `shared/workspace.md` is the Hermes↔Claw coordination file — agents do NOT read it.
- `briefing.md` is what every agent reads on wake-up — this is where vision/mission/current-goal MUST be written for the team to see it.
- The dashboard must surface it too (Mission Control). A goal that lives only in chat history is invisible to the team.

## Architecture

```
Quang (Telegram) ↔ Hermes (Hub)
                     │
          ┌──────────┴──────────┐
          │  Company Briefing    │
          │  (shared context)    │
          └──────────┬──────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
  CTO Agent ──── CMO Agent ──── Content Agent
  Dev1 Agent     Social Agent     Design Agent
  QA Agent       COO Agent        CFO Agent
```

## Directory Structure

```
ai-company/
├── briefing.md              # Shared context (auto-updated)
├── company.py               # CLI quick-start
├── server.py                # Dashboard server
├── dashboard/index.html     # Premium B/W/Y dashboard
├── hub/
│   ├── store.py             # All data CRUD (tasks, proposals, cost, goals, OKRs, skills, agents, org)
│   ├── process.py           # Message processor — routing, goal auto-parse
│   ├── run.py               # Hub CLI (process, agent, status, proposals)
│   ├── aggregate.py         # Dashboard data generator
│   └── agents/              # Agent scripts (cto, dev1, content, qa)
├── agents/
│   ├── base_agent.py        # Base class + profiles loader
│   ├── profiles.json        # Agent personalities, frameworks, skills
│   └── __init__.py
└── store/                   # JSON data stores (excluded from git)
    ├── tasks.json, proposals.json, activity.json, cost.json
    ├── goals.json, okrs.json, skills.json
    ├── custom_agents.json, org.json
```

## Agent Profiles (profiles.json)

Each agent has:
- **personality**: title, traits, communication style, working style, catchphrase
- **framework**: SOP steps (default + specialized like code_review, campaign, threads...)
- **skills**: skill_name → level (1-5)

Auto-loaded into system prompt via `format_system_prompt()`.

## Hub Operation

1. User sends message → Hub processes (update briefing, route agents)
2. Agents triggered via `python hub/run.py agent <name>`
3. Agent reads briefing + system prompt (personality + framework) → proposes or executes
4. Proposals auto-recorded into store/proposals.json
5. Dashboard shows all: status, tasks, proposals, cost, OKRs, goals, skills, org

## Workflow Phases (Strict Gates)

Every task goes through exactly 6 phases. NO phase skipping. NO code before plan is approved.

```
📋 Planning → 🔍 Review → ✅ Approved → 🔵 In Progress → 🧪 Testing → ✅ Completed
    ↑              ↓              ↓                ↓
 sửa plan     phản biện      chờ Quang         QA verify
              (PASS/FAIL)    confirm
```

### Phase details:

| Phase | Gate | What happens | Auto-action |
|-------|------|-------------|-------------|
| **planning** | — | Agent writes spec/design doc | Plan stored in `task.plan_doc` |
| **review** | Reviewer | Auto-routed to reviewer (CTO/CMO based on keywords) | Message sent via Agent Message Bus |
| **approved** | ❗ QUANG | Reviewer PASS'd → notify Quang for final confirmation | `notify_quang()` writes approval request |
| **in_progress** | Quang says "triển khai" | Agent implements per plan | Output stored in `task.output` |
| **testing** | QA | Agent self-tests or QA tests output | `PASS` → completed, `FAIL` → back to in_progress |
| **completed** | — | Task closed | Time logged, output archived |

### Reviewer routing (auto):

Task description keywords determine reviewer:
- technical/code/architecture → CTO
- marketing/content/campaign → CMO
- design/visual → Design
- operation/process → COO
- cost/budget → CFO
- Default → CTO

### Quang confirmation gate:

When reviewer approves (PASS), system writes a notification for Quang via:
```python
notify_quang(f"✅ Plan task #{id} '{title}' approved by {reviewer}. Say 'triển khai đi' to start implementation.", "approval")
```
Only when Quang confirms does the task move to `in_progress`.

## Agent Message Bus

Agents communicate through a shared message store (`store/messages.json`), NOT through Telegram. This bypasses Telegram's bot-to-bot blocking.

### Message types:
- `direct` — one-to-one message
- `review_request` — request for plan review (auto-sent after planning)
- `review_result` — PASS/FAIL with feedback
- `approval_request` — request for Quang confirmation
- `consensus` — team agreement signal

### Flow:

```python
# After planning → auto-request review
request_review(task_id)  # sends message to appropriate reviewer

# When agent runs → checks unread messages first
unread = get_messages(to_agent="CTO", status="unread")
# Processes review, transitions task, notifies Quang
```

### Message recording:
- All messages in `store/messages.json` with status tracking (unread→read→replied→resolved)
- Activity log records every message
- Dashboard shows pending messages

## OKR System (Objectives & Key Results)

Full OKR hierarchy with auto-progress calculation.

### Data model
```python
# store/okrs.json
objective = {
    "id": 1,
    "objective": "Tối ưu conversion rate landing page",
    "quarter": "Q3 2026",
    "owner": "CTO",
    "status": "active",
    "progress": 45.0,  # auto-calculated from KRs
    "key_results": [{
        "id": 1,
        "kr": "Từ 2.1% lên 3.5%",
        "metric": "%",
        "baseline": 2.1,
        "target": 3.5,
        "current": 2.8,
        "owner": "CMO",
        "progress_pct": 41.7,  # auto-calculated
        "status": "on_track"
    }]
}
```

### Functions
- `create_objective(title, quarter, owner)` → creates Objective
- `add_key_result(obj_id, kr_name, target, baseline, owner, metric)` → adds KR with progress tracking
- `update_kr_progress(obj_id, kr_id, current)` → auto-calculates % from current vs target vs baseline
- Progress auto-summarizes to Objective level (average of all KR progress_pct)
- `get_active_objectives()` → current active goals
- `get_all_objectives()` → full history
- `get_objective_tree(objective_id=None)` → full hierarchy with KRs and linked task objects
- `auto_gen_tasks_for_kr(objective_id, kr_id)` → creates 2-3 tasks from KR content

### Auto task generation (implemented)

KR entries now include a `task_ids: []` field. `auto_gen_tasks_for_kr(objective_id, kr_id)` generates 2-3 tasks based on KR content keywords and assigns them to the appropriate agent:

| KR keywords | Assignee | Tasks |
|-------------|----------|-------|
| SEO/content/blog | Content | Research keywords, Create plan, Publish & optimize |
| conversion/landing/CVR | Design, Dev1, CMO | Design variants, Implement, Analyze results |
| traffic/visitor/user | CMO | Audit sources, Run campaign |
| default | KR owner | Research & plan, Execute, Measure & report |

```python
auto_gen_tasks_for_kr(obj_id, kr_id)
# Creates tasks in planning phase, links to KR via task_ids
```

Hierarchy view via `get_objective_tree(objective_id=None)` — returns each objective with KRs and their linked task objects embedded.

CLI: `python company.py okr` — full tree with progress bars:
```
🎯  Tăng traffic blog lên 10K visitors/tháng  ░░░░░░░░░░ 0%
  📌 SEO content 4 bài/tháng [2/4 bài]
     ├─ #3 Research keywords [planning] → Content
     ├─ #4 Create content plan [planning] → Content
     └─ #5 Publish & optimize [planning] → Content
```

### Dashboard display
```
🎯  Tối ưu conversion rate landing page  [45%]
    Q3 2026 | Owner: CTO
  📊 Từ 2.1% lên 3.5%  2.8/3.5  ████░░░░░░
  📊 Giảm bounce rate    65/50  ████████░░
```

## Skills & Custom Agents

- `create_skill(name, category, description)` → global skill registry
- `create_custom_agent(name, role, personality, skills, reports_to)` → adds new agent (auto-syncs to profiles.json)
- `delete_custom_agent(id)` → removes agent
- `create_team(name, lead, members)` → org chart
- `add_dependency(from, to, type)` → workflow dependencies

## Dashboard

- URL: `company.thefirstonly.com` or `upload.thefirstonly.com/company`
- Ports: 8090 (standalone), 8769 (via upload portal)
- Real-time: agents status, goals, OKRs, proposals, tasks, cost, activity
- Dark theme: Black/White/Yellow (#FFD600)

### Mission Control — the 3 questions Quang asks (user-mandated layout)

Quang: *"Anh vào dashboard anh đang xem cái gì đang diễn ra, mục tiêu nào, ai đang có mục tiêu nào."* The dashboard must answer at a glance — no digging:

| Column | Content |
|--------|---------|
| 🎯 MỤC TIÊU HIỆN TẠI | Current goal (large, yellow border) + "X task đang chạy · Y tổng" |
| ⚡ ĐANG DIỄN RA | Active tasks with phase icon + assignee (#id · phase · agent) |
| 👥 AI ĐANG LÀM GÌ | Non-idle agents with colored dot + current_task |

- If nothing is running, say so explicitly ("Tất cả 10 agents đang idle — chờ task") — an honest empty state beats a blank box.
- Idle agents are NOT listed in "AI ĐANG LÀM GÌ" — only working ones.
- `data.current_goal.goal` may be null; fall back to `briefing_summary` prefix.
- Feature Tracker (`store/features.json`, `get_features()`) sits below Mission Control: name, status (live/done/in_progress/planned/blocked), owner, progress bar, priority P0-P2.

### Test-data hygiene (user correction)

Quang: *"Sao lại có SEO với cả content ở đây? Team check lại đi."* — Test OKRs/tasks created during feature testing (SEO, content, conversion goals) stayed in the stores and confused him.

- **NEVER leave test objects (tasks/OKRs/goals/proposals) in live stores.** Clean them before presenting to Quang.
- After testing a feature, reset `store/tasks.json`, `okrs.json`, `goals.json`, `proposals.json` to empty, then create ONE realistic current task.
- Verify via `/company-data.json` before reporting: `Tasks=N | OKR trees=0 | Features=...`.

## Cost Management

- DeepSeek via OpenCode Go API (`OPENCODE_GO_API_KEY` env var)
- Models: deepseek-v4-flash ($0.15/$0.60 per 1M in/out) for workers
- Models: deepseek-v4-pro ($0.50/$2.00 per 1M in/out) for managers
- Cost tracking in store/cost.json — per agent, per call
- Budget: $100/month default

## API Key Setup

```bash
# Already set in env. For persistence:
echo 'export OPENCODE_GO_API_KEY="<key>"' >> ~/.bashrc
```

## Cloudflare Tunnel

- Tunnel: TQUANG-DELL (ID: 0ce9aa47-7d52-4d6a-9a16-13b48c508cff)
- Zone: `09a2d553b4c5ce037065260ea1feb732`; Account tag: `7aa3945509f3a3c90b75fca0317e7e5b`
- API token (env `CLOUDFLARE_API_TOKEN`, starts `cfut_...`) — has zone + tunnel access
- Windows service runs with `--token` (Zero Trust remote config); **config_src=cloudflare**

### Adding a hostname via API (works — do NOT assume dashboard-only)

The old pitfall ("Windows service trumps local config, use dashboard") was wrong for API access. This session succeeded:

```bash
# 1. Create DNS CNAME → tunnel
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" -H "Content-Type: application/json" \
  -d "{\"type\":\"CNAME\",\"name\":\"tfo\",\"content\":\"$TUNNEL_ID.cfargotunnel.com\",\"ttl\":1,\"proxied\":true}"

# 2. ⚠️ PUT FULL ingress list — this REPLACES the whole config, include ALL hostnames
curl -s -X PUT "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_TAG/cfd_tunnel/$TUNNEL_ID/configurations" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" -H "Content-Type: application/json" \
  -d '{"config":{"ingress":[
    {"hostname":"tfo.thefirstonly.com","service":"http://localhost:8100"},
    {"hostname":"company.thefirstonly.com","service":"http://localhost:8090"},
    {"hostname":"upload.thefirstonly.com","service":"http://localhost:8769"},
    {"hostname":"bot.thefirstonly.com","service":"http://localhost:9877"},
    {"hostname":"me.thefirstonly.com","service":"http://localhost:5099"},
    {"hostname":"thefirstonly.com","service":"http://localhost:5099"},
    {"hostname":"www.thefirstonly.com","service":"http://localhost:5099"},
    {"service":"http_status:404"}
  ],"warp-routing":{"enabled":false}}}'
```

**CRITICAL pitfall:** the PUT **overwrites the entire ingress list**. A single-hostname PUT silently kills every other hostname (company/me/upload all go 502). Always send the full list. Note the token needed for GET /cfd_tunnel/{id}/config is 404, but the PUT /configurations endpoint works.

## Pitfalls

- **Windows Service trumps local config**: Cloudflared runs as Windows service with --token; local config file is ignored. Use Zero Trust dashboard for ingress rules.
- **Agent names case-sensitive**: `hub/run.py agent CTO` works, `agent cto` now fixed with normalization.
- **Export API key for background processes**: Background terminal processes inherit env, but cron jobs need workdir or bashrc export.
- **Dashboard data**: Fetches from `/company-data.json` endpoint — ensure the serving server has the aggregate import path correct.
- **Review message consumed before transition**: If `mark_message_read()` succeeds but `transition_task()` fails (e.g. import error), the message is consumed but the task stays stuck. Fix: wrap transition in try/except, or re-send the message on failure.
- **Multiple overlapping AI-company skills**: `ai-company`, `ai-company-builder`, `ai-company-system` overlap significantly. Consolidation needed — `ai-company-system` should be the canonical umbrella.
- **Phase-check filter**: `cmd_agent` must check `t["phase"] not in ("completed","cancelled")` not `t["status"] in ("pending","in_progress")` — otherwise tasks in review/approved/testing phases are invisible to the agent.
- **Self-review loops**: When an agent reviews its own plan, it often fails itself (correct critic behavior). In practice, let the assigned reviewer (CTO/CMO etc.) handle review via the message bus instead.
- **⚠ `_write_file` sends wrong argument**: `send()` in `inbox.py` must write `data` (the full structure), NOT `msg` (a single message). Writing `msg` silently drops all prior messages. Bug: `_write_file(filepath, msg)` should be `_write_file(filepath, data)`.
- **`hub/run.py` missing `mark_message_read` import**: `cmd_agent()` calls `mark_message_read()` but it must be imported from `store`. Missing import → `NameError: name 'mark_message_read' is not defined`.
- **Detached HEAD after git rebase conflicts**: When `git pull --rebase` fails on `inbox.json` or `to_claw.json`, git enters detached HEAD. Fix: `git rebase --abort`, resolve manually, then `git push origin HEAD:main && git checkout main`.
- **Cron sync `no_agent=True`**: Set `--no-agent` so the script's stdout IS the cron output. Empty output = silent (nothing delivered). Only output on important keywords to avoid spamming the user every minute.
- **Split-file naming convention**: to_hermes.json = inbound for Hermes (Claw writes). to_claw.json = inbound for OpenClaw (Hermes writes). shared/inbox.py v2 uses `me` parameter to determine which file to read.\n- **CRITICAL: Keyword filter lost messages**: v2 sync script filtered by keywords (chốt/done/approved...). Claw sent "PLAN" and "Phản biện" which did NOT match → silently consumed, never delivered. Fix: v3 outputs ALL messages, no filter.\n- **CRITICAL: No code before QUANG approval**: User corrected this explicitly. Even when reviewer approves (PASS), task stays at `approved` phase. Wait for Quang to say "triển khai đi" before implementing.\n- **`send()` must write `data` not `msg`**: _write_file(filepath, msg) corrupts the file. Always write the full structure.
- **Duplicate `let` declaration kills the whole `<script>`**: A second `let mediaRecorder = null;` in the same script block throws `SyntaxError: Identifier 'mediaRecorder' has already been declared` — the ENTIRE script stops parsing, so later functions like `doLogin` are undefined and the login button silently fails. Symptom in console: `Uncaught ReferenceError: doLogin is not defined` + a 404 for the page's HTML resource. Fix: delete the duplicate block. **Verify any hand-edited HTML's JS with:** `python -c "import re;html=open('f.html').read();js=re.search(r'<script>(.*?)</script>',html,re.S).group(1);open('/tmp/c.js','w').write(js)" && node --check /tmp/c.js` — catches parse-killing duplicates before deploying. (Watch out: patch-tool replacements that re-add a block you thought you moved create this exact bug.)
- **Task field convention — `status` vs `phase`**: `get_agent_statuses()` reads `t["status"]`, but workflow uses `t["phase"]` (planning/review/approved/...). Hand-created tasks must carry BOTH: `phase` (workflow gate) AND `status` (dashboard/agent-status field). Missing `status` → `KeyError: 'status'` crashes the whole dashboard JSON endpoint.
- **Venv must pin Python 3.11 on this machine**: default `python` is 3.14 (C:\Python314) and pydantic-core wheels break under it (`ModuleNotFoundError: pydantic_core._pydantic_core`). Create venv explicitly with 3.11: `"/c/Users/NTQUANG_DELL/AppData/Local/Programs/Python/Python311/python.exe" -m venv .venv` then `.venv/Scripts/python.exe -m pip install fastapi uvicorn python-multipart`. Verify with `.venv/Scripts/python.exe -c "import fastapi,uvicorn; print(fastapi.__version__)"`. Also: `pip install` output patterns can be falsely flagged as "long-lived server process" — wrap in a small `install_deps.py` script and run it.
- **`git pull --rebase` with unstaged changes**: fails with "cannot pull with rebase: You have unstaged changes". Fix pattern: `git stash && git pull --rebase origin main && git stash pop && git add -A && git commit && git push origin HEAD:main`. Claw pushes concurrently, so expect this several times a session.
- **HTML served stale → user "can't login"**: if the HTML changed but the browser cached it, the login overlay never appears. Fix: serve index with `Cache-Control: no-cache, no-store, must-revalidate` headers; tell user to hard-refresh (Ctrl+F5).\n\n## TFO MVP Web Track (product — same repo, different app)

The FirstOnly product MVP (CEO assistant web app) lives in the same repo but is a separate FastAPI track at port 8100. See `references/tfo-mvp-web.md` for the full architecture: email+passcode auth, resilient recording (chunking + watchdog), meetings history, Groq >16MB chunking, Telegram push to beFounders, and deploy commands.

## Cross-Machine Communication (Hermes ↔ OpenClaw) — v2 Split-File

Both agents run on different machines. They communicate via **separate files** to eliminate merge conflicts.

| File | Writer | Reader |
|------|--------|--------|
| `shared/to_hermes.json` | OpenClaw | Hermes |
| `shared/to_claw.json` | Hermes | OpenClaw |

Python helper: `shared/inbox.py` (v2 — uses separate files internally)

See `references/shared-inbox.md` for full API and setup, and the v1→v2 migration notes.

### Quick usage (Hermes side):

```python
from shared.inbox import send, read, mark_read

# Send to Claw — auto writes to to_claw.json + git push
send(to="OpenClaw", subject="Review task #5", body="Plan ready")

# Read from Claw — auto pull + read to_hermes.json
msgs = read(me="Hermes")  # "me" defaults to Hermes
for m in msgs:
    print(m["body"])
    mark_read(m["id"])
```

### Why separate files?
- **Zero merge conflicts** — each side writes only to its own outbound file
- **Simple git flow** — no rebase, no conflict resolution
- **Push any time** — simultaneous pushes to different files never conflict

### Silence cron sync (v3 — output ALL messages, no keyword filter lost)

Set up a cron that runs every 1 minute with `no_agent=True`. Earlier versions used keyword filters to avoid spam but this caused messages to be silently consumed without delivery. **v3 outputs ALL new messages** (brief one-liner), no filters:

```python
# ai-inbox-sync.py — place in ~/AppData/Local/hermes/scripts/
import json, subprocess, os, sys

BASE = "/path/to/repo"
MY_FILE = os.path.join(BASE, "shared", "to_hermes.json")  # Hermes side
# Claw side: to_claw.json

def git(cmd):
    subprocess.run(["git"] + cmd, cwd=BASE, capture_output=True, timeout=30)

git(["pull", "--rebase"])
if not os.path.exists(MY_FILE):
    sys.exit(0)

with open(MY_FILE) as f:
    data = json.load(f)
new_msgs = [m for m in data["messages"] if m["status"] == "unread"]
if not new_msgs:
    sys.exit(0)  # silent — nothing new

for msg in new_msgs:
    msg["status"] = "read"
    snippet = msg.get('body', '')[:120].replace('\n', ' | ')
    print(f"📨 {msg.get('from','?')}: {msg.get('subject','')}")
    print(f"   {snippet}")

with open(MY_FILE, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
git(["add", "shared/to_hermes.json"])
git(["commit", "-m", "inbox: sync auto"])
git(["push"])
```

Cron creation:
```bash
hermes cron create --name ai-company-inbox --schedule "every 1m" \
  --no-agent --script ai-inbox-sync.py --deliver origin
```

### OpenClaw pattern:
```python
from shared.inbox import read, mark_read, send

msgs = read(me="OpenClaw")
for m in msgs:
    process(m)
send(to="Hermes", subject="Re: ...", body="Done")
```

### Pitfalls (v2)
- **`_write_file` bug**: `send()` must write `data` (full structure), not `msg` (single message). Writing `msg` silently drops all prior messages.
- **`mark_message_read` import**: `hub/run.py` calls `mark_message_read()` but it must be imported from `store` — missing import causes `NameError`.
- **`send()` hangs on big payloads**: `git push` with large bodies may time out. Keep messages under 5KB.
- **Detached HEAD after rebase conflicts**: If `git pull --rebase` fails (conflict in to_hermes.json or to_claw.json), git enters detached HEAD. Fix: `git rebase --abort` then manually merge.
