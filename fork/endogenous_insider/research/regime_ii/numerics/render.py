"""Renderer: CSV in, tables and one vector figure out. Nothing here solves, changes a parameter or drops a row.

  python3 render.py        writes tables.txt and fig_regime_ii.pdf, and refreshes every
                           <!-- T:name --> ... <!-- /T:name --> block in note.md

Status words follow the paper: analytical, computer-assisted, numerical diagnostic, open. Every number here comes
from a CSV written by a solver in this folder. A missing CSV gives a block that says "open: file missing".
"""
from __future__ import annotations

import csv
import math
import re
from fractions import Fraction
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
RHOS = ("0.1", "0.25", "0.5")


# ------------------------------------------------------------------------------------------------
# reading
# ------------------------------------------------------------------------------------------------

def read(name: str) -> list[dict] | None:
    p = HERE / name
    if not p.exists() or p.stat().st_size == 0:
        return None
    with p.open() as fh:
        rows = list(csv.DictReader(fh))
    return rows or None


def num(s: str | None) -> float:
    if s is None or s == "" or s.lower() == "nan":
        return math.nan
    if s in ("inf", "-inf"):
        return math.inf if s == "inf" else -math.inf
    return float(s)


def flag(s: str | None) -> bool | None:
    if s is None or s == "":
        return None
    return s.strip().lower() == "true"


def f4(x: float) -> str:
    return "nan" if math.isnan(x) else f"{x:.4f}"


def f3(x: float) -> str:
    return "nan" if math.isnan(x) else f"{x:.3f}"


def table(head: list[str], body: list[list[str]]) -> str:
    out = ["| " + " | ".join(head) + " |", "|" + "|".join(["---"] * len(head)) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in body]
    return "\n".join(out)


MISSING = "open: file missing (the solver has not written it)"


# ------------------------------------------------------------------------------------------------
# tables
# ------------------------------------------------------------------------------------------------

def t_r0() -> str:
    rows = read("weak_r0.csv")
    if rows is None:
        return MISSING
    body = []
    for rho in sorted({r["rho"] for r in rows}, key=lambda s: float(Fraction(s))):
        sub = [r for r in rows if r["rho"] == rho]
        e = {r["E_r0"] for r in sub}
        o = {r["OH_r0"] for r in sub}
        nt = all(r["no_trade_unique"] == "True" for r in sub)
        body.append([rho, str(len(sub)), ", ".join(sorted(e)), ", ".join(sorted(o)), "yes" if nt else "no",
                     sub[0]["DeltaT_r0"], sub[0]["k"], sub[0]["B_r0_half"] + " = " + sub[0]["B_r0_half_dec"]])
    return table(["rho", "c_L values tested", "E(r0)", "O_H(r0)", "no trade unique", "Delta_T(r0)", "k",
                  "B_r0(1/2)"], body)


def t_sweep(tag: str, picks: list[float]) -> str:
    rows = read(f"summary_r3_rho{tag}.csv")
    if rows is None:
        return MISSING
    body = []
    for c in picks:
        r = min(rows, key=lambda x: abs(num(x["cL"]) - c))
        if abs(num(r["cL"]) - c) > 1e-6:
            continue
        rng = f"{f4(num(r['E_min']))} to {f4(num(r['E_max']))}" if r["n_eq"] != "0" else "none found"
        orng = f"{f4(num(r['OH_min']))} to {f4(num(r['OH_max']))}" if r["n_eq"] != "0" else "none found"
        body.append([f"{num(r['cL']):.4f}", r["regime"], r["n_eq"], r["fam_at_Emin"], r["q_at_Emin"], rng, orng,
                     r["n_unresolved"], r["all_informative"], r["unique_full"], r["reversal_all"], r["reversal_any"]])
    return table(["c_L", "regime", "equilibria", "family at lowest E", "orders (q_H;q_L) at lowest E", "E range",
                  "O_H range", "unconverged starts", "price informative in all", "only (1,-1) found", "reversal in all",
                  "reversal in some"], body)


