"""End points of the baseline-tie branches that memo C1 does not report.

Print-only, double precision (numerical diagnostic). Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/X_C1_check/branches_extra.py

1. Constant entry: the zero set of G_H - G_L off the diagonal does not depend on r, because both
   gains are rho * DT(r) times functions of (u, v). Each point of that curve is an interior
   equilibrium at the strength r that solves rho DT(r) g_H(u, v) = k, if the pattern stays constant.
2. Ends of the symmetric family, the one-sided constant-entry edges, and the c_H = 5 partial-buy
   branch with recruitment.
"""
import numpy as np
from scipy.optimize import brentq

H_VAL, ELL, P_RES, RHO, B_SCALE, K = 10.0, 1.0, 0.5, 0.25, 2.0, 0.02
A = np.exp(-1.0 / B_SCALE)
D = 1.0 - A
ALPHA, BETA, GAMMA = A / (1 + A), 1 / (1 + A), (1 - A) / (1 + A)
DELTA, PHI = A ** 2 / (1 + A), A * (1 - A) / (1 + A)


def prims(r):
    gL = (ELL ** 2 - P_RES ** 2) / (2 * r)
    gH = H_VAL - r / 2 - P_RES ** 2 / (2 * r)
    return gL, gH, (r - ELL) ** 2 / (2 * r)


def tau(r, cH):
    gL, gH, _ = prims(r)
    return (cH - gL) / (gH - gL)


def rr(dd):
    return ELL + dd + np.sqrt(dd ** 2 + 2 * ELL * dd)


def post(u, v):
    Ap, Bp = 1 + u * D / A, 1 - v * D
    Am, Bm = 1 - u * D, 1 + v * D / A
    return Ap / (Ap + Bp), Am / (Am + Bp), Am / (Am + Bm)


def g_const(u, v):
    """G_H and G_L divided by rho * DT under constant entry rho."""
    mp_, m0, mm = post(u, v)
    return (BETA * (1 - mp_) + PHI * (1 - m0) + DELTA * (1 - mm),
            DELTA * mp_ + PHI * m0 + BETA * mm)


def g_rec(u, v):
    """G_H and G_L divided by DT under entry (1, rho, rho)."""
    mp_, m0, mm = post(u, v)
    return (BETA * (1 - mp_) + RHO * PHI * (1 - m0) + RHO * DELTA * (1 - mm),
            DELTA * mp_ + RHO * PHI * m0 + RHO * BETA * mm)


def entry_prob(u, v, e):
    PH = ((1 - u) * ALPHA + u * BETA, (1 - u) * GAMMA + u * PHI, (1 - u) * ALPHA + u * DELTA)
    PL = ((1 - v) * ALPHA + v * DELTA, (1 - v) * GAMMA + v * PHI, (1 - v) * ALPHA + v * BETA)
    return sum(0.5 * (PH[i] + PL[i]) * e[i] for i in range(3))


print("=" * 78)
print("1. Constant entry: off-diagonal zero set of G_H - G_L (independent of r)")
print("=" * 78)
diff = lambda u, v: g_const(u, v)[0] - g_const(u, v)[1]
pts = []
for u in np.linspace(0.0, 1.0, 2001):
    vg = np.linspace(0.0, 1.0, 4001)
    dv = diff(u, vg)
    for i in np.nonzero(np.sign(dv[:-1]) * np.sign(dv[1:]) < 0)[0]:
        v = brentq(lambda t: diff(u, t), vg[i], vg[i + 1], xtol=1e-15)
        if abs(v - u) > 1e-4:
            pts.append((u, v))
