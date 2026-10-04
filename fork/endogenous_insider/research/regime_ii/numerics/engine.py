"""Exact-quadrature engine for the two-point-cost economy in regime I and regime II.

Numerics track of the regime II team. Pure functions with type hints. The parameter record comes first.
Nothing here writes files.

Model (paper Section 2 and the cost-distribution note). The investor of type theta in {H, L} chooses an
order q in [-1, 1]. Flow is X = q + Z with Laplace noise of scale b. The price is the competitive price. The
challenger prepares when its cost C <= B_r(mu), with C = c_L w.p. rho and c_H otherwise (tie rule: prepare).
So entry at revealed belief mu is e(mu) = rho 1{mu >= tau_L} + (1 - rho) 1{mu >= tau_H}.

A profile is a pair of finite order mixtures plus an optional voluntary pool. The pool N is the set of flows
where nobody prepares. It contains the forced pool {mu_X < tau_L} and any voluntary intervals. All pool flows
share the price t_0 and the belief mubar_N. The profile is consistent when mubar_N < tau_L.

Entry and the investor's residuals are piecewise constant in e, and smooth inside every panel. The
integral I_theta(q) = int f(x - q) A_theta(x) dx is computed with Gauss-Legendre panels and cumulative sums,
so the kink at x = q is handled exactly. Every value is a numerical diagnostic until verify.py confirms it
by independent adaptive quadrature.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Sequence

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import brentq

GLX, GLW = leggauss(14)
X0 = 80.0          # truncation of the flow line: Laplace tail e^{-40} at b = 2
PANEL = 4.0        # maximal panel length
TIE = 1e-13        # tie tolerance for mu >= tau comparisons


# ----------------------------------------------------------------------------------------------
# economy
# ----------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Econ:
    """Primitives, strength r, and the two-point cost law. tauL, tauH are belief thresholds B_r^{-1}(c)."""
    r: float
    rho: float
    cL: float
    cH: float
    h: float = 10.0
    ell: float = 1.0
    p: float = 0.5
    b: float = 2.0
    k: float = 0.02
    t0: float = 0.0
    tH: float = 0.0
    tL: float = 0.0
    gH: float = 0.0
    gL: float = 0.0
    DeltaT: float = 0.0
    wL: float = 0.0
    tauL: float = 0.0
    tauH: float = 0.0
    m: float = 0.0
    M: float = 0.0


def make_econ(r: float, rho: float, cL: float | None = None, cH: float = 6.0, *, tauL: float | None = None,
              h: float = 10.0, ell: float = 1.0, p: float = 0.5, b: float = 2.0, k: float = 0.02) -> Econ:
    """Build the economy. Give cL, or give tauL to fix the belief threshold exactly (ties)."""
    t0 = p * (1.0 - p / r)
    tH = r / 2.0 + p * p / (2.0 * r)
    tL = ell - (ell * ell - p * p) / (2.0 * r)
    gH = h - tH
    gL = (ell * ell - p * p) / (2.0 * r)
    span = gH - gL
    m = 1.0 / (1.0 + math.exp(2.0 / b))
    if tauL is None:
        if cL is None:
            raise ValueError("give cL or tauL")
        tauL = (cL - gL) / span
    else:
        cL = gL + tauL * span
    tauH = (cH - gL) / span
    return Econ(r=r, rho=rho, cL=float(cL), cH=cH, h=h, ell=ell, p=p, b=b, k=k, t0=t0, tH=tH, tL=tL, gH=gH, gL=gL,
                DeltaT=tH - tL, wL=tL - t0, tauL=tauL, tauH=tauH, m=m, M=1.0 - m)


def B_of(ec: Econ, mu: float) -> float:
    return ec.gL + mu * (ec.gH - ec.gL)


def entry_at_belief(ec: Econ, mu: float) -> float:
    """e(mu) with the tie rule."""
    return ec.rho * float(mu >= ec.tauL - TIE) + (1.0 - ec.rho) * float(mu >= ec.tauH - TIE)


# ----------------------------------------------------------------------------------------------
# profiles
# ----------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Profile:
    """Order mixtures and a voluntary pool. H atoms have q >= 0 and L atoms q <= 0 in equilibrium.

    H, L: tuples of (order, weight). pool: tuple of (lo, hi) flow intervals, lo may be -inf.
    """
    H: tuple[tuple[float, float], ...]
    L: tuple[tuple[float, float], ...]
    pool: tuple[tuple[float, float], ...] = ()


def pure(qH: float, qL: float, cutoff: float | None = None) -> Profile:
    pool = () if cutoff is None or cutoff == -math.inf else ((-math.inf, float(cutoff)),)
    return Profile(H=((float(qH), 1.0),), L=((float(qL), 1.0),), pool=pool)


def pure_pool(qH: float, qL: float, pool: tuple[tuple[float, float], ...]) -> Profile:
    """Pure orders with an arbitrary voluntary pool (union of flow intervals)."""
    return Profile(H=((float(qH), 1.0),), L=((float(qL), 1.0),), pool=tuple(pool))


def _lap_cdf(z: np.ndarray | float, b: float) -> np.ndarray | float:
    z = np.asarray(z, dtype=float)
    out = np.where(z <= 0.0, 0.5 * np.exp(np.minimum(z, 0.0) / b), 1.0 - 0.5 * np.exp(-np.maximum(z, 0.0) / b))
    return float(out) if out.ndim == 0 else out


def flow_density(ec: Econ, atoms: Sequence[tuple[float, float]], x: np.ndarray) -> np.ndarray:
    out = np.zeros_like(x, dtype=float)
    for q, w in atoms:
        out = out + w * np.exp(-np.abs(x - q) / ec.b) / (2.0 * ec.b)
    return out


def mu_flow(ec: Econ, prof: Profile, x: np.ndarray) -> np.ndarray:
    """Posterior Pr(H | X = x) under the order mixtures."""
    aH = flow_density(ec, prof.H, x)
    aL = flow_density(ec, prof.L, x)
    return aH / (aH + aL)


def mass(ec: Econ, atoms: Sequence[tuple[float, float]], lo: float, hi: float) -> float:
    """Pr(lo < X < hi) under the order mixture."""
    total = 0.0
    for q, w in atoms:
        a = 0.0 if lo == -math.inf else _lap_cdf(lo - q, ec.b)
        c = 1.0 if hi == math.inf else _lap_cdf(hi - q, ec.b)
        total += w * (c - a)
    return total


# ----------------------------------------------------------------------------------------------
# schedule: panels with constant entry
# ----------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Schedule:
    edges: np.ndarray       # panel edges, length P + 1
    e: np.ndarray           # entry level per panel
    prof: Profile
    ec: Econ
    nodes: np.ndarray = field(repr=False)      # (P, n) GL nodes
    wts: np.ndarray = field(repr=False)        # (P, n) GL weights (include half-length)
    cum1: np.ndarray = field(repr=False)       # prefix sums of int e^{x/b} A_theta over panels, per theta
    suf2: np.ndarray = field(repr=False)       # suffix sums of int e^{-x/b} A_theta
    pool_mass_H: float = 0.0
    pool_mass_L: float = 0.0
    consistent: bool = True


def _crossings(ec: Econ, prof: Profile, tau: float) -> list[float]:
    """Flows where mu_X crosses tau. Pure-order profiles use the closed form; mixtures use root finding."""
    qs = sorted({q for q, _ in prof.H} | {q for q, _ in prof.L})
    if len(prof.H) == 1 and len(prof.L) == 1:
        qH, qL = prof.H[0][0], prof.L[0][0]
        if qH == qL:
            return []
        lo, hi = (qL, qH) if qH > qL else (qH, qL)
        if not (0.0 < tau < 1.0):
            return []
        x = 0.5 * (qH + qL) + 0.5 * ec.b * math.log(tau / (1.0 - tau)) * (1.0 if qH > qL else -1.0)
        return [x] if lo < x < hi else []
    segs = [-X0] + qs + [X0]
    roots: list[float] = []
    g = lambda x: float(mu_flow(ec, prof, np.array([x]))[0]) - tau  # noqa: E731
    for a, c in zip(segs[:-1], segs[1:]):
        if c - a < 1e-12:
            continue
        xs = np.linspace(a, c, 65)
        vs = mu_flow(ec, prof, xs) - tau
        for i in range(64):
            if vs[i] == 0.0:
                roots.append(float(xs[i]))
            elif vs[i] * vs[i + 1] < 0.0:
                roots.append(brentq(g, xs[i], xs[i + 1], xtol=1e-13, rtol=1e-13))
    return roots


def build_schedule(ec: Econ, prof: Profile) -> Schedule:
    """Panels, entry, pool consistency, and cumulative integrals for the investor's payoffs."""
    pts = {-X0, X0}
    for q, _ in prof.H + prof.L:
        pts.add(q)
    for tau in (ec.tauL, ec.tauH):
        pts.update(_crossings(ec, prof, tau))
    for lo, hi in prof.pool:
        for v in (lo, hi):
            if -X0 < v < X0:
                pts.add(v)
    base = sorted(pts)
    edges = [base[0]]
    for a, c in zip(base[:-1], base[1:]):
        n = max(1, int(math.ceil((c - a) / PANEL)))
        edges.extend(np.linspace(a, c, n + 1)[1:].tolist())
    edges_a = np.array(edges)
    mids = 0.5 * (edges_a[:-1] + edges_a[1:])
    mu_mid = mu_flow(ec, prof, mids)
    e = ec.rho * (mu_mid >= ec.tauL - TIE) + (1.0 - ec.rho) * (mu_mid >= ec.tauH - TIE)
    for lo, hi in prof.pool:
        inside = (mids > lo) & (mids < hi)
        e = np.where(inside, 0.0, e)
    half = 0.5 * (edges_a[1:] - edges_a[:-1])
    nodes = mids[:, None] + half[:, None] * GLX[None, :]
    wts = half[:, None] * GLW[None, :]
    mu_n = mu_flow(ec, prof, nodes)
    A = np.stack([e[:, None] * ec.DeltaT * (1.0 - mu_n), e[:, None] * ec.DeltaT * mu_n])   # (2, P, n)
    p1 = (np.exp(nodes / ec.b)[None] * A * wts[None]).sum(axis=2)    # (2, P)
    p2 = (np.exp(-nodes / ec.b)[None] * A * wts[None]).sum(axis=2)
    cum1 = np.concatenate([np.zeros((2, 1)), np.cumsum(p1, axis=1)], axis=1)           # (2, P+1)
    suf2 = np.concatenate([np.cumsum(p2[:, ::-1], axis=1)[:, ::-1], np.zeros((2, 1))], axis=1)
    pool_H = pool_L = 0.0
    for j in np.nonzero(e == 0.0)[0]:
        pool_H += mass(ec, prof.H, float(edges_a[j]), float(edges_a[j + 1]))
        pool_L += mass(ec, prof.L, float(edges_a[j]), float(edges_a[j + 1]))
    pm = pool_H + pool_L
    mubar = pool_H / pm if pm > 1e-300 else float("nan")
    consistent = (pm <= 1e-300) or (mubar < ec.tauL - TIE)
    return Schedule(edges=edges_a, e=np.asarray(e, dtype=float), prof=prof, ec=ec, nodes=nodes, wts=wts, cum1=cum1,
                    suf2=suf2, pool_mass_H=pool_H, pool_mass_L=pool_L, consistent=bool(consistent))


