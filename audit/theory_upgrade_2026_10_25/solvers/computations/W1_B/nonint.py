# Non-interval coexistence set with point-mass classes (benchmark h,l,p,cH,rho,pi, benchmark slot)
# Incumbent: mixture w*U[a-eps,a+eps] + (1-w)*U[b-eps,b+eps], with p<a-eps<a+eps<l<b-eps, b+eps<h.
# Path in three phases (each a FOSD strengthening): b: b0->b1, then a: a0->a1, then b: b1->b2.
import sys; sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W1_B')
from engine import *
from mpmath import e as E
h, l, p, cH = mpf(10), mpf(1), mpf(1)/2, mpf(6)
rho, pi = mpf(1)/4, mpf(1)/2
u = E - 1; beta = mpf('0.294655'); lam = u*beta/(1+u*beta)
M = M_of(pi, u)
def closed(w, a, b):
    D = (1-w)*(b-l); gL = w*(l-a); gH = w*(h-a) + (1-w)*(h-b); gam = gH - gL
    tau = (cH-gL)/gam
    return D, tau, D*(1-tau)
best = None
import itertools
for w in [mpf(x)/20 for x in range(6, 19)]:
    for a0, a1 in [(mpf('0.55'), mpf('0.95'))]:
        # choose b1 so that tau(a1,b1) = M - margin, then pick k between J(a1,b1) and J(a0,b1)
        for b1 in [mpf(1) + mpf(i)/100 for i in range(10, 400)]:
            D1, t1, J1 = closed(w, a0, b1)   # end of phase 1
            D2, t2, J2 = closed(w, a1, b1)   # end of phase 2
            if not (pi < t1 and t2 < M): continue
            # phase 3: raise b until tau hits M or rho*D/2 hits k; J3 max on that stretch
            k = (J1 + J2)/2
            if rho*D1/2 > k: continue
            J3max, b3 = None, None
            bb = b1
            while True:
                bb += mpf(1)/1000
                D3, t3, J3 = closed(w, a1, bb)
                if t3 > M or rho*D3/2 > k or bb > h - 1: break
                if J3max is None or J3 > J3max: J3max, b3 = J3, bb
            if J3max is None or J3max <= k: continue
            score = min((J1-k)/k, (k-J2)/k, (J3max-k)/k)
            if best is None or score > best[0]:
                best = (score, w, a0, a1, b1, b3, k, (D1,t1,J1), (D2,t2,J2), closed(w,a1,b3))
print("best relative margin:", float(best[0]))
score, w, a0, a1, b1, b3, k, P1, P2, P3 = best
print("w=",float(w)," a0=",float(a0)," a1=",float(a1)," b1=",float(b1)," b3=",float(b3)," k=",float(k), " M=", float(M))
for name, P in [("end phase 1", P1), ("end phase 2", P2), ("in phase 3", P3)]:
    D, t, J = P
    print(f"{name}: Delta={float(D):.5f} tau={float(t):.5f} J={float(J):.5f} rhoDelta/2={float(rho*D/2):.5f} crit={coexist_criterion(D,t,pi,rho,k,u)}")
