#!/usr/bin/env python3
"""Force-remove a directory that resists shutil.rmtree / rm -rf on Windows.

Primary use: uninstalling a git-sourced Hermes plugin, where Git marks
`.git/objects/pack/*.idx|*.pack` read-only and the stock rmtree aborts with
`PermissionError: [WinError 5] Access is denied`, leaving the folder half-deleted.

Usage:
    python force_remove_dir.py <path> [<path> ...]

Clears the read-only bit recursively, then rmtree with an on-error handler that
chmods the offending entry and retries, up to 3 attempts. Verifies absence and
exits 1 if anything remains.

Notes:
  * Windows paths from git-bash work: "D:/Hermes/hermes-home/plugins/<name>" or
    "/d/Hermes/..." -> pass the native form ("D:\\Hermes\\...") for reliability.
  * A junctioned data dir means the D: and C: paths are the SAME files; pass one.
  * py3.11 uses rmtree(onerror=...); py3.12+ renamed it to onexc=... . Both handled.
"""
import os
import shutil
import stat
import sys
import time

WRITE_BITS = stat.S_IWRITE | stat.S_IREAD


def _fix(func, path, exc_info):
    """Retry a failed unlink/rmdir after clearing the read-only bit."""
    try:
        os.chmod(path, WRITE_BITS)
        func(path)
    except Exception as e:  # noqa: BLE001 - report, don't crash the sweep
        print(f"  ! still failed: {path} :: {type(e).__name__}: {e}")


def force_remove(target):
    if not os.path.exists(target):
        print(f"skip (absent): {target}")
        return True

    # 1. clear read-only across the tree (dirs after files, done via a single walk)
    for root, dirs, files in os.walk(target):
        for name in files + dirs:
            try:
                os.chmod(os.path.join(root, name), WRITE_BITS)
            except Exception:  # noqa: BLE001
                pass

    # 2. rmtree with a version-appropriate error hook
    kwargs = {"onexc": lambda f, p, e: _fix(f, p, None)} if sys.version_info >= (3, 12) \
        else {"onerror": _fix}
    for attempt in range(3):
        try:
            shutil.rmtree(target, **kwargs)
            break
        except Exception as e:  # noqa: BLE001
            print(f"  attempt {attempt}: {type(e).__name__}: {e}")
            time.sleep(1)

    gone = not os.path.exists(target)
    print(("REMOVED " if gone else "STILL THERE ") + target)
    return gone


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    return 0 if all(force_remove(p) for p in argv[1:]) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
