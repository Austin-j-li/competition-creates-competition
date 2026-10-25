import sys; sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W1_B')
from engine import *
from mpmath import e as E
# 1. exact difference identity: gam*gam'*(J'-J) = Gamma*(gH'-cH)*(Delta'-Delta) - gam'*Delta*(gH-gH')
h, l, p, cH = mpf(10), mpf(1), mpf(1)/2, mpf(6)
def unif(r): return lambda y: mpf(0) if y <= 0 else (mpf(1) if y >= r else y/r)
A = auction(unif(mpf('1.3')), h, l, p, cH, pts=(mpf('1.3'),)); B = auction(unif(mpf('2.9')), h, l, p, cH, pts=(mpf('2.9'),))
Gam = h - l
lhs = A['gam']*B['gam']*(B['J']-A['J']); rhs = Gam*(B['gH']-cH)*(B['Delta']-A['Delta']) - B['gam']*A['Delta']*(A['gH']-B['gH'])
print("difference identity:", float(lhs), float(rhs))
# 2. robustness of the non-interval example to mixing a uniform on [0, 10] with weight eps0 into every law
rho, pi, k = mpf(1)/4, mpf(1)/2, mpf(1)/50
u = E - 1; M = M_of(pi, u)
w, eps = mpf(17)/20, mpf(1)/50
def Fmix(a, b, e0):
    def F(y):
        def U(c): return mpf(0) if y <= c-eps else (mpf(1) if y >= c+eps else (y-c+eps)/(2*eps))
        base = w*U(a) + (1-w)*U(b)
        un = mpf(0) if y <= 0 else (mpf(1) if y >= 10 else y/10)
        return (1-e0)*base + e0*un
    return F
for e0 in [mpf(0), mpf('0.001'), mpf('0.003')]:
    out = []
    for (a, b) in [(mpf('0.55'), mpf('1.38')), (mpf('0.95'), mpf('1.38')), (mpf('0.95'), mpf('1.46'))]:
        Ax = auction(Fmix(a, b, e0), h, l, p, cH, pts=(a-eps, a+eps, b-eps, b+eps))
        out.append((round(float(Ax['J']),5), round(float(Ax['tau']),4), coexist_criterion(Ax['Delta'], Ax['tau'], pi, rho, k, u)))
    print("mix weight", float(e0), out)
# 3. elasticity ratios on the benchmark path: eps_Delta/eps_m = (gH-cH)/(eta*Delta) and the (c) thresholds
from mpmath import diff
def Delta(r): return (r-l)**2/(2*r)
def gH(r): return h - r/2 - p**2/(2*r)
def gL(r): return (l**2-p**2)/(2*r)
def tau(r): return (cH-gL(r))/(gH(r)-gL(r))
def eta(r): return -diff(gH, r)/diff(Delta, r)
rs = [mpf(6)/5 + (mpf(18)/5-mpf(6)/5)*i/1000 for i in range(1001)]
rat = [(gH(r)-cH)/(eta(r)*Delta(r)) for r in rs]
sig = [Delta(r)/Gam for r in rs]
print("min eps_Delta/eps_m:", float(min(rat)), " needed for J: max(1-sigma) =", float(max(1-s for s in sig)),
      " needed for Delta(1-tau)^2: max 2(1-sigma)/(1+sigma) =", float(max(2*(1-s)/(1+s) for s in sig)))
r2 = mpf(18)/5
print("at r2: gH-cH =", float(gH(r2)-cH), " 2*eta*Delta =", float(2*eta(r2)*Delta(r2)))
# 4. eta at r0 and the prior-free condition k*eta_bar <= Gamma*rho^2/4
print("eta(r0) =", float(eta(mpf(6)/5)), " k*eta(r0) =", float(k*eta(mpf(6)/5)), " Gamma rho^2/4 =", float(Gam*rho**2/4),
      " factor =", float(Gam*rho**2/4/(k*eta(mpf(6)/5))))
# 5. the referee family with benchmark slot (M=0.7311), k=2: coexistence set
pts=[]
for i in range(0, 2001):
    z = mpf(5) + mpf(i)/1000
    D = z-1; t = 2/(10-z)
    if coexist_criterion(D, t, pi, rho, mpf(2), u): pts.append(float(z))
print("the referee family, benchmark slot, k=2: coexistence from", pts[0], "to", pts[-1], "; tau=M at z =", float(10-2/M))
