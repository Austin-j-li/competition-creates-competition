"""Print-only checks of the class-model formulas used in drafts A01-A15.

The script prints values. It makes no assertions.
Run from the repository root:
    .venv/bin/python audit/revision_v2_2026_10_21/scripts/A_reading_n_checks.py
"""

import math

import numpy as np
from scipy import integrate, optimize


# ----------------------------------------------------------------------------
# Value laws: mixtures of atoms and uniform pieces
# ----------------------------------------------------------------------------
class ValueLaw:
    def __init__(self, atoms=(), unifs=()):
        self.atoms = list(atoms)  # (value, weight)
        self.unifs = list(unifs)  # (lo, hi, weight)

    def cdf(self, u):
        s = sum(w for v, w in self.atoms if v <= u)
        for lo, hi, w in self.unifs:
            s += w * min(max((u - lo) / (hi - lo), 0.0), 1.0)
        return s

    def cdf_left(self, u):
        s = sum(w for v, w in self.atoms if v < u)
        for lo, hi, w in self.unifs:
            s += w * min(max((u - lo) / (hi - lo), 0.0), 1.0)
        return s

    def expect(self, fn, extra_breaks=()):
        s = sum(w * fn(v) for v, w in self.atoms)
        for lo, hi, w in self.unifs:
            pts = sorted({lo, hi, *[b for b in extra_breaks if lo < b < hi]})
            for a, b in zip(pts[:-1], pts[1:]):
                val, _ = integrate.quad(fn, a, b, limit=200)
                s += w * val / (hi - lo)
        return s

    def upper(self):
        vals = [v for v, _ in self.atoms] + [hi for _, hi, _ in self.unifs]
        return max(vals)


def unif_cdf(r):
    return lambda u: min(max(u / r, 0.0), 1.0)


# ----------------------------------------------------------------------------
# Per-value objects by direct integration of the payment rule over R ~ U[0,r]
# ----------------------------------------------------------------------------
def t_direct(theta, p, r):
    """Expected target proceeds after preparation, value theta, R ~ U[0,r]."""
    if theta >= p:
        fn = lambda R: max(p, min(R, theta))
    else:
        fn = lambda R: p * (R >= p)
    pts = sorted({0.0, r, *[x for x in (p, theta) if 0.0 < x < r]})
    return sum(integrate.quad(fn, a, b)[0] for a, b in zip(pts[:-1], pts[1:])) / r


def g_direct(theta, p, r):
    if theta < p:
        return 0.0
    fn = lambda R: max(theta - max(p, R), 0.0)
    pts = sorted({0.0, r, *[x for x in (p, theta) if 0.0 < x < r]})
    return sum(integrate.quad(fn, a, b)[0] for a, b in zip(pts[:-1], pts[1:])) / r


def t0_uniform(p, r):
    return p * (1.0 - min(p / r, 1.0))


# Formula (6) objects for a uniform incumbent
def class_objects_formula(GH, GL, p, r, top):
    F = unif_cdf(r)
    D = lambda u: GL.cdf(u) - GH.cdf(u)
    Dp = GL.cdf_left(p) - GH.cdf_left(p)
    brk = sorted({p, r, top, *[a[0] for a in GH.atoms + GL.atoms],
                  *[x for lo, hi, _ in GH.unifs + GL.unifs for x in (lo, hi)]})
    brk = [b for b in brk if p <= b <= top]

    def piecewise(fn):
        return sum(integrate.quad(fn, a, b, limit=200)[0] for a, b in zip(brk[:-1], brk[1:]))

    dT = p * F(p) * Dp + piecewise(lambda u: (1.0 - F(u)) * D(u))
    gH = piecewise(lambda u: (1.0 - GH.cdf(u)) * F(u))
    gL = piecewise(lambda u: (1.0 - GL.cdf(u)) * F(u))
    return dT, gH, gL, Dp


def class_objects_direct(GH, GL, p, r):
    br = (p, r)
    tH = GH.expect(lambda th: t_direct(th, p, r), br)
    tL = GL.expect(lambda th: t_direct(th, p, r), br)
    gH = GH.expect(lambda th: g_direct(th, p, r), br)
    gL = GL.expect(lambda th: g_direct(th, p, r), br)
    return tH, tL, gH, gL


def hat_mean(G, p):
    return G.expect(lambda th: max(th, p), (p,))


# ----------------------------------------------------------------------------
# Posterior bounds and closed forms
# ----------------------------------------------------------------------------
def m_of(pi, b):
    return pi / (pi + (1 - pi) * math.exp(2 / b))


