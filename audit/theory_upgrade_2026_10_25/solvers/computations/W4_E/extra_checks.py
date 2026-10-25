"""Odds ratio vs relative risk beyond h; recruitment-vs-peak threshold for c_H; solver_A's counterexample economy. Prints only."""
import math

u = math.e - 1
M, m = (1 + u) / (2 + u), 1 / (2 + u)
vartheta = M - m


def OR(WH, WL):
    w1 = M * WH + (1 - M) * WL
    wm = m * WH + (1 - m) * WL
    return (w1 / (1 - w1)) / (wm / (1 - wm)), w1 / wm


print("Odds ratio vs relative risk for point-mass classes (ell=1, h=2), U[0,r]:")
for r in (1.2, 1.5, 2.0, 2.5, 3.0, 5.0, 10.0, 100.0):
    WH, WL = min(2 / r, 1), min(1 / r, 1)
    o, rr = OR(WH, WL)
    print(f"  r={r:6.1f}: W_H={WH:.4f} W_L={WL:.4f}  odds ratio={o:.4f}  relative risk={rr:.4f}  gap={vartheta*(WH-WL):.4f}")

print("\nSame for benchmark classes (ell=1, h=10):")
for r in (1.2, 3.0, 3.6, 10.0, 20.0, 100.0):
    WH, WL = min(10 / r, 1), min(1 / r, 1)
    o, rr = OR(WH, WL)
    print(f"  r={r:6.1f}: odds ratio={o:.4f}  relative risk={rr:.4f}  gap={vartheta*(WH-WL):.4f}")

# recruitment ceiling vs the peak at r = h (benchmark primitives)
h, ell, p, c_H = 10.0, 1.0, 0.5, 6.0


def B(r, mu):
    if r <= h:
        gH = h - r / 2 - p * p / (2 * r)
    else:
        gH = (h * h - p * p) / (2 * r)
    gL = (ell**2 - p**2) / (2 * r) if r >= ell else 0.0
    return gL + mu * (gH - gL)


print("\nB_h(M) = best profit against an incumbent at the high class's value:", B(h, M), " c_H =", c_H,
      " ratio c_H/B_h(M) =", c_H / B(h, M))
print("c_H threshold below which recruitment survives past r = h (benchmark primitives, slot):", B(h, M))
print("in units of h:", B(h, M) / h)
# ceiling r_C: B_r(M) = c_H
lo, hi = 1.01, 9.99
for _ in range(100):
    mid = 0.5 * (lo + hi)
    if B(mid, M) > c_H:
        lo = mid
    else:
        hi = mid
print("r_C =", lo, " (paper: 3.592659)")

# solver_A's counterexample economy: pi=1/2, rho=1/2, lam=beta=1/3, k=1/100, c_H=2, classes (1,2), p=1/2
lam, beta = 1 / 3, 1 / 3
b = (1 - lam) * beta
uu = lam / b
Mc, mc = (1 + uu) / (2 + uu), 1 / (2 + uu)
rho, k, cH, hh, ll, pp = 0.5, 0.01, 2.0, 2.0, 1.0, 0.5
print("\nSol's economy: b=%.4f u=%.4f M=%.4f m=%.4f vartheta=%.4f" % (b, uu, Mc, mc, Mc - mc))
for r in (2.0, 2.5, 3.0, 5.0, 10.0):
    Delta = 1 - 3 / (2 * r)
    gH = (hh * hh - pp * pp) / (2 * r)
    gL = (ll * ll - pp * pp) / (2 * r)
    BM = gL + Mc * (gH - gL)
    KH = rho * Delta * (1 - Mc)
    KL = rho * Delta * mc
    print(f"  r={r}: Delta={Delta:.4f} B(M)={BM:.4f} (<c_H={cH}) K_H>={KH:.4f} K_L>={KL:.4f} (k={k}) "
          f"gap = vartheta*(1/r) = {(Mc-mc)/r:.4f}")
