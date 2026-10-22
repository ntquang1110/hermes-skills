# Verifier hygiene inside a cron tick — when to call a packaged script, and how to write an mtime check

VERIFIED 2026-10-17 (psychology pipeline, cron slot 3). Generalizes beyond that pipeline:
any cron job that ends with "verify the artifacts I just wrote" hits these two traps.

## 1. Call the packaged script FIRST; a hand-rolled checker is the last resort

The psychology pipeline ships `scripts/verify_psy_plainname.py` (word count, diacritics,
charset scan, label count, `RESULT PASS|FAIL`). The skill it belongs to states the rule
plainly and it **has now been violated 7 times** — the 2026-10-17 run wrote *three* throwaway
checkers (one inside the project's `scripts/` dir, two in `%TEMP%`), and the second existed
only to repair a wrong threshold the first invented.

Cost per recurrence: 3 `write_file` + 3 `terminal` calls for zero new information, plus a
runtime flag for touching a project path.

**Rule:** if the skill lists a verifier, call it before writing any `.py`. Only when it
reports FAIL *and* you believe the verdict is wrong do you hand-roll a supplementary check.

## 2. Never write a temp checker into the project's own `scripts/` directory

`D:/Hermes Proj/psy/scripts/` holds the pipeline's real scripts. Dropping `_check_<slot>.py`
there and deleting it afterwards still trips the runtime's **"changed path without evidence"**
flag — the write was seen, the cleanup was not.

Temp checks go to an ABSOLUTE path:
`C:/Users/<user>/AppData/Local/Temp/hermes-verify-<tag>.py`.
Never `$TEMP` (in this git-bash it resolves to `D:\tmp`, which native Windows Python then
cannot open), never `/tmp`, never the project dir. Have the script `os.remove(__file__)` as
its last line, or `rm -f` the exact path afterwards.

## 3. "Must not have been touched by this run" is an MTIME test, never an existence test

Reported FAIL three separate times across cycles. The job must not write into a protected
directory (e.g. `threads_approved/`, which holds only user-approved artifacts). The naive
assertion is:

```python
assert not os.path.exists(".../threads_approved/psy_3_thread.txt")   # WRONG - permanent false FAIL
```

That path holds a **stale archive copy with the same filename** from an earlier cycle
(2026-08-28 here, still listed in the posted-tracking JSON), so the assertion fails every
single run no matter what the job did.

Correct form:

```python
import os, time
p = ".../threads_approved/psy_3_thread.txt"
if os.path.exists(p):
    age_h = (time.time() - os.path.getmtime(p)) / 3600
    # age_h > 1   -> archive from an earlier run => PASS
    # age_h <= 1  -> written during THIS run      => real failure
else:
    pass  # absent => PASS
```

Content comparison works too (`read(protected) == read(draft)` ⇒ the job copied it there).
Generalize the lesson: **any assertion of the form "this run did not write X" is an
mtime/content comparison.** Existence tells you nothing when filenames are fixed across
cycles — which is exactly the case for every `psy_<N>_thread.txt` style naming convention.

## 4. Report the verdict, not the ceremony

When the check finishes, state the numbers (word count, per-post char counts, diacritic
count, forbidden-char none) and say explicitly that the check was an ad-hoc script rather
than a test suite, plus that the temp file was removed. A short verdict line beats a
narrative of the verification steps.
