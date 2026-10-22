---
name: github-branch-review
description: "Review a remote GitHub branch or PR without cloning."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [github, code-review, api, no-clone, branch-audit, rest]
    related_skills: [volden-ops-web, requesting-code-review, web-app-security-review, github-auth]
---

# GitHub Branch Review (remote, no clone)

Review someone else's branch or PR straight from the GitHub REST API. No clone, no
working tree, no merge conflicts. You read the diff and the files **at the ref**.

## Trigger

- "review branch X", "review PR #12", "branch này khác main như nào", "audit branch"
- User drops a repo + branch name and expects a findings report
- Deciding whether a branch is safe to merge, should be deleted, or needs a rebase first

**Not this skill:** reviewing your *own* uncommitted work before a commit. That is
`requesting-code-review`. This skill is for changes that already live on GitHub.

## Step 0 — get a token

Hermes keeps a GitHub PAT base64-encoded in the active profile's `.env`. `gh` being
installed-but-not-logged-in does not matter; the PAT talks to the API directly.

```bash
ENVF="$HOME/AppData/Local/hermes/.env"   # or $HERMES_HOME/.env
export GITHUB_TOKEN=$(python -c "
import base64
v=''
for line in open(r'$ENVF',encoding='utf-8',errors='ignore'):
    if line.startswith('GITHUB_PAT_B64='): v=line.split('=',1)[1].strip()
print(base64.b64decode(v).decode())
")
curl -s  -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
curl -sI -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | grep -i x-oauth-scopes
```

Report the login and the scopes. **Never echo the token** — print the prefix and length
only. If the scopes are wider than the job (classic PAT dragging `admin:org` and
`workflow` for a read-only review), say so and recommend a fine-grained token limited to
the repos in question.

Full endpoint set: `references/github-api-recipes.md`.

## Step 1 — inventory

Three calls orient you: repos (`affiliation=owner,collaborator,organization_member`),
branches per repo, open PRs per repo. Run them in one shell loop, not one turn each.

## Step 2 — triage before reading code

For each branch call `compare/{default}...{branch}` and read `ahead_by`, `behind_by`,
file count, additions, deletions.

| Shape | Meaning | Action |
|---|---|---|
| `ahead_by=0` | Every commit already in the default branch | Branch is dead. Recommend delete. Do not review it. |
| `ahead_by>0`, `behind_by` large | Stale | Review the diffstat, but warn that the diff carries reverse noise. Rebase first for a clean read. |
| both `>0` | Will conflict on merge | Say so before reviewing. Conflicts are a separate job. |

Do not burn tokens reviewing a branch that is fully merged. "2 of your 4 branches are
dead, here are their names" is often the highest-value line in the whole report.

## Step 3 — pull the diff

`compare` returns a `patch` per file, usually enough on its own. GitHub omits `patch` for
large files; then read the whole file at the ref:

```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.raw" \
  "https://api.github.com/repos/$OWNER/$REPO/contents/$PATH?ref=$BRANCH"
```

Pull config files at the ref too (`tsconfig.json`, `package.json`, CI config). They decide
what the project's own gates actually cover, which changes how much a green build means.

## Step 4 — verify at the ref, never from the description

**The single most important rule.** A PR body, a branch name, and a CHANGELOG entry are
claims, not evidence. The author wrote what they *intended*; the review is about what the
code *does*.

Worked failure mode: the CHANGELOG said the auto-advance path had been fixed to load the
record, and the diff did add the load. Reading `api/app.ts` at the ref showed the
notification was still gated on a request field (`if (stage && stage !== current?.stage)`)
that the auto path never sends, and reading the frontend caller at the same ref confirmed
the request body carried only the URL fields. The fix worked; the side effect it was
supposed to trigger was still skipped. That finding exists only because the source at the
ref was read.

Method: for every behavioural claim, trace to the actual call site at the ref. "The diff
looks right" is not a review.

## Step 5 — what to hunt

