"""Independent verification of a candidate equilibrium by adaptive quadrature (QUADPACK).

This module does not import engine.py. It rebuilds every object from first principles:
  1. auction values by integrating over the incumbent's value R (no use of closed forms (4));
  2. the posterior from the order mixtures; thresholds by root finding on the posterior itself;
  3. the pool and its belief by quadrature of the flow densities over the zero-entry set;
  4. the market maker's price as the posterior-weighted expected value, and the investor's gain
     as the difference between a type's expected value and that price;
  5. the investor's global best response by a fine order grid plus local refinement, every point by quad.
A candidate is accepted only if the pool is consistent and both types' regrets are below tol.
Status of an accepted row: computer-assisted at tolerance tol (floating-point quadrature, not an interval
enclosure). The independent check is a numerical diagnostic of the engine, not a proof.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

from scipy import integrate, optimize

INF = math.inf


# ----------------------------------------------------------------------------------------------
# auction values by integration over the incumbent's value R ~ U[0, r]
# ----------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Values:
    t0: float
    tH: float
    tL: float
    gH: float
    gL: float


def _q(f, a: float, b: float, pts: Sequence[float] = ()) -> float:
    """Adaptive quadrature on (a, b), split at every kink in pts (the integrand is smooth between kinks)."""
    cuts = [a] + sorted(x for x in pts if a < x < b) + [b]
    total = 0.0
    for lo, hi in zip(cuts[:-1], cuts[1:]):
        val, _ = integrate.quad(f, lo, hi, epsabs=1e-14, epsrel=1e-13, limit=400)
        total += val
    return total


def auction_values(h: float, ell: float, p: float, r: float) -> Values:
    """Second-price auction with reserve p. Incumbent value R ~ U[0, r]; challenger value v in {ell, h}.

    The seller's proceeds are max(p, second-highest admissible bid). The challenger's gross profit is
    (v - price) when it wins. A prepared challenger with v > R wins; the incumbent must have R >= p to bid.
    """
    def proceeds(v: float, R: float) -> float:
        # challenger always admissible (v > p). Price is max(p, R) when R < v, else v.
        return max(p, min(R, v))

    t0 = _q(lambda R: (p if R >= p else 0.0) / r, 0.0, r, [p])      # incumbent alone, reserve p
    tH = _q(lambda R: proceeds(h, R) / r, 0.0, r, [p])
    tL = _q(lambda R: proceeds(ell, R) / r, 0.0, r, [p, ell])
    gH = _q(lambda R: (h - max(p, R)) / r, 0.0, r, [p])                # v = h > r always wins
    gL = _q(lambda R: ((ell - max(p, R)) if R < ell else 0.0) / r, 0.0, r, [p, ell])
    return Values(t0=t0, tH=tH, tL=tL, gH=gH, gL=gL)


# ----------------------------------------------------------------------------------------------
# flows, posterior, entry
# ----------------------------------------------------------------------------------------------

def _dens(b: float, atoms: Sequence[tuple[float, float]], x: float) -> float:
    return sum(w * math.exp(-abs(x - q) / b) / (2.0 * b) for q, w in atoms)


def _cdf(b: float, atoms: Sequence[tuple[float, float]], lo: float, hi: float) -> float:
    def F(z: float) -> float:
        return 0.5 * math.exp(z / b) if z <= 0.0 else 1.0 - 0.5 * math.exp(-z / b)
    total = 0.0
    for q, w in atoms:
        a = 0.0 if lo == -INF else F(lo - q)
        c = 1.0 if hi == INF else F(hi - q)
        total += w * (c - a)
    return total


@dataclass(frozen=True)
class Case:
    """A candidate equilibrium in the verifier's own terms."""
    h: float
    ell: float
    p: float
    b: float
    k: float
    r: float
    rho: float
    cL: float
    cH: float
    H: tuple[tuple[float, float], ...]
    L: tuple[tuple[float, float], ...]
    pool: tuple[tuple[float, float], ...] = ()


