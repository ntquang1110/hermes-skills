---
name: shipping-carrier-integration
description: "Tích hợp carrier vận chuyển (Viettel Post hiện tại; GHN/247/GHTK sau): VTP API auth + endpoints + status mapping, standard address format dùng chung, sender từ warehouse, COD logic, webhook. Dùng khi làm 'lên đơn ship' trong dự án bán hàng."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [viettel-post, shipping, carrier, logistics, integration]
---

# Shipping Carrier Integration (VTP → GHN/247)

Tích hợp "lên đơn ship" từ order vào carrier API. Bắt đầu với Viettel Post (VTP); kiến trúc chuẩn bị sẵn adapter cho GHN/247/GHTK.

## Kiến trúc chuẩn (đã implement trong volden-ops-web 2026-07-26)

```
Order → POST /api/shipping/vtp/create
  → api/vtp.ts (client: login, address catalog, createOrder, query, cancel, print)
  → api/vtp-cache.ts (cache tỉnh/huyện/xã 24h)
  → api/address-format.ts (StandardAddress: text + ID theo VTP — dùng chung mọi carrier)
  → api/app.ts routes: /api/shipping/vtp/{status,config,provinces,districts,wards,services,create,query,cancel,print}
  → Webhook: /api/webhooks/vtp (VTP push status change)
  → UI: VtpOrderActions.tsx (nút Lên đơn + sync + in tem), SettingsModule (credentials)
```

**Nguyên tắc address dùng chung:** lưu CẢ text lẫn ID theo chuẩn VTP (`provinceId/districtId/wardId`). Carrier mới (GHN/247) chỉ cần viết 1 adapter convert từ StandardAddress → format riêng — KHÔNG đụng data.

**Sender = warehouse:** mỗi kho (`warehouses` table) có `address/province/district/ward` + ID + `senderName/senderPhone`. Khi lên đơn lấy sender từ `order.warehouse` → kho. Không hardcode.

## VTP API cheatsheet (đã verify Swagger chính thức)

Swagger: `https://partnerdev.viettelpost.vn/v2/v2/api-docs`
- **Sandbox:** `https://partnerdev.viettelpost.vn` (mặc định)
- **Production:** `https://api.viettelpost.vn`
- **Auth:** `POST {base}/api/user/login` body `{USERNAME, PASSWORD, PARTNER_CODE}` → `data.token`. Token truyền header `Token` cho mọi request. Cache 55 phút.
- Env: `VTP_USERNAME`, `VTP_PASSWORD`, `VTP_PARTNER_CODE`, `VTP_BASE_URL`, `VTP_WEBHOOK_SECRET`

| Endpoint | Mục đích |
|----------|---------|
| `GET /categories/listProvince` | Tỉnh |
| `GET /categories/listDistrict?provinceId=` | Huyện |
| `GET /categories/listWards?districtId=` | Xã |
| `POST /categories/listService` | Dịch vụ |
| `POST /order/createOrderV2` | Tạo đơn (OrderAIForm) |
| `GET /order/orderInfo?orderNumber=` | Query trạng thái |
| `POST /order/cancelOrderV2` | Hủy đơn |
| `POST /order/printV2` | In tem |

Create order fields quan trọng: `ORDER_NUMBER`, `ORDER_SERVICE`, `SENDER_FULLNAME/PHONE/ADDRESS/PROVINCE/DISTRICT/WARD`, `RECEIVER_*` (tương tự), `PRODUCT_NAME/QUANTITY/WEIGHT(gram)/PRICE`, `MONEY_COLLECTION` (COD), `MONEY_TOTAL`, `ORDER_NOTE`, `PICKUP_DATE`, `DELIVERY_DATE`.

Response parse: `data.ORDER_NUMBER` là mã vận đơn; `data.MONEY_TOTALFEE` là phí ship.

## Business rules đã chốt với user

- **Weight:** ưu tiên `products.weightGram`, **mặc định 5000g (5kg)/item** nếu trống
- **COD:** `paymentMethod === 'cod'` → `moneyCollection` = tổng tiền; prepaid → 0
- **Validate trước khi gọi:** kho phải có senderName/senderPhone + đủ provinceId/districtId/wardId; nếu thiếu → báo lỗi rõ "Vào Cài đặt > Kho để cấu hình"
- **Không lên đơn trùng:** nếu order đã có `vtpOrderNumber` → chặn
- **Tracking URL:** `https://viettelpost.vn/chi-tiet-don-hang?orderNumber=<code>`

## Status mapping (VTP → ShippingStatus)

1→pending, 2→picking, 3/9→in_transit, 4/10/11→delivered, còn lại→pending. Names: 1 Chờ xử lý, 2 Đã lấy hàng, 3 Đang VC, 4 Đã phát thành công, 9 Đang giao, 10 Phát thành công, 12 Hàng trả lại.

## Webhook

VTP gọi `POST {app}/api/webhooks/vtp`, body `{DATA: {ORDER_NUMBER, ORDER_STATUS}, SECRET_WEBHOOK}`. Verify secret nếu config có. Khi nhận → tìm order theo `vtpOrderNumber` → update `shippingStatus` + stage (delivered→delivered, in_transit→shipping).

## Pitfalls

- Login endpoint nằm ở ROOT không có `/v2` prefix: `{base.replace(/\/v2$/, "")}/api/user/login`
- VTP API đôi khi trả lỗi `invalid key` kể cả khi key đúng — kiểm tra theo cặp key+token cùng 1 app (xem skill trello-workflow auth failures)
- Auto-progress timer hardcode GHN name — đã fix: chỉ set khi `carrierType !== 'viettel_post'`
- Weight luôn tính theo gram; `PRODUCT_QUANTITY` tổng số item
- Production switch = `VTP_BASE_URL` env, không sửa code

Xem thêm: `references/vtp-deep-dive.md`
