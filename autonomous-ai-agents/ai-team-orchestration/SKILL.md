---
name: ai-team-orchestration
category: autonomous-ai-agents
description: Design, build, and operate multi-agent AI teams — agent roles, inter-agent communication, workflow enforcement, OKRs, cross-machine sync.
trigger: user asks to build an AI company, AI team, multi-agent system, or agent orchestration
tags:
  - multi-agent
  - orchestration
  - agent-communication
  - workflow
  - okr
---

# AI Team Orchestration

## 🔴 CRITICAL: Real agents vs Script agents (lesson 2026-09-22)

**Agents MUST be real Hermes subagents with tool access via `delegate_task`, NOT Python scripts.**

Quang caught this immediately: "task này nó trả ra task gì cả mà kết quả nó không phù hợp". Root cause: `worker_v2.py` was a deterministic Python script with no LLM, no web search, no file read — it could only generate template text from input. The result was always a fake.

**Right pattern:**

```
Task → inbox agent
  → Watchdog cron (no_agent=True, silent) detects + sets status "pending"
  → CEO runs `python company.py check` to see pending tasks
  → CEO dispatches via `delegate_task` with full context
  → Subagent is a REAL Hermes session with terminal, read_file, search tools
  → Subagent produces actual research/content/code
  → Writes result.json + report.html
  → Reports back to CEO inbox via message_bus.report_done()
  → Sets status idle
```

**Wrong pattern (what NOT to do):**

```python
# worker_v2.py — script-only, no tools, no LLM
def process_tasks(agent_id):
    for msg in read_inbox(agent_id):
        result = _execute_task(agent_id, payload)  # just templates
        write_result(result)  # always fake content
```

**Why scripts fail for agent work:**

| Script | Hermes subagent |
|--------|----------------|
| No tool access | Full tool access (terminal, read_file, search) |
| No LLM reasoning | Full LLM reasoning |
| Template text only | Real web research, analysis |
| Cheap (0 tokens) | Costs tokens per call |
| Good for: watchdog, detect, set status | Good for: actual agent work |

**Where to use each:**

| Component | Method | Why |
|-----------|--------|-----|
| **Watchdog** (check inbox, set status) | `no_agent=True` cron script | Deterministic, fast, silent |
| **Agent work** (research, code, sales) | `delegate_task` subagent | Needs tools + LLM |
| **CEO dispatch** (route tasks) | Hermes prompt (this conversation) | Needs reasoning to route correctly |

**The transparency layer proved this:** the first demo ran `worker_v2.py` scripts — Quang saw empty templates. The second demo used `delegate_task` to a real subagent — it produced actual EZ80 competitor data with prices, ingredients, comparison table (9.6KB result). Same task, different execution model.

## 🔴 HARD RULE: Critique first, always

Never code before the plan is solid. The user enforces a strict stage-gate:

```
User says "làm cái X"
  → Brainstorm với partner agent (Claw) qua inbox
  → Viết proposal: design, cost, time, trade-offs
  → Gửi user phản biện
  → User: "Triển khai đi" ✅
  → Code + push
  → Partner review code
  → User confirm → merge
```

Violations hurt trust. If the user says "ủa, anh đã duyệt gì đâu mà thực thi vậy", stop immediately and present the unapproved work as a proposal for review, not as a deliverable. No exceptions.

Design and operate a team of AI agents working together toward shared goals. This skill covers the architecture patterns, communication models, and workflow enforcement used in production multi-agent systems.

## Architecture Patterns

### 1. Agent Profile System
Each agent needs three layers:

```
Personality    → title, traits, communication style, working style, catchphrase
Framework      → SOPs (default + specific: code_review, campaign, bug_fix...)
Skills         → name + level (1-5), used for task routing
```

**Implementation:** Store in `agents/profiles.json`. Base agent class loads profile and injects into system prompt via `format_system_prompt()`.

**System prompt assembly:**
```
[Base role prompt]
→ [Personality section: traits, comm style, working style, catchphrase]
→ [Framework section: default SOP steps]
→ [Enforced workflow section: plan → review → implement → test]
→ [Skills section: skill bars with levels]
```

