# Vietnamese Legal & Regulatory Source Routing

Verified by direct use 03/10/2026 while researching Land Law / Civil Code
articles for a land-compensation dispute. Complements `vietnam-search-blocking.md`
(which covers commercial/product search) — this file covers **statutory retrieval**,
where a wrong number is a defective filing rather than a bad price.

## Source hierarchy

| # | Source | Role | Access notes |
|---|---|---|---|
| 1 | **vbpl.vn** (CSDLQG, Bộ Tư pháp) | **Authority for metadata + effectiveness status** | Renders via JS → must drive the DOM; no direct API hit |
| 2 | **luatvietnam.vn** | Full statute text **plus appended annexes** (`Phụ lục`), clean plain text | Renders JS. **Never guess the `<id>` in the URL** — a guessed id silently returns a *different* law. Take the URL from the search listing. |
| 3 | **datafiles.chinhphu.vn** | Official signed PDFs | Direct download, fastest for word-by-word comparison. URL pattern `/cpp/files/vbpq/<YYYY>/<MM>/<slug>.pdf`. `web_extract` reads the PDF directly. Keep a mirror in reserve — the same law was reachable on one host and returned empty on another in the same session. |
| 4 | **baochinhphu.vn · xaydungchinhphu.vn · chinhsachonline.chinhphu.vn** | News + Q&A articles that **quote decree and law articles verbatim** | Fastest route to an article's exact wording when the decree PDF is not directly reachable. Verified: NĐ 253/2026 art. 42 and NĐ 260/2026 arts. 4–5 were obtained in full from `baochinhphu.vn` articles. Quotes sit inside responses of provincial tax departments or ministry explainers — still verbatim, cite the decree, not the news site. |
| 5 | **vanban.chinhphu.vn** (`?pageid=27160&docid=<n>`) | **Metadata only** — số ký hiệu, ngày ban hành, ngày có hiệu lực, người ký, trích yếu | Never returns full text. Best single source for the effective-date field. See "Do not use for negatives" below. |
| 6 | **congbao.chinhphu.vn** | Công báo listing | Clean fallback when an article page is blocked |
| 7 | Ministry portals (`mst.gov.vn`, `vast.gov.vn`, `cema.gov.vn`) | Summary articles for Quyết định / Danh mục | Useful for verifying a decision's date and scope; not for verbatim text |
| 8 | thuvienphapluat.vn | Backup | Cloudflare blocks curl. **Article and consulting pages return `bot_blocked` to `web_extract`** — their full text is usually unreachable. Search snippets still prove a document *exists* but are **not text**: never quote from a `thuvienphapluat` snippet. |

## Long pages truncate — recover the omitted middle, never assume the list ended

Annexes (`Phụ lục`) are the substance of a Danh mục: 70 technologies, 100 products.
When a page is long, `web_extract` returns **head + tail** with the middle replaced
by `[… middle omitted …]`, and prints a footer giving the cache path and the exact
call to resume. **The full clean text is on disk.** Read it:

```
read_file(path="~/AppData/Local/hermes/cache/web/<domain>-<hash>.md",
          offset=<N>, limit=<M>)
```

Cost of skipping this: a 70-item annex silently reads as ~54 items, or a 100-item
annex as 44. Nothing errors. The numbered list just looks like it ended. Always
confirm the **last item number** against the count stated in the document's own
prose (e.g. "có 70 công nghệ", "gồm 100 sản phẩm") before treating a list as complete.

Worked instance 10/2026: QĐ 23/2026/QĐ-TTg — `web_extract` on the LuatVietnam page
gave Phụ lục I items 1–54 then jumped to 95–100. `read_file` on
`cache/web/luatvietnam.vn-2a2d06015e.md` at `offset=243` returned items 55–70, and
at `offset=373` returned Phụ lục II items 45–100.

## Do not use any single source to prove a negative

`vanban.chinhphu.vn` returned **NOT FOUND for Land Law 2024 (`31/2024/QH15`)** —
a document that verifiably exists and is in force. A negative from this portal
carries no information.

To conclude a document number **does not exist**, require agreement across
**≥3 genuinely independent** sources, and check what each actually indexes.
Verified negative: `85/2024/UBTVQH15` was absent from vanban.chinhphu.vn,
DuckDuckGo (which surfaced `85/2025` instead), LuatVietnam, and the Ministry of
Agriculture & Environment's own list of Land Law 2024 amending instruments
(Công văn 3669/BNNMT-QLĐĐ, 15/4/2026 — 11 laws + 5 resolutions, none from
UBTVQH15). Four sources, one conclusion.

