"""Information acquisition in the endogenous-insider fork: solver.

The investor pays kappa > 0 to learn theta before it trades. Acquisition is private and may be
mixed with probability lambda. In the main game (game A) a non-acquirer does not trade. In the
variant (game B) a non-acquirer may trade; this module evaluates that only as a deviation
against the lambda = 1 schedule.

Benchmark primitives of the fork: (h, ell, p, b, k, c) = (10, 1, 0.5, 2, 0.02, 6).

This module solves and writes CSV only. Renderers never solve. Every closed-form row is
labeled analytical; every grid fixed point is labeled numerical diagnostic. A node where the
search fails stays unresolved and is never replaced by zero.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import NamedTuple

import mpmath as mpm
import numpy as np

HERE = Path(__file__).resolve().parent
FORK = HERE.parents[1]

mpm.mp.dps = 30


class Primitives(NamedTuple):
    h: float
    ell: float
    p: float
    b: float
    k: float
    c: float


BENCH = Primitives(h=10.0, ell=1.0, p=0.5, b=2.0, k=0.02, c=6.0)


class Payoffs(NamedTuple):
    t0: float
    tH: float
    tL: float
    gH: float
    gL: float
    DeltaT: float
    wL: float
    B_half: float
    B_M: float
    tau: float


class Grid(NamedTuple):
    X: np.ndarray
    DX: float
    S: np.ndarray
    kernel: np.ndarray  # kernel[i, j] = f(X_j - S_i)


class Schedule(NamedTuple):
    r: float
    lam: float
    qH: float
    qL: float
    tau: float
    DeltaT: float
    mu: np.ndarray
    e: np.ndarray
    P: np.ndarray
    VH: np.ndarray
    VL: np.ndarray
    eH: float
    eL: float
    E: float
    x_star: float
    mubar: float
    pool_ok: bool


class FixedPoint(NamedTuple):
    r: float
    lam: float
    qH: float
    qL: float
    U_H: float
    U_L: float
    U: float
    eH: float
    eL: float
    E: float
    x_star: float
    mubar: float
    F_H1: float
    F_L1: float
    suff_test: bool
    iterations: int


# ----------------------------------------------------------------------------------------------
# Closed forms (analytical)
# ----------------------------------------------------------------------------------------------

def posterior_bounds(prim: Primitives) -> tuple[float, float]:
    """(m, M) of equation (7) of the paper."""
    m = 1.0 / (1.0 + math.exp(2.0 / prim.b))
    return m, 1.0 - m


def payoffs(prim: Primitives, r: float) -> Payoffs:
    """Acquisition payoffs (4) with one preparation cost c; tau is (F.1)."""
    t0 = prim.p * (1.0 - prim.p / r)
    tH = r / 2.0 + prim.p**2 / (2.0 * r)
    tL = prim.ell - (prim.ell**2 - prim.p**2) / (2.0 * r)
    gH = prim.h - tH
    gL = (prim.ell**2 - prim.p**2) / (2.0 * r)
    _, M = posterior_bounds(prim)
    return Payoffs(t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, DeltaT=tH - tL, wL=tL - t0,
                   B_half=gL + 0.5 * (gH - gL), B_M=gL + M * (gH - gL), tau=(prim.c - gL) / (gH - gL))


def M_lambda(prim: Primitives, lam: float) -> float:
    """Largest posterior any strategy can produce when the investor is informed with probability lam."""
    a, d = math.exp(1.0 / prim.b), math.exp(-1.0 / prim.b)
    return (lam * a + 1.0 - lam) / (lam * (a + d) + 2.0 * (1.0 - lam))


def lambda_min(prim: Primitives, r: float) -> float:
    """Smallest acquisition probability at which some price can reach tau. nan above the ceiling."""
    tau = payoffs(prim, r).tau
    _, M = posterior_bounds(prim)
    if tau > M:
        return float("nan")
    if tau <= 0.5:
        return 0.0
    a, d = math.exp(1.0 / prim.b), math.exp(-1.0 / prim.b)
    u = a + d - 2.0
    return (2.0 * tau - 1.0) / ((a - 1.0) - tau * u)


def gudermannian(u: float) -> float:
    return float(mpm.atan(mpm.sinh(mpm.mpf(u))))


def J_closed(prim: Primitives, r: float) -> float:
    """J(r) of (F.3) in closed form for Laplace noise, full orders, minimal pool.

    J = Delta_T [ m/2 + (e^{-1/b}/4) (gd(1/b) - gd(x*/b)) ], gd the Gudermannian, x* = (b/2) log(tau/(1-tau)).
    Defined when 1/2 < tau <= M. Returns nan otherwise.
    """
    pay = payoffs(prim, r)
    m, M = posterior_bounds(prim)
    if pay.tau > M or pay.tau <= 0.5:
        return float("nan")
    tau = mpm.mpf(pay.tau)
    b = mpm.mpf(prim.b)
    xs_over_b = mpm.log(tau / (1 - tau)) / 2
    bracket = mpm.atan(mpm.sinh(1 / b)) - mpm.atan(mpm.sinh(xs_over_b))
    val = mpm.mpf(pay.DeltaT) * (mpm.mpf(m) / 2 + mpm.exp(-1 / b) / 4 * bracket)
    return float(val)


def full_order_test_closed(prim: Primitives, r: float) -> bool:
    """Existence test of Proposition F.2(c): k < (1 - 1/b) J(r)."""
    J = J_closed(prim, r)
    return bool(np.isfinite(J) and prim.k < (1.0 - 1.0 / prim.b) * J)


def U_star_closed(prim: Primitives, r: float) -> float:
    """Investor's ex-ante live profit on the full-order branch: U* = J(r) - k. nan where J is undefined."""
    J = J_closed(prim, r)
    return float("nan") if not np.isfinite(J) else J - prim.k


