"""Curve data for the interactive figures of the slot talk.

Each curve is a closed form of the order-slot manuscript at the benchmark, evaluated on a grid of
incumbent strengths r. The primitives and every boundary come from the registry
(audit/slot_manuscript_2026_10_23/registry/registry.csv); a boundary is never recomputed here. The
closed forms are the ones that audit/slot_manuscript_2026_10_23/scripts/F_figures/make_figures.py
draws into the manuscript figures: tau, Delta, gH, gL (Proposition 2 and Lemma A.3), the entry of
branch R and of the plateau F (Proposition 3), and the research branch (Proposition 4).
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
    bd = {key: g(key) for key in ("rA", "rF_B", "rN", "rJ", "rS_B", "rC_B", "res_rR", "res_rcap", "res_rUR")}

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

    def entry_R(r): return rho + (1 - rho) * b * delta(r) / (2 * k)
    plateau = rho + (1 - rho) * (b + lam / 2)
    def entry_research(l): return rho + (1 - rho) * (beta + (0.5 - beta) * l)

    r4 = lambda x: round(x, 6)  # noqa: E731

    def flat(lo, hi, y, n=24):
        """A constant segment on a grid, so a hover finds a point anywhere along it."""
        xs = grid(lo, hi, (hi - lo) / n)
        return {"r": xs, "y": [r4(y)] * len(xs)}

    # F7: the gross return of a correctly signed order lies between rho*kappa*Delta and Delta.
    rs = grid(1.01, 3.2, 0.01)
    r_k = ell + k + math.sqrt(k * k + 2 * ell * k)   # Delta(r) = k: below it no order covers the cost
    gain = {"r": rs, "upper": [r4(delta(r) / k) for r in rs], "lower": [r4(rho * kappa * delta(r) / k) for r in rs], "r_k": r4(r_k)}

    # F8: the threshold belief and the profit at the posterior bounds, 1.2 to 3.6.
    rb = grid(1.2, 3.6, 0.01)
    belief = {"r": rb, "tau": [r4(tau(r)) for r in rb], "B_M": [r4(B(r, M)) for r in rb],
              "B_prior": [r4(B(r, pi)) for r in rb], "B_m": [r4(B(r, m)) for r in rb]}

    # F12: entry on each branch at the prior (Proposition 3).
    rR_ = grid(bd["rA"], bd["rF_B"], (bd["rF_B"] - bd["rA"]) / 60)
    entry = {"N": flat(r0, bd["rN"], rho), "Q": flat(bd["rN"], bd["rJ"], rho, 8),
             "R": {"r": rR_, "y": [r4(entry_R(r)) for r in rR_]},
             "F": flat(bd["rF_B"], bd["rC_B"], plateau, 60), "F_floor": flat(bd["rC_B"], r2, rho, 4)}

    # F13: the research branch on [1.2, 2.0] (Proposition 4).
    rb2 = grid(bd["res_rR"], bd["res_rcap"], (bd["res_rcap"] - bd["res_rR"]) / 40)
    lamb = [lam_R(r) for r in rb2]
    research = {"branch": {"r": rb2, "lambda": [r4(x) for x in lamb], "entry": [r4(entry_research(x)) for x in lamb]},
                "zero": flat(r0, bd["rN"], 0.0), "cap": flat(bd["res_rcap"], bd["rN"], lam, 8),
                "cap_value": r4(lam), "plateau": r4(plateau)}

    return {"inputs": {"r0": r0, "r1": r1, "r2": r2, "rho": rho, "k": k, "cH": cH, "pi": pi, "m": m, "M": M, "kappa": kappa},
            "bounds": bd, "gain": gain, "belief": belief, "entry": entry, "research": research}
