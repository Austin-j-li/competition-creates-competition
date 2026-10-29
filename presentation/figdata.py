"""Curve data for the interactive figures of the slot talk.

Each curve is a closed form of the order-slot manuscript in the example, evaluated on a grid of
incumbent strengths r. The primitives and every boundary come from the registry
(audit/slot_manuscript_2026_10_23/registry/registry.csv); a boundary is never recomputed here. The
closed forms are the ones that audit/slot_manuscript_2026_10_23/scripts/F_figures/make_figures.py
draws into the manuscript figures: tau, Delta, gH, gL (Proposition 2 and Lemma A.3), the coexistence
region and the entry of R, F and T (Proposition 3, Corollary 2), and recruiting and floor-entry research
(Proposition 4, Corollary 3).
Standard library only. The browser reads the result and draws it; it computes nothing.
"""
from __future__ import annotations

import math
from fractions import Fraction


def num(registry: dict, key: str) -> float:
    """The registry value of a key as a float; fractions such as 6/5 are exact."""
    raw = registry[key]["value"].strip()
    return float(Fraction(raw)) if "/" in raw else float(raw)


def grid(lo: float, hi: float, step: float) -> list[float]:
    n = round((hi - lo) / step)
    return [round(lo + i * step, 10) for i in range(n + 1)]


