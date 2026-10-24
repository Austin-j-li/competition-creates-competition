"""C1 branches: edge roots, jump-mixing candidates, interior roots, ordering.

Print only. Double precision search. Challenger mixing at a jump means the
common entry rate e in [rho,1] at the threshold belief tau is chosen freely;
nets are affine in e, so required values are exact linear solves given mus.

Run: .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C1_two_sided/branches.py
"""
import math

h, ell, p, rho, k, b = 10.0, 1.0, 0.5, 0.25, 0.02, 2.0
a = math.exp(-1.0 / b)
d = 1.0 - a
alpha = a / (1 + a)
beta = 1.0 / (1 + a)
gamma = (1 - a) / (1 + a)
delta = a * a / (1 + a)
phi = a * (1 - a) / (1 + a)


def auction(r):
    gH = h - r / 2 - p * p / (2 * r)
    gL = (ell * ell - p * p) / (2 * r)
    DT = (r - ell) ** 2 / (2 * r)
    return gH, gL, DT


def mus(u, v):
    Ap = 1 + u * d / a
    Bp = 1 - v * d
    Am = 1 - u * d
    Bm = 1 + v * d / a
    return Ap / (Ap + Bp), Am / (Am + Bp), Am / (Am + Bm)


def gains_uv(u, v, DT, ep, e0, em):
    mup, mu0, mum = mus(u, v)
    gH = DT * (beta * ep * (1 - mup) + phi * e0 * (1 - mu0) + delta * em * (1 - mum))
    gL = DT * (delta * ep * mup + phi * e0 * mu0 + beta * em * mum)
    return gH, gL


def base_entry(u, v, tau):
    mup, mu0, mum = mus(u, v)
    return (1.0 if mup >= tau else rho, 1.0 if mu0 >= tau else rho,
            1.0 if mum >= tau else rho)


def outcome(u, v, ep, e0, em):
    pHp = (1 - u) * alpha + u * beta
    pH0 = (1 - u) * gamma + u * phi
    pHm = (1 - u) * alpha + u * delta
    pLp = (1 - v) * alpha + v * delta
    pL0 = (1 - v) * gamma + v * phi
    pLm = (1 - v) * alpha + v * beta
    E = 0.5 * (pHp * ep + pH0 * e0 + pHm * em + pLp * ep + pL0 * e0 + pLm * em)
    OH = 0.5 * (pHp * ep + pH0 * e0 + pHm * em)
    return E, OH


def mixing_at(u, v, tau, DT, label):
    """At a jump point, jumping regions share mu=tau. Vary common e."""
    mup, mu0, mum = mus(u, v)
    musv = [mup, mu0, mum]
    jump = [abs(x - tau) < 1e-8 for x in musv]
    fixed = [(1.0 if x > tau + 1e-8 else rho) for x in musv]

    def nets(e):
        es = [e if jump[i] else fixed[i] for i in range(3)]
        gHg, gLg = gains_uv(u, v, DT, es[0], es[1], es[2])
        return gHg - k, gLg - k, es

    nH_lo, nL_lo, _ = nets(rho)
    nH_hi, nL_hi, _ = nets(1.0)
    print(f"  {label} at (u,v)=({u:.10f},{v:.10f}) mus=({mup:.6f},{mu0:.6f},{mum:.6f}) "
          f"jump={jump} fixed={fixed}")
    print(f"    netH: e=rho {nH_lo:+.6e} -> e=1 {nH_hi:+.6e};  netL: {nL_lo:+.6e} -> {nL_hi:+.6e}")
    out = {}
    for who, lo, hi in [("H", nH_lo, nH_hi), ("L", nL_lo, nL_hi)]:
        if hi != lo:
            estar = rho + (0 - lo) * (1 - rho) / (hi - lo)
        else:
            estar = float("nan")
        out[who] = estar
        if rho - 1e-12 <= estar <= 1 + 1e-12:
            nH, nL, es = nets(estar)
            E, OH = outcome(u, v, es[0], es[1], es[2])
            print(f"    e* zeroing {who}: e={estar:.10f} (theta={(estar-rho)/(1-rho):.10f}) "
                  f"netH={nH:+.3e} netL={nL:+.3e} E={E:.8f} OH={OH:.8f}")
        else:
            print(f"    e* zeroing {who}: e={estar:.6f} outside [rho,1]")
    return out


