import sys, math
sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W3_B')
from model import *
from scan import research_equilibria
u = math.e - 1; beta = 0.294655; lbar = u*beta/(1+u*beta)
P = Par(h=10, ell=1, p=0.5, cH=6, k=0.02, rho=0.25, beta=beta, a=0.2, lbar=lbar)
print("a=0.2: Lam_sw = %.4f, r_N=%.4f, r at L full sale on branch:" % (P.k*(1-P.rho)/(2*P.a*P.rho), fr(2*P.k/P.rho,P)))
for r in (2.25, 2.4, 2.5, 2.6, 2.66, 2.7, 3.0, 3.5):
    A, res = research_equilibria(r, P, "IM", n=3000)
    D = A['Delta']
    print("r=%.2f Lam*=%.5f lamE=%.5f lamQ=%s" % (r, Lam_star(D,P), lamE_of(A['tau'],P), ("%.5f" % Lam_Q(D,P)) if Lam_Q(D,P) else '-'))
    for e in res:
        print("    lam=%.5f %-10s entry=%.6f" % (e['lam'], e['form'], e['entry']) + ((" t/lam=%.3f UL=%.5f" % (e['t']/e['lam'] if e['lam']>0 else 0, e['UL'])) if 't' in e else ""))
a_max = None
rC = bisect(lambda r: auction(P,r)['tau'] - M_of(lbar,P), 2.0, 3.6)
JC = auction(P, rC)['J']
print("benchmark: branch disappears for a >= a_max = %.5f (r_C=%.6f, J(r_C)=%.5f)" % ((JC - P.k + max(P.rho*JC-P.k,0))/(2*lbar), rC, JC))
