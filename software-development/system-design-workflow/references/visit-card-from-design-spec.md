# Visit Card — Design Spec to Deploy

> Example workflow: Implement a digital business card from a user-provided `design.md`, then deploy via Cloudflare Tunnel with custom domain.

## Step-by-step

### 1. Extract design tokens

From user's `design.md`, extract into CSS `:root` variables:

```css
:root {
  --yellow: #FFD600;
  --bg: #0D0D0D;
  --surface: #1B1B1D;
  --text-primary: #FFFFFF;
  --text-secondary: #8B8B8B;
  --border: rgba(255,255,255,.05);
  --r-card: 28px;
  --r-btn: 999px;
  --r-input: 18px;
}
```

### 2. Structure per design rules

| Rule | Implementation |
|------|---------------|
| 1 Hero | Name = H1 32px/700 — everything else smaller |
| 1 Primary CTA | Yellow "Lưu liên hệ" button (duy nhất) |
| Card max 3 levels | Avatar + Name → Contact → QR → Actions |
| Section spacing 24 | Each section separated by `margin-top: 24px` |
| Dark mode no shadow | `border: 1px solid rgba(255,255,255,.05)` |

### 3. Interactive features

- **QR codes**: `https://api.qrserver.com/v1/create-qr-code/?size=NxN&data=URL`
- **vCard download**: Generate `.vcf` blob → trigger download
- **Share**: Use `navigator.share()` with `navigator.clipboard` fallback
- **Photo**: Support both `<img>` avatar and letter-initial fallback; use `object-fit: cover` + `overflow: hidden` để ảnh fit khung tròn

### 🔴 Platform icons — dùng SVG brand, không dùng emoji

User có các app nhắn tin: **Zalo**, **WhatsApp**, **WeChat**. KHÔNG dùng emoji (💚💬🟢) — phải dùng **inline SVG brand icon** đúng màu sắc:

| App | Màu | Ghi chú |
|-----|-----|---------|
| **Zalo** | `#0068FF` | Blue rounded square with white "Z" |
| **WhatsApp** | `#25D366` | Green circle with white phone icon |
| **WeChat** | `#07C160` | Green chat bubbles |

SVG icons được nhúng inline trong `<svg viewBox="0 0 24 24">` — mỗi icon ~20-22px trong contact row, ~24px trong QR grid.

**Email** giữ nguyên Material Icon `mail` (outlined style).

### 4. Deploy options

| Option | When to use |
|--------|-------------|
| **Gist** (no preview) | Code/text snippet, no HTML rendering needed |
| **GitHub repo + htmlpreview.io** | Need rendered preview without domain |
| **Cloudflare Tunnel + domain** | Production with custom domain |

### 5. Cloudflare Tunnel DNS setup

```
┌──────────────────────────────┐
│  Cloudflare Dashboard → DNS  │
├──────────────────────────────┤
│  CNAME  @  → tunnel.cfargotunnel.com  ☁️ Proxied
│  CNAME  www → example.com           ☁️ Proxied
└──────────────────────────────┘
```

Tunnel config (`firstonly-config.yml`):
```yaml
tunnel: <tunnel-uuid>
credentials-file: C:\Users\...\.cloudflared\<uuid>.json
ingress:
  - hostname: thefirstonly.com
    service: http://localhost:5099
  - hostname: www.thefirstonly.com
    service: http://localhost:5099
  - service: http_status:404
```

⚠️ **Windows path pitfall**: Use `C:\Users\...` NOT `/c/Users/...` for `--config` flag.

### 6. Final file layout

```
visit-card/
├── index.html        # Single-file visit card (CSS + HTML + JS)
└── (deploy via Gist, repo, or tunnel)
```

## Design spec → HTML checklist

- [ ] Map all color tokens to CSS variables
- [ ] Typography matches spec (H1 32/700, Body 16, Caption 12)
- [ ] Spacing uses 8pt grid only (4,8,12,16,24,32,40,48,64)
- [ ] Card radius 28, Button 999, Input 18
- [ ] Button height 56px
- [ ] Touch target ≥ 48px
- [ ] 1 Hero, 1 Primary CTA only
- [ ] Dark mode: no shadow, use border .05
- [ ] Icons: outlined style, FILL=0; brand apps (Zalo/WhatsApp/WeChat) = inline SVG
- [ ] Platform icons: SVG brand colors, not emoji
- [ ] Photo avatar: object-fit cover + overflow hidden
- [ ] Animation 200ms ease-out
- [ ] Animation 200ms ease-out
- [ ] Mobile responsive ≥ 360px
