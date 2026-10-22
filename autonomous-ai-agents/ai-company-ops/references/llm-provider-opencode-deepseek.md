## DeepSeek via OpenCode (LLM calls — agent.think)

- Endpoint `https://opencode.ai/zen/go/v1/chat/completions`, key `OPENCODE_GO_API_KEY` (có sẵn, đừng tạo mới). Rotate key → cập nhật 3 chỗ: session export, `~/.bashrc`, Hermes `.env` → test `call_deepseek` 1 câu → restart server 8100 (đọc env lúc start).
- Models: chat/coder→flash, reasoner→pro (bare IDs; prefix `bytedance/` chết 15/09). Cost `store/cost.json` qua `MODEL_PRICING` (flash $0.15/$0.60, pro $0.50/$2.00 per 1M). Chi tiết: `references/opencode-model-ids-2026-09.md`.
- Rỗng/transient: retry 2-3s; flash rỗng ~80% với prompt dài → retry 3 lần + fallback pro (chọn model bằng benchmark 5 lần, đếm ok). Chi tiết: `references/tfo-provider-transient-2026-08.md`.
- **Hết sub OpenCode → ByteDance Ark fallback (22/09, cứu chuỗi None 11 ngày): `references/bytedance-ark-fallback-2026-09.md`.**
- **Chain giờ 4 chân: OpenCode → Ark → OpenRouter → Gemini (cả 2 chân cũ chết cùng lúc 05/10 → 0/5 agent 9 ngày; 14/10 nối lại, 5/5). Bẫy: 402 free-tier giữa chừng (200 ở 3 call đầu ≠ còn tiền), model Google đổi tên, "chết ở bước đọc key" vs "provider chặn", probe `docs/qa/probe_llm_chain.py` + 2 pitfall PASS giả: `references/llm-chain-fallback-2026-10.md`.**
- Prompt Việt dài: gọi Python trực tiếp (`BaseAgent(...).think(...)`), không qua CLI (escaping hỏng). `cmd_agent` + `prompt` = bypass phase logic có chủ đích.
