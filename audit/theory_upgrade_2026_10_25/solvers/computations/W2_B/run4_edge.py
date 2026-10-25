"""Targeted check: point masses, r > h, ownership rising requires small lambda, tiny a, k close to Delta*m."""
import sys
sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W2_B')
from model import branch, eps_e

h, ell, p = 10.0, 1.0, 0.5
cases = [
    dict(h=h, ell=ell, p=p, cH=2.734, rho=0.01, k=1.70, beta=0.2, a=0.001, cap=0.99),
    dict(h=h, ell=ell, p=p, cH=2.734, rho=0.01, k=1.50, beta=0.2, a=0.001, cap=0.99),
    dict(h=h, ell=ell, p=p, cH=2.734, rho=0.05, k=1.70, beta=0.2, a=0.01, cap=0.99),
    dict(h=h, ell=ell, p=p, cH=2.734, rho=0.25, k=1.70, beta=0.2, a=0.001, cap=0.99),
]
for prm in cases:
    print("params:", {kk: prm[kk] for kk in ('cH', 'rho', 'k', 'beta', 'a')})
    for r in [10.5, 11.0, 11.2]:
        b0, b1 = branch(r, prm), branch(r + 0.01, prm)
        if b0['lam'] is None:
            print("  r", r, "no root")
            continue
        ee, lam, _ = eps_e(b0['Delta'], prm)
        eta = 2 * r / (h + ell) - 1
        print(f"  r={r} on={b0['on_branch']} tau={b0['tau']:.4f} lamE={b0.get('lamE', float('nan')):.4f} lamR={lam:.4f} "
              f"k/(Delta*m_lamR)={prm['k']/(b0['Delta']*(prm['beta']*(1-lam)/(2*prm['beta']+(1-2*prm['beta'])*lam))):.4f} "
              f"eps_e={ee:.4f} eta={eta:.4f} own: {b0.get('own', float('nan')):.6f} -> {b1.get('own', float('nan')):.6f}")
