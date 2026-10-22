#!/usr/bin/env python3
"""Launch threads_poster.py DETACHED so no agent-tool timeout kills it.

Use from a cron agent that must auto-post long Threads reply chains. A direct
synchronous `terminal` call to threads_poster.py gets cut when the tool's
foreground timeout (~125s) hits mid-lanuch of headless Chromium, so the agent
retries endlessly ("stop at 125s, called repeatedly").

This helper spawns the poster as a child process (non-blocking, no timeout),
writes its stdout to a log, and returns instantly with "DETACHED pid=...".
The agent then POLLS the log until it sees "Done! N posts." (success) or
"Session expired" (needs re-login). Never blocks a single tool call.

Usage:
  python threads_auto_post.py --file <draft.txt> [--log <logfile>]

Success signal in log:  contains both
  "Posted! URL: https://www.threads.com/..."
  "Done! N posts."
"""
import subprocess, sys, os

VENV_PY = os.path.expanduser(r"~\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe")
POSTER = os.path.expanduser(r"~\AppData\Local\hermes\scripts\threads_poster.py")
DEFAULT_LOG = os.path.expanduser(r"~\AppData\Local\hermes\cache\auto_post_log.txt")


def main():
    args = sys.argv[1:]
    if "--file" not in args:
        print("Need --file <draft.txt>", file=sys.stderr); sys.exit(1)
    draft = args[args.index("--file") + 1]
    log = DEFAULT_LOG
    if "--log" in args:
        log = args[args.index("--log") + 1]

    if not os.path.exists(POSTER):
        print(f"POSTER NOT FOUND: {POSTER}", file=sys.stderr); sys.exit(1)
    if not os.path.exists(draft):
        print(f"DRAFT NOT FOUND: {draft}", file=sys.stderr); sys.exit(1)

    with open(log, "w", encoding="utf-8") as f:  # truncate previous run
        f.write("")
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    logh = open(log, "a", encoding="utf-8", buffering=1)
    proc = subprocess.Popen(
        [VENV_PY, POSTER, "--file", draft],
        stdout=logh, stderr=subprocess.STDOUT, creationflags=flags,
    )
    print(f"DETACHED pid={proc.pid} running -> log={log}")


if __name__ == "__main__":
    main()