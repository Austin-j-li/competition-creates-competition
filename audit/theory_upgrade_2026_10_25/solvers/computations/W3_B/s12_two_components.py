import sys
sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W3_B')
from model import *
from scan import research_equilibria
P1 = Par(h=10, ell=1, p=0.5, cH=4.75, k=0.02, rho=0.25, beta=0.3, a=2.0, lbar=0.9)
for r in (1.40, 1.45, 1.55, 1.70, 1.85, 2.5, 4.0, 4.95):
    A, res = research_equilibria(r, P1, "IM", n=20000)
    print("r=%.2f tau=%.5f J=%.5f Lam*=%.5f lamE=%.5f :" % (r, A['tau'], A['J'], Lam_star(A['Delta'],P1), lamE_of(A['tau'],P1)),
          ["%s lam=%.5f entry=%.4f" % (e['form'], e['lam'], e['entry']) for e in res])
# boundaries of the recruiting set
g = lambda r: phi_star(auction(P1,r)['Delta'], auction(P1,r)['tau'], P1)
t_half = bisect(lambda r: auction(P1,r)['tau'] - 0.5, 1.2, 1.5)
print("tau=1/2 at r=%.6f; phi* zeros at %.6f, %.6f, %.6f" % (t_half, bisect(g,1.42,1.5), bisect(g,1.8,1.95), bisect(g,4.8,5.0)))
print("normalized research cost 2a lbar/k = %.1f (benchmark 0.84)" % (2*P1.a*P1.lbar/P1.k))
