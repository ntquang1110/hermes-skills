---
name: viettel-post-integration
description: "Integrate Viettel Post (VTP) shipping API into order/ERP systems — auth (token), address categories, order creation, tracking query, webhooks, sandbox vs production switching."
category: productivity
---

# Viettel Post Shipping API Integration

Integrate Viettel Post (VTP) into an order-management app so orders can be booked as VTP shipments ("lên đơn ship"), tracked, and label-printed. Use when the user asks to integrate VTP, Viettel Post, lên đơn ship, or create shipment via VTP.

## Base URLs — sandbox vs production

| Env | Host | Use for |
|-----|------|---------|
| **Sandbox (dev)** | `https://partnerdev.viettelpost.vn` | Testing — first choice per user preference |
| **Production** | `https://api.viettelpost.vn` | Real shipments |

- Both use **basePath `/v2`** for the modern API surface (Swagger: `GET /v2/v2/api-docs` on partnerdev).
- Swagger spec is the authoritative reference: `curl https://partnerdev.viettelpost.vn/v2/v2/api-docs` → full JSON (auth, endpoints, DTOs).
- The root `/` returns 404 on prod — that's normal, don't treat it as a down signal. Hit real endpoints only.
- Partner web portal (credentials/contracts): `https://partner2.viettelpost.vn` — has human docs ("Tạo đơn", "Hướng dẫn tích hợp").

## Auth

Modern VTP API uses a **partner token**, not an API key:

1. `POST /user/login` (or `POST /user/register` for new) with `LoginForm`:
   ```json
   { "USERNAME": "...", "PASSWORD": "...", "PARTNER_CODE": "..." }
   ```
2. Response contains the token.
3. Send token on EVERY subsequent call in the **`Token` request header** (Swagger: `Token` header, "get from login API").
4. `GET /core/create-token?token=...` also exists (older pattern).

Credentials to request from user: USERNAME, PASSWORD, PARTNER_CODE (from partner2.viettelpost.vn account/partner info). Store in env: `VTP_USERNAME`, `VTP_PASSWORD`, `VTP_PARTNER_CODE`, `VTP_BASE_URL`, `VTP_WEBHOOK_SECRET`.

## Key endpoints (verified from Swagger)

| Purpose | Method + Path | Notes |
|---------|--------------|-------|
| List provinces | `GET /categories/listProvince` | |
| List districts | `GET /categories/listDistrict?provinceId=` | |
| List wards | `GET /categories/listWards?districtId=` | |
| List services | `POST /categories/listService` | body `DrafForm` |
| Extra services | `GET /categories/listServiceExtra?serviceCode=` | |
| List post offices | `GET /categories/listBuuCucVTP` | |
| **Create order** | `POST /core/orders/save?edit=false` | body `OrderAIForm` (see below) |
| Query order | `GET /core/orders/query?code=` | status lookup |
| Webhook config | `PostData`: `URL_WEBHOOK` + `SECRET_WEBHOOK` | VTP pushes status updates |

## Order creation essentials (`OrderAIForm` / `OrderInfo`)

Key fields for a shipment (Vietnamese order of the API):

- `ORDER_NUMBER` — your own order reference (idempotency key)
- `ORDER_SERVICE` / `ORDER_SERVICE_ADD` — service code(s), get from listService
- **Sender** — `SENDER_FULLNAME`, `SENDER_PHONE`, `SENDER_ADDRESS`, `SENDER_PROVINCE`, `SENDER_DISTRICT`, `SENDER_WARD` (province/district/ward are **numeric IDs**, not names)
- **Receiver** — `RECEIVER_FULLNAME`, `RECEIVER_PHONE`, `RECEIVER_ADDRESS`, `RECEIVER_PROVINCE`, `RECEIVER_DISTRICT`, `RECEIVER_WARD`
- **Products** — `PRODUCT_NAME`, `PRODUCT_QUANTITY`, `PRODUCT_WEIGHT` (required), `PRODUCT_PRICE`
- **Money** — `MONEY_COLLECTION` (COD amount), `MONEY_TOTAL`, `MONEY_TOTALFEE`
- `PICKUP_DATE`, `DELIVERY_DATE`, `ORDER_NOTE`, `ORDER_TYPE`

Response includes VTP `ORDER_NUMBER` (the waybill/tracking code) — store it as `trackingUrl`/`shippingStatus` on the order.

## Integration plan shape (used for volden-ops-web)

Four phases, each independently testable:

1. **VTP client + config** — `api/vtp.ts` (login, token cache, address list, createOrder, queryOrder), env vars, settings UI for credentials
2. **UI "Lên đơn VTP"** — button on eligible orders (approved/paid/reported_warehouse), pick service, send shipping info, save waybill number + trackingUrl
3. **Webhook + status sync** — `POST /api/webhooks/vtp` (verify SECRET_WEBHOOK), update `shippingStatus`; fallback periodic `core/orders/query`
4. **Print label** — `core/orders/print` style endpoint → PDF

## User-confirmed decisions (volden-ops-web)

- **Sandbox first** (`partnerdev`), update `.env` + `.env.prod` for prod switching
- **COD + transfer BOTH allowed** — `moneyCollection` depends on paymentMethod (COD = outstanding amount, transfer = 0)
- **Weight default: 5kg per item** if the product has no weight column (kg column may exist; use it when present)
- Existing `CarrierType` already includes `viettel_post`; ShippingModule already has a Viettel Post tab (pending → in_transit → delivered) — hook real statuses into it
- Watch for hardcoded GHN auto-progress in `api/app.ts` (~line 5963) that sets `carrierName="Giao hàng Nhanh (GHN)"` on `shipping_booked` — must only apply when carrierType=ghn, never overwrite VTP

## Pitfalls

- **Address fields need numeric IDs** (province/district/ward), not text — map & cache VTP's own lists (listProvince/listDistrict/listWards) and store IDs alongside the display names
- `PRODUCT_WEIGHT` is required — never send an order without it
- Token is a header (`Token:`), NOT a query param like Trello/GitHub
- Sandbox vs prod tokens are NOT interchangeable — keep separate env per environment
- Partner credentials (username/password/partner_code) differ from the web login — user must fetch them from the partner portal, not guess
- If VTP returns an error body, read `message`/`error` fields — the API often returns HTTP 200 with an error flag inside the JSON body

## References

- `references/vtp-swagger-notes.md` — Swagger field dump + endpoint inventory from partnerdev.viettelpost.vn (retrieved 2026-07-26)