def U_lower_envelope(prim: Primitives, r: float) -> float:
    """Plateau-only lower bound on the full-order branch: m Delta_T / 2 - k."""
    m, _ = posterior_bounds(prim)
    return m * payoffs(prim, r).DeltaT / 2.0 - prim.k


def U_upper_bound(prim: Primitives, r: float) -> float:
    """Upper bound on the investor's ex-ante profit in every equilibrium with entry (any lambda, any orders).

    On the entry set 1 - mu_X <= 1 - tau and mu_X <= M, so U_H <= (Delta_T (1 - tau) - k)_+ and
    U_L <= (Delta_T M - k)_+. Zero when no live equilibrium exists (tau > M or Delta_T < k).
    """
    pay = payoffs(prim, r)
    _, M = posterior_bounds(prim)
    if pay.tau > M or pay.DeltaT < prim.k:
        return 0.0
    uh = max(pay.DeltaT * (1.0 - pay.tau) - prim.k, 0.0)
    ul = max(pay.DeltaT * M - prim.k, 0.0)
    return 0.5 * (uh + ul)


class LambdaMinProfile(NamedTuple):
    U_H: float
    U_L: float
    U: float
    full_orders_optimal: bool


def U_at_lambda_min(prim: Primitives, r: float) -> LambdaMinProfile:
    """Investor's profit at lambda = lambda_min(r), full orders, entry on the plateau x >= 1 only.

    U_H = Delta_T (1 - tau)/2 - k; U_L = Delta_T tau e^{-2/b}/2 - k. Full orders are globally optimal
    for both types when Delta_T (1 - tau) e^{-1/b}/2 > k and Delta_T tau e^{-2/b} (1 - 1/b)/2 > k.
    """
    pay = payoffs(prim, r)
    b = prim.b
    UH = pay.DeltaT * (1.0 - pay.tau) / 2.0 - prim.k
    UL = pay.DeltaT * pay.tau * math.exp(-2.0 / b) / 2.0 - prim.k
    okH = pay.DeltaT * (1.0 - pay.tau) * math.exp(-1.0 / b) / 2.0 > prim.k
    okL = pay.DeltaT * pay.tau * math.exp(-2.0 / b) * (1.0 - 1.0 / b) / 2.0 > prim.k
    return LambdaMinProfile(U_H=UH, U_L=UL, U=0.5 * (UH + UL), full_orders_optimal=bool(okH and okL))


class MonotonicityBounds(NamedTuple):
    r_a: float
    r_C: float
    tau_prime_bound: float
    growth_term_lower: float   # lower bound on Delta_T' G / Delta_T on [r_a, r_C]
    threshold_term_upper: float  # upper bound on |G'(tau) tau'| on [r_a, r_C]
    margin: float
    holds: bool


