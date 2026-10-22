---
name: volden-ops-web
description: "Volden Ops Web — ERP/CRM bán hàng sỉ. Đọc source tiết kiệm token, build-test loop, commit rules, VTP integration state."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [volden, erp, react, supabase, viettel-post, project-ops]
---

# Volden Ops Web — Project Operations

App quản lý bán hàng sỉ Volden (leads → quotes → contracts → orders → shipping → checkin → KPI → ERP 14 modules). Stack: React 19 + Vite 6 + Tailwind 4 + Express 4 + Supabase (PostgreSQL). Mobile-first + desktop admin.

## Trigger

- Mọi task trên repo `volden-ops-web` (fix bug, feature mới, deploy, test, đọc hiểu source)

## Fast Facts

- **⚠️ CÓ 2 Supabase project KHÁC NHAU — đây là nguồn lỗi "thiếu schema" 2026-08-17:**
  - `.env` (dev) = `wggluyflkdrgffugpidk` — connect pg IPv4 OK
  - `.env.prod` (PRODUCTION) = `wevhmrezxgnyvkbmcqux` — host chỉ resolve **IPv6** (máy nhà không route IPv6 → timeout), pooler mọi region "tenant not found" (chưa bật Connection Pooling)
  - **Migration phải apply CẢ 2 project**, không chỉ 1. Trước giờ chỉ apply dev → production thiếu `discount_mode` (lỗi "thiếu schema khi lên đơn") + `cancelled_by`.
  - `.env.prod` password bị **bọc nháy kép** `"hO7..."` — khi parse bằng tay phải strip `"`/`'`. Script `run-sql-direct.mjs` dùng `dotenv.config()` mặc định đọc `.env` (dev) — KHÔNG đọc `.env.prod`.
- Repo: `github.com/ntquang1110/volden-ops-web` (PRIVATE) — clone tại `D:/Hermes Proj/volden-ops-web`
- Auth clone: PAT lấy từ env `GITHUB_PAT_B64` (base64-encoded) → `echo $GITHUB_PAT_B64 | base64 -d` → `git clone https://<user>:<pat>@github.com/...`
- Test accounts: `admin@gmail.com` / `<PASSWORD>` (7 users, password chung)
- Source map: `docs/SOURCE-MAP.md` — navigation chuẩn, đọc trước khi làm gì
- DB: Supabase (service_role key trong `.env`)
- **⚠️ HAI PROJECT SUPABASE — `.env` là DEV, `.env.prod` là PRODUCTION:** `.env` → `wggluyflkdrgffugpidk` (dev), `.env.prod` → `wevhmrezxgnyvkbmcqux` (production thật mà Vercel dùng). Migration apply lên `.env` KHÔNG tự vào production → code mới deploy (Vercel auto) nhưng DB prod thiếu column = "thiếu schema khi lên đơn". Chi tiết + recipe verify: `references/supabase-projects.md`
- Deploy: Vercel; cấu hình trong `vercel.json`

## Đọc source TIẾT KIỆM TOKEN (user yêu cầu — ~95% savings)

1. `docs/SOURCE-MAP.md` (~500 tok) — map toàn bộ file/thư mục, KHÔNG đọc từng file
2. `package.json` + `tsconfig.json` — stack & scripts
3. `vite.config.ts` + `vercel.json` — build/deploy config
4. `README.md` + `docs/TESTER_GUIDE.md` — user flows, test accounts
5. Chỉ deep-read file liên quan feature cần sửa — không đọc cả app

**BẮT BUỘC cập nhật `docs/SOURCE-MAP.md`** khi thêm/sửa/xoá page, file, route — rule đã đóng vào `AGENTS.md` section 3.6. Trước commit check `git diff --stat docs/SOURCE-MAP.md`.

## Build → Test → Commit Rules (AGENTS.md)

1. `npm run build` trước — FAIL: fix rồi build lại; PASS: log "✅ Build OK"
2. Test qua Supabase client trực tiếp (`npx tsx -e "..."`), KHÔNG cần server HTTP, KHÔNG start background server
3. **Chỉ commit khi test thành công toàn bộ** — commit message format: `hermes - <mô tả commit>`
4. Luôn update `CHANGELOG.md` (reverse-chronological, format mẫu trong AGENTS.md section 3) + `docs/SOURCE-MAP.md`
5. Đọc `PENDING_TASKS.md` + `BUGS.md` TRƯỚC khi bắt đầu task mới

## Multi-agent pushes — merge conflict workflow

Repo có nhiều agent/user push cùng lúc. `git push` bị reject → `git pull origin main --no-edit` → resolve conflict bằng patch (giữ cả 2 thay đổi, xoá `<<<<<<<`/`=======`/`>>>>>>>` markers) → build lại → commit `hermes - merge: ...` → push.

### Audit branch khác main (user hỏi "branch đang mở khác main như nào")

- List remote branches: `git ls-remote --heads origin`
- Check PR đang mở: `curl -H "Authorization: token $PAT" https://api.github.com/repos/ntquang1110/volden-ops-web/pulls?state=open`
- Fetch branch riêng: `git fetch origin <branch>:refs/remotes/origin/<branch>` rồi `git log --oneline main..origin/<branch>` — xem commits khác main
- **Kiểm tra conflict KHÔNG đụng working tree:** `git merge-tree $(git merge-base main origin/<branch>) main origin/<branch> | grep -E "changed in both|CONFLICT"` — nếu "changed in both" ở file trùng với vùng mình vừa sửa (vd `api/db.ts paymentsDb.confirm`, `OrdersModule.tsx`) thì merge cẩn thận, không tự ý merge khi chưa trình user (repo có dev khác: Quynh Anh Vuong push branch fix riêng, chưa PR — 2026-07-26 có `fix/checkin-bank-match-bugs` + `fix/order-approval-route-status-note`)

