# Crossref Finance DOI Bank — Factor Investing / Asset Pricing (verified via Crossref API, Aug 2026)

Reusable verified DOIs for the 💰 Tài chính rotation group (CFA/Quant/M&A). All checked against `api.crossref.org` — reuse without re-verifying. Primary identifier is DOI (finance has no PMID).

## Core pattern — bibliographic search + DOI verification (Python)

```python
import urllib.request, json, ssl, urllib.parse, time
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE
UA = 'ResearchBot/1.0 (mailto:research@example.com)'

def crossref_query(query, rows=2, retries=4):
    url = 'https://api.crossref.org/works?rows=%d&query.bibliographic=%s' % (rows, urllib.parse.quote(query))
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=30)
            return json.loads(resp.read().decode())
        except Exception:
            time.sleep(3 * (attempt + 1))
    return {}

def get_doi(doi):
    url = 'https://api.crossref.org/works/' + urllib.parse.quote(doi)
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    resp = urllib.request.urlopen(req, context=ssl_ctx, timeout=30)
    return json.loads(resp.read().decode())
    # message.abstract (strip HTML) -> verify headline numbers, never quote from memory
```

- Query with `Author Year Title-fragment` → DOI + journal + year.
- Fetch abstracts by DOI for number verification (e.g. McLean–Pontiff 26%/58%).

## Verified DOI bank (12 papers)

| # | Paper | Journal/Year | DOI | Key numbers |
|---|-------|-------------|-----|-------------|
| 1 | Basu 1977 — Investment Performance of Common Stocks in Relation to Their Price-Earnings Ratios | JF 1977 | 10.1111/j.1540-6261.1977.tb01979.x | Value premium (P/E) first documented |
| 2 | Banz 1981 — The relationship between return and market value of common stocks | JFE 1981 | 10.1016/0304-405X(81)90018-0 | Size premium, 40+ years |
| 3 | Fama & French 1992 — The Cross-Section of Expected Stock Returns | JF 1992 | 10.1111/j.1540-6261.1992.tb04398.x | Beta insignificant once size+B/M controlled |
| 4 | Fama & French 1993 — Common risk factors in the returns on stocks and bonds | JFE 1993 | 10.1016/0304-405X(93)90023-5 | FF3 explains >90% vs CAPM ~70% |
| 5 | Jegadeesh & Titman 1993 — Returns to Buying Winners and Selling Losers | JF 1993 | 10.1111/j.1540-6261.1993.tb04702.x | Momentum 3–12mo positive, not from systematic risk |
| 6 | Carhart 1997 — On Persistence in Mutual Fund Performance | JF 1997 | 10.1111/j.1540-6261.1997.tb03808.x | 4-factor model + MOM, mutual fund evaluation standard |
| 7 | Ang, Hodrick, Xing, Zhang 2006 — The Cross-Section of Volatility and Expected Returns | JF 2006 | 10.1111/j.1540-6261.2006.00836.x | High idiosyncratic vol → abysmally low returns |
| 8 | Asness, Moskowitz, Pedersen 2013 — Value and Momentum Everywhere | JF 2013 | 10.1111/jofi.12021 | Consistent premia in 8 markets/assets; value–momentum negatively correlated |
| 9 | Fama & French 2015 — A five-factor asset pricing model | JFE 2015 | 10.1016/j.jfineco.2014.10.010 | Adds RMW+CMA; fails on small-stock high-investment pattern |
| 10 | Daniel & Moskowitz 2016 — Momentum crashes | JFE 2016 | 10.1016/j.jfineco.2015.12.002 | Crashes in panic states (after declines + high vol) |
| 11 | McLean & Pontiff 2016 — Does Academic Research Destroy Stock Return Predictability? | JF 2016 | 10.1111/jofi.12365 | 97 predictors: returns 26% lower OOS, 58% lower post-publication (32% from informed trading) |
| 12 | Asness, Frazzini, Pedersen 2019 — Quality minus junk | RAST 2019 | 10.1007/s11142-018-9470-2 | QMJ alpha (profitability, growth, safety, payout) |

