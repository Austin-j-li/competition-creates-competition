"""Solver for items 2 and 3: the full-order region and the live branch near its lower edge.

Writes CSV only:
  full_order_region.csv  global optimality of (1, -1) against the minimal-pool schedule, both types,
                         by a 2001-point order grid on [-1, 1] with golden-section refinement.
  live_branch.csv        the q_H = 1 live branch on [r_e, 2.1] (and coarser to r_C), from the closed
                         form Psi(z, r) = 0, re-verified by the general quadrature layer.
  below_edge.csv         max over z of Psi(z, r) below the edge, on a fine grid (including the 1e-5 gap
                         that the interval cover leaves next to r_e).
  pure_scan.csv          every pure profile (q_H, q_L) on a grid with a live schedule: where is the high
                         type's global best response? (interior values would allow q_H < 1 equilibria)
Status of every row: numerical diagnostic. Certificates are in certify.py.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np

from core import (BENCH, Primitives, acquisition, best_response, C_low, edge_G, J_closed, low_best_magnitude,
                  minimal_entry, n_edge, order_payoff, pool_posterior, psi, pure, r_ceiling, state_entry)

HERE = Path(__file__).resolve().parent
R_E = 1.6585908245511433   # midpoint of the certified enclosure (certificates.csv)
R_J = 2.0155164410601039


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for row in rows:
            w.writerow({k: (f"{v:.10g}" if isinstance(v, float) else v) for k, v in row.items()})


def global_gap(par: Primitives, r: float, prof, entry, theta: str, q_eq: float, n_grid: int = 2001) -> tuple[float, float, float]:
    """(U(q_eq) - sup_s U(s) over s in [-1, 1], argmax, sup over wrong-signed s)."""
    acq = acquisition(par, r)
    u_eq = order_payoff(par, acq, prof, entry, theta, q_eq)
    s_best, v_best, grid, vals = best_response(par, acq, prof, entry, theta, n_grid=n_grid)
    wrong = np.linspace(-1.0, 0.0, 201) * (1.0 if theta == "H" else -1.0)
    v_wrong = max(order_payoff(par, acq, prof, entry, theta, float(s)) for s in wrong[:-1])
    return u_eq - max(v_best, 0.0), s_best, v_wrong


def region_rows(par: Primitives) -> list[dict]:
    rC = r_ceiling(par)
    rs = sorted(set(np.round(np.arange(1.70, 3.59, 0.02), 4).tolist()
                    + [R_J - 1e-3, R_J - 1e-4, R_J + 1e-4, R_J + 1e-3, 2.05, 3.0, 3.5, rC - 1e-6]))
    rows = []
    for r in rs:
        acq = acquisition(par, r)
        prof = pure(1.0, -1.0)
        A = minimal_entry(par, acq, prof)
        gH, sH, wH = global_gap(par, r, prof, A, "H", 1.0)
        gL, sL, wL = global_gap(par, r, prof, A, "L", -1.0)
        J = J_closed(par, r)
        h = 1e-6
        slope_L = (order_payoff(par, acq, prof, A, "L", -1.0) - order_payoff(par, acq, prof, A, "L", -1.0 + h)) / h
        rows.append({"r": r, "tau": acq.tau, "x_star": A[0][0], "J_closed": J,
                     "test_(1-1/b)J-k": (1 - 1 / par.b) * J - par.k,
                     "gap_H_U(1)-maxU": gH, "argmax_H": sH, "max_wrong_H": wH,
                     "gap_L_U(-1)-maxU": gL, "argmax_L": sL, "max_wrong_L": wL,
                     "slope_U_L_at_1_backward_difference": slope_L,
                     "equilibrium": (gH >= -1e-12 and gL >= -1e-12 and slope_L >= -1e-8),
                     "status": "numerical diagnostic"})
    return rows


def branch_z(par: Primitives, r: float) -> float:
    """Minimal-pool low-type magnitude z_U(r): root of Psi(., r) on [n(r), 1], or 1 at the corner."""
    n = n_edge(par, r)
    if psi(par, r, 1.0) >= 0.0:
        return 1.0
    if psi(par, r, n) < 0.0:
        return math.nan
    a, z = n, 1.0
    for _ in range(200):
        mid = 0.5 * (a + z)
        if psi(par, r, mid) >= 0.0:
            a = mid
        else:
            z = mid
    return 0.5 * (a + z)


def branch_rows(par: Primitives) -> list[dict]:
    rs = sorted(set([R_E, R_E + 1e-6, R_E + 1e-5, R_E + 1e-4, R_E + 1e-3]
                    + np.round(np.arange(1.66, 2.101, 0.005), 4).tolist()
                    + [R_J, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.5, 3.59]))
    rows = []
    for r in rs:
        acq = acquisition(par, r)
        z = branch_z(par, r)
        if math.isnan(z):
            continue
        prof = pure(1.0, -z)
        A = minimal_entry(par, acq, prof)
        # independent check of the low type's best response with the quadrature layer
        bL, vL, _, _ = best_response(par, acq, prof, A, "L", n_grid=401)
        gH, sH, _ = global_gap(par, r, prof, A, "H", 1.0, n_grid=1001)
        eH, eL = state_entry(par, prof, A, "H"), state_entry(par, prof, A, "L")
        mubar, _ = pool_posterior(par, prof, A)
        uH = order_payoff(par, acq, prof, A, "H", 1.0)
        uL = order_payoff(par, acq, prof, A, "L", -z)
        h = 1e-6
        psi_z = (psi(par, r, min(z + h, 1.0)) - psi(par, r, max(z - h, n_edge(par, r)))) / (min(z + h, 1.0) - max(z - h, n_edge(par, r)))
        rows.append({"r": r, "tau": acq.tau, "n_r": n_edge(par, r), "qH": 1.0, "qL": -z,
                     "x_star": A[0][0], "E": 0.5 * (eH + eL), "eH": eH, "eL": eL, "O_H": 0.5 * eH,
                     "U_H": uH, "U_L": uL, "U_H_formula_kz/(b-z)": par.k * z / (par.b - z) if z < 1 else uH,
                     "U_L_formula_kz2/(b-z)": par.k * z * z / (par.b - z) if z < 1 else uL,
                     "L_best_quadrature": bL, "H_gap_U(1)-maxU": gH, "H_argmax": sH,
                     "pool_posterior": mubar, "dPsi_dz": psi_z, "G_edge": edge_G(par, r),
                     "status": "numerical diagnostic"})
    return rows


def below_rows(par: Primitives) -> list[dict]:
    rs = sorted(set(np.round(np.arange(1.30, 1.66, 0.01), 4).tolist()
                    + [R_E - 1e-3, R_E - 1e-4, R_E - 1e-5, R_E - 3e-6, R_E - 1e-6, R_E - 1e-7]))
    rows = []
    for r in rs:
        if r >= R_E:
            continue
        n = n_edge(par, r)
        zs = np.linspace(n, 1.0, 4001)
        vals = np.array([psi(par, r, float(z)) for z in zs])
        brs = np.array([low_best_magnitude(par, C_low(par, r, float(z))) - z for z in zs[::40]])
        i = int(vals.argmax())
        rows.append({"r": r, "n_r": n, "max_Psi": float(vals[i]), "argmax_z": float(zs[i]),
                     "max_BR_minus_z": float(brs.max()), "G_edge": edge_G(par, r),
                     "live_with_qH_1": bool(vals.max() >= 0.0), "status": "numerical diagnostic"})
    return rows


def pure_scan_rows(par: Primitives) -> list[dict]:
    rows = []
    for r in [1.4, 1.55, 1.62, 1.65, 1.66, 1.7, 1.8, 2.0, 2.5, 3.0, 3.5]:
        acq = acquisition(par, r)
        n_live, n_interior, n_zero, n_one = 0, 0, 0, 0
        max_interior_gain = -math.inf
        for qH in np.linspace(0.05, 1.0, 20):
            for qL in np.linspace(-1.0, -0.0, 21)[:-1]:
                prof = pure(float(qH), float(qL))
                A0 = minimal_entry(par, acq, prof)
                if not A0:
                    continue
                for shift in (0.0, 0.4, 1.0):
                    A = ((A0[0][0] + shift, math.inf),)
                    n_live += 1
                    s_best, v_best, grid, vals = best_response(par, acq, prof, A, "H", n_grid=101)
                    if v_best <= 0.0:
                        n_zero += 1
                    elif abs(s_best - 1.0) < 1e-9:
                        n_one += 1
                    else:
                        n_interior += 1
                        max_interior_gain = max(max_interior_gain, v_best - max(float(vals[-1]), 0.0))
        rows.append({"r": r, "schedules_with_entry": n_live, "H_best_0": n_zero, "H_best_1": n_one,
                     "H_best_interior": n_interior,
                     "max_gain_interior_over_corners": max_interior_gain if n_interior else math.nan,
                     "status": "numerical diagnostic"})
    return rows


def main() -> None:
    par = BENCH
    write_csv(HERE / "full_order_region.csv", region_rows(par))
    print("region done", flush=True)
    write_csv(HERE / "live_branch.csv", branch_rows(par))
    print("branch done", flush=True)
    write_csv(HERE / "below_edge.csv", below_rows(par))
    print("below done", flush=True)
    write_csv(HERE / "pure_scan.csv", pure_scan_rows(par))
    print("scan done", flush=True)


if __name__ == "__main__":
    main()
