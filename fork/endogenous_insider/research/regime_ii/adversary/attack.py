"""Adversary track: attacks on the regime II version of Proposition 2. Writes CSV files only.

  python3 attack.py rho        rho_floor.csv, rho_star.csv: the cheap-type share breaks the entry reversal
  python3 attack.py examples   counterexamples.csv: full checks and certificates of named profiles
  python3 attack.py starved    starved_hcheck.csv: the high type along the starved family (certificates)
  python3 attack.py halfline   halfline_thresholds.csv: independent re-computation of Prop R.9 thresholds
  python3 attack.py a3prime    a3prime_feasible.csv: when (A3') is nonempty (largest r0)
  python3 attack.py mixed      mixed_window.csv: lattice audit of low-type mixtures in the open window
  python3 attack.py all        everything except 'mixed'

Benchmark primitives (h, ell, p, b, k, c_H) = (10, 1, 0.5, 2, 0.02, 6), r0 = 1.2, r1 = 3 unless a row says
otherwise. Every number is a numerical diagnostic unless the note says closed form.
"""
from __future__ import annotations

import csv
import math
import sys
import time
from pathlib import Path

import numpy as np

from model import (Econ, Profile, F, K_forcing, S, SX, a3_window, bathtub_inf, best_response, certify, check, gross,
                   flow_of_belief, full_minimal, gross_parts, make_econ, mu_of, outcome, pool_belief_halfline,
                   pure, regime, rho_star_floor, schedule, starved_cutoff, starved_pool_belief, v_H)

HERE = Path(__file__).resolve().parent
R0, R1, CH, K = 1.2, 3.0, 6.0, 0.02


def fmt(v: object) -> str:
    if isinstance(v, (bool, np.bool_)):
        return "true" if v else "false"
    if isinstance(v, (float, np.floating)):
        if math.isnan(v):
            return "nan"
        if math.isinf(v):
            return "inf" if v > 0 else "-inf"
        return f"{float(v):.10g}"
    return str(v)


def write(path: Path, rows: list[dict]) -> None:
    cols: list[str] = []
    for r in rows:
        for c in r:
            if c not in cols:
                cols.append(c)
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: fmt(r.get(c, "")) for c in cols})
    print(f"wrote {path.name}: {len(rows)} rows")


# ----------------------------------------------------------------------------------------------
# attack 1: the cheap-type share
# ----------------------------------------------------------------------------------------------

def attack_rho() -> None:
    rows = []
    for r1 in (2.5, 3.0, 3.5):
        ec = make_econ(r1, 0.25, 3.0, CH)
        rE, rO, a, pi0 = rho_star_floor(ec)
        rows.append({"r1": r1, "cH": CH, "tauH": ec.tauH, "xstar": flow_of_belief(ec, ec.tauH), "a": a, "pi0": pi0,
                     "rho_star_entry": rE, "rho_star_ownership": rO, "B_m": ec.gL + ec.m * (ec.gH - ec.gL),
                     "status": "closed form"})
    write(HERE / "rho_star.csv", rows)

    rows = []
    for rho in (0.1, 0.25, 0.4, 0.5, 0.515, 0.52, 0.6, 0.7, 0.75, 0.8, 0.9):
        for cL in (2.37, 2.4, 2.5, 2.8, 3.0, 3.46):
            ec = make_econ(R1, rho, cL, CH)
            fm = full_minimal(ec)
            infE, _ = bathtub_inf(ec, "E")
            infH, _ = bathtub_inf(ec, "eH")
            Kc = K_forcing(ec)
            d0, top = a3_window(ec, R0)
            rows.append({"rho": rho, "cL": cL, "tauL": ec.tauL, "z0": fm.z0, "pool_prob_min": fm.pool_prob,
                         "E0": fm.E0, "inf_E_bathtub": infE, "eH0": fm.eH0, "inf_eH_bathtub": infH,
                         "E0_minus_rho": fm.E0 - rho, "eH0_minus_rho": fm.eH0 - rho,
                         "entry_fails_min_pool": fm.E0 < rho, "entry_fails_some_pool": infE < rho,
                         "own_fails_min_pool": fm.eH0 < rho, "own_fails_some_pool": infH < rho,
                         "K": Kc, "A3_top": top, "DeltaT_r0": d0, "A3_holds_k02": d0 < K < top,
                         "A3prime_holds_k02": d0 < K <= Kc, "min_pool_test_margin": fm.test_margin})
    write(HERE / "rho_floor.csv", rows)


# ----------------------------------------------------------------------------------------------
# attack 2: named counterexamples, fully checked
# ----------------------------------------------------------------------------------------------

