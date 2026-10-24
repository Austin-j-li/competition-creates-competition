#!/usr/bin/env python3
"""P3 diagnostic: a floating-point scan for equilibria of the research game at calibration B.

Status: numerical diagnostic. The scan does not use the classification lemmas of the proof package.
It uses only the strict loss of wrong-signed orders, which holds against every price function.
It covers the challenger rule C1 (prepare at indifference); a challenger mixture is a measure-zero
event on a grid, so the threshold equilibria of rule CM are outside this scan.

Grid: conjectured intensity lam in [0, cap] (step cap/4000), high-class purchase probability alpha
and low-class sale probability sigma after success (step 1/50 each). For every grid point the
program computes posteriors, entry, prices, every order payoff, the research best response
min(cap, V/a), and the regret of each class. It prints the clusters of grid points whose residuals
lie below the stated tolerances.

Usage:
  python P3_float_scan.py > P3_float_scan.log
"""
import hashlib
import math
import pathlib
import platform

import numpy as np

H_VAL, L_VAL, P_RES = 10.0, 1.0, 0.5
RHO, C_H, K = 0.25, 6.0, 0.02
BETA = 0.294655
A_RES = 1.0 / 40.0
U = math.e - 1.0
CAP = U * BETA / (1.0 + U * BETA)
STRENGTHS = [1.2, 1.55, 1.6, 1.65, 3.0, 3.6]
N_LAM = 4000
N_MIX = 50
TOL_ORDER = 5.0e-4
TOL_RES = 3.0e-4


def auction(r):
    p, l, h = P_RES, L_VAL, H_VAL
    t0 = p * (1 - p / r)
    tH = r / 2 + p * p / (2 * r)
    tL = l - (l * l - p * p) / (2 * r)
    gH = h - r / 2 - p * p / (2 * r)
    gL = (l * l - p * p) / (2 * r)
    return dict(t0=t0, tH=tH, tL=tL, Delta=tH - tL, tau=(C_H - gL) / (gH - gL))


def scan(r):
    A = auction(r)
    Dl, tau = A["Delta"], A["tau"]
    lam = np.linspace(0.0, CAP, N_LAM + 1)
    mix = np.linspace(0.0, 1.0, N_MIX + 1)
    alpha, sigma = np.meshgrid(mix, mix, indexing="ij")
    hits = []
    for i, lm in enumerate(lam):
        b = (1 - lm) * BETA
        c = (1 - lm) * (1 - 2 * BETA)
        fHp, fH0, fHm = b + lm * alpha, c + lm * (1 - alpha), b + 0 * alpha
        fLp, fL0, fLm = b + 0 * sigma, c + lm * (1 - sigma), b + lm * sigma
        mup = fHp / (fHp + fLp)
        mu0 = fH0 / (fH0 + fL0)
        mum = fHm / (fHm + fLm)
        ep = RHO + (1 - RHO) * (mup >= tau)
        e0 = RHO + (1 - RHO) * (mu0 >= tau)
        em = RHO + (1 - RHO) * (mum >= tau)
        UHp = ep * Dl * (1 - mup) - K
        UHm = -em * Dl * (1 - mum) - K
        ULm = em * Dl * mum - K
        ULp = -ep * Dl * mup - K
        maxH = np.maximum(np.maximum(UHp, UHm), 0.0)
        maxL = np.maximum(np.maximum(ULm, ULp), 0.0)
        regH = maxH - alpha * UHp
        regL = maxL - sigma * ULm
        V = 0.5 * (maxH + maxL)
        zstar = np.minimum(CAP, V / A_RES)
        resid = np.abs(lm - zstar)
        ok = (regH <= TOL_ORDER) & (regL <= TOL_ORDER) & (resid <= TOL_RES)
        if ok.any():
            Pr_p = 0.5 * (fHp + fLp)
            Pr_0 = 0.5 * (fH0 + fL0)
            Pr_m = 0.5 * (fHm + fLm)
            E = Pr_p * ep + Pr_0 * e0 + Pr_m * em
            for a_i, s_i in zip(*np.nonzero(ok)):
                hits.append((i, lm, alpha[a_i, s_i], sigma[a_i, s_i], E[a_i, s_i], resid[a_i, s_i],
                             max(regH[a_i, s_i], regL[a_i, s_i])))
    return hits


def clusters(hits):
    hits = sorted(hits, key=lambda x: x[0])
    out, cur = [], []
    for h in hits:
        if cur and h[0] - cur[-1][0] > 200:
            out.append(cur)
            cur = []
        cur.append(h)
    if cur:
        out.append(cur)
    return out


def main():
    src = pathlib.Path(__file__).read_bytes()
    print("P3 floating-point scan (numerical diagnostic; challenger rule C1)")
    print(f"python {platform.python_version()}, numpy {np.__version__} | source sha256 {hashlib.sha256(src).hexdigest()}")
    print(f"beta = {BETA}, cap = {CAP:.12f}, a = {A_RES}, grid: {N_LAM + 1} intensities, {N_MIX + 1}^2 order mixtures")
    print(f"tolerances: order regret <= {TOL_ORDER}, research residual <= {TOL_RES}")
    for r in STRENGTHS:
        hits = scan(r)
        cl = clusters(hits)
        print(f"r = {r}: {len(hits)} grid points pass; {len(cl)} clusters")
        for c in cl:
            lams = [h[1] for h in c]
            als = [h[2] for h in c]
            sis = [h[3] for h in c]
            Es = [h[4] for h in c]
            best = min(c, key=lambda h: h[5] + h[6])
            print(f"   lambda in [{min(lams):.6f}, {max(lams):.6f}], alpha in [{min(als):.2f}, {max(als):.2f}], "
                  f"sigma in [{min(sis):.2f}, {max(sis):.2f}], entry in [{min(Es):.6f}, {max(Es):.6f}]; "
                  f"best point lambda {best[1]:.6f}, alpha {best[2]:.2f}, sigma {best[3]:.2f}, entry {best[4]:.6f}, "
                  f"research residual {best[5]:.2e}, regret {best[6]:.2e}")


if __name__ == "__main__":
    main()
