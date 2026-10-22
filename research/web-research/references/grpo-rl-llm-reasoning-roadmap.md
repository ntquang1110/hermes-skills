# GRPO & RL for LLM Reasoning — Condensed Research Bank (arXiv-based, Aug 2026)

Data extracted from FULL PDFs during the 2026-08-01 AI-rotation run (index 1). Use these
numbers to cite exact values in future AI/tech KF cards WITHOUT re-downloading/re-extracting
the 5MB PDFs. Card created this run: "🤖 GRPO & RL cho LLM Reasoning — Từ DeepSeekMath đến
DeepSeek-R1" (KF reading time 780s, verified landed 2026-08-01). For dedup: check `/api/cards`
for title containing GRPO/RL/reasoning before reusing this topic.

## Papers

| Paper | arXiv ID | Contribution |
|---|---|---|
| Shao et al. 2024 — DeepSeekMath | 2402.03300 | Introduces GRPO: formula, mechanism, ablations |
| DeepSeek-AI 2025 — DeepSeek-R1 | 2501.12948 | R1-Zero pure RL + "aha moment", R1 4-stage pipeline, reward design, distillation, costs |
| Schulman et al. 2017 — PPO | 1707.06347 | Base algorithm GRPO derives from |
| Ouyang et al. 2022 — InstructGPT/RLHF | 2203.02155 | Standard PPO+KL RLHF context |
| Wang et al. 2023 — Self-Consistency | 2203.11171 | Cons@16 decoding used in R1-Zero eval |

## GRPO core algorithm (DeepSeekMath Eq.3 / DeepSeek-R1 Eq.1)

- GRPO **drops the critic/value model** of PPO (saves ~50% memory/compute). Baseline = group z-score.
- Per question q, sample G outputs {o1..oG} from old policy, reward model scores them:

```
J_GRPO(θ) = E[ 1/G Σᵢ 1/|oᵢ| Σₜ min( πθ(oᵢ,ₜ|q,oᵢ,<ₜ)/πθold(oᵢ,ₜ|q,oᵢ,<ₜ)·Âᵢ,ₜ,
                                    clip(πθ/πθold, 1−ε, 1+ε)·Âᵢ,ₜ ) − β·D_KL(πθ||πref) ]
Advantage:  Âᵢ = (rᵢ − mean(r)) / std(r)   ← group-normalized
KL (unbiased, always ≥0):  D_KL = πref/πθ − log(πref/πθ) − 1   (Schulman 2020)
```

- KL penalty goes into the LOSS directly (not into reward like PPO) — keeps Âᵢ,ₜ clean.
- **Outcome supervision** (OS): reward at end, same normalized reward for all tokens.
  **Process supervision** (PS): reward per step, Âᵢ,ₜ = Σ normalized rewards of steps AFTER t.
  DeepSeekMath found **GRPO+PS > GRPO+OS**.
- GRPO > Online RFT because it scales gradient by reward magnitude (penalizes wrong answers,
  rewards correct ones proportionally); RFT rewards all correct answers equally, never penalizes.

## Hyperparameters

- **DeepSeekMath (7B):** lr 3e-6, KL β 0.001, temp 1.0, G=16 (per-question outputs).
- **DeepSeek-R1-Zero (671B MoE, 37B active):** lr 3e-6, β 0.001, temp 1.0, G=16, max len
  32,768 tokens → 65,536 after step 8.2k; 10,400 steps = 1.6 epochs; batch 512
  (32 questions × 16); reference model refreshed every 400 steps; 8,192 rollouts/step →
  16 minibatches, 1 inner epoch.
- **DeepSeek-R1 stage 1:** clip ratio **ε = 10** (critical — low ε truncates gradients and
  degrades performance), lr 3e-6, β 0.001, temp 1.0, G=16.
- **Reward:** `Reward_rule = Reward_accuracy + Reward_format` (same weight). Accuracy = rule-based
  (math answer match / compiler test cases for code); format = `<think>...</think><answer>...</answer>`
  tags. **No neural reward model for reasoning** — neural RMs get reward-hacked at scale.

## Key results (quote these)

**DeepSeekMath-RL 7B (GRPO on subset of SFT data):**
| Metric | Instruct 7B | RL 7B (GRPO) |
|---|---|---|
| GSM8K | 82.9% | 88.2% |
| MATH (competition) | 46.8% | 51.7% |
| CMATH (out-of-domain) | 84.6% | 88.8% |

- RL raises **Maj@K but NOT Pass@K** → RL makes output distribution more robust (boosts correct
  answer into Top-K), doesn't raise base capability.
- Corpus: 120B math tokens from Common Crawl (fastText classifier + human refinement), ~7× Minerva,
  ~9× OpenWebMath. Code pre-training before math helps reasoning.

**DeepSeek-R1-Zero (no SFT at all):** AIME 2024 pass@1 **15.6% → 77.9%** during training
(beyond avg human competitor); Cons@16 = **86.7%**. "Aha moment" (Table 2): model self-wrote
"Wait, wait. Wait. That's an aha moment I can flag here." → emergent self-reflection/verification.
Response length grows naturally during training (model learns to think longer).

