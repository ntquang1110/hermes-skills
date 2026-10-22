# Knowledge Flow (kflow) — System Overview

kflow là hệ thống knowledge base dùng Next.js 16 + Supabase. Dùng để lưu trữ research, tài liệu, và các card kiến thức.

## Thông tin hệ thống

| Property | Value |
|---|---|
| Directory | `~/knowledge-flow/` |
| Port | 3003 |
| Database | Supabase project `theliems` (`vgozvweyqcqkayafntwx`) |
| Render | Next.js 16 + Tailwind 4 + shadcn/ui |
| Auth (kflow) | Bearer token `hermes-knowledge-secret` |
| Passcode gate | 🔒 Active từ 2026-08: MỌI request cần `Cookie: tfo_auth=<sha256('<PASSCODE>')>` — xem kflow-push-api.md |
| Cards (Aug 02) | **227 cards** — 9 chủ đề chính |

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/knowledge` | POST | Push card (auto-creates topic) |
| `/api/cards` | GET | List all cards (dùng cho dedup) |
| `/api/cards` | POST | Push card (manual topic) |
| `/api/topics` | GET | List topics |

**Auth header:** `Authorization: Bearer hermes-knowledge-secret` + `Cookie: tfo_auth=<sha256('<PASSCODE>')>` (passcode gate — thiếu cookie → 307 redirect /passcode, API trả trang login thay vì JSON)

## Push API

**Endpoint:** `POST /api/knowledge`

```json
{
  "title": "Research title",
  "summary": "1-2 sentence summary",
  "content": "Full content (markdown or raw text)",
  "tags": ["tag1", "tag2"],
  "topic_slug": "topic-name",
  "source_url": "https://preview.thefirstonly.com/<gist_id>"
}
```

**Topic auto-creation:** Nếu `topic_slug` chưa tồn tại, kflow tự tạo topic mới.

## Dedup & Dual Push Architecture

Chi tiết tại **`references/kflow-push-api.md`** — bao gồm:
- Dedup 3 tầng (title overlap ≥50%, content match, session search)
- Dual push architecture (knowledge-researcher 2h/lần + auto-push midnight)
- Windows cron pitfalls (MSYS2 path, Python version, execute_code blocking)
- Full code examples và proof 5+ lần chạy thành công

## Cron jobs

| Cron ID | Lịch | Vai trò |
|---------|------|---------|
| `d43697af1322` | Mỗi 2h | Knowledge-researcher: research sâu + push trực tiếp |
| `da7c6b38c7d9` | 00:00 daily | Auto-push: safety net, catch research bị sót → [SILENT] là bình thường |

## Chủ đề coverage (Aug 02)

KF đã bao phủ toàn bộ các chủ đề: Vật lý (4 cards), Kim loại nặng As/Pb/Hg/Cd (14+ cards), Xử lý khô/ướt (5 cards), Than bùn (3 cards), Saponin (3 cards), Sinh học phân tử (125 cards), Chăn nuôi heo (157 cards).

## Passcode gate & timestamps (cập nhật Aug 03)

- **Passcode gate:** KF 3003 có `web-passcode-gate` (passcode `<PASSCODE>`, hash `1d1e977a...`). API `/api/*` cũng bị gate → mọi curl/Python phải kèm `Cookie: tfo_auth=<hash>` (chi tiết + code mẫu trong `kflow-push-api.md`)
- **Timestamps:** `cards.created_at` là UTC, `sessions.started_at` là local (UTC+7) — lệch 7h khi đối chiếu
- **session_search không thấy cron sessions:** query `state.db` trực tiếp (bảng `sessions`, `messages`) để tìm knowledge-researcher sessions
