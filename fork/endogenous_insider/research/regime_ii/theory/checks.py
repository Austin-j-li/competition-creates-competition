"""Numerical checks for the theory note. Every output is a numerical diagnostic, not a proof.

1. checks_roc.csv: ROC bounds of Lemma R.5 on random correctly signed mixed orders and random unions of
   intervals N: Pr(N|L) <= beta_2(Pr(N|H)), Pr(Z-s in N) <= beta_{1+s}(Pr(N|H)), Pr(Z+s in N) <= beta_1(Pr(N|H)).
2. checks_forcing.csv: at k = 0.008 and c_L in {2.4, 2.5}, where k <= K(c_L), full orders are the best response
   to every consistent schedule built from pure orders on a grid and a half-line pool (Proposition R.6).
3. checks_forcing_map.csv: the pure-schedule forcing level across c_L (Section 3.2, remark 2).
4. checks_island.csv: investor test at k = 0.02 against the bathtub worst pools (Proposition R.7).
5. checks_break.csv: forcing level near c_L = 2B(1/2) - c_H with shorts just below v_H (Lemma R.11).
"""
from __future__ import annotations

import csv
import math
from dataclasses import replace

import numpy as np

import formulas as fm

PRM = fm.Params()


def F(z: np.ndarray, b: float) -> np.ndarray:
    return np.where(z <= 0, 0.5 * np.exp(np.minimum(z, 0) / b), 1 - 0.5 * np.exp(-np.maximum(z, 0) / b))


def Finv(u: float, b: float) -> float:
    return b * math.log(2 * u) if u <= 0.5 else -b * math.log(2 * (1 - u))


def beta(u: float, d: float, b: float) -> float:
    if u <= 0.0:
        return 0.0
    if u >= 1.0:
        return 1.0
    return float(F(np.array(Finv(u, b) + d), b))


def prob_union(q: float, ivs: list[tuple[float, float]], b: float) -> float:
    return float(sum(F(np.array(hi - q), b) - F(np.array(lo - q), b) for lo, hi in ivs))