M_LOW = 1.0 / (1.0 + math.e)       # the low posterior m for b = 2 and full orders


def a3_right(h: dict) -> float:
    """Right side of the paper's (A3) as the theory track states it: (1 - 1/b) rho m Delta_T(r1), with b = 2."""
    return 0.5 * float(h["rho"]) * M_LOW * num(h["DeltaT"])


def clip_holds(h: dict) -> str:
    """Further hold intervals of the oracle, clipped at the lowest knapsack threshold (islands break everything above)."""
    txt = h.get("other_holds") or ""
    if not txt:
        return ""
    cap = min([num(h.get(k, "")) for k in ("cL_knapE", "cL_knapO", "cL_lpexact") if not math.isnan(num(h.get(k, "")))],
              default=math.inf)
    out = []
    for piece in txt.split(";"):
        lo, hi = (float(v) for v in piece.split("-"))
        if lo < cap:
            out.append(f"{lo:.3f}-{min(hi, cap):.3f}")
    return "; ".join(out)


def region_text(h: dict) -> str:
    txt = region_text0(h)
    return txt + (" *" if a3_right(h) < num(h["k"]) - 1e-12 else "")


def region_text0(h: dict) -> str:
    cs, cm, ch = num(h["cL_star"]), num(h["B_m"]), num(h["B_half"])
    bind = h["binding"]
    more = clip_holds(h)
    if bind in ("no-trade", "ceiling"):
        return f"empty ({bind})"
    if bind == "lowtrade" and abs(cs - cm) < 1e-9:
        return "empty at B(m) (low-trade)" + (f"; holds on {more}" if more else "")
    if math.isnan(cs):
        return f"{f3(cm)}-{f3(ch)} (all of regime II)"
    tag = {"partial": "partial", "window": "partial", "lowtrade": "low-trade", "knapE": "island E",
           "knapO": "island O_H", "lpexact": "island, exact LP"}.get(bind, bind)
    return f"{f3(cm)}-{f3(cs)} ({tag})" + (f"; again on {more}" if more else "")


def t_thresholds() -> str:
    rows = read("thresholds.csv")
    if rows is None:
        return MISSING
    body = []
    for rho in RHOS:
        for r in rows:
            if r["rho"] != rho:
                continue
            r1 = num(r["r1"])
            if round(r1 * 10) % 5 != 0 and abs(r1 - 3.6) > 1e-9:
                continue
            body.append([rho, f"{r1:g}", f4(num(r["B_m"])), f4(num(r["B_half"])), r["no_trade"], r["ceiling"],
                         f4(num(r["cL_partial"])), r["partial_kind"], f4(num(r["cL_knapE"])), f4(num(r["cL_knapO"])),
                         f4(num(r.get("cL_lpexact", ""))), f4(num(r["cL_star"])), r["binding"]])
    return table(["rho", "r1", "B(m)", "B(1/2)", "no-trade eq.", "ceiling", "c_L first break (families)", "family",
                  "c_L island E (sufficient test)", "c_L island O_H (sufficient test)", "c_L island (exact LP)",
                  "c_L* (least)", "binding"], body)


def t_thresholds_all() -> str:
    rows = read("thresholds.csv")
    if rows is None:
        return MISSING
    body = []
    for rho in RHOS:
        for r in rows:
            if r["rho"] == rho:
                cs, cm, ch = num(r["cL_star"]), num(r["B_m"]), num(r["B_half"])
                width = (cs - cm) if not math.isnan(cs) else (ch - cm)
                body.append([rho, f"{num(r['r1']):g}", f4(cm), f4(cs), f4(ch), f4(width), r["binding"],
                             f4(num(r["partial_v"])), f4(num(r["partial_E"])), f4(num(r["partial_OH"])),
                             r["grid_flags"]])
    return table(["rho", "r1", "B(m)", "c_L*", "B(1/2)", "window width", "binding", "v at break", "E at break",
                  "O_H at break", "oracle flags on the c_L grid (B = break found)"], body)


