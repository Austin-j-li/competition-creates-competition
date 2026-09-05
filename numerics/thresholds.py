"""Exact analytical boundaries (Proposition 3, OA.19 to OA.21) with defining-residual checks."""
from __future__ import annotations

from decimal import Decimal, getcontext

import numpy as np

from .auction import payoffs_closed_form
from .noise import posterior_bounds
from .params import Primitives

getcontext().prec = 60


def frak_r(ell: float, d: float) -> float:
    """r(d) = ell + d + sqrt(d^2 + 2 ell d): the root of Delta_T(r) = d above ell."""
    return ell + d + np.sqrt(d * d + 2 * ell * d)


def compute_thresholds(prim: Primitives) -> list[dict]:
    """Rows for numerics/thresholds.csv (C.2)."""
    h, ell, p, rho, b, k, cL, cH = prim.fh, prim.fell, prim.fp, prim.frho, prim.fb, prim.fk, prim.fc_L, prim.fc_H
    m, M = posterior_bounds(b)
    rows = []

    def domain_flags(r: float) -> tuple[bool, bool]:
        pay = payoffs_closed_form(prim, r)
        in_support = ell < r < h
        floor_ok = cL < pay.B(m)
        prior_ok = pay.B(0.5) < cH
        return in_support and prior_ok, floor_ok

    def add(boundary, value, residual, interp, applies=True):
        if applies:
            ds, fl = domain_flags(value)
            rows.append({"boundary": boundary, "value": value, "lower": np.nextafter(value, -np.inf),
                         "upper": np.nextafter(value, np.inf), "defining_residual": residual,
                         "in_support_domain": ds, "low_cost_floor_valid": fl, "interpretation": interp})
        else:
            rows.append({"boundary": boundary, "value": value, "lower": "n/a", "upper": "n/a", "defining_residual": residual,
                         "in_support_domain": "n/a", "low_cost_floor_valid": "n/a", "interpretation": interp})

    Delta = lambda r: (r - ell) ** 2 / (2 * r)
    r_pu = frak_r(ell, k)
    add("pooling_unique_sufficient", r_pu, Delta(r_pu) - k,
        "r(k): below this strength Delta_T < k and no trade is the unique outcome (sufficient bound)")
    r_N = frak_r(ell, 2 * k / rho)
    add("pooling_existence", r_N, rho * Delta(r_N) / 2 - k,
        "r_N = r(2k/rho): exact boundary of pooling existence, rho Delta_T/2 = k")
    r_U = frak_r(ell, k / ((1 - 1 / b) * rho * m))
    add("full_orders_unique_sufficient", r_U, (1 - 1 / b) * rho * m * Delta(r_U) - k,
        "r_U: (1-1/b) rho m Delta_T = k; above it full orders are the unique outcome (sufficient bound)")
    # r_C from OA.20 / eq. (16)
    disc = (M * h - cH) ** 2 + M * ((1 - M) * ell * ell - p * p)
    if disc >= 0:
        r_C = ((M * h - cH) + np.sqrt(disc)) / M
        payC = payoffs_closed_form(prim, r_C)
        add("high_cost_ceiling", r_C, payC.B(M) - cH,
            "r_C: B_r(M) = c_H; above it expensive entry is infeasible in every equilibrium (tie rule retained at equality)")
    else:
        add("high_cost_ceiling", float("nan"), disc, "no real root: B_r(M) = c_H has no crossing", applies=False)
    add("m", m, m - 1 / (1 + np.exp(2 / b)), "lower posterior bound m = (1 + e^{2/b})^{-1}", applies=False)
    add("M", M, M - (1 - m), "upper posterior bound M = 1 - m", applies=False)
    left = rho + (1 - rho) * (1 + np.exp(-2 / b)) / 4
    add("laplace_entry_left_limit", left, 0.0,
        "lim E(r) as r -> r_C from below under full Laplace orders (OA.21); one-sided limit, not the boundary equilibrium", applies=False)
    return rows
