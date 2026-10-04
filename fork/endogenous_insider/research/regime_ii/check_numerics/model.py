"""Referee model for the regime II test. New code; no import from the other tracks.

Everything is a pure function of a parameter record. Payoffs of the investor are computed
by adaptive quadrature (scipy QUADPACK) piece by piece. Entry is a step function of the
posterior, so inside each piece the integrand is smooth.

Conventions
  prm = Prm(...): h, ell, p, b, k, rho, cL, cH, r.
  An order law is a tuple of (q, weight) atoms.
  A pool is a tuple of (lo, hi) intervals (lo may be -inf, hi may be +inf).
  A profile = (prm, orders_H, orders_L, pool).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, replace
from typing import Sequence

from scipy import integrate, optimize

Orders = tuple[tuple[float, float], ...]
Pool = tuple[tuple[float, float], ...]
LIM = 70.0  # flow range; exp(-35) is about 6e-16


@dataclass(frozen=True)
class Prm:
    h: float = 10.0
    ell: float = 1.0
    p: float = 0.5
    b: float = 2.0
    k: float = 0.02
    rho: float = 0.25
    cL: float = 1.0
    cH: float = 6.0
    r: float = 3.0


# ---------------------------------------------------------------- auction layer
@dataclass(frozen=True)
class Auction:
    t0: float
    tH: float
    tL: float
    gH: float
    gL: float
    DT: float
    wL: float
    m: float
    M: float
    tauL: float
    tauH: float


def logistic(z: float) -> float:
    return 1.0 / (1.0 + math.exp(-z))


def auction(P: Prm) -> Auction:
    r, p, ell, h = P.r, P.p, P.ell, P.h
    t0 = p * (1.0 - p / r)
    tH = r / 2.0 + p * p / (2.0 * r)
    tL = ell - (ell * ell - p * p) / (2.0 * r)
    gL = (ell * ell - p * p) / (2.0 * r)
    gH = h - tH
    m = logistic(-2.0 / P.b)
    M = logistic(2.0 / P.b)
    return Auction(t0, tH, tL, gH, gL, tH - tL, tL - t0, m, M,
                   (P.cL - gL) / (gH - gL), (P.cH - gL) / (gH - gL))


def B(P: Prm, mu: float) -> float:
    a = auction(P)
    return a.gL + mu * (a.gH - a.gL)


# ---------------------------------------------------------------- noise
def f(z: float, b: float) -> float:
    return math.exp(-abs(z) / b) / (2.0 * b)


def F(z: float, b: float) -> float:
    return 0.5 * math.exp(z / b) if z < 0 else 1.0 - 0.5 * math.exp(-z / b)


def S(z: float, b: float) -> float:
    return F(-z, b)


# ---------------------------------------------------------------- information layer
def dens(orders: Orders, x: float, b: float) -> float:
    return sum(w * f(x - q, b) for q, w in orders)


def posterior(oH: Orders, oL: Orders, x: float, b: float) -> float:
    aH, aL = dens(oH, x, b), dens(oL, x, b)
    return aH / (aH + aL)


def phi(P: Prm, a: Auction, mu: float) -> float:
    """Entry at revealed belief mu, with the tie rule (indifferent prepares)."""
    return P.rho * (mu >= a.tauL) + (1.0 - P.rho) * (mu >= a.tauH)


def in_pool(pool: Pool, x: float) -> bool:
    return any(lo <= x < hi for lo, hi in pool)


def cuts(P: Prm, oH: Orders, oL: Orders, pool: Pool) -> list[float]:
    """Breakpoints of the entry function: pool ends and posterior crossings of the thresholds."""
    a = auction(P)
    pts = {-LIM, LIM}
    for lo, hi in pool:
        for e in (lo, hi):
            if -LIM < e < LIM:
                pts.add(e)
    # posterior crossings, found on a grid then polished
    n = 2800
    xs = [-LIM + 2 * LIM * i / n for i in range(n + 1)]
    for tau in (a.tauL, a.tauH):
        g = [posterior(oH, oL, x, P.b) - tau for x in xs]
        for i in range(n):
            if g[i] == 0.0:
                pts.add(xs[i])
            elif g[i] * g[i + 1] < 0:
                pts.add(optimize.brentq(lambda x: posterior(oH, oL, x, P.b) - tau,
                                        xs[i], xs[i + 1], xtol=1e-14, rtol=1e-14))
    for q, _ in list(oH) + list(oL):
        pts.add(q)
    return sorted(pts)


def entry_pieces(P: Prm, oH: Orders, oL: Orders, pool: Pool, pts: Sequence[float] | None = None
                 ) -> list[tuple[float, float, float]]:
    """Pieces (lo, hi, e) with e constant on each piece."""
    a = auction(P)
    pts = list(pts) if pts is not None else cuts(P, oH, oL, pool)
    out = []
    for lo, hi in zip(pts[:-1], pts[1:]):
        if hi - lo < 1e-15:
            continue
        mid = 0.5 * (lo + hi)
        e = 0.0 if in_pool(pool, mid) else phi(P, a, posterior(oH, oL, mid, P.b))
        out.append((lo, hi, e))
    return out


def prob(orders: Orders, lo: float, hi: float, b: float) -> float:
    """Pr(X in [lo,hi]) under an order law, closed form (used only for pool probabilities)."""
    return sum(w * (F(hi - q, b) - F(lo - q, b)) for q, w in orders)


def pool_belief(P: Prm, oH: Orders, oL: Orders, pool: Pool) -> float:
    pH = sum(prob(oH, max(lo, -LIM), min(hi, LIM), P.b) for lo, hi in pool)
    pL = sum(prob(oL, max(lo, -LIM), min(hi, LIM), P.b) for lo, hi in pool)
    return pH / (pH + pL) if pH + pL > 0 else float("nan")


# ---------------------------------------------------------------- investor payoff
def payoff(P: Prm, theta: str, q: float, pieces: list[tuple[float, float, float]],
           oH: Orders, oL: Orders) -> float:
    """U_theta(q) = q * E[(V_T - P) | theta, X = q+Z] - k|q| by adaptive quadrature."""
    if q == 0.0:
        return 0.0
    a = auction(P)
    b = P.b
    tot = 0.0
    for lo, hi, e in pieces:
        if e == 0.0:
            continue
        if theta == "H":
            g = lambda x: f(x - q, b) * (1.0 - posterior(oH, oL, x, b))
        else:
            g = lambda x: -f(x - q, b) * posterior(oH, oL, x, b)
        segs = [(lo, hi)]
        if lo < q < hi:
            segs = [(lo, q), (q, hi)]
        for s0, s1 in segs:
            v, _ = integrate.quad(g, s0, s1, epsabs=1e-14, epsrel=1e-12, limit=200)
            tot += e * v
    return q * a.DT * tot - P.k * abs(q)


def best_response(P: Prm, theta: str, pieces: list[tuple[float, float, float]],
                  oH: Orders, oL: Orders, ngrid: int = 201) -> tuple[float, float, list[tuple[float, float]]]:
    """Global best response on [-1,1]: grid, then polish every local maximum.
    Returns (argmax, max value, list of (q, U) local maxima)."""
    qs = [-1.0 + 2.0 * i / (ngrid - 1) for i in range(ngrid)]
    if 0.0 not in qs:
        qs.append(0.0)
        qs.sort()
    us = [payoff(P, theta, q, pieces, oH, oL) for q in qs]
    cand: list[tuple[float, float]] = []
    n = len(qs)
    for i in range(n):
        left = us[i - 1] if i > 0 else -1e18
        right = us[i + 1] if i < n - 1 else -1e18
        if us[i] >= left and us[i] >= right:
            lo = qs[i - 1] if i > 0 else qs[i]
            hi = qs[i + 1] if i < n - 1 else qs[i]
            if hi - lo < 1e-15 or qs[i] in (-1.0, 1.0, 0.0):
                cand.append((qs[i], us[i]))
            else:
                # keep the kink at zero out of the bracket
                if lo < 0.0 < hi:
                    lo, hi = (lo, 0.0) if qs[i] < 0 else (0.0, hi)
                res = optimize.minimize_scalar(lambda q: -payoff(P, theta, q, pieces, oH, oL),
                                               bounds=(lo, hi), method="bounded",
                                               options={"xatol": 1e-12})
                qv, uv = float(res.x), -float(res.fun)
                cand.append((qv, uv) if uv >= us[i] else (qs[i], us[i]))
    best = max(cand, key=lambda t: t[1])
    return best[0], best[1], cand


# ---------------------------------------------------------------- equilibrium check
def outcomes(P: Prm, oH: Orders, oL: Orders, pieces: list[tuple[float, float, float]]) -> dict:
    """E, e_H, e_L, O_H = e_H/2 by quadrature of entry against each flow law."""
    b = P.b
    eH = eL = 0.0
    for lo, hi, e in pieces:
        if e == 0.0:
            continue
        eH += e * prob(oH, lo, hi, b)
        eL += e * prob(oL, lo, hi, b)
    return {"E": 0.5 * (eH + eL), "eH": eH, "eL": eL, "OH": 0.5 * eH}


def check(P: Prm, oH: Orders, oL: Orders, pool: Pool, ngrid: int = 201) -> dict:
    """Independent equilibrium check of a profile. The profile is accepted when
    (1) the pool belief is below tauL (or the pool is null),
    (2) every flow with posterior below tauL lies in the pool,
    (3) each type's regret at its supported orders is below 1e-9."""
    a = auction(P)
    pts = cuts(P, oH, oL, pool)
    pieces = entry_pieces(P, oH, oL, pool, pts)
    pb = pool_belief(P, oH, oL, pool) if pool else float("nan")
    cond_pool = (not pool) or (pb < a.tauL)
    # entry set must sit where posterior >= tauL: pieces outside pool with phi=0 break it
    bad_mass = 0.0
    for lo, hi, e in pieces:
        mid = 0.5 * (lo + hi)
        if e == 0.0 and not in_pool(pool, mid):
            bad_mass += prob(oH, lo, hi, P.b) + prob(oL, lo, hi, P.b)
    cond_forced = bad_mass < 1e-12
    reg = {}
    brs = {}
    for th, orders in (("H", oH), ("L", oL)):
        qb, ub, cand = best_response(P, th, pieces, oH, oL, ngrid)
        used = max(payoff(P, th, q, pieces, oH, oL) for q, _ in orders)
        usedmin = min(payoff(P, th, q, pieces, oH, oL) for q, _ in orders)
        reg[th] = max(0.0, ub - usedmin)
        brs[th] = (qb, ub, used)
    out = outcomes(P, oH, oL, pieces)
    ppool = sum(0.5 * (prob(oH, max(lo, -LIM), min(hi, LIM), P.b) + prob(oL, max(lo, -LIM), min(hi, LIM), P.b))
                for lo, hi in pool)
    accepted = cond_pool and cond_forced and reg["H"] < 1e-9 and reg["L"] < 1e-9
    return {"accepted": accepted, "pool_belief": pb, "tauL": a.tauL, "pool_prob": ppool,
            "regret_H": reg["H"], "regret_L": reg["L"], "br_H": brs["H"][0], "br_L": brs["L"][0],
            "forced_ok": cond_forced, **out}


# ---------------------------------------------------------------- closed-form helpers (full orders)
def logit(u: float) -> float:
    return math.log(u / (1.0 - u))


def z0(P: Prm) -> float:
    return 0.5 * P.b * logit(auction(P).tauL)


def xstar(P: Prm) -> float:
    return 0.5 * P.b * logit(auction(P).tauH)


def mubar(x: float, b: float) -> float:
    """Pool belief of (-inf, x) under full orders."""
    u, v = F(x - 1, b), F(x + 1, b)
    return u / (u + v)


def xbar(P: Prm) -> float:
    """Root of mubar(x) = tauL, x > -1."""
    a = auction(P)
    return optimize.brentq(lambda x: mubar(x, P.b) - a.tauL, -1.0 + 1e-9, 60.0, xtol=1e-14)


def SX(x: float, b: float) -> float:
    """Pr(X >= x) under full orders."""
    return 0.5 * (S(x - 1, b) + S(x + 1, b))


def full_orders() -> tuple[Orders, Orders]:
    return ((1.0, 1.0),), ((-1.0, 1.0),)


def with_(P: Prm, **kw) -> Prm:
    return replace(P, **kw)
