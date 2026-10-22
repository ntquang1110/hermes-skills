---
name: prime-agent
description: "Prime Agent CLI: install, providers, custom models, usage."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [prime-agent, prime-intellect, coding-agent, rlm, harness, self-improving]
    related_skills: [claude-code, codex, opencode, hermes-agent]
---

# Prime Agent (Prime Intellect) — coding/research harness

Prime Agent là coding + research agent mã nguồn mở (MIT) của Prime Intellect, v0.7.0 ra 05/08/2026. Điểm khác biệt: **self-improving** — agent tự CRUD memory/skill/prompt của chính nó từ trajectory (`/refine`), chạy trong persistent IPython kernel, subagent = function call (`await rlm(...)`), session chạy nền qua daemon.

## Khi dùng

- Cần agent chạy autonomous dài hạn (đêm) có budget + quality gate: `--autonomous --autonomous-gate "npm run check" --autonomous-max-turns 20`
- Cần harness tự học cách làm việc của dự án (refine → skill/memory) qua nhiều session
- User yêu cầu đánh giá/thử Prime Agent — dùng làm agent thứ 4 cạnh Claude Code / Codex / OpenCode

## Cài đặt

- Official (macOS/Linux): `curl -fsSL https://app.primeintellect.ai/prime-agent/install.sh | sh`
- **Windows (máy Quang):** Git Bash (đã có) + Node ≥22.8 (máy có v24). Chạy source: `git clone https://github.com/PrimeIntellect-ai/prime-agent && cd prime-agent && npm ci && ./prime-agent.sh`
- Kernel: tự bootstrap IPython lần đầu; dùng env `PRIME_AGENT_KERNEL_PYTHON` trỏ Python có sẵn `ipykernel`
- Repo: `PrimeIntellect-ai/prime-agent`; docs trong `packages/coding-agent/docs/` (quickstart, providers, models, windows, json/rpc mode)

## Providers (nhiều option — xài được hạ tầng sẵn có)

- **Subscription** qua `/login`: Claude Pro/Max, ChatGPT Plus/Pro (Codex), GitHub Copilot
- **API key** (env hoặc `~/.prime/agent/auth.json`): Anthropic, OpenAI, Azure, Prime Inference, DeepSeek, Gemini, Mistral, Groq, Cerebras, OpenRouter, xAI, OpenCode Go (`OPENCODE_API_KEY`), Hugging Face, Fireworks, Kimi, MiniMax, Xiaomi...
- **Custom provider** qua `~/.prime/agent/models.json`: bất kỳ OpenAI-compatible (api `openai-completions`/`openai-responses`/`anthropic-messages`/`google-generative-ai`), chỉ cần `baseUrl` + `apiKey` + `models[]`. → **Trỏ được OmniRoute LAN `http://192.168.1.110:20128/v1` (331 models) hoặc OpenCode Go, không tốn thêm tiền.**
  ```json
  { "providers": { "omniroute": { "baseUrl": "http://192.168.1.110:20128/v1", "api": "openai-completions", "apiKey": "any", "models": [ { "id": "<model-id>" } ] } } }
  ```
- Server không hiểu `developer` role → set `compat.supportsDeveloperRole: false` (Ollama/vLLM/SGLang hay gặp)

## Lệnh chính

```bash
prime-agent                  # chạy trong project dir, load AGENTS.md/CLAUDE.md
prime-agent agents           # browse session đang chạy/idle
prime-agent attach <agent>   # reattach session nền
prime-agent -p "..."         # one-shot
prime-agent --mode json|rpc  # headless automation / tích hợp pipeline
prime-agent --autonomous --autonomous-gate "npm run check" --autonomous-max-turns 20 "task"
```
Trong session: `/refine` (tự cải thiện harness), `/goal` (objective bền), `/heartbeat` + `prime-agent schedule` (cron-style), `/model` / `/effort`, `await rlm("subtask")` (subagent, trả handle ngay, kết quả qua `agent_message`), `rlm.harness.create_memory/create_skill(...)`, `compact.run()`.

## Pitfalls / Trade-offs (đã research 08/2026)

1. **KHÔNG phải sandbox.** Chạy code model sinh ra với quyền user. Chỉ chạy trong repo clone/disposable, review diff, đừng thả vào production.
2. **Reward hacking có thật.** Case study Factorio: agent tự tìm loophole (spawn resource qua RCON) và `/refine` còn tự viết skill gian lận. Autonomous mode bắt buộc gate + review người.
3. **Rất mới.** v0.7.0 ra 1 ngày, chính tác giả nói còn "friction khi chạy với model". Chưa model nào được train cho harness này. Kỳ vọng lỗi, đừng cài đại trà.
4. **Token tốn** nếu dùng frontier model (Opus 5) cho autonomous dài. Dùng model rẻ trên OmniRoute/OpenCode Go thì không đạt benchmark như quảng cáo.
5. **Trùng lặp với Hermes** (delegate, cron, skills, state đều có). Giá trị thật của Prime Agent = `/refine` + autonomous mode + session persistent — đánh giá 3 thứ đó, không phải toàn bộ.

## Reference

- `references/research-2026-08.md` — chi tiết: benchmark (ARC-AGI-3 95.5% Opus 5, EmulatorBench), bảng providers, kiến trúc RLM + Continual Harness, docs paths
