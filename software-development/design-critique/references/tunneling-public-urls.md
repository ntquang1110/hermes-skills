# Tunneling — Quick Public URLs on Windows

When the user accesses output from a different device (phone via Telegram,
tablet, colleague's machine), localhost is invisible. Use one of these
tunnels to get a public URL fast.

## LocalTunnel (recommended — works every time)

```bash
npx.cmd localtunnel --port <port>
# Example:
npx.cmd localtunnel --port 8080
```

**URL pattern**: `https://<random-words>.loca.lt`

- ✅ Works immediately, no signup
- ✅ Output goes to stdout: `your url is: https://khaki-insects-rest.loca.lt`
- ⚠️ The foreground command will time out after the URL is printed —
  start it in background mode for persistence
- ⚠️ First visit may show a "Click to Continue" interstitial

## Why not the others (on Windows)

| Tool | Result on this machine |
|------|----------------------|
| **cloudflared** | `cloudflared tunnel --url http://localhost:8080` — started but produced zero output even after 20+ seconds. Requires auth on first run. |
| **serveo.net** | `ssh -R 80:localhost:8080 serveo.net` — hangs silently, no URL emitted. |

Both may work fine on macOS/Linux, but on this Windows (git-bash/MSYS2)
environment they hang. LocalTunnel via `npx.cmd` (not `npx`) is the
reliable fallback.

## PWABuilder — APK from URL (Flutter build fallback)

When local Flutter/Gradle APK build fails (e.g. Kotlin incremental cache
corruption on Windows), use PWABuilder to turn any public URL into a
sideloadable Android APK:

```
https://www.pwabuilder.com
1. Enter the tunnel URL
2. Click "Generate"
3. Download the APK
4. Sideload onto the device
```

Requirements:
- Must be a **public HTTPS URL** (tunnel URL works)
- App gets basic WebView chrome + offline support
- No native notification/background without work

## When to raise this in the design process

Add to the **Collect** phase questions:

- "Where will the user be when they use this?" (same machine vs phone/tablet)
- "Does the user need persistent background/notification?" (then a tunnel +
  PWA won't cut it — need a real app or a bot)
- "Can we assume the machine is reachable from the user's device?" (if same
  LAN, use local IP; if remote, tunnel needed)