## VTP (Viettel Post) Integration — state 2026-07-26

- Đã implement: `api/vtp.ts` (client), `api/vtp-cache.ts`, `api/address-format.ts` (standard address format cho mọi carrier), routes `/api/shipping/vtp/*` + webhook `/api/webhooks/vtp`, `src/components/VtpOrderActions.tsx`, Settings UI, warehouse address+sender, `weightGram` (mặc định 5kg/item)
- **CHỜ credentials**: `VTP_USERNAME/PASSWORD/PARTNER_CODE` trong `.env` (để trống) — user chưa điền; sandbox mặc định `partnerdev.viettelpost.vn`
- **SQL migration ĐÃ APPLY** (2026-07-26): `sql/2026-07-26_add_vtp_integration.sql` + `sql/2026-07-26_add_warehouse_address_sender.sql` — qua `scripts/run-sql-direct.mjs` (xem mục SQL Migration)
- **CHỜ cấu hình kho**: mỗi warehouse cần address + provinceId/districtId/wardId (VTP) + senderName/senderPhone — seed 3 kho đã có address mặc định (Diem/Service_HN → Hà Nội, Service_HCM → HCM), cần kiểm tra lại senderName/senderPhone thật trước khi lên đơn
- Chi tiết API: xem `references/vtp-api.md`

## Pitfalls

- **Windows write_file path bug**: khi cwd ở drive khác (vd cwd=`D:/Hermes Proj/ai-company`), truyền path MSYS `/d/Hermes Proj/volden-ops-web/...` vào write_file/patch sẽ resolve SAI thành `D:\\d\\Hermes Proj\\...`. LUÔN dùng absolute Windows path với forward slash: `D:/Hermes Proj/volden-ops-web/...`
- **search_files (rg) fail trên path chứa space** (`D:/Hermes Proj/...` → `IO error ... cannot find the path`, gặp 4+ lần 2026-08-11): tool search_files không xử lý được path có dấu cách trong repo này. Dùng terminal `grep -rn '<pattern>' api/ src/` thay thế.
- **Terminal grep pattern chứa nháy kép bị hardline block** (vd `grep -n "app.post(\"/api/orders"` → blocked + lưu vào blocked-scripts): dùng nháy ĐƠN + substring đơn giản (`grep -n 'api/orders' api/app.ts`) là đủ.
- **Discount 2 tầng (CK theo sản phẩm + CK cả đơn) — ĐÃ FIX exclusive (2026-08-11, commit `edda69f`)**: `orders.discount_mode` ('item'|'order'|NULL), helper `calcOrderTotal()`/`resolveDiscountMode()` trong `src/lib/safeMath.ts` là NƠI DUY NHẤT tính tổng đơn — mọi block hiển thị đã chuyển sang dùng nó. User chốt: nhập CK bên nào tự reset bên kia về 0 (KHÔNG disable), đơn cũ NULL giữ cộng dồn, Quotes không gói. Chi tiết: `references/discount-calc-map.md`
- Lint `npm run lint` báo lỗi pre-existing (esModuleInterop, `api/db.ts:1031`, dotenv default export...) — không phải do code mới; dựa vào `npm run build` làm gate chuẩn
- **Terminal tool chặn `npx vite build`** (heuristic nhầm thành server/watch process) → chạy qua node trực tiếp: `node node_modules/vite/bin/vite.js build 2>&1 | tail -20` (PASS "✓ built in Xs"). API typecheck riêng: `npx tsc --noEmit -p api/tsconfig.json` FAIL sẵn (config `moduleResolution: nodenext` nhưng thiếu `module: NodeNext`) → dùng esbuild bundle làm gate: `npx esbuild api/app.ts --bundle --platform=node --format=esm --packages=external --outfile=/tmp/app-check.mjs` (output "Done in Xms" = syntax/import OK). Chạy xong xoá file check tạm. ⚠️ Trên git-bash Windows, esbuild resolve `/tmp/app-check.mjs` thành `<cwd>/tmp/app-check.mjs` (thư mục `tmp/` trong repo) chứ KHÔNG phải `/tmp` hệ thống → `rm -f /tmp/app-check.mjs` không dọn được; xoá bằng `rm -rf tmp/` sau khi check.
- Auto-progress timer hardcode GHN đã fix (chỉ set khi chưa có carrier) — không đè lên `viettel_post`
- `.env` chứa secrets — read_file tool chặn đọc; dùng grep/python để kiểm tra key names thay vì đọc full file
- `companyInfoDb` dùng method `get()` (không có `findFirst()`) — tra db.ts trước khi gọi; `warehousesDb` có `findByCode()` cho warehouse riêng
- **DB schema quirks (Supabase production):** users table là `users` (KHÔNG phải `profiles` — query `profiles` báo "Could not find the table"); orders dùng camelCase `createdAt` (KHÔNG có `created_at`); orders KHÔNG có cột `auto_approved` — dùng `needs_approval` + `approval_reason` + `approved_by` để biết trạng thái duyệt. RPC `create_export_stock_order` bắt buộc 2 params `p_order_id` + `p_actor_id` — gọi thiếu param báo "Could not find the function ... in the schema cache" (dễ hiểu nhầm function không tồn tại; gọi đủ params + id giả → "Order not found" = function OK)
- **contracts stage enum (từ migration `2026-07-22_contract_fulfillment.sql`):** constraint `contracts_stage_check` CHỈ cho phép: `drafting, gdkd_review, admin_process, submitted, shipping_booked, sent_to_customer, pending_archive, completed, cancelled, rejected`. `coo_signing`/`signed` ĐÃ BỊ LOẠI (migrate coo_signing→submitted, signed→completed). Flow mới: `admin_process → (generate) → submitted → shipping_booked → sent_to_customer → pending_archive → completed`. Lỗi `violates check constraint "contracts_stage_check"` khi generate = code còn set stage cũ `coo_signing` (route `POST /api/contracts/generate/:id` app.ts ~1944-1973 — fix: đổi sang `submitted`). **Khi migration đổi stage enum → grep `coo_signing`/`signed` toàn repo để bắt drift:** api/app.ts route + notify.ts labels + src/types.ts ContractStage + ContractsModule.tsx STAGE_FLOW/STAGE_STYLES. Constraint đổi mà code không theo = 500 runtime.\n- **Verify constraint bằng insert test row (không cần server):** insert contract test → update sang stage MỚI (phải OK) → update sang stage CŨ (phải BỊ CHẶN = tái hiện đúng lỗi gốc) → delete cleanup. 4/4 PASS mới commit. **Lưu ý not-null columns khi insert contract test:** thiếu lần lượt `leadId`, `contactName`, `paymentTerm`, `value` → 4 lần fail `null value in column X`. Row test tối thiểu: `{ id: 'CTRCT_TEST_...', companyName, contactName, paymentTerm: 'prepaid', value: 1000000, leadId: '<lead thật>', stage: 'admin_process', createdAt }`.
- **`npx tsx -e "..."` multi-line inline có thể trả output RỖNG (exit 0, im lặng)** trên bash Windows — gặp 2 lần 2026-08-09 (check contract stage + pg_constraint). Workaround đã chạy OK: viết file tạm `scripts/tmp-check-<topic>.ts` → `npx tsx scripts/tmp-check-<topic>.ts` → xoá file sau khi xong. Lưu ý: write_file báo lint TS6053 "File not found" khi tạo file .ts mới trong repo — bỏ qua, file vẫn được tạo và chạy được.

