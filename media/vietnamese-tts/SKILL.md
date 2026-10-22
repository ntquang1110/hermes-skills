---
name: vietnamese-tts
description: "Use when picking or setting up Vietnamese TTS voices."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [tts, vietnamese, voice, text-to-speech, vie-neu, wheneu, whisper, edge, azure, gemini, mac]
    related_skills: [voice-and-stt, songwriting-and-ai-music, whisper-groq-transcription, publish]
---

# Vietnamese TTS (chọn giọng & setup local)

## When to Use

- User cần chọn/nghiên cứu giọng đọc tiếng Việt "mượt, tự nhiên".
- Cần sinh audio tiếng Việt từ các provider có sẵn hoặc model local trên Mac.
- Cần verify một file audio có đúng nội dung/tiếng Việt không (dùng local Whisper transcribe lại).

## Landscape nhanh giọng tiếng Việt (2025-2026)

| Provider | Giọng tiếng Việt | Giới tính | Giá / cần key | Ghi chú |
|----------|-----------------|-----------|---------------|---------|
| **Edge TTS** (miễn phí) | `vi-VN-HoaiMyNeural` (nữ), `vi-VN-NamMinhNeural` (nam) | cả 2 | Free, không key | Chính là giọng Azure Neural; cài `edge-tts` là sinh được ngay |
| **Google Gemini TTS** | qua `gemini-2.5-flash-preview-tts`, dùng đang có `GOOGLE_API_KEY` | — | Free tier | Nói tiếng Việt chuẩn (đã verify) |
| Google Cloud Chirp3-HD | `vi-VN-Chirp3-HD-*` (2025, 30 giọng)+Neural2+Gemini Flash TTS | cả 2 | Chirp3 $30/1M, Neural2 $16/1M | Siêu tự nhiên; gọi `texttospeech.googleapis.com` bằng `GOOGLE_API_KEY`
| **ElevenLabs** | `eleven_v3` & `flash_v2_5` (CÓ `vi`); ⚠️ `multilingual_v2` KHÔNG có VN | cả 2 | $100/1M (v3), $50/1M Flash, free tier 10k chars | Chuẩn vàng cảm xúc, "người thật nhất"; Hermes chưa có key |
| Amazon Polly | `Hanna` (nữ), `Lam` (nam) | cả 2 | Theo usage | Ổn, không xuất sắc |
| **VinAI VieNeu (vieneu SDK)** | 20 giọng preset, 3 vùng Bắc/Nam/Trung | cả 2 | Free, 100% local | 48kHz, clone giọng, cảm xúc inline |
| Zalo AI / Vbee / Viettel AI | 1-N giọng | — | Theo nhà cung cấp | Nội địa |

## Workflow chọn giọng (thủ tục chuẩn)

1. **Hiểu use-case** trước (đọc nội dung? podcast? giọng nam/nữ? vùng nào?).
2. **Research landscape** + giá. Cá biệt hóa: cái nào ĐÃ có key/tài nguyên (sinh mẫu ngay) vs cần mua.
3. **Sinh cùng 1 đoạn văn cố định** qua mọi giọng ứng viên → đệ gửi audio để user nghe so sánh. Đoạn văn ngắn, tự nhiên, đủ đặc trưng giọng.
4. **Verify nội dung**: transcribe lại audio đã sinh bằng local Whisper để chắc đúng tiếng Việt / đúng chữ. Cảnh giác: `say` (macOS TTS) đọc tiếng Việt KHÔNG chuẩn → không dùng để đánh giá chất lượng, chỉ transcribe audio thật.

## Giọng VieNeu đã chốt (07/09): "Thanh Bình"

Thanh Bình = Nam · Bắc · kể chuyện, v3 Turbo, preset #13. Mẫu: `D:/Hermes Proj/tts_samples/vieneu_all/13_Thanh_Binh.wav` (đã sinh TOÀN BỘ 20 giọng cùng đoạn văn ở `vieneu_all/`). Chọn giọng cho app = quyết định 2 bước: user nghe mẫu → chốt "giọng X đi" → confirm tên + đặc tính, LƯU state/memory, rồi HỎI mục đích dùng (app nào / đọc gì) trước khi tích hợp. Đừng tự đoán app.

### Tích hợp VieNeu vào app chạy máy KHÁC (cross-machine LAN)