def monotonicity_bounds(prim: Primitives, r_a: float, r_C: float) -> MonotonicityBounds:
    """Closed-form bounds that prove dJ/dr > 0 on [r_a, r_C] when the margin is positive.

    J = Delta_T G(tau) with G >= m/2 and G'(tau) = -(e^{-1/b}/4) / sqrt(tau (1 - tau)).
    dJ/dr = Delta_T [ (Delta_T'/Delta_T) G + G'(tau) tau' ].
    Delta_T'/Delta_T = (r + ell)/(r (r - ell)) is decreasing in r, so its minimum on the interval is at r_C.
    tau' = N'/D + tau |D'|/D with N' = (ell^2 - p^2)/(2 r^2) <= (ell^2 - p^2)/(2 r_a^2), |D'| <= 1/2,
    tau <= M, D = g_H - g_L >= D(r_C). sqrt(tau (1 - tau)) >= sqrt(M m) = 1/(2 cosh(1/b)) on tau <= M.
    """
    m, M = posterior_bounds(prim)
    ell, p, b, h = prim.ell, prim.p, prim.b, prim.h
    D_rC = h - r_C / 2.0 - ell**2 / (2.0 * r_C)
    tau_prime_bound = ((ell**2 - p**2) / (2.0 * r_a**2) + M / 2.0) / D_rC
    growth_lower = (r_C + ell) / (r_C * (r_C - ell)) * m / 2.0
    threshold_upper = (math.exp(-1.0 / b) / 4.0) * tau_prime_bound * 2.0 * math.cosh(1.0 / b)
    margin = growth_lower - threshold_upper
    return MonotonicityBounds(r_a=r_a, r_C=r_C, tau_prime_bound=tau_prime_bound, growth_term_lower=growth_lower,
                              threshold_term_upper=threshold_upper, margin=margin, holds=bool(margin > 0.0))


def frak_r(prim: Primitives, d: float) -> float:
    """(A.10): the strength at which Delta_T(r) = d."""
    return prim.ell + d + math.sqrt(d * d + 2.0 * prim.ell * d)


def r_ceiling(prim: Primitives) -> float:
    """(A.11) with c_H replaced by c: B_r(M) = c."""
    _, M = posterior_bounds(prim)
    h, ell, p, c = prim.h, prim.ell, prim.p, prim.c
    return ((M * h - c) + math.sqrt((M * h - c) ** 2 + M * ((1 - M) * ell**2 - p**2))) / M


# ----------------------------------------------------------------------------------------------
# Grid continuation at acquisition probability lambda (numerical diagnostic)
# ----------------------------------------------------------------------------------------------

def laplace(prim: Primitives, z: np.ndarray) -> np.ndarray:
    return np.exp(-np.abs(z) / prim.b) / (2.0 * prim.b)


def make_grid(prim: Primitives, half_width: float = 30.0, n: int = 60001, n_orders: int = 201) -> Grid:
    X = np.linspace(-half_width, half_width, n)
    S = np.round(np.linspace(-1.0, 1.0, n_orders), 3)
    kernel = laplace(prim, X[None, :] - S[:, None])
    return Grid(X=X, DX=float(X[1] - X[0]), S=S, kernel=kernel)


def schedule(prim: Primitives, grid: Grid, r: float, lam: float, qH: float, qL: float,
             cutoff_floor: float = -np.inf) -> Schedule:
    """Candidate continuation at (r, lambda, orders): entry on {mu >= tau} intersected with [cutoff_floor, inf).

    The market maker's conditional flow densities are a_theta = lam f(x - q_theta) + (1 - lam) f(x):
    with probability 1 - lam the investor did not acquire and does not trade.
    """
    pay = payoffs(prim, r)
    X = grid.X
    aH = lam * laplace(prim, X - qH) + (1.0 - lam) * laplace(prim, X)
    aL = lam * laplace(prim, X - qL) + (1.0 - lam) * laplace(prim, X)
    mu = aH / (aH + aL)
    entry = (mu >= pay.tau) & (X >= cutoff_floor)
    e = entry.astype(float)
    pool = ~entry
    if pool.any():
        wH, wL = float(aH[pool].sum()), float(aL[pool].sum())
        mubar = wH / (wH + wL)
        pool_ok = bool(pay.gL + mubar * (pay.gH - pay.gL) < prim.c)
    else:
        mubar, pool_ok = float("nan"), True
    price = pay.t0 + e * (pay.wL + pay.DeltaT * mu)
    VH = pay.t0 + e * (pay.tH - pay.t0)
    VL = pay.t0 + e * (pay.tL - pay.t0)
    # entry probabilities conditional on theta for an informed investor at its equilibrium order
    eH = float((e * laplace(prim, X - qH)).sum() * grid.DX)
    eL = float((e * laplace(prim, X - qL)).sum() * grid.DX)
    x_star = float(X[entry][0]) if entry.any() else float("inf")
    return Schedule(r=r, lam=lam, qH=qH, qL=qL, tau=pay.tau, DeltaT=pay.DeltaT, mu=mu, e=e, P=price, VH=VH, VL=VL,
                    eH=eH, eL=eL, E=0.5 * (eH + eL), x_star=x_star, mubar=mubar, pool_ok=pool_ok)


def profit_curve(prim: Primitives, grid: Grid, gain: np.ndarray) -> np.ndarray:
    """Profit of every order on the coarse order grid against a fixed residual gain(x) = V(x) - P(x)."""
    return grid.S * (grid.kernel @ gain) * grid.DX - prim.k * np.abs(grid.S)


