# Paperclip Pattern Absorption — Worked Example

**Source:** paperclipai/paperclip (94.2k ⭐, MIT, TypeScript, Node.js server + React UI)
**Date:** 2026-09-29
**Target:** ai-company-v2 (registry SQLite + CEO + worker + watchdog)

## Methodology

This is the template for absorbing patterns from any open-source project:

1. **GitHub API triage** — stars, language, license, topics, last commit
2. **README analysis** — 4 pillars, features, problems solved, architecture diagram
3. **Codebase structure scan** — packages/, server/, ui/, adapters/
4. **Claim verification** — separate marketing from substance
5. **Stack fit check** — does it run on our infra? (Windows, Node.js 24+, Docker)
6. **Pattern extraction** — what to steal, what to skip
7. **Adoption plan** — incremental GĐs, not wholesale rewrite

## Patterns Extracted (5 total)

### 1. Goal Hierarchy
**Paperclip:** Company → Project → Goal → Issue → Task. Every item traces upward. Agent knows "why."

**Implementation:** Add `goals` table to registry SQLite + `company.py goal` subcommand + CEO passes goal chain in context.

### 2. Budget per Agent
**Paperclip:** Each agent has monthly token budget. Hard stop when exhausted.

**Implementation:** Add `budgets` table + worker checks before execution + cron reset monthly.

### 3. Audit Trail
**Paperclip:** Every mutating request traced to actor. Activity log is immutable tree.

**Implementation:** Extend `activity_log` with actor (agent_id), parent_event_id (tree), metadata (JSON) + dashboard tab.

### 4. Heartbeat Scheduling
**Paperclip:** DB-backed wakeup queue. Agent wakes, checks work, runs, sleeps. Context persistent across heartbeats.

**Implementation:** Add `heartbeats` table + watchdog auto-wakes agent + worker saves context_state.

### 5. Company Portability
**Paperclip:** Export/import entire org — agents, skills, projects, routines. Secret scrubbing.

**Implementation:** dump registry tables to JSON + scrub secrets + validate + upsert.

## What We Skipped

| Feature | Reason |
|---------|--------|
| Multi-user org chart | Single user (Quang) |
| Approval gates | CEO is Quang himself |
| MCP server integration | No external tool servers |
| Plugin system | Would add complexity without benefit |
| Docker deployment | No Docker on this machine |
| React UI rewrite | Dashboard already exists (port 5050) |

## Decision Framework

When evaluating any open-source project for absorption:

```
Is it single-user or multi-user?  →  Skip multi-user features
Does it need Docker/Node 24+?    →  Skip or find alternative
Is the claim verifiable?          →  If no, discount heavily
Does our existing code cover it?  →  If yes, skip (don't reimplement)
Can we extract just the pattern?  →  Yes → absorb pattern, not code
```

## Key Insight

Paperclip is NOT for single-user setups. 94k stars doesn't mean "install it." It means "study how they solved the problems you're about to hit." The value is in the patterns, not the code.
