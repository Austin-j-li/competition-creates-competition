"""Check phi*(k) = min{phi_NT, phi_FB} against the exact-piece hull at r = 3 for several trading costs."""
from common import *
import branch, pieces as pc

set_mode('hp')
half = K(1, 2)
r = Fr(3)
print("   k      phi*_formula   phi*_hull   weight   E*      G1(phi3)+k")
for k in [Fr(1, 50), Fr(18, 100), Fr(19, 100), Fr(191, 1000), Fr(2, 10), Fr(22, 100), Fr(25, 100), Fr(27, 100), Fr(28, 100), Fr(3, 10)]:
    par = P(k=k)
    A = auction(par, r)
    st = pc.structure(par, A)
    T = st['T']
    phi3 = st['thr']['Ta']
    g13 = pc.G_profile(par, A, 'FB', K(1), K(1), phi3) + par.k
    fb = phi3 if g13 - par.k > 0 else None
    nt = max(st['tau'], 1 - par.k / A['DT'])
    form = nt if fb is None else min(nt, fb)
    pts, st, cs = pc.hull_points(par, A, 'inf')
    hull = pc.upper_hull([(p[0], p[1], p[2], p[3], p[4]) for p in pts])
    val, v1, v2, w = pc.policy_at(hull, half)
    E = (1 - w) * v1[4]['E'] + w * v2[4]['E']
    print(f"{float(k):6.3f} {mp.nstr(form,8):>13} {mp.nstr(v2[0],8):>11} {mp.nstr(w,5):>8} {mp.nstr(E,5):>7} {mp.nstr(g13,6):>10}")
