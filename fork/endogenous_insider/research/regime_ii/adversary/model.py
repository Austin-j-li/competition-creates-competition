"""Adversary track, regime II team: independent model code.

This module does not import the numerics or theory code. It rebuilds the two-point-cost economy from the
paper's primitives and evaluates candidate profiles by adaptive quadrature (QUADPACK). Pure functions with
type hints; the parameter record comes first; nothing here writes files.

Objects.
  Econ            primitives, strength r, cost law (c_L, c_H, rho); payoffs (4); thresholds tau_L, tau_H.
  Profile         finite order mixtures for H and L plus voluntary pool intervals.
  schedule(...)   the pieces of constant entry, the pool, and its belief.
  payoff(...)     U_theta(q) = q * int f(x - q) A_theta(x) dx - k |q| by quad.
  best_response   global best response on the correct-sign half of [-1, 1] with a Lipschitz envelope
                  certificate: |F_theta'| <= F_theta / b, so between grid points U is bounded above.
  Closed forms for full orders: z_0, x*, S_X, E_0, e_H0, J_min (Lemma CD.6), K(c_L) (Prop R.6), the
  rho thresholds at the floor, and a fractional-knapsack (bathtub) value on a fine cell grid.

Status of every number: numerical diagnostic (floating-point quadrature), unless the text says closed form.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Sequence

import numpy as np
from scipy import integrate, optimize

XMAX = 60.0     # truncation of the flow line; Laplace tail e^{-30} at b = 2
INF = math.inf


# ----------------------------------------------------------------------------------------------
# economy
# ----------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Econ:
    h: float
    ell: float
    p: float
    b: float
    k: float
    r: float
    rho: float
    cL: float
    cH: float
    t0: float
    tH: float
    tL: float
    gH: float
    gL: float
    DeltaT: float
    wL: float
    tauL: float
    tauH: float
    m: float
    M: float


def make_econ(r: float, rho: float, cL: float, cH: float = 6.0, *, h: float = 10.0, ell: float = 1.0,
              p: float = 0.5, b: float = 2.0, k: float = 0.02) -> Econ:
    """Payoffs (4) of the paper for the uniform incumbent on [0, r], 0 < p < ell < r < h."""
    t0 = p * (1.0 - p / r)
    tH = r / 2.0 + p * p / (2.0 * r)
    tL = ell - (ell * ell - p * p) / (2.0 * r)
    gH = h - tH
    gL = (ell * ell - p * p) / (2.0 * r)
    m = 1.0 / (1.0 + math.exp(2.0 / b))
    span = gH - gL
    return Econ(h=h, ell=ell, p=p, b=b, k=k, r=r, rho=rho, cL=cL, cH=cH, t0=t0, tH=tH, tL=tL, gH=gH, gL=gL,
                DeltaT=tH - tL, wL=tL - t0, tauL=(cL - gL) / span, tauH=(cH - gL) / span, m=m, M=1.0 - m)


def B(ec: Econ, mu: float) -> float:
    """Gross profit B_r(mu) = g_L + mu (g_H - g_L)."""
    return ec.gL + mu * (ec.gH - ec.gL)


def regime(ec: Econ) -> str:
    """Regime of the cheap cost at strength r (tie rule: prepare when c <= B)."""
    if ec.cL <= B(ec, ec.m):
        return "I"
    if ec.cL <= B(ec, 0.5):
        return "II"
    if ec.cL <= B(ec, ec.M):
        return "III"
    return "IV"


def phi(ec: Econ, mu: float, tie: float = 1e-12) -> float:
    """Entry at a revealed belief: rho 1{mu >= tau_L} + (1 - rho) 1{mu >= tau_H}."""
    return ec.rho * float(mu >= ec.tauL - tie) + (1.0 - ec.rho) * float(mu >= ec.tauH - tie)


# ----------------------------------------------------------------------------------------------
# Laplace noise
# ----------------------------------------------------------------------------------------------

def F(ec: Econ, z: float) -> float:
    return 0.5 * math.exp(z / ec.b) if z <= 0.0 else 1.0 - 0.5 * math.exp(-z / ec.b)


def S(ec: Econ, z: float) -> float:
    return 1.0 - F(ec, z)


def f(ec: Econ, z: float) -> float:
    return math.exp(-abs(z) / ec.b) / (2.0 * ec.b)


# ----------------------------------------------------------------------------------------------
# full orders (1, -1): closed forms
# ----------------------------------------------------------------------------------------------

def mu_full(ec: Econ, x: float) -> float:
    """(A.8)."""
    return 1.0 / (1.0 + math.exp(-(abs(x + 1.0) - abs(x - 1.0)) / ec.b))


def flow_of_belief(ec: Econ, mu: float) -> float:
    """Inverse of (A.8) on (-1, 1)."""
    return 0.5 * ec.b * math.log(mu / (1.0 - mu))


def SX(ec: Econ, z: float) -> float:
    """Pr(X >= z) under full orders."""
    return 0.5 * (S(ec, z - 1.0) + S(ec, z + 1.0))


def pool_belief_halfline(ec: Econ, x: float) -> float:
    """Pr(H | X < x) under full orders (CD.7(b))."""
    a, c = F(ec, x - 1.0), F(ec, x + 1.0)
    return a / (a + c)


@dataclass(frozen=True)
class FullOrderMinimal:
    """Full orders with the minimal pool Z_0 = (-inf, z_0); regime II only."""
    z0: float
    xstar: float
    alphaH: float
    alphaL: float
    E0: float
    eH0: float
    pool_prob: float
    pool_belief: float
    J_min: float
    test_margin: float      # (1 - 1/b) J_min - k; >= 0 means the profile passes the investor test


def full_minimal(ec: Econ) -> FullOrderMinimal:
    z0 = flow_of_belief(ec, ec.tauL)
    xs = flow_of_belief(ec, ec.tauH)
    aH, aL = S(ec, xs - 1.0), S(ec, xs + 1.0)
    E0 = ec.rho * SX(ec, z0) + (1.0 - ec.rho) * SX(ec, xs)
    eH0 = ec.rho * S(ec, z0 - 1.0) + (1.0 - ec.rho) * aH
    # Lemma CD.6 with g_m = 0, g_M = 1 and pool end z0 in (-1, 1):
    w = lambda u: 1.0 / math.sqrt(u * (1.0 - u))  # noqa: E731
    mid1, _ = integrate.quad(w, ec.tauL, ec.tauH, epsabs=1e-14, epsrel=1e-12)
    mid2, _ = integrate.quad(w, ec.tauH, ec.M, epsabs=1e-14, epsrel=1e-12)
    J = ec.DeltaT * (math.exp(-1.0 / ec.b) / 4.0 * (ec.rho * mid1 + mid2) + ec.m / 2.0)
    pp = 1.0 - SX(ec, z0)
    return FullOrderMinimal(z0=z0, xstar=xs, alphaH=aH, alphaL=aL, E0=E0, eH0=eH0, pool_prob=pp,
                            pool_belief=pool_belief_halfline(ec, z0), J_min=J,
                            test_margin=(1.0 - 1.0 / ec.b) * J - ec.k)


def rho_star_floor(ec: Econ) -> tuple[float, float, float, float]:
    """Closed-form rho thresholds at the floor limit c_L -> B(m)+ (depend on b and tau_H only).

    Returns (rho_E, rho_O, a, pi0): E_0 < rho for every regime II c_L iff rho >= rho_E = a / (a + pi0),
    with a = (alpha_H + alpha_L)/2 and pi0 = Pr(X <= -1) = (1 + e^{-2/b})/4;
    e_H0 < rho iff rho > rho_O = alpha_H / (alpha_H + F(-2)).
    """
    xs = flow_of_belief(ec, ec.tauH)
    aH, aL = S(ec, xs - 1.0), S(ec, xs + 1.0)
    a = 0.5 * (aH + aL)
    pi0 = 0.25 * (1.0 + math.exp(-2.0 / ec.b))
    return a / (a + pi0), aH / (aH + F(ec, -2.0)), a, pi0


def K_forcing(ec: Econ) -> float:
    """Prop R.6's forcing bound K(c_L) = (1 - 1/b) rho Delta_T min{tau_L S(xbar + 1), m S(xbar)}."""
    xbar = optimize.brentq(lambda x: pool_belief_halfline(ec, x) - ec.tauL, -1.0, 400.0, xtol=1e-14)
    return (1.0 - 1.0 / ec.b) * ec.rho * ec.DeltaT * min(ec.tauL * S(ec, xbar + 1.0), ec.m * S(ec, xbar))