## Query strings that resolve them one-shot
```
Fama French Common risk factors in the returns on stocks and bonds 1993
Carhart On Persistence in Mutual Fund Performance 1997
Jegadeesh Titman Returns to Buying Winners and Selling Losers 1993
Fama French A five-factor asset pricing model 2015
Asness Moskowitz Pedersen Value and Momentum Everywhere 2013
Asness Frazzini Pedersen Quality Minus Junk 2019
Basu Investment performance of common stocks in relation to their price earnings ratios 1977
Banz The relationship between return and market value of common stocks 1981
Ang Hodrick Xing Zhang The cross-section of volatility and expected returns 2006
Daniel Moskowitz Momentum crashes 2016
McLean Pontiff Does academic research destroy stock return predictability 2016
```

## Pitfalls hit (tested Aug 2026)
- **Crossref 429 on rapid queries** → sleep 1–2s between calls + retry with `3*(attempt+1)` backoff. Retry succeeds; don't give up.
- **Lowercase / duplicate DOIs** — `10.1016/0304-405x(93)90023-5` vs uppercase; JSTOR `10.2307/2329112` vs Wiley `10.1111/j.1540-6261.1992.tb04398.x` for the same 1992 paper. Pick the journal-of-record (Wiley/JFE) DOI.
- **SSRN preprint surfaces first** (`10.2139/...`) — prefer the published journal version for citations.
- **Wikipedia Action API search misses modern factor names** — "quality minus junk" returns yield spread / credit rating / Maceo Plex. Crossref is the primary source for finance papers.

## Card conventions (finance topics in KF)
- Reference table uses **DOI as the identifier column** (no PMID exists in finance).
- Verify headline numbers against Crossref abstracts before quoting (e.g. McLean–Pontiff 26%/58%, Ang et al. IVOL finding, Asness 8-market claim).
- `topic_slug`: `tai-chinh` · emoji: 📈 for factor/quant, 💰/📜 for deals/valuation.
- Dedup against biology-heavy KB: use finance-specific phrases (`factor investing`, `nhân tố`, `smart beta`, `momentum`, `định giá`, `trái phiếu`) — short words like `factor`/`risk`/`alpha` collide with biology cards.

## Fixed Income / CFA DOI bank (verified Aug 2026 — Duration & Convexity card)

Verified via Crossref for CFA fixed-income topics (duration, convexity, term structure, credit/liquidity). Additive to the factor/quant bank above; both live in this file.

| # | Paper | Journal/Year | DOI | Key numbers |
|---|-------|-------------|-----|-------------|
| 1 | Macaulay 1938 — Some Theoretical Problems Suggested by the Movements of Interest Rates, Bond Yields and Stock Prices in the US since 1856 | NBER book | 10.2307/2143533 (book-review entry only) | Duration concept; cite as NBER book, no true DOI |
| 2 | Redington 1952 — Review of the Principles of Life-office Valuations | J. Inst. Actuaries | 10.1017/s0020268100052811 | Immunization concept |
| 3 | Fisher & Weil 1971 — Coping with the Risk of Interest-Rate Fluctuations | J. Business | 10.1086/295402 | Duration matching, naive vs optimal strategies |
| 4 | Vasicek 1977 — An equilibrium characterization of the term structure | JFE | 10.1016/0304-405x(77)90016-2 | Mean reversion; rates can go negative |
| 5 | Cox, Ingersoll, Ross 1985 — A Theory of the Term Structure of Interest Rates | Econometrica | 10.2307/1911242 | Square-root diffusion, non-negative rates |
| 6 | Hull & White 1990 — Pricing Interest-Rate-Derivative Securities | RFS | 10.1093/rfs/3.4.573 | No-arbitrage, fits observed curve |
| 7 | Litterman & Scheinkman 1991 — Common Factors Affecting Bond Returns | J. Fixed Income | 10.3905/jfi.1991.692347 | 3 factors ~98% of variance (level ~89%, steepness ~8.5%, curvature ~1%) |
| 8 | Bierwag, Kaufman, Toevs 1983 — Duration: Its Development and Use in Bond Portfolio Management | FAJ | 10.2469/faj.v39.n4.15 | Duration survey |
| 9 | Duffie & Singleton 1999 — Modeling Term Structures of Defaultable Bonds | RFS | 10.1093/rfs/12.4.687 | Reduced-form credit: discount at r + intensity×LGD |
| 10 | Chordia, Sarkar, Subrahmanyam 2005 — An Empirical Analysis of Stock and Bond Market Liquidity | RFS | 10.1093/rfs/hhi010 | Common liquidity across stock+bond markets |
| 11 | Gürkaynak, Sack, Wright 2007 — The U.S. Treasury yield curve: 1961 to the present | JME | 10.1016/j.jmoneco.2007.06.029 | Nelson-Siegel dataset, non-parallel shifts |
| 12 | Greenwood & Vayanos 2014 — Bond Supply and Excess Bond Returns | RFS | 10.1093/rfs/hht133 | Supply → expected excess returns |

