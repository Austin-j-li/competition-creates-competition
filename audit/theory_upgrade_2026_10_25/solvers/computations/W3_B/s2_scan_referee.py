import sys
sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W3_B')
from model import *
from scan import research_equilibria

X = Par(h=10, ell=1, p=0.5, cH=4.5, k=0.5, rho=0.5, beta=0.2, a=0.01, lbar=0.4)
for rule in ("IM", "I0"):
    print("=== the referee path, investor rule", rule, "challenger C1 ===")
    for r in (4.5, 5.0, 5.5, 5.82, 5.9, 6.2, 6.5, 7.0, 7.25, 7.4, 8.0, 9.0):
        A, res = research_equilibria(r, X, rule, n=3000)
        D, tau = A['Delta'], A['tau']
        Ls = Lam_star(D, X) if D > 2*X.k else None
        LQ = Lam_Q(D, X)
        print("r=%.3f Delta=%.4f tau=%.4f rhoD/2-k=%+.4f lamE=%.4f Lam*=%s lamQ=%s Mlbar-tau=%+.4f" % (
            r, D, tau, X.rho*D/2-X.k, lamE_of(tau,X), ("%.5f"%Ls) if Ls else "-", ("%.5f"%LQ) if LQ else "-", M_of(X.lbar,X)-tau))
        for e in res:
            extra = ""
            if 'mum' in e:
                extra = " mu(1)=%.4f mu(-1)=%.4f t=%.4f UH=%.4f UL=%.4f" % (e['mu1'], e['mum'], e['t'], e['UH'], e['UL'])
            print("     lam=%.5f form=%-10s entry=%.6f%s" % (e['lam'], e['form'], e['entry'], extra))