Rank findings by severity. These classes keep paying off on Express + Supabase + React
codebases; they generalize well beyond them.

| Class | What to look for | Why it bites |
|---|---|---|
| Symptom vs root cause | The same one-line fix appears a 2nd or 3rd time in the log (one more field added to a whitelist, one more `if`). | The next occurrence is guaranteed. Ask for the class-level guard instead. |
| Empty / no-op payload | A dynamic payload reaches `update(x).eq(id).select().single()`. An empty payload returns zero rows and `.single()` errors (`Cannot coerce the result to a single JSON object` on PostgREST) = HTTP 500. | Any unlisted field produces a 500 instead of a 400. Should be caught before the DB call. |
| Side effect bypassed | State is written in one place while the notifier / audit / webhook is gated elsewhere. | Silent state drift. The record advances and nobody is told. |
| Authz parity | Route has `requireAuth` only while a `requireRole` helper already exists and is used on sibling routes. Field-level writes with no role check. | Any logged-in user can rewrite money or ownership fields. Also compare UI role flags against API middleware (a separate `admin_role` beside `admin` is the classic miss). |
| Type-check coverage | Read `tsconfig.json` `include` / `exclude`. If the backend dir is excluded, `tsc --noEmit` and `npm run build` prove nothing about it. | Real narrowing and type errors never surface. |
| Non-atomic multi-write | Two sequential updates where the second can fail. | Inconsistent records, no rollback, no retry. |
| Dead code in the fix | A `const x = ...` introduced and never used. | Marker of a half-finished refactor; the missing logic is usually nearby. |
| Silent client failure | `await` inside an async callback (`FileReader.onloadend`, `setTimeout`, a detached `.then`) that the enclosing `try` cannot catch. | Failed uploads and saves look successful to the user. |
| Recomputed derived value | `new Date()` called twice instead of reusing the value written to the DB. | The response disagrees with the stored data. |
| External-resource assumption | A link that only resolves if a doc or object is public, with no fallback and no error surface. | User gets a login page saved as `.pdf`, and no explanation. |

## Step 6 — report shape (user convention)

1. **Findings table first**, ranked: `# | mức | vấn đề | file:line`. Severity labels in
   Vietnamese: `Nặng` / `Vừa` / `Nhẹ`.
2. **Detail per finding**: the mechanism, the exact `file:line`, and a concrete fix in a
   code block. Not "should add validation" — show the guard.
3. **A short "Điểm được" block** naming what is actually correct in the branch. Facts, no
   applause.
4. **Close with "việc anh cần quyết"** — the decisions that are the user's, not yours:
   delete dead branches, rebase stale ones, change token scope, whether to open a PR.
5. Vietnamese with full diacritics. Address the user as `anh`, yourself as `đệ`. No em
   dash. Minimal bold.

The report is a deliverable, not a narration of your process. State a finding only when
you have the file and line to back it. Never claim you verified something you only read
in the diff.

## Offering the next step

After the report, name what is left and offer it in one line: review the bigger branch,
post findings as inline PR comments (the PAT often carries write scope), or stop. Do not
pad with a recap of the method.

## Pitfalls

- **Reviewing a merged branch.** Check `ahead_by` first. A dead branch is a deletion
  recommendation, not a review.
- **Trusting the CHANGELOG or PR body.** Step 4.
- **Reading the diff only.** A diff shows changed lines; the bug is often in the
  unchanged control flow around them. Read the enclosing function at the ref.
- **Skipping config files.** What a build gate covers is itself a finding.
- **Local path/quoting noise.** The API path needs no clone, so prefer it. If you must
  clone, on git-bash `git -C` with an MSYS path containing spaces can fail with
  `cannot change to` — `cd` into the repo first, then run git.
- **Printing the token.** Report login and scopes, never the secret.

## Support files

- `references/github-api-recipes.md` — every endpoint used, with exact commands.
- `references/case-remote-review-session.md` — a worked session: findings, and how each
  one generalized.
