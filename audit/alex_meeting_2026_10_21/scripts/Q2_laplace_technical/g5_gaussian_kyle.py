"""(c) Gaussian noise: which proof steps fail, and what survives. Print-only.

Run from the repository root:
    .venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q2_laplace_technical/g5_gaussian_kyle.py
"""
from __future__ import annotations

import math
import os
import sys
from dataclasses import replace

import numpy as np
from scipy import optimize, special, stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model import BENCH, R0, R1, auction, belief_threshold, deviation_profit, log_odds, outcome  # noqa: E402
from noise_laws import Gaussian, Laplace  # noqa: E402

b, rho, k = BENCH.b, BENCH.rho, BENCH.k
a1 = auction(BENCH, R1)
laws = [Laplace(b), Gaussian(b), Gaussian(math.sqrt(2) * b), Gaussian(math.sqrt(b))]

print("=" * 100)
print("1. Residual advantages under the full-order schedules at r1 = 3 (A_H = e dT (1 - mu), A_L = e dT mu)")
xs = [-20, -10, -5, -2, 0, 2, 5, 10, 20]
print(f"   paper floor rho m dT = {rho / (1 + math.exp(2 / b)) * a1['dT']:.6f}")
for law in laws:
    o = outcome(law, BENCH, R1)
    lam = log_odds(law, 1.0, -1.0)
    rowH, rowL = [], []
    for x in xs:
        mu = float(special.expit(lam(x)))
        e = (rho if any(lo <= x <= hi for lo, hi in o.fav_L) else 0.0) + ((1 - rho) if any(lo <= x <= hi for lo, hi in o.fav_H) else 0.0)
        rowH.append(e * a1["dT"] * (1 - mu))
        rowL.append(e * a1["dT"] * mu)
    print(f"   {law.name:22s} A_H: " + " ".join(f"{v:8.5f}" for v in rowH))
    print(f"   {'':22s} A_L: " + " ".join(f"{v:8.5f}" for v in rowL))
print("   flows x:                      " + " ".join(f"{x:8d}" for x in xs))

print("\n2. Score bound fails: for A = 1[x0, inf), F(s) = Pr(s + Z >= x0) and F'(0)/F(0) = hazard at x0")
for x0 in (2, 5, 10, 20):
    g = Gaussian(b)
    haz = stats.norm.pdf(x0, scale=b) / stats.norm.sf(x0, scale=b)
    print(f"   x0 = {x0:3d}: Gaussian(sigma=2) F'/F = {haz:8.4f}    Laplace(b=2) F'/F = {0.5:.4f} (= 1/b for x0 >= 0)")

print("\n3. Low-cost floor under Gaussian noise: A1 needs c_L < B_r1(0) = g_L(r1) =", f"{a1['gL']:.6f}; benchmark c_L = {BENCH.c_L}")
print(f"   so the low-cost challenger stays out when mu < {belief_threshold(BENCH, R1, BENCH.c_L):.6f}")

print("\n4. Best response of the low-value investor against the fixed full-order schedules (sale size s)")
for law in laws:
    for cl in (1.0, 0.0):
        prm = replace(BENCH, c_L=cl)
        res = optimize.minimize_scalar(lambda s: -deviation_profit(law, prm, R1, 1.0, -1.0, "L", -s)[0],
                                       bounds=(0.5, 1.0), method="bounded", options={"xatol": 1e-6})
        UH1 = deviation_profit(law, prm, R1, 1.0, -1.0, "H", 1.0)[0]
        UH9 = deviation_profit(law, prm, R1, 1.0, -1.0, "H", 0.99)[0]
        print(f"   {law.name:22s} c_L = {cl:3.1f}: argmax_s U_L = {res.x:.4f}  (U_L there {-res.fun:.6f}); "
              f"U_H(1) - U_H(0.99) = {UH1 - UH9: .2e}")

print("\n5. Expensive-entry ceiling. Laplace: B_r(M) = c_H at r_C = 3.592659.")
h, p, c = BENCH.h, BENCH.p, BENCH.c_H
r_tilde = (h - c) + math.sqrt((h - c) ** 2 - p * p)
print(f"   Gaussian (M = 1): expensive entry stays feasible while g_H(r) > c_H, i.e. up to r = {r_tilde:.6f}")

print("\n6. No affine price: the competitive price is bounded, flow support is the whole line")
lo_p = a1["t0"] + rho * a1["wL"]
hi_p = a1["t0"] + a1["wL"] + a1["dT"]
tau = belief_threshold(BENCH, R1, c)
print(f"   P(x) lies in [t0 + rho w_L, t0 + w_L + dT] = [{lo_p:.6f}, {hi_p:.6f}] for every flow")
print(f"   jump of the price at the entry threshold: (1 - rho)(w_L + dT tau) = {(1 - rho) * (a1['wL'] + a1['dT'] * tau):.6f}")

print("\n7. Part (i) of Prop. 2 needs only A <= Delta_T: Delta_T(r0) =", f"{auction(BENCH, R0)['dT']:.6f} < k = {k}: holds for every full-support law")
