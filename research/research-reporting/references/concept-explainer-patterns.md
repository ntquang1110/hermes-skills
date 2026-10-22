# Concept Explainer Patterns

Two formats for requests that are NOT "research a topic" but "explain a body of
knowledge so I actually understand it". Distilled from two sessions: a 37-term biology
glossary, and a "why does the same C/H/O formula behave completely differently" explainer.

Both shipped as single-file Say Briefly HTML, published to preview, verified HTTP 200 +
diacritics + mojibake 0. Both were structured, not listed. The structure IS the value.

## Meta-rule that matters most: correct the premise first

When the user asks a "why does X cause Y" question, check whether the premise is right
before answering it. Twice this proved to be the single highest-value move:

- **"Why does adding more C, H, O change the structure completely?"** → The stronger true
  answer is that **identical** atom counts still behave completely differently. The
  quantity framing is wrong; the arrangement is what matters. Say so in the first line,
  then prove it.
- **"Explain all the biology terms, e.g. protein, enzyme, cytokine."** → The implicit
  premise is that they are a flat list to be memorised. They are a **six-tier stack**
  where lower tiers are the substrate for upper tiers. Reorganising is the answer.

Lead with the correction. It is not pedantry when it changes the whole shape of the
explanation. Label it plainly ("Sửa lại giả định trước") and keep it to a few lines.

## The four-question card schema

For any glossary / term / entity explainer, every single entry answers the same four
questions in the same order. This is the reusable core:

| Field | Question it answers |
|---|---|
| **Nằm ở đâu** | Location. Where in the body/cell/system. |
| **Cơ chế** | Mechanism. How it does its job, mechanically. |
| **Tại sao có** | Why it exists. What problem it solves. |
| **Thiếu thì sao** | Consequence of absence or malfunction. |

Order matters: location first, because in biological systems *location determines
capability*. "Tại sao có" is the deepest field — the entity exists to solve a specific
problem, and understanding the problem removes the need to memorise the structure. Tell
the user this explicitly; it is the thing that makes the format reusable for them later.

Render as a card: header with number + Vietnamese name + English term in mono caps, then
four labelled rows, with the "thiếu" row tinted red (`background:rgba(179,0,0,.035)`,
label colour `--red`) so consequence reads differently from description.

## Pattern L — Tiered concept glossary

Trigger: "list cho anh toàn bộ thuật ngữ X", "giải thích cho anh ... Và tại sao."

Section order:

1. **Cách đọc bản đồ này** — state the organising principle (tiers, not alphabet) and
   the consequence ("hỏng tầng dưới kéo sập tầng trên"). Include the tier grid here as a
   2×3 or 3×2 `.cm-grid` of colour-coded zone boxes.
2. **Bản đồ không gian** — a spatial map BEFORE the terms. For biology this was an
   abstracted 8-zone cell grid (màng ngoài / bào tương / ty thể / lưới nội chất / Golgi /
   lysosome / nhân / ngoài tế bào), each zone naming which structures live there. Rationale
   to include: "vị trí quyết định chức năng".
3. **One section per tier**, each with its term cards, prefaced by a table that separates
   confusable categories before the detail (e.g. hormone vs cytokine vs neurotransmitter
   vs growth factor: ai gửi / đi đường nào / tới ai).
4. **Chain diagram per tier** where a one-way dependency exists (DNA → gen → RNA → acid
   amin → protein → enzyme). Use the `.flow` / `.fn2` chip pattern with `<small>` sub-labels.
5. **Bảng tra nhanh** — every term, one line each: term | English | tier | one sentence.
   This is what makes it a reference rather than an essay.
6. **N điểm chính** as an `<ol>`, each point carrying a number or a verbatim claim.
7. **Kết** — close on a cross-cutting pattern, NOT a summary. See below.

### Closing on a pattern instead of a summary

The glossary's value doubled by ending on an observation that holds across every entry:

> Hầu hết cơ chế sinh học đều có hai chiều đều gây bệnh. Hormone thiếu hoặc thừa.
> Cytokine thiếu hoặc bão. Miễn dịch quá nhạy hoặc quá kém.

Then the reframe that follows from it: the right question is not "is this good or bad" but
"where is the equilibrium, and how does the body adjust". Look for this kind of
cross-cutting invariant while writing; it is worth more than any single entry.

### Ground each tier back in the user's own operation

Generic biology stays generic. Where a mechanism touches the user's actual business,
say so in the "thiếu" row. Two that landed:

- Thụ thể nhận dạng mẫu (TLR) triggered continuously by endotoxin in shed dust / mouldy
  feed → chronic inflammation → energy drain → reduced weight gain despite adequate
  intake. This turns "clean the shed" from a hygiene slogan into a productivity mechanism.
- Thiếu coenzyme (vitamin B group) → enzyme present but non-functional → reduced feed
  conversion. Same pattern: the feed is adequate, the machinery is not.

This is what converts an educational document into something they use.

## Pattern M — Same-formula / different-structure explainer

Trigger: "tại sao chỉ khác nhau về số lượng mà cơ chế khác được", "cùng công thức mà
khác hoàn toàn".

