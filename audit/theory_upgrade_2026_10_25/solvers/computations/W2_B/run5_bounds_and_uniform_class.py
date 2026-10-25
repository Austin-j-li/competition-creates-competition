"""(1) sup over lambda of the a->0 bound on eps_e, as a function of (rho, beta).
(2) A continuous high class G_H = U[A,B] with G_L = delta_ell and a uniform incumbent:
    ownership along the research branch when the incumbent's support overlaps the high-class support.
"""
import sys
import numpy as np
sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W2_B')
from model import lam_R, lam_E, m_of, dm_of


def ebar(rho, beta):
    lam = np.linspace(0, 1, 200001)[:-1]
    N = (1 - lam) * (2 * beta + (1 - 2 * beta) * lam)
    D = rho + (1 - rho) * (beta + (1 - beta) * lam)
    v = (1 - rho) * (1 - beta) * N / D
    i = v.argmax()
    return v[i], lam[i]


print("sup_lambda bound on eps_e (a -> 0):")
for rho in [0.01, 0.05, 0.1, 0.25, 0.5]:
    row = []
    for beta in [0.05, 0.1, 0.2, 0.294655, 1 / 3, 0.45]:
        v, l = ebar(rho, beta)
        row.append(f"b={beta:.3f}:{v:.3f}")
    print(f"  rho={rho}: " + "  ".join(row))
print("  (h-ell)/(h+ell) at h/ell=10:", 9 / 11, "; at h/ell=5:", 4 / 6)

# (2) continuous high class
p, ell = 0.5, 1.0
A, B = 8.0, 12.0
th = np.linspace(A, B, 40001)


def objs(r):
    def t_of(v):
        return np.where(v <= r, v - (v * v - p * p) / (2 * r), r / 2 + p * p / (2 * r))
    tH = t_of(th).mean()
    gH = (th - t_of(th)).mean()
    WH = np.minimum(th / r, 1).mean()
    tL = float(t_of(np.array([ell]))[0])
    gL = ell - tL
    return tH - tL, gH, gL, WH


prm = dict(cH=4.5, rho=0.25, k=0.4, beta=0.2, a=0.5, cap=0.95)
print("\nG_H = U[8,12], G_L = delta_1, p=1/2, R ~ U[0,r];", prm)
prev = None
for r in [7.0, 7.5, 7.9, 8.0, 8.1, 8.3, 8.6, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0]:
    Delta, gH, gL, WH = objs(r)
    tau = (prm['cH'] - gL) / (gH - gL)
    lam = lam_R(Delta, prm['a'], prm['k'], prm['beta'])
    lE = lam_E(tau, prm['beta']) if 0.5 < tau < 1 else float('nan')
    on = (lam is not None) and (0.5 < tau < 1) and lam >= lE and lam < prm['cap'] and prm['rho'] * Delta <= 2 * prm['k']
    eH = prm['rho'] + (1 - prm['rho']) * (prm['beta'] + (1 - prm['beta']) * lam)
    own = 0.5 * eH * WH
    print(f"r={r:5.2f} on_branch={on} Delta={Delta:.4f} tau={tau:.4f} lamE={lE:.4f} lamR={lam:.4f} eH={eH:.5f} WH={WH:.5f} own={own:.6f}")
