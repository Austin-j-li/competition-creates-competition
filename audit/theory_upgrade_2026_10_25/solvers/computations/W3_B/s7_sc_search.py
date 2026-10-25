"""(1) the ratio J'/(2 lamE' tau') along the benchmark path; (2) fine sweep of a near the
branch's disappearance; (3) search for J increasing but recruitment exit before the cap."""
import sys, math, random
sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W3_B')
from model import *

u = math.e - 1; beta = 0.294655; lbar = u*beta/(1+u*beta)
def bench(a, **kw):
    d = dict(h=10, ell=1, p=0.5, cH=6, k=0.02, rho=0.25, beta=beta, a=a, lbar=lbar); d.update(kw)
    return Par(**d)
def deriv(f, r, h=1e-6):
    return (f(r+h) - f(r-h))/(2*h)
P = bench(0.025)
print("ratio J'/(2 lamE'(tau) tau') on the benchmark path:")
for r in (1.2, 1.39, 1.5, 1.75, 2.0, 2.5, 3.0, 3.6, 4.0, 4.5, 5.0, 5.1):
    Jp = deriv(lambda x: auction(P,x)['J'], r); tp = deriv(lambda x: auction(P,x)['tau'], r)
    print("  r=%.2f J'=%.5f tau'=%.5f lamE'=%.4f ratio=%.4f" % (r, Jp, tp, dlamE_of(auction(P,r)['tau'],P), Jp/(2*dlamE_of(auction(P,r)['tau'],P)*tp)))

def branch_summary(P, rlo, rhi, n=6000):
    rs = [rlo + i*(rhi-rlo)/n for i in range(n+1)]
    out = []
    for r in rs:
        A = auction(P, r)
        if not (0.5 < A['tau'] < 1) or A['Delta'] <= 2*P.k:
            out.append((r, None, None, A)); continue
        Ls = Lam_star(A['Delta'], P)
        lam = min(P.lbar, Ls)
        rec = M_of(lam, P) >= A['tau']     # recruiting research equilibrium exists (C1, weak)
        out.append((r, rec, Ls >= P.lbar, A))
    return out

print("\nfine sweep of a on the benchmark path r in [1.2, 7.9]:")
for a in (0.3, 0.32, 0.34, 0.36, 0.38, 0.40, 0.42, 0.44, 0.46):
    P = bench(a)
    s = branch_summary(P, 1.2, 7.9, 3000)
    segs = []; cur = None
    for (r, rec, capd, A) in s:
        if rec and cur is None: cur = [r, r, capd, capd]
        elif rec: cur[1] = r; cur[3] = capd or cur[3]
        elif cur is not None: segs.append(tuple(cur)); cur = None
    if cur: segs.append(tuple(cur))
    print("  a=%.2f recruiting segments [start, end, capped at start?, reaches cap?]:" % a, ["[%.4f, %.4f, %s, %s]" % sg for sg in segs])

# (3) random search in the point-mass/uniform family for J increasing on the branch but an exit before the cap
random.seed(1)
found = 0
for trial in range(4000):
    h = 10; ell = 1; p = random.uniform(0.0, 0.99)
    cH = random.uniform(1.0, 9.0); k = 10**random.uniform(-2.5, -0.3); rho = random.uniform(0.05, 0.6)
    bt = random.uniform(0.05, 0.33); a = 10**random.uniform(-3, 0.5); lb = random.uniform(0.1, 0.9)
    P = Par(h=h, ell=ell, p=p, cH=cH, k=k, rho=rho, beta=bt, a=a, lbar=lb)
    try:
        s = branch_summary(P, 1.05, 9.95, 800)
    except Exception as e:
        continue
    # find a recruiting interior stretch that ends (rec True -> False) while research not capped and J still rising
    for i in range(1, len(s)):
        r0, rec0, cap0, A0 = s[i-1]; r1, rec1, cap1, A1 = s[i]
        if rec0 and rec1 is False and cap0 is False:
            # J rising at the exit?
            if A1['J'] > A0['J'] and A1['tau'] > A0['tau'] and A1['Delta'] > A0['Delta']:
                found += 1
                if found <= 6:
                    print("EXIT BEFORE CAP with J rising: p=%.3f cH=%.3f k=%.4f rho=%.3f beta=%.3f a=%.4f lbar=%.3f at r~%.3f tau=%.3f J=%.4f" % (p, cH, k, rho, bt, a, lb, r1, A1['tau'], A1['J']))
            break
print("random search: %d parameter draws with an exit before the cap while J rises" % found)
