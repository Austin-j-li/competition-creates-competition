"""Complete pricing-and-trading continuations (OA C.6, OA.70, A.10; peer-circulation spec S2).

A continuation is the complete object the seller faces after a reserve: the investor's
state-contingent orders, the pricing rule (including every positive-mass price pool), the
buyer's information at each price (pooled posterior on an atom, inverted posterior elsewhere),
the preparation rule by observed price and cost, and the validation evidence. Identity is
economic: two candidates are the same continuation only when their complete strategies and
induced price information agree within the declared identity tolerances. A candidate identity
records how a calculation was obtained and is kept separately in the attempt ledger.

This module never accepts a candidate on its own authority except through
`validate_pooled_schedule`, which applies the C.0 tolerances and records every breach.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from decimal import Decimal
from fractions import Fraction
from typing import Mapping, Sequence

import mpmath as mp
import numpy as np

from .auction import AuctionPayoffs
from .deviations import dU, deviation_scan, F
from .information import OrderProfile, entry_at_posterior
from .noise import pdf, posterior_bounds, survival
from .params import Controls, CostLaw, Noise, Primitives
from .quadrature import integrate_segments, segments

NA = "n/a"
NEG_INF = "-inf"
POS_INF = "inf"

# identity tolerances (documented canonical rule, C.0 acceptance bounds reused where they apply)
ORDER_IDENTITY_TOL = 1e-6          # orders and mixing weights (matches the fixed-point tolerance in search.py)
ATOM_IDENTITY_TOL = 1e-8           # price-atom values, masses and posteriors (probability_acceptance)


# ---------------------------------------------------------------------------------------------
# identifiers
# ---------------------------------------------------------------------------------------------
def _norm_dec(s: str) -> str:
    """Shortest exact decimal for a declared string; symbolic strings pass through."""
    try:
        d = Decimal(s)
    except Exception:
        return s
    if d == d.to_integral():
        return str(d.quantize(Decimal(1)))
    return format(d.normalize(), "f")


def parameter_set_id(prim: Primitives, r: str, p_exact: str, value_law: str = "binary", eps_V: str = "0",
                     extra: Mapping[str, str] | None = None) -> str:
    """Canonical immutable parameter identity built from the exact declarations (not a hash)."""
    parts = [f"h={_norm_dec(prim.h)}", f"ell={_norm_dec(prim.ell)}", f"p={_norm_dec(p_exact)}", f"rho={_norm_dec(prim.rho)}",
             f"c_L={_norm_dec(prim.c_L)}", f"c_H={_norm_dec(prim.c_H)}", f"b={_norm_dec(prim.b)}", f"k={_norm_dec(prim.k)}",
             f"r={_norm_dec(r)}", f"noise={prim.noise.value}", f"cost={prim.cost_law.value}",
             f"cost_halfwidth={_norm_dec(prim.cost_halfwidth)}", f"prior_H={_norm_dec(prim.fundamental_prior_H)}",
             f"value_law={value_law}", f"eps_V={_norm_dec(eps_V)}"]
    for k_, v_ in sorted((extra or {}).items()):
        parts.append(f"{k_}={v_}")
    return "|".join(parts)


INSTITUTION_RESERVE_AUCTION = "reserve_auction:uniform_incumbent[0,r];sale_to_highest_admissible_at_max(p,min(R,v));bid_equal_reserve_is_admissible=yes"
INFO_FEEDBACK_STATE = "public_price_feedback;investor_observes=fundamental_state;buyer_observes=price_only"
INFO_FEEDBACK_CLASS = "public_price_feedback;investor_observes=value_class_not_within_class_value;buyer_observes=price_only"
INFO_HIDDEN = "price_hidden;investor_observes=fundamental_state;buyer_observes=prior_only"
TIE_RULE = "entry_at_indifference=yes;bid_equal_reserve_is_admissible=yes;upper_plateau_enters_at_tau=M;lower_plateau_enters_at_B(m)=c_L"


# ---------------------------------------------------------------------------------------------
# records
# ---------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class PricingRule:
    rule_family: str                                  # benchmark_inversion | lower_cutoff_pool | constant_price | interval_union_pool
    pool_sets: tuple[tuple[str, str], ...]            # zero-entry pool as closed/open intervals with exact endpoint strings
    pool_cutoff_exact: str                            # exact expression for a lower cutoff, else n/a
    pool_cutoff_decimal: str                          # 30-digit decimal of the cutoff, else n/a
    positive_entry_price_map: str                     # formula on the positive-entry region
    event_ids: tuple[str, ...] = ()

    def definition(self) -> str:
        pools = ";".join(f"[{a},{b_})" for a, b_ in self.pool_sets) or "none"
        return f"{self.rule_family}:pool={pools}:positive={self.positive_entry_price_map}"


@dataclass(frozen=True)
class PriceAtom:
    atom_value: float
    preimage: tuple[tuple[float, float], ...]         # full flow preimage of the atom
    mass_H: float                                     # int_A a_H
    mass_L: float                                     # int_A a_L
    probability: float                                # pi mass_H + (1 - pi) mass_L
    posterior: float                                  # pi mass_H / (pi mass_H + (1 - pi) mass_L)
    kind: str                                         # no_entry_pool | positive_entry_plateau


@dataclass(frozen=True)
class PriceInformation:
    atoms: tuple[PriceAtom, ...]
    posterior_map: str                                # description of the posterior on nonpooled prices
    inversion_error: float                            # max |P^{-1}(P(x)) - mu_X(x)| over tested positive-entry flows


@dataclass(frozen=True)
class PreparationRule:
    rule_id: str
    actions: tuple[tuple[str, str, bool], ...]        # (price_region, cost_label, prepares)

    def prepares(self, region: str, cost_label: str) -> bool:
        for reg, c, a in self.actions:
            if reg == region and c == cost_label:
                return a
        raise KeyError(f"preparation rule {self.rule_id} has no action for ({region}, {cost_label})")

    def definition(self) -> str:
        return self.rule_id + ":" + ";".join(f"{r_}/{c}={'prepare' if a else 'stay_out'}" for r_, c, a in self.actions)


@dataclass(frozen=True)
class ContinuationOutcome:
    e_H: float
    e_L: float
    E: float                                          # Pr(I = 1)
    A: float                                          # Pr(I = 1, V >= p)  admissible challenger
    S: float                                          # Pr(R >= p or [I = 1, V >= p])  sale
    C2: float                                         # Pr(R >= p, I = 1, V >= p)  two admissible bidders
    O_H: float                                        # high-value challenger ownership from the allocation event
    R_T: float
    mean_price: float


@dataclass(frozen=True)
class ValidationEvidence:
    pricing_error: float
    belief_error: float
    entry_deviation_gain: float
    investor_deviation_gain_estimate: float
    investor_deviation_gain_upper_bound: float | None  # None: no rigorous bound available (never reported as 0)
    error_budget: float
    support_evidence: str
    arithmetic_evidence: str
    breaches: tuple[str, ...]

    @property
    def accepted(self) -> bool:
        return not self.breaches


@dataclass(frozen=True)
class Continuation:
    candidate_id: str
    continuation_id: str
    parameter_set_id: str
    institution_id: str
    information_structure_id: str
    tie_rule_id: str
    investor_strategy: OrderProfile
    pricing_rule: PricingRule
    price_information: PriceInformation
    preparation_rule: PreparationRule
    outcome: ContinuationOutcome
    validation: ValidationEvidence
    result_status: str
    existence_scope: str
    uniqueness_scope: str
    search_coverage_scope: str
    pricing_family_coverage: str
    exhaustive_pricing_search: bool = False
    event_id: str = NA
    event_defining_relation: str = NA
    rejection_reason: str = ""
    unresolved_reason: str = ""
    run_id: str = ""
    branch: str = ""

    @property
    def accepted(self) -> bool:
        return self.validation.accepted and not self.unresolved_reason


# ---------------------------------------------------------------------------------------------
# identity and deduplication
# ---------------------------------------------------------------------------------------------
def _fmt_tol(x: float, tol: float) -> str:
    d = max(0, int(round(-np.log10(tol))))
    return f"{x:.{d}f}"


def canonical_strategy(profile: OrderProfile) -> str:
    def side(qs, ws):
        pairs = sorted((float(q), float(w)) for q, w in zip(qs, ws) if w > 0)
        return ",".join(f"({_fmt_tol(q, ORDER_IDENTITY_TOL)}:{_fmt_tol(w, ORDER_IDENTITY_TOL)})" for q, w in pairs)
    return f"qH={side(profile.q_H, profile.w_H)}|qL={side(profile.q_L, profile.w_L)}"


def continuation_identity(parameter_set: str, institution: str, information: str, tie_rule: str, profile: OrderProfile,
                          pricing: PricingRule, prep: PreparationRule, info: PriceInformation, controls: Controls) -> str:
    """Canonical economic identity: complete strategies plus induced price information.

    Pools and atoms of probability at most `probability_acceptance` are null sets and are dropped;
    numeric components are written at the identity tolerances. The string is the identity, not a hash.
    """
    atoms = sorted((a for a in info.atoms if a.probability > controls.probability_acceptance), key=lambda a: a.atom_value)
    atom_s = ";".join(f"{a.kind}@{_fmt_tol(a.atom_value, ATOM_IDENTITY_TOL)}:mH={_fmt_tol(a.mass_H, ATOM_IDENTITY_TOL)}:"
                      f"mL={_fmt_tol(a.mass_L, ATOM_IDENTITY_TOL)}:mu={_fmt_tol(a.posterior, ATOM_IDENTITY_TOL)}:"
                      f"preimage={tuple((_fmt_tol(lo, ORDER_IDENTITY_TOL), _fmt_tol(hi, ORDER_IDENTITY_TOL)) for lo, hi in a.preimage)}" for a in atoms) or "none"
    return "|".join([f"ps[{parameter_set}]", f"inst[{institution}]", f"info[{information}]", f"tie[{tie_rule}]",
                     canonical_strategy(profile), f"price[{pricing.rule_family}:{pricing.positive_entry_price_map}]", f"atoms[{atom_s}]", f"prep[{prep.definition()}]",
                     f"posterior[{info.posterior_map}]"])


def orders_only_key(cont: Continuation) -> str:
    """The forbidden key (spec 7.3): orders alone. Provided only so tests can show it merges distinct continuations."""
    return f"ps[{cont.parameter_set_id}]|" + canonical_strategy(cont.investor_strategy)


def _same_profile(a: OrderProfile, b: OrderProfile) -> bool:
    def side(qs, ws):
        return sorted((float(q), float(w)) for q, w in zip(qs, ws) if w > 0)
    for sa, sb in ((side(a.q_H, a.w_H), side(b.q_H, b.w_H)), (side(a.q_L, a.w_L), side(b.q_L, b.w_L))):
        if len(sa) != len(sb):
            return False
        if any(abs(x[0] - y[0]) > ORDER_IDENTITY_TOL or abs(x[1] - y[1]) > ORDER_IDENTITY_TOL for x, y in zip(sa, sb)):
            return False
    return True


def _same_atoms(a: PriceInformation, b: PriceInformation, controls: Controls) -> bool:
    fa = sorted((x for x in a.atoms if x.probability > controls.probability_acceptance), key=lambda x: x.atom_value)
    fb = sorted((x for x in b.atoms if x.probability > controls.probability_acceptance), key=lambda x: x.atom_value)
    if len(fa) != len(fb):
        return False
    for x, y in zip(fa, fb):
        if x.kind != y.kind or abs(x.atom_value - y.atom_value) > ATOM_IDENTITY_TOL or abs(x.mass_H - y.mass_H) > ATOM_IDENTITY_TOL \
                or abs(x.mass_L - y.mass_L) > ATOM_IDENTITY_TOL or abs(x.posterior - y.posterior) > ATOM_IDENTITY_TOL:
            return False
        if len(x.preimage) != len(y.preimage):
            return False
        if any(u != v and (not np.isfinite(u) or not np.isfinite(v) or abs(u - v) > ORDER_IDENTITY_TOL)
               for ix, iy in zip(x.preimage, y.preimage) for u, v in zip(ix, iy)):
            return False
    return True


def economically_equivalent(a: Continuation, b: Continuation, controls: Controls) -> bool:
    """Pairwise identity test: same parameter set, institution, information, tie rule, complete strategies,
    pricing family, preparation rule, and positive-mass price atoms (within the identity tolerances)."""
    return (a.parameter_set_id == b.parameter_set_id and a.institution_id == b.institution_id
            and a.information_structure_id == b.information_structure_id and a.tie_rule_id == b.tie_rule_id
            and _same_profile(a.investor_strategy, b.investor_strategy)
            and a.pricing_rule.rule_family == b.pricing_rule.rule_family
            and a.pricing_rule.positive_entry_price_map == b.pricing_rule.positive_entry_price_map
            and a.price_information.posterior_map == b.price_information.posterior_map
            and a.preparation_rule.definition() == b.preparation_rule.definition()
            and _same_atoms(a.price_information, b.price_information, controls))


def deduplicate(conts: Sequence[Continuation], controls: Controls) -> tuple[tuple[Continuation, ...], dict[str, tuple[str, ...]]]:
    """Group economically equivalent continuations. Returns representatives (first found) and a map from each
    representative's continuation_id to every candidate_id it absorbed. The raw attempts are not discarded."""
    reps: list[Continuation] = []
    absorbed: dict[str, list[str]] = {}
    for c in conts:
        for rep in reps:
            if economically_equivalent(c, rep, controls):
                absorbed[rep.continuation_id].append(c.candidate_id)
                break
        else:
            reps.append(c)
            absorbed[c.continuation_id] = [c.candidate_id]
    return tuple(reps), {k_: tuple(v_) for k_, v_ in absorbed.items()}