def roc_rows(n: int = 4000, seed: int = 7) -> list[dict]:
    rng = np.random.default_rng(seed)
    b = PRM.b
    worst = {"L_vs_H": -1.0, "dev_short": -1.0, "dev_buy": -1.0}
    for _ in range(n):
        kH, kL = rng.integers(1, 4), rng.integers(1, 4)
        qH, wH = rng.uniform(0, 1, kH), rng.dirichlet(np.ones(kH))
        qL, wL = -rng.uniform(0, 1, kL), rng.dirichlet(np.ones(kL))
        cuts = np.sort(rng.uniform(-6, 6, 2 * rng.integers(1, 4)))
        ivs = [(-math.inf if i == 0 and rng.random() < 0.5 else cuts[2 * i], cuts[2 * i + 1])
               for i in range(len(cuts) // 2)]
        PH = sum(w * prob_union(q, ivs, b) for q, w in zip(qH, wH))
        PL = sum(w * prob_union(q, ivs, b) for q, w in zip(qL, wL))
        s = rng.uniform(0, 1)
        worst["L_vs_H"] = max(worst["L_vs_H"], PL - beta(PH, 2.0, b))
        worst["dev_short"] = max(worst["dev_short"], prob_union(-s, ivs, b) - beta(PH, 1.0 + s, b))
        worst["dev_buy"] = max(worst["dev_buy"], prob_union(s, ivs, b) - beta(PH, 1.0, b))
    return [{"check": key, "max_violation": val, "draws": n} for key, val in worst.items()]


def forcing_rows() -> list[dict]:
    x = np.linspace(-40, 40, 80001)
    dx = x[1] - x[0]
    f = lambda z: np.exp(-np.abs(z) / PRM.b) / (2 * PRM.b)
    S = np.linspace(0, 1, 201)
    KH = f(x[None, :] - S[:, None])
    KL = f(x[None, :] + S[:, None])
    out = []
    for cL in (2.4, 2.5):
        prm = replace(PRM, k=0.008, c_L=cL)
        lv = fm.levels(prm)
        K = fm.forcing_bound(prm, lv)
        n_sched, n_bad, min_slope = 0, 0, math.inf
        for qH in np.linspace(0.0, 1.0, 11):
            for qL in np.linspace(-1.0, 0.0, 11):
                if qH == 0.0 and qL == 0.0:
                    continue
                aH, aL = f(x - qH), f(x - qL)
                mu = aH / (aH + aL)
                phi = prm.rho * (mu >= lv.tau_L) + (1 - prm.rho) * (mu >= lv.tau_H)
                for cut in np.concatenate(([-np.inf], np.linspace(-3, 8, 45))):
                    N = (phi == 0) | (x < cut)
                    if N.any():
                        mb = aH[N].sum() / (aH[N].sum() + aL[N].sum())
                        if not mb < lv.tau_L:
                            continue
                    e = np.where(N, 0.0, phi)
                    UH = S * (KH @ (e * lv.DeltaT * (1 - mu))) * dx - prm.k * S
                    UL = S * (KL @ (e * lv.DeltaT * mu)) * dx - prm.k * S
                    n_sched += 1
                    slope = min(np.diff(UH).min(), np.diff(UL).min()) / (S[1] - S[0])
                    min_slope = min(min_slope, slope)
                    if UH.argmax() != len(S) - 1 or UL.argmax() != len(S) - 1:
                        n_bad += 1
        out.append({"c_L": cL, "k": prm.k, "K_force": K, "schedules": n_sched, "not_full_best_response": n_bad,
                    "min_marginal_payoff": min_slope})
    return out


def write(path: str, rows: list[dict]) -> None:
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.6g}" if isinstance(v, float) else v) for k, v in r.items()})




def forcing_map(cLs: tuple[float, ...] = (2.37, 2.45, 2.55, 2.57, 2.58, 2.59, 2.60, 2.62, 2.65, 2.75, 2.85,
                                          2.95, 3.05),
                n_q: int = 21, n_cut: int = 61) -> list[dict]:
    """Pure-schedule forcing threshold: inf over consistent schedules of min_s d/ds[s F_theta(s)].

    Schedules: pure orders (q_H, q_L) on an n_q x n_q grid of [0,1] x [-1,0], pools Z_0 or Z_0 plus a
    half-line (-inf, cut). If k is below the reported value, full orders are the unique best response to
    every such schedule. Numerical diagnostic; islands and mixed orders are not covered.
    """
    x = np.linspace(-20, 20, 20001)
    dx = x[1] - x[0]
    f = lambda z: np.exp(-np.abs(z) / PRM.b) / (2 * PRM.b)
    S = np.linspace(0, 1, 101)
    KH = f(x[None, :] - S[:, None])
    KL = f(x[None, :] + S[:, None])
    out = []
    for cL in cLs:
        prm = replace(PRM, c_L=cL)
        lv = fm.levels(prm)
        best = (math.inf, None)
        for qH in np.linspace(0.0, 1.0, n_q):
            for qL in np.linspace(-1.0, 0.0, n_q):
                if qH == 0.0 and qL == 0.0:
                    continue
                aH, aL = f(x - qH), f(x - qL)
                mu = aH / (aH + aL)
                phi = prm.rho * (mu >= lv.tau_L) + (1 - prm.rho) * (mu >= lv.tau_H)
                for cut in np.concatenate(([-np.inf], np.linspace(-3, 6, n_cut))):
                    N = (phi == 0) | (x < cut)
                    if N.any() and not aH[N].sum() / (aH[N].sum() + aL[N].sum()) < lv.tau_L:
                        continue
                    e = np.where(N, 0.0, phi)
                    VH = S * (KH @ (e * lv.DeltaT * (1 - mu))) * dx
                    VL = S * (KL @ (e * lv.DeltaT * mu)) * dx
                    slope = min(np.diff(VH).min(), np.diff(VL).min()) / (S[1] - S[0])
                    if slope < best[0]:
                        best = (slope, (float(qH), float(qL), float(cut)))
        out.append({"c_L": cL, "K_force": fm.forcing_bound(prm, lv), "k_pure": best[0],
                    "worst_qH": best[1][0], "worst_qL": best[1][1], "worst_cut": best[1][2]})
    return out


def island_rows(cLs: tuple[float, ...] = (2.5, 3.0, 3.3, 3.45, 3.5), k: float = 0.02, slack: float = 0.995) -> list[dict]:
    """Investor check at k = 0.02 against the bathtub worst pool (Proposition R.7) under full orders.

    The pool is Z_0, a mid band [z0, y1), an island [x_star, y2), and the plateau share placed as a far tail
    [x_far, inf). The bathtub budget is scaled by `slack` < 1 so that the pool belief is strictly below tau_L.
    Grid best responses: numerical diagnostic.
    """
    x = np.linspace(-40, 40, 160001)
    dx = x[1] - x[0]
    f = lambda z: np.exp(-np.abs(z) / PRM.b) / (2 * PRM.b)
    S = np.linspace(0, 1, 201)
    aH, aL = f(x - 1.0), f(x + 1.0)
    mu = aH / (aH + aL)
    out = []
    for cL in cLs:
        prm = replace(PRM, k=k, c_L=cL)
        lv = fm.levels(prm)
        ks = fm.knapsack(replace(prm), lv, "E")
        # rebuild the bathtub set at a slightly smaller budget by bisection on the threshold
        lo, hi = 0.0, ks.theta
        target = ks.budget * slack
        def pool(th: float, frac: float) -> np.ndarray:
            m1 = min(lv.tau_L + prm.rho * th, lv.tau_H)
            y1 = lv.x_star if m1 >= lv.tau_H else 0.5 * prm.b * math.log(m1 / (1 - m1))
            m2 = lv.tau_L + th
            y2 = lv.x_star if m2 < lv.tau_H else (1.0 if m2 >= lv.M else 0.5 * prm.b * math.log(m2 / (1 - m2)))
            N = (x < y1) | ((x >= lv.x_star) & (x < y2))
            if frac > 0:
                N = N | (x >= 1.0 - prm.b * math.log(frac))
            return N
        def cost(N: np.ndarray) -> float:
            return float((((mu - lv.tau_L) * 0.5 * (aH + aL))[N]).sum() * dx)
        # pick frac or theta to meet the slack budget
        if ks.plateau_frac > 0:
            fl, fh = 0.0, ks.plateau_frac
            for _ in range(60):
                fmid = 0.5 * (fl + fh)
                if cost(pool(ks.theta, fmid)) < 0:
                    fl = fmid
                else:
                    fh = fmid
            N = pool(ks.theta, fl)
        else:
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if cost(pool(mid, 0.0)) < 0:
                    lo = mid
                else:
                    hi = mid
            N = pool(lo, 0.0)
        phi = prm.rho * (mu >= lv.tau_L) + (1 - prm.rho) * (mu >= lv.tau_H)
        e = np.where(N, 0.0, phi)
        UH = S * (f(x[None, :] - S[:, None]) @ (e * lv.DeltaT * (1 - mu))) * dx - k * S
        UL = S * (f(x[None, :] + S[:, None]) @ (e * lv.DeltaT * mu)) * dx - k * S
        mb = float(aH[N].sum() / (aH[N].sum() + aL[N].sum()))
        out.append({"c_L": cL, "k": k, "tau_L": lv.tau_L, "pool_belief": mb, "E": float((e * 0.5 * (aH + aL)).sum() * dx),
                    "eH": float((e * aH).sum() * dx), "inf_E_bathtub": ks.inf_value,
                    "full_best_H": bool(UH.argmax() == len(S) - 1), "full_best_L": bool(UL.argmax() == len(S) - 1),
                    "min_marginal_H": float(np.diff(UH).min() / (S[1] - S[0])),
                    "min_marginal_L": float(np.diff(UL).min() / (S[1] - S[0]))})
    return out


def break_rows(cLs: tuple[float, ...] = (2.58, 2.59, 2.60, 2.62)) -> list[dict]:
    """Forcing level near the break c_L = 2B(1/2) - c_H, using q_H = 1 and shorts just below v_H.

    Same statistic as forcing_map, restricted to v in [0.70, v_H) on a fine grid and half-line pools.
    Numerical diagnostic.
    """
    x = np.linspace(-20, 20, 20001)
    dx = x[1] - x[0]
    f = lambda z: np.exp(-np.abs(z) / PRM.b) / (2 * PRM.b)
    S = np.linspace(0, 1, 101)
    KH = f(x[None, :] - S[:, None])
    KL = f(x[None, :] + S[:, None])
    out = []
    for cL in cLs:
        prm = replace(PRM, c_L=cL)
        lv = fm.levels(prm)
        vh = fm.v_H(prm, lv)
        best = (math.inf, float("nan"), float("nan"))
        for v in np.linspace(0.70, vh * (1 - 1e-6), 40):
            aH, aL = f(x - 1.0), f(x + v)
            mu = aH / (aH + aL)
            phi = prm.rho * (mu >= lv.tau_L) + (1 - prm.rho) * (mu >= lv.tau_H)
            for cut in np.concatenate(([-np.inf], np.linspace(-1, 3, 81))):
                N = (phi == 0) | (x < cut)
                if not N.any() or not aH[N].sum() / (aH[N].sum() + aL[N].sum()) < lv.tau_L:
                    continue
                e = np.where(N, 0.0, phi)
                VH = S * (KH @ (e * lv.DeltaT * (1 - mu))) * dx
                VL = S * (KL @ (e * lv.DeltaT * mu)) * dx
                sl = min(np.diff(VH).min(), np.diff(VL).min()) / (S[1] - S[0])
                if sl < best[0]:
                    best = (float(sl), float(v), float(cut))
        out.append({"c_L": cL, "tau_L": lv.tau_L, "pooled_subvH_schedule_exists": math.isfinite(best[0]),
                    "k_pure_subvH": best[0], "worst_v": best[1], "worst_cut": best[2]})
    return out


if __name__ == "__main__":
    write("checks_roc.csv", roc_rows())
    write("checks_forcing.csv", forcing_rows())
    write("checks_forcing_map.csv", forcing_map())
    write("checks_island.csv", island_rows())
    write("checks_break.csv", break_rows())
