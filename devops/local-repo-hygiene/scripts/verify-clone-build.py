#!/usr/bin/env python3
"""Chung minh repo la "hoan chinh": clone sach -> build lai -> hash trung -> repo goc khong nhuc nhich.

Dung:
  python verify-clone-build.py --repo "D:/Proj/x" --clone "D:/Proj/_clonetest" \
      --cmd "python visual/build-a.py" --cmd "python visual/build-b.py" \
      --artifact visual/a.html --artifact visual/b.html [--twice]

Vi sao can script nay thay vi so mat:
  - So in ra (KPI/log) co the GIONG nhau trong khi script hardcode duong dan tuyet doi
    van dang ghi nguoc ve repo goc. Chi phep "repo goc con sach" moi bat duoc loi do.
  - Hash phai trung; lech = con file input bi .gitignore chan hoac build khong tat dinh.
Tra ve exit 0 khi TAT CA dat, 1 khi co loi.
"""
import argparse, hashlib, io, os, shutil, subprocess, sys


def sh(cmd, cwd):
    r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    out = (r.stdout + r.stderr).strip().splitlines()
    return r.returncode, (out[-1][:110] if out else "")


def h(p):
    return hashlib.sha256(io.open(p, "rb").read()).hexdigest()[:12] if os.path.exists(p) else "MISSING"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--clone", required=True)
    ap.add_argument("--cmd", action="append", default=[], required=True)
    ap.add_argument("--artifact", action="append", default=[], required=True)
    ap.add_argument("--twice", action="store_true", help="chay lai lan 2 de kiem tinh tat dinh")
    a = ap.parse_args()

    repo, clone = os.path.abspath(a.repo), os.path.abspath(a.clone)
    bad = []

    goc = {f: h(os.path.join(repo, f)) for f in a.artifact}
    print("[1] hash ban goc:", goc)

    shutil.rmtree(clone, ignore_errors=True)
    rc, o = sh('git clone -q "%s" "%s"' % (repo, clone), os.path.dirname(clone) or ".")
    print("[2] clone:", "OK" if rc == 0 else "LOI %s" % o)
    if rc != 0:
        sys.exit(1)

    for c in a.cmd:
        rc, o = sh(c, clone)
        print("    %-45s rc=%s | %s" % (c, rc, o))
        if rc != 0:
            bad.append("lenh loi: %s" % c)

    ban = {f: h(os.path.join(clone, f)) for f in a.artifact}
    for f in a.artifact:
        ok = ban[f] == goc[f] and ban[f] != "MISSING"
        print("[3] %-40s clone=%s goc=%s %s" % (f, ban[f], goc[f], "TRUNG" if ok else "LECH <-- LOI"))
        if not ok:
            bad.append("hash lech: %s" % f)

    if a.twice:
        for c in a.cmd:
            sh(c, clone)
        lai = {f: h(os.path.join(clone, f)) for f in a.artifact}
        for f in a.artifact:
            if lai[f] != ban[f]:
                bad.append("khong tat dinh: %s" % f)
        print("[4] kiem tat dinh (chay lai lan 2):", "OK" if not any("tat dinh" in b for b in bad) else "LECH")

    rc, o = sh("git status --short", repo)
    print("[5] repo goc sau khi chay script o ban clone:", "SACH (dat)" if not o.strip() else "DIRTY <-- LOI")
    if o.strip():
        bad.append("repo goc bi sua khi chay script tu clone (nghi duong dan tuyet doi):\n%s" % o)
        rc2, hits = sh('grep -rn "D:/\\|C:/Users\\|/home/" --include=*.py .', repo)
        if hits.strip():
            print("    nghi pham:\n%s" % hits.strip()[:600])

    print("\n=== KET LUAN:", "DAT — repo tu dung duoc sau khi clone" if not bad else "KHONG DAT")
    for b in bad:
        print("   -", b)
    shutil.rmtree(clone, ignore_errors=True)
    sys.exit(0 if not bad else 1)


if __name__ == "__main__":
    main()