### 2. Communication Models

| Model | When to use | Mechanism |
|-------|------------|-----------|
| **Direct** (same machine) | Agents on same server | Shared `store/messages.json` — agent writes, another reads on next trigger |
| **Git-based** (cross-machine) | Hermes ↔ OpenClaw on different machines | Separate files — `to_claw.json` / `to_hermes.json` — each side writes to the other's file. NO shared file. |
| **API/Webhook** (realtime) | Need low latency | HTTP endpoint with POST/GET |
| **File-based queue** (local multi-agent) | Multiple agents on same machine, single Hermes instance | `inbox/{agent_id}.json` per agent — `message_bus.py: send/read_inbox/mark_read`. CEO dispatches, worker reads, agent reports back. Watchdog cron (1m, no_agent=True) auto-processes inboxes. |

**Inter-agent handoff** — non-CEO agents can pass work between themselves:

```json
{"type": "handoff", "from": "research", "to": "sales",
 "subject": "Handoff: outreach draft for T-001",
 "body": "...findings...", "ref_task_id": "T-001"}
```

CEO routes task → Agent A → Agent A sends `handoff` to Agent B → Agent B reports to CEO. Both results in CEO inbox. Worker_v2 handles both `task` and `handoff` message types. Use `send(from, to, subject, body, msg_type="handoff", ref_task_id=task_id)` from `message_bus.py`.

**Git-based shared inbox pattern (v2 — separate files, no conflict):**
```
shared/
  inbox.py      → send(), read(), mark_read()
  sync.py       → cron script v3: output ALL messages, no keyword filter
  to_hermes.json → Claw writes → Hermes reads (git tracked)
  to_claw.json   → Hermes writes → Claw reads (git tracked)
```

**Critical: v1 used a single `inbox.json` shared file → merge conflicts every time both wrote simultaneously.**
**Fix v2: each machine writes ONLY to the other's file. No conflict possible.**

**Silent cron pattern (v3):**
Earlier versions used keyword filters ("chốt", "approved", "cần anh"...) → messages that didn't match were silently consumed and never delivered. Fix: output ALL messages from the other agent, each as one line. No filtering. Use 1-minute interval, `no_agent=True`.

**Message format:**
```json
{
  "id": 1,
  "from": "Hermes | OpenClaw | AgentName",
  "to": "Hermes | OpenClaw | AgentName",
  "subject": "Review request: Task title",
  "body": "Full message content",
  "type": "direct | review_request | reply",
  "ref_task_id": 5,
  "status": "unread | read",
  "created_at": "2026-07-27 00:03:02"
}
```

### 3. Workflow Enforcement (Phase-Gate)

Every task MUST go through phases in order:

```
📋 Planning → 🔍 Review → ✅ Approved → 🔵 In Progress → 🧪 Testing → ✅ Completed
                 ↑            ↓              ↓                ↓
              sửa plan    chờ duyệt      code/build       QA verify
```

**Implementation:**
- Task store has `phase` field instead of just `status`
- `transition_task(task_id, new_phase)` validates phase order
- Agent `cmd_agent()` checks current phase and acts accordingly:
  - `planning` → write spec → auto-request review
  - `review` → critique plan, PASS or FAIL
  - `approved` → wait for human confirmation "triển khai"
  - `in_progress` → implement
  - `testing` → QA verify

### 4. Auto-Review Routing

Route review requests based on task content keywords:

```python
REVIEWER_ROUTES = {
    "technical": "CTO",
    "code": "CTO",
    "marketing": "CMO",
    "content": "CMO",
    "design": "Design",
    "cost": "CFO",
    "process": "COO",
}
```

### 5. OKR System

```json
{
  "objectives": [{
    "objective": "Tối ưu conversion rate",
    "quarter": "Q3 2026",
    "owner": "CTO",
    "key_results": [{
      "kr": "Conversion từ 2.1% lên 3.5%",
      "baseline": 2.1,
      "target": 3.5,
      "current": 2.1,
      "owner": "CMO",
      "metric": "%",
      "progress_pct": 0,
      "task_ids": [3, 4, 5]
    }]
  }]
}
```

