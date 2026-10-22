# Viettel Post (VTP) Partner API — notes từ Swagger chính thức

Nguồn: `https://partnerdev.viettelpost.vn/v2/v2/api-docs` (Swagger 2.0, fetched 2026-07-26).

## Envs
- Sandbox (dev): `https://partnerdev.viettelpost.vn/v2` — base URL mặc định khi `VTP_BASE_URL` trống
- Production: `https://api.viettelpost.vn`
- Login endpoint nằm ở ROOT (không có `/v2` prefix): `{base}/api/user/login`

## Auth
- `POST /api/user/login` body: `{USERNAME, PASSWORD, PARTNER_CODE?}` → response `data.token`
- Token truyền qua **header `Token`** (không phải Authorization Bearer) cho mọi request sau đó
- Token cache 55 phút (in-memory, `api/vtp.ts`) — tránh login liên tục
- Endpoint `https://api.viettelpost.vn` (không /v2) trả 404 — cần đúng path

## Endpoints đã verify (Swagger)

| Endpoint | Method | Mục đích |
|----------|--------|---------|
| `/categories/listProvince` | GET | Danh sách tỉnh |
| `/categories/listDistrict?provinceId=` | GET | Quận/huyện |
| `/categories/listWards?districtId=` | GET | Phường/xã |
| `/categories/listService` | POST `{}` | Dịch vụ vận chuyển |
| `/order/createOrderV2` | POST | **Tạo đơn** — body OrderAIForm |
| `/order/orderInfo?orderNumber=` | GET | Query trạng thái |
| `/order/cancelOrderV2` | POST `{ORDER_NUMBER}` | Hủy đơn |
| `/order/printV2` | POST `{ORDER_ARRAY, TYPE, EXPIRY_TIME}` | In tem |

## Create order — OrderAIForm fields chính

Người gửi: `SENDER_FULLNAME, SENDER_PHONE, SENDER_ADDRESS, SENDER_PROVINCE, SENDER_DISTRICT, SENDER_WARD` (ID numeric)
Người nhận: `RECEIVER_FULLNAME, RECEIVER_PHONE, RECEIVER_ADDRESS, RECEIVER_PROVINCE, RECEIVER_DISTRICT, RECEIVER_WARD`
Hàng hóa: `PRODUCT_NAME, PRODUCT_QUANTITY, PRODUCT_WEIGHT` (gram), `PRODUCT_PRICE`, `PRODUCT_DESCRIPTION`
Tài chính: `MONEY_COLLECTION` (COD — 0 nếu prepaid), `MONEY_TOTAL`, `MONEY_TOTALFEE`
Khác: `ORDER_NUMBER` (mã tham chiếu Volden), `ORDER_SERVICE`, `ORDER_NOTE`, `PICKUP_DATE` (dd/MM/yyyy), `DELIVERY_DATE`

Response: `data.ORDER_NUMBER` = mã vận đơn VTP; `data.MONEY_TOTALFEE` = phí ship.

## Status mapping (ORDER_STATUS → shippingStatus)

| VTP status | ShippingStatus |
|-----------|----------------|
| 1 (Chờ xử lý), 7, 8, 5, 6, 12 | pending |
| 2 (Đã lấy hàng) | picking |
| 3, 9 (Đang VC/Đang giao) | in_transit |
| 4, 10, 11 (Phát thành công) | delivered |

## Webhook (PostData)

VTP gọi POST tới URL đăng ký với body `{DATA: {ORDER_NUMBER, ORDER_STATUS, ...}, SECRET_WEBHOOK}`. Verify bằng `SECRET_WEBHOOK` hoặc header `x-vtp-secret` so với `VTP_WEBHOOK_SECRET` env.

## Pitfall — receiver phone

Order Volden chưa có phone khách — `RECEIVER_PHONE` đang gửi rỗng. VTP có thể require; nếu lỗi, cần thêm field phone vào order/lead trước khi createOrder hoạt động ổn định.
