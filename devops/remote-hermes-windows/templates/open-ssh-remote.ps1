# open-ssh-remote.ps1
#
# Muc dich: mo port 22 (SSH) tren mot may Windows tu xa, chay TU MAY DICH
# trong PowerShell voi quyen Admin. Dung khi chi con duong RDP vao duoc
# (port 3389 mo, port 22 dong).
#
# TRANG THAI: DA CHAY THAT end-to-end (2026-10-07, may Windows 10 `lqremote`,
# user NLQuan). Truoc khi chay: port 22 tra `10035` (timeout) tu ngoai, chi RDP
# 3389 mo. Sau khi chay: port 22 `OPEN`, SSH vao duoc bang credential cua user do
# (khong phai Admin — user thuong cung du, mien la trong nhom Administrators).
# => Tier 1 (Add-WindowsCapability) thanh cong. Hai tier du phong (winget, zip)
#    VAN CHUA chay that lan nao — dung tin phan do la da verify.
#
# Chay xong van khong vao duoc tu ngoai thi theo thu tu nay, dung doan:
#   1. netstat -ano | findstr ":22"  -> co LISTENING khong
#   2. Get-NetFirewallRule -Name OpenSSH-Server-In-TCP  -> rule co Enabled khong
#   3. ca hai OK ma ngoai van `10035` -> luc do moi ket luan ROUTER chua forward.
#
# Bien the truyen thang khong can file (dan vao PowerShell Admin):
#   Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
#   Set-Service sshd -StartupType Automatic; Start-Service sshd
#   New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' `
#     -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22 -Profile Any

$ErrorActionPreference = 'Continue'
Write-Host "=== MO PORT SSH TREN MAY DICH ===" -ForegroundColor Cyan

# 0. Phai la Admin
$isAdmin = ([Security.Principal.WindowsPrincipal] `
  [Security.Principal.WindowsIdentity]::GetCurrent()
  ).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "LOI: Phai chay bang quyen Admin. Mo PowerShell -> Run as Administrator." -ForegroundColor Red
    exit 1
}
Write-Host "[0] Quyen Admin: OK"

# 1. Cai OpenSSH Server — ba tang du phong
$cap = Get-WindowsCapability -Online -Name 'OpenSSH.Server*' -ErrorAction SilentlyContinue
if ($cap -and $cap.State -eq 'Installed') {
    Write-Host "[1] OpenSSH Server da co san"
} else {
    Write-Host "[1] Dang cai OpenSSH Server..."
    try {
        Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0 -ErrorAction Stop | Out-Null
        Write-Host "    Cai qua Windows Capability: OK"
    } catch {
        Write-Host "    Capability that bai: $_" -ForegroundColor Yellow
        Write-Host "    Thu winget..."
        try {
            winget install --id Microsoft.OpenSSH.Beta --accept-source-agreements `
              --accept-package-agreements --silent
        } catch {
            Write-Host "    winget that bai. Tai thu cong..." -ForegroundColor Yellow
            $url = 'https://github.com/PowerShell/Win32-OpenSSH/releases/download/v9.8.1.0p1-Preview/OpenSSH-Win64.zip'
            $zip = "$env:TEMP\OpenSSH-Win64.zip"
            [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
            Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
            Expand-Archive -Path $zip -DestinationPath 'C:\Program Files\' -Force
            & 'C:\Program Files\OpenSSH-Win64\install-sshd.ps1'
        }
    }
}

# 2. Bat service + tu dong khoi dong lai sau reboot
Write-Host "[2] Bat service sshd..."
Set-Service -Name sshd -StartupType Automatic -ErrorAction SilentlyContinue
Start-Service sshd -ErrorAction SilentlyContinue
Set-Service -Name ssh-agent -StartupType Automatic -ErrorAction SilentlyContinue
Start-Service ssh-agent -ErrorAction SilentlyContinue

# 3. Firewall: cho phep port 22
#    LUU Y: neu port 22 tra ve errno 10035 (timeout) tu ngoai, nguyen nhan thuong la
#    ROUTER chua forward 22, khong phai rule nay. Rule nay chi mo firewall tren host.
Write-Host "[3] Mo firewall port 22..."
Remove-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -ErrorAction SilentlyContinue
New-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' `
  -DisplayName 'OpenSSH Server (sshd)' `
  -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22 `
  -Profile Any | Out-Null
Write-Host "    Da them rule"

# 4. Shell mac dinh = PowerShell (de lenh tu xa chay dung)
if (-not (Test-Path 'HKLM:\SOFTWARE\OpenSSH')) {
    New-Item -Path 'HKLM:\SOFTWARE\OpenSSH' -Force | Out-Null
}
New-ItemProperty -Path 'HKLM:\SOFTWARE\OpenSSH' -Name DefaultShell `
  -Value 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' `
  -PropertyType String -Force | Out-Null

# 5. Kiem tra
Write-Host ""
Write-Host "=== KET QUA ===" -ForegroundColor Cyan
$svc = Get-Service sshd -ErrorAction SilentlyContinue
Write-Host ("Service sshd   : {0} / {1}" -f $svc.Status, $svc.StartType)
$listen = (netstat -ano | Select-String ':22\s' | Select-Object -First 3)
if ($listen) { Write-Host "Dang lang nghe port 22:"; $listen | ForEach-Object { Write-Host "   $_" } }
else         { Write-Host "CHUA thay port 22 lang nghe!" -ForegroundColor Red }

Write-Host ""
Write-Host "Ten may        : $env:COMPUTERNAME"
Write-Host "Nguoi dung     : $env:USERNAME"
Write-Host ""
Write-Host "Neu port 22 VAN dong tu ngoai sau khi chay xong: can forward port 22 tren"
Write-Host "ROUTER ve IP noi bo cua may nay (xem danh sach IP ben duoi)."
Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike '127.*' } |
  ForEach-Object { Write-Host ("  {0}  ({1})" -f $_.IPAddress, $_.InterfaceAlias) }
Write-Host ""
Write-Host "XONG. Tu may ngoai kiem tra lai bang port scan <= 40 luong, timeout >= 4s." -ForegroundColor Green
