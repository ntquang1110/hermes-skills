"""Recursive Google Drive folder tree walker.

Usage:
    python walk_drive.py <ROOT_FOLDER_ID> <OUTPUT_TXT> [credential_json_path]

Builds an indented tree of DIR/file lines (name, id, mimeType) for all
trashed=false descendants of the root folder. Uses the same OAuth token as
the google-workspace skill (google_token.json).

Windows note: pass a NATIVE output path (e.g. r"D:\\Hermes Proj\\tree.txt").
The shell's MSYS paths (/d/...) are NOT understood by native Windows Python
and open() will silently resolve to a stray file or fail.
"""
import os, sys
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


def find_token():
    for cand in (
        os.path.join(os.path.expanduser("~"), "AppData", "Local", "hermes", "google_token.json"),
        os.path.join(os.path.expanduser("~"), ".hermes", "google_token.json"),
    ):
        if os.path.exists(cand):
            return cand
    raise SystemExit("google_token.json not found")


def children(svc, fid):
    items, page = [], None
    while True:
        res = svc.files().list(
            q=f"'{fid}' in parents and trashed=false",
            pageSize=1000, pageToken=page,
            fields="nextPageToken, files(id,name,mimeType,size,modifiedTime,parents)",
        ).execute()
        items.extend(res.get("files", []))
        page = res.get("nextPageToken")
        if not page:
            break
    return items


def walk(svc, fid, depth, out):
    for it in sorted(children(svc, fid), key=lambda x: x["name"]):
        isdir = it["mimeType"] == "application/vnd.google-apps.folder"
        kind = "DIR " if isdir else "file"
        out.append("  " * depth + f"{kind} {it['name']}\t{it['id']}\t{it['mimeType']}")
        if isdir:
            walk(svc, it["id"], depth + 1, out)


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    root, outpath = sys.argv[1], sys.argv[2]
    creds = Credentials.from_authorized_user_file(find_token())
    svc = build("drive", "v3", credentials=creds)
    out = [f"ROOT: {root}"]
    walk(svc, root, 0, out)
    with open(outpath, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print(f"Total lines: {len(out)}")


if __name__ == "__main__":
    main()