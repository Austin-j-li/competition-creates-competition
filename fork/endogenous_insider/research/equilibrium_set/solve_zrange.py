"""Solver for the projection of the live equilibrium set on the low type's order, and the tie branch.

Writes CSV only:
  z_range.csv     for each strength r, the interval [n(r), z_U(r)] of low-type magnitudes that some entry
                  set can support with q_H = 1 (Proposition ES.4(a), (c)); for interior points the supporting
                  cutoff x'(z) is solved and both types' global best responses are re-verified.
  least_entry.csv for each (r, z), the entry set of least entry among all sets that support (1, -z):
                  the bounded interval [x*(z), y] (the argument of Proposition ES.6(c)); both types re-verified.
  entry_band.csv  on a dense grid of r in [r_e, r_C]: n(r), z_U(r), entry of the minimal-pool member and of
                  the least-entry member (z = n(r), entry on part of the plateau), for the figure.
  tie_branch.csv  the branch that appears if the challenger may mix when it is exactly indifferent
                  (outside the fork's tie rule; Remark ES.1). Closed form, re-verified by quadrature.
Status of every row: numerical diagnostic.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np

from core import (BENCH, Primitives, acquisition, best_response, edge_G, minimal_entry, n_edge, order_payoff,
                  pure, r_ceiling, residual_integral, state_entry)
from solve_branch import branch_z, R_E, write_csv

HERE = Path(__file__).resolve().parent


def C_needed(par: Primitives, z: float) -> float:
    """Coefficient C with argmax_s s(C e^{-s/b} - k) = z (interior z)."""
    return par.k * math.exp(z / par.b) / (1.0 - z / par.b)


def cutoff_for(par: Primitives, r: float, z: float) -> float:
    """x' >= x*(z) with Delta_T int_{x'}^inf f(x) mu_X dx = C_needed(z) under orders (1, -z)."""
    acq = acquisition(par, r)
    prof = pure(1.0, -z)
    xs = minimal_entry(par, acq, prof)[0][0]
    target = C_needed(par, z)
    C = lambda x: acq.DeltaT * residual_integral(par, prof, ((x, math.inf),), "L", 0.0)
    a, b = xs, xs + 40.0
    for _ in range(100):
        mid = 0.5 * (a + b)
        if C(mid) > target:
            a = mid
        else:
            b = mid
    return 0.5 * (a + b)


def zrange_rows(par: Primitives) -> list[dict]:
    rows = []
    for r in [R_E, 1.7, 1.8, 2.0, 2.5, 3.0, 3.5]:
        acq = acquisition(par, r)
        n, zU = n_edge(par, r), branch_z(par, r)
        zs = [n] if abs(zU - n) < 1e-9 else list(np.linspace(n, zU, 6))
        for z in zs:
            z = float(z)
            prof = pure(1.0, -z)
            if z < 1.0 - 1e-12:
                xp = cutoff_for(par, r, z)
            else:
                xp = minimal_entry(par, acq, prof)[0][0]
            A = ((xp, math.inf),)
            sH, vH, _, _ = best_response(par, acq, prof, A, "H", n_grid=1001)
            sL, vL, _, _ = best_response(par, acq, prof, A, "L", n_grid=1001)
            uH = order_payoff(par, acq, prof, A, "H", 1.0)
            uL = order_payoff(par, acq, prof, A, "L", -z)
            eH, eL = state_entry(par, prof, A, "H"), state_entry(par, prof, A, "L")
            rows.append({"r": r, "n_r": n, "z_U": zU, "z": z, "cutoff_x'": xp, "E": 0.5 * (eH + eL),
                         "U_H": uH, "U_L": uL, "H_best": sH, "H_gap": uH - max(vH, 0.0), "L_best": sL,
                         "L_dev": sL + z, "equilibrium": bool(uH - max(vH, 0.0) >= -1e-10 and abs(sL + z) < 1e-5),
                         "status": "numerical diagnostic"})
    return rows


def tie_rows(par: Primitives) -> list[dict]:
    rows = []
    rC = r_ceiling(par)
    for r in [R_E, 1.7, 2.0, 2.5, 3.0, 3.5, rC - 1e-6]:
        acq = acquisition(par, r)
        n = n_edge(par, r)
        if not 0.0 < n <= 1.0:
            continue
        G = edge_G(par, r)
        pi = par.k / (G + par.k)          # preparation probability on the plateau atom
        # verification: residuals scale by pi; emulate by scaling Delta_T in the payoff
        prof = pure(1.0, -n)
        A = ((1.0, math.inf),)
        scaled = acq.__class__(acq.r, acq.t0, acq.tH, acq.tL, acq.gH, acq.gL, pi * acq.DeltaT, acq.tau)
        sH, vH, _, _ = best_response(par, scaled, prof, A, "H", n_grid=1001)
        sL, vL, _, _ = best_response(par, scaled, prof, A, "L", n_grid=1001)
        eH, eL = state_entry(par, prof, A, "H"), state_entry(par, prof, A, "L")
        rows.append({"r": r, "n_r": n, "pi_plateau": pi, "E": pi * 0.5 * (eH + eL), "E_formula_pi/(4tau)": pi / (4 * acq.tau),
                     "O_H": pi * 0.5 * eH, "U_H": order_payoff(par, scaled, prof, A, "H", 1.0),
                     "U_H_formula_kn/(b-n)": par.k * n / (par.b - n), "H_best": sH, "L_best": sL,
                     "status": "numerical diagnostic (outside the fork's tie rule)"})
    return rows


def least_entry_rows(par: Primitives) -> list[dict]:
    rows = []
    for r in [1.7, 2.0, 2.5, 3.0, 3.5]:
        acq = acquisition(par, r)
        n, zU = n_edge(par, r), branch_z(par, r)
        for z in np.linspace(n, zU, 6):
            z = float(z)
            prof = pure(1.0, -z)
            xs = min(minimal_entry(par, acq, prof)[0][0], 1.0)
            if z < 1.0 - 1e-12:
                target = C_needed(par, z)
                C = lambda y: acq.DeltaT * residual_integral(par, prof, ((xs, y),), "L", 0.0)
            else:
                target = par.k / (1.0 - 1.0 / par.b)
                C = lambda y: acq.DeltaT * residual_integral(par, prof, ((xs, y),), "H", 1.0)
            a, b = xs, xs + 60.0
            if C(b) < target:
                continue
            for _ in range(100):
                mid = 0.5 * (a + b)
                if C(mid) < target:
                    a = mid
                else:
                    b = mid
            y = 0.5 * (a + b) + 1e-9
            A = ((xs, y),)
            sH, vH, _, _ = best_response(par, acq, prof, A, "H", n_grid=1001)
            sL, vL, _, _ = best_response(par, acq, prof, A, "L", n_grid=1001)
            uH = order_payoff(par, acq, prof, A, "H", 1.0)
            eH, eL = state_entry(par, prof, A, "H"), state_entry(par, prof, A, "L")
            rows.append({"r": r, "z": z, "x_star": xs, "y": y, "E_least": 0.5 * (eH + eL), "U_H": uH,
                         "H_best": sH, "H_gap": uH - max(vH, 0.0), "L_best": sL, "L_dev": sL + z,
                         "equilibrium": bool(uH - max(vH, 0.0) >= -1e-10 and abs(sL + z) < 1e-4),
                         "status": "numerical diagnostic"})
    return rows


def band_rows(par: Primitives) -> list[dict]:
    from core import F_Z, frak_r
    rows = []
    rC = r_ceiling(par)
    for r in sorted(set([R_E] + np.round(np.arange(1.66, rC, 0.01), 4).tolist() + [rC - 1e-9])):
        acq = acquisition(par, r)
        n, zU = n_edge(par, r), branch_z(par, r)
        xs = (1.0 - zU) / 2.0 + par.b / 2.0 * math.log(acq.tau / (1.0 - acq.tau))
        e_max = 0.5 * ((1.0 - F_Z(par, xs - 1.0)) + (1.0 - F_Z(par, xs + zU)))
        G = edge_G(par, r)
        e_min = par.k / (G + par.k) / (4.0 * acq.tau)
        rows.append({"r": r, "n_r": n, "z_U": zU, "x_star_minimal": xs, "E_minimal_pool": e_max,
                     "E_least_z_eq_n": e_min, "G_edge": G, "r_e": R_E, "r_C": rC, "frak_r_k": frak_r(par, par.k),
                     "status": "numerical diagnostic"})
    return rows


def main() -> None:
    par = BENCH
    write_csv(HERE / "z_range.csv", zrange_rows(par))
    print("z range done", flush=True)
    write_csv(HERE / "least_entry.csv", least_entry_rows(par))
    print("least entry done", flush=True)
    write_csv(HERE / "entry_band.csv", band_rows(par))
    print("band done", flush=True)
    write_csv(HERE / "tie_branch.csv", tie_rows(par))
    print("tie done", flush=True)


if __name__ == "__main__":
    main()
