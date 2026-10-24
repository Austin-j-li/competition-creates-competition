"""Compare the exact hull policy with the closed form phi*(r) = min{phi_{T/a}, max(tau, phi_N)} and print the support-line margins.

phi_N = 1 - k/DT(r): the lowest prior at which no trade with full entry is an equilibrium.
For the support-line proof the script prints, for the chord l(phi) = rho*wL + gamma*phi through (0, rho*wL) and (phi*, wL + DT*phi*):
  margin_aT  = l(phi_aT) - Phi_(1,rho)(phi_aT)   (must be > 0)
  margin_mix = max over cell edges of  [Phi(edge) - l(edge)]   (must be <= 0)
"""
import sys
from common import *
import branch, pieces as pc

set_mode('hp')
par = P()
pi = K(1, 2)
a, rho, k = par.a, par.rho, par.k
print("   r     tau     phiN     phi_Ta   phi*_formula  phi*_hull    w      E      margin_aT  worst_edge_excess")
rs = [Fr(6, 5) + Fr(i, 20) for i in range(0, 161, 4)]
for r in rs:
    A = auction(par, r)
    st = pc.structure(par, A)
    if st['thr'] is None:
        continue
    tau_r = st['tau']
    phiN = 1 - k / A['DT']
    phiTa = st['thr']['Ta']
    form = min(phiTa, max(tau_r, phiN))
    pts, st, cs = pc.hull_points(par, A, 'inf')
    hull = pc.upper_hull([(p[0], p[1], p[2], p[3], p[4]) for p in pts])
    val, v1, v2, w = pc.policy_at(hull, pi)
    # support line at the formula point
    wL, DT = A['wL'], A['DT']
    ps = v2[0]
    gamma = DT + (1 - rho) * wL / ps
    line = lambda x: rho * wL + gamma * x
    aT = st['thr']['aT']
    PhiaT = pc.piece_values(par, A, 'FB', K(1), rho, aT)['Pi'] - A['t0']
    m_aT = line(aT) - PhiaT
    worst = None
    for p_ in pts:
        ex = (p_[1] - A['t0']) - line(p_[0])
        if worst is None or ex > worst:
            worst = ex
    print(f"{float(r):5.2f} {mp.nstr(tau_r,5):>7} {mp.nstr(phiN,5):>8} {mp.nstr(phiTa,5):>8} {mp.nstr(form,7):>12} {mp.nstr(ps,7):>11} {mp.nstr(w,5):>7} {mp.nstr((1-w)*v1[4]['E']+w*v2[4]['E'],5):>7} {mp.nstr(m_aT,5):>10} {mp.nstr(worst,5):>12}")
