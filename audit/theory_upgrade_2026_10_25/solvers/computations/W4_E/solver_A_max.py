"""Max over r of B_r(M) in solver_A's economy (classes 1 and 2, p=1/2, M=5/7); strictness example for (C2) not (C3). Prints only."""
import numpy as np
h, ell, p = 2.0, 1.0, 0.5
M = 5 / 7
def prof(theta, r):
    # g(theta) = int_p^theta F(y) dy with F = min(y/r,1)
    if theta <= r:
        return (theta**2 - p**2) / (2 * r)
    return (r**2 - p**2) / (2 * r) + (theta - r)
best = 0
for r in np.linspace(0.51, 40, 400000):
    gH, gL = prof(h, r), prof(ell, r)
    B = gL + M * (gH - gL)
    if B > best:
        best, rb = B, r
print("max_r B_r(M) =", best, "at r =", rb)

# (C2) but not (C3): G_L = delta_1, G_H = 1/2 delta_1 + 1/2 delta_10, uniform incumbent with rbar = 3.6
def piv(r):
    WL = min(1 / r, 1)
    WH = 0.5 * min(1 / r, 1) + 0.5 * min(10 / r, 1)
    return WH - WL
print("piv(r) for r=1.2,2,3,3.6:", [round(piv(r), 4) for r in (1.2, 2.0, 3.0, 3.6)], "-> rising")
