"""Exact objects of the no-sale buyer-mixing branch with recruitment only at x = 2 (theta > 1/3).

On profiles (A, 0) with entry (rho, rho, rho, rho, 1) at x = (-2, ..., 2), the purchase payoff per unit
Delta is
    K2(A) = rho [theta (1 - mu_0) + phi (1 - mu_1)] + theta (1 - mu_2),
    1 - mu_0 = L0 / (2 L0 - A d),  1 - mu_1 = L1 / (2 L1 + A d),  1 - mu_2 = c / (2c + A).
The branch is A(r) solving K2(A) = k / Delta(r) with A_2(r) < A < lam, where A_2(r) = c q(r) and
q = (2 tau - 1)/(1 - tau) is the recruitment threshold at x = 2.
Functions accept rationals or rational intervals (class Iv). Nothing here prints.
"""
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from t6_core import Iv, is_iv, sign_of  # noqa: E402

RHO, K, H, ELL, PR, CH = F(1, 4), F(1, 50), F(10), F(1), F(1, 2), F(6)


def auc(r):
    gH = H - r / 2 - PR * PR / (2 * r)
    gL = (ELL * ELL - PR * PR) / (2 * r)
    D = (r - ELL) ** 2 / (2 * r)
    tau = (CH - gL) / (gH - gL)
    return D, tau


def consts(lam, beta, theta):
    c = (1 - lam) * beta
    ph = 1 - 2 * theta
    d = ph - theta
    L0 = 2 * c * theta + (1 - 2 * c) * ph
    L1 = c * ph + (1 - 2 * c) * theta
    return c, ph, d, L0, L1


def K2(lam, beta, theta, A, e2=1):
    c, ph, d, L0, L1 = consts(lam, beta, theta)
    return RHO * (theta * L0 / (2 * L0 - A * d) + ph * L1 / (2 * L1 + A * d)) + theta * e2 * c / (2 * c + A)


def K2_prime(lam, beta, theta, A, e2=1):
    c, ph, d, L0, L1 = consts(lam, beta, theta)
    return RHO * (theta * L0 * d / (2 * L0 - A * d) ** 2 - ph * L1 * d / (2 * L1 + A * d) ** 2) \
        - theta * e2 * c / (2 * c + A) ** 2


def q_of(r):
    _, tau = auc(r)
    return (2 * tau - 1) / (1 - tau)


def A2(lam, beta, theta, r):
    c = consts(lam, beta, theta)[0]
    return c * q_of(r)


def kappa(r):
    D, _ = auc(r)
    return K / D


def gL_noside(lam, beta, theta, A):
    """Sale payoff per unit Delta under (A, 0) with entry rho at x = -2, -1, 0."""
    c, ph, d, L0, L1 = consts(lam, beta, theta)
    mu0 = (L0 - A * d) / (2 * L0 - A * d)
    mum1 = (L1 - A * theta) / (2 * L1 - A * theta)
    return RHO * (theta * mu0 + ph * mum1 + theta * F(1, 2))


def posts(lam, beta, theta, A):
    c, ph, d, L0, L1 = consts(lam, beta, theta)
    return {2: (c + A) / (2 * c + A), 1: (L1 + A * d) / (2 * L1 + A * d), 0: (L0 - A * d) / (2 * L0 - A * d),
            -1: (L1 - A * theta) / (2 * L1 - A * theta), -2: F(1, 2)}


def bisect_r(fun, lo, hi, width=F(1, 10 ** 13)):
    """Rational bracket [l, u] of a sign change of fun on [lo, hi] (exact signs at the endpoints)."""
    flo, fhi = sign_of(fun(lo)), sign_of(fun(hi))
    if flo == fhi or 0 in (flo, fhi):
        return None, (flo, fhi)
    while hi - lo > width:
        m = (lo + hi) / 2
        fm = sign_of(fun(m))
        if fm == 0:
            return (m, m), (flo, fhi)
        if fm == flo:
            lo = m
        else:
            hi = m
    return (lo, hi), (flo, fhi)


def r_A(lam, beta, theta, lo=F(3, 2), hi=F(8, 5)):
    """Start of the branch: K2(A_2(r)) = kappa(r)."""
    return bisect_r(lambda r: K2(lam, beta, theta, A2(lam, beta, theta, r)) - kappa(r), lo, hi)


def r_F(lam, beta, theta, lo=F(3, 2), hi=F(17, 10)):
    """Full purchase: K2(lam) = kappa(r)."""
    return bisect_r(lambda r: K2(lam, beta, theta, lam) - kappa(r), lo, hi)


def root_A(lam, beta, theta, r, width=F(1, 2 ** 80)):
    """Bracket of the branch rate A(r) in (A_2(r), lam) by exact payoff signs, or None."""
    lo, hi = A2(lam, beta, theta, r), lam
    f = lambda a: K2(lam, beta, theta, a) - kappa(r)  # noqa: E731
    slo, shi = sign_of(f(lo)), sign_of(f(hi))
    if not (slo > 0 and shi < 0):
        return None, (slo, shi)
    while hi - lo > width:
        m = (lo + hi) / 2
        if sign_of(f(m)) > 0:
            lo = m
        else:
            hi = m
    return (lo, hi), (slo, shi)
