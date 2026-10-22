# Remote branch audit + review (volden-ops-web)

Repo-specific companion to the class-level skill `github-branch-review`. Read that one for
the general workflow; this file holds what is specific to this repo.

## Why the API path beats cloning here

The repo has a space in its local path (`D:/Hermes Proj/volden-ops-web`), which has already
caused trouble with `search_files` and `git -C` in this environment. The REST API path
touches no working tree at all: no fetch, no checkout, no merge conflict, no local path
quoting. Prefer it for any "what is on this branch" question.

## Getting the token

`GITHUB_PAT_B64` (base64) lives in `~/AppData/Local/hermes/.env`. Decode it and use it as
`Authorization: token $GITHUB_TOKEN`. Verify with `GET /user` plus
`curl -sI ... | grep -i x-oauth-scopes`.

Account: `ntquang1110`. Scope on the PAT in use: full `repo` plus `admin:org`, `workflow`,
`admin:repo_hook`, `gpg_key`, `packages` — wider than a read-only review needs, but it does
mean findings can be posted back as PR comments.

`gh auth status` reports "not logged into any GitHub hosts". This does not matter and is
not a blocker: the PAT talks to the API directly and `gh` is never needed.

## Endpoints that carry the work

```bash
# diff + diffstat + triage in one call
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/ntquang1110/volden-ops-web/compare/main...<branch>"

# whole file at a ref (needs the raw accept header or you get base64 JSON)
curl -s -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github.raw" \
  "https://api.github.com/repos/ntquang1110/volden-ops-web/contents/api/app.ts?ref=<branch>"
```

Read `ahead_by` before reading any code. `ahead_by=0` means the branch is fully merged into
main: recommend deletion, do not review. That check alone resolved 2 of 4 branches in the
2026-10-05 pass.

## Branch state 2026-10-05

Default branch `main` at `1f44fe1d`. No open PRs on the repo.

| Branch | vs main | files / lines | Verdict |
|---|---|---|---|
| `fix/vtp-integration` | ahead 2, behind 7 | 14 / +1175 -90 | Real work, worth watching. Stale, rebase before merging |
| `fix/contract-bugs` | ahead 1, behind 7 | 4 / +96 -8 | Real work, reviewed 2026-10-05 |
| `fix/order-approval-route-status-note` | ahead 0, behind 20 | 0 | **DEAD** — fully in main, recommend delete |
| `fix/checkin-bank-match-bugs` | ahead 0, behind 20 | 0 | **DEAD** — fully in main, recommend delete |

Note on provenance: the other dev (Quynh Anh Vuong) pushes branches without opening PRs, so
"no open PRs" never means "no pending work". Always list branches, not just PRs.

## Bug classes confirmed on this repo

These came out of reviewing `fix/contract-bugs` at the ref on 2026-10-05. All line numbers
are from `api/app.ts` on that branch (6849 lines total).

### 1. Whitelist drop to empty payload, 3rd occurrence

The route at `app.ts:1751` destructures ~30 named fields and then does
`if (x !== undefined) updates.x = x` for each. A request body containing only fields
outside that whitelist leaves `updates = {}`, which hits
`contractsDb.update` in `api/db.ts` (`.update(updates).eq("id", id).select().single()`).
PostgREST returns zero rows for an empty update and `.single()` then fails with
`Cannot coerce the result to a single JSON object`, surfacing as HTTP 500.

This has now happened three times: `submitted_contract_url`, `signed_both_contract_url`,
`shipping_courier` / `shipping_tracking_code`. Each time the fix was to add more fields to
the whitelist. The class-level guard is still missing and belongs before the DB call:

```ts
if (Object.keys(updates).length === 0)
  return res.status(400).json({ error: "No updatable fields" });
```

Better: make `contractsDb.update` a no-op returning `findById(id)` on an empty payload, and
replace the 30-line destructure with a const field array plus a loop so a field cannot be
forgotten again.

### 2. Auto-advance advances the stage but skips the Lark notification

The notification is gated on `if (stage && stage !== current?.stage)` at `app.ts:1929`.
The frontend upload handlers (`ContractsModule.tsx` `handleUploadSigned` line 114,
`handleUploadBothSigned` line 132) PUT only
`{ submitted_contract_url, submitted_contract_name }` and
`{ signed_both_contract_url, signed_both_contract_name }`. No `stage` field.

So the server auto-advances `submitted → shipping_booked` (`app.ts:1897`) and
`pending_archive → completed` (`app.ts:1903`) through its own `contractsDb.update` calls,
while the notify branch never runs. The stage changes and nobody is told. Any future change
to the auto-advance paths has to check the notify gate alongside it.

### 3. Contracts PUT has no role check

`app.put("/api/contracts/:id", requireAuth, ...)` at `app.ts:1751` uses `requireAuth`
only. `requireRole` exists in `api/middleware/role.ts` and is used on the warehouse route at
`app.ts:3270`. Same class as the known gap on `PUT /api/orders/:id`.

Consequence: any logged-in user, including role `sale`, can PUT `partner_bank_account`,
`business_registration_url`, `revenue_target`, `submitted_contract_url`. The stage
transition has `stageRoleCheck`; field writes have nothing.

Generalized pitfall: grep `app.put(` and check every route that writes money or ownership
fields for a missing `requireRole`.

### 4. `api/` is never type-checked

`tsconfig.json` has `"include": ["src"]` and
`"exclude": ["api", "scripts", "sdk", "supabase", "dist", "node_modules"]`.
`npm run lint` is `tsc --noEmit`, so it never sees `api/app.ts` (6849 lines).

That is why the narrowing issue is invisible: `let current: Record<string, any> | null`
is assigned inside `if (stage || uploadingSignedFile)` at `app.ts:1864`, and then
`current.stage` is read inside a separate `if (stage)` at `app.ts:1870` and `1875`. The
logic is sound (a truthy `stage` implies the first branch ran) but TypeScript will not
narrow across the two blocks, and nothing checks it.

Do not treat a green build or lint as evidence about the backend layer.

### 5. Smaller ones on the same diff

- Auto-advance is two sequential writes (`update(url)` then `update({ stage })`), not
  atomic. If the second fails the contract has the file but the wrong stage, with no
  rollback and no retry.
- `const updatedStage = updates.stage || current.stage` at `app.ts:1894` is declared and
  never used anywhere in the file. Marker of a half-finished refactor.
- `completed_at` is computed twice (`app.ts:1908` and `1912`); the value returned to the
  client differs by milliseconds from what was written to the DB.
- `await apiCall(...)` sits inside `reader.onloadend`, an async callback, so the enclosing
  `try/catch` in the upload handlers cannot catch it. A 500 or network failure produces no
  alert at all: the user believes the upload succeeded. This applies to every FileReader
  handler in the repo.
- `getGoogleDocPdfUrl` in `ContractsModule.tsx` builds
  `docs.google.com/document/d/<id>/export?format=pdf` on the assumption the doc is public
  (the comment says Apps Script sets ANYONE_WITH_LINK). If it is not public the user gets a
  login page saved as `.pdf`, with no fallback and no error surface.

## What was correct on that branch

Worth recording so it is not "fixed" backwards: the payload fix to `fileBase64` is right
(the previous `base64` + `dataURL.split(',')[1]` pair genuinely mismatched the API's
expectation of a full data URL), and renaming "Tải bản HĐ đã ký" to "Tải lên bản HĐ đã ký"
is accurate since those controls upload rather than download.