**DeepSeek-R1 (Table 8):**
| Benchmark | GPT-4o | o1-1217 | DeepSeek-V3 | **R1** |
|---|---|---|---|---|
| AIME 2024 Pass@1 | 9.3 | 79.2 | 39.2 | **79.8** |
| MATH-500 Pass@1 | 74.6 | 96.4 | 90.2 | **97.3** |
| CNMO 2024 | 10.8 | — | 43.2 | **78.8** |
| GPQA Diamond | 49.9 | 75.7 | 59.1 | **71.5** |
| Codeforces percentile | 23.6 | 96.6 | 58.7 | **96.3** |
| LiveCodeBench | 32.9 | 63.4 | 36.2 | **65.9** |
| SWE Verified | 38.8 | 48.9 | 42.0 | 49.2 |
| MMLU | 87.2 | 91.8 | 88.5 | **90.8** |
| AlpacaEval2.0 LC-win | 51.1 | 57.8 | 70.0 | **87.6** |
| ArenaHard | 80.4 | 92.0 | 85.5 | **92.3** |

Human comparison: R1 beats avg AIME competitors; beats 96.3% of Codeforces humans; still below
PhD-with-web humans on GPQA (71.5 vs 75.8).

## R1 4-stage pipeline

```
0: Cold-start SFT (few thousand human-aligned conversational CoT)
1: RL reasoning — rule reward + Language Consistency reward  (Reward_lang = Num(target words)/Num(words))
2: Rejection sampling + SFT (800k: reasoning + non-reasoning)
3: RL stage 2 — helpfulness (RM 66,000 preference pairs, arena-hard format, 4 judgments/model,
   keep Δ>1, length-balanced) + harmlessness (point-wise RM, 106,000 prompts) + reasoning
```

- Helpful RM: batch 256, lr 6e-6, 1 epoch, max seq 8,192.
- Language-consistency reward slightly degrades coding benchmark but improves readability —
  trade-off accepted.

## Distillation (fine-tune base 2–3 epochs on 800k data, cosine decay → lr/10, ctx 32768, batch 64)

| Distill model | Base | Initial LR |
|---|---|---|
| R1-Distill-Qwen-1.5B | Qwen2.5-Math-1.5B | 1e-4 |
| R1-Distill-Qwen-7B | Qwen2.5-Math-7B | 8e-5 |
| R1-Distill-Qwen-14B | Qwen2.5-14B | 7e-5 |
| R1-Distill-Qwen-32B | Qwen2.5-32B | 6e-5 |
| R1-Distill-Llama-8B | Llama-3.1-8B | 5e-5 |
| R1-Distill-Llama-70B | Llama-3.3-70B-Instruct | 2e-5 |

Distilled small models beat their original instruct-tuned counterparts → reasoning compresses well.

## Training cost (Table 7, H800 at $2/GPU-hr)

- R1-Zero: 101K GPU-hrs ($202K); SFT data creation: 5K ($10K); R1: 41K ($82K); **Total 147K ($294K)**.
- R1-Zero used 64×8 H800, ~198 hrs; R1 ~80 hrs.

## Known limitations (DeepSeek-R1 Section 5)

- **Reward hacking** (Fig 6): reward climbs while CodeForces drops when using helpful RM → policy
  learns to fool the RM. Rule-based rewards are the backbone of pure-RL reasoning; tasks without a
  reliable verifier (e.g. writing) can't scale pure RL yet.
- Overthinking: excess tokens on easy questions (test-time compute not optimal).
- Language mixing (EN/CN only optimized); few-shot prompting DEGRADES performance (use zero-shot +
  explicit output format); software-engineering RL underdeveloped due to slow eval.

## 2026 follow-up papers (for future AI-rotation cards)

| Paper | arXiv | One-liner |
|---|---|---|
| MC-GRPO | 2601.22582 | Small rollout budget → mean-baseline noise → advantage sign flips; use MEDIAN baseline |
| DaGRPO | 2512.06337 | GRPO training instability from gradient conflict between group outputs; distinctiveness-aware |
| Constrained GRPO | 2602.05863 | Lagrangian extension for behavioral constraints (safety/cost) |
| Invisible Reasoning | 2607.22925 | Models use semantically-irrelevant filler tokens to score higher on synthetic reasoning tasks — CoT is NOT a faithful trace (13 frontier models, 3 tasks) — safety-monitoring warning |
| Training-Free GRPO | 2510.08191 | GRPO-style advantage without training (agentic setting) |
| GRPO for Speech Recognition | 2509.01939 | GRPO applied to ASR |

## Suggested future subtopics (index-1 rotation, avoid repeating GRPO card)

- PPO vs GRPO deep-dive (critic model cost analysis, GAE vs group-z-score)
- RLHF vs DPO vs GRPO unified paradigm (DeepSeekMath Section 4.2 unified framework)
- Reward hacking in LLM RL (mechanisms + mitigations)
- Test-time compute scaling (CoT length, majority voting, MCTS vs dynamic allocation)
- Knowledge distillation for reasoning models (why reasoning compresses to small models)
- RL with Verifiable Rewards (RLVR) pattern — cheapest way to improve reasoning
