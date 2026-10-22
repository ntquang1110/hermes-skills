#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quet toan bo danh muc san pham cua mot website doi thu (WordPress/WooCommerce
hoac HTML tinh) va xuat JSON + bang tom tat.

Da chay that tren greentechvs.com (77 san pham, SSL het han).

Vi du:
  python crawl-catalog.py --domain greentechvs.com --sitemap product-sitemap.xml \
      --out greentech_products.json

  # khong co sitemap -> crawl tu trang danh muc (tu tim so trang)
  python crawl-catalog.py --domain example.com --listing /san-pham/ --out out.json

  # tu doan sitemap
  python crawl-catalog.py --domain example.com --out out.json

Luu y:
- Tu dong bo qua loi chung chi SSL (ssl._create_unverified_context).
- MSYS/Windows: KHONG dung /tmp, mac dinh ghi vao ~/httptmp.
- Chi doc HTML, khong thuc thi JS. Site render bang JS se tra ve rong.
"""
import argparse
import collections
import html
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

CTX = ssl._create_unverified_context()
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
HDR = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "vi,en;q=0.8",
}

SITEMAP_CANDIDATES = [
    "product-sitemap.xml", "products-sitemap.xml", "san-pham-sitemap.xml",
    "page-sitemap.xml", "post-sitemap.xml", "product_cat-sitemap.xml",
    "sitemap_index.xml", "sitemap.xml",
]

# duoi URL san pham WooCommerce: -i.<shopid>.<itemid>
RE_ITEM_ID = re.compile(r"-i\.\d+\.\d+")
# URL san pham thong thuong: slug dai, khong phai trang he thong
SKIP_SLUGS = {
    "san-pham", "products", "shop", "cua-hang", "cart", "gio-hang",
    "checkout", "thanh-toan", "my-account", "tai-khoan", "lien-he",
    "gioi-thieu", "about", "tuyen-dung", "tin-tuc", "blog", "kien-thuc",
    "feed", "wp-json", "wp-admin", "wp-content", "page", "category",
    "product-category", "tag", "tu-khoa-san-pham", "danh-muc",
}

# Tien to duong dan chua san pham (dung cho site dat SP duoi 1 nhanh rieng)
PRODUCT_PREFIXES = (
    "san-pham", "products", "product", "shop", "cua-hang", "thuoc",
    "thuoc-thu-y", "thuoc-thuy-san", "thuoc-gia-cam", "thuoc-thu-cung",
    "thuc-pham", "hang-hoa", "dich-vu", "combo", "khuyen-mai", "catalog",
)

# Segment chac chan KHONG phai san pham
EXCLUDE_SEG = {
    "lien-he", "gioi-thieu", "about", "tuyen-dung", "tin-tuc", "blog",
    "kien-thuc", "page", "feed", "wp-json", "wp-admin", "wp-content",
    "tag", "tu-khoa-san-pham", "category", "danh-muc", "product-category",
    "author", "search", "cart", "gio-hang", "checkout", "thanh-toan",
    "tai-khoan", "my-account", "chinh-sach", "dieu-khoan", "faq",
    "lien-he-voi-chung-toi", "hoi-dap", "tuyen-dung-2",
}


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def fetch(url, tries=3, timeout=30):
    """GET co retry. Tra ve (html_text, error_str_or_None)."""
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=HDR)
            with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
                raw = r.read()
                enc = "utf-8"
                m = re.search(rb'charset=["\']?([\w-]+)', raw[:2000], re.I)
                if m:
                    enc = m.group(1).decode("ascii", "ignore")
                return raw.decode(enc, "ignore"), None
        except Exception as e:
            last = e
            if i < tries - 1:
                time.sleep(1.2 * (i + 1))
    return "", "%s: %s" % (type(last).__name__, str(last)[:160])


def text_of(s):
    s = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def which_sitemaps(base):
    """Tra ve DANH SACH (url, ten) cac sitemap doc duoc, uu tien sitemap san pham truoc.

    KHONG tra ve cai dau tien tim thay: mot lan fetch loi se khien script chon nham
    sitemap bai viet va bo sot gan het san pham (da dinh: 77 -> 3).
    """
    found, seen = [], set()
    robots, _ = fetch(base.rstrip("/") + "/robots.txt", tries=2, timeout=15)
    for m in re.finditer(r"(?im)^\s*sitemap:\s*(\S+)", robots):
        u = m.group(1).strip()
        if u not in seen:
            seen.add(u)
            found.append((u, os.path.basename(urllib.parse.urlparse(u).path)))
    for name in SITEMAP_CANDIDATES:
        u = base.rstrip("/") + "/" + name
        if u in seen:
            continue
        body, err = fetch(u, tries=2, timeout=20)
        if body and "<loc>" in body:
            seen.add(u)
            found.append((u, name))
    found.sort(key=lambda t: (0 if "product" in t[1].lower() else 1))
    return found


def which_sitemap(base):
    """Tuong thich nguoc: tra ve sitemap tot nhat, hoac (None, None)."""
    f = which_sitemaps(base)
    return f[0] if f else (None, None)


def urls_from_sitemap(sm_url, domain=None, depth=0, prefix=None):
    """Doc <loc> va chon ra URL san pham. Neu la sitemapindex thi de quy vao sitemap con.

    Thu tu uu tien:
      0. loc nam duoi nhanh san pham user chi ra (prefix, vd '/san-pham/')  <- sach nhat
      1. sitemap tu ten la sitemap san pham -> tin tuyet doi moi <loc>
      2. loc trong nhu trang chi tiet san pham
      3. host chiem uu the (de gom nhieu, co the lan bai viet)

    QUAN TRONG: o buoc 1 KHONG duoc ap heuristic slug. WooCommerce rat hay dat san pham
    o slug toan so (/1175/, /738/) hoac slug ngan, ap heuristic se loai oan.
    Da dinh loi nay: 77 -> 73 san pham.
    """
    body, err = fetch(sm_url, timeout=30)
    if not body:
        log("  [warn] khong doc duoc sitemap: " + str(err))
        return []
    locs = [html.unescape(x) for x in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", body)]
    if not locs:
        return []

    if "<sitemapindex" in body[:1500] and depth < 2:
        out = []
        ordered = sorted(locs, key=lambda u: (0 if _score_loc(u, prefix) else 1))
        for sub in ordered:
            got = urls_from_sitemap(sub, domain, depth + 1, prefix)
            if got:
                out.extend(got)
        return out

    # Uu tien 1 (manh nhat): chinh sitemap nay tu ten la sitemap san pham -> tin tuyet doi moi <loc>.
    # WooCommerce hay dat san pham o slug toan so (/1175/, /738/) nen KHONG duoc ap heuristic.
    # Phai dat TRUOC bo loc prefix: da dinh loi vinavetco bi cat 228 -> 97 vi loc prefix truoc.
    if "product" in sm_url.lower():
        cand = [u for u in locs if _not_listing_page(u)]
        if cand:
            return cand

    # Uu tien 2: loc nam duoi dung nhanh san pham user chi ra, vd /san-pham/.
    # Dung khi site khong co sitemap ten 'product' (Next.js, HTML tinh, CMS khac).
    if prefix:
        cand = [u for u in locs
                if prefix in urllib.parse.urlparse(u).path.lower()
                and _tail_after(u, prefix)]
        if len(cand) >= 3:
            log("  [prefix] loc duoc %d/%d URL theo '%s'" % (len(cand), len(locs), prefix))
            return cand

    # Uu tien 3: loc nao trong nhu trang chi tiet san pham
    prods = [u for u in locs if _is_product_url(u)]
    if prods:
        return prods

    # Uu tien 4 (cuoi, de gom nhieu): host chiem uu the trong chinh sitemap.
    # Nhieu site doi domain (vinavetco.com.vn -> vinavetco.com), loc khong chua domain
    # nguoi dung nhap nen loc theo domain se ra 0.
    # CANH BAO: buoc nay co the gom ca bai viet neu site khong co cau truc danh muc.
    host = _dominant_host(locs)
    if host:
        cand = [u for u in locs if _host_of(u) == host and _not_listing_page(u)]
        if cand:
            log("  [warn] dung fallback host: %d URL, CO THE LAN BAI VIET. Kiem tra lai." % len(cand))
            return cand
    return []


def _score_loc(u, prefix):
    if not prefix:
        return False
    return prefix in urllib.parse.urlparse(u).path.lower() and _tail_after(u, prefix)


def _tail_after(u, prefix):
    """Sau nhanh san pham phai con slug that (tranh chinh trang danh muc)."""
    p = urllib.parse.urlparse(u).path.lower()
    i = p.find(prefix)
    if i < 0:
        return False
    tail = p[i + len(prefix):].strip("/")
    if not tail:
        return False
    if re.search(r"\.(xml|txt|jpg|jpeg|png|webp|avif|pdf|css|js|json)$", tail, re.I):
        return False
    return "page" not in tail.split("/")[0]

    # Uu tien 2: loc nao trong nhu trang chi tiet san pham
    prods = [u for u in locs if _is_product_url(u)]
    if prods:
        return prods

    # Uu tien 3: host chiem uu the trong chinh sitemap.
    # Nhieu site doi domain (vinavetco.com.vn -> vinavetco.com), loc khong chua domain
    # nguoi dung nhap nen loc theo domain se ra 0.
    host = _dominant_host(locs)
    if host:
        cand = [u for u in locs if _host_of(u) == host and _not_listing_page(u)]
        if cand:
            return cand
    return []


def _host_of(u):
    return urllib.parse.urlparse(u).netloc.lower().replace("www.", "", 1)


def _dominant_host(locs):
    c = collections.Counter(_host_of(u) for u in locs if _host_of(u))
    return c.most_common(1)[0][0] if c else None


def _not_listing_page(u):
    """Loai trang danh muc goc + trang he thong; GIU ca slug toan so."""
    p = urllib.parse.urlparse(u).path.strip("/").lower()
    if p in ("san-pham", "products", "cua-hang", "shop", ""):
        return False
    segs = [s for s in p.split("/") if s]
    if any(s in EXCLUDE_SEG for s in segs):
        return False
    if re.search(r"\.(xml|txt|jpg|jpeg|png|webp|avif|pdf|css|js|json)$", p, re.I):
        return False
    return True


def _is_product_url(u):
    """True neu URL trong nhu trang chi tiet san pham (ho tro duong dan nhieu cap)."""
    p = urllib.parse.urlparse(u).path.strip("/")
    if not p:
        return False
    low = p.lower()
    if re.search(r"\.(xml|txt|jpg|jpeg|png|webp|avif|pdf|css|js|json)$", low, re.I):
        return False
    segs = [s for s in low.split("/") if s]
    if any(s in EXCLUDE_SEG for s in segs):
        return False
    if len(segs) >= 2 and segs[0] in PRODUCT_PREFIXES:
        return True
    if len(segs) == 1:
        s = segs[0]
        if s in SKIP_SLUGS or re.fullmatch(r"\d+", s):
            return False
        return len(s) > 3
    return False


def _looks_like_product(u, domain=None):
    """Dung cho href bat tu trang danh muc (co the la duong dan tuong doi)."""
    if u.startswith("/") and domain:
        u = "https://" + domain + u
    return u.startswith("http") and _is_product_url(u)


def urls_from_listing(base, listing, domain, max_pages=30):
    """Fallback khi khong co sitemap: doc trang danh muc + tu tim so trang."""
    seen, order = set(), []
    listing = "/" + listing.strip("/") + "/"
    for pg in range(1, max_pages + 1):
        u = base.rstrip("/") + listing + ("" if pg == 1 else "page/%d/" % pg)
        body, err = fetch(u)
        if not body:
            break
        found = set()
        for m in re.finditer(r'href=["\']([^"\']+)["\']', body):
            href = html.unescape(m.group(1)).split("#")[0].split("?")[0]
            if _looks_like_product(href, domain) or RE_ITEM_ID.search(href):
                if href not in seen:
                    seen.add(href)
                    order.append(href)
                    found.add(href)
        if not found:
            break
    return order


def extract(url, h):
    d = {"url": url, "slug": urllib.parse.urlparse(url).path.strip("/")}
    m = re.search(r"<title[^>]*>(.*?)</title>", h, re.S)
    d["title"] = text_of(m.group(1)) if m else ""

    m = (re.search(r'class="product_title[^"]*"[^>]*>(.*?)</h1>', h, re.S)
         or re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S))
    d["name"] = text_of(m.group(1)) if m else d["title"]
    # bo phan sau dau gach trong <title> kieu "Ten - Ten site"
    if not d["name"] and d["title"]:
        d["name"] = re.split(r"\s+[|\u2013\u2014-]\s+", d["title"])[0].strip()

    # gia
    prices = re.findall(
        r'<bdi>([^<]*)<span class="woocommerce-Price-currencySymbol">([^<]*)</span>', h)
    if prices:
        d["price"] = [text_of(a) + b for a, b in prices][:5]
    else:
        d["price"] = [text_of(x) for x in re.findall(
            r'class="woocommerce-Price-amount amount"><bdi>([^<]*)', h)][:5]

    d["cats"] = [text_of(x) for x in re.findall(r'rel="tag">([^<]+)</a>', h)][:8]

    m = re.search(
        r'(?is)<div[^>]*class="[^"]*woocommerce-product-details__short-description[^"]*"[^>]*>(.*?)</div>',
        h)
    d["short"] = text_of(m.group(1))[:900] if m else ""

    m = (re.search(r'(?is)<div[^>]*id="tab-description"[^>]*>(.*?)</div>\s*</div>', h)
         or re.search(
             r'(?is)<div[^>]*class="[^"]*woocommerce-Tabs-panel--description[^"]*"[^>]*>(.*?)</section>', h)
         or re.search(r'(?is)<div[^>]*id="tab-description"[^>]*>(.*)', h))
    d["desc"] = text_of(m.group(1))[:6000] if m else ""

    attrs = {}
    for k, v in re.findall(
            r'(?is)<th[^>]*class="woocommerce-product-attributes-item__label"[^>]*>(.*?)</th>\s*'
            r'<td[^>]*class="woocommerce-product-attributes-item__value"[^>]*>(.*?)</td>', h):
        attrs[text_of(k)] = text_of(v)[:600]
    d["attrs"] = attrs

    m = re.search(r'class="sku"[^>]*>([^<]+)<', h)
    d["sku"] = text_of(m.group(1)) if m else ""

    # tin hieu thuong mai
    d["has_cart"] = "add-to-cart" in h
    d["cta"] = sorted(set(re.findall(
        r"(Th\u00eam v\u00e0o gi\u1ecf|Mua ngay|\u0110\u1eb7t h\u00e0ng|Li\u00ean h\u1ec7|"
        r"Y\u00eau c\u1ea7u b\u00e1o gi\u00e1|Nh\u1eadn b\u00e1o gi\u00e1|Add to cart|Contact)", h)))
    d["has_form"] = bool(re.search(r"wpcf7|contact-form|elFSForm", h))
    d["n_images"] = len(set(re.findall(
        r'wp-content/uploads/[^"\'\s>]+\.(?:jpg|jpeg|png|webp|avif)', h, re.I)))
    d["has_related"] = "related products" in h.lower()

    blob = (d["name"] + " " + " ".join(d["cats"]) + " " + d["desc"] + " " + d["short"])
    d["is_herbal"] = bool(re.search(
        r"th\u1ea3o d\u01b0\u1ee3c|chi\u1ebft xu\u1ea5t|d\u1ecbch chi\u1ebft|th\u1ea3o m\u1ed9c|"
        r"t\u1ecfi|ngh\u1ec7|oregano|qu\u1ebf|g\u1eebng|h\u01b0\u01a1ng th\u1ea3o|"
        r"kinh gi\u1edbi|x\u1ea1 h\u01b0\u01a1ng|khuynh di\u1ec7p|keo ong|propolis|"
        r"herbal|extract|botanical", blob, re.I))
    d["mentions_import"] = bool(re.search(
        r"nh\u1eadp kh\u1ea9u|nh\u1eadp t\u1eeb|imported", blob, re.I))
    d["mentions_no_abx"] = bool(re.search(
        r"kh\u00f4ng kh\u00e1ng sinh|h\u1ea1n ch\u1ebf kh\u00e1ng sinh|"
        r"thay th\u1ebf kh\u00e1ng sinh|antibiotic[- ]free", blob, re.I))
    d["has_dosage"] = bool(re.search(
        r"li\u1ec1u|h\u00f2a|tr\u1ed9n|ml/|g/|kg th\u1ec3 tr\u1ecdng|n\u01b0\u1edbc u\u1ed1ng|dosage",
        blob, re.I))
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", required=True, help="vd greentechvs.com")
    ap.add_argument("--scheme", default="https")
    ap.add_argument("--sitemap", default=None, help="ten file sitemap san pham")
    ap.add_argument("--listing", default=None, help="duong dan trang danh muc, vd /san-pham/")
    ap.add_argument("--prefix", default=None,
                    help="nhanh chua san pham de loc, vd /san-pham/. Tu suy ra tu --listing")
    ap.add_argument("--out", default=None)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0, help="0 = khong gioi han")
    ap.add_argument("--dump-html-dir", default=None,
                    help="luu ca HTML goc de doc lai bang mat (tuy chon)")
    a = ap.parse_args()

    base = a.scheme + "://" + a.domain

    # Nhanh san pham: tin hieu SACH NHAT de tach san pham khoi bai viet.
    # Luon truyen URL user dua (--listing) de suy ra.
    prefix = a.prefix or (("/" + a.listing.strip("/") + "/") if a.listing else None)
    if prefix and not prefix.startswith("/"):
        prefix = "/" + prefix
    if prefix:
        log("[prefix] " + prefix)
    urls = []

    if a.sitemap:
        urls = urls_from_sitemap(base + "/" + a.sitemap.strip("/"), a.domain, prefix=prefix)
    if not urls:
        best, best_n = [], 0
        for sm_url, sm_name in which_sitemaps(base):
            got = urls_from_sitemap(sm_url, a.domain, prefix=prefix)
            if not got:
                continue
            log("[sitemap] %-26s -> %4d URL" % (sm_name, len(got)))
            if "product" in sm_name.lower():
                urls = got          # sitemap san pham: tin ngay, khong can so sanh
                break
            if len(got) > best_n:
                best, best_n = got, len(got)
        if not urls:
            urls = best
    if not urls and a.listing:
        log("[listing] " + a.listing)
        urls = urls_from_listing(base, a.listing, a.domain)
    if not urls:
        for guess in ("/san-pham/", "/products/", "/cua-hang/", "/shop/", "/"):
            log("[listing thu] " + guess)
            urls = urls_from_listing(base, guess, a.domain)
            if urls:
                break

    urls = [u for u in dict.fromkeys(urls)]
    if a.limit:
        urls = urls[:a.limit]

    if not urls:
        log("[LOI] khong tim duoc URL san pham nao.")
        log("      Site co the render bang JS, hoac chan bot. Thu mo bang browser that.")
        sys.exit(2)

    log("[crawl] %d URL san pham" % len(urls))
    if a.dump_html_dir:
        os.makedirs(a.dump_html_dir, exist_ok=True)

    out = []
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(fetch, u): u for u in urls}
        done = 0
        for f in as_completed(futs):
            u = futs[f]
            h, err = f.result()
            done += 1
            if err or not h:
                log("  [%d/%d] LOI %s -> %s" % (done, len(urls), u, err))
                continue
            if a.dump_html_dir:
                fn = re.sub(r"[^\w.-]", "_", urllib.parse.urlparse(u).path.strip("/"))[:90] or "root"
                try:
                    with open(os.path.join(a.dump_html_dir, fn + ".html"), "w",
                              encoding="utf-8") as fh:
                        fh.write(h)
                except OSError:
                    pass
            out.append(extract(u, h))
            if done % 10 == 0:
                log("  ... %d/%d" % (done, len(urls)))

    out.sort(key=lambda d: d["name"].lower())
    dest = a.out or os.path.join(os.path.expanduser("~"), "httptmp",
                                 a.domain.replace(".", "_") + "_products.json")
    os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)

    with_price = sum(1 for d in out if d["price"])
    log("")
    log("=" * 96)
    log("%-52s %-20s %s" % ("TEN", "GIA", "DANH MUC"))
    log("=" * 96)
    for i, d in enumerate(out, 1):
        log("%3d. %-48s %-20s %s" % (
            i, d["name"][:48],
            (" | ".join(d["price"]))[:20] if d["price"] else "(khong gia)",
            ", ".join(d["cats"])[:44]))
    log("=" * 96)
    log("Tong san pham      : %d" % len(out))
    log("Co gia niem yet    : %d" % with_price)
    log("Co bang lieu dung  : %d" % sum(1 for d in out if d["has_dosage"]))
    log("Co thanh phan thao duoc: %d" % sum(1 for d in out if d["is_herbal"]))
    log("Co nut add-to-cart : %d" % sum(1 for d in out if d["has_cart"]))
    if out and with_price == 0:
        log("")
        log(">>> 0/%d co gia + nut 'Lien he' => MO HINH CATALOGUE B2B, khong phai cua hang." % len(out))
        log("    Day la LUACHON chien luoc, khong phai loi. Ghi vao bao cao.")
    log("")
    log("Da luu -> " + dest)


if __name__ == "__main__":
    main()