def build(registry: dict) -> dict:
    g = lambda k: num(registry, k)  # noqa: E731
    h, ell, p, pi = g("prim_h"), g("prim_ell"), g("prim_p"), g("prim_pi")
    rho, cH, k = g("prim_rho"), g("prim_cH"), g("prim_k")
    beta, a = g("beta_B"), g("res_a")
    u = g("u_B")
    lam = u * beta / (1 + u * beta)
    b = beta / (1 + u * beta)
    M, m = g("M_half_B"), g("m_half_B")
    kappa = min(m, 1 - M)
    r0, r1, r2 = g("prim_r0"), g("prim_r1"), g("prim_r2")
    bd = {key: g(key) for key in ("rA", "rF_B", "rN", "rJ", "rS_B", "rC_B", "res_rR", "res_rcap", "res_rN", "res_rQ",
                                  "res_rC")}

    def g_H(r): return h - r / 2 - p * p / (2 * r)
    def g_L(r): return (ell * ell - p * p) / (2 * r)
    def delta(r): return (r - ell) ** 2 / (2 * r)
    def B(r, mu): return g_L(r) + mu * (g_H(r) - g_L(r))
    def tau(r): return (cH - g_L(r)) / (g_H(r) - g_L(r))

    def lam_E(r):
        t = tau(r)
        return beta * (2 * t - 1) / (beta + (1 - 2 * beta) * (1 - t))

    def lam_R(r):
        """Positive root of the research polynomial (Proposition 4, equation (F))."""
        D = delta(r)
        A = 2 * a * (1 - 2 * beta)
        Bc = 4 * a * beta + k * (1 - 2 * beta) + beta * D
        C = beta * (2 * k - D)
        return (-Bc + math.sqrt(Bc * Bc - 4 * A * C)) / (2 * A)

    def lam_Q(r):
        """Floor-entry research: the root in [0, 1) of a lambda = rho Delta m_lambda - k (Corollary 3)."""
        D = delta(r)
        A = a * (1 - 2 * beta)
        Bc = rho * D * beta + k * (1 - 2 * beta) + 2 * a * beta
        C = beta * (2 * k - rho * D)
        return -2 * C / (Bc + math.sqrt(Bc * Bc - 4 * A * C))

    def entry_R(r): return rho + (1 - rho) * b * delta(r) / (2 * k)
    def entry_T(r):
        """Entry on the threshold pair T, when an indifferent high-cost challenger may prepare with any probability."""
        D, t = delta(r), tau(r)
        return rho + (b / 2) * (k - rho * D * (1 - t)) / (D * (1 - t) ** 2)
    plateau = rho + (1 - rho) * (b + lam / 2)
    def entry_research(l): return rho + (1 - rho) * (beta + (0.5 - beta) * l)

    r4 = lambda x: round(x, 6)  # noqa: E731

    def flat(lo, hi, y, n=24):
        """A constant segment on a grid, so a hover finds a point anywhere along it."""
        xs = grid(lo, hi, (hi - lo) / n)
        return {"r": xs, "y": [r4(y)] * len(xs)}

    # Frame 14: the threshold belief and the profit at the belief bounds, 1.2 to 3.6 (the figure shows r_1 to r_2).
    rb = grid(1.2, 3.6, 0.01)
    belief = {"r": rb, "tau": [r4(tau(r)) for r in rb], "B_M": [r4(B(r, M)) for r in rb],
              "B_prior": [r4(B(r, pi)) for r in rb], "B_m": [r4(B(r, m)) for r in rb]}

    # B3: the coexistence region at the prior 1/2 (Proposition 3): pi < tau <= M and k/(1 - tau) <= Delta <= 2k/rho,
    # with the example's path (Delta(r), tau(r)) from r_0 until the spread leaves the window at 0.2.
    taus = grid(0.5, M, (M - 0.5) / 60)
    r_out = ell + 0.2 + math.sqrt(0.2 * 0.2 + 2 * ell * 0.2)
    rp = grid(r0, r_out, (r_out - r0) / 120)
    region = {"left": {"Delta": [r4(k / (1 - x)) for x in taus], "tau": [r4(x) for x in taus]},
              "D_N": r4(2 * k / rho), "D_F": r4(k / (1 - M)),
              "path": {"r": rp, "Delta": [r4(delta(r)) for r in rp], "tau": [r4(tau(r)) for r in rp]},
              "marks": {key: [r4(delta(bd[key])), r4(tau(bd[key]))] for key in ("rA", "rF_B", "rN")}
              | {"prim_r0": [r4(delta(r0)), r4(tau(r0))]}}

    # B3, page 2: entry in each equilibrium at the prior (Corollary 2).
    rR_ = grid(bd["rA"], bd["rF_B"], (bd["rF_B"] - bd["rA"]) / 60)
    rT_ = grid(bd["rA"], bd["rJ"], (bd["rJ"] - bd["rA"]) / 80)
    entry = {"N": flat(r0, bd["rN"], rho), "Q": flat(bd["rN"], bd["rJ"], rho, 8),
             "R": {"r": rR_, "y": [r4(entry_R(r)) for r in rR_]},
             "T": {"r": rT_, "y": [r4(entry_T(r)) for r in rT_]},
             "F": flat(bd["rF_B"], bd["rC_B"], plateau, 60), "F_floor": flat(bd["rC_B"], r2, rho, 4)}

    # B12, page 2: research along the path (Corollary 3): zero research on [r_0, r_N]; recruiting research below the cap on
    # [r_R, r_lambda-bar) and at the cap on [r_lambda-bar, r_C]; floor-entry research on (r_N, r_Q) and at the cap on (r_C, r_2].
    rb2 = grid(bd["res_rR"], bd["res_rcap"], (bd["res_rcap"] - bd["res_rR"]) / 40)
    lamb = [lam_R(r) for r in rb2]
    rq = grid(bd["res_rN"], bd["res_rQ"], (bd["res_rQ"] - bd["res_rN"]) / 60)
    lamq = [max(lam_Q(r), 0.0) for r in rq]
    research = {"recruit": {"r": rb2, "lambda": [r4(x) for x in lamb], "entry": [r4(entry_research(x)) for x in lamb]},
                "zero": flat(r0, bd["res_rN"], 0.0), "cap": flat(bd["res_rcap"], bd["res_rC"], lam, 40),
                "floor": {"r": rq, "lambda": [r4(x) for x in lamq], "entry": [r4(rho)] * len(rq)},
                "floor_cap": flat(bd["res_rC"], r2, lam, 8),
                "cap_value": r4(lam), "plateau": r4(plateau)}

    return {"inputs": {"r0": r0, "r1": r1, "r2": r2, "rho": rho, "k": k, "cH": cH, "pi": pi, "m": m, "M": M, "kappa": kappa},
            "bounds": bd, "belief": belief, "region": region, "entry": entry, "research": research}
