---
name: plan
description: "Plan mode: write an actionable markdown plan to .hermes/plans/, no execution. Bite-sized tasks, exact paths, complete code."
version: 2.1.0
author: Hermes Agent (writing-craft adapted from obra/superpowers)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [planning, plan-mode, implementation, workflow, design, documentation]
    related_skills: [design-critique, subagent-driven-development, test-driven-development, requesting-code-review]
---

# Plan Mode

Use this skill when the user wants a plan instead of execution.

## Prerequisites

**Do not skip the design phase before writing an implementation plan for greenfield projects.**

When the user says "tạo dự án mới" (new project), "build a system", or anything involving multiple components, follow this sequential workflow:

### Phase 0: Design Phase (MANDATORY — no coding yet)

Do NOT code, create files, or write implementation plans until the user has reviewed and approved all three design deliverables below.

**Deliverable 1 — Architecture Diagram (HTML)**
Create a standalone HTML file showing the system architecture as a visual flow diagram:
- Input → Processing → Storage → Output
- All modules and their relationships
- Data flow arrows between components
- Save as `NN-architecture-overview.html` in the project folder

**Deliverable 2 — User-System Interaction Flow (HTML or MD)**
Map concrete interaction scenarios with timeline (T+0s, T+2s, etc.):
- Every user action → system response → output at each stage
- Include real examples with realistic data (not placeholder text)
- Cover ALL modes of operation (real-time, batch, search, etc.)
- Save alongside the architecture diagram

**Deliverable 3 — Dependency-Priority Matrix**
Analyze the actual dependency graph of all components:
- List every module/feature with its dependencies
- Identify what blocks what
- Re-sort tasks by dependency order (not by perceived importance)
- Assign priority (P0/P1/P2) based on actual dependency chain
- Present as a table so the user sees WHY P0 comes first

**Gate:** Present all three deliverables to the user. Do NOT proceed to implementation planning until the user has reviewed and approved the design. Only after collecting info, critiquing the design, mapping interaction flows, and identifying correct dependencies should you move to writing an implementation plan.

### When to use the full design phase

MANDATORY when:
- "Create a new project", "build a system", "làm dự án mới"
- Multiple modules/components with unclear interactions
- Any real-time or streaming requirement
- First time working with this domain or tech stack
- User hasn't specified architecture details (they need critique help)

SKIP (go straight to `plan`) when:
- Well-understood feature with clear requirements
- User explicitly says "just plan the implementation" or "cứ code đi"
- Bug fix or mechanical change with no design decisions

## Core behavior

For this turn, you are planning only.

- Do not implement code.
- Do not edit project files except the plan markdown file.
- Do not run mutating terminal commands, commit, push, or perform external actions.
- You may inspect the repo or other context with read-only commands/tools when needed.
- Your deliverable is a markdown plan saved inside the active workspace under `.hermes/plans/`.

## Output requirements

Write a markdown plan that is concrete and actionable.

Include, when relevant:
- Goal
- Current context / assumptions
- Proposed approach
- Step-by-step plan
- Files likely to change
- Tests / validation
- Risks, tradeoffs, and open questions
- Decision log (borrowed from wayfinder 2026-09-20: one line per key decision, why X over Y)
- Fog of war (borrowed from wayfinder 2026-09-20: in-scope but not yet sharp enough to task out; graduates into tasks later, never forced into premature spec)
- Open questions kept in their own list, separate from tasks (questions block decisions, tasks execute decisions)

### Fog of war, decision log, questions vs tasks

Borrowed from mattpocock wayfinder review (2026-09-20). Wayfinder itself was rejected
(Trello is our tracker, not GitHub/Linear), but these 3 concepts are tracker-agnostic:

- **Fog of war:** a `## Fog of war` section at the end of the plan for items that are
  in scope but cannot be stated sharply yet. Do not pre-slice fog into task-sized pieces.
  One fog patch may graduate into several tasks, or none, once the frontier reaches it.
  Test: if you can state the question precisely now, it is a task or open question;
  if not, it is fog.
- **Decision log:** a `## Decision log` section, one line per decision
  (`<decision>: <why X over Y>`). This is the plan-level ADR. Never restate a decision
  in multiple places; the log is the single source.
- **Questions vs tasks:** never mix them in one numbered list. Tasks declare what to do
  and their blocking edges. Questions declare what decision is blocked and who answers it.
  A task blocked by an unanswered question stays sequenced after it, not parallel to it.

If the task is code-related, include exact file paths, likely test targets, and verification steps.

## Save location

Save the plan with `write_file` under:
- `.hermes/plans/YYYY-MM-DD_HHMMSS-<slug>.md`

Treat that as relative to the active working directory / backend workspace. Hermes file tools are backend-aware, so using this relative path keeps the plan with the workspace on local, docker, ssh, modal, and daytona backends.

If the runtime provides a specific target path, use that exact path.
If not, create a sensible timestamped filename yourself under `.hermes/plans/`.

## Interaction style

- If the request is clear enough, write the plan directly.
- If no explicit instruction accompanies `/plan`, infer the task from the current conversation context.
- If it is genuinely underspecified, ask a brief clarifying question instead of guessing.
- After saving the plan, reply briefly with what you planned and the saved path.

---

# Writing the Plan Well

The rest of this skill is the craft of authoring a *good* implementation plan — the content that goes inside the markdown file above.

## Overview

