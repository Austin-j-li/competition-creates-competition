"""Referee grid checks: convolution accuracy, cutoff-family members, Table 3 rows, gap region.
Writes CSV only."""
from __future__ import annotations
import time
import numpy as np
import mpmath as mp
from check import (BENCH, Par, mM, pay, B, tau, logit, J_closed, grid_profile, conv_laplace, lap,
                   XG, I_ORD, write_csv, HERE)

par = BENCH
half = 0.5
P3 = pay(par, 3)
ts0 = float(tau(par, P3, 0)); xs0 = float(logit(mp.mpf(ts0)))
# 1. accuracy: F_H(1) under full orders and entry [x*, inf) equals J
aH, aL = lap(par.b, XG - 1), lap(par.b, XG + 1)
mu = aH/(aH+aL); e = (mu >= ts0).astype(float)
FH = conv_laplace(par.b, e*float(P3["DT"])*(1-mu))
i1 = int(np.argmin(np.abs(XG-1.0)))
print("F_H(1) grid", FH[i1], "J closed", float(J_closed(par, P3, mp.mpf(xs0))))

t = time.time()
rows = []
def show(tag, r, s, qH, qL, cut=-np.inf):
    o = grid_profile(par, r, s, qH, qL, cut)
    rows.append(dict(tag=tag, r=r, s=s, qH=qH, qL=qL, cutoff=cut, brH=o.brH, brL=o.brL, UH=o.UH, UL=o.UL,
                     E=0.5*(o.eH+o.eL), mubar=o.mubar, pool_ok=o.pool_ok))
    print(f"{tag:28s} r={r} s={s:.4f} q=({qH},{qL}) cut={cut} -> BR=({o.brH:+.4f},{o.brL:+.4f}) "
          f"U=({o.UH:.5f},{o.UL:.5f}) E={0.5*(o.eH+o.eL):.4f} mubar={o.mubar:.5f} pool_ok={o.pool_ok}")
    return o
print(time.time()-t)
# 2. cutoff family members at r = 3, s = 0
show("family x'=0.872", 3.0, 0.0, 1.0, -1.0, 0.872)
show("family x'=2.572", 3.0, 0.0, 1.0, -1.0, 2.572)
show("family x'=2.622", 3.0, 0.0, 1.0, -0.9975, 2.622)
show("family x'=3.222", 3.0, 0.0, 1.0, -0.7585, 3.222)
show("family x'=3.272 (fork: collapse)", 3.0, 0.0, 1.0, -0.74, 3.272)
# 3. Table 3 grid rows at s = s_D
for r, qH, qL in [(1.55, 1.0, -0.227), (1.70, 1.0, -0.718), (1.85, 1.0, -1.0)]:
    sD = float(par.c - B(pay(par, r), mp.mpf(1)/2))
    show(f"Table 3 r={r}", r, sD, qH, qL)
# fork live branch cross-check at s = 0
show("fork r=1.66 s=0", 1.66, 0.0, 1.0, -0.25)
print("elapsed", time.time()-t)
write_csv(HERE / "ref_grid_points.csv", rows)
