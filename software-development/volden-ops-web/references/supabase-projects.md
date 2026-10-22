# Supabase Projects — dev vs prod (Volden Ops Web)

## Sự thật: CÓ HAI PROJECT

| File env | Project ref | Vai trò |
|---|---|---|
| `.env` (mặc định, mọi script chạy) | `wggluyflkdrgffugpidk` | DEV — migration hay apply nhầm vào đây |
| `.env.prod` | `wevhmrezxgnyvkbmcqux` | PRODUCTION (Vercel dùng) |

**Pitfall kinh điển (đã xảy ra 2026-08-17):** migration apply qua `run-sql-direct.mjs` (đọc `.env`) → chỉ lên DEV. Code deploy lên Vercel (auto từ main) dùng project prod → prod DB thiếu column → "báo thiếu schema khi lên đơn" = `Could not find the 'X' column of 'orders' in the schema cache`.

## Cách xác định production đang trỏ project nào (không cần Vercel token)

1. Curl production bundle: `curl -s https://volden-ops-web.vercel.app/ -o prod.html` → grep `src="/assets/index-<hash>.js"` → `curl -s https://volden-ops-web.vercel.app/assets/index-<hash>.js -o prod-bundle.js`
2. Grep supabase URL trong bundle: `node -e "const s=require('fs').readFileSync('prod-bundle.js','utf8'); console.log([...new Set(s.match(/https:\/\/[a-z0-9]+\.supabase\.co/g)||[])])"` → ra ref production thật.
3. Cách chứng minh login 401 ≠ password sai: tạo user tạm bằng service_role key của DEV, login local Supabase OK nhưng login qua production API vẫn 401 → chứng tỏ production dùng project KHÁC (user không tồn tại bên prod).

## Check column tồn tại trên 1 project

- PostgREST CHẶN query `information_schema.columns` (`Could not find the table 'public.information_schema.columns' in the schema cache`) → KHÔNG dùng supabase-js để xem schema.
- Cách nhanh qua PostgREST (service_role): SELECT thử column → lỗi `column X does not exist` = thiếu; thành công = có. Insert thử row chứa column mới → `Could not find the 'X' column of 'Y' in the schema cache` = THIẾU (lỗi này dễ hiểu nhầm là cache, nhưng với column vắng mặt thật thì nó là thiếu schema). Nhớ cleanup: `sb.from('orders').delete().eq('id', testId)`.
- Cách đầy đủ: pg direct xuống từng project (xem dưới).

## pg direct connection

- URL: `postgresql://postgres:<SUPABASE_PASSWORD>@db.<ref>.supabase.co:5432/postgres`
- **⚠️ `.env.prod` password bị bọc nháy kép + CRLF:** dòng `SUPABASE_PASSWORD="<PASSWORD>"\r` → phải strip `"` và `\r` trước khi dùng (script parse thủ công không strip → `password authentication failed`). Dev `.env` password không bọc.
- IPv6/timeout (`timeout expired` dù password đúng) → thử `family: 4` hoặc pooler `postgresql://postgres.<ref>:<pw>@aws-0-<region>.pooler.supabase.com:6543/postgres`. Region pooler của prod chưa xác định được (8/2026); nếu cần chắc chắn thì hỏi user hoặc dùng SQL Editor Dashboard.

## Recipe: test production API end-to-end (khi không có account prod)

1. Tạo auth user tạm qua admin API: `sb.auth.admin.createUser({ email, password, email_confirm: true, user_metadata: {...} })`
2. **Trigger `handle_new_user()` TỰ insert public.users** → đừng insert thủ công (sẽ dính `duplicate key violates users_pkey`). Chỉ insert thủ công khi biết chắc trigger không chạy.
3. Login qua production API `/api/auth/login` → token.
4. Gọi endpoint cần test (vd `POST /api/orders` với `discount_mode`) → đọc status + body.
5. Cleanup: delete order test row + `sb.from('users').delete().eq('email', ...)` + `sb.auth.admin.deleteUser(id)`.

## Checklist trước khi báo "SQL applied"

- [ ] Apply CẢ 2 project: dev (`.env`) + prod (`.env.prod`)
- [ ] Verify trên TỪNG project: query `information_schema` (pg direct) hoặc SELECT/INSERT test qua PostgREST
- [ ] Ghi rõ ref project nào đã apply vào comment/STATE — tránh "applied rồi" mà thật ra chỉ dev