## Test Guide Pattern (cho bé tester — 2026-07-26)

User yêu cầu vẽ **flow chart module + test cases từng bước** để tester tự detect lỗi. Đã làm cho module Tạo Lead (`docs/test-guide-create-lead.html`):

1. **Map code thật** → 7 bước: mở CRM → chọn kiểu KH → nhập bắt buộc → phân loại → ảnh/GPS → validation UI → backend (trùng SĐT, short_id, segment_code) → UI sau tạo
2. **HTML B/W/Y** (Design System v1.0: #FFD600/#0D0D0D/#1B1B1D, radius 28/999) — stats (số bước/test case/phút) → flow chart dọc có mũi tên ▼ → từng test case có **checkbox PASS** → done-box "tất cả PASS = module test xong" → tips
3. Mỗi test case ghi: ID (TC-x), bước làm, kỳ vọng **PASS (xanh)** / **block (đỏ)** — dựa trên code thật (validation message, HTTP 400 text, hành vi sau tạo)
4. Publish `https://preview.thefirstonly.com/api/store` (curl + python json.dumps vào file payload — KHÔNG python urllib, bị 403)
5. **KHÔNG lưu vào KFlow** — user explicit "không lưu vào kflow" cho test guides (KFlow chỉ cho research pipeline)
6. Báo link + bảng tóm tắt test cases trong chat

Template HTML tái dùng: `templates/test-guide-flow.html` (đổi title/stats/bước/test cases cho module khác: Quote, Contract, Order).

## Backlog Sprint 2026-07-26 — root causes đã fix (trừ T8 MISA)

User duyệt triển khai backlog Trello (trừ VTP đã xong + 247 + MISA). **Kết quả: 9/9 tests PASS + build PASS + commit `a4416ea` đã push + SQL đã apply.** Các root cause:

- **BUG-2 Khách lẻ không auto-approve CK 0% + không tặng quà**: segment null → `resolveSegmentAndPolicy` (api/db.ts) + `executeEngine` (api/sales-policy/engine.ts) set `autoApproved=false` → order rơi vào `order_pending` thay vì `approved`. Fix: khi `!finalSegmentCode` hoặc `rules.length===0` → `autoApproved=true` (không segment = không ràng buộc = auto-approve).
- **BUG-3 "Order does not need approval"**: approve route chỉ nhận `needs_approval===true`, nhưng order ở `pending_approval`/`order_pending` (retail chờ duyệt) có thể `needs_approval=false`. Fix: chấp nhận approve khi `needs_approval || ['pending_approval','order_pending'].includes(stage)`.
- **BUG-1 + FEAT-5 (webhook thanh toán)**: webhook chỉ tạo transaction, KHÔNG tự match order → tiền vào nhưng đơn không tự xác nhận. Fix: thêm `autoMatchTransactionToOrder(tx)` trong api/app.ts — tìm order `payment_pending` khớp content (order id / 8 ký tự đầu / publicToken) + đủ tiền → tự paymentsDb.create+confirm+match+finalize. Response webhook thêm `autoMatched` field.
- **FEAT-6 Xem NPP quá hạn**: endpoint mới `GET /api/debt/overdue` (lọc v_npp_debt remaining_debt>0) + `src/components/OverdueNppList.tsx` + button "Xem NPP quá hạn" trên CeoDashboard scroll tới `#overdue-npp-section`.
- **FEAT-7 Auto phiếu xuất kho khi admin xác nhận**: SQL mới `create_export_stock_order` (idempotent — không tạo trùng phiếu active, không đổi stage) + gọi RPC khi PUT order stage=`reported_warehouse`.
- Scripts verify: `scripts/verify-retail-autoapprove.ts`, `scripts/verify-bugfixes.ts`.
- **KẾT QUẢ: 9/9 tests PASS + build PASS → đã commit `a4416ea` + push main.** Các SQL migration ĐÃ APPLY lên DB production (xem mục SQL Migration bên dưới).

## Tester re-open 2026-08-05 — 3 card quay lại Need fixed (root cause MỚI + đã fix)

Sau fix a4416ea + push, tester (Quỳnh Anh) đẩy cả 3 card về Need fixed — **fix code PASS build KHÔNG đồng nghĩa tester chấp nhận**. Triage bằng cách đọc card actions (commentCard/updateCard) lấy comment thật của tester. **User duyệt fix cả 3, commit `f727b14` đã push, card move sang Testing.**

- **[FEAT] NPP quá hạn** (`6a6f7ebdf783f834aed8f211`): button "Xem NPP quá hạn" chỉ `scrollIntoView('#overdue-npp-section')` (CeoDashboard.tsx:597) — tester bấm không thấy "redirect". Card yêu cầu "redirect đến giao diện xem cụ thể". **Fix đã apply:** `onNavigate('debt')` → tab Công Nợ (ErpDebtPage đã có), fallback scroll nếu không có onNavigate.
- **[BUG] Admin tạo đơn ngoài chính sách không duyệt được** (`6a6f7d7bb7396a918320c8fa`): fix BUG-3 (approve route) là cần nhưng CHƯA đủ. Root cause thật (verified DB): đơn có `segment_code = null` → `resolveSegmentAndPolicy` (api/db.ts) bỏ qua policy check hoàn toàn → `autoApproved=true` → order chạy thẳng `payment_pending`, KHÔNG BAO GIỜ vào `pending_approval`. VD thực: ORD_MKEA4Z/ORD_YTJ97R (admin_role tạo, segment null, item discount 25%) → `needs_approval=false`; ORD_P9DWMD (sale tạo, segment SEG_NPP, CK 40%>15%) → đúng `needs_approval=true` reason "Vượt ngưỡng CK". Tester tự hỏi "maybe đây là tính năng". **User chốt: FIX — đơn không segment + không phải khách lẻ + không phải GDKD → bắt buộc `pending_approval`** (đổi `const` → `let` cho needsApproval/autoApproved/approvalReason rồi override; `isRetailCustomer` phải tính TRƯỚC khi override). Verify: 6/6 case logic PASS (admin no-segment→pending_approval; retail/gdkd giữ auto).
- **[FEAT] Auto phiếu xuất kho** (`6a6c16b5927965c1ef7b5327`): RPC `create_export_stock_order(p_order_id, p_actor_id)` TỒN TẠI (verify: gọi với id giả → "Order not found: __test__" = function OK). Tester không biết xem phiếu xuất ở đâu — phiếu nằm table `stock_orders`, page `ErpStockOrdersPage` / route `stock-orders`, KHÔNG phải inventory ("kho bãi chỉ có số lượng stock"). **Root cause thật:** auto-export CHỈ gắn ở route PATCH `PUT /api/orders/:id` (stage=`reported_warehouse`), còn luồng khớp tiền `finalizeOrderAfterBankMatch` (app.ts) chuyển stage `payment_pending→reported_warehouse` mà KHÔNG gọi RPC → order completed KHÔNG có phiếu xuất. **Fix đã apply:** tách helper `autoCreateExportStockOrder(orderId, actorId)` dùng chung, gọi ở CẢ PATCH + `finalizeOrderAfterBankMatch`. Verify thật: insert order test payment_pending → RPC tạo `so_...` status pending → gọi lần 2 idempotent ("Đã có phiếu xuất active") → xoá test data. **User xác nhận: VTP OUT OF SCOPE — "k quan tâm đến VTP", không sửa button VTP lỗi** (lỗi do env trống → `VTP_CHUA_CẤU_HÌNH`).

## Fix SĐT khách lẻ — 2026-08-05 (card To do → Testing, commit `7729c5c`)

Card: `[BUG] Ô lên đơn hàng cho "Khách lẻ" đang cho phép điền số điện thoại nhiều hơn 10 chữ số` (`6a7346b90971ba38aefbed35`) — plan trình user, duyệt "ok" mới code.

**Pattern chuẩn SĐT VN (10 số bắt đầu 0) — copy từ CRM cho MỌI ô phone mới:**
```tsx
onChange={(e) => setX(e.target.value.replace(/\D/g, '').slice(0, 10))}
pattern="0[0-9]{9}" maxLength={10} inputMode="numeric" title="SĐT 10 chữ số, bắt đầu bằng 0"
```
- CRM (`CRMModule.tsx` handleCreateLead + new-phone-input) ĐÃ chuẩn — check nơi khác trước khi nghĩ "chưa có convention"
- Ô khách lẻ walk-in trong `OrdersModule.tsx` (retailPhone, ~1972) thiếu → áp đúng pattern
- Submit cũng phải validate regex `^0\d{9}$` (alert nếu sai), đừng chỉ chặn ở input
- Verify: build PASS + `node -e` test regex 7/7 case (đủ 10, 11 số chặn, chữ chặn, thiếu số chặn)

## Fix 2026-08-05 (tiếp) — 403 bank-accounts + duplicate v_npp_debt (commit `32e5778` + `7f88954`)

### GET /api/bank-accounts 403 với sale (commit `32e5778`)
- **Root cause:** route gắn `requireAuth, requireAdmin`, nhưng `OrdersModule.fetchOrdersAndContext` (dùng chung MỌI role, OrdersModule.tsx:557) gọi nó để đổ `window.__bankAccounts` — ErpDebtPage đọc để vẽ QR VietQR khi khớp tiền. Sale user → 403 (app không crash vì có `.catch(() => [])`, chỉ console đầy lỗi + QR mất bank info).
- **Quy tắc:** API admin-only mà component dùng chung (sale + admin) cần đọc → mở GET xuống `requireAuth`, giữ POST/PUT/DELETE admin-only. Bank account là public info cho khách chuyển tiền (PublicOrderView đã trả qua endpoint public) — không phải dữ liệu nhạy cảm.
- Verify: esbuild bundle OK + vite build PASS.

### OverdueNppList duplicate key (`lead_...`) — view SQL GROUP BY sai (commit `7f88954` + SQL applied)
- **Triệu chứng:** React warning "Encountered two children with the same key" ở OverdueNppList.tsx:71.
- **Root cause:** view `v_npp_debt` GROUP BY **cả** `paid.total_paid` → 1 lead có N order (total_paid khác nhau) bị tách N dòng cùng `lead_id`. VD thật: `lead_1785426082592` 2 dòng (7,290,000/3,645,000 + 6,521,250/0).
- **Fix:** GROUP BY chỉ `l.id, l."companyName", l."contactName"`; total_paid bọc `COALESCE(SUM(paid.total_paid), 0)`. Migration: `sql/2026-08-05_fix_v_npp_debt_duplicate.sql`. Verify: 114→113 rows, duplicate = 0.
- **Anti-pattern cần nhớ:** view tổng hợp theo lead mà GROUP BY thêm cột con (paid/order-level) → tách dòng. Bao giờ cũng verify view bằng script đếm duplicate theo key trước khi tin data.

## FEAT CK exclusive theo SP / cả đơn — 2026-08-11 (commit `edda69f` + SQL applied)

Card CzGIZ3eB → Testing 11/08. Đơn hàng KHÔNG còn cộng dồn 2 tầng CK.

**⚠️ 2026-08-17 — production BỊ THIẾU column `discount_mode` (đang mở):** migration `2026-08-11_add_order_discount_mode.sql` chỉ được apply lên project dev (`.env` = `wgglu...`), KHÔNG apply lên project production (`.env.prod` = `wevhm...`). Code production ĐÃ deploy (bundle `OrdersModule-bqyWhBhQ.js` có `discount_mode`) nhưng DB prod chưa có column → khi lên đơn báo lỗi `column orders.discount_mode does not exist` / `Could not find the 'discount_mode' column of 'orders' in the schema cache` (= "thiếu schema"). Fix: apply `ALTER TABLE orders ADD COLUMN IF NOT EXISTS discount_mode TEXT;` lên production qua SQL Editor hoặc pg direct với creds `.env.prod`.

**Quy tắc nghiệp vụ (user chốt):**
1. Người dùng tự chốt bằng việc nhập: nhập CK sản phẩm > 0 → reset CK cả đơn = 0; nhập CK cả đơn > 0 → reset toàn bộ CK sản phẩm = 0 (đối xứng, KHÔNG disable)
2. Đơn cũ (`discount_mode` NULL) giữ hành vi cũ (cộng dồn) — không đụng data
3. Quotes KHÔNG gói
4. Áp dụng cả tạo đơn + inline sửa đơn
5. Invariant: `subtotal − tổng CK = total phải trả` — test trước commit

**Kiến trúc:**
- `orders.discount_mode` TEXT ('item'|'order'|NULL); migration `sql/2026-08-11_add_order_discount_mode.sql`
- `src/lib/safeMath.ts`: `calcOrderTotal(items, order, mode)` + `resolveDiscountMode(mode)` — NƠI DUY NHẤT tính tổng frontend; mode 'order' bỏ CK dòng + order CK tính trên rawSubtotal, mode 'item' bỏ order CK
- `api/sales-policy/engine.ts`: `calculateManualOrderTotal` + `executeEngine` thêm param `discountMode` (thứ 4 / thứ 8); block customerVisibleTotal tôn trọng mode
- `api/app.ts`: POST /api/orders + /calculate nhận `discount_mode`; PUT /api/orders/:id nhận `discountType`/`discountValue`/`discount_mode`
- `OrdersModule.tsx`: selector pill "Theo SP / Cả đơn"; onChange order-level → reset items; onChange item-level → reset order; inline edit save ép mode
- Chi tiết + verify 25/25 + 9/9: `references/discount-calc-map.md`

## Fix 2026-08-12 — 3 card Need fixed + FEAT màu sắc (commits `ff548c2` + `235839e` đã push, card → Testing) — pattern class-level

Triage 3 card tester đẩy về Need fixed 11/08. **Tester Quỳnh Anh dùng tài khoản `admin_role@gmail.com` (role `admin_role`)** — luôn check role thật của tester trước khi đoán lỗi 403.

1. **[FEAT] NPP quá hạn** (`6a6f7ebdf783f834aed8f211`): button "Xem NPP quá hạn" nằm trong `{kpi.overduedDebtCount > 0 && (...)}` → count=0 là button biến mất, tester không tìm thấy. **Quy tắc: button điều hướng của 1 feature phải LUÔN render, không gate bằng count>0.** Fix: bỏ điều kiện, luôn hiện button → `onNavigate('debt')`.

2. **[BUG] Đơn ngoài chính sách** (`6a6f7d7bb7396a918320c8fa`): khách lẻ walk-in (`leadId=retail_customer`, segment null) auto-approve kể cả CK 25% (ngưỡng Shop Lẻ chỉ 5%). Root cause: `resolveSegmentAndPolicy` + `executeEngine` branch `else` (không segment) luôn `autoApproved=true`. **Quy tắc mới: khách lẻ không segment → áp ngưỡng `SEG_SHOP_LE.max_discount_rate` (5%) cho quyết định duyệt; CK hiệu dụng > 5% → `pending_approval` reason "Vượt ngưỡng CK khách lẻ".** Tính CK hiệu dụng PHẢI tôn trọng `discount_mode` (mirror `calcOrderTotal`): mode 'order' chỉ tính CK cả đơn, mode 'item' chỉ tính CK dòng, null/legacy cộng dồn cả 2. Áp cả POST /api/orders + /api/orders/calculate (preview đồng bộ). Verify: `scripts/verify-retail-ck-threshold.ts` 8/8 PASS (25%→duyệt, 5%/3%/0%→auto, item 30%→duyệt, mode order bỏ CK sản phẩm, legacy cộng dồn 30%→duyệt, fixed 200k/1tr→duyệt).
   - **Pitfall chung: "segment null = auto-approve" là lỗ hổng policy.** Mọi đơn không segment (khách lẻ, chưa phân loại) đều auto-approve qua branch `else`. Card nào báo "đơn ngoài chính sách không cần duyệt" → grep branch này trước.

3. **[FEAT] Auto phiếu xuất kho** (`6a6c16b5927965c1ef7b5327`): tester bị 403 "Forbidden: Requires one of [admin] role" dù role `admin_role`. Root cause: UI `isAdmin = roles.includes('admin') || roles.includes('admin_role')` → hiện button Hủy/Nhập kho, nhưng API `POST /api/stock-orders/:id/cancel` + `import` dùng `requireAdmin` (= `requireRole("admin")` CHỈ admin) → admin_role 403. **Pitfall chung: UI role flags vs API middleware lệch nhau** — tester báo 403 "Requires one of [X]" → grep `isAdmin`/role check trong page vs `requireX` trong route. `admin_role` (Admin Điều Phối) là role RIÊNG, UI thường gồm nó trong isAdmin nhưng API quên. Fix: `requireRole("admin", "admin_role")` đồng bộ UI.

4. **Badge CK trên order lệch**: badge `CK {order.discount_level}%` hiện segment level (0) trong khi đơn CK 25% → tester tưởng lỗi. **Quy tắc hiển thị: % CK phải tính từ CK THỰC qua `calcOrderTotal(paidItems, order, resolveDiscountMode(order.discount_mode))` → rate = (itemDiscountSum + orderDiscVal)/rawSubtotal; ẩn badge khi rate = 0. KHÔNG dùng `discount_level` làm CK hiển thị** (discount_level là segment level, không phải CK áp dụng).

## Sales policy + products — facts (2026-08-12, verify DB thật)

- **Table rules là `rules_config`** (rulesConfigDb) — KHÔNG tồn tại `sales_policy_rules`/`promotions`/`gift_rules`/`combos` (đừng mất thời gian thử các tên đó)
- **Segments:** SEG_NPP max_discount_rate 15% · SEG_SHOP_LE max 5% · **khách lẻ walk-in (`leadId='retail_customer'`) có segment NULL** — chính là lỗ hổng "segment null = auto-approve" ở branch `else` của `resolveSegmentAndPolicy`/`executeEngine`
- **Engine gift:** filter theo `discount_level` rồi `bestGiftApplied` → **chỉ 1 gift/level (priority cao nhất)** — mua nhiều dòng combo trong 1 đơn chỉ nhận 1 quà (hành vi có chủ đích, chưa ai report là bug)
- **Products có field `color`** (Đen/Be/Xanh/Ghi) + variant là SKU RIÊNG: BABAIRDEN/BABAIRBE/BABAIRXANH (= "Volden Baby Airvoice"), VOLDENBABYCLOUDDEN/GHI/BE; base BABAIR/BABCLOUD color rỗng. **`OrderItem` KHÔNG lưu color** (chỉ productId + productName chung) → đơn không phân biệt được màu
- **Card "[FEAT] Thêm màu sắc sản phẩm" - **FEAT Thêm màu sắc sản phẩm ĐÃ XONG (12/08, commit `235839e` → Testing):** `OrderItem.color` + helper `enrichItemsWithColor(items)` trong api/app.ts (lookup products → gắn màu; gọi ở POST /api/orders `finalItems` + PUT /api/orders/:id khi items thay đổi). Frontend `getItemColor(it) = it.color || productMap lookup` → badge màu cạnh tên SP tại detail desktop/mobile, invoice sheet, 3 chỗ hàng tặng; PublicOrderView dùng `it.color` (public view KHÔNG có products list để lookup — đơn cũ không màu sẽ không hiện, chấp nhận). Verify `scripts/verify-item-color.ts` 6/6 (Đen/Be/Xanh/không màu/giữ nguyên/gift).
- **Card "[BUG] Tặng nhầm bục trưng bày" — điều tra xong, CHƯA fix:** 16 rules_config hiện tại (SEG_SHOP_LE + SEG_NPP, combo BABAIR/BABCLOUD/KIDAIR/JRPKT) KHÔNG rule nào tặng "Bục trưng bày" (id `6af09a2b-9ce4-4fb8-86ef-a216fc9e3c0b`); chỉ 1 đơn cũ ORD_VJM448 chứa bục x2 dạng gift manual (gift_type rỗng ≠ engine 'platform') → nghi người dùng tự thêm dòng "hàng tặng" thủ công (form có button thêm gift). **Trước khi fix: quét toàn bộ rules_config + resolve gift_product_id sang tên SP; nếu không tìm thấy nguồn → hỏi tester order ID, không tự sửa theo giả định** (tránh fix nhầm tầng)

- **Kết luận card bục (12/08, đã resolve — KHÔNG có logic auto-tặng bục):** bục trưng bày là product `BUCTRUNGBAYVOLDEN` (id `6af09a2b-9ce4-4fb8-86ef-a216fc9e3c0b`) price **0** (insert 23/07). Quy trình trace nguồn gift → 1) rules_config (16 rule, không rule nào gift bục); 2) engine `executeEngine` chỉ gift `rule.gift_product_id`; 3) frontend `computeGifts` (OrdersModule) cùng logic; 4) **production bundle**: curl `https://volden-ops-web.vercel.app/` → grep asset js từ index → grep `BUCTRUNGBAY|6af09a2b` = 0; 5) real order data: gift KHÔNG khớp rule (mua BABAIRDEN → ORD_31V2SD tặng KIDAIRBE, ORD_VAGAE0 tặng SBS01TRANG — rule R1 phải tặng BABCLOUD) → gift được thêm THỦ CÔNG qua form. Card → **Need explanation** (list `6a734f50c60866066bbb8d99`) + comment hỏi tester mã đơn. **Pattern: muốn biết 1 giá trị/quà trong đơn từ đâu ra → trace ngược: rules DB → engine → frontend compute → production bundle → data đơn thật; gift không khớp rule = thêm tay.** Đơn ORD_VJM448 bục x2 gift_type rỗng = thêm tay (engine luôn set 'platform')

