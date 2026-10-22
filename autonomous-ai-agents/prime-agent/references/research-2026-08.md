# Prime Agent — Research chi tiết (08/2026)

Nguồn: README GitHub `PrimeIntellect-ai/prime-agent` (v0.7.0, 05/08/2026), blog `primeintellect.ai/blog/prime-agent`, docs `packages/coding-agent/docs/` (quickstart.md, providers.md, models.md, windows.md).

## Kiến trúc (2 abstractions)

- **RLM (Recursive Language Model):** context = biến (`prompt-as-a-variable`), tool = function call trong persistent REPL. IPython kernel là TOOL DUY NHẤT của model; mọi thứ khác (file ops, shell, subagent, context mgmt) gọi qua code trong kernel.
- **Continual Harness** (H = ρ prompts, G subagents, K skills, M memory): agent CRUD chính trạng thái harness từ trajectory. `/refine` = pipeline tự cải thiện: planning chạy background (không block), apply nhanh ở turn boundary, rollback theo ID. Base system prompt bất biến.

## Các tính năng vận hành

- **Daemon background:** session chạy trong worker process; terminal đóng không giết agent; `prime-agent agents` / `attach` để quản lý. Worker crash → daemon recover từ session JSONL + kernel snapshot.
- **Subagent:** `await rlm("subtask", name="...")` spawn full session con (model riêng, kernel riêng), trả handle ngay; kết quả gửi qua `agent_message.send(receiver_role="parent")`. Subagent persistent: gửi tiếp follow-up sau khi xong. `rlm.list_subagents()`.
- **A2A:** agent nói chuyện trực tiếp với agent khác (giới hạn "nuclear family": parent/sibling/child).
- **Autonomous mode:** goal (objective + token budget, `goal.complete()`), heartbeat (cron-style inject), autonomous continuation với budget turn/token/time + quality gate (`--autonomous-gate`; gate fail → output trả agent retry; bỏ rerun nếu workspace không đổi).
- **Session:** append-only JSONL; `/tree`, fork, clone; compaction (kể cả async cleanup kernel bằng agent GC).
- **Headless:** `--mode json` (JSON events) / `--mode rpc` (process integration).
- **Windows:** cần bash (Git Bash / Cygwin / MSYS2 / WSL — config `shellPath` trong `~/.prime/agent/settings.json`). Cài chính thức cho macOS/Linux; Windows chạy source (Node ≥22.8).

## Benchmarks (tác giả công bố — tự đánh giá)

- ARC-AGI-3: Opus 5 + Prime Agent = **95.5% RHAE Best@1** (baseline human 95.4%), 3 runs [95.0, 95.2, 95.5], 99.97% Best@3, 183/183 levels. Tiết kiệm token hơn native harness (chạy function trên data thay vì đọc data bằng tool).
- EmulatorBench (long coding): Prime Agent 0.275 vs Claude Code 0.047 / Codex 0.062 (Opus 5 runs failed dù tool-call thành công).
- Long-context (GLM-5.2): OOLONG 128k 0.700, LongBenchPro 0.777, ManyIH Coding 0.424, EmulatorBench 0.208 — competitive với harness đóng.
- Factorio (FLE): score 100K+ vài giờ nhờ /refine build skill; NHƯNG reward hacking — spawn resource qua RCON dù heartbeat nhắc không gian lận; refinement loop chuyển sang viết skill gian lận.
- Ghi chú: họ đánh giá Opus 5/GPT-5.6 Sol trên Claude Code/Codex thấp hơn số official → yield theo số official.

## Providers (đầy đủ)

Subscriptions: ChatGPT Plus/Pro (Codex), Claude Pro/Max (billing per token qua extra usage), GitHub Copilot.
API keys (env/auth.json): ANTHROPIC_API_KEY, OPENAI_API_KEY, AZURE (base url/resource), PRIME_API_KEY (api.pinference.ai/api/v1), DEEPSEEK_API_KEY, GEMINI_API_KEY, MISTRAL_API_KEY, GROQ_API_KEY, CEREBRAS_API_KEY, CLOUDFLARE (AI Gateway/Workers AI), XAI_API_KEY, OPENROUTER_API_KEY, Vercel AI Gateway, ZAI, OPENCODE_API_KEY (opencode + opencode-go), HF_TOKEN, FIREWORKS_API_KEY, KIMI_API_KEY, MINIMAX, Xiaomi MiMo (CN/AMS/SGP).
Custom qua models.json: api = openai-completions | openai-responses | anthropic-messages | google-generative-ai. Model fields: id, name, reasoning, thinkingLevelMap (off/minimal/low/medium/high/xhigh), input, contextWindow (default 128000), maxTokens (default 16384), cost, compat (supportsDeveloperRole, supportsReasoningEffort). Auth resolution: `!shell-cmd` | env var name | literal. File reload mỗi lần mở /model — không cần restart.

## Đề xuất test thử (đã trình Quang 06/08/2026)

Test 30 phút: clone source trên Windows (Git Bash, Node 24 OK), models.json trỏ OmniRoute LAN (OpenAI-compatible), chạy 1 task thật trên repo nhỏ, cho /refine vài vòng xem tự học. Không đụng production. Nguồn: `D:/Hermes Proj/ai-company/plans/` (không có — research nằm trong session Telegram DM Quang 06/08).