class _Model:
    def __init__(self, c: Case):
        self.c = c
        self.v = auction_values(c.h, c.ell, c.p, c.r)
        self.span = self.v.gH - self.v.gL
        self.DeltaT = self.v.tH - self.v.tL
        self.m = 1.0 / (1.0 + math.exp(2.0 / c.b))
        self.tau = [(c.cL - self.v.gL) / self.span, (c.cH - self.v.gL) / self.span]
        self.costs = [(c.cL, c.rho), (c.cH, 1.0 - c.rho)]
        atoms = sorted({q for q, _ in c.H + c.L})
        pts = set(atoms)
        for lo, hi in c.pool:
            pts.update(v for v in (lo, hi) if abs(v) < 60.0)
        for tau in self.tau:
            pts.update(self._roots(tau, atoms))
        self.breaks = sorted(pts)
        self.pieces = []
        edges = [-INF] + self.breaks + [INF]
        for lo, hi in zip(edges[:-1], edges[1:]):
            if lo == -INF:
                rep = hi - 1.0
            elif hi == INF:
                rep = lo + 1.0
            else:
                rep = 0.5 * (lo + hi)
            self.pieces.append((lo, hi, self.entry_flow(rep)))

    def mu(self, x: float) -> float:
        """Posterior Pr(H | X = x), computed with log-sum-exp so that far tails do not underflow."""
        b = self.c.b
        def log_a(atoms):
            terms = [math.log(w) - abs(x - q) / b for q, w in atoms if w > 0.0]
            top = max(terms)
            return top + math.log(sum(math.exp(t - top) for t in terms))
        d = log_a(self.c.L) - log_a(self.c.H)
        if d > 700.0:
            return 0.0
        if d < -700.0:
            return 1.0
        return 1.0 / (1.0 + math.exp(d))

    def entry_belief(self, mu: float) -> float:
        """Pr(C <= B(mu)): the challenger prepares when its cost is covered (tie rule)."""
        B = self.v.gL + mu * self.span
        return sum(w for cost, w in self.costs if cost <= B + 1e-12)

    def entry_flow(self, x: float) -> float:
        for lo, hi in self.c.pool:
            if lo < x < hi:
                return 0.0
        return self.entry_belief(self.mu(x))

    def _roots(self, tau: float, atoms: list[float]) -> list[float]:
        out = []
        xs = [-60.0] + atoms + [60.0]
        for a, c in zip(xs[:-1], xs[1:]):
            if c - a < 1e-12:
                continue
            n = 80
            grid = [a + (c - a) * i / n for i in range(n + 1)]
            vals = [self.mu(x) - tau for x in grid]
            for i in range(n):
                if vals[i] * vals[i + 1] < 0.0:
                    out.append(optimize.brentq(lambda x: self.mu(x) - tau, grid[i], grid[i + 1], xtol=1e-14, rtol=1e-14))
        return out

    # ---- quantities by quad over the pieces of constant entry ----

    def piece_integral(self, g) -> float:
        """int g(x, e) dx over the line, piece by piece."""
        total = 0.0
        for lo, hi, e in self.pieces:
            total += _q(lambda x: g(x, e), lo if lo != -INF else -INF, hi if hi != INF else INF)
        return total

    def pool_belief(self) -> tuple[float, float]:
        PH = PL = 0.0
        for lo, hi, e in self.pieces:
            if e == 0.0:
                PH += _cdf(self.c.b, self.c.H, lo, hi)
                PL += _cdf(self.c.b, self.c.L, lo, hi)
        pm = PH + PL
        return (PH / pm if pm > 1e-300 else float("nan")), 0.5 * pm

    def entry_probs(self) -> tuple[float, float]:
        eH = sum(e * _cdf(self.c.b, self.c.H, lo, hi) for lo, hi, e in self.pieces)
        eL = sum(e * _cdf(self.c.b, self.c.L, lo, hi) for lo, hi, e in self.pieces)
        return eH, eL

    def gain(self, theta: str, x: float, e: float) -> float:
        """E[V_T | theta, x] - P(x) for theta = H, and P(x) - E[V_T | L, x] for theta = L, as signed 'long' gains.

        V_theta(x) = t0 + e (t_theta - t0). P(x) = mu V_H + (1 - mu) V_L. Returns V_theta - P.
        """
        v = self.v
        mu = self.mu(x)
        VH = v.t0 + e * (v.tH - v.t0)
        VL = v.t0 + e * (v.tL - v.t0)
        P = mu * VH + (1.0 - mu) * VL
        return (VH if theta == "H" else VL) - P

    def payoff(self, theta: str, q: float) -> float:
        """q * int f(x - q) [V_theta(x) - P(x)] dx - k |q|."""
        b = self.c.b
        total = 0.0
        for lo, hi, e in self.pieces:
            if e == 0.0:
                continue
            f = lambda x, e=e: math.exp(-abs(x - q) / b) / (2.0 * b) * self.gain(theta, x, e)  # noqa: E731
            pts = [q]
            total += _q(f, lo, hi, pts)
        return q * total - self.c.k * abs(q)


