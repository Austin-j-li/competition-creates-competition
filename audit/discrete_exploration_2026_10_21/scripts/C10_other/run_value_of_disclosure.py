"""Value of optimal disclosure over the market-only baseline, by incumbent strength (hp mode)."""
from common import *
import branch, pieces as pc

set_mode('hp')
par = P()
half = K(1, 2)
print("   r    Pi*-t0   market-only (inf)  gain    market-only (nt)  gain    E*     E market-only(inf)")
for r in [Fr(6, 5), Fr(3, 2), Fr(7, 4), Fr(2), Fr(5, 2), Fr(3), Fr(7, 2), Fr(18, 5), Fr(4), Fr(21, 5), Fr(5), Fr(6)]:
    A = auction(par, r)
    pts, st, cs = pc.hull_points(par, A, 'inf')
    hull = pc.upper_hull([(p[0], p[1], p[2], p[3], p[4]) for p in pts])
    val, v1, v2, w = pc.policy_at(hull, half)
    E = (1 - w) * v1[4]['E'] + w * v2[4]['E']
    eqs = dict(branch.equilibria(par, A, half)[0])
    inf = eqs.get('FB', eqs.get('NT'))
    nt = eqs.get('NT', eqs.get('FB'))
    f = lambda x: mp.nstr(x, 5)
    print(f"{float(r):5.2f} {f(val-A['t0']):>8}  {f(inf['Pi']-A['t0']):>10}  {f(val-inf['Pi']):>8}   {f(nt['Pi']-A['t0']):>10}  {f(val-nt['Pi']):>8}  {f(E):>6}  {f(inf['E']):>6}")