def best_response(prim: Primitives, grid: Grid, gain: np.ndarray) -> tuple[float, float]:
    """Best order and its profit; the zero order is always available and earns exactly zero."""
    coarse = profit_curve(prim, grid, gain)
    i = int(coarse.argmax())
    lo, hi = max(-1.0, grid.S[i] - 0.01), min(1.0, grid.S[i] + 0.01)
    fine = np.linspace(lo, hi, 41)
    vals = np.array([s * (laplace(prim, grid.X - s) * gain).sum() * grid.DX - prim.k * abs(s) for s in fine])
    j = int(vals.argmax())
    best, value = float(fine[j]), float(vals[j])
    if value <= 0.0:
        return 0.0, 0.0
    return best, value


def gross_full(prim: Primitives, grid: Grid, sch: Schedule) -> tuple[float, float]:
    """F_H(1) and F_L(1): gross profit per unit of the full correctly signed orders against the schedule."""
    X = grid.X
    FH = float((laplace(prim, X - 1.0) * (sch.VH - sch.P)).sum() * grid.DX)
    FL = float((laplace(prim, X + 1.0) * (sch.P - sch.VL)).sum() * grid.DX)
    return FH, FL


def fixed_point(prim: Primitives, grid: Grid, r: float, lam: float, qH0: float, qL0: float,
                cutoff_floor: float = -np.inf, max_iter: int = 80, tol: float = 5e-4) -> FixedPoint | None:
    """Best-response iteration on orders at fixed (r, lambda). None when no fixed point is reached."""
    qH, qL = qH0, qL0
    for it in range(1, max_iter + 1):
        sch = schedule(prim, grid, r, lam, qH, qL, cutoff_floor)
        # each type's residual is its own expected value minus the price; the low type's is negative on the
        # entry set, so its best response is a short order
        bH, uH = best_response(prim, grid, sch.VH - sch.P)
        bL, uL = best_response(prim, grid, sch.VL - sch.P)
        if abs(bH - qH) < tol and abs(bL - qL) < tol:
            if not sch.pool_ok:
                return None
            FH, FL = gross_full(prim, grid, sch)
            suff = bool(prim.k < (1.0 - 1.0 / prim.b) * min(FH, FL)) and abs(qH - 1.0) < tol and abs(qL + 1.0) < tol
            return FixedPoint(r=r, lam=lam, qH=qH, qL=qL, U_H=uH, U_L=uL, U=0.5 * (uH + uL), eH=sch.eH, eL=sch.eL,
                              E=sch.E, x_star=sch.x_star, mubar=sch.mubar, F_H1=FH, F_L1=FL, suff_test=suff,
                              iterations=it)
        qH, qL = bH, bL
    return None


class FullOrderQuad(NamedTuple):
    """Full-order minimal-pool continuation at (r, lambda) evaluated by quadrature with the exact threshold."""
    r: float
    lam: float
    x_star: float
    F_H1: float
    F_L1: float
    V: float
    eH: float
    eL: float
    E: float
    suff_test: bool


def posterior_full(prim: Primitives, lam: float, x: float) -> float:
    """mu^lambda_X(x) under full orders (1, -1) and acquisition probability lambda."""
    if x >= 1.0:
        return M_lambda(prim, lam)
    if x <= -1.0:
        return 1.0 - M_lambda(prim, lam)
    fH = math.exp(-abs(x - 1.0) / prim.b)
    fL = math.exp(-abs(x + 1.0) / prim.b)
    f0 = math.exp(-abs(x) / prim.b)
    aH = lam * fH + (1.0 - lam) * f0
    aL = lam * fL + (1.0 - lam) * f0
    return aH / (aH + aL)


def threshold_full(prim: Primitives, r: float, lam: float) -> float:
    """x*_lambda: the flow at which mu^lambda_X reaches tau under full orders; inf when none does."""
    from scipy.optimize import brentq

    tau = payoffs(prim, r).tau
    if tau > M_lambda(prim, lam):
        return float("inf")
    if tau <= 0.5:
        return -math.inf
    if posterior_full(prim, lam, 1.0) <= tau:
        return 1.0
    return float(brentq(lambda x: posterior_full(prim, lam, x) - tau, 0.0, 1.0, xtol=1e-14))


