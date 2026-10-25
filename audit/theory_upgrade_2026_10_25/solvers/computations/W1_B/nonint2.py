import sys; sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W1_B')
from engine import *
from mpmath import e as E
h, l, p, cH = mpf(10), mpf(1), mpf(1)/2, mpf(6)
rho, pi, k = mpf(1)/4, mpf(1)/2, mpf('0.186')
u = E - 1; beta = mpf('0.294655'); lam = u*beta/(1+u*beta); M = M_of(pi, u)
w, eps = mpf(17)/20, mpf(1)/50
def Fmix(a, b):
    def F(y):
        def U(c): return mpf(0) if y <= c-eps else (mpf(1) if y >= c+eps else (y-c+eps)/(2*eps))
        return w*U(a) + (1-w)*U(b)
    return F
# path: s in [0,3]: phase 1 (s in [0,1]) b: 2 -> 5 at a=0.55; phase 2 (s in [1,2]) a: 0.55 -> 0.95 at b=5;
# phase 3 (s in [2,3]) b: 5 -> 7 at a=0.95
def ab(s):
    if s <= 1: return mpf('0.55'), 2 + 3*s
    if s <= 2: return mpf('0.55') + mpf('0.4')*(s-1), mpf(5)
    return mpf('0.95'), 5 + 2*(s-2)
rows = []
for i in range(0, 301):
    s = mpf(i)/100
    a, b = ab(s)
    A = auction(Fmix(a, b), h, l, p, cH, pts=(a-eps, a+eps, b-eps, b+eps))
    D, tau = A['Delta'], A['tau']
    crit = coexist_criterion(D, tau, pi, rho, k, u)
    eqs = equilibria(D, tau, pi, rho, k, lam, beta) if pi < tau < 1 else []
    labs = sorted(set(x[0] for x in eqs))
    direct = ('N' in labs) and any(x in labs for x in ('R','F','T'))
    rows.append((float(s), float(a), float(b), float(D), float(tau), float(A['J']), crit, direct, labs))
mism = [r for r in rows if r[6] != r[7]]
print("criterion vs enumeration mismatches:", len(mism))
# print the runs of the coexistence set
runs, cur = [], None
for r in rows:
    if r[6] and cur is None: cur = [r[0], r[0]]
    elif r[6]: cur[1] = r[0]
    elif cur is not None: runs.append(cur); cur = None
if cur: runs.append(cur)
print("coexistence runs in s:", runs)
for r in rows[::25]:
    print(f"s={r[0]:.2f} a={r[1]:.3f} b={r[2]:.3f} Delta={r[3]:.4f} tau={r[4]:.4f} J={r[5]:.4f} coexist={r[6]} eqs={r[8]}")
# FOSD check: F_s(y) nonincreasing in s on a grid of y
ys = [mpf(i)/100 for i in range(0, 1001)]
ok = True
prev = None
for i in range(0, 301, 5):
    a, b = ab(mpf(i)/100); F = Fmix(a, b); cur = [F(y) for y in ys]
    if prev is not None and any(c > q + mpf(10)**-20 for c, q in zip(cur, prev)): ok = False
    prev = cur
print("path is FOSD-ordered on grid:", ok)
