"""Independent validation layer (C.0): identities, deviation diagnostics, status assignment.

Only this layer assigns `accepted`. A breached acceptance bound is reported, never loosened.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy import integrate, optimize

from .deviations import U, dU, deviation_scan, payoff_of_profile
from .information import Schedule, entry_at_posterior, expected_paid_cost_at_posterior
from .noise import pdf, posterior_bounds, survival
from .params import Controls, CostLaw, Noise
from .quadrature import integrate_segments, segments


@dataclass(frozen=True)
class Outcome:
    e_H: float
    e_L: float
    E: float
    O_H: float
    R_T: float
    W: float
    expected_preparation_cost: float
    mean_price: float
    tau: float
    x_star: float


@dataclass
class Validation:
    outcome: Outcome
    epsilon_P: float
    epsilon_e: float
    epsilon_q: float
    epsilon_q_refined: float
    identity_errors: dict
    entry_independent_error: float
    posterior_inversion_error: float
    tail_bound: float
    quadrature_error: float
    scans: dict = field(default_factory=dict)
    breaches: list[str] = field(default_factory=list)

    @property
    def accepted(self) -> bool:
        return not self.breaches


def _marginal_grid(sched: Schedule, halfwidth: float, pts_per_unit: int = 400) -> np.ndarray:
    lo, hi = sched.hull()
    lo = min(lo, min(sched.breakpoints, default=lo)) - halfwidth
    hi = max(hi, max(sched.breakpoints, default=hi)) + halfwidth
    xs = np.linspace(lo, hi, int((hi - lo) * pts_per_unit) + 1)
    return np.array(sorted(set(xs.tolist()) | set(sched.breakpoints)))


def _integrate_flow(sched: Schedule, fun, n: int = 48) -> float:
    """Integrate fun(x) against the full line with analytic constant tails when Laplace."""
    lo, hi = sched.hull()
    bps = list(sched.breakpoints)
    lo = min([lo, *bps]) - 1.0
    hi = max([hi, *bps]) + 1.0
    b = sched.prim.fb
    T = 60.0 * b
    segs = segments([lo - T, lo, *bps, hi, hi + T], b)
    return integrate_segments(fun, segs, n)


def conditional_entry_flow(sched: Schedule, state: str) -> float:
    """Flow-based entry: int a_theta(x) e(x) dx."""
    aθ = lambda x: sched.profile.a(sched.prim.noise, sched.prim.fb, x, state)
    return _integrate_flow(sched, lambda x: aθ(x) * sched.entry(x))


def threshold_flow(sched: Schedule, c: float) -> float:
    """Flow x_c with B_r(mu_X(x)) >= c  iff  x >= x_c, for a monotone posterior. +-inf when never/always."""
    prim, pay = sched.prim, sched.pay
    tau = pay.tau(c)
    lo, hi = sched.hull()
    if hi - lo < 1e-14:  # uninformative profile: constant posterior
        mu0 = float(sched.mu(np.array([lo]))[0])
        return -np.inf if tau <= mu0 else np.inf
    if prim.noise == Noise.LAPLACE:
        mu_lo, mu_hi = float(sched.mu(np.array([lo - 1.0]))[0]), float(sched.mu(np.array([hi + 1.0]))[0])
        if tau <= mu_lo:
            return -np.inf
        if tau > mu_hi:
            return np.inf
        if tau == mu_hi:
            return hi  # tie rule: the whole upper plateau enters
        g = lambda x: float(sched.mu(np.array([x]))[0]) - tau
        if g(lo) >= 0:
            return lo
        if g(hi) <= 0:
            return hi
        return float(optimize.brentq(g, lo, hi, xtol=1e-15))
    m, M = posterior_bounds(prim.fb)
    if tau <= m:
        return -np.inf
    if tau >= M:
        return np.inf
    span = 60.0 * prim.fb
    return float(optimize.brentq(lambda x: float(sched.mu(np.array([x]))[0]) - tau, lo - span, hi + span, xtol=1e-15))


def conditional_entry_cost_based(sched: Schedule, state: str) -> float:
    """Cost-based entry: integrate Pr(B_r(mu_X) >= c | theta) over the cost law using exact noise tails."""
    prim, pay = sched.prim, sched.pay
    qs, ws = (sched.profile.q_H, sched.profile.w_H) if state == "H" else (sched.profile.q_L, sched.profile.w_L)
    # monotone posterior check on a grid (correctly signed supports give a monotone likelihood ratio)
    lo, hi = sched.hull()
    xs = np.linspace(lo - 3 * prim.fb, hi + 3 * prim.fb, 2001)
    monotone = bool(np.all(np.diff(sched.mu(xs)) >= -1e-12))

    def tail(c: float) -> float:
        if sched.regime == "price_hidden":
            return float(pay.B(0.5) >= c)
        if not monotone:
            return _integrate_flow(sched, lambda x: sched.profile.a(prim.noise, prim.fb, x, state) * (pay.B(sched.mu(x)) >= c))
        xc = threshold_flow(sched, c)
        if sched.tie_at_ceiling and c == prim.fc_H:
            xc = min(xc, sched.hull()[1])  # symbolic tau = M: the entire upper plateau enters
        if xc == -np.inf:
            return 1.0
        if xc == np.inf:
            return 0.0
        return float(sum(w * survival(prim.noise, xc - q, prim.fb) for q, w in zip(qs, ws)))

    rho, cL, cH = prim.frho, prim.fc_L, prim.fc_H
    if prim.cost_law == CostLaw.ATOMS:
        return rho * tail(cL) + (1 - rho) * tail(cH)
    e = prim.feps_C
    m, M = posterior_bounds(prim.fb)
    plateau = [pay.B(m), pay.B(M)]
    tot = 0.0
    for w, c0 in ((rho, cL), (1 - rho, cH)):
        pts = sorted({c0 - e, c0 + e, *[c for c in plateau if c0 - e < c < c0 + e]})
        v = 0.0
        for a, b_ in zip(pts[:-1], pts[1:]):
            val, _ = integrate.quad(tail, a, b_, epsabs=1e-13, epsrel=1e-13, limit=200)
            v += val
        tot += w * v / (2 * e)
    return tot


def price_inverse(sched: Schedule, P_obs: float) -> float:
    """Recover the posterior from an observed price using the strictly increasing map P_r(mu)."""
    pay, prim = sched.pay, sched.prim
    m, M = posterior_bounds(prim.fb)
    Pmu = lambda mu: pay.t_0 + entry_at_posterior(prim, pay, mu) * (pay.w_L + pay.Delta_T * mu) + sched.dividend
    lo, hi = m - 1e-12, M + 1e-12
    if P_obs <= Pmu(lo):
        return lo
    if P_obs >= Pmu(hi):
        return hi
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if Pmu(mid) <= P_obs:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def validate(sched: Schedule, controls: Controls, refine: bool = True, scan_extra: list[float] | None = None,
             price_pools: bool = False) -> Validation:
    """Validate a candidate schedule. With `price_pools`, zero-entry flows are allowed to pool at t_0 (C.6, OA.70):
    the inversion check is restricted to positive-entry flows and the pooled posterior must itself imply zero entry."""
    prim, pay = sched.prim, sched.pay
    rho = prim.frho
    breaches: list[str] = []

    # --- entry, ownership, revenue -------------------------------------------------
    eH = conditional_entry_flow(sched, "H")
    eL = conditional_entry_flow(sched, "L")
    eH2 = conditional_entry_cost_based(sched, "H")
    eL2 = conditional_entry_cost_based(sched, "L")
    entry_err = max(abs(eH - eH2), abs(eL - eL2))
    if entry_err > controls.independent_formula_acceptance:
        breaches.append(f"entry_independent_error={entry_err:.3e}")
    E = 0.5 * (eH + eL)
    O_H = 0.5 * eH
    R_T = pay.t_0 + 0.5 * (eH * pay.w_H + eL * pay.w_L)

    # expected paid preparation cost and allocation surplus (OA.49)
    g = lambda x: 0.5 * (sched.profile.a(prim.noise, prim.fb, x, "H") + sched.profile.a(prim.noise, prim.fb, x, "L"))
    paid = _integrate_flow(sched, lambda x: g(x) * expected_paid_cost_at_posterior(prim, pay, sched.public_posterior(x)))
    r, p = pay.r, pay.p
    no_entry_alloc = (r * r - p * p) / (2 * r) if p < r else 0.0
    p_term = p * min(p / r, 1.0)  # p * Pr(R < p)
    W = no_entry_alloc + 0.5 * (eH * (pay.g_H + p_term) + eL * (pay.g_L + p_term)) - paid

    # --- identities ------------------------------------------------------------------
    ints = {s: _integrate_flow(sched, lambda x, s=s: sched.profile.a(prim.noise, prim.fb, x, s)) for s in "HL"}
    Emu = _integrate_flow(sched, lambda x: g(x) * sched.mu(x))
    EP = _integrate_flow(sched, lambda x: g(x) * sched.price(x))
    EV = R_T + sched.dividend
    identity_errors = {"int_a_H": abs(ints["H"] - 1), "int_a_L": abs(ints["L"] - 1),
                       "E_mu": abs(Emu - 0.5), "E_P_minus_E_V": abs(EP - EV)}
    for name, val in identity_errors.items():
        if val > controls.probability_acceptance:
            breaches.append(f"{name}={val:.3e}")

    # --- pointwise price identity, entry optimality, inversion ------------------------
    xs = _marginal_grid(sched, controls.initial_flow_halfwidth)
    mu = sched.mu(xs)
    mu_pub = sched.public_posterior(xs)
    e = sched.entry(xs)
    P = sched.price(xs)
    EV_x = pay.t_0 + e * (mu * pay.w_H + (1 - mu) * pay.w_L) + sched.dividend
    eps_P = float(np.max(np.abs(P - EV_x)))
    resid_err = max(float(np.max(np.abs(sched.A(xs, s) - sched.A_direct(xs, s)))) for s in "HL")
    if eps_P > controls.price_identity_acceptance:
        breaches.append(f"epsilon_P={eps_P:.3e}")
    if resid_err > controls.price_identity_acceptance:
        breaches.append(f"residual_direct_error={resid_err:.3e}")
    # entry optimality: reversing any cost type's decision at any tested posterior
    B = pay.B(mu_pub)
    costs = [prim.fc_L, prim.fc_H] if prim.cost_law == CostLaw.ATOMS else \
        [prim.fc_L - prim.feps_C, prim.fc_L, prim.fc_L + prim.feps_C, prim.fc_H - prim.feps_C, prim.fc_H, prim.fc_H + prim.feps_C]
    eps_e = 0.0
    for c in costs:
        enters = B >= c
        gain_reverse = np.where(enters, c - B, B - c)
        eps_e = max(eps_e, float(np.max(np.maximum(gain_reverse, 0.0))))
    if eps_e > controls.entry_optimality_acceptance:
        breaches.append(f"epsilon_e={eps_e:.3e}")
    inv_err = 0.0
    pool_mass, pool_mu = 0.0, float("nan")
    if sched.regime == "feedback":
        sub = xs[:: max(1, len(xs) // 400)]
        if price_pools:
            sub = np.array([x for x in sub if float(sched.entry(np.array([x]))[0]) > 0])
            # OA.70: pooled posterior over the zero-entry preimage of P = t_0
            zero = lambda x: (sched.entry(x) <= 0).astype(float)
            pool_mass = _integrate_flow(sched, lambda x: g(x) * zero(x))
            if pool_mass > 1e-15:
                num = _integrate_flow(sched, lambda x: sched.profile.a(prim.noise, prim.fb, x, "H") * zero(x))
                pool_mu = num / (2 * pool_mass)
                if float(entry_at_posterior(prim, pay, np.array([pool_mu]))[0]) > 0:
                    breaches.append(f"no_entry_pool_inconsistent: pooled posterior {pool_mu:.6f} implies positive entry")
        if len(sub):
            inv_err = max(abs(price_inverse(sched, float(sched.price(np.array([x]))[0])) - float(sched.mu(np.array([x]))[0])) for x in sub)
        if inv_err > 1e-7:
            breaches.append(f"posterior_inversion_error={inv_err:.3e}")

    # --- global order deviations ------------------------------------------------------
    tau = pay.tau(prim.fc_H)
    x_star = float("nan")
    if sched.regime == "feedback" and prim.cost_law == CostLaw.ATOMS:
        cands = [x for x in sched.breakpoints if x not in sched.profile.supports]
        x_star = cands[0] if cands else (float("inf") if tau > 0.5 else float("-inf"))
    extra = list(scan_extra or []) + [x_star, -x_star] if np.isfinite(x_star) else list(scan_extra or [])
    scans = {}
    eps_q = 0.0
    qerr, tb = 0.0, 0.0
    for s in "HL":
        sc = deviation_scan(sched, s, controls.initial_order_intervals, extra)
        scans[s] = sc
        eps_q = max(eps_q, sc["max_gain"])
        qerr = max(qerr, max(rw[4] for rw in sc["rows"]))
        tb = max(tb, max(rw[5] for rw in sc["rows"]))
    eps_q_ref = eps_q
    if refine:
        for s in "HL":
            sc = deviation_scan(sched, s, controls.refined_order_intervals, extra, n=64)
            scans[s + "_refined"] = sc
            eps_q_ref = max(eps_q_ref, sc["max_gain"])
    if max(eps_q, eps_q_ref) > controls.deviation_gain_acceptance:
        breaches.append(f"epsilon_q={max(eps_q, eps_q_ref):.3e}")

    mean_price = EP
    out = Outcome(eH, eL, E, O_H, R_T, W, paid, mean_price, tau, x_star)
    v = Validation(out, eps_P, eps_e, eps_q, eps_q_ref, identity_errors, entry_err, inv_err, tb, qerr, scans, breaches)
    v.no_entry_price_mass = pool_mass
    v.posterior_in_no_entry_pool = pool_mu
    return v
