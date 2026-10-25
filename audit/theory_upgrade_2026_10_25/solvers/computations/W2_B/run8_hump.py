"""Continuous high class G_H = U[8,12], G_L = delta_1, p = 1/2, R ~ U[0,r];
cH=3, rho=0.05, k=0.6, beta=0.2, a=0.01, cap=0.95. Branch extent, ownership hump, eps_e vs eta at the peak."""
import sys
import numpy as np
sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W2_B')
from model import lam_R, lam_E, eps_e

p, ell = 0.5, 1.0
th = np.linspace(8.0, 12.0, 40001)
prm = dict(cH=3.0, rho=0.05, k=0.6, beta=0.2, a=0.01, cap=0.95)


def at(r):
    t = np.where(th <= r, th - (th * th - p * p) / (2 * r), r / 2 + p * p / (2 * r))
    tL = ell - (ell * ell - p * p) / (2 * r)
    Delta, gH, gL = t.mean() - tL, (th - t).mean(), ell - tL
    WH = np.minimum(th / r, 1).mean()
    tau = (prm['cH'] - gL) / (gH - gL)
    lam = lam_R(Delta, prm['a'], prm['k'], prm['beta'])
    on = (lam is not None) and 0.5 < tau < 1 and lam >= lam_E(tau, prm['beta']) and lam < prm['cap'] \
        and prm['rho'] * Delta <= 2 * prm['k']
    eH = prm['rho'] + (1 - prm['rho']) * (prm['beta'] + (1 - prm['beta']) * lam) if lam is not None else float('nan')
    return dict(r=r, Delta=Delta, tau=tau, lam=lam, on=on, WH=WH, own=0.5 * eH * WH, eH=eH)


rs = np.arange(2.0, 12.001, 0.01)
rows = [at(r) for r in rs]
onr = [x['r'] for x in rows if x['on']]
print("branch (on grid step 0.01): from", min(onr), "to", max(onr), " contiguous:",
      all(abs(onr[i + 1] - onr[i] - 0.01) < 1e-6 for i in range(len(onr) - 1)))
for r in [8.07, 8.5, 9.0, 9.5, 10.0, 10.1, 10.2, 11.0, 12.0]:
    x = at(r)
    print(f"r={r:5.2f} on={x['on']} tau={x['tau']:.4f} lamR={x['lam']:.4f} WH={x['WH']:.5f} own={x['own']:.6f}")
on_rows = [x for x in rows if x['on']]
pk = max(on_rows, key=lambda x: x['own'])
print("peak ownership on the branch at r =", round(pk['r'], 2), " WH =", round(pk['WH'], 5), " own =", round(pk['own'], 6))
# eps_e vs eta near the peak (finite differences)
for r in [9.0, pk['r'], 11.0]:
    x0, x1 = at(r), at(r + 1e-4)
    ee, _, _ = eps_e(x0['Delta'], dict(prm))
    eta = -((x1['WH'] - x0['WH']) / x0['WH']) / ((x1['Delta'] - x0['Delta']) / x0['Delta'])
    print(f"  r={r:.2f}: eps_e={ee:.4f}  eta={eta:.4f}")
