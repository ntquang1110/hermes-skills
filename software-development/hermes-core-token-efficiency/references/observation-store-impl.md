# ObservationStore — production implementation detail

Built into Hermes core at `tools/tool_result_storage.py` (session: Sept 2026).
Goal: archive large tool output out of context automatically, recall later
without losing data, with zero new registered tools.

## Public API

```python
from tools.tool_result_storage import (
    ObservationStore,        # class
    recall_tool_result,      # convenience wrapper (dev use; model uses read_file)
    get_observation_stats,   # session stats dict
)

obs = ObservationStore.store(tool_name, content, tool_use_id="")
# -> None if below min_chars, else {
#   "handle": "<16-hex>", "excerpt": content[:300], "total_chars": N,
#   "total_lines": N, "tool": name,
# }

ObservationStore.recall(handle)      # memory first, then disk (rehydrates cache)
ObservationStore.get_stats()         # total_observations, chars archived/in-context, savings %
ObservationStore.clear_session()     # clear memory only; disk persists
```

## Storage layout

- In-memory `_OBSERVATION_CACHE: dict[handle -> entry]` — fast same-session recall
- Disk: `<storage_dir>/<handle>.json` — FULL entry including `content` key
  (excerpt alone would make read_file recall lie)
- `handle = sha256(content)[:16]` — deterministic, dedupes identical outputs
- `storage_dir` resolves from config (`~/.hermes/observations` default), `os.path.expanduser`

## In-context preview format (`_build_observation_preview`)

```
<observation>
Handle: 841a2d7c4cd689d2
Tool: search_files
Total: 1,500 chars (1.5 KB), 1 lines
Full content saved to: C:\Users\...\.hermes\observations\841a2d7c4cd689d2.json
Read with: read_file('C:\Users\...\.hermes\observations\841a2d7c4cd689d2.json')

Excerpt (first 300 chars):
<content head>
...
</observation>
```

Model recall contract: `read_file('<disk path>')`. NOT `recall_tool_result(handle)`
— that function is dev-facing; the model can only invoke registered tools.

Note: the disk file is JSON, not raw text. The `<observation>` preview should
include a hint like "JSON file — read the 'content' field" so the model knows
to extract it. This hint was still missing from `_build_observation_preview` as
of the last session (Sept 2026).

## Integration points

1. `maybe_persist_tool_result(content, tool_name, tool_use_id, env, config, threshold)`:
   - content <= threshold → still `ObservationStore.store()` (archive for recall),
     return content unchanged
   - content > threshold → archive + sandbox persist. If obs exists, return
     `<observation>` preview (primary format, ~400 chars). Falls back to legacy
     `<persisted-output>` only when obs is None (store failed).
   - if sandbox write fails AND obs exists → `<observation>` preview (replaces
     bare inline truncation)

2. `agent/context_compressor.py` `_demote_tool_result_at()`:
   - archive full content BEFORE replacing with 1-line summary
   - if content >= 5000 chars, append recall hint to summary:
     `[observation saved to ~/.hermes/observations/<handle>.json — use read_file to recall]`
   - whole block wrapped in try/except — archive failure must never crash pruning

3. `tools/tool_result_storage.enforce_turn_budget()`:
   - Must check BOTH `PERSISTED_OUTPUT_TAG` and `OBSERVATION_TAG` when
     determining which results are candidates for spill-to-disk. Missing the
     OBSERVATION_TAG check causes already-archived results to be re-persisted.

4. `hermes_cli/config_defaults.py` `DEFAULT_CONFIG["observation_store"]`:
   - enabled=True, min_chars=500, max_excerpt_chars=300,
     recall_hint_chars=5000, storage_dir="~/.hermes/observations"

## Config reader pattern (`_observation_config`)

Lazy global cache + try/except fallback to hardcoded defaults. Uses
`hermes_cli.config.cfg_get(loaded, "observation_store", "min_chars", default=500)`
and `load_config_readonly()`. Never raises into the archive path.
User config.yaml needs no manual edit — DEFAULT_CONFIG merge handles it.

## Test inventory (tests/test_observation_store.py, 10 cases)

- small content (< min_chars) → None
- large content archived; handle length 16; total_chars/tool correct
- recall from memory == full content
- cross-session recall from disk after clear_session
- disk file exists; contains excerpt AND full content
- preview format: has <observation> tag, handle, read_file hint, disk path, excerpt
- maybe_persist small unchanged
- maybe_persist large (threshold=0) truncated, mentions size
- stats computed with positive savings
- budget enforcement still returns list

Guard suites that must stay green when touching compression:
`test_context_compressor.py`, `test_proactive_tool_result_pruning.py`,
`test_ghost_skill_pruning.py`, `test_summarize_tool_result_type_safety.py`,
`tests/run_agent/test_proactive_prune_loop_wiring.py` — total 154 tests.

## Fixed bugs during build

1. `cls._OBSERVATION_CACHE` in classmethod → AttributeError. Module-level dict
   must be referenced by plain name inside classmethods.
2. Test asserted `content_len` key after switching disk entry to full `content` —
   update assertions when storage format changes.
3. `maybe_persist_tool_result` test with 5000 chars didn't persist: search_files
   threshold is 100K via budget_config. Force with `threshold=0`.