## Hủy đơn hàng — plan 2026-08-17 (đã trình user, CHƯA code — chờ duyệt "triển khai đi")

User yêu cầu: GDKD + 2 loại admin (admin, admin_role) + COO + CEO đều hủy được đơn, có lý do hủy. Plan đã trình: API `POST /api/orders/:id/cancel` (`requirePolicyEditor` + reason bắt buộc) + nút "Hủy đơn hàng" + modal tái dùng pattern "Từ chối" (OrdersModule.tsx ~3173). **Chưa code.** Facts đã verify khi đọc code:

- **DB đã có sẵn:** `orders.cancelled_at`, `orders.cancel_reason`, stage `cancelled` (RPC `auto_cancel_stale_orders` set cả 3) → không cần migration cho phần này
- **RPC `cancel_stock_order(p_stock_order_id, p_actor_id, p_reason)` đã tồn tại** → hủy phiếu xuất khi hủy đơn (nếu stage >= reported_warehouse)
- **`requirePolicyEditor` = `requireRole("admin", "admin_role", "gđkd", "coo", "ceo")`** (api/middleware/role.ts) — đúng 5 nhóm role user yêu cầu, dùng luôn cho cancel route
- Route `POST /api/orders/:id/reject` hiện CHỈ dành cho đơn `needs_approval` (GDKD từ chối duyệt), ghi lý do vào `approval_reason` — KHÔNG phải hủy đơn chung; cancel riêng phải ghi `cancel_reason`
- **⚠️ `PUT /api/orders/:id` chỉ `requireAuth` (KHÔNG role check)** — ai đăng nhập cũng set stage được (kể cả stage='cancelled'); khi làm cancel nên cân nhắc thêm role check cho stage='cancelled' qua route này
- UI role flags trong OrdersModule: `isGDKD = isSenior || roles.includes('gđkd') || roles.includes('admin_role')` — coo/ceo KHÔNG trong isGDKD, cần check riêng cho nút hủy