def a3_window(ec: Econ, r0: float) -> tuple[float, float]:
    """(Delta_T(r0), (1 - 1/b) rho m Delta_T(r1)): the paper's (A3) window for k."""
    d0 = (r0 - ec.ell) ** 2 / (2.0 * r0)
    return d0, (1.0 - 1.0 / ec.b) * ec.rho * ec.m * ec.DeltaT


def bathtub_inf(ec: Econ, which: str = "E", width: float = 0.002, lo: float = -12.0, hi: float = 14.0
                ) -> tuple[float, float]:
    """Smallest entry (which='E') or high-type entry (which='eH') over all consistent full-order pools.

    Fractional knapsack on cells of width `width`: each cell above z_0 costs (mu - tau_L) dP of belief
    budget and removes rho or 1 (times the cell's H-weight for 'eH') of entry. The budget is the belief
    slack of the forced pool Z_0. Returns (inf value, value with the minimal pool). Independent of the
    theory track's implementation.
    """
    fm = full_minimal(ec)
    z0 = fm.z0
    xs = np.arange(max(z0, lo), hi, width)
    xs = np.append(xs, hi)
    mids = 0.5 * (xs[:-1] + xs[1:])
    dx = np.diff(xs)
    mu = np.array([mu_full(ec, x) for x in mids])
    fH = np.exp(-np.abs(mids - 1.0) / ec.b) / (2.0 * ec.b)
    fL = np.exp(-np.abs(mids + 1.0) / ec.b) / (2.0 * ec.b)
    dP = 0.5 * (fH + fL) * dx
    e = np.array([phi(ec, u) for u in mu])
    cost = (mu - ec.tauL) * dP
    if which == "E":
        value = e * dP
    else:
        value = e * fH * dx
    # budget: integral over Z_0 of (tau_L - mu) dP
    budget, _ = integrate.quad(lambda x: (ec.tauL - mu_full(ec, x)) * 0.5 * (f(ec, x - 1.0) + f(ec, x + 1.0)),
                               -XMAX, z0, points=[-1.0], epsabs=1e-14, epsrel=1e-12, limit=400)
    ratio = cost / np.maximum(value, 1e-300)
    order = np.argsort(ratio)
    spent = 0.0
    removed = 0.0
    for i in order:
        if value[i] <= 0.0:
            continue
        if spent + cost[i] <= budget:
            spent += cost[i]
            removed += value[i]
        else:
            frac = (budget - spent) / cost[i]
            removed += frac * value[i]
            break
    base = fm.E0 if which == "E" else fm.eH0
    return base - removed, base


