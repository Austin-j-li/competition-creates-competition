"""Referee scratch, part 2: closed form (ES.2) against quadrature, Lemma ES.2 and Proposition ES.2(a)
on random mixed profiles, and the monotonicity in z of the least- and largest-entry members.
Prints results; writes recheck2.csv. Status: numerical diagnostic.
"""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
from recheck import B, K, INF, acq, C_quad, entry, f, integ, mu_pure, n_of, xstar  # noqa: E402
import core  # noqa: E402  (the note's closed forms, compared against the referee's quadrature)

out = []


def rec(name, val):
    out.append({"name": name, "value": repr(val)})
    print(f"{name:60s} {val!r}")


def main() -> None:
    # (a) closed form C(z, r) of (ES.2) against quadrature
    worst = 0.0
    for r in (1.7, 2.0, 2.5, 3.0, 3.5):
        n = n_of(r)
        for z in np.linspace(n, 1.0, 9):
            worst = max(worst, abs(core.C_low(core.BENCH, r, float(z)) - C_quad(r, float(z))))
    rec("max |C closed (ES.2) - C quadrature|", worst)
    # (b), (c) random mixed correctly signed profiles: monotone posterior and bound on x <= 0
    rng = np.random.default_rng(7)
    xs = np.linspace(-12, 12, 4801)
    mu_hat = 1 / (1 + math.exp(-1 / B))
    worst_mono, worst_bound, worst_left = -INF, -INF, -INF
    for _ in range(2000):
        kH, kL = rng.integers(1, 4), rng.integers(1, 4)
        qH, wH = rng.uniform(0, 1, kH), rng.dirichlet(np.ones(kH))
        qL, wL = -rng.uniform(0, 1, kL), rng.dirichlet(np.ones(kL))
        aH = sum(w * np.exp(-np.abs(xs - q) / B) for q, w in zip(qH, wH))
        aL = sum(w * np.exp(-np.abs(xs - q) / B) for q, w in zip(qL, wL))
        mu = aH / (aH + aL)
        worst_mono = max(worst_mono, float(-np.diff(mu).min()))
        worst_bound = max(worst_bound, float(mu[xs <= 0].max() - mu_hat))
        worst_left = max(worst_left, float(mu[xs <= -1].max() - 0.5))
    rec("Lemma ES.2: max decrease of mu over grid (should be <= 0)", worst_mono)
    rec("ES.2(a): max of mu on x<=0 minus mu_hat (should be <= 0)", worst_bound)
    rec("Lemma ES.2: max of mu on x<=-1 minus 1/2 (should be <= 0)", worst_left)
    # (d), (e) least and largest entry over admissible A for each z, q_H = 1
    for r in (1.7, 2.0, 2.5, 3.0, 3.5):
        dT, tau = acq(r)
        n = n_of(r)
        def psi(z):
            return C_quad(r, z) * math.exp(-z / B) * (1 - z / B) - K
        zU = 1.0 if psi(1.0) >= 0 else brentq(psi, n, 1.0, xtol=1e-12)
        zs = np.linspace(n, min(zU - 1e-9, 1 - 1e-9), 25)
        least, most = [], []
        for z in zs:
            z = float(z)
            target = K * math.exp(z / B) / (1 - z / B)
            x0 = max(xstar(r, 1.0, z), 1e-12)
            fun = lambda x: f(x) * mu_pure(x, 1.0, z)
            if C_quad(r, z) <= target * (1 + 1e-12):
                eH, eL = entry(r, 1.0, z, [(x0, INF)])
                least.append(0.5 * (eH + eL))
                most.append(0.5 * (eH + eL))
                continue
            if z > n + 1e-12:
                y = brentq(lambda t: dT * integ(fun, x0, t, [1.0]) - target, x0 + 1e-9, 80.0, xtol=1e-12)
                eH, eL = entry(r, 1.0, z, [(x0, y)])
                least.append(0.5 * (eH + eL))
            else:
                pi = target / C_quad(r, z)
                least.append(pi / (4 * tau))
            xc = brentq(lambda t: dT * integ(fun, t, INF, [1.0]) - target, x0, 80.0, xtol=1e-12) \
                if C_quad(r, z) > target else x0
            eH, eL = entry(r, 1.0, z, [(xc, INF)])
            most.append(0.5 * (eH + eL))
        least, most = np.array(least), np.array(most)
        rec(f"r={r}: least entry increasing in z (min step)", float(np.diff(least).min()))
        rec(f"r={r}: largest entry increasing in z (min step)", float(np.diff(most).min()))
        rec(f"r={r}: least at z=n, largest at z_U", (float(least[0]), float(most[-1])))
    with (HERE / "recheck2.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["name", "value"])
        w.writeheader()
        w.writerows(out)


if __name__ == "__main__":
    main()
