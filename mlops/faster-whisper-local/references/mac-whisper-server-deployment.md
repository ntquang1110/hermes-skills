# Mac Whisper HTTP Server — full deployment record (2026-09-22)

Deployed on `192.168.1.3` (Mac Mini M1, macOS, user `tquang`, password `<PASSWORD>`).
Server URL: `http://192.168.1.3:9000` (OpenAI-compatible endpoint).

## Server script (`~/whisper/whisper_server.py`)

FastAPI + uvicorn, loads `Systran/faster-whisper-large-v3` once at startup.

Endpoints:
- `POST /v1/audio/transcriptions` — multipart `file` + `language`, returns `{"text":"...","duration":N,"language":"..."}`
- `GET /v1/models` — OpenAI-compatible model list
- `GET /health` — `{"status":"ok","model":"large-v3","pid":N}`

Start: `~/whisper-venv/bin/python ~/whisper/whisper_server.py --port 9000 --model large-v3`
Needs `fastapi uvicorn python-multipart` in `~/whisper-venv`.

## launchd (`~/Library/LaunchAgents/com.user.whisper-server.plist`)

```xml
<key>Label</key><string>com.user.whisper-server</string>
<key>ProgramArguments</key>
<array>
    <string>/Users/tquang/whisper-venv/bin/python</string>
    <string>/Users/tquang/whisper/whisper_server.py</string>
    <string>--port</string><string>9000</string>
    <string>--model</string><string>large-v3</string>
</array>
<key>RunAtLoad</key><true/>
<key>KeepAlive</key><true/>
<key>StandardOutPath</key><string>/Users/tquang/whisper/server.log</string>
<key>StandardErrorPath</key><string>/Users/tquang/whisper/server.err</string>
<key>EnvironmentVariables</key>
<dict><key>PATH</key><string>/Users/tquang/whisper-venv/bin:/usr/local/bin:/usr/bin:/bin</string></dict>
```

Load: `launchctl load ~/Library/LaunchAgents/com.user.whisper-server.plist`
Check: `launchctl list | grep whisper-server`

## Hermes fallback wiring

Two entry points, both ultimately curl the Mac server:

### A. Command provider (`stt.providers.mac-whisper`)

Added to `config.yaml` under `stt.providers`:
```yaml
stt:
  providers:
    mac-whisper:
      type: command
      command: "python \"C:/Users/NTQUANG_DELL/AppData/Local/hermes/scripts/stt_mac_wrapper.py\" {input_path} {output_path} {language}"
      timeout: 120
      language: vi
```
Wrapper: `scripts/stt_mac_wrapper.py` — multipart POST, saves transcript to `{output_path}`.

### B. Gateway fallback (`HERMES_LOCAL_STT_COMMAND`)

Added to `~/.hermes/.env`:
```
HERMES_LOCAL_STT_COMMAND=python "C:/Users/NTQUANG_DELL/AppData/Local/hermes/scripts/stt_mac_local.py" {input_path} --output_format txt --output_dir {output_dir} --language {language}
HERMES_LOCAL_STT_LANGUAGE=vi
```
Wrapper: `scripts/stt_mac_local.py` — parses Hermes template grammar, POSTs to Mac, writes `{output_dir}/{stem}.txt`.

### Patches to `tools/transcription_tools.py`

1. `_get_local_command_template()` — add fallback to `hermes_cli.config.get_env_value()` because `os.getenv` alone misses `~/.hermes/.env` (Hermes loads .env via config module, not process env).

2. `transcribe_audio_local_fallback()` — try `local_command` **before** `faster-whisper` on Windows where `venv/Lib/numpy` is cpython-3.11 built but runtime is 3.14 (numpy._core._multiarray_umath ModuleNotFoundError).

## Watchdog cron

`scripts/watchdog_mac_whisper.py` — GET `/health`, silent when `status==ok`.
Cron: `every 30m`, `no_agent=true`.

## Cleanup

Remove small/tiny cached models: `rm -rf ~/.cache/huggingface/hub/models--Systran--faster-whisper-{small,tiny}`
