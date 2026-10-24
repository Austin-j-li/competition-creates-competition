"""High-precision library for the discrete-Laplace stake model (mpmath; print only users import this).

Noise Z = G1 - G2, P(Z = z) = (1-a)/(1+a) a^|z|, a = exp(-1/b). Orders q in {0,1} (buy-only).
Flow X = q + Z takes every integer value. Every flow x >= 1 has one posterior and every flow
x <= 0 has another, for every mixing pair (bH, bL): the model is a good-news / bad-news model.
"""
from mpmath import mp, mpf, exp

mp.dps = 60

BENCH = dict(h=mpf(10), l=mpf(1), p=mpf(1) / 2, rho=mpf(1) / 4, cL=mpf(0), cH=mpf(5), k=mpf(1) / 50, b=mpf(2))
R0, R1, R2, R_END = mpf(6) / 5, mpf(3), mpf(21) / 5, mpf(4)


def auction(r, par=BENCH):
    h, l, p = par["h"], par["l"], par["p"]
    t0 = p * (1 - p / r)
    tH = r / 2 + p * p / (2 * r)
    tL = l - (l * l - p * p) / (2 * r)
    gH = h - tH
    gL = (l * l - p * p) / (2 * r)
    return dict(r=r, t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, D=tH - tL, wL=tL - t0, wH=tH - t0)


def tau_of(a, par=BENCH):
    return (par["cH"] - a["gL"]) / (a["gH"] - a["gL"])


def noise_pmf(z, par=BENCH):
    aa = exp(-1 / par["b"])
    return (1 - aa) / (1 + aa) * aa ** abs(z)


def good_news_probs(bH, bL, par=BENCH):
    """Pr(X >= 1 | type) when the type buys with probability b_j: (a + b_j (1-a)) / (1+a)."""
    aa = exp(-1 / par["b"])
    return (aa + bH * (1 - aa)) / (1 + aa), (aa + bL * (1 - aa)) / (1 + aa)


def posteriors(bH, bL, par=BENCH):
    """(M, m): posterior after good news (x >= 1) and bad news (x <= 0)."""
    gH, gL = good_news_probs(bH, bL, par)
    M = gH / (gH + gL)
    m = (1 - gH) / (2 - gH - gL)
    return M, m


def check_reduction_by_summation(bH, bL, par=BENCH, span=120):
    """Return (M_sum, m_sum, max flow-posterior deviation) from direct summation over flows."""
    M_vals, m_vals = [], []
    gHs = mpf(0)
    gLs = mpf(0)
    for x in range(-span, span + 1):
        fH = bH * noise_pmf(x - 1, par) + (1 - bH) * noise_pmf(x, par)
        fL = bL * noise_pmf(x - 1, par) + (1 - bL) * noise_pmf(x, par)
        mu = fH / (fH + fL)
        (M_vals if x >= 1 else m_vals).append(mu)
    return min(M_vals), max(M_vals), min(m_vals), max(m_vals)