## Effectiveness dates lie in the amending instrument

Land Law 2024 (`31/2024/QH15`) art. 252(1) as enacted says effective
**01/08/2024**. But art. 1(2) of **Law 43/2024/QH15** moved it to
**01/01/2025**. Citing the original date is an error.

Exceptions exist too — arts. 190 and 248 took effect 01/04/2024. Always record
exceptions when present.

**Always look for a consolidated version** (`Văn bản hợp nhất`) and prefer it.
Bidding Law 2023 is consolidated as `74/VBHN-VPQH` (signed 25/03/2026) — cite
that, not the 2023 original.

To check whether a statute still stands, search not only the statute but the
**list of instruments that amended it**. A statute's own text will not tell you.

## Keyword match ≠ scope match

Land Law 2024 art. 79(3) lists *"xây dựng công trình cấp nước, thoát nước,
bao gồm: **nhà máy nước**; trạm bơm nước…"*

That means **municipal water supply**, explicitly not private mineral-water
bottling. Invoking art. 79 for a private bottling plant **weakens your own
argument**. Read the definition or explanatory clause before relying on a
listed term.

## Clause names change between versions

Land Law 2024 art. 79 reads *"lợi ích **quốc gia, công cộng**"* — it **dropped
"quốc tế"** compared with art. 74 of the 2013 law. Quoting the older wording
from habit is a one-word error that weakens the cite.

## Superseded instruments in this area

- Land Law 2003 = **`13/2003/QH11`** (not `03/2003/QH11`, which is the
  **Accounting Law**)
- Land Law 2013 = `45/2013/QH13`
- Bidding Decree `24/2024/NĐ-CP` — **fully expired 04/08/2025**, replaced by
  `214/2025/NĐ-CP`; had itself been amended by `17/2025/NĐ-CP`
- Bidding Law = **`22/2023/QH15`** (not `43/2023/QH15`)
- Civil Code 2015 = `91/2015/QH13`, **never amended** — a claimed
  "Civil Code amendment 2025" does not exist; draft amendments remain at
  research stage

## Delegating statutory research

**Do not put candidate numbers in the subagent prompt.** It treats them as
premises and researches support for them. Give subject matter, date,
jurisdiction and the question. Add: *"If any number in this brief does not
match the full text, say so and give the correct one."* Require verbatim
quotation, and require an explicit list of what could **not** be verified —
that last section is what keeps unverified claims out of the filing.

In the measured session, briefs seeded with wrong numbers produced reports
opening with "5 of 5 assumptions are wrong — do not use verbatim" and
"2 of 3 assumptions are wrong". The instruction works.

## Historical-effect traps in Vietnamese land disputes

A transaction from 2005 is governed by the law **in force in 2005**, not the
current statute. Land Law 2003 art. 40(2) then allowed a private investor to
**negotiate directly** with landowners, expressly *"không phải thực hiện thủ
tục Nhà nước thu hồi đất, giao đất, cho thuê đất"* — so the absence of a
formal expropriation decision was **lawful at the time**, not a defect.

Citing the current law to condemn the old arrangement inverts the analysis.
Ground historical conduct in Civil Code 2015 art. 156(1): provisions do not
apply retroactively to completed acts.

Cross-check with the current law's transition article (Land Law 2024 art. 254,
six clauses) to see which stage a partly-completed 2005 case falls into.

Also note the arithmetic trap: the Civil Code 2015 applied to transactions
**from 01/01/2017**. Citing its art. 117/129 as a "shield" for a 2005 contract
is wrong unless the equivalent 2005 provision (Civil Code 2005,
`23/2005/QH11`) is verified first.

## One article can carry two effective dates

The `Điều khoản thi hành` article routinely splits itself, and the split is where
the practical deadline lives. Law 109/2025/QH15 (PIT) art. 29:

- **khoản 1** — statute effective **01/07/2026**
- **khoản 2** — provisions on income from business and from wages of *resident
  individuals* apply **from tax period 2026**
- **khoản 3** — names the old statute (`04/2007/QH12` plus its six amending laws)
  and gives the old law a *separate* death date, again 01/07/2026 for most
  matters but from tax period 2026 for wages

Reading only khoản 1 reports the wrong compliance deadline. Always read the whole
`Điều khoản thi hành`, including which clause of which repealed statute survives.