### Pitfalls hit 2026-08-01 (fixed income verify)
- **⚠️ DOI collision — always verify DOI → title before citing.** `10.1093/rfs/hht033` resolves to "Capturing Option Anomalies with a Variance-Dependent Pricing Kernel" (2013), NOT Greenwood-Vayanos. Correct: `10.1093/rfs/hht133`. Bibliographic search surfaced the wrong RFS DOI first. Rule: after getting a candidate DOI, GET `https://api.crossref.org/works/<doi>` and confirm the title matches before putting it in a card.
- **SSRN preprint surfaces first** for Chordia (`10.2139/ssrn.289219`) and Gürkaynak (`10.2139/ssrn.920183`) — always prefer the published journal version (RFS/JME) for citations.
- **Macaulay 1938 has no true DOI** — it's an NBER book; Crossref's top hit is a book review in Political Science Quarterly. Cite as NBER book and flag the DOI as review-only.
- **Crossref 429 on rapid queries**: verified sleep 2s between calls + `4*(attempt+1)` backoff; retries succeed (matches the factor-bank pattern).

### Worked-example technique (finance cards)
Compute duration/convexity numbers directly with Python rather than quoting from memory — cards then carry real worked tables. Numbers for a 5y 5% coupon bond at YTM 5% (verified 2026-08): Macaulay 4.546y, ModDur 4.3295, convexity 23.936; ±200bp duration-only errs ~0.5% vs actual, adding convexity matches almost exactly. Zero-coupon 5y Macaulay = exactly 5.000. Script: `scripts/duration_convexity_calc.py`. ⚠️ Cash-flow list must be `[coupon]*(N-1) + [coupon+face]` — a `[coupon]*N + [coupon+face]` list zipped against `range(1,N+1)` silently truncates the final principal payment and produces a garbage price (~21.6 instead of 100).

## Options / Derivatives DOI bank (verified Aug 2026 — Black-Scholes & Greeks card)

Verified via Crossref for CFA derivatives topics (options pricing, Black-Scholes-Merton, Greeks, binomial/CRR, stochastic vol). Additive to both banks above.

