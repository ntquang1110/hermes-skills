#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
audio_check.py — Kiem tra chat luong ghi am TRUOC khi goi STT

Van de: Whisper (ca Groq, ca Hermes auto-STT) hallucinate khi audio im lang.
Whisper khong nghe duoc gi nen no doc ra template mac dinh:
"Hay subscribe cho kenh ... de khong bo los nhung video hap dan".
Ket qua: user nghe transcript rac va nghi STT hong, nhung that ra file rong.

Script nay do bang am thanh, chan TRUOC khi ton 1 call API.

Usage
-----
  python audio_check.py <file.ogg> [file2.wav ...]
  python audio_check.py --quiet <file>     # chi in PASS/FAIL

Exit codes
----------
0  PASS — audio co noi dung, dung de STT
1  FAIL — audio khong dung (im lang / qua nho / stereo sai)
2  Loi (thieu ffmpeg, file khong ton tai)
"""

import os
import re
import sys
import json
import subprocess

# ---------------------------------------------------------------- nguong
THRESH = {
    "min_duration_s": 1.0,
    "min_bitrate": 4000,
    "max_mean_db": -60.0,
    "max_peak_db": -50.0,
    "max_silence_ratio": 0.95,
}

HALLUC_MARKERS = [
    "subscribe", "dang ky kenh", "ung ho kenh", "video hap dan",
    "bo los", "like and share", "phan binh luan",
    "lalaschool", "la la school", "ghien mi go",
]


def run(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=60)
        return r.returncode, r.stdout, r.stderr
    except FileNotFoundError:
        return 127, "", "khong tim thay tool: %s" % cmd[0]
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"


def need_tools():
    for t in ("ffmpeg", "ffprobe"):
        rc, _, _ = run([t, "-version"])
        if rc != 0:
            sys.stderr.write("[LOI] Thieu %s. Cai choco-chim truoc.\n" % t)
            sys.exit(2)


def probe(path):
    rc, out, _ = run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration,bit_rate,size",
        "-show_entries", "stream=codec_name,sample_rate,channels",
        "-of", "json", path])
    if rc != 0:
        return None
    try:
        d = json.loads(out)
    except json.JSONDecodeError:
        return None
    dur = float(d.get("format", {}).get("duration") or 0)
    br = int(d.get("format", {}).get("bit_rate") or 0)
    size = int(d.get("format", {}).get("size") or 0)
    st = (d.get("streams") or [{}])[0]
    return {
        "duration": dur,
        "bitrate": br,
        "size": size,
        "codec": st.get("codec_name", "?"),
        "sr": int(st.get("sample_rate") or 0),
        "channels": st.get("channels", 0),
    }


def volumedetect(path):
    rc, _, err = run(["ffmpeg", "-i", path, "-af", "volumedetect",
                      "-f", "null", "-"])
    mean = peak = None
    m = re.search(r"mean_volume:\s*(-?[\d.inf]+) dB", err)
    if m:
        mean = float(m.group(1))
    m = re.search(r"max_volume:\s*(-?[\d.inf]+) dB", err)
    if m:
        peak = float(m.group(1))
    return mean, peak


def silence_ratio(path, noise_db=-50.0, min_dur=0.3):
    rc, _, err = run(["ffmpeg", "-i", path, "-af",
                      "silencedetect=noise=%ddB:d=%s" % (int(noise_db), min_dur),
                      "-f", "null", "-"])
    if rc != 0:
        return None, 0
    durs = [float(x) for x in re.findall(r"silence_duration:\s*([\d.]+)", err)]
    return (sum(durs) if durs else 0.0), len(durs)


def voiced_ratio_check(path):
    rc, _, err = run(["ffmpeg", "-i", path, "-af",
                      "astats=metadata=1:reset=48", "-f", "null", "-"])
    if rc != 0:
        return None
    vals = [float(x) for x in
            re.findall(r"RMS level dB:\s*(-?[\d.]+|-inf)", err)]
    vals = [v for v in vals if v > -90]
    if not vals:
        return 0.0
    voiced = sum(1 for v in vals if v > -55)
    return voiced / float(len(vals))


def check_one(path):
    res = {"file": path, "ok": False, "problems": [], "warns": []}
    if not os.path.exists(path):
        res["problems"].append("khong ton tai")
        return res

    pr = probe(path)
    if not pr:
        res["problems"].append("khong doc duoc (file hong hoac khong phai audio)")
        return res
    res.update(pr)

    mean, peak = volumedetect(path)
    res["mean_db"] = mean
    res["peak_db"] = peak

    sil_total, sil_n = silence_ratio(path)
    res["silence_sec"] = sil_total
    res["silence_ratio"] = (sil_total / pr["duration"]
                            if sil_total is not None and pr["duration"] > 0
                            else None)

    voiced = voiced_ratio_check(path)
    res["voiced_ratio"] = voiced

    if pr["duration"] < THRESH["min_duration_s"]:
        res["problems"].append("thoi luong %.1fs — qua ngan" % pr["duration"])
    if pr["bitrate"] and pr["bitrate"] < THRESH["min_bitrate"]:
        res["problems"].append("bitrate %d bps — qua thap, nghi file rong" % pr["bitrate"])
    if mean is not None and mean <= THRESH["max_mean_db"]:
        res["problems"].append("mean_volume %s dB — im lang hoac gan im lang" % mean)
    if peak is not None and peak <= THRESH["max_peak_db"]:
        res["problems"].append("max_volume %s dB — khong co song am nao" % peak)
    if res["silence_ratio"] is not None and \
            res["silence_ratio"] >= THRESH["max_silence_ratio"]:
        res["problems"].append("%.0f%% thoi luong la im lang"
                               % (res["silence_ratio"] * 100))
    if voiced is not None and voiced == 0.0:
        res["problems"].append("khong khung nao co tieng (voiced_ratio = 0)")

    if pr["channels"] == 2:
        res["warns"].append("stereo — nen mono de tiet kiem")
    if pr["sr"] and pr["sr"] > 16000:
        res["warns"].append("sample rate %d Hz — resample ve 16000 truoc khi STT" % pr["sr"])
    if pr["duration"] > 300:
        res["warns"].append("audio %.0fs — chunk 150s voi overlap 15s" % pr["duration"])

    res["ok"] = (len(res["problems"]) == 0)
    return res


def has_hallucination(text):
    if not text:
        return False
    low = text.lower()
    return any(m in low for m in HALLUC_MARKERS)


def report(r, quiet=False):
    if quiet:
        print("%s  %s" % ("PASS" if r["ok"] else "FAIL", os.path.basename(r["file"])))
        return

    print("=" * 68)
    print(os.path.basename(r["file"]))
    print("=" * 68)
    print("  thoi luong   : %.1f giay" % r.get("duration", 0))
    print("  codec       : %s  %d Hz  %d kenh"
          % (r.get("codec", "?"), r.get("sr", 0), r.get("channels", 0)))
    print("  bitrate     : %s bps" % (r.get("bitrate") or "?"))
    print("  dung luong  : %s bytes" % r.get("size", 0))
    if r.get("mean_db") is not None:
        print("  mean volume : %s dB" % r["mean_db"])
    if r.get("peak_db") is not None:
        print("  max_volume  : %s dB" % r["peak_db"])
    if r.get("silence_ratio") is not None:
        print("  im lang     : %.1f giay (%.0f%%)"
              % (r.get("silence_sec") or 0, r["silence_ratio"] * 100))
    if r.get("voiced_ratio") is not None:
        print("  co tieng    : %.0f%% khung" % (r["voiced_ratio"] * 100))
    print("")

    if r["ok"]:
        print("  [PASS] Audio dung de STT.")
        for w in r["warns"]:
            print("    canh bao: %s" % w)
    else:
        print("  [FAIL] Khong nen chay STT:")
        for p in r["problems"]:
            print("    - %s" % p)
        for w in r["warns"]:
            print("    canh bao: %s" % w)
        print("")
        print("  -> KHONG goi Groq. Whisper se hallucinate 'subscribe cho kenh'.")
        print("  -> Kiem tra: mic, app ghi am, thu lai bang tai.")
    print("")


def main():
    args = list(sys.argv[1:])
    quiet = "--quiet" in args
    if quiet:
        args.remove("--quiet")
    if not args:
        sys.stderr.write(__doc__)
        sys.exit(2)

    need_tools()

    results = []
    for p in args:
        r = check_one(p)
        results.append(r)
        report(r, quiet)

    failed = [r for r in results if not r["ok"]]
    if not quiet and len(results) > 1:
        print("=" * 68)
        print("TONG: %d file — %d PASS, %d FAIL"
              % (len(results), len(results) - len(failed), len(failed)))
        print("=" * 68)

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()