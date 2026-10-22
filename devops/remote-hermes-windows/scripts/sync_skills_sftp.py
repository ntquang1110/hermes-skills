#!/usr/bin/env python3
"""Đồng bộ skills từ máy này sang máy Windows khác qua SFTP.

Dùng khi setup Hermes cho máy đích và cần copy cả bộ skill.

    python sync_skills_sftp.py --host lqremote.example.com --user NLQuan --pass '...'

Đặc điểm:
- Bỏ qua `.archive/` (skill đã bỏ, không cần mang sang).
- So kích thước file trước khi put -> chạy lại lần 2 rất nhanh (idempotent).
- Tạo thư mục lồng nhau (references/, templates/, scripts/, assets/).
- In tiến độ mỗi 60 skill để không bị tưởng là treo.

Đã chạy thật: 341 skill / 1466 file, ~2 phút, 0 lỗi.
"""

from __future__ import annotations

import argparse
import os
import posixpath
import sys
import time

try:
    import paramiko
except ImportError:
    sys.exit("pip install paramiko")


def remote_base(user: str) -> str:
    # Đường dẫn data Hermes của user, suy từ tên user — KHÔNG hardcode user cũ.
    return rf"C:\Users\{user}\AppData\Local\hermes\skills"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", required=True)
    ap.add_argument("--user", required=True)
    ap.add_argument("--pass", dest="password", required=True)
    ap.add_argument("--local", default=None, help="thư mục skills local")
    ap.add_argument("--port", type=int, default=22)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    local_base = args.local or os.path.join(
        os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "hermes", "skills"
    )
    if not os.path.isdir(local_base):
        sys.exit(f"không thấy thư mục skills: {local_base}")

    remote = remote_base(args.user)

    skills: list[str] = []
    for root, _dirs, files in os.walk(local_base):
        if "SKILL.md" in files:
            rel = os.path.relpath(root, local_base).replace("\\", "/")
            if not rel.startswith(".archive"):
                skills.append(rel)
    print(f"local: {len(skills)} skill")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        args.host,
        port=args.port,
        username=args.user,
        password=args.password,
        timeout=25,
        banner_timeout=40,
        auth_timeout=40,
        allow_agent=False,
        look_for_keys=False,
    )
    sftp = client.open_sftp()

    def ensure(rel_dir: str) -> None:
        cur = remote
        for part in rel_dir.replace("\\", "/").split("/"):
            if not part:
                continue
            cur = cur + "\\" + part
            try:
                sftp.stat(cur)
            except IOError:
                try:
                    sftp.mkdir(cur)
                except Exception:
                    pass  # đã có do race, bỏ qua

    uploaded = skipped = errors = 0
    t0 = time.time()
    for i, skill in enumerate(skills, 1):
        local_dir = os.path.join(local_base, skill.replace("/", os.sep))
        ensure(skill)
        for root, _dirs, files in os.walk(local_dir):
            sub = os.path.relpath(root, local_dir).replace("\\", "/")
            target = skill if sub == "." else f"{skill}/{sub}"
            ensure(target)
            for fname in files:
                src = os.path.join(root, fname)
                dst = remote + "\\" + target.replace("/", "\\") + "\\" + fname
                try:
                    size = os.path.getsize(src)
                    try:
                        if sftp.stat(dst).st_size == size:
                            skipped += 1
                            continue
                    except IOError:
                        pass
                    if not args.dry_run:
                        sftp.put(src, dst)
                    uploaded += 1
                except Exception as exc:  # noqa: BLE001
                    errors += 1
                    if errors <= 5:
                        print(f"  LỖI {target}/{fname}: {exc}", file=sys.stderr)
        if i % 60 == 0:
            print(f"  ... {i}/{len(skills)} | up={uploaded} skip={skipped} err={errors} ({time.time()-t0:.0f}s)")

    print(f"XONG: upload={uploaded} skip={skipped} err={errors} trong {time.time()-t0:.0f}s")
    sftp.close()
    client.close()

    # Nghiệm thu: đếm lại SKILL.md trên máy đích, so với số local.
    print(f"KIỂM LẠI  : đếm trên máy đích phải ra >= {len(skills)}")
    print(r'           (Get-ChildItem "<remote>" -Recurse -Filter SKILL.md).Count')
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
