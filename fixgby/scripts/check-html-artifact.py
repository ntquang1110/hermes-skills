#!/usr/bin/env python
"""Kiem tra TINH mot file HTML truoc khi publish. Chay: python check-html-artifact.py <file.html> [file2.html ...]

Kiem cai gi (deu la loi da tung xay ra that trong du an fixgby):
  1. Bang <table>  -> spec Quang: 0 bang, thay bang diagram
  2. Entity hong   -> &a1; , &Dstrok; , 'X;&#nnn;' (dau ';' mo coi) lam hien ra ky tu rac
  3. font-size khai bao < 12.4px -> luat >= 12,5px sau co
  4. meta viewport + lang="vi" (tieng Viet co dau bat buoc)
  5. Dem PMID / tag H / so dong / so byte / so tu -> de doi chieu voi bao cao
  6. Placeholder chua xoa: "dang verify", "se vao", "TODO", "cap nhat sau"
  7. the <div> lech so luong mo/dong

CANH BAO: day la kiem TINH. Do bo cuc that (tran ngang, co chu sau khi co, do tuong phan)
      PHAI do bang browser_console, khong doan. Xem SKILL.md muc "Deliverable cho Quang".
"""
import sys, re, os
from html.entities import html5

HARD = []   # loi phai sua
SOFT = []   # canh bao

def check(path):
    s = open(path, encoding="utf-8").read()
    txt = re.sub(r"<script.*?</script>", "", s, flags=re.S)
    txt = re.sub(r"<style.*?</style>", "", txt, flags=re.S)
    plain = re.sub(r"<[^>]+>", " ", txt)
    plain = re.sub(r"&#?\w+;", " ", plain)

    print("=" * 74)
    print(os.path.basename(path))
    print(f"  dong {s.count(chr(10)) + 1} · byte {len(s.encode('utf-8'))} · tu {len(plain.split())}")

    # 1. bang
    n_tbl = len(re.findall(r"<table\b", s, re.I))
    (HARD if n_tbl else SOFT).append(f"{path}: {n_tbl} bang <table> (spec: 0 bang)")
    print(f"  bang <table>            : {n_tbl}   {'<-- VI PHAM' if n_tbl else 'OK'}")

    # 2. entity
    ents = sorted(set(re.findall(r"&[a-zA-Z0-9#]{1,8};", s)))
    unknown = [e for e in ents if not e.startswith("&#") and e[1:-1] not in html5]
    orphan = re.findall(r"[A-Za-z];&#", s)          # 'h;&#432;' -> hien ra 'h;'
    lone = re.findall(r"&[a-zA-Z]{1,8}[^a-zA-Z0-9#;]", s)  # '&amp' thieu ';'
    print(f"  entity la              : {len(unknown)}    {unknown[:6]}")
    print(f"  dau ';' mo coi         : {len(orphan)}    {orphan[:4]}")
    print(f"  '&' thieu ';'          : {len(lone)}    {[x[:12] for x in lone[:4]]}")
    for lst, msg in ((unknown, "entity khong ton tai"), (orphan, "dau ';' mo coi sau chu"),
                     (lone, "'&' thieu ';'")):
        if lst:
            HARD.append(f"{path}: {msg} ({len(lst)}) {lst[:4]}")

    # 3. font-size
    small = [f for f in re.findall(r"font-size:\s*([\d.]+)px", s) if float(f) < 12.4]
    print(f"  font-size < 12,4px      : {len(small)}   {sorted(set(small))[:6]}")
    if small:
        HARD.append(f"{path}: {len(small)} khai bao font-size < 12,4px")

    # 4. khung
    has_vp = 'name="viewport"' in s
    has_vi = 'lang="vi"' in s
    print(f"  meta viewport / lang vi : {has_vp} / {has_vi}")
    if not (has_vp and has_vi):
        SOFT.append(f"{path}: thieu meta viewport hoac lang=\"vi\"")

    # 5. dem
    pmids = set(re.findall(r"\b\d{7,8}\b", s))
    tagh = len(re.findall(r"tag H", s))
    print(f"  PMID khac nhau          : {len(pmids)}")
    print(f"  cho 'tag H'             : {tagh}")
    print(f"  so luong oitem          : {len(re.findall(r'class=.oitem', s))}")

    # 6. placeholder
    ph = [k for k in ("dang verify", "đang verify", "se vao", "sẽ vào", "TODO", "cap nhat sau", "cập nhật sau") if k in s]
    print(f"  placeholder sot lai     : {ph}")
    if ph:
        SOFT.append(f"{path}: con placeholder {ph}")

    # 7. div can
    op = len(re.findall(r"<div\b", s, re.I))
    cl = len(re.findall(r"</div>", s, re.I))
    print(f"  <div> mo / dong         : {op} / {cl}   {'<-- LECH' if op != cl else 'OK'}")
    if op != cl:
        HARD.append(f"{path}: <div> lech {op}/{cl}")

for p in sys.argv[1:]:
    check(p)

print("=" * 74)
if SOFT:
    print("CANH BAO:")
    for x in SOFT:
        print("  -", x)
if HARD:
    print("LOI PHAI SUA:")
    for x in HARD:
        print("  -", x)
    sys.exit(1)
print("TINH: sach. Buoc tiep theo: publish roi do bang browser_console (font, tran, tuong phan).")
