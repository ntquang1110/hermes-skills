# GBrain — deep dive from source (Garry Tan, garrytan/gbrain, v0.4x, 08/2026)

Production brain behind Garry Tan's OpenClaw AND Hermes deployments at YC: 155,795 pages / 24,589 people / 5,340 companies / 66 cron jobs. Runs 24/7, ingests meetings/email/tweets/voice, enriches people+companies, fixes citations, consolidates memory overnight ("I wake up smarter"). This is the reference for the architecture the company-brain-design skill abstracts.

## Where it verified
Clone shallow (`git clone --depth 1`), read in this order: `README.md` → `docs/architecture/system-of-record.md` → `docs/tutorials/company-brain.md` → `docs/architecture/topologies.md`. The rest (`AGENTS.md`, `DESIGN.md`, `docs/architecture/schema-packs.md`, `RETRIEVAL.md`) is filler until you need a specific mechanism.

## System of record (the core contract)
> The GitHub repo (markdown + frontmatter) is the system of record. The Postgres/PGLite database is a derived cache. We do not back up the database — we rebuild it from the repo.

- DB rows split into 3 categories: FS-canonical (user knowledge, stored as markdown fences `<!--- gbrain:NAME:begin/end -->`), derived-from-FS (chunks, embeddings, page_versions), DB-only-by-design (runtime/job/credentials/audit).
- Disaster recovery = wipe derived tables, `gbrain sync && gbrain extract all`, counts match. No backups.
- `gbrain forget` rewrites the fence row with strikethrough + `valid_until=today`; DB reconstructs the forget state on rebuild. This is how "delete" stays canonical in git.
- Privacy: 3-layer strip for untrusted readers (chunker strips private facts before embedding; get_page strips fences for remote; git-level via `db_only` paths gitignored).
- CI gate (`scripts/check-system-of-record.sh`) fails any PR that writes a derived table outside the reconciler — the rule is enforced in code.

## Self-wiring knowledge graph (the retrieval moat)
- Every `put_page` extracts entity refs from markdown/`[[wikilinks]]`/typed-link syntax and writes typed edges (`attended`, `works_at`, `invested_in`, `founded`, `advises`, `mentions`) with ZERO LLM calls.
- Multi-hop traversal via `gbrain graph-query` ("who works at Acme?" — vector search can't answer this).
- Benchmarks: P@5 49.1%, R@5 97.9% on a 240-page Opus-rich-prose corpus; **+31.4 points P@5** over its graph-disabled variant and over ripgrep-BM25 + vector-only RAG.

## Search vs think (two query layers)
- `gbrain search` — raw retrieval, hybrid score (vector HNSW pgvector + BM25 + RRF + source-tier boost + optional reranker), returns top pages. Cheap, no LLM.
- `gbrain think` — runs retrieval then composes a synthesized answer with citations AND an honest gap-analysis note: when a page is stale, a claim uncited, two pages contradictory, or there's a hole to fill. The gap analysis is the differentiator.

## Dream cycle
Cron-driven enrichment that runs overnight: dedup people pages, fix citations, score salience, find contradictions, prep tomorrow's tasks. This is the "self-update" function made concrete — the agent keeps the brain sharp while the human sleeps.

## Company-brain mode (multi-user)
- Not a different install — same agent runtime + Supabase + CLI + harness, plus: multiple `sources` (repos) in one brain, per-user OAuth scopes, per-person folders/crons/skills.
- **Model A** (recommended 10-50 humans, each their own AI client): separate sources with OAuth client per teammate; `--source` controls write authority, `--federated-read` controls read scope; isolation enforced at the SQL layer.
- **Model B** (ONE agent serves everyone over Telegram/shared interface — Quang's pattern): a single `default` source with a `partners/<slug>/` convention, each partner gets a subdir (`USER.md`, `concepts/`, `sources/`). Simpler ops, no per-user OAuth. Write scoping can be server-enforced with `--bound-slug-prefixes`.
- Workspace repo conventions: `skills/<skill>/SKILL.md` (trigger phrases in frontmatter + procedure), flat `_*-rules.md` at skills root that EVERY skill reads (`_brain-filing-rules`, `_output-rules`, `_excluded-people`, `_operating-rules`), `crons/<slug>/*.md` with a `client:` frontmatter field to enforce per-person scoping.
- **Botmaster onboarding:** pre-populate `partners/<slug>` before login → walk 2-3 wow flows (synthesis query, gap-analysis query, write-back) → only then graduate to DM. Empty slice = abandoned tool.

## Topologies (where the brain lives)
1. **Single brain** (default): PGLite local (≤ ~50K pages, 2s setup, no Docker) or Supabase for larger. One agent.
2. **Cross-machine thin client**: heavy brain on a host, agent elsewhere consumes over HTTP MCP + OAuth. No local DB; CLI dispatch guard refuses DB-bound commands.
3. **Split-engine per-worktree**: each Conductor worktree gets its own `GBRAIN_HOME` code-brain (local PGLite) + a shared artifact brain. Explicit alias-based routing (`mcp__gbrain_code__*` vs `mcp__gbrain_artifacts__*`) — a wrong alias silently writes the wrong brain.

## Schema packs (the brain has a shape)
- Not a fixed layout. Bundled `gbrain-base-v2` = 15-type MECE taxonomy (person, company, media, tweet, social-digest, analysis, atom, concept, source, deal, email, slack, writing, project, note). Agents can evolve the shape (`gbrain schema detect → suggest → review-candidates --apply`).
- Threads through every read+write path: parse infers type from path prefix, fact extraction only on `extractable` types, search cache keys fold in the pack version.

## Engines / stack
- Two engines, one `BrainEngine` contract (140+ methods): PGLite (Postgres 17 WASM, zero-config personal) vs Postgres+pgvector (Supabase/self-hosted shared/multi-machine).
- Embedding providers: Voyage (default `voyage-4` 1024d), OpenAI, OpenRouter, Gemini, Ollama, llama.cpp (local), LiteLLM. Rerankers: Voyage `rerank-2.5`, llama-server cross-encoder recipe.
- FTS language configurable (`GBRAIN_FTS_LANGUAGE`); non-English brains supported (unaccent + stemmer recipe).
- Minions: Postgres-native BullMQ-shaped durable job queue for subagents, crash-safe two-phase persistence.
- Query modes: `conservative` / `balanced` / `tokenmax` bundle cost-vs-quality knobs.
- Connect to Hermes: `hermes mcp add gbrain --command $(which gbrain) --args serve`; verify `hermes mcp test gbrain`. Install ONLY via `bun install -g github:garrytan/gbrain` or clone+bun — the npm `gbrain` package is an unrelated impostor.

## Honest cost/effort read
- Full always-on setup: deployed server 8GB+ RAM + raw API token cost that scales with how hard the agent runs. ~30 min install via `INSTALL_FOR_AGENTS.md`; ~90 min to extend to company brain; 25-person company under ~$100/mo sustained.
- For Quang's stack: he already has markdown-in-git memory (ai-company, .hermes-state), graft context graph, KFlow. Recommendation was NOT to deploy GBrain — steal the 3 portable principles instead.