def full_order_quad(prim: Primitives, r: float, lam: float) -> FullOrderQuad:
    """F_H(1), F_L(1), entry and the sufficient test at full orders, by adaptive quadrature on [x*, inf)."""
    from scipy.integrate import quad

    pay = payoffs(prim, r)
    xs = threshold_full(prim, r, lam)
    if not np.isfinite(xs):
        return FullOrderQuad(r=r, lam=lam, x_star=xs, F_H1=float("nan"), F_L1=float("nan"), V=float("nan"),
                             eH=0.0, eL=0.0, E=0.0, suff_test=False)
    b = prim.b

    def fH(x: float) -> float:
        return math.exp(-abs(x - 1.0) / b) / (2.0 * b)

    def fL(x: float) -> float:
        return math.exp(-abs(x + 1.0) / b) / (2.0 * b)

    def gH(x: float) -> float:
        return fH(x) * (1.0 - posterior_full(prim, lam, x))

    def gL(x: float) -> float:
        return fL(x) * posterior_full(prim, lam, x)

    # the integrands are smooth on [x*, 1]; on [1, inf) the posterior is the constant M_lambda and the tails
    # integrate in closed form: int_1^inf f(x-1) dx = 1/2 and int_1^inf f(x+1) dx = e^{-2/b}/2
    Ml = M_lambda(prim, lam)
    IH = quad(gH, xs, 1.0, epsabs=1e-13, epsrel=1e-12)[0] + 0.5 * (1.0 - Ml)
    IL = quad(gL, xs, 1.0, epsabs=1e-13, epsrel=1e-12)[0] + 0.5 * math.exp(-2.0 / b) * Ml
    FH, FL = pay.DeltaT * IH, pay.DeltaT * IL
    eH = 0.5 * math.exp(-(xs - 1.0) / b) if xs >= 1.0 else 1.0 - 0.5 * math.exp((xs - 1.0) / b)
    eL = 0.5 * math.exp(-(xs + 1.0) / b)
    suff = bool(prim.k < (1.0 - 1.0 / b) * min(FH, FL))
    return FullOrderQuad(r=r, lam=lam, x_star=xs, F_H1=FH, F_L1=FL, V=0.5 * (FH + FL) - prim.k, eH=eH, eL=eL,
                         E=0.5 * (eH + eL), suff_test=suff)


class UninformedDeviation(NamedTuple):
    s: float
    profit: float
    Phi0: float


def uninformed_best(prim: Primitives, grid: Grid, sch: Schedule) -> UninformedDeviation:
    """Game B: best order of a non-acquirer who may trade, against a fixed schedule.

    Its own belief is 1/2 at every flow, so its residual is e(x) Delta_T (1/2 - mu(x)), nonpositive on the
    entry set. Phi0 is the marginal gross gain of a vanishing short.
    """
    gain = sch.e * sch.DeltaT * (0.5 - sch.mu)
    s, value = best_response(prim, grid, gain)
    Phi0 = float((laplace(prim, grid.X) * sch.e * sch.DeltaT * (sch.mu - 0.5)).sum() * grid.DX)
    return UninformedDeviation(s=s, profit=value, Phi0=Phi0)


# ----------------------------------------------------------------------------------------------
# CSV
# ----------------------------------------------------------------------------------------------

def fmt(v: object) -> str:
    if isinstance(v, (bool, np.bool_)):
        return "true" if v else "false"
    if isinstance(v, (float, np.floating)):
        if np.isnan(v):
            return "n/a"
        if np.isinf(v):
            return "inf" if v > 0 else "-inf"
        return repr(float(v))
    return str(v)


def write_csv(path: Path, columns: list[str], rows: list[dict]) -> Path:
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(columns)
        for row in rows:
            w.writerow([fmt(row.get(col, float("nan"))) for col in columns])
    return path


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


# ----------------------------------------------------------------------------------------------
# Exercises
# ----------------------------------------------------------------------------------------------

def r_grid_region() -> list[float]:
    pts = set(np.round(np.arange(1.20, 3.7001, 0.01), 4).tolist())
    pts.update([1.2, 2.05, 3.0, 3.5926, 3.5927, 3.6])
    return sorted(pts)


def exercise_region(prim: Primitives) -> list[dict]:
    """Closed-form objects of the insider region on a fine strength grid (analytical rows)."""
    m, M = posterior_bounds(prim)
    rows = []
    for r in r_grid_region():
        pay = payoffs(prim, r)
        J = J_closed(prim, r)
        full_ok = full_order_test_closed(prim, r)
        prof = U_at_lambda_min(prim, r)
        live_possible = bool(pay.tau <= M and pay.DeltaT >= prim.k and pay.B_half < prim.c)
        rows.append({
            "r": r, "tau": pay.tau, "DeltaT": pay.DeltaT, "B_half": pay.B_half, "B_M": pay.B_M,
            "dead_exists": pay.B_half < prim.c, "live_possible": live_possible,
            "lambda_min": lambda_min(prim, r), "J_closed": J,
            "full_order_test": full_ok,
            "U_star_closed": U_star_closed(prim, r) if full_ok else float("nan"),
            "U_lower_envelope": U_lower_envelope(prim, r) if (full_ok) else float("nan"),
            "U_upper_bound": U_upper_bound(prim, r),
            "U_H_lambda_min": prof.U_H if np.isfinite(J) else float("nan"),
            "U_L_lambda_min": prof.U_L if np.isfinite(J) else float("nan"),
            "U_lambda_min": prof.U if np.isfinite(J) else float("nan"),
            "lambda_min_full_orders_optimal": prof.full_orders_optimal if np.isfinite(J) else False,
            "status": "analytical",
        })
    return rows


