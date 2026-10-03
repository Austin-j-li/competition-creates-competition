"""Referee probe of mixed candidates in the gap region at s = s_D (numerical diagnostic only).
Candidate (a): H plays +1 w.p. lam and 0 otherwise, L plays 0.
Candidate (b): H plays +1 w.p. lam and 0 otherwise, L plays -1 w.p. lam and 0 otherwise.
Entry set {mu_X >= 1/2} (minimal pool). Prints only."""
from __future__ import annotations
import numpy as np
import mpmath as mp
from scipy.optimize import brentq
from check import BENCH, pay, B, XG, I_ORD, lap, conv_laplace, write_csv, HERE

par = BENCH

def payoffs(r: float, lam: float, sym: bool):
    P = pay(par, r); DT = float(P["DT"])
    aH = (1-lam)*lap(par.b, XG) + lam*lap(par.b, XG-1)
    aL = (1-lam)*lap(par.b, XG) + lam*lap(par.b, XG+1) if sym else lap(par.b, XG)
    mu = aH/(aH+aL); e = (mu >= 0.5-1e-12).astype(float)
    FH, FL = conv_laplace(par.b, e*DT*(1-mu)), conv_laplace(par.b, e*DT*mu)
    q = XG[I_ORD]
    UH = q*FH[I_ORD] - par.k*np.abs(q); UL = -q*FL[I_ORD] - par.k*np.abs(q)
    pool = e == 0
    mubar = np.trapezoid(aH*pool, XG)/(np.trapezoid(aH*pool, XG)+np.trapezoid(aL*pool, XG))
    return q, UH, UL, mubar

rows = []
for sym in (False, True):
    for r in [1.35, 1.40, 1.45, 1.50]:
        g = lambda lam: payoffs(r, lam, sym)[1][-1]   # U_H(1)
        lo, hi = 1e-4, 1.0
        glo, ghi = g(lo), g(hi)
        if glo*ghi > 0:
            print(f"sym={sym} r={r}: U_H(1) at lam->0 {glo:.5f}, at lam=1 {ghi:.5f}: no indifference root")
            rows.append(dict(candidate="b" if sym else "a", r=r, lam=float("nan"), UH1=float("nan"), max_UH_interior=float("nan"),
                             L_best=float("nan"), L_best_q=float("nan"), mubar=float("nan"), passes=False,
                             note=f"U_H(1) {glo:.5f} at lam->0 and {ghi:.5f} at lam=1"))
            continue
        lam = brentq(g, lo, hi, xtol=1e-6)
        q, UH, UL, mubar = payoffs(r, lam, sym)
        inner = UH[(q > 1e-9) & (q < 1)].max()
        wrongH = UH[q < 0].max()
        bestL = UL.max(); argL = q[UL.argmax()]
        UL_full = UL[0]
        msg = (f"sym={sym} r={r}: lam*={lam:.4f}, U_H(1)={UH[-1]:.2e}, max U_H on (0,1)={inner:.2e}, "
               f"max U_H wrong sign={wrongH:.2e}, L best={bestL:.2e} at q={argL:+.3f}, U_L(-1)={UL_full:.2e}, mubar={mubar:.4f}")
        print(msg)
        ok = inner <= 0 and wrongH <= 0 and bestL <= 1e-9 and mubar < 0.5
        rows.append(dict(candidate="b" if sym else "a", r=r, lam=lam, UH1=float(UH[-1]), max_UH_interior=float(inner),
                         L_best=float(bestL), L_best_q=float(argL), mubar=float(mubar), passes=bool(ok), note=""))
write_csv(HERE / "ref_gap_mixed.csv", rows)