def _row(label: str, ec: Econ, prof: Profile, certs: bool = True) -> dict:
    t = time.time()
    c = check(ec, prof)
    sch = schedule(ec, prof)
    row = {"label": label, "r1": ec.r, "rho": ec.rho, "cL": ec.cL, "cH": ec.cH, "k": ec.k, "regime": regime(ec),
           "tauL": ec.tauL, "H": ";".join(f"{q}:{w}" for q, w in prof.H), "L": ";".join(f"{q}:{w}" for q, w in prof.L),
           "pool": ";".join(f"[{a},{b})" for a, b in prof.pool), "consistent": c.consistent,
           "pool_belief": c.pool_belief, "pool_prob": c.pool_prob, "E": c.E, "O_H": c.O_H, "eH": c.eH, "eL": c.eL,
           "E_weak": ec.rho, "OH_weak": 0.5 * ec.rho, "E_below_rho": c.E < ec.rho, "OH_below_half_rho": c.O_H < 0.5 * ec.rho,
           "regret_H": c.regret_H, "regret_L": c.regret_L, "uH": c.uH, "uL": c.uL, "accepted": c.accepted,
           "mu_max": sch.mu_max, "mu_min_A": sch.mu_min_A}
    if certs and len(prof.H) == 1 and len(prof.L) == 1:
        cH = certify(sch, "H", prof.H[0][0])
        cL = certify(sch, "L", prof.L[0][0])
        row.update({"cert_H": cH.certified, "cert_H_far": cH.far_margin, "cert_H_near": cH.near_margin,
                    "cert_L": cL.certified, "cert_L_far": cL.far_margin, "cert_L_near": cL.near_margin,
                    "cert_L_excl": cL.exclusion})
        row["status"] = "computer-assisted (float quad)" if (c.accepted and cH.certified and cL.certified) else \
            ("numerical diagnostic" if c.accepted else "rejected")
    else:
        row["status"] = "numerical diagnostic" if c.accepted else "rejected"
    row["seconds"] = time.time() - t
    return row


def attack_examples() -> None:
    rows = []
    # (a) rho above rho*: full orders, minimal pool, at the paper's k and r0. (A3') holds (K scales with rho).
    for rho, cL in ((0.6, 2.4), (0.52, 2.37), (0.6, 3.0), (0.75, 2.4), (0.8, 2.4), (0.5, 2.37), (0.5, 2.4)):
        ec = make_econ(R1, rho, cL, CH)
        fm = full_minimal(ec)
        rows.append(_row(f"rho={rho} minimal pool", ec, pure(1.0, -1.0, cutoff=fm.z0)))
    # (b) rho = 0.6, c_L = 2.4: the bathtub (worst) pool truncated to a consistent member
    ec = make_econ(R1, 0.6, 2.4, CH)
    fm = full_minimal(ec)
    rows.append(_row("rho=0.6 half-line pool x'=-0.7", ec, pure(1.0, -1.0, cutoff=-0.7)))
    rows.append(_row("rho=0.6 island pool", ec, pure(1.0, -1.0, cutoff=fm.z0, extra=[(fm.xstar, fm.xstar + 0.03)])))
    # (c) teammates' counterexamples at rho = 0.25
    ec = make_econ(R1, 0.25, 3.5, CH)
    rows.append(_row("numerics #2 starved c_L=3.5", ec, pure(1.0, -0.7196, cutoff=0.5)))
    ec = make_econ(R1, 0.25, 3.0, CH)
    xp = starved_cutoff(ec, 0.7344)
    rows.append(_row("numerics #3 starved c_L=3.0", ec, pure(1.0, -0.7344, cutoff=xp)))
    ec = make_econ(R1, 0.25, 3.7, CH)
    rows.append(_row("theory R.9 half-line c_L=3.7 x'=1.7", ec, pure(1.0, -1.0, cutoff=1.7)))
    ec = make_econ(R1, 0.25, 4.0, CH)
    rows.append(_row("numerics corner (1,0) c_L=4.0", ec, pure(1.0, 0.0, cutoff=1.906076), certs=False))
    # (d) clean-range controls at rho = 0.25
    for cL in (2.4, 2.5, 2.8):
        ec = make_econ(R1, 0.25, cL, CH)
        fm = full_minimal(ec)
        rows.append(_row(f"control rho=0.25 minimal pool c_L={cL}", ec, pure(1.0, -1.0, cutoff=fm.z0)))
    # (e) regime I control
    ec = make_econ(R1, 0.25, 1.0, CH)
    rows.append(_row("regime I paper benchmark c_L=1", ec, pure(1.0, -1.0)))
    write(HERE / "counterexamples.csv", rows)


# ----------------------------------------------------------------------------------------------
# attack 3: the high type along the starved family
# ----------------------------------------------------------------------------------------------

