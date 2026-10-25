# Benchmark: point masses h=10, l=1, p=1/2, R~U[0,r], c_H=6, k=1/50, rho=1/4, pi=1/2, 1+u=e
from mpmath import mp, mpf, e, sqrt, diff, findroot
mp.dps = 30
h, l, p, cH, k, rho = mpf(10), mpf(1), mpf(1)/2, mpf(6), mpf(1)/50, mpf(1)/4
u = e - 1
M = (1+u)/(2+u)
Gam = h - l
def Delta(r): return (r-l)**2/(2*r)
def gH(r): return h - r/2 - p**2/(2*r)
def gL(r): return (l**2 - p**2)/(2*r)
def gam(r): return gH(r) - gL(r)
def tau(r): return (cH - gL(r))/gam(r)
def J(r): return Delta(r)*(1-tau(r))
def eta(r): return -diff(gH, r)/diff(Delta, r)
print("M =", M, " 1-M =", 1-M, " Gamma(1-M)^2 =", Gam*(1-M)**2, " /k =", Gam*(1-M)**2/k)
# check J' formula: J' = (Delta'/gamma) [Gamma(1-tau) - eta*Delta]
for r in [mpf('1.2'), mpf('1.394'), mpf('2'), mpf('3'), mpf('3.6')]:
    lhs = diff(J, r)
    rhs = diff(Delta, r)/gam(r) * (Gam*(1-tau(r)) - eta(r)*Delta(r))
    print(f"r={float(r):.3f} J'={float(lhs):.6e} formula={float(rhs):.6e}  eta={float(eta(r)):.4f} "
          f"Gam(1-tau)={float(Gam*(1-tau(r))):.4f} etaDelta={float(eta(r)*Delta(r)):.4f} "
          f"gH-cH={float(gH(r)-cH):.4f} sigma={float(Delta(r)/Gam):.5f}")
# Elasticity comparison (E): gH - cH >= eta*Delta on the path; worst at r2
r0, r1, r2 = mpf(6)/5, mpf(3), mpf(18)/5
print("(E) at r2: gH-cH =", gH(r2)-cH, " eta*Delta =", eta(r2)*Delta(r2), " ratio =", (gH(r2)-cH)/(eta(r2)*Delta(r2)))
print("(J) at r2: Gam(1-tau) =", Gam*(1-tau(r2)), " ratio =", Gam*(1-tau(r2))/(eta(r2)*Delta(r2)))
# eta*Delta closed form: (r-1)(r^2-p^2)/(2r(r+1))
for r in [r0, mpf(2), r2]:
    print("etaDelta closed", float((r-l)*(r**2-p**2)/(2*r*(r+l))), float(eta(r)*Delta(r)))
# scan monotonic pieces
import numpy as np
rs = [r0 + (r2-r0)*i/2000 for i in range(2001)]
ed = [eta(r)*Delta(r) for r in rs]; gm = [gH(r)-cH for r in rs]
print("etaDelta increasing:", all(ed[i+1] > ed[i] for i in range(2000)), " gH-cH decreasing:", all(gm[i+1] < gm[i] for i in range(2000)))
print("min over path of (gH-cH)/(eta*Delta):", min(g/x for g,x in zip(gm,ed)))
print("min over path of Gam(1-tau)/(eta*Delta):", min(Gam*(1-tau(r))/(eta(r)*Delta(r)) for r in rs))
# marked strengths
rA = findroot(lambda r: J(r)-k, mpf('1.39'))
rJ = findroot(lambda r: rho*J(r)-k, mpf('1.96'))
rF = findroot(lambda r: Delta(r)*(1-M)-k, mpf('1.46'))
rN = findroot(lambda r: rho*Delta(r)/2-k, mpf('1.75'))
rC = findroot(lambda r: tau(r)-M, mpf('3.59'))
print("rA,rF,rN,rJ,rC =", [float(x) for x in (rA,rF,rN,rJ,rC)])
print("tau(rA) =", tau(rA), " eta(rA) =", eta(rA), " Delta(rA)=", Delta(rA))
print("local up-set margin at rA: Gam(1-tauA)^2 / (k eta) =", Gam*(1-tau(rA))**2/(k*eta(rA)))
# relevant band for crossings at prior 1/2: Delta in (k/(1-pi), k/(1-M))
rlo = findroot(lambda r: Delta(r)-k/(1-mpf(1)/2), mpf('1.33'))
print("band of crossing strengths: [", float(rlo), ",", float(rF), "] eta range:", float(eta(rF)), float(eta(rlo)))
print("(K) k*eta_bar vs Gam(1-M)^2: eta(rlo)=", float(eta(rlo)), " ratio=", float(Gam*(1-M)**2/(k*eta(rlo))),
      " with eta(r0)=", float(eta(r0)), " ratio=", float(Gam*(1-M)**2/(k*eta(r0))))
# Lemma (c): Delta(1-tau)^2 increasing iff Gam(1-tau) >= Delta(1+tau+2 eps_L)
def epsL(r): return eta(r)-1
print("(c) margin min over [r0,r2]:", min(Gam*(1-tau(r)) - Delta(r)*(1+tau(r)+2*epsL(r)) for r in rs))
def K2(r): return Delta(r)*(1-tau(r))**2
print("(c) check derivative sign at r2:", diff(K2, r2) > 0)
# low-class-untouched condition cH - gL >= M^2 Gamma, as a curiosity
print("M^2*Gamma =", M**2*Gam, " cH =", cH)
