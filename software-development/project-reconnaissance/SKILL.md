---
name: project-reconnaissance
description: "Systematically audit an unfamiliar project: mission, features, architecture, gaps, and prioritized next steps."
category: software-development
---

# Project Reconnaissance

Systematically understand a project from the ground up — what it IS, what it HAS, what's MISSING, and what to do NEXT.

## When to Use

- User says "tổng quan dự án", "overview the project", "what features exist", "kiểm tra tiến độ"
- Joining an existing project mid-stream
- Revisiting a dormant or unfamiliar codebase
- Onboarding onto a project you haven't touched in weeks/months

## Process

### Phase 1: Find & Clone

1. **Search GitHub** for the repo first (before cloning) to get metadata:
   - Is it private/public?
   - Description, language, topics
   - Last commit date
   - File tree at root level

2. **Check existing credentials before attempting clone:**
   - Run `env | grep -iE "GITHUB|GH_|GIT|PAT|TOKEN"` to find pre-existing tokens/environment variables
   - Look for `GITHUB_PAT_B64` — a common base64-encoded PAT pattern on this machine. Decode with: `echo "$GITHUB_PAT_B64" | base64 -d`
   - Check `gh auth status` if gh CLI is available
   - Check `git config --global --list | grep -i github` for saved credentials
   - Check Windows Git Credential Manager: `cmd.exe /c "where git-credential-manager.exe 2>&1"`

3. **Clone with proper auth:**
   - `gh repo clone owner/repo-name` if gh is authenticated with `repo` scope
   - HTTPS with PAT embedded in URL if `gh` fails: `https://owner:PAT@github.com/owner/repo.git`
   - For base64-encoded PATs: embed after single-decoding inline (`$(echo "$B64" | base64 -d)`) — avoids exposing the plain token in shell history
   - Use `GIT_TERMINAL_PROMPT=0` to prevent git from hanging on interactive auth prompts
   - Use `--depth 1` for quick reconnaissance (shallow clone)

4. **Debug hung clones:**
   - If `git clone` hangs silently, kill it (Ctrl+C) and retry with: `GIT_CURL_VERBOSE=1 git clone ... 2>&1 | head -30`
   - Look for `HTTP/1.1 401 Unauthorized` → private repo, needs auth
   - Look for `HTTP/1.1 200` but hanging → repo is large, use `--depth 1`
   - Look for `Could not resolve host` → network/VPN issue

5. **For local-only projects**, navigate to the project directory first.

### Phase 2: Structure Scan

Read the file tree and identify:
- **Entry points** — `app/page.tsx`, `main.py`, `main.go`, `src/index.tsx`, etc.
- **Route structure** — pages/ directories, API routes
- **Config files** — `package.json`, `tsconfig.json`, `requirements.txt`, `Cargo.toml`, `pyproject.toml`
- **Database schema** — SQL migration files, Prisma schema, SQLAlchemy models, `schema.sql`
- **State management** — Redux stores, React context, global state

### Phase 3: Read Key Sources — BATCH IN PARALLEL

**Token-saving principle:** Read multiple independent files together (same tool call batch) instead of one-at-a-time. The runtime parallelizes independent reads, so you get all the info in one round-trip.

| Order | Batch | Files | What you learn |
|-------|-------|-------|----------------|
| 1 | **Config + Stack** | `package.json`, `tsconfig.json`, `vite.config.ts`, `next.config.js`, `Cargo.toml`, `requirements.txt` | Tech stack, build setup, routing config |
| 2 | **Docs** | `README.md`, `docs/SOURCE-MAP.md` (if exists), `.env.example` | Mission, project structure map, env requirements |
| 3 | **Project State** | `BUGS.md`, `PENDING_TASKS.md`, `CHANGELOG.md` | Known issues, task queue, what's actually in progress — CRITICAL for understanding what needs doing |
| 4 | **Entry Points** | Layout root, app/page, main entry | Branding, metadata, global component structure |
| 5 | **DB Schema** | SQL migration files, Prisma schema, `supabase_schema.sql`, `api/db-schema.sql` | Data model, relationships, permissions |
| 6 | **Key Components** | Auth middleware, API routes, main module files | Access control, API surface, feature implementation |

