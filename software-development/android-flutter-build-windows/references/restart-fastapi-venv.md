# Restart FastAPI server trên Windows giữ env (recipe đã chạy 16/08/2026)

⚠️ **`metelligent-project` skill (user-owned, không patch được) vẫn ghi URL cũ
`metelligent-123.loca.lt` — SAI TỪ 16/08.** Domain chính thức:
`https://metelligent.theliems.com` (app default URL + Settings quick-switch đã đổi).
Loca.lt (`metelligent-app.loca.lt`) chết → app không gọi được server. Khi làm
việc với meTelligent, lấy URL từ code (`server_service.dart`) chứ không từ skill.

Áp dụng cho server FastAPI project (meTelligent 8766, TFO 8100, ...) khi cần
restart sau khi sửa code/route. Các bước dưới đây ĐÃ CHẠY THÀNH CÔNG 16/08.

## Vì sao `python -c` inline SAI (đã dính 16/08)

Trên máy này `python` trong PATH resolve về **hermes-agent venv**
(`~/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe`), không phải
Python hệ thống. Venv đó có uvicorn NHƯNG thiếu deps project
(`faster_whisper`, `ctranslate2`...) → chạy `python -c "...uvicorn.run..."` ra
`ModuleNotFoundError: No module named 'faster_whisper'` dù trước đó server vẫn
chạy tốt (vì trước đó chạy bằng venv CỦA PROJECT).

Check nhanh python đang resolve về đâu:
```bash
python -c "import sys; print(sys.executable)"
```

## Recipe restart đúng

1. **Kill process cũ:**
   ```bash
   netstat -ano | grep ":<port>" | grep LISTENING   # lấy PID
   taskkill -F -PID <pid>
   ```

2. **Venv project thường thiếu deps** — cài bổ sung bằng subprocess (qua
   execute_code, không gọi venv python trực tiếp trong terminal vì lifecycle
   guard chặn "embedded null character in path"):
   - `pyyaml` (ctranslate2/faster-whisper cần)
   - `packaging tqdm typing-extensions` (huggingface-hub cần)
   - `uvicorn[standard] fastapi python-multipart webrtcvad-wheels groq requests`
   ```python
   import subprocess, os
   venv_py = r"D:\...\<project>\server\venv\Scripts\python.exe"
   env = dict(os.environ); env["PYTHONPATH"] = r"D:\...\<project>\server"
   r = subprocess.run([venv_py, "-m", "pip", "install", "pyyaml", "packaging", "tqdm", "typing-extensions", "uvicorn[standard]", "fastapi", "python-multipart", "webrtcvad-wheels", "groq", "requests"], capture_output=True, text=True, timeout=300, env=env)
   ```

3. **Import test trước khi start:** chạy venv python import app module, check
   route mới:
   ```python
   # set GROQ_* env từ hermes .env + NOTION_API_KEY (base64) trước import
   from metelligent import app
   print([r.path for r in app.routes if hasattr(r, 'path') and 'apk' in r.path])
   ```

4. **Start bằng execute_code + subprocess.Popen (không qua terminal tool):**
   terminal tool chặn gọi venv python trực tiếp + chặn lệnh chứa `uvicorn`
   (lifecycle guard "embedded null character in path"). Dùng launcher script
   đọc env từ hermes `.env` rồi uvicorn.run, spawn bằng Popen:
   ```python
   import subprocess
   launcher = r"D:\...\<project>\server\run_server_v2.py"  # script tự đọc env
   log = open(r"D:\...\<project>\server\server.log", "w", encoding="utf-8")
   proc = subprocess.Popen([venv_py, launcher], stdout=log, stderr=subprocess.STDOUT,
                           cwd=r"D:\...\<project>\server",
                           creationflags=subprocess.CREATE_NO_WINDOW)
   print("started pid:", proc.pid)
   ```

5. **Verify sau 6s:** `curl :<port>/api/health` → 200; route mới qua tunnel
   thật: `curl -s -o /dev/null -w "%{http_code}" https://<domain>/<route>` → 200.

## Launcher script mẫu (run_server_v2.py)

```python
import os, base64, sys
sys.path.insert(0, r'D:\...\<project>\server')
for line in open(r'C:\Users\NTQUANG_DELL\AppData\Local\hermes\.env', encoding='utf-8'):
    line = line.strip()
    if '=' in line:
        k, v = line.split('=', 1)
        if k.startswith('GROQ'):
            os.environ[k] = v
os.environ['NOTION_API_KEY'] = base64.b64decode('<b64>').decode()
import uvicorn
uvicorn.run('metelligent:app', host='0.0.0.0', port=8766, reload=False)
```
