---
name: self-hosted-web-apps
description: "Use when building a self-contained web app (Node+JSON+SPA)."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [webapp, node, fullstack, json-store, spa, cloudflare-tunnel, exam]
    related_skills: [cloudflare-tunnel, design-critique, html-interactive-dashboard]
---

# Self-Hosted Web Apps (Node + JSON + SPA + Tunnel)

Build complete, self-contained web applications on the user's Windows machine: a
pure-Node HTTP server with a JSON-file data store, a vanilla HTML/JS SPA frontend,
and public exposure through a Cloudflare tunnel. No framework, no DB server, no
build step. This is the stack for "app thi", TFO-style tools, upload services, etc.

**Trigger:** user asks for a tool/app with a real backend (auth, state, scoring,
admin view, exports) that will be served locally and accessed remotely via a
subdomain of thefirstonly.com / theliems.com / kiemion.online.

## Architecture

```
Browser ──HTTPS──→ Cloudflare tunnel ──→ localhost:PORT (Node http server)
                                               │
                                               ├── /public/*  static HTML/JS/CSS
                                               ├── /api/*     JSON endpoints
                                               └── data/*.json (persistence)
```

- **Server**: single `server.js`, Node built-in `http` module. No Express needed —
  a `routes` array + `readBody()` promise + MIME map for static files is enough.
- **Storage**: JSON files in `data/`, rewritten with `fs.writeFileSync` after each
  mutation. Atomic enough for single-process apps; 30-100 users is fine.
- **Excel export**: `exceljs` npm package (pure JS, no native deps). `npm i exceljs`.
- **Deploy**: Cloudflare tunnel, API-managed ingress (see `cloudflare-tunnel` skill
  + its `scripts/add-cf-ingress.py` / `scripts/add-cf-dns.py`).

## Exam-app patterns (proven)

For timed multiple-choice exams with unique paper assignment:

1. **Pre-generate N unique papers at startup.** Each paper = fixed question count per
   teacher/category ratio. Shuffle answer options per question but track the CORRECT
   index after shuffling. Dedup by a signature (sorted qids joined with comma); retry
   generation until N unique papers exist (loop with a cap, e.g. 200 attempts).
2. **Assign next unused paper on entry** — track used exam_ids in a Set, pick the
   first free one → guarantees no two people get the same paper.
3. **Server-enforced deadline — NEVER trust the client countdown.** Every save/submit/
   overview request calls `enforceDeadline(c)`: if `now > started_at + duration`, mark
   `submitted`, set `submitted_at = deadline`, `auto = true`, compute score from saved
   answers. The client countdown is UX only.
4. **Session resume via localStorage.** On enter, server returns a random token; client
   stores token+STT in localStorage. Boot flow calls `/api/enter` with the saved token;
   server returns current state (assigned / in_progress with remaining_ms / submitted).
   On refresh/mid-exam drop, the candidate resumes where they left off.
