---
name: windows-drive-migration
description: "Move app data off a full Windows drive via NTFS junctions."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [windows, disk, storage, junction, mklink, robocopy, migration]
---

# Windows Drive Migration (NTFS Junction)

Move data directories from a full system drive (C:) to a larger drive (D:) while keeping the original paths transparent to the app. The app never notices the data moved; all new writes land on the new drive automatically.

## When to use
- C: drive nearly full, another drive has space (always check `df -h /c /d` first)
- App data dirs (skills, sessions, caches, logs, DBs) must stop growing on C:
- User wants "everything from now on" stored on another drive

## Core pattern
For each unlocked directory:
```
robocopy <src> <dst> /E /MOVE
mklink /J <src> <dst>
```
The junction is a transparent pointer: the app reads/writes `C:\...\path`, the bytes physically land on D:.

## Steps
1. Survey: `df -h /c /d`. Measure per-folder sizes with `du -sh <folder>` individually — a single `du -sh` over the whole home tree times out (hermes-agent/ source + venv is huge).
   - **Pitfall (found 08/2026): `du` in git-bash WALKS NTFS junctions**, so a sweep over `AppData\Local` follows the `hermes` => `D:` junction and hangs recursing into the other drive. Kill it and use `du -x` (stops at filesystem boundary) or — best — run the PowerShell sizing sweep below, which returns every child folder's GB fast even over huge trees:
   ```powershell
   Get-ChildItem 'C:\Users\<user>\AppData' -Force | Where-Object PSIsContainer | ForEach-Object {
     $s=(Get-ChildItem $_.FullName -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
     [PSCustomObject]@{Dir='AppData\'+$_.Name; GB=[math]::Round($s/1GB,2)}
   } | Sort-Object GB -Descending | Format-Table -AutoSize
   ```
   In MSYS/bash, single-quote the whole `-Command` string and escape each `$` as `\$` or bash eats it. Measure one level at a time (top → AppData\Local → Program Files) and sort, instead of one giant recursive du.
2. Identify locked files: a running gateway/service holds handles on SQLite DBs and open log files. Those cannot be moved hot ("Device or resource busy").
3. Create target root: `mkdir -p /d/<root>/<folder>`.
4. Move unlocked dirs (skills, sessions, cron, caches, plugins, bin...) with a .bat script — see `templates/junction-move.bat`.
5. For locked files: copy now while running (`cp`/robocopy), prepare a swap .bat to run when the service is stopped — see `templates/junction-swap-locked.bat`. Verify the copy exists before the swap.
6. Verify: write a test file through the junction (`echo x > <src>/_t.txt`, confirm it appears in `<dst>/`), then `df -h`.
7. Record the policy so future sessions write new files to the new drive: AGENTS.md section + memory entry ("DISK: ổ C ~18GB → MỌI thứ mới ghi Ổ D ...").

## Known-good targets and their sizes

| Directory | Typical size | Notes |
|---|---|---|
| `~/.cache/huggingface` | 8 GB | Pure cache — safe to relocate, nothing holds handles on it while no model is loading. `hub/` holds `models--<org>--<name>/{blobs,snapshots,refs}`; `blobs/` is where the bytes actually live, so folder-level `du` on a snapshot dir under-reports. |
| downloaded model dirs inside a repo checkout | 1-2.5 GB each | Move these too, or they quietly refill the drive you just cleaned. |
| `%TEMP%` venvs from throwaway experiments | 1-3 GB each | `uv venv` under `AppData\Local\Temp\` survives until reboot; sweep them when done. |

Checkpoint downloads inflate C: fast: a single 2.5 GB multilingual checkpoint plus a 1.05 GB base model pushed C: from 22 GB free to 12 GB during one research session. Repoint `HF_HOME` / the cache junction to D: **before** pulling models, not after.

## Pitfalls (Windows / git-bash)
- **Prefer PowerShell for the junction itself — skip the .bat ceremony.** `cmd //c mklink /J ...` from git-bash frequently does *not* error; it silently opens an interactive cmd banner and creates nothing, so you finish the copy, see the source dir gone and no junction in its place. The one-liner that works first try from `terminal`:
  ```bash
  powershell -NoProfile -Command "New-Item -ItemType Junction -Path 'C:\Users\<user>\.cache\huggingface' -Target 'D:\hf-cache' | Out-Null; Test-Path 'C:\Users\<user>\.cache\huggingface\hub'"
  ```
  It returns `True` when the junction resolves. Confirm the link type independently with `(Get-Item '<link>').LinkType` → `Junction`. Single-quote the whole `-Command` string so bash leaves the inner quotes alone.
- **mklink from bash is escaping hell.** If you must use it: `cmd //c 'mklink /J ...'`, `MSYS_NO_PATHCONV=1 cmd /c ...` and other inline variants fail with "The filename, directory name, or volume label syntax is incorrect." The alternative: write a `.bat` file and run `cmd.exe /c "C:\\full\\path\\file.bat"` (double backslashes + quotes). Or `cd` into the dir first in the bat.
- **A copy+replace can finish with the source already deleted** — `mv` / `robocopy /MOVE` succeeds, then the junction step fails silently and the data is on the target with no pointer. Always re-verify with `Test-Path <link>/<known-child>` immediately; the data is safe on the target, you only need to re-run the junction command.
- **Directory junction (mklink /J) needs no admin; plain file symlink (mklink) also worked in this env** — but symlink file may require admin/developer mode on other machines; prefer /J for dirs.
- **robocopy exit codes**: 0 = no files copied, 1 = copied OK, 2+ = warnings/errors. `$?` after a pipe reflects the last pipe command (e.g. tail), not robocopy — don't trust it; check `if exist <src>` after /MOVE instead.
- **Never move the app's source/venv** — only data dirs. E.g. keep `hermes-agent/` source tree on C:, junction just skills/sessions/cron/cache/bin/logs/state.db.
- **df won't instantly show freed space** — junction itself is tiny; space frees as old files are deleted from C:. The real win is that all future growth lands on D:.
- **Locked DB/log files**: copying works, moving doesn't. Do copy-now → swap-on-restart. Don't kill a running gateway mid-session to force the move — that kills the session doing the work (and the user's active chat).
- **Hermes data junction targets live under `D:\Hermes\hermes-home`** on Quang's machine; `D:/Hermes Proj/.hermes-state` state files were already on D:.

## Files
- `templates/junction-move.bat` — starter batch: robocopy /MOVE a list of dirs to D: root, then mklink /J each back.
- `templates/junction-swap-locked.bat` — swap state.db + logs after the gateway is stopped (copy-first done while running).