# ---------------------------------------------------------------------------------------------
# exact auction payoffs on the full reserve domain (Fraction or mpf arithmetic)
# ---------------------------------------------------------------------------------------------
def payoff_regime(ell, h, r, p) -> str:
    """Regime of the reserve on the full domain, decided by exact comparisons of the supplied numbers."""
    if p < 0:
        raise ValueError("reserve below zero")
    if p < ell:
        return "p<ell<r<h (benchmark support)" if ell < r < h else "p<ell (nonbenchmark ordering of ell, r, h)"
    if p == ell:
        return "p=ell (low value bids at the reserve; admissible by the tie rule)"
    if p < r:
        return "ell<p<r (low value excluded; incumbent can exceed the reserve)"
    if p == r:
        return "p=r (incumbent support top equals reserve)"
    if p < h:
        return "r<p<h (only the high value can meet the reserve)"
    if p == h:
        return "p=h (high value bids at the reserve; zero acquisition rent)"
    return "p>h (no sale possible)"


def kernel_exact(r, v, p):
    """(t_v, g_v) of OA.51 in the arithmetic of the inputs (Fraction or mpf). Mirrors auction.kernel_uniform."""
    t_0 = p * (1 - p / r) if p <= r else 0 * p
    if v < p:
        return t_0, 0 * p
    if v < r:
        return v - (v * v - p * p) / (2 * r), (v * v - p * p) / (2 * r)
    if p <= r <= v:
        t_v = r / 2 + p * p / (2 * r)
        return t_v, v - t_v
    return p, v - p


