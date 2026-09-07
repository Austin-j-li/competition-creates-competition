"""Cross-check of the handout explorer's closed forms against the validated CSV rows.

Shared formula block (keep byte-identical with the header comment in handout/explorer.js):

    t_0 = p (1 - p/r);  t_H = r/2 + p^2/(2r);  t_L = ell - (ell^2 - p^2)/(2r)
    g_H = h - r/2 - p^2/(2r);  g_L = (ell^2 - p^2)/(2r);  Delta_T = (r - ell)^2/(2r)
    m = 1/(1 + exp(2/b));  M = 1 - m;  B(mu) = g_L + mu (g_H - g_L)
    tau = (c_H - g_L)/(g_H - g_L)
      c_H > B(M): E = rho, O_H = rho/2, x* = +inf, alpha_H = alpha_L = 0
      c_H <= B(m): x* = -inf, alpha_H = alpha_L = 1, E = 1, O_H = 1/2
      otherwise  : x* = (b/2) log(tau/(1-tau)); alpha_H = S_Laplace(x*-1); alpha_L = S_Laplace(x*+1)
                   E = rho + (1-rho)/2 (alpha_H + alpha_L);  O_H = (rho + (1-rho) alpha_H)/2
    chips: A1 = B(m) - c_L; A2a = c_H - B(1/2); A2b = B(M) - c_H;
           A3_no_trade = k - Delta_T; A3_full = (1 - 1/b) rho m Delta_T - k
    rr(d) = ell + d + sqrt(d^2 + 2 ell d); r_k = rr(k); r_N = rr(2k/rho); r_U = rr(k/((1-1/b) rho m))
    r_C = (M h - c_H + sqrt((M h - c_H)^2 + M ((1-M) ell^2 - p^2))) / M

Sources: paper/main.md eq. (4), (7), (12), conditions (A1) to (A3), and (A.1), (A.2).
The Python side evaluates in float64, the same arithmetic the browser uses, so agreement to
1e-9 with the CSV (produced by the numerics layer) is the statement being checked.
Stdlib only; no imports from numerics/.
"""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOL = 1e-9

INPUT_NAMES = {
    "h": "base_h", "ell": "base_ell", "p": "base_p", "rho": "base_rho", "c_L": "base_c_low",
    "c_H": "base_c_high", "b": "base_b", "k": "base_k", "r_weak": "base_r_weak",
    "r_strong": "base_r_strong", "r_collapse": "base_r_collapse",
}


