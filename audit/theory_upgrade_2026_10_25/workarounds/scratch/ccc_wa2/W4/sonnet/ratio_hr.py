"""(a) hazard-rate-ordered but not LR-ordered classes: is Lambda monotone along U[0,r]?
(b) derivative formula d ln Lambda / dr = S_H(r)/int_0^r S_H - S_L(r)/int_0^r S_L
(c) location family (translated uniform window) with LR-ordered classes.
(d) among random FOSD pairs, classify by HR; count Lambda-monotonicity violations by class. Prints only."""
import numpy as np

rng = np.random.default_rng(99)


def W_unif(atoms, probs, r):
    return (probs * np.minimum(atoms / r, 1.0)).sum()


# (a) the hand-built pair: L uniform on {1,2,3,4}; H = (0.1, 0.3, 0.1, 0.5)
atoms = np.array([1.0, 2.0, 3.0, 4.0])
qL = np.array([0.25, 0.25, 0.25, 0.25])
qH = np.array([0.1, 0.3, 0.1, 0.5])
SL = lambda y: (qL * (atoms > y)).sum()
SH = lambda y: (qH * (atoms > y)).sum()
print("(a) HR-not-LR pair. q_H/q_L =", qH / qL, "(not monotone => not LR)")
print("    S_H/S_L at 0.5, 1.5, 2.5, 3.5:", [SH(y) / SL(y) for y in (0.5, 1.5, 2.5, 3.5)], "(nondecreasing => HR)")
rs = np.linspace(0.4, 30, 6000)
Lam = np.array([W_unif(atoms, qH, r) / W_unif(atoms, qL, r) for r in rs])
print("    min step of Lambda(r):", np.diff(Lam).min(), " Lambda at r=0.5,2,4,10,30:",
      [round(W_unif(atoms, qH, r) / W_unif(atoms, qL, r), 5) for r in (0.5, 2, 4, 10, 30)])

# (b) derivative formula check on the same pair
print("(b) d ln Lambda/dr: finite difference vs formula")
def intS(S, r, n=200001):
    ys = np.linspace(0, r, n)
    v = np.array([S(y) for y in ys[:-1] + 0.5 * (ys[1] - ys[0])])
    return v.sum() * (ys[1] - ys[0])
for r in (1.5, 2.5, 3.5, 6.0):
    eps = 1e-5
    fd = (np.log(W_unif(atoms, qH, r + eps) / W_unif(atoms, qL, r + eps))
          - np.log(W_unif(atoms, qH, r - eps) / W_unif(atoms, qL, r - eps))) / (2 * eps)
    fm = SH(r) / intS(SH, r) - SL(r) / intS(SL, r)
    print(f"    r={r}: finite difference={fd:.6f}, formula={fm:.6f}")

# (c) translated uniform window with LR-ordered classes
viol = 0
tot = 0
for t in range(300):
    n = rng.integers(3, 8)
    a = np.sort(rng.uniform(0.6, 12.0, n))
    qLr = rng.dirichlet(np.ones(n))
    l = np.sort(rng.uniform(0.2, 3.0, n))
    qHr = qLr * l
    qHr /= qHr.sum()
    w = rng.uniform(0.5, 6.0)
    ss = np.linspace(-w, a.max() + 1.0, 3000)
    Lam = []
    for s in ss:
        FH = (qHr * np.clip((a - s) / w, 0, 1)).sum()
        FL = (qLr * np.clip((a - s) / w, 0, 1)).sum()
        if FL > 1e-9:
            Lam.append(FH / FL)
    Lam = np.array(Lam)
    # Lambda should be nonincreasing in s here? stronger incumbent = larger s; check monotone nondecreasing
    tot += 1
    if np.diff(Lam).min() < -1e-9:
        viol += 1
print(f"(c) translated-window family, LR classes: {viol} violations of 'Lambda nondecreasing in s' in {tot} trials")

# (d) classify random FOSD pairs by HR
def hr_holds(aL, qL, aH, qH):
    pts = np.unique(np.concatenate([aL, aH]))
    mids = np.concatenate([[pts[0] - 1], 0.5 * (pts[1:] + pts[:-1])])
    SLv = np.array([(qL * (aL > y)).sum() for y in mids])
    SHv = np.array([(qH * (aH > y)).sum() for y in mids])
    ok = SLv > 1e-12
    ratio = SHv[ok] / SLv[ok]
    return np.diff(ratio).min() >= -1e-12 if len(ratio) > 1 else True


counts = {"HR": [0, 0], "notHR": [0, 0]}
rs = np.linspace(0.6, 40, 3000)
for t in range(1500):
    n = rng.integers(2, 6)
    q = rng.dirichlet(np.ones(n))
    aL = np.sort(rng.uniform(0.6, 8.0, n))
    aH = aL + rng.exponential(1.5, n) * (rng.uniform(size=n) < 0.8)
    # same probabilities after coupling; G_H need not have sorted atoms, so keep as is (S_H computed from atoms directly)
    hr = hr_holds(aL, q, aH, q)
    Lam = np.array([W_unif(aH, q, r) / W_unif(aL, q, r) for r in rs])
    bad = np.diff(Lam).min() < -1e-12
    key = "HR" if hr else "notHR"
    counts[key][0] += 1
    counts[key][1] += int(bad)
print("(d) random FOSD pairs: [trials, violations of monotone Lambda]:", counts)