def t_region_check() -> str:
    """Cross-check of the threshold solvers against the cutoff scan, point by point (summary_region.csv)."""
    th = read("thresholds.csv")
    sm = read("summary_region.csv")
    if th is None or sm is None:
        return MISSING
    body = []
    for rho in RHOS:
        ctrl = ctrl_ok = ctrl_nt = 0
        below_ok = below_open = below_break = 0
        above_break = above_hold = above_open = 0
        for t in th:
            if t["rho"] != rho:
                continue
            cs = num(t["cL_star"])
            for s in sm:
                if abs(num(s["r"]) - num(t["r1"])) > 1e-9 or s["rho"] != rho:
                    continue
                c = num(s["cL"])
                is_open = s["n_eq"] == "0"
                rev = s["reversal_all"] == "true"
                if s["regime"] == "I":
                    ctrl += 1
                    ctrl_ok += int(rev)
                    ctrl_nt += int((not rev) and s["no_trade_r1"] == "true")
                    continue
                holds_pred = math.isnan(cs) or c < cs - 1e-9
                if holds_pred:
                    if is_open:
                        below_open += 1
                    elif rev:
                        below_ok += 1
                    else:
                        below_break += 1
                else:
                    if is_open:
                        above_open += 1
                    elif rev:
                        above_hold += 1
                    else:
                        above_break += 1
        body.append([rho, f"{ctrl_ok} of {ctrl}", f"{ctrl - ctrl_ok} (no-trade eq.: {ctrl_nt})", str(below_ok),
                     str(below_open), str(below_break), str(above_break), str(above_hold), str(above_open)])
    return table(["rho", "regime I points: reversal in all", "regime I points: reversal fails", "below c_L*: scan agrees",
                  "below c_L*: no eq. found (open)", "below c_L*: scan finds a break (conflict)",
                  "at or above c_L*: scan finds a break", "at or above c_L*: scan sees no break (low-trade basin, narrow "
                  "window or island)", "at or above c_L*: no eq. found (open)"], body)


def t_region_map() -> str:
    """Where the reversal holds in every found equilibrium, by r1 and rho."""
    rows = read("thresholds.csv")
    if rows is None:
        return MISSING
    r1s = sorted({num(r["r1"]) for r in rows})
    head = ["r1"] + [f"rho={rho}" for rho in RHOS]
    body = []
    for r1 in r1s:
        line = [f"{r1:g}"]
        for rho in RHOS:
            hit = [r for r in rows if r["rho"] == rho and abs(num(r["r1"]) - r1) < 1e-9]
            line.append(region_text(hit[0]) if hit else "")
        body.append(line)
    return table(head, body)


def t_candidate() -> str:
    """Theory's sufficient candidate c_L + c_H <= 2 B_r1(1/2), tested against c_L* from the solvers."""
    rows = read("thresholds.csv")
    if rows is None:
        return MISSING
    body = []
    for rho in RHOS:
        for r in rows:
            if r["rho"] != rho:
                continue
            r1 = num(r["r1"])
            if round(r1 * 10) % 5 != 0 and abs(r1 - 3.6) > 1e-9:
                continue
            cm, ch, cs = num(r["B_m"]), num(r["B_half"]), num(r["cL_star"])
            cand = 2.0 * ch - 6.0
            top = min(cand, ch)
            if top <= cm:
                verdict = "candidate range empty"
            elif r["binding"] in ("no-trade", "ceiling", "lowtrade") and abs(cs - cm) < 1e-9:
                verdict = f"fails: {r['binding']}"
            elif math.isnan(cs) or cs >= top - 1e-9:
                verdict = "safe"
            else:
                verdict = f"fails above {cs:.4f}"
            body.append([rho, f"{r1:g}", f4(cm), f4(cand), f4(cs), verdict])
    return table(["rho", "r1", "B(m)", "2B(1/2) - c_H", "c_L*", "candidate range"], body)