def exercise_branch_uninformed(prim: Primitives, grid: Grid) -> list[dict]:
    """Game B deviation along the fork's lambda = 1 live branch, read from branches.csv (never re-solved here)."""
    rows = []
    for row in read_csv(FORK / "branches.csv"):
        if row["branch"] != "live" or row["exists"].strip().lower() != "true":
            continue
        r, qH, qL = float(row["r"]), float(row["qH"]), float(row["qL"])
        UH, UL = float(row["U_H"]), float(row["U_L"])
        sch = schedule(prim, grid, r, 1.0, qH, qL)
        dev = uninformed_best(prim, grid, sch)
        U_star = 0.5 * (UH + UL)
        rows.append({
            "r": r, "qH": qH, "qL": qL, "U_H": UH, "U_L": UL, "U_star": U_star,
            "U_star_closed": U_star_closed(prim, r) if (abs(qH - 1.0) < 1e-9 and abs(qL + 1.0) < 1e-9) else float("nan"),
            "x_star": sch.x_star, "E": sch.E,
            "Phi0": dev.Phi0, "s_uninformed": dev.s, "U_uninformed": dev.profit,
            "uninformed_short_profitable": dev.profit > 0.0,
            "kappa_max_gameA": U_star, "kappa_max_gameB": U_star - dev.profit,
            "status": "numerical diagnostic",
        })
    return rows


def lambda_grid(prim: Primitives, r: float, n: int = 26) -> list[float]:
    lmin = lambda_min(prim, r)
    pts = [max(lmin - 0.02, 0.0), lmin + 1e-6]
    pts.extend(np.linspace(lmin + 1e-6, 1.0, n)[1:].tolist())
    return pts


STARTS = ((1.0, -1.0), (1.0, -0.5), (1.0, -0.25), (0.5, -0.5))


def exercise_profiles(prim: Primitives, grid: Grid, strengths: tuple[float, ...]) -> list[dict]:
    """V(lambda, r) on the minimal-pool branch at fixed strengths.

    Each row carries the grid fixed point reached from the first start in STARTS that converges (numerical
    diagnostic) and, beside it, the quadrature evaluation of the full-order candidate with its sufficient test.
    """
    rows = []
    for r in strengths:
        lmin = lambda_min(prim, r)
        for lam in lambda_grid(prim, r):
            base = {"r": r, "lambda": lam, "lambda_min": lmin}
            if lam < lmin:
                rows.append({**base, "live": False, "qH": 0.0, "qL": 0.0, "x_star": float("inf"), "E": 0.0,
                             "U_H": 0.0, "U_L": 0.0, "U": 0.0, "F_H1": float("nan"), "F_L1": float("nan"),
                             "suff_test": False, "start": "n/a", "x_star_quad": float("inf"), "V_quad": 0.0,
                             "suff_test_quad": False,
                             "status": "analytical (no price reaches tau below lambda_min)"})
                continue
            q = full_order_quad(prim, r, lam)
            fp, start = None, "n/a"
            for qH0, qL0 in STARTS:
                cand = fixed_point(prim, grid, r, lam, qH0, qL0)
                if cand is not None and cand.E > 0.0:
                    fp, start = cand, f"({qH0:+.2f},{qL0:+.2f})"
                    break
            if fp is None:
                rows.append({**base, "live": False, "qH": float("nan"), "qL": float("nan"), "x_star": float("nan"),
                             "E": float("nan"), "U_H": float("nan"), "U_L": float("nan"), "U": float("nan"),
                             "F_H1": float("nan"), "F_L1": float("nan"), "suff_test": False, "start": "n/a",
                             "x_star_quad": q.x_star, "V_quad": q.V, "suff_test_quad": q.suff_test,
                             "status": "unresolved (no live fixed point from any start)"})
                continue
            rows.append({**base, "live": True, "qH": fp.qH, "qL": fp.qL, "x_star": fp.x_star, "E": fp.E,
                         "U_H": fp.U_H, "U_L": fp.U_L, "U": fp.U, "F_H1": fp.F_H1, "F_L1": fp.F_L1,
                         "suff_test": fp.suff_test, "start": start, "x_star_quad": q.x_star, "V_quad": q.V,
                         "suff_test_quad": q.suff_test,
                         "status": "numerical diagnostic" + ("; sufficient test holds" if fp.suff_test else "")})
    return rows


