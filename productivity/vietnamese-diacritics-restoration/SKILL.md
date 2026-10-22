---
name: vietnamese-diacritics-restoration
description: "Use when adding Vietnamese dau to unaccented text safely."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Vietnamese, Diacritics, JSON, Data-Quality, i18n]
    related_skills: [ocr-and-documents, docx, xlsx]
---

# Vietnamese Diacritics Restoration

Restore full Vietnamese diacritics (dấu) to unaccented (`khong dau`) text in data files
without corrupting IDs, citations, numbers, or formulas.

## Trigger — use when

- JSON/CSV/Markdown contains Vietnamese without dấu (`tha truc tiep`, `nuoc thai heo`).
- Task says "thêm dấu", "restore diacritics", or ratio of accented words is ~0.
- Domain text is Vietnamese (chăn nuôi, xử lý nước thải, pháp lý, QCVN) mixed with
  protected tokens: PMID/DOI/URL, chemical formulas, Latin names, English citations.
- Markdown research notes / article files (`*.md`) where EVERY Vietnamese word lost dấu
  and the task demands a **diacritic-only diff**, verified by a strip-identity check
  (`strip(input) == strip(output)`). See "Diacritic-only mode" below.

## Workflow

1. **Read + snapshot before-state.** Read the full file (no offset pagination before
   overwrite). Record `rows` count and unaccented ratio. Keep any `.raw.json` backup
   untouched — never write to it.
2. **Classify fields into PROTECTED vs VIETNAMESE.**
   - PROTECTED (byte-identical): `id`, `pmid`, `doi`, `pubmed_url`, numbers/units,
     chemical formulas (`Mg2+`, `NH4+`, `PO4^3-`, `MgNH4PO4.6H2O`, `FeCl3`, `CaCO3`,
     `CaO`, `MgO`, `FePO4`, `FeS`), Latin names, English-only `label`/`citation`,
     `type: paper`.
   - VIETNAMESE (add dấu): `element`, `element_vi`, `name`, `effect`, `group`,
     `mechanism`, `dosage_ref`/`dose_calc`, `side_effects`, `verification`,
     `note` (Vietnamese part), `synergy_or_conflict`, `qcvn_target`,
     `metadata.title`/`note`.
3. **Restore dấu with domain semantics.** Use chuyên ngành meaning, not naive mapping:
   `tha truc tiep` → `thả trực tiếp`, `nuoc thai heo` → `nước thải heo`,
   `lieu` → `liều`, `ket tua` → `kết tủa`, `hieu suat` → `hiệu suất`,
   `thieu hut` → `thiếu hụt`, `bo sung` → `bổ sung`, `tach ran` → `tách rắn`,
   `ham biogas` → `hầm biogas`, `ky khi` → `kỵ khí`, `dong u` → `đống ủ`.
4. **Overwrite original file(s) only**, then `json.load` to validate.
5. **Verify preservation.** Compare sorted regex extracts new-vs-raw for
   `pmid`, `doi`, `pubmed_url`, `label`/`citation`, and all digit sequences —
   all must match exactly. Spot-check formulas listed in step 2.
6. **Verify ratio.** Compute accented-word ratio with NFD Mark stripping on the
   VIETNAMESE fields only (whole-file ratio is diluted by English keys/citations).
   Target ≥ 0.5 on VI fields. Report rows fixed + before/after ratios.

```python
import json, re, unicodedata
def has_mark(w):
    nfd = unicodedata.normalize('NFD', w)
    return ''.join(c for c in nfd if unicodedata.category(c) != 'Mn') != w
def vi_ratio(path, keys, ref_note_key='note'):
    d = json.load(open(path, encoding='utf-8'))
    parts = [json.dumps(d.get('metadata', {}), ensure_ascii=False)]
    for r in d.get('rows', []):
        for k in keys:
            v = r.get(k)
            if isinstance(v, str): parts.append(v)
            elif isinstance(v, list): parts += [x for x in v if isinstance(x, str)]
        for ref in r.get(ref_note_key, []) or []:
            pass
        for ref in r.get('references', []) or []:
            if isinstance(ref.get(ref_note_key), str): parts.append(ref[ref_note_key])
    words = [w for w in re.findall(r'[A-Za-zÀ-ỹ]+', '\n'.join(parts)) if len(w) > 1]
    m = sum(1 for w in words if has_mark(w))
    return len(words), m, m / len(words) if words else 0
```

## Diacritic-only mode (strip-identity contract)

When the task says *"the ONLY difference between input and output must be diacritic
marks"*, the acceptance test is a **strip-identity check** on the full file text:

```python
import unicodedata
def strip(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = unicodedata.normalize('NFC', s)
    return s.replace('đ', 'd').replace('Đ', 'D')
```

