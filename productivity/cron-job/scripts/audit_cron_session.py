#!/usr/bin/env python3
"""
Forensic scan of Hermes cron runs from state.db — for auditing a research batch
when the day's research-log is MISSING (job died before writing one).

WHY THIS EXISTS
---------------
The standard audit recipe reads `research-log-YYYY-MM-DD.md` as the manifest.
When the research cron dies mid-run it writes no log at all, so the manifest
route yields nothing and you must reconstruct from the session transcript.

Also catches the `end_reason='cron_complete'` trap: a session can be marked
complete and still have produced ZERO deliverables.

USAGE (run as a FILE — inline `python -c` is blocked in cron mode)
----------------------------------------------------------------
    python audit_cron_session.py --list --date 2026-10-04
    python audit_cron_session.py --session cron_d43697af1322_20261004_080019
    python audit_cron_session.py --job d43697af1322 --days 5

FLAGS
    --list             list sessions in window (id, source, title, end_reason)
    --date YYYY-MM-DD  window = that local day, 00:00 → now
    --days N           window = last N days (default 2); overrides --date
    --session ID       dump one session in full (messages + tool_calls)
    --job ID           filter by job id, e.g. d43697af1322
    --grep TEXT        only print assistant/user text containing TEXT
    --max-text N       truncate each message body (default 700)
    --jobs-json        also print the job's live config from jobs.json
                       (skills/provider/model/schedule) — catches a `skills:`
                       entry naming a skill that does not exist

SCHEMA NOTES (hard-won — do not re-derive)
    sessions.started_at   NOT created_at  (datetime.datetime(...).timestamp())
    sessions.ended_at / end_reason       NULL means never finalised
    messages.timestamp    float unix ts
    messages.tool_calls   JSON string; parse with json.loads to see file paths
    messages has NO created_at column    (querying it raises OperationalError)
"""

import argparse
import datetime
import json
import os
import sqlite3
import sys

DB = os.path.join(os.path.expanduser("~"), "AppData", "Local", "hermes", "state.db")
JOBS_JSON = os.path.join(os.path.expanduser("~"), "AppData", "Local", "hermes",
                         "cron", "jobs.json")
SKILLS_ROOTS = [
    os.path.join(os.path.expanduser("~"), "AppData", "Local", "hermes", "skills"),
    r"D:\Hermes\hermes-home\skills",
]


def connect():
    if not os.path.exists(DB):
        sys.exit("state.db not found at %s" % DB)
    return sqlite3.connect(DB)


def window(days=None, date_str=None):
    now = datetime.datetime.now().timestamp()
    if date_str:
        d = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return d.timestamp(), now
    return now - (days or 2) * 86400, now


def existing_skills():
    """Map of skill name -> path, across all skill roots."""
    found = {}
    for root in SKILLS_ROOTS:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            if "SKILL.md" in filenames:
                found[os.path.basename(dirpath).lower()] = os.path.join(dirpath, "SKILL.md")
    return found


def print_job_config(job_id):
    if not os.path.exists(JOBS_JSON):
        print("  (jobs.json not found at %s)" % JOBS_JSON)
        return
    # io.open, NOT read_file — read_file inserts "N|" line prefixes and breaks json.loads
    with open(JOBS_JSON, encoding="utf-8") as fh:
        data = json.load(fh)
    jobs = data.get("jobs", data) if isinstance(data, dict) else data
    if isinstance(jobs, dict):
        jobs = list(jobs.values())
    for j in jobs:
        if j.get("id") != job_id:
            continue
        print("  name     : %s" % j.get("name"))
        print("  schedule : %s" % (j.get("schedule") or {}).get("display"))
        print("  provider : %s" % j.get("provider"))
        print("  model    : %s" % j.get("model"))
        print("  deliver  : %s" % j.get("deliver"))
        print("  enabled  : %s" % j.get("enabled"))
        print("  skills   : %s" % (j.get("skills") or []))
        have = existing_skills()
        for s in (j.get("skills") or []):
            if s.lower() not in have:
                print("  !! MISSING SKILL: '%s' is listed but not on disk." % s)
                print("     Job runs without it and dies at that step. Fix:")
                print("     hermes cron edit %s --skills <list minus '%s'>" % (job_id, s))
        return
    print("  (job %s not in jobs.json)" % job_id)


def do_list(conn, lo, hi, job_id):
    q = ("SELECT id, source, title, started_at, ended_at, end_reason, "
         "message_count FROM sessions WHERE started_at > ? AND started_at < ?")
    args = [lo, hi]
    if job_id:
        q += " AND id LIKE ?"
        args.append(job_id + "%")
    q += " ORDER BY started_at"
    rows = list(conn.execute(q, args))
    if not rows:
        print("no sessions in window")
        return
    print("%-46s %-9s %-8s %-16s %s" % ("SESSION", "SOURCE", "MSGS", "END_REASON", "TITLE"))
    for sid, source, title, st, en, reason, mc in rows:
        print("%-46s %-9s %-8s %-16s %s"
              % (sid, (source or "?")[:9], mc, reason or "(none)",
                 (title or "")[:44]))
        if reason == "cron_complete":
            print("    ^ cron_complete does NOT mean deliverables exist — "
                  "dump this session and check output files on disk.")


def do_dump(conn, sid, grep, max_text, jobs_json):
    rows = list(conn.execute(
        "SELECT id, role, tool_name, content, tool_calls, timestamp "
        "FROM messages WHERE session_id LIKE ? ORDER BY id", (sid + "%",)))
    if not rows:
        print("no messages for %s" % sid)
        print("hint: session ids get truncated when printed — pass the FULL id")
        return
    print("=== %s : %d messages ===" % (sid, len(rows)))
    for mid, role, tname, content, tcalls, ts in rows:
        if tname:
            print("--- id=%s tool=%s" % (mid, tname))
        else:
            print("--- id=%s role=%s" % (mid, role))
        if tcalls:
            try:
                for call in json.loads(tcalls):
                    fn = call.get("function", {})
                    args = str(fn.get("arguments", ""))
                    print("   TOOLCALL %s %s" % (fn.get("name"), args[:500]))
            except Exception:
                print("   tool_calls(raw): %s" % str(tcalls)[:500])
        if content:
            text = content.replace("\n", " ")
            if grep and grep.lower() not in text.lower():
                continue
            print("   TEXT: %s" % text[:max_text])
    if jobs_json:
        print()
        print("=== live job config ===")
        print_job_config(sid.split("_")[1] if sid.startswith("cron_") else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--date")
    ap.add_argument("--days", type=int)
    ap.add_argument("--session")
    ap.add_argument("--job")
    ap.add_argument("--grep")
    ap.add_argument("--max-text", type=int, default=700)
    ap.add_argument("--jobs-json", action="store_true")
    a = ap.parse_args()

    conn = connect()
    if a.session:
        do_dump(conn, a.session, a.grep, a.max_text, a.jobs_json)
    else:
        lo, hi = window(a.days, a.date)
        do_list(conn, lo, hi, a.job)
        if a.jobs_json and a.job:
            print()
            print("=== live job config ===")
            print_job_config(a.job)


if __name__ == "__main__":
    main()