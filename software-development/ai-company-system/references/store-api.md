# Store API Reference (hub/store.py)

## Core
- `read_briefing()` → str
- `update_briefing(key, value)` — append/replace line in briefing.md
- `add_activity(message)` — log to activity feed

## Tasks
- `add_task(title, desc, assignee, goal_id, depends_on, phase="planning")` → task dict (with phase tracking: planning→review→approved→in_progress→testing→completed)
- `transition_task(id, new_phase, **fields)` — move through workflow phases, auto-updates status + timestamps
- `update_task(id, status, output, ...)` — legacy direct status update
- `get_tasks(status=None)` — filter by status; use phase field for workflow-aware filtering

## Proposals
- `add_proposal(agent, title, problem, solution, cost_est, time_est)` → proposal dict
- `approve_proposal(id) / reject_proposal(id, reason)`
- `get_proposals(status=None)` — filter: pending/approved/rejected

## Cost
- `track_cost(agent, model, tokens_in, tokens_out, cost)` — auto-called by call_deepseek
- `get_cost_summary()` → {total_spent, daily_budget, month_budget, remaining, agent_costs, call_count}

## Goals (structured)
- `set_goal(title, expectation, deadline)` → auto-sets as current
- `complete_goal(goal_id=None)` — completes current if no ID
- `get_current_goal()` → active goal dict or None
- `get_goals(status=None)` — filter: active/completed

## OKRs
- `create_objective(objective, quarter, owner)` → objective dict
- `add_key_result(obj_id, kr, target, baseline=0, owner, metric)` → KR dict
- `update_kr_progress(obj_id, kr_id, current)` — auto-calculates %
- `get_active_objectives()` → list (status=active)
- `get_all_objectives()` → all

## Skills Registry
- `create_skill(name, category, description)` → skill dict
- `get_all_skills()` → list

## Custom Agents
- `create_custom_agent(name, role, personality, skills_list, reports_to)` → agent dict + syncs to profiles.json
- `get_custom_agents()` → list
- `delete_custom_agent(id)` — removes from registry + profiles.json

## Org Chart
- `create_team(name, lead, members_list)` → team dict
- `add_dependency(from_agent, to_agent, dep_type)` — type: waiting/reviews/tests
- `get_org()` → {teams, dependencies, all_agents}

## Agent Message Bus
- `send_message(from, to, subject, body, msg_type, ref_task_id)` → sends internal message between agents
- `get_messages(to_agent=None, status="unread")` → list
- `mark_message_read(message_id)` → marks as read
- `get_all_messages(limit=20)` → recent messages
- `assign_reviewer(task_dict)` → str (auto-routes: technical→CTO, marketing→CMO etc.)
- `request_review(task_id)` → auto-sends review_request message to correct reviewer
- `notify_quang(message, msg_type)` → writes notification for Quang (types: info/approval/pending/revision)
- `get_quang_notifications(limit=10)` → list

## Agent Status
- `get_agent_statuses()` → list of {name, role, status, current_task, done_today} — derived from profiles.json + task store. Status is now phase-aware: 📋 Planning / 🔍 Review / ✅ Approved / 🔵 Working / 🧪 Testing / 🟢 Done

## Shared Inbox (Cross-Machine via Git)
See `shared/inbox.py` — functions for Hermes↔OpenClaw communication:
- `send(to, subject, body, type, ref)` → auto push to GitHub
- `read(to, status)` → auto pull from GitHub, returns unread messages
- `mark_read(id)` → auto push after marking
- `reply(msg, body)` → auto push

## DeepSeek/OpenCode API
- `call_deepseek(model, system, messages, temperature=0.3, max_tokens=2000, agent_name)` → str | None
  - Model mapping: deepseek-chat → deepseek-v4-flash, deepseek → deepseek-v4-pro
  - Uses OPENCODE_GO_API_KEY env var, endpoint: https://opencode.ai/zen/go/v1/chat/completions
