# Benchmark auction family (uniform, point masses, c_H=6) with a larger trading cost and a more informative slot
from mpmath import mp, mpf, findroot
mp.dps = 25
h, l, p, cH, rho, pi = mpf(10), mpf(1), mpf(1)/2, mpf(6), mpf(1)/4, mpf(1)/2
def Delta(r): return (r-l)**2/(2*r)
def gH(r): return h - r/2 - p**2/(2*r)
def gL(r): return (l**2-p**2)/(2*r)
def tau(r): return (cH-gL(r))/(gH(r)-gL(r))
def J(r): return Delta(r)*(1-tau(r))
for (M, k) in [(mpf('0.85'), mpf('0.25')), (mpf('0.731059'), mpf('0.25'))]:
    rs = [mpf(1) + mpf(i)/1000 for i in range(1, 7000)]
    C = [float(r) for r in rs if J(r) >= k and pi < tau(r) <= M and rho*Delta(r)*max(pi,1-pi) <= k]
    rN = findroot(lambda r: rho*Delta(r)/2 - k, mpf(5.8)); rC = findroot(lambda r: tau(r)-M, mpf(5.5))
    print(f"M={float(M)} k={float(k)}: C from {C[0]:.3f} to {C[-1]:.3f}; r_N={float(rN):.3f}, r_C={float(rC):.3f}; J at end={float(J(mpf(C[-1]))):.4f}")
print("---")
rstar = mpf('5.7'); k = J(rstar); M = mpf('0.87')
rs = [mpf(1) + mpf(i)/1000 for i in range(1, 7000)]
C = [float(r) for r in rs if J(r) >= k and pi < tau(r) <= M and rho*Delta(r)*max(pi,1-pi) <= k]
rN = findroot(lambda r: rho*Delta(r)/2 - k, mpf(6)); rC = findroot(lambda r: tau(r)-M, mpf(6))
print(f"k=J(5.7)={float(k):.4f} (={float(k/mpf(1)*50):.1f}x benchmark), M={float(M)}: C from {C[0]:.3f} to {C[-1]:.3f}; r_N={float(rN):.3f}, r_C={float(rC):.3f}; tau(5.7)={float(tau(rstar)):.4f}")
