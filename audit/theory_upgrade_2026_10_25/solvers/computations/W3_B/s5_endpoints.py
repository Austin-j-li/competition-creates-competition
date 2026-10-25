import sys, math
sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W3_B')
from model import *

def endpoints(P, rlo, rhi, label):
    A = lambda r: auction(P, r)
    rN = fr(2*P.k/P.rho, P)
    rR = bisect(lambda r: phi_star(A(r)['Delta'], A(r)['tau'], P), rlo, rN)
    mbar = m_of(P.lbar, P)
    # cap point on the extended branch
    if P.rho*(2*P.a*P.lbar + P.k) <= P.k:
        Dcap = (2*P.a*P.lbar + P.k)/mbar; where = "while L mixes or abstains"
    else:
        Dcap = 2*(P.a*P.lbar + P.k)/((1+P.rho)*mbar); where = "after L sells fully"
    rcap = fr(Dcap, P)
    rS = fr(P.k/(P.rho*mbar), P)            # L sells fully at the cap
    rC = bisect(lambda r: A(r)['tau'] - M_of(P.lbar, P), rlo, rhi)  # ceiling
    lam_sw = P.k*(1-P.rho)/(2*P.a*P.rho)   # research at the switch to full sale (interior)
    print(f"[{label}] r_R={rR:.6f} r_N={rN:.6f} r_cap*={rcap:.6f} ({where}) r_S(lbar)={rS:.6f} r_C={rC:.6f}  Lam_sw={lam_sw:.4f} vs lbar={P.lbar:.4f}")
    # Q-research range: exists for r>r_N while lamQ < min(lamE, lbar)
    def qgap(r):
        a_ = A(r); L = Lam_Q(a_['Delta'], P)
        return min(lamE_of(a_['tau'], P), P.lbar) - L
    rr = [rN + 1e-6 + i*(rhi - rN)/4000 for i in range(4001)]
    vals = [qgap(r) for r in rr]
    ends = [ (rr[i], rr[i+1]) for i in range(len(rr)-1) if (vals[i] > 0) != (vals[i+1] > 0)]
    print("   Q-research (non-recruiting, entry rho) margin min(lamE,lbar)-lamQ at r_N+:", "%.5f" % vals[0], " sign changes near:", ["%.6f" % bisect(qgap, a, b) for a, b in ends])
    return dict(rR=rR, rN=rN, rcap=rcap, rS=rS, rC=rC)

u = math.e - 1; beta = 0.294655; lbar = u*beta/(1+u*beta)
B = Par(h=10, ell=1, p=0.5, cH=6, k=0.02, rho=0.25, beta=beta, a=1/40, lbar=lbar)
eB = endpoints(B, 1.2, 3.6, "benchmark a=1/40")
X = Par(h=10, ell=1, p=0.5, cH=4.5, k=0.5, rho=0.5, beta=0.2, a=0.01, lbar=0.4)
eX = endpoints(X, 4.0, 9.9, "the referee")
# research and entry along the referee extended branch
print("\nreferee extended branch, research and entry (IM):")
for r in [eX['rR']+1e-4, 5.0, 5.5, eX['rN'], 6.0, 6.5, 7.0, eX['rcap'], 8.0, 8.5, eX['rC']-1e-4]:
    a_ = auction(X, r); lam = min(X.lbar, Lam_star(a_['Delta'], X)); t, mum, reg = low_class_rate(lam, a_['Delta'], X)
    print("  r=%.4f lam=%.5f entry=%.5f  L:%s sigma_L(-1)=%.4f  M_lam-tau=%+.4f" % (r, lam, entry_branch(lam, X), reg, t/lam, M_of(lam,X)-a_['tau']))