def pool_belief(sch: Schedule) -> float:
    pm = sch.pool_mass_H + sch.pool_mass_L
    return sch.pool_mass_H / pm if pm > 1e-300 else float("nan")


# ----------------------------------------------------------------------------------------------
# investor payoffs
# ----------------------------------------------------------------------------------------------

def _I(sch: Schedule, theta: int, q: np.ndarray) -> np.ndarray:
    """I_theta(q) = int f(x - q) A_theta(x) dx for an array of orders q (theta 0 = H, 1 = L)."""
    ec, prof = sch.ec, sch.prof
    q = np.atleast_1d(np.asarray(q, dtype=float))
    j = np.clip(np.searchsorted(sch.edges, q, side="right") - 1, 0, len(sch.e) - 1)
    lo = sch.edges[j]
    hi = sch.edges[j + 1]
    ej = sch.e[j]
    # partial integral over [lo, q] of e^{x/b} A and over [q, hi] of e^{-x/b} A
    h1 = 0.5 * (q - lo)
    x1 = lo[:, None] + h1[:, None] * (1.0 + GLX[None, :])
    h2 = 0.5 * (hi - q)
    x2 = q[:, None] + h2[:, None] * (1.0 + GLX[None, :])
    mu1 = mu_flow(ec, prof, x1)
    mu2 = mu_flow(ec, prof, x2)
    fac1 = (1.0 - mu1) if theta == 0 else mu1
    fac2 = (1.0 - mu2) if theta == 0 else mu2
    part1 = (np.exp(x1 / ec.b) * ej[:, None] * ec.DeltaT * fac1 * (h1[:, None] * GLW[None, :])).sum(axis=1)
    part2 = (np.exp(-x2 / ec.b) * ej[:, None] * ec.DeltaT * fac2 * (h2[:, None] * GLW[None, :])).sum(axis=1)
    W1 = sch.cum1[theta, j] + part1
    W2 = sch.suf2[theta, j + 1] + part2
    return (np.exp(-q / ec.b) * W1 + np.exp(q / ec.b) * W2) / (2.0 * ec.b)


