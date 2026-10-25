"""Can ownership rise on the research branch when the high class can lose (W_H < 1)?

(1) Point masses, uniform incumbent, r > h: grid over (cH, rho, k, beta, a), check eps_e > eta at branch points.
(2) Supremum bound eps_e < 2(1-beta) and the r-threshold above which ownership must fall.
"""
import sys
import itertools
sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W2_B')
from model import branch, eps_e

h, ell, p = 10.0, 1.0, 0.5
best = None
count_branch = 0
count_rise = 0
for cH in [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]:
    for rho in [0.01, 0.05, 0.1, 0.25]:
        for beta in [0.05, 0.1, 0.2, 0.3]:
            for k in [0.01, 0.02, 0.05, 0.1, 0.2, 0.4]:
                for a in [0.001, 0.01, 0.05, 0.2, 1.0, 5.0]:
                    prm = dict(h=h, ell=ell, p=p, cH=cH, rho=rho, k=k, beta=beta, a=a, cap=0.99)
                    for r in [10.01, 10.1, 10.3, 10.6, 11.0, 12.0, 13.0, 15.0]:
                        b = branch(r, prm)
                        if not b.get('on_branch'):
                            continue
                        count_branch += 1
                        ee, lam, dlam = eps_e(b['Delta'], prm)
                        eta = 2 * r / (h + ell) - 1  # point masses, r > h
                        if ee > eta:
                            count_rise += 1
                            gap = ee - eta
                            if best is None or gap > best[0]:
                                best = (gap, dict(r=r, cH=cH, rho=rho, beta=beta, k=k, a=a,
                                                  tau=b['tau'], lamE=b['lamE'], lam=lam, ee=ee, eta=eta))
print("branch points with r>h:", count_branch, " of which ownership rises:", count_rise)
print("largest eps_e - eta:", best)

# direct check of a rising example by finite differences
if best is not None:
    q = best[1]
    prm = dict(h=h, ell=ell, p=p, cH=q['cH'], rho=q['rho'], k=q['k'], beta=q['beta'], a=q['a'], cap=0.99)
    b0, b1 = branch(q['r'], prm), branch(q['r'] + 0.01, prm)
    print("finite difference: own", b0['own'], "->", b1['own'], " on_branch", b0['on_branch'], b1['on_branch'],
          " WH", b0['WH'], b1['WH'], " eH", b0['eH'], b1['eH'])

# eps_e upper bound check: max over all branch points
mx = 0
for cH in [x / 4 for x in range(2, 40)]:
    for rho in [0.001, 0.01, 0.05, 0.25, 0.5]:
        for beta in [0.02, 0.1, 0.2, 0.3, 0.33, 0.45]:
            for k in [0.001, 0.01, 0.05, 0.2]:
                for a in [1e-5, 1e-3, 0.05, 1.0]:
                    prm = dict(h=h, ell=ell, p=p, cH=cH, rho=rho, k=k, beta=beta, a=a, cap=0.999)
                    for r in [1.2, 1.5, 2, 3, 5, 8, 10.5, 12, 15]:
                        b = branch(r, prm)
                        if not b.get('on_branch'):
                            continue
                        ee, lam, _ = eps_e(b['Delta'], prm)
                        ratio = ee / (2 * (1 - beta))
                        if ratio > mx:
                            mx = ratio
                            arg = (r, cH, rho, beta, k, a, ee, lam, b['lamE'])
print("max over branch points of eps_e / (2(1-beta)):", mx, arg)
