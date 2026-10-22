# Discount mode exclusive — bản đồ + trạng thái implement (2026-08-11)

Card: `[FEAT] Đơn hàng cần chọn CK theo sản phẩm hoặc theo cả đơn` (Trello CzGIZ3eB). **ĐÃ IMPLEMENT: commit `edda69f` + push main + SQL `2026-08-11_add_order_discount_mode.sql` applied. Card → Testing 11/08.**

## Vấn đề gốc

Form đơn hàng có 2 tầng chiết khấu, trước đây bị **cộng dồn**:
- **CK theo sản phẩm**: từng dòng `formItems[].discountType` / `discountValue` (UI: OrdersModule.tsx ~2210-2238)
- **CK cả đơn**: `discountType` / `discountValue` state chung (OrdersModule.tsx:157-158, UI ~2440-2468)

Tổng tiền = item discount trừ trước → `afterItemDiscount`, rồi order discount trừ TIẾP lên số đó (2 tầng chồng nhau).

## Quyết định user chốt (quan trọng — khác plan đầu)

1. **Người dùng tự chốt bằng việc nhập** (không default ép): nhập CK sản phẩm > 0 → **reset CK cả đơn về 0**; nhập CK cả đơn > 0 → **reset TOÀN BỘ CK từng sản phẩm về 0**. Đối xứng, KHÔNG disable-giữ-giá-trị (plan đầu đề xuất disable — user bác).
2. **Đơn cũ** (`discount_mode` NULL): **giữ hành vi cũ cộng dồn** (phương án A — không đụng data cũ, không lệch tiền đã lưu).
3. **Quotes KHÔNG gói** vào feature này.
4. Áp dụng cho **cả tạo đơn mới lẫn inline sửa đơn**.
5. Invariant bắt buộc: `subtotal − tổng CK = total phải trả`, khớp từng đồng (test trước khi commit).

## Thiết kế cuối

- **Schema**: `orders.discount_mode TEXT` — `'item' | 'order' | NULL` (NULL = đơn cũ → legacy cộng dồn).
- **Helper frontend (NƠI DUY NHẤT tính tổng)** — `src/lib/safeMath.ts`:
  - `resolveDiscountMode(mode)` → `'item' | 'order' | 'legacy'` (null/undefined → legacy)
  - `calcOrderTotal(items, order, mode)` → `{ rawSubtotal, itemDiscountSum, afterItemDisc, orderDiscVal, total }`
  - Mode `item`: `orderDiscVal=0`. Mode `order`: `itemDiscountSum=0`, order CK tính trên `rawSubtotal` (KHÔNG trên afterItemDisc). Legacy: cộng dồn như cũ.
- **Backend** `api/sales-policy/engine.ts`:
  - `calculateManualOrderTotal(items, orderDiscountType, orderDiscountValue, discountMode)` — thêm param thứ 4
  - `executeEngine(..., orderDiscountType, orderDiscountValue, discountMode)` — thêm param thứ 8
  - Block tính `customerVisibleTotal` (~375-397): mode 'order' → bỏ qua CK dòng trong `discountedSubtotal`; mode 'item' → `orderDiscount = 0`.
- **API** `api/app.ts`:
  - `POST /api/orders` + `POST /api/orders/calculate`: destructure `discount_mode`, truyền vào `executeEngine`, lưu `discount_mode: discount_mode || null`
  - `PUT /api/orders/:id`: nhận `discountType`/`discountValue`/`discount_mode` (inline edit)
- **UI** `src/components/OrdersModule.tsx`:
  - Selector pill "Theo SP / Cả đơn" cạnh ô Chiết khấu (form tạo đơn)
  - Order-level input onChange: `v>0` → `setDiscountMode('order')` + reset hết `formItems[].discountValue=0`
  - Item-level input onChange: `v>0` → `setDiscountMode('item')` + `setDiscountValue(0)`
  - Inline edit save: `hasItemDisc = editedItems.some(it => discountValue>0)` → body thêm `discount_mode:'item', discountValue:0`; ngược lại nếu order có CK → `discount_mode:'order'`
  - TẤT CẢ block hiển thị tổng (detail desktop/mobile, invoice, PaymentSplitSummary, QR block, card view, list view) chuyển sang `calcOrderTotal(paidItems, order, resolveDiscountMode(order.discount_mode))` — bỏ tính inline cũ

## Các chỗ tính cũ (đã thay bằng calcOrderTotal — ghi nhận để grep khi sửa sau này)

**Backend:** engine.ts `calculateManualOrderTotal` (:198) gọi ở :233 + :253; block `customerVisibleTotal` ~375-397; app.ts `POST /api/orders` :2570, `POST /api/orders/calculate` :2788. Quotes (:1463) KHÔNG đụng.

**Frontend OrdersModule (7+ chỗ cũ tính inline):** 1107-1140, 1211-1248, 1605-1657, 1713-1747 (2 chỗ detail), card view ~2738, list view ~2960. **Khi sửa discount, grep `discountValue || 0` toàn file để bắt block còn sót.**

**Không đụng:** `PublicOrderView.tsx` (đọc `customer_visible_total` đã lưu, data đã exclusive nên hiển thị đúng), `QuotesModule.tsx` (ngoài scope).

## Verify đã chạy (2026-08-11)

- Frontend helper: 25/25 PASS (mode item/order/fixed/legacy + invariant subtotal−CK=total + resolveDiscountMode mapping)
- Backend engine: 9/9 PASS (`executeEngine` segment null, từng mode, invariant)
- SQL: apply OK + select/insert/delete test row `discount_mode` OK
- Build: vite PASS + esbuild backend OK

## Pitfall tooling gặp khi làm

- `search_files` (rg) IO error trên path chứa space `D:/Hermes Proj/...` → dùng `grep -rn 'pattern' api/ src/` trong terminal
- Terminal grep pattern chứa nháy kép → hardline block → dùng nháy đơn + substring ngắn
- Có file dirty của dev khác (`.gitignore`, `agents.md`, `opencode.json`) → `git add` CHỈ các file feature, đừng commit chung
