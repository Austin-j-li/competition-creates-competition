"""Independent checks of the theory track's regime II claims (referee track).

Nothing here imports the theory, numerics, or adversary code. Every function is pure and takes the
parameter record first. Payoffs come from the closed forms of the second-price auction with reserve p
and incumbent value R ~ U[0, r]:
    g_L = (ell^2 - p^2) / (2r),  g_H = h - (r^2 + p^2) / (2r),  Delta_T = (r - ell)^2 / (2r).
Investor payoffs are computed by adaptive quadrature from the residuals of Lemma CD.2(d); they never use
the exponential shortcut of R.10(a). Status of every number: numerical diagnostic (double precision).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, replace

import numpy as np
from scipy import integrate, optimize


@dataclass(frozen=True)
class Prm:
    h: float = 10.0
    ell: float = 1.0
    p: float = 0.5
    b: float = 2.0
    k: float = 0.02
    rho: float = 0.25
    cL: float = 3.0
    cH: float = 6.0
    r: float = 3.0


@dataclass(frozen=True)
class Lev:
    gL: float
    gH: float
    DT: float
    m: float
    M: float
    tauL: float
    tauH: float


def lev(P: Prm, r: float | None = None) -> Lev:
    r = P.r if r is None else r
    gL = (P.ell ** 2 - P.p ** 2) / (2 * r)
    gH = P.h - (r * r + P.p ** 2) / (2 * r)
    DT = (r - P.ell) ** 2 / (2 * r)
    m = 1.0 / (1.0 + math.exp(2.0 / P.b))
    return Lev(gL, gH, DT, m, 1 - m, (P.cL - gL) / (gH - gL), (P.cH - gL) / (gH - gL))


def Bmu(P: Prm, mu: float, r: float | None = None) -> float:
    L = lev(P, r)
    return L.gL + mu * (L.gH - L.gL)


def F(P: Prm, z: float) -> float:
    return 0.5 * math.exp(z / P.b) if z <= 0 else 1 - 0.5 * math.exp(-z / P.b)


def S(P: Prm, z: float) -> float:
    return 1 - F(P, z)


def f(P: Prm, z: float) -> float:
    return math.exp(-abs(z) / P.b) / (2 * P.b)


def logit(u: float) -> float:
    return math.log(u / (1 - u))


# ------------------------------------------------------------------ full orders
def mu_full(P: Prm, x: float) -> float:
    return 1.0 / (1.0 + math.exp(-(abs(x + 1) - abs(x - 1)) / P.b))


def mubar_full(P: Prm, xp: float) -> float:
    a, c = F(P, xp - 1), F(P, xp + 1)
    return a / (a + c)


def xbar(P: Prm) -> float:
    L = lev(P)
    return optimize.brentq(lambda x: mubar_full(P, x) - L.tauL, -1 + 1e-12, 60.0, xtol=1e-14)


def K_forcing(P: Prm) -> float:
    L = lev(P)
    xb = xbar(P)
    return (1 - 1 / P.b) * P.rho * L.DT * min(L.tauL * S(P, xb + 1), L.m * S(P, xb))


def bathtub(P: Prm, which: str = "E", n: int = 400000, hi: float = 60.0) -> dict:
    """Fractional knapsack on a fine cell grid of [z0, hi): sup of removed value s.t. Gamma < B0.

    Cells are sorted by cost per unit value; fractional last cell. Independent of the closed form.
    """
    L = lev(P)
    z0 = (P.b / 2) * logit(L.tauL)
    xs = np.linspace(z0, hi, n + 1)
    xm = 0.5 * (xs[:-1] + xs[1:])
    dx = np.diff(xs)
    fH = np.exp(-np.abs(xm - 1) / P.b) / (2 * P.b)
    fL = np.exp(-np.abs(xm + 1) / P.b) / (2 * P.b)
    dens = 0.5 * (fH + fL)
    mu = fH / (fH + fL)
    phi = P.rho * (mu >= L.tauL) + (1 - P.rho) * (mu >= L.tauH)
    cost = (mu - L.tauL) * dens * dx
    if which == "E":
        val = phi * dens * dx
    else:
        val = phi * fH * dx
    B0 = 0.5 * (L.tauL * F(P, z0 + 1) - (1 - L.tauL) * F(P, z0 - 1))
    ratio = cost / np.maximum(val, 1e-300)
    order = np.argsort(ratio, kind="stable")
    cc = np.cumsum(cost[order])
    vv = np.cumsum(val[order])
    j = int(np.searchsorted(cc, B0))
    prev_c = cc[j - 1] if j > 0 else 0.0
    prev_v = vv[j - 1] if j > 0 else 0.0
    frac = (B0 - prev_c) / cost[order][j]
    V = prev_v + frac * val[order][j]
    xstar = (P.b / 2) * logit(L.tauH)
    a = 0.5 * (S(P, xstar - 1) + S(P, xstar + 1))
    if which == "E":
        base = P.rho * 0.5 * (S(P, z0 - 1) + S(P, z0 + 1)) + (1 - P.rho) * a
    else:
        base = P.rho * S(P, z0 - 1) + (1 - P.rho) * S(P, xstar - 1)
    return {"z0": z0, "B0": B0, "base": base, "V": V, "inf": base - V}


def halfline_thresholds(P: Prm) -> dict:
    """R.9: x' where E = S_X(x') = rho and e_H = S(x'-1) = rho; c_L thresholds B(mubar(x'))."""
    SX = lambda x: 0.5 * (S(P, x - 1) + S(P, x + 1))  # noqa: E731
    xE = optimize.brentq(lambda x: SX(x) - P.rho, -5, 80)
    xO = optimize.brentq(lambda x: S(P, x - 1) - P.rho, -5, 80)
    L = lev(P)
    xk = 1 + P.b * math.log((1 - 1 / P.b) * L.m * L.DT / (2 * P.k))
    return {"xE": xE, "xO": xO, "xk": xk, "cE": Bmu(P, mubar_full(P, xE)), "cO": Bmu(P, mubar_full(P, xO)),
            "a3_right": (1 - 1 / P.b) * P.rho * L.m * L.DT}


# ------------------------------------------------------------------ general pure orders, half-line pool
def mu_pure(P: Prm, x: float, qH: float, qL: float) -> float:
    a, c = f(P, x - qH), f(P, x - qL)
    return a / (a + c)


def pool_belief(P: Prm, xp: float, qH: float, qL: float) -> float:
    a, c = F(P, xp - qH), F(P, xp - qL)
    return a / (a + c)


def entry(P: Prm, mu: float) -> float:
    L = lev(P)
    return P.rho * (mu >= L.tauL) + (1 - P.rho) * (mu >= L.tauH)


def gross(P: Prm, theta: str, s: float, qH: float, qL: float, xp: float, hi: float = 80.0) -> float:
    """F_theta(s) = int f(x -+ s) A_theta(x) dx over the entry set [xp, inf), by adaptive quadrature."""
    L = lev(P)
    shift = s if theta == "H" else -s

    def A(x: float) -> float:
        mu = mu_pure(P, x, qH, qL)
        e = entry(P, mu)
        return e * L.DT * ((1 - mu) if theta == "H" else mu)

    pts = sorted({xp, shift, qH, qL})
    # entry jumps where mu crosses tauL or tauH
    for tau in (L.tauL, L.tauH):
        g = lambda x: mu_pure(P, x, qH, qL) - tau  # noqa: E731
        lo_, hi_ = qL - 0.0, qH + 0.0
        if lo_ < hi_ and g(lo_) < 0 < g(hi_):
            pts.append(optimize.brentq(g, lo_, hi_, xtol=1e-14))
    cuts = [xp] + sorted(x for x in pts if xp < x < hi) + [hi]
    tot = 0.0
    for a, c in zip(cuts[:-1], cuts[1:]):
        val, _ = integrate.quad(lambda x: f(P, x - shift) * A(x), a, c, epsabs=1e-14, epsrel=1e-12, limit=400)
        tot += val
    return tot


def U(P: Prm, theta: str, s: float, qH: float, qL: float, xp: float) -> float:
    return s * gross(P, theta, s, qH, qL, xp) - P.k * s


def best_response(P: Prm, theta: str, qH: float, qL: float, xp: float, n: int = 201) -> tuple[float, float]:
    grid = np.linspace(0.0, 1.0, n)
    vals = np.array([U(P, theta, s, qH, qL, xp) for s in grid])
    i = int(np.argmax(vals))
    lo, hi = grid[max(i - 1, 0)], grid[min(i + 1, n - 1)]
    res = optimize.minimize_scalar(lambda s: -U(P, theta, s, qH, qL, xp), bounds=(lo, hi), method="bounded",
                                   options={"xatol": 1e-10})
    if -res.fun > vals[i]:
        return float(res.x), float(-res.fun)
    return float(grid[i]), float(vals[i])


# ------------------------------------------------------------------ starved family (R.10)
def CL_quad(P: Prm, v: float, xp: float) -> float:
    """C_L(v, x') = rho Delta_T int_{x'}^inf e^{-x/b}/(2b) mu_X dx, by quadrature."""
    L = lev(P)
    val, _ = integrate.quad(lambda x: math.exp(-x / P.b) / (2 * P.b) * mu_pure(P, x, 1.0, -v), xp, xp + 80,
                            epsabs=1e-15, epsrel=1e-12, limit=400, points=[1.0] if xp < 1 else None)
    return P.rho * L.DT * val


def starved_xp(P: Prm, v: float) -> float | None:
    """x' >= 0 solving the low type's FOC C_L(v,x') e^{-v/b}(1 - v/b) = k; None if no root on [0, 30]."""
    g = lambda x: CL_quad(P, v, x) * math.exp(-v / P.b) * (1 - v / P.b) - P.k  # noqa: E731
    if g(0.0) < 0:
        return None
    if g(30.0) > 0:
        return None
    return optimize.brentq(g, 0.0, 30.0, xtol=1e-13)


def vH(P: Prm) -> float:
    return P.b * logit(lev(P).tauH) - 1


def starved_check(P: Prm, v: float) -> dict:
    """Build the R.10 member at short v and check every condition with independent quadrature."""
    L = lev(P)
    xp = starved_xp(P, v)
    if xp is None:
        return {"v": v, "xp": math.nan, "ok": False}
    pb = pool_belief(P, xp, 1.0, -v)
    edge = mu_pure(P, xp, 1.0, -v)
    sH, uH = best_response(P, "H", 1.0, -v, xp)
    sL, uL = best_response(P, "L", 1.0, -v, xp)
    UH1 = U(P, "H", 1.0, 1.0, -v, xp)
    ULv = U(P, "L", v, 1.0, -v, xp)
    E = P.rho * 0.5 * (S(P, xp - 1) + S(P, xp + v))
    eH = P.rho * S(P, xp - 1)
    ok = (pb < L.tauL) and (edge >= L.tauL) and (v < vH(P)) and (uH - UH1 < 1e-8) and (uL - ULv < 1e-8)
    return {"v": v, "xp": xp, "pool_belief": pb, "edge_belief": edge, "tauL": L.tauL, "vH": vH(P),
            "brH": sH, "regretH": uH - UH1, "brL": sL, "regretL": uL - ULv, "UH1": UH1,
            "UH1_identity": P.k * v / (P.b - v), "E": E, "OH": eH / 2, "ok": ok}


# ------------------------------------------------------------------ random test of R.5 and R.6 (mixed orders, island pools)
def random_forcing_test(P: Prm, n_draws: int = 400, seed: int = 11, k_scale: float = 1.0) -> dict:
    """Draw mixed order laws and island pools that satisfy the equilibrium pool conditions.

    For each consistent draw: check the five R.5 bounds, and check that U_theta is strictly increasing on [0,1]
    at k = k_scale * K(c_L) (R.6 needs k <= K). Grid quadrature on [-40, 40], step 0.002.
    """
    rng = np.random.default_rng(seed)
    L = lev(P)
    xb = xbar(P)
    K = K_forcing(P)
    k = k_scale * K
    xs = np.arange(-40.0, 40.0, 0.002)
    dx = 0.002
    lap = lambda z: np.exp(-np.abs(z) / P.b) / (2 * P.b)  # noqa: E731
    sgrid = np.linspace(0.0, 1.0, 51)
    out = {"draws": 0, "consistent": 0, "R5_viol": 0, "R5_max_excess": -1.0, "R6_viol": 0, "min_dU": 1e9,
           "K": K, "k": k}
    for _ in range(n_draws):
        out["draws"] += 1
        nH, nL = rng.integers(1, 4), rng.integers(1, 4)
        qH = rng.uniform(0, 1, nH)
        qL = -rng.uniform(0, 1, nL)
        if rng.uniform() < 0.6:
            qH[0] = 1.0
        if rng.uniform() < 0.6:
            qL[0] = -1.0
        wH = rng.dirichlet(np.ones(nH))
        wL = rng.dirichlet(np.ones(nL))
        aH = sum(w * lap(xs - q) for q, w in zip(qH, wH))
        aL = sum(w * lap(xs - q) for q, w in zip(qL, wL))
        mu = aH / (aH + aL)
        Z0 = mu < L.tauL
        N = Z0.copy()
        if rng.uniform() < 0.7:
            N |= xs < rng.uniform(-1.5, xb + 0.5)
        # add random voluntary intervals
        for _j in range(rng.integers(0, 4)):
            c = rng.uniform(-3, 5)
            w = rng.uniform(0.05, 1.5)
            N |= (xs >= c) & (xs < c + w)
        if rng.uniform() < 0.3:
            N |= xs >= rng.uniform(1, 8)
        uH = np.sum(aH[N]) * dx
        uL = np.sum(aL[N]) * dx
        if uH + uL <= 1e-12:
            continue
        if uH / (uH + uL) >= L.tauL:
            continue
        out["consistent"] += 1
        A = ~N
        e = np.where(A, P.rho * (mu >= L.tauL) + (1 - P.rho) * (mu >= L.tauH), 0.0)
        AH = e * L.DT * (1 - mu)
        AL = e * L.DT * mu
        bounds = [(uH, F(P, xb - 1)), (uL, F(P, xb + 1)), (0.5 * (uH + uL), 0.5 * (F(P, xb - 1) + F(P, xb + 1)))]
        for s in sgrid:
            bounds.append((np.sum(lap(xs - s)[N]) * dx, F(P, xb)))
            bounds.append((np.sum(lap(xs + s)[N]) * dx, F(P, xb + s)))
        exc = max(a - b_ for a, b_ in bounds)
        out["R5_max_excess"] = max(out["R5_max_excess"], exc)
        if exc > 1e-6:
            out["R5_viol"] += 1
        UH = np.array([s * np.sum(lap(xs - s) * AH) * dx - k * s for s in sgrid])
        UL = np.array([s * np.sum(lap(xs + s) * AL) * dx - k * s for s in sgrid])
        dU = min(np.min(np.diff(UH)), np.min(np.diff(UL)))
        out["min_dU"] = min(out["min_dU"], dU)
        if dU <= 0:
            out["R6_viol"] += 1
    return out


def partial_member(P: Prm, xp: float, v0: float = 0.7, iters: int = 60) -> dict:
    """Orders (1, -v) with a half-line cutoff xp (the forced pool is added by the entry rule).

    The low type's order is found by best-response iteration; then both types are checked. The pool is
    (-inf, max(xp, z0(v))) where mu(z0) = tauL; its belief is computed on that set.
    """
    L = lev(P)
    v = v0
    for _ in range(iters):
        s, _u = best_response(P, "L", 1.0, -v, xp, n=101)
        if abs(s - v) < 1e-9:
            break
        v = 0.5 * (v + s)
    g = lambda x: mu_pure(P, x, 1.0, -v) - L.tauL  # noqa: E731
    z0 = optimize.brentq(g, -v - 1e-9, 1 + 1e-9) if g(-v - 1e-9) < 0 < g(1 + 1e-9) else -math.inf
    cut = max(xp, z0)
    sH, uH = best_response(P, "H", 1.0, -v, xp, n=401)
    sL, uL = best_response(P, "L", 1.0, -v, xp, n=401)
    xs_star = None
    E = P.rho * 0.5 * (S(P, cut - 1) + S(P, cut + v))
    big = 1 / (1 + math.exp(-(1 + v) / P.b)) >= L.tauH
    return {"cL": P.cL, "k": P.k, "xp": xp, "v": v, "pool_end": cut, "pool_belief": pool_belief(P, cut, 1.0, -v),
            "tauL": L.tauL, "starved": not big, "brH": sH, "regretH": uH - U(P, "H", 1.0, 1.0, -v, xp),
            "brL": sL, "regretL": uL - U(P, "L", v, 1.0, -v, xp), "E": E, "OH": P.rho * S(P, cut - 1) / 2,
            "a3_right": (1 - 1 / P.b) * P.rho * L.m * L.DT}


# ------------------------------------------------------------------ closed-form starved members with x' >= 1 (referee result)
def starved_closed(P: Prm, v: float) -> dict:
    """Orders (1,-v), pool (-inf,x'), x' >= 1: every object is closed form.

    On [1, inf) the posterior is M_v = 1/(1+e^{-(1+v)/b}), so C_L = (rho DT / 2) M_v e^{-x'/b}. The low type's
    FOC gives x' = b log[(rho DT/2) M_v (1 - v/b) / k] - v. Valid when x' >= 1 and 0 <= v < v_H.
    """
    L = lev(P)
    Mv = 1.0 / (1.0 + math.exp(-(1 + v) / P.b))
    xp = P.b * math.log(P.rho * L.DT / 2 * Mv * (1 - v / P.b) / P.k) - v
    pb = F(P, xp - 1) / (F(P, xp - 1) + F(P, xp + v))
    return {"v": v, "xp": xp, "Mv": Mv, "pool_belief": pb, "cL_threshold": Bmu(P, pb),
            "E": P.rho * 0.5 * (S(P, xp - 1) + S(P, xp + v)), "OH": P.rho * S(P, xp - 1) / 2,
            "valid": (xp >= 1.0 - 1e-9) and (0.0 <= v < vH(P))}


def starved_closed_threshold(P: Prm, n: int = 4001) -> dict:
    """Smallest c_L at which a closed-form starved member (x' >= 1) exists: min pool belief over valid v."""
    best = None
    for v in np.linspace(0.0, vH(P) - 1e-9, n):
        r = starved_closed(P, float(v))
        if r["valid"] and (best is None or r["pool_belief"] < best["pool_belief"]):
            best = r
    return best if best is not None else {"cL_threshold": math.nan}
