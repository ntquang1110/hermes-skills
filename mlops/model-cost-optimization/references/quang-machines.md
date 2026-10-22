# Quang's Machine Topology (for model deployment)

Up-to-date as of 2026-08-22. Re-verify before relying on it — hardware/network can change.

## Hermes host (this machine — the laptop)
- **OS:** Windows 10, MSYS/git-bash shell, workdir `D:\Hermes Proj`.
- **CPU (verified 2026-09-25):** Intel i7-4910MQ 4 cores / 8 threads @2.9 GHz (Haswell, AVX2, no AVX-512/VNNI/AMX), 15.9 GB RAM total (~10.5 GB free at rest), 141 GB disk ~86% used (~21 GB free).
- **GPU:** NVIDIA Quadro K2100M **2GB VRAM** + Intel HD Graphics 4600. **No usable GPU for LLM inference.** `nvidia-smi` is NOT present on this host.
- **CPU has enough RAM for offload** but 2GB VRAM means any real model (even 7B Q4 ≈5GB) spills to CPU → ~1-3 tok/s. **Local LLM inference on THIS host is not viable.** Don't recommend it.
- **BUT CPU-only *encoder/classifier* models DO run here (measured 2026-09-25, torch CPU fp32 eager, 8 threads):** 146M encoder (1.05 GB fp32 bin) = **411 ms @77 tokens bs=1**, 250 ms/text at bs=8 (batching only 1.6x), **4.19 s @797 tokens**; a full 3-question request end-to-end ≈ 0.6 s. Scale ≈ **x2.6** for a 400M/2.3 GB encoder on this x86 laptop (Apple silicon is ~x1 — bandwidth-bound). Encoder weights: ~2.6 GB resident per 1.05 GB fp32 checkpoint.
- DeepSeek default via opencode-go; fallback chain: opencode-zen flash/vultra-free → opencode-go flash/pro.
- Keys available: OPENROUTER, GOOGLE (gemini), GROQ, NOTION, TRELLO, SEARXNG.

## Remote GPU machine — GTX 1660 Super 6GB
- **Reach:** Tailscale/WireGuard IP **100.88.115.32** (CGNAT 100.64.0.0/10). Ping OK, latency ~124-450ms avg 287ms (check whether P2P direct or DERP relay — relay hurts token streaming).
- **Status 2026-08-22:** machine ONLINE but **NO service port open** (22/11434/8080/8000/3000/7860/5000/9000 all closed). User said "Unsloth already running" — but Unsloth does **not** auto-serve HTTP. Hermes host cannot reach it until the remote runs `ollama serve`, `llama-server`, or `vllm serve` bound to `0.0.0.0`.
- **To use it:** must open port 11434 (Ollama) or 8080/8000, then point Hermes `base_url` at `http://100.88.115.32:<port>/v1`.

## Model deployment decision for this setup
With 1660 Super 6GB: Qwen8B Q4 ≈5GB fits cleanly (~10-15 tok/s); Gemma12B Q4 ≈7GB slightly overruns. Qwen27B (≈16GB) is NOT viable on 6GB — advise against.

## Quang's workload tiers (mapped 2026-08-22)
- **Heavy/API:** knowledge-researcher-4h (deepseek-v4-pro), Daily Research for Threads (citations), legal review. These MUST stay on strong API — local fabricates citations and loses Vietnamese diacritics.
- **Light/local-candidate:** Tâm lý 6 bài, leadership check-ins, transcript→threads raw summarize. Good candidates to offload to remote Qwen8B once the remote Ollama is up.
- **Pure script (already 0 LLM, keep):** all watchdogs (erp/tunnel/ports/firstonly/upload), trello-watch, follow-claw/lanchat, YouTube Schedule Poster. These are the best evidence the token spend is concentrated in the 3 LLM research jobs, not the 14 scripts.

## User approach preferences (learned this session)
- Wants **manual per-task setup first** for control, not an auto-router. Encode as: start with aliases + per-cron model assignment (Hermes-native = "Hướng A"), only build a custom orchestrator/dashboard ("Hướng B") once A proves insufficient AND real cost numbers are recorded.
- Expects plain, direct answers — say plainly when hardware can't do something (e.g. "27B on 6GB is not viable") instead of letting them download more huge models.
- Communicates in Vietnamese with diacritics; responds naturally in kind.