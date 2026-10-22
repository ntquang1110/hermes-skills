# CEO Routing Table & Agent Dispatch

## Keyword-based routing

```python
ROUTING = {
    "research": "research",
    "phân tích": "research",
    "điều tra": "research",
    "so sánh": "research",
    "outreach": "sales",
    "prospect": "sales",
    "khách": "sales",
    "pipeline": "sales",
    "code": "dev",
    "bug": "dev",
    "deploy": "dev",
    "feature": "dev",
    "sửa": "dev",
    "marketing": "cmo",
    "chiến dịch": "cmo",
}
```

Default (no keyword match) → `ceo` (self-handle via Hermes).

## Dispatch flow (correct — uses real Hermes subagents)

```
User → CEO dispatch("title", "context")
  → route_task(title + context) → pick agent
  → dispatch_task(task_id, task_data, to_agent, from="ceo")
    → message_bus.send() → agent inbox gets message

Watchdog cron (1m, no_agent=True)
  → Detects new task in agent inbox
  → Sets status "pending" (NOT "busy" — not processing yet)
  → Logs to activity: [agent] pending

CEO (Hermes — this conversation)
  → Run `python company.py check` to see pending tasks
  → For each pending task:
      delegate_task(goal=f"Process task {task_id} for {agent}",
                    context=f"Title: {title}, Context: {context}")
  → Subagent (REAL Hermes session with tool access):
      1. Reads inbox message for full context
      2. Uses web_search, terminal, read_file to do real work
      3. Writes result to tasks/{task_id}/result.json
      4. Reports back: report_done(agent, "ceo", task_id, result)
      5. Sets status idle: set_status(agent, "idle")
      6. Generates HTML report: _generate_report(task_id)
```

## Dispatch from CLI

```bash
cd ~/ai-company-v2
python -c "from agents.ceo import ceo_dispatch; print(ceo_dispatch('T-001', 'Research X', 'context'))"
```

## Check pending tasks

```bash
cd ~/ai-company-v2 && python company.py check
```

## Task data shape

```json
{
  "title": "Research EZ80 competitors",
  "description": "So sánh giá, chất lượng",
  "deadline": "2026-09-30",
  "context": "Farm 500 con, cai sữa 21 ngày",
  "created_at": "2026-09-22 00:17:10"
}
```

## Result data shape (from real subagent)

```json
{
  "handled_by": "research",
  "title": "Research EZ80 so với đối thủ",
  "status": "done",
  "summary": "Research Analysis: EZ80 vs DirectVet...",
  "ez80_profile": {
    "price": "12.500.000đ/100kg",
    "ingredients": {"Saponin": 1500, "Polyphenol": 4500, ...},
    "raw_materials": ["vỏ hàu", "cao lanh", ...]
  },
  "competitors": [
    {"name": "Zeolite", "price": "500K-1.5tr/tấn", "advantage": "rẻ, hấp phụ độc tố"},
    {"name": "Bentonite", "price": "400K-1.2tr/tấn", "advantage": "rẻ, kết dính TĂ"}
  ],
  "recommendation": "EZ80 5kg/tấn + zeolite 5-10kg/tấn",
  "finished_at": "2026-09-22 01:00:14"
}
```

## Key rule

**Do NOT process tasks with scripts.** Watchdog detects + sets pending. Only `delegate_task` to real Hermes subagents does actual processing. Scripts have no tool access and produce fake content.