def exercise_profiles_quad(prim: Primitives, strengths: tuple[float, ...], n: int = 201) -> list[dict]:
    """Dense V(lambda, r) of the full-order candidate by quadrature, for the figure. Zero below lambda_min
    is analytical (no live continuation exists there); above it the row is a candidate whose investor
    optimality is certified by the sufficient test when suff_test is true."""
    rows = []
    for r in strengths:
        lmin = lambda_min(prim, r)
        lo = max(lmin - 0.05, 0.0)
        for lam in np.linspace(lo, 1.0, n).tolist() + [lmin, min(lmin + 1e-9, 1.0)]:
            if lam < lmin:
                rows.append({"r": r, "lambda": lam, "lambda_min": lmin, "x_star": float("inf"), "F_H1": float("nan"),
                             "F_L1": float("nan"), "V": 0.0, "E": 0.0, "suff_test": False,
                             "status": "analytical (no price reaches tau below lambda_min)"})
                continue
            q = full_order_quad(prim, r, lam)
            rows.append({"r": r, "lambda": lam, "lambda_min": lmin, "x_star": q.x_star, "F_H1": q.F_H1,
                         "F_L1": q.F_L1, "V": q.V, "E": q.E, "suff_test": q.suff_test,
                         "status": "quadrature; sufficient test " + ("holds" if q.suff_test else "fails")})
    return sorted(rows, key=lambda d: (d["r"], d["lambda"]))


def exercise_mixed_band(prim: Primitives, profiles: list[dict], quad: list[dict]) -> list[dict]:
    """For each strength: the range of V over lambda in [lambda_min, 1] on the full-order branch, which is the
    band of kappa with a mixed-acquisition equilibrium on this branch, and the sign pattern of dV/dlambda.

    The shape and the band come from the dense quadrature profile where the sufficient test holds; the grid
    fixed points at lambda_min and at 1 are reported beside them as cross-checks.
    """
    rows = []
    for r in sorted({row["r"] for row in quad}):
        qs = sorted([row for row in quad if row["r"] == r and row["lambda"] >= row["lambda_min"]
                     and row["suff_test"]], key=lambda d: d["lambda"])
        live = sorted([row for row in profiles if row["r"] == r and row["live"]], key=lambda d: d["lambda"])
        if not qs:
            continue
        lams = np.array([d["lambda"] for d in qs])
        Vs = np.array([d["V"] for d in qs])
        diffs = np.diff(Vs)
        n_up, n_down = int((diffs > 0).sum()), int((diffs < 0).sum())
        shape = "increasing" if n_down == 0 else "decreasing" if n_up == 0 else "non-monotone"
        prof = U_at_lambda_min(prim, r)
        rows.append({"r": r, "lambda_min": lambda_min(prim, r),
                     "lambda_suff_first": float(lams[0]),
                     "V_lambda_min_closed": prof.U, "V_lambda_min_full_orders_optimal": prof.full_orders_optimal,
                     "V_lambda_min_quad": float(Vs[0]), "V_one_quad": float(Vs[-1]),
                     "V_one_closed": U_star_closed(prim, r),
                     "V_lambda_min_grid": float(live[0]["U"]) if live else float("nan"),
                     "V_one_grid": float(live[-1]["U"]) if live else float("nan"),
                     "band_lo": float(Vs.min()), "band_hi": float(Vs.max()),
                     "lambda_at_min": float(lams[int(Vs.argmin())]), "lambda_at_max": float(lams[int(Vs.argmax())]),
                     "shape": shape, "band_width": float(Vs.max() - Vs.min()),
                     "relative_rise": float((Vs[-1] - Vs[0]) / Vs[-1]),
                     "mixed_stability": "repeller (V increasing through kappa)" if shape == "increasing"
                     else "attractor (V decreasing through kappa)" if shape == "decreasing" else "mixed",
                     "status": "numerical diagnostic"})
    return rows


