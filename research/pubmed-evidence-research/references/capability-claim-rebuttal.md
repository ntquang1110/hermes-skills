# Rebutting a CAPABILITY claim with structural evidence

Method for the class of question where the user asserts a **capability** ("a device inside the
body reads cell signals", "we can learn each person's pathway", "this detects the problem's
location") rather than asking about an event or a fact. The answer must be argued with
**structure, not opinion** — otherwise it reads as the assistant's pessimism and gets ignored.

Verified 18/10/2026 on the fixgby question *"device nằm trong cơ thể đọc tín hiệu tế bào bằng
cách nào, và làm sao biết VẤN ĐỀ ĐANG NẰM Ở ĐÂU trong cơ thể của từng người?"*. Evidence bank for
that case: `references/invivo-biosensor-resolution-layers.md`.

## The 4 steps

### 1. Record the NEGATIVE queries as evidence
Do not write "no source found". Run **N independent queries**, log all N, then write
`KHÔNG TÌM THẤY`. The count of negative queries **is the finding** — it proves the absence was
tested, not assumed. Distinguish where each positive-but-irrelevant hit actually lives.

Worked case: 6 queries (S6a–S6f) for intracellular molecular sensing in-vivo in humans → 0
qualifying hits. Every positive-looking result (nanopipette papers, PMIDs 32542257 / 39821328)
was **in cultured cells**, i.e. grade (R) — not in-vivo. Writing that mapping down converts a
vague "doesn't exist" into a defensible claim.

### 2. Quantify the gap in ORDERS OF MAGNITUDE, with the criterion stated first
Adjectives ("still far", "not yet", "very early") are forbidden in this argument. State the
measuring criterion explicitly, then compute log₁₀ against it, so a reader can re-check the
arithmetic.

Worked case, criterion = *number of cells represented by ONE reported number*:
- CGM (continuous glucose monitor) → 10⁵–10⁷ cells per number ⇒ **5–7 orders** from a single cell
- whole-body wearable → 3.72 × 10¹³ cells per number (Bianconi, PMID 23829164) ⇒ **13.6 orders**
- cfDNA tissue deconvolution → 29 tissue types (cfSort, PMID 37399400) ⇒ **≈12.1 orders**, and it
  **cannot improve further** — bounded by how many tissues have distinct methylation profiles

That last clause matters: a ceiling that is *structural* is a different fact from a ceiling that
is merely current.

### 3. Separate ENGINEERING distance from MATHEMATICAL distance ← the decisive step
An engineering gap closes with money, people and time. A mathematical gap never closes. Telling
the user which one they are looking at changes the decision completely, so hunt for the
impossibility proof explicitly — search terms like *structural identifiability*, *non-identifiability*,
*parameter identifiability*, plus the network name.

Worked case: **PMID 19426527** (BMC Syst Biol 2009) proves signaling networks
(JAK-STAT / MAPK / NF-κB) are **"NOT IDENTIFIABLE even under the strong assumption that ALL system
state variables are measurable."** Since that is the ideal condition no instrument reaches, no
amount of extra instrumentation closes the gap. Supporting identifiability reviews:
PMIDs 27792726, 22132135, 29186132, 30472690.

Consequence for deliverables: a reduced, axis-limited model with recorded uncertainty is the
*honest* ceiling — not a temporary compromise awaiting better sensors.

### 4. Grade capability research on (I)/(A)/(R), not Mạnh/Vừa/Sơ bộ
For devices and methods, the useful axis is where the thing physically exists:
- **(I)** already commercial / already done **on humans**
- **(A)** done on **large animals** (non-human primate, pig, dog)
- **(R)** in-vitro / in-silico only

Write all three even when two are empty — `(I) KHÔNG TỒN TẠI` is a result, and it is the one that
carries the argument. (The Mạnh/Vừa/Sơ bộ axis stays for compound×effect rows.)

## Two supporting moves

**Split the axes before concluding.** A capability is often genuinely achieved on one axis and
entirely absent on another; concluding without naming the axis produces a misleading verdict.
Worked case: the ELECTRICAL axis has truly reached **0 orders** on humans (Neuropixels,
685 neurons, PMID 38093008) — while the MOLECULAR-INTRACELLULAR axis has **0 layers existing at
all**. Therefore "we can already read cellular signals in humans" is *technically true and
semantically false* if read as "we know what the cell is doing biochemically." Say it that way.

**Check for peer review as a fact, not a fallback.** If a capability ships publicly, it should
have peer-reviewed human data. Its absence is itself a citable finding — state it plainly instead
of reaching for a weak source. Worked case: Neuralink has **no peer-reviewed human publication**
at all (company updates + ClinicalTrials.gov registry only), so the deliverable records exactly
that rather than citing promotional material.

## Pitfalls

- **Don't let the negative result be silent.** An undocumented "not found" reads as sloppy
  searching; a logged 6-query negative with each near-miss graded (R) reads as proof.
- **Don't stop at the technical gap.** Users proposing a vision respond to *"this is an engineering
  problem, here's the ladder"* and to *"this is mathematically impossible, here's the proof"* very
  differently. Confusing the two either kills a feasible project or funds an impossible one.
- **Give the feasible fallback in the same breath.** Naming only the impossibility is unhelpful;
  pair it with the highest layer actually reachable and how to buy it (here: CGM for the continuous
  axis + cfDNA for tissue coordinates, both commercial today).
- **Never invent a cost figure.** Scale-of-trial is a valid sourced proxy for cost when dollar
  amounts have no source (e.g. "Layer 4 needs 304 patients / 37 centres / 6 countries / 2 years" —
  PMID 41929392). Unsourced money gets written `CHƯA CÓ NGUỒN (tag H)`.