5. **Single-use identifier locking.** STT already `submitted` → reject permanently.
   STT `in_progress` by another token → reject. STT `assigned` but younger than N
   minutes → reject (others can't steal). Older than N → release, reassign.
6. **Score computed server-side only.** Candidate sees only "chúc mừng hoàn thành",
   never the score. Admin API returns score + per-question detail.
7. **Admin:** token from password login, stored in localStorage, sent as
   `Authorization: Bearer`. Overview poll every 5s (simple `setInterval`). Export
   endpoint streams `.xlsx` with `Content-Disposition: attachment`.

## Design direction (user-approved, dithi emerald theme)

When the user asks to make an app look "tech" or picks a color direction, this is the
approved look for the dithi/contest family (white base + emerald + tech font):

- **Palette (emerald):** bg `#f2f7f5`, surface `#fff`, accent `#0f9d76` (hover `#0b7a5c`),
  deep text `#0f2e26`, muted `#5c6f69`, border `#dce8e3`, soft accent `#e6f4ef` /
  line `#cfe6dd`. Success `#16a34a`, danger `#dc2626`, warn `#d97706`.
  Overrides the AI-default blue (`#2563eb` + `#eff6ff`) that the first build shipped with.
- **Fonts:** display voice = Google Fonts **Space Grotesk** (timer, KPI numbers, headings,
  brand) + body = `system-ui` stack. Add the Google Fonts `<link>` in `<head>`;
  offline users fall back to system-ui gracefully.
- **Icons:** inline SVG, 1 stroke (`stroke-width≈1.8-2`), NOT emoji. Logo shield, clock,
  check-circle, download, refresh. Replaces the 📝⏱️🎉📊⬇ emoji of the first build.
- **Radius ramp:** 8 / 12 / 16 px only; pill (999px) reserved for small badges/controls.
- **Tech details:** `font-variant-numeric: tabular-nums` on timer/scores; sticky timer
  header with a thin 3px progress bar that turns red under 5 min; focus ring
  `box-shadow: 0 0 0 3px rgba(15,157,118,.12)`; table header uppercase + letter-spacing.
- **Semantic headings:** brand/title as real `<h1>`, not a styled `<span>` — fixes the
  `flat-type-hierarchy` AI-tell and improves the detector result.

**Verification:** after the redesign, run the impeccable `ui-audit.js` detector in the
browser (browser_console with the script from the `impeccable` skill). Target: `tells: []`,
fonts show a display face (not system-only), radii on the ramp. Contrast target ≥ 4.5
(emerald build measured 13.48 on body). Fix one batch, re-check once, then stop
(bounded passes).

## Pitfalls (all hit in real sessions)

- **SPA render() that replaces the whole `app.innerHTML` destroys the layout.**
  If `render(html)` wipes the container, calling it from a per-question update kills
  the timer, nav buttons and submit button (they're siblings of the card being
  re-rendered). Fix: render the static skeleton ONCE, then update only the
  sub-container (`document.getElementById('qcard').innerHTML = ...`). Always re-bind
  event handlers after innerHTML changes. Symptom seen: after answering one question,
  the countdown/nav/submit disappear from the snapshot.
- **JSON state lives in RAM; editing the file while the server runs gets overwritten.**
  `writeJson` happens on every mutation (including admin login!). To patch a
  contestant's `started_at` for testing: kill the server → edit `data/state.json` →
  restart. Patching the file while the server runs silently reverts on the next
  persist (observed: auto-submit test showed "in_progress" after patching the file).
- **Route ordering when you add an auth gate to a Node http server (email+passcode
  cookie auth — see `web-passcode-gate`).** Two live bugs hit in one build (COA app):
  1. **Serve public static + public API BEFORE the auth gate.** Put `/login.html`,
     public viewers, and any no-auth API (e.g. a public `/api/coa/:id` share-link)
     at the TOP of the handler, then the gate (`if (p.startsWith('/api/') &&
     !isAuthed()) return 401`), then authed routes. Naively gating ALL `/api/*`
     first silently kills the public API routes the user explicitly wants open —
     got `ok:false, 401` on a public COA link the user wanted password-free.
  2. **Do NOT put a global catch-all `if (!m) { 404 }` BEFORE the static-fallback
     serve.** If you match API routes with a regex and 404 on no-match, then
     `coa.js` (not matching that regex) hits the 404 and the public static JS never
     serves ("coa.js: 404" while `coa.html` returns 200). Correct order: public
     static → public API → auth gate → authed API → static fallback at the very end.
  3. **UTF-8 payloads over bash curl get mangled (accented text → `Dung d?ch`).**
     git-bash is not UTF-8-clean for `-d '{"name":"Dung dịch..."}'`. For API tests
     that must preserve Vietnamese diacritics, POST via Python `urllib.request`
     (encode body `.encode('utf-8')` + header `Content-Type: application/json`)
     instead of `curl -d`. Verify stored JSON with `json.load` + `repr()` before
     trusting a test — a valid login response proves the gate works, but mangled
     storage means the TEST harness is at fault, not the app.
- **Quoted heredocs (`<<'PYEOF'`) do NOT expand shell variables.** `TOKEN_PLACEHOLDER`
  inside a quoted heredoc stays literally. Write a real `.py` file and pass secrets
  via env: `export CF_TOKEN=$(...) ; python script.py`. Passing token through
  `urllib` + `Authorization: Bearer` header works; a literal placeholder → HTTP 400.
- **The hermes venv python has NO pip** (`No module named pip`). Use
  `uv run --with openpyxl python script.py` for one-off xlsx/json tooling instead of
  `pip install`.
- **Background server on Windows:** start with `terminal(background=true)`, verify
  with a health curl, and tell the user the server dies on reboot (give the exact
  restart command). `netstat -ano | grep :PORT | grep LISTEN` confirms the port.
  If the PID from netstat doesn't match the PID you started (bash wrapper vs. the
  real node/python child), disambiguate with:
  `cmd.exe /c "wmic process where processid=<PID> get processid,commandline"`.
  Multiple old watch-pattern notifications from killed background servers are stale
  logs — re-check `grep -c LISTEN` and keep only one real listener.