def exercise_thresholds(prim: Primitives, region: list[dict], band: list[dict]) -> list[dict]:
    m, M = posterior_bounds(prim)
    rk = frak_r(prim, prim.k)
    rC = r_ceiling(prim)
    full_first = min(row["r"] for row in region if row["full_order_test"])
    mono = monotonicity_bounds(prim, full_first, rC)
    return [
        {"boundary": "trading_impossible_sufficient", "value": rk,
         "definition": "r(k): Delta_T(r) = k; below it D is the unique equilibrium at every kappa > 0 (Prop. 1 iv)"},
        {"boundary": "preparation_ceiling", "value": rC,
         "definition": "r_C: B_r(M) = c; above it D is the unique equilibrium at every kappa > 0 (Prop. 1 iii)"},
        {"boundary": "full_order_closed_form_first", "value": full_first,
         "definition": "first grid strength with k < (1 - 1/b) J(r), J in closed form"},
        {"boundary": "lambda_min_at_full_first", "value": lambda_min(prim, full_first),
         "definition": "dilution floor at the first full-order strength"},
        {"boundary": "lambda_min_at_r3", "value": lambda_min(prim, 3.0), "definition": "dilution floor at r = 3"},
        {"boundary": "U_star_at_r3", "value": U_star_closed(prim, 3.0),
         "definition": "kappa ceiling for pure acquisition at r = 3, game A, closed form"},
        {"boundary": "U_star_sup", "value": max(row["U_star_closed"] for row in region if row["full_order_test"]),
         "definition": "largest kappa with a pure-acquisition equilibrium on the full-order branch (attained just below r_C)"},
        {"boundary": "monotonicity_margin", "value": mono.margin,
         "definition": "growth term lower bound minus threshold term upper bound on [full_first, r_C]; positive proves dJ/dr > 0"},
        {"boundary": "m", "value": m, "definition": "lower posterior bound"},
        {"boundary": "M", "value": M, "definition": "upper posterior bound"},
    ]


def main() -> None:
    prim = BENCH
    grid = make_grid(prim)

    region = exercise_region(prim)
    write_csv(HERE / "insider_region.csv",
              ["r", "tau", "DeltaT", "B_half", "B_M", "dead_exists", "live_possible", "lambda_min", "J_closed",
               "full_order_test", "U_star_closed", "U_lower_envelope", "U_upper_bound", "U_H_lambda_min",
               "U_L_lambda_min", "U_lambda_min", "lambda_min_full_orders_optimal", "status"], region)
    print(f"insider_region.csv: {len(region)} rows", flush=True)

    branch = exercise_branch_uninformed(prim, grid)
    write_csv(HERE / "uninformed_short.csv",
              ["r", "qH", "qL", "U_H", "U_L", "U_star", "U_star_closed", "x_star", "E", "Phi0", "s_uninformed",
               "U_uninformed", "uninformed_short_profitable", "kappa_max_gameA", "kappa_max_gameB", "status"], branch)
    for row in branch:
        print(f"r={row['r']:.4f} U*={row['U_star']:.5f} closed={row['U_star_closed']!s:>10} "
              f"s_U={row['s_uninformed']:+.3f} U_U={row['U_uninformed']:.5f}", flush=True)

    strengths = (2.05, 2.5, 3.0, 3.5)
    profiles = exercise_profiles(prim, grid, strengths)
    write_csv(HERE / "acquisition_profile.csv",
              ["r", "lambda", "lambda_min", "live", "qH", "qL", "x_star", "E", "U_H", "U_L", "U", "F_H1", "F_L1",
               "suff_test", "start", "x_star_quad", "V_quad", "suff_test_quad", "status"], profiles)
    for row in profiles:
        print(f"r={row['r']:.2f} lam={row['lambda']:.4f} live={row['live']} q=({row['qH']},{row['qL']}) "
              f"E={row['E']} U={row['U']} V_quad={row['V_quad']} start={row['start']}", flush=True)

    quad = exercise_profiles_quad(prim, strengths)
    write_csv(HERE / "acquisition_profile_quad.csv",
              ["r", "lambda", "lambda_min", "x_star", "F_H1", "F_L1", "V", "E", "suff_test", "status"], quad)

    band = exercise_mixed_band(prim, profiles, quad)
    write_csv(HERE / "mixed_band.csv",
              ["r", "lambda_min", "lambda_suff_first", "V_lambda_min_closed", "V_lambda_min_full_orders_optimal",
               "V_lambda_min_quad", "V_one_quad", "V_one_closed", "V_lambda_min_grid", "V_one_grid", "band_lo",
               "band_hi", "lambda_at_min", "lambda_at_max", "shape", "band_width", "relative_rise",
               "mixed_stability", "status"], band)
    for row in band:
        print({k: row[k] for k in ("r", "lambda_min", "V_lambda_min_quad", "V_one_quad", "shape", "band_width",
                                   "relative_rise", "lambda_suff_first")}, flush=True)

    rk = frak_r(prim, prim.k)
    rC = r_ceiling(prim)
    full_first = min(row["r"] for row in region if row["full_order_test"])
    mono = monotonicity_bounds(prim, full_first, rC)
    write_csv(HERE / "monotonicity.csv",
              ["r_a", "r_C", "tau_prime_bound", "growth_term_lower", "threshold_term_upper", "margin", "holds", "status"],
              [{**mono._asdict(), "status": "analytical (closed-form bounds)"}])
    print("monotonicity:", mono, flush=True)

    thresholds = exercise_thresholds(prim, region, band)
    write_csv(HERE / "thresholds.csv", ["boundary", "value", "definition"], thresholds)
    print("done", flush=True)


if __name__ == "__main__":
    main()