def edge_jump_points(tau):
    """All edge jump points as (edge, t, (u,v))."""
    omt = 1 - tau
    res = []
    # u=1 vary v, mu+ and mu0
    for lab, A in [("mu+", 1 + d / a), ("mu0", 1 - d)]:
        vv = (1 - A * omt / tau) / d if tau > 0 else -1
        if 0 < vv < 1:
            res.append((f"u=1 {lab}", vv, (1.0, vv)))
    # u=0 vary v, mu+=mu0 (single point)
    vv = (1 - omt / tau) / d if tau > 0 else -1
    if 0 < vv < 1:
        res.append(("u=0 mu+=mu0", vv, (0.0, vv)))
    # v=1 vary u
    Bp = 1 - d
    uu = (tau * Bp / omt - 1) * a / d if omt > 0 else -1
    if 0 < uu < 1:
        res.append(("v=1 mu+", uu, (uu, 1.0)))
    uu0 = (1 - tau * Bp / omt) / d if omt > 0 else -1
    if 0 < uu0 < 1:
        res.append(("v=1 mu0", uu0, (uu0, 1.0)))
    # v=0 vary u
    uu = (tau / omt - 1) * a / d if omt > 0 else -1
    if 0 < uu < 1:
        res.append(("v=0 mu+", uu, (uu, 0.0)))
    uu0 = (1 - tau / omt) / d if omt > 0 else -1
    if 0 < uu0 < 1:
        res.append(("v=0 mu0", uu0, (uu0, 0.0)))
    return res


def interior_search(r, cH, tau, DT):
    """Grid + Newton (finite differences) for NH=NL=0 inside each cell."""
    print(" Interior cell search (Newton from grid starts, residuals printed):")
    starts = [(i / 10, j / 10) for i in range(1, 10) for j in range(1, 10)]
    found = []
    for (u0, v0) in starts:
        ep, e0, em = base_entry(u0, v0, tau)
        u, v = u0, v0
        ok = True
        for _ in range(50):
            gHg, gLg = gains_uv(u, v, DT, ep, e0, em)
            F = [gHg - k, gLg - k]
            if max(abs(F[0]), abs(F[1])) < 1e-13:
                break
            hh = 1e-7
            g1 = gains_uv(u + hh, v, DT, ep, e0, em)
            g2 = gains_uv(u, v + hh, DT, ep, e0, em)
            J = [[(g1[0] - gHg) / hh, (g2[0] - gHg) / hh],
                 [(g1[1] - gLg) / hh, (g2[1] - gLg) / hh]]
            det = J[0][0] * J[1][1] - J[0][1] * J[1][0]
            if abs(det) < 1e-14:
                ok = False
                break
            du = (-F[0] * J[1][1] + F[1] * J[0][1]) / det
            dv = (-J[0][0] * F[1] + J[1][0] * F[0]) / det
            u, v = u + du, v + dv
            if not (0 < u < 1 and 0 < v < 1):
                ok = False
                break
        if not ok:
            continue
        gHg, gLg = gains_uv(u, v, DT, ep, e0, em)
        if max(abs(gHg - k), abs(gLg - k)) > 1e-9:
            continue
        # verify the fixed entry pattern matches the point (strictly inside cell)
        ep2, e02, em2 = base_entry(u, v, tau)
        mup, mu0, mum = mus(u, v)
        near_jump = min(abs(mup - tau), abs(mu0 - tau), abs(mum - tau)) < 1e-6
        key = (round(u, 6), round(v, 6), ep, e0, em)
        if key in [(round(x[0], 6), round(x[1], 6), x[2], x[3], x[4]) for x in found]:
            continue
        found.append((u, v, ep, e0, em))
        E, OH = outcome(u, v, ep, e0, em)
        print(f"   start ({u0},{v0}) -> (u,v)=({u:.10f},{v:.10f}) e=({ep:.2f},{e0:.2f},{em:.2f}) "
              f"pattern-match={(ep2, e02, em2) == (ep, e0, em)} near-jump={near_jump} "
              f"netH={gHg-k:+.3e} netL={gLg-k:+.3e} E={E:.8f} OH={OH:.8f}")
    if not found:
        print("   no interior cell root found from 81 starts (diagnostic, not a proof)")


