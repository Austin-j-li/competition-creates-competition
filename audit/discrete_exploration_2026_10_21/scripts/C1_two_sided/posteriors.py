"""C1 posteriors, auction objects, windows, endpoint profits. Print only.

High precision with mpmath (50 digits). Direct convolution over a truncated
flow range checks the closed-form three-class reduction. The omitted tail
mass is printed as an explicit bound.
Run: .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C1_two_sided/posteriors.py
"""
from mpmath import mp, mpf, exp, sqrt

mp.dps = 50

h, ell, p, rho, k, b = mpf(10), mpf(1), mpf("0.5"), mpf("0.25"), mpf("0.02"), mpf(2)
a = exp(-1 / b)
d = 1 - a
c0 = (1 - a) / (1 + a)
print("a = exp(-1/b) =", a)
print("d = 1-a =", d, " c0 = P(Z=0) =", c0)
m1 = a / (1 + a)
M1 = 1 / (1 + a)
m = a * a / (1 + a * a)
M = 1 / (1 + a * a)
print("buy-only bounds m1, M1 =", m1, M1)
print("two-sided bounds m, M =", m, M, " (paper Laplace M = 1/(1+exp(-2/b)))")

alpha = a / (1 + a)          # P(Z>=1)
beta = 1 / (1 + a)           # P(Z>=0)
gamma = (1 - a) / (1 + a)    # P(Z=0)
delta = a * a / (1 + a)      # P(Z>=2)
phi = a * (1 - a) / (1 + a)  # P(Z=1)
print("alpha P(Z>=1) =", alpha)
print("beta  P(Z>=0) =", beta)
print("gamma P(Z=0)  =", gamma)
print("delta P(Z>=2) =", delta)
print("phi   P(Z=1)  =", phi)
print("checks (should be 0): beta-alpha-gamma =", beta - alpha - gamma,
      " alpha-delta-phi =", alpha - delta - phi,
      " beta+phi+delta-1 =", beta + phi + delta - 1)


def f(z):
    return c0 * a ** abs(z)


def mu_closed(u, v):
    Ap = 1 + u * d / a
    Bp = 1 - v * d
    Am = 1 - u * d
    Bm = 1 + v * d / a
    return Ap / (Ap + Bp), Am / (Am + Bp), Am / (Am + Bm)


print("\nDirect convolution check, flows x in [-6,6], tail outside printed below.")
for (u, v) in [(mpf(1), mpf(1)), (mpf(1), mpf(0)), (mpf(0), mpf(1)),
               (mpf("0.7"), mpf("0.3")), (mpf("0.2"), mpf("0.9")), (mpf(0), mpf(0))]:
    mup, mu0, mum = mu_closed(u, v)
    print(f"\n(u,v)=({u},{v}) closed form mu+, mu0, mu- = {mup} {mu0} {mum}")
    worst = mpf(0)
    for x in range(-6, 7):
        ah = (1 - u) * f(x) + u * f(x - 1)
        al = (1 - v) * f(x) + v * f(x + 1)
        mu = ah / (ah + al)
        target = mup if x >= 1 else (mu0 if x == 0 else mum)
        err = abs(mu - target)
        if err > worst:
            worst = err
        print(f"  x={x:+d} mu_direct={mu} target={target} diff={err}")
    print("  worst diff on [-6,6] =", worst)

K = 60
tail = 2 * a ** (K + 1) / (1 + a)
print(f"\nTail bound: P(|Z|>{K}) = 2*a^{K+1}/(1+a) =", tail)
s = sum(f(z) for z in range(-K, K + 1))
print(f"Sum of f over [-{K},{K}] =", s, " 1-sum =", 1 - s)


def objs(r):
    t0 = p * (1 - p / r)
    gH = h - r / 2 - p * p / (2 * r)
    gL = (ell * ell - p * p) / (2 * r)
    DT = (r - ell) ** 2 / (2 * r)
    tH = r / 2 + p * p / (2 * r)
    tL = ell - (ell * ell - p * p) / (2 * r)
    return t0, tH, tL, gH, gL, DT


print("\nAuction objects and B values.")
for r in [mpf("1.2"), mpf("1.55"), mpf("1.6"), mpf("1.65"), mpf(3), mpf("3.6")]:
    t0, tH, tL, gH, gL, DT = objs(r)
    B = lambda mu: gL + mu * (gH - gL)
    print(f"r={r}: DT={DT} gL={gL} gH={gH} B(1/2)={B(mpf(1)/2)} "
          f"B(m1)={B(m1)} B(M1)={B(M1)} B(m)={B(m)} B(M)={B(M)}")
    for cH in [mpf(5), mpf(6)]:
        tau = (cH - gL) / (gH - gL)
        print(f"   cH={cH}: tau={tau}")