| # | Paper | Journal/Year | DOI | Key numbers |
|---|-------|-------------|-----|-------------|
| 1 | Black & Scholes 1973 — The Pricing of Options and Corporate Liabilities | JPE 1973 | 10.1086/260062 | BS formula + PDE; equity as call on assets |
| 2 | Merton 1973 — Theory of Rational Option Pricing | Bell J. Econ. 1973 | 10.2307/3003143 | General rational pricing, dividends |
| 3 | Merton 1976 — Option pricing when underlying stock returns are discontinuous | JFE 1976 | 10.1016/0304-405X(76)90022-2 | Jump-diffusion, fat tails |
| 4 | Black 1976 — The pricing of commodity contracts | JFE 1976 | 10.1016/0304-405X(76)90024-6 | Black formula for futures/commodity options |
| 5 | Cox, Ross, Rubinstein 1979 — Option pricing: A simplified approach | JFE 1979 | 10.1016/0304-405X(79)90015-1 | Binomial model, backward induction |
| 6 | Breeden & Litzenberger 1978 — Prices of State-Contingent Claims Implicit in Option Prices | J. Business 1978 | 10.1086/296025 | Risk-neutral PDF from option prices (2nd deriv of call vs strike) |
| 7 | Garman & Kohlhagen 1983 — Foreign currency option values | JIMF 1983 | 10.1016/S0261-5606(83)80001-1 | FX options, two interest rates |
| 8 | Heston 1993 — A Closed-Form Solution for Options with Stochastic Volatility | RFS 1993 | 10.1093/rfs/6.2.327 | Stochastic vol, matches smile |
| 9 | Gatheral 2006 — The Volatility Surface: A Practitioner's Guide | Wiley 2006 | 10.1002/9781119202073 | Vol surface practice |

### Pitfalls hit 2026-08-02 (options verify)
- **⚠️ DOI collision on Breeden-Litzenberger**: `10.1086/260795` does NOT resolve to Breeden-Litzenberger — it is "Unemployment, Justice, and Keynes's General Theory" (JPE 1979). Correct: `10.1086/296025`. Always confirm title after DOI lookup.
- **⚠️ Garman-Kohlhagen 404**: `10.1016/0261-5606(83)90001-1` returns HTTP 404 (wrong segment). Correct: `10.1016/S0261-5606(83)80001-1` (note leading `S` and `80001-1`). Bibliographic search (`Foreign currency option values 1983`) resolves it first try.
- **Crossref 429 on bibliographic search**: `query.bibliographic` 429s after a couple of rapid calls; retry with `3*(attempt+1)` backoff succeeds (same pattern as the other banks).
- **Bibliographic search beats DOI guessing**: when a DOI guess fails, `query.bibliographic` returns the right paper + DOI in the first 1-2 rows. Use it instead of guessing DOI patterns.

### Worked-example numbers (Black-Scholes & Greeks, verified 2026-08-02)
Script: `scripts/black_scholes_calc.py`. Base case S=100, K=100, T=1y, r=5%, σ=20%: Call = 10.4506, Put = 5.5735; put-call parity holds exactly (C−P = 4.8771 = S − K·e^(−rT)); d1=0.350, d2=0.150 → N(d2)≈0.56 (risk-neutral ITM prob). Greeks: Δcall +0.6368, Δput −0.3632, Γ 0.0188, Vega 0.3752 per 1 vol%, Θ −0.0176/day, ρ 0.5323 per 1%. Δ-approx check: S+1% → actual +0.646 vs Δ·1 = +0.637 (gamma explains the gap). Binomial CRR converges to BS: n=10 → 197bp err, n=500 → 4bp err. Vol sensitivity: σ=15% → call 8.59; σ=25% → call 12.34. ITM/OTM: K=90 call 16.70 Δ0.81; K=110 call 6.04 Δ0.45.

## Risk Management (VaR & Expected Shortfall) DOI bank (verified Aug 2026 — VaR card)

Verified via Crossref for CFA risk-management topics (VaR, ES/CVaR, backtesting, Basel/FRTB). Additive to the factor, fixed-income, and options banks above. All 9 DOIs checked against `api.crossref.org` 2026-08-03.