`strip(input) == strip(output)`.  `đ→d` is folded in, so `dau`→`đậu` passes; all tones,
hooks, horns and breves strip away.

Rules that follow from the contract:

- **Follow the source's literal base letters, never the semantically-intended word.**
  The stripped source may itself be malformed; you may put dấu only on the letters
  present.  Restore `ban sinh` → `bản sinh` (NOT `bẩm sinh`), `Khain niệm` → `Kháin niệm`
  (NOT `Khái niệm`), `sot nhiet` → `sốt nhiệt` (NOT `sốc nhiệt`).  Never add/drop a
  letter or a space to "fix" it — report such lines to the requester as source-text
  anomalies instead.
- **Line endings and the trailing newline are part of the contract.**  `strip()` does not
  touch `\r`, so a CRLF→LF rewrite or an added/removed final newline prints MISMATCH
  while every dấu is correct.  Measure the source in BINARY first
  (`b.count(b'\r\n')`, `b.endswith(b'\n')`) and match it — see `scripts/normalize_eol.py`.
  Write output in binary or with explicit CRLF; don't rely on text-mode translation.
- **Keep the verifier pure.**  Run the mandated check from a script with no side effects
  (`scripts/strip_identity_check.py`) and report its raw stdout as the evidence.  Do EOL
  normalization in a separate fixer step — never inside the verifier.
- **The checker must print ALL differing positions grouped by line**, not just the first,
  or each run reveals one error and you loop N times.
