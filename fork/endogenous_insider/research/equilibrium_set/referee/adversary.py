"""Adversarial search (referee scratch): live equilibria with an interior or mixed high-type order.

Necessary conditions for a pure live equilibrium (q, -z) with q < 1 and z < 1 both interior
(derived in review.md): F_H(q) = F_L(z) = k b/(b - z) by Lemma ES.5, and the high type's first-order
condition with |F_H'| <= F_H/b gives z <= q. Entry needs q + z >= 1 + n(r).

The search uses entry sets the note's scans did not use: sets bounded above, A = [L, y], and
two-piece sets [x*, y1] U [y1 + gap, inf). For each (r, q, z, member) the low type's condition
C_A = k e^{z/b}/(1 - z/b) fixes the free end (Lemma ES.4(a)); then both global best responses are
computed on a grid of magnitudes. A pure equilibrium needs the high type's best response at q.
Grid integrals (trapezoid on a fine flow grid). Prints a summary; writes adversary.csv and
adversary_mixed.csv. Status: numerical diagnostic.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
H_, ELL, P_, B, K, C = 10.0, 1.0, 0.5, 2.0, 0.02, 6.0
X = np.linspace(-15.0, 50.0, 26001)
DX = X[1] - X[0]
S = np.linspace(0.0, 1.0, 201)
KER_H = np.exp(-np.abs(X[None, :] - S[:, None]) / B) / (2 * B)    # f(x - s)
KER_L = np.exp(-np.abs(X[None, :] + S[:, None]) / B) / (2 * B)    # f(x + s)
F0 = np.exp(-np.abs(X) / B) / (2 * B)


def acq(r: float) -> tuple[float, float]:
    tH = r / 2 + P_ ** 2 / (2 * r)
    tL = ELL - (ELL ** 2 - P_ ** 2) / (2 * r)
    gH = H_ - tH
    gL = (ELL ** 2 - P_ ** 2) / (2 * r)
    return tH - tL, (C - gL) / (gH - gL)


def mu_mix(qs, ws, zs, vs) -> np.ndarray:
    aH = sum(w * np.exp(-np.abs(X - q) / B) for q, w in zip(qs, ws))
    aL = sum(v * np.exp(-np.abs(X + z) / B) for z, v in zip(zs, vs))
    return aH / (aH + aL)


def curves(dT: float, mu: np.ndarray, ind: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    wH = ind * dT * (1 - mu)
    wL = ind * dT * mu
    FH = (KER_H * wH[None, :]).sum(axis=1) * DX
    FL = (KER_L * wL[None, :]).sum(axis=1) * DX
    return S * (FH - K), S * (FL - K)


def br(u: np.ndarray) -> float:
    return float(S[int(u.argmax())]) if u.max() > 0 else 0.0


def search(r: float) -> list[dict]:
    dT, tau = acq(r)
    n = B * math.log(tau / (1 - tau)) - 1
    rows = []
    for q in np.linspace(0.30, 0.99, 24):
        for z in np.linspace(0.04, 0.99, 20):
            if q + z < 1 + n:
                continue
            mu = mu_mix([q], [1.0], [z], [1.0])
            live = mu >= tau
            if not live.any():
                continue
            ixs = int(np.argmax(live))
            target = K * math.exp(z / B) / (1 - z / B) / dT      # required int_A f mu
            cf = np.concatenate([[0.0], np.cumsum(F0[:-1] * mu[:-1]) * DX])   # int_{X0}^{x} f mu
            total = cf[-1]
            members = []
            for L in (0.0, 0.1, 0.3, 0.6):
                iL = int(np.searchsorted(X, X[ixs] + L))
                need = cf[iL] + target
                if need > total:
                    continue
                iy = int(np.searchsorted(cf, need))
                members.append((f"interval L={L}", (X >= X[iL]) & (X <= X[iy])))
            for gap in (0.2, 0.6, 1.5):
                ig = int(round(gap / DX))
                idx = np.arange(ixs, len(X) - ig)
                Cy = (cf[idx] - cf[ixs]) + (total - cf[idx + ig])
                sgn = np.sign(Cy - target)
                for j in np.where(np.diff(sgn) != 0)[0][:3]:
                    y1 = idx[j]
                    members.append((f"two-piece gap={gap}",
                                    ((X >= X[ixs]) & (X <= X[y1])) | (X >= X[y1 + ig])))
            # the note's cutoff family, for comparison
            if total - cf[ixs] >= target:
                ic = int(np.searchsorted(-(total - cf), -target))  # total - cf decreasing
                members.append(("cutoff", X >= X[max(ic - 1, ixs)]))
            for lab, ind in members:
                uH, uL = curves(dT, mu, ind.astype(float))
                sH, sL = br(uH), br(uL)
                rows.append({"r": r, "q": float(q), "z": float(z), "member": lab,
                             "low_BR": sL, "low_BR_minus_z": sL - float(z), "high_BR": sH,
                             "high_BR_minus_q": sH - float(q), "high_interior": bool(0 < sH < 1),
                             "U_H_interior_max_minus_corners": float(uH[1:-1].max() - max(uH[-1], 0.0))})
    return rows


def mixed_search(r: float) -> list[dict]:
    """Two-point high-type mixtures {s1, 1} against pure low orders, minimal pool and bounded sets.
    A mixed equilibrium needs U_H(s1) = U_H(1) = max U_H."""
    dT, tau = acq(r)
    rows = []
    for s1 in np.linspace(0.2, 0.95, 16):
        for lam in (0.2, 0.5, 0.8):
            for z in np.linspace(0.1, 1.0, 19):
                mu = mu_mix([s1, 1.0], [1 - lam, lam], [z], [1.0])
                live = mu >= tau
                if not live.any():
                    continue
                xs = X[live][0]
                for y in (xs + 0.3, xs + 1.0, 50.0):
                    ind = ((X >= xs) & (X <= y)).astype(float)
                    uH, uL = curves(dT, mu, ind)
                    rows.append({"r": r, "s1": float(s1), "lam": lam, "z": float(z), "y": float(y),
                                 "interior_max_minus_corners": float(uH[1:-1].max() - max(uH[-1], 0.0)),
                                 "high_BR": br(uH), "low_BR": br(uL)})
    return rows


def main() -> None:
    rows = []
    for r in (1.55, 1.62, 1.65, 1.7, 2.0, 2.5, 3.0, 3.5):
        rr = search(r)
        rows += rr
        n_int = sum(x["high_interior"] for x in rr)
        worst = max((x["U_H_interior_max_minus_corners"] for x in rr), default=float("nan"))
        okL = max((abs(x["low_BR_minus_z"]) for x in rr), default=float("nan"))
        print(f"r={r}: schedules {len(rr)}, high BR interior {n_int}, max(interior - corners) {worst:.3e},"
              f" max |low BR - z| {okL:.3f}", flush=True)
    with (HERE / "adversary.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    mrows = []
    for r in (1.62, 1.65, 2.0, 3.0):
        mr = mixed_search(r)
        mrows += mr
        best = max(x["interior_max_minus_corners"] for x in mr)
        n_int = sum(0 < x["high_BR"] < 1 for x in mr)
        print(f"r={r}: mixed schedules {len(mr)}, interior high BR {n_int}, max(interior - corners) {best:.3e}",
              flush=True)
    with (HERE / "adversary_mixed.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(mrows[0].keys()))
        w.writeheader()
        w.writerows(mrows)


if __name__ == "__main__":
    main()
