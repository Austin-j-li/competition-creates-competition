"""Uniform-family derivative, single-peaked D => single-peaked gap, Delta' + Delta/r identity,
location-family identity gap = dDelta/ds. Prints only."""
import math
import numpy as np

p = 0.5


def norm_cdf(x):
    return 0.5 * (1 + np.vectorize(math.erf)(x / math.sqrt(2)))


def trunc_norm_cdf(mu, sd, lo=p):
    base = norm_cdf((lo - mu) / sd)
    return lambda y: np.where(y < lo, 0.0, (norm_cdf((y - mu) / sd) - base) / (1 - base))


def unif_cdf(a, b):
    return lambda y: np.clip((y - a) / (b - a), 0, 1)


def make_D(GL, GH):
    return lambda y: GL(y) - GH(y)


ys = np.linspace(0, 60, 600001)
dy = ys[1] - ys[0]


def analyse(name, GL, GH):
    D = make_D(GL, GH)
    Dv = D(ys)
    Gam = np.cumsum(Dv) * dy
    Gam = Gam - 0.5 * Dv * dy
    # gap(r) = Gam(r)/r for the uniform family (D = 0 below p automatically)
    rs = ys[ys > 0.2]
    gap = Gam[ys > 0.2] / rs
    # single peakedness of D?
    dD = np.diff(Dv)
    sgn = np.sign(dD[np.abs(dD) > 1e-12])
    changes_D = int(np.sum(np.diff(sgn) != 0))
    # slope changes of the gap
    dg = np.diff(gap)
    sg = np.sign(dg[np.abs(dg) > 1e-12])
    changes_g = int(np.sum(np.diff(sg) != 0))
    i = int(np.argmax(gap))
    r_star = rs[i]
    Dstar = D(np.array([r_star]))[0]
    print(f"{name}: sign changes of D' = {changes_D}, of gap' = {changes_g}; "
          f"gap peak r*={r_star:.3f} (gap={gap[i]:.4f}), D(r*)={Dstar:.4f} vs avg gap(r*)={gap[i]:.4f}; "
          f"D peak at {ys[np.argmax(Dv)]:.2f}")


analyse("benchmark points (1,10)", lambda y: (y >= 1.0) * 1.0, lambda y: (y >= 10.0) * 1.0)
analyse("counterexample points (1,2)", lambda y: (y >= 1.0) * 1.0, lambda y: (y >= 2.0) * 1.0)
analyse("uniform pair U[1,4] vs U[2,9]", unif_cdf(1, 4), unif_cdf(2, 9))
analyse("uniform pair U[0.6,3] vs U[0.6,12]", unif_cdf(0.6, 3), unif_cdf(0.6, 12))
analyse("trunc normal (2,1) vs (5,1)", trunc_norm_cdf(2, 1), trunc_norm_cdf(5, 1))
analyse("trunc normal (2,1) vs (9,3)", trunc_norm_cdf(2, 1), trunc_norm_cdf(9, 3))
analyse("trunc normal (3,2) vs (4,2)", trunc_norm_cdf(3, 2), trunc_norm_cdf(4, 2))

# identity gap(r) = Delta'(r) + Delta(r)/r on the uniform family (point-mass benchmark classes 1 and 10)
print("\nIdentity gap(r) = Delta'(r) + Delta(r)/r, benchmark classes, uniform family")
ell, h = 1.0, 10.0
for r in (1.2, 2.0, 3.0, 3.6, 8.0):
    Delta = (r - ell) ** 2 / (2 * r)
    dDelta = (r - ell) * (r + ell) / (2 * r * r)
    print(f"  r={r}: Delta'+Delta/r = {dDelta + Delta / r:.6f}  vs  1-ell/r = {1 - ell / r:.6f}")

# location family: gap = dDelta/ds, with xi(R) = int_p^R D
print("\nLocation family R = s + Z, Z ~ U[0,2], benchmark classes (ell=1, h=10): gap vs finite-difference Delta'(s)")


def Delta_loc(s, w=2.0, ell=1.0, h=10.0):
    # Delta = E[xi(R)], xi(R) = (min(R,h)-ell)_+ for benchmark classes
    zs = np.linspace(0, w, 200001)
    R = s + zs
    xi = np.clip(np.minimum(R, h) - ell, 0, None)
    return xi.mean()


def gap_loc(s, w=2.0, ell=1.0, h=10.0):
    zs = np.linspace(0, w, 200001)
    R = s + zs
    WH = np.clip(np.minimum(h / np.maximum(R, 1e-9), 1), 0, 1)  # placeholder, replaced below
    # direct: W_j = Pr(theta > R) = Pr(R < theta) for point mass theta
    WH = (R < h).mean()
    WL = (R < ell).mean()
    return WH - WL


for s in (0.2, 0.5, 1.0, 2.0, 5.0, 9.0):
    eps = 1e-4
    dD = (Delta_loc(s + eps) - Delta_loc(s - eps)) / (2 * eps)
    print(f"  s={s}: dDelta/ds = {dD:.5f}   gap = {gap_loc(s):.5f}")
