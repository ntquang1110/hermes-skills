---
name: deterministic-llm-hybrid
description: "Deterministic+LLM hybrid: code for facts, LLM for judgment."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [architecture, llm, deterministic, optimization, system-design, token-efficiency]
    related_skills: [system-design-workflow, model-cost-optimization, design-critique]
---

# Deterministic + LLM Hybrid Architecture

**Core principle:** Not everything needs an LLM. Things that have a right answer should be handled by deterministic code. Things that need judgment should call an LLM — but only with clean, structured input.

Inspired by Alibaba's OCR and NVIDIA's SoL-Pi. Applied to Quang's systems.

---

## When to Use

- Building any system that calls LLMs (agent, pipeline, automation)
- Asked how to reduce token cost or improve reliability
- LLM keeps making mistakes on structured tasks
- Multi-agent system with inter-agent communication

## When NOT to Use

- One-off script, throwaway prototype
- Purely creative task with no structured output
- LLM is already the right tool for the entire task

---

## The Pattern

### Step 1: Audit the LLM call chain

Classify each LLM call:

| Category | Example | Should be |
|----------|---------|-----------|
| Extraction | Getting dates/names from text | Deterministic parser |
| Validation | Checking schema compliance | Deterministic validator |
| Transformation | Summary → tasks | Structured prompt + parser |
| Reasoning | Judgment, synthesis, writing | LLM (keep) |
| Routing | Which path to take | Deterministic if-then |
| Search | Finding information | Index/SQL/grep |

**Rule:** If you can write a Python function that does it correctly, don't call an LLM.

### Step 2: Build the deterministic layer

Pure functions for:
- Date/time parsers (Vietnamese: "mai", "tuần sau", "thứ 6")
- Priority mappers ("gấp" → high, check "không gấp" BEFORE "gấp")
- Schema validators (type checking, required fields, coercion)
- Topic/quote/number extractors (regex)
- File selectors (path/extension/size gates)

**Pitfall — Priority substring order:** Check negative phrases ("không gấp") before positive ones ("gấp"). Otherwise "không gấp" matches "gấp" first and maps to high.

### Step 3: Feed LLM only structured data

**Bad:** `llm_input = raw_transcript` (5000 chars, full noise)
**Good:** `llm_input = {"quotes": [], "numbers": [], "topics": [], "key_sentences": []}`

Benefits: smaller context, cheaper, no distraction, less hallucination.

### Step 4: Contract between LLM and downstream

1. LLM outputs JSON with fixed schema
2. Deterministic validator checks required fields, types
3. Coercion layer fixes common LLM mistakes (string→list, missing optionals)
4. Pipeline gate rejects invalid output

### Step 5: Measure token savings

| Before | After | Savings |
|--------|-------|---------|
| LLM reads full transcript | LLM reads structured extract | ~40-60% input tokens |
| LLM extracts tasks | Deterministic parser | 1 call eliminated |
| Agent A sends NL to Agent B | Agent A sends validated JSON | No decode cost |
| LLM re-reads file every turn | Handle + excerpt (ObservationPack) | ~44-49% tokens |

---

## Case Studies

### OCR (Alibaba Open Code Review)

Deterministic `selectFiles()` + `groupDiffs()` (LLM-assisted with fallback) + rule engine → then LLM does actual review. Result: ~1/9 tokens.

### SoL-Pi (NVIDIA)

4 harness mechanisms: 3 deterministic engineering, 1 cheaper LLM. Result: 44-49% token reduction, ~33% cost cut.

### Quang's Implementation

`C:\Users\NTQUANG_DELL\deterministic/`:

| Module | Deterministic | LLM |
|--------|--------------|-----|
| `metelligent/parser.py` | Date/priority parsing, validation | Summarize (structured JSON) |
| `content/extractor.py` | Quote/number/topic extraction | Fill thread template |
| `aicompany/contract.py` | Schema validation, coercion | Agent reasoning |

## Reference files

- `references/ocr-alibaba-pattern.md` — OCR review (in design-critique skill)
- `references/sol-pi-nvidia-pattern.md` — SoL-Pi review (in design-critique skill)
- Source: `C:\Users\NTQUANG_DELL\deterministic/`

## Related Skills

| Skill | Use |
|-------|-----|
| `system-design-workflow` | Full system design cycle |
| `model-cost-optimization` | Provider/model/harness cost choices |
| `design-critique` | Source-first claim verification |
