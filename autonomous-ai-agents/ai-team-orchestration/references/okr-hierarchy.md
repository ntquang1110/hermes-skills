# OKR Hierarchy — Implementation Reference

## Data Flow

```
User sets OKR
  → create_objective(title, quarter, owner)
  → add_key_result(objective_id, kr, target, baseline, owner, metric)
  → auto_gen_tasks_for_kr(objective_id, kr_id)
      → sinh 2-3 tasks, phase="planning", assign agent phù hợp
      → tasks linked via kr["task_ids"] = [task_id, ...]
  → get_objective_tree(id) → full hierarchy: obj → KRs → tasks
```

## Auto-Gen Routing Logic

| KR contains | Tasks assigned to |
|-------------|------------------|
| seo, content, blog | Content (3 tasks: research, plan, publish) |
| conversion, landing, cvr | Design + Dev1 + CMO (3 tasks: design variant, implement, analyze) |
| traffic, visitor, user | CMO (2 tasks: audit, campaign) |
| anything else | KR owner (3 tasks: research, execute, measure) |

## Dashboard Rendering

The dashboard `index.html` renders OKR Board from `data.okrs.trees`:

```
🎯 Objective [progress%]
  ████████░░░░ progress bar
  📌 KR [current/target metric]
    ████████░░░░ KR progress bar
    ● #3 Task title → assignee [phase colored dot]
    ● #4 Task title → assignee
```

## CLI

```
python company.py okr
  → Shows all objectives with KRs, progress bars, linked tasks
  → Also shows total cost
```

## Progress Calculation

- KR progress = (current - baseline) / (target - baseline) * 100
- Objective progress = average of all KR progress_pct values
- Auto-updated when `update_kr_progress()` is called
