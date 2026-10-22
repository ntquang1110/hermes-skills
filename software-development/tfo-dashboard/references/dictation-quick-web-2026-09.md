# Dictation quick web — Nói nhanh (15/09/2026)

Pivot all-web: meTelligent Android bỏ, dictation gộp vào TFO web. Không build pipeline mới — TFO đã đủ `ghi âm → /api/transcribe → /api/summarize → task`.

## Nút Nói nhanh (dashDictateBtn)

- **Vị trí:** action bar đầu Dashboard, cạnh Ghi âm / Tải lên / Nói chuyện trực tiếp. Id `dashDictateBtn` + `dashDictateLabel`, style `background:rgba(91,141,239,0.12)`.
- **Hàm:** `startQuickDictation()` trong `app/static/index.html` (~50 dòng, trước `setDefaultMeetingTime()`).
- **Luồng:**
  ```
  click → getUserMedia({audio:true}) → MediaRecorder(webm) → chunks[]
  click lần 2 → stop() → Blob(webm) → FormData(file=dictation.webm, token)
    → POST /api/transcribe → {transcript}
    → POST /api/summarize {transcript, token} → {summary}
    → resultBox.innerHTML (📝 Dictation: 400ch transcript + 600ch summary) + loadTasks()
  ```
- **Trạng thái nút:** `recording` class khi đang ghi, label `🔴 Đang ghi...` → `Đang xử lý...` → `Nói nhanh`.
- **Giữ trong cùng view:** dictation và record đều ghi vào `#resultBox` (không tạo card mới), để view vấn đề nhanh nhất không bị phân tán.

## Quyết định liên quan

- 9 task meTelligent paused (17-25) → completed 15/09, close_note "Pivot web, bỏ Android" (store/tasks.json, gitignored — không commit).
- Feature 9 meTelligent: 40% in_progress → 100% done (store/features.json, commit 92f84df).
- Endpoint meTelligent SQLite `/api/metelligent/meetings` giữ nguyên cho tương thích, card dashboard đã chôn.
- `metelligent-project` skill giữ làm tài liệu lịch sử server 8766/tunnel/APK — không dùng cho việc mới.

## Khi nào dùng lại

- Cần dictation 5-30s không cần lưu meeting dài → dùng Nói nhanh.
- Cần họp dài có lưu + timeline → dùng Ghi âm (MediaRecorder chunk 10s + /api/record/*).
- Cần hỏi tri thức bằng giọng → dùng Nói chuyện trực tiếp (WS /ws/stream + RAG/TTS).