**Hierarchy: Objective → KR → Tasks (linked via `task_ids`).**

Auto-calculates objective progress from KR progress. Auto-gen tasks from KR content via `auto_gen_tasks_for_kr()` which routes based on keywords (SEO → Content, conversion → Dev1+Design, traffic → CMO). Generated tasks start in `planning` phase and MUST go through the full workflow — no shortcuts.

`python company.py okr` — displays full tree from CLI.

### 6. Skill Registry

Central skill catalog + per-agent skill assignment. Skills from profiles.json sync into the registry for cross-referencing.

### 7. Team Architecture Patterns (chọn pattern trước khi delegate)

Trước khi spawn agent, chọn pattern theo bảng + decision tree đầy đủ trong `references/team-architecture-patterns.md`. Tóm tắt nhanh:

| Pattern | Dùng khi | Hermes mode |
|---------|----------|-------------|
| Pipeline | Chuỗi phụ thuộc mạnh | delegate tuần tự, task sau nhận output task trước |
| Fan-out/Fan-in | Nhiều góc nhìn độc lập, cùng đầu vào | **batch delegate (max 3)** + 1 task gộp |
| Expert Pool | Input khác loại → xử lý khác nhau | sub-agent đơn, agent chính tự chọn skill |
| Producer-Reviewer | Chất lượng quan trọng, tiêu chí khách quan | delegate tạo + task review agent KHÁC, retry cứng 2-3 lần |
| Supervisor | Phân việc động theo tiến độ runtime | orchestrator giữ task list, dispatch từng bước |
| Hierarchical Delegation | Phân cấp tự nhiên | **Cẩn thận:** Hermes max_spawn_depth=1 → flat hóa |

Quyết định nhanh: ≥2 agent và cần đối chiếu/feedback → team mode (batch). Chỉ cần trả kết quả → sub-agent. 1 agent → sub-agent đơn.

Kèm 3 quy tắc vận hành (chi tiết trong reference):
- **Reuse review trước khi tạo agent/skill mới** — agent cũ phủ vai trò thì dùng lại, generalize trước khi tạo mới.
- **Phase selection khi mở rộng** — audit hiện trạng → route build mới / thêm agent / thêm skill / đổi kiến trúc, mỗi loại chỉ chạy subset bước cần thiết.
- **Evolution loop** — sau mỗi run hỏi feedback; feedback lặp ≥2 lần, agent fail lặp lại, hoặc user bypass orchestrator → tự đề xuất sửa skill/agent/orchestrator tương ứng, ghi change history 4 cột (ngày, nội dung, đối tượng, lý do).

## Transparency & Observability (multi-agent, added 2026-09-22)

User expects to see xuyên suốt what each agent is doing and result per task — not just demo JSON. Wire this BEFORE claiming multi-agent is done.

| Layer | File | What it does |
|-------|------|--------------|
| **Activity Log** | `logs/activity.jsonl` — JSONL append-only (`activity.py`: `log()`, `get_recent()`, `get_task_activity()`) | Every agent step logged: `watchdog → task_received → started → analyzing/drafting → analysis_complete → task_complete`. Dashboard reads `get_recent(15)`. Report reads `get_task_activity(task_id)` for per-task timeline. |
| **Task HTML Report** | `tasks/{task_id}/report.html` — generated by `tasks/report.py: generate_report()` | One HTML per task: Task Info (title/desc/context/deadline), Activity steps for that task, Result summary, Raw JSON. Served via `GET /task/{id}` on dashboard server. |
| **Dashboard feed** | `dashboard/server.py: /data` includes `activity` + `tasks[]` with `report_url`; `dashboard/index.html` renders activity feed + task list with Report → link | Real-time 10s refresh. `GET /data` returns `{agents, inbox, activity, tasks, stats}`. |
| **Worker v2** | `agents/worker_v2.py: process_tasks()` | Real content per role (research/sales/dev), logs each step via `activity.log()`, writes `result.json`, calls `_generate_report()`, marks read + idle. Replaces `worker.py` demo. |
| **Workspace CLI** | `company.py` now imports `worker_v2` | `python company.py status/inbox/watch` works end-to-end (use `cd ~/ai-company-v2 && python ...` — bare `~/` literal fails on cpython-314). |