def attack_starved() -> None:
    rows = []
    for cL in (3.0, 3.1, 3.25, 3.5, 3.75, 3.9):
        ec = make_econ(R1, 0.25, cL, CH)
        vh = v_H(ec)
        for v in np.linspace(0.05, vh - 1e-6, 9):
            xp = starved_cutoff(ec, float(v))
            if xp is None:
                continue
            belief = starved_pool_belief(ec, float(v), xp)
            prof = pure(1.0, -float(v), cutoff=xp)
            sch = schedule(ec, prof)
            o = outcome(sch)
            cH = certify(sch, "H", 1.0)
            cL_ = certify(sch, "L", -float(v))
            brH = best_response(sch, "H", [1.0], n=201)
            rows.append({"cL": cL, "tauL": ec.tauL, "v": v, "x_prime": xp, "pool_belief": belief,
                         "consistent": belief < ec.tauL, "E": o.E, "O_H": o.O_H, "uH_full": cH.u_own,
                         "uH_identity": ec.k * v / (ec.b - v), "H_best_q": brH.q_best, "H_regret": brH.regret,
                         "cert_H": cH.certified, "cert_H_far": cH.far_margin, "cert_H_near": cH.near_margin,
                         "cert_L": cL_.certified, "cert_L_far": cL_.far_margin, "cert_L_near": cL_.near_margin,
                         "member": belief < ec.tauL and cH.certified and cL_.certified})
    write(HERE / "starved_hcheck.csv", rows)


# ----------------------------------------------------------------------------------------------
# attack 4: half-line thresholds (Prop R.9), recomputed
# ----------------------------------------------------------------------------------------------

def attack_halfline() -> None:
    from scipy.optimize import brentq
    rows = []
    for rho in (0.1, 0.2, 0.25, 0.3, 0.35, 0.5):
        ec = make_econ(R1, rho, 3.0, CH)
        xk = 1.0 + ec.b * math.log((1.0 - 1.0 / ec.b) * ec.m * ec.DeltaT / (2.0 * ec.k))
        xs = flow_of_belief(ec, ec.tauH)
        # entry S_X(x') = rho and e_H = S(x'-1) = rho
        xE = brentq(lambda x: SX(ec, x) - rho, xs, 60.0) if SX(ec, xs) > rho else float("nan")
        xO = brentq(lambda x: S(ec, x - 1.0) - rho, xs, 60.0) if S(ec, xs - 1.0) > rho else float("nan")
        Bof = lambda mu: ec.gL + mu * (ec.gH - ec.gL)  # noqa: E731
        rows.append({"rho": rho, "x_k": xk, "x_E": xE, "x_O": xO, "within_test_E": xE <= xk, "within_test_O": xO <= xk,
                     "cL_threshold_E": Bof(pool_belief_halfline(ec, xE)) if xE <= xk else float("nan"),
                     "cL_threshold_O": Bof(pool_belief_halfline(ec, xO)) if xO <= xk else float("nan"),
                     "status": "closed form"})
    write(HERE / "halfline_thresholds.csv", rows)


# ----------------------------------------------------------------------------------------------
# attack 5: when is (A3') nonempty
# ----------------------------------------------------------------------------------------------

def attack_a3prime() -> None:
    rows = []
    for rho in (0.1, 0.25, 0.4, 0.5, 0.6, 0.75):
        for cL in (2.37, 2.4, 2.5, 2.6, 2.8, 3.0, 3.46, 3.74):
            ec = make_econ(R1, rho, cL, CH)
            Kc = K_forcing(ec)
            # Delta_T(r0) = (r0 - ell)^2 / (2 r0) < K  <=>  r0 < ell + K + sqrt(K^2 + 2 ell K)
            r0max = ec.ell + Kc + math.sqrt(Kc * Kc + 2.0 * ec.ell * Kc)
            rows.append({"rho": rho, "cL": cL, "K": Kc, "A3_top": a3_window(ec, R0)[1], "r0_max_for_A3prime": r0max,
                         "r0=1.2_allowed": r0max > R0, "k=0.02_allowed": Kc >= K, "status": "closed form"})
    write(HERE / "a3prime_feasible.csv", rows)


# ----------------------------------------------------------------------------------------------
# attack 6: low-type mixtures in the open window (2.59, 2.98]
# ----------------------------------------------------------------------------------------------

def _peaks(u: np.ndarray, tol: float = 1e-12) -> list[int]:
    out = []
    n = len(u)
    for i in range(n):
        left = u[i] - u[i - 1] if i > 0 else math.inf
        right = u[i] - u[i + 1] if i < n - 1 else math.inf
        if u[i] > tol and left > tol and right >= -tol:
            out.append(i)
        elif u[i] > tol and left >= -tol and right > tol and (not out or i - out[-1] > 1):
            out.append(i)
    return out


