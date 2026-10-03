"""Shared model layer for the equilibrium-set track of the endogenous-insider fork.

Pure functions with type hints. Every function takes the primitive record first and returns
floats or immutable records. Nothing here writes files. Notation follows paper/main.md (4), (7),
(9), (A.4) and fork/endogenous_insider/mechanism.md (F.1) to (F.3).

Order strategies are finite-support distributions. An entry set is a finite union of closed
intervals (lo, hi) with hi possibly +inf. The integrals of (A.4) are evaluated piece by piece:
composite Gauss-Legendre on each smooth piece between breakpoints, and an exact exponential
formula on the far tail, where the posterior is constant.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

GL_NODES, GL_WEIGHTS = np.polynomial.legendre.leggauss(48)


@dataclass(frozen=True)
class Primitives:
    h: float
    ell: float
    p: float
    b: float
    k: float
    c: float


BENCH = Primitives(h=10.0, ell=1.0, p=0.5, b=2.0, k=0.02, c=6.0)


@dataclass(frozen=True)
class Acquisition:
    r: float
    t0: float
    tH: float
    tL: float
    gH: float
    gL: float
    DeltaT: float
    tau: float


@dataclass(frozen=True)
class Profile:
    """Finite-support conditional order distributions sigma_H and sigma_L."""
    qH: tuple[float, ...]
    wH: tuple[float, ...]
    qL: tuple[float, ...]
    wL: tuple[float, ...]


def pure(qH: float, qL: float) -> Profile:
    return Profile((qH,), (1.0,), (qL,), (1.0,))


def acquisition(par: Primitives, r: float) -> Acquisition:
    """Equation (4) and the threshold belief (F.1)."""
    t0 = par.p * (1.0 - par.p / r)
    tH = r / 2.0 + par.p ** 2 / (2.0 * r)
    tL = par.ell - (par.ell ** 2 - par.p ** 2) / (2.0 * r)
    gH = par.h - tH
    gL = (par.ell ** 2 - par.p ** 2) / (2.0 * r)
    return Acquisition(r, t0, tH, tL, gH, gL, tH - tL, (par.c - gL) / (gH - gL))


def m_bound(par: Primitives) -> float:
    return 1.0 / (1.0 + math.exp(2.0 / par.b))


def f(par: Primitives, z: np.ndarray | float) -> np.ndarray | float:
    return np.exp(-np.abs(z) / par.b) / (2.0 * par.b)


def F_Z(par: Primitives, z: float) -> float:
    return 0.5 * math.exp(z / par.b) if z <= 0 else 1.0 - 0.5 * math.exp(-z / par.b)


def density(par: Primitives, x: np.ndarray, qs: tuple[float, ...], ws: tuple[float, ...]) -> np.ndarray:
    out = np.zeros_like(np.asarray(x, dtype=float))
    for q, w in zip(qs, ws):
        out = out + w * f(par, np.asarray(x, dtype=float) - q)
    return out


def mu(par: Primitives, prof: Profile, x: np.ndarray) -> np.ndarray:
    """Order-flow posterior (7). Computed through log densities to avoid underflow in far tails."""
    x = np.asarray(x, dtype=float)
    lH = _logsum(par, x, prof.qH, prof.wH)
    lL = _logsum(par, x, prof.qL, prof.wL)
    return 1.0 / (1.0 + np.exp(lL - lH))


def _logsum(par: Primitives, x: np.ndarray, qs: tuple[float, ...], ws: tuple[float, ...]) -> np.ndarray:
    terms = np.stack([math.log(w) - np.abs(x - q) / par.b for q, w in zip(qs, ws) if w > 0.0])
    top = terms.max(axis=0)
    return top + np.log(np.exp(terms - top).sum(axis=0))


def support_hi(prof: Profile) -> float:
    return max(max(prof.qH), max(prof.qL))


def support_lo(prof: Profile) -> float:
    return min(min(prof.qH), min(prof.qL))


def mu_sup(par: Primitives, prof: Profile) -> float:
    """Posterior on the right plateau x >= every support point (its supremum for correctly signed profiles)."""
    return float(mu(par, prof, np.array([support_hi(prof) + 1.0]))[0])


def threshold_flow(par: Primitives, prof: Profile, tau: float) -> float:
    """Smallest x with mu_X(x) >= tau, for a profile with nondecreasing mu_X; +inf if none."""
    hi = support_hi(prof)
    if mu_sup(par, prof) < tau:
        return math.inf
    lo = support_lo(prof) - 1.0
    if float(mu(par, prof, np.array([lo]))[0]) >= tau:
        return -math.inf
    a, z = lo, hi + 1e-12
    for _ in range(200):
        mid = 0.5 * (a + z)
        if float(mu(par, prof, np.array([mid]))[0]) >= tau:
            z = mid
        else:
            a = mid
        if z - a < 1e-15:
            break
    return z


def _piece_integral(par: Primitives, prof: Profile, theta: str, q: float, lo: float, hi: float) -> float:
    """int_lo^hi f(x - q) w_theta(x) dx on a smooth piece, w_H = 1 - mu, w_L = mu."""
    if hi <= lo:
        return 0.0
    n_sub = max(1, int(math.ceil((hi - lo) / 0.5)))
    edges = np.linspace(lo, hi, n_sub + 1)
    total = 0.0
    for a, z in zip(edges[:-1], edges[1:]):
        x = 0.5 * (z - a) * GL_NODES + 0.5 * (z + a)
        m_x = mu(par, prof, x)
        w = (1.0 - m_x) if theta == "H" else m_x
        total += 0.5 * (z - a) * float(np.dot(GL_WEIGHTS, f(par, x - q) * w))
    return total


def residual_integral(par: Primitives, prof: Profile, entry: tuple[tuple[float, float], ...],
                      theta: str, q: float) -> float:
    """int_A f(x - q) w_theta(x) dx, with w_H = 1 - mu_X and w_L = mu_X (Lemma F.1(d) divided by Delta_T)."""
    hi_sup = max(support_hi(prof), q)
    lo_sup = min(support_lo(prof), q)
    breaks = sorted(set(list(prof.qH) + list(prof.qL) + [q]))
    total = 0.0
    for lo, hi in entry:
        # left far tail: x <= lo_sup, posterior constant, density exponential
        if lo < lo_sup:
            a, z = lo, min(hi, lo_sup)
            m_left = float(mu(par, prof, np.array([lo_sup - 1.0]))[0])
            w = (1.0 - m_left) if theta == "H" else m_left
            # int_a^z f(x-q) dx with x <= q: 0.5*(e^{(z-q)/b} - e^{(a-q)/b})
            ea = 0.0 if a == -math.inf else math.exp((a - q) / par.b)
            total += w * 0.5 * (math.exp((z - q) / par.b) - ea)
        # middle region between lo_sup and hi_sup, split at breakpoints
        a0, z0 = max(lo, lo_sup), min(hi, hi_sup)
        if z0 > a0:
            pts = [a0] + [t for t in breaks if a0 < t < z0] + [z0]
            for a, z in zip(pts[:-1], pts[1:]):
                total += _piece_integral(par, prof, theta, q, a, z)
        # right far tail: x >= hi_sup
        if hi > hi_sup:
            a, z = max(lo, hi_sup), hi
            m_right = mu_sup(par, prof)
            w = (1.0 - m_right) if theta == "H" else m_right
            ez = 0.0 if z == math.inf else math.exp(-(z - q) / par.b)
            total += w * 0.5 * (math.exp(-(a - q) / par.b) - ez)
    return total


def order_payoff(par: Primitives, acq: Acquisition, prof: Profile,
                 entry: tuple[tuple[float, float], ...], theta: str, q: float) -> float:
    """Expected trading profit of type theta from order q against the fixed schedule (P, e).

    E[V_T | theta, x] - P(x) = 1_A(x) Delta_T (1{theta=H} - mu_X(x)), so
    Pi_H(q) = q Delta_T int_A f(x-q)(1-mu) - k|q| and Pi_L(q) = -q Delta_T int_A f(x-q) mu - k|q|.
    """
    integ = residual_integral(par, prof, entry, theta, q)
    sign = 1.0 if theta == "H" else -1.0
    return sign * q * acq.DeltaT * integ - par.k * abs(q)


def payoff_curve(par: Primitives, acq: Acquisition, prof: Profile, entry: tuple[tuple[float, float], ...],
                 theta: str, grid: np.ndarray) -> np.ndarray:
    return np.array([order_payoff(par, acq, prof, entry, theta, float(q)) for q in grid])


def best_response(par: Primitives, acq: Acquisition, prof: Profile, entry: tuple[tuple[float, float], ...],
                  theta: str, n_grid: int = 201, refine: int = 3) -> tuple[float, float, np.ndarray, np.ndarray]:
    """Global maximizer on [-1, 1] for the correctly signed half (wrong signs are dominated, Lemma ES.2).

    Returns (argmax, max, grid, values). The grid includes 0 and the corner 1 (or -1). Local refinement
    by golden-section search on every grid local maximum.
    """
    sgn = 1.0 if theta == "H" else -1.0
    s_grid = np.linspace(0.0, 1.0, n_grid)
    vals = np.array([order_payoff(par, acq, prof, entry, theta, sgn * s) for s in s_grid])
    cands = [(0.0, 0.0), (1.0, float(vals[-1]))]
    # the end cells: a maximizer just inside a corner is not a grid local maximum
    for a, z in ((s_grid[-2], 1.0), (0.0, s_grid[1])):
        cands.append(_golden(lambda s: order_payoff(par, acq, prof, entry, theta, sgn * s), a, z))
    for i in range(1, n_grid - 1):
        if vals[i] >= vals[i - 1] and vals[i] >= vals[i + 1]:
            a, z = s_grid[i - 1], s_grid[i + 1]
            s_best, v_best = _golden(lambda s: order_payoff(par, acq, prof, entry, theta, sgn * s), a, z)
            cands.append((s_best, v_best))
    s_star, v_star = max(cands, key=lambda t: t[1])
    if v_star <= 0.0:
        s_star, v_star = 0.0, 0.0
    return sgn * s_star, v_star, sgn * s_grid, vals


def _golden(fun, a: float, z: float, tol: float = 1e-11) -> tuple[float, float]:
    g = (math.sqrt(5.0) - 1.0) / 2.0
    c, d = z - g * (z - a), a + g * (z - a)
    fc, fd = fun(c), fun(d)
    while z - a > tol:
        if fc > fd:
            z, d, fd = d, c, fc
            c = z - g * (z - a)
            fc = fun(c)
        else:
            a, c, fc = c, d, fd
            d = a + g * (z - a)
            fd = fun(d)
    s = 0.5 * (a + z)
    return s, fun(s)


def pool_posterior(par: Primitives, prof: Profile, entry: tuple[tuple[float, float], ...]) -> tuple[float, float]:
    """(Pr(H | X in N), Pr(X in N)) for the pool N = complement of the entry set."""
    eH = state_entry(par, prof, entry, "H")
    eL = state_entry(par, prof, entry, "L")
    nH, nL = 1.0 - eH, 1.0 - eL
    if nH + nL <= 0.0:
        return math.nan, 0.0
    return nH / (nH + nL), 0.5 * (nH + nL)


def _cdf_mix(par: Primitives, x: float, qs: tuple[float, ...], ws: tuple[float, ...]) -> float:
    if x == math.inf:
        return 1.0
    if x == -math.inf:
        return 0.0
    return sum(w * F_Z(par, x - q) for q, w in zip(qs, ws))


def state_entry(par: Primitives, prof: Profile, entry: tuple[tuple[float, float], ...], theta: str) -> float:
    """e_theta = Pr(X in A | theta)."""
    qs, ws = (prof.qH, prof.wH) if theta == "H" else (prof.qL, prof.wL)
    return sum(_cdf_mix(par, hi, qs, ws) - _cdf_mix(par, lo, qs, ws) for lo, hi in entry)


def minimal_entry(par: Primitives, acq: Acquisition, prof: Profile) -> tuple[tuple[float, float], ...]:
    xs = threshold_flow(par, prof, acq.tau)
    return () if xs == math.inf else ((xs, math.inf),)


def frak_r(par: Primitives, d: float) -> float:
    """(A.10): the root above ell of Delta_T(r) = d."""
    return par.ell + d + math.sqrt(d * d + 2.0 * par.ell * d)


def r_ceiling(par: Primitives) -> float:
    """(A.11) with c_H replaced by c."""
    M = 1.0 - m_bound(par)
    a = M * par.h - par.c
    return (a + math.sqrt(a * a + M * ((1.0 - M) * par.ell ** 2 - par.p ** 2))) / M


# ---------------------------------------------------------------------------------------------
# Closed forms used by the solvers (derivations in note.md, Lemma ES.1 and Section 4.4).
# ---------------------------------------------------------------------------------------------

def logit(x: float) -> float:
    return math.log(x / (1.0 - x))


def n_edge(par: Primitives, r: float) -> float:
    """n(r) = b logit tau(r) - 1: the smallest low-type magnitude z with entry under orders (1, -z)."""
    return par.b * logit(acquisition(par, r).tau) - 1.0


def J_closed(par: Primitives, r: float) -> float:
    """(ES.1): J(r) = Delta_T [m/2 + (e^{-1/b}/2)(atan e^{1/b} - atan sqrt(tau/(1-tau)))]."""
    acq = acquisition(par, r)
    tau = min(acq.tau, 1.0 - m_bound(par))
    u = math.sqrt(tau / (1.0 - tau))
    return acq.DeltaT * (m_bound(par) / 2.0
                         + math.exp(-1.0 / par.b) / 2.0 * (math.atan(math.exp(1.0 / par.b)) - math.atan(u)))


def C_low(par: Primitives, r: float, z: float) -> float:
    """(ES.2): Delta_T int_{x*}^inf f(x) mu_X(x) dx under orders (1, -z) and the minimal pool.

    The low type's correctly signed payoff against that schedule is U_L(s) = s (C e^{-s/b} - k).
    Requires z >= n(r), so that x* <= 1.
    """
    acq = acquisition(par, r)
    b = par.b
    root_kappa = math.exp((1.0 - z) / (2.0 * b))
    Mz = 1.0 / (1.0 + math.exp(-(1.0 + z) / b))
    diff = math.atan(math.exp((1.0 + z) / (2.0 * b))) - math.atan(math.sqrt(acq.tau / (1.0 - acq.tau)))
    return acq.DeltaT * (max(diff, 0.0) / (2.0 * root_kappa) + Mz * math.exp(-1.0 / b) / 2.0)


def psi(par: Primitives, r: float, z: float) -> float:
    """(ES.3): Psi(z, r) = C(z, r) e^{-z/b} (1 - z/b) - k, the low type's marginal profit at its own order."""
    return C_low(par, r, z) * math.exp(-z / par.b) * (1.0 - z / par.b) - par.k


def low_best_magnitude(par: Primitives, C: float) -> float:
    """argmax_{s in [0,1]} s (C e^{-s/b} - k); unique because the objective is strictly concave."""
    if C <= par.k:
        return 0.0
    g = lambda s: C * math.exp(-s / par.b) * (1.0 - s / par.b) - par.k
    if g(1.0) >= 0.0:
        return 1.0
    a, z = 0.0, 1.0
    for _ in range(200):
        mid = 0.5 * (a + z)
        if g(mid) > 0.0:
            a = mid
        else:
            z = mid
    return 0.5 * (a + z)


def edge_G(par: Primitives, r: float) -> float:
    """(ES.4): G(r) = Delta_T (1 - tau)/2 (1 + 1/b - logit tau) - k = Psi(n(r), r)."""
    acq = acquisition(par, r)
    return acq.DeltaT * (1.0 - acq.tau) / 2.0 * (1.0 + 1.0 / par.b - logit(acq.tau)) - par.k