Khi app chạy trên Windows (vd TFO, `app/tts.py` dùng EdgeTTSProvider VOICE `vi-VN-HoaiMyNeural`) mà giọng VieNeu local trên Mac (192.168.1.3) — không gọi thẳng được như edge. Pattern:
- Recipe Deploy micro TTS-server trên Mac + client Windows đầy đủ (script deploy, pitfalls WAV-vs-MP3 sniff, fallback edge, voice phải giữ dấu khi qua heredoc/paramiko, cổng FFT chống hallucinate STT): xem **`references/vieneu-http-server.md`**.
- Giữ interface `TTSProvider` (synth/stream) có sẵn; thêm `VieNeuProvider` CẠNH EdgeTTSProvider, đóng sau interface để swap không phá.
- Chạy mini TTS server trên Mac: nhận text → `tts.infer(voice="Thanh Bình")` → trả wav. App HTTP request tới `192.168.1.3:<port>`.
- Edge giữ làm fallback khi Mac chết.
- Trade-off phải nêu với user: latency LAN ~2-4s/câu (M1 render + truyền) so edge ~1-2s; init model lần đầu ~20s; phải giữ Mac sống.
- 0đ, free local.

### Cổng tần số giọng người chống hallucinate STT (VAD quá nhạy)

Khi VAD dùng RMS energy thuần, tạp âm nền (quạt/gió/hum 50Hz) vượt ngưỡng vẫn bị gửi vào Whisper/Groq → model BỊA chữ khi không có giọng. Fix đã verify (numpy, 0đ): FFT đoạn PCM → tính tỉ lệ năng lượng trong băng 300-3400Hz (formant giọng người) → dưới ngưỡng (0.55) hoặc RMS quá yếu (0.02) thì BỎ không gửi STT. Chi tiết code + verify: `references/vieneu-http-server.md` §4. Hiệu quả: hum 50/100Hz ratio≈0 (loại), sine 500/1000Hz ratio≈1 (giữ).

## Level-1: Edge TTS (nhanh, miễn phí, không key)

Sinh mẫu VN (`edge-tts`, không cần key):
```python
import asyncio, edge_tts
async def main():
    vn = [v for v in await edge_tts.list_voices() if v["ShortName"].startswith("vi-VN")]
    for v in sorted(vn, key=lambda x:x["Gender"]):
        print(v["ShortName"], v["Gender"])
    await edge_tts.Communicate(TEXT, "vi-VN-HoaiMyNeural").save("hoaimy.mp3")
asyncio.run(main())
```
Edge chỉ có ĐÚNG 2 giọng VN (HoaiMy nữ + NamMinh nam), đều dạng Natural.

## Level-2: VieNeu local trên Mac (20 giọng preset)

Xem `references/vie-neu-mac-setup.md` cho recipe chi tiết.
- SDK: `pip install vieneu`. Cần **Python ≥3.10** — python system trên Mac là 3.9 nên dùng `~/.local/bin/python3.11 -m venv ~/vieneu-venv`.
- Lần đầu `Vieneu()` tự tải thêm file model, gồm `speaker_encoder.onnx` (cần clone giọng).
- Pitfall: **`style` arg bị deprecated/ignored trên v3 Turbo** — phong cách đọc (tự nhiên/tin tức/kể chuyện/đọc truyện) gắn sẵn TRONG từng preset voice, chọn `voice="Tên"` chứ không truyền `style`.
- Sinh rất nhanh trên Apple Silicon: mỗi giọng clip ngắn ~4-5s.

## Cách gửi audio mẫu cho user

Dùng `MEDIA:<absolute path>` trong response (Telegram tự gửi file âm thanh). Đặt tên file có ý nghĩa: `vieneu_natural.wav`, `edge_vi-VN-HoaiMyNeural.mp3`...

- Khi user nói "gửi hết voice / gửi toàn bộ voice" → sinh **TOÀN BỘ các giọng preset** (không chỉ vài cái), cùng 1 đoạn văn cố định, nhóm theo phong cách đọc (tự nhiên / tin tức / kể chuyện / đọc truyện), gửi hết qua `MEDIA:`. Mỗi giọng gắn label: tên, giới tính, vùng, phong cách.
- Nếu user muốn thêm giọng khác (nam/nữ, vùng), hoặc clone theo giọng mẫu (đưa audio 3-8s), hoặc chấm điểm top candidates — đề xuất rõ để anh chốt.

## Giọng Hermes toàn cục PHẢI là giọng Việt (bug đã gặp)

`tts.edge.voice` trong `~/AppData/Local/hermes/config.yaml` từng để `en-US-AriaNeural`.
Hệ quả: MỌI text tiếng Việt Hermes đọc ra đều thành âm vô nghĩa — giọng Anh đọc chữ Việt.
Nghi ngay khi audio TTS "nghe như tiếng Anh bồi", hoặc khi STT trả về câu vô nghĩa.

```
python -c "import yaml; t=yaml.safe_load(open('config.yaml'))['tts']; print(t.get('provider'), t.get('edge',{}).get('voice'))"
hermes config set tts.edge.voice vi-VN-NamMinhNeural   # hoặc vi-VN-HoaiMyNeural
```

