#!/usr/bin/env python3
"""Doc reply/comment cua MOT post Threads bang session da luu.

Vi sao can script nay: mo post bang guest (web_extract / browser khong cookie)
chi tra ve BAI CHINH, phan reply bi chan sau login wall ("Log in or sign up
for Threads"). Muon doc comment that de audit bai bi che thi phai nap cookies
trong ~/.hermes/threads_state.json roi render bang Playwright.

Dung:
  "<HERMES_VENV>/Scripts/python.exe" read_threads_replies.py <post_url> [out.json]

  HERMES_VENV = C:/Users/NTQUANG_DELL/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe

PITFALL da gap 2026-10-19:
- Phai goi bang python cua HERMES VENV (3.11). `python` tran tren host nay la
  C:\\Python314, ban playwright o do import greenlet loi
  (`ModuleNotFoundError: No module named 'greenlet._greenlet'`) -> script chet
  ngay dong import.
- Neu terminal tool tu choi lenh voi loi guard kieu
  `ValueError: open: embedded null character in path` (no doc nham script duoc
  tham chieu), doi cach goi: `cd <dir> && VP="<venv python>" && "$VP" ./script.py`.
- Giu `headless=True`: post cong khai + cookie hop le la doc duoc, khong can mo
  cua so that.

Output: JSON {url, items[], body} + in ra stderr so container va so comment.
`items` gom ca post chinh lan reply; loc theo dong dau tien (username) de tach
chu bai vs comment nguoi khac.
"""
import json, sys
from pathlib import Path

from playwright.sync_api import sync_playwright

STATE_FILE = Path.home() / ".hermes" / "threads_state.json"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    url = sys.argv[1]
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.home() / "hermes-temp" / "threads_replies.json"
    out.parent.mkdir(parents=True, exist_ok=True)

    if not STATE_FILE.exists():
        print(f"KHONG CO SESSION: {STATE_FILE} — chay threads_login.py truoc.", file=sys.stderr)
        sys.exit(1)
    state = json.load(open(STATE_FILE, encoding="utf-8"))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        ctx = browser.new_context(
            viewport={"width": 1280, "height": 1200},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
        )
        ctx.add_cookies(state.get("cookies", []))
        page = ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(6000)

        logged_in = page.locator('[aria-label*="Type to compose"]').count() > 0
        print(f"URL: {page.url} | logged_in: {logged_in}", file=sys.stderr)
        if not logged_in:
            print("Session het han hoac cookie chet — chay threads_login.py roi thu lai.", file=sys.stderr)

        for _ in range(14):
            page.mouse.wheel(0, 2600)
            page.wait_for_timeout(1500)

        for sel in ["text=/View more replies/i", "text=/more repl/i", "text=/Xem thêm/i"]:
            try:
                for _ in range(min(page.locator(sel).count(), 6)):
                    page.locator(sel).first.click(timeout=2500)
                    page.wait_for_timeout(2500)
            except Exception:
                pass

        items = page.evaluate(
            """() => Array.from(document.querySelectorAll('[data-pressable-container="true"]'))
                       .map(n => (n.innerText || '').trim()).filter(Boolean)"""
        )
        body = page.evaluate("() => document.body.innerText || ''")
        json.dump({"url": page.url, "items": items, "body": body},
                  open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

        others = [t for t in items if t.split("\n")[0].strip() not in ("", "ntquang1110")]
        print(f"containers: {len(items)} | comment nguoi khac: {len(others)} | body chars: {len(body)}", file=sys.stderr)
        print(f"saved: {out}", file=sys.stderr)
        browser.close()


if __name__ == "__main__":
    main()
