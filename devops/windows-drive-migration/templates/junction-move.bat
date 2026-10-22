@echo off
rem ============================================================
rem Junction move starter: robocopy /MOVE each dir to D: root,
rem then mklink /J back to keep the original path transparent.
rem Run from git-bash with:
rem   cmd.exe /c "C:\\path\\to\\junction-move.bat"
rem (inline `cmd //c 'mklink ...'` from bash FAILS with syntax error)
rem ============================================================
cd /d C:\Users\NTQUANG_DELL\AppData\Local\hermes
mkdir D:\Hermes\hermes-home >nul 2>&1

echo === Moving skills ===
robocopy skills D:\Hermes\hermes-home\skills /E /MOVE /NFL /NDL /NJH /NJS >nul 2>&1
if exist skills (echo SKILLS_FAIL) else (mklink /J skills D:\Hermes\hermes-home\skills && echo SKILLS_OK)

echo === Moving sessions ===
robocopy sessions D:\Hermes\hermes-home\sessions /E /MOVE /NFL /NDL /NJH /NJS >nul 2>&1
if exist sessions (echo SESSIONS_FAIL) else (mklink /J sessions D:\Hermes\hermes-home\sessions && echo SESSIONS_OK)

echo === Moving cron ===
robocopy cron D:\Hermes\hermes-home\cron /E /MOVE /NFL /NDL /NJH /NJS >nul 2>&1
if exist cron (echo CRON_FAIL) else (mklink /J cron D:\Hermes\hermes-home\cron && echo CRON_OK)

echo === Moving plugins ===
robocopy plugins D:\Hermes\hermes-home\plugins /E /MOVE /NFL /NDL /NJH /NJS >nul 2>&1
if exist plugins (echo PLUGINS_FAIL) else (mklink /J plugins D:\Hermes\hermes-home\plugins && echo PLUGINS_OK)

echo === Moving cache ===
robocopy cache D:\Hermes\hermes-home\cache /E /MOVE /NFL /NDL /NJH /NJS >nul 2>&1
if exist cache (echo CACHE_FAIL) else (mklink /J cache D:\Hermes\hermes-home\cache && echo CACHE_OK)

echo === Moving bin ===
robocopy bin D:\Hermes\hermes-home\bin /E /MOVE /NFL /NDL /NJH /NJS >nul 2>&1
if exist bin (echo BIN_FAIL) else (mklink /J bin D:\Hermes\hermes-home\bin && echo BIN_OK)

echo.
echo ALLDONE - verify: ls -la | grep '^l'  (each target should show as junction to D:)
pause