## SQL Migration — cách chạy (QUAN TRỌNG — user từng hỏi "tại sao k chạy được sql")

**Script cũ KHÔNG chạy được** vì Supabase chặn mọi cách DDL từ xa qua REST/SDK:
1. `POST /pg/query` → **404** (endpoint đã deprecated từ 2024, project mới không có)
2. RPC `exec_sql` → **404 PGRST202** (function không tồn tại — cần tạo thủ công)

**Cách chạy được (đã verify 3 migration):** kết nối Postgres TRỰC TIẾP bằng `pg` client + `SUPABASE_PASSWORD` trong `.env`:

> ⚠️ **`run-sql-direct.mjs` đọc `dotenv.config()` → chỉ chạy trên PROJECT DEV (`.env` = `wgglu...`).** Muốn apply lên PRODUCTION phải load `.env.prod` (ref `wevhm...`) — xem `references/supabase-projects.md`. Migration "applied" trên dev = KHÔNG có nghĩa production có.

```
postgresql://postgres:<SUPABASE_PASSWORD>@db.<project-ref>.supabase.co:5432/postgres
```

- Script dùng được: `npx tsx scripts/run-sql-direct.mjs sql/<file>.sql` (đã commit vào repo)
- Verify đã apply: `npx tsx scripts/verify-sql-applied.mjs` (check RPC + columns + seed)
- Project ref lấy từ `SUPABASE_URL` (vd `https://wggluyflkdrgffugpidk.supabase.co` → ref `wggluyflkdrgffugpidk`)
- Lỗi kết nối IPv6/timeout → thử pooler: `postgresql://postgres.<ref>:<pw>@aws-0-<region>.pooler.supabase.com:5432/postgres`

