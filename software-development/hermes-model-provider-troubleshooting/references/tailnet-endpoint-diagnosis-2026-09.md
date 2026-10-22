# Tailnet (Tailscale CGNAT) LLM endpoint — unreachable diagnosis, 2026-09

Context: cron watchdog `watchdog-unsloth` flagged endpoint `racial-clarke-some-redhead.trycloudflare.com`
dead (`getaddrinfo failed`). A peer proposed an IP `100.88.115.32` to bypass the tunnel.

## Why `100.x.x.x` is special

`100.64.0.0/10` is CGNAT. In this setup it is **Tailscale** — every node in Quang's tailnet
gets a `100.x` IP. So `100.88.115.32` is a mesh address, NOT a home-LAN address. A peer's
"here's the IP" is almost always a tailnet host id, not a routable public/LAN target.

Confirm with `tailscale status`:
```
100.100.18.97   tquang-dell      (this machine)
100.88.115.32   pharma-duc-anh   windows  idle, tx 4044 rx 476  ← online, mesh alive
```

## 4-step diagnosis that resolved the dead-end loop

The tempting move is to keep re-probing the endpoint. That loops forever. Instead:

1. **Mesh still up?** `tailscale status` shows host online + recent tx/rx; `route -n | grep <ip>`
   shows `on-link`; single-digit-ms ping = mesh healthy. → Networking is NOT the problem.
2. **Probe TCP ports, never rely on ping.** loop `timeout 3 bash -c "echo > /dev/tcp/ip/port"`
   over candidate service ports. Here `8888/8080/8000/3000/80/443/22` all closed but `445`+`3389`
   OPEN → the Windows box is up; the LLM server is simply **not listening on the tailnet iface**.
3. **Decisive clue — ask host owner to run `netstat -ano | findstr :8888`:**
   → `127.0.0.1:8888 LISTENING` + `192.168.0.84:8888 LISTENING` (PID 26232).
   Service IS running and healthy (active ESTABLISHED connections), but bound only to loopback
   and the LAN NIC. The tailnet IP `100.88.115.32` has NO listener → unreachable from peers.
4. **Cross-subnet:** host LAN `192.168.0.84`, this machine LAN `192.168.1.111` — different subnets,
   no LAN route this direction. Tailnet is the only path, so the service MUST bind `0.0.0.0`.

## The fix (what to tell the host owner)

Rebind the server to `0.0.0.0:PORT` and **restart** it (config edit alone does nothing until restart):
- uvicorn / FastAPI: `--host 0.0.0.0 --port 8888`
- docker: `-p 0.0.0.0:8888:8888` or `--network host`
- GUI server (LM Studio / custom): "bind address" / "host" → `0.0.0.0`

Success = `netstat -ano | findstr :8888` shows `0.0.0.0:8888 LISTENING`.

Then on this side: re-point Hermes `custom_providers.<name>.base_url` to `http://100.88.115.32:8888/v1`
and update the same URL inside the watchdog script — **two places** (see main SKILL "watchdog" section).
Dropping the trycloudflare hop also removes the 120s proxy-read cap entirely.

## Takeaway

"Peer gave me an IP, can I fix it from here" → I could NOT start the service from terminal (no SSH, 22 closed).
The only agent-side lever is re-pointing client config + watchdog URL once bind becomes `0.0.0.0`.
Do not claim a fix is done until the remote netstat shows `0.0.0.0:PORT LISTENING`; otherwise verify 8s+ timeouts are still real.