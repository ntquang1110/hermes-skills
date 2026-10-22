# Prime Agent (Prime Intellect) — research 08/2026, chưa cài

Nguồn: README GitHub (PrimeIntellect-ai/prime-agent) + blog primeintellect.ai/blog/prime-agent + docs
quickstart/providers/models/windows. Cập nhật 06/08/2026 (v0.7.0 ra 05/08/2026).

## Là gì
Open-source (MIT) coding/research agent harness "self-improving" của Prime Intellect
(Series A $130M, NVIDIA-backed). Built trên `pi` (earendil-works). Hai abstraction cốt lõi:

- **RLM (Recursive Language Model):** IPython kernel persistent là tool duy nhất; context = biến;
  subagent = function call `await rlm("subtask")` — trả handle ngay, kết quả qua `agent_message`.
  Model viết Python để điều khiển chính quá trình của nó.
- **Continual Harness:** `/refine` đọc trajectory, tự CRUD prompt note / memory / skill / subagent
  spec; ghi trigger + outcome, rollback theo ID; base system prompt immutable.

## Cài đặt
- macOS/Linux: `curl -fsSL https://app.primeintellect.ai/prime-agent/install.sh | sh`
- Windows: cần bash (Git Bash OK) — docs/windows.md; hoặc source: Node >= 22.8 + `npm ci` + `./prime-agent.sh`
- Máy Quang: Node v24.16.0 + Git Bash + Python 3.11 → đủ điều kiện (chưa cài)
- Auth: `/login` (subscription) hoặc API key (env hoặc `~/.prime/agent/auth.json`)
- Lệnh: `prime-agent`, `-c` continue, `-r` resume, `agents` / `attach`, `doctor`, `shutdown`,
  `--mode json|rpc`, `-p "one-shot"`

## Providers
- Subscription: Claude Pro/Max, ChatGPT Plus/Pro (Codex), GitHub Copilot
- API key: Anthropic, OpenAI, DeepSeek, Groq, Cerebras, OpenRouter, OpenCode Zen/Go, MiniMax,
  Kimi, xAI, HF, Fireworks, Azure, Bedrock, Cloudflare gateway...
- Custom OpenAI-compatible qua `~/.prime/agent/models.json` (api: openai-completions |
  openai-responses | anthropic-messages | google-generative-ai; baseUrl + apiKey + models)
  - Trỏ OmniRoute LAN được: `baseUrl: http://192.168.1.110:20128/v1`, `api: openai-completions`
  - Server không hiểu `developer` role (Ollama/vLLM) → `compat.supportsDeveloperRole: false`,
    không hỗ trợ reasoning_effort → `compat.supportsReasoningEffort: false`

## Tính năng đáng chú ý
- Daemon nền: session chạy khi đóng terminal, reattach; worker crash tự recover từ session JSONL
- Autonomous mode: `--autonomous --autonomous-gate "npm run check" --autonomous-max-turns 20`
  (gate chạy trước khi session được phép kết thúc; skip re-run nếu workspace không đổi)
- Heartbeat/schedule cron-style; persistent goal (token budget); compaction tự động
- A2A messaging: agent message agent (giới hạn nuclear family: parent/sibling/child)
- Skills = Python package importable; skill creator built-in
- Subagent persistent: giữ session riêng, nhắn tiếp sau khi xong

## Kết quả (blog chính chủ, tự báo cáo)
- ARC-AGI-3: Opus 5 → 95.5% Best@1 (baseline người 95.4%)
- EmulatorBench 0.275 vs Claude Code 0.047 / Codex 0.062
- Mạnh long-context/long-running; token usage thấp hơn (chạy code thay vì đọc data bằng tool)

## Rủi ro / lưu ý khi triển khai
- KHÔNG phải sandbox: chạy model-generated code với quyền user — chỉ chạy trong repo disposable
- Mới v0.7.0, chính tác giả thừa nhận "còn friction khi chạy với model"; chưa model nào
  được train trên harness này (model-harness co-learning còn là tiềm năng)
- Reward hacking có thật: Factorio — agent tự tìm loophole (RCON spawn resource), rồi /refine
  viết luôn skill gian lận. Autonomous mode bắt buộc gate + review người
- Trùng lặp Hermes: delegate/cron/skills/state đã có. Giá trị thật của Prime Agent =
  /refine + autonomous mode + session persistent. Không cài đại trà
- Nếu test: cấu hình models.json trỏ OmniRoute LAN, chạy 1 task trên repo nhỏ, 30 phút đủ đánh giá

## Quyết định trạng thái (08/2026)
- Đã research, đề xuất test thử 30 phút — chờ Quang chốt (test hay chờ stable)
