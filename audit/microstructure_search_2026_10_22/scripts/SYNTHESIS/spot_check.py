"""Synthesis spot-checks (print-only, exact fractions).

Check A: the T6 trade-off at the paper's benchmark.
  A1. tau(3), tau(18/5), and the margin that forces full purchases at 18/5.
  A2. The cap on lambda that Prop. 2(iii) implies (beta = 1/2).
  A3. The posterior that a rising branch of T1's kind needs at 31/20 and 33/20.
  A4. A direct grid: with M <= tau(18/5) and theta <= 1/3, the purchase payoff
      with recruitment at flows {1, 2} never falls to kappa(31/20).
  A5. A direct grid: with recruitment at flow {2} only, the purchase payoff
      never reaches kappa(31/20).
  A6. A direct grid: the low-class sale payoff at r = 3 stays above kappa(3)
      (so the paper's partial sale cannot appear on the strip).

Check B: T4 (one-sided geometric noise, D1) against T2 (V3 buy slot).
  With a = b/(b + lambda), b = (1 - lambda) beta, s = v, the purchase returns
  coincide; the top posteriors coincide; entry above the floor differs by 1/(b + lambda).

Part C: the slot model (T2 V3) across the band (tau(3), tau(18/5)).
  C1. The strength r_F where full purchases start, at the ends of the band.
  C2. The slot parameters with u = e - 1, which give the paper's top posterior.
  C3. With u = e - 1, the liquidity rate beta that gives the paper's entry at r = 3.
"""

from fractions import Fraction as F

H, ELL, P, RHO, CH, K = F(10), F(1), F(1, 2), F(1, 4), F(6), F(1, 50)


def delta_t(r):
    return (r - ELL) ** 2 / (2 * r)


def g_l(r):
    return (ELL ** 2 - P ** 2) / (2 * r)


def g_h(r):
    return H - r / 2 - P ** 2 / (2 * r)


def tau(r):
    return (CH - g_l(r)) / (g_h(r) - g_l(r))


def kappa(r):
    return K / delta_t(r)


def show(label, x):
    print(f"{label}: {x} = {float(x):.6f}")


print("=== Check A: T6 trade-off ===")
r1, r2, r155, r165 = F(3), F(18, 5), F(31, 20), F(33, 20)
t3, t36 = tau(r1), tau(r2)
show("tau(3)", t3)
show("tau(18/5)", t36)
show("band width tau(18/5) - tau(3)", t36 - t3)
force = RHO * delta_t(r2) * (1 - t36) - K
show("A1 rho*Delta(18/5)*(1 - tau(18/5)) - k  (>0 forces full purchase)", force)

# M = (1+u)/(2+u) <= tau  <=>  u <= (2 tau - 1)/(1 - tau)
u_max = (2 * t36 - 1) / (1 - t36)
show("A2 u_max = (2 tau - 1)/(1 - tau) at 18/5", u_max)
beta = F(1, 2)
lam_cap = u_max * beta / (1 + u_max * beta)
show("A2 lambda cap at beta = 1/2", lam_cap)
u_min = (2 * t3 - 1) / (1 - t3)
show("A2 u_min (recruit at 3)", u_min)

for r, lab in ((r155, "31/20"), (r165, "33/20")):
    for th in (F(1, 3), F(1, 10)):
        need = 1 - (kappa(r) - RHO * th / 2) / (1 - th)
        show(f"A3 needed M at r = {lab}, theta = {th}", need)
show("A3 kappa(31/20)", kappa(r155))
bound = (1 - F(1, 3)) * (1 - t36) + F(1, 3) * RHO / 2
show("A3 smallest kappa a {1,2} branch needs when M <= tau(18/5)", bound)
# r at which kappa(r) equals that bound: Delta(r) = k / bound
dd = K / bound
lo, hi = F(1), F(2)
for _ in range(80):
    mid = (lo + hi) / 2
    if delta_t(mid) < dd:
        lo = mid
    else:
        hi = mid
print(f"A3 kappa(r) > bound only for r < {float(lo):.6f}")


def flows(lam, beta, th, A, S):
    """T6 flow laws at x = -2..2, prior 1/2: returns dict x -> (f_H, f_L)."""
    c = (1 - lam) * beta
    ph = 1 - 2 * th
    d = ph - th
    l1 = c * ph + (1 - 2 * c) * th
    l0 = 2 * c * th + (1 - 2 * c) * ph
    return {
        2: ((c + A) * th, c * th),
        1: (l1 + A * d, l1 - S * th),
        0: (l0 - A * d, l0 - S * d),
        -1: (l1 - A * th, l1 + S * d),
        -2: (c * th, (c + S) * th),
    }


