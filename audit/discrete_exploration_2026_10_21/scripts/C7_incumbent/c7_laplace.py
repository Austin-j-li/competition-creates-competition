"""C7 cross-check in the paper's continuous Laplace model (numerical diagnostic, print only).

Paper benchmark at r_1 = 3: h=10, ell=1, p=0.5, rho=0.25, c_H=6, b=2, k=0.02, full orders (1, -1).
c_L = 0 or c_L = 1 gives the same entry here, because every belief gives gross profit above 1.
The same posterior-by-posterior continuation as in c7_model.py is applied at each flow x.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpmath import mp, mpf, exp, quad, findroot, nstr, log
import c7_model as M

mp.dps = 25
par = M.Par(cH=6)
b, rho, r = par.b, par.rho, mpf(3)
A = M.auction(par, r)
f = lambda z: exp(-abs(z) / b) / (2 * b)
m, Mx = 1 / (1 + exp(2 / b)), 1 - 1 / (1 + exp(2 / b))
mu = lambda x: 1 / (1 + exp(-2 * max(min(x, 1), -1) / b))
tau = (par.cH - A['gL']) / (A['gH'] - A['gL'])
xstar = (b / 2) * log(tau / (1 - tau))
print('m =', nstr(m, 10), ' M =', nstr(Mx, 10), ' tau =', nstr(tau, 10), ' x* =', nstr(xstar, 10))
print('condition N: M(h-(ell+r)/2) =', nstr(Mx * (par.h - (par.ell + r) / 2), 10), '<= c_H = 6')
print('deterrence feasible: M(h-r) =', nstr(Mx * (par.h - r), 10), '< c_H = 6')
print('A3 floor (1-1/b) rho m Delta_T =', nstr((1 - 1 / b) * rho * m * A['DT'], 10), ' vs k = 0.02')


def ent_jump(x):
    c = M.continuation(par, r, mu(x), True)
    return rho + (1 - rho) * c['Rhat'] / r if c['case'] == 'C' else c['e_silent']


def dW(x):
    c = M.continuation(par, r, mu(x), True)
    if c['case'] != 'C':
        return mpf(0)
    return (1 - rho) * (1 - c['Rhat'] / r) * (par.cH - M.D(par, r, mu(x), c['Rhat']))


# corner region: posteriors where D(mu;[p,r]) <= c_H
lo, hi = xstar, mpf(1)
for _ in range(90):
    mid = (lo + hi) / 2
    if M.D(par, r, mu(mid), par.p) - par.cH < 0:
        lo = mid
    else:
        hi = mid
xc = (lo + hi) / 2
print('corner (R_hat* = p) for x in [x*, x_c), x_c =', nstr(xc, 10))
pts = [xstar, xc, 1]
EH = rho + (1 - rho) * quad(lambda x: (ent_jump(x) - rho) / (1 - rho) * f(x - 1), pts) \
    + (1 - rho) * (ent_jump(mpf(2)) - rho) / (1 - rho) * quad(lambda x: f(x - 1), [1, mp.inf])
EL = rho + (1 - rho) * quad(lambda x: (ent_jump(x) - rho) / (1 - rho) * f(x + 1), pts) \
    + (1 - rho) * (ent_jump(mpf(2)) - rho) / (1 - rho) * quad(lambda x: f(x + 1), [1, mp.inf])
aH = 1 - exp((xstar - 1) / b) / 2
aL = exp(-(xstar + 1) / b) / 2
print('base entry  E =', nstr(rho + (1 - rho) * (aH + aL) / 2, 10), ' O_H =', nstr((rho + (1 - rho) * aH) / 2, 10))
print('jump entry  E =', nstr((EH + EL) / 2, 10), ' O_H =', nstr(EH / 2, 10))
WH = quad(lambda x: dW(x) * f(x - 1), pts) + dW(mpf(2)) * quad(lambda x: f(x - 1), [1, mp.inf])
WL = quad(lambda x: dW(x) * f(x + 1), pts) + dW(mpf(2)) * quad(lambda x: f(x + 1), [1, mp.inf])
print('surplus gain from the jump option (corner part only) =', nstr((WH + WL) / 2, 10))
for x in [xstar + mpf('0.001'), xc, mpf('0.5'), mpf('0.8'), mpf(1)]:
    c = M.continuation(par, r, mu(x), True)
    print(f'  x={nstr(x,6)} mu={nstr(mu(x),8)} case={c["case"]}{c["sub"]} Rhat={nstr(c["Rhat"],8)} entry={nstr(ent_jump(x),8)}')
