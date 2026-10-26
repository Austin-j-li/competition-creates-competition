"""(1) relative risk depends on F only through Lambda = W_H/W_L and is bounded by M/m = 1+u;
(2) Lambda monotone in strength under LR-ordered classes + uniform family; fails without LR;
(3) D nondecreasing on the incumbent's range <=> gap rises along every FOSD pair (numerical probes);
(4) W_H = W_L with Delta>0, gamma>0. Prints only."""
import math
import numpy as np

rng = np.random.default_rng(7)
u = math.e - 1
M, m = (1 + u) / (2 + u), 1 / (2 + u)

# ---------- (1) relative risk -------------
print("(1) relative risk w_1/w_{-1} as a function of Lambda=W_H/W_L; bound M/m =", M / m, "= 1+u =", 1 + u)
for WH, WL in ((1.0, 1 / 3), (1.0, 0.2778), (0.5, 0.25), (0.2, 0.0), (0.3, 0.3), (0.0, 0.0)):
    w1 = M * WH + (1 - M) * WL
    wm1 = m * WH + (1 - m) * WL
    rr_direct = w1 / wm1 if wm1 > 0 else float("nan")
    Lam = WH / WL if WL > 0 else float("inf")
    rr_formula = (M * Lam + (1 - M)) / (m * Lam + (1 - m)) if WL > 0 else M / m
    print(f"   W_H={WH:.4f} W_L={WL:.4f}: RR direct={rr_direct:.5f} via Lambda={rr_formula:.5f}")
for r in (1.2, 3.0, 3.6, 10.0, 40.0):
    WH, WL = min(10 / r, 1), min(1 / r, 1)
    w1 = M * WH + (1 - M) * WL
    wm1 = m * WH + (1 - m) * WL
    print(f"   benchmark classes r={r}: RR={w1/wm1:.5f}  Lambda={WH/WL:.3f}")

# ---------- (2) Lambda monotone under LR + uniform family ---------------
def lam_path(aH_pts, qH, aL_pts, qL, rs):
    out = []
    for r in rs:
        WH = (qH * np.minimum(aH_pts / r, 1)).sum()
        WL = (qL * np.minimum(aL_pts / r, 1)).sum()
        out.append(WH / WL)
    return np.array(out)


rs = np.linspace(0.6, 40, 4000)
viol_lr = 0
tot_lr = 0
for t in range(400):
    n = rng.integers(3, 9)
    a = np.sort(rng.uniform(0.6, 12.0, n))
    qL = rng.dirichlet(np.ones(n))
    l = np.sort(rng.uniform(0.2, 3.0, n))       # nondecreasing likelihood ratio
    qH = qL * l
    qH = qH / qH.sum()
    lam = lam_path(a, qH, a, qL, rs)
    tot_lr += 1
    if np.min(np.diff(lam)) < -1e-12:
        viol_lr += 1
print(f"\n(2) LR-ordered discrete classes, uniform family: {viol_lr} violations of monotone Lambda in {tot_lr} trials")

viol_nolr = 0
tot_nolr = 0
for t in range(400):
    n = rng.integers(2, 6)
    qL = rng.dirichlet(np.ones(n))
    aL = np.sort(rng.uniform(0.6, 8.0, n))
    inc = rng.exponential(1.5, n)
    aH = aL + inc * (rng.uniform(size=n) < 0.8)
    lam = lam_path(aH, qL, aL, qL, rs)
    tot_nolr += 1
    if np.min(np.diff(lam)) < -1e-12:
        viol_nolr += 1
print(f"    only FOSD-ranked classes (quantile coupling, not LR): {viol_nolr} violations in {tot_nolr} trials")

# the explicit non-LR example
aL = np.array([1.0, 5.0])
aH = np.array([1.5, 6.0])
q = np.array([0.5, 0.5])
for r in (1.5, 2.0, 3.0, 4.0, 5.0, 5.5, 6.0, 8.0):
    WH = (q * np.minimum(aH / r, 1)).sum()
    WL = (q * np.minimum(aL / r, 1)).sum()
    print(f"    non-LR example r={r}: Lambda={WH/WL:.4f}, gap W_H-W_L={WH-WL:.4f}")

# ---------- (3) necessity / sufficiency of D nondecreasing on [p, rbar) -------------
print("\n(3) sufficiency probe: classes with D nondecreasing on [p, rbar); random FOSD pairs inside [0, rbar)")
rbar = 5.0
bad = 0
trials = 0
for t in range(300):
    n = rng.integers(3, 8)
    q = rng.dirichlet(np.ones(n))
    aL = np.sort(rng.uniform(0.6, 9.0, n))
    aH = aL.copy()
    for i in range(n):
        if aL[i] < rbar:
            if rng.uniform() < 0.6:
                aH[i] = rbar + rng.uniform(0.5, 4.0)   # move this H atom above the incumbent's range
        else:
            aH[i] = aL[i] + rng.exponential(1.0) * (rng.uniform() < 0.7)
    # R0 ~ U[a0, b0], R1 = R0 + shift (FOSD ordered, both inside [0, rbar))
    for s in range(20):
        w = rng.uniform(0.2, 1.5)
        a0 = rng.uniform(0.0, rbar - 1.5 - w)
        d = rng.uniform(0.0, rbar - (a0 + w) - 0.01)

        def Fcdf(x, a, ww):
            return np.clip((x - a) / ww, 0, 1)
        W0 = (q * (Fcdf(aH, a0, w) - Fcdf(aL, a0, w))).sum()
        W1 = (q * (Fcdf(aH, a0 + d, w) - Fcdf(aL, a0 + d, w))).sum()
        trials += 1
        if W1 < W0 - 1e-12:
            bad += 1
print(f"   falling gap in {bad} of {trials} FOSD pairs (expect 0)")

print("   necessity probe: D(1.5-) > D(1.5+) in the example G_L=(1,5), G_H=(1.5,6) with prob 1/2 each:")
q = np.array([0.5, 0.5])
aL = np.array([1.0, 5.0])
aH = np.array([1.5, 6.0])
for a0 in (1.0, 1.6):
    Fc = lambda x: np.clip((x - a0) / 0.4, 0, 1)
    WHg = (q * Fc(aH)).sum()
    WLg = (q * Fc(aL)).sum()
    print(f"      R ~ U[{a0},{a0+0.4}]: W_H - W_L = {WHg - WLg:.4f}")

# ---------- (4) W_H = W_L although Delta>0, gamma>0 ----------
print("\n(4) classes differ only where the incumbent never is:")
p = 0.5
aL = np.array([1.0, 5.0]); aH = np.array([1.5, 6.0]); q = np.array([0.5, 0.5])
ys = np.linspace(p, 8, 800001)
dy = ys[1] - ys[0]
GL = (q[None, :] * (aL[None, :] <= ys[:, None])).sum(1)
GH = (q[None, :] * (aH[None, :] <= ys[:, None])).sum(1)
D = GL - GH
F = np.clip((ys - 2.0) / 1.0, 0, 1)          # R ~ U[2,3]
Delta = ((1 - F) * D).sum() * dy
gamma = (F * D).sum() * dy
WH = (q * np.clip((aH - 2.0) / 1.0, 0, 1)).sum()
WL = (q * np.clip((aL - 2.0) / 1.0, 0, 1)).sum()
print(f"   Delta_T={Delta:.4f} gamma={gamma:.4f}  W_H={WH:.4f} W_L={WL:.4f}  W_H-W_L={WH-WL:.4f}")
