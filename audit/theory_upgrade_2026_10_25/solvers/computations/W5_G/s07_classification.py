"""Sign of T = Pbar - P(0) as tau moves through (m, pi, M); uninformative-order version on branch R;
general-prior covariances of A.13(iii); M-m versus the informed share."""
import sys
sys.path.insert(0, "audit/theory_upgrade_2026_10_25/solvers/computations/W5_G")
from mpmath import mp, mpf, nstr
from model import *

s = slot()
u, lam, b, b0, beta = s["u"], s["lam"], s["b"], s["b0"], s["beta"]
eta = {-1: beta, 0: 1 - 2 * beta, 1: beta}
X = (-1, 0, 1)

print("== T sign classification under C1 (full orders, benchmark r=3, tau moved by c_H) ==")
pi, r = mpf("0.6"), mpf(3)
a = auction(r)
M, m = Mtop(pi, u), mbot(pi, u)
print(f"   m={nstr(m,6)} pi={nstr(pi,3)} M={nstr(M,6)}")
p1, pm1 = b + pi * lam, b + (1 - pi) * lam
for tau in (mpf("0.2"), m, mpf("0.45"), pi, mpf("0.7"), M, mpf("0.9")):
    ent = {x: (mpf(1) if mu >= tau else rho) for x, mu in ((-1, m), (0, pi), (1, M))}
    post = {-1: m, 0: pi, 1: M}
    P = {x: a["t0"] + ent[x] * (a["wL"] + a["D"] * post[x]) for x in X}
    prob = {1: p1, -1: pm1, 0: b0}
    T = sum(prob[x] * P[x] for x in X) - P[0]
    print(f"   tau={nstr(tau,6):9} entry={[nstr(ent[x],2) for x in X]}  T={nstr(T,6)}")
print("   (incentive margins are not imposed in this sweep; it checks the identity's sign only)")

print("\n== uninformative-order version on branch R (sale uninformative), pi=0.55, r=1.45 ==")
pi, r = mpf("0.55"), mpf("1.45")
a = auction(r)
sR = b * ((1 - pi) * a["D"] / k - 1) / pi
sH = {-1: 0, 0: 1 - sR / lam, 1: sR / lam}
sL = {-1: 0, 0: 1, 1: 0}
fH = {x: (1 - lam) * eta[x] + lam * sH[x] for x in X}
fL = {x: (1 - lam) * eta[x] + lam * sL[x] for x in X}
mu = {x: pi * fH[x] / (pi * fH[x] + (1 - pi) * fL[x]) for x in X}
ent = {x: (mpf(1) if mu[x] >= a["tau"] else rho) for x in X}
P = {x: a["t0"] + ent[x] * (a["wL"] + a["D"] * mu[x]) for x in X}
prob = {x: pi * fH[x] + (1 - pi) * fL[x] for x in X}
Pbar = sum(prob[x] * P[x] for x in X)
U = {j: {q: q * (a["t0"] + ent[q] * (tj - a["t0"]) - P[q]) - k * abs(q) for q in X}
     for j, tj in (("H", a["tH"]), ("L", a["tL"]))}
print("   posteriors", {x: nstr(mu[x], 6) for x in X}, " entry", {x: nstr(ent[x], 2) for x in X})
print("   U_H", {q: nstr(U["H"][q], 6) for q in X}, " U_L", {q: nstr(U["L"][q], 6) for q in X})
print(f"   Pbar-P(-1) = {nstr(Pbar-P[-1],8)}  formula sum p_x(e_x-rho)A(mu_x) = "
      f"{nstr(sum(prob[x]*(ent[x]-rho)*(a['wL']+a['D']*mu[x]) for x in X),8)};  Pbar-P(0) = {nstr(Pbar-P[0],8)}")

print("\n== A.13(iii) at a general prior: Cov(X,1_A) = (e+-rho) p1 (1-E[X]); Cov(X, mu(X)) = 2 pi(1-pi) lam ==")
for pi in (mpf("0.3"), mpf("0.5"), mpf("0.6")):
    for r in (mpf(3), mpf("3.6")):
        F = full_orders(pi, r)
        prob, ent, post = F["prob"], F["ent"], F["post"]
        EX = prob[1] - prob[-1]
        EA = sum(prob[x] * ent[x] for x in X)
        cov = sum(prob[x] * x * ent[x] for x in X) - EX * EA
        covmu = sum(prob[x] * x * post[x] for x in X) - EX * pi
        print(f"   pi={nstr(pi,2)} r={nstr(r,2)}: Cov(X,1_A)={nstr(cov,8)} formula={nstr((ent[1]-ent[0])*prob[1]*(1-EX),8)}"
              f"  Cov(X,mu)={nstr(covmu,8)} 2pi(1-pi)lam={nstr(2*pi*(1-pi)*lam,8)}")

print("\n== M-m versus the informed share u/(2+u) (prior-free) ==")
th = u / (2 + u)
for pi in (mpf("0.1"), mpf("0.3"), mpf("0.5"), mpf("0.7")):
    M, m = Mtop(pi, u), mbot(pi, u)
    q = pi * (1 - pi)
    print(f"   pi={nstr(pi,2)}: M-m={nstr(M-m,8)}  theta*q(2+u)^2/(1+u+u^2 q)={nstr(th*q*(2+u)**2/(1+u+u*u*q)*(2+u)/(2+u),8)}"
          f"  closed form q u (2+u)/((1+u pi)(1+u(1-pi)))={nstr(q*u*(2+u)/((1+u*pi)*(1+u*(1-pi))),8)}  theta={nstr(th,6)}"
          f"  sale-impact share of class comp p1/v={nstr((b+pi*lam)/(2*b+lam),5)}")
