"""Stake thresholds of the three-point model as functions of incumbent strength r (exact fractions; print only).

Regions of the (r, omega) plane for the correspondence of Proposition C5-1:
  omega_H(r) <= omega <= Omega1(r)   : S = (bH, bL) = (1, 0) exists
  Omega2(r) <= omega <= Omega1(r)    : partial manipulation M exists as well
  omega >= Omega2(r)                 : challenger-mixing equilibrium M' exists
  omega <= omega_H(r) (D1 belief)    : no trade
Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C5_stake/tp_phase.py
"""
import os
import sys
from fractions import Fraction as F
from math import sqrt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tp_lib import BENCH, auction, tau_of  # noqa: E402

rho, k, cH = BENCH["rho"], BENCH["k"], BENCH["cH"]
ell, p, h = BENCH["l"], BENCH["p"], BENCH["h"]


def th(r):
    a = auction(r)
    tau = tau_of(a)
    wH = (3 * k - rho * a["D"]) / ((1 - rho) * a["wH"])
    O2 = ((rho + tau) * a["D"] + 3 * k) / ((1 - rho) * a["wL"]) if tau <= 1 else None
    O1 = ((1 + rho) * a["D"] + 3 * k) / ((1 - rho) * a["wL"])
    return a, tau, wH, O2, O1


def root(f, lo, hi, n=200):
    flo = f(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


if __name__ == "__main__":
    print("r        tau      Delta_T   zero-stake H gain   omega_H    Omega2     Omega1    beta_max")
    for r in (F(101, 100), F(11, 10), F(6, 5), F(3, 2), F(7, 4), F(197, 100), F(2), F(5, 2), F(3), F(4), F(6), F(7), F(79, 10), F(8), F(9)):
        a, tau, wH, O2, O1 = th(r)
        zs = rho * a["D"] / 3 - k
        bm = (1 / tau - 1) if tau <= 1 else None
        print(f"{float(r):7.3f}  {float(tau):7.4f}  {float(a['D']):8.5f}  {float(zs):+10.6f}        "
              f"{float(max(wH, F(0))):8.5f}  {('%8.5f' % float(O2)) if O2 else '   n/a  '}  {float(O1):8.5f}  "
              f"{('%7.4f' % float(bm)) if bm is not None else '  n/a'}")
    print("\nLimits at r -> l = 1: omega_H = Omega1 = Omega2 =", float(3 * k / ((1 - rho) * auction(F(1))['wH'])),
          "= 3k/((1-rho) w(l)), w(l) =", auction(F(1))['wH'])
    # zero-stake cutoff r_T: rho Delta_T(r)/3 = k
    d = 3 * k / rho
    rT = ell + d + sqrt(float(d * d + 2 * ell * d))
    print("zero-stake cutoff r_T = l + d + sqrt(d^2 + 2 l d), d = 3k/rho:", rT)
    # high-cost ceiling r_C: g_H(r) = cH
    rC = (h - cH) + sqrt(float((h - cH) ** 2 - p * p))
    print("ceiling r_C = (h-cH) + sqrt((h-cH)^2 - p^2):", rC)
    print("\nOnset r_S(omega): smallest r with omega_H(r) <= omega (S appears); and r_L(omega): smallest r with Omega1(r) >= omega")
    for om in (F(0), F(5, 100), F(1, 10), F(15, 100), F(18, 100), F(2, 10), F(21, 100), F(22, 100), F(25, 100), F(1, 2), F(1), F(2)):
        def fH(r):
            return th(r)[2] - om
        def fL(r):
            return th(r)[4] - om
        lo, hi = F(10001, 10000), F(79, 10)
        rS = root(fH, lo, hi) if (fH(lo) > 0 and fH(hi) < 0) else (lo if fH(lo) <= 0 else None)
        rL = root(fL, lo, hi) if (fL(lo) < 0 and fL(hi) > 0) else (lo if fL(lo) >= 0 else None)
        print(f"  omega={float(om):6.3f}  r_S={None if rS is None else round(float(rS), 4)}  r_L={None if rL is None else round(float(rL), 4)}")
