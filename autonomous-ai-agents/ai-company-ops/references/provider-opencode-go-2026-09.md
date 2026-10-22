# OpenCode Go — x-opencode-session bắt buộc + deepseek-v4-pro disabled (08/09/2026)

## Triệu chứng
- Standup 08/09: 5/5 agents trả `(LLM trả None)`. Standup 06/09 cũng 5/5 None (cùng nguyên nhân, chưa chẩn đoán ra).
- `call_deepseek('deepseek-v4-flash', ...)` và `deepseek-v4-pro` đều None. Retry trong function cũng None → tưởng "flash empty transient".

## Chẩn đoán (path đã verify)
1. Gọi raw bằng requests tới `https://opencode.ai/zen/go/v1/chat/completions` với chỉ `Authorization` header:
```python
resp = requests.post(OPENCODE_URL, json=payload, headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}, timeout=60)
```
→ **HTTP 400**
```json
{"type":"error","error":{"type":"MissingSessionID","message":"Request is missing x-opencode-session and cannot be routed efficiently. Please see https://opencode.ai/docs/go/#where-can-i-use-it"}}
```
2. Docs opencode.ai/docs/go (mục "Where can I use it?"): client phải gửi traffic kiểu coding-agent, **User-Agent của chính mình** (không phải tên SDK/thư viện generic), và **session ID ổn định trong `x-opencode-session`** cho mỗi conversation (để routing + prompt caching).
3. Hermes tự gửi header này (merged PR #101864, sau v0.21.0) → gateway Hermes chạy OK trong khi hub code AI Company chết. Đừng đổ lỗi key/network khi thấy 2 nơi khác nhau.

## Fix (commit b348840, pushed main)
Trong `hub/store.py::call_deepseek` — áp cho call chính VÀ cả 2 block retry (`resp2`, `resp3`) vì retry thiếu header cũng 400 và bị đọc nhầm thành "empty response":
```python
import hashlib
_session_id = "ac-" + hashlib.sha256(agent_name.encode("utf-8")).hexdigest()[:16]
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "User-Agent": "ai-company-agent/1.0",
    "x-opencode-session": _session_id,
}
```
- Session ID stable theo `agent_name` (không random mỗi call) — đúng yêu cầu routing/prompt cache.
- Verify: raw request thêm 2 headers → 200 + content "OK"; `call_deepseek` flash → `'OK'`; chạy lại standup → QA/CMO/Dev1/Content/CTO đều ra báo cáo.

## deepseek-v4-pro DISABLED trên Go plan (cùng ngày)
```json
HTTP 401 {"type":"error","error":{"type":"ModelError","message":"Model is disabled"}}
```
- Mọi fallback `force_pro=True` / `fallback_models=["deepseek-v4-pro", ...]` fail im lặng → agent trả None dù flash OK.
- Phân biệt 2 lỗi khi agent None: đọc body raw — `MissingSessionID` = thiếu header; `ModelError Model is disabled` = model không khả dụng trên plan.
- Hướng xử lý (chờ Quang quyết): bật pro trên OpenCode, hoặc đổi `MODEL_MAP` sang model khác trong danh sách Go (GLM-5.3, Kimi K3...). Trạng thái model thay đổi theo thời gian — KHÔNG hardcode "pro không dùng được" vĩnh viễn.
- Check nhanh trạng thái provider trong credential pool: `~/AppData/Local/hermes/auth.json` → `credential_pool.<provider>[0].last_status/last_error_message` (thấy `exhausted` + `ModelError`).

## Tham chiếu
- Docs: https://opencode.ai/docs/go/#where-can-i-use-it
- Fix trong repo: `hub/store.py` (hàm `call_deepseek`), commit `b348840` (08/09/2026).