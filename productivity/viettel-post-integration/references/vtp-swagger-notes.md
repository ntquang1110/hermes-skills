# Viettel Post API — Swagger Notes (partnerdev.viettelpost.vn)

Retrieved 2026-07-26 from `https://partnerdev.viettelpost.vn/v2/v2/api-docs`. Host: `partnerdev.viettelpost.vn`, basePath `/v2`, swagger 2.0, title "Viettelpost - Tài liệu API".

## Auth model

- All endpoints take a **`Token` header** — "Partner token, get from login API".
- `LoginForm` body: `PARTNER_CODE`, `PASSWORD`, `USERNAME` (+ optional `roles: RoleForm[]`).
- Older pattern: `GET /core/create-token?token=...` (also passes `Token` header).

## Controller → endpoint inventory

### categories-controller (all GET unless noted)
| Endpoint | Required params |
|----------|----------------|
| `/categories/checkAddressWarning` | wardId |
| `/categories/districtByIdAndProvince` | districtId, provinceById |
| `/categories/listBuuCucVTP` | — |
| `/categories/listDistrict` | provinceId |
| `/categories/listNational` | — |
| `/categories/listProvince` | — |
| `/categories/listProvinceById` | provinceId |
| `/categories/listProvinceNew` | — |
| `/categories/listService` (**POST**, body `DrafForm`) | — |
| `/categories/listServiceExtra` | serviceCode |
| `/categories/listWards` | districtId |
| `/categories/listWardsInternal` | districtId |
| `/categories/listWardsNew` | provinceId |
| `/categories/nationalById` | nationalId |
| `/categories/provinceById` | provinceById |
| `/categories/wardByDistrictAndId` | districtId, wardsId |

### core-controller
| Endpoint | Method | Notes |
|----------|--------|-------|
| `/core/create-token` | GET | token param |
| `/core/orders/save` | POST | body `OrderSaveForm`, query `edit` (boolean, required) |
| `/core/orders/query` | GET | code param |
| `/core/orders/query-customer` | GET | code + order params |
| `/core/list-bill-vtp` | GET | fromDate, toDate |
| `/core/complaint-detail`, `/core/create-complaint`, `/core/list-complaint` | GET/POST | complaints |
| `/core/list-payments/{start}/{end}` | GET | + status |
| `/core/off/*` | GET/POST | group bills |
| `/order/**` | OPTIONS | CORS preflight |

### order-controller (legacy surface, also present)
`/order/**` routes exist but the `/core/orders/*` + `/v2` surface is the one to target.

## Key DTOs (field names are UPPERCASE in JSON)

### OrderAIForm (create order)
- `ORDER_NUMBER`, `ORDER_TYPE`, `ORDER_SERVICE`, `ORDER_SERVICE_ADD`, `ORDER_NOTE`
- `SENDER_FULLNAME`, `SENDER_PHONE`, `SENDER_ADDRESS`, `SENDER_PROVINCE`, `SENDER_DISTRICT`, `SENDER_WARD`
- `RECEIVER_FULLNAME`, `RECEIVER_PHONE`, `RECEIVER_ADDRESS`, `RECEIVER_PROVINCE`, `RECEIVER_DISTRICT`, `RECEIVER_WARD`
- `PRODUCT_NAME`, `PRODUCT_DESCRIPTION`, `PRODUCT_QUANTITY`, `PRODUCT_WEIGHT`, `PRODUCT_PRICE`, `PRODUCT_TYPE`, `PRODUCT_DETAIL[]`
- `MONEY_COLLECTION`, `MONEY_TOTAL`, `MONEY_TOTALFEE`, `EXTRA_MONEY`, `UNLIMIT_COD`, `IS_COD_AUTO`
- `PICKUP_DATE`, `DELIVERY_DATE`, `DELIVERY_CODE`, `PICKUP_CODE`
- `GROUPADDRESS_ID`, `CUS_ID`, `RETURN_ADDRESS` (AddressInputForm), `VERIFICATION_CODE`
- `TOKEN` (string, legacy)

### OrderItem
- `ORDER_NUMBER`, `ORDER_NUMBER_ITEM`, `PRODUCT_NAME`, `PRODUCT_PRICE`, `PRODUCT_QUANTITY`, `PRODUCT_TYPE`, `PRODUCT_WEIGHT`

### AddressInputForm
- `PROVINCE_ID`, `DISTRICT_ID`, `WARDS_ID`, `ADDRESS`, `REQUIRED` (booleans) — confirms address IDs are integers

### CustomerForm (B2C surface)
- `name`, `phone`, `address`, `provinceId`, `districtId`, `wardsId` (camelCase here — watch which DTO family you use)

### B2COrderForm (alternative B2C create)
- `orderNumber`, `orderNote`, `orderPayment`, `moneyColletion`, `serviceCode`, `extendServiceCode`, `inventoryCode`, `listProduct[]` (B2cProductForm: productName, quantity, price, weight, length, width, height), `receiverInfo` (CustomerForm), `productTypeArray`

### Response shapes
- Standard wrapper: `ResponseEntity` (`body`, `statusCode`).
- Typed wrappers: `ResData«T»` → `{ data, error (bool), message, status (int) }`.
- `WebhookData`: `{ description, order_number, status }` — shape of pushed status events.
- `PostData`: `{ DATA, TOKEN, URL_WEBHOOK, SECRET_WEBHOOK }` — webhook registration payload.
- `PriceResponse`: `{ KPI, PRICE, SERVICE_CODE, SERVICE_NAME }` — from listPrice.
- `PrintForm` / `PrintFormV2`: `ORDER_ARRAY[]` + `PRINT_TOKEN` / `EXPIRY_TIME` — label printing.

## Notes for implementation

- Save the Swagger JSON (`curl https://partnerdev.viettelpost.vn/v2/v2/api-docs > vtp-swagger.json`) into the project for offline DTO reference.
- Orders created via `/core/orders/save` return VTP's waybill `ORDER_NUMBER` → persist to the order's tracking field.
- Webhook registration via `PostData` means the app must expose a public endpoint + verify `SECRET_WEBHOOK`.
- Sandbox (`partnerdev`) and prod (`api.viettelpost.vn`) both use basePath `/v2`; switch only the host via `VTP_BASE_URL`.
