# Fresh Hermes Git-Install on Windows — Full Setup (2026-09)

Case study: lqremote.thefirstonly.com — Windows Server, Hermes v0.21.5 (git install).

## Timeline

1. Enabled OpenSSH Server on Windows (PowerShell Admin)
2. Forwarded port 22 on router
3. Connected via paramiko SSH (user `Admin`, password `<PASSWORD>`)
4. Found Hermes home at `C:\Users\Admin\AppData\Local\hermes`
5. Found `.env.txt` instead of `.env` → renamed to `.env`
6. Gateway was running but model returned 401 "API key format is incorrect"
7. Fixed by switching `key_env: BYTEDANCE_ARK_API_KEY` → `api_key: <key>` directly
8. Enabled `platforms.telegram.enabled: true`
9. Restarted gateway → Telegram auto-connected
10. Verified: `hermes -z "say hi"` → "Hi there."

## Key Findings

### `.env` encoding matters
- PowerShell `Set-Content -Encoding UTF8` adds BOM → Hermes reads key with extra bytes
- Fix: use `StreamWriter` with `new UTF8Encoding($false)`

### `key_env` vs `api_key` for ByteDance Ark coding plan
- `key_env` works with standard `ark-*` keys but fails (401) with coding plan JWT keys (`VxCg...`)
- Workaround: put `api_key:` directly in `custom_providers` entry
- See the main SKILL.md for full pitfall details

### Telegram auto-installs on restart
- `hermes plugins install telegram` fails (catalog name is `hermes-telegram` or internal)
- Gateway auto-detects missing plugin and installs it on restart when `platforms.telegram.enabled: true`

### Network setup for remote management
- Windows firewall: `netsh advfirewall firewall add rule name="OpenSSH" dir=in action=allow protocol=TCP localport=22 profile=any`
- Router: forward port 22 to the machine's internal IP
- If network is "Public", WinRM firewall exception will fail — use SSH instead
