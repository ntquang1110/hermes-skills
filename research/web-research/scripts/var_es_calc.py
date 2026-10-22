"""VaR & Expected Shortfall worked-example calculator (finance cards).

Computes the numbers that go into a KF "Value at Risk" card: historical /
parametric / Monte Carlo VaR, Expected Shortfall, Kupiec backtest, sqrt-10
scaling, and 2-asset diversification benefit, on a synthetic fat-tailed
return series (student-t df=4, fixed seed). All numbers verified 2026-08-03.

Run on Windows with:  py -3.11 var_es_calc.py
(plain `python` may resolve to 3.14 where numpy C-extensions are broken;
`py -0` lists installed versions.)

Requires numpy + scipy.
"""
import numpy as np
import scipy.stats as st

rng = np.random.default_rng(7)
n = 500          # 500 trading days
P0 = 10_000_000.0  # portfolio value ($10M)
z95 = st.norm.ppf(0.95)  # 1.645

# Synthetic "real" return series with fat tails: student-t df=4, ~1%/day vol
daily = rng.standard_t(df=4, size=n) * 0.008 + 0.0004
port = daily
mu, sigma = port.mean(), port.std()
print(f"mu={mu:.6f} sigma={sigma:.6f}")

# 1) HISTORICAL VaR (no distribution assumption)
hist_var = -np.percentile(port, 5)
print(f"HIST VaR95 = {hist_var*100:.3f}% = ${hist_var*P0:,.0f}")

# 2) PARAMETRIC (variance-covariance, normal assumption)
param_var = -(mu - z95 * sigma)
print(f"PARAM VaR95 = {param_var*100:.3f}% = ${param_var*P0:,.0f}")

# 3) MONTE CARLO (normal, same assumption as parametric)
sim = rng.normal(mu, sigma, 200_000)
mc_var = -np.percentile(sim, 5)
print(f"MC VaR95 = {mc_var*100:.3f}% = ${mc_var*P0:,.0f}")

# 4) EXPECTED SHORTFALL (historical tail mean + parametric closed form)
tail = port[port <= -hist_var]
es_hist = -tail.mean()
es_param = -(mu - sigma * st.norm.pdf(z95) / (1 - 0.95))
print(f"HIST ES95 = {es_hist*100:.3f}% = ${es_hist*P0:,.0f}")
print(f"PARAM ES95 = {es_param*100:.3f}% = ${es_param*P0:,.0f}")

# 5) KUPIEC BACKTEST: breaches of parametric VaR vs expected 5%
breaches = (port < -param_var).sum()
print(f"Breaches param = {breaches}/{n} = {breaches/n*100:.1f}% (expected 5%)")

# 6) sqrt-10 scaling (Basel 10-day horizon)
var10 = param_var * np.sqrt(10)
print(f"VaR95 10d = {var10*100:.3f}% = ${var10*P0:,.0f}")

# 7) 2-asset diversification: 60/40, correlation 0.305
z1 = rng.normal(0.0004, 0.008, n)
z2 = rng.normal(0.0002, 0.006, n)
r2c = 0.3 * (z1 - z1.mean()) / z1.std() * z2.std() + np.sqrt(1 - 0.3**2) * (z2 - z2.mean()) + z2.mean()
corr = np.corrcoef(z1, r2c)[0, 1]
w = 0.6
mu_p = w * z1.mean() + (1 - w) * r2c.mean()
sig1, sig2 = z1.std(), r2c.std()
sigma_p = np.sqrt(w**2 * sig1**2 + (1 - w)**2 * sig2**2 + 2 * w * (1 - w) * corr * sig1 * sig2)
varp = -(mu_p - z95 * sigma_p)
sigma_undiv = w * sig1 + (1 - w) * sig2
var_undiv = -(mu_p - z95 * sigma_undiv)
print(f"CORR={corr:.3f} sig_p={sigma_p*100:.3f}% varp={varp*100:.3f}%=${varp*P0:,.0f} "
      f"var_undiv={var_undiv*100:.3f}% benefit=${(var_undiv-varp)*P0:,.0f}")