- **curl on Windows does NOT read MSYS paths (`/d/`, `/tmp/`).** `curl -F
  "file=@/d/foo.bin"` fails with `curl: (26) Failed to open/read local data from
  file/application` and `HTTP:000 time:0.000s` — which looks exactly like a dead
  server but is a client path problem. Always use `D:/foo.bin` style for curl -F
  and file args on this host. Rule out path/exit-26 BEFORE blaming the server.
- **Large-file upload servers need streaming receive, not read-all-into-RAM.**
  For endpoints that accept big uploads (audio, exports): read the body in chunks
  sized by remaining `Content-Length`, never a fixed `read(65536)` — on
  HTTP/1.1 keep-alive the socket never EOFs, so a fixed-size read blocks forever
  when the remaining body is smaller than the buffer (symptom: file written
  completely, but response never arrives; curl times out; server logs
  `ConnectionAbortedError: [WinError 10053]`). Python recipe:
  `left = content_length - read_total; chunk = rfile.read(min(65536, left))`,
  then drain the leftover closing-boundary bytes so the response isn't mixed
  with body remnants. Also switch to `ThreadingHTTPServer` so one big upload
  doesn't block the whole server, and report REAL progress in the browser via
  `XMLHttpRequest` `upload.onprogress` (fetch has no upload events) — fake
  progress bars mislead users about actual throughput.
- **Bandwidth is a physical constraint; don't promise to "remove" it.** When a
  user reports slow uploads (e.g. 100kb/s), the bottleneck is usually their
  uplink, not the server. Verify with a local-host upload test + a tunnel upload
  test with `-w "speed_upload"` before concluding. The code-side fix is reducing
  bytes sent (client-side compression) or making the receiver robust (streaming,
  resume), never "removing the bandwidth limit".
- **Refactoring the JSON model breaks public/*.js that reads the API — update BOTH
  in one change.** When you reshape the store (add a tier, rename a field, change
  an array's name — e.g. to support products+companies, `data.indicators` became
  `products` with nested `indicators`), every `public/*.js` client that consumed
  the OLD shape silently breaks: the page renders an empty table or throws
  (`data.indicators` undefined) while the API itself responds fine (200 + correct
  JSON). Symptom is a page that worked before a model upgrade and now fails, with
  the API looking healthy. Do a source scan of `public/*.js` for every field the
  API view hooked the client on (`grep -n "data\.\w\+" public/*.js`), patch the
  consumers, and re-verify the exact public viewer/URL the user quoted. Also: the
  static JS that served a cached OLD version won't pick up the fix if the edge
  cached that path — rename the asset (`coa.js` -> `coa-app.js`) + update the
  `<script src>` reference + add the new name to the server static allow-list
  (see `cloudflare-tunnel` skill "edge caches 404s — rename asset to bust").

## Verification ritual (do this before reporting done)

1. `node --check server.js` after edits.
2. curl every API endpoint: enter → start → save → submit → re-submit (must be
   rejected) → admin login (wrong + right password) → overview → detail → export.
3. Auto-submit test: stop server, patch `started_at` to 51 min ago, start server,
   call overview → row must flip to `submitted auto:true`.
4. Browser flow test via tunnel URL: enter STT → ready page → start → answer → nav →
   submit confirm modal → done page (no score shown).
5. Verify xlsx by reopening with openpyxl (`uv run --with openpyxl`).
6. Tunnel: local curl 200 → tunnel curl 200 (may need retry loop for DNS, 1-5 min).

## Deploy checklist

1. `scripts/add-cf-ingress.py <ACCT> <TUNNEL> <sub.domain.com> http://localhost:PORT`
   → PUT success + version bump, VERIFY line printed.
2. `scripts/add-cf-dns.py <zone> <sub> <TUNNEL_ID>` → CNAME created; DNS resolve may
   fail for 1-5 min (normal).
3. `curl -s -o /dev/null -w "%{http_code}" https://sub.domain.com/` → 200.
4. Tell the user: admin URL = `/admin.html`, default password location, reset
   procedure (delete `data/state.json` + restart to regenerate papers).

See `references/dithi-exam-app.md` for the full worked example (exam app on port
5100, dithi.thefirstonly.com).
