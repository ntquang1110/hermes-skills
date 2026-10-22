# LAN service IP drift — diagnosis & resolver pattern

Applies to any home-lab service on a DHCP host: Mac Whisper `:9000`, Unsloth
`:18888`, OmniRoute `:20128`, the ERP ports. Same failure mode, same fix.

## The failure mode

A service is deployed and documented as `192.168.1.3:9000`. The host's DHCP lease
changes (router restart, Wi-Fi reconnect, sleep/wake). Now:

- the watchdog pings `.3`, times out, and alerts "server unreachable";
- the STT wrapper POSTs to `.3` and fails;
- **the service is fine.** Nothing is broken except the address in the code.

Observed drift in one session: `.3 → .2 → .4 → .5`, with `.2` appearing and
vanishing from ARP within minutes. Any hardcoded literal is a time bomb.

## Do NOT trust a failed ping

A ping to the *old* address timing out says nothing about whether the host is up.
In the real incident the host had `uptime` = 74 days and a healthy whisper server
the entire time the watchdog was alerting.

Probes, in the order that actually discriminates:

| Probe | Reading |
|---|---|
| `ping <old-ip>` | often 100% loss; **not evidence the host is down** |
| `arp -a` | keeps the stale dynamic entry after the host moves |
| TCP sweep for the *service port* | decisive — finds the host at its new address |
| `:22 → REFUSED` | host is UP, sshd is off (≠ timeout) |
| `:22 → timeout` | host unreachable OR firewalled, not necessarily off |
| `uptime`, `launchctl list \| grep <label>`, `lsof -nP -iTCP:<port> -sTCP:LISTEN` | proves liveness once you are in |

`errno 10035` / `WinError 10060` from Windows means connect timed out; `10061`
means actively refused. Refused is more informative — it proves the host answered.

## Resolver pattern

`scripts/mac_whisper_resolve.py` implements the three-tier lookup. Use it as the
template for any other drifting service — change `HOSTNAMES`, `PORT`, `LAN_PREFIX`.

1. **mDNS hostname** (`Mac-mini-cua-kiem.local`). Survives DHCP. Requires Bonjour
   resolution to work from the caller — verified from Windows on this LAN.
2. **Cached last-good IP**, re-verified with a TCP connect before being trusted,
   so a stale cache can never be returned as fact.
3. **Parallel `/24` sweep** on the service port, 80 workers, 0.8 s timeout.
   Cheap enough to run on every watchdog tick.

Callers pass `force=True` when a stale cache would be harmful (watchdog), and
default (cache-first) when latency matters (per-request STT).

## Fast parallel TCP sweep (stdlib only)

```python
import socket, concurrent.futures

def _reachable(ip, port, tmo=1.5):
    s = socket.socket(); s.settimeout(tmo)
    try:    return s.connect_ex((ip, port)) == 0
    except Exception: return False
    finally: s.close()

def find(port, prefix="192.168.1."):
    def scan(i):
        ip = prefix + str(i)
        return ip if _reachable(ip, port, tmo=0.8) else None
    with concurrent.futures.ThreadPoolExecutor(max_workers=80) as ex:
        for r in ex.map(scan, range(1, 255)):
            if r:
                return r
    return None
```

Validate the sweep before trusting a negative result — probe a port you *know* is
open (e.g. `:445` on a Windows box) and confirm it comes back open. A sweep that
returns "nothing found" while a known-good host is up means the sweep is broken,
not that the LAN is empty.

## Driving the probes from Windows

No `sshpass`/`expect` in git-bash. Use `paramiko` with password auth:
`references/win-mac-ssh-paramiko.md`.

Gotcha: the Mac's system `python3` has no `faster_whisper`. Always use the
server's venv interpreter for on-box tests: `/Users/tquang/whisper-venv/bin/python`.

## Prevention

- Document services by **hostname**, not IP.
- Any script that takes a LAN address should resolve it, never inline it.
- A watchdog that reports "unreachable" should say which address it tried, so an
  IP-drift false alarm is distinguishable from a real outage at a glance.
