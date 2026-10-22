---
name: hermes-core-token-efficiency
description: "Use when cutting Hermes token spend via core internals."
category: software-development
---

# Hermes Core Token Efficiency

How to reduce token usage by working INSIDE the Hermes agent source
(`~/AppData/Local/hermes/hermes-agent/`), not just by config. Covers the
internals map, the ObservationStore pattern, deterministic compression hooks,
and how to test core changes safely.

## When to use

- User reports high token usage and config tuning alone is insufficient
- Need to archive large tool outputs out of context automatically
- Need deterministic (no-LLM) compression before LLM summarization
- Any task touching `tool_result_storage.py`, `context_compressor.py`,
  `budget_config.py`, or `config_defaults.py`

## Internals map (where the token-waste levers live)

| File | Role |
|------|------|
| `tools/tool_result_storage.py` | 4-layer persistence: per-tool cap, ObservationStore archive, sandbox persist, per-turn budget (`enforce_turn_budget`) |
| `tools/budget_config.py` | Thresholds: `DEFAULT_RESULT_SIZE_CHARS=100K`, `DEFAULT_TURN_BUDGET_CHARS=200K`, `PINNED_THRESHOLDS` (read_file=inf), `BudgetConfig.resolve_threshold()` |
| `agent/context_compressor.py` | Full compression pipeline; `_prune_old_tool_results()` = deterministic pre-pass (dedup + summarize + arg truncate), `prune_tool_results_only()` = cost-oriented no-LLM prune |
| `agent/context_engine.py` | Compaction / subtask boundary logic |
| `hermes_cli/config_defaults.py` | `DEFAULT_CONFIG` dict — new feature blocks register here |
| `hermes_cli/config.py` | `cfg_get(cfg, *keys, default)` for safe nested reads; `load_config_readonly()` |

Key entry point: `agent/tool_executor.py` calls `maybe_persist_tool_result()`
and `enforce_turn_budget()` after every tool run — that is the chokepoint where
all tool output passes before entering context.

## Core-extension patterns

### 1. ObservationStore (archive tool output, recall via read_file)

Pattern validated in production: when archiving tool output OUT of context so the
model can fetch it later, the recall surface must be an EXISTING registered tool
(`read_file`), never a new Python function — the model cannot call arbitrary
functions. So: write full content to disk (`~/.hermes/observations/<sha16>.json`),
keep handle + excerpt + disk path in context, model recalls with
`read_file('<disk path>')`.

```python
handle = hashlib.sha256(content.encode()).hexdigest()[:16]
# store full content on disk: <storage_dir>/<handle>.json
# in-context preview: <observation> handle / excerpt / total / disk path </observation>
```

### 2. Deterministic pre-compression hook

In `context_compressor._demote_tool_result_at()`: archive the full content into
ObservationStore BEFORE replacing it with the 1-line summary, and append a recall
hint only for genuinely large outputs (>=5000 chars) to keep summaries compact.
Wrap the archive call in try/except — archiving must never crash pruning.

### 3. Config-aware feature blocks

New feature = new block in `config_defaults.DEFAULT_CONFIG` + lazy reader in the
feature module with try/except fallback to hardcoded defaults (avoids circular
imports and never breaks the feature on config read failure):

```python
def _observation_config() -> dict:
    global _CACHE
    if _CACHE is not None: return _CACHE
    try:
        from hermes_cli.config import cfg_get, load_config_readonly
        loaded = load_config_readonly()
        _CACHE = {"enabled": cfg_get(loaded, "observation_store", "enabled", default=True), ...}
    except Exception:
        _CACHE = {defaults...}
    return _CACHE
```

User config.yaml needs NO manual edit — defaults merge automatically (verified).

## Testing core changes

- pytest is dev-only (`pyproject.toml [dev]`), NOT in the runtime venv. Install to a
  scratch dir: `python -m pip install pytest==9.1.1 --target ./_testdeps`
- Run: `python -c "import sys; sys.path.insert(0,'.'); sys.path.insert(0,'./_testdeps'); import pytest; pytest.main(['tests/...', '-q', '--no-header', '-p', 'no:cacheprovider'])"`
- Clean up `_testdeps/` after (it's a scratch dir, not part of the repo).
- Before touching compression code, run the guard suites: `test_context_compressor.py`,
  `test_proactive_tool_result_pruning.py`, `test_ghost_skill_pruning.py`,
  `test_summarize_tool_result_type_safety.py`, `tests/run_agent/test_proactive_prune_loop_wiring.py`.

## Pitfalls

- **Do NOT use `./venv/Scripts/python.exe` in commands** — Hermes's own lifecycle
  guard can throw `ValueError: open: embedded null character in path` on venv paths
  under git-bash. Use the system `python` + `sys.path.insert` instead.
- **`cls._MODULE_LEVEL_DICT` in a classmethod raises AttributeError.** If the cache
  dict is module-level, reference it by its module-level name directly, not via `cls.`.
- **`maybe_persist_tool_result` respects per-tool thresholds** (registry / budget_config).
  To force persistence in tests pass `threshold=0`. Content below the tool's threshold
  is returned unchanged even if it would otherwise be archived.
- **Compression tests pin exact summary strings** (e.g. `summary == "[skill_view] name=docker (1,234 chars)"`).
  Appending to summaries unconditionally breaks them — gate additions behind a size
  threshold and use `startswith`-safe placement.
- Disk store must include FULL content (not just excerpt) or `read_file` recall lies.
- **Observation preview is PRIMARY (not fallback)**: `maybe_persist_tool_result`
  returns `<observation>` tag when obs exists — legacy `<persisted-output>` only
  fires when ObservationStore.store() fails (obs is None). Sandbox persist
  (`env.execute`) still runs for remote backends but the in-context preview is
  always the compact observation format.
- **`enforce_turn_budget` must check both tags**: the candidates loop at line 471
  filters on `PERSISTED_OUTPUT_TAG not in content and OBSERVATION_TAG not in content`.
  Missing OBSERVATION_TAG causes double-persist.
- **The JSON file note**: the disk file is JSON (`{"content": "...", ...}`), not raw
  text. The `<observation>` preview should hint this so the model knows to extract
  the `content` field from the JSON after read_file.

## TODO — next session

- `_build_observation_preview()` in `tool_result_storage.py`: add one line
  `"The file is JSON — read the 'content' field."` to the preview block so the
  model knows to extract `content` from the JSON after read_file.
- Remove `_ensure_dir()`, `_store_path()`, and `_OBSERVATION_AUTO_TAG` from
  `ObservationStore` class — they are vestigial since `_storage_dir()` and
  `_observation_config()` replaced them.

## References

- `references/observation-store-impl.md` — full implementation detail from the
  production build (store/recall/stats API, preview format, test inventory).