| # | Paper | Journal/Year | DOI | Key numbers |
|---|-------|-------------|-----|-------------|
| 1 | Markowitz — Portfolio Selection | JF 1952 | 10.2307/2975974 | Covariance foundation: portfolio risk = wᵀΣw |
| 2 | Engle — ARCH | Econometrica 1982 | 10.2307/1912773 | Time-varying volatility |
| 3 | Bollerslev — GARCH | J. Econometrics 1986 | 10.1016/0304-4076(86)90063-1 | GARCH(1,1) |
| 4 | J.P. Morgan — RiskMetrics Technical Document | tech doc 1996 | (no DOI — cite as tech doc) | Popularized variance-covariance VaR |
| 5 | Kupiec — Techniques for Verifying the Accuracy of Risk Measurement Models | J. Derivatives 1995 | 10.3905/jod.1995.407942 | POF backtest |
| 6 | Duffie & Pan — An Overview of Value at Risk | J. Derivatives 1997 | 10.3905/jod.1997.407971 | Academic standardization of VaR |
| 7 | Hull & White — VaR When Daily Changes in Market Variables are not Normally Distributed | J. Derivatives 1998 | 10.3905/jod.1998.407998 | Normal assumption understates tail risk |
| 8 | Artzner, Delbaen, Eber, Heath — Coherent Measures of Risk | Math. Finance 1999 | 10.1111/1467-9965.00068 | VaR not subadditive → ES is coherent |
| 9 | Glasserman — Monte Carlo Methods in Financial Engineering | Springer 2003 | 10.1007/978-0-387-21617-1 | MC reference for VaR simulation |
| 10 | Danielsson — The Emperor Has No Clothes: Limits to Risk Modelling | J. Banking & Finance 2002 | 10.1016/s0378-4266(02)00263-7 | Model risk; regime shifts break models |

### Worked-example numbers (VaR & ES, verified 2026-08-03)
Script: `scripts/var_es_calc.py`. Portfolio $10M, 500 days synthetic fat-tailed returns (student-t df=4, σ≈1.03%/day, seed 7). Historical VaR95 1-day = 1.910% = $191,016; Parametric (normal) = 1.751% = $175,079 (understates due to fat tails); MC normal 200k scenarios = 1.752%; Historical ES95 = 2.460% = $246,002; Parametric ES = 2.183%. Kupiec backtest: parametric VaR breached 28/500 = 5.6% (expected 5%). sqrt-10: VaR95 10-day = 5.536% = $553,649. 2-asset 60/40 (corr 0.305): σ_p = 0.607%, VaR $99,438 vs non-diversified 1.198% → diversification benefit $20,407 (~17%). Didactic arc for the card: fat tails → parametric < historical; ES > VaR (~29%); Basel FRTB moved from VaR 99% to ES 97.5%.

### Pitfalls hit 2026-08-03 (VaR verify + calc)
- **⚠️ Windows `python` may resolve to Python 3.14 with broken numpy** — on this box `python` → C:\Python314 (numpy C-extensions compiled for cp311 → ImportError at import; scipy unusable). `py -3.11` resolves the working interpreter (numpy 2.4.3 + scipy OK). Rule for numpy/scipy calc scripts here: run `py -3.11 script.py`, not `python script.py`. Check with `py -0` to list installed versions.
- **⚠️ Student-t scaled to the same σ has a SMALLER 5% quantile than normal** (t₄ z₀.₀₅ ≈ −1.51 vs normal −1.645 after std-normalization, because the t peak is higher). Do NOT demo "fat tails → bigger VaR" with MC student-t vs normal at 95% — it produces the opposite result and confuses readers. Use the Historical vs Parametric contrast instead (historical VaR > parametric on fat-tailed data), and reserve student-t for ES / 1%-tail comparisons where it behaves as expected.
- **Kupiec breach rate is a useful didactic signal**: parametric VaR on fat-tailed data gives a breach rate above the 5% expectation (28/500 = 5.6%) — points at model understatement without needing formal rejection.
- **Dedup for the finance rotation**: by Aug 2026 the KF already had Factor Investing, Black-Scholes, Duration & Convexity, Deal Architecture, and Patent Valuation cards. VaR/ES filled the CFA Risk bucket — the natural next gaps after these are Portfolio Theory/Markowitz, Term Structure/Yield Curve, and Statistical Arbitrage.