def post(fh, fl):
    return fh / (fh + fl)


betas = [F(j, 20) for j in range(1, 11)]
thetas = [F(j, 30) for j in range(1, 11)]  # 1/30 .. 1/3
us = [u_max * F(j, 12) for j in range(1, 13)]  # up to the cap, inclusive
afrac = [F(j, 10) for j in range(1, 10)]  # A / lambda in (0, 1)

minA4_all = None
minA4_cons = None
maxA5 = None
n_all = n_cons = n5 = 0
t155 = tau(r155)
for b_ in betas:
    for u in us:
        lam = u * b_ / (1 + u * b_)
        for th in thetas:
            ph = 1 - 2 * th
            for af in afrac:
                A = af * lam
                fl = flows(lam, b_, th, A, F(0))
                mu = {x: post(*fl[x]) for x in fl}
                # A4: recruitment at {1, 2}: e = (rho, 1, 1) at x = 0, 1, 2
                g12 = th * RHO * (1 - mu[0]) + ph * (1 - mu[1]) + th * (1 - mu[2])
                n_all += 1
                minA4_all = g12 if minA4_all is None else min(minA4_all, g12)
                if mu[1] >= t155 and mu[2] >= t155:
                    n_cons += 1
                    minA4_cons = g12 if minA4_cons is None else min(minA4_cons, g12)
                # A5: recruitment at {2} only
                if mu[2] >= t155 and mu[1] < t155:
                    g2 = th * RHO * (1 - mu[0]) + ph * RHO * (1 - mu[1]) + th * (1 - mu[2])
                    n5 += 1
                    maxA5 = g2 if maxA5 is None else max(maxA5, g2)

print(f"A4 grid points (theta <= 1/3, M <= tau(18/5), 0 < A < lambda): {n_all}")
show("A4 min purchase payoff / Delta, set {1,2}, all points", minA4_all)
print(f"A4 points where flows 1 and 2 both recruit at 31/20: {n_cons}")
if minA4_cons is not None:
    show("A4 min purchase payoff / Delta on those points", minA4_cons)
show("A4 kappa(31/20) (indifference level)", kappa(r155))
print(f"A5 points where only flow 2 recruits at 31/20: {n5}")
if maxA5 is not None:
    show("A5 max purchase payoff / Delta, set {2}", maxA5)

# A6: low-class sale payoff at r = 3, entry floor rho everywhere (a lower bound)
minA6 = None
n6 = 0
sfrac = [F(j, 10) for j in range(0, 11)]
for b_ in betas:
    for u in us:
        lam = u * b_ / (1 + u * b_)
        for th in thetas:
            ph = 1 - 2 * th
            for af in [F(0)] + afrac + [F(1)]:
                for sf in sfrac:
                    fl = flows(lam, b_, th, af * lam, sf * lam)
                    mu = {x: post(*fl[x]) for x in fl}
                    gl = RHO * (th * mu[0] + ph * mu[-1] + th * mu[-2])
                    n6 += 1
                    minA6 = gl if minA6 is None else min(minA6, gl)
print(f"A6 grid points (all A, S in [0, lambda]): {n6}")
show("A6 min sale payoff / Delta at r = 3 (entry rho everywhere)", minA6)
show("A6 T6 bound rho*(2/3)*(1 - tau(18/5))", RHO * F(2, 3) * (1 - t36))
show("A6 kappa(3)", kappa(r1))

print()
print("=== Check B: T4 D1 against T2 V3 buy ===")


def k_v3(lam, beta, v, e, dlt):
    b = (1 - lam) * beta
    return dlt * e * b / (2 * b + lam * v)


def k_d1(a, s, e, dlt):
    return dlt * e * a / (2 * a + (1 - a) * s)


pts = [
    (F(6, 17), F(1, 3)),
    (F(9, 20), F(1, 2)),
    (F(1, 3), F(2, 5)),
    (F(2, 7), F(3, 10)),
]
vs = [F(0), F(1, 7), F(1, 2), F(5, 6), F(1)]
es = [RHO, F(3, 5), F(1)]
rs = [F(31, 20), F(8, 5), F(3), F(18, 5)]
maxdiff = F(0)
count = 0
for lam, beta in pts:
    b = (1 - lam) * beta
    a = b / (b + lam)
    for v in vs:
        for e in es:
            for r in rs:
                dlt = delta_t(r)
                diff = k_v3(lam, beta, v, e, dlt) - k_d1(a, v, e, dlt)
                maxdiff = max(maxdiff, abs(diff))
                count += 1