def t_klow() -> str:
    rows = read("klow.csv")
    if rows is None:
        return MISSING
    body = [[f"{num(r['r1']):g}", r["rho"], f"{num(r['cL']):.2f}", f"{num(r['DeltaT']):.4f}", f"{num(r['k_no_trade']):.4f}",
             f"{num(r['k_LT']):.4f}", f"{num(r['k_LT']) / num(r['k_no_trade']):.3f}", f"{num(r['q_edge']):.3f}",
             "yes" if num(r["k_paper"]) >= num(r["k_LT"]) else "no"] for r in rows]
    return table(["r1", "rho", "c_L", "Delta_T(r1)", "no-trade bound rho Delta_T/2", "k_LT (low-trade band starts)",
                  "k_LT / no-trade bound", "q* at the edge", "k = 0.02 inside the band"], body)


def t_forcing() -> str:
    rows = read("forcing_test.csv")
    if rows is None:
        return MISSING
    body = [[f"{num(r['cL']):.1f}", f"{num(r['k']):g}", f"{num(r['K_theory']):.5f}", r["consistent"], r["not_equilibrium"],
             f"{num(r['max_regret']):.1e}"] for r in rows]
    return table(["c_L", "k", "theory K(c_L)", "consistent random pools", "of them not an equilibrium",
                  "largest regret"], body)


def t_theorycheck() -> str:
    rows = read("theory_test.csv")
    if rows is None:
        return MISSING
    out = []
    knap = [r for r in rows if r["kind"].startswith("knap")]
    head = ["rho", "island E: theory", "mine, k = 0.005", "mine, k = 0.02", "island O_H: theory", "mine, k = 0.005",
            "mine, k = 0.02"]
    body = []
    for rho in sorted({r["rho"] for r in knap}, key=float):
        def pick(kind: str, k: str) -> dict:
            return next(r for r in knap if r["rho"] == rho and r["kind"] == kind and abs(num(r["k"]) - float(k)) < 1e-12)
        e5, e2, o5, o2 = pick("knap_E", "0.005"), pick("knap_E", "0.02"), pick("knap_O", "0.005"), pick("knap_O", "0.02")
        body.append([rho, f4(num(e5["theory"])), f4(num(e5["mine"])), f4(num(e2["mine"])), f4(num(o5["theory"])),
                     f4(num(o5["mine"])), f4(num(o2["mine"]))])
    out.append(table(head, body))
    st = [r for r in rows if r["kind"] == "starved"]
    body2 = [[f"{num(r['k']):g}", f"{num(r['theory']):.6f}", f"{num(r['mine']):.6f}", f"{num(r['diff']):.1e}"] for r in st]
    out.append("")
    out.append(table(["k (rho = 0.25)", "starved threshold: theory", "mine", "difference"], body2))
    return "\n".join(out)


def cs_without_lp(h: dict) -> float:
    """c_L* from the other mechanisms only (no exact-LP island threshold); nan when none is found."""
    cm = num(h["B_m"])
    vals = []
    if h["no_trade"] == "true" or h["ceiling"] == "true":
        vals.append(cm)
    for k in ("cL_partial", "cL_knapE", "cL_knapO"):
        v = num(h.get(k, ""))
        if not math.isnan(v):
            vals.append(v)
    return min(vals) if vals else math.nan


