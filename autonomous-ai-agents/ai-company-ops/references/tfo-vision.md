# TheFirstOnly — Purpose / Mission / Vision (chốt với Quang 2026-07)

Nguồn sự thật: `shared/workspace.md` trong repo ai-company (cả Hermes + Claw cập nhật). Bản ghi này là tóm tắt để agent nắm context nhanh.

## Purpose (Why)
Con người chết đuối trong thông tin — quá tải, lỡ việc, kiến thức rời rạc, không biết làm gì tiếp theo.
TheFirstOnly = trợ lý thực sự: ghi nhớ mọi thứ, xử lý dữ liệu, phân task, lên lịch, tự thực thi.
Không dừng ở "quản lý thông tin" — đi tới "định hướng hành động": thông tin → task → deadline → thực thi.

## Mission
Mọi lãnh đạo cấp cao đều có trợ lý thực — không bỏ lỡ, không quên, luôn biết việc tiếp theo.

## Vision
- Khách hàng: Founder/CEO/lãnh đạo cấp cao, sẵn sàng thuê trợ lý cá nhân.
- Khác biệt: (1) realtime lắng nghe liên tục → tự hình thành task → lên lịch → nhắc nhở → đề xuất; (2) chủ động "làm trước", không thụ động; (3) framework mới connect MCP với toàn bộ hệ sinh thái app.
- Moat: không phải 1 app cô lập — là framework kết nối mọi thứ.

## Quyết định đã chốt

### Autonomy
- Con người duyệt trước việc ai làm (human-in-the-loop, không auto 100%).
- **Bổ sung:** "duyệt trước → thực thi luôn" — 1 cổng duyệt, sau cổng AI chạy tức thời, không duyệt nhiều bước.

### 3 giá trị CEO không thể sống thiếu
1. Lắng nghe liên tục → bối cảnh luôn mới
2. Quét bối cảnh công ty → hỗ trợ ra quyết định, phân tích sâu
3. Thực thi task tức thời — CEO hustle

### Roadmap 3 giá trị
- Muốn cả 3, nhưng **phase đầu tiên phải làm được 1 + 2** (lắng nghe liên tục + quét bối cảnh/quyết định). Giá trị 3 (thực thi tức thời) để phase sau.

### Ghi âm / nghe (value 1)
- Thông báo trước cuộc họp → ghi âm → thực thi.
- **Ban đầu mặc định bật** — bật ghi âm cũng không ai phàn nàn. Cần consent flow đơn giản (1 lần, dạng onboarding).

### Phân phối mục tiêu (value 2)
- Mục tiêu + task luôn sẵn sàng — hỏi là có, agent tự đi hỏi để lấy kết quả trả về.

### Kính HUD (smart glasses)
- Thiết bị giống VR nhưng **không cần đeo** — tích hợp kính thông thường, luôn nhìn thấy mục tiêu **treo trước mắt**.
- ⚠️ Hardware = phase rất xa. MVP nên là app mobile/desktop trước, HUD là vision phase sau.

### Meeting presence (value 3)
- Luôn có mặt trong meeting — nghe, tổng hợp, truy xuất tức thời, đề xuất, sẵn sàng thực thi.

### Privacy
- Local-first, đồng bộ cloud multi-device.
- **Bổ sung:** có mã hóa — **key do người dùng tự cầm** (E2E encryption, user holds key). Cloud chỉ lưu bản mã hóa để sync — zero-knowledge, thành điểm bán cho CEO.

### M4 — Pricing
- Base hàng tháng + vượt limit trả thêm tiền (subscription + usage-based).

### M5 — Giá trị bán (value prop cho CEO)
- Tiết kiệm thời gian: không mất thời gian đọc meeting note, hiểu vấn đề rất nhanh.
- **Detect luôn vấn đề** + sẵn sàng quyết định + sẵn sàng action.

### M6 — Reliability
- **Không được để sập** — nhiều server sẵn sàng (multi-server redundancy).
- Sẵn sàng đẩy giá monthly lên để duy trì ổn định.

## Open questions (chưa chốt)
- CEO Việt Nam đau nhất điều gì lúc 3h sáng? (nỗi sợ = điểm bán hàng)
- Trợ lý người thật từng thất vọng ở đâu? (chậm, quên, không chủ động, sợ trách nhiệm?)

## Vòng 7 — Vai trò con người & rủi ro
- Con người làm những thứ AI không làm: leading, ý tưởng mới, khai phá những thứ mới AI chưa chạm tới.
- **Rủi ro lớn nhất:** bão hòa app/tính năng bị phổ biến hóa → ông lớn nhảy vào cướp vì có foundation model.
- **User đầu tiên:** Quang + anh trai (cũng là CEO) — dogfooding: AI build sản phẩm cho AI.

## VISION ĐÃ ĐƯỢC DUYỆT (2026-07)
- Bản nháp chính thức TheFirstOnly (Purpose/Mission/Vision) — Quang duyệt "1. Chuẩn".
- Lệnh tiếp: **"Bắt đầu lên plan thực thi tổng đi"** — sau khi hoàn thiện tầng 1-2.

## Plan thực thi (P1-P3, Quang chốt)
- **P1 — Đội ngũ build:** tự team AI Company agents (10 agents) — dùng sơ đồ phân role + task đã setup. Dogfooding thật sự.
- **P2 — Tech stack:** do **CTO agent** đề xuất (đã xong, xem tóm tắt bên dưới).
- **P3 — CEO pilot:** Quang + anh trai = 2 CEO đầu tiên.

### Tech stack MVP (CTO agent đề xuất — shared/cto_techstack.md trong repo)
- LLM: DeepSeek V4 Flash (realtime) + V4 (task phức tạp) — qua OpenCode.
- STT: Groq Whisper large-v3 streaming (free tier, có rate limit — chấp nhận với tần suất CEO).
- TTS: edge-tts (free).
- Backend: FastAPI + WebSocket, 1 VPS $6/tháng.
- DB: PostgreSQL + pg_dump backup mỗi 6h → Cloudflare R2 (free 10GB).
- Sync: WebSocket realtime + REST history, session ID per device.
- HA: 1 VPS + systemd auto-restart + Uptime Kuma; chấp nhận downtime <5 phút (multi-region overkill với budget $100).
- Recovery key: backup AES-256 bằng passphrase CEO giữ (openssl); mất passphrase = mất backup cũ (trade-off rẻ nhất).
- **Tổng cost: ~$10-15/tháng** — dư budget $100.

## Roles (đã đảo 2026-07 — Quang yêu cầu)
- **OpenClaw = FRONT:** tương tác trực tiếp với Quang — hỏi, chốt định hướng, trình tổng hợp.
- **Hermes = BACK:** logic, phản biện kín, review, triển khai kỹ thuật, giữ hạ tầng. Không tự hỏi anh.
