# E2E Encryption opt-in (2026-08-28) — value prop "key user cầm, zero-knowledge"

## Triết lý
E2E chỉ CHO EXPORT (opt-in, key user giữ), **KHÔNG** mã hóa at-rest luồng realtime ghi âm — tránh friction + giữ server ổn. Vision coi E2E zero-knowledge là điểm bán khi sync cloud; chưa có cloud sync nên chỉ export.

## `hub/encctl.py` (stdlib only, KHÔNG pycryptodome)
AES-256-GCM thay thế = **Encrypt-then-MAC**.

- `derive_keys(passphrase, salt)` = PBKDF2-HMAC-SHA256 **600k iter** → 64 byte → tách `enc_key`(32) + `mac_key`(32).
- `_ctr_keystream(enc_key, nonce, len)` = keystream CTR dùng HMAC-SHA256 làm PRF (`HMAC(enc_key, nonceIV||ctr)`), XOR vào data.
- Encrypt-then-MAC: ciphertext = data XOR keystream; MAC = `HMAC-SHA256(mac_key, header+ct)` → 32-byte tag.
- Header = `TF1E2E` + version(1) + salt(16) + nonce(12). Salt+nonce ngẫu nhiên mỗi lần → cùng data+pass ra ciphertext khác.
- Sai pass / tampered → `E2EError` "Sai passphrase hoặc file bị sửa đổi", exit 1.

### ⚠️ PITFALL: tự build GHASH (GCM) dễ sai tag
Đã thử, fail round-trip. Chuyển sang HMAC PRF keystream + Encrypt-then-MAC = đơn giản, đúng, verify pass.

### CLI
```bash
python hub/encctl.py encrypt|decrypt|genkey <file> [-p PASS]
```
`genkey` = 8 từ nối gạch (kiem-saphia-thefirst-...) làm recovery key user giữ.

## API — `POST /api/export/encrypt`
Gom data user theo `data_type` (meetings/tasks/projects/transcript/face/all) → encrypt → lưu `tfo_data/exports/e2e_<name>_<type>_<ts>.tfoe`. Passphrase ≥ 8 ký tự.

### ⚠️ PITFALL: token phải truyền QUERY param (`?token=`), KHÔNG qua form field
`_resolve_user` đọc Form token nhưng POST `/api/export/encrypt` qua form field bị **401**; query param chạy. Các POST endpoint khác dùng form token OK — riêng endpoint này chịu query.