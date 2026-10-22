"""Black-Scholes-Merton option pricing + Greeks + binomial convergence calculator.

Verified numbers (2026-08-02), base case S=100, K=100, T=1y, r=5%, sigma=20%:
  Call = 10.4506, Put = 5.5735; put-call parity holds exactly.
  Greeks: dC +0.6368, dP -0.3632, Gamma 0.0188, Vega 0.3752/1vol%, Theta -0.0176/day, Rho 0.5323/1%.
  CRR binomial n=500 -> 4bp error vs BS (convergence proof for cards).

Usage: python black_scholes_calc.py [S] [K] [T] [r] [sigma]
"""
import sys
from math import log, sqrt, exp, erf, pi


def N(x):
    return 0.5 * (1 + erf(x / sqrt(2)))


def phi(x):
    return exp(-0.5 * x * x) / sqrt(2 * pi)


def bs(S, K, T, r, sigma, q=0.0):
    """Black-Scholes-Merton price + Greeks. q = continuous dividend yield (0 default)."""
    if T <= 0 or sigma <= 0:
        return None
    d1 = (log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    call = S * exp(-q * T) * N(d1) - K * exp(-r * T) * N(d2)
    put = K * exp(-r * T) * N(-d2) - S * exp(-q * T) * N(-d1)
    delta_c = exp(-q * T) * N(d1)
    delta_p = exp(-q * T) * (N(d1) - 1)
    gamma = phi(d1) * exp(-q * T) / (S * sigma * sqrt(T))
    vega = S * exp(-q * T) * phi(d1) * sqrt(T)  # per 1.0 vol unit
    theta_c = (-S * phi(d1) * sigma * exp(-q * T) / (2 * sqrt(T))
               - r * K * exp(-r * T) * N(d2) + q * S * exp(-q * T) * N(d1)) / 365  # per day
    rho_c = K * T * exp(-r * T) * N(d2)  # per 1.0 rate unit
    return dict(d1=d1, d2=d2, call=call, put=put, delta_c=delta_c, delta_p=delta_p,
                gamma=gamma, vega=vega, theta_c=theta_c, rho_c=rho_c)


def binomial_european_call(S, K, T, r, sigma, n):
    """CRR binomial tree, European call. Converges to BS as n -> inf."""
    dt = T / n
    u = exp(sigma * sqrt(dt))
    d = 1 / u
    p = (exp(r * dt) - d) / (u - d)
    disc = exp(-r * dt)
    call = [max(S * (u ** (n - i)) * (d ** i) - K, 0.0) for i in range(n + 1)]
    for j in range(n - 1, -1, -1):
        for i in range(j + 1):
            call[i] = disc * (p * call[i] + (1 - p) * call[i + 1])
    return call[0]


if __name__ == '__main__':
    S, K, T, r, sigma = 100.0, 100.0, 1.0, 0.05, 0.20
    if len(sys.argv) == 6:
        S, K, T, r, sigma = (float(x) for x in sys.argv[1:6])
    res = bs(S, K, T, r, sigma)
    print(f"S={S}, K={K}, T={T}y, r={r:.2%}, sigma={sigma:.0%}")
    print(f"Call = {res['call']:.4f} | Put = {res['put']:.4f}")
    print(f"Put-Call Parity: C-P = {res['call'] - res['put']:.4f} vs S-K*e^-rT = {S - K * exp(-r * T):.4f}")
    print(f"d1={res['d1']:.4f} d2={res['d2']:.4f} | N(d2)={N(res['d2']):.4f} (risk-neutral ITM prob)")
    print(f"Greeks: dC={res['delta_c']:.4f} dP={res['delta_p']:.4f} Gamma={res['gamma']:.4f} "
          f"Vega={res['vega'] / 100:.4f}/1vol% Theta={res['theta_c']:.4f}/day Rho={res['rho_c'] / 100:.4f}/1%")
    print("Binomial convergence vs BS:")
    for n in [10, 50, 100, 500]:
        b = binomial_european_call(S, K, T, r, sigma, n)
        print(f"  n={n}: {b:.4f} (err {abs(b - res['call']) * 10000:.1f} bp)")
