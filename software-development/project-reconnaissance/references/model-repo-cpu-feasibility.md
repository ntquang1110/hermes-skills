# Auditing a MODEL repo for real deployability (worked example: jeff / GLiFormer, 2026-09-25)

Companion to `references/external-framework-evaluation.md`, which covers *should we adopt this
repo?*. This file covers the harder question the user actually asks about ML repos:
**"nó chạy được trên máy anh không?"** — can this model repo actually run and serve here?

Task shape: user points at a GitHub repo implementing a self-hosted version of some hosted
model API. Deliverable = Vietnamese report with REAL numbers (benchmarks quoted from the repo,
plus first-hand measurements where possible), architecture walkthrough, and a feasibility verdict.

## 1. Read order that works (parallel batches)

| Batch | Files | What you get |
|---|---|---|
| 1 | `README.md`, `bench/RESULTS.md` (or docs/benchmarks), `pyproject.toml`/`requirements.txt`, `.python-version` | pitch, HONEST benchmark tables, dep set, interpreter pin |
| 2 | every file in `core/` (engine/answers/…) + `backends/` | how a request actually becomes model input |
| 3 | `server/` (`app.py`, `batcher.py`, `config.py`, `main.py`) | API surface, error codes, limits, defaults |
| 4 | `deploy/*`, `tests/*`, `scripts/*` | what the author considers production, and how they test |

Repo benchmark files are the goldmine: they usually contain the author's own CPU-vs-GPU arm and
an explicit verdict (jeff's RESULTS.md literally says the CPU arm "is not a cheaper tier"). Quote
those numbers verbatim; do NOT re-derive them.

## 2. Turn "requires-python" into a real answer

A pin like `requires-python = ">=3.12,<3.13"` is policy, not physics. Check, in order:
1. PyPI JSON for each key dep: `requires_python` + the wheel filename list → does a
   `cpXX-win_amd64` (or manylinux) wheel exist for the interpreter the user actually has?
2. `uv pip install --dry-run --python <venv python>` with the repo's dep list → resolution proof
   without downloading GBs.
3. `uv python install <pinned version>` → uv pulls that CPython itself, so the pin costs ~15 s.
4. Only then decide. Report: "pin is not a blocker; uv fetches 3.12.13 in 13 s" beats
   "requires 3.12, user has 3.14, blocked".

Also apply `references/external-framework-evaluation.md`'s claim-verification habit to the
README's headline numbers: check them against the repo's own raw result JSONL files.

## 3. Prove the code path, not just the install

Three tiers of evidence, all cheap once deps exist:
- Fake/mock-backend unit tests under the target interpreter (jeff: `tests/test_core.py`,
  `tests/test_server.py`, 15 + 7 passed on BOTH 3.12 and 3.14).
- One REAL model run: load the smallest checkpoint the repo tests with (jeff's `*-base-v1`,
  1 GB, not the 400M production one) and run the repo's own bench/probe script.
- Cross-interpreter diff: same request, same decoded output on both interpreters — this is what
  proves the pipeline is real rather than "imports happened".

Environment gotcha that will bite every venv on this host: Hermes exports a 3.11
`PYTHONPATH`, so a 3.12 venv dies with `numpy._core._multiarray_umath`. `unset PYTHONPATH` first.
Details + the CPU probe script live in `model-cost-optimization`.

## 4. Report structure that satisfied the ask

Numbers first, verdict last, and label extrapolation loudly:
1. Bản chất (what it IS — encoder classifier, not an LLM; which API it impersonates)
2. Kiến trúc code, per-module (engine → groups → backend; decode math: normalize/confidence/temperature)
3. Benchmark THẬT from the repo (latency, cost, accuracy vs the hosted original, leaderboard score + rank)
4. Đo thực tế trên máy này (table: case | ms | tokens | interp) — plus what you did NOT get to measure
5. Khả năng deploy (dependency/wheel audit, pins, workarounds, RAM/disk budget)
6. Đánh giá khả thi + "nên dùng khi / không nên dùng khi"

Never let extrapolated numbers masquerade as measurements. In the jeff session the 400M row was
computed from the measured 146M row x2.6 (the repo's own base→large factor on x86) because the
2.3 GB download didn't finish; saying so explicitly was part of the deliverable, and the estimate
landed near the repo's own official CPU figure (0.94 s p50 on a 4-thread Ryzen 5 3600).

## 5. jeff specifics worth not re-deriving

- GLiFormer 400M encoder answering jev `choice`/`score`/`noul` questions; each question = a label
  group; `noul` gets its own encoder pass (`JEFF_ISOLATE=nouls`), choice+score share one.
- `temperature=3.2` flattens probabilities/confidence/noul but `score` is computed from the RAW
  distribution (so `score` only matches `probabilities` at T=1).
- JevBench v1.2.2: jeff 66.9 (#9/18) vs jev 75.3 (#2); Intelligence #14, Speed #16, Cost #5 —
  the rank is carried by cost, hard tier 37.7% vs 74.1%.
- Official CPU row: 4 threads of a Ryzen 5 3600 → 0.94 s p50 raw, 10.97 s p95 on long hard items.
  Sanity-check any new CPU estimate against those two numbers.
- Windows verdict: works (uv-managed 3.12; ONNX-int8 `JEFF_BACKEND=onnx` for CPU); Python 3.14
  runs it too but `torch.jit.script` is unsupported there — not recommended.
