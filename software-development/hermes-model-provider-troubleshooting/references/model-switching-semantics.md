# Model switching & session-follow semantics

Verified against local source: `~/AppData/Local/hermes/hermes-agent` (git checkout, Oct 2026). Khi docs và source lệch nhau, source thắng; docs: https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models

## Sự thật cốt lõi

**Không có config nào bắt session đang mở tự follow `model.default`.** Đây là design: mỗi session pin model của riêng nó để tránh switch giữa chừng (mất prompt cache, đổi chi phí). "Chat không đổi model theo config" almost always = session đang bị pin override.

## Thứ tự resolve model (gateway, mỗi message)

`_resolve_session_agent_runtime` — gateway/run.py ~:6814:

1. **Session `/model` override** — in-memory `_session_model_overrides`, write-through vào session store (`set_model_override`, api_key KHÔNG bao giờ persist). `_rehydrate_session_model_override` đọc lại sau gateway restart → override sống sót restart.
2. **`channel_overrides`** trong config.yaml (per chat/thread).
3. **Global `model.default`** — đọc FRESH mỗi message qua `_load_gateway_config()` (mtime-keyed cache, tự invalidate khi file đổi).

Hệ quả: chat Telegram/Discord **chưa từng** `/model` thì đã tự follow config per-message rồi. Nếu không follow → override cũ đang pin → `/new` để clear (clear cả RAM lẫn DB theo docstring của `_rehydrate_session_model_override`).

## Desktop / TUI gateway

- `session.create` (tui_gateway/methods_session.py ~:64): composer model được ship lên như `model_override` per-session → **pin ngay từ lúc tạo**. Settings → Model chỉ áp cho session mới (frontend `applySavedMainModel` cố ý không paint default lên live session).
- `_sync_agent_model_with_config` (tui_gateway/server.py ~:4525) chạy mỗi turn start: ADOPT config.yaml change **chỉ khi session không có override**. Session pin → giữ model cũ. Failed switch = no-op, không block turn.
- Desktop model pill (`apps/desktop/src/app/session/hooks/use-model-controls.ts` → `selectModel`) gọi `config.set` với `--session` tường minh → session-scoped, không bao giờ ghi profile default.
- `config.set model` khi session đang busy → stash `pending_model_switch`, apply ở turn start kế tiếp (`_apply_pending_model_switch`) — không kill turn.

## Flag persist (hermes_cli/model_switch.py, `_should_persist_model_switch`)

| Lệnh | Session hiện tại | config.yaml (session mới) |
|---|---|---|
| `/model X --once` | turn sau tự restore | không |
| `/model X --session` | có | không |
| `/model X --global` | có | CÓ |
| `/model X` (trần) | có | theo `model.persist_switch_by_default` (mặc định false) |
| `/model X --provider Y` (không cờ persist) | có | KHÔNG (provider switch = exploratory) |

Desktop model pill luôn gửi `--session` → không bị ảnh hưởng bởi `persist_switch_by_default`.

## Mid-session confirm

`model.switch_context_confirm_tokens` (mặc định 100000, docs) — hỏi confirm khi session đã lớn trước khi switch (turn sau re-read toàn bộ context không cache). Re-select model hiện tại không prompt. Key này có thể vắng mặt ở checkout cũ (docs dẫn trước source).

## Workflow trả lời user "đổi model rồi chat không follow"

1. Xác định surface: gateway chat hay desktop live session.
2. Gateway: kiểm tra có override pin không → `/new` hoặc `/model <tên mới>`.
3. Desktop: session pin từ lúc create hoặc do pill → `/model <tên>` trong chat, hoặc model pill ở footer.
4. Muốn vừa switch session vừa làm default mới: `/model <tên> --global`.
5. Đổi default không đụng session cũ: `hermes config set model.default <tên>` — chỉ session mới nhận.
