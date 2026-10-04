"""Write every referee CSV. Run: python3 run_checks.py (about two minutes).

Each CSV row is a numerical diagnostic in double precision (adaptive quadrature or fine cells). Rows that
confirm an equilibrium list both best responses and both regrets from an independent order grid with refinement.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from scipy import optimize

from referee import (Prm, partial_member, starved_closed, starved_closed_threshold, CL_quad, S, Bmu, F, K_forcing, U, bathtub, best_response, halfline_thresholds, lev, logit,
                     mu_full, mu_pure, mubar_full, pool_belief, random_forcing_test, replace, starved_check,
                     starved_xp, vH, xbar)

HERE = Path(__file__).resolve().parent


def write(name: str, rows: list[dict]) -> None:
    with (HERE / name).open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.10g}" if isinstance(v, float) else v) for k, v in r.items()})


def table1(P: Prm) -> list[dict]:
    rows = []
    for cL in (2.37, 2.5, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2):
        Q = replace(P, cL=cL)
        bE, bH = bathtub(Q, "E"), bathtub(Q, "H")
        xb = xbar(Q)
        rows.append({"cL": cL, "tauL": lev(Q).tauL, "xbar": xb, "pibar": 0.5 * (F(Q, xb - 1) + F(Q, xb + 1)),
                     "K": K_forcing(Q), "E0": bE["base"], "infE": bE["inf"], "eH0": bH["base"], "infeH": bH["inf"]})
    return rows


def a4pp(P: Prm, c: float, rho: float) -> float:
    Q = replace(P, cL=c, rho=rho)
    L = lev(Q)
    z0, xs = logit(L.tauL), logit(L.tauH)
    xb = xbar(Q)
    pib = 0.5 * (F(Q, xb - 1) + F(Q, xb + 1))
    pZ0 = 0.5 * (F(Q, z0 - 1) + F(Q, z0 + 1))
    a = 0.5 * (S(Q, xs - 1) + S(Q, xs + 1))
    E0 = rho * (1 - pZ0) + (1 - rho) * a
    B0 = 0.5 * (L.tauL * F(Q, z0 + 1) - (1 - L.tauL) * F(Q, z0 - 1))
    return E0 - rho * (pib - pZ0) - (1 - rho) * min(a, B0 / (L.tauH - L.tauL)) - rho


def thresholds(P: Prm) -> list[dict]:
    rows = []
    L = lev(P)
    lo, hi = Bmu(P, L.m) + 1e-4, Bmu(P, 0.5) - 1e-3
    for rho in (0.1, 0.2, 0.25, 0.3, 0.35, 0.5):
        gE = lambda c: bathtub(replace(P, cL=c, rho=rho), "E", n=200000)["inf"] - rho  # noqa: E731
        gH = lambda c: bathtub(replace(P, cL=c, rho=rho), "H", n=200000)["inf"] - rho  # noqa: E731
        a3 = (1 - 1 / P.b) * rho * L.m * L.DT
        h = halfline_thresholds(replace(P, rho=rho, k=0.999 * a3))
        xs = logit(L.tauH)
        xE = max(h["xE"], xs)   # R.9 needs x' >= x*
        rows.append({"rho": rho, "knap_E": optimize.brentq(gE, lo, hi, xtol=1e-6),
                     "knap_O": optimize.brentq(gH, lo, hi, xtol=1e-6),
                     "A4pp_E": optimize.brentq(lambda c: a4pp(P, c, rho), lo, hi, xtol=1e-9),
                     "a3_right": a3, "halfline_xE": xE, "halfline_xO": h["xO"], "xk_at_a3": h["xk"],
                     "halfline_E_in_A3": Bmu(P, mubar_full(P, xE)), "halfline_O_in_A3": h["cO"],
                     "xk_at_k002": halfline_thresholds(replace(P, rho=rho, k=0.02))["xk"]})
    return rows


def starved_rows(P: Prm) -> list[dict]:
    rows = []
    for cL, k, vs in ((2.9, 0.0224, (0.72, 0.73, 0.74)), (2.9, 0.022, (0.735, 0.74)), (2.8, 0.025, (0.69,))):
        for v in vs:
            r = starved_check(replace(P, cL=cL, k=k), v)
            rows.append({"cL": cL, "k": k, "a3_right": (1 - 1 / P.b) * P.rho * lev(P).m * lev(P).DT, **r})
    for k in (0.0224, 0.022412, 0.022, 0.021, 0.02, 0.019, 0.015, 0.01, 0.0075, 0.005):
        Q = replace(P, k=k)
        v = vH(Q) - 1e-9
        xp = starved_xp(Q, v)
        rows.append({"cL": math.nan, "k": k, "a3_right": math.nan, "v": v, "xp": xp,
                     "pool_belief": pool_belief(Q, xp, 1, -v), "edge_belief": mu_pure(Q, xp, 1, -v),
                     "tauL": math.nan, "vH": vH(Q), "brH": math.nan, "regretH": math.nan, "brL": math.nan,
                     "regretL": math.nan, "UH1": math.nan, "UH1_identity": math.nan,
                     "E": Q.rho * 0.5 * (S(Q, xp - 1) + S(Q, xp + v)), "OH": Q.rho * S(Q, xp - 1) / 2,
                     "ok": f"threshold c_L={Bmu(Q, pool_belief(Q, xp, 1, -v)):.6f}"})
    return rows


def full_check(Q: Prm, xp: float) -> dict:
    L = lev(Q)
    sH, uH = best_response(Q, "H", 1.0, -1.0, xp, n=401)
    sL, uL = best_response(Q, "L", 1.0, -1.0, xp, n=401)
    xs = logit(L.tauH)
    E = Q.rho * 0.5 * (S(Q, xp - 1) + S(Q, xp + 1)) + (1 - Q.rho) * 0.5 * (S(Q, xs - 1) + S(Q, xs + 1))
    eH = Q.rho * S(Q, xp - 1) + (1 - Q.rho) * S(Q, xs - 1)
    return {"rho": Q.rho, "cL": Q.cL, "k": Q.k, "xp": xp, "pool_belief": mubar_full(Q, xp), "tauL": L.tauL,
            "edge_belief": mu_full(Q, xp), "brH": sH, "regretH": uH - U(Q, "H", 1, 1, -1, xp), "brL": sL,
            "regretL": uL - U(Q, "L", 1, 1, -1, xp), "E": E, "OH": eH / 2, "K": K_forcing(Q),
            "no_trade_bound": Q.rho * L.DT / 2, "a3_right": (1 - 1 / Q.b) * Q.rho * L.m * L.DT,
            "candidate_2Bhalf_minus_cH": 2 * Bmu(Q, 0.5) - Q.cH}


def candidate_rows(P: Prm) -> list[dict]:
    rows = [full_check(replace(P, rho=0.5, cL=2.5), xp) for xp in (-0.6, -0.5, -0.4)]
    Q = replace(P, rho=0.6, cL=2.4)
    rows.append(full_check(Q, logit(lev(Q).tauL)))
    Q = replace(P, rho=0.1, cL=3.0, k=0.04)          # informative eq above the no-trade bound
    rows.append(full_check(Q, logit(lev(Q).tauL)))
    return rows


def jgap_rows(P: Prm) -> list[dict]:
    L = lev(P)
    asq = lambda u: math.asin(math.sqrt(u))  # noqa: E731
    rows = []
    for rho in (0.5, 0.6, 0.7, 0.8, 0.9):
        for tau in (0.3, 0.4, 0.49):
            J = L.DT * (L.m / 2 + math.exp(-1 / P.b) / 2 * (rho * (asq(L.M) - asq(tau)) + (1 - rho) * (asq(L.M) - asq(L.tauH))))
            rows.append({"rho": rho, "tauL": tau, "J_z0": J, "rho_m_DT": rho * L.m * L.DT, "gap": J - rho * L.m * L.DT})
    return rows


def random_rows(P: Prm) -> list[dict]:
    rows = []
    for cL in (2.4, 2.6, 2.8, 3.0, 3.4, 4.0):
        r = random_forcing_test(replace(P, cL=cL), n_draws=600, seed=int(cL * 100))
        rows.append({"cL": cL, **{k: float(v) for k, v in r.items()}})
    return rows


def partial_rows(P: Prm) -> list[dict]:
    """Starved members outside (A3) at rho = 0.25: they test the numerics k-scan, not Proposition 2'."""
    return [partial_member(replace(P, cL=cL, k=k), xp) for cL, k, xp in
            ((2.6, 0.03, -0.75), (2.9, 0.03, -0.3), (2.9, 0.035, -0.5))]


