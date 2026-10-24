"""Robust search for interior equilibria (both investor types mix), check of memo C1.

Print-only, double precision (numerical diagnostic). Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/X_C1_check/interior.py

For each strength r, each c_H and each fixed entry pattern, the script traces the contour
G_L(u, v) = k on a grid (linear interpolation in v inside each cell of each row) and looks for
sign changes of G_H - k between neighbouring contour points in adjacent rows. Each sign change is
refined by a 2-D solve. A root counts only if it is interior and its actual entry pattern
(baseline ties) equals the fixed pattern. The diagonal u = v is also solved directly, and the
antisymmetric eigenvalue p - q of the Jacobian is printed there (p = dG_H/du, q = dG_H/dv).
"""
import numpy as np
from scipy.optimize import brentq, fsolve

H_VAL, ELL, P_RES, RHO, B_SCALE, K = 10.0, 1.0, 0.5, 0.25, 2.0, 0.02
A = np.exp(-1.0 / B_SCALE)
D = 1.0 - A
ALPHA, BETA, GAMMA = A / (1 + A), 1 / (1 + A), (1 - A) / (1 + A)
DELTA, PHI = A ** 2 / (1 + A), A * (1 - A) / (1 + A)
PATTERNS = {"rrr": (RHO, RHO, RHO), "1rr": (1.0, RHO, RHO), "11r": (1.0, 1.0, RHO)}


def prims(r):
    gL = (ELL ** 2 - P_RES ** 2) / (2 * r)
    gH = H_VAL - r / 2 - P_RES ** 2 / (2 * r)
    return gL, gH, (r - ELL) ** 2 / (2 * r)


def tau(r, cH):
    gL, gH, _ = prims(r)
    return (cH - gL) / (gH - gL)


def post(u, v):
    Ap, Bp = 1 + u * D / A, 1 - v * D
    Am, Bm = 1 - u * D, 1 + v * D / A
    return Ap / (Ap + Bp), Am / (Am + Bp), Am / (Am + Bm)


def pattern_of(r, cH, u, v):
    t = tau(r, cH)
    return "".join("1" if mu >= t else "r" for mu in post(u, v))


def gains(r, pat, u, v):
    DT = prims(r)[2]
    e = PATTERNS[pat]
    mp_, m0, mm = post(u, v)
    GH = DT * (BETA * e[0] * (1 - mp_) + PHI * e[1] * (1 - m0) + DELTA * e[2] * (1 - mm))
    GL = DT * (DELTA * e[0] * mp_ + PHI * e[1] * m0 + BETA * e[2] * mm)
    return GH, GL


def entry_prob(u, v, pat):
    e = PATTERNS[pat]
    PH = ((1 - u) * ALPHA + u * BETA, (1 - u) * GAMMA + u * PHI, (1 - u) * ALPHA + u * DELTA)
    PL = ((1 - v) * ALPHA + v * DELTA, (1 - v) * GAMMA + v * PHI, (1 - v) * ALPHA + v * BETA)
    return sum(0.5 * (PH[i] + PL[i]) * e[i] for i in range(3))


