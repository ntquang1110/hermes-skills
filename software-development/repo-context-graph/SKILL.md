---
name: repo-context-graph
title: Repo Context Graph (Graft)
description: Cut token spend on codebases with graft repo context graph.
version: 1.0.0
tags: [graft, context-graph, tokens, codebase, tree-sitter, mcp]
---

# Repo Context Graph (Graft)

Tool: `@nanonets/graft` (NanoNets context-graph-engine). Builds a repo's context graph
as a folder of linked markdown files (`graft/`) that live in the repo and stay in sync
via git. Each node explains one system/API/concept with exact `file:line` spans — the
agent reads the map once and stops re-exploring the repo from zero every session.
Vendor-neutral: structural graph is deterministic tree-sitter (no key, no LLM);
`--deep` adds LLM-written summaries through any OpenAI-compatible endpoint.

Why it matters here: user's recurring pain is token spend + session-memory loss after
switching providers. Graft attacks the exploration half — the part SFP (state files)
doesn't cover (SFP = project state; Graft = code structure).

## When to use

- User asks to reduce token usage on a codebase (agent keeps re-reading files/symbols)
- New repo with active coding-agent work (volden-ops-web, ai-company are wired)
- AGENTS.md says "get context from the graph before grepping" (graft:start section)

## Setup (done 2026-08-05, already installed on this machine)

```bash
npm install -g --allow-scripts=@nanonets/graft,tree-sitter,tree-sitter-go,tree-sitter-python,tree-sitter-typescript,tree-sitter-javascript @nanonets/graft
# allow-scripts REQUIRED — tree-sitter native bindings need node-gyp-build; bare install warns and may leave broken parsers
graft --version   # 0.8.2
```

## Build the graph (per repo)

```bash
cd <repo>
export GRAFT_PROVIDER=openai GRAFT_BASE_URL=http://192.168.1.110:20128/v1 GRAFT_MODEL=deepseek-v4-flash GRAFT_API_KEY=omniroute
graft build          # structural graph, $0 — no LLM, no key. FAST.
graft build --deep   # adds LLM concept map + per-symbol summaries. NEEDS a working LLM endpoint.
```

- `graft build` (no key): parsing 167 files → `✓ wiring: 1352 nodes (799 function, 192 interface...), 2764 edges, 166 cards`. Output to `<repo>/graft/`, auto-gitignored (local cache like node_modules).
- `graft build --deep` requires the LLM endpoint to be UP. If `GRAFT_BASE_URL` host is down (port not listening), the build hangs silently at "reading concepts" — check the endpoint BEFORE running deep:
  ```bash
  curl -s -o /dev/null -w "%{http_code}" --max-time 8 http://192.168.1.110:20128/v1/models   # 200 = ok
  ```
  OmniRoute (LAN LLM proxy on 192.168.1.110:20128) died during 2026-08-05 and deep could not complete — the structural graph is the 80% win and works without it.

## Wire into agents

```bash
graft init --agents agents   # appends a <!-- graft:start --> section to AGENTS.md + writes opencode.json MCP entry
graft init --dry-run         # see exactly what it would touch first
```

- Writes a fenced `## Graft — repo context graph` section into AGENTS.md: tells agents to `graft ask "<q>" --source`, `graft skeleton <file>`, `graft callers <symbol>`, browse `graft/INDEX.md` — before grepping source.
- Hermes reads AGENTS.md (cwd-only discovery), so sessions running in a wired repo inherit the rules automatically.
- For repos that had NO AGENTS.md before (e.g. ai-company): `graft init` creates a bare one with only the graft section — PREPEND the repo's own operating rules (SFP protocol, workflow rules) so the file isn't just graft content.

## Hermes MCP integration

```bash
hermes config set mcp_servers.graft_volden.command "npx"
hermes config set mcp_servers.graft_volden.args '["-y","@nanonets/graft","mcp","D:/Hermes Proj/volden-ops-web"]'
hermes config set mcp_servers.graft_volden.env.GRAFT_PROVIDER "openai"
hermes config set mcp_servers.graft_volden.env.GRAFT_BASE_URL "http://192.168.1.110:20128/v1"
hermes config set mcp_servers.graft_volden.env.GRAFT_MODEL "deepseek-v4-flash"
hermes config set mcp_servers.graft_volden.env.GRAFT_API_KEY "omniroute"
```

Exposes `mcp_graft_volden_*` tools (graft_find_code, graft_file_api, graft_trace_calls, graft_find_all, graft_repo_map, graft_check_freshness). Requires Hermes venv to have `mcp` package (`pip install mcp` — already present) and a gateway restart.

## Usage patterns (what the agent actually does)

- `graft ask "order creation flow with VTP shipping" --source` → ranked nodes with file:line + source inlined — usually the full answer, no follow-up read.
- `graft skeleton <file>` → every signature + span, ~10× cheaper than reading the file (skim API surface).
- `graft callers <symbol>` / `--direction out` → precomputed edges, blast radius.
- `graft grep "<literal>"` → exhaustive hits grouped by enclosing symbol (ranked ask is top-N, NOT complete — use grep for "every occurrence").
- `graft check` → fails if graft/ is stale vs code (CI use).

## Pitfalls

- **Structural build is the win; deep is optional.** `graft build` alone (tree-sitter, $0) already gives nodes+edges+cards. Deep adds prose but costs LLM calls and depends on endpoint uptime.
- **Don't commit graft/** — it's auto-gitignored; teammates run `graft build` for their own copy.
- **Graph goes stale as code changes** — rebuild (`graft build`) when a repo has drifted; `graft check` reports drift.
- **`allow-scripts` required at install** — without it tree-sitter native binding may not compile (see Setup).
- **`init` on a repo without AGENTS.md creates one with ONLY graft content** — prepend project rules (SFP etc.) or the file loses the repo's operating conventions.
- Benchmark claims (−42% tokens, −46% tool calls) are from the vendor on Claude Code; treat as direction, measure on Hermes with a real task before promising numbers.