def closed_rows(P: Prm) -> list[dict]:
    """Closed-form starved members with x' >= 1 (analytical family; the root in v is double precision)."""
    rows = []
    for k in (0.0167, 0.018, 0.02, 0.022, 0.0224, 0.015, 0.0125, 0.01, 0.0075, 0.005):
        Q = replace(P, k=k)
        L = lev(Q)
        g = lambda v: L.DT * Q.rho / 2 * (1 - v / Q.b) / (1 + math.exp((1 + v) / Q.b)) - k  # noqa: E731  FOC at x'=1
        if g(0.0) > 0 > g(vH(Q) - 1e-12):
            v1 = optimize.brentq(g, 0.0, vH(Q) - 1e-12, xtol=1e-14)
            r = starved_closed(Q, v1)
            kind = "x'=1 member"
        else:
            r = starved_closed(Q, vH(Q) - 1e-12)
            kind = "v->v_H limit"
        rows.append({"k": k, "kind": kind, **{a: b for a, b in r.items() if a != "valid"}, "valid": r["valid"]})
    # corner v = 0 at k = 0.02 (low type abstains, high type indifferent between 0 and 1)
    xp0 = optimize.brentq(lambda x: CL_quad(P, 0.0, x) - P.k, 0.0, 10.0, xtol=1e-13)
    pb0 = pool_belief(P, xp0, 1.0, 0.0)
    rows.append({"k": P.k, "kind": "corner v=0", "v": 0.0, "xp": xp0, "Mv": 1 / (1 + math.exp(-1 / P.b)),
                 "pool_belief": pb0, "cL_threshold": Bmu(P, pb0), "E": P.rho * 0.5 * (S(P, xp0 - 1) + S(P, xp0)),
                 "OH": P.rho * S(P, xp0 - 1) / 2, "valid": xp0 >= 1})
    # quadrature confirmation of the k = 0.02 x'=1 member at c_L = 3.43
    return rows


def closed_confirm(P: Prm) -> list[dict]:
    Q = replace(P, cL=3.43)
    L = lev(Q)
    g = lambda v: L.DT * Q.rho / 2 * (1 - v / Q.b) / (1 + math.exp((1 + v) / Q.b)) - Q.k  # noqa: E731
    v1 = optimize.brentq(g, 0.0, vH(Q) - 1e-12, xtol=1e-14)
    return [starved_check(Q, v1)]


def main() -> None:
    P = Prm()
    write("table1_check.csv", table1(P))
    write("thresholds_check.csv", thresholds(P))
    write("starved_a3.csv", starved_rows(P))
    write("candidate_counter.csv", candidate_rows(P))
    write("jgap.csv", jgap_rows(P))
    write("random_forcing.csv", random_rows(P))
    write("partial_outside_a3.csv", partial_rows(P))
    write("starved_closed.csv", closed_rows(P))
    write("starved_closed_confirm.csv", closed_confirm(P))
    print("referee CSVs written")


if __name__ == "__main__":
    main()
