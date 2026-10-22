#!/usr/bin/env python3
"""Probe: repo da san sang de publish private chua?

Chay: python check-repo-ready.py [duong-dan-repo]   (mac dinh: thu muc hien tai)

Kiem 4 thu ma mat thuong:
  1. File lon nhat dang track (bat >5MB de canh bao)
  2. Secret lo trong file track (token/key/private key)
  3. File INPUT bi .gitignore chan nhung script dang track co doc  -> clone ve build ra TRANG TRANG
  4. Co .gitattributes chua (repo Windows hay CRLF)

Luu y: dung subprocess list-args, KHONG dung shell=True (tren Windows shell=True la cmd.exe,
`git ls-files | grep` se tra RONG kem loi bi che -> ket luan sai la "khong thieu gi").
"""
import os, re, subprocess, sys

R = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
NAME_RE = re.compile(r"[\w./\-]+\.(?:json|txt|csv|tsv|md|html|js|py|yaml|yml)")
SECRET_RE = re.compile(
    r"(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|"
    r"AIza[0-9A-Za-z\-_]{30,}|xox[bp]-[A-Za-z0-9\-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY|"
    r"service_role|(?:password|passwd|secret|api[_-]?key|token)\s*[:=]\s*['\"][^'\"]{8,}['\"])",
    re.I,
)


def git(*a):
    r = subprocess.run(["git", *a], cwd=R, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.stdout


def main():
    if not os.path.isdir(os.path.join(R, ".git")):
        sys.exit("khong phai git repo: %s" % R)
    tracked = [x for x in git("ls-files").split("\n") if x.strip()]
    ignored = set(x.strip() for x in git("ls-files", "-o", "-i", "--exclude-standard").split("\n") if x.strip())
    print("repo: %s\nfile track: %d | file bi ignore: %d\ncommit cuoi: %s"
          % (R, len(tracked), len(ignored), git("log", "-1", "--pretty=%h %s").strip()[:100]))

    # 1. file lon
    big = []
    for f in tracked:
        p = os.path.join(R, f)
        if os.path.isfile(p):
            big.append((os.path.getsize(p), f))
    big.sort(reverse=True)
    print("\n== 10 file lon nhat dang track:")
    for s, f in big[:10]:
        flag = "  <-- CANH BAO >5MB" if s > 5 * 1024 * 1024 else ""
        print("  %8.1f KB  %s%s" % (s / 1024, f, flag))

    # 2. secret
    print("\n== quet secret:")
    hits = 0
    for f in tracked:
        p = os.path.join(R, f)
        if not os.path.isfile(p) or os.path.getsize(p) > 3 * 1024 * 1024:
            continue
        if os.path.splitext(f)[1].lower() in (".png", ".jpg", ".jpeg", ".webp", ".pdf", ".zip"):
            continue
        try:
            t = open(p, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        for m in SECRET_RE.finditer(t):
            line = t[:m.start()].count("\n") + 1
            print("  !! %s:%d  %s" % (f, line, m.group(0)[:60]))
            hits += 1
    print("  -> %d nghi van (0 la sach)" % hits)

    # 3. input bi ignore ma script dang doc
    print("\n== file script doc nhung bi .gitignore chan (clone ve se build thieu du lieu):")
    missing = {}
    for f in tracked:
        if os.path.splitext(f)[1].lower() not in (".py", ".js", ".ts", ".mjs", ".sh"):
            continue
        p = os.path.join(R, f)
        if not os.path.isfile(p):
            continue
        t = open(p, encoding="utf-8", errors="ignore").read()
        for name in set(NAME_RE.findall(t)):
            base = os.path.basename(name)
            if base == os.path.basename(f):
                continue
            for cand in (name, os.path.join(os.path.dirname(f), name), base):
                cand = cand.replace("\\", "/")
                for ig in ignored:
                    if ig.endswith(base) and (cand in ig or base in cand):
                        missing.setdefault(ig, set()).add(f)
    for ig, who in sorted(missing.items()):
        print("  !! %s  <- doc boi %s" % (ig, ", ".join(sorted(who)[:3])))
    print("  -> %d file (0 la repo tu dung duoc)"
          % len(missing) if missing else "  -> 0 file (repo tu dung duoc)")

    # 4. gitattributes
    print("\n== .gitattributes: %s" % ("co" if os.path.exists(os.path.join(R, ".gitattributes"))
                                       else "THIEU (them '* text=auto')"))
    print("\nBuoc cuoi bat buoc: git clone <repo> ../_clonetest && cd ../_clonetest && chay lai script build.")


if __name__ == "__main__":
    main()
