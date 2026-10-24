"""Order-slot model with a general class prior (point-mass classes, other benchmark inputs fixed). Print only.
Bounds after one order: m(pi) = pi/(pi + (1-pi)(1+u)), M(pi) = pi(1+u)/(pi(1+u) + 1 - pi).
Prop. 2 hypotheses (two-sided menu; corrected 23 Oct as in memos/E1_auction_side.md, eq. (3)):
B_r0(pi) < c_H < B_r1(M); Delta(r0) < k < rho*min(m, 1-M)*Delta(r1); B_r2(M) < c_H."""
from mpmath import mp, mpf, e, findroot, sqrt
mp.dps = 30
rho, k = mpf(1) / 4, mpf(1) / 50
D = lambda r: (r - 1) ** 2 / (2 * r)
tau = lambda r: (48 * r - 3) / (4 * (20 * r - r * r - 1))
def bounds(pi, u):
    M = pi * (1 + u) / (pi * (1 + u) + 1 - pi); m = pi / (pi + (1 - pi) * (1 + u)); return m, M
def ok(pi, u):
    m, M = bounds(pi, u); r0, r1, r2 = mpf('1.2'), mpf(3), mpf('3.6')
    return (pi < tau(r0) and tau(r1) < M and D(r0) < k < rho * min(1 - M, m) * D(r1) and M < tau(r2))
for name, u in [('A: u = 18/11', mpf(18) / 11), ('B: u = e - 1', e - 1)]:
    # scan, then refine the two ends by bisection on each binding condition
    grid = [mpf(i) / 20000 for i in range(1, 20000)]
    good = [p for p in grid if ok(p, u)]
    lo, hi = good[0], good[-1]
    def refine(a, b):
        fa = ok(a, u)
        for _ in range(80):
            c = (a + b) / 2
            if ok(c, u) == fa: a = c
            else: b = c
        return (a + b) / 2
    lo = refine(lo - mpf(1) / 20000, lo); hi = refine(hi, hi + mpf(1) / 20000)
    m, M = bounds(mpf(1) / 2, u)
    print(f"{name}: M(1/2) = {float(M):.6f}; Prop. 2 (i)-(iii) hold for priors in ({float(lo):.6f}, {float(hi):.6f})")
    # which condition binds at each end
    for p in [lo - mpf('1e-7'), hi + mpf('1e-7')]:
        m, M = bounds(p, u)
        print(f"   at pi = {float(p):.7f}: M = {float(M):.6f} (tau(3) = 0.705, tau(3.6) = {float(tau(mpf('3.6'))):.6f}); "
              f"rho*D(3)*min(1-M,m) - k = {float(rho*D(mpf(3))*min(1-M,m)-k):.5f}")
# general-prior entry and ownership at r1 for calibration A, pi = 1/2 check
lam, beta = mpf(6) / 17, mpf(1) / 3; b = (1 - lam) * beta
for pi in [mpf(1) / 2, mpf('0.49'), mpf('0.505')]:
    E1 = rho + (1 - rho) * (pi * lam + b); O = pi * (rho + (1 - rho) * (lam + b))
    rN = 1 + k / (rho * max(pi, 1 - pi)) + sqrt((k / (rho * max(pi, 1 - pi))) ** 2 + 2 * k / (rho * max(pi, 1 - pi)))
    print(f"A, pi = {float(pi)}: entry(r1) = {float(E1):.6f}, O_H(r1) = {float(O):.6f}, r_N = {float(rN):.6f}")