def t_lpregion() -> str:
    """Exact all-pool LP over the region, against the other solvers."""
    th = read("thresholds.csv")
    lp = read("lp_summary_region.csv")
    if th is None or lp is None:
        return MISSING
    body = []
    for rho in RHOS:
        tot = nof = hold = hold_ok = hold_conf = brk = brk_seen = 0
        for h in th:
            if h["rho"] != rho:
                continue
            cs = cs_without_lp(h)
            for r in lp:
                if r["rho"] != rho or abs(num(r["r"]) - num(h["r1"])) > 1e-9:
                    continue
                tot += 1
                if num(r["n_feasible"]) == 0:
                    nof += 1
                    continue
                c = num(r["cL"])
                lp_hold = r["reversal_all_LP"] == "true"
                if math.isnan(cs) or c < cs - 1e-9:
                    hold += 1
                    if lp_hold:
                        hold_ok += 1
                    else:
                        hold_conf += 1
                else:
                    brk += 1
                    brk_seen += int(not lp_hold)
        body.append([rho, str(tot), str(nof), str(hold), str(hold_ok), str(hold_conf), str(brk), str(brk_seen)])
    t1 = table(["rho", "LP points (12 per r1)", "no feasible order pair (no equilibrium of the lattice)",
                "other solvers say hold", "LP agrees: E and O_H stay above r0", "LP lowers E or O_H to the r0 value or below "
                "(island break the other solvers missed)", "other solvers say break",
                "LP also sees a break"], body)
    lt = read("lp_thresholds.csv")
    if lt is None:
        return t1
    rows = []
    for r in lt:
        if math.isnan(num(r["cL_lpexact"])):
            continue
        h = next((x for x in th if x["rho"] == r["rho"] and abs(num(x["r1"]) - num(r["r1"])) < 1e-9), None)
        if h is None:
            continue
        cs = cs_without_lp(h)
        if math.isnan(cs) or num(r["cL_lpexact"]) < cs - 1e-9:
            rows.append([r["rho"], f"{num(r['r1']):g}", f4(num(r["cL_lpexact"])), f4(cs), f4(num(r["E"])), f4(num(r["O_H"])),
                         f"({num(r['qH']):g}; {num(r['qL']):g})"])
    if rows:
        t1 += "\n\nPairs where the exact LP finds a confirmed island break below the other solvers' c_L*:\n\n"
        t1 += table(["rho", "r1", "c_L (exact LP)", "c_L* of the other solvers", "E at the break", "O_H at the break",
                     "orders"], rows)
    else:
        t1 += "\n\nNo pair has a confirmed island break below the other solvers' c_L*."
    return t1


def t_verify() -> str:
    body = []
    for name in ("eq_r3_rho0.25_verified.csv", "eq_r3_rho0.1_verified.csv", "eq_r3_rho0.5_verified.csv",
                 "eq_region_verified.csv", "lp_polished_verified.csv"):
        rows = read(name)
        if rows is None:
            continue
        chk = [r for r in rows if r.get("ver_accepted") not in ("unchecked", "", None)]
        acc = [r for r in chk if r["ver_accepted"] == "true"]
        mre = max([max(num(r["ver_regret_H"]), num(r["ver_regret_L"])) for r in chk], default=math.nan)
        mde = max([num(r["ver_dE"]) for r in chk], default=math.nan)
        body.append([name.replace("_verified.csv", ".csv"), str(len(rows)), str(len(chk)), str(len(acc)),
                     str(len(chk) - len(acc)), f"{mre:.1e}", f"{mde:.1e}"])
    if not body:
        return MISSING
    return table(["equilibrium file", "rows", "checked by quadrature", "accepted", "rejected", "max regret",
                  "max |E - E_quad|"], body)


def t_lp() -> str:
    rows = read("lp_summary_r3_rho0.25.csv")
    if rows is None:
        return MISSING
    picks = [2.3662, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 2.95, 3.0, 3.05, 3.1, 3.5, 4.0]
    body = []
    for c in picks:
        r = min(rows, key=lambda x: abs(num(x["cL"]) - c))
        if abs(num(r["cL"]) - c) > 0.0126:
            continue
        body.append([f"{num(r['cL']):.4f}", r["regime"], f"{r['n_feasible']} of {r['n_lattice']}",
                     f4(num(r["E_min_LP"])), f4(num(r["OH_min_LP"])),
                     f"({num(r['qH_at_Emin']):g}; {num(r['qL_at_Emin']):g})" if r["qH_at_Emin"] else "",
                     r["reversal_all_LP"]])
    return table(["c_L", "regime", "order pairs feasible", "lowest E over all pools", "lowest O_H over all pools",
                  "orders at lowest E", "reversal in all"], body)


