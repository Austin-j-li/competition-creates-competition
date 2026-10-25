"""Benchmark research branch: elasticities of the information channel; primitive-condition margins."""
import sys
from math import e as EU
sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W2_B')
from model import branch, eps_e, auction

u = EU - 1
beta = 0.294655  # registry beta_B (rounded); cap = u*beta/(1+u*beta)
cap = u * beta / (1 + u * beta)
bm = dict(h=10, ell=1, p=0.5, cH=6.0, rho=0.25, k=0.02, beta=beta, a=1 / 40, cap=cap)
print("benchmark cap", cap)
for r in [1.501023, 1.55, 1.60, 1.65, 1.677]:
    b = branch(r, bm)
    ee, lam, dlam = eps_e(b['Delta'], bm)
    D1 = 0.5 * (1 - 1 / r ** 2)  # Delta'(r) for point masses, ell=1, r<h
    dlnD_dlnr = r * D1 / b['Delta']
    print(f"r={r:.4f} on={b['on_branch']} Delta={b['Delta']:.6f} lamR={lam:.6f} eH={b['eH']:.6f} eL={b['eL']:.6f} "
          f"own={b['own']:.6f} eps_e(dlnEH/dlnDelta)={ee:.4f} dlnDelta/dlnr={dlnD_dlnr:.4f} "
          f"dln eH/dln r={ee*dlnD_dlnr:.4f}")

# Primitive condition P2 for point masses + uniform: cH >= gH(r=h) = (h^2-p^2)/(2h)
h, p = 10, 0.5
gH_at_h = (h * h - p * p) / (2 * h)
print("\nP2: gH at r=h:", gH_at_h, " benchmark cH=6, margin", 6 - gH_at_h, " ratio", 6 / gH_at_h)
print("P1 margins: h - rbar_R =", 10 - 1.677633, " h - r2 =", 10 - 3.6, " h/r2 =", 10 / 3.6)
# tau at r = h at benchmark cH
au = auction(10.0, 10, 1, 0.5)
print("benchmark tau at r=h:", (6 - au['gL']) / (au['gH'] - au['gL']))
# smallest cH for which tau<1 is possible at r just above h? tau<1 iff gH>cH
print("Counterexample cH=2.5 < gH(h) =", gH_at_h, ": P2 fails; branch at r>h possible iff r < (h^2-p^2)/(2cH) =", (h*h-p*p)/(2*2.5))

# Prop 2 benchmark ownership ratio eH/rho
lamB = 0.336122; bB = 0.195615
eH = 0.25 + 0.75 * (bB + lamB)
print("\nProp 2 benchmark: eH =", eH, " eH/rho =", eH / 0.25, " -> ownership rises unless W_H falls by more than", 1 - 0.25 / eH)
