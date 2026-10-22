#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tải CLAIM NGUYÊN VĂN của patent từ Google Patents (server-rendered HTML).

Dùng khi cần phân tích novelty / inventive step / rủi ro xâm phạm: KHÔNG suy đoán
từ abstract — luôn đọc claim gốc + các thông số trong phần mô tả (%/°C/tỉ lệ/ví dụ).

Ví dụ:
    python patent_claims.py EP2022343B1
    python patent_claims.py CN102250159A CN105145977A US20040168266A1
    python patent_claims.py --save "/tmp/pat" CN101883575B     # lưu HTML+txt để grep tiếp
    python patent_claims.py --full CN102250159A                # in thêm phần mô tả (để grep thông số)

Ghi chú kỹ thuật (verify 24/09/2026):
- Trang `patents.google.com/patent/<PN>/en` KHÔNG bị chặn (HTTP 200, 150-600 KB) khi
  gửi UA giả trình duyệt. Phiên 24/09/2026 đã đọc claim của EP2022343B1,
  US20040168266A1, CN102250159A, CN105145977A, CN101883575B bằng logic này (bản curl;
  bản urllib ở đây tương đương — nếu bị 403/503 thì thử lại sau 45-60s hoặc chuyển
  sang `curl -s -A "<UA>" -o file.html "<url>"`).
- XHR search (`/xhr/query?url=q%3D...`) bị throttle sớm hơn (~3-5 request → trang
  "<title>Sorry...</title>"). Dùng script này cho claim, dùng XHR/trang `/?q=` cho tra cứu.
- Layout mới KHÔNG còn `section[itemprop="claims"]` → nếu dùng browser_console thì
  dùng `document.body.innerText.slice(innerText.indexOf('Claims ('))`.
"""
import argparse
import html
import os
import re
import sys
import time
import urllib.error
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
CLAIM_MARKERS = ("Claims (", "What is claimed", "I claim")


def fetch(pn, tries=3, wait=45):
    url = "https://patents.google.com/patent/%s/en" % pn
    for attempt in range(1, tries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read().decode("utf-8", "ignore")
        except urllib.error.HTTPError as exc:
            print("  ! %s: HTTP %s (lan %d/%d)" % (pn, exc.code, attempt, tries), file=sys.stderr)
        except Exception as exc:  # timeout, DNS, TLS...
            print("  ! %s: %s (lan %d/%d)" % (pn, exc, attempt, tries), file=sys.stderr)
        if attempt < tries:
            time.sleep(wait)
    return None


def to_text(raw):
    s = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
    s = re.sub(r"(?is)<br\s*/?>", "\n", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\xa0]+", " ", s)
    return re.sub(r"\n\s*\n+", "\n", s)


def extract(text, full=False):
    """Trả về dict: claims / abstract / status / expiration / (tuỳ chọn) description."""
    out = {"chars": len(text)}
    for marker in CLAIM_MARKERS:
        i = text.find(marker)
        if i < 0:
            continue
        end = text.find("Patent Citations", i)
        out["claims"] = text[i:end if end > i else i + 4000].strip()
        break
    else:
        out["claims"] = "(không tìm thấy mốc 'Claims (' — kiểm tra lại trang, có thể bị chặn)"

    i = text.find("Abstract")
    if i >= 0:
        out["abstract"] = text[i:i + 1200].strip()

    m = re.search(r"Status\s+(Active|Expired|Pending|Granted)", text)
    if m:
        out["status"] = m.group(1)
    m = re.search(r"(\d{4}-\d{2}-\d{2})\s*Anticipated expiration", text)
    if m:
        out["expiration"] = m.group(1)

    if full:
        i = text.find("Description")
        if i >= 0:
            j = text.find("Claims (", i)
            out["description"] = text[i:j if j > i else i + 20000].strip()
    return out


def main():
    ap = argparse.ArgumentParser(description="Tải claim nguyên văn từ Google Patents")
    ap.add_argument("publications", nargs="+", help="số công bố, vd EP2022343B1")
    ap.add_argument("--full", action="store_true", help="in thêm phần mô tả (để grep thông số)")
    ap.add_argument("--save", metavar="DIR", help="lưu HTML + TXT vào thư mục để grep tiếp")
    ap.add_argument("--wait", type=int, default=45, help="giây chờ giữa các lần retry (mặc định 45)")
    args = ap.parse_args()

    if args.save:
        os.makedirs(args.save, exist_ok=True)

    for idx, pn in enumerate(args.publications):
        if idx:
            time.sleep(3)  # tránh rate limit giữa các patent
        print("=" * 90)
        print("PATENT:", pn)
        raw = fetch(pn, wait=args.wait)
        if raw is None:
            print("  ✗ không tải được (503/403 sau 3 lần thử) — thử lại sau 45-60s, "
                  "hoặc browser_navigate tới cùng URL rồi đọc innerText")
            continue
        text = to_text(raw)
        if args.save:
            open(os.path.join(args.save, pn + ".html"), "w", encoding="utf-8").write(raw)
            open(os.path.join(args.save, pn + ".txt"), "w", encoding="utf-8").write(text)
            print("  (đã lưu %s.html / %s.txt)" % (pn, pn))
        data = extract(text, full=args.full)
        if "status" in data:
            print("  TRẠNG THÁI: %s%s" % (data["status"],
                  " | hết hạn dự kiến %s" % data["expiration"] if "expiration" in data else ""))
        if "abstract" in data:
            print("\n--- ABSTRACT ---\n" + data["abstract"])
        print("\n--- CLAIMS ---\n" + data.get("claims", ""))
        if args.full and "description" in data:
            print("\n--- DESCRIPTION (dùng search_files/grep để tìm %%, °C, tỉ lệ) ---\n"
                  + data["description"][:6000])


if __name__ == "__main__":
    main()
