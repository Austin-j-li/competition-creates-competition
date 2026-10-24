"""The five equilibria of the discrete-Laplace weak economy at omega = 9/25 (print only).

Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C5_stake/dl_five.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpmath import mp, mpf, nstr  # noqa: E402
from dl_lib import R0, R1  # noqa: E402
from dl_enumerate import equilibria  # noqa: E402

mp.dps = 40

if __name__ == "__main__":
    for r, om in ((R0, mpf(9) / 25), (R1, mpf(7) / 2), (R1, mpf(18) / 5)):
        print(f"\nr = {nstr(r, 4)}, omega = {nstr(om, 6)}")
        for eq in equilibria(r, om):
            phi = "-" if eq["phiG"] is None else nstr(eq["phiG"], 10)
            print(f"  {eq['kind']:13s} bH={nstr(eq['bH'], 10):>12s} bL={nstr(eq['bL'], 10):>12s} phi={phi:>12s} "
                  f"E={nstr(eq['E'], 8)} O_H={nstr(eq['OH'], 8)} eH={nstr(eq['eH'], 8)} eL={nstr(eq['eL'], 8)} "
                  f"posteriors M={nstr(eq['M'], 6)} m={nstr(eq['m'], 6)}")