def t_relaxed() -> str:
    rows = read("lp_relaxed.csv")
    if rows is None:
        return MISSING
    body = []
    for c in sorted({num(r["cL"]) for r in rows}):
        sub = [r for r in rows if abs(num(r["cL"]) - c) < 1e-9]
        far = [r for r in sub if r["near_full"] != "true"]
        pol = [r for r in far if r["polished"] == "true"]
        low = min([num(r["E_pol"]) for r in pol], default=math.nan)
        body.append([f"{c:.3f}", str(len(sub)), str(len(sub) - len(far)), str(len(far)), str(len(pol)), f4(low)])
    return table(["c_L", "order pairs epsilon-feasible", "near (1,-1)", "elsewhere", "elsewhere with an exact "
                  "equilibrium nearby", "lowest E there"], body)


def t_mixed() -> str:
    rows = read("mixed_audit.csv")
    if rows is None:
        return MISSING
    body = [[f"{num(r['cL']):g}", r["sampled"], r["multi_peak_H"], r["multi_peak_L"], r["max_peaks_H"],
             r["max_peaks_L"]] for r in rows]
    return table(["c_L", "consistent schedules sampled", "schedules where H has two local maxima",
                  "schedules where L has two local maxima", "most peaks H", "most peaks L"], body)


def t_collapse() -> str:
    rows = read("collapse.csv")
    if rows is None:
        return MISSING
    body = []
    keys = sorted({(num(r["r"]), num(r["cL"])) for r in rows})
    for r2, c in keys:
        sub = [r for r in rows if num(r["r"]) == r2 and abs(num(r["cL"]) - c) < 1e-9]
        e = [num(r["E"]) for r in sub]
        o = [num(r["O_H"]) for r in sub]
        rho = num(sub[0]["rho"])
        body.append([f"{r2:g}", f"{c:.4f}", sub[0]["regime"], str(len(sub)), f"{min(e):.4f} to {max(e):.4f}",
                     f"{min(o):.4f} to {max(o):.4f}", "yes" if max(e) <= rho + 1e-9 else "no",
                     "yes" if max(e) < rho - 1e-9 else "no"])
    return table(["r2", "c_L", "regime at r2", "equilibria", "E range", "O_H range", "E <= rho in all",
                  "E < rho in all"], body)


def t_kscan() -> str:
    rows = read("kscan.csv")
    if rows is None:
        return MISSING
    body = [[f"{num(r['cL']):.2f}", f4(num(r["tauL"])), f"{num(r['no_trade_k']):.4f}", f"{num(r['K_th']):.5f}",
             f"{num(r['k_S']):.5f}", f"{num(r['k_U']):.4f}", f"{num(r['k_R']):.4f}"] for r in rows]
    return table(["c_L", "tau_L", "no-trade bound rho Delta_T/2", "theory K(c_L)", "k_S (no starved eq. below)",
                  "k_U (unique trading outcome below)", "k_R (reversal below)"], body)


def t_rho() -> str:
    rows = read("rho_check.csv")
    if rows is None:
        return MISSING
    body = []
    for r in rows:
        body.append([r["rho"], f"{num(r['cL']):.4f}", r["n_eq"], f"{f4(num(r['E_min']))} to {f4(num(r['E_max']))}",
                     f"{f4(num(r['OH_min']))} to {f4(num(r['OH_max']))}", r["E_gt_rho_all"], r["E_gt_rho_any"],
                     r["reversal_all"]])
    return table(["rho", "c_L", "equilibria", "E range", "O_H range", "E > rho in all", "E > rho in some",
                  "reversal in all"], body)


