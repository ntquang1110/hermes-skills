# Hermes Skills

A working library of **356 agent skills** for [Hermes Agent](https://hermes-agent.nousresearch.com/docs) — the procedural memory layer that lets an agent reload a proven workflow instead of rediscovering it every session.

`1706` files · `356` skills · 29 categories. Each skill is a folder with a `SKILL.md` (YAML frontmatter + instructions) and optional `references/`, `scripts/`, `templates/`, `assets/`.

## Install

```bash
git clone https://github.com/ntquang1110/hermes-skills.git
cp -r hermes-skills/* ~/.hermes/skills/     # macOS / Linux
# Windows: copy into %LOCALAPPDATA%\hermes\skills\
```

Hermes picks up new skills on the next session. Load one with `skill_view(name='...')`.

## Categories

| Category | Skills |
|---|---|
| `legal` | 127 |
| `software-development` | 54 |
| `productivity` | 52 |
| `creative` | 27 |
| `research` | 26 |
| `devops` | 13 |
| `mlops` | 10 |
| `autonomous-ai-agents` | 8 |
| `understand-anything` | 8 |
| `coaching` | 6 |
| `media` | 5 |
| `github` | 3 |
| `council-believer` | 1 |
| `council-investor` | 1 |
| `council-judge` | 1 |
| `council-skeptic` | 1 |
| `critique-council` | 1 |
| `data-science` | 1 |
| `fixgby` | 1 |
| `legacy-msdoc-extraction` | 1 |
| `market-gap-analysis-framework` | 1 |
| `meeting-transcriber` | 1 |
| `metelligent-project` | 1 |
| `multi-agent-council` | 1 |
| `purchaser-pro` | 1 |
| `search` | 1 |
| `sol-pi-hermes` | 1 |
| `use-tinyfish` | 1 |
| `yuanbao` | 1 |

## What is in here

The library was built by running real work, then writing down the part that was hard. A skill only earns its place if it carries something a model would otherwise get wrong: an exact command, a config trap, a verification step, a decision table.

Recurring themes:

- **Agent infrastructure** — Hermes itself: config, providers, gateways, cron, plugins,
  token-efficiency internals, MCP wiring.
- **Deployment on Windows** — Docker Compose, Node web apps, Cloudflare Workers and
  tunnels, systemd-less process management, drive migration via NTFS junctions.
- **Research and evidence** — verified-citation workflows, PubMed/arXiv retrieval,
  regulatory dossiers, competitor catalog audits, 7-section compound profiles.
- **Production engineering** — Python, SQL, shipping pipelines, deterministic-vs-LLM
  boundaries, iterative optimisation loops.
- **Design and documents** — HTML report systems, design token sets, diagram authors,
  docx/xlsx/pdf generation.
- **Domain skills** — animal nutrition, alkaline mineral products, Vietnamese corporate
  and contract law, lab data handling.

## Conventions used throughout

Skills in this library follow the same shape, so they stay cheap to load and hard to misuse:

1. **Trigger first.** The `description` states exactly when the skill applies.
2. **Numbered steps with real commands**, not prose descriptions of commands.
3. **A pitfalls section.** Every entry is something that actually broke once.
4. **Verification before the claim.** A skill that says "done" must show the command and
   its output that proves it.
5. **Evidence over adjectives.** Numbers, hashes, file paths, exit codes.

## Notes

- Some skills were **absorbed from open-source projects**; the source repo and the exact
  diff are recorded in the relevant `references/` file rather than left implicit.
- Credentials, tokens, internal IDs and personal contact details have been **redacted**
  from this copy. Placeholders look like `<PASSWORD>`, `<API_KEY>`, `<SHEET_ID>`, `<EMAIL>`.
- A number of skills ship with Hermes by default and are included here for completeness;
  they are the work of the Hermes/Nous Research team, not this library's author.

## License

MIT for the skills authored here. Skills derived from third-party projects keep their
original licence — see the `references/` file inside each such skill.
