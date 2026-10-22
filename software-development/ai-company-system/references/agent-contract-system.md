# Structured Agent Contract System

Built for AI Company multi-agent communication. Implemented Sep 2026 in `C:\Users\NTQUANG_DELL\deterministic\aicompany\contract.py`.

## Problem

Agents communicate via natural language. Each decode loses information. LLM must guess what another LLM meant. Result: drift, hallucinated tasks, inconsistent output.

## Solution

Every inter-agent message has a **schema contract** that is validated deterministically before forwarding. No natural language between agents.

## Core architecture

```
Agent A produces raw dict
  -> Contract.validate() -> raises SchemaValidationError with field-level errors
  -> Contract.coerce() -> attempts auto-fix (string to list, missing defaults)
  -> validated JSON -> Agent B receives
  -> Agent B only reasons from clean data, never guesses format
```

## Contract definition

```python
from deterministic.aicompany.contract import Contract, AgentPipeline

RESEARCHER = Contract(
    name="researcher",
    output_schema={
        "query": "str",
        "findings": [{
            "claim": "str",
            "source": "str",
            "confidence": "float",
            "verified?": "bool",
        }],
        "sources_consulted": ["str"],
        "summary": "str",
    },
)

# Validate
output = RESEARCHER.validate(raw_llm_output)
# Or coerce (auto-fix common LLM mistakes)
output = RESEARCHER.coerce(messy_llm_output)
```

## Schema type system

| Type | Meaning |
|------|---------|
| `"str"` | String |
| `"int"` | Integer |
| `"float"` | Number (int or float accepted) |
| `"bool"` | Boolean |
| `["str"]` | List of strings |
| `[{"key": "str"}]` | List of nested dicts with schema |
| `"field?"` | Suffix `?` on key = optional field |

## Validation behavior

- Missing required field: error with field path (e.g. `$.findings[0].source: required field missing`)
- Wrong type: error (`$.findings: expected list, got str`)
- Unknown fields: warning in errors
- Optional field missing: silently skipped

## Coercion behavior

- `str` to `int`/`float`: attempts parse, falls back to 0/0.0
- single value to `list`: wraps in `[value]`
- `"true"`/`"yes"`/`"1"` string to `bool`: parses correctly
- nested dict missing required sub-fields: sets empty defaults
- Can't coerce string to dict with required fields: fails cleanly

## Predefined contracts

| Contract | Output fields | Use case |
|----------|--------------|----------|
| RESEARCHER_CONTRACT | query, findings[], sources_consulted[], summary | Research agent output |
| WRITER_CONTRACT | topic, draft, tone, key_quotes[], word_count | Content writing agent |
| REVIEWER_CONTRACT | draft_reviewed, issues[], verdict, overall_score | Peer review agent |
| PLANNER_CONTRACT | goal, steps[], total_steps, risks[] | Task planning agent |

## Pipeline orchestration

```python
pipeline = AgentPipeline()
pipeline.add_step("research", RESEARCHER_CONTRACT, my_researcher_fn)
pipeline.add_step("write", WRITER_CONTRACT, my_writer_fn)
results = pipeline.run({"request": "..."})
# Each result is validated before passing to next step
```

## Integration with existing AI Company

The contract system lives in `deterministic/` as an independent Python package. Import into `ai-company/` scripts:

```python
import sys
sys.path.insert(0, "C:/Users/NTQUANG_DELL/deterministic")
from aicompany.contract import RESEARCHER_CONTRACT
```

The existing AI Company uses natural language message bus (shared/inbox.py). Add contract validation at the integration point where an agent reads messages: validate before processing.