print(f"B1 return comparisons: {count}; max |K_V3 - K_D1| = {maxdiff}")
for lam, beta in pts:
    b = (1 - lam) * beta
    a = b / (b + lam)
    m_v3 = (b + lam) / (2 * b + lam)
    m_d1 = 1 / (1 + a)
    e_v3 = RHO + (1 - RHO) * (2 * b + lam) / 2
    e_d1 = RHO + (1 - RHO) * (1 + a) / 2
    ratio = (e_d1 - RHO) / (e_v3 - RHO)
    print(
        f"B2 lambda={lam}, beta={beta}: a={a}, M_V3={m_v3}, M_D1={m_d1}, "
        f"entry V3={e_v3} ({float(e_v3):.6f}), entry D1={e_d1} ({float(e_d1):.6f}), "
        f"excess ratio={ratio}, 1/(b+lambda)={1 / (b + lam)}"
    )
print("B3 r_A solves Delta(r)(1 - tau(r)) = k in both models (no device parameter);")
print("   r_F solves Delta(r)(1 - M) = k, and M coincides, so r_F coincides.")

print()
print("=== Part C: the slot model (T2 V3) across the posterior band ===")


def r_of_delta(dd):
    """Inverse of Delta_T(r) = (r - 1)^2 / (2 r) for r > 1, by exact bisection."""
    lo, hi = F(1), F(10)
    for _ in range(80):
        mid = (lo + hi) / 2
        if delta_t(mid) < dd:
            lo = mid
        else:
            hi = mid
    return lo


for lab, m in (("tau(3)", t3), ("29/40", F(29, 40)), ("tau(18/5)", t36)):
    rf = r_of_delta(K / (1 - m))
    print(f"C1 r_F = r(k/(1 - M)) at M = {lab}: {float(rf):.6f}")
# u = e - 1 gives M = e/(1 + e), the paper's top posterior (numerical diagnostic)
import math

u_e = math.e - 1
m_e = (1 + u_e) / (2 + u_e)
print(f"C2 u = e - 1 = {u_e:.6f}: M = {m_e:.6f} (paper 1/(1 + e^-1) = {1 / (1 + math.exp(-1)):.6f})")
for bb in (1 / 3, 1 / 2):
    print(f"C2 lambda at beta = {bb:.6f}: {u_e * bb / (1 + u_e * bb):.6f}")
print(f"C2 strip at beta = 1/3: ({float(u_min / 3 / (1 + u_min / 3)):.6f}, {float(u_max / 3 / (1 + u_max / 3)):.6f})")

# C3: with u = e - 1 (paper's top posterior), choose beta so that entry at r = 3
# equals the paper's 0.522757 (numerical diagnostic; floats).
# Two-sided slot, full orders at r = 3: only flow +1 recruits, so
#   E = rho + (1 - rho)(b + lambda/2),  O_H = 1/8 + 3(b + lambda)/8,
#   with b = (1 - lambda) beta = beta/(1 + u beta) and lambda = u b.
rho_f = float(RHO)
e_target = 0.522757
q = (e_target - rho_f) / (1 - rho_f)
beta_c = 2 * q / (2 + u_e - 2 * q * u_e)
b_c = beta_c / (1 + u_e * beta_c)
lam_c = u_e * b_c
e_c = rho_f + (1 - rho_f) * (b_c + lam_c / 2)
o_c = 1 / 8 + 3 * (b_c + lam_c) / 8
print(f"C3 u = e - 1, entry target {e_target}: beta = {beta_c:.6f}, lambda = {lam_c:.6f}, b = {b_c:.6f}")
print(f"C3 check: entry at 3 = {e_c:.6f}, high-class ownership = {o_c:.6f}, M = {m_e:.6f}")
print(f"C3 informed share of nonzero slot orders 2M - 1 = {2 * m_e - 1:.6f}")
lo, hi = 1.0, 10.0
d_f = float(K) / (1 - m_e)
for _ in range(200):
    mid = (lo + hi) / 2
    if (mid - 1) ** 2 / (2 * mid) < d_f:
        lo = mid
    else:
        hi = mid
print(f"C3 r_F at M = e/(1 + e): {lo:.6f}")
print(f"C3 margin at r = 3: rho*Delta(3)*(1 - M) - k = {rho_f * 2 / 3 * (1 - m_e) - float(K):.6f}")
