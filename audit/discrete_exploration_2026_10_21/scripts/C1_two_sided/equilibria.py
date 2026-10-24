"""C1 equilibrium finder for two-sided discrete-Laplace. Print only.

Double precision for search; headline values are recomputed in posteriors.py
at 50 digits. Entry uses the baseline tie rule (prepare at indifference).
Jumps at mu=tau are handled by splitting each edge at the exact linear
threshold and by reporting left/right limits. Challenger-mixing points at a
jump are reported separately.

Run: .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C1_two_sided/equilibria.py
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
    return Ap / (Ap + Bp), Am / (Am + Bp), Am / (Am + Bm), Ap, Bp, Am, Bm


def entry_rates(u, v, tau, eplus_override=None, e0_override=None):
    mup, mu0, mum, *_ = mus(u, v)
    ep = 1.0 if mup >= tau else rho
    e0 = 1.0 if mu0 >= tau else rho
    em = 1.0 if mum >= tau else rho
    if eplus_override is not None:
        ep = eplus_override
    if e0_override is not None:
        e0 = e0_override
    return ep, e0, em


def gains(u, v, tau, DT, ep=None, e0=None, em=None):
    mup, mu0, mum, Ap, Bp, Am, Bm = mus(u, v)
    if ep is None:
        ep, e0, em = entry_rates(u, v, tau)
    gH = DT * (beta * ep * (1 - mup) + phi * e0 * (1 - mu0) + delta * em * (1 - mum))
    gL = DT * (delta * ep * mup + phi * e0 * mu0 + beta * em * mum)
    return gH, gL


def entry_outcome(u, v, tau, ep=None, e0=None, em=None):
    if ep is None:
        ep, e0, em = entry_rates(u, v, tau)
    pHp = (1 - u) * alpha + u * beta
    pH0 = (1 - u) * gamma + u * phi
    pHm = (1 - u) * alpha + u * delta
    pLp = (1 - v) * alpha + v * delta
    pL0 = (1 - v) * gamma + v * phi
    pLm = (1 - v) * alpha + v * beta
    E = 0.5 * (pHp * ep + pH0 * e0 + pHm * em + pLp * ep + pL0 * e0 + pLm * em)
    OH = 0.5 * (pHp * ep + pH0 * e0 + pHm * em)
    Pp = 0.5 * (pHp + pLp)
    return E, OH, Pp


def jump_points_edge(edge, tau):
    """Exact v (or u) in (0,1) where mu+ or mu0 equals tau along an edge.

    edge: ('u1', vary v), ('u0', vary v), ('v1', vary u), ('v0', vary u).
    Returns sorted list of (point, label).
    """
    pts = []
    omt = 1 - tau
    if edge == "u1":  # u=1, vary v: mu+: Ap*omt = tau*(1-v d); mu0: Am*omt = tau*(1-v d)
        Ap = 1 + d / a
        Am = 1 - d
        for lab, A in [("mu+", Ap), ("mu0", Am)]:
            if tau > 0:
                vv = (1 - A * omt / tau) / d
                if 0 < vv < 1:
                    pts.append((vv, lab))
    elif edge == "u0":  # u=0, vary v: Ap=1, Am=1
        for lab in ["mu+", "mu0"]:
            vv = (1 - omt / tau) / d if tau > 0 else -1
            if 0 < vv < 1:
                pts.append((vv, lab))
    elif edge == "v1":  # v=1, vary u: mu+: (1+u d/a)omt = tau*Bp, Bp=1-d=a; mu0: (1-u d)omt = tau*a
        Bp = 1 - d
        uu = (tau * Bp / omt - 1) * a / d if omt > 0 else -1
        if 0 < uu < 1:
            pts.append((uu, "mu+"))
        uu0 = (1 - tau * Bp / omt) / d if omt > 0 else -1
        if 0 < uu0 < 1:
            pts.append((uu0, "mu0"))
    elif edge == "v0":  # v=0, vary u: Bp=1
        uu = (tau / omt - 1) * a / d if omt > 0 else -1
        if 0 < uu < 1:
            pts.append((uu, "mu+"))
        uu0 = (1 - tau / omt) / d if omt > 0 else -1
        if 0 < uu0 < 1:
            pts.append((uu0, "mu0"))
    pts.sort()
    return pts


def bisect(func, lo, hi, flo, fhi, iters=80):
    for _ in range(iters):
        mid = (lo + hi) / 2
        fm = func(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi, fhi = mid, fm
    return (lo + hi) / 2


def analyse(r, cH):
    gH, gL, DT = auction(r)
    tau = (cH - gL) / (gH - gL)
    print(f"\n===== r={r} cH={cH} DT={DT:.10f} gL={gL:.10f} gH={gH:.10f} tau={tau:.10f} k/DT={k/DT:.10f} =====")
    print("Corners (netH=gH-k, netL=gL-k; entry pattern ep,e0,em):")
    for (u, v, name) in [(0, 0, "NT(0,0)"), (1, 1, "T(1,1)"), (1, 0, "BNS(1,0)"), (0, 1, "SNB(0,1)")]:
        gHg, gLg = gains(u, v, tau, DT)
        ep, e0, em = entry_rates(u, v, tau)
        mup, mu0, mum, *_ = mus(u, v)
        E, OH, Pp = entry_outcome(u, v, tau)
        okH = (gHg - k <= 1e-12) if u == 0 else (gHg - k >= -1e-12)
        okL = (gLg - k <= 1e-12) if v == 0 else (gLg - k >= -1e-12)
        print(f" {name}: mus=({mup:.6f},{mu0:.6f},{mum:.6f}) e=({ep:.2f},{e0:.2f},{em:.2f}) "
              f"netH={gHg-k:+.8f} netL={gLg-k:+.8f} E={E:.8f} OH={OH:.8f} P+={Pp:.6f} "
              f"equilibrium(conventional)={okH and okL}")
    # Edges
    edges = [
        ("u1", "edge u=1, v in (0,1): need netL=0, netH>=0", lambda t: (1.0, t), "L"),
        ("u0", "edge u=0, v in (0,1): need netL=0, netH<=0", lambda t: (0.0, t), "L"),
        ("v1", "edge v=1, u in (0,1): need netH=0, netL>=0", lambda t: (t, 1.0), "H"),
        ("v0", "edge v=0, u in (0,1): need netH=0, netL<=0", lambda t: (t, 0.0), "H"),
    ]
    for code, label, point, who in edges:
        jumps = jump_points_edge(code, tau)
        print(f" {label}. Jump points: {[(round(x, 10), s) for x, s in jumps]}")
        bounds = [0.0] + [x for x, _ in jumps] + [1.0]
        for si in range(len(bounds) - 1):
            lo, hi = bounds[si], bounds[si + 1]
            if hi - lo < 1e-12:
                continue
            # sample inside segment to fix entry pattern, then scan for sign change
            mid = (lo + hi) / 2
            um, vm = point(mid)
            ep, e0, em = entry_rates(um, vm, tau)
            def netfun(t, ep=ep, e0=e0, em=em, point=point, who=who):
                uu, vv = point(t)
                gHg, gLg = gains(uu, vv, tau, DT, ep, e0, em)
                return (gHg - k) if who == "H" else (gLg - k)
            N = 400
            roots = []
            prev_t, prev_f = lo + (hi - lo) * 1e-9, netfun(lo + (hi - lo) * 1e-9)
            for i in range(1, N + 1):
                t = lo + (hi - lo) * i / N * (1 - 1e-9) if i == N else lo + (hi - lo) * i / N
                fv = netfun(t)
                if prev_f == 0.0:
                    roots.append(prev_t)
                elif fv != 0.0 and (fv > 0) != (prev_f > 0):
                    roots.append(bisect(netfun, prev_t, t, prev_f, fv))
                prev_t, prev_f = t, fv
            for rt in roots:
                uu, vv = point(rt)
                gHg, gLg = gains(uu, vv, tau, DT, ep, e0, em)
                E, OH, Pp = entry_outcome(uu, vv, tau, ep, e0, em)
                mup, mu0, mum, *_ = mus(uu, vv)
                print(f"   ROOT segment ({lo:.6f},{hi:.6f}) e=({ep:.2f},{e0:.2f},{em:.2f}): "
                      f"(u,v)=({uu:.10f},{vv:.10f}) netH={gHg-k:+.3e} netL={gLg-k:+.3e} "
                      f"mus=({mup:.6f},{mu0:.6f},{mum:.6f}) E={E:.8f} OH={OH:.8f}")
            if not roots:
                flo = netfun(lo + (hi - lo) * 1e-7)
                fhi = netfun(hi - (hi - lo) * 1e-7)
                print(f"   segment ({lo:.6f},{hi:.6f}) e=({ep:.2f},{e0:.2f},{em:.2f}): no sign change; "
                      f"net({who}) near ends = {flo:+.3e}, {fhi:+.3e}")
        # Jump limits: challenger-mixing candidates
        for (jx, lab) in jumps:
            for side, tt in [("left", jx - 1e-9), ("right", jx + 1e-9), ("at(tie e=1)", jx)]:
                uu, vv = point(tt)
                gHg, gLg = gains(uu, vv, tau, DT)
                ep, e0, em = entry_rates(uu, vv, tau)
                print(f"   JUMP {lab} at {jx:.10f} {side}: e=({ep:.2f},{e0:.2f},{em:.2f}) "
                      f"netH={gHg-k:+.3e} netL={gLg-k:+.3e}")
    # Diagonal and global grid summary
    print(" Diagonal s=u=v (netH, netL):")
    for s in [0.0, 0.25, 0.5, 0.75, 1.0]:
        gHg, gLg = gains(s, s, tau, DT)
        ep, e0, em = entry_rates(s, s, tau)
        print(f"   s={s}: netH={gHg-k:+.8f} netL={gLg-k:+.8f} diffH-L={gHg-gLg:+.3e} e=({ep:.2f},{e0:.2f},{em:.2f})")
    # Grid min/max of nets (diagnostic for uniqueness bounds)
    NG = 81
    minH, maxH, minL, maxL = 1e9, -1e9, 1e9, -1e9
    argminH = argmaxH = argminL = argmaxL = None
    interior_flags = []
    for iu in range(NG):
        for iv in range(NG):
            u, v = iu / (NG - 1), iv / (NG - 1)
            gHg, gLg = gains(u, v, tau, DT)
            if gHg - k < minH:
                minH, argminH = gHg - k, (u, v)
            if gHg - k > maxH:
                maxH, argmaxH = gHg - k, (u, v)
            if gLg - k < minL:
                minL, argminL = gLg - k, (u, v)
            if gLg - k > maxL:
                maxL, argmaxL = gLg - k, (u, v)
    print(f" Grid {NG}x{NG} netH range [{minH:+.8f} at {argminH}, {maxH:+.8f} at {argmaxH}]")
    print(f" Grid {NG}x{NG} netL range [{minL:+.8f} at {argminL}, {maxL:+.8f} at {argmaxL}]")
    print(f" Analytic bounds: gross in [rho*m*DT, DT] = [{rho*0.2689414213699951*DT:.8f}, {DT:.8f}]; k={k}")


for cH in [5.0, 6.0]:
    for r in [1.2, 1.55, 1.6, 1.65, 3.0, 3.6]:
        analyse(r, cH)