# ----------------------------------------------------------------------------------------------
# general profiles: finite mixtures and pools, evaluated by quadrature
# ----------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Profile:
    """H atoms (order, weight) with order in [0, 1]; L atoms with order in [-1, 0]; voluntary pool intervals."""
    H: tuple[tuple[float, float], ...]
    L: tuple[tuple[float, float], ...]
    pool: tuple[tuple[float, float], ...] = ()


def pure(qH: float, qL: float, cutoff: float | None = None,
         extra: Sequence[tuple[float, float]] = ()) -> Profile:
    pool: list[tuple[float, float]] = [] if cutoff is None else [(-INF, float(cutoff))]
    pool.extend((float(a), float(c)) for a, c in extra)
    return Profile(H=((float(qH), 1.0),), L=((float(qL), 1.0),), pool=tuple(pool))


def density(ec: Econ, atoms: Sequence[tuple[float, float]], x: float) -> float:
    return sum(w * math.exp(-abs(x - q) / ec.b) for q, w in atoms) / (2.0 * ec.b)


def mass(ec: Econ, atoms: Sequence[tuple[float, float]], lo: float, hi: float) -> float:
    """Pr(lo < q + Z < hi) under the mixture."""
    total = 0.0
    for q, w in atoms:
        a = 0.0 if lo == -INF else F(ec, lo - q)
        c = 1.0 if hi == INF else F(ec, hi - q)
        total += w * (c - a)
    return total


def mu_of(ec: Econ, prof: Profile, x: float) -> float:
    """Posterior Pr(H | X = x), with log-sum-exp for far tails."""
    def log_a(atoms: Sequence[tuple[float, float]]) -> float:
        terms = [math.log(w) - abs(x - q) / ec.b for q, w in atoms if w > 0.0]
        top = max(terms)
        return top + math.log(sum(math.exp(t - top) for t in terms))
    d = log_a(prof.L) - log_a(prof.H)
    if d > 700.0:
        return 0.0
    if d < -700.0:
        return 1.0
    return 1.0 / (1.0 + math.exp(d))