Edge chỉ có ĐÚNG 2 giọng VN: `vi-VN-HoaiMyNeural` (nữ), `vi-VN-NamMinhNeural` (nam).
Nếu user muốn "Thanh Bình v3" (VieNeu) thì phải dựng provider riêng — xem mục VieNeu dưới.

**Đã chốt giọng toàn cục (10/2026): user chọn GIỌNG NỮ → `vi-VN-HoaiMyNeural`.**
Khi hỏi chọn giữa 2 giọng Edge, user trả lời ngắn "dùng giọng nữ đi" — set rồi, không hỏi lại.
Phân biệt 2 tầng giọng đang dùng song song, đừng lẫn:

| Tầng | Giọng | Ghi chú |
|------|-------|---------|
| Hermes toàn cục (`tts.edge.voice`) | `vi-VN-HoaiMyNeural` (nữ) | user chốt 10/2026 |
| App TTS riêng (VieNeu local) | "Thanh Bình" (nam, Bắc) | user chốt 07/09 — xem mục VieNeu |

### Dấu hiệu gián tiếp: STT hallucinate một câu cố định

Audio sai ngôn ngữ KHÔNG báo lỗi. Nó chảy xuống STT, và Whisper ép `language=vi` lên
audio không phải tiếng Việt sẽ **bịa ra một câu trôi chảy nhưng vô nghĩa**, ví dụ:
`"Hãy subscribe cho kênh La La School Để không bỏ lỡ những video hấp dẫn"`.
Cùng một file, output giống nhau từng ký tự (70 ký tự) ⇒ model không hề decode audio.
Gặp STT trả câu trôi chảy mà vô nghĩa → kiểm tra giọng TTS TRƯỚC khi nghi model STT.
Quy trình triage đầy đủ: skill `faster-whisper-local`, mục "STT returns a fluent but WRONG sentence".

### Sinh audio test đúng tiếng Việt trên macOS

`say` mặc định (giọng Anh) đọc tiếng Việt sai bét — không dùng để đánh giá gì cả.
Dùng giọng Việt thật, và **luôn viết câu nguồn CÓ DẤU đầy đủ**:

```
say -v Linh -o /tmp/t.aiff "Kiểm tra hệ thống nhận dạng giọng nói."
afconvert -f WAVE -d LEI16@16000 -c 1 /tmp/t.aiff /tmp/t.wav
```

Mac không có ffmpeg; `afconvert` có sẵn. `say -v '?' | grep vi_VN` để liệt kê giọng Việt.
Câu nguồn thiếu dấu ⇒ `say` đọc sai thanh ⇒ transcript trông hỏng dù stack khoẻ.
Đã đo trên máy thật: câu có dấu đầy đủ → khớp 87% từ (2 chỗ "lệch" chỉ là `7`/`bảy`, `10`/`mười`).

## Pitfalls / mẹo

- **Chirp3-HD gọi API trả `401 Unauthorized`** dù có `GOOGLE_API_KEY`: key đó là key Gemini thuần, chưa bật "Cloud Text-to-Speech" API trên Google Cloud project. KHÔNG phải lỗi code — chỉ dẫn bật API/service + billing. Giọng test: `vi-VN-Chirp3-HD-Aoede` (nữ), `-Fenrir` (nam trầm).
- **ElevenLabs `multilingual_v2` / `eleven_monolingual_v2` KHÔNG có tiếng Việt** — đừng chọn làm giọng VN. Chỉ `eleven_v3` và `flash_v2_5` hỗ trợ `vi`.
- SSH tới thiết bị khác (Mac) từ Windows/git-bash: `sshpass` KHÔNG có sẵn, key auth có thể fail → dùng `paramiko` (`pip install paramiko`) kết nối bằng password. Mac: user `tquang`, pw `<PASSWORD>`. ⚠️ **ĐỪNG hardcode IP Mac** — máy dùng DHCP, IP đã drift `.3 → .2 → .4 → .5` chỉ trong vài ngày; mọi `192.168.1.3` viết cứng sẽ âm thầm hỏng. Dùng `scripts/mac_whisper_resolve.py` (mDNS `Mac-mini-cua-kiem.local` → cache → quét `/24` cổng 9000) trong skill `faster-whisper-local`.
- Verify audio = transcribe lại (local Whisper trên Mac: `~/whisper-venv/bin/python ~/whisper/run_whisper.py <file> --lang vi`).
- Trước khi nói "giọng X đã có", kiểm tra key/provider thật: Hermes chưa có key ElevenLabs cho tiếng Việt; có `GOOGLE_API_KEY` (Gemini TTS), Edge free, vieneu local.
- Đừng bỏ password/credential vào tài liệu publish công khai trừ khi user yêu cầu; đánh dấu "nội bộ LAN".
- Cài venv với đúng python: package có thể yêu cầu version tối thiểu (vieneu cần ≥3.10) → tạo venv bằng `python3.11` đúng bản rồi cài trong venv đó.