# Standup — hết credit kéo dài 09→21/09 (11 ngày) — chẩn đoán & xử lý

Nguồn: standup cron 21/09/2026, ops_guard --json, verify trực tiếp.

## Hiện tượng
- `python hub/run.py standup` → 5/5 agent `None` (CTO, Dev1, QA, CMO, Content).
- `activity.json` ghi liên tiếp: `[ERROR] OpenCode API error (X): {'type':'server_error','message':'Upstream request failed: Insufficient account funds'}`.
- `ops_guard --json` vẫn chạy determinist: STALE 5 (#8 QA 11.1d + #43-46 planning 16.9d), NO_DC 4 (#43-46), WAKE 0.

## Chẩn đoán phân biệt (đã verify 21/09)
1. **Models 200 ≠ credit OK.** `GET /zen/go/v1/models` với Bearer vẫn 200 (list 30, first deepseek-v4-flash) ngay cả khi hết tiền.
2. **Chat mới lộ credit.** `POST /zen/go/v1/chat/completions` với đủ header (`Authorization`, `User-Agent`, `x-opencode-session`) → `server_error Insufficient account funds`.
3. **Thiếu header ra lỗi khác, không phải credit.** Thiếu `x-opencode-session` → `400 MissingSessionID` (dễ nhầm là credit). Luôn gọi qua `store.call_deepseek` (đã set `x-opencode-session = ac-<sha256>`) để chẩn đoán đúng.
4. **Direct probe đúng cách:** `call_deepseek('deepseek-v4-flash', 'Bạn là CTO', [{'role':'user','content':'Say hi in 3 words'}], agent_name='CTO')` → None khi hết credit; truyền `messages` là string → `TypeError: can only concatenate list (not "str") to list` tại `store.py:360` (phải là list[dict]).

## Xử lý khi kéo dài
- **Đừng wake agent.** Worker gọi LLM sẽ fail y hệt → chỉ tốn log. Báo thẳng: chờ nạp.
- **Billing link cố định:** `https://opencode.ai/workspace/wrk_01KS52FWVYXBS15WZAJRJFVB34/billing`.
- **Guard là cơ cứng.** Dù LLM chết, guard vẫn báo STALE/NO_DC chính xác → báo cáo standup lấy số guard, không suy đoán.
- **Briefing + state vẫn flush.** `briefing.md` (`Standup (last)` + `Last Updated`) và `D:/Hermes Proj/.hermes-state/ai-company.md` cập nhật ngày outage (11) dù không có agent report.
- **Context-scan synthesis null** khi credit hết: `tfo_data/context_scan.json` có `synthesis: null` — cron context_scan cũng fail, không phải chỉ standup.

## Pitfall call_deepseek signature
`call_deepseek(model, system, messages, ...)` — `messages` BẮT BUỘC là `list[{"role":..., "content":...}]`. Truyền string → TypeError, không phải lỗi provider. Test nhanh sai sẽ nhầm là credit.
