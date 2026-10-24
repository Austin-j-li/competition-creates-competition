"""Enumerate equilibria of the two-sided discrete-Laplace model (check of memo C1).

Print-only, double precision (numerical diagnostic). Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/X_C1_check/enumerate.py

Candidate: H buys with probability u, L sells with probability v (wrong-signed orders are
strictly dominated against every schedule, so no other candidate can be an equilibrium).
Posterior classes: X >= 1, X = 0, X <= -1. Entry at posterior mu under baseline ties:
rho + (1-rho) 1{mu >= tau}. For tau > 1/2 the entry pattern on the three classes is one of
(rho,rho,rho), (1,rho,rho), (1,1,rho).

Search, for each strength r and each c_H:
  corners: direct check;
  edges: for each fixed pattern, roots of the indifference of the free type on a 4001-point
         grid, refined by brentq; kept only if the actual pattern matches and the other type's
         corner condition holds;
  interior: for each fixed pattern, grid squares (401 x 401 nodes) where both indifference
         functions change sign; refined by a 2-D Newton solve; kept only if the root is
         interior and the actual pattern matches.
Then: challenger-mixing points on the jump lines mu_+ = tau and mu_0 = tau.
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
    DT = (r - ELL) ** 2 / (2 * r)
    return gL, gH, DT


def tau(r, cH):
    gL, gH, _ = prims(r)
    return (cH - gL) / (gH - gL)


def post(u, v):
    Ap, Bp = 1 + u * D / A, 1 - v * D
    Am, Bm = 1 - u * D, 1 + v * D / A
    return Ap / (Ap + Bp), Am / (Am + Bp), Am / (Am + Bm)


def pattern_of(r, cH, u, v):
    t = tau(r, cH)
    mus = post(u, v)
    key = "".join("1" if mu >= t else "r" for mu in mus)
    return key, min(abs(mu - t) for mu in mus)


def gains(r, pat, u, v, es=None):
    DT = prims(r)[2]
    e = PATTERNS[pat] if es is None else es
    mp_, m0, mm = post(u, v)
    GH = DT * (BETA * e[0] * (1 - mp_) + PHI * e[1] * (1 - m0) + DELTA * e[2] * (1 - mm))
    GL = DT * (DELTA * e[0] * mp_ + PHI * e[1] * m0 + BETA * e[2] * mm)
    return GH, GL


def entry_prob(u, v, e):
    PH = ((1 - u) * ALPHA + u * BETA, (1 - u) * GAMMA + u * PHI, (1 - u) * ALPHA + u * DELTA)
    PL = ((1 - v) * ALPHA + v * DELTA, (1 - v) * GAMMA + v * PHI, (1 - v) * ALPHA + v * BETA)
    return sum(0.5 * (PH[i] + PL[i]) * e[i] for i in range(3))


def corner_eqs(r, cH):
    out = []
    names = {(0, 0): "NT", (1, 1): "T", (1, 0): "BNS", (0, 1): "SNB"}
    for (u, v), name in names.items():
        pat, gap = pattern_of(r, cH, u, v)
        GH, GL = gains(r, pat, u, v)
        okH = GH <= K if u == 0 else GH >= K
        okL = GL <= K if v == 0 else GL >= K
        if okH and okL:
            out.append((name, u, v, pat, entry_prob(u, v, PATTERNS[pat]), min(abs(GH - K), abs(GL - K))))
    return out


TGRID = np.linspace(1e-9, 1 - 1e-9, 4001)


def edge_eqs(r, cH):
    out = []
    # (label, fixed coordinate, free type, other type's condition)
    edges = (("u=1", 1.0, "L", lambda GH: GH >= K), ("u=0", 0.0, "L", lambda GH: GH <= K),
             ("v=0", 0.0, "H", lambda GL: GL <= K), ("v=1", 1.0, "H", lambda GL: GL >= K))
    for label, fixed, free, other_ok in edges:
        for pat in PATTERNS:
            if label.startswith("u"):
                f = lambda t: gains(r, pat, fixed, t)[1] - K
            else:
                f = lambda t: gains(r, pat, t, fixed)[0] - K
            vals = f(TGRID)
            idx = np.nonzero(np.sign(vals[:-1]) * np.sign(vals[1:]) < 0)[0]
            for i in idx:
                t0 = brentq(f, TGRID[i], TGRID[i + 1], xtol=1e-15)
                u, v = (fixed, t0) if label.startswith("u") else (t0, fixed)
                act, gap = pattern_of(r, cH, u, v)
                if act != pat:
                    continue
                GH, GL = gains(r, pat, u, v)
                other = GH if free == "L" else GL
                if other_ok(other):
                    out.append(("edge " + label, u, v, pat, entry_prob(u, v, PATTERNS[pat]),
                                abs(other - K), gap))
    return out


NG = 401
UG = np.linspace(1e-7, 1 - 1e-7, NG)
UU, VV = np.meshgrid(UG, UG, indexing="ij")


def interior_eqs(r, cH):
    out = []
    for pat in PATTERNS:
        GH, GL = gains(r, pat, UU, VV)
        F1, F2 = GH - K, GL - K
        s1, s2 = np.sign(F1), np.sign(F2)

        def changes(sg):
            c = np.stack([sg[:-1, :-1], sg[1:, :-1], sg[:-1, 1:], sg[1:, 1:]])
            return (c.max(axis=0) > 0) & (c.min(axis=0) < 0)

        cand = np.argwhere(changes(s1) & changes(s2))
        found = []
        for i, j in cand:
            x0 = np.array([(UG[i] + UG[i + 1]) / 2, (UG[j] + UG[j + 1]) / 2])
            sol, info, ier, _ = fsolve(lambda z: np.array(gains(r, pat, z[0], z[1])) - K, x0,
                                       full_output=True, xtol=1e-14)
            if ier != 1:
                continue
            u, v = sol
            if not (0 < u < 1 and 0 < v < 1):
                continue
            if np.max(np.abs(np.array(gains(r, pat, u, v)) - K)) > 1e-12:
                continue
            act, gap = pattern_of(r, cH, u, v)
            if act != pat:
                continue
            if any(abs(u - a_) < 1e-7 and abs(v - b_) < 1e-7 for a_, b_ in found):
                continue
            found.append((u, v))
            out.append(("interior", u, v, pat, entry_prob(u, v, PATTERNS[pat]), 0.0, gap))
    return out


def all_eqs(r, cH):
    return corner_eqs(r, cH) + edge_eqs(r, cH) + interior_eqs(r, cH)


def kind(eq):
    name, u, v = eq[0], eq[1], eq[2]
    if name in ("NT", "T", "BNS", "SNB"):
        return name
    if name == "edge u=1":
        return "FB-PS[" + eq[3] + "]"
    if name == "edge v=1":
        return "PB-FS[" + eq[3] + "]"
    if name == "edge v=0":
        return "PB-NS[" + eq[3] + "]"
    if name == "edge u=0":
        return "NB-PS[" + eq[3] + "]"
    return ("SYM-" if abs(u - v) < 1e-9 else "INT-") + "[" + eq[3] + "]"


def fmt(eq):
    return f"{kind(eq):14s} u={eq[1]:.6f} v={eq[2]:.6f} E={eq[4]:.6f}"


print("Parameters: h=10, ell=1, p=0.5, rho=0.25, b=2, k=0.02, c_L=0; a =", f"{A:.12f}")
print()
rgrid = np.round(np.arange(1.40, 1.9501, 0.0025), 6)
extra = np.array([1.05, 1.1, 1.2, 1.3, 1.35, 2.0, 2.2, 2.5, 3.0, 3.3, 3.6, 4.0, 5.0, 6.0, 6.3, 6.4, 7.0, 8.0])
rall = np.unique(np.concatenate([rgrid, extra]))
detail = {1.2, 1.45, 1.5, 1.52, 1.525, 1.53, 1.5325, 1.535, 1.55, 1.6, 1.65, 1.7, 1.745, 1.75,
          1.7625, 1.78, 1.8, 1.82, 1.8225, 1.825, 1.8275, 1.83, 1.835, 1.84, 1.845, 1.85, 1.9, 3.0, 3.6}
for cH in (5.0, 6.0):
    print("=" * 78)
    print(f"c_H = {cH:g}: equilibria under baseline ties (investor may mix; challenger prepares at indifference)")
    print("=" * 78)
    runs = []
    for r in rall:
        eqs = all_eqs(r, cH)
        sigk = tuple(sorted(set(kind(e) for e in eqs)))
        if runs and runs[-1][2] == sigk:
            runs[-1][1] = r
        else:
            runs.append([r, r, sigk])
        if any(abs(r - d_) < 1e-9 for d_ in detail):
            print(f"r={r:.4f} tau={tau(r, cH):.6f}  ({len(eqs)} equilibria)")
            for e in sorted(eqs, key=lambda e: (kind(e), e[1], e[2])):
                print("    " + fmt(e))
    print("-" * 78)
    print("Ranges of strengths on the grid with the same set of equilibrium kinds:")
    for lo, hi, sigk in runs:
        print(f"  r in [{lo:.4f}, {hi:.4f}]: {', '.join(sigk) if sigk else 'NONE'}")
    print()

# Fine scans of the constant-entry full-buy / partial-sell edge for c_H = 6.
print("=" * 78)
print("Constant-entry edge u = 1 for c_H = 6: root of G_L(1,v) = k with entry rho everywhere")
print("=" * 78)
for r in np.round(np.arange(1.8190, 1.8320, 0.0005), 6):
    f = lambda t: gains(r, "rrr", 1.0, t)[1] - K
    vals = f(TGRID)
    idx = np.nonzero(np.sign(vals[:-1]) * np.sign(vals[1:]) < 0)[0]
    roots = [brentq(f, TGRID[i], TGRID[i + 1], xtol=1e-15) for i in idx]
    t6 = tau(r, 6.0)
    vt = (1 - (1 - t6) / (A * t6)) / D
    line = f"  r={r:.4f} v_tau={vt:.6f} roots:"
    for v in roots:
        GH, GL = gains(r, "rrr", 1.0, v)
        line += f" v={v:.6f} (mu+<tau: {post(1.0, v)[0] < t6}, H net={GH - K:+.2e})"
    print(line)


def end_of_branch():
    g = lambda r: (lambda vt: gains(r, "rrr", 1.0, vt)[1] - K)((1 - (1 - tau(r, 6.0)) / (A * tau(r, 6.0))) / D)
    return brentq(g, 1.8194, 1.86, xtol=1e-14)


r_end = end_of_branch()
print(f"  constant-entry FB-PS branch for c_H=6 starts at r=1.819330 (v=0) and meets mu+ = tau at r={r_end:.6f}")
print()

# Challenger mixing on the jump lines.
print("=" * 78)
print("Jump lines: points where both investor types are indifferent need e_H* = e_L*")
print("=" * 78)
for cH in (5.0, 6.0):
    for r in (1.55, 1.60, 1.65):
        t = tau(r, cH)
        DT = prims(r)[2]
        # Line mu_+ = tau: (1-t)(D/A) u + t D v = 2t - 1.
        us = np.linspace(0, 1, 20001)[1:]
        vs = (2 * t - 1 - (1 - t) * (D / A) * us) / (t * D)
        keep = (vs >= 0) & (vs <= 1)
        u_, v_ = us[keep], vs[keep]
        mp_, m0, mm = post(u_, v_)
        e0 = np.where(m0 >= t, 1.0, RHO)
        eH = (K / DT - e0 * PHI * (1 - m0) - RHO * DELTA * (1 - mm)) / (BETA * (1 - t))
        eL = (K / DT - e0 * PHI * m0 - RHO * BETA * mm) / (DELTA * t)
        dif = eL - eH
        sgn = np.nonzero(np.sign(dif[:-1]) * np.sign(dif[1:]) < 0)[0]
        print(f"c_H={cH:g} r={r:.2f} line mu+=tau: u in [{u_.min():.4f}, {u_.max():.4f}], "
              f"e_L*-e_H* in [{dif.min():.4f}, {dif.max():.4f}], sign changes: {len(sgn)}")
        if cH == 5.0:
            # Line mu_0 = tau: -(1-t) D u + t D v = 2t - 1; here mu_+ > tau, so e_+ = 1.
            us = np.linspace(0, 1, 20001)[1:]
            vs = (2 * t - 1 + (1 - t) * D * us) / (t * D)
            keep = (vs >= 0) & (vs <= 1)
            u_, v_ = us[keep], vs[keep]
            mp_, m0, mm = post(u_, v_)
            eH = (K / DT - BETA * (1 - mp_) - RHO * DELTA * (1 - mm)) / (PHI * (1 - t))
            eL = (K / DT - DELTA * mp_ - RHO * BETA * mm) / (PHI * t)
            dif = eL - eH
            sgn = np.nonzero(np.sign(dif[:-1]) * np.sign(dif[1:]) < 0)[0]
            print(f"           line mu0=tau: u in [{u_.min():.4f}, {u_.max():.4f}], "
                  f"e_L*-e_H* in [{dif.min():.4f}, {dif.max():.4f}], sign changes: {len(sgn)}, "
                  f"e_H* in [{eH.min():.3f}, {eH.max():.3f}]")