**When to use:** any multi-agent system where CEO dispatches and user needs transparency per task. Always wire activity log before claiming transparency is done.

### Dashboard Server Pattern

Run a lightweight Python `HTTPServer` that serves both the dashboard HTML and a JSON data API — no need for a separate backend framework.

```python
# dashboard/server.py
class DashboardHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/data":        # JSON API
            data = self._build_data()   # agents + inbox + activity + tasks
            self.wfile.write(json.dumps(data))
        elif self.path.startswith("/task/"):  # Task HTML reports
            task_id = self.path.split("/task/")[-1]
            self.wfile.write(report_path.read_bytes())
        else:                           # Static files (index.html, CSS)
            super().do_GET()
    def do_POST(self):
        if self.path == "/dispatch":    # Dispatch task from web
            body = self.rfile.read()
            payload = json.loads(body)
            ceo_dispatch(...)
```

**Endpoints:**
| Route | Method | Returns |
|-------|--------|---------|
| `/` | GET | Dashboard HTML (index.html) |
| `/data` | GET | JSON: `{agents, inbox, activity, tasks, stats}` |
| `/task/{id}` | GET | HTML report for that task |
| `/dispatch` | POST | JSON: dispatch result |

Start with `terminal(background=true)` on port 5050. Expose via localtunnel: `lt --port 5050 --subdomain ai-company-v2`. Dashboard auto-refreshes every 10s via `setInterval(fetch('/data'), 10000)`.

**When to use:** any multi-agent system where the user wants a web view of agent status, inbox, activity feed, and task reports. Wire this AFTER the activity log and task report generator exist.

## Pitfalls

- **🔴 Subagent research timeout → SALVAGE, không chạy lại** — delegate batch research dài (browser search + fetch nhiều trang) hay bị `status=interrupted` sau ~2400s, nhất là task cuối batch. TRƯỚC khi đánh giá thất bại hoặc chạy lại:
  1. Đọc live transcript: `~AppData/Local/hermes/cache/delegation/live/<delegation_id>/task-N.log` — thấy subagent đã chạy query nào, ghi file gì.
  2. Tìm file trung gian subagent đã ghi (VD: JSONL batch search format `{"q":..., "ts":..., "results":[{"u":url,"t":title,"s":snippet}]}` đặt ở project root, thường `_<tên>*.jsonl` hoặc thư mục research riêng).
  3. Đọc lại JSONL bằng execute_code (parser cho key `u/t/s`, KHÔNG dùng `url/snippet`) → gom đủ kết quả search + snippet, tự tổng hợp báo cáo; chỉ chạy lại subagent nếu thực sự thiếu dữ liệu.
  Kết quả session 09/2026: task 3/3 agrivoltaics bị interrupted nhưng 8 file `_agri*.jsonl` đã chứa ~40 query x case study + giá cả → tổng hợp xong báo cáo không cần chạy lại.
- **🔴 Session reset giữa chừng → mất kết quả delegation, vẫn SALVAGE được từ log** — khi conversation bị reset (VD daily schedule) trước khi consolidated result của `delegate_task` re-enter, kết quả KHÔNG mất hẳn. Log live transcript vẫn còn nguyên: `~AppData/Local/hermes/cache/delegation/live/<delegation_id>/task-N.log`. Cách lấy lại:
  1. Dòng `final | status=completed ... summary:` ở CUỐI mỗi task-N.log chứa summary nhưng thường bị cắt `(+N chars)`.
  2. Dùng execute_code đọc cả file log, grep theo từ khóa (`MASOTHUE`, `Địa chỉ`, `MST`, tên pháp nhân...) để trích block kết quả trung gian — thường chứa đầy đủ dữ liệu bị cắt ở summary.
  3. File trung gian subagent viết vào `~/httptmp/` hoặc project dir cũng còn (VD `mnv_*.py`, `*_search*.py`) — đọc lại để lấy script + output.
  Kết quả session 09/2026: MOU 3 bên — 3 subagent tra pháp nhân đã completed nhưng session reset trước khi result về; recover 100% dữ liệu từ task-0/1/2.log + script httptmp, không cần chạy lại delegation.
