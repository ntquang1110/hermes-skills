---
name: design-critique
description: "Critique-first project design: collect requirements, critique architecture, map interaction flows, identify dependencies, then prioritize before writing any code."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, architecture, critique, planning, project-inception, workflow]
    related_skills: [plan, spike, test-driven-development]
---

# Design Critique — Critique-First Project Methodology

**Core principle: Collect → Critique → Map → Prioritize → THEN code.**

Never jump to implementation before the design has been actively criticized. A
design that hasn't been stress-tested will produce rework, missed requirements,
and wrong priorities.

**Workflow enforcement:** Every task MUST go through 6 phases in order:
📋 Planning → 🔍 Review → ✅ Approved → 🔵 In Progress → 🧪 Testing → ✅ Completed.
No phase may be skipped. No code may be written before the plan is approved.
See `references/task-workflow-phases.md` for detailed phase transitions and agent behavior.

This skill covers the **Phase 0** of any project: the work you do **before**
opening a single code file.

---

## When to use

- User says "create a new project" or "build a system/feature"
- User describes a system with multiple interacting components
- Any greenfield feature or architecture decision
- When the user's first instinct is to ask for code — use this instead

## When NOT to use

- The task is a well-understood, mechanical change (fix a bug, add a known field)
- The user explicitly says "just code it, I know what I want"
- The task is a one-shot script or utility (e.g. "download this CSV and plot it")

## The 5-Step Critique Process

### Step 1: 📋 Collect Everything

Gather ALL information before making any design decisions:

- **Goal**: What is this system supposed to DO? One sentence.
- **Users**: Who uses it? In what scenarios?
- **Constraints**: Platform, budget, time, skills, dependencies.
- **Existing context**: What already exists? What's the current pain?
- **Success criteria**: How do we know when it's done?

**Output**: A concise problem statement + constraint list.

**Pitfall**: Don't fill gaps with assumptions. If something is unclear, list it
as an open question, don't guess.

**Pitfall — Token-efficient codebase scan**: When critiquing a project that has
an existing codebase, resist reading every file. Use the 3-step scan instead:

1. **Map structure** — `git ls-tree -r HEAD --name-only` (1 call reveals stack,
   routing, data layer)
2. **Config layer only** — Read package.json, tsconfig, .env.example,
   entry points. ~80% of architecture at <10% token cost.
3. **Feature-gated deep read** — Search for the specific feature files,
   read only those. Read consumer before producer.

Skipping this step means burning tokens on implementation details before
understanding the architecture — the most expensive way to learn a codebase.

**Pitfall — Deployment surface**: When the user interacts from a different
device (phone, tablet) than where the server runs, `localhost` is inaccessible.
The Collect phase MUST clarify: "How will the user access the output?" —
if not on the same machine, plan for a public tunnel (localtunnel, ngrok,
cloudflared) or deploy to a reachable host. Getting this wrong means the
user sees nothing and you waste rounds debugging connectivity. See
`references/tunneling-public-urls.md` for quick Windows-friendly options.

#### Example (from meTelligent session)

> **Goal**: Trợ lý ảo nghe real-time, phân tích, phản biện, lưu memory, tạo task.
> **Modes**: Real-time listening + After-process transcript.
> **Platform**: Local-first, desktop (Windows/macOS), điện thoại xem qua web.
> **Cốt lõi**: Không phụ thuộc Claude, nhưng có thể dùng Claude API làm backend.

---

### Step 2: 🔍 Critique the Design Actively

This is the most important step. Be adversarial — look for what's **wrong** or
**missing**, not what's right.

For each component, ask:

| Question | Why it matters |
|----------|---------------|
| **What's the actual dependency order?** | You can't build the engine before the STT works. |
| **What's the latency budget?** | If Whisper takes 5s, "real-time" needs a streaming plan. |
| **Who speaks?** | No diarization → critique engine can't attribute statements. |
| **How does it fail gracefully?** | Mic dies → what happens? No internet → what happens? |
| **Is the tech stack optimal?** | PyAudio blocks on Windows. spaCy `vi` models are weak. |
| **What's the data privacy model?** | Audio is sensitive. Can it be local-only? |
| **What's missing entirely?** | Notifications? Auth? Cross-session memory? |

**Common critique categories to scan:**

- **Architecture**: Linear vs parallel vs event-driven; coupling between modules.
- **Latency**: Is "real-time" actually real-time? What's the slowest path?
- **Tech stack**: Library choices, platform compatibility, maintenance burden.
- **Dependencies**: The actual build-order, not the assumed one.
- **Completeness**: What features are listed but have no implementation plan?
- **Data model**: Can the schemas actually represent the domain?