Same trap with grandfathering: QĐ 23/2026/QĐ-TTg replaced QĐ 38/2020/QĐ-TTg
**but** organisations already certified under the old list keep using it until the
expiry printed on their certificate. Two versions of the same Danh mục are legally
live at once. Check whether a replace clause has a transitional carve-out before
saying an old list is dead.

## Verified instrument set — high-tech / digital-industry tax incentives (checked 19/10/2026)

Recorded so this cluster is not re-researched. Numbers verified against primary or
official-portal sources; all in force at the check date.

| Số hiệu | Ban hành | Hiệu lực | Ghi chú |
|---|---|---|---|
| `109/2025/QH15` Luật Thuế TNCN 2025 | 10/12/2025 | 01/07/2026 | Replaces `04/2007/QH12` + 6 amending laws. Art. 5(2) digital-industry workforce, art. 5(3) high-tech workforce, art. 4(17)(18) S&T tasks, art. 9 brackets, art. 10 deductions |
| `133/2025/QH15` Luật Công nghệ cao 2025 | 10/12/2025 | 01/07/2026 | Replaces `21/2008/QH12`. 6 chapters. Art. 13 defines the workforce, arts. 11–12 define the qualifying R&D activity |
| `253/2026/NĐ-CP` NĐ hướng dẫn Luật Thuế TNCN | 30/06/2026 | 01/07/2026 | Art. 42 = the exemption mechanics. Also states 22 exempt-income cases |
| `260/2026/NĐ-CP` NĐ chi tiết Luật Công nghệ cao | 30/06/2026 | 01/07/2026 | Art. 4(3)(a) high-tech, art. 5(3)(a) strategic-tech personal relief. Replaces `10/2024/NĐ-CP` |
| `353/2025/NĐ-CP` NĐ chi tiết Luật Công nghiệp công nghệ số | 31/12/2025 | 01/01/2026 | Arts. 5–10 = the five workforce criteria groups. **This is the instrument that decides who qualifies** |
| `71/2025/QH15` Luật Công nghiệp công nghệ số 2025 | 14/06/2025 | 01/01/2026 | Arts. 11, 28, 29 effective earlier, 01/07/2025. 6 chapters, 51 articles. Art. 19 = attraction policy |
| `23/2026/QĐ-TTg` | 15/05/2026 | 01/07/2026 | Phụ lục I = 70 high technologies; Phụ lục II = 100 high-tech products. Replaces `38/2020/QĐ-TTg` with grandfathering |
| `21/2026/QĐ-TTg` | 30/04/2026 | 01/07/2026 | 10 strategic-technology groups; 30 strategic products (22 + 8). Replaces `1131/QĐ-TTg` of 12/06/2025 |

Statutes routinely referenced in this area but **not** verified in that pass:
`354/2025/NĐ-CP` (khu công nghệ số tập trung) — confirm before citing.
`211/2026/NĐ-CP` (livestock/feed administrative penalties) and `253/2026/NĐ-CP`
are different instruments in different domains despite overlapping ordinal years.

## Snippet-only documents must be flagged, never quoted

Some instruments are known only from a search-result description because every
full-text host blocks automated reads. Worked instance: `16763/HYE-QLDN2` dated
10/09/2026, a provincial tax department guidance letter — the number and date came
from a snippet, both LuatVietnam and ThuvienPhapluat article pages returned
`bot_blocked`.

Rule: a snippet proves **existence and metadata only**. State the number, say it was
not read in full, and keep it out of the deliverable's source list. Do not paraphrase
its content, and do not quote it. Say which hosts were tried. Never let a snippet
become the load-bearing citation for a rule.

## Registration codes are not legal criteria

Do not infer entitlement from an enterprise's registered industry code, its sector,
or its job titles. Asked to confirm whether a data-analytics manager at a foreign
enterprise (registered code 6219) qualified for the 5-year personal-income-tax
exemption, the HCMC tax department cited NĐ 253/2026 art. 42 and told the taxpayer to
assess her **actual job content** against the Law on High Technology themselves.

The operative test always resolves to a named criteria instrument — here NĐ
353/2025 arts. 5–10, which quantify the test (revenue threshold, income as a multiple
of GDP per capita, university rankings, years of experience, Q1 publications,
ownership of a protected IP right). Find that instrument; do not reason from codes.
Consequence for drafting: whether an exemption applies is a three-part conjunctive
test — the *person* is qualifying workforce, the *activity* is qualifying R&D, and
the *technology* is on the Danh mục. Satisfying one part proves nothing.