def payoffs_exact(prim: Primitives, r, p) -> dict:
    """Binary-value payoffs {t_0, t_H, t_L, g_H, g_L, Delta_T} in exact arithmetic (Fraction for rational inputs)."""
    conv = Fraction if isinstance(p, Fraction) else (lambda s: mp.mpf(s))
    h, ell = conv(prim.h), conv(prim.ell)
    t_0 = p * (1 - p / r) if p <= r else 0 * p
    t_H, g_H = kernel_exact(r, h, p)
    t_L, g_L = kernel_exact(r, ell, p)
    return {"t_0": t_0, "t_H": t_H, "t_L": t_L, "g_H": g_H, "g_L": g_L, "Delta_T": t_H - t_L,
            "regime": payoff_regime(ell, h, r, p)}


def to_float_payoffs(ex: dict, r, p) -> AuctionPayoffs:
    return AuctionPayoffs(r=float(r), p=float(p), t_0=float(ex["t_0"]), t_H=float(ex["t_H"]), t_L=float(ex["t_L"]),
                          g_H=float(ex["g_H"]), g_L=float(ex["g_L"]))


# ---------------------------------------------------------------------------------------------
# Laplace CDF / survival in high precision (CDF F_Z, survival S_Z = 1 - F_Z: kept distinct)
# ---------------------------------------------------------------------------------------------
def laplace_cdf_mp(z, b):
    return mp.mpf(1) / 2 * mp.exp(z / b) if z <= 0 else 1 - mp.mpf(1) / 2 * mp.exp(-z / b)


def laplace_survival_mp(z, b):
    return 1 - laplace_cdf_mp(z, b)


