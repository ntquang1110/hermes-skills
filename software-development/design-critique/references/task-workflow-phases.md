# Task Workflow Phases — Plan → Review → Implement → Test → Complete

**Rule: Every task MUST go through all phases. No skipping. No code before plan approval.**

---

## Phase Diagram

```
📋 Planning
   │
   ▼
🔍 Review ──fail──▶ 📋 Planning (revise plan)
   │
   ▼ pass
✅ Approved
   │
   ▼
🔵 In Progress
   │
   ▼
🧪 Testing ──fail──▶ 🔵 In Progress (fix)
   │
   ▼ pass
✅ Completed
```

## Phase Definitions

### 📋 Planning
- Output: **Spec/design doc** (`plan_doc`)
- Content: goal, approach, trade-offs, cost estimate, dependencies
- Rule: NO code written in this phase
- Transition trigger → `transition_task(id, "review", plan_doc=result)`

### 🔍 Review
- Adversarial critique of the plan
- Role: CTO reviews technical plans, CMO reviews marketing plans
- Pass condition: reviewer explicitly says "pass"
- Fail → move back to Planning with `review_notes`
- Transition trigger → `transition_task(id, "approved", review_notes=result)` on pass, `transition_task(id, "planning", review_notes=result)` on fail

### ✅ Approved
- Plan is approved, waiting for implementation
- Chuyển tiếp tự động sang In Progress khi agent nhận task
- Transition trigger → `transition_task(id, "in_progress")`

### 🔵 In Progress
- Actual implementation (code, content, design)
- Agent produces output
- Transition trigger → `transition_task(id, "testing", output=result)`

### 🧪 Testing
- QA verification
- Pass condition: output contains "pass" (case-insensitive)
- Fail → move back to In Progress for fixes, include `test_results`
- Transition trigger → `transition_task(id, "completed", test_results=result)` on pass, `transition_task(id, "in_progress", test_results=result)` on fail

### ✅ Completed
- Task is closed. No further transitions.

---

## Agent Workflow Enforcement

When an agent picks up a task, its `cmd_agent()` function checks `task["phase"]` and branches accordingly:

```python
phase = task.get("phase", "planning")

if phase == "planning":
    # Write plan
    result = agent.think("Phase PLANNING: Viết spec...")
    transition_task(task["id"], "review", plan_doc=result)

elif phase == "review":
    # Critique plan
    result = agent.think("Phase REVIEW: Phản biện...")
    if "pass" in result.lower():
        transition_task(task["id"], "approved", review_notes=result)
    else:
        transition_task(task["id"], "planning", review_notes=result)

elif phase == "approved":
    transition_task(task["id"], "in_progress")
    result = agent.think("Phase IMPLEMENT: Code theo plan...")
    transition_task(task["id"], "testing", output=result)

elif phase == "testing":
    result = agent.think("Phase TESTING: Verify output...")
    if "pass" in result.lower():
        transition_task(task["id"], "completed", test_results=result)
    else:
        transition_task(task["id"], "in_progress", test_results=result)
```

## Task Store Schema

```json
{
  "id": 1,
  "title": "A/B Test Headline",
  "assignee": "Dev1",
  "phase": "planning",        // current lifecycle phase
  "plan_doc": null,           // output of planning phase
  "review_notes": null,       // output of review phase
  "output": null,             // output of implementation
  "test_results": null,       // output of testing phase
  "status": "pending"         // mirrors phase except "completed"
}
```

## Agent Status Display

Status is derived from the task's current phase:

| Phase | Dashboard Display |
|-------|------------------|
| planning | 📋 Planning |
| review | 🔍 Review |
| approved | ✅ Approved |
| in_progress | 🔵 Working |
| testing | 🧪 Testing |
| completed | 🟢 Done |
| no task | ⚪ Idle |