pts = sorted(pts)
print(f"  points found: {len(pts)}")
for u, v in pts[:: max(1, len(pts) // 12)] + pts[-1:]:
    gh = g_const(u, v)[0]
    r = rr(K / (RHO * gh))
    mp_, m0, mm = post(u, v)
    print(f"  u={u:.4f} v={v:.4f}  g_H={gh:.6f}  r={r:.6f}  mu=({mp_:.4f},{m0:.4f},{mm:.4f})"
          f"  tau5={tau(r, 5):.4f} tau6={tau(r, 6):.4f}")
# Where the curve crosses the diagonal (pitchfork point of the symmetric family).
dd = lambda s: (diff(s + 1e-6, s - 1e-6))
sgrid = np.linspace(0.01, 0.99, 981)
vals = np.array([dd(s) for s in sgrid])
for i in np.nonzero(np.sign(vals[:-1]) * np.sign(vals[1:]) < 0)[0]:
    s = brentq(dd, sgrid[i], sgrid[i + 1], xtol=1e-13)
    gh = g_const(s, s)[0]
    print(f"  crossing of the diagonal near s={s:.6f}, strength r={rr(K / (RHO * gh)):.6f}")
# Where the curve meets the edges.
for name, f in (("v=0", lambda u: diff(u, 0.0)), ("u=0", lambda v: diff(0.0, v)),
                ("u=1", lambda v: diff(1.0, v)), ("v=1", lambda u: diff(u, 1.0))):
    tg = np.linspace(1e-9, 1 - 1e-9, 4001)
    fv = f(tg)
    for i in np.nonzero(np.sign(fv[:-1]) * np.sign(fv[1:]) < 0)[0]:
        t = brentq(f, tg[i], tg[i + 1], xtol=1e-15)
        u, v = {"v=0": (t, 0.0), "u=0": (0.0, t), "u=1": (1.0, t), "v=1": (t, 1.0)}[name]
        gh = g_const(u, v)[0]
        print(f"  meets edge {name} at ({u:.6f}, {v:.6f}), strength r={rr(K / (RHO * gh)):.6f}")

print()
print("=" * 78)
print("2. Ends of the symmetric constant-entry family u = v = s")
print("=" * 78)
print(f"  starts at s=0, r = r_N = {rr(2 * K / RHO):.6f}")
for cH in (5.0, 6.0):
    def gap(r):
        s = brentq(lambda t: RHO * prims(r)[2] * g_const(t, t)[0] - K, 1e-12, 1 - 1e-12)
        return post(s, s)[0] - tau(r, cH), s
    r_end = brentq(lambda r: gap(r)[0], rr(2 * K / RHO) + 1e-9, 1.85)
    print(f"  c_H={cH:g}: leaves the constant pattern (mu+ = tau) at r={r_end:.6f}, s={gap(r_end)[1]:.6f}")

print()
print("=" * 78)
print("3. One-sided edges at constant entry (c_H = 6)")
print("=" * 78)
for r in np.round(np.arange(1.765, 1.7801, 0.0025), 6):
    DT = prims(r)[2]
    f = lambda u: RHO * DT * g_const(u, 0.0)[0] - K
    ug = np.linspace(1e-9, 1 - 1e-9, 4001)
    fv = f(ug)
    out = []
    for i in np.nonzero(np.sign(fv[:-1]) * np.sign(fv[1:]) < 0)[0]:
        u = brentq(f, ug[i], ug[i + 1], xtol=1e-15)
        gl = RHO * DT * g_const(u, 0.0)[1] - K
        out.append(f"u={u:.6f} L net={gl:+.2e} mu+={post(u, 0)[0]:.4f} tau6={tau(r, 6):.4f}")
    print(f"  r={r:.4f} PB-NS candidates: " + ("; ".join(out) if out else "none"))

print()
print("=" * 78)
print("4. c_H = 5: partial buys, no sales, with recruitment at + (H mixes, L abstains)")
print("=" * 78)


def u_jump(r, cH):
    t = tau(r, cH)
    return A * (2 * t - 1) / (D * (1 - t))


for r in np.round(np.arange(1.400, 1.4451, 0.0025), 6):
    DT = prims(r)[2]
    up = u_jump(r, 5.0)
    f = lambda u: DT * g_rec(u, 0.0)[0] - K
    if f(up) * f(1.0) < 0:
        u = brentq(f, up, 1.0, xtol=1e-15)
        gl = DT * g_rec(u, 0.0)[1] - K
        E = entry_prob(u, 0.0, (1.0, RHO, RHO))
        print(f"  r={r:.4f} u_jump={up:.6f} root u={u:.6f} L net={gl:+.3e} E={E:.6f}")
    else:
        print(f"  r={r:.4f} u_jump={up:.6f} no root in the recruited part of the edge")
r_lo = brentq(lambda r: prims(r)[2] * g_rec(u_jump(r, 5.0), 0.0)[0] - K, 1.40, 1.443)
print(f"  lower end: root meets the jump at r={r_lo:.6f}, u={u_jump(r_lo, 5.0):.6f};"
      f" upper end: BNS at r={rr(K / (ALPHA * BETA * (1 + RHO))):.6f}")
print(f"  entry at the ends: {entry_prob(u_jump(r_lo, 5.0), 0.0, (1.0, RHO, RHO)):.6f} and 0.625000")

print()
print("=" * 78)
print("5. Two end values quoted in the check memo (c_H = 6)")
print("=" * 78)
# Entry at the upper end of the recruited FB-PS branch: v = v_tau(r) at r = 1.532313.
r_up = 1.53231276342
t6 = tau(r_up, 6.0)
v_up = (1 - (1 - t6) / (A * t6)) / D
print(f"  recruited FB-PS upper end: r={r_up:.6f} v={v_up:.6f} E={entry_prob(1.0, v_up, (1.0, RHO, RHO)):.6f}")


# End of the constant-entry PB-FS branch: the mirror point (v, 1) reaches mu+ = tau.
def pbfs_gap(r):
    v = brentq(lambda t: RHO * prims(r)[2] * g_const(1.0, t)[1] - K, 1e-12, 0.6)
    return post(v, 1.0)[0] - tau(r, 6.0), v


r_pb = brentq(lambda r: pbfs_gap(r)[0], 1.8195, 1.8399)
print(f"  constant-entry PB-FS leaves the constant pattern at r={r_pb:.6f} (v={pbfs_gap(r_pb)[1]:.6f})")
