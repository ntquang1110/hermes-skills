# SOURCE-MAP.md Verification — Worked Example

> Applied to `volden-ops-web` on 2026-07-26.
> Full delta: 283 → 543 lines, 356 insertions, 96 deletions.

## Starting Point

The existing `docs/SOURCE-MAP.md` was heavily stale — written months earlier and never re-synced.

## Delta Scan Results

| Category | Old | Actual | Delta |
|----------|-----|--------|-------|
| Root structure | 11 entries | 35+ entries | +24 missing |
| Backend files | 7 listed (incl. 1 non-existent) | 15 actual files | +9, -1 phantom |
| Frontend lib/ | 2 files | 11 files | +9 missing |
| Components | ~25 listed | ~80 components | +55 missing |
| ERP pages | 4 listed | 23 pages | +19 missing |
| Executive section | 0 | 3 files | New section |
| SQL migrations | 31 | 77 | +46 files |
| Scripts | 15 (10 don't exist) | 28 (all different) | Complete rewrite |
| Docs listed | 10 | 30+ | +20 missing |
| AI Agent Config | 0 | `.agents/`, `.opencode/`, `.superpowers/` | New section |
| Supabase Edge Functions | 0 | `supabase/functions/` | New section |

## Root Causes of Drift

1. **New features added** without updating SOURCE-MAP.md (ERP pages, executive dashboard, many components)
2. **Migration files accumulated** (31 → 77) but count never revised
3. **Scripts were refactored/renamed** but SOURCE-MAP was not updated
4. **Temporary test scripts deleted** but remained in documentation
5. **`api/server-utils.ts` never existed** — was a phantom file
6. **New directories appeared** (`.agents/`, `.superpowers/`, `supabase/`, `public/`, `sdk/`)

## Command Sequence Used

```bash
# 1. List root contents
cd /d/Hermes Proj/volden-ops-web
find . -maxdepth 1 -type f -o -type d | grep -v .git | sort

# 2. List all source files
find src -type f -name "*.ts" -o -name "*.tsx" | sort
ls api/

# 3. List scripts
ls scripts/

# 4. List SQL migrations
ls sql/

# 5. List docs
ls docs/

# 6. Count migrations
ls sql/*.sql | wc -l

# 7. Check for phantom files (verify each file in SOURCE-MAP actually exists)
grep -c "server-utils" docs/SOURCE-MAP.md  # found reference → checked actual → didn't exist
```

## Key Insight

The most common drift pattern is **asymmetric updates**: files get added/removed/renamed during development but the documentation is never updated to match. The verification must be systematic — go section by section and compare `ls` output against documented entries.

## Preventing Re-Drift: AGENTS.md Self-Maintenance Rule

A one-shot SOURCE-MAP.md fix does not survive — the map drifts again the next time a developer/agent adds a page. The user's explicit convention (volden-ops-web, 2026-07-26) is to **encode the maintenance duty into the project's AGENTS.md** so every future agent self-enforces it.

Added section (mirrors the FEATURES.md / CHANGELOG.md management sections already in AGENTS.md):

```markdown
## 3.6 QUẢN LÝ SOURCE MAP (docs/SOURCE-MAP.md) (BẮT BUỘC)

1. Mỗi khi thêm page/route/component/API mới → PHẢI thêm vào SOURCE-MAP.md
   ngay trong cùng commit
2. File mới trong src/, api/, scripts/, sql/, docs/ → cập nhật section tương ứng
3. Xoá/đổi tên file → sửa trong SOURCE-MAP.md
4. Thư mục mới → thêm vào tree view
5. Giữ đúng format table | Path | Mục đích |
6. Không cần update cho format code, fix typo nhỏ
Verification: trước commit check `git diff --stat docs/SOURCE-MAP.md` — nếu code
thay đổi mà SOURCE-MAP.md không đổi thì review lại.
```

Numbering: the project's AGENTS.md uses `## 3.5` for FEATURES.md; insert the new section as `## 3.6` right before `## 4. QUẢN LÝ SQL SCHEMA`.

## Path Resolution Bug (Windows MSYS)

When writing the updated SOURCE-MAP.md:

```bash
# ❌ This writes to wrong path when CWD != repo root
write_file(path="/d/Hermes Proj/volden-ops-web/docs/SOURCE-MAP.md", ...)
# Resolves to: D:\Hermes Proj\ai-company\d\Hermes Proj\... (WRONG)

# ✅ Get Windows absolute path first
cd "/d/Hermes Proj/volden-ops-web"
pwd -W  # → D:/Hermes Proj/volden-ops-web

# ✅ Then use that
write_file(path="D:/Hermes Proj/volden-ops-web/docs/SOURCE-MAP.md", ...)
```

The write_file tool resolves relative paths against the Hermes active workspace directory, not the terminal's CWD. Always use Windows absolute paths.
