import sys, math
sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W3_B')
from model import *

def t_of(theta, p, r):
    if theta <= r:
        return p*p/r + (theta*theta - p*p)/(2*r) + theta*(r-theta)/r
    return p*p/r + (r*r - p*p)/(2*r)

def check_Q(P, r, label):
    A = auction(P, r); D, tau = A['Delta'], A['tau']
    t0 = P.p*(1-P.p/r); tH, tL = t_of(P.h,P.p,r), t_of(P.ell,P.p,r); gH, gL = A['gH'], A['gL']
    lam = Lam_Q(D, P); b = (1-lam)*P.beta; b0 = (1-lam)*(1-2*P.beta)
    fH = {-1: b, 0: b0, 1: b+lam}; fL = {-1: b+lam, 0: b0, 1: b}
    mu = {x: fH[x]/(fH[x]+fL[x]) for x in (-1,0,1)}
    e = {x: P.rho + (1-P.rho)*(1.0 if mu[x]*gH+(1-mu[x])*gL >= P.cH else 0.0) for x in (-1,0,1)}
    price = {x: t0 + e[x]*(mu[x]*(tH-t0) + (1-mu[x])*(tL-t0)) for x in (-1,0,1)}
    U = {(j,q): q*(t0 + e[q]*(tj-t0) - price[q]) - P.k*abs(q) for j, tj in (("H",tH),("L",tL)) for q in (-1,0,1)}
    V = 0.5*max(U[("H",q)] for q in (-1,0,1)) + 0.5*max(U[("L",q)] for q in (-1,0,1))
    print(f"--- Q-research {label}: r={r} lam_Q={lam:.6f} lamE={lamE_of(tau,P):.6f}")
    print("    mu=(%.4f, %.4f, %.4f) tau=%.4f e=(%.2f, %.2f, %.2f)" % (mu[-1], mu[0], mu[1], tau, e[-1], e[0], e[1]))
    print("    U_H=(%.6f, %.6f, %.6f) U_L=(%.6f, %.6f, %.6f)  V/a=%.6f" % (U[("H",-1)],U[("H",0)],U[("H",1)],U[("L",-1)],U[("L",0)],U[("L",1)], V/P.a))
    ent = sum((0.5*fH[x]+0.5*fL[x])*e[x] for x in (-1,0,1))
    print("    entry=%.6f" % ent)

u = math.e - 1; beta = 0.294655; lbar = u*beta/(1+u*beta)
B = Par(h=10, ell=1, p=0.5, cH=6, k=0.02, rho=0.25, beta=beta, a=1/40, lbar=lbar)
X = Par(h=10, ell=1, p=0.5, cH=4.5, k=0.5, rho=0.5, beta=0.2, a=0.01, lbar=0.4)
check_Q(B, 1.9, "benchmark"); check_Q(X, 6.5, "the referee")

# critical values of each primitive for condition (ii) at the benchmark
mb = m_of(B.lbar, B)
print("\nbenchmark condition (ii) rho(2 a lbar + k) <= 2 k m_lbar; critical values one at a time:")
print("  a*   = %.6f (benchmark 0.025)" % ((2*B.k*mb/B.rho - B.k)/(2*B.lbar)))
print("  rho* = %.6f (benchmark 0.25)" % (2*B.k*mb/(2*B.a*B.lbar + B.k)))
print("  k*   = %.6f (benchmark 0.02; (ii) fails for k below)" % (2*B.rho*B.a*B.lbar/(2*mb - B.rho)))
# lbar with beta fixed: rho(2 a L + k) <= 2k m_L
lstar = bisect(lambda L: 2*B.k*m_of(L,B) - B.rho*(2*B.a*L + B.k), 0.01, 0.99)
print("  lbar*= %.6f (benchmark %.6f)" % (lstar, B.lbar))
# weaker condition for the cap to come before the full sale: rho(2 a lbar + k) <= k
print("  cap before full sale: rho(2a lbar+k)/k = %.4f (<=1 needed)" % (B.rho*(2*B.a*B.lbar+B.k)/B.k))
print("the referee: (ii) normalized = %.4f ; rho(2a lbar+k)/k = %.4f" % (X.rho*(1+2*X.a*X.lbar/X.k)*(1+(X.lbar/((1-X.lbar)*X.beta))/2), X.rho*(2*X.a*X.lbar+X.k)/X.k))
# share of Prop A.2 cost window where (ii) fails
alo, aup = 0.021469, 0.036763; acr = (2*B.k*mb/B.rho - B.k)/(2*B.lbar)
print("share of A.2 window (a_lo,a_up) with a > a*: %.3f" % ((aup-acr)/(aup-alo)))
# at a in (a*, a_up), check: R-branch end at r_N with research below cap, extended branch reaches cap later
for a in (0.035, 0.036):
    P = Par(h=10, ell=1, p=0.5, cH=6, k=0.02, rho=0.25, beta=beta, a=a, lbar=lbar)
    rN = fr(2*P.k/P.rho, P); lamN = Lam_R(2*P.k/P.rho, P)
    Dcap = (2*P.a*P.lbar + P.k)/mb if P.rho*(2*P.a*P.lbar+P.k) <= P.k else 2*(P.a*P.lbar+P.k)/((1+P.rho)*mb)
    print("  a=%.3f: research at r_N=%.6f is %.6f < lbar=%.6f; extended branch reaches the cap at r=%.6f (L mixing); r_R=%.6f" % (
        a, rN, lamN, P.lbar, fr(Dcap,P), bisect(lambda r: phi_star(auction(P,r)['Delta'],auction(P,r)['tau'],P), 1.2, rN)))
