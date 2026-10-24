"""L2: pure-profile scan, EGJ two-sided menu, three-point noise, presence lam, c_L = 0.

Print-only. Orders in {-1,0,1}; noise {-1,0,1} with probability 1/3; investor present w.p. lam.
Beliefs at flows reached by nobody: Intuitive Criterion (x>0 -> 1, x<0 -> 0).
Challenger prepares at indifference (rule E). Investor trades only if strictly better than 0.
Payoffs are in units of Delta_T: k means k / Delta_T.
Output: for each (r, lam) the k-intervals on which each pure profile is an equilibrium.
"""
import itertools
import numpy as np

h, l, p, rho, cH = 10.0, 1.0, 0.5, 0.25, 6.0
pi = 0.5
def gH(r): return h - r / 2 - p * p / (2 * r)
def gL(r): return (l * l - p * p) / (2 * r)
Z = {-1: 1/3, 0: 1/3, 1: 1/3}

def flow_law(q, lam):
    out = {x: 0.0 for x in range(-2, 3)}
    for z, pz in Z.items():
        out[z] += (1 - lam) * pz
        out[q + z] += lam * pz
    return out

def beliefs_entry(qH, qL, lam, r):
    LH, LL = flow_law(qH, lam), flow_law(qL, lam)
    mu, e = {}, {}
    for x in range(-2, 3):
        a, b = LH[x], LL[x]
        if a + b > 1e-15:
            mu[x] = pi * a / (pi * a + (1 - pi) * b)
        else:
            mu[x] = 1.0 if x > 0 else 0.0
        B = gL(r) + mu[x] * (gH(r) - gL(r))
        e[x] = rho + (1 - rho) * (1.0 if B >= cH - 1e-12 else 0.0)
    return mu, e

def payoff(cls, q, mu, e, k):
    if q == 0:
        return 0.0
    tot = 0.0
    for z, pz in Z.items():
        x = q + z
        resid = e[x] * ((1.0 if cls == 'H' else 0.0) - mu[x])
        tot += pz * q * resid
    return tot - k * abs(q)

def is_eq(qH, qL, lam, r, k):
    mu, e = beliefs_entry(qH, qL, lam, r)
    for cls, q in (('H', qH), ('L', qL)):
        pay = {qq: payoff(cls, qq, mu, e, k) for qq in (-1, 0, 1)}
        best = max(pay.values())
        if q == 0:
            if pay[0] < best - 1e-12: return False
        else:
            if pay[q] < best - 1e-12 or pay[q] <= 1e-12: return False
    return True

names = {(0, 0): 'NT', (1, -1): 'T', (1, 0): 'BNS', (0, -1): 'SNB'}
ks = np.arange(0.001, 0.2001, 0.001)
def intervals(flags):
    out, start = [], None
    for i, f in enumerate(flags):
        if f and start is None: start = ks[i]
        if (not f) and start is not None:
            out.append((round(start, 3), round(ks[i - 1], 3))); start = None
    if start is not None: out.append((round(start, 3), round(ks[-1], 3)))
    return out

for r in (3.0, 3.6):
    print(f"=== r = {r}: B_r(1/2) = {gL(r)+0.5*(gH(r)-gL(r)):.3f} < c_H = {cH}; g_H = {gH(r):.3f}; tau = {(cH-gL(r))/(gH(r)-gL(r)):.4f}")
    for lam in (1.0, 0.9, 0.8, 0.7, 0.6, 0.5):
        print(f" lam = {lam}: mu_x = 1/(2-lam) = {1/(2-lam):.4f}")
        for prof, nm in names.items():
            flags = [is_eq(prof[0], prof[1], lam, r, k) for k in ks]
            print(f"   {nm:4s} holds for k/Delta_T in {intervals(flags)}")