# ---------------------------------------------------------------------------------------------
# pooled schedule: fixed orders, explicit lower-tail zero-entry pool, prescribed preparation
# ---------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class PooledSchedule:
    """Complete candidate: orders, lower cutoff pool at t_0, preparation prescribed by observed-price region.

    Duck-types the `Schedule` interface used by the deviation layer (prim, pay, profile, breakpoints,
    hull, A, mu, entry, price). `pool_posterior` is the pooled posterior of the zero-entry atom (OA.70)
    and is the buyer's information there; `raw_posterior_in_pool` reproduces the incorrect policy in
    which the buyer acts on mu_X inside the pool and exists only as a negative control.
    """
    prim: Primitives
    pay: AuctionPayoffs
    profile: OrderProfile
    cutoff: float
    prep_zero: tuple[bool, bool]         # (low cost prepares, high cost prepares) at the zero-entry price atom
    prep_positive: tuple[bool, bool]     # (low cost prepares, high cost prepares) at positive-entry prices
    pool_posterior: float
    regime: str = "feedback"
    dividend: float = 0.0
    breakpoints: tuple[float, ...] = ()
    raw_posterior_in_pool: bool = False

    def mu(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        aH = self.profile.a(self.prim.noise, self.prim.fb, x, "H")
        aL = self.profile.a(self.prim.noise, self.prim.fb, x, "L")
        return aH / (aH + aL)

    def _entry_level(self, prep: tuple[bool, bool]) -> float:
        rho = self.prim.frho
        return rho * float(prep[0]) + (1 - rho) * float(prep[1])

    def entry_from_mu_region(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        if self.raw_posterior_in_pool:
            # negative control: pointwise cost comparison on raw mu_X everywhere (not price-measurable)
            from .information import entry_at_posterior
            return entry_at_posterior(self.prim, self.pay, self.mu(x))
        return np.where(x < self.cutoff, self._entry_level(self.prep_zero), self._entry_level(self.prep_positive))

    def entry(self, x: np.ndarray) -> np.ndarray:
        return self.entry_from_mu_region(x)

    def public_posterior(self, x: np.ndarray) -> np.ndarray:
        """Buyer's posterior at the observed price: pooled on the zero-entry atom, mu_X where the price reveals it."""
        x = np.asarray(x, dtype=float)
        return np.where(x < self.cutoff, self.pool_posterior, self.mu(x))

    def price(self, x: np.ndarray) -> np.ndarray:
        mu = self.mu(x)
        e = self.entry(x)
        return self.pay.t_0 + e * (self.pay.w_L + self.pay.Delta_T * mu) + self.dividend

    def A(self, x: np.ndarray, state: str) -> np.ndarray:
        mu = self.mu(x)
        e = self.entry(x)
        return e * self.pay.Delta_T * (1 - mu) if state == "H" else e * self.pay.Delta_T * mu

    def A_direct(self, x: np.ndarray, state: str) -> np.ndarray:
        e = self.entry(x)
        P = self.price(x)
        if state == "H":
            return self.pay.t_0 + e * self.pay.w_H + self.dividend - P
        return P - (self.pay.t_0 + e * self.pay.w_L + self.dividend)

    def hull(self) -> tuple[float, float]:
        s = self.profile.supports
        return min(s), max(s)


def pool_masses_closed_form(prim: Primitives, profile: OrderProfile, cutoff_mp, dps: int = 50) -> dict:
    """Closed-form (mpmath) masses of the lower pool {x < c} for pure Laplace orders: F_Z(c - q_theta)."""
    if prim.noise != Noise.LAPLACE or not profile.is_pure:
        raise ValueError("closed-form pool masses require Laplace noise and pure orders")
    with mp.workdps(dps):
        b = mp.mpf(prim.b)
        pi = mp.mpf(prim.fundamental_prior_H)
        mH = laplace_cdf_mp(cutoff_mp - mp.mpf(profile.q_H[0]), b)
        mL = laplace_cdf_mp(cutoff_mp - mp.mpf(profile.q_L[0]), b)
        prob = pi * mH + (1 - pi) * mL
        post = pi * mH / prob if prob > 0 else mp.mpf("nan")
        return {"mass_H": mH, "mass_L": mL, "probability": prob, "posterior": post}


def make_pooled_schedule(prim: Primitives, pay: AuctionPayoffs, profile: OrderProfile, cutoff: float,
                         prep_zero: tuple[bool, bool], prep_positive: tuple[bool, bool],
                         pool_posterior: float | None = None, raw_posterior_in_pool: bool = False) -> PooledSchedule:
    """Build the complete candidate; the pooled posterior defaults to the closed form for pure Laplace orders."""
    if pool_posterior is None:
        pool_posterior = float(pool_masses_closed_form(prim, profile, mp.mpf(cutoff))["posterior"])
    bps = tuple(sorted(set(profile.supports) | {float(cutoff)}))
    return PooledSchedule(prim, pay, profile, float(cutoff), tuple(prep_zero), tuple(prep_positive), float(pool_posterior),
                          breakpoints=bps, raw_posterior_in_pool=raw_posterior_in_pool)


def _flow_integral(sched: PooledSchedule, fun, n: int = 48) -> float:
    lo, hi = sched.hull()
    bps = list(sched.breakpoints)
    lo, hi = min([lo, *bps]) - 1.0, max([hi, *bps]) + 1.0
    b = sched.prim.fb
    T = 60.0 * b
    return integrate_segments(fun, segments([lo - T, lo, *bps, hi, hi + T], b), n)


# ---------------------------------------------------------------------------------------------
# global rational bound for full orders against a lower-cutoff pool (spec 8.5)
# ---------------------------------------------------------------------------------------------
def _rational_upper(x_mp, digits: int = 40) -> Fraction:
    """A rational strictly above the high-precision value (outward rounding)."""
    return Fraction(mp.nstr(x_mp, digits, strip_zeros=False)) + Fraction(1, 10 ** (digits - 5))


def rational_full_order_bound(prim: Primitives, Delta_T_exact: Fraction, cutoff_upper: Fraction) -> dict:
    """Exact-rational lower bound on U_theta'(s) for correctly signed full orders (1, -1) with a lower pool.

    Hypotheses (checked by the caller numerically and structurally): Laplace noise; residuals nonnegative;
    the pool is contained in {x < cutoff} with cutoff <= 1 so that x >= 1 is active with entry at least rho;
    on x >= 1 the posterior is the upper plateau M, so 1 - mu = m. Then J = F_H(1) = F_L(1) >= rho Delta m / 2
    and U'(s) >= (1 - 1/b) J - k for every s in [0, 1] (density-ratio bound with |F'| <= F / b).
    """
    if prim.noise != Noise.LAPLACE:
        return {"available": False, "reason": "bound derived for Laplace noise only"}
    if cutoff_upper > 1:
        return {"available": False, "reason": "pool cutoff exceeds 1: x >= 1 is not fully active"}
    rho, b, k = Fraction(Decimal(prim.rho)), Fraction(Decimal(prim.b)), Fraction(Decimal(prim.k))
    with mp.workdps(60):
        e_ub = _rational_upper(mp.exp(2 / mp.mpf(prim.b)))
    m_lb = 1 / (1 + e_ub)
    J_lb = rho * Delta_T_exact * m_lb / 2
    Up_lb = (1 - 1 / b) * J_lb - k
    return {"available": True, "m_lower_bound": m_lb, "J_lower_bound": J_lb, "Uprime_lower_bound": Up_lb,
            "positive": Up_lb > 0, "reason": ""}


# ---------------------------------------------------------------------------------------------
# validation of a pooled schedule (spec 7.4): atoms, buyer optimality, pointwise pricing, collisions,
# investor deviations over the full order interval, closed forms versus integration
# ---------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class PooledValidation:
    atoms: tuple[PriceAtom, ...]
    outcome: ContinuationOutcome
    evidence: ValidationEvidence
    buyer_slack: dict
    global_bound: dict
    closed_forms: dict
    scans: dict


def _cost_labels(prim: Primitives) -> tuple[tuple[str, float], ...]:
    if prim.cost_law != CostLaw.ATOMS:
        raise ValueError("pooled-schedule validation is implemented for the atomic cost law")
    return (("c_L", prim.fc_L), ("c_H", prim.fc_H))


def validate_pooled_schedule(sched: PooledSchedule, controls: Controls, cutoff_exact=None,
                             pool_is_null_expected: bool = False) -> PooledValidation:
    """Apply the C.0 tolerances to a complete pooled candidate. Every breach is recorded; none is loosened."""
    prim, pay = sched.prim, sched.pay
    rho = prim.frho
    breaches: list[str] = []
    pi = float(Decimal(prim.fundamental_prior_H))
    aH = lambda x: sched.profile.a(prim.noise, prim.fb, x, "H")
    aL = lambda x: sched.profile.a(prim.noise, prim.fb, x, "L")
    g = lambda x: pi * aH(x) + (1 - pi) * aL(x)
    below = lambda x: (np.asarray(x, dtype=float) < sched.cutoff).astype(float)

    # --- price atom: full preimage, state masses, pooled posterior (OA.70) ----------------------
    mH_int = _flow_integral(sched, lambda x: aH(x) * below(x))
    mL_int = _flow_integral(sched, lambda x: aL(x) * below(x))
    prob_int = pi * mH_int + (1 - pi) * mL_int
    post_int = pi * mH_int / prob_int if prob_int > 0 else float("nan")
    belief_err = 0.0
    cf = {}
    if prim.noise == Noise.LAPLACE and sched.profile.is_pure:
        c_mp = mp.mpf(sched.cutoff) if cutoff_exact is None else cutoff_exact
        cfm = pool_masses_closed_form(prim, sched.profile, c_mp)
        cf = {k_: float(v_) for k_, v_ in cfm.items()}
        belief_err = max(abs(cf["mass_H"] - mH_int), abs(cf["mass_L"] - mL_int), abs(cf["probability"] - prob_int))
        if prob_int > 0:
            belief_err = max(belief_err, abs(cf["posterior"] - post_int))
        if belief_err > controls.independent_formula_acceptance:
            breaches.append(f"pool_mass_closed_form_vs_integration={belief_err:.3e}")
        if prob_int > controls.probability_acceptance and abs(sched.pool_posterior - cf["posterior"]) > controls.probability_acceptance:
            breaches.append(f"pooled_posterior_used_by_buyer_differs_from_OA70={abs(sched.pool_posterior - cf['posterior']):.3e}")
    e_zero = sched._entry_level(sched.prep_zero)
    e_pos = sched._entry_level(sched.prep_positive)
    atoms = []
    if prob_int > controls.probability_acceptance:
        kind = "no_entry_pool" if e_zero == 0.0 else "positive_entry_pool"
        atoms.append(PriceAtom(pay.t_0 + e_zero * (pay.w_L + pay.Delta_T * post_int) if e_zero > 0 else pay.t_0,
                               ((-np.inf, sched.cutoff),), mH_int, mL_int, prob_int, post_int, kind))
    # upper plateau (Laplace, pure orders): a positive-entry price atom that must be conditioned on correctly
    if prim.noise == Noise.LAPLACE and sched.profile.is_pure and e_pos > 0:
        hi = sched.hull()[1]
        lo_pl = max(hi, sched.cutoff)
        mHp = float(survival(prim.noise, lo_pl - sched.profile.q_H[0], prim.fb))
        mLp = float(survival(prim.noise, lo_pl - sched.profile.q_L[0], prim.fb))
        probp = pi * mHp + (1 - pi) * mLp
        M_post = float(sched.mu(np.array([lo_pl + 1.0]))[0])
        atoms.append(PriceAtom(float(sched.price(np.array([lo_pl + 1.0]))[0]), ((lo_pl, np.inf),), mHp, mLp, probp,
                               pi * mHp / probp, "positive_entry_plateau"))
        if abs(pi * mHp / probp - M_post) > controls.probability_acceptance:
            breaches.append(f"upper_plateau_posterior_mismatch={abs(pi * mHp / probp - M_post):.3e}")

    # --- information consistency: the buyer's action must be measurable with respect to the price ------
    if sched.raw_posterior_in_pool:
        xs_pool = np.linspace(sched.cutoff - 3.0, sched.cutoff - 1e-9, 601)
        e_in_pool = sched.entry(xs_pool)
        if prob_int > controls.probability_acceptance and float(e_in_pool.max() - e_in_pool.min()) > 0:
            breaches.append("preparation_not_price_measurable: buyer acts on raw mu_X inside a single price atom")

    # --- buyer optimality at each price information set (tie: equality admitted) --------------------
    slack = {}
    eps_e = 0.0
    B_pool = pay.B(post_int) if prob_int > controls.probability_acceptance else float("nan")
    for i, (lab, c) in enumerate(_cost_labels(prim)):
        if prob_int > controls.probability_acceptance:
            prep = sched.prep_zero[i]
            gain = (c - B_pool) if prep else (B_pool - c)       # profit from reversing the prescribed action
            slack[f"zero_price_{lab}"] = -gain
            eps_e = max(eps_e, max(gain, 0.0))
            if gain > controls.entry_optimality_acceptance:
                breaches.append(f"buyer_deviation_at_zero_price_{lab}: pooled posterior {post_int:.10f}, B={B_pool:.6f}, gain={gain:.3e}")
    # positive-entry region: the price reveals mu_X, so the comparison is pointwise on x >= cutoff
    xs = np.array(sorted(set(np.linspace(sched.cutoff, max(sched.cutoff, sched.hull()[1]) + controls.initial_flow_halfwidth, 4001).tolist())
                         | {sched.cutoff, *[bp for bp in sched.breakpoints if bp >= sched.cutoff]}))
    mu_pos = sched.mu(xs)
    B_pos = pay.B(mu_pos)
    for i, (lab, c) in enumerate(_cost_labels(prim)):
        prep = sched.prep_positive[i]
        gain = (c - B_pos) if prep else (B_pos - c)
        slack[f"positive_price_{lab}_min"] = float(-gain.max())
        worst = float(gain.max())
        eps_e = max(eps_e, max(worst, 0.0))
        if worst > controls.entry_optimality_acceptance:
            xw = float(xs[int(gain.argmax())])
            breaches.append(f"buyer_deviation_at_positive_price_{lab}: x={xw:.6f}, mu_X={float(sched.mu(np.array([xw]))[0]):.6f}, "
                            f"B={float(pay.B(sched.mu(np.array([xw]))[0])):.6f}, gain={worst:.3e}")

    # --- pointwise conditional pricing on both regions --------------------------------------------
    xs_all = np.array(sorted(set(np.linspace(sched.cutoff - controls.initial_flow_halfwidth, sched.cutoff + controls.initial_flow_halfwidth, 8001).tolist())
                             | set(sched.breakpoints) | {sched.cutoff - 1e-9, sched.cutoff}))
    mu_all = sched.mu(xs_all)
    e_all = sched.entry(xs_all)
    P_all = sched.price(xs_all)
    EV_all = pay.t_0 + e_all * (mu_all * pay.w_H + (1 - mu_all) * pay.w_L) + sched.dividend
    eps_P = float(np.max(np.abs(P_all - EV_all)))
    if sched.raw_posterior_in_pool and prob_int > controls.probability_acceptance:
        # the prescribed price on the pool is the atom t_0, so the pricing error of the altered policy is measured against it
        in_pool = xs_all < sched.cutoff
        eps_P = max(eps_P, float(np.max(np.abs(pay.t_0 - EV_all[in_pool]))))
    resid_err = max(float(np.max(np.abs(sched.A(xs_all, s) - sched.A_direct(xs_all, s)))) for s in "HL")
    if eps_P > controls.price_identity_acceptance:
        breaches.append(f"epsilon_P={eps_P:.3e}")
    if resid_err > controls.price_identity_acceptance:
        breaches.append(f"residual_direct_error={resid_err:.3e}")
    # collision: positive-entry prices must stay away from the zero-entry atom, else they share one preimage
    pos = xs_all >= sched.cutoff
    if prob_int > controls.probability_acceptance and pos.any():
        atom_value = atoms[0].atom_value
        gap = float(np.min(np.abs(P_all[pos] - atom_value)))
        if gap <= controls.price_identity_acceptance:
            breaches.append(f"price_collision: positive-entry price meets the pool atom (gap {gap:.3e}); one preimage")
        if e_pos > 0 and pay.Delta_T > 0 and not sched.raw_posterior_in_pool:
            if np.any(np.diff(P_all[pos]) < -controls.price_identity_acceptance):
                breaches.append("positive-entry price not monotone: posterior not recoverable from the price")
    inv_err = 0.0
    if e_pos > 0 and pay.Delta_T > 0 and not sched.raw_posterior_in_pool:
        # posterior map on nonpooled prices: invert P = t_0 + e_pos (w_L + Delta mu) directly
        mu_rec = (P_all[pos] - pay.t_0 - sched.dividend) / e_pos - pay.w_L
        mu_rec = mu_rec / pay.Delta_T
        inv_err = float(np.max(np.abs(mu_rec - mu_all[pos])))
        if inv_err > 1e-7:
            breaches.append(f"posterior_inversion_error={inv_err:.3e}")

    # --- probability identities --------------------------------------------------------------------
    ident = {"int_a_H": abs(_flow_integral(sched, aH) - 1), "int_a_L": abs(_flow_integral(sched, aL) - 1),
             "E_mu": abs(_flow_integral(sched, lambda x: g(x) * sched.mu(x)) - pi)}
    for k_, v_ in ident.items():
        if v_ > controls.probability_acceptance:
            breaches.append(f"{k_}={v_:.3e}")

    # --- outcome measures by conditional integration ----------------------------------------------
    eH = _flow_integral(sched, lambda x: aH(x) * sched.entry(x))
    eL = _flow_integral(sched, lambda x: aL(x) * sched.entry(x))
    E = pi * eH + (1 - pi) * eL
    h, ell, p, r = prim.fh, prim.fell, pay.p, pay.r
    admit_H, admit_L = float(h >= p), float(ell >= p)
    A = pi * eH * admit_H + (1 - pi) * eL * admit_L
    pr_R = max(0.0, 1.0 - p / r) if p <= r else 0.0
    C2 = pr_R * A
    S = pr_R + A - C2
    # allocation event for the high-value challenger: prepared, admissible, and R < h
    O_H = pi * eH * admit_H * min(h / r, 1.0)
    R_T = pay.t_0 + pi * eH * pay.w_H + (1 - pi) * eL * pay.w_L
    EP = _flow_integral(sched, lambda x: g(x) * sched.price(x))
    if abs(EP - R_T) > controls.probability_acceptance:
        breaches.append(f"E_P_minus_E_V={abs(EP - R_T):.3e}")
    if not (0 <= C2 <= A + 1e-15 and A <= E + 1e-15 and E <= 1 + 1e-15 and 0 <= S <= 1 + 1e-15):
        breaches.append(f"outcome_bounds: C2={C2}, A={A}, E={E}, S={S}")
    # independent union-event integration of the sale probability, state by state
    S_union = (pi * _flow_integral(sched, lambda x: aH(x) * (pr_R + (1 - pr_R) * sched.entry(x) * admit_H))
               + (1 - pi) * _flow_integral(sched, lambda x: aL(x) * (pr_R + (1 - pr_R) * sched.entry(x) * admit_L)))
    if abs(S_union - S) > controls.independent_formula_acceptance:
        breaches.append(f"sale_union_identity={abs(S_union - S):.3e}")
    outcome = ContinuationOutcome(eH, eL, E, A, S, C2, O_H, R_T, EP)

    # --- investor deviations over the full order interval, both signs, both types ----------------
    scans = {}
    eps_q, qerr, tb = 0.0, 0.0, 0.0
    for s in "HL":
        sc = deviation_scan(sched, s, controls.initial_order_intervals, [sched.cutoff, -sched.cutoff])
        scans[s] = sc
        eps_q = max(eps_q, sc["max_gain"])
        qerr = max(qerr, max(rw[4] for rw in sc["rows"]))
        tb = max(tb, max(rw[5] for rw in sc["rows"]))
        sc2 = deviation_scan(sched, s, controls.refined_order_intervals, [sched.cutoff, -sched.cutoff], n=64)
        scans[s + "_refined"] = sc2
        eps_q = max(eps_q, sc2["max_gain"])
    if eps_q > controls.deviation_gain_acceptance:
        breaches.append(f"epsilon_q={eps_q:.3e}")

    # --- global rational bound (proof) and mesh derivative scan (implementation check) ------------
    gb: dict = {"available": False, "reason": "not a pure full-order profile"}
    full = sched.profile.is_pure and sched.profile.q_H[0] == 1.0 and sched.profile.q_L[0] == -1.0
    if full and pay.Delta_T > 0 and sched.prep_positive[0] and not sched.raw_posterior_in_pool:
        Delta_exact = Fraction(Decimal(repr(pay.t_H))) - Fraction(Decimal(repr(pay.t_L)))
        c_up = Fraction(Decimal(repr(sched.cutoff))) + Fraction(1, 10 ** 12)
        gb = rational_full_order_bound(prim, Delta_exact, c_up)
        if gb["available"]:
            gb["hypothesis_residuals_nonnegative"] = bool(np.all(sched.A(xs_all, "H") >= 0) and np.all(sched.A(xs_all, "L") >= 0))
            gb["hypothesis_entry_on_upper_region_at_least_rho"] = bool(e_pos >= rho - 1e-15)
            JH, JL = F(sched, "H", 1.0).value, F(sched, "L", 1.0).value
            gb["J_H"], gb["J_L"] = JH, JL
            gb["J_gap"] = abs(JH - JL)
            n_mesh = 200
            dmin = min(min(dU(sched, s, j / n_mesh).value for j in range(n_mesh + 1)) for s in "HL")
            gb["min_dU_mesh"] = dmin
            gb["J_numeric_consistent"] = bool(min(JH, JL) + controls.independent_formula_acceptance >= float(gb["J_lower_bound"]))
            gb["dU_mesh_consistent"] = bool(dmin + controls.deviation_gain_acceptance >= float(gb["Uprime_lower_bound"]))
            if gb["J_gap"] > controls.independent_formula_acceptance:
                breaches.append(f"J_H_minus_J_L={gb['J_gap']:.3e}")
            if not gb["J_numeric_consistent"] or not gb["dU_mesh_consistent"]:
                breaches.append("global_bound_implementation_check_failed: numeric J or mesh derivative below the rational bound")
    upper = 0.0 if (gb.get("available") and gb.get("positive") and gb.get("hypothesis_residuals_nonnegative")
                    and gb.get("hypothesis_entry_on_upper_region_at_least_rho")) else None
    evidence = ValidationEvidence(eps_P, belief_err, eps_e, eps_q, upper, qerr + tb,
                                  support_evidence="pure orders: deviation scan on the declared and refined order grids over [-1, 1], both signs",
                                  arithmetic_evidence="pool masses: mpmath closed form (50 digits) vs segment-wise Gauss-Legendre integration; "
                                                      "Laplace tails analytic", breaches=tuple(breaches))
    return PooledValidation(tuple(atoms), outcome, evidence, slack, gb, cf, scans)


# ---------------------------------------------------------------------------------------------
# CSV schema (spec 16.1) and row construction
# ---------------------------------------------------------------------------------------------
SCHEMA_COLUMNS = [
    "candidate_id", "continuation_id", "parameter_set_id", "institution_id", "information_structure_id", "order_rule_id",
    "price_rule_id", "pricing_family_coverage", "exhaustive_pricing_search", "pool_id", "pool_set_definition", "pool_cutoff_exact",
    "price_atom_value", "state_H_pool_mass", "state_L_pool_mass", "pool_probability", "pool_posterior", "preparation_rule_id",
    "tie_rule_id", "event_id", "event_defining_relation", "preparation_probability", "admissible_challenger_probability",
    "sale_probability", "two_admissible_bidders_probability", "high_value_ownership_probability", "seller_revenue",
    "mean_financial_price", "pricing_error", "belief_error", "entry_deviation_gain", "investor_deviation_gain_estimate",
    "investor_deviation_gain_upper_bound", "error_budget", "result_status", "existence_scope", "uniqueness_scope",
    "search_coverage_scope", "accepted", "rejection_reason", "unresolved_reason", "run_id",
]


def _na(v) -> object:
    return NA if v is None else v


def continuation_row(c: Continuation) -> dict:
    """Wide-schema row. `n/a` marks unavailable fields; a missing rigorous bound is never written as zero."""
    pools = [a for a in c.price_information.atoms if a.kind.endswith("pool")]
    pool = pools[0] if pools else None
    return {
        "candidate_id": c.candidate_id, "continuation_id": c.continuation_id, "parameter_set_id": c.parameter_set_id,
        "institution_id": c.institution_id, "information_structure_id": c.information_structure_id,
        "order_rule_id": canonical_strategy(c.investor_strategy), "price_rule_id": c.pricing_rule.definition(),
        "pricing_family_coverage": c.pricing_family_coverage, "exhaustive_pricing_search": c.exhaustive_pricing_search,
        "pool_id": (pool.kind + "@" + repr(pool.atom_value)) if pool else "none",
        "pool_set_definition": ";".join(f"[{a},{b_})" for a, b_ in c.pricing_rule.pool_sets) or "none",
        "pool_cutoff_exact": c.pricing_rule.pool_cutoff_exact,
        "price_atom_value": pool.atom_value if pool else NA, "state_H_pool_mass": pool.mass_H if pool else NA,
        "state_L_pool_mass": pool.mass_L if pool else NA, "pool_probability": pool.probability if pool else 0.0,
        "pool_posterior": pool.posterior if pool else NA, "preparation_rule_id": c.preparation_rule.definition(),
        "tie_rule_id": c.tie_rule_id, "event_id": c.event_id, "event_defining_relation": c.event_defining_relation,
        "preparation_probability": c.outcome.E, "admissible_challenger_probability": c.outcome.A, "sale_probability": c.outcome.S,
        "two_admissible_bidders_probability": c.outcome.C2, "high_value_ownership_probability": c.outcome.O_H,
        "seller_revenue": c.outcome.R_T, "mean_financial_price": c.outcome.mean_price,
        "pricing_error": c.validation.pricing_error, "belief_error": c.validation.belief_error,
        "entry_deviation_gain": c.validation.entry_deviation_gain,
        "investor_deviation_gain_estimate": c.validation.investor_deviation_gain_estimate,
        "investor_deviation_gain_upper_bound": _na(c.validation.investor_deviation_gain_upper_bound),
        "error_budget": c.validation.error_budget, "result_status": c.result_status, "existence_scope": c.existence_scope,
        "uniqueness_scope": c.uniqueness_scope, "search_coverage_scope": c.search_coverage_scope, "accepted": c.accepted,
        "rejection_reason": c.rejection_reason, "unresolved_reason": c.unresolved_reason, "run_id": c.run_id,
    }


# ---------------------------------------------------------------------------------------------
# adapter: existing Schedule + Validation (validation.validate) -> Continuation
# ---------------------------------------------------------------------------------------------
def _interval_point(lo: float, hi: float, scale: float) -> float:
    if not np.isfinite(lo):
        return hi - scale if np.isfinite(hi) else 0.0
    return lo + scale if not np.isfinite(hi) else (lo + hi) / 2


def _interval_mass(sched, preimage: Sequence[tuple[float, float]], state: str) -> float:
    qs, ws = (sched.profile.q_H, sched.profile.w_H) if state == "H" else (sched.profile.q_L, sched.profile.w_L)
    def tail(x: float, q: float) -> float:
        if x == -np.inf:
            return 1.0
        if x == np.inf:
            return 0.0
        return float(survival(sched.prim.noise, x - q, sched.prim.fb))
    return sum(w * (tail(lo, q) - tail(hi, q)) for lo, hi in preimage for q, w in zip(qs, ws) if w > 0)


def schedule_price_atoms(sched, controls: Controls) -> tuple[tuple[PriceAtom, ...], tuple[str, ...], float]:
    """Find full constant-price preimages on the candidate's threshold/support partition.

    Between consecutive Laplace supports, the posterior is a ratio of two
    linear combinations of exp(x/b) and exp(-x/b). Its derivative has constant
    sign, so its flat pieces and the schedule's threshold crossings suffice.
    Nonmonotone candidates can have unions of intervals at the same price.
    """
    prim, pay = sched.prim, sched.pay
    pi = float(Decimal(prim.fundamental_prior_H))
    edges = [-np.inf, *sorted(set(sched.breakpoints) | set(sched.profile.supports)), np.inf]
    groups: list[tuple[float, list[tuple[float, float]], list[float]]] = []
    breaches = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        x = _interval_point(lo, hi, prim.fb)
        entry = float(sched.entry(np.array([x]))[0])
        constant_mu = False
        if prim.noise == Noise.LAPLACE:
            coefficients = []
            for qs, ws in ((sched.profile.q_H, sched.profile.w_H), (sched.profile.q_L, sched.profile.w_L)):
                coefficients.append((sum(w * np.exp((q - x) / prim.fb) for q, w in zip(qs, ws) if q <= x),
                                     sum(w * np.exp((x - q) / prim.fb) for q, w in zip(qs, ws) if q > x)))
            (hl, hr), (ll, lr) = coefficients
            constant_mu = abs(hl * lr - hr * ll) <= 1e-14 * (hl + hr) * (ll + lr)
        else:
            constant_mu = sched.profile.q_H == sched.profile.q_L and sched.profile.w_H == sched.profile.w_L
        constant = entry == 0 or constant_mu or (pay.Delta_T == 0 and (prim.cost_law == CostLaw.ATOMS or sched.regime == "price_hidden"))
        if not constant:
            continue
        price = float(sched.price(np.array([x]))[0])
        for value, intervals, entries in groups:
            if abs(value - price) <= 1e-13:
                if intervals[-1][1] == lo:
                    intervals[-1] = (intervals[-1][0], hi)
                else:
                    intervals.append((lo, hi))
                entries.append(entry)
                break
        else:
            groups.append((price, [(lo, hi)], [entry]))
    atoms = []
    belief_error = 0.0
    for price, intervals, entries in groups:
        mH, mL = (_interval_mass(sched, intervals, state) for state in "HL")
        probability = pi * mH + (1 - pi) * mL
        if probability <= controls.probability_acceptance:
            continue
        posterior = pi * mH / probability
        for state, mass in (("H", mH), ("L", mL)):
            def density_on_atom(x, state=state):
                inside = np.zeros_like(x, dtype=bool)
                for lo, hi in intervals:
                    inside |= (x >= lo) & (x < hi)
                return sched.profile.a(prim.noise, prim.fb, x, state) * inside
            mass_error = abs(_flow_integral(sched, density_on_atom) - mass)
            belief_error = max(belief_error, mass_error)
            if mass_error > controls.probability_acceptance:
                breaches.append(f"price_atom_mass_{state}_error={mass_error:.3e}")
        kind = "no_entry_pool" if max(entries) == 0 else "positive_entry_plateau"
        atom = PriceAtom(price, tuple(intervals), mH, mL, probability, posterior, kind)
        atoms.append(atom)
        buyer_mu = pi if sched.regime == "price_hidden" else posterior
        optimal_entry = float(entry_at_posterior(prim, pay, np.array([buyer_mu]))[0])
        # Exact floor/ceiling events prescribe entry at equality independently
        # of the final binary rounding of the declared event value.
        if sched.tie_at_floor and abs(pay.B(buyer_mu) - prim.fc_L) <= controls.entry_optimality_acceptance:
            optimal_entry = max(optimal_entry, prim.frho)
        if sched.tie_at_ceiling and abs(pay.B(buyer_mu) - prim.fc_H) <= controls.entry_optimality_acceptance:
            optimal_entry = 1.0
        if max(abs(entry - optimal_entry) for entry in entries) > controls.probability_acceptance:
            breaches.append(f"price_atom_preparation_inconsistent:P={price:.12g},mu={posterior:.12g}")
        # Conditional price on an atom must also equal the atom-conditioned
        # target payoff. This catches collisions with different entry rules.
        expected_price = pay.t_0 + optimal_entry * (pay.w_L + pay.Delta_T * posterior) + sched.dividend
        if abs(price - expected_price) > controls.price_identity_acceptance:
            breaches.append(f"price_atom_pricing_error={abs(price - expected_price):.3e}")
        if not all(np.isfinite(v) for v in (price, mH, mL, probability, posterior)):
            breaches.append("price_atom_nonfinite")
        if sched.regime == "feedback" and kind != "no_entry_pool":
            for lo, hi in intervals:
                mu = float(sched.mu(np.array([_interval_point(lo, hi, prim.fb)]))[0])
                # A constant terminal payoff need not reveal the flow posterior.
                if pay.Delta_T != 0:
                    belief_error = max(belief_error, abs(mu - posterior))
    if belief_error > controls.probability_acceptance:
        breaches.append(f"price_atom_belief_error={belief_error:.3e}")
    return tuple(sorted(atoms, key=lambda atom: atom.atom_value)), tuple(breaches), belief_error


def continuation_from_schedule(sched, val, *, candidate_id: str, parameter_set: str, information: str, controls: Controls,
                               branch: str, result_status: str, existence_scope: str, uniqueness_scope: str,
                               search_coverage_scope: str, run_id: str, event_id: str = NA, event_relation: str = NA,
                               outcome_extra: ContinuationOutcome | None = None, unresolved_reason: str = "") -> Continuation:
    """Wrap an existing benchmark-construction candidate (information.Schedule validated by validation.validate)."""
    prim, pay = sched.prim, sched.pay
    pi = float(Decimal(prim.fundamental_prior_H))
    o = val.outcome
    atoms, atom_breaches, atom_belief_error = schedule_price_atoms(sched, controls)
    pool_sets = tuple((str(lo), str(hi)) for atom in atoms if atom.kind == "no_entry_pool" for lo, hi in atom.preimage)
    family = "benchmark_inversion"
    if len(atoms) == 1 and atoms[0].preimage == ((-np.inf, np.inf),):
        family = "constant_price"
    elif pool_sets:
        family = "lower_cutoff_pool" if len(pool_sets) == 1 and pool_sets[0][0] == NEG_INF else "interval_union_pool"
    if sched.regime == "price_hidden":
        family = "price_hidden_flow_pricing"
    cutoff_exact = "x:B_r(mu_X(x))=c_min; endpoints solved from schedule threshold equations" if pool_sets else NA
    cutoff_decimal = pool_sets[0][1] if family == "lower_cutoff_pool" else NA
    entry_map = "H_C(B(prior))" if sched.regime == "price_hidden" else "H_C(B(mu_X(x)))"
    pricing = PricingRule(family, pool_sets, cutoff_exact, cutoff_decimal,
                          f"P(x)=t_0+{entry_map}[w_L+Delta_T mu_X(x)]+{sched.dividend!r}", ())
    actions = []
    # Each region is a condition on the observed-price posterior. Unlike an
    # 'enters somewhere' flag, this records both actions at a cost threshold.
    for lab, cost in (("c_L", prim.fc_L), ("c_H", prim.fc_H)):
        actions.extend(((f"nonatom_price:B(mu_P)>={cost!r}", lab, True),
                        (f"nonatom_price:B(mu_P)<{cost!r}", lab, False)))
    if prim.cost_law != CostLaw.ATOMS:
        actions = [("nonatom_price:C<=B(mu_P)", "C in declared cost support", True),
                   ("nonatom_price:C>B(mu_P)", "C in declared cost support", False)]
    for atom_index, atom in enumerate(atoms):
        mu_buyer = pi if sched.regime == "price_hidden" else atom.posterior
        region = f"price_atom[{atom_index}]"
        if prim.cost_law == CostLaw.ATOMS:
            for lab, cost in _cost_labels(prim):
                enters = bool(pay.B(mu_buyer) >= cost)
                if sched.tie_at_floor and lab == "c_L":
                    enters = True
                if sched.tie_at_ceiling and lab == "c_H" and atom.preimage[-1][1] == np.inf:
                    enters = True
                actions.append((region, lab, enters))
        else:
            actions.extend(((region + ":C<=B(mu_P)", "C in declared cost support", True),
                            (region + ":C>B(mu_P)", "C in declared cost support", False)))
    prep = PreparationRule("cost_threshold_at_price_information", tuple(actions))
    posterior_map = ("buyer posterior=prior; financial price conditions on flow" if sched.regime == "price_hidden" else
                     "mu_P=pooled Bayes posterior on each atom; invert P(mu) on nonatom positive-entry prices")
    info = PriceInformation(atoms, posterior_map, float(val.posterior_inversion_error))
    identity = continuation_identity(parameter_set, INSTITUTION_RESERVE_AUCTION, information, TIE_RULE, sched.profile, pricing, prep, info, controls)
    h, ell, p, r = prim.fh, prim.fell, pay.p, pay.r
    if outcome_extra is None:
        admit_H, admit_L = float(h >= p), float(ell >= p)
        A = pi * o.e_H * admit_H + (1 - pi) * o.e_L * admit_L
        pr_R = max(0.0, 1.0 - p / r) if p <= r else 0.0
        C2 = pr_R * A
        outcome_extra = ContinuationOutcome(o.e_H, o.e_L, o.E, A, pr_R + A - C2, C2, pi * o.e_H * admit_H * min(h / r, 1.0), o.R_T, o.mean_price)
    upper = 0.0 if result_status.startswith("analytical") and val.accepted and not atom_breaches else None
    ev = ValidationEvidence(val.epsilon_P, max(float(val.posterior_inversion_error), atom_belief_error), val.epsilon_e, max(val.epsilon_q, val.epsilon_q_refined),
                            upper, val.quadrature_error + val.tail_bound,
                            "deviation scans on declared and refined order grids over [-1, 1] against the fixed schedule",
                            "flow- and cost-based entry integrations agree; atom state masses: analytic tails versus segment quadrature",
                            tuple(val.breaches) + atom_breaches)
    if not ev.accepted:
        result_status, existence_scope, uniqueness_scope = "rejected", "none (rejected)", "not established"
    return Continuation(candidate_id, identity, parameter_set, INSTITUTION_RESERVE_AUCTION, information, TIE_RULE, sched.profile, pricing, info,
                        prep, outcome_extra, ev, result_status, existence_scope, uniqueness_scope, search_coverage_scope,
                        "benchmark construction only (pool = zero-entry preimage of the cost threshold); alternative cutoffs not scanned at this node",
                        False, event_id, event_relation, "; ".join(ev.breaches), unresolved_reason, run_id, branch)