**Always check:**
- `docs/SOURCE-MAP.md` — if this exists, it's THE most token-efficient way to understand the entire codebase (single file, rich detail)
- `BUGS.md` — tells you what's broken, what was fixed, and patterns of past failures
- `PENDING_TASKS.md` — tells you what features are in-flight and what's blocked
- `AGENTS.md` or `CLAUDE.md` — project-specific AI guidelines and constraints. These override your default approach. Read them before writing any code.
- Every route file / page file — features live here

**VERIFY SOURCE-MAP.md accuracy BEFORE trusting it:**
SOURCE-MAP.md can be stale or incomplete if not updated regularly. After reading it, run a delta scan:

```bash
# 1) Get actual file tree
find . -maxdepth 1 -type f -o -type d | grep -v .git | sort
find src -type f -name "*.ts" -o -name "*.tsx" -o -name "*.vue" | sort
ls api/

# 2) Cross-check against SOURCE-MAP.md sections
#    - Root structure: compare top-level directories/files
#    - Backend: check all api/ files listed
#    - Frontend: check all src/ components, lib/, types
#    - Scripts: verify script filenames mentioned actually exist
#    - Docs: compare listed docs against real docs/ directory
#    - SQL migrations: count actual files in sql/ vs listed count

# 3) Check for:
#    - Files listed in SOURCE-MAP that DON'T exist (removed/renamed)
#    - Files that exist but AREN'T listed
#    - Incorrect counts (e.g., "31 migrations" when 77 exist)
#    - Non-existent references (e.g., api/server-utils.ts no longer exists)

# 4) Update SOURCE-MAP.md with the findings:
#    - Add missing entries
#    - Remove stale entries
#    - Correct directory structure, file lists, and counts

# 5) EMBED A SELF-MAINTENANCE RULE IN AGENTS.md (user convention — critical):
#    Add a section (e.g. "QUẢN LÝ SOURCE MAP") mandating that every new page/path/file
#    created in src/, api/, scripts/, sql/, docs/ MUST be added to SOURCE-MAP.md in the
#    same commit. Include a verification step ("check git diff --stat docs/SOURCE-MAP.md
#    before commit"). Without this, the map drifts again within weeks — the one-shot fix
#    does not survive. The user explicitly requires this ("cứ mỗi khi có page mới thì
#    update vào source map").
#    NOTE: volden-ops-web already has this rule as AGENTS.md section 3.6 (created 2026-07-26).
#    Verify the rule exists on OTHER projects, don't duplicate it there.
```

**IMPORTANT — Path resolution pitfall when writing SOURCE-MAP.md:**
On Windows with MSYS (git-bash), `/d/...` paths used in terminal are MSYS-style paths. The `write_file` tool resolves relative paths against the active workspace directory (Hermes CWD), NOT the terminal's CWD. This means a path like `/d/Hermes Proj/project/docs/SOURCE-MAP.md` written from `write_file` may resolve to `D:\Hermes Proj\ai-company\d\Hermes Proj\...` instead of the intended `D:\Hermes Proj\project\...`.

**Fix:** Always pass the **Windows absolute path** (`D:/Hermes Proj/project/docs/SOURCE-MAP.md` with forward slashes) to `write_file`, or use a relative path from the project root. To get the Windows path, run `pwd -W` inside the project directory via terminal first.

### Phase 4: Feature Audit

Build a table with three columns:

| Feature | Status | Notes |
|---------|--------|-------|
| Feature A | ✅ Built | Where it lives, key files |
| Feature B | 🔴 Referenced but missing | Referenced in nav/CTA but no page |
| Feature C | 🟡 Partial | Built but incomplete |

**Track every feature:**
- Found in code (✅)
- Referenced in UI but page not found (🔴)
- Partially implemented (🟡)
- Database table exists but no UI (🟡)

### Phase 5: Extract Mission & Map

Look in these places for the project's mission:
- **README.md** description
- **Layout metadata** — `title`, `description` fields
- **Hero section** — headline, subtitle, CTA text
- **Database schema comments** — table descriptions, category names
- **Footer** — about text, links

Map each existing feature to a mission pillar. Gaps = features implied by the mission but not yet built.

### Phase 6: Prioritized Suggestions

Group suggestions by impact tier:

