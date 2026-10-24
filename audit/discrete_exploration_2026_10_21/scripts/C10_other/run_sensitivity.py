"""Optimal disclosure policy under parameter changes (hp mode). Prior pi may differ from 1/2."""
import sys
from common import *
import branch, pieces as pc

set_mode('hp')


def run(label, par, r, pi, sel='inf'):
    A = auction(par, r)
    pts, st, cs = pc.hull_points(par, A, sel)
    if pts is None:
        return f"{label}: tau={mp.nstr(st['tau'],5)} outside (0,1)"
    hull = pc.upper_hull([(p[0], p[1], p[2], p[3], p[4]) for p in pts])
    val, v1, v2, w = pc.policy_at(hull, pi)
    E = (1 - w) * v1[4]['E'] + w * v2[4]['E']
    OH = (1 - w) * v1[4]['OH'] + w * v2[4]['OH']
    base = branch.equilibria(par, A, pi)[0]
    if base:
        d = dict(base)
        b0 = d['FB'] if (sel == 'inf' and 'FB' in d) else base[0][1]
        b0s = f"{mp.nstr(b0['Pi']-A['t0'],5)} (E={mp.nstr(b0['E'],4)})"
    else:
        b0s = 'GAP'
    # full disclosure: phi in {0,1}
    f0 = branch.equilibria(par, A, K(0))[0]
    f1 = branch.equilibria(par, A, K(1))[0]
    o0 = f0[0][1] if f0 else None
    o1 = f1[0][1] if f1 else None
    fd = ((1 - pi) * o0['Pi'] + pi * o1['Pi'] - A['t0']) if o0 and o1 else None
    return (f"{label}: phi*=({mp.nstr(v1[0],4)},{mp.nstr(v2[0],6)}) w={mp.nstr(w,5)} E={mp.nstr(E,5)} OH={mp.nstr(OH,5)} "
            f"Pi-t0 cav={mp.nstr(val-A['t0'],6)} none={b0s} full={mp.nstr(fd,6) if fd is not None else 'NA'}")


half = K(1, 2)
print('--- selection rules at r=1.5 (coexistence of NT and FB at the prior)')
par = P()
for sel in ['inf', 'nt', 'best', 'worst']:
    print(sel, run('  r=1.5', par, Fr(3, 2), half, sel))
print('--- k sensitivity (r = 3)')
for k in [Fr(1, 200), Fr(1, 50), Fr(1, 10), Fr(1, 5), Fr(3, 10), Fr(1, 2)]:
    print(run(f'  k={float(k)}', P(k=k), Fr(3), half))
print('--- c_H sensitivity (r = 3); c_H=6 is the paper value, the market alone cannot recruit there')
for cH in [4, 5, 5.3, 6, 7, 8]:
    print(run(f'  cH={cH}', P(cH=Fr(cH).limit_denominator(100)), Fr(3), half))
print('--- rho sensitivity (r = 3)')
for rho in [Fr(1, 10), Fr(1, 4), Fr(1, 2)]:
    print(run(f'  rho={float(rho)}', P(rho=rho), Fr(3), half))
print('--- b sensitivity (r = 3)')
for b in [1.5, 2, 4, 10]:
    print(run(f'  b={b}', P(b=b), Fr(3), half))
print('--- prior sensitivity (r = 3)')
for pr in [Fr(3, 10), Fr(1, 2), Fr(7, 10)]:
    print(run(f'  pi={float(pr)}', P(), Fr(3), K(pr.numerator, pr.denominator)))
