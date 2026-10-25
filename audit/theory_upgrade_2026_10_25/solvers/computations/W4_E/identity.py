"""Check W_H - W_L = E_F[D(R)] and the 'split probability' reading on random ranked class pairs.
Prints the largest discrepancy found. No assertions."""
import numpy as np

rng = np.random.default_rng(12345)


def random_classes(n_atoms=8, scale=6.0):
    # monotone coupling: theta_H = theta_L + nonnegative increment, same probabilities
    q = rng.dirichlet(np.ones(n_atoms))
    aL = np.sort(rng.uniform(0.6, scale, n_atoms))
    inc = rng.exponential(1.0, n_atoms) * (rng.uniform(size=n_atoms) < 0.7)
    aH = aL + inc
    return q, aL, aH


def Dfun(y, q, aL, aH):
    y = np.atleast_1d(y)[:, None]
    GL = (q[None, :] * (aL[None, :] <= y)).sum(1)
    GH = (q[None, :] * (aH[None, :] <= y)).sum(1)
    return GL - GH


def uniform_cdf(r):
    return lambda x: np.clip(x / r, 0, 1)


def trunc_exp_cdf(scale, top):
    z = 1 - np.exp(-top / scale)
    return lambda x: np.clip((1 - np.exp(-np.clip(x, 0, top) / scale)) / z, 0, 1)


def shifted_uniform_cdf(a, w):
    return lambda x: np.clip((x - a) / w, 0, 1)


worst = 0.0
worst_split = 0.0
for trial in range(300):
    q, aL, aH = random_classes()
    which = rng.integers(3)
    if which == 0:
        r = rng.uniform(1.0, 12.0)
        F = uniform_cdf(r)
        lo, hi = 0.0, r
    elif which == 1:
        a, w = rng.uniform(0.0, 6.0), rng.uniform(0.5, 6.0)
        F = shifted_uniform_cdf(a, w)
        lo, hi = a, a + w
    else:
        scale, top = rng.uniform(0.5, 4.0), rng.uniform(3.0, 14.0)
        F = trunc_exp_cdf(scale, top)
        lo, hi = 0.0, top
    # W_j = sum_a q_a F(a)  (exact since classes are discrete)
    WL = (q * F(aL)).sum()
    WH = (q * F(aH)).sum()
    # E_F[D(R)] by fine midpoint rule against the density dF
    ys = np.linspace(lo, hi, 400001)
    mid = 0.5 * (ys[1:] + ys[:-1])
    dF = F(ys[1:]) - F(ys[:-1])
    ED = (Dfun(mid, q, aL, aH) * dF).sum()
    worst = max(worst, abs((WH - WL) - ED))
    # split probability under the quantile coupling (probability that theta_L < R < theta_H)
    split = (q * (F(aH) - F(aL))).sum()
    worst_split = max(worst_split, abs(split - (WH - WL)))
print("largest |(W_H - W_L) - E_F[D]| over 300 random trials:", worst)
print("largest |split probability - (W_H - W_L)|:", worst_split)