def _crossings(ec: Econ, prof: Profile, tau: float) -> list[float]:
    atoms = sorted({q for q, _ in prof.H + prof.L})
    pts = [-XMAX] + atoms + [XMAX]
    out: list[float] = []
    g = lambda x: mu_of(ec, prof, x) - tau  # noqa: E731
    for a, c in zip(pts[:-1], pts[1:]):
        if c - a < 1e-12:
            continue
        n = 200
        grid = np.linspace(a, c, n + 1)
        vals = [g(x) for x in grid]
        for i in range(n):
            if vals[i] == 0.0:
                out.append(float(grid[i]))
            elif vals[i] * vals[i + 1] < 0.0:
                out.append(optimize.brentq(g, grid[i], grid[i + 1], xtol=1e-14, rtol=1e-14))
    return out


@dataclass(frozen=True)
class Schedule:
    ec: Econ
    prof: Profile
    pieces: tuple[tuple[float, float, float], ...]    # (lo, hi, entry level)
    pool_prob: float
    pool_belief: float
    consistent: bool
    mu_min_A: float      # smallest posterior on the entry set
    mu_max: float        # largest posterior anywhere


def schedule(ec: Econ, prof: Profile) -> Schedule:
    """Pieces of constant entry: the forced pool {phi(mu_X) = 0}, the voluntary pool, and the entry set."""
    pts = set()
    for q, _ in prof.H + prof.L:
        pts.add(q)
    for lo, hi in prof.pool:
        for v in (lo, hi):
            if -XMAX < v < XMAX:
                pts.add(v)
    for tau in (ec.tauL, ec.tauH):
        pts.update(_crossings(ec, prof, tau))
    edges = [-INF] + sorted(pts) + [INF]
    pieces = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        rep = hi - 1.0 if lo == -INF else (lo + 1.0 if hi == INF else 0.5 * (lo + hi))
        in_pool = any(a < rep < c for a, c in prof.pool)
        e = 0.0 if in_pool else phi(ec, mu_of(ec, prof, rep))
        pieces.append((lo, hi, e))
    pH = sum(mass(ec, prof.H, lo, hi) for lo, hi, e in pieces if e == 0.0)
    pL = sum(mass(ec, prof.L, lo, hi) for lo, hi, e in pieces if e == 0.0)
    pm = pH + pL
    mubar = pH / pm if pm > 1e-300 else float("nan")
    consistent = pm <= 1e-300 or phi(ec, mubar) == 0.0
    mus = []
    for lo, hi, e in pieces:
        if e > 0.0:
            a = max(lo, -XMAX)
            c = min(hi, XMAX)
            mus.append(min(mu_of(ec, prof, x) for x in np.linspace(a, c, 50)))
    mu_max = max(mu_of(ec, prof, x) for x in np.linspace(-XMAX, XMAX, 2001))
    return Schedule(ec=ec, prof=prof, pieces=tuple(pieces), pool_prob=0.5 * pm, pool_belief=mubar,
                    consistent=bool(consistent), mu_min_A=min(mus) if mus else float("nan"), mu_max=mu_max)


def residual(sch: Schedule, theta: str, x: float, e: float) -> float:
    """A_H = e Delta_T (1 - mu), A_L = e Delta_T mu: the investor's gross gain per unit at flow x."""
    mu = mu_of(sch.ec, sch.prof, x)
    return e * sch.ec.DeltaT * ((1.0 - mu) if theta == "H" else mu)


def _quad(g: Callable[[float], float], a: float, b: float, pts: Sequence[float] = ()) -> float:
    cuts = [a] + sorted(x for x in pts if a < x < b) + [b]
    total = 0.0
    for lo, hi in zip(cuts[:-1], cuts[1:]):
        if hi - lo < 1e-15:
            continue
        val, _ = integrate.quad(g, lo, hi, epsabs=1e-14, epsrel=1e-13, limit=400)
        total += val
    return total


def gross(sch: Schedule, theta: str, q: float) -> float:
    """F_theta at the order q: int f(x - q) A_theta(x) dx (q >= 0 for H, q <= 0 for L)."""
    ec = sch.ec
    total = 0.0
    for lo, hi, e in sch.pieces:
        if e == 0.0:
            continue
        a, c = max(lo, -XMAX), min(hi, XMAX)
        if c <= a:
            continue
        total += _quad(lambda x: f(ec, x - q) * residual(sch, theta, x, e), a, c, [q])
    return total


