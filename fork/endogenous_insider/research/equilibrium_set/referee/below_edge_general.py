"""Referee scratch: below r_e, can any high-type strategy (pure q < 1 or a mixture) meet the low
type's condition? For a high-type strategy sigma_H on [0, 1] and a low order -z, the low type's
condition needs Psi = C_max e^{-z/b}(1 - z/b) - k >= 0 (z < 1 interior) or (1-1/b) e^{-1/b} C_max >= k
(z = 1), where C_max = Delta_T int_{mu >= tau} f mu (Lemma ES.4(a)). This is necessary for any live
equilibrium; the high type's optimality is not checked. Grid integrals. Status: numerical diagnostic.
Writes below_edge_general.csv.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
H_, ELL, P_, B, K, C = 10.0, 1.0, 0.5, 2.0, 0.02, 6.0
X = np.linspace(-15.0, 60.0, 75001)
DX = X[1] - X[0]
F0 = np.exp(-np.abs(X) / B) / (2 * B)


def acq(r: float) -> tuple[float, float]:
    tH = r / 2 + P_ ** 2 / (2 * r)
    tL = ELL - (ELL ** 2 - P_ ** 2) / (2 * r)
    gH = H_ - tH
    gL = (ELL ** 2 - P_ ** 2) / (2 * r)
    return tH - tL, (C - gL) / (gH - gL)


def psi_general(r: float, qs, ws, z: float) -> float:
    dT, tau = acq(r)
    aH = sum(w * np.exp(-np.abs(X - q) / B) for q, w in zip(qs, ws))
    aL = np.exp(-np.abs(X + z) / B)
    mu = aH / (aH + aL)
    Cmax = dT * float((F0 * mu * (mu >= tau)).sum() * DX)
    return Cmax * math.exp(-z / B) * (1 - z / B) - K


def main() -> None:
    rows = []
    rng = np.random.default_rng(11)
    for r in (1.40, 1.55, 1.62, 1.65, 1.658):
        best_pure, arg_pure = -math.inf, None
        for q in np.linspace(0.0, 1.0, 51):
            for z in np.linspace(0.0, 1.0, 51):
                v = psi_general(r, [q], [1.0], float(z))
                if v > best_pure:
                    best_pure, arg_pure = v, (float(q), float(z))
        best_mix = -math.inf
        for _ in range(1500):
            kH = int(rng.integers(2, 4))
            qs = rng.uniform(0.0, 1.0, kH)
            ws = rng.dirichlet(np.ones(kH))
            z = float(rng.uniform(0.0, 1.0))
            best_mix = max(best_mix, psi_general(r, qs, ws, z))
        rows.append({"r": r, "max_Psi_pure": best_pure, "argmax_q_z": str(arg_pure), "max_Psi_mixed": best_mix})
        print(rows[-1], flush=True)
    with (HERE / "below_edge_general.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
