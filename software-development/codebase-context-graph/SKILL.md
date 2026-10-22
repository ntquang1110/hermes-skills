---
name: codebase-context-graph
description: "graft context graph: cut agent token spend on codebases."
version: 1.0.0
tags: [graft, context-graph, tokens, codebase, mcp, efficiency]
---

# Codebase Context Graph (Graft) — giảm token cho coding agents

## When to use

- User wants to cut token/tool-call spend when agents work on large codebases
- Agent sessions keep re-exploring a repo (grep, open file, follow import) — same cost every task
- Adding a repo-map/context layer so a fresh session starts oriented instead of blind

## What Graft is

`@nanonets/graft` (NanoNets context-graph-engine, MIT, v0.8.x) builds a "context graph" of a
codebase into a folder of **linked markdown files** (`graft/`), one node per system/API/concept,
with exact `file:line` spans and plain-English explanations. It is a **repo-local regenerable
cache** (like node_modules) — git-ignored automatically, never committed; teammates run
`graft build` to get their own.

Key properties (verified 2026-08):
- **Structural graph (`graft build`) is $0** — deterministic tree-sitter, NO LLM, no API key.
- **`--deep` adds LLM concept map** (file summaries + symbol crux) via any OpenAI-compatible
  endpoint — vendor-neutral: `GRAFT_PROVIDER=openai GRAFT_BASE_URL=... GRAFT_MODEL=... GRAFT_API_KEY=...`.
- Vendor benchmark: −42% tokens, −46% tool-calls, −60% time (Claude Code; expect smaller gains
  on Hermes because State File Protocol already trims context — graft adds the code-structure layer).

## Install

```bash
npm install -g @nanonets/graft
# tree-sitter native bindings need explicit allow-scripts on this machine:
npm install -g --allow-scripts=@nanonets/graft,tree-sitter,tree-sitter-go,tree-sitter-python,tree-sitter-typescript,tree-sitter-javascript @nanonets/graft
graft --version   # 0.8.x
```

## Build (structural, $0)

```bash
cd /path/to/repo
graft build            # parses N files → nodes/edges/cards → graft/ (git-ignored)
# Verify: graft/INDEX.md exists; `graft ask "some question"` returns ranked nodes with file:line
```

Observed scale: volden-ops-web 167 TS files → 1,352 nodes, 2,764 edges, 166 cards (~6MB);
ai-company 36 py files → 310 nodes, 943 edges, 36 cards (~1.3MB).

## Build --deep (LLM concept map)

```bash
cd /path/to/repo
export GRAFT_PROVIDER=openai
export GRAFT_BASE_URL=https://api.groq.com/openai/v1     # or any OpenAI-compatible endpoint
export GRAFT_MODEL=llama-3.3-70b-versatile               # Groq free tier
export GRAFT_API_KEY=<key>
graft build --deep
```

Pitfalls (verified):
- **Groq free tier rate-limits fast on --deep** (12k TPM, llama-3.3-70b). Multi-file repos
  (150+ files) will drop some files with 429s. Accept partial concept map, or use a paid/larger
  TPM provider, or run in background (`terminal background=true`) and let it grind.
- On this LAN, **OmniRoute (192.168.1.110:20128) is NOT a dependable graft provider** — it can be
  down; prefer Groq (key already in `~/AppData/Local/hermes/.env` as `GROQ_API_KEY`).
- `--deep` writes concept files into `graft/*.md` (e.g. `*-concept.md`, `*-system.md`) and updates
  `graft/INDEX.md`; structural files stay under `graft/<topdir>/`.

## Wire into Hermes (AGENTS.md + MCP)

1. **AGENTS.md wiring** (agents host): `graft init --agents agents` appends a fenced
   `<!-- graft:start -->` section to the repo's `AGENTS.md` telling any agent to query the graph
   (`graft ask --source`, `graft skeleton`, `graft callers`, `graft grep`, `graft map`) before
   grepping/opening source. Re-running only updates graft's own section.
2. **MCP server** — Hermes native MCP client (config.yaml `mcp_servers`), tools appear as
   `mcp_graft_*` after gateway restart:
   ```bash
   hermes config set mcp_servers.graft_volden.command "npx"
   hermes config set mcp_servers.graft_volden.args '["-y","@nanonets/graft","mcp","D:/Hermes Proj/volden-ops-web"]'
   hermes config set mcp_servers.graft_volden.env.GRAFT_PROVIDER "openai"
   hermes config set mcp_servers.graft_volden.env.GRAFT_BASE_URL "https://api.groq.com/openai/v1"
   hermes config set mcp_servers.graft_volden.env.GRAFT_MODEL "llama-3.3-70b-versatile"
   hermes config set mcp_servers.graft_volden.env.GRAFT_API_KEY "<groq key>"
   ```
   Requires `pip install mcp` in Hermes venv (already installed on this machine). MCP changes
   need a gateway restart (no hot-reload).
3. **Parent AGENTS.md pointer** — if multiple repos use graft, add a §0.5 note in the umbrella
   `D:/Hermes Proj/AGENTS.md` listing which repos have graphs + the commands.

## CLI quick reference

| Command | Purpose | LLM? |
|---------|---------|------|
| `graft ask "<q>" --source` | ranked nodes with code spans inlined | $0 |
| `graft skeleton <file>` | signatures only (~10× cheaper than reading file) | $0 |
| `graft callers <symbol>` | who calls it (`--direction out` callees, `--depth N` blast radius) | $0 |
| `graft grep "<regex>"` | exhaustive hits grouped by enclosing symbol | $0 |
| `graft map` | token-budgeted repo orientation (clusters, hubs, hotspots) | $0 |
| `graft check` | fail if graph stale vs code (CI) | $0 |
| `graft viz` | interactive graph viz server | $0 |

## Pitfalls

- **Do NOT commit `graft/`** — it's a regenerable local cache; `graft build` auto-gitignores.
- **Rebuild after big code moves** — stale graph shows as diff in review; can add a cron for
  periodic `graft build`.
- **Tree-sitter bindings** — native install scripts are blocked by npm allow-scripts by default;
  use the `--allow-scripts=...` form above or `graft` fails on parse.
- **MCP tools appear only after gateway restart** — config change is not hot-reloaded.
- **Environment-dependent provider**: don't hardcode "OmniRoute is dead" — the lesson is
  "prefer Groq for graft --deep on this machine; OmniRoute may be down, ping+port-check first".
