# DeepSeek Harness (dsh) — adoption evaluation, 2026-08-15

Repo: deepseek-ai/deepseek-harness — MIT, TypeScript, ~105k stars (08/2026),
default branch **master** (main 404s). "Everything is a plugin" agent harness on
Cordis. Developer preview, version 0.1.0-rc.6, README warns breaking changes.

## Verdict (đã chốt với Quang)

- KHÔNG thay Hermes. KHÔNG build sản phẩm khách (Volden/dithi/meTelligent) trên nó.
- Boot test thất bại: `npx -y @deepseek-ai/dsh web` treo >6 phút, npm cache 0 bytes,
  không listen port → kill, báo trung thực. Dev preview đúng nghĩa.
- Giá trị: 3 pattern kiến trúc đáng học (dưới), không phải code.

## 3 pattern đáng học (cho agent-system design của mình)

1. **Layered patch config** — profile → bundle → cordis.patch.yml → --patch. Layer sau
   đè layer trước; mọi config row thay được bằng patch mà không đụng core.
   → Áp dụng: cấu hình Volden/TFO/AI Company thay vì sed file config.
2. **Session log là nguồn sự thật duy nhất** — invariant "model-visible means logged":
   mọi thứ model thấy phải tái dựng được từ log. Fork/resume/telemetry/replay đều derive
   từ một luồng SessionEvent duy nhất.
   → Áp dụng: nâng state-file protocol.
3. **Capability seams + E2B remote sandbox** — fs/subprocess/sandbox là interface đổi
   provider được; mount E2B adapters → Bash/PTY/LSP chạy remote Linux theo, không đổi
   consumer.
   → Áp dụng: khi cần chạy code agent trên Linux sandbox thay Windows (ổ C kẹt).

## Cấu trúc packages (đáng chú ý)

- core/: session, system-prompt, tools, agent, agent-loop, scope
- llm/, skill/, sandbox/, subagent/ (in-process, ACP, codex, claude-code, dsh-sdk),
  code-runtime/, e2b/, mcp-client/, schedule/, compaction/, jobs/, plan/, spill/,
  session-query/, guard/, hooks/, lsp/, terminal/, workflow/
- apps/: cli, web. bundle/: base, web-app, headless

## Khác biệt so với stack hiện tại

- Subagent providers (codex, claude-code, ACP, dsh-sdk): tương đương thứ Hermes đã có qua
  skills → không mới.
- MCP client, skills catalog, compaction, schedule: Hermes đã có → không lý do đổi.
- DeepSeek-native (model adapter riêng cho model của họ): đáng theo dõi khi DeepSeek tune
  harness cho model họ, nhưng chưa đủ để cân nhắc.
