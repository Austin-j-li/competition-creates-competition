"""Recruiting window {r : B_r(1/2) < c_H <= B_r(M)} for benchmark primitives and several c_H; location of the hump peak h. Prints only."""
import math
import numpy as np

h, ell, p = 10.0, 1.0, 0.5
u = math.e - 1
M = (1 + u) / (2 + u)
vartheta = 2 * M - 1


def gs(r):
    gH = h - r / 2 - p * p / (2 * r) if r <= h else (h * h - p * p) / (2 * r)
    gL = (ell**2 - p**2) / (2 * r) if r >= ell else 0.0
    return gH, gL


def B(r, mu):
    gH, gL = gs(r)
    return gL + mu * (gH - gL)


rs = np.linspace(1.01, 60, 590001)
for cH in (6.0, 4.0, 3.656, 3.0, 2.6, 2.0):
    inwin = np.array([(B(r, 0.5) < cH) and (B(r, M) >= cH) for r in rs])
    if inwin.any():
        lo, hi = rs[inwin].min(), rs[inwin].max()
        # contiguous?
        idx = np.where(inwin)[0]
        contiguous = (idx.max() - idx.min() + 1 == len(idx))
        print(f"c_H={cH}: recruiting window ({lo:.3f}, {hi:.3f}], contiguous={contiguous}; contains peak h=10? {lo < h <= hi}")
        for r in (lo + 1e-3, hi):
            s = (r - ell) / r if r <= h else (h - ell) / r
            print(f"      r={r:.3f}: split prob={s:.4f}, winner gap={vartheta*s:.4f}")
    else:
        print(f"c_H={cH}: no recruiting window")
print("B_h(1/2)=", B(h, 0.5), " B_h(M)=", B(h, M))