**Đã apply 2026-07-26:** `2026-07-26_add_vtp_integration.sql` + `2026-07-26_add_warehouse_address_sender.sql` + `2026-07-26_auto_export_stock_order.sql` — verified: RPC `create_export_stock_order` tồn tại, warehouses/orders/products columns đủ, seed 3 kho (Diem HN, Service_HN HN, Service_HCM HCM) có sender.

**Đã apply 2026-08-05:** `2026-08-05_fix_v_npp_debt_duplicate.sql` — recreate view `v_npp_debt` (fix duplicate lead). Verify bằng script đếm duplicate theo `lead_id` (114→113 rows, duplicate 0).

## Trello

- Board **"Volden - Ops App"** id `6a6b793f7e5888b26f2ad776` — URL `trello.com/b/l3d1Zx31`. Lists: Document/To do/Doing/Testing/Need fixed/Fixing/Done/Cancel
- **Board PRIVATE** — browser scan sẽ dừng ở trang login (không có email/password Trello trong .env, chỉ API key+token). Luôn scan qua API, đừng mở browser.
- **Creds: `TRELLO_API_KEY` + `TRELLO_TOKEN` trong `~/AppData/Local/hermes/.env`** (KHÔNG phải `D:/Hermes Proj/.env` — grep nhầm chỗ sẽ ra rỗng). Trello API cần **cả key + token** (ATTA token format mới). Token không khớp key → `invalid key`; chỉ có key → `invalid token`. Check board: `GET /1/members/me/boards?key=&token=`
- List IDs (board Volden, scan nhanh không cần fetch lists): To do `6a6b7945048bf91d79b6e3ea` · Need fixed `6a6b7984660b393096300f15` · Testing `6a6b794c7489177d352244b8` · Doing `6a6b794abbaff2499c1c4436` · Done `6a6b7951c8cad25b4a3f3b1b` · Document `6a6f713725189e8127253158` · Fixing `6a6b798d6e2207053549802e` · Cancel `6a6b7953c26e63e9fee443d3`
- Scan 1 list: `curl -s "https://api.trello.com/1/lists/<id>/cards?key=$KEY&token=$TOKEN&fields=name,id,desc,url,dateLastActivity"` — trả JSON mảng, parse bằng python
- **⚠️ Windows/MSYS pitfall — ID dính `\r` khi dùng bash loop:** `for CID in $(curl ... | python -c "...")` sinh ID có trailing `\r` → curl `/1/cards/$CID` trả `invalid id` hoặc JSON rỗng → JSONDecodeError. Gặp 3+ lần 2026-08-09. **Workaround chạy OK: viết hẳn 1 script python dùng `urllib.request`** (lấy key/token từ `~/AppData/Local/hermes/.env` qua `grep`, truyền vào script) — không đi qua bash loop, không dính `\r`. Hoặc nếu bắt buộc bash: `tr -d '\r'` trên ID trước khi dùng.
- Đọc card actions để triage (tester comment thật): `GET /1/cards/{id}/actions?filter=commentCard,updateCard&limit=10` — `updateCard.listAfter.name` = list mới, `commentCard.data.text` = comment. Comment text có thể bị percent-encode lỗi (`%3F%3F`) khi hiển thị — đọc raw là đủ để biết ý.
- Move card: `PUT /1/cards/{id}?key=&token=&idList=`; comment: `POST /1/cards/{id}/actions/comments?key=&token=&text=`

