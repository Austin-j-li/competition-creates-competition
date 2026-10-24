"""(g) Posterior as a function of flow under full orders, and entry at the strong benchmark.

Print-only. Run from the repository root:
    .venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q2_laplace_technical/g1_posterior_entry.py

Laws (benchmark b = 2):
  matched scale     Laplace(2), Logistic(2), Gaussian(sigma = b = 2)
  matched variance  Laplace(2), Logistic(s = sqrt(24)/pi), Gaussian(sigma = sqrt(8))   [variance 8]
  matched slope     Gaussian(sigma^2 = b), whose full-order log-odds equal the Laplace log-odds on [-1, 1]
  other class members at score bound 1/2: hyperbolic secant, Student t (nu = 3), Laplace + N(0, 1)
"""
from __future__ import annotations

import math
import os
import sys

import numpy as np
from scipy import special

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model import BENCH, R1, auction, deviation_profit, log_odds, outcome  # noqa: E402
from noise_laws import Gaussian, HypSecant, Laplace, Logistic, NormalLaplace, StudentT  # noqa: E402

b = BENCH.b
LAWS = [
    ("Laplace, scale b", Laplace(b)),
    ("Logistic, matched scale", Logistic(b)),
    ("Logistic, matched variance", Logistic(math.sqrt(6.0) * b / math.pi)),
    ("Gaussian, sigma = b", Gaussian(b)),
    ("Gaussian, matched variance", Gaussian(math.sqrt(2.0) * b)),
    ("Gaussian, sigma^2 = b", Gaussian(math.sqrt(b))),
    ("Hyperbolic secant, bound 1/b", HypSecant(b)),
    ("Student t nu=3, bound 1/b", StudentT.with_bound(3.0, 1.0 / b)),
    ("Laplace(b) + N(0,1)", NormalLaplace(b, 1.0)),
]

print("=" * 100)
print("Benchmark (h, ell, p, rho, c_L, c_H, b, k) =", (BENCH.h, BENCH.ell, BENCH.p, BENCH.rho, BENCH.c_L, BENCH.c_H, BENCH.b, BENCH.k))
a = auction(BENCH, R1)
print(f"Strong economy r1 = {R1}: g_L = {a['gL']:.6f}, g_H = {a['gH']:.6f}, Delta_T = {a['dT']:.6f}, t_0 = {a['t0']:.6f}")
m_lap = 1.0 / (1.0 + math.exp(2.0 / b))
print(f"Paper bounds at b = 2: m = {m_lap:.6f}, M = {1 - m_lap:.6f}")

print("\n" + "=" * 100)
print("Table 1. Full-order posterior mu(x) = f(x-1) / [f(x-1) + f(x+1)]")
xs = [-8, -4, -2, -1, -0.5, 0, 0.5, 1, 2, 4, 8, 16]
print(f"{'law':34s}{'var':>7s}" + "".join(f"{x:>8g}" for x in xs))
for label, law in LAWS:
    lam = log_odds(law, 1.0, -1.0)
    mus = special.expit(lam(np.array(xs, dtype=float)))
    print(f"{label:34s}{law.var():7.3f}" + "".join(f"{v:8.4f}" for v in mus))

print("\nTable 2. Full-order log-odds lambda(x), with the clipped line (2/b) clip(x, -1, 1) for reference")
print(f"{'law':34s}" + "".join(f"{x:>8g}" for x in xs))
print(f"{'(2/b) clip(x,-1,1)':34s}" + "".join(f"{2.0 / b * max(-1.0, min(1.0, x)):8.4f}" for x in xs))
for label, law in LAWS:
    lam = log_odds(law, 1.0, -1.0)
    print(f"{label:34s}" + "".join(f"{v:8.4f}" for v in lam(np.array(xs, dtype=float))))

print("\nTable 3. Score bound L, sup of the full-order posterior, and its limit at large flow")
print(f"{'law':34s}{'L':>9s}{'sup mu (grid)':>15s}{'argmax x':>10s}{'mu(1e4)':>10s}{'paper M':>10s}")
grid = np.linspace(-60, 60, 120001)
for label, law in LAWS:
    lam = log_odds(law, 1.0, -1.0)
    vals = lam(grid)
    i = int(np.argmax(vals))
    print(f"{label:34s}{law.L:9.4f}{special.expit(vals[i]):15.6f}{grid[i]:10.3f}"
          f"{float(special.expit(lam(1e4))):10.6f}{1 - m_lap:10.6f}")

print("\n" + "=" * 100)
print("Table 4. Entry at the strong benchmark r1 = 3 under full orders (fixed profile (1, -1))")
print("  tau_H = high-cost belief threshold; fav = flow set where mu >= tau_H; tau_L = low-cost threshold")
print(f"{'law':34s}{'tau_H':>8s}{'favourable flow set':>26s}{'a_H':>9s}{'a_L':>9s}{'low-cost':>10s}{'E':>9s}{'O_H':>9s}")
for label, law in LAWS:
    o = outcome(law, BENCH, R1)
    fav = " U ".join(f"[{lo:.4f},{hi:.4g}]" if math.isfinite(hi) else f"[{lo:.4f},inf)" for lo, hi in o.fav_H) or "empty"
    low = "all x" if o.fav_L == [(-math.inf, math.inf)] else " U ".join(f"[{lo:.3f},{hi:.3g}]" for lo, hi in o.fav_L)
    print(f"{label:34s}{o.tau_H:8.4f}{fav:>26s}{o.alpha_H:9.5f}{o.alpha_L:9.5f}{low:>10s}{o.E:9.6f}{o.O_H:9.6f}")
print("  Paper: Laplace E = 0.522757, O_H = 0.324192; logistic E = 0.301509, x* = 5.424598398.")
lg = Logistic(b)
o = outcome(lg, BENCH, R1)
print(f"  Logistic cutoff in noise standard deviations: {o.fav_H[0][0] / (b * math.pi / math.sqrt(3)):.6f} (paper 1.495369)")

print("\n" + "=" * 100)
print("Table 5. Is the full-order profile a best response against its own schedules? (fixed-profile check)")
print("  U_theta(s) = profit of a correctly signed order of size s; uniform bound margin = (1 - L) rho m_f dT - k")
sgrid = np.linspace(0.0, 1.0, 41)
print(f"{'law':34s}{'margin':>10s}{'U_H(1)':>10s}{'argmax_H':>9s}{'U_L(1)':>10s}{'argmax_L':>9s}{'verdict':>12s}")
for label, law in LAWS:
    lam = log_odds(law, 1.0, -1.0)
    inf_mu = float(special.expit(np.min(lam(grid))))
    if math.isfinite(law.L) and law.L < 1:
        margin = (1 - law.L) * BENCH.rho * inf_mu * a["dT"] - BENCH.k
        mtxt = f"{margin:10.5f}"
    else:
        mtxt = f"{'n/a':>10s}"
    UH = [deviation_profit(law, BENCH, R1, 1.0, -1.0, "H", s)[0] for s in sgrid]
    UL = [deviation_profit(law, BENCH, R1, 1.0, -1.0, "L", -s)[0] for s in sgrid]
    iH, iL = int(np.argmax(UH)), int(np.argmax(UL))
    ok = (iH == len(sgrid) - 1) and (iL == len(sgrid) - 1)
    print(f"{label:34s}{mtxt}{UH[-1]:10.6f}{sgrid[iH]:9.3f}{UL[-1]:10.6f}{sgrid[iL]:9.3f}{'(1,-1) BR' if ok else 'NOT BR':>12s}")