r0, r1 = mpf("1.2"), mpf(3)
_, _, _, gH0, gL0, DT0 = objs(r0)
_, _, _, gH1, gL1, DT1 = objs(r1)
Blo = gL0 + mpf(1) / 2 * (gH0 - gL0)
Bhi_buy = gL1 + M1 * (gH1 - gL1)
Bhi_two = gL1 + M * (gH1 - gL1)
print("\nAdmissible cH windows at (r0,r1)=(1.2,3), lower bound open, upper closed (tie prepares):")
print(" lower B_r0(1/2) =", Blo)
print(" buy-only upper B_r1(M1) =", Bhi_buy)
print(" two-sided upper B_r1(M) =", Bhi_two)
print("Trading bounds:")
print(" DT(r0) =", DT0, " k =", k, " DT(r0)<k ?", DT0 < k)
print(" rho*m*DT(r1) =", rho * m * DT1, " rho*m1*DT(r1) =", rho * m1 * DT1)
print(" (1-1/b)*rho*m*DT(r1) [paper sufficient bound] =", (1 - 1 / b) * rho * m * DT1)
print(" rho*DT(r1)/2 [no-trade deviation gross at r1] =", rho * DT1 / 2)

J = a * a / ((1 + a) * (1 + a * a))
print("\nJ = beta*m = delta*M =", J, " beta*m =", beta * m, " delta*M =", delta * M)
c_full_rho = rho * (beta * m + phi / 2 + delta * M)
c_full_rec = J * (1 + rho) + phi * rho / 2
print("g(1,1) coefficient at constant entry rho (times DT):", c_full_rho,
      " = rho *", beta * m + phi / 2 + delta * M)
print("g(1,1) coefficient with recruitment at + only:", c_full_rec)
print("g(0,0) coefficient with entry rho:", rho / 2)


def r_of_DT(dd):
    return ell + dd + sqrt(dd * dd + 2 * ell * dd)


print("Full-trade existence threshold r (with recruitment): DT=k/c_full ->",
      r_of_DT(k / c_full_rec))
print("No-trade existence boundary r_N: DT=k/(rho/2) ->", r_of_DT(k / (rho / 2)))
print("Sufficient full-uniqueness threshold: DT=k/(rho*m) ->", r_of_DT(k / (rho * m)))
print("Sufficient NT-uniqueness threshold: DT=k ->", r_of_DT(k))
print("Buy-only full gross at r1 with recruitment (check vs coordinator 0.195836...):")
g_buy = DT1 * (beta * 1 * m1 + alpha * rho * M1)
print(" DT*[beta*m1 + alpha*rho*M1] =", g_buy, " net =", g_buy - k)
g_buy_no = DT1 * 2 * rho * alpha * beta
print(" buy-only gross without recruitment 2*rho*alpha*beta*DT =", g_buy_no, " net =", g_buy_no - k)
print("Two-sided full gross at r1 with recruitment:", c_full_rec * DT1, " net =", c_full_rec * DT1 - k)
print("Two-sided full gross at r1 without recruitment:", c_full_rho * DT1, " net =", c_full_rho * DT1 - k)

Pp_full = (beta + delta) / 2
E_full = rho + (1 - rho) * Pp_full
OH_full = (rho + (1 - rho) * beta) / 2
print("\nFull two-sided entry at r1: P(+)=", Pp_full, " E=", E_full, " O_H=", OH_full)
print("Buy-only full entry: P(good)=1/2, E=", rho + (1 - rho) / 2, " O_H=", OH_full)
print("Prices at r1, full two-sided, cH in window (e+,e0,e-)=(1,rho,rho):")
t0, tH, tL, gH, gL, DT = objs(r1)
for lab, mu, e in [("+", M, mpf(1)), ("0", mpf(1) / 2, rho), ("-", m, rho)]:
    print(f"  P{lab} = t0+e*(tL-t0+DT*mu) =", t0 + e * (tL - t0 + DT * mu),
          f" (mu={mu}, e={e})")
print(" t0,tL,tH =", t0, tL, tH)

print("\nCeilings r_C solving B_r(bound)=cH by bisection on (1.01, 9.99):")
for cH in [mpf(5), mpf(6)]:
    for lab, bd in [("M1", M1), ("M", M)]:
        lo, hi = mpf("1.01"), mpf("9.99")
        flo = objs(lo)[4] + bd * (objs(lo)[3] - objs(lo)[4]) - cH
        fhi = objs(hi)[4] + bd * (objs(hi)[3] - objs(hi)[4]) - cH
        if (flo > 0) == (fhi > 0):
            print(f" cH={cH} bound {lab}: no sign change on (1.01,9.99); "
                  f"B-cH at ends = {flo}, {fhi} (B falls in r, so no ceiling root here)")
            rnear = mpf("1.000001")
            print(f"   B at r=1+1e-6 = {objs(rnear)[4] + bd * (objs(rnear)[3] - objs(rnear)[4])}")
            continue
        for _ in range(200):
            mid = (lo + hi) / 2
            fm = objs(mid)[4] + bd * (objs(mid)[3] - objs(mid)[4]) - cH
            if (fm > 0) == (flo > 0):
                lo, flo = mid, fm
            else:
                hi = mid
        print(f" cH={cH} bound {lab}: r_C in [{lo}, {hi}] width {hi-lo}")
