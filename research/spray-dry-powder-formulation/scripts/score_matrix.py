#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tính điểm tổng cho bảng sàng lọc chất mang (spray-dry-powder-formulation).
Input: file JSON dạng {"items":[{"id":..., "s":{"kiem":..,"nhiet":..,"am":..,"maillard":..,
        "bao":..,"giu_pH":..,"pl":..,"tb":..}, "override":"..."}, ...]}
Mọi tiêu chí 0..5, 5 = tốt/an toàn nhất.  Override = xếp loại ghi đè thủ công (lập luận quyết định).

Usage:
  python score_matrix.py scores.json
In ra diem_tong_100, rating (0-5), band A-E và xếp hạng; ghi lại JSON đã chấm (nếu có tham số 2).
"""
import json, sys, io, os

W = {"kiem": 0.18, "nhiet": 0.18, "am": 0.12, "maillard": 0.10,
     "bao": 0.12, "giu_pH": 0.10, "pl": 0.10, "tb": 0.10}


def band(t):
    if t >= 75: return "A - UU TIEN"
    if t >= 60: return "B - KHA THI"
    if t >= 45: return "C - CO DIEU KIEN"
    if t >= 30: return "D - HAN CHE"
    return "E - KHONG NEN"


def score(s):
    t = round(sum(float(s.get(k, 0)) * w for k, w in W.items()) / 5 * 100, 1)
    return t, max(0, min(5, int(round(t / 20))))


def main(path_in, path_out=None):
    data = json.load(io.open(path_in, encoding="utf-8"))
    items = data["items"] if isinstance(data, dict) else data
    out = []
    for it in items:
        t, r = score(it.get("s", {}))
        xl = it.get("override") or band(t)
        out.append((it.get("id", "?"), t, r, xl))
    out.sort(key=lambda x: -x[1])
    print("%-30s %6s %4s  %s" % ("id", "diem", "rat", "xep_loai"))
    for i, (nid, t, r, xl) in enumerate(out, 1):
        print("%2d %-27s %6s %4s  %s" % (i, nid, t, r, xl))
    if path_out:
        res = [{"id": n, "diem_tong_100": t, "rating": r, "xep_loai": xl} for n, t, r, xl in out]
        with io.open(path_out, "w", encoding="utf-8") as f:
            json.dump({"thang_diem": W, "ket_qua": res}, f, ensure_ascii=False, indent=2)
        print("WROTE", path_out, os.path.getsize(path_out), "bytes")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
