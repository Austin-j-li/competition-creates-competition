"""Recompute the counterexample and the two channels of ownership along it."""
import sys
sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W2_B')
from model import branch, eps_e

cx = dict(h=10, ell=1, p=0.5, cH=2.5, rho=0.05, k=0.2, beta=0.2, a=5.0, cap=0.9)
print("Counterexample primitives:", cx)
for r in [10.0, 10.5, 11.0, 11.5, 12.0, 13, 14, 15, 16, 18, 19.9]:
    b = branch(r, cx)
    if b['lam'] is None:
        print(r, 'no lambda_R')
        continue
    ee, lam, dlam = eps_e(b['Delta'], cx)
    # eta: elasticity of W_H w.r.t. Delta along the uniform path (numerical)
    dr = 1e-6
    b2 = branch(r + dr, cx)
    dlnW = (b2['WH'] - b['WH']) / b['WH']
    dlnD = (b2['Delta'] - b['Delta']) / b['Delta']
    eta = -dlnW / dlnD if dlnD != 0 else float('nan')
    print(f"r={r:5.2f} on_branch={b['on_branch']} Delta={b['Delta']:.6f} tau={b['tau']:.6f} "
          f"lamE={b.get('lamE', float('nan')):.6f} lamR={b['lam']:.6f} entry={b.get('entry', float('nan')):.6f} "
          f"eH={b.get('eH', float('nan')):.6f} WH={b['WH']:.6f} own={b.get('own', float('nan')):.6f} "
          f"eps_e={ee:.4f} eta={eta:.4f} rhoDelta-2k={cx['rho']*b['Delta']-2*cx['k']:.4f}")

# The two channels between r = 11 and r = 12
b11, b12 = branch(11.0, cx), branch(12.0, cx)
print()
print("Ownership ratio O(12)/O(11)     =", b12['own'] / b11['own'])
print("  information channel eH ratio =", b12['eH'] / b11['eH'])
print("  direct channel WH ratio      =", b12['WH'] / b11['WH'])
print("Research premium O^R/O^Z = eH/rho at 11, 12:", b11['eH'] / cx['rho'], b12['eH'] / cx['rho'])
print("Share of H acquisitions by recruited challengers 1 - rho/eH:", 1 - cx['rho'] / b11['eH'], 1 - cx['rho'] / b12['eH'])
# conditional ownership at incumbent value x <= 10 (H wins for sure): 0.5*eH
for x in [5.0, 9.0, 10.5]:
    sH = 1.0 if x < cx['h'] else 0.0
    print(f"Pr(H acquires | R={x}) at r=11: {0.5*b11['eH']*sH:.6f}, at r=12: {0.5*b12['eH']*sH:.6f}")
# share of challenger acquisitions won by H
for b in (b11, b12):
    odds = (b['eH'] * b['WH']) / (b['eL'] * b['WL'])
    print(f"r={b['r']}: Pr(H | challenger acquires) = {odds/(1+odds):.6f};  Pr(H | prepared) = {b['eH']/(b['eH']+b['eL']):.6f}")
# incumbent's chance of losing at a given value x in [1, 10): 0.5*(eH*1 + eL*0) -> only H beats x>ell
