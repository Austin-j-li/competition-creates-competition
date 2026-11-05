"""(b) Class membership, extremal properties of Laplace, and the Blackwell comparison.

Print-only. Run from the repository root:
    .venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q2_laplace_technical/g2_class_extremal_blackwell.py

Score psi = -(log f)'. The class C_L is {f : |psi| <= L a.e.}. Benchmark b = 2, L = 1/2.
Blackwell check for a dichotomy at prior 1/2 under full orders: experiment E dominates E'
iff G_E(tau) >= G_E'(tau) for every tau, where G(tau) = E[(mu - tau)_+]
= (1/2) int [(1 - tau) f(x - 1) - tau f(x + 1)]_+ dx.
"""
from __future__ import annotations

import math
import os
import sys

import numpy as np
from scipy import integrate, optimize, special, stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from noise_laws import Gaussian, HypSecant, Laplace, Logistic, NormalLaplace, StudentT  # noqa: E402

b = 2.0
L = 1.0 / b


class GaussMix:
    """Finite Gaussian mixture 0.5 N(0, s1^2) + 0.5 N(0, s2^2)."""

    def __init__(self, s1, s2):
        self.s1, self.s2 = s1, s2
        self.name = f"0.5N(0,{s1:g}^2)+0.5N(0,{s2:g}^2)"
        self.L = math.inf
        self.kinks = []

    def logpdf(self, z):
        z = np.asarray(z, dtype=float)
        return np.logaddexp(stats.norm.logpdf(z, scale=self.s1), stats.norm.logpdf(z, scale=self.s2)) + math.log(0.5)

    def sf(self, z):
        z = np.asarray(z, dtype=float)
        return 0.5 * stats.norm.sf(z, scale=self.s1) + 0.5 * stats.norm.sf(z, scale=self.s2)

    def score(self, z):
        z = np.asarray(z, dtype=float)
        w1 = np.exp(stats.norm.logpdf(z, scale=self.s1) - self.logpdf(z) + math.log(0.5))
        return w1 * z / self.s1 ** 2 + (1 - w1) * z / self.s2 ** 2

    def var(self):
        return 0.5 * (self.s1 ** 2 + self.s2 ** 2)


MEMBERS = [
    Laplace(b), Logistic(b), HypSecant(b), StudentT.with_bound(3.0, L), StudentT.with_bound(1.0, L),
    NormalLaplace(b, 1.0),
]
OUTSIDE = [Gaussian(b), Gaussian(math.sqrt(2.0) * b), GaussMix(1.0, 3.0)]

print("=" * 100)
print("Part A. Class membership: score bound, log-concavity, likelihood-ratio bound K_f")
print("  K_f = sup over shifts 0 < d <= 2 of sup_y f(y+d)/f(y), on |y| <= 200; paper bound e^{2/b} =", f"{math.exp(2 * L):.6f}")
zz = np.linspace(-200, 200, 400001)
print(f"{'law':40s}{'sup|psi| grid':>14s}{'analytic L':>11s}{'psi at 200':>11s}{'log-concave':>12s}{'K_f':>10s}")
for law in MEMBERS + OUTSIDE:
    psi = law.score(zz)
    lc = bool(np.min(np.diff(psi)) >= -1e-12)
    K = 0.0
    for d in (0.5, 1.0, 1.5, 2.0):
        K = max(K, float(np.max(law.logpdf(zz + d) - law.logpdf(zz))))
    Ktxt = f"{math.exp(K):10.4f}" if K < 20 else f"{'e^' + format(K, '.0f'):>10s}"
    print(f"{law.name:40s}{np.max(np.abs(psi)):14.6f}{law.L:11.4f}{float(law.score(200.0)):11.5f}{str(lc):>12s}{Ktxt}")
print("  Uniform noise on [-c, c]: f = 0 outside the support, so log f is not Lipschitz and K_f = infinity.")

print("\n" + "=" * 100)
print("Part B. Concentration: Pr(|Z| > t) for members with L = 1/2 (claim: Laplace is smallest, = e^{-t/2})")
ts = [0.25, 0.5, 1, 2, 4, 8, 16, 32]
print(f"{'law':40s}{'var':>9s}" + "".join(f"{t:>9g}" for t in ts))
for law in MEMBERS:
    print(f"{law.name:40s}{law.var():9.3f}" + "".join(f"{2 * float(law.sf(t)):9.5f}" for t in ts))
print(f"{'e^{-L t}':40s}{'':9s}" + "".join(f"{math.exp(-L * t):9.5f}" for t in ts))

print("\n" + "=" * 100)
print("Part C. Fisher information I(f) = E[psi^2] (claim: at most L^2 = 0.25, equal only for Laplace)")
for law in MEMBERS:
    val, _ = integrate.quad(lambda z: law.score(z) ** 2 * math.exp(float(law.logpdf(z))), -np.inf, np.inf, limit=400, points=None)
    print(f"  {law.name:40s} I(f) = {val:.6f}")

