# Case study — first remote review session

Context: the user asked "làm sao để đệ review branch code của anh trên github?" (how do I
get you to review my branch). No clone, no PR existed. Answer was the workflow in
SKILL.md, demonstrated live on one branch.

## What the reconnaissance produced

```
git 2.54.0  |  gh 2.95.0 — installed but NOT logged in
PAT in ~/AppData/Local/hermes/.env as GITHUB_PAT_B64 (base64)
→ GET /user = ntquang1110
→ X-OAuth-Scopes: admin:gpg_key, admin:org, admin:org_hook, admin:public_key,
                   admin:repo_hook, admin:ssh_signing_key, codespace, gist,
                   project, repo, user, workflow, write:discussion, ...
→ 12 repos, all private, across personal + 2 orgs
```

`gh auth status` said "not logged into any GitHub hosts" and that turned out to be
irrelevant. The PAT was already there, base64-encoded, and `gh` was never needed. Lesson:
run the `gh auth status` check for information, but do not stop at "not authenticated" —
check the profile `.env` for `GITHUB_PAT_B64` before concluding there is no access.

## Triage result across four branches

Default branch `main`. No open PRs anywhere.

| Branch | ahead | behind | files | lines | Verdict |
|---|---|---|---|---|---|
| `fix/vtp-integration` | 2 | 7 | 14 | +1175 / -90 | Real work, stale, rebase before merging |
| `fix/contract-bugs` | 1 | 7 | 4 | +96 / -8 | Real work, reviewed |
| `fix/order-approval-route-status-note` | 0 | 20 | 0 | 0 | Dead, already in main, recommend delete |
| `fix/checkin-bank-match-bugs` | 0 | 20 | 0 | 0 | Dead, already in main, recommend delete |

The two `ahead_by=0` branches cost one `compare` call each and produced actionable
findings (delete these) without a single line of code being read. Two of four branches
resolved for near-zero tokens.

## The finding that only came from reading the source

The branch's `CHANGELOG.md` claimed three fixes, including that auto-advance had been
repaired by loading the contract record when a signed file is uploaded. The diff supported
that claim: `let current` was now populated under `if (stage || uploadingSignedFile)`.

Reading `api/app.ts` at the ref showed two things the diff did not:

1. The Lark notification was still gated on `if (stage && stage !== current?.stage)`. The
   auto-advance path writes the new stage with its own `contractsDb.update` call and never
   sets a body `stage`.
2. `const updatedStage = updates.stage || current.stage` was introduced and never used
   anywhere in the file.

Then reading `src/components/ContractsModule.tsx` at the same ref settled it: the upload
handler PUTs only `{ submitted_contract_url, submitted_contract_name }`. No `stage`. So the
stage advanced server-side and the notification was skipped, on exactly the two paths the
changelog claimed to have fixed.

None of the three claims could be settled from the diff alone. Only the diff plus the
enclosing function plus the caller at the ref gave the answer.

## The class-level findings and how they generalized

| Finding on this branch | Generalized into |
|---|---|
| Whitelist destructure dropped 6 fields, so `updates` was `{}` and `update({}).select().single()` raised `Cannot coerce the result to a single JSON object` (3rd occurrence of the class) | "Empty / no-op payload" + "Symptom vs root cause" rows of the Step 5 table |
| Auto-advance advanced the stage while the notifier was gated on a field the caller never sent | "Side effect bypassed" row |
| `app.put("/api/contracts/:id", requireAuth, ...)` with no role check, while `requireRole` existed and was used on a sibling route | "Authz parity" row |
| `tsconfig.json` had `"include": ["src"]` and `"exclude": ["api", ...]`, so `npm run lint` (`tsc --noEmit`) never saw the 6849-line backend | "Type-check coverage" row |
| `update(url)` then a second `update({stage})`, non-atomic | "Non-atomic multi-write" row |
| `await apiCall(...)` inside `reader.onloadend`, so the enclosing `try/catch` could not catch it; failed uploads were silent | "Silent client failure" row |
| Two separate `new Date().toISOString()` calls, one written to the DB and one returned to the client | "Recomputed derived value" row |
| PDF export URL assumed the Google Doc was public, with no fallback or error surface | "External-resource assumption" row |

Every row in the Step 5 hunt table traces to something real found in one review. That is
why the table is in the SKILL.md body rather than left in this file.

## What the user asked for at the end

Nothing was corrected; the format landed. The report closed by naming the two decisions
that belonged to the user (delete the two dead branches, rebase the stale ones before
reviewing the big branch) and offered to run the full review on the 14-file branch. The
only unprompted advisory added was that the classic PAT carried `admin:org` and `workflow`,
wider than a read-only review needs.
