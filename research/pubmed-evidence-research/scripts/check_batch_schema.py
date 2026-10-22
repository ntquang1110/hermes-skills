#!/usr/bin/env python3
"""Kiểm SCHEMA + đếm PMID cho deliverable `batch-*.json` (khung 8 chặng).

    python check_batch_schema.py "D:/Hermes Proj/fixgby/docs/10-cong-thuc-23/batch-c.json"

Vì sao cần: khi task chốt "schema CHÍNH XÁC" (19/10/2026, fixgby `10-cong-thuc-23` lô C — 7 chất),
một object thiếu khoá `pmid` trong 1 chặng vẫn `json.load` OK và vẫn trông "hợp lệ". Script này bắt
đúng những khoá thiếu đó, và in **tổng PMID DUY NHẤT** — con số đúng để viết `verified N/N`.

Ghi nhớ về con số cuối: |set hợp| — KHÔNG BAO GIỜ cộng `pass` của lượt trước với `fail` của lượt đó.
Ca thật cùng ngày: fetch 61 PMID, 50 pass / 11 fail (rate limit), retry 11 cái kia xong ⇒ bản nháp vẫn
in `verified 61/72` vì `n_tot = n_ok + len(bad)` đếm 11 PMID hai lần. Sự thật là 61/61.

Exit 0 = schema sạch; exit 1 = có chất sai schema (không ship).
"""
import json
import sys

STAGES = ["cua_vao", "qua_hang_rao", "gan_lan_dau", "gan_de_di",
          "toi_mo", "ra_khoi_te_bao", "thai", "o_lai"]
KEYS = (["chat", "ten_vi", "cong_thuc", "nhom", "dang_dung"] + STAGES +
        ["tuong_tac", "bat_kha", "da_that_bai", "chi_dau_do_duoc",
         "muc_bang_chung", "tag_H", "pmids"])
LEVELS = {"I", "A", "R"}


def unwrap(data):
    """Nhận cả MẢNG trần (chuẩn `batch-*.json`) lẫn dict bọc {"meta":..,"chat":[...]}."""
    if isinstance(data, dict):
        for k in ("chat", "ingredients", "data", "items", "rows"):
            if isinstance(data.get(k), list):
                return data[k], f"(bọc trong dict, lấy khoá '{k}')"
    return data, ""


def main(path):
    data, note = unwrap(json.load(open(path, encoding="utf-8")))
    if not isinstance(data, list):
        print("FAIL: JSON phải là MẢNG object (hoặc dict chứa list)")
        return 1
    if note:
        print(note)
    bad, uniq = False, set()
    for c in data:
        if not isinstance(c, dict):
            print(f"FAIL: phần tử không phải object: {type(c).__name__}")
            bad = True
            continue
        miss = [k for k in KEYS if k not in c]
        stage_bad = []
        for s in STAGES:
            v = c.get(s)
            if not isinstance(v, dict):
                stage_bad.append(f"{s}(không phải object)")
            elif "pmid" not in v:
                stage_bad.append(f"{s}.pmid")
        if c.get("muc_bang_chung") not in LEVELS:
            stage_bad.append(f"muc_bang_chung={c.get('muc_bang_chung')!r} (phải I|A|R)")
        if not isinstance(c.get("tag_H"), list):
            stage_bad.append("tag_H(không phải list)")
        for s in STAGES:
            for p in ((c.get(s) or {}).get("pmid") or []):
                uniq.add(str(p).strip())
        for p in (c.get("pmids") or []):
            uniq.add(str(p).strip())
        ok = not (miss or stage_bad)
        bad |= not ok
        print(f"{'OK  ' if ok else 'FAIL'} {c.get('chat', '<thiếu chat>'):<32} "
              f"thiếu={miss or '-'}  chặng lỗi={stage_bad or '-'}")
    uniq.discard("")
    print(f"\nchất: {len(data)} | PMID DUY NHẤT: {len(uniq)}"
          f"   <-- dùng ĐÚNG con số này cho `verified N/N`")
    print("Tổng = |set hợp của mọi PMID trong file|. Không cộng pass+fail của hai lượt chạy.")
    if bad:
        print("KẾT LUẬN: schema CHƯA sạch — không ship.")
    return 1 if bad else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
