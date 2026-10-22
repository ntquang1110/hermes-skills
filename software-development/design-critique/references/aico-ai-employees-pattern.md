# AICO / AI Employees — Agent Configuration Pattern

**Source:** github.com/markfulton/ai-employees (MIT)
**Creator:** Mark Fulton, Reinventing.AI
**Date reviewed:** September 20, 2026. This repo's contract + guardrails pattern directly informed the deterministic-llm-hybrid skill.
**Status:** 107 stars, 28 forks, 48 commits, first commit Sep 2, 2026

## What it is

Not "AI Employees" — it's 8 markdown-based role configuration folders that your existing AI agent (Claude Code, Hermes, OpenClaw, etc.) reads and follows on a schedule. The agent is the employee. These are job descriptions + SOPs.

## Repo structure

```
ai-employees/
  employees/
    gtm-engineer/
    seo-employee/
    web-dev-employee/
    social-media-employee/
    ad-manager-employee/
    sales-employee/
    customer-satisfaction-employee/
    chief-of-staff/
```

## Per-role structure

```
gtm-engineer/
  ROLE.md            — what it owns, what it never touches
  CONTRACT.md        — what it may do alone, what needs approval, channel release rules
  SCHEDULE.md        — one row per routine: days, fire, window, budget, browser lane
  AGENTS.md          — harness-agnostic entry point (follows AGENTS.md convention)
  CAPABILITIES.md    — which concrete route a named capability takes
  RELEASES.md        — channel release permissions (user edits this)
  INSTALL-PROMPT.md  — what the agent reads for first-time setup
  CHANGELOG.md
  VERSION
  employee.json
  routines/
    <routine-id>/
      SKILL.md       — the actual routine instructions
  run/               — run scripts per harness
  scripts/           — guard scripts (guard.mjs, etc.)
  recipes/           — browser recipes
  examples/          — fictional output samples
```

## Key design decisions

| Decision | Why |
|----------|-----|
| AGENTS.md convention | Any harness can pick up the kit without being told how |
| SCHEDULE.md as single source of truth | No clock time in SKILL.md files; all timing in one table |
| Browser lane system | Prevents two routines fighting for the same browser |
| Period keys (YYYY-MM-DD, YYYY-Www, YYYY-MM) | Prevents duplicate runs on wake-from-sleep |
| Guardrail 1: held outbound | Drafts, fills, stages — last click is user's until channel released |
| Guardrail 2: never credentials | No account creation, no password entry, no captcha |
| Precedence chain | Member's workspace rule > CONTRACT.md > SCHEDULE.md > CAPABILITIES.md > ROLE.md > SKILL.md |
| Self-improvement | Routines fix their own instructions when pages change |

## Notable pitfalls

- **Heavy Claude Code dependency** — listed as 1 of 11 harnesses but clearly designed for Claude Code first
- **Real cost** — runs on Claude Pro/Max ($20-60/mo), not free
- **Young repo** — first commit Sep 2, 2026. Only 3 weeks of claimed real use
- **Lead funnel** — README has 5+ CTAs to Agent Ops Club ($499 lifetime). The real value (install prompt, training) is behind the paywall

## What to steal

- The ROLE.md + CONTRACT.md + SCHEDULE.md + routines/ structure is clean for any agent-based system
- AGENTS.md convention for harness-agnostic entry
- Browser lane system for concurrent agent scheduling
- Period key approach for duplicate-run prevention
