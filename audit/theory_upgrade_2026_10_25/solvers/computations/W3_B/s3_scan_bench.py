import sys, math
sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W3_B')
from model import *
from scan import research_equilibria

u = math.e - 1; beta = 0.294655; lbar = u*beta/(1+u*beta)
B = Par(h=10, ell=1, p=0.5, cH=6, k=0.02, rho=0.25, beta=beta, a=1/40, lbar=lbar)
rS = fr(B.k/(B.rho*m_of(B.lbar,B)), B)
print("benchmark r_S^lbar (rho Delta m_lbar = k) = %.6f ; r_N = %.6f ; r_U = %.6f" % (rS, fr(2*B.k/B.rho,B), fr((B.k+B.a*B.lbar)/(B.rho*m_of(B.lbar,B)),B)))
for rule in ("IM", "I0"):
    print("=== benchmark path, investor", rule, ", C1 ===")
    for r in (1.45, 1.50, 1.502, 1.55, 1.65, 1.70, 1.74, 1.76, 1.80, 1.90, 2.0, 2.1, 2.2, 2.43, 2.5, 3.0, 3.5, 3.59, 3.6):
        A, res = research_equilibria(r, B, rule, n=3000)
        D, tau = A['Delta'], A['tau']
        Ls = Lam_star(D, B) if D > 2*B.k else None
        LQ = Lam_Q(D, B)
        print("r=%.3f D=%.5f tau=%.5f lamE=%.5f Lam*=%s lamQ=%s phi*=%+.5f" % (r, D, tau, lamE_of(tau,B), ("%.5f"%Ls) if Ls else "-", ("%.5f"%LQ) if LQ else "-", phi_star(D,tau,B)))
        for e in res:
            extra = ""
            if 'mum' in e:
                extra = " mu1=%.4f mu-1=%.4f t=%.4f UH=%.5f UL=%.5f" % (e['mu1'], e['mum'], e['t'], e['UH'], e['UL'])
            print("     lam=%.5f %-10s entry=%.6f%s" % (e['lam'], e['form'], e['entry'], extra))
