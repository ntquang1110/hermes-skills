# Windows-Specific Quirks

Hermes runs natively on Windows (PowerShell, cmd, Windows Terminal, git-bash
mintty, VS Code integrated terminal). Most of it just works, but a handful
of differences between Win32 and POSIX have bitten us — document new ones
here as you hit them so the next person (or the next session) doesn't
rediscover them from scratch.

### Input / Keybindings

**Alt+Enter doesn't insert a newline** — Windows Terminal (and mintty) grab it
for fullscreen before prompt_toolkit sees it. Use **Ctrl+Enter** instead (the
CLI binds it to newline on Windows; raw Ctrl+J does the same, harmlessly).
To inspect how your terminal reports a keystroke, run
`python scripts/keystroke_diagnostic.py` from the repo root.

### Config / Files

**HTTP 400 "No models provided" on first run** — `config.yaml` was saved with
a UTF-8 BOM (Notepad does this). Re-save as UTF-8 without BOM;
`hermes config edit` writes correctly.

### `execute_code` / Sandbox

**WinError 10106** from the sandbox child process — it can't create an
`AF_INET` socket. Root cause is usually Hermes's env scrubber dropping
`SYSTEMROOT`/`WINDIR`/`COMSPEC` (Python's `socket` needs `SYSTEMROOT` to find
`mswsock.dll`), not a broken Winsock LSP. The `_WINDOWS_ESSENTIAL_ENV_VARS`
allowlist in `tools/code_execution_tool.py` covers it; if you still hit it,
echo `os.environ` inside an `execute_code` block to confirm `SYSTEMROOT` is set.

### Testing on Windows

`scripts/run_tests.sh` is POSIX-only (expects `.venv/bin/activate`); the
Hermes-installed `venv/Scripts/` has no pip/pytest (stripped for size).
Install pytest into a system Python and run directly (the repo no longer
uses pytest-xdist; the canonical runner does per-file subprocess isolation,
which the POSIX-only wrapper handles):

```bash
"/c/Program Files/Python311/python" -m pip install --user pytest pyyaml
export PYTHONPATH="$(pwd)"
"/c/Program Files/Python311/python" -m pytest tests/foo/test_bar.py -v --tb=short
```

(POSIX-only tests need skip guards — see the cross-platform guard list in
`references/contributor-guide.md`.)

### Path / Filesystem

**Line endings.** Git may warn `LF will be replaced by CRLF`. Cosmetic — the
repo's `.gitattributes` normalizes. Don't let editors auto-convert committed
POSIX-newline files to CRLF.

**Forward slashes work almost everywhere.** `C:/Users/...` is accepted by
every Hermes tool and most Windows APIs. Prefer forward slashes in code
and logs — avoids shell-escaping backslashes in bash.

### Terminal command guard (git-bash + cron lifecycle_guard)

Occasionally a `terminal`/`execute_code` command dies with
`ValueError: open: embedded null character in path` wrapped inside
`cron/lifecycle_guard.py` — **before the command runs** — and the guard is
non-deterministic (the same command shape sometimes succeeds). It triggers
when the guard's `_iter_referenced_shell_scripts` treats a command token as a
"referenced script" and scans it: any executable token containing `/` (e.g. a
full path to `python.exe`) is yield-and-read, and a raw Windows path
(`D:\Hermes Proj\...`) tokenized inside a scanned `.py` source can produce a
NUL-byte path that crashes `os.open` (only `OSError` is caught, not
`ValueError`). Workarounds, in order of reliability:

- **Use bare `python`** instead of the full venv path. On Quang's host bare
  `python` resolves to the hermes venv, and the bare token (no `/`) is not
  scanned as a script — commands run cleanly.
- **Keep raw backslash Windows paths out of scanned `.py` files** — use
  forward slashes (`D:/Hermes Proj/...`) or `Path.home()`.
- Run long logic through `execute_code` (its `terminal()` helper returns
  `exit -1` on the crash instead of surfacing the guard traceback).
- Retrying a few times sometimes slips past the non-determinism.

