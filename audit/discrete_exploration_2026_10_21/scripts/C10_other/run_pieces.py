"""Exact-piece hull: optimal public disclosure at several strengths (hp mode, selection rules)."""
import sys
from common import *
import branch, pieces as pc

set_mode('hp')
par = P()
pi = K(1, 2)
sel = sys.argv[1] if len(sys.argv) > 1 else 'inf'
print('selection', sel)
for r in [Fr(6, 5), Fr(1, 1) * Fr(13, 10), Fr(3, 2), Fr(2), Fr(3), Fr(18, 5), Fr(21, 5), Fr(5), Fr(7), Fr(9)]:
    A = auction(par, r)
    pts, st, cs = pc.hull_points(par, A, sel)
    if pts is None:
        print(f"r={float(r)}: tau outside (0,1): tau={mp.nstr(st['tau'],6)}")
        continue
    hull = pc.upper_hull([(p[0], p[1], p[2], p[3], p[4]) for p in pts])
    val, v1, v2, w = pc.policy_at(hull, pi)
    base = branch.equilibria(par, A, pi)[0]
    base_desc = ', '.join(f"{l}: Pi-t0={mp.nstr(o['Pi']-A['t0'],6)} E={mp.nstr(o['E'],5)} OH={mp.nstr(o['OH'],5)}" for l, o in base) or 'no pure eq'
    E_pol = (1 - w) * v1[4]['E'] + w * v2[4]['E']
    OH_pol = (1 - w) * v1[4]['OH'] + w * v2[4]['OH']
    thr = st['thr']
    print(f"r={float(r):.3f} DT={mp.nstr(A['DT'],5)} tau={mp.nstr(st['tau'],6)} phi_T/a={mp.nstr(thr['Ta'],6)} phi_aT={mp.nstr(thr['aT'],6)}")
    print(f"   no disclosure: {base_desc}")
    print(f"   optimal policy: phi in {{{mp.nstr(v1[0],6)} [{v1[2]}], {mp.nstr(v2[0],8)} [{v2[2]}]}}, weight on upper={mp.nstr(w,6)};  Pi-t0={mp.nstr(val-A['t0'],7)}  E={mp.nstr(E_pol,6)} O_H={mp.nstr(OH_pol,6)}")
