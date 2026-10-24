"""Symmetric public signal of accuracy d (prior 1/2): entry, ownership, proceeds, trading, by incumbent strength."""
import sys
from common import *
import branch, pieces as pc

set_mode('hp')
par = P()
pi = K(1, 2)
for r in [Fr(6, 5), Fr(3), Fr(18, 5), Fr(21, 5)]:
    A = auction(par, r)
    st = pc.structure(par, A)
    print(f"\nr={float(r)} DT={mp.nstr(A['DT'],5)} tau={mp.nstr(st['tau'],6)}  phi_aT={mp.nstr(st['thr']['aT'],5)} phi_T={mp.nstr(st['thr']['T'],5)} phi_T/a={mp.nstr(st['thr']['Ta'],5)}")
    print(" d      E       O_H     Pi-t0    | branch d (label e_g,e_b)     | branch 1-d (label e_g,e_b)")
    for dd in [500, 550, 600, 650, 700, 750, 800, 900, 990, 1000]:
        d = K(dd, 1000)
        res = []
        for ph in (d, 1 - d):
            eqs, G0, G1 = branch.equilibria(par, A, ph)
            res.append(eqs)
        if not res[0] or not res[1]:
            print(f"{float(d):.3f} GAP", [bool(x) for x in res])
            continue
        def pick(eqs):
            return dict(eqs)['FB'] if len(eqs) == 2 else eqs[0][1]
        def lab(eqs):
            return '+'.join(l for l, _ in eqs)
        o1, o2 = pick(res[0]), pick(res[1])
        E = (o1['E'] + o2['E']) / 2
        OH = (o1['OH'] + o2['OH']) / 2
        Pi = (o1['Pi'] + o2['Pi']) / 2
        print(f"{float(d):.3f}  {mp.nstr(E,6):>7} {mp.nstr(OH,6):>7} {mp.nstr(Pi-A['t0'],7):>8} | {lab(res[0]):6s} ({mp.nstr(o1['eg'],3)},{mp.nstr(o1['eb'],3)}) | {lab(res[1]):6s} ({mp.nstr(o2['eg'],3)},{mp.nstr(o2['eb'],3)})")