- **Token audit to prove "nothing added/removed/reordered":** whitespace-split token
  counts of input and output must be equal; then list tokens that are identical in both
  and confirm each is legitimately unaccented (English titles/DOIs, `Dalton`, `axit`,
  `heo`, `gen`, `vi sinh`, `hòa tan`'s `tan`, `cạnh tranh`, `con đường`).  This is also
  how you catch words you forgot to restore.
- Numbers, units, PMIDs, DOIs, URLs, markdown table pipes and `\|` escapes stay
  byte-identical; keep the same line count and structure.
- Ambiguity is normal and the checker cannot arbitrate it: `Chế`/`Chẹn`, `sốt`/`sốc`,
  `bản`/`bẩm` all strip identically.  Choose by domain sense and say so in the report.

## Replacement-map mode — the mechanism that scales

Hand-editing line by line is for small files. For a whole document (or a batch of sibling
files) apply an **ordered whole-word / phrase replacement map to the ORIGINAL bytes**: numbers,
units, markdown, `\|` escapes, English, URLs and PMIDs are then untouched *by construction*,
so the only diff is the dấu you injected.

```python
import re
def sub_word(text, pat, repl):                       # whole-word, case-insensitive
    rx = re.compile(r'(?<![0-9A-Za-z_\u00c0-\u1ef9])' + re.escape(pat) +
                    r'(?![0-9A-Za-z_\u00c0-\u1ef9])', re.IGNORECASE)
    def f(m):
        s, r = m.group(0), repl
        if s[0].isupper() and r[0].islower():        # keep sentence-case
            r = r[0].upper() + r[1:]
        return r
    return rx.sub(f, text)

# read with io.open(..., encoding='utf-8', newline='') so CRLF / no-final-NL survive
for p, r in PHRASES: text = sub_word(text, p, r)     # phrases FIRST
for p, r in BARE:    text = sub_word(text, p, r)     # bare tokens SECOND
for a, b in POSTFIX: text = text.replace(a, b)       # exact-string repairs LAST
```

Two ordering rules — both fail **silently**: they print IDENTICAL while leaving text wrong.

1. **Longest / most-specific phrase first.** A shorter phrase that is a *substring* of a
   longer one must run after it, or it consumes the substring and the longer rule never
   matches. Real collisions (2026-10-13): `dong hoa hoc` before `hoa hoc`; `co dong nang` /
   `co nhiet do` before `dong nang` / `nhiet do`; `dai phan tu` and `so phan tu` before
   `phan tu`; `hieu qua` before `qua cao`; `muc bo sung` before `bo sung`; `chu ky ban`
   before `chu ky`.
2. **A phrase's OUTPUT can be re-mangled by a later bare rule.** `va cham`→`va chạm`, then
   bare `va`→`và` gives `và chạm`; `tinh bot`→`tinh bột`, then bare `tinh`→`tính` gives
   `tính bột`. Repair with a tiny exact-string POSTFIX pass after every other rule
   (`('và chạm','va chạm')`, `('tính bột','tinh bột')`).

**Never write a bare rule for a token that also occurs in English or identifiers.** Actual
corruption: bare `doi`→`đổi` rewrote the citation prefix `DOI:`; bare `co`→`có` would rewrite
the chemical `Cu-Co`; bare `to`→`tố` would rewrite English "to"; bare `U`→`Ủ` would rewrite
`500-1500 U/kg`. Keep `the`, `so`, `do`, `dai`, `dien`, `dong`, `mo`, `nong`, `dung`, `ban`,
`to`, `doi`, `khi` **phrase-only** (`the ky`, `so sanh`, `do thay doi`, `khi thai`, `yeu to`…),
and handle non-word headings with a literal `str.replace` (`U (Annealing)`→`Ủ (Annealing)`).
Bare rules are fine for tokens that never appear outside Vietnamese
(`nhiet`, `phan`, `nghien`, `thuoc`, `luong`, `quyet`, `hoat`, `thiet`…).

**Base `d` is ambiguous — `đ` or `d`.** The stripper folds `đ→d`, so every `d` needs a
decision: `do`→`độ`/`đo`, `dong`→`động`/`đông`, `dai`→`đại`/`dai`, `dac`→`đặc`, `dau`→`đầu`,
`de`→`để`, `don`→`đơn`, `duoc`→`được`/`dược`, `duc`→`đúc`. Resolve by domain sense. One
literal `đ` may also have SURVIVED stripping (`đai bac`→`đại bác`) — keep it, don't "fix" it.

Folder habit: look for a `.raw.*` sibling first — if the pipeline archives the pre-strip text
it is the authority for ambiguous senses. Read it; never write to it.

## Reference

- `references/ordered-replacement-map-session.md` — ordered phrase/bare/POSTFIX map: two-reading
  ambiguity table, ordering-collision catalogue, English/identifier casualties, QA allowlist,
  verification stdout (2026-10-13 batch of 3 markdown research notes).
- `references/ez80-groupA-groupD-session.md` — worked example: measured ratios,
  false-positive catalogue, verification queries, domain glossary.
- `references/md-notes-diacritic-only-session.md` — worked example of diacritic-only
  mode: source EOL/byte layout, the 2 mismatch fixes, source-anomaly catalogue
  (`Khain`, `ban sinh`, `nguy co`, `Bui sua`…), token-audit allowlist.
- `scripts/strip_identity_check.py` — pure verifier: strip-identity + layout diff +
  ALL differing positions with line numbers.  Usage: `python strip_identity_check.py DIR key1 key2`.
- `scripts/normalize_eol.py` — force outputs to the source's CRLF/trailing-newline state.
  Usage: `python normalize_eol.py SRC.md OUT.vn.md`.
- `scripts/sweep_unrestored_tokens.py` — post-verify QA sweep: flags Vietnamese words still
  left as plain ASCII, with an allowlist for legitimately unaccented remainders.
  Usage: `python sweep_unrestored_tokens.py DIR [stem ...]`.

## Pitfalls

- **HTTP writes: never send Vietnamese through `curl -d`.** On Windows git-bash the request BODY
  gets mangled — a `PATCH` of a card title stored `? ??ng h? sinh h?c` in the database
  (2026-09-23, KFlow card). `GET` via curl is fine; anything that WRITES dấu goes through a
  `write_file` script using `urllib.request` +
  `json.dumps(body, ensure_ascii=False).encode("utf-8")`. After the write, re-GET the field and dump
  it to a UTF-8 file to verify: the terminal rendering lies, the stored value does not.
- **Generated artifacts can arrive with 0% dấu — gate them BEFORE publishing/pushing.**
  Pipelines (cron + LLM) occasionally emit an entire article without dấu: 3 HTML files in Sep 2026
  (`nuclear-fusion-2tab.html`, `activated-carbon-2tab.html`, `ozone-water-treatment.html`). Cheap
  detector to run before any publish/upload/DB step:
  ```python
  import re, unicodedata
  def accent_ratio(txt):
      words = [w for w in re.findall(r"[A-Za-zÀ-ỹ]+", txt) if len(w) > 1]
      marked = sum(1 for w in words if unicodedata.normalize("NFD", w) != w)
      return marked / len(words) if words else 0.0
  # gate: ratio >= 0.15 (healthy Vietnamese prose = 0.55-0.80). ratio 0.00 -> REGENERATE,
  # do not publish, do not "add dấu later", do not silently skip without reporting.
  ```
  Name the source pipeline as the bug (model drift), not the downstream job that caught it.
- **Whole-file ratio lies.** Keys (`element`, `verification`), English citations,
  units (`g/L`, `mg/L`), and formulas are unaccented by design — whole-file ratio
  ~0.42–0.44 is normal even when VI-field ratio is ~0.60. Always report VI-field ratio.
- **Suspect-word scans false-positive.** `trong`, `sang`, `pha`, `thu`, `sau`,
  `nhu/loai/ngoai/hoa` hits are usually: `id` slugs (`fe-ket-tua-...`), `language`,
  English words (`phase`, `change`, `nitrate`), units (`CaCO3`), or already-accented
  words (`nhu cầu`, `quy hoạch`) matched by substring. Verify with word-boundary
  regex `(?<![A-Za-zÀ-ỹ])nhu(?![A-Za-zÀ-ỹ])` + 60-char context before editing.
- **EN allowlist needed** when hunting leftovers: `zeolit, struvite, verified,
  ferrous/ferric fragments (fecl, fepo), units (g/l, mg/l, mmol/l, mgp/l)` are not
  missing dấu.
- **Partial read → overwrite warning.** Re-read the whole file before overwriting;
  the write tool warns if the last read was paginated.
- **Markdown table separators are substring traps.** `'|---|---|---|'` CONTAINS
  `'|---|---|'` (and `'|---|---|---|\r\n'.count('|---|---|\r\n') == 1`), so
  `s.count('|---|---|\r\n')` over-counts and `s.replace(old, new, 1)` rewrites the WRONG
  table.  Anchor replacements on the unique header line
  (`'| Thành phần \| … |\r\n|---|---|'`) and assert on `split('\r\n')[i]` after the edit.
  A source may legitimately mix 2-column and 3-column separators between tables — copy
  each one verbatim, never "normalize" them to match.
- **The strip check is necessary but NOT sufficient — always run a second QA pass.**
  `strip(in)==strip(out)` only proves you added/dropped/reordered no *base letters*. A word
  you forgot (e.g. `chat` never mapped) or a wrong sense (`học` vs `hoc`) strips identically
  and still prints IDENTICAL. 2026-10-13: three files printed IDENTICAL on three consecutive
  runs while ~40 Vietnamese words were still plain ASCII — only a full re-read of the *output*
  plus a token sweep found them. Always: (1) re-read the output end-to-end, (2) run
  `scripts/sweep_unrestored_tokens.py`, (3) accept only known-legit remainders (`tinh bột`,
  `va chạm`, `ban đầu`, `bi nghiền`, `nghiên cứu`, `Trung Quốc`, `so sánh` — "so" carries no
  mark) and prefix-substring false positives (`quy` in `quyết`, `khu` in `khuỷu`, `kho` in
  `khoảng`, `so` in `soát`, `thuy` in `thuyết`).
- **Letter-count arithmetic can veto a semantically better word.** Base letters must match
  the source *count*: `cỗi` strips to `coi` (3 letters), so a source reading `gia co` must
  become `gia cố`, never the nicer `già cỗi`. Count the base letters of your candidate before
  committing it; when two candidate readings both strip correctly, pick the domain-appropriate
  one and say so in the report.
- **Assert before write.** Put the post-condition asserts (`lines[i] == '|---|---|'`)
  ahead of the `write()` call, so a failed assertion aborts with the files untouched
  instead of half-rewritten.
- **Sibling files with dấu are reference, not target.** Only touch files named in
  the task; leave other files in the same directory alone.

## Prevention — write WITH dấu from the first keystroke

- All new Vietnamese output (chat replies, HTML, markdown research files) MUST be authored WITH full diacritics from the start. Never draft unaccented Vietnamese intending to "add dấu later" — session lesson 2026-09-15: a full HTML master framework authored without dấu had to be rewritten (~45KB → ~81KB).
- Prefer `write_file` (UTF-8) for long Vietnamese HTML/MD. Do NOT compose large Vietnamese bodies inside `execute_code` raw strings — dấu get silently dropped there.
- After writing, spot-check with a quick accented-word count (`đến/được/điều/công ty/không/người/của/khủng hoảng/tuyển dụng/giao tiếp` must be >0 in a Vietnamese doc). If counts are ~0, the file lost dấu: rewrite the file, don't patch word-by-word.
- User rule (Quang): every deliverable touching Vietnamese carries full dấu — no exceptions for drafts, previews, or internal files.

## Verification checklist

- [ ] JSON parses after write; `rows` count unchanged; `id` order unchanged.
- [ ] pmid/doi/url/label/citation + digit sequences identical to raw backup.
- [ ] VI-field accented ratio ≥ 0.5, reported before/after with row counts.
- [ ] No backup (`.raw.json`) modified.

Diacritic-only mode additionally:

- [ ] `strip(input) == strip(output)` prints IDENTICAL for every file (raw stdout reported).
- [ ] Same line count as input; line endings (CRLF/LF) and trailing-newline state match.
- [ ] Whitespace-split token counts equal; identical-token audit reviewed (all legitimately
      unaccented); no added/removed/reordered word.
- [ ] Second QA pass done: output re-read end-to-end **and**
      `scripts/sweep_unrestored_tokens.py` run; every surviving ASCII token justified.
      IDENTICAL from the verifier alone is NOT proof the file is done.
- [ ] Never wrote dấu via echo/heredoc/curl — used `write_file` or `io.open(encoding='utf-8')`
      / binary writes only.