Write comprehensive implementation plans assuming the implementer has zero context for the codebase and questionable taste. Document everything they need: which files to touch, complete code, testing commands, docs to check, how to verify. Give them bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume the implementer is a skilled developer but knows almost nothing about the toolset or problem domain. Assume they don't know good test design very well.

**Core principle:** A good plan makes implementation obvious. If someone has to guess, the plan is incomplete.

## When a Full Implementation Plan Helps

**Always use before:**
- Implementing multi-step features
- Breaking down complex requirements
- Delegating to subagents via subagent-driven-development

**Don't skip when:**
- Feature seems simple (assumptions cause bugs)
- You plan to implement it yourself (future you needs guidance)
- Working alone (documentation matters)

## Bite-Sized Task Granularity

**Each task = 2-5 minutes of focused work.**

Every step is one action:
- "Write the failing test" — step
- "Run it to make sure it fails" — step
- "Implement the minimal code to make the test pass" — step
- "Run the tests and make sure they pass" — step
- "Commit" — step

**Too big:**
```markdown
### Task 1: Build authentication system
[50 lines of code across 5 files]
```

**Right size:**
```markdown
### Task 1: Create User model with email field
[10 lines, 1 file]

### Task 2: Add password hash field to User
[8 lines, 1 file]

### Task 3: Create password hashing utility
[15 lines, 1 file]
```

## Plan Document Structure

### Header (Required)

Every plan MUST start with:

```markdown
# [Feature Name] Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

### Task Structure

Each task follows this format:

````markdown
### Task N: [Descriptive Name]

**Objective:** What this task accomplishes (one sentence)

**Files:**
- Create: `exact/path/to/new_file.py`
- Modify: `exact/path/to/existing.py:45-67` (line numbers if known)
- Test: `tests/path/to/test_file.py`

**Step 1: Write failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify failure**

Run: `pytest tests/path/test.py::test_specific_behavior -v`
Expected: FAIL — "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify pass**

Run: `pytest tests/path/test.py::test_specific_behavior -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## Writing Process

### Step 1: Understand Requirements

Read and understand:
- Feature requirements
- Design documents or user description
- Acceptance criteria
- Constraints

### Step 2: Explore the Codebase

Use Hermes tools to understand the project:

```python
# Understand project structure
search_files("*.py", target="files", path="src/")

# Look at similar features
search_files("similar_pattern", path="src/", file_glob="*.py")

# Check existing tests
search_files("*.py", target="files", path="tests/")

# Read key files
read_file("src/app.py")
```

### Step 3: Design Approach

Decide:
- Architecture pattern
- File organization
- Dependencies needed
- Testing strategy

### Step 4: Write Tasks

Create tasks in order:
1. Setup/infrastructure
2. Core functionality (TDD for each)
3. Edge cases
4. Integration
5. Cleanup/documentation

### Step 5: Add Complete Details

For each task, include:
- **Exact file paths** (not "the config file" but `src/config/settings.py`)
- **Complete code examples** (not "add validation" but the actual code)
- **Exact commands** with expected output
- **Verification steps** that prove the task works

### Step 6: Review the Plan

Check:
- [ ] Tasks are sequential and logical
- [ ] Each task is bite-sized (2-5 min)
- [ ] File paths are exact
- [ ] Code examples are complete (copy-pasteable)
- [ ] Commands are exact with expected output
- [ ] No missing context
- [ ] DRY, YAGNI, TDD principles applied

## Principles

### DRY (Don't Repeat Yourself)

**Bad:** Copy-paste validation in 3 places
**Good:** Extract validation function, use everywhere

### YAGNI (You Aren't Gonna Need It)

**Bad:** Add "flexibility" for future requirements
**Good:** Implement only what's needed now

```python
# Bad — YAGNI violation
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.preferences = {}  # Not needed yet!
        self.metadata = {}     # Not needed yet!

# Good — YAGNI
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
```

### TDD (Test-Driven Development)

Every task that produces code should include the full TDD cycle:
1. Write failing test
2. Run to verify failure
3. Write minimal code
4. Run to verify pass

See `test-driven-development` skill for details.

### Frequent Commits

Commit after every task:
```bash
git add [files]
git commit -m "type: description"
```

## Common Mistakes

### Vague Tasks

**Bad:** "Add authentication"
**Good:** "Create User model with email and password_hash fields"

### Incomplete Code

**Bad:** "Step 1: Add validation function"
**Good:** "Step 1: Add validation function" followed by the complete function code

### Missing Verification

**Bad:** "Step 3: Test it works"
**Good:** "Step 3: Run `pytest tests/test_auth.py -v`, expected: 3 passed"

### Missing File Paths

**Bad:** "Create the model file"
**Good:** "Create: `src/models/user.py`"

## Execution Handoff

After saving the plan, offer the execution approach:

**"Plan complete and saved. Ready to execute using subagent-driven-development — I'll dispatch a fresh subagent per task with two-stage review (spec compliance then code quality). Shall I proceed?"**

When executing, use the `subagent-driven-development` skill:
- Fresh `delegate_task` per task with full context
- Spec compliance review after each task
- Code quality review after spec passes
- Proceed only when both reviews approve

## Remember

```
Bite-sized tasks (2-5 min each)
Exact file paths
Complete code (copy-pasteable)
Exact commands with expected output
Verification steps
DRY, YAGNI, TDD
Frequent commits
```

**A good plan makes implementation obvious.**