def jump_curve_scan(r, cH, tau, DT):
    """Scan line mu+=tau: v as affine function of u. Print e*_H - e*_L."""
    omt = 1 - tau
    print(" Jump-curve mu+=tau scan (interior both-zero needs e*_H == e*_L):")
    def v_of_u(u):
        return (1 - (1 + u * d / a) * omt / tau) / d
    us = [i / 20 for i in range(21)]
    prev = None
    for u in us:
        v = v_of_u(u)
        if not (0 <= v <= 1):
            continue
        # jumping region is + (mu0 jumps too only at u=0 endpoint)
        mup, mu0, mum = mus(u, v)
        e0 = 1.0 if mu0 > tau + 1e-9 else rho
        em = 1.0 if mum > tau + 1e-9 else rho
        def nets(e):
            gHg, gLg = gains_uv(u, v, DT, e, e0, em)
            return gHg - k, gLg - k
        nHlo, nLlo = nets(rho)
        nHhi, nLhi = nets(1.0)
        eH = rho - nHlo * (1 - rho) / (nHhi - nHlo) if nHhi != nHlo else float("nan")
        eL = rho - nLlo * (1 - rho) / (nLhi - nLlo) if nLhi != nLlo else float("nan")
        print(f"   u={u:.2f} v={v:.6f} mu0={mu0:.6f} e0={e0:.2f} e*_H={eH:.6f} e*_L={eL:.6f} diff={eH-eL:+.6f}")
        if prev is not None and (prev[1] - prev[2]) * (eH - eL) < 0:
            print(f"   *** sign change of e*_H-e*_L between u={prev[0]} and u={u}: interior candidate bracket ***")
        prev = (u, eH, eL)


def analyse(r, cH):
    gH, gL, DT = auction(r)
    tau = (cH - gL) / (gH - gL)
    print(f"\n########## r={r} cH={cH} DT={DT:.8f} tau={tau:.8f} k/DT={k/DT:.8f} ##########")
    for (u, v, nm) in [(0, 0, "NT"), (1, 1, "T"), (1, 0, "BNS"), (0, 1, "SNB")]:
        ep, e0, em = base_entry(u, v, tau)
        gHg, gLg = gains_uv(u, v, DT, ep, e0, em)
        E, OH = outcome(u, v, ep, e0, em)
        print(f" {nm}({u},{v}): netH={gHg-k:+.6e} netL={gLg-k:+.6e} E={E:.6f} OH={OH:.6f}")
    print(" Edge jump-mixing candidates:")
    for lab, t, (u, v) in edge_jump_points(tau):
        mixing_at(u, v, tau, DT, lab)
    interior_search(r, cH, tau, DT)
    jump_curve_scan(r, cH, tau, DT)


for cH in [5.0, 6.0]:
    for r in [1.4, 1.525, 1.55, 1.65, 1.9]:
        analyse(r, cH)

