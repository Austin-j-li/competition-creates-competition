"""Bounds that decide the importance of W2: the point-mass bound on 1 - W_H along any research branch, the
condition OUT (tau < 1 => W_H = 1) at the benchmark, the research-cost sweep in the counterexample, and a random
scan of the uniform point-mass family beyond h. Prints only."""
import random
from mpmath import mp, mpf, sqrt, e as E, findroot

mp.dps = 30


def m_of(lam, beta):
    return (1 - lam) * beta / (2 * beta + lam * (1 - 2 * beta))


def lam_R(Delta, a, beta, k):
    A = 2 * a * (1 - 2 * beta)
    B = 4 * a * beta + k * (1 - 2 * beta) + beta * Delta
    C = beta * (2 * k - Delta)
    return (-B + sqrt(B * B - 4 * A * C)) / (2 * A)


def Lprime(Delta, lam, a, beta):
    den = 2 * beta + lam * (1 - 2 * beta)
    return m_of(lam, beta) / (2 * a + Delta * beta / den ** 2)


def unif_point(h, ell, p, r):
    def pay(v):
        if v <= r:
            return v - (v * v - p * p) / (2 * r), (v * v - p * p) / (2 * r), v / r
        t = r / 2 + p * p / (2 * r)
        return t, v - t, mpf(1)
    tH, gH, WH = pay(h)
    tL, gL, WL = pay(ell)
    return tH - tL, gH, gL, WH, WL


def branch_point(r, P):
    h, ell, p, cH, rho, k, beta, a, cap = P
    Delta, gH, gL, WH, WL = unif_point(h, ell, p, r)
    gam = gH - gL
    if gam <= 0 or Delta <= 2 * k:
        return None
    tau = (cH - gL) / gam
    if not (mpf(1) / 2 < tau < 1):
        return None
    if rho * Delta >= 2 * k:
        return None
    lE = beta * (2 * tau - 1) / (beta + (1 - 2 * beta) * (1 - tau))
    lR = lam_R(Delta, a, beta, k)
    phi = Delta * (1 - tau) - k - 2 * a * lE
    if phi < 0 or lR >= cap:
        return None
    eH = rho + (1 - rho) * (beta + (1 - beta) * lR)
    eps_e = Delta * (1 - rho) * (1 - beta) * Lprime(Delta, lR, a, beta) / eH
    return dict(Delta=Delta, gam=gam, tau=tau, lR=lR, eH=eH, WH=WH, eps_e=eps_e)


print("=== (1) point-mass bound: 1 - W_H <= Delta/(h - ell) for every incumbent law; on a branch rho*Delta < 2k ===")
for name, (h, ell, rho, k) in (("benchmark", (10, 1, mpf(1) / 4, mpf(1) / 50)), ("counterexample", (10, 1, mpf(1) / 20, mpf(1) / 5))):
    print(f"  {name}: 2k/(rho(h-ell)) = {mp.nstr(2 * k / (rho * (h - ell)), 6)}")
print("  counterexample check r=11: 1-W_H =", mp.nstr(1 - mpf(10) / 11, 6), " Delta/(h-ell) =", mp.nstr((9 - mpf(49.5) / 11) / 9, 6))

print("\n=== (2) condition OUT at the benchmark: tau(F) < 1 (g_H > c_H) only where W_H(F) = 1 ===")
h, ell, p, cH = mpf(10), mpf(1), mpf(1) / 2, mpf(6)
gH_at_h = (h * h - p * p) / (2 * h)
print(f"  uniform point masses: W_H(r) < 1 iff r > h; g_H(r) for r >= h is (h^2-p^2)/(2r) <= {mp.nstr(gH_at_h, 6)}")
print(f"  OUT holds iff c_H >= (h^2-p^2)/(2h): margin c_H - g_H(h) = {mp.nstr(cH - gH_at_h, 6)}")
# strength at which tau = 1 along the benchmark uniform path (r < h): 4r^2 - 32r + 1 = 0
rt = (32 + sqrt(1024 - 16)) / 8
print(f"  tau(r) = 1 at r = {mp.nstr(rt, 7)} (root of 4r^2-32r+1=0); margin to h: {mp.nstr(h - rt, 6)}")
print(f"  check: g_H(rt) = h - rt/2 - p^2/(2 rt) = {mp.nstr(h - rt / 2 - p * p / (2 * rt), 8)} vs c_H = 6")
# the strong incumbent of Prop 2 and A.4/A.7 recruit only where B(M) > c_H, hence g_H > c_H
print("  every recruiting economy (B(mu) > c_H for some posterior mu < 1) has g_H > c_H, hence tau < 1")

