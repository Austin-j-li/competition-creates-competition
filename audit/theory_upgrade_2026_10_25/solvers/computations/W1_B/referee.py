import sys; sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W1_B')
from engine import *
h, l, p, cH = mpf(10), mpf(1), mpf(1)/2, mpf(2)
def Fz(z):
    a, c = z - mpf('0.1'), z + mpf('0.1')
    return lambda y: mpf(0) if y <= a else (mpf(1) if y >= c else (y-a)/(c-a))
for z in [mpf(7), mpf('7.5')]:
    A = auction(Fz(z), h, l, p, cH, pts=(z-mpf('0.1'), z+mpf('0.1')))
    print("z=", z, {kk: float(v) for kk, v in A.items()})
# J along the family: closed form J = (z-1)(8-z)/(10-z); peak where gamma^2 = Gamma*cH
import math
zpk = 10 - math.sqrt(9*2)
print("J peak at z =", zpk, " J =", (zpk-1)*(8-zpk)/(10-zpk))
# coexistence set with rho=1/4, pi=1/2, k=3/2, u=3 (M=4/5), beta=0.3
rho, pi, k, u, beta = mpf(1)/4, mpf(1)/2, mpf(3)/2, mpf(3), mpf('0.3')
lam = u*beta/(1+u*beta)
print("M =", float(M_of(pi,u)), " lam =", float(lam))
zs = [mpf('5.5') + mpf(i)/200 for i in range(0, 501)]
C = []
for z in zs:
    D = z - 1; tau = 2/(10 - z)
    crit = coexist_criterion(D, tau, pi, rho, k, u)
    eqs = equilibria(D, tau, pi, rho, k, lam, beta) if pi < tau < 1 else []
    labs = sorted(set(e[0] for e in eqs))
    direct = ('N' in labs) and any(x in labs for x in ('R','F','T'))
    if crit != direct: print("MISMATCH at z", z, crit, labs)
    if crit: C.append(float(z))
print("coexistence set (grid 1/200): from", C[0], "to", C[-1], " count", len(C), " contiguous:",
      all(abs(C[i+1]-C[i]-0.005) < 1e-9 for i in range(len(C)-1)))
# endpoints predicted: tau = 1/2 at z = 6; J = k at z solving z^2 - 10.5 z + 23 = 0 (upper root); tau = M at z = 7.5; rhoDelta/2 = k at z = 13
print("J=k upper root:", (10.5 + math.sqrt(10.5**2 - 92))/2, " s_F (Delta(1-M)=k):", 1 + 1.5/0.2)
# equilibria at a few points
for z in [mpf('6.2'), mpf('7.3'), mpf('7.45')]:
    D = z - 1; tau = 2/(10 - z)
    print("z=", float(z), "tau=", float(tau), "J=", float(D*(1-tau)), equilibria(D, tau, pi, rho, k, lam, beta))