def payoff(sch: Schedule, theta: str, q: float) -> float:
    """U_H(q) = q F_H(q) - k|q|; U_L(q) = -q F_L(q) - k|q| (so a short q < 0 earns |q| F_L - k|q|)."""
    sign = 1.0 if theta == "H" else -1.0
    return sign * q * gross(sch, theta, q) - sch.ec.k * abs(q)


def gross_parts(sch: Schedule, theta: str, q: float) -> tuple[float, float]:
    """(F_-, F_+): the parts of F_theta(q) from flows below and above the kernel centre q."""
    ec = sch.ec
    lo_part = hi_part = 0.0
    for lo, hi, e in sch.pieces:
        if e == 0.0:
            continue
        a, c = max(lo, -XMAX), min(hi, XMAX)
        if c <= a:
            continue
        g = lambda x: f(ec, x - q) * residual(sch, theta, x, e)  # noqa: E731
        if c <= q:
            lo_part += _quad(g, a, c)
        elif a >= q:
            hi_part += _quad(g, a, c)
        else:
            lo_part += _quad(g, a, q)
            hi_part += _quad(g, q, c)
    return lo_part, hi_part


@dataclass(frozen=True)
class BestResponse:
    theta: str
    q_best: float
    u_best: float
    u_at: float            # payoff at the profile's own order(s): the smallest over support points
    regret: float          # max(0, u_best - u_at)
    envelope_margin: float  # u_at - (upper bound on U between grid points, excluding cells around q_own)
    n_local_max: int       # number of local maxima of U on the grid (zero order counted if best)
    local_max_orders: tuple[float, ...]


def best_response(sch: Schedule, theta: str, own: Sequence[float], n: int = 401) -> BestResponse:
    """Global best response on [0, 1] (H) or [-1, 0] (L) by a grid, local refinement, and the envelope.

    Envelope: |F'| <= F/b gives F(s) <= F(s_i) e^{|s - s_i|/b}. On a cell [s_i, s_{i+1}] of width h,
    U(s) <= s_{i+1} e^{h/b} min{F(s_i), F(s_{i+1})} e^{0} ... we use the looser but safe bound
    U(s) <= s_{i+1} e^{h/b} min(F(s_i), F(s_{i+1})) - k s_i. If every cell's bound is below u_at, except
    cells containing a support point, the support points are global maxima up to quadrature error.
    """
    sign = 1.0 if theta == "H" else -1.0
    grid = np.linspace(0.0, 1.0, n)
    Fs = np.array([gross(sch, theta, sign * s) for s in grid])
    Us = grid * Fs - sch.ec.k * grid
    Us[0] = 0.0
    # local maxima on the grid
    loc = []
    for i in range(n):
        left = Us[i] >= Us[i - 1] if i > 0 else True
        right = Us[i] >= Us[i + 1] if i < n - 1 else True
        if left and right and (i == 0 or Us[i] > Us[i - 1] or i == n - 1 or Us[i] > Us[i + 1]):
            loc.append(i)
    loc = [i for i in loc if Us[i] >= 0.0]
    # refine the best few
    best_q, best_u = 0.0, 0.0
    for i in sorted(loc, key=lambda j: -Us[j])[:4]:
        lo, hi = grid[max(i - 1, 0)], grid[min(i + 1, n - 1)]
        if hi - lo > 1e-12:
            res = optimize.minimize_scalar(lambda s: -(s * gross(sch, theta, sign * s) - sch.ec.k * s),
                                           bounds=(lo, hi), method="bounded", options={"xatol": 1e-11})
            if -res.fun > best_u:
                best_q, best_u = float(res.x), float(-res.fun)
        if Us[i] > best_u:
            best_q, best_u = float(grid[i]), float(Us[i])
    u_own = [payoff(sch, theta, sign * abs(s)) for s in own]
    u_at = min(u_own)
    h = grid[1] - grid[0]
    bound = -INF
    for i in range(n - 1):
        cell_has_own = any(grid[i] - 1e-12 <= abs(s) <= grid[i + 1] + 1e-12 for s in own)
        if cell_has_own:
            continue
        ub = grid[i + 1] * math.exp(h / sch.ec.b) * min(Fs[i], Fs[i + 1]) - sch.ec.k * grid[i]
        bound = max(bound, ub)
    return BestResponse(theta=theta, q_best=sign * best_q, u_best=best_u, u_at=u_at,
                        regret=max(0.0, best_u - u_at), envelope_margin=u_at - bound, n_local_max=len(loc),
                        local_max_orders=tuple(float(sign * grid[i]) for i in loc))