TABLES = {
    "r0": t_r0,
    "sweep025": lambda: t_sweep("0.25", [2.30, 2.35, 2.366178511, 2.37, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 2.95, 2.975, 3.0,
                                         3.025, 3.1, 3.25, 3.5, 3.75, 4.0, 4.291666667]),
    "sweep01": lambda: t_sweep("0.1", [2.5, 3.0, 3.5, 4.0]),
    "sweep05": lambda: t_sweep("0.5", [2.4, 2.5, 3.0, 3.5]),
    "thresholds": t_thresholds,
    "thresholds_all": t_thresholds_all,
    "region_map": t_region_map,
    "region_check": t_region_check,
    "candidate": t_candidate,
    "lpregion": t_lpregion,
    "theorycheck": t_theorycheck,
    "klow": t_klow,
    "forcing": t_forcing,
    "verify": t_verify,
    "lp": t_lp,
    "relaxed": t_relaxed,
    "mixed": t_mixed,
    "collapse": t_collapse,
    "kscan": t_kscan,
    "rho": t_rho,
}


# ------------------------------------------------------------------------------------------------
# figure
# ------------------------------------------------------------------------------------------------

def figure() -> bool:
    sm = read("summary_r3_rho0.25.csv")
    th = read("thresholds.csv")
    lp = read("lp_summary_r3_rho0.25.csv")
    if sm is None:
        return False
    plt.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42, "font.size": 9, "axes.spines.top": False,
                         "axes.spines.right": False})
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(10.4, 4.0), constrained_layout=True)
    bhalf = 4.291666667
    rows = sorted([r for r in sm if num(r["cL"]) <= bhalf + 1e-6], key=lambda r: num(r["cL"]))

    def series(key: str) -> tuple[list[float], list[float]]:
        # a node is open when no equilibrium was found or some starts did not converge: the line breaks there
        x2, y2 = [], []
        for r in rows:
            open_node = r["n_eq"] == "0" or num(r["n_unresolved"]) > 0
            x2.append(num(r["cL"]))
            y2.append(math.nan if open_node else num(r[key]))
        return x2, y2
    for key, lab, col, ls in (("E_max", "E highest", "#1b4f72", "-"), ("E_min", "E lowest", "#1b4f72", "--"),
                              ("OH_max", "O_H highest", "#a04000", "-"), ("OH_min", "O_H lowest", "#a04000", "--")):
        x2, y2 = series(key)
        ax.plot(x2, y2, ls, color=col, lw=1.3, label=lab)
    if lp is not None:
        pts = sorted([(num(r["cL"]), num(r["E_min_LP"]), num(r["OH_min_LP"])) for r in lp
                      if num(r["cL"]) <= bhalf + 1e-6 and r["regime"] == "II"])
        ax.plot([p[0] for p in pts], [p[1] for p in pts], ":", color="#1b4f72", lw=1.0, label="E lowest, all pools (LP)")
        ax.plot([p[0] for p in pts], [p[2] for p in pts], ":", color="#a04000", lw=1.0, label="O_H lowest, all pools (LP)")
    ax.axhline(0.25, color="0.35", lw=0.8, ls="-.")
    ax.axhline(0.125, color="0.35", lw=0.8, ls="-.")
    ax.text(2.31, 0.258, r"$E(r_0)=\rho$", fontsize=8, color="0.25")
    ax.text(2.31, 0.133, r"$O_H(r_0)=\rho/2$", fontsize=8, color="0.25")
    for c, lab in ((2.366178511, "B(m)"), (2.9844, "partial"), (3.4607, "islands"), (bhalf, "B(1/2)")):
        ax.axvline(c, color="0.65", lw=0.7)
        ax.text(c - 0.015, 0.575, lab, rotation=90, fontsize=7.5, va="top", ha="right", color="0.35")
    ax.set_xlabel(r"$c_L$")
    ax.set_ylabel("entry and ownership")
    ax.set_xlim(2.3, 4.32)
    ax.set_ylim(0.0, 0.58)
    ax.legend(frameon=False, fontsize=7.2, loc="center right", ncol=1, bbox_to_anchor=(1.0, 0.30))
    ax.text(-0.12, 1.02, "(a)", transform=ax.transAxes, fontsize=11, fontweight="bold")
    if th is not None:
        cols = {"0.1": ("#117a65", "o", -0.02), "0.25": ("#1b4f72", "s", 0.0), "0.5": ("#922b21", "^", 0.02)}
        sub = sorted([r for r in th if r["rho"] == "0.25"], key=lambda r: num(r["r1"]))
        r1s = [num(r["r1"]) for r in sub]
        bx.fill_between(r1s, [num(r["B_m"]) for r in sub], [num(r["B_half"]) for r in sub], color="0.92", lw=0)
        bx.plot(r1s, [num(r["B_m"]) for r in sub], "-", color="0.35", lw=0.8)
        bx.plot(r1s, [num(r["B_half"]) for r in sub], "-", color="0.35", lw=0.8)
        for rho in RHOS:
            col, mk, off = cols[rho]
            sub = sorted([r for r in th if r["rho"] == rho], key=lambda r: num(r["r1"]))
            xs2, ys2, closed = [], [], []
            for r in sub:
                cs, cm, ch = num(r["cL_star"]), num(r["B_m"]), num(r["B_half"])
                xs2.append(num(r["r1"]) + off)
                if math.isnan(cs):
                    ys2.append(ch)
                    closed.append(False)          # holds on all of regime II
                else:
                    ys2.append(cs)
                    closed.append(True)
            bx.plot(xs2, ys2, "-", color=col, lw=0.9, alpha=0.8)
            bx.scatter([x for x, c in zip(xs2, closed) if c], [y for y, c in zip(ys2, closed) if c], marker=mk, s=16,
                       color=col, label=fr"$c_L^*$, $\rho={rho}$", zorder=3)
            bx.scatter([x for x, c in zip(xs2, closed) if not c], [y for y, c in zip(ys2, closed) if not c], marker=mk,
                       s=22, facecolors="none", edgecolors=col, zorder=3)
        bx.set_xlabel(r"$r_1$")
        bx.set_ylabel(r"$c_L$")
        bx.set_xlim(1.45, 3.65)
        bx.legend(frameon=False, fontsize=7.5, loc="upper left")
        bx.text(3.5, 4.05, "B(1/2)", fontsize=7.5, color="0.35", ha="right")
        bx.text(3.5, 2.40, "B(m)", fontsize=7.5, color="0.35", ha="right", va="top")
    bx.text(-0.12, 1.02, "(b)", transform=bx.transAxes, fontsize=11, fontweight="bold")
    fig.savefig(HERE / "fig_regime_ii.pdf")
    plt.close(fig)
    return True


# ------------------------------------------------------------------------------------------------
# output
# ------------------------------------------------------------------------------------------------

def splice(note: Path, blocks: dict[str, str]) -> int:
    text = note.read_text()
    n = 0
    for name, body in blocks.items():
        pat = re.compile(rf"(<!-- T:{name} -->\n).*?(\n<!-- /T:{name} -->)", re.S)
        if pat.search(text):
            text = pat.sub(lambda m: m.group(1) + body + m.group(2), text)
            n += 1
    note.write_text(text)
    return n


def main() -> None:
    blocks = {name: fn() for name, fn in TABLES.items()}
    with (HERE / "tables.txt").open("w") as fh:
        for name, body in blocks.items():
            fh.write(f"<!-- T:{name} -->\n{body}\n<!-- /T:{name} -->\n\n")
    ok = figure()
    note = HERE / "note.md"
    spliced = splice(note, blocks) if note.exists() else 0
    print(f"tables.txt written ({len(blocks)} tables); figure {'written' if ok else 'skipped'}; note blocks refreshed: {spliced}")


if __name__ == "__main__":
    main()
