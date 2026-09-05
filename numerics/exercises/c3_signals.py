"""C.3: complementary private signals, declared example and the 5x5 accuracy sweep."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy import integrate

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.auction import payoffs_closed_form  # noqa: E402
from numerics.deviations import deviation_scan  # noqa: E402
from numerics.exercises.common import deviation_rows  # noqa: E402
from numerics.information import OrderProfile  # noqa: E402
from numerics.io import write_csv, write_manifest  # noqa: E402
from numerics.noise import pdf  # noqa: E402
from numerics.params import CONTROLS, SIGNAL, SIGNAL_ACCURACIES, SIGNAL_STRENGTHS, SIGNAL_SWEEP_A, SIGNAL_SWEEP_D  # noqa: E402
from numerics.quadrature import integrate_segments, segments  # noqa: E402
from numerics.signals import (SignalSchedule, full_order_signal_objects, make_signal_schedule, phi, signal_margins)  # noqa: E402

TOL = CONTROLS.independent_formula_acceptance


def _flow_int(sched: SignalSchedule, fun) -> float:
    lo, hi = sched.hull()
    b = sched.prim.fb
    bps = list(sched.breakpoints)
    lo, hi = min([lo, *bps]) - 1, max([hi, *bps]) + 1
    T = 60 * b
    return integrate_segments(fun, segments([lo - T, lo, *bps, hi, hi + T], b), 48)


def validate_signal(sched: SignalSchedule, closed: dict | None) -> dict:
    prim, pay, a, d = sched.prim, sched.pay, sched.a, sched.d
    rho, b = prim.frho, prim.fb
    breaches = []
    # entry by (OA.40)-(OA.41) style flow integration over fundamental-conditioned densities
    fH = lambda x: a * sched.profile.a(prim.noise, b, x, "H") + (1 - a) * sched.profile.a(prim.noise, b, x, "L")
    fL = lambda x: (1 - a) * sched.profile.a(prim.noise, b, x, "H") + a * sched.profile.a(prim.noise, b, x, "L")
    eH = _flow_int(sched, lambda x: fH(x) * sched.entry_states(x)[0])
    eL = _flow_int(sched, lambda x: fL(x) * sched.entry_states(x)[1])
    # independent: sum over (Theta, T, Y) states and integrate Z (noise realization)
    def joint(theta: str) -> float:
        tot = 0.0
        pT = {"+": a if theta == "H" else 1 - a, "-": 1 - a if theta == "H" else a}
        pY = {"+": d if theta == "H" else 1 - d, "-": 1 - d if theta == "H" else d}
        for T, q in (("+", sched.profile.q_H[0]), ("-", sched.profile.q_L[0])):
            for y in ("+", "-"):
                def ind(z, y=y, q=q):
                    mu = sched.mu(z + q)
                    return rho + (1 - rho) * (pay.B(phi(mu, d, y)) >= prim.fc_H)
                lo, hi = sched.hull()
                bps = [bp - q for bp in sched.breakpoints]
                T_ = 60 * b
                val = integrate_segments(lambda z: pdf(prim.noise, z, b) * ind(z), segments([-T_ - 2, *bps, T_ + 2], b), 48)
                tot += pT[T] * pY[y] * val
        return tot
    eH2, eL2 = joint("H"), joint("L")
    entry_err = max(abs(eH - eH2), abs(eL - eL2))
    if closed is not None:
        entry_err = max(entry_err, abs(eH - closed["e_H"]), abs(eL - closed["e_L"]))
    if entry_err > TOL:
        breaches.append(f"entry_independent_error={entry_err:.3e}")
    E, O_H = 0.5 * (eH + eL), 0.5 * eH
    R_T = pay.t_0 + 0.5 * (eH * pay.w_H + eL * pay.w_L)
    g = lambda x: 0.5 * (fH(x) + fL(x))
    EP = _flow_int(sched, lambda x: g(x) * sched.price(x))
    price_mean_err = abs(EP - R_T)
    # pointwise price identity: P(x) = E[V_T | X = x] via the joint likelihood of (Theta, T)
    xs = np.linspace(-6 - 40, 6 + 40, 8001)
    xs = np.array(sorted(set(xs.tolist()) | set(sched.breakpoints)))
    muX = sched.mu(xs)
    eHx, eLx = sched.entry_states(xs)
    EV = pay.t_0 + muX * eHx * pay.w_H + (1 - muX) * eLx * pay.w_L
    eps_P = float(np.max(np.abs(sched.price(xs) - EV)))
    # direct: Pr(H|x) from the joint likelihood a f(x-q+) + (1-a) f(x-q-) over the total
    aH = fH(xs)
    aL = fL(xs)
    post_err = float(np.max(np.abs(aH / (aH + aL) - muX)))
    # public posterior recovered from the price, then updated with Y, versus the direct joint posterior
    def invert(Pobs: float) -> float:
        m_lo, m_hi = sched.mu(np.array([-1e3]))[0], sched.mu(np.array([1e3]))[0]
        lo_, hi_ = min(m_lo, m_hi) - 1e-12, max(m_lo, m_hi) + 1e-12
        def Pmu(mu):
            Ip = float(pay.B(phi(mu, d, "+")) >= prim.fc_H)
            Im = float(pay.B(phi(mu, d, "-")) >= prim.fc_H)
            eh = rho + (1 - rho) * (d * Ip + (1 - d) * Im)
            el = rho + (1 - rho) * ((1 - d) * Ip + d * Im)
            return pay.t_0 + mu * eh * pay.w_H + (1 - mu) * el * pay.w_L
        if Pobs <= Pmu(lo_):
            return lo_
        if Pobs >= Pmu(hi_):
            return hi_
        for _ in range(200):
            mid = 0.5 * (lo_ + hi_)
            if Pmu(mid) <= Pobs:
                lo_ = mid
            else:
                hi_ = mid
        return 0.5 * (lo_ + hi_)
    sub = xs[:: max(1, len(xs) // 300)]
    inv_err = 0.0
    hull = sched.hull()
    if hull[1] - hull[0] > 1e-14:
        for x in sub:
            mu_rec = invert(float(sched.price(np.array([x]))[0]))
            mu_true = float(sched.mu(np.array([x]))[0])
            inv_err = max(inv_err, abs(mu_rec - mu_true))
            for y in ("+", "-"):
                Ly_H, Ly_L = (d, 1 - d) if y == "+" else (1 - d, d)
                direct = mu_true * Ly_H / (mu_true * Ly_H + (1 - mu_true) * Ly_L)
                inv_err = max(inv_err, abs(float(phi(mu_rec, d, y)) - direct))
    resid_err = max(float(np.max(np.abs(sched.A(xs, s) - sched.A_direct(xs, s)))) for s in "HL")
    for name, val, tol in (("epsilon_P", eps_P, CONTROLS.price_identity_acceptance), ("posterior_error", post_err, TOL),
                           ("posterior_inversion_error", inv_err, 1e-7), ("residual_error", resid_err, TOL),
                           ("mean_price_error", price_mean_err, CONTROLS.probability_acceptance)):
        if val > tol:
            breaches.append(f"{name}={val:.3e}")
    # entry optimality for each (Y, cost) at tested prices
    eps_e = 0.0
    for y in ("+", "-"):
        Bp = pay.B(phi(muX, d, y))
        for c in (prim.fc_L, prim.fc_H):
            enters = Bp >= c
            eps_e = max(eps_e, float(np.max(np.maximum(np.where(enters, c - Bp, Bp - c), 0.0))))
    if eps_e > CONTROLS.entry_optimality_acceptance:
        breaches.append(f"epsilon_e={eps_e:.3e}")
    # global trader deviations (the investor never observes Y)
    scans = {}
    eps_q = 0.0
    for s in "HL":
        sc = deviation_scan(sched, s, CONTROLS.initial_order_intervals)
        sc2 = deviation_scan(sched, s, CONTROLS.refined_order_intervals, n=64)
        scans[s] = sc
        scans[s + "_refined"] = sc2
        eps_q = max(eps_q, sc["max_gain"], sc2["max_gain"])
    if eps_q > CONTROLS.deviation_gain_acceptance:
        breaches.append(f"epsilon_q={eps_q:.3e}")
    return {"e_H": eH, "e_L": eL, "E": E, "O_H": O_H, "R_T": R_T, "epsilon_P": eps_P, "epsilon_e": eps_e, "epsilon_q": eps_q,
            "posterior_error": max(post_err, inv_err), "residual_error": resid_err, "entry_err": entry_err, "breaches": breaches,
            "accepted": not breaches, "scans": scans}


def solve_pair(prim, a_s: str, d_s: str, checks: dict, dev_rows: list, ledger: bool) -> list[dict]:
    a, d = float(a_s), float(d_s)
    pay0 = payoffs_closed_form(prim, float(SIGNAL_STRENGTHS["r_weak"]))
    pay1 = payoffs_closed_form(prim, float(SIGNAL_STRENGTHS["r_strong"]))
    mg = signal_margins(prim, pay0, pay1, a, d)
    five = [mg[k] for k in ("low_cost_margin", "private_only_exclusion_margin", "joint_entry_margin", "weak_order_margin", "strong_order_margin")]
    all_pos = all(z > 0 for z in five)
    rows = []
    for name, pay in (("r_weak", pay0), ("r_strong", pay1)):
        results = {}
        for branch, prof in (("pooling", OrderProfile.pure(0.0, 0.0)), ("full_orders", OrderProfile.pure(1.0, -1.0))):
            sched = make_signal_schedule(prim, pay, prof, a, d)
            closed = full_order_signal_objects(prim, pay, a, d) if branch == "full_orders" else None
            v = validate_signal(sched, closed)
            results[branch] = (sched, v, closed)
            checks[f"{branch}_{name}_a{a_s}_d{d_s}"] = {"accepted": v["accepted"], "breaches": v["breaches"]}
            if ledger:
                class _V:  # adapter for deviation_rows
                    scans = v["scans"]
                dev_rows += [{"a": a_s, "d": d_s, "r": SIGNAL_STRENGTHS[name], "trader_signal": ("+" if row["state"] == "H" else "-"), **{k: row[k] for k in ("q", "U(q)", "U(candidate)", "deviation_gain", "quadrature_error", "tail_bound")}}
                             for row in deviation_rows({}, _V)]
        accepted = [b_ for b_, (_, v, _) in results.items() if v["accepted"]]
        want = "pooling" if name == "r_weak" else "full_orders"
        theorem = all_pos and accepted == [want]
        for branch in accepted:
            sched, v, closed = results[branch]
            xs_p = closed["x_star_Yplus"] if closed else ("n/a")
            xs_m = closed["x_star_Yminus"] if closed else ("n/a")
            status = ("analytical (Theorem R2 region: all five margins strictly positive; unique outcome)" if theorem and branch == want
                      else "numerical diagnostic (validated candidate; theorem margins not all positive or multiple candidates)")
            rows.append({"a": a_s, "d": d_s, "r": SIGNAL_STRENGTHS[name], "q_plus": sched.profile.q_H[0], "q_minus": sched.profile.q_L[0],
                         "mu_lower": mg["mu_lower"], "mu_upper": mg["mu_upper"], "phi_minus_mu_lower": mg["phi_minus_mu_lower"],
                         "phi_plus_mu_upper": mg["phi_plus_mu_upper"], "x_star_Yplus": xs_p, "x_star_Yminus": xs_m,
                         "e_H": v["e_H"], "e_L": v["e_L"], "E": v["E"], "O_H": v["O_H"], "R_T": v["R_T"],
                         **{k: mg[k] for k in ("low_cost_margin", "private_only_exclusion_margin", "joint_entry_margin", "weak_order_margin", "strong_order_margin")},
                         "posterior_error": v["posterior_error"], "residual_error": v["residual_error"], "epsilon_P": v["epsilon_P"], "epsilon_q": v["epsilon_q"],
                         "status": status, "accepted": True})
        for branch in results:
            if branch not in accepted:
                sched, v, closed = results[branch]
                rows.append({"a": a_s, "d": d_s, "r": SIGNAL_STRENGTHS[name], "q_plus": sched.profile.q_H[0], "q_minus": sched.profile.q_L[0],
                             "mu_lower": mg["mu_lower"], "mu_upper": mg["mu_upper"], "phi_minus_mu_lower": mg["phi_minus_mu_lower"],
                             "phi_plus_mu_upper": mg["phi_plus_mu_upper"], "x_star_Yplus": "n/a", "x_star_Yminus": "n/a",
                             "e_H": v["e_H"], "e_L": v["e_L"], "E": v["E"], "O_H": v["O_H"], "R_T": v["R_T"],
                             **{k: mg[k] for k in ("low_cost_margin", "private_only_exclusion_margin", "joint_entry_margin", "weak_order_margin", "strong_order_margin")},
                             "posterior_error": v["posterior_error"], "residual_error": v["residual_error"], "epsilon_P": v["epsilon_P"], "epsilon_q": v["epsilon_q"],
                             "status": "rejected: " + "; ".join(v["breaches"]), "accepted": False})
        checks[f"node_{name}_a{a_s}_d{d_s}"] = {"accepted_branches": accepted, "theorem_region": theorem}
    return rows


def run() -> bool:
    checks, dev_rows = {}, []
    prim = SIGNAL
    rows = solve_pair(prim, SIGNAL_ACCURACIES["a"], SIGNAL_ACCURACIES["d"], checks, dev_rows, ledger=True)
    for a_s in SIGNAL_SWEEP_A:
        for d_s in SIGNAL_SWEEP_D:
            if (a_s, d_s) == (SIGNAL_ACCURACIES["a"], SIGNAL_ACCURACIES["d"]):
                continue
            rows += solve_pair(prim, a_s, d_s, checks, dev_rows, ledger=False)
    cols = ["a", "d", "r", "q_plus", "q_minus", "mu_lower", "mu_upper", "phi_minus_mu_lower", "phi_plus_mu_upper", "x_star_Yplus", "x_star_Yminus",
            "e_H", "e_L", "E", "O_H", "R_T", "low_cost_margin", "private_only_exclusion_margin", "joint_entry_margin", "weak_order_margin",
            "strong_order_margin", "posterior_error", "residual_error", "epsilon_P", "epsilon_q", "status", "accepted"]
    write_csv("numerics/two_signals.csv", cols, rows)
    write_csv("numerics/two_signal_deviations.csv", ["a", "d", "r", "trader_signal", "q", "U(q)", "U(candidate)", "deviation_gain", "quadrature_error", "tail_bound"], dev_rows)
    decl = [r for r in rows if r["a"] == SIGNAL_ACCURACIES["a"] and r["d"] == SIGNAL_ACCURACIES["d"] and r["accepted"]]
    ok = len(decl) == 2 and all(r["status"].startswith("analytical") for r in decl)
    checks["declared_example"] = {"pass": ok, "rows": [(r["r"], r["E"], r["status"]) for r in decl]}
    n_theorem = sum(1 for k, v in checks.items() if k.startswith("node_r_strong") and v["theorem_region"])
    checks["sweep_theorem_region_count"] = {"strong_nodes_in_region": n_theorem, "of": len(SIGNAL_SWEEP_A) * len(SIGNAL_SWEEP_D)}
    write_manifest("c3_signals", {"signal": prim.__dict__, "strengths": SIGNAL_STRENGTHS, "accuracies": SIGNAL_ACCURACIES,
                                  "sweep_a": SIGNAL_SWEEP_A, "sweep_d": SIGNAL_SWEEP_D},
                   "Signal-contingent schedules (OA.35, OA.37); entry by fundamental-conditioned flow densities and independently by the joint "
                   "(Theta, T, Y, Z) sum; pointwise price identity, price inversion plus Y-update versus joint likelihood, residual identities, "
                   "state-contingent entry optimality, global trader deviations on both grids (trader never sees Y).",
                   CONTROLS.as_dict(), ["numerics/two_signals.csv", "numerics/two_signal_deviations.csv"], checks, ok)
    print("C.3 passed" if ok else "C.3 FAILED", checks["declared_example"], checks["sweep_theorem_region_count"])
    return ok


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
