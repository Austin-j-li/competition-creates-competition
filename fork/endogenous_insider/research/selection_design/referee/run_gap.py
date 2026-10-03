"""Referee scan of the gap region under the uniform subsidy s = s_D (tau_s = 1/2), minimal pools,
pure orders. Writes CSV only."""
from __future__ import annotations
import numpy as np
import mpmath as mp
from check import BENCH, pay, B, grid_profile, write_csv, HERE

par = BENCH
out = []
for r in [1.35, 1.40, 1.45, 1.50, 1.52, 1.54]:
    sD = float(par.c - B(pay(par, r), mp.mpf(1)/2))
    best = []
    qHs = np.round(np.arange(0.0, 1.0001, 0.02), 3)
    qLs = np.round(np.arange(-1.0, 0.0001, 0.02), 3)
    for qH in qHs:
        for qL in qLs:
            if qH == qL:
                continue
            o = grid_profile(par, r, sD, float(qH), float(qL))
            dist = max(abs(o.brH - qH), abs(o.brL - qL))
            best.append((dist, qH, qL, o.brH, o.brL))
    best.sort()
    # 1-D fine scan along q_H = 1
    line = []
    for qL in np.round(np.arange(-1.0, 0.0001, 0.002), 4):
        o = grid_profile(par, r, sD, 1.0, float(qL))
        line.append((float(qL), o.brH, o.brL, o.UL))
    gaps = [(a[0], a[2], b[0], b[2]) for a, b in zip(line, line[1:]) if abs(a[2]-b[2]) > 0.05]
    cross = [(a[0], a[2], b[0], b[2]) for a, b in zip(line, line[1:]) if (a[2]-a[0])*(b[2]-b[0]) <= 0]
    print(f"r={r}: closest 2-D profiles (dist, qH, qL, BR_H, BR_L): {best[:3]}")
    print(f"   along qH=1: BR_L jumps {gaps[:4]}; sign changes of BR_L-qL {cross[:4]}")
    print(f"   BR_H range along qH=1: {min(x[1] for x in line)} .. {max(x[1] for x in line)}")
    out.append(dict(r=r, s_D=sD, best_dist=best[0][0], best_qH=best[0][1], best_qL=best[0][2],
                    BR_L_jumps=str(gaps[:4]), BR_L_crossings=str(cross[:4])))
write_csv(HERE / "ref_gap_scan.csv", out)
