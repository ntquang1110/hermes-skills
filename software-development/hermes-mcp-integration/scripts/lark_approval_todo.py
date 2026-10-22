#!/usr/bin/env python3
"""Lark Approval to-do list + batch approve (key KSP, international domain).

Đúng endpoint: GET /approval/v4/tasks/query?topic=1 (TodoApproval).
KHÔNG dùng tasks/search — trả toàn bộ task lịch sử (bẫy 09/08).

Usage:
  python lark_approval_todo.py                  # chỉ list to-do + phân loại
  python lark_approval_todo.py --approve        # approve hết (mặc định loại trừ "Yêu cầu duyệt chi")
  python lark_approval_todo.py --approve --include-duyet-chi   # approve cả duyệt chi (CẨN THẬN)
  python lark_approval_todo.py --user ou_xxx    # user khác (mặc định đọc từ --user hoặc KSP user)

Đọc KSP_MCP_APP_ID/SECRET từ ~/AppData/Local/hermes/.env. Approve KHÔNG hoàn tác được.
"""
import argparse, json, os, sys, time, urllib.request, urllib.error

HOME = os.path.expanduser("~")
ENV_FILE = os.path.join(HOME, "AppData", "Local", "hermes", ".env")
EXCLUDE_DEFAULT = "Yêu cầu duyệt chi"
API = "https://open.larksuite.com/open-apis"


def load_env():
    env = {}
    with open(ENV_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def get_token(env):
    req = urllib.request.Request(
        f"{API}/auth/v3/tenant_access_token/internal",
        data=json.dumps({"app_id": env["KSP_MCP_APP_ID"], "app_secret": env["KSP_MCP_APP_SECRET"]}).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        tok = json.loads(r.read().decode()).get("tenant_access_token", "")
    if not tok:
        raise RuntimeError("Không lấy được tenant_access_token — check KSP_MCP_* trong .env")
    return tok


def todo_tasks(token, user_id):
    """GET /approval/v4/tasks/query?topic=1 — trả data.tasks[] (KHÔNG phải task_list)."""
    out, page_token = [], ""
    while True:
        url = f"{API}/approval/v4/tasks/query?user_id={user_id}&topic=1&page_size=100&user_id_type=open_id"
        if page_token:
            url += f"&page_token={page_token}"
        req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token})
        with urllib.request.urlopen(req, timeout=30) as r:
            resp = json.loads(r.read().decode())
        if resp.get("code") != 0:
            raise RuntimeError(f"tasks/query lỗi {resp.get('code')} {resp.get('msg')}")
        data = resp.get("data", {})
        out.extend(data.get("tasks") or [])
        if not data.get("has_more"):
            break
        page_token = data.get("page_token", "")
    return out


def approve(token, user_id, t, comment):
    body = {
        "approval_code": t["definition_code"],   # KHÔNG phải approval.code (tasks/search field)
        "instance_code": t["process_code"],       # KHÔNG phải instance.code
        "user_id": user_id,
        "task_id": t["task_id"],
        "comment": comment,
    }
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                f"{API}/approval/v4/tasks/approve?user_id_type=open_id",
                data=json.dumps(body).encode(),
                headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as r:
                resp = json.loads(r.read().decode())
            if resp.get("code") == 0:
                return True, "OK"
            return False, f"{resp.get('code')} {resp.get('msg','')}"
        except urllib.error.HTTPError as e:
            raw = e.read().decode()[:150]
            if e.code in (429, 500, 502, 503):
                time.sleep(2)
                continue
            return False, f"HTTP-{e.code} {raw}"
        except Exception:
            time.sleep(2)
            continue
    return False, "FAIL-3x"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--approve", action="store_true", help="approve các task (mặc định loại trừ duyệt chi)")
    ap.add_argument("--include-duyet-chi", action="store_true", help="approve cả Yêu cầu duyệt chi (CẨN THẬN)")
    ap.add_argument("--user", default="ou_eac881f6920ef15f97970faf059ddc1f", help="open_id của user cần xử lý")
    ap.add_argument("--comment", default="Duyệt theo chỉ đạo Quang")
    args = ap.parse_args()

    env = load_env()
    token = get_token(env)
    tasks = todo_tasks(token, args.user)

    from collections import Counter
    c = Counter(t.get("definition_name", "?") for t in tasks)
    print(f"=== TODO ({len(tasks)}) ===")
    for name, n in c.most_common():
        print(f"{n:4d}  {name}")

    if not args.approve:
        return

    targets = tasks
    if not args.include_duyet_chi:
        targets = [t for t in tasks if EXCLUDE_DEFAULT not in t.get("definition_name", "")]
        print(f"\nLoại trừ '{EXCLUDE_DEFAULT}'. Approve {len(targets)} task.")
    else:
        print(f"\nApprove CẢ duyệt chi: {len(targets)} task. KHÔNG hoàn tác được!")

    ok = fail = 0
    for t in targets:
        success, msg = approve(token, args.user, t, args.comment)
        init = ", ".join(t.get("initiator_names") or [])
        print(("✅" if success else "❌"), t.get("definition_name"), init, t.get("task_id"), msg)
        if success:
            ok += 1
        else:
            fail += 1
        time.sleep(0.3)
    print(f"\nDone: OK={ok} FAIL={fail}")


if __name__ == "__main__":
    main()
