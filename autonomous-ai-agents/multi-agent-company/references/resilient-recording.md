# Resilient audio recording — chunk + watchdog pattern

User rule (Quang, TFO MVP): a recording must NEVER be lost. Normal flow: press record → press End → saved.
But if the user does NOT press End and the network drops / session dies mid-recording → the audio must still be saved.

## Why not the naive approach
Naive: collect all MediaRecorder chunks in memory, upload once on stop. If network dies mid-recording, everything since the last successful upload is lost — the whole point (recording survives network drop) fails.

## Client pattern (app/static/index.html)
```js
mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
mediaRecorder.start(10000);  // timeslice → dataavailable fires every 10s
mediaRecorder.ondataavailable = async (e) => {
  if (e.data && e.data.size > 0 && sessionId) {
    const fd = new FormData();
    fd.append('session_id', sessionId);
    fd.append('audio', e.data, 'chunk.webm');
    await fetch('/api/record/chunk', { method: 'POST', body: fd });
  }
};
```
Each 10s chunk is pushed to the server immediately — so the server always holds everything recorded up to the last successful chunk, even if the tab closes or network drops.

On End: stop recorder → send the final chunk (if any) → `POST /api/record/end` with session_id → server transcribes.

## Server pattern (app/main.py)
```python
SESSIONS = {}  # sid -> {"file": Path, "last_seen": float, "parts": int}

@app.post("/api/record/start")
def record_start():
    sid = uuid.uuid4().hex[:12]
    rec_file = REC_DIR / f"{sid}.webm"
    SESSIONS[sid] = {"file": rec_file, "last_seen": _time.time(), "parts": 0}
    return {"session_id": sid}

@app.post("/api/record/chunk")
async def record_chunk(session_id: str = Form(...), audio: UploadFile = File(...)):
    sess = SESSIONS.get(session_id)
    data = await audio.read()
    with open(sess["file"], "ab") as f:  # append, not overwrite
        f.write(data)
    sess["parts"] += 1
    sess["last_seen"] = _time.time()
    return {"ok": True, "parts": sess["parts"]}

@app.post("/api/record/end")
def record_end(session_id: str = Form(...)):
    sess = SESSIONS.pop(session_id, None)
    return _finalize_recording(sess)

def _finalize_recording(sess):
    transcript = _transcribe_chunked(sess["file"]) if size > 15MB else _groq_transcribe(sess["file"])
    return {"session_id": f.stem, "parts": sess["parts"], "transcript": transcript}
```

## Watchdog — the safety net
Session that goes silent (no chunk, no end) >30s is treated as dead → auto-finalize + save transcript file:
```python
def _recording_watchdog():
    while True:
        _time.sleep(10)
        now = _time.time()
        for sid in list(SESSIONS.keys()):
            if now - SESSIONS[sid]["last_seen"] > 30:
                sess = SESSIONS.pop(sid)
                result = _finalize_recording(sess)
                (REC_DIR / f"{sid}.transcript.txt").write_text(result.get("transcript",""), encoding="utf-8")
                print(f"🛟 Auto-saved session {sid} ({sess['parts']} parts) do timeout")
threading.Thread(target=_recording_watchdog, daemon=True).start()
```

## Verification (how it was tested)
1. start session → send 3 chunks → end → assert file has all 3 parts concatenated.
2. start session → send 1 chunk → DO NOT end → wait ~35s → assert watchdog wrote `{sid}.webm` AND `{sid}.transcript.txt`.
Recordings live in `tfo_data/recordings/`.

## Notes
- MediaRecorder emits the FULL accumulated stream per timeslice in some browsers — appending raw blobs can duplicate. Real-world fix if transcription shows overlap: use `MediaRecorder` with `audio/webm` timeslice + send each blob as separate segment and de-dup server-side, or send only deltas. For MVP (tested OK) the append pattern is sufficient; flag for hardening when >5-10 min recordings are exercised.
- `.webm` chunks appended to a single file transcribe fine with Groq in practice; if a specific browser's blob stream is not appendable, fall back to chunk-per-file naming `{sid}_p{n}.webm` and transcribe each then join transcripts.
