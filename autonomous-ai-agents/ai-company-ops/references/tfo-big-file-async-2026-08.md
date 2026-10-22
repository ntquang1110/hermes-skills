# TFO — upload file lớn: chunk + async job (2026-08, tách khỏi SKILL.md 03/10)

Chi tiết 2 lỗi nối tiếp khi Quang upload meeting dài. SKILL.md chỉ giữ 3 dòng trỏ tới đây.

## ⚠️ Cloudflare tunnel giới hạn body ~100MB (24/08)
Triệu chứng: upload >100MB → browser tưởng treo (không lỗi, không response). File **không** tới server (0 file mới trong `tfo_data/uploads/`) — CF tunnel miễn phí cắt request giữa chừng, code chặn tiếp >60MB (`transcribe()` dòng `if size_mb > 60 → 413`).

Fix (`bde2915`) — chunk upload:
- Frontend `uploadFileChunked()`: file >55MB → `file.slice()` 10MB/chunk, gửi **TUẦN TỰ** (không bắn song song — reassemble đọc theo index, lộn thứ tự hỏng), retry 3 lần/chunk (CÙNG chunk, không skip), cập nhật % tổng.
- Backend `transcribe_chunk()`: ghi chunk theo index (`upload_id.p<index>`), đủ N chunk → reassemble đúng thứ tự → transcribe. **Guard path traversal: `upload_id` phải hex-only.** Dọn chunk sau merge.
- **SÓT SIZE-LIMIT CŨ:** khi thêm endpoint mới, `grep -n "size_mb >" app/main.py` — đừng copy cụm `if size_mb > 60 → 413` từ đường upload đơn sang chunk. Chunk đã qua CF (10MB/request) nên 60MB hết ý nghĩa. Giới hạn xử lý theo **DURATION**, không theo size nguồn.
- Verify patch: `ast.parse(open('app/main.py').read())` (dễ dính IndentationError khi chèn nhầm vào hàm khác).

## 🧵 Phải transcribe ASYNC JOB (5657e90 — 176MB/2h05 vẫn "chưa xử lý được")
Chunk cuối chạy `_transcribe_chunked` **đồng bộ trong request** → file 2h05 mất hàng chục phút → client XHR timeout 120s cắt request → transcribe chết, meeting không lưu (chỉ frontend lưu sau khi nhận transcript).

**Triệu chứng nhận diện:** file reassemble xong trong `uploads/` (`.m4a` >60MB) nhưng **KHÔNG** có `.opus` nén + **KHÔNG** có meeting mới = transcribe chưa từng chạy hết. Không phải upload lỗi.

Fix trong `app/main.py`:
- `_JOBS` registry + `_run_transcribe_job(job_id, final_path)` background thread (`_th.Thread(daemon=True)`): silent-check → `_transcribe_chunked` nếu duration>3300 / `_groq_transcribe` nếu ngắn → ghi `_JOBS[job_id]`.
- Chunk cuối → `return {"status":"processing","job_id":...,"file_id":...}` **NGAY**, spawn thread.
- `GET /api/transcribe/job?job_id=&token=` → poll `done`/`error`/`processing`. Validate `job_id` hex-only.
- Frontend: `res.status==="processing"` → `pollJob()` mỗi 500ms, cap `pollPhase>=600` (>5 phút) → reject.

**Pitfall `_JOBS` in-memory mất khi restart** → job đang transcribe chết im. Muốn restart khi còn file đang kẹt: spawn process **DETACHED**, đừng chạm PID xử lý.
**`_JOBS` khỏi dữ liệu trên đĩa** — không phải thiếu cài đặt.

## Chạy processing script độc lập (không qua HTTP) cho file dài
```python
flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW
p = subprocess.Popen([py, script], cwd=cwd, stdout=logf, stderr=logf, stdin=subprocess.DEVNULL,
                     creationflags=flags, close_fds=True)
```
Script phải **TỰ nạp keys** từ `~/AppData/Local/hermes/.env` (tiến trình tách không kế thừa bashrc exports). Xác nhận align: `tasklist /FI "PID eq <pid>"`.

## Transcript ngắn bất thường (25/08) — KHÔNG bịa, ghi chú rõ
File 176MB m4a duration 7485s → `_transcribe_chunked` chỉ 2550 từ (mất nhiều nội dung, còn lẫn CTA "đăng ký kênh"). Báo user: "transcript tự động ngắn, cần cải thiện chunk codec nếu cần chính xác" — vẫn summarize + lưu meeting. Giữ `file_kept` local để retry.