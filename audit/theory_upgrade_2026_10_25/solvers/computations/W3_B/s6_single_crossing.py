"""Single crossing of the recruitment margin phi*_a along the benchmark path, as a varies."""
import sys, math
sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W3_B')
from model import *

u = math.e - 1; beta = 0.294655; lbar = u*beta/(1+u*beta)
def bench(a):
    return Par(h=10, ell=1, p=0.5, cH=6, k=0.02, rho=0.25, beta=beta, a=a, lbar=lbar)

rgrid = [1.2 + i*(7.9-1.2)/6000 for i in range(6001)]
pre = [(r, auction(bench(0.025), r)) for r in rgrid]
# J monotonicity on the extended range
Js = [A['J'] for r, A in pre]
peak = max(range(len(Js)), key=lambda i: Js[i])
print("benchmark: J rises on [1.2, %.4f], peak J=%.5f, tau there=%.4f; tau(3.6)=%.4f" % (rgrid[peak], Js[peak], pre[peak][1]['tau'], auction(bench(0.025),3.6)['tau']))

def analyse(a):
    P = bench(a)
    vals = [phi_star(A['Delta'], A['tau'], P) for r, A in pre]
    caps = [Lam_star(A['Delta'], P) >= P.lbar if A['Delta'] > 2*P.k else False for r, A in pre]
    # sign changes of phi* before the cap point
    changes = []
    for i in range(len(rgrid)-1):
        if (vals[i] > 0) != (vals[i+1] > 0):
            changes.append((rgrid[i], '+' if vals[i+1] > 0 else '-', caps[i]))
    first_cap = next((rgrid[i] for i in range(len(rgrid)) if caps[i]), None)
    return changes, first_cap

print("\n a        sign changes of phi*_a on [1.2,7.9] (r, new sign, research already capped?)   first r with Lam*>=lbar")
for a in (0.005, 0.01, 0.025, 0.03, 0.0343, 0.04, 0.06, 0.08, 0.1, 0.1617, 0.2, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0, 3.0):
    ch, fc = analyse(a)
    print(" %-7g  %-70s  %s" % (a, ", ".join("(%.4f,%s,%s)" % c for c in ch), ("%.4f" % fc) if fc else "none"))

# exact local monotonicity bound a_mono = inf J'/(2 lamE'(tau) tau') over [r0, r] for several right ends
def deriv(f, r, h=1e-6):
    return (f(r+h) - f(r-h))/(2*h)
P = bench(0.025)
def amono(rlo, rhi, n=4000):
    best = (1e9, None)
    for i in range(n+1):
        r = rlo + i*(rhi-rlo)/n
        Jp = deriv(lambda x: auction(P,x)['J'], r)
        tp = deriv(lambda x: auction(P,x)['tau'], r)
        v = Jp/(2*dlamE_of(auction(P,r)['tau'], P)*tp)
        if v < best[0]:
            best = (v, r)
    return best
for rhi in (1.75, 2.0, 2.5, 3.0, 3.6):
    v, r = amono(1.2, rhi)
    print("a_mono on [1.2, %.2f] = %.6f (attained at r=%.4f)" % (rhi, v, r))
