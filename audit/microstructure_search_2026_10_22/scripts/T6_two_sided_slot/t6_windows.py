"""Equilibria along a grid of strengths at fixed (lam, beta, theta) (print only).

Usage: python t6_windows.py LAM BETA THETA [RLO RHI STEP]   (rationals as a/b; default 13/10 9/5 1/200)
For each strength it prints every informative equilibrium (rule M, rule X): label, recruiting set,
P (pure entry) or X (challenger mixing), entry, A, S; and whether no trade is an equilibrium.
"""
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from t6_core import bench, enumerate_equilibria, fl  # noqa: E402


def main():
    lam, beta, theta = (F(v) for v in sys.argv[1:4])
    lo, hi, st = (F(v) for v in sys.argv[4:7]) if len(sys.argv) > 4 else (F(13, 10), F(9, 5), F(1, 200))
    print(f"lam = {lam} ({float(lam):.6f}), beta = {beta}, theta = {theta}; c = {(1 - lam) * beta}")
    r = lo
    while r <= hi:
        eqs, und, M = enumerate_equilibria(bench(lam=lam, beta=beta, theta=theta, r=r))
        nt = any(q['label'] == 'NT' for q in eqs)
        inf = [q for q in eqs if q['label'] != 'NT']
        desc = '; '.join(f"{q['label']}/{''.join(str(x) for x in q['recruit'])}/{'X' if q['chall_mix'] else 'P'}/"
                         f"E={fl(q['out']['E']):.6f}/A={fl(q['a']):.5f}/S={fl(q['s']):.5f}" for q in inf)
        print(f"r={float(r):.4f} NT={'y' if nt else 'n'} undecided={len(und)} | {desc}")
        r += st


if __name__ == '__main__':
    main()