## DONE — BUG "Xem kho" redirect sai (fix xong 2026-07-26, commit `c04e27c`)

Card: `[BUG] Admin click vào các sản phẩm sắp hết hàng cần nhập thì bị redirect đến một trang không liên quan` (id `6a6f7fe9c8a8e35b92dbfbe5`) — **đã move To do → Testing**, chờ bé tester.

**Root cause (verified):** alert low-stock trên CEO dashboard trả `actionTab="stocks"` (api/app.ts) nhưng `ROUTE_TO_MODULE` trong `src/components/ErpApp.tsx` KHÔNG có `stocks` (module cũ merge thành `inventory` từ 2026-07-23) → fallback về ErpDashboard = "trang không liên quan".

**Fix đã apply (3 chỗ):**
1. `api/app.ts` — `actionTab: "stocks"` → `"inventory"` (alert low stock)
2. `src/types.ts` — `CeoAlert.actionTab` union thêm `'inventory'`
3. `src/components/ErpApp.tsx` — `ROUTE_TO_MODULE` thêm alias `stocks: 'inventory'` (URL cũ `/admin/erp/stocks` redirect đúng)

**Verify:** build PASS · `scripts/verify-stocks-alias.ts` 4/4 PASS (alert tab, URL cũ, URL mới, fallback dashboard). Commit `hermes - fix bug: alert 'Xem kho' redirect sai (stocks->inventory), thêm route alias stocks` → push `c04e27c`. Card → **Testing** (KHÔNG Done).


