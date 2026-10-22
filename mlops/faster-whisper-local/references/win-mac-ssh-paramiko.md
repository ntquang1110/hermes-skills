# Driving SSH to a Mac from Windows (git-bash) with paramiko

git-bash (MSYS) lacks `sshpass` and `expect`, so password-auth SSH can't be scripted in pure shell.
The working path: install `paramiko` in the LOCAL Windows Python and drive it from a script.

## Setup (Windows side)
```
python -m pip install paramiko
```
NOTE: on this host `python` = 3.11, `pip` = python3.14, system `python3` = missing — use
`python -m pip` (not bare `pip`, not `python3`) so the install lands in the interpreter that runs the call.
Earlier attempt `pip install paramiko` went to the wrong client and `import paramiko` still failed.
Verify with `python -c "import paramiko; print(paramiko.__version__)"`.

## Password-auth connect (works even when SSH key is rejected)
```python
import paramiko
c = paramiko.SSHClient(); c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(host, username=user, password=pw, timeout=15)

# run a script: feed a heredoc via stdin so a long multi-line cmd stays one exec
stdin, stdout, stderr = c.exec_command("bash -s", timeout=900)
stdin.write(script); stdin.channel.shutdown_write()
data = stdout.read().decode(errors="replace")
err  = stderr.read().decode(errors="replace").strip()
c.close()
```
SSH key `Permission denied (publickey,password,...)` is expected when the Mac is password-/kbd-interactive
only — paramiko password auth is the fallback that works.

## Transfer a file (sftp)
```python
sftp = c.open_sftp()
try: sftp.stat("whisper")           # avoid mkdir when it exists
except: sftp.mkdir("whisper")
sftp.put(r"D:\path\localfile.py", "whisper/run_whisper.py")
sftp.close()
```
Define the `_has` helper BEFORE using it — Python resolves the call at runtime (NameError otherwise).

## Pitfall: reading stdout
`stdout.readline()` returns bytes when you init `out = b""`; concatenating str lines crashes
(`TypeError: can't concat str to bytes`). Simplest: collect `stdout.read()` once after the exec
finishes. If you must stream line-by-line, stay all-bytes or all-str consistently.

## Long remote jobs
Bump exec timeout to 900-1500 s for model downloads. Make the remote script idempotent and have it
echo a DONE marker; retry (loop) until the marker appears. Don't assume first attempt finished if
your local reader crashed mid-way — the remote bash keeps running, so re-verify via the marker line.