Section order (this one has a strong narrative spine — follow it):

1. **Correct the premise**, then state the one-liner: formula = alphabet, structure =
   sentence.
2. **The single sharpest example first.** For C/H/O this is C2H6O:
   ethanol (bp +78 °C, drinkable) vs dimethyl ether (bp −25 °C, propellant). Same nine
   atoms, one different bond. **A 100 °C boiling point gap from a single connectivity
   change** is the most persuasive number available, and it comes with a clean mechanism:
   donor count 1 vs 0, so ethanol hydrogen-bonds and the ether cannot. Put this in a
   2-column comparison table, not prose.
3. **The four isomerism types**, one worked example each:
   - connectivity (C3H6O: acetone / propanal / propylene oxide)
   - position (theophylline vs theobromine — same formula, same MW, same complexity
     value, one methyl in a different position; one is an asthma drug, one is the
     chocolate alkaloid)
   - stereochemistry (thalidomide; note the enantiomers **interconvert in vivo**, so
     purifying one does not make it safe)
   - oxidation state (OH vs =O vs COOH from the same C and O)
4. **The strongest evidence section: glucose vs galactose.** Both C6H12O6, and PubChem
   reports *identical* XLogP (−2.6), TPSA (110), H-bond donors (5), acceptors (6) and
   complexity (151). Only the 3D arrangement of one OH differs. The biology is completely
   different (fuel vs a separate GALT-dependent pathway; GALT deficiency = galactosemia).
   Nothing was added or removed, every measured property matches, and the body treats them
   as different substances. Then generalise: **the body does not read formulas, it reads
   shapes.**
5. **The mechanism section** — why shape is readable: target sites are 3D pockets; binding
   is geometric plus chemical complementarity; then the three recognition layers (shape,
   functional group, chirality — pockets are themselves chiral because they are built from
   chiral amino acids).
6. **Clinical case with a one-atom delta** — morphine vs codeine: one CH3 caps a
   phenolic OH, donor count 2 → 1, and codeine becomes a **prodrug** requiring CYP2D6 to
   unmask it. Then the pharmacogenomic consequence: poor metabolisers get no analgesia,
   ultra-rapid metabolisers risk toxicity. This is where "one methyl changes everything"
   stops being a slogan.
7. **The combinatorial closer** — why adding atoms adds *information*, not mass. Carbon
   bonds four ways and can chain, branch and ring, so isomer counts explode:

   | Ankan | Formula | Isomers |
   |---|---|---|
   | Butan | C4H10 | 2 |
   | Octan | C8H18 | 18 |
   | Hexadecan | C16H34 | 10,359 |
   | Triacontan | C30H62 | 4,111,846,763 |

   4.1 billion compounds sharing one formula, before introducing a single heteroatom.
8. **Kết — land it on the user's own practice.** For dược liệu: avicularin and
   guaijaverin are both quercetin + arabinose (different sugar ring form), berberine and
   palmatine are close analogues. Therefore **quantifying one and inferring the other is
   invalid by principle** — each needs its own reference standard. This is a real
   analytical constraint, not a rhetorical flourish.

### PubChem fetch for isomer pairs

One call gets everything needed for the comparison tables:

```
https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/<CID1>,<CID2>/property/MolecularFormula,MolecularWeight,XLogP,TPSA,HBondDonorCount,HBondAcceptorCount,Complexity/JSON
```

CIDs used: ethanol 702, dimethyl ether 8254, acetone 180, propanal 527, propylene oxide
6378, theophylline 2153, theobromine 5429, caffeine 2519, morphine 5288826, codeine 5284371,
thalidomide 5426, glucose 5793, galactose 6036, fructose 2723872.

**Pitfall:** `CanonicalSMILES` in the property list returned HTTP 400 on some CIDs — drop it
if the request fails; the numeric properties above are sufficient for the tables.

## Verification (both patterns)

```python
src = open(path, encoding='utf-8').read()
cjk = [c for c in src if '\u4e00' <= c <= '\u9fff']       # must be empty
assert src.count('<div') == src.count('</div>')            # div balance
assert src.count('<section') == src.count('</section>')
assert src.count('<table') == src.count('</table>')
```

Then after publish, re-fetch and check diacritics present + mojibake 0 + `h1`/`section`/
`table` counts match local (catches a truncated upload).

**Pitfall — structural tags must match the wrapper.** When emitting comparison rows,
do not reach for `<tr>` inside a div-based pair structure; it produces an unbalanced tree
that renders as garbage and only shows up in the div count. This happened once while
building the C2H6O table; the fix was switching the row wrapper to `<div class="pr">` to
match the surrounding pair layout.

## Publish pitfall (MSYS on Windows, cwd on a different drive)

Running the payload helper with `~` from a `D:/` working directory resolves to
`D:\c\Users\...` and fails with "can't open file". **Use the fully qualified Windows path**:

```bash
python "C:/Users/<user>/AppData/Local/hermes/scripts/make_payload.py" in.html "Title" out.json
```

Also note the payload file must be written as UTF-8 with `ensure_ascii=False`, and the
POST must use `curl --data-binary @payload.json` (Python urllib gets 403 from the preview
API).