def M_of(pi, b):
    return pi / (pi + (1 - pi) * math.exp(-2 / b))


def kappa(pi, b):
    return min(m_of(pi, b), 1 - M_of(pi, b))


def logit(x):
    return math.log(x / (1 - x))


def laplace_f(z, b):
    return math.exp(-abs(z) / b) / (2 * b)


def laplace_sf(z, b):
    return 0.5 * math.exp(-z / b) if z >= 0 else 1 - 0.5 * math.exp(z / b)


def full_order_posterior(x, pi, b):
    a = pi * laplace_f(x - 1, b)
    c = (1 - pi) * laplace_f(x + 1, b)
    return a / (a + c)


def closed_forms(gH, gL, cH, pi, b, rho, WH):
    tau = (cH - gL) / (gH - gL)
    xs = 0.5 * b * (logit(tau) - logit(pi))
    aH = 1 - 0.5 * math.exp((xs - 1) / b)
    aL = 0.5 * math.exp(-(xs + 1) / b)
    eH = rho + (1 - rho) * aH
    eL = rho + (1 - rho) * aL
    E = pi * eH + (1 - pi) * eL
    OH = pi * eH * WH
    return dict(tau=tau, xs=xs, aH=aH, aL=aL, eH=eH, eL=eL, E=E, OH=OH)


def W_H(GH, p, r):
    F = unif_cdf(r)
    return GH.expect(lambda th: F(th) * (th >= p), (p, r))


