"""(e) One-directional trading with Laplace noise: buy-only q in [0, 1], sell-only q in [-1, 0].

Print-only. Run from the repository root:
    .venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q2_laplace_technical/g4_one_directional.py

With an order set of width w (w = 2 two-sided, w = 1 one-directional) the Laplace likelihood
ratio of any two feasible orders lies in [e^{-w/b}, e^{w/b}], so m_w = 1/(1 + e^{w/b}), M_w = 1 - m_w.
"""
from __future__ import annotations

import math
import os
import sys
from dataclasses import replace

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model import BENCH, R0, R1, B, auction, belief_threshold, deviation_profit, frak_r, logit, outcome  # noqa: E402
from noise_laws import Laplace  # noqa: E402

b, rho, k = BENCH.b, BENCH.rho, BENCH.k
lap = Laplace(b)
VARIANTS = [("two-sided (1,-1)", 1.0, -1.0, 2.0), ("buy-only (1,0)", 1.0, 0.0, 1.0), ("sell-only (0,-1)", 0.0, -1.0, 1.0)]


def r_ceiling(prm, M):
    h, ell, p, c = prm.h, prm.ell, prm.p, prm.c_H
    disc = (M * h - c) ** 2 + M * ((1 - M) * ell ** 2 - p ** 2)
    return (M * h - c + math.sqrt(disc)) / M if disc >= 0 else float("nan")


print("=" * 100)
print("Bounds and conditions at the benchmark (r0, r1) = (1.2, 3)")
a0, a1 = auction(BENCH, R0), auction(BENCH, R1)
print(f"  B_r0(1/2) = {B(BENCH, R0, 0.5):.6f}; Delta_T(r0) = {a0['dT']:.6f}; Delta_T(r1) = {a1['dT']:.6f}; tau_H(r1) at c_H = 6: {belief_threshold(BENCH, R1, 6.0):.6f}")
print(f"{'variant':20s}{'m_w':>9s}{'M_w':>9s}{'A1 bound':>10s}{'c_H range for A2':>24s}{'A3 upper':>10s}{'r_U':>9s}{'r_C(c_H=6)':>12s}")
for name, qH, qL, w in VARIANTS:
    m = 1 / (1 + math.exp(w / b))
    M = 1 - m
    a1_bound = B(BENCH, R1, m)
    lo, hi = B(BENCH, R0, 0.5), B(BENCH, R1, M)
    a3 = (1 - 1 / b) * rho * m * a1["dT"]
    rU = frak_r(BENCH.ell, k / ((1 - 1 / b) * rho * m))
    print(f"{name:20s}{m:9.5f}{M:9.5f}{a1_bound:10.4f}{f'({lo:.4f}, {hi:.4f})':>24s}{a3:10.5f}{rU:9.4f}{r_ceiling(BENCH, M):12.4f}")
print(f"  r_N = {frak_r(BENCH.ell, 2 * k / rho):.6f} for every variant (no-trade test uses only rho Delta_T / 2 <= k)")

for c_H in (6.0, 5.0):
    prm = replace(BENCH, c_H=c_H)
    print("\n" + "=" * 100)
    print(f"Fixed one-sided-full profiles at r1 = 3 with c_H = {c_H}")
    print(f"{'variant':20s}{'tau_H':>8s}{'x*':>10s}{'alpha_H':>10s}{'alpha_L':>10s}{'E':>10s}{'O_H':>10s}")
    for name, qH, qL, w in VARIANTS:
        o = outcome(lap, prm, R1, qH, qL)
        xs = f"{o.fav_H[0][0]:.6f}" if o.fav_H else "none"
        print(f"{name:20s}{o.tau_H:8.4f}{xs:>10s}{o.alpha_H:10.6f}{o.alpha_L:10.6f}{o.E:10.6f}{o.O_H:10.6f}")
    tau = belief_threshold(prm, R1, c_H)
    if 0.5 < tau < 1 / (1 + math.exp(-1 / b)):
        xb = (1 + b * logit(tau)) / 2
        print(f"  closed form buy-only: x* = (1 + b logit tau)/2 = {xb:.6f}, alpha_H = {1 - 0.5 * math.exp((xb - 1) / b):.6f}, alpha_L = {0.5 * math.exp(-xb / b):.6f}")
        xs_ = (b * logit(tau) - 1) / 2
        print(f"  closed form sell-only: x* = (b logit tau - 1)/2 = {xs_:.6f}, alpha_H = {1 - 0.5 * math.exp(xs_ / b):.6f}, alpha_L = {0.5 * math.exp(-(xs_ + 1) / b):.6f}")

prm = replace(BENCH, c_H=5.0)
print("\n" + "=" * 100)
print("Best-response check against the fixed buy-only schedules (c_H = 5, r1 = 3)")
grid = np.linspace(0.0, 1.0, 21)
UH = [deviation_profit(lap, prm, R1, 1.0, 0.0, "H", s)[0] for s in grid]
UL = [deviation_profit(lap, prm, R1, 1.0, 0.0, "L", s)[0] for s in grid]
print(f"  H buys s: argmax {grid[int(np.argmax(UH))]:.2f}, U_H(1) = {UH[-1]:.6f}; min increment {min(np.diff(UH)):.6f}")
print(f"  L buys s (wrong sign): max over s > 0 of U_L = {max(UL[1:]):.6f} (negative means zero is optimal)")
UHs = [deviation_profit(lap, prm, R1, 0.0, -1.0, "L", -s)[0] for s in grid]
print(f"  sell-only, L sells s: argmax {grid[int(np.argmax(UHs))]:.2f}, U_L(1) = {UHs[-1]:.6f}  (equal to buy-only U_H(1) by translation and symmetry)")
