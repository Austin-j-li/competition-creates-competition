import sys, math
sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W3_B')
from model import *
from scan import research_equilibria
u = math.e - 1; beta = 0.294655; lbar = u*beta/(1+u*beta)
B = Par(h=10, ell=1, p=0.5, cH=6, k=0.02, rho=0.25, beta=beta, a=1/40, lbar=lbar)
for r in (1.75, 2.12, 2.13, 2.16, 2.17, 2.3, 3.59, 3.595):
    A, res = research_equilibria(r, B, "IM", n=20000)
    print("r=%.3f" % r, ["%s lam=%.5f entry=%.6f" % (e['form'], e['lam'], e['entry']) for e in res])
