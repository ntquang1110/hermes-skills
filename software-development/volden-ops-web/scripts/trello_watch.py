"""
Trello Watch — phát hiện card mới trên board Volden Ops App.
Cron chạy mỗi 15 phút. Chỉ in ra stdout khi CÓ card mới (watchdog pattern:
stdout rỗng = silent = không gửi gì; stdout có nội dung = gửi message).

Lists theo dõi: To do, Need fixed, Document, Testing
(Khi card mới xuất hiện ở bất kỳ list nào trong số này → báo về group)

State lưu tại: ~/AppData/Local/hermes/scripts/trello_state.json
Lần chạy đầu tiên: chỉ baseline (lưu state, không bắn card cũ).

Cron setup: job no_agent=true, schedule */15 * * * *, script = filename
tương đối tới ~/.hermes/scripts/ (KHÔNG absolute path — cron tool reject).
"""

import json
import os
import urllib.parse
import urllib.request

HOME = os.path.expanduser("~")
ENV_PATH = os.path.join(HOME, "AppData", "Local", "hermes", ".env")
STATE_PATH = os.path.join(HOME, "AppData", "Local", "hermes", "scripts", "trello_state.json")

BOARD_ID = "6a6b793f7e5888b26f2ad776"
TRACKED_LISTS = ["To do", "Need fixed", "Document", "Testing"]


def load_env():
    """Đọc TRELLO_API_KEY + TRELLO_TOKEN từ hermes .env"""
    env = {}
    try:
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, _, v = line.partition("=")
                    env[k.strip()] = v.strip().strip('"').strip("'")
    except Exception as e:
        print(f"⚠️ Không đọc được .env: {e}")
    return env


def api_get(url, key, token):
    sep = "&" if "?" in url else "?"
    full = f"{url}{sep}key={key}&token={token}"
    req = urllib.request.Request(full, headers={"User-Agent": "hermes-trello-watch"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def load_state():
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def main():
    env = load_env()
    key = env.get("TRELLO_API_KEY") or env.get("TRELLO_KEY")
    token = env.get("TRELLO_TOKEN")
    if not key or not token:
        print("⚠️ Thiếu TRELLO_API_KEY/TRELLO_TOKEN trong hermes .env — không watch được.")
        return

    try:
        lists = api_get(f"https://api.trello.com/1/boards/{BOARD_ID}/lists", key, token)
        cards = api_get(
            f"https://api.trello.com/1/boards/{BOARD_ID}/cards?fields=name,id,idList,url,desc",
            key, token,
        )
    except Exception as e:
        print(f"⚠️ Lỗi gọi Trello API: {e}")
        return

    list_names = {l["id"]: l["name"] for l in lists}
    state = load_state()
    is_first_run = not state
    new_cards = []

    for c in cards:
        list_name = list_names.get(c["idList"], "?")
        if list_name not in TRACKED_LISTS:
            continue
        if c["id"] not in state:
            desc = (c.get("desc") or "").strip().replace("\n", " ")[:200]
            new_cards.append({"id": c["id"], "name": c["name"], "list": list_name, "url": c.get("url", ""), "desc": desc})
            state[c["id"]] = {"name": c["name"], "list": list_name, "seen_at": None}

    if not is_first_run and new_cards:
        lines = []
        for card in new_cards:
            lines.append(f"🆕 **Card mới: {card['name']}**")
            lines.append(f"   📍 List: **{card['list']}**")
            if card["desc"]:
                lines.append(f"   📝 {card['desc']}")
            lines.append(f"   🔗 {card['url']}")
            lines.append("")
        print("\n".join(lines).strip())
        print("(Em đã nhận — sẽ lên plan trình anh duyệt trước khi xử lý.)")

    save_state(state)


if __name__ == "__main__":
    main()