- **🔴 Deliverable của subagent PHẢI verify trước khi báo user** (verified 18/10/2026) — summary subagent là **SELF-REPORT**, không phải fact. Ca thật: 2 subagent research báo "deliverable complete and verified, 102 PMID, đã đọc abstract 100%" → parent tự verify mới lộ ra **1 kết luận pháp lý đã LỖI THỜI** mà subagent đã gắn tag [F] và còn gọi là "cực kỳ quan trọng". Nếu relay thẳng thì đã báo sai cho founder. Quy trình 4 bước, chạy TRƯỚC khi relay bất kỳ con số/kết luận nào:
  1. **Kiểm artifact vật lý** — `os.path.getsize()` từng file mà subagent nói đã ghi; so với con số trong summary (summary ghi "~84 KB" mà file 0 byte / không tồn tại = subagent bịa). Kèm `os.walk` để thấy file nào thực sự có.
  2. **Spot-check citation trên nguồn gốc** — không đọc lại hết; lấy 10–15 citation quan trọng nhất và mở trên API gốc, đối chiếu **title** với claim mà nó supposedly chống đỡ. PMID → Europe PMC (`EXT_ID:<pmid>&resultType=lite`). Script sẵn: `pubmed-evidence-research/scripts/verify_pmids.py`.
  3. **Đọc phần summary bị cắt** — summary dài bị chèn `[... middle omitted ...]` kèm đường dẫn file đầy đủ. Phần bị cắt thường chứa đúng danh sách điểm yếu/rủi ro. Đọc lại file cache TRƯỚC khi kết luận "subagent không nói gì về X".
  4. **Săn cái SAI, đừng săn cái đúng** — chọn claim **quyết định nhất** trong deliverable rồi tự tra nguồn gốc. Với claim pháp lý/quy định: tra **văn bản hợp nhất** (văn bản ban hành sau có dừng điều khoản đó không) — đây là nơi lỗi ẩn nhiều nhất, vì nó "trông đúng" ở bản gốc.
  Báo cho user **đã verify được gì và bằng cách nào** (số citation đã mở, so size file), không chỉ nói "đã kiểm tra".
- **🔴 Trần `delegation.max_iterations` (mặc định 50) giết con đang viết dở** (19/10/2026) — con tự khai *"hết lượt gọi tool giữa chừng"* và **không có file deliverable nào**. Không phải timeout, không phải provider hỏng. TRƯỚC khi dispatch batch có viết file: `hermes config get delegation` → nếu `max_iterations` ≤ 50 thì `hermes config set delegation.max_iterations 140`. Ước lượng ngân sách theo **khối lượng viết** (1 đầu việc vừa tra vừa viết ≈ 20 calls → tối đa 2–3 đầu việc/con), bắt con **ghi file ngay sau mỗi đầu việc** thay vì dồn về cuối, và để **builder deterministic của parent** gộp file — con không tự viết file tổng hợp. Chi tiết + ca thật trong `references/delegation-split-research-authoring.md`.
- **🔴 Skipping critique step** — Most dangerous violation. User explicitly enforces: brainstorm → phản biện → duyệt → triển khai. If you skip, you lose trust. Always stop at proposal stage until user says "Triển khai đi".
- **Silent cron keyword filter** — Don't filter messages by importance keywords. Output ALL messages from the other agent. v1 had keyword filter → messages like "PLAN" and "Phản biện" were silently consumed with no delivery. v3 outputs everything.
- **Git merge conflicts** on shared file — Both writing to the same file causes conflicts. Fix: each side writes to their own file (`to_hermes.json`, `to_claw.json`). Never share a single inbox file between two agents.