print("\n" + "=" * 100)
print("Part D. Plateau mass at the upper bound M = e^{2L}/(1+e^{2L}) under full orders")
M = math.exp(2 * L) / (1 + math.exp(2 * L))
print("  mass of {x : lambda(x) >= 2L - tol} under H; an exact plateau keeps its mass as tol -> 0")
for law in MEMBERS:
    lam = law.logpdf(zz - 1) - law.logpdf(zz + 1)
    row = []
    for tol in (1e-4, 1e-8, 1e-12):
        on = lam >= 2 * L - tol
        row.append(float(law.sf(zz[on].min() - 1)) if on.any() else 0.0)
    print(f"  {law.name:40s} max lambda = {lam.max():.12f};  tol 1e-4: {row[0]:.6f}  1e-8: {row[1]:.6f}  1e-12: {row[2]:.6f}")
lap_ = Laplace(b)
print(f"  Laplace exact plateau x >= 1: Pr(mu=M|H) = {float(lap_.sf(0.0)):.6f}, Pr(mu=M|L) = {float(lap_.sf(2.0)):.6f}")
print(f"  Bounds from the claim: Pr(mu=M|H) <= 1/2, Pr(mu=M|L) <= e^(-2L)/2 = {math.exp(-2 * L) / 2:.6f}")

print("\n" + "=" * 100)
print("Part E. Laplace kernel k = f - b^2 f'' = f (1 - b^2 psi^2 + b^2 psi') (f = Laplace(b) * k iff k >= 0)")


def kernel(law, z, h=1e-5):
    psi_p = (law.score(z + h) - law.score(z - h)) / (2 * h)
    return np.exp(law.logpdf(z)) * (1 - b * b * law.score(z) ** 2 + b * b * psi_p)


zk = np.linspace(-60, 60, 120001)
for law in MEMBERS[1:]:
    kv = kernel(law, zk)
    tot, _ = integrate.quad(lambda z: float(kernel(law, z)), -np.inf, np.inf, limit=400)
    imin = int(np.argmin(kv))
    print(f"  {law.name:40s} min k = {kv[imin]: .3e} at z = {zk[imin]: .3f}; integral of k = {tot:.8f}")
lg, hs = Logistic(b), HypSecant(b)
err_lg = np.max(np.abs(kernel(lg, zk) - 3 / (8 * b) / np.cosh(zk / (2 * b)) ** 4))
err_hs = np.max(np.abs(kernel(hs, zk) - 2 / (math.pi * b) / np.cosh(zk / b) ** 3))
print(f"  closed forms: logistic k = (3/(8b)) sech^4(z/(2b)), max error {err_lg:.2e}; "
      f"hyperbolic secant k = (2/(pi b)) sech^3(z/b), max error {err_hs:.2e}")
lap = Laplace(b)
print("  Convolution check f(z) = int Laplace_b(z - w) k(w) dw:")
def sech(x):
    a = abs(x)
    return 2.0 * math.exp(-a) / (1.0 + math.exp(-2.0 * a))


for law, kfun in ((lg, lambda w: 3 / (8 * b) * sech(w / (2 * b)) ** 4), (hs, lambda w: 2 / (math.pi * b) * sech(w / b) ** 3)):
    for z in (0.0, 1.0, 3.0, 8.0):
        integrand = lambda w: math.exp(float(lap.logpdf(z - w))) * kfun(w)
        conv = integrate.quad(integrand, -np.inf, z, limit=400, epsabs=1e-14)[0] + integrate.quad(integrand, z, np.inf, limit=400, epsabs=1e-14)[0]
        print(f"    {law.name:20s} z = {z:4.1f}: convolution {conv:.10f}  density {math.exp(float(law.logpdf(z))):.10f}")
cau = StudentT.with_bound(1.0, L)
u = np.linspace(-5, 5, 100001)
kc = (u ** 2 - 1) * (u ** 2 - 3) / (1 + u ** 2) ** 3 / (math.pi * cau.sigma)
print(f"  Cauchy (sigma = b): k = (u^2-1)(u^2-3)/(pi sigma (1+u^2)^3), u = z/sigma; min = {kc.min():.4f} -> not Laplace(b) * k")

print("\n" + "=" * 100)
print("Part F. Blackwell comparison of full-order experiments: D(tau) = G_Laplace(b=2)(tau) - G_other(tau)")
xg = np.linspace(-200, 200, 80001)