def payoff(sch: Schedule, theta: int, q: np.ndarray | float) -> np.ndarray:
    """U_theta(q): H earns q I_H(q) - k|q|; L earns -q I_L(q) - k|q|."""
    qa = np.atleast_1d(np.asarray(q, dtype=float))
    sign = 1.0 if theta == 0 else -1.0
    return sign * qa * _I(sch, theta, qa) - sch.ec.k * np.abs(qa)


QGRID_H = np.linspace(0.0, 1.0, 101)
QGRID_L = np.linspace(-1.0, 0.0, 101)


def _zoom_max(sch: Schedule, theta: int, lo: float, hi: float, levels: int = 6) -> tuple[float, float]:
    """Maximise the payoff on [lo, hi] by repeated 17-point zoom. Robust to kinks."""
    best_q, best_u = lo, -math.inf
    for _ in range(levels):
        pts = np.linspace(lo, hi, 17)
        vals = payoff(sch, theta, pts)
        j = int(vals.argmax())
        if vals[j] > best_u:
            best_q, best_u = float(pts[j]), float(vals[j])
        lo, hi = float(pts[max(j - 1, 0)]), float(pts[min(j + 1, 16)])
    return best_q, best_u


def best_response(sch: Schedule, theta: int, ncand: int = 3) -> tuple[float, float]:
    """Global best response on the correct-sign half of [-1, 1]; wrong-sign orders lose at least k|q|.

    A 101-point grid finds the local maxima. Each of the best `ncand` is refined by a zoom search.
    Returns (order, payoff). Zero is always available and earns zero.
    """
    grid = QGRID_H if theta == 0 else QGRID_L
    u = payoff(sch, theta, grid)
    n = len(grid)
    cand = [i for i in range(n) if (i == 0 or u[i] >= u[i - 1]) and (i == n - 1 or u[i] >= u[i + 1])]
    cand.sort(key=lambda i: -u[i])
    step = float(grid[1] - grid[0])
    best_q, best_u = 0.0, 0.0
    for i in cand[:ncand]:
        q_try, u_try = _zoom_max(sch, theta, max(grid[0], float(grid[i]) - step), min(grid[-1], float(grid[i]) + step))
        if u_try > best_u + 1e-15:
            best_q, best_u = q_try, u_try
    return best_q, best_u


