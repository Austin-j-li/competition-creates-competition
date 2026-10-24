"""Optimal public disclosure (concavification of target proceeds) at several incumbent strengths."""
import sys
from common import *
import branch, persuasion as ps

set_mode('hp')
par = P()
pi = K(1, 2)
sels = sys.argv[1:] or ['inf', 'nt']
for sel in sels:
    print('\n===== selection:', sel)
    for r in [Fr(6, 5), Fr(2), Fr(3), Fr(18, 5), Fr(21, 5), Fr(5), Fr(7)]:
        A = auction(par, r)
        verts = ps.vertices(par, A, sel)
        hull = ps.upper_hull([(v[0], v[1]) for v in verts])
        val, v1, v2, w = ps.cav_at(hull, pi)
        v0 = ps.branch_value(par, A, pi, sel)
        # symmetric binary signals
        best_d, best_val = None, None
        for j in range(0, 101):
            d = K(50 + j // 2 if False else 500 + 5 * j, 1000)
            if d >= 1:
                d = 1 - K(1, 10 ** 6)
            vv = (ps.branch_value(par, A, d, sel), ps.branch_value(par, A, 1 - d, sel))
            if vv[0] is None or vv[1] is None:
                continue
            tot = (vv[0][1]['Pi'] + vv[1][1]['Pi']) / 2
            if best_val is None or tot > best_val:
                best_val, best_d = tot, d
        # outcomes at hull vertices
        def out(phi):
            v = ps.branch_value(par, A, phi, sel)
            return v
        o1, o2 = out(v1[0]), out(v2[0])
        print(f"r={float(r):.2f}: no-disclosure Pi-t0={mp.nstr(v0[1]['Pi']-A['t0'],7)} ({v0[0]}, E={mp.nstr(v0[1]['E'],5)});  cav Pi-t0={mp.nstr(val-A['t0'],7)};  "
              f"best symmetric d={mp.nstr(best_d,5)} Pi-t0={mp.nstr(best_val-A['t0'],7)}")
        print(f"   hull segment: phi_lo={mp.nstr(v1[0],8)} (Pi-t0={mp.nstr(v1[1]-A['t0'],6)}, {v1[2] if len(v1)>2 else ''}) -- phi_hi={mp.nstr(v2[0],8)} (Pi-t0={mp.nstr(v2[1]-A['t0'],6)}, {v2[2] if len(v2)>2 else ''}); weight on phi_hi={mp.nstr(w,6)}")
        if o1 and o2:
            E_cav = (1 - w) * o1[1]['E'] + w * o2[1]['E']
            OH_cav = (1 - w) * o1[1]['OH'] + w * o2[1]['OH']
            print(f"   at the cav policy: E={mp.nstr(E_cav,6)}, O_H={mp.nstr(OH_cav,6)}  (branches: {o1[0]} E={mp.nstr(o1[1]['E'],5)}, {o2[0]} E={mp.nstr(o2[1]['E'],5)})")