- **Git merge conflicts** on shared inbox.json — both machines writing concurrently. Resolve by keeping all messages with distinct IDs, renumbering conflicting ones. Use `sync_pull()` before write to minimize conflicts. After conflict, git workflow: `git add shared/inbox.json && git rebase --continue` (if mid-rebase) or `git reset --hard origin/main && git push origin HEAD:main`.
- **Detached HEAD after rebase** — when rebase conflicts leave you in detached HEAD state. Fix: `git push origin HEAD:main && git checkout main && git reset --hard origin/main`.
- **Agent never finishes** — always set timeout on agent calls. Use background processes with `notify_on_complete` for long tasks.
- **Cost runaway** — each DeepSeek API call is tracked per-agent. Set daily budget cap per agent.
- **Review loops** — agent reviewing its own plan tends to FAIL itself. Route review to a DIFFERENT agent for proper critique.
- **Telegram blocks** bots can't message each other. Use shared file/message bus instead.
- **Silent cron needed** — 1-min sync cron must use `no_agent=True` and only output on important messages. Otherwise floods the chat. Script checks for keywords like "chốt", "quyết định", "approved", "reject", "cần anh" to decide if output is needed.
- **Quang notification fatigue** — only notify the human founder for phase changes that need sign-off: review approved (needs "triển khai đi"), review FAILED (needs replan), or blocker. Don't spam for every phase transition.
- **Both agents write at same time** — inbox.json will conflict. Each agent should write to their own file (`to_hermes.json`, `to_claw.json`) instead of a single shared file to eliminate conflicts entirely.

## Related Skills

- `design-critique` — critique-first design workflow (complements the Review phase)
- `plan` — structured planning before execution
- `system-design-workflow` — full-cycle system design
- `openclaw` — OpenClaw agent platform: multi-channel gateway, Telegram integration, model routing via OpenCode backend (absorbed into this umbrella)

## Reference Files

- `references/ai-company-impl.md` — Full implementation layout, agent roles, code patterns
- `references/task-workflow.md` — Phase-gate state machine, Quang notification rules, review routing
- `references/git-merge-conflicts.md` — Cross-machine inbox conflict resolution, detached HEAD recovery
- `references/silent-cron-pattern.md` — 1-minute silent cron for agent sync, importance filtering
- `references/okr-hierarchy.md` — OKR → KR → Task data flow, auto-gen logic, progress calc
- `references/git-recovery.md` — Detached HEAD, rebase stuck, lost commit recovery
- `references/prime-agent.md` — Prime Agent (Prime Intellect): agent harness self-improving (RLM + /refine), research 08/2026 trước khi cài — providers, models.json custom, Windows, rủi ro
- `references/team-architecture-patterns.md` — 6 pattern team (adapt revfactory/harness): bảng pattern, decision tree, composite, phase selection matrix, reuse review, evolution loop
- `references/grok-bot-inspired-hermes-v2.md` — Grok Bot → Hermes Multi-Agent 2.0: single-instance + Agent Registry (verified from x.ai/bot), 4-phase roadmap (13h), 7-point self-critique, teach-by-demonstration 3-stage plan
- `references/ceo-routing-table.md` — CEO keyword routing, dispatch flow, task/result data shapes
- `references/delegation-output-verification.md` — **Verify deliverable của subagent trước khi relay** (18/10/2026): checklist 4 bước (artifact thật / spot-check citation trên API gốc / đọc phần summary bị cắt / săn claim quyết định nhất), cách viết phần báo cáo verify, và ca thật bắt được kết luận pháp lý lỗi thời mà subagent gắn tag [F].
- `references/subagent-timeout-recovery.md` — Salvage kết quả khi subagent bị `interrupted`: đọc live transcript + file trung gian, không chạy lại.
- `references/delegation-split-research-authoring.md` — Chia việc cho con khi goal gồm *research + viết deliverable*: trần `delegation.max_iterations` (mặc định 50) và cách nâng; ước lượng ngân sách theo khối lượng viết; bắt ghi file ngay sau mỗi đầu việc; mẫu `src/<slug>.txt` + builder deterministic của parent; pitfall builder làm rơi trường mà tầng dưới cần.
