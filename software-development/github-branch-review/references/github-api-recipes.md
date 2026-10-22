# GitHub REST API — remote review recipes

All calls assume `$GITHUB_TOKEN` is exported (see SKILL.md Step 0). `$OWNER`, `$REPO`,
`$BRANCH`, `$PATH` are yours to fill. `python` is used for JSON parsing because it is
always present and avoids quoting fights on git-bash.

## Who am I / what can I do

```bash
curl -s  -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user \
  | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('login'), d.get('name'))"

curl -sI -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user \
  | grep -iE 'x-oauth-scopes|x-ratelimit-limit'
```

`X-OAuth-Scopes` lists everything the token can do. Worth reporting: a review needs only
`repo` read (or `public_repo` for public repos). Anything like `admin:org`, `workflow`,
`gpg_key` is excess surface for this job.

## Inventory repos

`affiliation` is what makes this useful: it returns the user's own repos plus anything
they collaborate on or reach through an org.

```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/user/repos?per_page=100&sort=pushed&affiliation=owner,collaborator,organization_member" \
  | python -c "
import sys,json
d=json.load(sys.stdin)
print(f'TOTAL: {len(d)}')
for r in d:
    print(f\"{r['full_name']:<45} {'PRIVATE' if r['private'] else 'public ':<7} default={r['default_branch']:<10} pushed={r['pushed_at'][:16]}\")
"
```

`sort=pushed` puts the active repos on top, which is usually the answer to "which repo
should I look at".

## Branches and PRs for one repo

```bash
R=owner/repo
curl -s -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/repos/$R/branches?per_page=50" \
  | python -c "
import sys,json
for b in json.load(sys.stdin): print('  ', b['name'], '|', b['commit']['sha'][:8])
"

curl -s -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/repos/$R/pulls?state=all&per_page=10" \
  | python -c "
import sys,json
d=json.load(sys.stdin)
print('   none') if not d else [print(f\"   #{p['number']} [{p['state']}] {p['head']['ref']} -> {p['base']['ref']} : {p['title'][:60]}\") for p in d]
"
```

If there are no PRs, the workflow stays branch-based: `compare` replaces the PR.

## The compare endpoint — diff, diffstat and triage in one call

This is the workhorse. It returns commits, per-file `patch`, and `additions`/`deletions`,
plus `ahead_by` / `behind_by` relative to the base.

```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$R/compare/main...$BRANCH" \
  | python -c "
import sys,json
d=json.load(sys.stdin)
if 'files' not in d: print('  ERR', d.get('message')); raise SystemExit
print(f\"  ahead_by={d.get('ahead_by')} behind_by={d.get('behind_by')} files={len(d['files'])} +{sum(f['additions'] for f in d['files'])} -{sum(f['deletions'] for f in d['files'])}\")
if d.get('commits'):
    c=d['commits'][-1]['commit']
    print('  last commit:', c['message'].splitlines()[0][:70], '|', c['committer']['date'][:16])
for f in d['files'][:8]: print('   ', f['status'][:7].ljust(7), f['filename'][:70])
if len(d['files'])>8: print('    ... +', len(d['files'])-8, 'more')
"
```

Reading `ahead_by=0` as "dead branch" and skipping the review is the main token saver.
`ahead_by` counts commits on the head that are not on the base; `behind_by` counts the
reverse. Both non-zero means the merge will conflict.

### Dumping the patches to a file

Inline patches inflate the conversation. Write them out, then read the file:

```bash
mkdir -p /d/Hermes/tmp/ghreview
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$R/compare/main...$BRANCH" \
  | python -c "
import sys,json
d=json.load(sys.stdin)
out=[]
for f in d['files']:
    out.append(f\"\n===== {f['status']}  {f['filename']}  (+{f['additions']} -{f['deletions']}) =====\")
    out.append(f.get('patch','[no patch]'))
open(r'D:\Hermes\tmp\ghreview\review.diff','w',encoding='utf-8').write('\n'.join(out))
print('written', sum(len(x) for x in out), 'chars')
"
```

Use the user's D-drive temp convention (`D:/Hermes/tmp/`), not `%TEMP%` on C.

## Read a whole file at a ref

Needed when `compare` omits `patch` (large files), or when you must read the unchanged
control flow around a change to judge it.

```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.raw" \
  "https://api.github.com/repos/$R/contents/api/app.ts?ref=$BRANCH" -o app.ts
wc -l app.ts
awk 'NR>=1859 && NR<=1935 {printf "%d|%s\n", NR, $0}' app.ts
```

Without the `Accept: application/vnd.github.raw` header you get base64 JSON instead of
the file text. The `awk` slice keeps the read cheap and keeps real line numbers, which is
what the report needs.

## Decide whether a green gate means anything

```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github.raw" \
  "https://api.github.com/repos/$R/contents/tsconfig.json?ref=$BRANCH" | head -45
curl -s -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github.raw" \
  "https://api.github.com/repos/$R/contents/package.json?ref=$BRANCH" | head -45
```

Look at `include` / `exclude` and at what the `lint` / `build` scripts actually invoke. A
`"lint": "tsc --noEmit"` with `"exclude": ["api"]` means the backend is never type-checked
no matter how green CI looks.

## Posting findings back as review comments

The PAT usually carries write scope, so the review can be delivered onto the PR instead of
copied into chat.

- PR-level comment: `POST /repos/$R/issues/{number}/comments`
- Inline on a diff line: `POST /repos/$R/pulls/{number}/comments` with `body`, `commit_id`,
  `path`, and `line` (or `position`). Inline comments require a real PR — a bare branch
  has no diff position to anchor to, which is itself a reason to suggest opening one.
