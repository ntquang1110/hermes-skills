---
name: sol-pi-hermes
description: "Use when reducing Hermes token waste via SoL-Pi patterns."
category: software-development
---

# SoL-Pi for Hermes

Apply 4 efficiency mechanisms from NVIDIA SoL-Pi paper into Hermes workflow.

## 1. ObservationPack — archive large tool output

When file/tool output >500 chars, archive with `pack()` instead of keeping full content.

```python
from deterministic.hermes.pack import observe_file, recall

packed = observe_file(path)
# Only packed (handle + excerpt) goes to context
content = recall(packed["handle"])  # when needed
```

## 2. Action Fusion — batch commands without LLM

```python
from deterministic.hermes.fusion import run_sequence, git_commit_all

result = git_commit_all("fix: update config")  # 1 call instead of 3
result = run_sequence(["npm install", "npm run build"])  # 1 call instead of 2
```

## 3. Context Compact — compress after each subtask

```python
from deterministic.hermes.compact import save_state, load_state

save_state("phase-1", {"findings": findings})  # dump, clear context
prev = load_state("phase-1")  # clean context, only prev state
```

## 4. Evidence-Preserving Reducer

Use deterministic code for tasks with right answers:
- `deterministic/metelligent/parser.py` — parse tasks
- `deterministic/content/extractor.py` — extract structured data
- `deterministic/aicompany/contract.py` — validate schema

LLM only for reasoning.

## Triggers

- Output >500 chars -> ObservationPack
- 2+ sequential commands -> Action Fusion
- Long multi-step session -> Context Compact
- Deterministic task -> code, not LLM
