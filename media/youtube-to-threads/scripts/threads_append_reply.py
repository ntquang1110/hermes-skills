#!/usr/bin/env python3
"""Append ONE single-paragraph reply to a Threads thread — VERIFIED reliable recipe
(written 2026-08-24 after fixing a Herjavec thread).

WHY this exists:
  - Threads reply composer SUBMITS when keyboard.type emits a newline -> a reply
    with internal \\n truncates to its first paragraph and the rest is lost.
  - editors[-1] / fill() / textContent= all misfire on the reply editor once the
    thread has 2+ replies. JS-focusing the single contenteditable is reliable.
  - Threads auto-saves reply drafts; textContent='' does NOT clear Lexical's
    state. Must Ctrl+A+Backspace to clear.

Usage:
  python threads_append_reply.py <single-paragraph-text-file> <thread_url>

Constraints:
  - Content file MUST be a single paragraph with NO newlines (script enforces).
    For a desired multi-paragraph reply, post each paragraph as its own reply.
  - Links a fresh headless Chromium using the saved Threads session cookies.
"""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

STATE_FILE = Path.home() / ".hermes" / "threads_state.json"

def main():
    if len(sys.argv) < 3:
        print("usage: threads_append_reply.py <content.txt> <thread_post_url>", file=sys.stderr)
        sys.exit(1)
    content = open(sys.argv[1], encoding="utf-8").read().strip()
    url = sys.argv[2]
    if "\n" in content:
        print("ABORT: content has newlines (reply editor submits on \\n). Use one paragraph per reply.", file=sys.stderr)
        sys.exit(3)
    state = json.load(open(STATE_FILE))

    def ftext(page):
        return page.evaluate("()=>{const e=document.activeElement;return e?(e.textContent||'')+'':'(null)';}")

    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        ctx = b.new_context(viewport={"width":1280,"height":900},
                            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        ctx.add_cookies(state.get("cookies", []))
        page = ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=40000)
        page.wait_for_timeout(8000)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2500)
        page.locator('div[role="button"]:has-text("Reply")').first.click(force=True)
        page.wait_for_timeout(4500)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(600)
        # JS-focus the single reply contenteditable
        page.evaluate("""()=>{const el=document.querySelector('div[contenteditable="true"]');
            if(el){el.focus();} return document.activeElement?document.activeElement.tagName:'none';}""")
        page.wait_for_timeout(500)
        # clear auto-saved draft lexically (textContent='' does NOT clear Lexical)
        page.keyboard.press("Control+a")
        page.wait_for_timeout(300)
        page.keyboard.press("Backspace")
        page.wait_for_timeout(500)
        page.keyboard.type(content, delay=6)
        page.wait_for_timeout(1200)
        got = ftext(page)
        if got.strip()[:30] != content.strip()[:30]:
            print("ABORT: text did not land in activeElement. No submit.", file=sys.stderr)
            print("  want:", content.strip()[:40], file=sys.stderr)
            print("  got :", got.strip()[:40], file=sys.stderr)
            b.close(); sys.exit(2)
        page.keyboard.press("Control+Enter")
        page.wait_for_timeout(9000)
        print("SUBMITTED")
        b.close()

if __name__ == "__main__":
    main()