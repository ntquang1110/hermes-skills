# Deterministic Layer — Python Implementation

**Location:** `C:\Users\NTQUANG_DELL\deterministic/`

Three modules implementing the deterministic+LLM hybrid pattern.

## Module 1: meTelligent Task Parser

**File:** `deterministic/metelligent/parser.py`

**Flow:** STT (Groq) → LLM summarize (JSON output) → deterministic parser validates + formats tasks

**Deterministic functions:**
- `parse_date(raw_date, today)` — Vietnamese date parser: "mai" → next day, "thứ 6" → next Friday, "cuối tuần này" → next Sat+Sun, "ngày 15/10" → 2026-10-15
- `parse_priority(hint)` — Priority mapper: "gấp" → high, "không gấp" → low (checked BEFORE "gấp")
- `validate_action_item(item)` — Checks who/what exist, minimum 5 chars
- `parse_summary(llm_output)` — Strips markdown fences, fixes trailing commas, validates JSON
- `format_tasks(items)` — Sorts by priority→date→name, assigns TASK-001 IDs

**Prompt template:** `SUMMARIZE_PROMPT_TEMPLATE` — tells LLM to output JSON with `summary`, `decisions`, `action_items[]`, `questions`, `next_steps[]`

## Module 2: Content Pipeline Extractor

**File:** `deterministic/content/extractor.py`

**Flow:** YouTube transcript → deterministic extractor → structured data → LLM fills thread template

**Deterministic extractors:**
- `extract_timestamps(text)` — Finds HH:MM:SS patterns with surrounding context
- `extract_quotes(text)` — Finds quoted text (double quotes, single quotes, Vietnamese 「」)
- `extract_numbers(text)` — Finds percentages, money amounts with context
- `extract_topics(text)` — Segments by transition markers ("tiếp theo", "đầu tiên", "bây giờ", "next", "finally")
- `extract_key_sentences(text, max)` — First sentence of each paragraph + topic-marked sentences

**Thread template:** `THREAD_PROMPT_TEMPLATE` — Fixed structure (mở đầu → Tầng 1 → Tầng 2 → kết), LLM fills from structured data only

## Module 3: AI Company Contract System

**File:** `deterministic/aicompany/contract.py`

**Flow:** Agent A → JSON output → Contract.validate() → Agent B receives clean JSON → reasoning only

**Contracts defined:**
- `RESEARCHER_CONTRACT` — query, findings[].{claim, source, confidence}, sources[], summary
- `WRITER_CONTRACT` — topic, draft, tone, key_quotes[], word_count
- `REVIEWER_CONTRACT` — draft_reviewed, issues[].{severity, description, suggestion}, verdict, score
- `PLANNER_CONTRACT` — goal, steps[].{id, action, assigned_to, depends_on}, total_steps, risks

**Key classes:**
- `Contract(output_schema)` — validate() (strict), coerce() (try-fix)
- `AgentPipeline()` — chain agents with contract validation between steps

**Schema features:**
- Type validation (str, int, float, bool, list, dict)
- Nested schema (list-of-dict with sub-schema)
- Optional fields (key? → "str")
- Coercion: string→list, int→float, missing optionals→defaults
