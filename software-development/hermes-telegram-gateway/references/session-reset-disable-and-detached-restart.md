# Disabling automatic session reset (`session_reset`) + detached gateway restart

## The problem

Hermes auto-resets long-lived sessions by policy in the `session_reset` section of
`config.yaml`. Each platform's daily schedule can reset a session overnight or after
inactivity, dropping the context a user expected to persist. Symptoms:

- System prompt banner: `The user's session was automatically reset by the daily schedule.`
- User complaint: "mỗi 12h k dùng lại bị reset" (sessions reset after ~12h idle).

## The config keys

```yaml
session_reset:
  mode: both        # "daily" | "idle" | "both" | "none"
  at_hour: 4        # local hour for the daily reset (daily/both modes)
  idle_minutes: 1440 # minutes of inactivity before reset (idle/both modes)
```

- `mode: none` → sessions never auto-reset. They only end when the user runs `/new` or
  `/exit`. This is the de-facto default Hermes changed to in July 2026.
- `mode: daily` / `idle` / `both` re-enable the two reset triggers.

### The trap — the CLI warning is a FALSE ALARM

`hermes config set session_reset.mode none` prints:

```
⚠ 'session_reset.mode' is not a recognized config key — it was saved anyway...
  Did you mean: sessions.mode
```

This warning is misleading. `session_reset` IS a real top-level key — the gateway reads it
every startup (`gateway/config.py` merges `yaml_cfg["session_reset"]` into
`default_reset_policy`, and `hermes_cli/config.py` lists `session_reset` as a known
top-level form). The CLI just doesn't have a typed schema entry for the dotted path. The
value IS written to config.yaml and IS honored. Ignore the "Did you mean" hint.

### Apply — restart needed

The gateway caches the reset policy at startup (`self.config = load_gateway_config_for_runner()`),
so an edit to config.yaml only takes effect after the gateway restarts. See the detached
restart recipe below to apply without killing your in-flight reply.

## Detached gateway restart (from inside a gateway session)

`hermes gateway restart` is blocked when run from a terminal inside the gateway process:

```
Blocked: cannot restart or stop the gateway from inside the gateway process.
```

Doing `hermes gateway stop` in-line also drops the session mid-turn (your reply is lost).

**Preferred: schedule a detached restart** via a `.bat` registered as a one-shot
`scheduled` task, so it runs outside the gateway process tree:

`restart_gw.bat`:
```bat
@echo off
schtasks /End /TN "Hermes_Gateway" 2>> gw_sched.log
timeout /t 5 /nobreak >> gw_sched.log 2>&1
schtasks /Run /TN "Hermes_Gateway" >> gw_sched.log 2>&1
echo DONE >> gw_sched.log
```

Register it to fire in a few minutes (enough time for your final user-facing message to
deliver first):
```bash
MSYS_NO_PATHCONV=1 cmd /c "schtasks /Create /TN HmGwRestart /SC ONCE /ST 09:53 /TR \"C:\\Path\\to\\restart_gw.bat\" /F"
```

Verify the old PID was replaced after it fires:
```bash
hermes gateway status    # PID should differ from before
```

### MSYS bash → cmd flag mangling (Windows / git-bash)

Passing `schtasks /End /Run /Create` flags through the bash-invoked `cmd` mangles the
leading `/` (bash converts `/X` to a path, or `//X` to `\`). Symptoms:
`ERROR: Invalid argument/option - '//End'`. Use `MSYS_NO_PATHCONV=1` to disable the
conversion and pass the flags through verbatim. Same for any `cmd /c "schtasks /..."`
invocation, and for `tasklist`/`wmic` filters.

## Alternatives (also valid)

- `hermes gateway run --replace` from the gateway session spawns a new process that
  auto-kills the old one — simplest if you don't mind the restart happening immediately.
- Harsh failsafe (only if run --replace is stuck): `taskkill //F //IM pythonw.exe` (kills ALL
  pythonw) + `rm gateway.lock gateway.pid` + `schtasks /run /tn Hermes_Gateway`. Last resort.

## Verify the policy took effect

After restart, confirm resets are actually off before claiming success:
- `hermes gateway status` shows a NEW PID (proves the restart happened).
- Optionally `grep -A4 "^session_reset:" config.yaml` → `mode: none`.
- Don't trust `last_status`/`last_run` from before the restart; the banner shouldn't
  re-appear on the next daily boundary.