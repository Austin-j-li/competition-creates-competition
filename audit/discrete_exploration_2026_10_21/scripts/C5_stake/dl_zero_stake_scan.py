"""Zero-stake and small-stake equilibrium counts of the discrete-Laplace model over incumbent strength (print only).

Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C5_stake/dl_zero_stake_scan.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpmath import mp, mpf, nstr  # noqa: E402
from dl_enumerate import equilibria  # noqa: E402

mp.dps = 30

if __name__ == "__main__":
    print("Equilibria at omega = 0 by r (conventional rules): kinds, (rule-ok kinds) ")
    prev = None
    for i in range(0, 61):
        r = mpf("1.05") + mpf(i) * mpf("0.05")
        eqs = equilibria(r, mpf(0))
        kinds = "+".join(sorted(e["kind"] for e in eqs))
        kinds_rule = "+".join(sorted(e["kind"] for e in eqs if e["rule_ok"]))
        if kinds != prev:
            print(f"  from r={nstr(r, 4)}: {kinds}   [with challenger rule: {kinds_rule}]")
            prev = kinds
