"""Closed forms for the regime II test of Proposition 2 (theory track).

The cost law is the benchmark two-point law: c_L with probability rho, c_H otherwise. At the strong
incumbent r1 the cheap type is in regime II: B_r1(m) < c_L <= B_r1(1/2). Every function takes the
parameter record first and returns floats or frozen records. Nothing here writes files. Values are exact
closed forms in the Laplace CDF, evaluated in double precision, plus one-dimensional root finding and
adaptive quadrature; the note states the status of each number it uses.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from scipy import integrate, optimize


@dataclass(frozen=True)
class Params:
    """Primitives of the paper plus the two-point cost law and the strong incumbent r1."""
    h: float = 10.0
    ell: float = 1.0
    p: float = 0.5
    b: float = 2.0
    k: float = 0.02
    rho: float = 0.25
    c_L: float = 3.0
    c_H: float = 6.0
    r: float = 3.0


@dataclass(frozen=True)
class Levels:
    """Payoffs (4) and the belief thresholds at strength r."""
    t0: float
    wL: float
    DeltaT: float
    gL: float
    gH: float
    m: float
    M: float
    B_m: float
    B_half: float
    B_M: float
    tau_L: float
    tau_H: float
    z0: float       # forced pool end under full orders: mu_X(z0) = tau_L
    x_star: float   # expensive threshold flow under full orders: mu_X(x_star) = tau_H
    x_bar: float    # largest half-line pool: mubar(x_bar) = tau_L


@dataclass(frozen=True)
class Knapsack:
    """Worst consistent pool under full orders (bathtub solution)."""
    base: float      # value with the minimal pool Z_0 (entry E_0 or e_H0)
    lost: float      # supremum of the value removed by a consistent pool
    inf_value: float # base - lost: infimum over consistent pools (not attained)
    budget: float    # B_0 = int_{Z_0} (tau_L - mu) dP
    theta: float     # bathtub threshold
    y1: float        # mid pool [z0, y1)
    y2: float        # island [x_star, y2); y2 = 1 when the plateau is reached
    plateau_frac: float


# ---------------------------------------------------------------------------------------------
# primitives
# ---------------------------------------------------------------------------------------------

def noise_cdf(prm: Params, z: float) -> float:
    return 0.5 * math.exp(z / prm.b) if z <= 0.0 else 1.0 - 0.5 * math.exp(-z / prm.b)


def noise_sf(prm: Params, z: float) -> float:
    return 1.0 - noise_cdf(prm, z) if z <= 0.0 else 0.5 * math.exp(-z / prm.b)


def noise_pdf(prm: Params, z: float) -> float:
    return math.exp(-abs(z) / prm.b) / (2.0 * prm.b)


def logit(u: float) -> float:
    return math.log(u / (1.0 - u))


def mu_full(prm: Params, x: float) -> float:
    """(A.8): posterior under full orders (1, -1)."""
    return 1.0 / (1.0 + math.exp(-(abs(x + 1.0) - abs(x - 1.0)) / prm.b))


def mubar(prm: Params, xp: float, qH: float = 1.0, qL: float = -1.0) -> float:
    """Belief of the half-line pool (-inf, xp) under pure orders (qH, qL)."""
    a = noise_cdf(prm, xp - qH)
    c = noise_cdf(prm, xp - qL)
    return a / (a + c)


def levels(prm: Params, r: float | None = None) -> Levels:
    r = prm.r if r is None else r
    t0 = prm.p * (1.0 - prm.p / r)
    tH = r / 2.0 + prm.p ** 2 / (2.0 * r)
    tL = prm.ell - (prm.ell ** 2 - prm.p ** 2) / (2.0 * r)
    gH = prm.h - tH
    gL = (prm.ell ** 2 - prm.p ** 2) / (2.0 * r)
    m = 1.0 / (1.0 + math.exp(2.0 / prm.b))
    M = 1.0 - m
    B = lambda mu: gL + mu * (gH - gL)
    tau_L = (prm.c_L - gL) / (gH - gL)
    tau_H = (prm.c_H - gL) / (gH - gL)
    z0 = 0.5 * prm.b * logit(tau_L) if 0.0 < tau_L < 1.0 else float("nan")
    xs = 0.5 * prm.b * logit(tau_H) if 0.0 < tau_H < 1.0 else float("nan")
    if m < tau_L < 0.5:
        xb = optimize.brentq(lambda x: mubar(prm, x) - tau_L, -1.0 + 1e-12, 200.0, xtol=1e-14)
    else:
        xb = float("nan")
    return Levels(t0=t0, wL=tL - t0, DeltaT=tH - tL, gL=gL, gH=gH, m=m, M=M, B_m=B(m), B_half=B(0.5),
                  B_M=B(M), tau_L=tau_L, tau_H=tau_H, z0=z0, x_star=xs, x_bar=xb)


def regime_ii(prm: Params, lv: Levels) -> bool:
    """(A1') with a strict lower end: B_r(m) < c_L <= B_r(1/2)."""
    return lv.B_m < prm.c_L <= lv.B_half


# ---------------------------------------------------------------------------------------------
# pool cap and the forcing bound (Lemma R.5, Proposition R.6)
# ---------------------------------------------------------------------------------------------

def pool_cap(prm: Params, lv: Levels) -> tuple[float, float, float]:
    """Strict upper bounds on Pr(N|H), Pr(N|L), Pr(N) over every equilibrium (any orders, any pool)."""
    uH = noise_cdf(prm, lv.x_bar - 1.0)
    uL = noise_cdf(prm, lv.x_bar + 1.0)
    return uH, uL, 0.5 * (uH + uL)


def forcing_bound(prm: Params, lv: Levels) -> float:
    """K(c_L) = (1-1/b) rho Delta_T min{tau_L S(xbar+1), m S(xbar)}: k < K forces full orders."""
    low = lv.tau_L * noise_sf(prm, lv.x_bar + 1.0)
    high = lv.m * noise_sf(prm, lv.x_bar)
    return (1.0 - 1.0 / prm.b) * prm.rho * lv.DeltaT * min(low, high)


def a3_bound(prm: Params, lv: Levels) -> float:
    """Right side of the paper's (A3): (1-1/b) rho m Delta_T."""
    return (1.0 - 1.0 / prm.b) * prm.rho * lv.m * lv.DeltaT


# ---------------------------------------------------------------------------------------------
# full orders: interval masses, minimal pool, half-line family
# ---------------------------------------------------------------------------------------------

def mass_H(prm: Params, lo: float, hi: float) -> float:
    """Pr(H, X in [lo, hi)) under full orders = (1/2) Pr(Z + 1 in [lo, hi))."""
    if hi <= lo:
        return 0.0
    F = lambda z: 1.0 if z == math.inf else (0.0 if z == -math.inf else noise_cdf(prm, z))
    return 0.5 * (F(hi - 1.0) - F(lo - 1.0))


def mass_L(prm: Params, lo: float, hi: float) -> float:
    if hi <= lo:
        return 0.0
    F = lambda z: 1.0 if z == math.inf else (0.0 if z == -math.inf else noise_cdf(prm, z))
    return 0.5 * (F(hi + 1.0) - F(lo + 1.0))


def full_minimal_pool(prm: Params, lv: Levels) -> tuple[float, float]:
    """Entry and e_H under full orders and the minimal pool (-inf, z0)."""
    P = lambda lo, hi: mass_H(prm, lo, hi) + mass_L(prm, lo, hi)
    E0 = prm.rho * P(lv.z0, math.inf) + (1.0 - prm.rho) * P(lv.x_star, math.inf)
    eH0 = 2.0 * (prm.rho * mass_H(prm, lv.z0, math.inf) + (1.0 - prm.rho) * mass_H(prm, lv.x_star, math.inf))
    return E0, eH0


def half_line_outcome(prm: Params, lv: Levels, xp: float) -> tuple[float, float]:
    """Entry and e_H under full orders with the pool (-inf, xp), xp >= z0."""
    P = lambda lo, hi: mass_H(prm, lo, hi) + mass_L(prm, lo, hi)
    lo1 = max(xp, lv.z0)
    lo2 = max(xp, lv.x_star)
    E = prm.rho * P(lo1, math.inf) + (1.0 - prm.rho) * P(lo2, math.inf)
    eH = 2.0 * (prm.rho * mass_H(prm, lo1, math.inf) + (1.0 - prm.rho) * mass_H(prm, lo2, math.inf))
    return E, eH


def J_upper_half_line(prm: Params, lv: Levels, xp: float) -> float:
    """Existence statistic (A.7) for full orders with A = [xp, inf), xp >= x_star (e = 1 on A)."""
    if xp >= 1.0:
        return lv.DeltaT * lv.m * math.exp(-(xp - 1.0) / prm.b) / 2.0
    mu = 1.0 / (1.0 + math.exp(-2.0 * xp / prm.b))
    return lv.DeltaT * (math.exp(-1.0 / prm.b) / 2.0 * (math.asin(math.sqrt(lv.M)) - math.asin(math.sqrt(mu)))
                        + lv.m / 2.0)


def half_line_thresholds(prm: Params, lv: Levels) -> dict[str, float]:
    """Half-line counterexample family (Proposition R.9): flows and c_L thresholds for E and e_H."""
    E = lambda x: 0.5 * (noise_sf(prm, x - 1.0) + noise_sf(prm, x + 1.0))
    eH = lambda x: noise_sf(prm, x - 1.0)
    xk = optimize.brentq(lambda x: (1.0 - 1.0 / prm.b) * J_upper_half_line(prm, lv, x) - prm.k,
                         lv.x_star, 200.0) if (1.0 - 1.0 / prm.b) * J_upper_half_line(prm, lv, lv.x_star) >= prm.k \
        else float("nan")
    B = lambda mu: lv.gL + mu * (lv.gH - lv.gL)
    out = {"x_k": xk}
    for name, fn in (("E", E), ("eH", eH)):
        if fn(lv.x_star) <= prm.rho:
            x = lv.x_star
        elif fn(200.0) > prm.rho:
            x = float("nan")
        else:
            x = optimize.brentq(lambda y: fn(y) - prm.rho, lv.x_star, 200.0, xtol=1e-14)
        out["x_" + name] = x
        ok = (not math.isnan(x)) and (math.isnan(xk) is False) and x <= xk
        out["cL_" + name] = B(mubar(prm, x)) if ok else float("nan")
    return out


# ---------------------------------------------------------------------------------------------
# bathtub (fractional knapsack) over consistent pools under full orders (Proposition R.7)
# ---------------------------------------------------------------------------------------------

def _flow_of_belief(prm: Params, mu: float) -> float:
    return 0.5 * prm.b * logit(mu)


def _gamma(prm: Params, lv: Levels, lo: float, hi: float) -> float:
    """int_[lo,hi) (mu - tau_L) dP under full orders."""
    return (1.0 - lv.tau_L) * mass_H(prm, lo, hi) - lv.tau_L * mass_L(prm, lo, hi)


def knapsack(prm: Params, lv: Levels, target: str = "E") -> Knapsack:
    """Supremum of the entry (target 'E') or e_H (target 'eH') removed by a consistent pool.

    Items are flows x >= z0 with cost (mu - tau_L) dP and value phi(mu) dP (for E) or phi(mu) dPr(H, .)
    (for e_H, reported as e_H = 2 Pr(H, prepare)). The bathtub rule keeps the items with the smallest
    cost/value ratio. Region R1 = [z0, x_star) has phi = rho; region R2 = [x_star, inf) has phi = 1; the
    plateau [1, inf) has constant ratio and is taken fractionally.
    """
    rho, tl = prm.rho, lv.tau_L
    if target == "E":
        mu1 = lambda th: tl + rho * th
        mu2 = lambda th: tl + th
        plateau_ratio = lv.M - tl
        valH, valL = 1.0, 1.0
    else:
        mu1 = lambda th: tl / (1.0 - rho * th) if rho * th < 1.0 else 1.0
        mu2 = lambda th: tl / (1.0 - th) if th < 1.0 else 1.0
        plateau_ratio = 1.0 - tl / lv.M
        valH, valL = 2.0, 0.0  # e_H = 2 Pr(H, prepare)

    def value(lo: float, hi: float, phi: float) -> float:
        return phi * (valH * mass_H(prm, lo, hi) + valL * mass_L(prm, lo, hi))

    def parts(th: float) -> tuple[float, float]:
        m1 = min(mu1(th), lv.tau_H)
        y1 = lv.x_star if m1 >= lv.tau_H else max(lv.z0, _flow_of_belief(prm, m1))
        m2 = mu2(th)
        if m2 < lv.tau_H:
            y2 = lv.x_star
        elif m2 >= lv.M:
            y2 = 1.0
        else:
            y2 = _flow_of_belief(prm, m2)
        return y1, y2

    def cost(th: float, with_plateau: bool) -> float:
        y1, y2 = parts(th)
        c = _gamma(prm, lv, lv.z0, y1) + _gamma(prm, lv, lv.x_star, y2)
        if with_plateau:
            c += _gamma(prm, lv, 1.0, math.inf)
        return c

    budget = -_gamma(prm, lv, -math.inf, lv.z0)
    E0, eH0 = full_minimal_pool(prm, lv)
    base = E0 if target == "E" else eH0
    th_max = (lv.tau_H - tl) / rho if target == "E" else (1.0 - tl / lv.tau_H) / rho
    th_max = max(th_max, plateau_ratio) * 1.000001 + 1e-9
    # cost below the plateau ratio excludes the plateau; at and above it includes the plateau fully
    c_before = cost(plateau_ratio * (1 - 1e-15), False)
    c_after = cost(plateau_ratio, True)
    frac = 0.0
    if budget <= c_before:
        th = optimize.brentq(lambda t: cost(t, False) - budget, 0.0, plateau_ratio * (1 - 1e-15), xtol=1e-15)
        incl = False
    elif budget <= c_after:
        th = plateau_ratio
        incl = False
        frac = (budget - c_before) / _gamma(prm, lv, 1.0, math.inf)
    else:
        if cost(th_max, True) <= budget:
            th = th_max
        else:
            th = optimize.brentq(lambda t: cost(t, True) - budget, plateau_ratio, th_max, xtol=1e-15)
        incl = True
        frac = 1.0
    y1, y2 = parts(th)
    lost = value(lv.z0, y1, rho) + value(lv.x_star, y2, 1.0)
    if incl or frac > 0.0:
        lost += frac * value(1.0, math.inf, 1.0)
    return Knapsack(base=base, lost=lost, inf_value=base - lost, budget=budget, theta=th, y1=y1, y2=y2,
                    plateau_frac=frac)


def simple_sufficient(prm: Params, lv: Levels) -> float:
    """Closed-form lower bound on inf E under full orders: E_0 - rho*(pi_bar - P(Z_0)) - (1-rho)*min(P_hi, B_0/(tau_H - tau_L))."""
    E0, _ = full_minimal_pool(prm, lv)
    _, _, pib = pool_cap(prm, lv)
    PZ0 = mass_H(prm, -math.inf, lv.z0) + mass_L(prm, -math.inf, lv.z0)
    Phi = mass_H(prm, lv.x_star, math.inf) + mass_L(prm, lv.x_star, math.inf)
    budget = -_gamma(prm, lv, -math.inf, lv.z0)
    return E0 - prm.rho * (pib - PZ0) - (1.0 - prm.rho) * min(Phi, budget / (lv.tau_H - lv.tau_L))


# ---------------------------------------------------------------------------------------------
# the starved family (Proposition R.10): orders (1, -v), v < v_H, pool (-inf, xp), xp >= 0
# ---------------------------------------------------------------------------------------------

def v_H(prm: Params, lv: Levels) -> float:
    """Largest short with no expensive entry under q_H = 1: 1 + v < b logit(tau_H)."""
    return prm.b * logit(lv.tau_H) - 1.0


def mu_pure(prm: Params, x: float, v: float) -> float:
    a = noise_pdf(prm, x - 1.0)
    c = noise_pdf(prm, x + v)
    return a / (a + c)


def starved_C_L(prm: Params, lv: Levels, v: float, xp: float) -> float:
    """C_L = rho Delta_T int_xp^inf e^{-x/b} mu_X(x) / (2b) dx, so that F_L(s) = e^{-s/b} C_L for xp >= 0."""
    mup = 1.0 / (1.0 + math.exp(-(1.0 + v) / prm.b))
    tail = mup * math.exp(-max(xp, 1.0) / prm.b) / 2.0
    mid = 0.0
    if xp < 1.0:
        mid = integrate.quad(lambda x: math.exp(-x / prm.b) / (2.0 * prm.b) * mu_pure(prm, x, v), xp, 1.0,
                             epsabs=1e-14, epsrel=1e-13)[0]
    return prm.rho * lv.DeltaT * (mid + tail)


def starved_member(prm: Params, lv: Levels, v: float) -> tuple[float, float, float, float] | None:
    """Pool end xp >= 0 solving the low type's first-order condition at short v; None if none exists.

    Returns (xp, pool belief, E, e_H).
    """
    foc = lambda xp: starved_C_L(prm, lv, v, xp) * math.exp(-v / prm.b) * (1.0 - v / prm.b) - prm.k
    if foc(0.0) < 0.0 or foc(200.0) > 0.0:
        return None
    xp = optimize.brentq(foc, 0.0, 200.0, xtol=1e-13)
    pb = mubar(prm, xp, 1.0, -v)
    E = prm.rho * 0.5 * (noise_sf(prm, xp - 1.0) + noise_sf(prm, xp + v))
    eH = prm.rho * noise_sf(prm, xp - 1.0)
    return xp, pb, E, eH


def starved_UH(prm: Params, lv: Levels, v: float, xp: float, s: float) -> float:
    """High type's payoff from buying s against the starved schedule (entry rho on [xp, inf))."""
    g = lambda x: noise_pdf(prm, x - s) * (1.0 - mu_pure(prm, x, v))
    pts = [t for t in (s, 1.0) if t > xp]
    val = integrate.quad(g, xp, xp + 80.0, points=pts or None, limit=400, epsabs=1e-14, epsrel=1e-12)[0]
    return s * prm.rho * lv.DeltaT * val - prm.k * s
