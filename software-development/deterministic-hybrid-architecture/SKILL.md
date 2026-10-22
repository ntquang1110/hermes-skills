---
name: deterministic-hybrid-architecture
description: "Use when deterministic code handles structure, LLM reasoning"
category: software-development
---

# Deterministic + LLM Hybrid Architecture

OCR-inspired pattern: tasks with right answers use deterministic code, only reasoning tasks use LLM.

## Core Principle

Việc nào có đáp án đúng thì code tất định lo.
Việc nào cần phán đoán thì mới gọi LLM.

This cuts token cost 40-60% and improves reliability vs pure-LLM approaches.

## How to Identify What Goes Where

| Task type | Deterministic | LLM | Example |
|-----------|--------------|-----|---------|
| Parse/extract | Yes | No | Date parsing, regex extraction |
| Validate schema | Yes | No | JSON schema check, type validation |
| Format/transform | Yes | No | Sort, filter, map, template fill |
| Search/lookup | Yes | No | SQL query, file search, regex match |
| Calculate | Yes | No | Math, aggregation, statistics |
| Summarize | No | Yes | Condense meaning, extract key points |
| Generate content | No | Yes | Write draft, compose response |
| Decide ambiguous | No | Yes | Priority judgment, tone selection |
| Research/explore | No | Yes | Web search, source synthesis |

## Architecture Pattern

Input → [Deterministic Layer: parse, validate, extract, format. NO LLM.]
→ structured data → [LLM Agent: reasoning only. Clean structured input.]
→ [Deterministic Post: validate LLM output, format, persist. NO LLM.]

## Implementations (Quang's system)

### metelligent/parser.py — Task Parser

LLM summarize (structured JSON) → deterministic parse_summary() validates + normalizes → deterministic format_tasks() sorts + assigns IDs. Vietnamese date parser handles mai, tuần sau, thứ 6. Saves 1 LLM call per meeting.

### content/extractor.py — Transcript Extractor

Deterministic extract_structured(): regex for quotes, numbers, timestamps, topics. LLM only writes thread from pre-extracted building blocks. Template-based prompt. Token savings grow with transcript length.

### aicompany/contract.py — Agent Contracts

Contract.validate(): deterministic schema check (types, required fields, nested). Contract.coerce(): deterministic type coercion (string→list, int→float). AgentPipeline chains agents with validation between steps. LLM only produces content within schema.

## Hermes Integration

- ObservationPack (deterministic/hermes/pack.py): archive tool output, keep handle + excerpt in context. Recall on demand.
- Action Fusion (deterministic/hermes/fusion.py): batch sequential commands into one call. No LLM between steps.
- Context Compact (deterministic/hermes/compact.py): save state between subtasks. Clean context per subtask.

## When NOT to Use

- One-shot tasks where deterministic overhead > LLM cost
- No clear structure (open-ended conversation)
- Rapid prototyping where speed > efficiency

## References

- Open Code Review (OCR) by Alibaba: deterministic file selection + LLM review
- SoL-Pi by NVIDIA: 3/4 mechanisms are deterministic harness engineering
- Files in C:\Users\NTQUANG_DELL\deterministic\