def G_curve(law, taus):
    lam_g = law.logpdf(xg - 1) - law.logpdf(xg + 1)
    lam = lambda x: float(law.logpdf(x - 1) - law.logpdf(x + 1))
    out = []
    for tau in taus:
        c = math.log(tau / (1 - tau))
        g = lam_g - c
        ins = g >= 0
        ivs, start = [], (-math.inf if ins[0] else None)
        for i in np.nonzero(ins[1:] != ins[:-1])[0]:
            root = optimize.brentq(lambda x: lam(x) - c, xg[i], xg[i + 1], xtol=1e-13)
            if ins[i + 1]:
                start = root
            else:
                ivs.append((start, root))
                start = None
        if start is not None:
            ivs.append((start, math.inf))
        tot = 0.0
        for lo, hi in ivs:
            pH = (1.0 if lo == -math.inf else float(law.sf(lo - 1))) - (0.0 if hi == math.inf else float(law.sf(hi - 1)))
            pL = (1.0 if lo == -math.inf else float(law.sf(lo + 1))) - (0.0 if hi == math.inf else float(law.sf(hi + 1)))
            tot += 0.5 * ((1 - tau) * pH - tau * pL)
        out.append(tot)
    return np.array(out)


taus = np.concatenate([np.linspace(0.005, 0.995, 199), [0.7, 0.73, 0.7310, 0.7311, 0.75, 0.8, 0.9]])
taus.sort()
G_lap = G_curve(Laplace(b), taus)
others = [Logistic(b), HypSecant(b), NormalLaplace(b, 1.0), StudentT.with_bound(3.0, L), StudentT.with_bound(1.0, L),
          Logistic(math.sqrt(6.0) * b / math.pi), Gaussian(b), Gaussian(math.sqrt(2.0) * b), Gaussian(math.sqrt(b))]
print(f"{'other law':40s}{'var':>8s}{'min D':>12s}{'at tau':>8s}{'max D':>12s}{'at tau':>8s}  verdict")
for law in others:
    D = G_lap - G_curve(law, taus)
    i0, i1 = int(np.argmin(D)), int(np.argmax(D))
    if D.min() >= -1e-10:
        verdict = "Laplace dominates"
    elif D.max() <= 1e-10:
        verdict = "other dominates"
    else:
        verdict = "curves cross: neither dominates"
    print(f"{law.name:40s}{law.var():8.3f}{D[i0]:12.3e}{taus[i0]:8.4f}{D[i1]:12.3e}{taus[i1]:8.4f}  {verdict}")


print("\n" + "=" * 100)
print("Part G. ROC bound for any member (claim: beta_f(alpha) <= beta_Lap(alpha) for every test, every f in C_L)")
print("  Laplace ROC for orders (1, -1): beta(a) = a e^{2L} (a <= e^{-2L}/2); 1 - e^{-2L}/(4a) (<= 1/2); 1 - (1-a) e^{-2L} (a >= 1/2)")
print("  Grid laws (normalised numerically, step 0.002 on [-150, 150]); Lipschitz constant of log f is at most L = 1/2.")
xs = np.linspace(-150, 150, 150001)
dx = xs[1] - xs[0]


def grid_law(logf_unnorm):
    lf = logf_unnorm(xs)
    w = np.exp(lf - lf.max())
    Z = np.trapezoid(w, xs)
    return lambda x: np.interp(x, xs, w / Z, left=0.0, right=0.0)


def beta_lap(a):
    e = math.exp(-2 * L)
    if a <= e / 2:
        return a / e
    if a <= 0.5:
        return 1 - e / (4 * a)
    return 1 - (1 - a) * e


def roc_points(f):
    fH, fL = f(xs - 1), f(xs + 1)
    keep = (fH > 1e-300) | (fL > 1e-300)
    lr = np.where(fL[keep] > 0, fH[keep] / np.maximum(fL[keep], 1e-300), np.inf)
    order = np.argsort(-lr)
    aL = np.cumsum(fL[keep][order]) * dx
    bH = np.cumsum(fH[keep][order]) * dx
    return aL, bH


cases = [
    ("Laplace(b=2) itself", lambda x: -L * np.abs(x)),
    ("bimodal exp(-L||z|-1|)", lambda x: -L * np.abs(np.abs(x) - 1.0)),
    ("bimodal exp(-L||z|-3|)", lambda x: -L * np.abs(np.abs(x) - 3.0)),
    ("oscillating -0.3|z| + 0.2 sin z", lambda x: -0.3 * np.abs(x) + 0.2 * np.sin(x)),
    ("asymmetric rates 0.5 / 0.25", lambda x: np.where(x < 0, 0.5 * x, -0.25 * x)),
    ("Student t nu=3 (bound 1/2)", lambda x: StudentT.with_bound(3.0, L).logpdf(x)),
]
print(f"{'law':36s}{'max [beta_f - beta_Lap]':>26s}{'at alpha':>10s}")
for name, lf in cases:
    f = grid_law(lf)
    aL, bH = roc_points(f)
    sel = (aL > 1e-6) & (aL < 1 - 1e-6)
    gap = bH[sel] - np.array([beta_lap(a) for a in aL[sel]])
    i = int(np.argmax(gap))
    print(f"{name:36s}{gap[i]:26.2e}{aL[sel][i]:10.4f}")
