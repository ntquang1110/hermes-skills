# -*- coding: utf-8 -*-
"""CONFIG GUARDIAN V3 — ép cứng config.yaml + auth.json khỏi reset/đổi provider.
Canh: model, providers, fallback_providers, custom_providers (rác), moa, model_aliases (config)
+ credential pool bytedance (reset exhausted-429 tạm thời) + custom:unsloth base_url (auth.json).
Chạy qua cron no_agent (15 phút/lần). Im lặng khi OK.

⚠️ TRƯỚC KHI BÀN GIAO: phải LIST-CONFIRM-APPLY.
- User tự sửa config.yaml làm chuẩn ("follow theo file này") → PAUSE cron guard NGAY
  (guard golden cũ sẽ REVERT file user trong tick kế tiếp), list config theo ĐÚNG file,
  user confirm → mới cập nhật GOLDEN dưới đây theo đúng list → resume cron → test.
- yaml.safe_dump toàn file làm ALPHABETIZE config (user có thể không đồng ý "thứ tự khác").
  Nếu user quan tâm thứ tự file gốc: text-line patch, không dump toàn file.

Test trước bàn giao:
1. Chạy guard khi OK → stdout rỗng, exit 0 (im lặng).
2. Bẻ config + auth (đổi provider, chèn custom_providers[1], đánh dấu bytedance exhausted-429,
   lệch unsloth base_url) → guard tự sửa TẤT CẢ + báo cáo từng mục.
3. cronjob(action=run) → execution_success=true.
"""
import os, sys, subprocess, shutil, json, time, yaml

CFG = os.path.join(os.environ.get("LOCALAPPDATA", r"C:\Users\NTQUANG_DELL\AppData\Local"), "hermes", "config.yaml")
AUTH = os.path.join(os.path.dirname(CFG), "auth.json")

# GOLDEN — CẬP NHẬT THEO FILE USER CONFIRM (đừng tự bịa). Ví dụ mặc định dưới đây.
GOLDEN = {
    "model": {
        "default": "deepseek-v4-flash-ga-260731",
        "provider": "bytedance",
        "base_url": "https://ark.ap-southeast.bytepluses.com/api/v3"
    },
    "providers": {
        "unsloth": {"base_url": "http://192.168.1.3:18888", "stale_timeout_seconds": 900, "ttfb_timeout_seconds": 600},
        "custom": {"stale_timeout_seconds": 900, "ttfb_timeout_seconds": 600},
        "bytedance": {"base_url": "https://ark.ap-southeast.bytepluses.com/api/v3", "stale_timeout_seconds": 900, "ttfb_timeout_seconds": 600}
    },
    "fallback_providers": [
        {"provider": "bytedance", "model": "deepseek-v4-flash-ga-260731"},
        {"provider": "unsloth", "model": "unsloth/Ministral-3-8B-Instruct-2512-GGUF"},
        {"provider": "gemini", "model": "gemini-flash-lite-latest"}
    ],
    "moa": {
        "enabled": False,
        "aggregator": {"provider": "bytedance", "model": "deepseek-v4-flash-ga-260731"}
    },
    "agent": {
        "api_max_retries": 0
    }
}

UNSLOTH_PROXY = "http://192.168.1.3:18888"

def load_conf():
    try:
        with open(CFG, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return None

def get_path(cfg, key):
    cur = cfg
    for part in key.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur

def load_auth():
    try:
        with open(AUTH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def desktop_running():
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "@(Get-Process Hermes -ErrorAction SilentlyContinue).Count"],
            capture_output=True, text=True, timeout=20)
        n = out.stdout.strip().splitlines()[-1] if out.stdout.strip() else "0"
        return int(n) > 0
    except Exception:
        return False

def kill_desktop():
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-Process Hermes -ErrorAction SilentlyContinue | Stop-Process -Force"],
            capture_output=True, text=True, timeout=30)
        return True
    except Exception:
        return False

