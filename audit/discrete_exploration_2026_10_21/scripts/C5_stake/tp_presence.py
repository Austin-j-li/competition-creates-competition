"""Presence probability lambda < 1 in the three-point stake model (exact fractions; print only).

A present investor chooses q. With probability 1 - lambda the order is zero. The stake pays in both cases.
The script recomputes, from primitives, the gains of a present investor at S and at M for several lambda,
and the stake thresholds (affine in omega, so two evaluations give the root).
Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C5_stake/tp_presence.py
"""
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tp_lib import BENCH, R1, auction, tau_of, payoffs, gains  # noqa: E402

PAR = BENCH
RHO = PAR["rho"]


def flows_lambda(lam, bH, bL):
    third = F(1, 3)
    fH = {x: (1 - lam) * third for x in (-1, 0, 1)}
    fL = {x: (1 - lam) * third for x in (-1, 0, 1)}
    fH[2] = F(0)
    fL[2] = F(0)
    for f, b in ((fH, bH), (fL, bL)):
        for z in (-1, 0, 1):
            f[z] += lam * (1 - b) * third          # present, no buy
            f[1 + z] += lam * b * third            # present, buy
    return fH, fL


def gains_at(a, omega, lam, bH, bL, phi2):
    fH, fL = flows_lambda(lam, bH, bL)
    mu = {x: fH[x] / (fH[x] + fL[x]) for x in (-1, 0, 1, 2)}
    e = {}
    for x in (-1, 0, 1, 2):
        b = a["gL"] + mu[x] * (a["gH"] - a["gL"])
        if b > PAR["cH"]:
            ph = F(1)
        elif b < PAR["cH"]:
            ph = F(0)
        else:
            ph = phi2
        e[x] = RHO + (1 - RHO) * ph
    g = gains(payoffs(a, PAR, omega, bH, bL, e, mu))
    eH = sum(fH[x] * e[x] for x in e)
    eL = sum(fL[x] * e[x] for x in e)
    return g, (eH + eL) / 2, eH / 2, mu


if __name__ == "__main__":
    a = auction(R1, PAR)
    tau = tau_of(a, PAR)
    bmax = 1 / tau - 1
    print("r1 = 3, benchmark. Present investor's gains do not depend on lambda; entry scales with lambda.")
    for lam in (F(1), F(4, 5), F(1, 2), F(1, 10)):
        # S: L's gain is affine in omega -> root
        g0, *_ = gains_at(a, F(0), lam, F(1), F(0), F(1))
        g1, *_ = gains_at(a, F(1), lam, F(1), F(0), F(1))
        Om1 = -g0["L"] / (g1["L"] - g0["L"])
        # M at beta_max with phi = 1: root in omega
        h0, *_ = gains_at(a, F(0), lam, F(1), bmax, F(1))
        h1, *_ = gains_at(a, F(1), lam, F(1), bmax, F(1))
        Om2 = -h0["L"] / (h1["L"] - h0["L"])
        gS, E_S, OH_S, muS = gains_at(a, F(0), lam, F(1), F(0), F(1))
        gM, E_M, OH_M, muM = gains_at(a, Om2, lam, F(1), bmax, F(1))
        print(f" lambda={str(lam):5s}  Omega1={float(Om1):.10f}  Omega2={float(Om2):.10f}  "
              f"E(S)={float(E_S):.6f} [rho+lam(1-rho)/6={float(F(1,4)+lam*F(3,4)/6):.6f}]  "
              f"E(M at Omega2)={float(E_M):.6f} [rho+lam(1-rho)/(6 tau)={float(F(1,4)+lam*F(3,4)/(6*tau)):.6f}]  "
              f"O_H(S)={float(OH_S):.6f}  posterior at flow -1 under S={float(muS[-1]):.6f}")
