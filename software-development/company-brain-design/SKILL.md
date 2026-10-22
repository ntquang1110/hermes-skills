---
name: company-brain-design
description: Design/evaluate cross-session LLM agent memory layer.
---

# Company Brain Design

A "company brain" (YC RFS term) is a durable, queryable memory layer that an agent or team of agents uses across sessions so they stop being amnesiac about everything except code. This skill covers how to **evaluate** the existing solutions and **decide what to actually build** — without over-engineering.

Triggers: user pastes a "company brain" / "bộ não công ty" article or asks about durable agent memory, GBrain, Mem0, Letta, Graphiti, Sylph, knowledge graphs for agents, cross-session memory, or proposes deploying such a system.

## The 4 functions every company brain must solve
1. **Ingest signal** — capture meetings, email, tweets, voice, ideas into a store
2. **Memorize** — persist durably across sessions, not in chat context
3. **Self-update** — enrich/consolidate proactively (dedup, fix citations, find contradictions, keep fresh) via a scheduled "dream cycle" cron
4. **Retrieve + answer** — find AND synthesize; return an answer with citations, not "10 chunks that mention the query"

## Solution landscape (stars verified 08/2026)
| Solution | ⭐ | Focus |
|----------|-----|-------|
| GBrain (garrytan) | 29k | Git/Markdown + self-wiring knowledge graph + synthesis/gap-analysis. Runs ON Hermes/OpenClaw (supported harness) |
| Mem0 | 64k | Universal memory layer plug-in for any agent; chooses what to remember |
| Letta | 24k | Stateful agents, long-horizon memory across sessions |
| Graphiti/Zep | 30k | Knowledge graph with a timeline ("what was true in March ≠ now") |
| Sylph | 192 | Whole company = a Git repo (CONTEXT.md + per-domain dirs); human edits output, agent learns back |

## Decision rule (the moat insight)
Don't deploy a second heavy brain wholesale. If you already have markdown-in-git memory + a retrieval layer (Hermes memory/skills, state files, graft context graph, KFlow), adding GBrain/Mem0/Letta becomes a 2nd system of record competing with what you have — worse, not better. Instead **steal the architecture** the solutions converge on and apply the 3 portable principles to whatever repo already holds your knowledge:

### The 3 portable GBrain principles
1. **Git repo = system of record; DB is a derived cache.** Never back up the database — wipe it and rebuild from the markdown repo (`sync` + re-extract). Multi-machine = git push/pull. This is the single most important design property; everything else is optional.
2. **Shared `_*rules.md` files every skill/agent reads.** `_filing-rules` (where new knowledge lands — decision tree), `_output-rules` (real citations, deterministic links, no AI-slop, gap analysis required), `_excluded-people` (names never attributed), `_operating-rules` (when write-to-brain vs when ask-human). Edit one file → every skill/agent picks it up next request.
3. **Synthesis + gap analysis.** Answers must end with "what the brain doesn't know yet" (stale / uncited / contradictory / hole), not just present known facts. This is the actual differentiator over keyword search.

### Supporting patterns (from the company-brain playbook)
- **Per-agent/scoped workspace:** `partners/<slug>/` with `USER.md` (role, top-3 priorities, writing style), `concepts/`, `sources/`. When ONE agent serves the whole company/team, use directory-based scoping inside a single source — NOT per-user OAuth (that's only for 10+ humans each running their own AI client).
- **Botmaster onboarding:** pre-populate each person's slice → walk them through 3 wow flows (synthesis query, gap-analysis query, write-back) → only then graduate to open DM. An empty slice gets abandoned.

## Pitfalls
- **"What's my name / top jobs" answered from identity files is NOT proof of a working brain.** The real test is the cross-session round-trip: tell it one fact, restart the session, ask for it back — the answer must come from the brain, not context.
- **Self-wiring typed knowledge graphs** (edges extracted with ZERO LLM calls from `[[wikilinks]]` + `works_at`-style refs) give real retrieval lifts (+31 P@5 over vector-only), but only justify a build once you have actual entity data (people/companies/deals). Skip it early.
- Deploys are heavy: Postgres/PGLite + embedding provider (Voyage/OpenAI = recurring API cost) + a 24/7 daemon. Real money and ops; do it only when the portable principles stop being enough.

## Reference
- `references/gbrain-architecture.md` — deep-dive from reading GBrain's source (system-of-record contract, self-wiring graph, synthesis/gap-analysis example, dream cycle, company-brain tutorial, deployment topologies, schema packs).