def fix_config():
    cfg = load_conf()
    if not cfg:
        return False
    cfg["model"] = GOLDEN["model"]
    cfg["providers"] = GOLDEN["providers"]
    cfg["fallback_providers"] = GOLDEN["fallback_providers"]
    if "moa" not in cfg:
        cfg["moa"] = {}
    cfg["moa"]["enabled"] = GOLDEN["moa"]["enabled"]
    cfg["moa"]["aggregator"] = GOLDEN["moa"]["aggregator"]
    if "agent" not in cfg:
        cfg["agent"] = {}
    cfg["agent"]["api_max_retries"] = GOLDEN["agent"]["api_max_retries"]
    if "custom_providers[1]" in cfg:
        del cfg["custom_providers[1]"]
    shutil.copy2(CFG, CFG + f".guard-{time.strftime('%Y%m%d-%H%M%S')}.bak")
    with open(CFG, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, allow_unicode=True, sort_keys=False)
    return True

def fix_auth():
    d = load_auth()
    if not d:
        return False, []
    pool = d.get("credential_pool", {})
    fixed = []
    for e in pool.get("bytedance", []):
        # 429 TPM limit là TẠM THỜI — key chưa chết; pool exhausted làm Hermes né primary
        if e.get("last_status") == "exhausted" and e.get("last_error_code") == 429:
            e.pop("last_status", None); e.pop("last_error_code", None); e.pop("last_error_reason", None)
            fixed.append("bytedance reset trạng thái exhausted (429 tạm thời) → thử lại")
    for e in pool.get("custom:unsloth", []):
        if e.get("base_url") != UNSLOTH_PROXY:
            e["base_url"] = UNSLOTH_PROXY
            fixed.append("custom:unsloth base_url đồng bộ → " + UNSLOTH_PROXY)
    if not fixed:
        return False, []
    shutil.copy2(AUTH, AUTH + f".guard-{time.strftime('%Y%m%d-%H%M%S')}.bak")
    with open(AUTH, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    return True, fixed

def main():
    if not os.path.exists(CFG):
        print(f"⚠ CONFIG GUARD: {CFG} không tồn tại!")
        return
    cfg = load_conf()
    if cfg is None:
        print("⚠ CONFIG GUARD: không đọc được config.yaml (YAML lỗi?)")
        return

    checks = [
        ("model.default", GOLDEN["model"]["default"]),
        ("model.provider", GOLDEN["model"]["provider"]),
        ("fallback_providers", GOLDEN["fallback_providers"]),
        ("moa.enabled", GOLDEN["moa"]["enabled"]),
        ("agent.api_max_retries", GOLDEN["agent"]["api_max_retries"])
    ]

    deviated = []
    for key, want in checks:
        got = get_path(cfg, key)
        if got != want:
            deviated.append((key, got, want))

    report = []
    if deviated or "custom_providers[1]" in cfg:
        lines = ["⚠ CONFIG BỊ THAY ĐỔI / RESET — guardian tự phục hồi:"]
        for key, got, want in deviated:
            lines.append(f"  - {key}: '{got}' → '{want}'")
        if "custom_providers[1]" in cfg:
            lines.append("  - Phát hiện rác 'custom_providers[1]' → Đã dọn.")
        ok = fix_config()
        lines.append("  Kết quả phục hồi: " + ("ĐÃ KHÔI PHỤC THÀNH CÔNG" if ok else "LỖI"))
        report.extend(lines)

    auth_fixed, auth_msgs = fix_auth()
    if auth_fixed:
        report.append("⚠ CREDENTIAL POOL — guardian tự sửa:")
        report.extend(f"  - {m}" for m in auth_msgs)

    if report:
        if desktop_running():
            kill_desktop()
            report.append("  Desktop Hermes.exe đang chạy (nguồn reset) → đã tắt.")
        print("\n".join(report))
    else:
        if desktop_running():
            print("⚠ CONFIG GUARD: config chuẩn nhưng desktop Hermes.exe ĐANG CHẠY — nên đóng để tránh ghi đè.")

if __name__ == "__main__":
    main()
