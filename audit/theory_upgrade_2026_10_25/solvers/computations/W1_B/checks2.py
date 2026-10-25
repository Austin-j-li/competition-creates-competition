import sys; sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W1_B')
from engine import *
from mpmath import e as E
h, l, p, cH = mpf(10), mpf(1), mpf(1)/2, mpf(6)
rho, pi, k = mpf(1)/4, mpf(1)/2, mpf(1)/50
u = E - 1; M = M_of(pi, u); beta = mpf('0.294655'); lam = u*beta/(1+u*beta)
w, eps = mpf(17)/20, mpf(1)/50
def Fmix(a, b, e0, top):
    def F(y):
        def U(c): return mpf(0) if y <= c-eps else (mpf(1) if y >= c+eps else (y-c+eps)/(2*eps))
        base = w*U(a) + (1-w)*U(b)
        un = mpf(0) if y <= 0 else (mpf(1) if y >= top else y/top)
        return (1-e0)*base + e0*un
    return F
for e0, top in [(mpf('0.0001'), mpf(10)), (mpf('0.001'), mpf(2))]:
    out = []
    for (a, b) in [(mpf('0.55'), mpf('1.38')), (mpf('0.95'), mpf('1.38')), (mpf('0.95'), mpf('1.46'))]:
        Ax = auction(Fmix(a, b, e0, top), h, l, p, cH, pts=(a-eps, a+eps, b-eps, b+eps, top))
        eqs = equilibria(Ax['Delta'], Ax['tau'], pi, rho, k, lam, beta)
        out.append((round(float(Ax['J']),5), round(float(Ax['tau']),4), coexist_criterion(Ax['Delta'], Ax['tau'], pi, rho, k, u), sorted(set(x[0] for x in eqs))))
    print("uniform on [0,%s] with weight %s:" % (top, e0), out)