print("\n\n===== Gain coefficients at constant entry rho over grid (max location) =====")
NG = 41
for ep, e0, em, lab in [(rho, rho, rho, "e=(rho,rho,rho)"), (1.0, rho, rho, "e=(1,rho,rho)"),
                        (1.0, 1.0, rho, "e=(1,1,rho)")]:
    mxH = mxL = -1
    mnH = mnL = 1e9
    aMxH = aMxL = aMnH = aMnL = None
    for iu in range(NG):
        for iv in range(NG):
            u, v = iu / (NG - 1), iv / (NG - 1)
            gHg, gLg = gains_uv(u, v, 1.0, ep, e0, em)  # DT=1: coefficients
            if gHg > mxH:
                mxH, aMxH = gHg, (u, v)
            if gLg > mxL:
                mxL, aMxL = gLg, (u, v)
            if gHg < mnH:
                mnH, aMnH = gHg, (u, v)
            if gLg < mnL:
                mnL, aMnL = gLg, (u, v)
    print(f" {lab}: coeffH in [{mnH:.8f} at {aMnH}, {mxH:.8f} at {aMxH}]; "
          f"coeffL in [{mnL:.8f} at {aMnL}, {mxL:.8f} at {aMxL}]")

print("\n\n===== Asymmetric branch values =====")
print("cH=6, edge u=1 jump v*(r) with challenger mixing (L indifferent):")
for r in [1.52, 1.55, 1.6, 1.65, 1.7, 1.74, 1.9, 2.5, 3.0]:
    gH, gL, DT = auction(r)
    tau = (6.0 - gL) / (gH - gL)
    omt = 1 - tau
    vv = (1 - (1 + d / a) * omt / tau) / d
    print(f" r={r}: tau={tau:.6f} v*={vv:.6f} (in (0,1): {0 < vv < 1})")
    if 0 < vv < 1:
        mixing_at(1.0, vv, tau, DT, "u=1 mu+")
print("\ncH=5, edge v=0 jump u_p(r) with challenger mixing (H indifferent):")
for r in [1.4, 1.52, 1.55, 1.6, 1.65, 1.7, 1.9]:
    gH, gL, DT = auction(r)
    tau = (5.0 - gL) / (gH - gL)
    omt = 1 - tau
    uu = (tau / omt - 1) * a / d
    print(f" r={r}: tau={tau:.6f} u_p={uu:.6f} (in (0,1): {0 < uu < 1})")
    if 0 < uu < 1:
        mixing_at(uu, 0.0, tau, DT, "v=0 mu+")
print("\ncH=5, baseline edge root (1,v) in recruitment cell: coeffL(1,v) vs k/DT")
for r in [1.51, 1.52, 1.525, 1.53, 1.54, 1.55]:
    gH, gL, DT = auction(r)
    tau = (5.0 - gL) / (gH - gL)
    vals = []
    for v in [0.0, 0.25, 0.5, 0.75, 1.0]:
        ep, e0, em = base_entry(1.0, v, tau)
        gHg, gLg = gains_uv(1.0, v, DT, ep, e0, em)
        vals.append(f"v={v}:netL={gLg-k:+.2e},netH={gHg-k:+.2e}")
    print(f" r={r} k/DT={k/DT:.6f}: " + " | ".join(vals))
    # bisect netL on [0,1] with fixed pattern (1,rho,rho) (valid on this edge for cH=5 near r)
    def netL1(v):
        gHg, gLg = gains_uv(1.0, v, DT, 1.0, rho, rho)
        return gLg - k
    f0, f1 = netL1(0.0), netL1(1.0)
    if f0 * f1 < 0:
        lo, hi, flo = 0.0, 1.0, f0
        for _ in range(80):
            mid = (lo + hi) / 2
            fm = netL1(mid)
            if (fm > 0) == (flo > 0):
                lo, flo = mid, fm
            else:
                hi = mid
        vv = (lo + hi) / 2
        gHg, gLg = gains_uv(1.0, vv, DT, 1.0, rho, rho)
        E, OH = outcome(1.0, vv, 1.0, rho, rho)
        print(f"   BASELINE ROOT v={vv:.10f} netH={gHg-k:+.3e} netL={gLg-k:+.3e} E={E:.8f} OH={OH:.8f}")
    else:
        print(f"   no baseline root on u=1 (netL ends {f0:+.3e}, {f1:+.3e})")
