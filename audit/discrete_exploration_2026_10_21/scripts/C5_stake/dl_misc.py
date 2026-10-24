"""Small exact checks quoted in the memo (print only).

Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C5_stake/dl_misc.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpmath import mp, mpf, sqrt, nstr  # noqa: E402
from dl_lib import BENCH, R1, auction  # noqa: E402
from dl_thresholds import consts, thresholds  # noqa: E402

mp.dps = 40

if __name__ == "__main__":
    aa, delta, g0, g1 = consts()
    rho, k, ell = BENCH["rho"], BENCH["k"], BENCH["l"]
    # zero-stake coexistence window of no trade and S (discrete Laplace)
    d_low = k / (g0 * g1 * (1 + rho))     # S exists at zero stake iff Delta_T >= d_low
    d_high = 2 * k / rho                  # no trade exists iff Delta_T <= d_high
    for name, d in (("S appears", d_low), ("no trade ends", d_high)):
        r = ell + d + sqrt(d * d + 2 * ell * d)
        print(f"  {name}: Delta_T = {nstr(d, 10)}  ->  r = {nstr(r, 10)}")
    # entry at M' with phi = 1 (omega = Omega2), discrete Laplace, r1
    t = thresholds(R1)
    tau = t["tau"]
    E = rho + (1 - rho) * g1 / (2 * tau)
    print("  E at Omega2 (D-Laplace, r1):", nstr(E, 10), " expected rho + (1-rho) g1/(2 tau)")
    print("  three-point E at Omega2, r1:", float(0.25 + 0.75 / (6 * 0.705)), "= 241/564 =", 241 / 564)
