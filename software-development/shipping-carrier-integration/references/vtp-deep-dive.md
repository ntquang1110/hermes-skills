# VTP Deep-Dive — triển khai 2026-07-26 trong volden-ops-web

Chi tiết triển khai thực tế, dùng khi tiếp tục (test sandbox thật, thêm 247/GHN, fix webhook).

## Files đã tạo

| File | Vai trò |
|------|---------|
| `api/vtp.ts` | Client: getVtpConfig (env → settings DB fallback), getVtpToken (cache 55p), listProvinces/Districts/Wards, listServices, createVtpOrder, queryVtpOrder, cancelVtpOrder, printVtpOrders, mapVtpStatus, vtpStatusName |
| `api/vtp-cache.ts` | Cache in-memory 24h cho province/district/ward |
| `api/address-format.ts` | StandardAddress + toVtpAddress + toGhnAddress/toExpress247Address (placeholder throw) + isVtpAddressComplete |
| `api/app.ts` | 10 routes `/api/shipping/vtp/*` + webhook `/api/webhooks/vtp` + fix GHN hardcode |
| `src/components/VtpOrderActions.tsx` | Nút lên đơn/sync/in tem/tracking (compact + full mode) |
| `src/components/SettingsModule.tsx` | Form VTP credentials + Test connection |
| `src/components/erp/pages/ErpInventoryPage.tsx` | Kho: address + sender fields |
| `sql/2026-07-26_add_vtp_integration.sql` | orders: shippingProvinceId/DistrictId/WardId, vtpOrderNumber, vtpMoneyCollection, vtpShippingFee, vtpLastSyncAt, vtpError, vtpServiceCode; products: weightGram |
| `sql/2026-07-26_add_warehouse_address_sender.sql` | warehouses: address/province/district/ward + ID + senderName/senderPhone + seed 3 kho |

## Flow create order (chi tiết)

1. `POST /api/shipping/vtp/create {orderId}` (admin only)
2. Check order tồn tại + chưa có vtpOrderNumber
3. Load warehouse từ `order.warehouse` → sender = warehouse fields
4. Validate sender đủ (name/phone + 3 IDs) → lỗi rõ ràng nếu thiếu
5. Items → productName (join, slice 200), productQuantity (sum qty), productWeight (weightGram × qty, fallback 5000g)
6. moneyCollection = total nếu cod, 0 nếu prepaid
7. createVtpOrder → parse ORDER_NUMBER + MONEY_TOTALFEE
8. Update order: vtpOrderNumber, carrierName="Viettel Post", carrierType, shippingStatus="pending", trackingUrl, stage (reported_warehouse→shipping_booked)
9. Lỗi → lưu vtpError (JSON slice 500) để debug

## Env cần user điền (sandbox trước)

```
VTP_USERNAME=      # từ partner2.viettelpost.vn
VTP_PASSWORD=
VTP_PARTNER_CODE=
VTP_BASE_URL=      # trống = partnerdev.viettelpost.vn (sandbox); prod = https://api.viettelpost.vn
VTP_WEBHOOK_SECRET=
```

## Test plan (khi có credentials)

1. `GET /api/shipping/vtp/status` → configured=true, connected=true
2. `GET /api/shipping/vtp/provinces` → list cache
3. Chọn tỉnh/huyện/xã → set order shippingProvinceId/DistrictId/WardId
4. Cấu hình kho sender → `POST /api/shipping/vtp/create` → vtpOrderNumber
5. Query status → shippingStatus mapping đúng
6. Webhook giả lập POST /api/webhooks/vtp với ORDER_STATUS → stage cập nhật
7. Print tem (optional)

## Ghi chú fix khác cùng sprint

- BUG-2 retail auto-approve: segment null → autoApproved=true (db.ts resolveSegmentAndPolicy + engine.ts 2 return sớm)
- BUG-3 "Order does not need approval": approve route chấp nhận stage pending_approval/order_pending
- FEAT-5 auto-match: webhook bank → autoMatchTransactionToOrder (content chứa order id/8 ký tự/publicToken + đủ tiền → confirm + finalize)
- FEAT-7 auto export: RPC create_export_stock_order khi order → reported_warehouse
- Branch merge: fix/order-approval-route-status-note (UI pending_approval) + fix/checkin-bank-match-bugs (normalizeCheckinTimeStatus + confirm_payment array) — đều đã merge main, verify test sau merge PASS
