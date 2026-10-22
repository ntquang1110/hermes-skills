# Config guard stale GOLDEN — worked example (2026-10-07)

## Symptom
User: "tại sao lại reset về openrouter?" — config kept reverting to OpenRouter
despite being set to command-code.

## Diagnosis path
1. Read config.yaml current state → `command-code / xiaomi/mimo-v2.5`, fallback = ark
   only. Config was CORRECT at time of inspection.
2. Checked backup `config.yaml.bak-fb-20261005-231121` → fallback had 5 entries
   including `openrouter / deepseek/deepseek-chat`. Confirms a rewrite happened.
3. Read `config_guard.py` GOLDEN → line 36 still had
   `{"provider": "openrouter", "model": "deepseek/deepseek-chat"}` in fallback_providers.
   GOLDEN also had stale model: `deepseek-v4-flash @ bytedance` (old setup).
4. Guard's `fix_config()` overwrites `fallback_providers` entirely with GOLDEN whenever
   it detects any drift → openrouter reappears.
5. `cron/jobs.json` was corrupted (1 byte "x") since 12:34 — cron scheduler dead,
   guard not currently running. But would reset config the moment cron recovered.

## Root cause
GOLDEN config in config_guard.py was set on 2026-09-14 and never updated when the
user switched providers. The guard "fixed" config back to the old GOLDEN state on
every cron tick.

## Fix applied
1. Updated GOLDEN in config_guard.py:
   - model: `xiaomi/mimo-v2.5 @ command-code / https://api.commandcode.ai/provider/v1`
   - fallback_providers: only `custom:ark.ap-southeast.bytepluses.com / deepseek-v4-flash-260425`
   - Removed openrouter, bytedance, command-code fallback entries
2. Restored jobs.json from `jobs.json.bak-20260909132716` (41 jobs, 27 enabled).
   Backup file was from Sep 9 — any jobs created after that date were lost and needed
   recreation (config-guard-hermes cron job recreated via `cronjob action=create`).
3. Tested guard manually → silent (config matches GOLDEN), only warned about desktop
   Hermes.exe running.

## Key lessons
- **GOLDEN must be updated whenever the user changes their provider/model setup.**
  The guard will fight you otherwise.
- **jobs.json corruption is silent.** Check `ls -la cron/jobs.json` when debugging
  "why did cron stop". A 1-byte file = all jobs dead.
- **After restoring old jobs.json backup, recreate jobs created after that backup.**
  Use `cronjob action=list` to see what exists, compare against what should exist.
- **Desktop Hermes.exe (Electron app) overwrites config.yaml** while running. The
  guard's `kill_desktop()` handles this, but tell the user to close it if not needed.
