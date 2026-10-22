# Case Study: Hermes Gateway + Provider Troubleshooting

When Telegram (or other gateway platforms) report "provider có vấn đề" (provider has issues), follow this systematic diagnostic flow.

## The Pattern

**Symptom**: Gateway platform reports provider errors / "provider has issues" / silent failures

**Root cause (most common)**: A corrupted session with mismatched tool_calls/tool_results messages causes the LLM provider (especially DeepSeek via OpenCode Go) to return a 400 error:

```
HTTP 400: Error from provider (DeepSeek): An assistant message with 'tool_calls' 
must be followed by tool messages responding to each 'tool_call_id'.
```

## Diagnostic Flow

### Step 1: Check gateway status
```bash
hermes gateway status
```

### Step 2: Run hermes doctor
```bash
hermes doctor
hermes status --all
```

### Step 3: Search logs for the real error
```bash
# Gateway logs — connection issues, provider errors
grep -i "error\|provider\|DeepSeek\|400\|timeout" ~/AppData/Local/hermes/logs/gateway.log | tail-40

# Errors log — tool execution failures
grep -i "error\|provider\|400\|tool_calls" ~/AppData/Local/hermes/logs/errors.log | tail-40

# Agent log — API call details
grep -i "provider\|422\|401\|403\|429\|timeout\|deepseek" ~/AppData/Local/hermes/logs/agent.log | tail-40
```

Windows path: `/c/Users/<USER>/AppData/Local/hermes/logs/`

### Step 4: Identify the corrupted session

The session ID appears in the error log entry, e.g.:
```
[20260629_195228_4260386f] agent.conversation_loop: API call failed...
```

### Step 5: Fix sequence

1. **Stop the gateway** first (especially on Windows — otherwise `config migrate` fails with PermissionError):
```bash
hermes gateway stop
```

2. **Delete the corrupted session**:
```bash
hermes sessions delete <CORRUPTED_SESSION_ID>
```

3. **Migrate config** (optional, if doctor reports outdated config):
```bash
hermes config migrate
```

4. **Restart gateway**:
```bash
hermes gateway start
```

## Windows-Specific Quirks

- `hermes config migrate` fails with `PermissionError: [WinError 5] Access is denied` when the gateway is running — the gateway process holds a lock on `config.yaml`. Always `hermes gateway stop` before migrating.
- The corrupted session may auto-disappear after `gateway stop` — if `sessions delete` returns "not found", that's normal.
- Use POSIX-style paths in bash: `/c/Users/...` not `C:\Users\...`

## Telegram Network Issues (Vietnam)

If Telegram frequently shows read timeout / connection failures:
```
Timed out → ReadTimeout → api.telegram.org connection failed
```

Configure a SOCKS5 proxy in `.env`:
```
TELEGRAM_PROXY=socks5://127.0.0.1:1080
```
Then restart gateway.

## Prevention

- The corrupted session typically results from a tool_calls/tool_results alternation failure during a gateway session. This can happen when the LLM produces tool calls but the session state is interrupted (e.g. network issue, manual kill).
- If a session keeps recurring with the same error, delete it proactively.
