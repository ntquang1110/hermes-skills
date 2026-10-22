# Deterministic + LLM Hybrid Architecture

Inspired by Alibaba's Open Code Review (ocr) and applied to Quang's systems Sep 2026.

## Core principle

Việc nào có đáp án đúng thì code tất định lo. LLM chỉ làm việc cần phán đoán.

## Why it matters

A pure LLM pipeline wastes tokens on things with right answers (parsing dates, validating schemas, extracting numbers) and introduces drift where none is needed. A pure deterministic pipeline can't handle ambiguity, summarization, or intent understanding.

The hybrid splits the work at the natural seam.

## Implementation patterns built this session

### 1. meTelligent task parser

**Path:** `C:\Users\NTQUANG_DELL\deterministic\metelligent\parser.py`

**Before:** STT to LLM summarize to LLM extract task (2 LLM calls, format drift)

**After:** STT to LLM summarize (output structured JSON) to deterministic parser validates + normalizes + sorts. Zero second LLM call.

**Deterministic components:**
- `parse_date(raw_date, today)` — Vietnamese date expressions (mai, tuần sau, thứ 6, cuối tuần này, ngày 15/10) to ISO dates. Handles relative, weekday, and absolute patterns.
- `parse_priority(hint)` — Vietnamese priority words (gấp, quan trọng, không gấp) to enum (high/medium/low). Ordered check to avoid "không gấp" matching "gấp" first.
- `validate_action_item(item)` — rejects empty who, short what, missing fields.
- `format_tasks(items)` — sorts by priority then due date then name, assigns stable TASK-NNN IDs.

### 2. Content pipeline extractor

**Path:** `C:\Users\NTQUANG_DELL\deterministic\content\extractor.py`

**Before:** Transcript to LLM summarize to LLM write thread (LLM reads full raw transcript)

**After:** Transcript to deterministic extract topics/quotes/numbers/timestamps to LLM fills template from structured data

**Deterministic components:**
- `extract_quotes(text)` — finds all quoted speech (double quotes, single quotes, Vietnamese corner brackets)
- `extract_numbers(text)` — percentages, money amounts with surrounding context
- `extract_topics(text)` — segments transcript by topic transition markers (tiếp theo, đầu tiên, thứ nhất, chuyển sang...)
- `extract_key_sentences(text, max)` — first sentence of each paragraph + sentences with topic markers

**Template:** `THREAD_PROMPT_TEMPLATE` with placeholder for structured data. LLM fills content but output structure is fixed.

### 3. AI Company contract system

**Path:** `C:\Users\NTQUANG_DELL\deterministic\aicompany\contract.py`

**Before:** Agent A outputs natural language to Agent B decodes to LLM guesses meaning to information drift

**After:** Agent A outputs JSON to Contract.validate() deterministic pass/fail to Agent B receives clean JSON to LLM only reasons

**Key classes:**
- `Contract(name, output_schema, description)` — defines expected output shape with field types
- `Contract.validate(data)` — checks types, required fields, nested dict/list structure. Raises SchemaValidationError with specific field-level errors.
- `Contract.coerce(data)` — attempts to fix common LLM issues: string to list, int to float, missing fields get defaults. Recursively handles nested schemas.
- `AgentPipeline` — chains multiple agents with contract validation between each step

**Schema format:**
- `"field": "str"` — required string
- `"field?": "int"` — optional integer
- `"field": ["str"]` — list of strings
- `"field": [{"nested": "str"}]` — list of nested dicts

**Predefined contracts:**
- `RESEARCHER_CONTRACT` — query, findings[claim/source/confidence], sources_consulted[], summary
- `WRITER_CONTRACT` — topic, draft, tone, key_quotes[], word_count
- `REVIEWER_CONTRACT` — issues[severity/description/suggestion], verdict, overall_score
- `PLANNER_CONTRACT` — goal, steps[id/action/assigned_to/depends_on], total_steps, risks[]
