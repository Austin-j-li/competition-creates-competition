"""Continuous high class G_H = U[A,B], G_L = delta_ell, uniform incumbent.
Search for a research branch that runs into the overlap region (W_H < 1) and report ownership along it.
"""
import sys
import itertools
import numpy as np
sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W2_B')
from model import lam_R, lam_E

p, ell = 0.5, 1.0
A, B = 8.0, 12.0
th = np.linspace(A, B, 8001)


def objs(r):
    t = np.where(th <= r, th - (th * th - p * p) / (2 * r), r / 2 + p * p / (2 * r))
    tL = ell - (ell * ell - p * p) / (2 * r) if ell <= r else r / 2 + p * p / (2 * r)
    WH = np.minimum(th / r, 1).mean()
    return t.mean() - tL, (th - t).mean(), ell - tL, WH


rs = np.arange(6.0, 12.01, 0.05)
cache = {r: objs(r) for r in rs}


def path(prm):
    rows = []
    for r in rs:
        Delta, gH, gL, WH = cache[r]
        tau = (prm['cH'] - gL) / (gH - gL)
        lam = lam_R(Delta, prm['a'], prm['k'], prm['beta'])
        if lam is None or not (0.5 < tau < 1):
            rows.append((r, False, None, None, WH))
            continue
        on = lam >= lam_E(tau, prm['beta']) and lam < prm['cap'] and prm['rho'] * Delta <= 2 * prm['k']
        eH = prm['rho'] + (1 - prm['rho']) * (prm['beta'] + (1 - prm['beta']) * lam)
        rows.append((r, on, lam, 0.5 * eH * WH, WH))
    return rows


best = None
for cH, rho, k, beta, a in itertools.product([3.0, 3.5, 4.0, 4.5, 5.0], [0.05, 0.1, 0.25], [0.3, 0.6, 1.0, 1.5],
                                            [0.2, 0.3], [0.01, 0.05, 0.2, 0.5]):
    prm = dict(cH=cH, rho=rho, k=k, beta=beta, a=a, cap=0.95)
    rows = [x for x in path(prm) if x[1]]
    over = [x for x in rows if x[4] < 1 - 1e-9]
    if len(over) < 6:
        continue
    owns = [x[3] for x in over]
    rises = sum(1 for i in range(len(owns) - 1) if owns[i + 1] > owns[i])
    falls = sum(1 for i in range(len(owns) - 1) if owns[i + 1] < owns[i])
    score = min(rises, falls)
    if best is None or score > best[0]:
        best = (score, prm, over[0][0], over[-1][0], rises, falls)
print("best example (rises and falls inside the overlap region):", best)
prm = best[1]
for r, on, lam, own, WH in path(prm):
    if on and abs((r * 20) - round(r * 20)) < 1e-9 and round(r * 20) % 4 == 0:
        print(f"  r={r:.2f} lamR={lam:.4f} WH={WH:.5f} own={own:.6f}")