def _best_on_grid(model: _Model, theta: str, qs: Sequence[float], refine: int = 3) -> tuple[float, float]:
    vals = [model.payoff(theta, q) for q in qs]
    cand = [i for i in range(len(qs)) if (i == 0 or vals[i] >= vals[i - 1]) and (i == len(qs) - 1 or vals[i] >= vals[i + 1])]
    cand.sort(key=lambda i: -vals[i])
    best_q, best_u = 0.0, 0.0
    for i in cand[:refine]:
        lo = qs[max(i - 1, 0)]
        hi = qs[min(i + 1, len(qs) - 1)]
        res = optimize.minimize_scalar(lambda s: -model.payoff(theta, s), bounds=(lo, hi), method="bounded",
                                       options={"xatol": 1e-10})
        for q_try, u_try in ((float(res.x), -float(res.fun)), (qs[i], vals[i])):
            if u_try > best_u:
                best_q, best_u = q_try, u_try
    return best_q, best_u


@dataclass(frozen=True)
class Verdict:
    accepted: bool
    pool_consistent: bool
    pool_belief: float
    pool_prob: float
    regret_H: float
    regret_L: float
    wrong_sign_max: float      # largest payoff over wrong-sign orders (must be <= 0)
    price_increasing: bool
    E: float
    O_H: float
    eH: float
    eL: float
    values: Values


def verify(c: Case, tol: float = 1e-8, step: float = 0.01) -> Verdict:
    """Check the market maker, the challenger, and the investor's global best response by quad."""
    M = _Model(c)
    mubar, pool_prob = M.pool_belief()
    pool_ok = math.isnan(mubar) or M.entry_belief(mubar) == 0.0
    eH, eL = M.entry_probs()
    # price strictly increasing in the posterior on the entry set, and above the pool price t_0
    v = M.v
    samples = []
    for i in range(-400, 401):
        x = i * 0.05
        e = M.entry_flow(x)
        if e > 0.0:
            mu = M.mu(x)
            samples.append((mu, v.t0 + e * (v.tL - v.t0 + (v.tH - v.tL) * mu)))
    samples.sort()
    price_ok = all(pr > v.t0 for _, pr in samples) and all(
        samples[i + 1][1] >= samples[i][1] - 1e-12 for i in range(len(samples) - 1))
    n = int(round(1.0 / step))
    qH = [i / n for i in range(n + 1)]
    qL = [-i / n for i in range(n, -1, -1)]
    _, uH = _best_on_grid(M, "H", qH)
    _, uL = _best_on_grid(M, "L", qL)
    own_H = sum(w * M.payoff("H", q) for q, w in c.H)
    own_L = sum(w * M.payoff("L", q) for q, w in c.L)
    # for mixed profiles every support point must earn the same: regret is the best minus each support point
    reg_H = max([uH - M.payoff("H", q) for q, _ in c.H] + [0.0])
    reg_L = max([uL - M.payoff("L", q) for q, _ in c.L] + [0.0])
    wrong = max([M.payoff("H", -s / 10.0) for s in range(1, 11)] + [M.payoff("L", s / 10.0) for s in range(1, 11)])
    ok = pool_ok and reg_H <= tol and reg_L <= tol and wrong <= 0.0 and price_ok
    return Verdict(accepted=bool(ok), pool_consistent=bool(pool_ok), pool_belief=mubar, pool_prob=pool_prob,
                   regret_H=reg_H, regret_L=reg_L, wrong_sign_max=wrong, price_increasing=bool(price_ok),
                   E=0.5 * (eH + eL), O_H=0.5 * eH, eH=eH, eL=eL, values=v)
