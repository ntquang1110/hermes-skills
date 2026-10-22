# AI Company — Full Implementation Reference

This is the concrete implementation built in the session. Use as a model for new multi-agent systems.

## Directory Structure

```
ai-company/
├── agents/
│   ├── profiles.json       # 10 agents: personality, framework, skills
│   └── base_agent.py       # Agent class, profile loader, system prompt assembler
├── hub/
│   ├── store.py            # CRUD: tasks, proposals, goals, OKRs, skills, agents, org, messages
│   ├── process.py          # NLP message routing, goal auto-parse
│   ├── run.py              # CLI: process, agent, status, proposals, review orchestration
│   └── agents/             # Agent entry scripts (cto, dev1, content, qa)
├── store/                  # Live data (gitignored)
│   ├── tasks.json
│   ├── proposals.json
│   ├── messages.json       # Agent-to-agent message bus
│   ├── okrs.json
│   └── goals.json
├── shared/                 # Tracked by git — cross-machine communication
│   ├── inbox.py            # Hermes ↔ OpenClaw send/read/sync
│   ├── inbox.json          # Message store
│   └── sync_minute.py      # Cron script — silent, only outputs on important msgs
├── dashboard/index.html    # Real-time dashboard B/W/Y theme
└── company.py              # Quick CLI: status, okr, skills, proposals
```

## Agent Initialization Flow

```
User sends message
  → process.py: parse type (goal/proposal/question/approve)
  → update company briefing (shared context)
  → wake_agents determined by keyword match
  → cmd_agent(name):
      1. Check unread messages (review requests)
      2. If review_request → process review (PASS/FAIL) → notify Quang
      3. If no messages → find my active task by phase
      4. Execute based on phase:
         planning → write plan → auto-transition to review → send message to reviewer
         review → critique plan → PASS→approved→notify Quang | FAIL→back to planning
         approved → implement → auto-transition to testing
         testing → QA verify → PASS→completed | FAIL→back to implement
      5. If no task → propose based on briefing
```

## Cron Setup (Hermes side)

```yaml
# Silently sync inbox every 1 minute, only report important decisions
cron:
  - name: ai-company-inbox
    schedule: "every 1m"
    no_agent: true
    script: ai-inbox-sync.py
    deliver: origin
```

## Key Code Patterns

### Agent System Prompt Assembly
```python
def format_system_prompt(agent_name):
    base = AGENT_SYSTEM_PROMPTS[agent_name]       # Role definition
    profile = AGENT_PROFILES[agent_name]           # From profiles.json
    # → Add personality (traits, comm style, catchphrase)
    # → Add framework (default SOP steps)
    # → Add enforced workflow (plan→review→implement→test)
    # → Add skills (skill bars with levels)
```

### Task State Machine
```python
VALID_PHASES = ["planning", "review", "approved", "in_progress", "testing", "completed"]

def transition_task(task_id, new_phase, **kwargs):
    task["phase"] = new_phase
    task["status"] = new_phase
    task.update(kwargs)  # plan_doc, review_notes, approved_by, test_results
```

### Cross-Machine Git Inbox
```python
def send(to, subject, body):
    data = pull_inbox()
    data["messages"].append(new_message)
    write_inbox(data)
    git_commit_push()

def read(to):
    git_pull_rebase()
    data = load_inbox()
    return [m for m in data["messages"] if m["to"] == to and m["status"] == "unread"]
```

## 10 Agents and Their Roles

| Agent | Role | Reports To | Key Skills |
|-------|------|------------|------------|
| CTO | Architecture, code review, tech decisions | Quang | system_design 5, python 5, code_review 5 |
| Dev1 | Primary developer | CTO | python 5, js 4, git 4 |
| Dev2 | Secondary developer | CTO | python 3, debugging 3 |
| QA | Testing, quality | CTO | manual_testing 5, bug_reporting 5 |
| CMO | Marketing strategy | Quang | growth_strategy 5, analytics 4 |
| Content | Writing, Threads, blog | CMO | copywriting 5, storytelling 5 |
| Social | Social media, engagement | CMO | social_media 4, scheduling 5 |
| COO | Operations, workflow | Quang | process_design 5, operations 5 |
| CFO | Finance, cost tracking | Quang | cost_analysis 5, budgeting 5 |
| Design | Visual, UI, brand | CMO | ui_design 5, visual_design 5 |

## Auto-Review Routing Rules

Keywords in task title/description → routed to:
- code, technical, architecture → **CTO**
- marketing, campaign, content → **CMO**
- design, visual → **Design**
- operation, process → **COO**
- cost, budget → **CFO**
- default → **CTO**