**Output**: A critique document with:
- ❌ Critical issues (blockers)
- ⚠️ Important gaps (will cause problems)
- 💡 Opportunities (nice-to-have, worth noting)
- ✅ Strengths (what's solid)

**Pitfall**: Don't soften critiques. "This might be an issue" → "This is a
blocker because...". Be direct.

#### Example critiques (meTelligent session):

| Issue | Severity | Fix |
|-------|----------|-----|
| Linear pipeline → 5-7s latency | ❌ Critical | Event bus + thread pool |
| Critique 100% regex → too shallow | ❌ Critical | Rule + LLM hybrid |
| PyAudio blocking on Windows | ⚠️ Important | sounddevice (async) |
| No speaker diarization | ⚠️ Important | WhisperX (defer to P2) |
| No LLM integration | ⚠️ Important | Add optional LLM layer |

---

### Step 3: 🗺️ Map User-System Interaction Flows

For each major scenario, draw the **timeline interaction** between user and
system. This reveals:

- What the system does at each step
- What the user sees/hears at each step
- Where latency is acceptable vs not
- Missing states (error recovery, edge cases)

**Format**: Time-based interaction table.

```
THỜI GIAN   USER                      SYSTEM
─────────   ────                      ──────
T+0s        👤 Bắt đầu nói
                                     🎤 Mic capture ON
T+2s        👤 "Nội dung..."         ⚙️ VAD detect → Whisper
T+4s                                  📝 Interim transcript push
T+5s                                  📊 Analyzer: intent, entities
                                     ⚡ Critique check vs memory
T+6s                                  📌 Push critique to UI
```

**For each flow, verify:**
1. **Happy path** — everything works
2. **Degraded path** — slow network, bad audio, model error
3. **Edge cases** — silence, multiple speakers, code-switching languages

**Output**: 3-5 interaction flows, each with happy + edge cases.

---

### Step 4: 🔗 Identify Actual Dependencies

Map the **real** dependency graph — what blocks what.

**Bad dependency map (assumed order):**
```
Engine → STT → Memory → Critique → Tasks
```

**Good dependency map (actual order):**
```
Audio Capture (hardware)
  └── STT (needs audio)
       └── Analyzer (needs text)
            ├── Critique (needs Analyzer + Memory)
            ├── FactExtractor (needs Analyzer)
            │    └── Memory Store (needs facts)
            └── Summarizer (needs full text)
                 └── Task Manager (needs summary + analysis)
```

**Output**: A dependency DAG showing what blocks what. Use this to sequence
your build phases.

---

### Step 5: 🏆 Set True Priorities

Phase tasks by dependency, not by excitement.

| Phase | What | Why |
|-------|------|-----|
| **P0** | Foundation (data models, audio, STT, storage) | Everything depends on these |
| **P1** | Core value (analyzer, critique, tasks) | This is why the project exists |
| **P2** | Polish (profile, dashboard, diarization) | Nice after basics work |
| **P3** | Future (plugins, TTS, multi-session) | Only if P0-P2 are solid |

**Priority matrix:**

```
                  HIGH VALUE               LOWER VALUE
HIGH URGENCY  │  P0: non-negotiable    P1: important but deferrable
LOW URGENCY   │  P1: core features      P2-P3: future
```

**Output**: A numbered task list ordered by dependency, each with:\n- What it does (one line)\n- What it depends on\n- Why it's in this phase\n\n---\n\n## 🔴 HARD RULE: No Code Before Approval\n\nThis session's **strongest signal**: the user caught me coding without approval and\ncalled it out:\n\n> "ủa, anh đã duyệt gì đâu mà thực thi vậy"\n\n**The workflow is not optional. It is absolute.**\n\n```\nPlan → Send for Critique → Get PASS → Get User Approval → THEN Code\n```\n\nThe "write plan → get critique → get approval → code" sequence is an **unbreakable gate**. Not a suggestion.\n\n### Enforcement checklist before ANY code:\n\n1. ✅ Have I written a plan/spec/design doc?\n2. ✅ Have I sent it for review (CTO/CMO/etc.)?\n3. ✅ Did reviewer PASS it?\n4. ✅ Did the user (Quang) say "triển khai đi" or equivalent?\n5. ❌ If any answer is NO → DO NOT WRITE CODE. Stop and get approval.\n\n### Pitfall: "But it's obvious" trap\n\nEven when the task seems trivial, even when you're 100% sure the answer is\nclear — **do not skip the steps**. The user notices, and every violation erodes\ntrust. Write the plan, get the critique, get the approval, every single time.\n\n### Pitfall: "I already have the plan in my head" trap\n\nThe plan must be **written**, not just thought. Writing forces clarity. The\nreviewer can't critique what they can't read. The user can't approve what they\ncan't see.\n\n---\n\n## Deliverables

By the end of this skill, produce **one consolidated design document** with:

```
1. Problem statement + constraints
2. Architecture diagram (text/ASCII)
3. Critique results (critical issues, gaps)
4. User-system interaction flows (3-5 scenarios)
5. Dependency graph
6. Priority-ordered task list (P0 → P3)
7. Open questions / decisions needed
```

Save to `<project>/<NN>-design-critique.md`.

---

## User-Specific Preferences (this session)

- User initiates in **Vietnamese** → converse in Vietnamese
- User wants **practical, immediately-working** solutions over theoretical ones
- User prefers being shown **multiple options with tradeoffs** rather than a single recommendation
- User explicitly forbids jumping to code before design critique is complete
- User prefers **concise, structured output** (tables, lists) over paragraphs
- Output should be saved as `.md` files for version control + mobile viewing
- **Task workflow:** Every task MUST pass through Plan → Review → Implement → Test → Complete. No code before plan approval. No closing before test pass.

## Spin Planning — Quang's 2-week cycle format (chốt 16/08/2026)

When Quang asks "gửi lại plan / chốt lại đi / bây giờ cần làm gì" for a product project (meTelligent, TFO/ai-company, ...), present a **spin plan**, not a vague to-do list.

**Spin** = one complete development cycle, minimum **2 weeks**, ending with a usable, tested, releasable iteration. His words: *"plan ít nhất là 2 tuần để mình kết thúc 1 cái spin"*.

### Structure

- **Header**: spin name + mục tiêu 1 câu (what "done" means for this spin).
- **Tuần 1** = test thật + vá lỗi (real-device testing, bug fixes, resilience).
- **Tuần 2** = release + đóng spin (build release artifact, distribution, docs, bàn giao).
- Numbered table per week: `# | Việc | Done criteria` — every item carries a **measurable done criteria** (con số/kết quả verify), never "xong cơ bản".
- **End with blockers/questions needing his chốt** — e.g. test date on 2 devices, or *"xong 1 spin = dùng nội bộ ổn hay sẵn sàng cho người ngoài?"*. Ask the definition of done when ambiguous; don't guess.
- Close with one line: *"Anh duyệt plan này thì em bắt đầu tuần 1 ngay."*

### Before writing the plan — ground in reality

1. Read STATE files: `D:/Hermes Proj/.hermes-state/chat/_INDEX.md` → chat file → project file(s).
2. **Verify live system state**, never plan from memory: health endpoint (`curl localhost:<port>/api/health`), public URL (`curl -o /dev/null -w "%{http_code}" https://...`), latest artifacts (`ls -lat *.apk`).
3. Use `session_search` for recent context on the topic if STATE is stale (fresh session after daily reset = read STATE first, then search).
4. Only after the plan is approved does execution begin — same gate as the hard rule above.

---

## Extension: Scientific / Technical Protocol Critique

This section covers **critique of scientific experiments, technical protocols, and engineering designs** — not just software architecture. Use it when the deliverable is a procedure, a recipe, a treatment method, or a laboratory/pilot/production process rather than a codebase.

### When to use the Scientific Protocol mode

- User proposes a chemical, physical, or biological treatment method
- User asks you to review a multi-step experimental or production protocol
- User wants a "peer review" of their technical approach
- There are competing methods (dry vs wet, physical vs chemical, batch vs continuous)

### When NOT to use

- Pure literature summary without a proposed action
- Established standard methods (ASTM, TCVN, ISO) — assume they work
- User is just asking for background knowledge, not protocol design

### 5-Step Scientific Protocol Critique

#### Step 1: Identify the PHYSICAL OBJECT and its constraints

Before evaluating the protocol, know exactly what is being processed:

| Question | Why it matters |
|----------|---------------|
| **What material?** | Clay vs sand vs peat → totally different behavior |
| **What's valuable about it?** | If the process destroys the valuable component, it's worthless |
| **What's the target form?** | Solid powder vs liquid vs paste determines equipment |
| **What's the scale?** | Lab (g) vs pilot (kg) vs production (t) → cost changes 10-100× |
| **What are the input specs?** | Contaminant concentration ranges, moisture, particle size |

**Pitfall — Material confusion:** The most common mistake is applying a method designed for one material class to a different material. Example: thermal desorption (450°C) works for inorganic soil (low OM) but **destroys peat (high OM)** — losing the very humic/fulvic acids that give peat its commercial value. **Always check: is the method compatible with the material's valuable components?**

#### Step 2: Decompose the protocol into unit operations

List each step with:
- **What happens** at the physical/chemical level
- **What equipment** is needed (specific, not vague)
- **What temperature / pressure / time / pH** — concrete numbers
- **What goes in and what comes out** (mass balance — even rough)
- **Byproducts** (waste gas, wastewater, solid residue)

**Pitfall — Hidden steps:** Protocols often omit drying, cooling, transfer, cleaning, and analysis time. These can double the actual processing time.

#### Step 3: Run the ADVERSARIAL PEER REVIEW

This is a specific technique: **take on the persona of a DIFFERENT lead researcher who is skeptical by default**. Explicitly play devil's advocate. Announce the role switch so the user knows you're now evaluating your own prior work from a separate perspective.

For each unit operation, systematically attack:

| Attack vector | Example questions |
|---------------|------------------|
| **Logical consistency** | Do steps A and B contradict each other? (e.g. "grind fine for reaction" vs "separate coarse by density") |
| **Physical feasibility** | Does the claimed mechanism actually work at the claimed scale? (e.g. air table cannot separate sub-micron particles) |
| **Thermodynamic / kinetic feasibility** | Is there enough time/energy for the reaction? (e.g. biochar adsorption in 15 min dry mix → negligible) |
| **Safety** | Does any step create fire/explosion/toxic gas risk? (e.g. sulfur + ball mill = dust explosion) |
| **Material compatibility** | Does the process destroy the valuable component? (e.g. 450°C + peat = OM incineration) |
| **Cost realism** | Is equipment cost within an order of magnitude? (e.g. 5L furnace at 2.5M VND vs industrial kiln at 500M) |
| **Scale-up** | Does the lab method translate to production? (e.g. hand-sieving vs mechanical screening throughput) |

**Output format:** Table with Severity (CRITICAL/HIGH/MEDIUM/LOW), Issue, Step, and Proposed Fix.

#### Step 4: Separate theory from practice

Many protocols cite lab-scale results (g, hours, ideal conditions). Create a reality-check column:

| Parameter | Lab value | Realistic production value | Delta |
|-----------|-----------|---------------------------|-------|
| Batch size | 500 g | 1,000 kg | 2,000× |
| Reaction time | 30 min | 2-4 h (mass transport limits) | 4-8× |
| Equipment cost | 20M DIY | 200M-2B industrial | 10-100× |
| Energy per ton | 1.5M VND | 5-8M VND (losses + overhead) | 3-5× |
| Operator skill | PhD researcher | Semi-skilled worker | Gap |

**Pitfall — Cost underestimation:** First-pass cost estimates are typically 3-5× lower than reality because they omit: energy losses, waste treatment, QC testing, maintenance, labor overhead, and equipment depreciation. Apply a **minimum 3× multiplier** to first-pass operational cost estimates for any non-trivial process.

#### Step 5: Redesign — the critical review that improves

After identifying flaws, propose a **modified protocol** that:
- Removes steps that destroy value
- Replaces infeasible steps with practical alternatives
- Adjusts equipment to realistic cost/performance
- Re-estimates cost with the 3× multiplier
- Explicitly lists what MUST be tested experimentally before scaling

**Structure the redesign as a side-by-side comparison:**

| Attribute | Original | Redesigned | Why |
|-----------|----------|------------|-----|
| Step 3 | 450°C furnace | Biochar adsorption at 25°C | Saves OM, avoids HA/FA destruction |
| Step 1 | Dry grinding + S | Wet citric acid wash | No explosion risk, separates better |
| Equipment cost | 20M VND | 150M VND (pilot) | Realistic for real throughput |
| Throughput | 5 kg/day | 500 kg/day | Actually meaningful volume |

### Examples from this session

The heavy metals in peat soil protocol produced these critique findings:

| Issue | Severity | Lesson |
|-------|----------|--------|
| 450°C destroys humic acids (the valuable product) | 🔴 CRITICAL | Always check: does the process destroy what makes the material valuable? |
| Ball mill + sulfur + air = explosion risk | 🔴 CRITICAL | Mechanochemical reactions generate localized heat; sulfur autoignition is ~190°C |
| Air table can't separate sub-micron sulfides | 🔴 CRITICAL | Physical separation works only when density difference + particle size are both favorable |
| "Self-built" equipment lacks reproducibility | 🟠 HIGH | Lab results from ad-hoc equipment can't be scaled reliably |
| First cost estimate 3-5× too low | 🟠 HIGH | Apply 3× multiplier as a starting rule for operational costs |

See `references/heavy-metals-remediation.md` for the full domain knowledge captured from this session.

---

## Extension: Third-Party Claim / Content Critique

This section covers **critique of claims, posts, or marketing content that reference external sources (repos, products, tools)** — not just internal design decisions. Use it when the user asks you to review someone else's work, announcement, or product pitch.

### When to use

- User shares a social media post, press release, or article claiming something about a product/repo
- User asks "review bài này" — a Threads post, LinkedIn post, marketing copy
- User asks you to evaluate whether a product/tool is worth using
- Someone makes specific structural claims ("one folder per role", "ROLE.md + CONTRACT.md", "MIT")

### When NOT to use

- User just wants a simple opinion ("is this good?")
- The post is purely opinion/commentary with no verifiable claims
- The subject is behind a login wall and cannot be verified

### The 4-Step Source-Verification Critique

#### Step 1: Identify verifiable claims

Before forming any opinion, extract every concrete, verifiable claim from the post:

| Claim category | Examples |
|----------------|----------|
| Structure claims | "one folder per role", "ROLE.md + CONTRACT.md + SCHEDULE.md + routines/" |
| License claims | "MIT", "free for commercial use" |
| Metric claims | "60 scheduled routines", "11 agent harnesses" |
| Timing claims | "went open source at midnight", "Product Hunt same minute" |
| Install claims | "Install is two steps", "one command" |
| Behavior claims | "researches your business from your website", "stops to show drafts" |

**Output:** A numbered list of claims that can be verified or falsified by reading the actual source.

**Pitfall — Don't take claims at face value:** A well-written post can describe a repo structure that doesn't exist yet, or exaggerate an existing one. The post is marketing, not documentation.

**Pitfall — Read source FIRST, opine SECOND:** The user will call you out if you critique a post before verifying the source. When the user says "review bài này" or "đánh giá đi", your first response must be to find and read the actual source repo/paper. DO NOT start with your own analysis or opinion — start with `browser_navigate` to the repo. The user's signal: "Em đọc source xong đánh giá đi" means they want source-based critique, not armchair analysis. Follow Step 2 (Find and read the actual source) before forming any opinion.

#### Step 2: Find and read the actual source

Systematically locate the referenced artifact:

1. **Search for the repo** — GitHub API with keywords from the post (project name, role names, file patterns like `ROLE.md`, `CONTRACT.md`)
2. **Check press releases** — If the post references a company, search for their press release which often contains the actual repo URL
3. **Visit the project website** — Often has the GitHub link in the header
4. **Read the raw source** — Not the README, the actual ROLE.md, CONTRACT.md, SCHEDULE.md, and at least one routine SKILL.md
5. **Check the commit history** — How old is the repo? How many contributors? Real use or just-launched?

**Pitfall — README is marketing too:** The README is written to sell, same as the post. Read the actual source files. A README saying "2-step install" may hide npm install, API key setup, and browser sign-in as additional implicit steps.

**Pitfall — Age matters:** A repo with first commit 2 weeks ago and "running my business since [date]" that is only 3 weeks prior is not battle-tested. Check the commit graph.

#### Step 3: Compare claims vs reality

Build a comparison table:

| Claim (from post) | Reality (from source) | Verdict |
|-------------------|----------------------|---------|
| "8 AI Employees" | 8 markdown role config folders, not actual AI agents | Misleading framing |
| "MIT" | LICENSE file confirmed MIT | True |
| "60 scheduled routines" | 8 roles x ~7-8 routines each = 60 | True |
| "went open source at midnight" | First commit 2 weeks ago, press release today | Drama, not factual |
| "Product Hunt same minute" | No PH listing found | Unverifiable claim |
| "Install is two steps" | Requires npm global install + browser sign-in + agent login | Understated |
| "ROLE.md + CONTRACT.md + SCHEDULE.md" | All confirmed present with substantial content | True |

**Pitfall — "AI Employee" framing:** When a post calls markdown config files "AI Employees", check what the repo actually contains. If it's plain text files that configure the user's existing agent, the claim is exaggerated — the agent is the employee, not the config files.

#### Step 4: Identify the business model

After verifying the source, identify why the post was written:

- **Is it pure open source?** — No monetization, no upsells, no paid tiers
- **Is it open source + support?** — Free repo, paid consulting/training
- **Is it a lead funnel?** — Free repo that drives to a paid membership/product
- **Is it a press release?** — Paid PR distribution (EIN Presswire, PRWeb, etc.)

The business model is not a flaw, but it must be named so the user can evaluate the post's objectivity.

**Red flags to name:**
- Post says "free" but README has 5+ CTAs to a paid club
- Repo exists but the real value (install prompt, training, premium employees) is behind a paywall
- Multiple CTAs in one post (repo + live call + club) — diffused focus

**Pitfall — "Free" with conditions:** A repo is MIT but the install instructions say "get your install prompt in the club" — the free repo is technically usable but practically requires the paid membership to onboard. Name this gap.

### Example output format

From the AICO / AI Employees session:

```
Claims vs Reality:
- "8 AI Employees" -> 8 markdown role configs (misleading)
- "MIT" -> Confirmed
- "60 routines" -> Confirmed
- "2-step install" -> Actually 4-5 steps (understated)
- "midnight / same minute PH" -> Drama, unverifiable

Business model: Open source repo (MIT) -> lead funnel for Agent Ops Club ($499)
Post is marketing, repo quality is decent.
```

### Extension: Open-Source Tool Evaluation for Adoption

This section covers evaluating an open-source tool/repo for potential adoption in the
user's stack. It is **not** about verifying claims (see 4-Step Source-Verification above)
but about answering: *"Should we use this, borrow from it, or skip it?"*

#### When to use

- User sends a GitHub link and asks "review xem mình có dùng được gì không"
- User asks "em review source này, có áp dụng được gì không"
- User sends a link to a library, framework, tool, or skill repo for adoption assessment

#### The 5-Step Tool Evaluation

**Step 1: Read the source, not just the README**

Collect GitHub API metadata (stars, language, license, created/pushed dates) and the
actual repo structure. READMEs are marketing. Read the actual files:

- GitHub API: `curl -sL "https://api.github.com/repos/<owner>/<repo>"` -> stars, language,
  license, created_at, pushed_at
- Languages breakdown: `curl -sL "https://api.github.com/repos/<owner>/<repo>/languages"`
- Root directory: `curl -sL "https://api.github.com/repos/<owner>/<repo>/contents"`
- README: `curl -sL "https://raw.githubusercontent.com/<owner>/<repo>/main/README.md"`
- Key source files: SKILL.md, AGENTS.md, package.json, config files

**Step 2: Map the core architecture**

Extract the essential structure:

- What is this tool really doing? (not what it claims, what the files actually do)
- What ecosystem does it belong to? (Claude Code, Codex, VS Code, CLI, web...)
- What are its hard dependencies? (tmux, Python, Node, specific CLI tools...)
- What platform does it target? (macOS, Linux, Windows, cross-platform)

**Step 3: Build a compatibility matrix**

Compare against the user's existing stack. Use a table with three verdicts:
+ (Available, same or equivalent), / (Possible, gap exists but workaroundable),
X (Blocker, cannot replicate or incompatible):

| Aspect | Tool | User's Stack | Verdict |
|--------|------|-------------|---------|
| Platform | macOS/Linux (tmux) | Windows | X Blocker |
| Agent harness | Claude Code / Codex | Hermes | X Ecosystem mismatch |
| Sub-agent pattern | tmux + worktree isolation | delegate_task batch | + Equivalent |
| State persistence | Disk-based reconcile | State file protocol | + Equivalent |

**Step 4: Decide: Adopt, Borrow, or Reject**

Three possible outcomes:

| Decision | Criteria | Action |
|----------|----------|--------|
| **Adopt** | No blockers, fills a genuine gap, works with existing stack | Full integration plan |
| **Borrow** | Core tool rejected (platform/ecosystem mismatch) but has useful concepts | Extract 2-5 specific concepts, plan integration into existing skills |
| **Reject** | No value add, or existing stack already covers it | State why, move on |

When the decision is **Borrow**, identify each concept with:
- What the concept does in the original tool
- How it maps to the user's stack (which skill/module)
- Whether it requires a patch to an existing skill or a new skill

**Step 5: Present the decision clearly**

Structure the output:

```
**Decision**: [Adopt / Borrow / Reject]

**Why**:
[primary reason in one sentence]

**Compatibility matrix**:
[table]

**If Borrow: specific concepts to integrate**:
1. Concept A -> skill X: [what to add]
2. Concept B -> skill Y: [what to add]
3. ...

**If Reject: reason**:
[blocking reason 1]
[blocking reason 2]
[if borrow-worthy concepts exist anyway, list them]
```

#### Example output (from Wayfinder review, 2026-09-20)

```
Decision: Reject (borrow 3 concepts)

Why: Wayfinder requires GitHub/Linear as tracker, user uses Trello.
Integration overhead > value.

Compatibility matrix:
- Issue tracker: GitHub/Linear vs Trello -> X Mismatch
- Plan format: Issue body vs .hermes/plans/ -> / Similar, different format
- Blocking edges: Native tracker vs Trello labels -> X No native blocking

Borrowed concepts:
1. Fog of war -> plan skill: section for items not yet sharp enough to task
2. Decision log -> plan skill: one-line ADR per key decision
3. Questions vs tasks -> plan skill: never mix in one numbered list
```

#### Example output (from FirstMate review, 2026-09-20)

```
Decision: Reject

Why: Windows incompatible (tmux dependency), designed for Claude Code/Grok, not Hermes.

Compatibility matrix:
- Platform: macOS/Linux (tmux) vs Windows -> X Hard blocker
- Harness: Claude Code/Pi/Grok vs Hermes -> X Ecosystem mismatch
- Sub-agent: tmux + worktree vs delegate_task -> + Hermes already has
- Watcher: bash daemon vs process() + cron -> + Equivalent

Borrowed concepts (not enough to patch: already covered):
- Scout vs Ship task shape: already partially covered by plan skill
- Project modes: already covered by trello-workflow card lifecycle
```

#### Pitfalls

- **Don't just describe the tool.** The user wants an applicability verdict, not a summary.
  Every paragraph must answer "should we use this?": if it doesn't, cut it.
- **Don't start with opinion.** Read the source first (Step 1), then evaluate (Steps 2-5).
- **A borrow outcome requires specific action.** If you borrow concepts, say which skills
  to patch and what to add. Vague "we could learn from this" is not useful.
- **Hard blockers > nice features.** A tool with 10 amazing features but Windows-only
  dependency is still rejected. State the blocker first, then list what is good about it.
- **"Equivalent" is not a blocker.** If the user's stack already has the capability,
  say + and move on: do not recommend adopting a whole tool for what one Hermes command
  already does.

### When the source is inaccessible

Sometimes the claimed source doesn't exist or can't be found:

1. No GitHub results after multiple search strategies -> name it
2. Repo exists but is empty or has a different structure -> name it
3. Post deleted or content changed -> say so
4. Behind login wall -> say "cannot verify, source is private"

Never fabricate a verdict when you couldn't read the source. Say "Could not verify — no public repo found matching this description."

---

## Extension: Verifying Delegated Research Output

When research comes back from **subagents / delegated batches** (or any external
worker), the returned summary is a **self-report, not a verified fact**. A child
that says "102 PMIDs verified by reading abstracts, file written, 145 KB" can be
wrong on every one of those three. Run this 4-step check **before** repeating any
of its numbers to the user.

### Step 1 — Stat the artifacts

Claimed path + claimed size must match reality. A missing file, or a size far off
the claim, means the summary describes work that did not land.

```python
import os
print(os.path.exists(p), os.path.getsize(p) if os.path.exists(p) else None)
```

Byte size ≠ char count for Vietnamese/multibyte text (83,916 bytes ≈ 75,031
chars). Compare like with like before calling a size wrong.

### Step 2 — Spot-check citations against an authoritative index

Never trust "all citations verified". Sample the 10-15 most load-bearing
identifiers and re-resolve them yourself. For biomedical PMIDs the fastest
deterministic check is the Europe PMC REST API (JSON, no key, script in
`references/delegated-research-verification.md`):

```
https://www.ebi.ac.uk/europepmc/webservices/rest/search
  ?query=EXT_ID:<pmid>%20AND%20SRC:MED&format=json&resultType=core&pageSize=1
```

Compare the returned **title + journal + year** against what the artifact claims
for that citation. A PMID that resolves to an unrelated paper is the signature of
a fabricated or mis-attributed reference. Existence alone is not enough.

### Step 3 — Hunt for superseding documents (the step everyone skips)

A claim can be **true at the moment of its cited document and false today**. This
is the highest-value check, and the one no citation spot-check will ever find.

- **Legal / regulatory:** after confirming the cited document exists, search
  explicitly for instruments that amend, suspend, or cancel it. Query patterns
  that work: document number + `sửa đổi`, `bãi bỏ`, `thay thế`, `dừng thực hiện
  thủ tục hành chính`, `VBHN`. Prefer the **consolidated ("nội dung hợp nhất")**
  view — it shows currently-effective text, not the original.
- **Standards / APIs / pricing:** check for a revision or changelog entry dated
  *after* the citation.
- **Anything tagged as hard fact (F):** ask "is there a later document that
  changed this?" before repeating it.

Session case: an analysis tagged a requirement of decree `NĐ 32/2026/NĐ-CP`
(21/01/2026) as `[F]` — accurate as written. A later resolution
`NQ 66.19/2026/NQ-CP` (18/5/2026) had **stopped that entire procedure**. The
artifact's operational conclusion was inverted (barrier went down, not up). Only
the superseding-document search found it.

### Step 4 — Patch in place, marked; never silently rewrite

The file may already have been read or forwarded, so make the correction visible:

1. Add a **correction banner near the top** (`## ⚠️ ĐÍNH CHÍNH <date>`) with a
   table: *original (wrong)* → *correct*, plus the sources you used.
2. Mark each corrected line inline (`⚠️ [ĐÃ SỬA — xem banner]`) instead of
   deleting the original claim — the trail is the value.
3. Add the newly-found sources to the reference list.
4. **Re-scan for every remaining occurrence** of the wrong fact. One superseded
   claim typically appears in 5-9 places (exec summary, tables, action lists,
   risk register, appendix). Grep the keyword, not the sentence, and check each
   surviving hit is either fixed or deliberately marked historical. Expect hits
   inside the banner itself (it quotes the old claim) — those are fine.
5. Commit the correction as its own commit so the fix reads as a fix.

### Report the child's negatives too

The child's **negatives** are often more valuable than its positives: sections
marked `KHÔNG CÓ NGUỒN` / "no source found", and anywhere it self-reported a gap.
Those are the honest edges of the evidence — usually the most decision-relevant
part — and exactly what a summary tends to under-report.

---

## Reference files

- `references/delegated-research-verification.md` — Runnable recipes for the section above: artifact stat check, Europe PMC PMID spot-check script, superseding-document query patterns with the `NQ 66.19/2026/NQ-CP` case study, and the in-place correction sweep

- `templates/spin-plan.md` — Template 2-tuần spin plan (Quang duyệt format): Tuần 1 test/fix + Tuần 2 release, mỗi việc có done criteria đo được, kết bằng blocker cần anh chốt
- `references/metelligent-case-study.md` — Full design critique transcript from the meTelligent session
- `references/tunneling-public-urls.md` — Tunnel options for cross-device development
- `references/heavy-metals-remediation.md` — Domain knowledge: As, Pb, Hg, Cd removal from soil (dry, wet, hybrid methods), equipment specs, cost analysis, and quality standards for agriculture/feed applications
- `references/task-workflow-phases.md` — Strict Plan→Review→Approve→Implement→Test→Complete workflow enforcement with phase transitions, agent behavior per phase, and task store schema
- `references/aico-ai-employees-pattern.md` — Notable agent configuration pattern from AICO / AI Employees: ROLE.md + CONTRACT.md + SCHEDULE.md + routines/, AGENTS.md convention, browser lane system, guardrails. Reviewed Sep 20, 2026
- `references/ocr-alibaba-pattern.md` — Open Code Review (Alibaba): hybrid deterministic+LLM architecture, ~1/9 token savings, delegation mode. Reviewed Sep 20, 2026
- `references/sol-pi-nvidia-pattern.md` — SoL-Pi (NVIDIA): auto-research loops, 4 harness mechanisms, 44-49% token reduction. Reviewed Sep 20, 2026
- `references/ceo-dashboard-review.md` — Framework review dashboard góc nhìn C-level + UX (TFO 2026-08): 5 câu hỏi trước khi review, layout CEO-first đã user duyệt (4 KPI clickable, Hôm nay, Cần chú ý, goal editable, nút ghi âm nổi), data model projects/issues/timeline/kanban, pitfalls (không tự xóa Org Chart khi chưa duyệt, goal tiếng Việt phải test bằng Python không phải bash curl, test 3 tầng node+API khi browser không sẵn)
- `references/neumorphism-design-system.md` — Complete Cool Grey Neumorphism design system: tokens (colors, shadows with RGBA, typography, radius), shadow system (extruded/inset/deep), component styling (buttons, cards, inputs), animation specs (300ms, translateY, float), accessibility (contrast, focus), anti-patterns checklist. Load when user requests "neumorphism", "soft UI", or "cool grey" aesthetic for HTML artifacts.

---

## Related Skills

| Skill | When to use |
|-------|-------------|
| `plan` | After critique: write implementation plan with bite-sized tasks |
| `spike` | For a single uncertain technical assumption from the critique |
| `test-driven-development` | During implementation: RED-GREEN-REFACTOR |
| `deterministic-llm-hybrid` | Architecture pattern: deterministic preprocessing before LLM calls |