def attack_mixed() -> None:
    rows = []
    sgrid = np.linspace(0.0, 1.0, 101)
    v1s = (0.0, 0.2, 0.4, 0.6)
    v2s = (0.5, 0.7, 0.74, 0.9, 1.0)
    ws = (0.2, 0.5, 0.8)
    cuts = (-1.0, -0.75, -0.5, -0.25, 0.0, 0.25, 0.5)
    islands = ((), ((0.6, 1.1),), ((1.5, math.inf),))
    t0 = time.time()
    for cL in (2.6, 2.7, 2.8, 2.9, 2.98):
        ec = make_econ(R1, 0.25, cL, CH)
        n_cons = 0
        for v1 in v1s:
            for v2 in v2s:
                if v2 <= v1:
                    continue
                for w in ws:
                    for cut in cuts:
                        for isl in islands:
                            prof = Profile(H=((1.0, 1.0),), L=((-v1, 1.0 - w), (-v2, w)), pool=((-math.inf, cut),) + isl)
                            sch = schedule(ec, prof)
                            if not sch.consistent:
                                continue
                            n_cons += 1
                            uL = np.array([s * gross(sch, "L", -s) - ec.k * s for s in sgrid])
                            uH = np.array([s * gross(sch, "H", s) - ec.k * s for s in sgrid])
                            pL, pH = _peaks(uL), _peaks(uH)
                            gapL = (sorted(uL[pL])[-1] - sorted(uL[pL])[-2]) if len(pL) > 1 else math.inf
                            gapH = (sorted(uH[pH])[-1] - sorted(uH[pH])[-2]) if len(pH) > 1 else math.inf
                            iL = int(np.argmax(uL))
                            lo_, hi_ = gross_parts(sch, "L", -float(sgrid[iL]))
                            inf_A = min(lo for lo, hi, e in sch.pieces if e > 0.0)
                            rows.append({"cL": cL, "v1": v1, "v2": v2, "w": w, "cutoff": cut,
                                         "island": ";".join(f"[{a},{b})" for a, b in isl), "pool_belief": sch.pool_belief,
                                         "pool_prob": sch.pool_prob, "inf_A": inf_A, "mu_max": sch.mu_max,
                                         "starved": sch.mu_max < ec.tauH, "n_peaks_L": len(pL), "n_peaks_H": len(pH),
                                         "peak_gap_L": gapL, "peak_gap_H": gapH, "L_best_grid": sgrid[iL],
                                         "H_best_grid": sgrid[int(np.argmax(uH))], "uL_best": uL[iL], "uH_best": uH.max(),
                                         "Fminus_over_Fplus_at_Lbest": lo_ / hi_ if hi_ > 0 else math.inf,
                                         "L_wants_v1": abs(sgrid[iL] - v1) < 0.011, "L_wants_v2": abs(sgrid[iL] - v2) < 0.011})
        print(f"cL={cL}: {n_cons} consistent schedules, {time.time() - t0:.0f}s", flush=True)
    write(HERE / "mixed_window.csv", rows)


# ----------------------------------------------------------------------------------------------
# attack 7: the exact rho threshold as a function of c_L (minimal pool: closed form root; all pools: bathtub)
# ----------------------------------------------------------------------------------------------

def attack_curve() -> None:
    from scipy.optimize import brentq
    rows = []
    for cL in (2.37, 2.4, 2.5, 2.6, 2.8, 3.0, 3.2, 3.46, 3.74, 4.0, 4.2):
        def gap_min(rho: float) -> float:
            return full_minimal(make_econ(R1, rho, cL, CH)).E0 - rho
        def gap_inf(rho: float) -> float:
            return bathtub_inf(make_econ(R1, rho, cL, CH), "E")[0] - rho
        def gapH_min(rho: float) -> float:
            return full_minimal(make_econ(R1, rho, cL, CH)).eH0 - rho
        def gapH_inf(rho: float) -> float:
            return bathtub_inf(make_econ(R1, rho, cL, CH), "eH")[0] - rho
        out = {"cL": cL, "tauL": make_econ(R1, 0.25, cL, CH).tauL}
        for name, g in (("rho_E_minpool", gap_min), ("rho_E_allpools", gap_inf), ("rho_O_minpool", gapH_min),
                        ("rho_O_allpools", gapH_inf)):
            out[name] = brentq(g, 1e-6, 1.0 - 1e-6, xtol=1e-10) if g(1e-6) > 0 > g(1.0 - 1e-6) else float("nan")
        out["status"] = "closed form root / fractional knapsack (numerical diagnostic)"
        rows.append(out)
    write(HERE / "rho_curve.csv", rows)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    jobs = {"rho": attack_rho, "examples": attack_examples, "starved": attack_starved, "halfline": attack_halfline,
            "a3prime": attack_a3prime, "mixed": attack_mixed, "curve": attack_curve}
    if what == "all":
        for name in ("rho", "halfline", "a3prime", "curve", "examples", "starved"):
            jobs[name]()
    else:
        jobs[what]()