def hr(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


# ----------------------------------------------------------------------------
# 1. Split identity and formula (6) against direct integration
# ----------------------------------------------------------------------------
hr("1. Formula (6) against direct integration; split identity")
p = 0.5
cases = {
    "point masses (10, 1)": (ValueLaw(atoms=[(10.0, 1.0)]), ValueLaw(atoms=[(1.0, 1.0)]), 0.5,
                             [0.3, 0.8, 1.2, 3.0, 3.6, 9.0, 25.0]),
    "value classes eps=0.05, p=0.5": (ValueLaw(unifs=[(9.95, 10.05, 1.0)]),
                                      ValueLaw(unifs=[(0.95, 1.05, 1.0)]), 0.5, [1.2, 3.0, 3.6]),
    "value classes eps=0.05, p=1.1 (D(p-)=1)": (ValueLaw(unifs=[(9.95, 10.05, 1.0)]),
                                                ValueLaw(unifs=[(0.95, 1.05, 1.0)]), 1.1, [1.2, 3.0]),
    "case 2b U[0.2,19.8] vs U[0.2,2.8]": (ValueLaw(unifs=[(0.2, 19.8, 1.0)]),
                                          ValueLaw(unifs=[(0.2, 2.8, 1.0)]), 0.5, [1.2, 3.0]),
    "case 2a (equal mass below p)": (ValueLaw(unifs=[(0.0, 0.5, 0.1), (0.5, 19.5, 0.9)]),
                                     ValueLaw(unifs=[(0.0, 0.5, 0.1), (0.5, 2.5, 0.9)]), 0.5, [1.2, 3.0]),
}
for name, (GH, GL, pp, rs) in cases.items():
    print(f"\n{name}")
    top = max(GH.upper(), GL.upper()) + 1.0
    for r in rs:
        dT, gH, gL, Dp = class_objects_formula(GH, GL, pp, r, top)
        tH, tL, gHd, gLd = class_objects_direct(GH, GL, pp, r)
        F = unif_cdf(r)
        lhs = dT + gH - gL
        rhs = hat_mean(GH, pp) - hat_mean(GL, pp) + pp * F(pp) * Dp
        print(f"  r={r:6.3f}  dT formula {dT:.9f} direct {tH - tL:.9f} | gH {gH:.9f}/{gHd:.9f}"
              f" gL {gL:.9f}/{gLd:.9f} | dT+gH-gL {lhs:.9f}  EHhat-ELhat+pF(p)D(p-) {rhs:.9f}"
              f"  reserve term {pp * F(pp) * Dp:.6f}")

# per-value identity t + g = theta
print("\nPer-value identity t(theta)+g(theta)=theta for theta>=p (p=0.5, r=3):")
for th in [0.5, 0.7, 1.0, 2.0, 3.0, 4.5]:
    print(f"  theta={th:4.2f}: t+g={t_direct(th, 0.5, 3.0) + g_direct(th, 0.5, 3.0):.12f}")
print(f"  theta=0.3 (<p): t={t_direct(0.3, 0.5, 3.0):.9f}, t0={t0_uniform(0.5, 3.0):.9f}, g={g_direct(0.3, 0.5, 3.0)}")

# value-class closed form for the spread
print("\nValue classes: dT(r) vs [(r-l)^2+eps^2/3]/(2r):")
GH = ValueLaw(unifs=[(9.95, 10.05, 1.0)])
GL = ValueLaw(unifs=[(0.95, 1.05, 1.0)])
for r in [1.2, 3.0, 3.6]:
    dT, *_ = class_objects_formula(GH, GL, 0.5, r, 11.0)
    print(f"  r={r}: {dT:.9f} vs {((r - 1) ** 2 + 0.05 ** 2 / 3) / (2 * r):.9f}")

# ----------------------------------------------------------------------------
# 2. Posterior bounds with a general prior
# ----------------------------------------------------------------------------
hr("2. m(pi), M(pi), kappa(pi) at b=2")
for pi in [0.3, 0.5, 0.7]:
    print(f"  pi={pi}: m={m_of(pi, 2):.6f}  M={M_of(pi, 2):.6f}  1-M={1 - M_of(pi, 2):.6f}"
          f"  m(1-pi)={m_of(1 - pi, 2):.6f}  kappa={kappa(pi, 2):.6f}  m(min)={m_of(min(pi, 1 - pi), 2):.6f}")
pi = 0.3
xs_grid = np.linspace(-6, 6, 2001)
post = [full_order_posterior(x, pi, 2) for x in xs_grid]
print(f"  full-order posterior range at pi=0.3: min {min(post):.6f} max {max(post):.6f}")

# ----------------------------------------------------------------------------
# 3. Threshold flow with prior shift, and J_H, J_L
# ----------------------------------------------------------------------------
hr("3. x* = (b/2)[logit tau - logit pi] against a direct root; J_H, J_L")
b, rho = 2.0, 0.25
for pi in [0.3, 0.5, 0.7]:
    tau = 0.5 * (pi + M_of(pi, b))
    xs_closed = 0.5 * b * (logit(tau) - logit(pi))
    xs_root = optimize.brentq(lambda x: full_order_posterior(x, pi, b) - tau, -0.999999, 0.999999)
    aH_num = 1 - integrate.quad(lambda z: laplace_f(z, b), -60, xs_closed - 1)[0]
    aL_num = integrate.quad(lambda z: laplace_f(z, b), xs_closed + 1, 60)[0]
    aH = 1 - 0.5 * math.exp((xs_closed - 1) / b)
    aL = 0.5 * math.exp(-(xs_closed + 1) / b)
    e = lambda x: rho + (1 - rho) * (x >= xs_closed)
    pts = [-60, -1, xs_closed, 1, 60]
    JH = sum(integrate.quad(lambda x: laplace_f(x - 1, b) * e(x) * (1 - full_order_posterior(x, pi, b)), a, c)[0]
             for a, c in zip(pts[:-1], pts[1:]))
    JL = sum(integrate.quad(lambda x: laplace_f(x + 1, b) * e(x) * full_order_posterior(x, pi, b), a, c)[0]
             for a, c in zip(pts[:-1], pts[1:]))
    K = sum(integrate.quad(lambda x: e(x) * laplace_f(x - 1, b) * laplace_f(x + 1, b)
                           / (pi * laplace_f(x - 1, b) + (1 - pi) * laplace_f(x + 1, b)), a, c)[0]
            for a, c in zip(pts[:-1], pts[1:]))
    print(f"  pi={pi}: tau={tau:.6f} x* closed {xs_closed:.12f} root {xs_root:.12f} | aH {aH:.9f}/{aH_num:.9f}"
          f" aL {aL:.9f}/{aL_num:.9f}")
    print(f"           J_H={JH:.9f} (1-pi)K={(1 - pi) * K:.9f}  J_L={JL:.9f} pi*K={pi * K:.9f}"
          f"  pi*J_H-(1-pi)*J_L={pi * JH - (1 - pi) * JL:.2e}  eH>(1+rho)/2: {rho + (1 - rho) * aH:.6f} > {(1 + rho) / 2}")

# ----------------------------------------------------------------------------
# 4. Benchmark (point masses) and value classes at the benchmark vector
# ----------------------------------------------------------------------------
hr("4. Proposition 2 margins at the benchmark vector (pi=1/2, c_L=0)")
h, l, p, rho, cH, b, k = 10.0, 1.0, 0.5, 0.25, 6.0, 2.0, 0.02
r0, r1, r2 = 1.2, 3.0, 3.6
pi = 0.5
for name, GH, GL in [("point masses", ValueLaw(atoms=[(h, 1.0)]), ValueLaw(atoms=[(l, 1.0)])),
                     ("value classes eps=0.05", ValueLaw(unifs=[(9.95, 10.05, 1.0)]),
                      ValueLaw(unifs=[(0.95, 1.05, 1.0)]))]:
    out = {}
    for r in (r0, r1, r2):
        dT, gH, gL, _ = class_objects_formula(GH, GL, p, r, 11.0)
        out[r] = (dT, gH, gL)
    B = lambda r, mu: out[r][2] + mu * (out[r][1] - out[r][2])
    m, M, kap = m_of(pi, b), M_of(pi, b), kappa(pi, b)
    print(f"\n{name}")
    print(f"  (A2): B_r0(pi)={B(r0, pi):.6f} < cH={cH} < B_r1(M)={B(r1, M):.6f}   margins {cH - B(r0, pi):.6f}, {B(r1, M) - cH:.6f}")
    print(f"  (A3): dT(r0)={out[r0][0]:.6f} < k={k} < (1-1/b)rho kappa dT(r1)={(1 - 1 / b) * rho * kap * out[r1][0]:.6f}")
    print(f"  (iii): B_r2(M)={B(r2, M):.6f} < cH, margin {cH - B(r2, M):.6f};  dT(r2)={out[r2][0]:.6f} >= dT(r1)={out[r1][0]:.6f}")
    print(f"  floor (c_L=0): B_r(m) at r0,r1,r2 = {B(r0, m):.6f}, {B(r1, m):.6f}, {B(r2, m):.6f} (all >= 0)")
    cf = closed_forms(out[r1][1], out[r1][2], cH, pi, b, rho, W_H(GH, p, r1))
    print(f"  closed forms at r1: tau={cf['tau']:.6f} x*={cf['xs']:.6f} E={cf['E']:.6f} O_H={cf['OH']:.6f}"
          f"  W_H(r0)={W_H(GH, p, r0):.6f} W_H(r1)={W_H(GH, p, r1):.6f}")
    print(f"  split at r1: dT+gH-gL={out[r1][0] + out[r1][1] - out[r1][2]:.9f}")

# Certificate-floor independence: B_r(m) at the certified strengths (point masses)
print("\nPoint-mass B_r(m) at the certified strengths (compare with the old c_L=1):")
for r in [1.55, 1.60, 1.65]:
    gL = (l ** 2 - p ** 2) / (2 * r)
    gH = h - r / 2 - p ** 2 / (2 * r)
    print(f"  r={r}: B_r(m)={gL + m_of(0.5, 2) * (gH - gL):.6f}")

# ----------------------------------------------------------------------------
# 5. General-prior no-trade condition against a direct computation
# ----------------------------------------------------------------------------
hr("5. No-trade residuals at a constant schedule, general prior")
GH, GL = ValueLaw(atoms=[(h, 1.0)]), ValueLaw(atoms=[(l, 1.0)])
for pi in [0.3, 0.7]:
    r = 1.2
    tH, tL, gH, gL = class_objects_direct(GH, GL, p, r)
    t0 = t0_uniform(p, r)
    Bpi = gL + pi * (gH - gL)
    e = rho + (1 - rho) * (Bpi >= cH)
    P = t0 + e * (pi * (tH - t0) + (1 - pi) * (tL - t0))
    resH = (t0 + e * (tH - t0)) - P
    resL = P - (t0 + e * (tL - t0))
    print(f"  pi={pi}: e(pi)={e}  residual H {resH:.9f} vs e dT (1-pi) {e * (tH - tL) * (1 - pi):.9f};"
          f" residual L {resL:.9f} vs e dT pi {e * (tH - tL) * pi:.9f}")

# ----------------------------------------------------------------------------
# 6. Nonemptiness construction (Claim 11) on two ranked pairs
# ----------------------------------------------------------------------------
hr("6. Nonemptiness construction for ranked pairs, uniform incumbents")


def construct(GH, GL, p, pi, b, rho, u0, label):
    top = max(GH.upper(), GL.upper()) + 1.0

    def objs(r):
        dT, gH, gL, _ = class_objects_formula(GH, GL, p, r, top)
        return dT, gH, gL

    def B(r, mu):
        dT, gH, gL = objs(r)
        return gL + mu * (gH - gL)

    M, kap = M_of(pi, b), kappa(pi, b)
    WH0 = W_H(GH, p, u0)
    # step 1: r1 close to u0
    for d1 in [0.5, 0.25, 0.1, 0.05, 0.02, 0.01]:
        r1 = u0 + d1
        if B(r1, M) > B(u0, pi) and W_H(GH, p, r1) / WH0 > 2 * rho / (1 + rho):
            break
    # step 2: r0 close to u0
    target = (1 - 1 / b) * rho * kap * objs(r1)[0]
    for frac in [0.5, 0.25, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001]:
        r0 = u0 + frac * d1
        if objs(r0)[0] < target:
            break
    k = math.sqrt(max(objs(r0)[0], 1e-12) * target)
    cH = 0.5 * (B(r0, pi) + B(r1, M))
    r2 = r1
    while B(r2, M) >= cH:
        r2 += 0.25
    dT0, dT1, dT2 = objs(r0)[0], objs(r1)[0], objs(r2)[0]
    print(f"\n{label}: pi={pi}, b={b}, rho={rho}, u0={u0}")
    print(f"  r0={r0:.4f} r1={r1:.4f} r2={r2:.4f} cH={cH:.6f} k={k:.6g}")
    print(f"  (A2) margins: cH-B_r0(pi)={cH - B(r0, pi):.6g}, B_r1(M)-cH={B(r1, M) - cH:.6g}")
    print(f"  (A3) margins: k-dT(r0)={k - dT0:.6g}, (1-1/b)rho kappa dT(r1)-k={target - k:.6g}")
    print(f"  (iii): cH-B_r2(M)={cH - B(r2, M):.6g}; trading at r2: (1-1/b)rho kappa dT(r2)-k={(1 - 1 / b) * rho * kap * dT2 - k:.6g}")
    WH_r0, WH_r1 = W_H(GH, p, r0), W_H(GH, p, r1)
    dTr1, gH1, gL1 = objs(r1)
    cf = closed_forms(gH1, gL1, cH, pi, b, rho, WH_r1)
    print(f"  r1 closed forms: tau={cf['tau']:.6f} in (pi, M)=({pi}, {M:.6f}); x*={cf['xs']:.6f}; E={cf['E']:.6f}")
    print(f"  ownership: O_H(r0)=pi rho W_H(r0)={pi * rho * WH_r0:.6f}  O_H(r1)={cf['OH']:.6f};"
          f"  (1+rho)W_H(r1)-2rho W_H(r0)={(1 + rho) * WH_r1 - 2 * rho * WH_r0:.6f}")
    print(f"  g_H-g_L at r1 = {gH1 - gL1:.6f} >= Gamma p/r1 = {(hat_mean(GH, p) - hat_mean(GL, p)) * p / r1:.6f}")


construct(ValueLaw(atoms=[(10.0, 1.0)]), ValueLaw(atoms=[(1.0, 1.0)]), 0.5, 0.7, 2.0, 0.25, 1.0,
          "point masses (u0 = l)")
construct(ValueLaw(unifs=[(0.0, 0.5, 0.1), (0.5, 19.5, 0.9)]),
          ValueLaw(unifs=[(0.0, 0.5, 0.1), (0.5, 2.5, 0.9)]), 0.5, 0.3, 2.0, 0.25, 0.5,
          "case 2a overlap, equal mass below p (u0 = p)")

# ----------------------------------------------------------------------------
# 7. Ownership caveat (case 2c) reproduces the memo numbers
# ----------------------------------------------------------------------------
hr("7. Case 2c: entry rises while high-class ownership falls")
GH = ValueLaw(unifs=[(0.0, 0.5, 0.1), (0.5, 19.5, 0.9)])
GL = ValueLaw(unifs=[(0.0, 0.5, 0.1), (0.5, 2.5, 0.9)])
p, pi, b, rho, cH, k = 0.5, 0.5, 2.0, 0.95, 5.121235, 0.029133
out = {r: class_objects_formula(GH, GL, p, r, 20.5) for r in (1.2, 3.0)}
cf = closed_forms(out[3.0][1], out[3.0][2], cH, pi, b, rho, W_H(GH, p, 3.0))
print(f"  entry r0=0.95 -> r1={cf['E']:.6f}; O_H r0={pi * rho * W_H(GH, p, 1.2):.6f} -> r1={cf['OH']:.6f};"
      f" W_H {W_H(GH, p, 1.2):.6f} -> {W_H(GH, p, 3.0):.6f}")
