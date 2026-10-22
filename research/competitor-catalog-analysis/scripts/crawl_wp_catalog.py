#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Crawl toan bo danh muc san pham cua mot site WordPress/WooCommerce -> JSON.

Dung:
    python crawl_wp_catalog.py https://<domain> out.json

Tai sao script nay ton tai:
  - Site cong ty VN nho rat hay co chung chi SSL het han. `web_extract` va
    TinyFish fetch_content tra `target_unreachable`, curl tra 000 +
    SEC_E_CERT_EXPIRED. Script nay dung ssl._create_unverified_context()
    nen doc duoc binh thuong. Do NOT ket luan "site chet" khi gap loi do.
  - Lay tu sitemap thay vi crawl listing phan trang: mot request ra duoc
    tong so san pham that, khong so sot.
  - Ghi JSON + in tien do moi 10 trang: crawl 70+ trang khong mat du lieu
    neu dut giua duong.

Truong trich ra: url, slug, title, name, price, cats, short, desc, attrs, sku.
Ban do truong chi tiet: references/woocommerce-catalog-extraction.md
"""
import html
import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.request

CTX = ssl._create_unverified_context()
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
HDR = {"User-Agent": UA, "Accept-Language": "vi,en", "Accept": "text/html,*/*"}


def get(url, tries=2, timeout=30):
    """Fetch URL. Bo qua verify SSL (site VN hay het han cert)."""
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=HDR)
            with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
                return r.read().decode("utf-8", "ignore")
        except Exception as e:
            if i == tries - 1:
                return "ERR:" + str(e)[:120]
            time.sleep(1.5)
    return ""


def txt(s):
    s = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def product_urls(base):
    """Sitemap truoc, listing sau. Tra ve list URL san pham."""
    sm = get(base.rstrip("/") + "/product-sitemap.xml")
    if not sm.startswith("ERR:"):
        urls = re.findall(r"<loc>([^<]+)</loc>", sm)
        out = [u for u in urls if u.rstrip("/").split("/")[-1] not in ("san-pham", "product", "shop")]
        if out:
            return out
    # Fallback: sitemap index -> tim *product*.xml
    idx = get(base.rstrip("/") + "/sitemap.xml")
    for m in re.findall(r"<loc>([^<]*product[^<]*\.xml)</loc>", idx):
        sub = get(m)
        urls = re.findall(r"<loc>([^<]+)</loc>", sub)
        if urls:
            return urls
    return []


def parse_product(u, h):
    d = {"url": u, "slug": u.rstrip("/").split("/")[-1]}
    m = re.search(r"<title>(.*?)</title>", h, re.S)
    d["title"] = txt(m.group(1)) if m else ""
    m = re.search(r'class="product_title[^"]*"[^>]*>(.*?)</h1>', h, re.S) or \
        re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
    d["name"] = txt(m.group(1)) if m else d["title"]
    prices = re.findall(r'<bdi>([^<]*)<span class="woocommerce-Price-currencySymbol">([^<]*)</span>', h)
    if prices:
        d["price"] = [txt(a) + b for a, b in prices][:3]
    else:
        d["price"] = [txt(x) for x in re.findall(r'class="woocommerce-Price-amount amount"><bdi>([^<]*)', h)][:3]
    d["cats"] = [txt(x) for x in re.findall(r'rel="tag">([^<]+)</a>', h)][:6]
    m = re.search(r'(?is)<div[^>]*class="[^"]*woocommerce-product-details__short-description[^"]*"[^>]*>(.*?)</div>', h)
    d["short"] = txt(m.group(1))[:700] if m else ""
    m = re.search(r'(?is)<div[^>]*id="tab-description"[^>]*>(.*)', h)
    d["desc"] = txt(m.group(1))[:5000] if m else ""
    attrs = {}
    for k, v in re.findall(r'(?is)<th[^>]*class="woocommerce-product-attributes-item__label"[^>]*>(.*?)</th>\s*'
                           r'<td[^>]*class="woocommerce-product-attributes-item__value"[^>]*>(.*?)</td>', h):
        attrs[txt(k)] = txt(v)[:600]
    d["attrs"] = attrs
    m = re.search(r'class="sku"[^>]*>([^<]+)<', h)
    d["sku"] = txt(m.group(1)) if m else ""
    return d


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    base, outfile = sys.argv[1], sys.argv[2]
    urls = product_urls(base)
    print("Tim thay " + str(len(urls)) + " URL san pham trong sitemap")
    if not urls:
        print("Khong doc duoc sitemap. Kiem tra cert bang: curl -skI " + base)
        sys.exit(2)
    prods = []
    for n, u in enumerate(urls, 1):
        h = get(u)
        if h.startswith("ERR:"):
            print("  [" + str(n) + "] LOI " + u + " -> " + h[:70])
            continue
        prods.append(parse_product(u, h))
        if n % 10 == 0:
            print("  ... " + str(n) + "/" + str(len(urls)))
            json.dump(prods, open(outfile, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(prods, open(outfile, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    noprice = sum(1 for p in prods if not p["price"])
    print("\nDa luu " + str(len(prods)) + " san pham -> " + outfile)
    print("  co gia: " + str(len(prods) - noprice) + " | khong gia: " + str(noprice))
    print("  co SKU: " + str(sum(1 for p in prods if p["sku"]))
          + " | co attr: " + str(sum(1 for p in prods if p["attrs"])))


if __name__ == "__main__":
    main()
