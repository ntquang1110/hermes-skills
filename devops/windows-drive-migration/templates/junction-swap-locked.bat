@echo off
rem ============================================================
rem PHASE 2: swap gateway-locked files (state.db + logs) to D:
rem Run ONLY when the gateway/service is STOPPED (files held open
rem while running -> "Device or resource busy").
rem Copy-first (cp/robocopy) while the service still runs, then
rem execute this during a restart window.
rem Run from git-bash with:
rem   cmd.exe /c "C:\\path\\to\\junction-swap-locked.bat"
rem ============================================================
cd /d C:\Users\NTQUANG_DELL\AppData\Local\hermes

echo === state.db ===
del /f /q state.db 2>nul
mklink state.db D:\Hermes\hermes-home\state.db
echo OK state.db -^> D:\Hermes\hermes-home\state.db (da copy san truoc do)

echo === logs ===
if exist logs (
  robocopy logs D:\Hermes\hermes-home\logs /E /MOVE /NFL /NDL /NJH /NJS
  if exist logs (echo LOGS_MOVE_FAIL - thu lai khi gateway tat) else (mklink /J logs D:\Hermes\hermes-home\logs && echo OK logs -^> junction D)
) else (
  mklink /J logs D:\Hermes\hermes-home\logs
  echo OK logs junction (da tao)
)

echo.
echo PHASE2 DONE. Restart gateway roi kiem tra: hermes doctor
pause