| Tier | Label | Example |
|------|-------|---------|
| 🔥 **Core** | Must-have for the mission | CRUD for the primary domain object |
| ⚡ **Engagement** | Interaction & community | Comments, likes, sharing |
| 📈 **Growth** | Quality, trust, SEO | Admin dashboard, sitemaps, analytics |
| 🔐 **Operations** | Auth, deploy, security | Email reset, deployment CI/CD |

Present as a table with columns: Tier, Feature, Rationale, Effort estimate.

For extracting adoptable patterns from an open-source project (user: "hấp thụ cho anh") — pattern identification, stack fit check, incremental adoption plan, and decision framework — see `references/paperclip-absorption.md` (worked example: paperclipai/paperclip 94k ⭐ → ai-company-v2, 2026-09-29).

## Pitfalls

| Issue | Solution |
|-------|----------|
| `gh repo clone` fails despite valid PAT | gh uses its own credential store, not `.env`. Use HTTPS clone with PAT embedded in URL, or `gh auth login` with the token |
| Base64-encoded PAT in env var (`GITHUB_PAT_B64`) | Decode and embed inline: `https://user:$(echo "$GITHUB_PAT_B64" | base64 -d)@github.com/owner/repo.git` |
| Private repo — can't view files via browser | Use GitHub API (`/repos/owner/repo/contents/`) to explore, or run a local file server |
| No README / minimal README | Infer mission from layout metadata, hero text, page titles, DB schema comments |
| Outdated lockfile / missing `node_modules` | Run `npm install` or `pnpm install` before reading typed imports |
| Monorepo structure | Each package/ or apps/ subdirectory may have its own `package.json` — check each |
| Supabase env vars missing locally | Check for `.env.example` or `scripts/` migration files — DB schema often exists independent of runtime env vars |
| Token has wrong scopes | Verify via API: check `X-OAuth-Scopes` header from `https://api.github.com/user` |
| Clone hangs indefinitely | Kill and retry with `GIT_CURL_VERBOSE=1` to see if it's 401 (auth) vs slow transfer (large repo) |
| `gh` not installed | Don't install — use HTTPS clone with PAT instead. Faster and avoids scope issues |
| `write_file` path resolution on Windows MSYS | Paths like `/d/Project/docs/` passed from terminal context can resolve incorrectly when the active workspace dir differs. Run `pwd -W` in the project dir to get the Windows absolute path, then pass that (e.g., `D:/Project/docs/file.md`) to `write_file`. |
| SOURCE-MAP.md is stale or incomplete | Always verify documented file lists against actual `find` output before trusting. Update the doc as part of the reconnaissance, not as an afterthought. Then add the AGENTS.md self-maintenance rule (step 5 of Phase 3) so it stays fresh. |
| Committed but not pushed | User expects commit AND push to remote. After committing, run `git push origin <branch>` — the user will ask "em có push không?" otherwise. |

## Reference

See `references/theliems-audit.md` and `references/volden-audit.md` for worked examples of this process applied to real projects.

See `references/source-map-verification.md` for a detailed worked example of verifying and updating a stale SOURCE-MAP.md (volden-ops-web, 283→543 lines).

For evaluating an EXTERNAL framework/tool repo for adoption (user: "phân tích source này cho anh") — GitHub API triage, claim verification, maturity signals, stack comparison, watch/adopt verdict — see `references/external-framework-evaluation.md` (worked example: penguin-harness, 2026-08-07).

For vetting a repo's PROVENANCE before trusting it — "code này của ai?", fork vs upstream, tests có thật
được chạy không, bẫy bảo mật, chi phí API ẩn — see `references/repo-provenance-fork-diff.md`
(worked example: PaperBanana 7,3k⭐ vs google-research/papervizagent, 2026-10-21).

For auditing an ML **model** repo for real deployability on this machine ("nó chạy được trên máy anh không?") — repo benchmark mining, wheel/interpreter pin checks, proving the code path with a real model run, and report structure that labels extrapolated numbers — see `references/model-repo-cpu-feasibility.md` (worked example: jeff / GLiFormer 400M on Windows CPU, 2026-09-25). The reusable CPU latency/RAM probe + large-checkpoint downloader scripts live in the `model-cost-optimization` skill.
