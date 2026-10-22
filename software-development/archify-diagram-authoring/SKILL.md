---
name: archify-diagram-authoring
description: "Author and publish Archify JSON-IR diagrams from repos."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [archify, diagram, architecture, json-ir, render, publish]
    related_skills: [repo-lean-read, html-publishing, architecture-diagram, diagram-design]
---

# Archify — authoring & rendering JSON-IR diagrams

## Khi nào dùng
- User muốn sơ đồ kiến trúc/workflow/sequence/dataflow/lifecycle từ repo (dùng lại renderer Archify local, MIT, $0 — KHÔNG build lại renderer).
- Repo Archify review: `D:/Hermes Proj/archify-review/` (clone tt-a1i/archify).
- Renderer CLI: `archify/bin/archify.mjs render <type> <input.json> <output.html> [--quality showcase]`.

## Vòng làm việc chuẩn (author → validate → render → publish)
1. **Đọc repo bằng skill `repo-lean-read`** (graft map → grep surface → graft ask) để dựng model kiến trúc — renderer KHÔNG tự đọc code, mình phải author JSON.
2. Author JSON theo schema `archify/schemas/<type>.schema.json`. Bắt buộc: `schema_version`, `diagram_type`, `meta.title`, `components`. Components cần id/type/label; có thể `pos`/`size` (vẽ thủ công) hoặc layout grid.
3. `validate` trước: `node archify/bin/archify.mjs validate <type> <input.json> --json` — chạy schema + layout composition checker (9 check) trước khi render.
4. Render `--quality showcase` → self-contained HTML (~700KB).
5. Publish (xem "Publish" bên dưới).

## Constraints đã VERIFY (tránh vòng lặp fail)
- **Locale chỉ nhận `en`/`zh`** — KHÔNG có `vi`. Nhãn tiếng Việt để trong content/label, chrome UI (legend, search) tiếng Anh.
- **Card dot chỉ nhận `cyan`/`emerald`/`rose`** — KHÔNG `yellow`.
- **`--repo-root` + component `sources` bắt buộc có `meta.repository`** = GitHub URL public pinned + revision 40-hex. Repo local/private → **KHÔNG dùng `--repo-root`, và bỏ hết `sources`** (nếu còn sources mà thiếu meta.repository → error `repository-evidence/repository-required`).

## Composition checker — các lỗi bố cục hay dính + cách sửa (đã verify 6+ lần render thật)
Báo `[composition/...]` + tọa độ + `supportedFixes` (labelAt [x,y] / labelDy ±n). Sửa theo gợi ý là qua.
- **label-route-clearance**: label đụng route của connection khác (<4px). → đổi `fromSide`/`toSide` để route đi đường khác, hoặc `labelDy` đẩy label ra.
- **Label chồng component**: → `labelDy` +(-) đẩy ra khỏi box, hoặc `labelAt`.
- **clean-flow/endpoint-side-direction**: `via` có đoạn CHÉO, hoặc vi phạm fromSide/toSide. → `via` PHẢI vuông góc (chỉ ngoằn H/V) và điểm đầu phải đi thẳng theo fromSide, điểm cuối thẳng vào theoTẹo toSide. Đơn giản hơn: BỎ via, dời node chặn giữa ra khỏi đường thẳng.
- **clean-flow/edge-through-node + proper-crossing**: edge dài xuyên node/edge khác (VD edge deploy từ góc xa vào node trung tâm). → chỉ vẽ edge THẬT là data flow; deploy/infra môi trường ghi trong boundary label, không kẻ.
- **Label DÀI HƠN gap giữa 2 node** → nhét vào gap = chồng CẢ 2 node (label rộng ~1.5px/char; gap < label width). → đặt `labelAt` xuống DƯỚI 2 node (y > bottom của cả 2), không đặt trong gap. (Cứ tưởng labelAt vào [mid-gap, mid-y] là đúng → vẫn đè. Gọi gap x660-740, label "SQL (service_role)" rộng ~110px, phải xuống [700, 408].)
- **Label chồng NGUỒN trong edge ngang**: label mặc định đặt sát source node đè lên nó; `labelDy` + vẫn còn trong box → `labelAt` explicit vào khoảng trống/ngoài là dứt điểm.
- **2 direction ngược nhau cùng 1 hành lang dọc** (VD create-order xuống / webhook lên giữa CÙNG 2 node) → label đụng (0px clearance). → cho 1 edge `fromSide` corridor khác, hoặc **bớt 1 edge ghi vào card**. Không vẽ 2 chiều đè nhau.
- **meta.viewBox min [320,240]**; nếu bố trí node rộng trái-phải, đặt viewBox theo canvas.
- Rule chung khi author: set `fromSide`/`toSide` cho connection từ cùng 1 node đi nhiều hướng; **node "busy hub" nhiều edge cùng 1 phía → cấp lane riêng** bằng fromSide/toSide khác + labelDy đảo dấu (±) cho mỗi label; `fromSide:"bottom"` cho cặp trên-dưới.
- CLI OK = 9 check pass, 0 lỗi, 0 warning, `minLabelRouteClearance=4`.

Layout patterns + case thật theo từng repo: `references/layout-error-patterns.md`.

## Publish HTML kết quả
- **≤1MB → KV**: POST `https://preview.thefirstonly.com/api/store` với payload file (json.dumps ghi ra file rồi `--data-binary @file`; dùng curl, python urllib bị 403). → `https://preview.thefirstonly.com/<id>`.
- **>1MB → Gist + preview worker**: worker proxy fetch `/raw/index.html` — **file trong gist PHẢI tên `index.html`**, không phải tên khác (gist `archify-delta.html` bị 404 cho tới khi rename). PAT dùng `GITHUB_PAT_B64` trong `~/AppData/Local/hermes/.env` (base64 decode), không phải `GITHUB_PAT`.

## So sánh Mermaid (để giải thích cho người khác)
Archify = "AI viết JSON theo khuôn → tool VALIDATE hình học rồi mới dựng". Mermaid vẽ thẳng, không cửa chất lượng hình học. Chỗ Archify hơn: composition checker (route rhythm, micro-segment ≥8px, label clearance ≥4px, crossing, container border) + diagnostic fail-closed (mã lỗi + supportedFixes, không stack trace) + delta compare 2 bản kiến trúc (graph diff thêm/bớt/dời/reroute).

## Pitfall — đo token
Renderer phải thuê để author JSON; renderer local $0. Đừng ném cả file lớn vào; dùng repo-lean-read để lấy đúng model rồi author gọn.