#!/usr/bin/env python3
"""Đăng ký Scheduled Task giám sát gateway Hermes trên máy Windows từ xa.

Vì sao cần: login-item (VBS trong Startup) KHÔNG tự bật lại khi gateway chết —
một lần chết là nằm chết tới khi có người đăng nhập. Case thật 13/10/2026:
gateway dừng 23:09, nằm chết ~15 tiếng.

Vì sao KHÔNG tự viết watchdog: Hermes gateway là SINGLETON — bật thêm một cái là
GIẾT cái đang sống. Đã dính vòng lặp: check báo "chết" sai → bật mới → giết cái
khoẻ → check lại báo sai. Task Scheduler với MultipleInstances=IgnoreNew chặn
việc này ở tầng OS, không phụ thuộc logic tự viết.

Chạy:
    python register_gateway_task.py --host HOST --user USER --pass 'PW'
    python register_gateway_task.py --host HOST --user USER --pass 'PW' --dry-run

Sau khi chạy, verify thủ công (in ra ở cuối):
    schtasks /Query /FO TABLE | findstr Hermes
    # kill thu -> phai tu bat lai
"""

import argparse
import base64
import sys

try:
    import paramiko
except ImportError:
    sys.exit("thieu paramiko:  pip install paramiko")

TASK_NAME = "HermesGateway"


def ps(script: str) -> str:
    """Bọc script vào -EncodedCommand (UTF-16LE base64) để khỏi escape quote."""
    enc = base64.b64encode(script.encode("utf-16-le")).decode()
    return "powershell -NoProfile -EncodedCommand " + enc


def run(client, script: str, timeout: int = 300) -> str:
    _, out, err = client.exec_command(ps(script), timeout=timeout)
    o = out.read().decode("utf-8", "replace")
    e = err.read().decode("utf-8", "replace")
    return (o or e).replace("\r", "").strip()


def build_script(user: str, password: str) -> str:
    """PowerShell dang ky task. KHONG dung backslash trong path (xem SKILL.md)."""
    # password co the chua nhay don -> escape bang cach nhan doi
    pw = password.replace("'", "''")
    return f"""
$hm  = "C:/Users/{user}/AppData/Local/hermes"
$gw  = "$hm/bin/hermes.exe"
if (-not (Test-Path $gw)) {{ "LOI: khong thay $gw"; exit 1 }}

# 1) Tat VBS trong Startup — task moi da co trigger AtLogOn, de VBS la trung
$startup = [Environment]::GetFolderPath('Startup')
$vbs = Join-Path $startup 'Hermes_Gateway.vbs'
if (Test-Path $vbs) {{
    Rename-Item $vbs 'Hermes_Gateway.vbs.disabled' -Force -ErrorAction SilentlyContinue
    "1. da tat VBS trong Startup"
}} else {{ "1. khong co VBS trong Startup (bo qua)" }}

# 2) Dang ky task — action CHINH LA gateway (khong boc .bat, khong start "")
$act = New-ScheduledTaskAction -Execute $gw -Argument "gateway run"
$t1  = New-ScheduledTaskTrigger -AtLogOn
$t2  = New-ScheduledTaskTrigger -AtStartup
$t3  = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) `
       -RepetitionInterval (New-TimeSpan -Minutes 5)
$set = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew `
       -ExecutionTimeLimit ([TimeSpan]::Zero) `
       -RestartInterval (New-TimeSpan -Minutes 1) -RestartCount 999 `
       -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
       -StartWhenAvailable
Register-ScheduledTask -TaskName "{TASK_NAME}" -Action $act `
  -Trigger $t1,$t2,$t3 -Settings $set `
  -User "{user}" -Password '{pw}' -RunLevel Limited -Force | Out-Null
"2. da dang ky task {TASK_NAME}"

# 3) Verify cau hinh — doc lai tu he thong, khong tin buoc 2
$t = Get-ScheduledTask -TaskName "{TASK_NAME}"
"3. State         : " + $t.State
"   MultipleInst  : " + $t.Settings.MultipleInstances
"   ExecTimeLimit : " + $t.Settings.ExecutionTimeLimit
"   RestartCount  : " + $t.Settings.RestartCount
"   RestartEvery  : " + $t.Settings.RestartInterval
"   LogonType     : " + $t.Principal.LogonType
"   Action        : " + $t.Actions[0].Execute + " " + $t.Actions[0].Arguments

# 4) Khoi dong neu chua chay
if ($t.State -ne 'Running') {{
    Start-ScheduledTask -TaskName "{TASK_NAME}"
    "4. da Start-ScheduledTask, cho 50s..."
    Start-Sleep -Seconds 50
}}

# 5) Bang chung that: gateway la python.exe DUY NHAT o session 0
$svc = @(Get-Process python -ErrorAction SilentlyContinue |
         Where-Object {{ $_.SessionId -eq 0 }})
"5. session-0 python: " + (($svc | ForEach-Object {{ "$($_.Id)/$([math]::Round($_.WorkingSet64/1MB))MB" }}) -join ", ")
"   task state      : " + (Get-ScheduledTask -TaskName "{TASK_NAME}").State
$st = Get-Content "$hm/gateway_state.json" -Raw -ErrorAction SilentlyContinue
if ($st) {{
    $j = $st | ConvertFrom-Json
    "   gateway_state   : pid=$($j.pid) state=$($j.gateway_state) telegram=$($j.platforms.telegram.state)"
}}
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", required=True)
    ap.add_argument("--user", required=True)
    ap.add_argument("--pass", dest="password", required=True)
    ap.add_argument("--port", type=int, default=22)
    ap.add_argument("--dry-run", action="store_true",
                    help="chi in script PowerShell, khong ket noi")
    args = ap.parse_args()

    script = build_script(args.user, args.password)

    if args.dry_run:
        print(script)
        return 0

    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # allow_agent/look_for_keys=False: khong thi SSH thu key trong ~/.ssh roi fail cham
    c.connect(args.host, port=args.port, username=args.user,
              password=args.password, timeout=25, banner_timeout=30,
              auth_timeout=30, allow_agent=False, look_for_keys=False)

    print(run(c, script, timeout=600))

    print()
    print("--- task Hermes tren may ---")
    print(run(c, 'schtasks /Query /FO TABLE | Select-String "Hermes"'))

    print()
    print("BUOC TIEP — test that, dung tin vao cau hinh:")
    print("  1. lay pid:  Get-Process python | Where SessionId -eq 0")
    print("  2. kill:     taskkill /PID <pid> /F")
    print("  3. cho ~2 phut roi kiem lai — phai co pid MOI o session 0")
    c.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
