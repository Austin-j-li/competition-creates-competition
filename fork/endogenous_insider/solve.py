"""Fork: deterministic preparation cost, endogenous insider.

Benchmark primitives (h, ell, p, b, k) with the cost floor removed: one preparation cost c,
no low-cost type. The challenger prepares iff its posterior gross profit covers c. On flows
where it would not prepare, the target is worth t_0 in both states, those flows pool at the
price t_0, and the investor's knowledge of theta is not information about the stock there.

This module solves; it writes CSV only. The renderer never solves. Status of every row is
"numerical diagnostic": pure-strategy fixed points of a best-response map on a grid, not
certified enclosures. The dead profile is checked analytically.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

# Benchmark primitives of Online Appendix C.0 with rho -> 0 and c_H -> c.
H, ELL, P, B, K = 10.0, 1.0, 0.5, 2.0, 0.02
C = 6.0
M_BOUND = 1.0 / (1.0 + math.exp(-2.0 / B))

X = np.linspace(-30.0, 30.0, 60001)
DX = float(X[1] - X[0])
S = np.round(np.linspace(-1.0, 1.0, 201), 3)


def f(z: np.ndarray) -> np.ndarray:
    return np.exp(-np.abs(z) / B) / (2.0 * B)


KERNEL = f(X[None, :] - S[:, None])  # KERNEL[i, j] = f(X_j - S_i)


def payoffs(r: float) -> dict:
    t0 = P * (1.0 - P / r)
    tH = r / 2.0 + P**2 / (2.0 * r)
    tL = ELL - (ELL**2 - P**2) / (2.0 * r)
    gH = H - tH
    gL = (ELL**2 - P**2) / (2.0 * r)
    return {"t0": t0, "tH": tH, "tL": tL, "gH": gH, "gL": gL, "DeltaT": tH - tL,
            "B_half": gL + 0.5 * (gH - gL), "B_M": gL + M_BOUND * (gH - gL),
            "tau": (C - gL) / (gH - gL)}


def schedule(r: float, qH: float, qL: float, cutoff_floor: float = -np.inf) -> dict:
    """Candidate continuation: orders (qH, qL); entry on {mu_X >= tau} intersected with [cutoff_floor, inf)."""
    pay = payoffs(r)
    aH, aL = f(X - qH), f(X - qL)
    mu = aH / (aH + aL)
    entry = (mu >= pay["tau"]) & (X >= cutoff_floor)
    e = entry.astype(float)
    pool = ~entry
    if pool.any():
        wH, wL = aH[pool].sum(), aL[pool].sum()
        mubar = wH / (wH + wL)
        pool_ok = pay["gL"] + mubar * (pay["gH"] - pay["gL"]) < C
    else:
        mubar, pool_ok = float("nan"), True
    price = pay["t0"] + e * (pay["tL"] - pay["t0"] + pay["DeltaT"] * mu)
    VH = pay["t0"] + e * (pay["tH"] - pay["t0"])
    VL = pay["t0"] + e * (pay["tL"] - pay["t0"])
    eH = float((e * aH).sum() * DX)
    eL = float((e * aL).sum() * DX)
    x_star = float(X[entry][0]) if entry.any() else float("inf")
    return {**pay, "mu": mu, "e": e, "P": price, "VH": VH, "VL": VL, "eH": eH, "eL": eL,
            "E": 0.5 * (eH + eL), "O_H": 0.5 * eH, "mubar": mubar, "pool_ok": pool_ok, "x_star": x_star}


def profit_curve(V: np.ndarray, Pr: np.ndarray) -> np.ndarray:
    return S * (KERNEL @ (V - Pr)) * DX - K * np.abs(S)


def best_response(V: np.ndarray, Pr: np.ndarray) -> tuple[float, float]:
    coarse = profit_curve(V, Pr)
    i = int(coarse.argmax())
    lo, hi = max(-1.0, S[i] - 0.01), min(1.0, S[i] + 0.01)
    fine = np.linspace(lo, hi, 41)
    gain = V - Pr
    vals = np.array([s * (f(X - s) * gain).sum() * DX - K * abs(s) for s in fine])
    j = int(vals.argmax())
    best, value = float(fine[j]), float(vals[j])
    if value <= 0.0:  # zero order is always available and earns exactly zero
        return 0.0, 0.0
    return best, value


def iterate(r: float, qH: float, qL: float, cutoff_floor: float = -np.inf,
            max_iter: int = 80, tol: float = 5e-4) -> dict | None:
    for _ in range(max_iter):
        sch = schedule(r, qH, qL, cutoff_floor)
        bH, uH = best_response(sch["VH"], sch["P"])
        bL, uL = best_response(sch["VL"], sch["P"])
        if abs(bH - qH) < tol and abs(bL - qL) < tol:
            if not sch["pool_ok"]:
                return None
            return {"qH": qH, "qL": qL, "U_H": uH, "U_L": uL, **{k: v for k, v in sch.items()
                    if k not in ("mu", "e", "P", "VH", "VL")}}
        qH, qL = bH, bL
    return None


def J_full(r: float) -> float:
    """Sharper existence statistic under full orders and the minimal pool: F_H(1) = F_L(1)."""
    sch = schedule(r, 1.0, -1.0)
    aH, aL = f(X - 1.0), f(X + 1.0)
    return float(sch["DeltaT"] * (sch["e"] * aH * aL / (aH + aL)).sum() * DX)


STARTS = [(1.0, -1.0), (1.0, -0.5), (1.0, 0.0), (0.5, -0.5), (0.25, -0.25)]


def solve_strength(r: float) -> list[dict]:
    pay = payoffs(r)
    rows = []
    dead_exists = pay["B_half"] < C
    rows.append({"r": r, "branch": "dead", "qH": 0.0, "qL": 0.0, "E": 0.0, "eH": 0.0, "eL": 0.0, "O_H": 0.0,
                 "U_H": 0.0, "U_L": 0.0, "tau": pay["tau"], "x_star": float("inf"), "mubar": 0.5,
                 "DeltaT": pay["DeltaT"], "B_half": pay["B_half"], "B_M": pay["B_M"], "J_full": J_full(r),
                 "exists": dead_exists, "status": "analytical" if dead_exists else "analytical (fails: B_r(1/2) >= c)"})
    found = []
    if pay["B_M"] >= C:
        for qH0, qL0 in STARTS:
            fp = iterate(r, qH0, qL0)
            if fp is None or fp["E"] <= 0.0:
                continue
            key = (round(fp["qH"], 2), round(fp["qL"], 2))
            if any(abs(key[0] - g[0]) < 0.015 and abs(key[1] - g[1]) < 0.015 for g in [(x["qH"], x["qL"]) for x in found]):
                continue
            found.append(fp)
    for fp in found:
        rows.append({"r": r, "branch": "live", **{k: fp[k] for k in ("qH", "qL", "E", "eH", "eL", "O_H", "U_H", "U_L",
                                                                    "tau", "x_star", "mubar", "DeltaT", "B_half", "B_M")},
                     "J_full": J_full(r), "exists": True, "status": "numerical diagnostic"})
    return rows


def r_grid() -> list[float]:
    pts = set()
    pts.update(np.round(np.arange(1.20, 3.72, 0.05), 3).tolist())
    pts.update(np.round(np.arange(1.50, 1.82, 0.01), 3).tolist())
    pts.update([1.2, 3.0, 3.6, 3.59, 3.5926, 3.5927])
    return sorted(pts)


def write_csv(path: Path, rows: list[dict]) -> None:
    keys = list(rows[0].keys())
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        for row in rows:
            w.writerow({k: (f"{v:.9g}" if isinstance(v, float) else v) for k, v in row.items()})


def main() -> None:
    branches = []
    for r in r_grid():
        branches.extend(solve_strength(r))
        print(f"r={r:.4f}: " + "; ".join(f"{row['branch']}({row['qH']:+.2f},{row['qL']:+.2f}) E={row['E']:.4f}"
                                         for row in branches if row["r"] == r and row["exists"]), flush=True)
    write_csv(HERE / "branches.csv", branches)

    # Cutoff family at the strong benchmark strength: the pool lower bound x' is the equilibrium object.
    r1 = 3.0
    base = schedule(r1, 1.0, -1.0)
    family = []
    for cutoff in np.round(np.arange(base["x_star"], 4.001, 0.05), 4):
        fp = iterate(r1, 1.0, -1.0, cutoff_floor=float(cutoff))
        if fp is None:
            family.append({"r": r1, "cutoff": float(cutoff), "qH": float("nan"), "qL": float("nan"), "E": float("nan"),
                           "U_H": float("nan"), "U_L": float("nan"), "mubar": float("nan"), "live": False,
                           "status": "unresolved (no fixed point from full-order start)"})
            continue
        live = fp["E"] > 0.0
        family.append({"r": r1, "cutoff": float(cutoff), "qH": fp["qH"], "qL": fp["qL"], "E": fp["E"],
                       "U_H": fp["U_H"], "U_L": fp["U_L"], "mubar": fp["mubar"], "live": live,
                       "status": "numerical diagnostic"})
        print(f"cutoff={cutoff:.3f}: q=({fp['qH']:+.2f},{fp['qL']:+.2f}) E={fp['E']:.4f} U_H={fp['U_H']:.4f} U_L={fp['U_L']:.4f}")
    write_csv(HERE / "cutoff_family.csv", family)

    # Thresholds. r(k) and r_C are the closed forms of Proposition A.4 with c_H -> c.
    def frak_r(d: float) -> float:
        return ELL + d + math.sqrt(d * d + 2.0 * ELL * d)
    Mb = M_BOUND
    r_C = ((Mb * H - C) + math.sqrt((Mb * H - C) ** 2 + Mb * ((1 - Mb) * ELL**2 - P**2))) / Mb
    live_rs = sorted({row["r"] for row in branches if row["branch"] == "live"})
    max_B_half = payoffs(1.0 + 1e-9)["B_half"]
    # sufficient full-order existence: k < (1 - 1/b) J_full(r); first grid r where it holds
    suff = sorted({row["r"] for row in branches if row["branch"] == "dead" and (1 - 1 / B) * row["J_full"] > K})
    thresholds = [
        {"boundary": "trading_impossible_sufficient", "value": frak_r(K), "definition": "r(k): Delta_T(r) = k; below it no order covers k in any equilibrium (Prop F1 iv)"},
        {"boundary": "preparation_ceiling", "value": r_C, "definition": "r_C: B_r(M) = c; above it no belief justifies preparation (Prop F1 iii)"},
        {"boundary": "dead_always_exists_check", "value": max_B_half, "definition": "sup_r B_r(1/2) on (ell, h); dead equilibrium exists at every r because this is below c"},
        {"boundary": "live_first_found", "value": live_rs[0] if live_rs else float("nan"), "definition": "smallest grid strength with a live pure fixed point (numerical diagnostic)"},
        {"boundary": "live_last_found", "value": live_rs[-1] if live_rs else float("nan"), "definition": "largest grid strength with a live pure fixed point (numerical diagnostic)"},
        {"boundary": "full_orders_sufficient_first", "value": suff[0] if suff else float("nan"), "definition": "smallest grid strength with k < (1-1/b) J_full(r) (Prop F2 c sufficient test)"},
        {"boundary": "m", "value": 1 - M_BOUND, "definition": "lower posterior bound"},
        {"boundary": "M", "value": M_BOUND, "definition": "upper posterior bound"},
    ]
    write_csv(HERE / "thresholds.csv", thresholds)
    print("done")


if __name__ == "__main__":
    main()
