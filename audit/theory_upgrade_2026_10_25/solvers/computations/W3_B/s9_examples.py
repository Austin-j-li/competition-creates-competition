import sys, math
sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W3_B')
from model import *

def show(P, rs, label):
    print("---", label)
    for r in rs:
        A = auction(P, r)
        D, tau, J = A['Delta'], A['tau'], A['J']
        Ls = Lam_star(D, P) if D > 2*P.k else float('nan')
        lam = min(P.lbar, Ls)
        print("  r=%.3f Delta=%.4f tau=%.4f J=%.5f lamE=%.4f Lam*=%.4f M_lam-tau=%+.4f phi*=%+.5f rhoD/2-k=%+.4f" % (
            r, D, tau, J, lamE_of(tau,P) if tau > 0.5 else float('nan'), Ls, M_of(lam,P)-tau, phi_star(D,tau,P), P.rho*D/2-P.k))

P1 = Par(h=10, ell=1, p=0.5, cH=4.75, k=0.02, rho=0.25, beta=0.3, a=2.0, lbar=0.9)
show(P1, [1.36, 1.37, 1.40, 1.43, 1.46, 1.50, 1.60, 1.70, 1.80, 1.90, 2.0, 3.0, 4.0, 4.9, 5.0], "two segments, J rising? (cH=4.75, a=2)")
# J monotone on [1.2, 5]?
rs = [1.2 + i*0.001 for i in range(3801)]
Js = [auction(P1, r)['J'] for r in rs]
print("  J increasing on [1.2, 5.0]:", all(Js[i+1] > Js[i] for i in range(len(Js)-1)))
P2 = Par(h=10, ell=1, p=0.5, cH=6.25, k=0.02, rho=0.25, beta=0.3, a=0.3, lbar=0.9)
show(P2, [3.5, 3.6, 3.62, 4.0, 4.3, 4.34, 4.35, 4.5, 5.0], "exit before the cap with J rising (cH=6.25, a=0.3, lbar=0.9)")
rs = [3.0 + i*0.001 for i in range(2001)]
Js = [auction(P2, r)['J'] for r in rs]
print("  J increasing on [3.0, 5.0]:", all(Js[i+1] > Js[i] for i in range(len(Js)-1)))
