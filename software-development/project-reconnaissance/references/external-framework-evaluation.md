# External Framework / Agent-Tool Evaluation (adoption decision) — worked example: penguin-harness

When user says "phân tích source này cho anh" / "evaluate this repo" about an EXTERNAL
tool or framework (not a project we own), the goal is an adoption verdict, not an
onboarding map. Distinct from project-reconnaissance's normal audit: we are deciding
whether to invest, not preparing to work inside.

## Worked example (2026-08-07): github.com/Prism-Shadow/penguin-harness

"Automated Agent Builder. Create Self-Evolving Agents in One Click" — TS monorepo,
984 stars, Apache-2.0, created 2026-07-19 (3 weeks old). Author = Yaowei Zheng
(LlamaFactory author).

### Step 1 — GitHub API triage BEFORE clone (cheap, no clone needed)

```bash
curl -s -m 15 "https://api.github.com/repos/OWNER/REPO" | python -c "import json,sys; d=json.load(sys.stdin); [print(f'{k}: {v}') for k,v in d.items() if k in ['full_name','description','language','stargazers_count','forks_count','default_branch','created_at','pushed_at','license','size']]"
curl -s -m 15 "https://api.github.com/repos/OWNER/REPO/contents/"  # root file tree
```

Signals from metadata: **age vs stars velocity** (3 weeks + 984 stars = viral, but
also immature), language, license (Apache-2.0 vs AGPL matters for commercial reuse),
last push date (actively maintained?).

### Step 2 — Shallow clone + scale measurement

```bash
git clone --depth 1 https://github.com/OWNER/REPO.git
find packages -name "*.ts" | xargs wc -l | tail -1   # LOC per package → effort to fork/tune
```

LOC per package tells you if this is forkable (10k) or a big commitment (100k+).

### Step 3 — Read in this order (batch parallel reads)

1. README (claims, supported models, install story, roadmap)
2. package.json + pnpm-workspace / workspace config (packages, scripts, deps)
3. Core engine files (entry point, session/loop, LLM adapter, tool registry)
4. The "wow" feature's implementation (self-evolution skills, benchmark loop)
5. Security posture (exec/command tool, path-traversal guards, vault/secret handling)
6. Changelog (version history, release cadence, pipeline failures)

### Step 4 — VERIFY CLAIMS before repeating them

The single most important step for AI-tool repos:
- README claims "1/70 cost of Claude Code" → check roadmap: "Public release of the
  benchmark suite" unchecked → **claim is NOT independently verifiable. Say so.**
- Don't take star count = quality. Check: version number (0.2.x = pre-1.0),
  unsigned installers, publish pipeline failures mentioned in changelog
  (penguin-harness 0.1.4 changelog admits a failed publish job).

### Step 5 — Compare against user's CURRENT stack (table)

| Dimension | Current (Hermes/ai-company) | Candidate |
|---|---|---|
| Multi-provider | OmniRoute LAN + opencode-go | AgentHub, 1000+ presets |
| Self-evolving | manual via skills | built-in benchmark→AGENTS.md edit loop |
| Maturity | stable | 3 weeks old |
| Cost | provider-dependent | claim cheaper, unverified |

### Step 6 — Verdict framework (not a summary, a decision)

Say explicitly: **"Đáng theo dõi, chưa đáng nhảy tàu"** or equivalent — with the
specific conditions that would change the verdict (e.g. "wait for benchmark suite
public + 1-2 more releases for API stability"). Name what the candidate has that the
current stack lacks (the adoption pull), and what blocks adoption today.

## Reusable pitfalls

- **Star count is a hype signal, not quality** — pair with age + version + changelog.
- **Unverifiable benchmark claims are the norm in AI-tool READMEs** — flag them
  explicitly instead of repeating as fact.
- **Monorepo = check each package.json**, count packages, LOC per package.
- **Deep links**: clone, don't just browse — grep needs local files.
- Present verdict as a decision with re-check conditions, not a neutral walkthrough.

## No-clone fast path (2026-08-15 — deepseek-harness case)

Cheaper than cloning when the repo is a well-structured monorepo and you only need an adoption verdict:

```bash
# 1. Metadata via API (also tells you default_branch — do NOT assume main)
curl -sL "https://api.github.com/repos/OWNER/REPO" | python -c "import json,sys; d=json.load(sys.stdin); [print(f'{k}: {v}') for k,v in d.items() if k in ['description','stargazers_count','default_branch','language','license','updated_at']]"

# 2. README from the DEFAULT branch — main may 404
curl -sL "https://raw.githubusercontent.com/OWNER/REPO/master/README.md"

# 3. Architecture without clone: root listing, then raw reads
curl -sL "https://api.github.com/repos/OWNER/REPO/contents/"   # packages/, apps/, docs/ → kiến trúc ngay
curl -sL "https://raw.githubusercontent.com/OWNER/REPO/master/docs/architecture.md"
curl -sL "https://raw.githubusercontent.com/OWNER/REPO/master/packages/<pkg>/README.md"
```

Reading order that worked: root README → root contents listing → docs/architecture.md →
READMEs of the capability packages relevant to the question (sandbox, subagent, skill, mcp,
schedule, compaction) → BENCHMARK.md if present. No clone needed for the verdict.

### Bounded live boot test (chỉ khi định chạy thật)

- `npx -y <pkg> web` cho preview tool: đặt budget cứng (~2-3 phút), poll port
  (`netstat -ano | grep <PORT>`) thay vì chờ process.
- **Pitfall:** pipe qua `| head -N` buffer hết output — không thấy gì cho tới khi đủ N dòng
  hoặc EOF. Redirect ra file hoặc poll port.
- **Pitfall:** npx cài package lạ có thể treo âm thầm (npm cache 0 bytes, không output).
  Kiểm tra `du -sh ~/AppData/Local/npm-cache/_npx` — trên máy Quang cache sẵn 787MB trên
  ổ C đang kẹt. Không boot trong budget → kill, báo trung thực "chưa boot được". Dev-preview
  mà không chạy được chính là một phần verdict.
- Không bao giờ báo "chạy được" khi chưa verify. Boot test thất bại = bằng chứng chưa chin.

## Verdict framing cho Quang (fit proposal)

- Bảng fit 3 cột: **Pattern dsh → Áp dụng vào đâu** — KHÔNG thay Hermes, KHÔNG build client
  product trên preview, chỉ học pattern.
- "Steal patterns, not code": với tool cùng class (agent harness), đừng đu theo stars hype,
  hãy rút pattern kiến trúc về áp dụng cho hệ thống mình (xem deepseek-harness case).
