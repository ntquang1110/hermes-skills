# Archify Layout Error Patterns — case thật (30/08/2026)

Các lỗi composition gặp khi render 4 repo (OpenWorker, meTelligent, dithi, volden). Ghi lại mã lỗi + hoàn cảnh + fix đã dùng để lần sau khỏi lặp vòng.

## 1. via chéo → clean-flow/endpoint-side-direction
Mã lỗi: `first segment [295,390] -> [380,430] does not honor fromSide`.
Hoàn cảnh: cố tránh node chặn giữa bằng via [[380,430],[700,430]]. Điểm đầu chéo (diagonal) → renderer từ chối vì vi phạm hướng fromSide/toSide.
Fix dùng được: **BỎ via, dời node chặn ra khỏi đường thẳng.** (VD flocal từ [450,320] dời lên [450,180] — api→notion có lối đi sạch ở y~355.) Không cố gồng via vuông góc.

## 2. Label dài hơn gap → chồng cả 2 node
Mã lỗi: `Label "SQL (service_role)" overlaps component "api"` + `overlaps "db"` (2 lần liền).
Nguyên nhân: label ~110px trong gap x660-740 (80px). labelAt [700,358] trong gap vẫn đè cả 2 bên.
Fix: `labelAt [700, 408]` (y DƯỚI bottom api=390) — ngoài gap, xuống vùng trống.
Tương tự dithi "persist already" / srv→store gap x400-480 (80px): labelAt [430,400] (dưới srv bottom 370).

**Quy tắc: label ngang giữa 2 node, nếu label rộng hơn gap → đặt labelAt xuống DƯỚI cả 2 node, không nhét vào giữa gap.**

## 3. Label mặc định đè source trong edge ngang
Mã lỗi: `Label "start/chunk/end" overlaps component "phone"`, `Label "REST /api/*" overlaps "spa"`.
Nguyên nhân: label ngang mặc định anchor sát source node → đè lên box source.
`labelDy +26` chưa đủ (label rect vẫn trong box source — box cao ~56-64px).
Fix: `labelAt` explicit vào khoảng trống GIỮA 2 node khi gap đủ rộng; nếu gap hẹp thì `labelAt` xuống dưới.

## 4. Back-forth 2 chiều cùng hành lang dọc
Mã lỗi: label "webhook" 0px (0.2px) từ segment "create order".
Hoàn cảnh: api→vtp (create order xuống) + vtp→api (webhook lên) giữa CÙNG 2 node — route cả 2 dọc theo x~570.
Fix dùng được (đơn giản nhất): **bớt 1 edge (webhook), ghi vào card** "webhook khớp tiền tự động" thay vì kẻ. Diagram vẫn trung thực, tránh đụng route.
Alternate: cho 1 edge corridor khác (fromSide khác) — phức tạp hơn, chỉ khi edge thật sự cần kẻ.

## 5. Edge môi trường xuyên diagram
Mã lỗi: vercel→spa "deploy" — `endpoint-side-direction` + `proper-crossing` với api-engine.
Nguyên nhân: vercel (góc trên phải) → spa (trung tâm trái), đi qua api/engine.
Fix: **bỏ edge deploy** — môi trường triển khai đã có trong boundary label "Volden App (triển khai Vercel)". Chỉ vẽ data-flow thật.

## 6. Busy hub nhiều edge cùng 1 phía
Hoàn cảnh: OpenWorker `perm` có 2 edge thoát cùng phải (→reviewer, →audit) + 1 qua bottom. 2 label kề đụng (0px clearance).
Fix: tách `labelDy` đảo dấu — "auto-approve" labelDy −38 (lên), "provenance" labelDy +24 (xuống). Pass ngay.

## Checklist nhanh trước khi render lần đầu (rút từ 5 lần render)
1. Label ngang 2 node / gap hẹp → dự định `labelAt` xuống dưới ngay từ đầu, đừng chờ lỗi.
2. 2 label cùng exit 1 phía node → trải labelDy ±(20..50) đảo dấu.
3. Không kẻ edge môi trường (deploy) / back-forth 2 chiều dọc cùng hành lang → ghi card.
4. Không dùng via trừ khi chắc chắn vuông góc + đúng hướng; ưu tiên dời node.
5. `meta.viewBox` đủ rộng theo bố trí trái-phải.