def regret(sch: Schedule, qH: float, qL: float) -> tuple[float, float]:
    """Gain from a global best response over the profile's own pure orders."""
    _, uH = best_response(sch, 0)
    _, uL = best_response(sch, 1)
    own_H = float(payoff(sch, 0, qH)[0])
    own_L = float(payoff(sch, 1, qL)[0])
    return max(0.0, uH - own_H), max(0.0, uL - own_L)


# ----------------------------------------------------------------------------------------------
# outcomes
# ----------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Outcome:
    eH: float
    eL: float
    E: float
    O_H: float
    pool_prob: float
    pool_belief: float
    var_mu: float          # E[(mu_P - 1/2)^2], zero iff the price is uninformative
    mu_min: float          # smallest posterior on the entry set (nan if none)
    entry_set_prob: float


def outcome(sch: Schedule) -> Outcome:
    ec, prof = sch.ec, sch.prof
    eH = eL = 0.0
    var = 0.0
    mus = []
    prob_A = 0.0
    for j in range(len(sch.e)):
        a, c = float(sch.edges[j]), float(sch.edges[j + 1])
        pH = mass(ec, prof.H, a, c)
        pL = mass(ec, prof.L, a, c)
        eH += sch.e[j] * pH
        eL += sch.e[j] * pL
        if sch.e[j] > 0.0:
            prob_A += 0.5 * (pH + pL)
            mu_n = mu_flow(ec, prof, sch.nodes[j])
            dens = 0.5 * (flow_density(ec, prof.H, sch.nodes[j]) + flow_density(ec, prof.L, sch.nodes[j]))
            var += float((((mu_n - 0.5) ** 2) * dens * sch.wts[j]).sum())
            if pH + pL > 1e-12:
                mus.append(float(mu_n.min()))
    pm = sch.pool_mass_H + sch.pool_mass_L
    mubar = pool_belief(sch)
    if pm > 1e-300:
        var += 0.5 * pm * (mubar - 0.5) ** 2
    return Outcome(eH=eH, eL=eL, E=0.5 * (eH + eL), O_H=0.5 * eH, pool_prob=0.5 * pm, pool_belief=mubar,
                   var_mu=var, mu_min=min(mus) if mus else float("nan"), entry_set_prob=prob_A)


def weak_entry(ec_weak: Econ) -> tuple[float, float]:
    """Entry and O_H at the weak strength: no trade, belief 1/2, entry G(B_r0(1/2))."""
    e = entry_at_belief(ec_weak, 0.5)
    return e, 0.5 * e


def no_trade_exists(ec: Econ) -> bool:
    """Proposition CD.4: an uninformative-price equilibrium exists iff Delta_T G(B_r(1/2)) <= 2k."""
    return ec.DeltaT * entry_at_belief(ec, 0.5) <= 2.0 * ec.k
