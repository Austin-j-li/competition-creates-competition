"""Fine referee scan near the end of the gap region (r = 1.50, s = s_D). Prints only."""
from __future__ import annotations
import numpy as np
import mpmath as mp
from check import BENCH, pay, B, grid_profile, XG, I_ORD, lap, conv_laplace, tau

par = BENCH
for r in [1.45, 1.50, 1.51]:
    sD = float(par.c - B(pay(par, r), mp.mpf(1)/2))
    res = []
    for qH in np.round(np.arange(0.80, 1.0001, 0.004), 4):
        for qL in np.round(np.arange(-0.2, 0.0001, 0.004), 4):
            o = grid_profile(par, r, sD, float(qH), float(qL))
            res.append((max(abs(o.brH-qH), abs(o.brL-qL)), qH, qL, o.brH, o.brL, o.UH))
    res.sort()
    print(r, "closest:", [tuple(round(float(v), 4) for v in x) for x in res[:4]])
    # H-type payoff at s=1 and s=0 along the critical line: is BR_H a corner?
    for qH, qL in [(0.96, -0.02), (0.98, -0.01), (1.0, 0.0)]:
        P = pay(par, r); DT = float(P["DT"])
        aH, aL = lap(par.b, XG-qH), lap(par.b, XG-qL); mu = aH/(aH+aL); e = (mu >= 0.5-1e-12).astype(float)
        FH = conv_laplace(par.b, e*DT*(1-mu)); q = XG[I_ORD]
        U = q*FH[I_ORD] - par.k*np.abs(q)
        print("   ", qH, qL, "U_H(1)=%.6f  max_{s in(0,1)} U_H=%.6f at s=%.3f" % (U[-1], U[(q > 0) & (q < 1)].max(), q[(q > 0) & (q < 1)][U[(q > 0) & (q < 1)].argmax()]))
