---
name: viettel-post-api
description: "Viettel Post (VTP) partner API: auth, address catalog, create/query/cancel/print orders, webhook, sandbox vs prod. Used for 'lên đơn ship' integrations."
category: productivity
---

# Viettel Post (VTP) Partner API

Viettel Post shipping API for creating courier orders from a business app ("lên đơn Viettel Post"). Documented from the official Swagger at `https://partnerdev.viettelpost.vn/v2/v2/api-docs` (2026-07-26).

## When to Use

- Integrating VTP shipping into an app (Volden Ops, e-commerce, ERP)
- "Lên đơn VTP", tạo vận đơn, in tem, sync trạng thái ship
- Resuming the volden-ops-web VTP integration (env vars pending)

## Environment: sandbox vs production

| Env | Base URL | Notes |
|-----|----------|-------|
| Sandbox (dev) | `https://partnerdev.viettelpost.vn` | Login at `{base}/api/user/login`, API under `/v2` |
| Production | `https://api.viettelpost.vn` | Same path structure |

Design rule: **one env var `VTP_BASE_URL` switches sandbox/prod** — code defaults to sandbox when unset. `{base}/api/user/login` is at root (no `/v2`), everything else under `/v2`.

## Auth

```
POST {base}/api/user/login
Body: { "USERNAME": "...", "PASSWORD": "...", "PARTNER_CODE": "..." }   # PARTNER_CODE optional
→ data.token (or data.TOKEN / token)
```

- Token passed as **header `Token`** on every subsequent request.
- Cache the token ~55 min (login is expensive); auto-refresh when expired; dedupe concurrent logins with an in-flight promise.
- Credentials come from partner2.viettelpost.vn. User convention (Volden): weight missing → default **5kg/item**.

## Endpoints (all under `/v2` unless noted)

| Path | Method | Purpose |
|------|--------|---------|
| `/categories/listProvince` | GET | Provinces |
| `/categories/listDistrict?provinceId=` | GET | Districts |
| `/categories/listWards?districtId=` | GET | Wards |
| `/categories/listService` | POST | Available services |
| `/order/createOrderV2` | POST | **Create shipment** (OrderAIForm below) |
| `/order/orderInfo?orderNumber=` | GET | Query status (also `/core/orders/query?code=`) |
| `/order/cancelOrderV2` | POST | Cancel `{ ORDER_NUMBER }` |
| `/order/printV2` | POST | Print label `{ ORDER_ARRAY, TYPE, EXPIRY_TIME }` |

Address catalog changes rarely → cache provinces/districts/wards in-memory 24h.

## Create order payload (OrderAIForm key fields)

```jsonc
{
  "ORDER_NUMBER": "volden-ref",        // your reference — becomes tracking code on success
  "ORDER_REFERENCE": "volden-ref",
  "ORDER_SERVICE": "VTP",              // from listService
  "SENDER_FULLNAME": "...", "SENDER_PHONE": "...", "SENDER_ADDRESS": "...",
  "SENDER_PROVINCE": 1, "SENDER_DISTRICT": 1, "SENDER_WARD": 1,   // numeric IDs, not names
  "RECEIVER_FULLNAME": "...", "RECEIVER_PHONE": "...", "RECEIVER_ADDRESS": "...",
  "RECEIVER_PROVINCE": 0, "RECEIVER_DISTRICT": 0, "RECEIVER_WARD": 0,
  "PRODUCT_NAME": "...", "PRODUCT_QUANTITY": 1, "PRODUCT_WEIGHT": 5000, // grams
  "PRODUCT_PRICE": 0, "PRODUCT_DESCRIPTION": "",
  "MONEY_COLLECTION": 0,   // COD thu hộ — 0 nếu đã chuyển khoản
  "MONEY_TOTAL": 0,
  "ORDER_NOTE": "", "PICKUP_DATE": "", "DELIVERY_DATE": ""
}
```

Response success → `data.ORDER_NUMBER` (or `data.orderNumber` / top-level) = mã vận đơn; `data.MONEY_TOTALFEE` = shipping fee. **Always validate presence before treating as success** — response is wrapped, shape varies.

## Status mapping

VTP numeric status → app shipping status:

| VTP | Meaning | Map to |
|-----|---------|--------|
| 1, 7, 8 | Chờ xử lý / xác nhận | pending |
| 2 | Đã lấy hàng | picking |
| 3, 9 | Đang vận chuyển / đang giao | in_transit |
| 4, 10, 11 | Phát thành công | delivered |
| 5, 6, 12 | Trả hàng | pending |

## Webhook

VTP posts to a public URL when order status changes. Body (PostData):
```
{ "DATA": { "ORDER_NUMBER": "...", "ORDER_STATUS": N }, "SECRET_WEBHOOK": "..." }
```
Verify `SECRET_WEBHOOK` against configured secret, look up order by `vtpOrderNumber`, update shipping status. Vercel/Express route must be **public** (no `requireAuth`).

## Pitfalls

| Issue | Fix |
|-------|-----|
| Login endpoint 404 | It's at `{base}/api/user/login` (root), NOT under `/v2` |
| Order rejected: address | VTP needs numeric province/district/ward IDs — text names alone won't work. Store IDs when picking address |
| Weight missing | User convention: default 5000g/item; sum over items × qty |
| Sender address | Take from company_info config; hardcode IDs only as fallback (Hà Nội = 1) |
| COD vs prepaid | `MONEY_COLLECTION` = COD full amount only when paymentMethod is cod; 0 for prepaid |
| GHN hardcoded elsewhere | Don't let auto-progress logic overwrite VTP carrier data — guard `carrierType !== 'viettel_post'` |

## Files in volden-ops-web (reference implementation)

- `api/vtp.ts` — client: config (env→DB fallback), login token cache, address, create/query/cancel/print, status map
- `api/vtp-cache.ts` — 24h in-memory address cache
- `api/app.ts` — routes `/api/shipping/vtp/*` (status/config/provinces/districts/wards/services/create/query/cancel/print) + `/api/webhooks/vtp`
- `src/components/VtpOrderActions.tsx` — reusable "Lên đơn VTP" button (detail + compact modes)
- `src/components/SettingsModule.tsx` — VTP config UI (username/password/partnerCode/baseUrl/webhookSecret + test)
- `sql/2026-07-26_add_vtp_integration.sql` — order address IDs, vtpOrderNumber, weightGram on products

Env vars (leave blank for user to fill): `VTP_USERNAME`, `VTP_PASSWORD`, `VTP_PARTNER_CODE`, `VTP_BASE_URL`, `VTP_WEBHOOK_SECRET`. Credentials from https://partner2.viettelpost.vn.