def read_rows(rel: str) -> list[dict]:
    with open(ROOT / rel, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def benchmark_inputs() -> dict:
    reg = {r["name"]: r["value"] for r in read_rows("numerics/quantity_registry.csv")}
    return {key: float(reg[name]) for key, name in INPUT_NAMES.items()}


def closed_forms(P: dict, r: float) -> dict:
    h, ell, p, rho, c_L, c_H, b, k = (P[x] for x in ("h", "ell", "p", "rho", "c_L", "c_H", "b", "k"))
    out = {"r": r, "in_domain": p < ell < r < h}
    t_0 = p * (1 - p / r)
    t_H = r / 2 + p * p / (2 * r)
    t_L = ell - (ell * ell - p * p) / (2 * r)
    g_H = h - r / 2 - p * p / (2 * r)
    g_L = (ell * ell - p * p) / (2 * r)
    Delta_T = (r - ell) ** 2 / (2 * r)
    m = 1 / (1 + math.exp(2 / b))
    M = 1 - m

    def B(mu: float) -> float:
        return g_L + mu * (g_H - g_L)

    tau = (c_H - g_L) / (g_H - g_L)
    if c_H > B(M):
        x_star, alpha_H, alpha_L = math.inf, 0.0, 0.0
    elif c_H <= B(m):
        x_star, alpha_H, alpha_L = -math.inf, 1.0, 1.0
    else:
        x_star = (b / 2) * math.log(tau / (1 - tau))
        alpha_H = 1 - math.exp((x_star - 1) / b) / 2 if x_star <= 1 else math.exp(-(x_star - 1) / b) / 2
        alpha_L = 1 - math.exp((x_star + 1) / b) / 2 if x_star <= -1 else math.exp(-(x_star + 1) / b) / 2
    E = rho + (1 - rho) / 2 * (alpha_H + alpha_L)
    O_H = (rho + (1 - rho) * alpha_H) / 2

    def rr(d: float) -> float:
        return ell + d + math.sqrt(d * d + 2 * ell * d)

    r_k = rr(k)
    r_N = rr(2 * k / rho)
    r_U = rr(k / ((1 - 1 / b) * rho * m))
    disc = (M * h - c_H) ** 2 + M * ((1 - M) * ell * ell - p * p)
    r_C = (M * h - c_H + math.sqrt(disc)) / M if disc >= 0 else math.nan
    out.update({
        "t_0": t_0, "t_H": t_H, "t_L": t_L, "g_H": g_H, "g_L": g_L, "Delta_T": Delta_T,
        "m": m, "M": M, "B_m": B(m), "B_prior": B(0.5), "B_M": B(M),
        "tau": tau, "x_star": x_star, "alpha_H": alpha_H, "alpha_L": alpha_L, "E": E, "O_H": O_H,
        "A1": B(m) - c_L, "A2a": c_H - B(0.5), "A2b": B(M) - c_H,
        "A3_no_trade": k - Delta_T, "A3_full": (1 - 1 / b) * rho * m * Delta_T - k,
        "r_k": r_k, "r_N": r_N, "r_U": r_U, "r_C": r_C,
    })
    return out


def as_number(s: str) -> float:
    t = s.strip().lower()
    if t in ("inf", "unattainable"):
        return math.inf
    if t in ("-inf", "always"):
        return -math.inf
    return float(s)


def close(a: float, b: float) -> tuple[bool, float]:
    if math.isinf(a) or math.isinf(b):
        return (a == b, 0.0 if a == b else math.inf)
    d = abs(a - b)
    return (d <= TOL, d)


def run(verbose: bool = True) -> tuple[bool, list[dict]]:
    P = benchmark_inputs()
    comparisons: list[dict] = []

    def compare(group: str, name: str, ours: float, theirs: float) -> None:
        ok, d = close(ours, theirs)
        comparisons.append({"group": group, "name": name, "ours": ours, "csv": theirs, "diff": d, "ok": ok})

    # tables/auction_primitives.csv, parameter_set=base at the three declared strengths
    prim = [r for r in read_rows("tables/auction_primitives.csv") if r["parameter_set"] == "base"]
    for row in prim:
        cf = closed_forms(P, float(row["r"]))
        for col in ("t_0", "t_H", "t_L", "g_H", "g_L", "Delta_T", "B_m", "B_prior", "B_M"):
            compare("auction_primitives", f"r={row['r']} {col}", cf[col], as_number(row[col]))

    # tables/equilibrium_controls.csv: full-order rows (feedback at r_strong, r_collapse; frozen at r_weak)
    ctrl = [r for r in read_rows("tables/equilibrium_controls.csv")
            if r["parameter_set"] == "base" and r["noise"] == "Laplace" and r["cost_law"] == "atoms" and r["accepted"] == "true"]
    wanted = {("feedback", str(P["r_strong"]).rstrip("0").rstrip(".")), ("feedback", str(P["r_collapse"]).rstrip("0").rstrip(".")),
              ("frozen", str(P["r_weak"]).rstrip("0").rstrip("."))}
    seen = set()
    for row in ctrl:
        key = (row["experiment"], row["r"])
        if key not in wanted:
            continue
        seen.add(key)
        cf = closed_forms(P, float(row["r"]))
        cols = ("E", "O_H", "tau", "x_star") if row["experiment"] == "feedback" else ("E", "O_H", "x_star")
        for col in cols:
            compare("equilibrium_controls", f"{row['experiment']} r={row['r']} {col}", cf[col], as_number(row[col]))
    for key in wanted - seen:
        comparisons.append({"group": "equilibrium_controls", "name": f"missing row {key}", "ours": math.nan, "csv": math.nan, "diff": math.inf, "ok": False})

    # tables/extensions.csv: the five strict margins of Proposition 2 at (r_weak, r_strong)
    ext = [r for r in read_rows("tables/extensions.csv")
           if r["parameter_set"] == "base" and r["noise"] == "Laplace" and r["cost_law"] == "atoms"]
    for row in ext:
        weak = closed_forms(P, float(row["r_weak"]))
        strong = closed_forms(P, float(row["r_strong"]))
        pairs = (("zeta_L", strong["A1"]), ("zeta_H0", weak["A2a"]), ("zeta_H1", strong["A2b"]),
                 ("zeta_0", weak["A3_no_trade"]), ("zeta_1", strong["A3_full"]))
        for col, ours in pairs:
            compare("extensions", col, ours, as_number(row[col]))

    # numerics/thresholds.csv: boundaries of Proposition A.4 and the posterior bounds
    thr = {r["boundary"]: r for r in read_rows("numerics/thresholds.csv")}
    cf = closed_forms(P, P["r_strong"])
    for boundary, col in (("pooling_unique_sufficient", "r_k"), ("pooling_existence", "r_N"),
                          ("full_orders_unique_sufficient", "r_U"), ("high_cost_ceiling", "r_C"), ("m", "m"), ("M", "M")):
        if boundary in thr:
            compare("thresholds", boundary, cf[col], as_number(thr[boundary]["value"]))
        else:
            comparisons.append({"group": "thresholds", "name": f"missing {boundary}", "ours": math.nan, "csv": math.nan, "diff": math.inf, "ok": False})

    ok = all(c["ok"] for c in comparisons)
    if verbose:
        for group in ("auction_primitives", "equilibrium_controls", "extensions", "thresholds"):
            items = [c for c in comparisons if c["group"] == group]
            worst = max((c["diff"] for c in items), default=0.0)
            good = all(c["ok"] for c in items)
            print(("PASS " if good else "FAIL ") + f"crosscheck {group}: {len(items)} comparisons, worst |diff| {worst:.2e}")
            for c in items:
                if not c["ok"]:
                    print(f"      {c['name']}: closed form {c['ours']!r} vs csv {c['csv']!r}")
        print(("PASS " if ok else "FAIL ") + f"crosscheck total: {len(comparisons)} comparisons at tolerance {TOL:g}")
    return ok, comparisons


def main() -> int:
    ok, _ = run(verbose=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