@dataclass(frozen=True)
class Outcome:
    E: float
    eH: float
    eL: float
    O_H: float
    pool_prob: float
    pool_belief: float
    consistent: bool
    informative: bool


def outcome(sch: Schedule) -> Outcome:
    ec, prof = sch.ec, sch.prof
    eH = sum(e * mass(ec, prof.H, lo, hi) for lo, hi, e in sch.pieces)
    eL = sum(e * mass(ec, prof.L, lo, hi) for lo, hi, e in sch.pieces)
    informative = any(abs(q) > 0.0 and w > 0.0 for q, w in prof.H + prof.L)
    return Outcome(E=0.5 * (eH + eL), eH=eH, eL=eL, O_H=0.5 * eH, pool_prob=sch.pool_prob,
                   pool_belief=sch.pool_belief, consistent=sch.consistent, informative=informative)


@dataclass(frozen=True)
class Check:
    """A full equilibrium check of a profile."""
    consistent: bool
    pool_belief: float
    pool_prob: float
    E: float
    O_H: float
    eH: float
    eL: float
    regret_H: float
    regret_L: float
    env_H: float
    env_L: float
    uH: float
    uL: float
    accepted: bool


def check(ec: Econ, prof: Profile, tol: float = 1e-9, n: int = 401) -> Check:
    sch = schedule(ec, prof)
    o = outcome(sch)
    brH = best_response(sch, "H", [q for q, _ in prof.H], n=n)
    brL = best_response(sch, "L", [q for q, _ in prof.L], n=n)
    ok = sch.consistent and brH.regret <= tol and brL.regret <= tol
    return Check(consistent=sch.consistent, pool_belief=sch.pool_belief, pool_prob=sch.pool_prob, E=o.E,
                 O_H=o.O_H, eH=o.eH, eL=o.eL, regret_H=brH.regret, regret_L=brL.regret,
                 env_H=brH.envelope_margin, env_L=brL.envelope_margin, uH=brH.u_at, uL=brL.u_at,
                 accepted=bool(ok))


# ----------------------------------------------------------------------------------------------
# starved family (Prop R.10): orders (1, -v), v < v_H, pool (-inf, x'), x' >= 0
# ----------------------------------------------------------------------------------------------

def v_H(ec: Econ) -> float:
    """b logit(tau_H) - 1: the largest short that keeps every belief below tau_H when q_H = 1."""
    return ec.b * math.log(ec.tauH / (1.0 - ec.tauH)) - 1.0


def C_L(ec: Econ, v: float, xp: float) -> float:
    """rho Delta_T int_{x'}^inf e^{-x/b} mu_X(x) / (2b) dx under orders (1, -v)."""
    def mu(x: float) -> float:
        return 1.0 / (1.0 + math.exp(-(abs(x + v) - abs(x - 1.0)) / ec.b))
    val = _quad(lambda x: math.exp(-x / ec.b) * mu(x) / (2.0 * ec.b), xp, XMAX, [1.0])
    return ec.rho * ec.DeltaT * val


def starved_cutoff(ec: Econ, v: float) -> float | None:
    """The pool end x' >= 0 at which the low type's first-order condition holds for the short v."""
    target = ec.k * math.exp(v / ec.b) / (1.0 - v / ec.b)
    g = lambda xp: C_L(ec, v, xp) - target  # noqa: E731
    if g(0.0) < 0.0:
        return None
    hi = 1.0
    while g(hi) > 0.0:
        hi += 1.0
        if hi > 40.0:
            return None
    return optimize.brentq(g, 0.0, hi, xtol=1e-12)


def starved_pool_belief(ec: Econ, v: float, xp: float) -> float:
    a, c = F(ec, xp - 1.0), F(ec, xp + v)
    return a / (a + c)


# ----------------------------------------------------------------------------------------------
# certificate for a pure own order: envelope away from it, derivative signs near it
# ----------------------------------------------------------------------------------------------

