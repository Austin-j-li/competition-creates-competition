"""Solver for item 4: equilibria outside the cutoff family.

Writes CSV only:
  holes_r3.csv        full orders at r = 3 with entry sets that have holes; each row re-verified by the
                      quadrature layer (global best responses of both types on a 2001-point grid).
  holes_range.csv     entry range over all full-order equilibria (any measurable entry set) against the
                      cutoff family, across strengths r in [r_J, r_C].
  mixed_scan.csv      the high type's payoff curve against many schedules (pure and mixed profiles,
                      half-line and holed entry sets): count of interior local maxima.
  identity_check.csv  E_{sigma_H}[F_H] = E_{sigma_L}[F_L] (Lemma ES.5) on mixed profiles.
Status of every row: numerical diagnostic. The characterizations are analytical (note.md, Section 4).
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np

from core import (BENCH, F_Z, Primitives, Profile, acquisition, best_response, m_bound, minimal_entry,
                  order_payoff, payoff_curve, pool_posterior, pure, r_ceiling, residual_integral, state_entry,
                  threshold_flow)

HERE = Path(__file__).resolve().parent
R_J = 2.0155164410601039


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for row in rows:
            w.writerow({k: (f"{v:.10g}" if isinstance(v, float) else v) for k, v in row.items()})


def g_mass(par: Primitives, lo: float, hi: float) -> float:
    """int_lo^hi g(x) dx for g = f(x-1)f(x+1)/(f(x-1)+f(x+1)) and 0 <= lo <= hi (closed form, Lemma ES.1)."""
    b = par.b
    def G(x: float) -> float:
        # antiderivative on [0, inf): (e^{-1/b}/2) atan(e^{x/b}) on [0,1]; exponential tail on [1, inf)
        if x == math.inf:
            return G(1.0) + m_bound(par) / 2.0
        if x <= 1.0:
            return math.exp(-1.0 / b) / 2.0 * math.atan(math.exp(x / b))
        tail = 0.5 * (math.exp(-2.0 / b) - math.exp(-(x + 1.0) / b)) / (1.0 + math.exp(-2.0 / b))
        return G(1.0) + tail
    return G(hi) - G(lo)


def flow_mass(par: Primitives, lo: float, hi: float) -> float:
    """int_lo^hi (a_H + a_L) dx under full orders: twice the entry contribution."""
    Fz = lambda z: 1.0 if z == math.inf else F_Z(par, z)
    return (Fz(hi - 1.0) - Fz(lo - 1.0)) + (Fz(hi + 1.0) - Fz(lo + 1.0))


def solve_upper(fun, a: float, z: float) -> float:
    """Bisection for an increasing function crossing zero on [a, z]."""
    for _ in range(200):
        mid = 0.5 * (a + z)
        if fun(mid) < 0.0:
            a = mid
        else:
            z = mid
    return 0.5 * (a + z)


def verify(par: Primitives, r: float, entry: tuple[tuple[float, float], ...], label: str) -> dict:
    acq = acquisition(par, r)
    prof = pure(1.0, -1.0)
    sH, vH, _, _ = best_response(par, acq, prof, entry, "H", n_grid=2001)
    sL, vL, _, _ = best_response(par, acq, prof, entry, "L", n_grid=2001)
    uH = order_payoff(par, acq, prof, entry, "H", 1.0)
    uL = order_payoff(par, acq, prof, entry, "L", -1.0)
    eH, eL = state_entry(par, prof, entry, "H"), state_entry(par, prof, entry, "L")
    mubar, _ = pool_posterior(par, prof, entry)
    J_A = acq.DeltaT * sum(g_mass(par, lo, hi) for lo, hi in entry)
    return {"r": r, "entry_set": label, "E": 0.5 * (eH + eL), "O_H": 0.5 * eH, "J_A": J_A,
            "test_(1-1/b)J_A-k": (1 - 1 / par.b) * J_A - par.k, "U_H(1)": uH, "U_L(-1)": uL,
            "H_best": sH, "H_gap": uH - max(vH, 0.0), "L_best": sL, "L_gap": uL - max(vL, 0.0),
            "pool_posterior": mubar, "tau": acq.tau,
            "equilibrium": bool(uH - max(vH, 0.0) >= -1e-12 and uL - max(vL, 0.0) >= -1e-12 and mubar < acq.tau),
            "status": "numerical diagnostic"}


def holes_rows(par: Primitives) -> list[dict]:
    r = 3.0
    acq = acquisition(par, r)
    xs = minimal_entry(par, acq, pure(1.0, -1.0))[0][0]
    G0 = par.k / ((1 - 1 / par.b) * acq.DeltaT)     # required g-mass of the entry set
    inf = math.inf
    # least-entry set (Proposition ES.6): keep the lowest posteriors first, i.e. [x*, y]
    y_np = solve_upper(lambda y: g_mass(par, xs, y) - G0, xs, 30.0)
    # same g-mass placed at the far end of the plateau: [x*, 1) and [y', inf)
    y_tail = solve_upper(lambda y: -(g_mass(par, xs, 1.0) + g_mass(par, y, inf) - G0), 1.0, 30.0)
    # cutoff family endpoint at full orders: [x', inf)
    x_cut = solve_upper(lambda x: -(g_mass(par, x, inf) - G0), xs, 30.0)
    sets = [
        (((xs, inf),), "minimal pool [x*, inf)"),
        (((xs, 1.2), (1.6, inf)), "[x*, 1.2) U [1.6, inf)"),
        (tuple([(xs, 2.0)] + [(2.5 + j, 3.0 + j) for j in range(8)] + [(10.5, inf)]),
         "[x*, inf) minus [2+j, 2.5+j), j = 0..8"),
        (((1.0, inf),), "plateau only [1, inf)"),
        (((xs, y_np),), f"least entry [x*, y], y = {y_np:.6f}"),
        (((xs, y_np + 0.01),), "[x*, y + 0.01]"),
        (((xs, 1.0), (y_tail, inf)), f"least entry [x*, 1) U [y', inf), y' = {y_tail:.6f}"),
        (((x_cut, inf),), f"cutoff family end [x', inf), x' = {x_cut:.6f}"),
        (((xs, y_np - 0.05),), "[x*, y - 0.05]: too little g-mass"),
        (((xs, 1.0),), "[x*, 1): too little g-mass"),
    ]
    return [verify(par, r, e, lab) for e, lab in sets]


def range_rows(par: Primitives) -> list[dict]:
    rows = []
    rC = r_ceiling(par)
    for r in sorted(set(np.round(np.arange(2.05, 3.59, 0.05), 3).tolist() + [R_J + 1e-6, 3.0, rC - 1e-6])):
        acq = acquisition(par, r)
        xs = minimal_entry(par, acq, pure(1.0, -1.0))[0][0]
        G0 = par.k / ((1 - 1 / par.b) * acq.DeltaT)
        if g_mass(par, xs, math.inf) < G0:
            continue
        y = solve_upper(lambda t: g_mass(par, xs, t) - G0, xs, 40.0)
        x_cut = solve_upper(lambda t: -(g_mass(par, t, math.inf) - G0), xs, 40.0)
        E_max = 0.5 * flow_mass(par, xs, math.inf)
        E_min = 0.5 * flow_mass(par, xs, y)
        E_cut = 0.5 * flow_mass(par, x_cut, math.inf)
        rows.append({"r": r, "x_star": xs, "E_max_minimal_pool": E_max, "E_min_any_entry_set": E_min,
                     "least_entry_set_upper_end_y": y, "E_min_cutoff_family": E_cut, "cutoff_end_x'": x_cut,
                     "status": "numerical diagnostic (closed-form integrals)"})
    return rows


def holed(entry: tuple[tuple[float, float], ...], holes: list[tuple[float, float]]) -> tuple[tuple[float, float], ...]:
    out = list(entry)
    for h0, h1 in holes:
        nxt = []
        for lo, hi in out:
            if h1 <= lo or h0 >= hi:
                nxt.append((lo, hi))
                continue
            if lo < h0:
                nxt.append((lo, h0))
            if h1 < hi:
                nxt.append((h1, hi))
        out = nxt
    return tuple(out)


def mixed_scan_rows(par: Primitives) -> list[dict]:
    grid = np.linspace(0.0, 1.0, 401)
    rows = []
    for r in [1.66, 1.8, 2.0, 2.5, 3.0, 3.5]:
        acq = acquisition(par, r)
        n_sched, n_int, worst = 0, 0, -math.inf
        for lam in (1.0, 0.9, 0.75, 0.5):
            for s1 in (0.0, 0.3, 0.6, 0.85):
                for z in np.linspace(0.2, 1.0, 9):
                    for z2, wz in ((None, 1.0), (0.3, 0.6)):
                        qL = (-float(z),) if z2 is None else (-float(z), -z2)
                        wL = (1.0,) if z2 is None else (wz, 1.0 - wz)
                        prof = (Profile((1.0,), (1.0,), qL, wL) if lam == 1.0
                                else Profile((s1, 1.0), (1.0 - lam, lam), qL, wL))
                        xs = threshold_flow(par, prof, acq.tau)
                        if xs == math.inf:
                            continue
                        base = ((xs, math.inf),)
                        for entry in (base, ((xs + 0.5, math.inf),),
                                      holed(base, [(xs + 0.05, xs + 0.15)]),
                                      holed(base, [(1.1, 1.6), (2.0, 2.4)])):
                            v = payoff_curve(par, acq, prof, entry, "H", grid)
                            n_sched += 1
                            d = np.diff(v)
                            idx = [i for i in range(1, len(d)) if d[i - 1] > 0 and d[i] <= 0]
                            if idx:
                                n_int += 1
                                worst = max(worst, float(v[idx].max() - max(v[-1], 0.0)))
        rows.append({"r": r, "schedules": n_sched, "H_interior_local_max": n_int,
                     "max_interior_minus_corner": worst if n_int else math.nan,
                     "status": "numerical diagnostic"})
    return rows


def identity_rows(par: Primitives) -> list[dict]:
    rows = []
    for r, prof in [(3.0, pure(1.0, -1.0)), (2.0, pure(1.0, -0.7)),
                    (3.0, Profile((0.6, 1.0), (0.3, 0.7), (-1.0,), (1.0,))),
                    (2.5, Profile((0.9, 1.0), (0.5, 0.5), (-0.8, -0.4), (0.7, 0.3)))]:
        acq = acquisition(par, r)
        xs = threshold_flow(par, prof, acq.tau)
        for entry in (((xs, math.inf),), holed(((xs, math.inf),), [(1.2, 2.0)])):
            lhs = sum(w * acq.DeltaT * residual_integral(par, prof, entry, "H", q) for q, w in zip(prof.qH, prof.wH))
            rhs = sum(w * acq.DeltaT * residual_integral(par, prof, entry, "L", q) for q, w in zip(prof.qL, prof.wL))
            rows.append({"r": r, "sigma_H": str(list(zip(prof.qH, prof.wH))), "sigma_L": str(list(zip(prof.qL, prof.wL))),
                         "entry": str([(round(a, 4), b) for a, b in entry]), "E_sigmaH_F_H": lhs, "E_sigmaL_F_L": rhs,
                         "difference": lhs - rhs, "status": "numerical diagnostic"})
    return rows


def main() -> None:
    par = BENCH
    write_csv(HERE / "holes_r3.csv", holes_rows(par))
    print("holes done", flush=True)
    write_csv(HERE / "holes_range.csv", range_rows(par))
    print("range done", flush=True)
    write_csv(HERE / "identity_check.csv", identity_rows(par))
    print("identity done", flush=True)
    write_csv(HERE / "mixed_scan.csv", mixed_scan_rows(par))
    print("mixed done", flush=True)


if __name__ == "__main__":
    main()