def contour_roots(r, cH, pat, n):
    g = np.linspace(1e-7, 1 - 1e-7, n)
    UU, VV = np.meshgrid(g, g, indexing="ij")
    GH, GL = gains(r, pat, UU, VV)
    F1, F2 = GH - K, GL - K
    sc = np.sign(F2[:, :-1]) * np.sign(F2[:, 1:]) < 0          # root of F2 inside cell (i, j) along v
    w = np.where(sc, F2[:, :-1] / (F2[:, :-1] - F2[:, 1:]), np.nan)
    vroot = g[:-1] + w * (g[1] - g[0])
    f1 = np.full(vroot.shape, np.nan)
    ii, jj = np.nonzero(sc)
    f1[ii, jj] = gains(r, pat, g[ii], vroot[ii, jj])[0] - K
    cands = []
    # Compare contour point (i, ja) with contour point (i + 1, jb), jb - ja = dj.
    for dj in (-1, 0, 1):
        if dj == 1:
            a_, b_ = f1[:-1, :-1], f1[1:, 1:]
        elif dj == -1:
            a_, b_ = f1[:-1, 1:], f1[1:, :-1]
        else:
            a_, b_ = f1[:-1, :], f1[1:, :]
        hit = np.argwhere(np.sign(a_) * np.sign(b_) < 0)
        for i, j in hit:
            ja = j if dj >= 0 else j + 1
            jb = j + 1 if dj == 1 else j
            cands.append(((g[i] + g[i + 1]) / 2, (vroot[i, ja] + vroot[i + 1, jb]) / 2))
    found = []
    for u0, v0 in cands:
        sol, info, ier, _ = fsolve(lambda z: np.array(gains(r, pat, z[0], z[1])) - K,
                                   np.array([u0, v0]), full_output=True, xtol=1e-14)
        u, v = sol
        res = np.max(np.abs(np.array(gains(r, pat, u, v)) - K))
        if ier != 1 or res > 1e-12 or not (0 < u < 1 and 0 < v < 1):
            u, v, res = u0, v0, np.max(np.abs(np.array(gains(r, pat, u0, v0)) - K))
            tag = "grid"
        else:
            tag = "refined"
        if pattern_of(r, cH, u, v) != pat:
            continue
        if any(abs(u - a2) < 2e-3 and abs(v - b2) < 2e-3 for a2, b2, _, _ in found):
            continue
        found.append((u, v, tag, res))
    return found


def diagonal(r, cH):
    """Symmetric roots at constant entry and the antisymmetric Jacobian eigenvalue."""
    f = lambda s: gains(r, "rrr", s, s)[0] - K
    sg = np.linspace(1e-9, 1 - 1e-9, 4001)
    vals = f(sg)
    out = []
    for i in np.nonzero(np.sign(vals[:-1]) * np.sign(vals[1:]) < 0)[0]:
        s = brentq(f, sg[i], sg[i + 1], xtol=1e-15)
        h = 1e-6
        p = (gains(r, "rrr", s + h, s)[0] - gains(r, "rrr", s - h, s)[0]) / (2 * h)
        q = (gains(r, "rrr", s, s + h)[0] - gains(r, "rrr", s, s - h)[0]) / (2 * h)
        out.append((s, pattern_of(r, cH, s, s), p - q, p + q))
    return out


print("Interior equilibria under baseline ties (both types mix). Grid n = 601 per axis.")
rgrid = np.round(np.arange(1.40, 1.9501, 0.0025), 6)
for cH in (5.0, 6.0):
    print("=" * 78)
    print(f"c_H = {cH:g}")
    print("=" * 78)
    for r in rgrid:
        lines = []
        for pat in PATTERNS:
            for u, v, tag, res in contour_roots(r, cH, pat, 601):
                kind = "SYM" if abs(u - v) < 1e-6 else "INT"
                lines.append(f"{kind}[{pat}] u={u:.6f} v={v:.6f} E={entry_prob(u, v, pat):.6f} ({tag}, res {res:.1e})")
        diag = [d for d in diagonal(r, cH) if d[1] == "rrr"]
        if lines or diag:
            dtxt = "; ".join(f"diag s={s:.6f} p-q={pq:+.3e} p+q={pp:+.3e}" for s, _, pq, pp in diag)
            print(f"r={r:.4f}: " + (" | ".join(lines) if lines else "no off-diagonal root") + (" || " + dtxt if dtxt else ""))
    print()

print("=" * 78)
print("Finer grid (n = 1601) at selected strengths")
print("=" * 78)
for cH in (5.0, 6.0):
    for r in (1.41, 1.42, 1.43, 1.44, 1.52, 1.55, 1.60, 1.65, 1.70, 1.76, 1.77, 1.775, 1.79, 1.80, 1.8025, 1.81, 1.815, 1.82, 1.83, 1.84):
        lines = []
        for pat in PATTERNS:
            for u, v, tag, res in contour_roots(r, cH, pat, 1601):
                kind = "SYM" if abs(u - v) < 1e-6 else "INT"
                lines.append(f"{kind}[{pat}] u={u:.6f} v={v:.6f} E={entry_prob(u, v, pat):.6f} ({tag})")
        print(f"c_H={cH:g} r={r:.4f}: " + (" | ".join(lines) if lines else "none"))
