"""Shared helpers for exercise scripts: node classification and validation records."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..auction import AuctionPayoffs
from ..information import Schedule
from ..params import Controls, CostLaw, Primitives
from ..search import Candidate, Margins, margins
from ..validation import Validation, validate


def effective_costs(prim: Primitives) -> tuple[float, float, float]:
    """(c_L upper, c_H lower, c_H upper) endpoints used in the theorem margins (Corollary 2)."""
    if prim.cost_law == CostLaw.ATOMS:
        return prim.fc_L, prim.fc_H, prim.fc_H
    e = prim.feps_C
    return prim.fc_L + e, prim.fc_H - e, prim.fc_H + e


def theorem_margins(prim: Primitives, pay0: AuctionPayoffs, pay1: AuctionPayoffs) -> dict:
    """The five strict margins of (OA.68) at the pair (r_0, r_1), with cost-law endpoints."""
    from ..noise import posterior_bounds
    m, M = posterior_bounds(prim.fb)
    cLu, cHl, cHu = effective_costs(prim)
    rho, b, k = prim.frho, prim.fb, prim.fk
    return {
        "zeta_L": pay1.B(m) - cLu,
        "zeta_H0": cHl - pay0.B(0.5),
        "zeta_H1": pay1.B(M) - cHu,
        "zeta_0": k - pay0.Delta_T,
        "zeta_1": (1 - 1 / b) * rho * m * pay1.Delta_T - k,
    }


def node_margins(prim: Primitives, pay: AuctionPayoffs) -> Margins:
    """Margins with the cost-law endpoints substituted for the low-cost floor and prior exclusion."""
    mg = margins(prim, pay)
    if prim.cost_law == CostLaw.ATOMS:
        return mg
    from ..noise import posterior_bounds
    m, M = posterior_bounds(prim.fb)
    cLu, cHl, cHu = effective_costs(prim)
    lc = pay.B(m) - cLu
    hp = cHl - pay.B(0.5)
    return Margins(lc, hp, pay.B(M) - cHu, mg.pooling_exists, mg.pooling_unique_bound, mg.full_unique_bound, mg.e0,
                   (lc > 0) and (hp > 0))


def classify_feedback(branch: str, mg: Margins, val: Validation) -> str:
    """Status vocabulary: analytical / numerical diagnostic / open, with the supporting region."""
    if not val.accepted:
        return "rejected: " + "; ".join(val.breaches)
    if branch == "pooling":
        if mg.in_domain and mg.pooling_unique_bound > 0:
            return "analytical (unique no-trade outcome: Delta_T < k within the maintained domain)"
        if mg.pooling_exists >= 0:
            return "numerical diagnostic (pooling exists: rho Delta_T/2 <= k; uniqueness not established)"
        return "rejected: pooling coefficient positive"
    if branch == "full_orders":
        if mg.low_cost_floor > 0 and mg.full_unique_bound > 0:
            if mg.high_ceiling < 0:
                return "analytical (unique full orders; expensive entry infeasible: B_r(M) < c_H)"
            return "analytical (unique full orders: (1-1/b) rho m Delta_T > k)"
        return "numerical diagnostic (full orders validated; uniqueness not established)"
    return "numerical diagnostic"


def classify_hidden(branch: str, mg: Margins, val: Validation) -> str:
    if not val.accepted:
        return "rejected: " + "; ".join(val.breaches)
    if branch == "pooling" and mg.pooling_unique_bound > 0:
        return "analytical (price hidden; unique no trade: Delta_T < k)"
    if branch == "full_orders" and mg.low_cost_floor > 0 and mg.full_unique_bound > 0:
        return "analytical (price hidden; unique full orders)"
    return "numerical diagnostic (price hidden)"


def validate_control(sched: Schedule, controls: Controls) -> Validation:
    """Fixed-profile control: investor deviations are retained as diagnostics, not acceptance failures."""
    val = validate(sched, controls)
    val.breaches = [b for b in val.breaches if not b.startswith("epsilon_q")]
    return val


def deviation_rows(prefix: dict, val: Validation) -> list[dict]:
    rows = []
    for state in "HL":
        sc = val.scans.get(state + "_refined", val.scans[state])
        for q, u, uc, gain, qe, tb in sc["rows"]:
            rows.append({**prefix, "state": state, "q": q, "U(q)": u, "U(candidate)": uc, "deviation_gain": gain,
                         "quadrature_error": qe, "tail_bound": tb})
    return rows