def dgross(sch: Schedule, theta: str, q: float) -> float:
    """dF_theta/ds at the own-sign size s = |q|: F_H'(s) = (H_+ - H_-)/b, F_L'(s) = (L_- - L_+)/b.

    H_-, H_+ are the parts of F_H below and above the kernel centre s; for L the centre is -s and a larger
    short moves the kernel left, so the sign flips.
    """
    lo, hi = gross_parts(sch, theta, q)
    if theta == "H":
        return (hi - lo) / sch.ec.b
    return (lo - hi) / sch.ec.b


@dataclass(frozen=True)
class Certificate:
    theta: str
    q_own: float
    u_own: float
    far_margin: float       # u_own minus the envelope bound on cells at distance >= d from q_own
    near_margin: float      # smallest |U'| minus the Lipschitz slack on the near grid, signed as required
    lipschitz: float        # bound on |U''| used on the near grid
    exclusion: float        # radius around an interior own order left to the regret check
    certified: bool


def certify(sch: Schedule, theta: str, q_own: float, n: int = 401, d: float = 0.06, hn: float = 0.0005
            ) -> Certificate:
    """Certify that the pure order q_own is a global best response for type theta (floating-point quad).

    Far cells (distance >= d from |q_own|): U(s) <= min over the two endpoint envelopes, each from
    |F'| <= F/b. Near grid (distance < d): U'(s) = F + sF' - k computed by quad on a grid of step hn;
    |U''| <= F (2/b + s/b^2) + A_max s/b^2 with A_max = Delta_T, so U' moves by at most L hn/2 between
    grid points. Required signs: U' > 0 on the left of the own order and U' < 0 on its right (for an
    interior own order), and U' > 0 on the left only for the corner |q_own| = 1. Zero is compared by value.
    """
    ec = sch.ec
    sign = 1.0 if theta == "H" else -1.0
    s_own = abs(q_own)
    u_own = payoff(sch, theta, sign * s_own)
    grid = np.linspace(0.0, 1.0, n)
    Fs = np.array([gross(sch, theta, sign * s) for s in grid])
    Us = grid * Fs - ec.k * grid
    h = grid[1] - grid[0]
    far = -INF
    for i in range(n - 1):
        if min(abs(grid[i] - s_own), abs(grid[i + 1] - s_own)) < d:
            continue
        b1 = max(Us[i], grid[i + 1] * Fs[i] * math.exp(h / ec.b) - ec.k * grid[i + 1])
        b2 = max(grid[i] * Fs[i + 1] * math.exp(h / ec.b) - ec.k * grid[i], Us[i + 1])
        far = max(far, min(b1, b2))
    far_margin = u_own - far
    # near grid
    lo_n, hi_n = max(0.0, s_own - d), min(1.0, s_own + d)
    near = np.arange(lo_n, hi_n + 1e-12, hn)
    Fn = np.array([gross(sch, theta, sign * s) for s in near])
    dFn = np.array([dgross(sch, theta, sign * s) for s in near])
    Un_prime = Fn + near * dFn - ec.k
    Fmax = float(Fn.max()) * math.exp(hn / ec.b)
    L = Fmax * (2.0 / ec.b + 1.0 / ec.b ** 2) + ec.DeltaT / ec.b ** 2
    slack = 0.5 * L * hn
    # exclusion radius around an interior own order: where |U'| is below the slack by its own slope
    eps = hn
    if 0.0 < s_own < 1.0:
        j = int(np.argmin(np.abs(near - s_own)))
        jl, jr = max(j - 5, 0), min(j + 5, len(near) - 1)
        slope = abs(Un_prime[jr] - Un_prime[jl]) / max(near[jr] - near[jl], hn)
        eps = max(hn, 2.0 * slack / max(slope, 1e-12) + abs(near[j] - s_own))
    margins = []
    for s, up in zip(near, Un_prime):
        if abs(s - s_own) <= eps:
            continue
        if s < s_own:
            margins.append(up - slack)          # need U' > 0 to the left
        else:
            margins.append(-up - slack)         # need U' < 0 to the right
    near_margin = min(margins) if margins else INF
    # zero order: compare by value (U(0) = 0)
    ok = far_margin > 0.0 and near_margin > 0.0 and u_own > 0.0
    if s_own == 0.0:
        ok = far_margin > 0.0 and near_margin > 0.0
    return Certificate(theta=theta, q_own=q_own, u_own=u_own, far_margin=far_margin, near_margin=near_margin,
                       lipschitz=L, exclusion=eps, certified=bool(ok))
