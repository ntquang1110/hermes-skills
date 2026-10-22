---
name: web-app-security-review
description: "Security review of web apps: threat model, OWASP, secrets."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [security, web-app, owasp, threat-modeling, defensive, code-review, secrets, browser-profile]
    related_skills: [requesting-code-review, web-passcode-gate, system-design-workflow]
---

# Web App Security Review (Defensive)

Use when a web app is going live, is live, or changed its auth/session/data handling and needs a security pass. **Defensive only**: identify and fix weaknesses in systems you own or have explicit permission to test. No offensive/exploit tooling, no running metasploit/sqlmap/etc.

## Authorization guard (always first)

- Only review systems you own or have written permission to test.
- If scope is unclear, ask before scanning anything outside your own codebase.
- Never touch profiles/accounts/data you do not own. Use a throwaway account and a dedicated browser profile.

## Threat model (lightweight, STRIDE-lite)

Map the surface in ~10 minutes before reading code:

1. **Assets**: what is valuable? (customer PII, orders/payments, credentials, admin actions, uploads)
2. **Entry points**: every place untrusted input enters (login, signup, search, upload, webhook, import, payment callback, API params, headers)
3. **Trust boundaries**: where data crosses from untrusted (user) to trusted (DB/admin/filesystem)
4. **Actors**: anonymous, logged-in user, admin, partner integration
5. **Worst-case impact per entry point**: leak, account takeover, auth bypass, RCE, defacement

Output a one-page table: Entry point | Input | Asset at risk | Worst-case | Priority.
P0 = exploitable from the internet with real damage, fix now. P1 = needs auth but real risk. P2 = hardening.

## Code-pass: static checks

### Secrets in code (P0)
```bash
grep -rniE "(api[_-]?key|secret|password|passwd|token|sk-|ghp_|AKIA)\s*[:=]\s*['\"][A-Za-z0-9_\-/+=]{12,}['\"]" --include=*.{js,ts,py,json,env,yml,yaml,html} .
```
If found: rotate the secret, remove from code, move to env/backend secret store, gitignore it. Never put API keys or customer data into prompts, logs, or page inputs.

### Injection (P0)
- SQL: `execute(f"...")` / string-concat queries → parameterized/prepared statements.
- Shell: `os.system`, `child_process.exec` with user input → argument arrays.
- `eval`/`exec` with user input → block.

### XSS (P0)
- `innerHTML`, `v-html`, `dangerouslySetInnerHTML` with renderable user data → use textContent / an escaping render path.
- Verify CSP is set (see headers below).

### Path traversal / unsafe file ops (P0)
- User-controlled paths/names → validate extension and resolved path stays under an allowed dir; block `..`, absolute paths, symlinks.

### Authentication & session (P0/P1)
- Passwords hashed with bcrypt/argon2 (never MD5/SHA1 plain).
- Session tokens: random, HttpOnly, Secure, SameSite, short expiry, rotated on login; server-side for sensitive apps; logout invalidates.
- MFA enforced for admin.
- JWT: strong env secret, pinned algorithm (HS256/RS256, never `none`), short expiry, audience/issuer validated.

### Authorization (P1)
- Every protected endpoint checks the caller's role, not only "is logged in".
- IDOR: user A cannot read/act on user B's resource by id.
- Admin routes behind a real role check, not just hidden UI.

### App hardening (P2)
- Rate limiting on login/OTP/import endpoints.
- Server-side input validation on all fields (length, type, allowlist).
- Uploads: type + size limits, stored outside web root, served with attachment disposition.
- Errors: do not leak stack traces / DB schema to clients.
- TLS everywhere; HSTS.

### Security headers (P2)
```
Strict-Transport-Security, X-Content-Type-Options: nosniff,
X-Frame-Options: DENY (or CSP frame-ancestors), Referrer-Policy,
Content-Security-Policy (default-src 'self'; script-src 'self')
```
Verify via `curl -sI <public-origin>`.

## Browser / agent profile safety

- Use a dedicated agent browser profile, never the primary profile that holds email/banking/password manager.
- Log in only the accounts the task needs.
- Require explicit human approval before any send (email/post/DM), delete, purchase, or payment.
- Never paste API keys, customer PII, or private data into prompts or logs.

## Verification

- Re-scan after fixes; confirm the original finding is gone (header present via curl, secret absent from grep, injection removed).
- Report evidence: exact file:line per finding, exact command output confirming the fix.
- Deliver a list with priority, file:line, impact, and concrete fix. No "maybe fixed" — verify the artifact.

## Pitfalls

- Skipping the authorization guard → you audit a system you don't own. Stop and ask.
- Only checking "is user logged in" → misses IDOR/privilege escalation. Check role per endpoint.
- Committed `.env` with secrets still counts as P0 even if not in source files; check git history.
- Trusting client-side validation only → always validate server-side.
- Offensive tooling is NOT part of this defensive skill. Do not load/run it.