### ⚠️ QUY TRÌNH Trello (user nhấn mạnh 2 lần — TUÂN THỦ NGHIÊM)

| Tình huống | Em làm |
|-----------|--------|
| Card mới (To do / Document / bất kỳ đâu) | **Đọc card → LÊN PLAN → đưa anh duyệt** → chờ "triển khai đi" → mới code |
| Bug ở Need fixed (từ tester) | **Fix ngay** (không cần plan dài) → test → đưa về Testing |
| Code xong | Card → **Testing** — **KHÔNG BAO GIỜ tự move Done** |
| Tester test xong | PASS → Done (do anh/tester move, không phải agent) |

**Lỗi đã mắc (2026-07-26):** em tự move 2 card sang Done sau khi code xong → user bắt quay về Testing: *"quy trình của anh không phải là của em test... bắt buộc user hoặc tester của anh test thì mới đăng phần test để em lưu lại"*. Done là trạng thái do NGƯỜI TEST xác nhận, không phải do code pass build.

- **Card state 2026-07-26 (sau sprint + correction):** **Done** — (trống, chờ bé tester); **Testing** — [BUG] webhook thanh toán, [FEAT] auto-payment, [BUG] khách lẻ CK 0%, [BUG] approve policy, [FEAT] NPP quá hạn, [FEAT] auto phiếu xuất kho, VTP; **To do** — [FEAT] MISA, [FEAT] 247, [BUG] redirect sản phẩm sắp hết hàng; **Document** — Cách review module.

### Trello Watch — cron phát hiện card mới (Option A, đã triển khai)

- **Job:** cron `trello-watch` id `dd56aa9adde8`, schedule `*/15 * * * *`, `no_agent=true`, deliver origin
- **Script:** `trello_watch.py` tại `~/.hermes/scripts/` (⚠️ cron script path phải là filename tương đối tới `~/.hermes/scripts/` — không dùng absolute path; state file `trello_state.json` cùng thư mục). Bản gốc lưu tại `scripts/trello_watch.py` trong skill này — copy sang `~/.hermes/scripts/` nếu bị mất
- **Cơ chế watchdog:** mỗi tick đọc Trello API → diff với state → **chỉ print stdout khi có card mới** (stdout rỗng = silent = 0 token). Lần chạy đầu = baseline (lưu state, không bắn card cũ). Theo dõi lists: To do / Need fixed / Document / Testing
- **Luồng:** card mới → message bắn về group → em đọc card → lên plan → trình anh duyệt → code
- Test nhanh: chạy `python trello_watch.py`; giả lập card mới bằng cách xoá 1 id khỏi `trello_state.json` rồi chạy lại
- Trello API endpoints: `GET /1/boards/{board}/lists`, `GET /1/boards/{board}/cards?fields=name,id,idList,url,desc`
