# Same construction with EVERY benchmark primitive (h,l,p,cH,k,rho,pi, slot) and only the incumbent family changed.
import sys; sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W1_B')
from engine import *
from mpmath import e as E
h, l, p, cH = mpf(10), mpf(1), mpf(1)/2, mpf(6)
rho, pi, k = mpf(1)/4, mpf(1)/2, mpf(1)/50
u = E - 1; beta = mpf('0.294655'); lam = u*beta/(1+u*beta); M = M_of(pi, u)
def closed(w, a, b):
    D = (1-w)*(b-l); gL = w*(l-a); gH = w*(h-a) + (1-w)*(h-b); gam = gH - gL
    tau = (cH-gL)/gam
    return D, tau, D*(1-tau)
# search w, b1 with a: 0.55 -> 0.95
best=None
for wi in range(10, 20):
    w = mpf(wi)/20
    for bi in range(1, 400):
        b1 = 1 + mpf(bi)/1000
        D1,t1,J1 = closed(w, mpf('0.55'), b1); D2,t2,J2 = closed(w, mpf('0.95'), b1)
        if not (J1 > k > J2 and pi < t1 and t2 < M): continue
        # phase 3 re-crossing
        bb=b1; ok=False
        while bb < b1 + 1:
            bb += mpf(1)/10000
            D3,t3,J3 = closed(w, mpf('0.95'), bb)
            if t3 > M or rho*D3/2 > k: break
            if J3 > k*mpf('1.02'): ok=True; break
        if ok:
            sc = min((J1-k)/k, (k-J2)/k)
            if best is None or sc > best[0]: best=(sc, w, b1, bb, (D1,t1,J1),(D2,t2,J2),(D3,t3,J3))
sc,w,b1,b3,P1,P2,P3 = best
print("margin", float(sc), "w", float(w), "b1", float(b1), "b3", float(b3))
for P in (P1,P2,P3): print([float(x) for x in P], coexist_criterion(P[0],P[1],pi,rho,k,u))
