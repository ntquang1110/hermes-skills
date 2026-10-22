#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tach SKILL.md qua kho thanh router + references/, KHONG mat noi dung.

Tach la MOVE, khong phai rewrite: chu da chuyen giu nguyen byte.
Script tu chay 2 diff kiem mat mat o cuoi va exit code != 0 neu co mat.

CACH DUNG
---------
1. Sua KEEP_KEYS (giu inline) va MOVE_MAP (title substring -> file dich) duoi day.
2. Chay:  python split_skill_md.py <duong_dan_thu_muc_skill>
   Vi du:  python split_skill_md.py "D:/Hermes/hermes-home/skills/software-development/my-skill"

Section nao KHONG khop KEEP_KEYS lan MOVE_MAP se duoc GIU LAI trong SKILL.md va
in ra canh bao — de ban tu quyet, khong bao gio bi am tham bo di.

Cach tim title de dien vao bang: chay truoc voi MOVE_MAP rong, script in ra
danh sach heading kem so byte tung section.
"""
import io
import os
import re
import shutil
import sys
import time

# --------------------------------------------------------------------------
# 1. GIU INLINE trong SKILL.md (substring cua heading)
# --------------------------------------------------------------------------
KEEP_KEYS = [
    "When to use",
    "Overview",
    "Common Pitfalls",
    "Verification Checklist",
]

# --------------------------------------------------------------------------
# 2. CHUYEN sang references/ (substring cua heading  ->  ten file dich)
# --------------------------------------------------------------------------
MOVE_MAP = [
    # ("mot phan cua heading", "references/chu-de.md"),
]

# --------------------------------------------------------------------------
# 3. Mo ta ngan cho tung file dich, hien trong muc luc SKILL.md
# --------------------------------------------------------------------------
FILE_DESC = {
    # "references/chu-de.md": "noi dung gi",
}

HEADING = "## Chi tiết theo chủ đề"


def parse_sections(body):
    """Tach theo H1/H2, BO QUA dong trong ``` fence.

    Code block chua '# comment' ma regex ^# ngay tho nhan nham la heading —
    parse sai buoc nay lam mat ca code block.
    """
    lines = body.split("\n")
    fence = False
    secs = []
    for i, l in enumerate(lines):
        s = l.strip()
        if s.startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"^(#{1,2}) (.+)$", l)
        if m:
            secs.append({"start": i, "title": m.group(2).strip()})
    for n, s in enumerate(secs):
        s["end"] = secs[n + 1]["start"] if n + 1 < len(secs) else len(lines)
        s["text"] = "\n".join(lines[s["start"]:s["end"]]).rstrip() + "\n"
    return secs


def headings(txt):
    """Heading o moi cap (H1-H3), fence-aware — dung cho buoc verify."""
    fence, out = False, []
    for l in txt.split("\n"):
        s = l.strip()
        if s.startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"^(#{1,3}) (.+)$", l)
        if m:
            out.append(m.group(2).strip())
    return out


def content_lines(txt):
    """Dong noi dung, da loai dong trong va separator '---' do script tu them."""
    return {l.strip() for l in txt.split("\n") if l.strip() and l.strip() != "---"}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    skill_dir = sys.argv[1]
    src = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(src):
        print("  ! khong thay SKILL.md tai", src)
        return 2

    raw = io.open(src, encoding="utf-8").read()
    m = re.match(r"^---\n.*?\n---\n", raw, re.S)
    front, body = (m.group(0), raw[m.end():]) if m else ("", raw)

    secs = parse_sections(body)
    if not MOVE_MAP and not KEEP_KEYS:
        print("  === HEADING + so byte tung section (dien vao KEEP_KEYS / MOVE_MAP) ===")
        for s in secs:
            print("  %-7d %s" % (len(s["text"]), s["title"][:95]))
        return 0

    def keep(s):
        return any(k in s["title"] for k in KEEP_KEYS)

    def target(s):
        for k, f in MOVE_MAP:
            if k in s["title"]:
                return f
        return None

    kept, moves, unassigned = [], {}, []
    for s in secs:
        if keep(s):
            kept.append(s)
            continue
        f = target(s)
        if f:
            moves.setdefault(f, []).append(s)
        else:
            unassigned.append(s)
            kept.append(s)

    print("== PHAN LOAI ==")
    print("  giu inline :", len(kept), "section")
    for f, lst in sorted(moves.items()):
        print("  -> %-52s %2d section" % (f, len(lst)))
    if unassigned:
        print("  KHONG KHOP (giu lai) :", len(unassigned))
        for s in unassigned:
            print("     !", s["title"][:85])
        print("  -> muon chuyen thi them vao MOVE_MAP roi chay lai.")

    # ---- ghi references (nguyen van) ----
    wrote = []
    for f, lst in moves.items():
        p = os.path.join(skill_dir, f.replace("/", os.sep))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if os.path.exists(p):
            shutil.copy2(p, p + ".bak-" + time.strftime("%Y%m%d-%H%M%S"))
        out = ["# %s\n" % FILE_DESC.get(f, f.split("/")[-1]), ""]
        for s in lst:
            out.append("\n---\n")
            out.append(s["text"])
        io.open(p, "w", encoding="utf-8").write("\n".join(out))
        wrote.append(f)
        print("  ghi", f)

    # ---- ghi SKILL.md moi ----
    pb = ["\n%s\n" % HEADING,
          "Các mục dưới đây đã tách sang file riêng (nguyên văn, không rút gọn):\n"]
    for f in wrote:
        pb.append("- `%s` — %s" % (f, FILE_DESC.get(f, "chi tiết")))
    pb.append("")

    outbody = "\n".join(s["text"] for s in kept)
    idx = outbody.find("\n## References")
    block = "\n".join(pb)
    outbody = (outbody[:idx] + "\n" + block + outbody[idx:]) if idx != -1 \
        else (outbody.rstrip() + "\n" + block)

    shutil.copy2(src, os.path.join(skill_dir, "SKILL.md.bak-pre-split"))
    io.open(src, "w", encoding="utf-8").write(front + outbody)

    # ---- VERIFY: ca hai diff phai RONG ----
    newraw = io.open(src, encoding="utf-8").read()
    pool = newraw + "\n" + "\n".join(
        io.open(os.path.join(skill_dir, f.replace("/", os.sep)), encoding="utf-8").read()
        for f in wrote)

    old_h, now_h = headings(raw), set(headings(pool))
    missing_h = [t for t in old_h if t not in now_h]
    lost = sorted(content_lines(raw) - content_lines(pool))

    print()
    print("== VERIFY ==")
    print("  heading goc / con lai :", len(old_h), "/", len(old_h) - len(missing_h))
    print("  dong noi dung mat     :", len(lost))
    for t in missing_h[:10]:
        print("     ! heading:", t[:85])
    for l in lost[:10]:
        print("     ! dong   :", l[:85])

    print()
    print("== KICH THUOC ==")
    print("  SKILL.md truoc :", len(raw), "chars /", len(raw.encode("utf-8")), "bytes")
    print("  SKILL.md sau   :", len(newraw), "chars /", len(newraw.encode("utf-8")), "bytes")
    print("  (cap 100,000 la CHARS — khong so bang bytes voi tieng Viet)")

    if missing_h or lost:
        print()
        print("  ❌ CO MAT MAT — khoi phuc tu SKILL.md.bak-pre-split roi chay lai.")
        return 1
    print()
    print("  ✅ khong mat gi. Backup: SKILL.md.bak-pre-split")
    return 0


if __name__ == "__main__":
    sys.exit(main())
