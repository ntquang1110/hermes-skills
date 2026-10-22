# Face Login — MediaPipe (ĐÃ BUILD 03/08, thay passcode)

User chốt: **"Ok em thử triển khai phương án MediaPipe đi"** — bỏ Faceplugin SDK (Torch 2GB, license mờ), dùng MediaPipe FaceLandmarker (Google, nhẹ, CPU-only, on-premise 100%).

## MediaPipe 1.0 API — PITFALL QUAN TRỌNG

- `mediapipe` 1.0.0 **XÓA `mp.solutions`** → `AttributeError: module 'mediapipe' has no attribute 'solutions'`
- Phải dùng **Tasks API**: `from mediapipe.tasks import python as mp_python; from mediapipe.tasks.python import vision`
- Model: `face_landmarker.task` (float16, ~3.7MB) — tự download về `app/face_landmarker.task`:
  `https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task`
- Khởi tạo:
```python
options = vision.FaceLandmarkerOptions(
    base_options=mp_python.BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=vision.RunningMode.IMAGE, num_faces=1,
    min_face_detection_confidence=0.5, min_face_presence_confidence=0.5)
landmarker = vision.FaceLandmarker.create_from_options(options)
result = landmarker.detect(mp_img)  # mp.Image(image_format=SRGB, data=rgb_numpy)
```

## Module `app/face_auth.py`

- `extract_embedding(image_bytes)` → 478 landmarks `(x,y,z)` → **chuẩn hóa: trừ centroid + chia norm** (bất biến khoảng cách camera) → list float 1434 dims. Trả `None` nếu không thấy mặt.
- `compare_embeddings(e1, e2)` → cosine similarity 0-1
- `is_match(sim, threshold=0.93)` — landmark-based, cùng người thường ~0.95+; ngưỡng 0.93 cân bằng false positive/false negative
- Test nhanh: `.venv/Scripts/python.exe -c "from app.face_auth import _ensure_model; ..."` → tải model + khởi tạo OK

## Endpoints (app/main.py)

| Endpoint | Auth | Chức năng |
|---|---|---|
| `POST /api/face/enroll` | **token** (đã login) | upload ảnh → extract embedding → lưu `users/<email>/face_embedding.json` |
| `POST /api/face/verify` | **email HOẶC token** | upload ảnh → so sánh → nếu match **tạo session token mới luôn** (trả `{matched, similarity, token, email}`) |
| `GET /api/face/status` | token | `{enrolled: bool}` — đã enroll chưa |

Lưu ý verify: user đang ở màn login nên CHƯA có token — frontend gửi `email` field; token param chỉ dùng khi đã login. Match → tự tạo session giống `/api/login` (ghi `tfo_data/sessions.json`).

## Frontend (app/static/index.html)

- Login overlay có **2 tab**: `😀 Khuôn mặt` (mặc định, có `faceEmail` input + `<video id="faceVideo">` webcam + nút "Xác minh") / `🔑 Passcode` (backup — KHÔNG xóa, user muốn face primary + passcode fallback)
- `faceTab('face'|'pass')` — bật/tắt camera (`getUserMedia({video:true, audio:false})`)
- `faceVerify()` — canvas capture frame → blob jpeg → `POST /api/face/verify` → match: lưu `d.token` vào localStorage + `initApp()`; fail: hiện % tương đồng + thử lại
- Đã test: enroll status `{'enrolled': False}` → verify báo "Chưa enroll" đúng

## Trạng thái

- ✅ MediaPipe cài (`.venv/Scripts/python.exe install_face.py` — mediapipe, opencv-python-headless, numpy)
- ✅ Module face_auth + 3 endpoints + UI 2 tab — build xong, push git (f1702d2)
- ⏳ **CHƯA enroll khuôn mặt user** — cần 1 ảnh selfie của Quang (ánh sáng tốt) để lưu embedding; passcode vẫn hoạt động cho tới khi enroll xong
- Backup plan: passcode giữ nguyên — mất face vẫn vào được

## PITFALL: liveness check (chớp mắt) làm USER THẤT BẠI

Spike của OpenClaw thêm liveness "nhìn thẳng + chớp mắt" — user chớp mắt nhiều lần vẫn không qua: *"Anh k chụp được ảnh toàn yêu cầu chớp mắt mà anh chớp r k được"*.

**Bài học:** MVP cho user là chính mình — KHÔNG thêm liveness khắt khe. Capture ảnh tĩnh + verify embedding là đủ cho giai đoạn stealth/pilot. Nếu sau này cần chống fake (ảnh in/photo replay), thêm liveness NHẸ (yêu cầu quay đầu nhẹ hoặc 2 frame cách nhau 1s) và phải test với chính user trước khi giao — không để user bị kẹt ở màn hình login.

## Faceplugin SDK (research 03/08 — KHÔNG dùng)

- `Faceplugin-ltd/Open-Source-Face-Recognition-SDK` — 1552 stars nhưng cần Torch 2.4.1 (~2GB), **không có LICENSE rõ ràng** (API trả license=None) — rủi ro cho product thương mại
- Đã thay bằng MediaPipe vì nhẹ hơn, license Apache 2.0 (Google), on-premise
