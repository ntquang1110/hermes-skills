# Vision Status Check Protocol

Khi user hỏi "check tiến độ với vision", "tình hình hiện tại", "progress review" — cross-reference 6 nguồn theo thứ tự:

## 6 nguồn check

1. **features.json** (`store/features.json`) — feature-level progress (status: done/in_progress/live, progress %). Đây là nguồn chính xác nhất về tiến độ thực tế.
2. **tasks.json** (`store/tasks.json`) — task-level phase (completed/in_progress/paused/planning) + stale tracking (ngày không update). Dùng `collections.Counter` để aggregate by phase.
3. **git log** (`git log --oneline -15`) — commits gần đây. Bằng chứng thực tế về code đã được triển khai. KHÔNG dựa vào status tự báo.
4. **State file** (`.hermes-state/ai-company.md`) — team status, blockers, agent health, active tasks. Đọc để biết "hôm nay team đang thế nào".
5. **Plan docs** (`shared/plan-*.md`) — so sánh plan gốc vs thực tế. Thường drift so với features.json. Nếu plan ghi "in_progress" nhưng features.json ghi "done 100%" → báo cáo theo features.json, ghi chú drift.
6. **Running services** — `curl -s --max-time 5 http://localhost:8100/api/health` để xác nhận server sống.

## Pitfalls

### Plan doc drift
Plan documents (`shared/plan-*.md`) thường KHÔNG được update sau khi implement xong. Features.json mới là nguồn chính xác. Khi báo cáo, nói rõ "plan ghi X nhưng thực tế đã Y" — đừng chỉ đọc plan.

### Features không có sub-task
Feature ở 80% mà không có task nào trong tasks.json → không biết 20% còn lại là gì. Feature nào in_progress phải có task tương ứng với done_criteria. Nếu phát hiện gap này, báo cáo rõ và đề xuất phân rã.

Ví dụ: Voice Phase A (voice-a) ở 80% nhưng không có sub-task nào → cần check code để xác định 20% cuối.

### Credit/blocker check first
Trước khi báo cáo tiến độ, check xem AI Company agents có bị block không:
- OpenCode Go credit (401 CreditsError)
- Stale wake (wake agent không có LLM)
- Claw offline (kênh inbox chết)
- NO_DC tasks (task planning không có done_criteria)

Nếu agents chết (5/5 agent None) thì mọi feature progress đều là code cũ, không có tiến triển mới. Báo blocker ngay đầu, feature progress sau.

### Mốc thời gian
- **STALE ≤ 3 ngày** — bình thường, chỉ note
- **STALE 3-7 ngày** — warning, cần nhắc
- **STALE > 7 ngày** — critical, cần quyết định (đóng/giao lại/bỏ)
- Task planning NO_DC > 7 ngày → đề xuất đóng hoặc gán done_criteria

## Output format

Khi báo cáo, dùng format:

```
## [Tên feature] [trạng thái] [progress%]

**Đã làm:** bullet list từ git log / features
**Còn thiếu:** bullet list gap so với plan
**Blocker:** nếu có
```

Feature-level trước, task-level sau, blocker đầu tiên.
