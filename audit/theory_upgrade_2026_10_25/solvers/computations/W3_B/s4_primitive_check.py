"""Check an extended-branch tuple (class L mixes) directly from auction primitives:
proceeds t_0,t_H,t_L, competitive prices, challenger beliefs and preparation, investor payoffs
E[V_T|j,q]-P(q), and research optimality.  Prints only."""
import sys, math
sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W3_B')
from model import *

def t_of(theta, p, r):
    # expected target proceeds when a prepared challenger with value theta >= p meets R~U[0,r]
    if theta <= r:
        return p*p/r + (theta*theta - p*p)/(2*r) + theta*(r-theta)/r
    return p*p/r + (r*r - p*p)/(2*r)

def check(P, r, label):
    A = auction(P, r)
    D, tau = A['Delta'], A['tau']
    t0 = P.p*(1 - P.p/r)
    tH, tL = t_of(P.h, P.p, r), t_of(P.ell, P.p, r)
    gH, gL = A['gH'], A['gL']
    lam = min(P.lbar, Lam_star(D, P))
    b = (1-lam)*P.beta; b0 = (1-lam)*(1-2*P.beta)
    t, mum, regime = low_class_rate(lam, D, P)
    s = lam
    fH = {-1: b, 0: b0 + lam - s, 1: b + s}
    fL = {-1: b + t, 0: b0 + lam - t, 1: b}
    mu = {x: fH[x]/(fH[x]+fL[x]) for x in (-1,0,1)}
    # entry: high-cost prepares iff belief*gH+(1-belief)*gL >= cH (C1); prices then solved jointly.
    # first pass: entry from posteriors, then check that prices separate or pool consistently
    e = {x: P.rho + (1-P.rho)*(1.0 if mu[x]*gH + (1-mu[x])*gL >= P.cH else 0.0) for x in (-1,0,1)}
    price = {x: mu[x]*(t0 + e[x]*(tH-t0)) + (1-mu[x])*(t0 + e[x]*(tL-t0)) for x in (-1,0,1)}
    # challenger belief at each price: pool orders with equal price
    belief = {}
    for x in (-1,0,1):
        same = [y for y in (-1,0,1) if abs(price[y]-price[x]) < 1e-14]
        belief[x] = sum(fH[y] for y in same)/sum(fH[y]+fL[y] for y in same)
    Bprof = {x: belief[x]*gH + (1-belief[x])*gL for x in (-1,0,1)}
    eq_check = {x: (Bprof[x] >= P.cH) == (e[x] == 1.0) for x in (-1,0,1)}
    U = {}
    for j, tj in (("H", tH), ("L", tL)):
        for q in (-1,0,1):
            U[(j,q)] = q*(t0 + e[q]*(tj-t0) - price[q]) - P.k*abs(q)
    V = 0.5*max(U[("H",q)] for q in (-1,0,1)) + 0.5*max(U[("L",q)] for q in (-1,0,1))
    print(f"--- {label}: r={r} Delta={D:.6f} tau={tau:.6f} regime(L)={regime}")
    print("    lam=%.6f  t(informed sale prob)=%.6f  sigma_L(-1)=%.6f" % (lam, t, t/lam))
    print("    posteriors mu(-1,0,1)=(%.6f, %.6f, %.6f)  tau=%.6f  M_lam=%.6f" % (mu[-1], mu[0], mu[1], tau, M_of(lam,P)))
    print("    entry e(-1,0,1)=(%.3f, %.3f, %.3f)  prices=(%.6f, %.6f, %.6f)" % (e[-1], e[0], e[1], price[-1], price[0], price[1]))
    print("    challenger gross profit at prices B=(%.4f, %.4f, %.4f) vs cH=%.3f ; preparation consistent: %s" % (Bprof[-1], Bprof[0], Bprof[1], P.cH, eq_check))
    print("    U_H(-1,0,1)=(%.6f, %.6f, %.6f)" % (U[("H",-1)], U[("H",0)], U[("H",1)]))
    print("    U_L(-1,0,1)=(%.6f, %.6f, %.6f)" % (U[("L",-1)], U[("L",0)], U[("L",1)]))
    print("    reduced form: U_H(1)=Delta*m-k=%.6f ; U_L(-1)=rho*Delta*mu(-1)-k=%.6f" % (D*m_of(lam,P)-P.k, P.rho*D*mu[-1]-P.k))
    print("    research: V=%.6f  V/a=%.6f  min(lbar,V/a)=%.6f  conjectured lam=%.6f" % (V, V/P.a, min(P.lbar, V/P.a), lam))
    ent = sum((0.5*fH[x]+0.5*fL[x])*e[x] for x in (-1,0,1))
    print("    entry=%.6f  formula rho+(1-rho)[beta+(1/2-beta)lam]=%.6f" % (ent, entry_branch(lam,P)))

X = Par(h=10, ell=1, p=0.5, cH=4.5, k=0.5, rho=0.5, beta=0.2, a=0.01, lbar=0.4)
check(X, 6.5, "the referee path, past r_N, interior research")
check(X, 8.0, "the referee path, research at the cap, L mixing")
u = math.e - 1; beta = 0.294655; lbar = u*beta/(1+u*beta)
B = Par(h=10, ell=1, p=0.5, cH=6, k=0.02, rho=0.25, beta=beta, a=1/40, lbar=lbar)
check(B, 1.9, "benchmark gray band, cap, L mixing")
