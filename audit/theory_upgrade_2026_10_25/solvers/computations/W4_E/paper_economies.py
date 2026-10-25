"""Where is the peak of the winner-gap hump relative to the strengths the paper's own economies use?
Uniform incumbent family U[0,r]; classes from Table A6 (numbers.tex). Prints only."""
import numpy as np

p = 0.5
ys = np.linspace(0, 80, 1600001)
dy = ys[1] - ys[0]


def unif(a, b):
    return lambda y: np.clip((y - a) / (b - a), 0, 1)


def pt(a):
    return lambda y: (y >= a) * 1.0


economies = {
    "benchmark points (1,10)":            (pt(1.0), pt(10.0), (1.2, 3.0, 3.6)),
    "moderate gap points (1,2)":          (pt(1.0), pt(2.0), (1.05, 1.5, None)),
    "narrow bands U[.95,1.05],U[9.95,10.05]": (unif(0.95, 1.05), unif(9.95, 10.05), (1.2, 3.0, 3.6)),
    "wide classes U[.6,1.4], U[1,19]":    (unif(0.6, 1.4), unif(1.0, 19.0), (1.0, 4.5, 5.5)),
    "same means points (1,10), r=1,4.5,5.5": (pt(1.0), pt(10.0), (1.0, 4.5, 5.5)),
}

for name, (GL, GH, rr) in economies.items():
    D = GL(ys) - GH(ys)
    Gam = np.cumsum(D) * dy - 0.5 * D * dy
    # gap(r) = Gamma(r)/r  (split probability, E_F[D(R)]) for U[0,r]
    idx = lambda r: int(round(r / dy))
    gap = lambda r: Gam[idx(r)] / r
    rs = ys[ys > 0.3]
    gaps = Gam[ys > 0.3] / rs
    i = int(np.argmax(gaps))
    print(f"{name}\n   peak of split probability at r*={rs[i]:.3f} with value {gaps[i]:.4f}")
    for r in rr:
        if r is not None:
            Dr = D[idx(r)]
            print(f"   r={r}: split prob={gap(r):.4f}, D(r)={Dr:.4f}, D(r)-avg={Dr-gap(r):+.4f}")
