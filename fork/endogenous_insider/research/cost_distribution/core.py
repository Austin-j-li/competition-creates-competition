"""Core objects for the cost-distribution track of the endogenous-insider fork.

One preparation-cost CDF G replaces the benchmark's two-point cost and the fork's point mass. Under the
tie rule an indifferent challenger prepares, so entry at a revealed belief mu is G(B_r(mu)) = Pr(C <= B_r(mu)),
with G right-continuous. Every function takes the parameter record first and returns floats, arrays, or
frozen records. Nothing here writes files. Closed forms are used where the note derives them; the rest is
adaptive quadrature, so every number this module returns is a numerical diagnostic unless a separate
certificate encloses it.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy import integrate, optimize


@dataclass(frozen=True)
class Primitives:
    """Benchmark primitives of the paper without the cost law: values, reserve, noise scale, trading cost."""
    h: float = 10.0
    ell: float = 1.0
    p: float = 0.5
    b: float = 2.0
    k: float = 0.02


@dataclass(frozen=True)
class Payoffs:
    """Acquisition-stage payoffs (4) at incumbent strength r."""
    r: float
    t0: float
    tH: float
    tL: float
    gH: float
    gL: float
    DeltaT: float
    wL: float


@dataclass(frozen=True)
class CostLaw:
    """A preparation-cost law: finitely many atoms plus finitely many uniform components.

    atoms: (location, mass) pairs. uniforms: (lo, hi, mass) triples with lo < hi. Masses sum to one.
    """
    label: str
    atoms: tuple[tuple[float, float], ...] = ()
    uniforms: tuple[tuple[float, float, float], ...] = ()


@dataclass(frozen=True)
class FullOrderOutcome:
    """Full orders (1,-1) with the half-line pool N = Z_0 union (-inf, cutoff)."""
    cutoff: float          # requested pool upper end; -inf means the minimal pool
    z0: float              # upper end of the forced pool Z_0 = {x : G(B_r(mu_X(x))) = 0}; -inf if empty
    pool_end: float        # max(cutoff, z0)
    pool_prob: float       # Pr(X in N)
    pool_belief: float     # Pr(H | X in N); nan if the pool is empty
    pool_consistent: bool  # G(B_r(pool_belief)) == 0, or empty pool
    J: float               # existence statistic (A.7) = F_H(1) = F_L(1)
    sufficient_test: bool  # k < (1 - 1/b) J
    eH: float
    eL: float
    E: float
    O_H: float
    U: float               # J - k, the full-order investor payoff in either state
    materiality_ex_ante: float  # Delta_T * E
    materiality_min_price: float  # smallest materiality over realized prices


# ----------------------------------------------------------------------------------------------
# primitives
# ----------------------------------------------------------------------------------------------

def payoffs(prim: Primitives, r: float) -> Payoffs:
    """Equation (4) for the uniform incumbent on [0, r] with 0 < p < ell < r < h."""
    t0 = prim.p * (1.0 - prim.p / r)
    tH = r / 2.0 + prim.p ** 2 / (2.0 * r)
    tL = prim.ell - (prim.ell ** 2 - prim.p ** 2) / (2.0 * r)
    gH = prim.h - tH
    gL = (prim.ell ** 2 - prim.p ** 2) / (2.0 * r)
    return Payoffs(r=r, t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, DeltaT=tH - tL, wL=tL - t0)


def m_bound(prim: Primitives) -> float:
    return 1.0 / (1.0 + math.exp(2.0 / prim.b))


def M_bound(prim: Primitives) -> float:
    return 1.0 - m_bound(prim)


def gross_profit(prim: Primitives, pay: Payoffs, mu: float | np.ndarray) -> float | np.ndarray:
    """B_r(mu) = g_L + mu (g_H - g_L)."""
    return pay.gL + mu * (pay.gH - pay.gL)


def belief_for_profit(prim: Primitives, pay: Payoffs, y: float) -> float:
    """Inverse of B_r: the belief at which gross profit equals y."""
    return (y - pay.gL) / (pay.gH - pay.gL)


def frak_r(prim: Primitives, d: float) -> float:
    """(A.10): the strength above ell at which Delta_T(r) = d."""
    return prim.ell + d + math.sqrt(d * d + 2.0 * prim.ell * d)


def ceiling_strength(prim: Primitives, c: float) -> float:
    """(A.11) with c_H replaced by c: the strength at which B_r(M) = c."""
    M = M_bound(prim)
    a = M * prim.h - c
    return (a + math.sqrt(a * a + M * ((1.0 - M) * prim.ell ** 2 - prim.p ** 2))) / M


# ----------------------------------------------------------------------------------------------
# cost laws
# ----------------------------------------------------------------------------------------------

def cost_cdf(prim: Primitives, law: CostLaw, y: float | np.ndarray) -> float | np.ndarray:
    """G(y) = Pr(C <= y), right-continuous, so the tie rule is built in."""
    y_arr = np.asarray(y, dtype=float)
    out = np.zeros_like(y_arr)
    for loc, mass in law.atoms:
        out = out + mass * (y_arr >= loc)
    for lo, hi, mass in law.uniforms:
        out = out + mass * np.clip((y_arr - lo) / (hi - lo), 0.0, 1.0)
    return float(out) if np.ndim(out) == 0 else out


def lowest_cost(prim: Primitives, law: CostLaw) -> tuple[float, bool]:
    """c_0 = inf supp G, and whether G has an atom at c_0."""
    locs = [loc for loc, mass in law.atoms if mass > 0] + [lo for lo, _, mass in law.uniforms if mass > 0]
    c0 = min(locs)
    atom = any(loc == c0 and mass > 0 for loc, mass in law.atoms)
    return c0, atom


def entry_at_belief(prim: Primitives, pay: Payoffs, law: CostLaw, mu: float | np.ndarray) -> float | np.ndarray:
    """e(mu) = G(B_r(mu))."""
    return cost_cdf(prim, law, gross_profit(prim, pay, mu))


def regime(prim: Primitives, pay: Payoffs, law: CostLaw) -> str:
    """Regime of Theorem C.3 from G at the three profit levels B_r(m) < B_r(1/2) < B_r(M)."""
    g_m = entry_at_belief(prim, pay, law, m_bound(prim))
    g_half = entry_at_belief(prim, pay, law, 0.5)
    g_M = entry_at_belief(prim, pay, law, M_bound(prim))
    if g_m > 0.0:
        return "I floor"
    if g_half > 0.0:
        return "II prior entry"
    if g_M > 0.0:
        return "III price-gated entry"
    return "IV no entry"


def no_trade_exists(prim: Primitives, pay: Payoffs, law: CostLaw) -> bool:
    """Proposition C.4: an uninformative-price equilibrium exists iff Delta_T G(B_r(1/2)) <= 2k."""
    return pay.DeltaT * entry_at_belief(prim, pay, law, 0.5) <= 2.0 * prim.k


def full_orders_unique_sufficient(prim: Primitives, pay: Payoffs, law: CostLaw) -> bool:
    """Proposition C.5(iii): k < (1 - 1/b) m Delta_T G(B_r(m)) forces full orders in every equilibrium."""
    m = m_bound(prim)
    return prim.k < (1.0 - 1.0 / prim.b) * m * pay.DeltaT * entry_at_belief(prim, pay, law, m)


def mass_needed_no_trade_removed(prim: Primitives, pay: Payoffs) -> float:
    """Smallest G(B_r(1/2)) that removes every uninformative-price equilibrium: 2k / Delta_T (strict excess)."""
    return 2.0 * prim.k / pay.DeltaT


def mass_needed_unique_full(prim: Primitives, pay: Payoffs) -> float:
    """G(B_r(m)) above this forces full orders: k / ((1 - 1/b) m Delta_T)."""
    return prim.k / ((1.0 - 1.0 / prim.b) * m_bound(prim) * pay.DeltaT)


# ----------------------------------------------------------------------------------------------
# full orders (1, -1): posterior, pools, existence statistic, outcomes
# ----------------------------------------------------------------------------------------------

def noise_cdf(prim: Primitives, z: float) -> float:
    b = prim.b
    return 0.5 * math.exp(z / b) if z <= 0.0 else 1.0 - 0.5 * math.exp(-z / b)


def noise_density(prim: Primitives, z: float | np.ndarray) -> float | np.ndarray:
    return np.exp(-np.abs(z) / prim.b) / (2.0 * prim.b)


def mu_full(prim: Primitives, x: float | np.ndarray) -> float | np.ndarray:
    """(A.8): posterior under full orders."""
    return 1.0 / (1.0 + np.exp(-(np.abs(np.asarray(x) + 1.0) - np.abs(np.asarray(x) - 1.0)) / prim.b))


def flow_for_belief(prim: Primitives, mu: float) -> float:
    """Inverse of (A.8) on (-1, 1): x = (b/2) logit(mu)."""
    return 0.5 * prim.b * math.log(mu / (1.0 - mu))


def half_line_pool_belief(prim: Primitives, cutoff: float) -> float:
    """(F.2) under full orders: Pr(H | X < cutoff)."""
    a = noise_cdf(prim, cutoff - 1.0)
    c = noise_cdf(prim, cutoff + 1.0)
    return a / (a + c)


def zero_entry_belief(prim: Primitives, pay: Payoffs, law: CostLaw) -> tuple[float, bool]:
    """mu_0 = sup{mu : G(B_r(mu)) = 0} and whether mu_0 itself has G = 0 (closed zero set)."""
    c0, atom = lowest_cost(prim, law)
    return belief_for_profit(prim, pay, c0), not atom


def forced_pool_end(prim: Primitives, pay: Payoffs, law: CostLaw) -> float:
    """z_0: upper end of Z_0 = {x : G(B_r(mu_X(x))) = 0} under full orders; -inf if Z_0 is empty, +inf if all."""
    m, M = m_bound(prim), M_bound(prim)
    if entry_at_belief(prim, pay, law, m) > 0.0:
        return -math.inf
    if entry_at_belief(prim, pay, law, M) == 0.0:
        return math.inf
    mu0, _ = zero_entry_belief(prim, pay, law)
    if mu0 <= m:
        return -1.0
    return flow_for_belief(prim, mu0)


def largest_consistent_cutoff(prim: Primitives, pay: Payoffs, law: CostLaw) -> float:
    """Sup of half-line cutoffs x' with G(B_r(Pr(H | X < x'))) = 0; +inf when mu_0 >= 1/2, -inf when no pool."""
    m = m_bound(prim)
    if entry_at_belief(prim, pay, law, m) > 0.0:
        return -math.inf
    mu0, _ = zero_entry_belief(prim, pay, law)
    if mu0 >= 0.5:
        return math.inf
    if mu0 <= m:
        return -1.0
    return optimize.brentq(lambda x: half_line_pool_belief(prim, x) - mu0, -1.0, 200.0, xtol=1e-14, rtol=1e-14)


def _breakpoints_mu(prim: Primitives, pay: Payoffs, law: CostLaw, lo: float, hi: float) -> list[float]:
    pts = [belief_for_profit(prim, pay, loc) for loc, _ in law.atoms]
    for a, b_, _ in law.uniforms:
        pts += [belief_for_profit(prim, pay, a), belief_for_profit(prim, pay, b_)]
    return sorted(p for p in pts if lo < p < hi)


def J_statistic(prim: Primitives, pay: Payoffs, law: CostLaw, cutoff: float = -math.inf) -> float:
    """Existence statistic (A.7) for full orders and pool N = Z_0 union (-inf, cutoff).

    Arcsine representation (Lemma C.6):
      J = Delta_T [ G(B(m)) m (1/2 - F_Z(x'+1)) 1{x' < -1}
                    + (e^{-1/b}/4) int_{max(m, mu(x'))}^{M} G(B(mu)) dmu / sqrt(mu (1-mu))   (x' < 1)
                    + G(B(M)) m S_Z(max(x', 1) - 1) ].
    On the forced pool Z_0 the integrand is zero, so the minimal pool needs no special case.
    """
    b = prim.b
    m, M = m_bound(prim), M_bound(prim)
    total = 0.0
    g_m = entry_at_belief(prim, pay, law, m)
    g_M = entry_at_belief(prim, pay, law, M)
    if cutoff < -1.0:
        tail = 0.5 if cutoff == -math.inf else 0.5 - noise_cdf(prim, cutoff + 1.0)
        total += g_m * m * tail
    if cutoff < 1.0:
        mu_lo = m if cutoff <= -1.0 else float(mu_full(prim, cutoff))
        pts = _breakpoints_mu(prim, pay, law, mu_lo, M)
        grid = [mu_lo] + pts + [M]
        mid = 0.0
        for a, c in zip(grid[:-1], grid[1:]):
            val, _ = integrate.quad(lambda u: float(entry_at_belief(prim, pay, law, u)) / math.sqrt(u * (1.0 - u)),
                                    a, c, epsabs=1e-14, epsrel=1e-12, limit=200)
            mid += val
        total += math.exp(-1.0 / b) / 4.0 * mid
    upper_start = max(cutoff, 1.0)
    total += g_M * m * 0.5 * math.exp(-(upper_start - 1.0) / b)
    return pay.DeltaT * total


def _state_entry(prim: Primitives, pay: Payoffs, law: CostLaw, start: float, shift: float) -> float:
    """Pr(entry | theta) = int_{start}^inf G(B(mu_X(x))) f(x - shift) dx under full orders; shift = +1 (H), -1 (L)."""
    b = prim.b
    m, M = m_bound(prim), M_bound(prim)
    out = 0.0
    if start < -1.0:
        lo_mass = noise_cdf(prim, -1.0 - shift) - (0.0 if start == -math.inf else noise_cdf(prim, start - shift))
        out += float(entry_at_belief(prim, pay, law, m)) * lo_mass
    a = max(start, -1.0)
    if a < 1.0:
        pts_mu = _breakpoints_mu(prim, pay, law, float(mu_full(prim, a)), M)
        pts_x = [flow_for_belief(prim, u) for u in pts_mu]
        grid = [a] + [x for x in pts_x if a < x < 1.0] + [1.0]
        for lo, hi in zip(grid[:-1], grid[1:]):
            val, _ = integrate.quad(lambda x: float(entry_at_belief(prim, pay, law, float(mu_full(prim, x))))
                                    * float(noise_density(prim, x - shift)), lo, hi, epsabs=1e-14, epsrel=1e-12,
                                    limit=200)
            out += val
    top = max(start, 1.0)
    out += float(entry_at_belief(prim, pay, law, M)) * (1.0 - noise_cdf(prim, top - shift))
    return out


def full_order_outcome(prim: Primitives, pay: Payoffs, law: CostLaw, cutoff: float = -math.inf) -> FullOrderOutcome:
    """Full orders with half-line pool N = Z_0 union (-inf, cutoff); challenger and market maker conditions checked."""
    z0 = forced_pool_end(prim, pay, law)
    end = max(cutoff, z0)
    if end == -math.inf:
        pool_prob, pool_belief, consistent = 0.0, float("nan"), True
    elif end == math.inf:
        pool_prob, pool_belief = 1.0, 0.5
        consistent = entry_at_belief(prim, pay, law, 0.5) == 0.0
    else:
        a, c = noise_cdf(prim, end - 1.0), noise_cdf(prim, end + 1.0)
        pool_prob, pool_belief = 0.5 * (a + c), a / (a + c)
        consistent = float(entry_at_belief(prim, pay, law, pool_belief)) == 0.0
    J = J_statistic(prim, pay, law, end)
    eH = _state_entry(prim, pay, law, end, 1.0) if end < math.inf else 0.0
    eL = _state_entry(prim, pay, law, end, -1.0) if end < math.inf else 0.0
    E = 0.5 * (eH + eL)
    m = m_bound(prim)
    min_mat = 0.0 if pool_prob > 0.0 else pay.DeltaT * float(entry_at_belief(prim, pay, law, m))
    return FullOrderOutcome(cutoff=cutoff, z0=z0, pool_end=end, pool_prob=pool_prob, pool_belief=pool_belief,
                            pool_consistent=consistent, J=J, sufficient_test=prim.k < (1.0 - 1.0 / prim.b) * J,
                            eH=eH, eL=eL, E=E, O_H=0.5 * eH, U=J - prim.k, materiality_ex_ante=pay.DeltaT * E,
                            materiality_min_price=min_mat)


def sufficient_cutoff_end(prim: Primitives, pay: Payoffs, law: CostLaw) -> float:
    """Largest half-line cutoff x' at which the sufficient full-order test k < (1-1/b) J(x') still holds."""
    z0 = forced_pool_end(prim, pay, law)
    start = max(z0, -60.0)
    g = lambda x: (1.0 - 1.0 / prim.b) * J_statistic(prim, pay, law, x) - prim.k  # noqa: E731
    if g(start) <= 0.0:
        return float("nan")
    hi = start + 1.0
    while g(hi) > 0.0:
        hi += 1.0
        if hi > 200.0:
            return math.inf
    return optimize.brentq(g, start, hi, xtol=1e-12)