print("\n=== (3) research-cost sweep in the counterexample family at r = 11.5 (rho=.05, k=.2, beta=.2, cap=.9, c_H=2.5) ===")
for a in (mpf(5), mpf(2), mpf(1), mpf("0.5"), mpf("0.25"), mpf("0.1"), mpf("0.05"), mpf("0.02"), mpf("0.01")):
    P = (mpf(10), mpf(1), mpf(1) / 2, mpf(5) / 2, mpf(1) / 20, mpf(1) / 5, mpf(1) / 5, a, mpf(9) / 10)
    s = branch_point(mpf("11.5"), P)
    if s is None:
        Delta = 9 - mpf(49.5) / mpf("11.5")
        print(f"  a={mp.nstr(a, 3)}: branch fails (lamR={mp.nstr(lam_R(Delta, a, mpf(1) / 5, mpf(1) / 5), 5)})")
        continue
    print(f"  a={mp.nstr(a, 3)}: lamR={mp.nstr(s['lR'], 6)} eps_e={mp.nstr(s['eps_e'], 6)} Delta/gamma={mp.nstr(s['Delta'] / s['gam'], 6)} "
          f"dlog O_H/dlog r = eps_e*gamma/Delta - 1 = {mp.nstr(s['eps_e'] * s['gam'] / s['Delta'] - 1, 6)}")

print("\n=== (4) analytic ceiling: eps_e < psi(lam) = (1-b)(1-lam)(2b+(1-2b)lam)/(b+(1-b)lam) ===")
for b in (mpf("0.1"), mpf("0.2"), mpf("0.294655"), mpf(1) / 3):
    vals = [((1 - b) * (1 - l) * (2 * b + (1 - 2 * b) * l) / (b + (1 - b) * l)) for l in (mpf(0), mpf("0.05"), mpf("0.1"), mpf("0.2"), mpf("0.4"))]
    print(f"  beta={mp.nstr(b, 4)}: psi(0, .05, .1, .2, .4) =", [mp.nstr(v, 4) for v in vals])
print("  uniform point masses beyond h: Delta/gamma >= (h-ell)/(h+ell) =", mp.nstr(mpf(9) / 11, 6), "at h=10, ell=1")

print("\n=== (5) random scan: uniform point masses h=10, ell=1, p=1/2, branch points with r in (h, 3h) ===")
random.seed(20261025)
n_pts = n_fall = 0
best = None
for trial in range(4000):
    rho = mpf(10) ** random.uniform(-2.5, -0.3)
    beta = mpf(random.uniform(0.02, 1 / 3))
    k = mpf(10) ** random.uniform(-2, 0.3)
    a = mpf(10) ** random.uniform(-3, 1.5)
    cap = mpf(random.uniform(0.3, 0.99))
    cH = mpf(random.uniform(0.3, 5))
    P = (mpf(10), mpf(1), mpf(1) / 2, cH, rho, k, beta, a, cap)
    for j in range(8):
        r = mpf(10) * (1 + mpf(random.uniform(0.001, 2)))
        s = branch_point(r, P)
        if s is None:
            continue
        n_pts += 1
        slope = s['eps_e'] * s['gam'] / s['Delta'] - 1
        if slope < 0:
            n_fall += 1
        if best is None or slope > best[0]:
            best = (slope, dict(rho=rho, beta=beta, k=k, a=a, cap=cap, cH=cH, r=r, eps=s['eps_e'], Dg=s['Delta'] / s['gam'], lR=s['lR']))
print(f"  branch points found: {n_pts}; ownership falling (dlog O_H/dlog r < 0) at {n_fall}")
if best:
    print("  largest slope found:", mp.nstr(best[0], 5), {k: mp.nstr(v, 4) for k, v in best[1].items()})

print("\n=== (6) uniform point masses, r <= h on the branch: W_H = 1, so O_H = e_H/2 rises; how often is the branch beyond h at all? ===")
random.seed(7)
cnt_branch = cnt_beyond = 0
for trial in range(3000):
    rho = mpf(10) ** random.uniform(-2.5, -0.3)
    beta = mpf(random.uniform(0.02, 1 / 3))
    k = mpf(10) ** random.uniform(-2, 0.3)
    a = mpf(10) ** random.uniform(-3, 1.5)
    cap = mpf(random.uniform(0.3, 0.99))
    cH = mpf(random.uniform(0.3, 9))
    P = (mpf(10), mpf(1), mpf(1) / 2, cH, rho, k, beta, a, cap)
    for j in range(10):
        r = mpf(random.uniform(1.0, 30))
        s = branch_point(r, P)
        if s is None:
            continue
        cnt_branch += 1
        if r > 10:
            cnt_beyond += 1
print(f"  branch points (r uniform on [1,30], c_H uniform on [0.3, 9]): {cnt_branch}; with r > h: {cnt_beyond}")
