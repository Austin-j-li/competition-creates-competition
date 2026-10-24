"""Shared exact objects for the N2 dynamics scripts.

Benchmark of the paper (point masses, prior 1/2): h = 10, l = 1, p = 1/2, rho = 1/4, c_L = 0, c_H = 6,
k = 1/50. Incumbent value R ~ U[0, r]. All economic quantities are fractions.Fraction.
Module only: it prints nothing when imported.
"""
from fractions import Fraction as F

H, L, P, RHO, CH, K, PI = F(10), F(1), F(1, 2), F(1, 4), F(6), F(1, 50), F(1, 2)
R0, R1, R2 = F(6, 5), F(3), F(18, 5)
MID = (F(31, 20), F(8, 5), F(33, 20))


def objects(r):
    """Closed forms of TEAM_RULES section 3 (paper equation (4))."""
    r = F(r)
    t0 = P * (1 - P / r)
    tH = r / 2 + P * P / (2 * r)
    tL = L - (L * L - P * P) / (2 * r)
    gH = H - r / 2 - P * P / (2 * r)
    gL = (L * L - P * P) / (2 * r)
    D = tH - tL
    return dict(r=r, t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, D=D, wH=tH - t0, wL=tL - t0,
                tau=(CH - gL) / (gH - gL))


def direct_objects(r):
    """The same objects by direct integration over R ~ U[0, r] (a check of the closed forms)."""
    r = F(r)

    def expect(pieces):
        tot = F(0)
        for lo, hi, a, b in pieces:
            lo2, hi2 = max(lo, F(0)), (r if hi is None else min(hi, r))
            if hi2 > lo2:
                tot += a * (hi2 - lo2) + b * (hi2 * hi2 - lo2 * lo2) / 2
        return tot / r

    t0 = expect([(P, None, P, F(0))])

    def t(th):
        return expect([(F(0), P, P, F(0)), (P, th, F(0), F(1)), (th, None, th, F(0))])

    def g(th):
        return expect([(F(0), P, th - P, F(0)), (P, th, th, F(-1))])

    return dict(t0=t0, tH=t(H), tL=t(L), gH=g(H), gL=g(L))


def B(o, mu):
    return o["gL"] + mu * (o["gH"] - o["gL"])


def entry(o, mu, zeta_at_tie=F(1)):
    """Entry e(mu) = rho + (1 - rho) 1{B(mu) >= c_H}; tie rule C1 by default (prepare at indifference)."""
    b = B(o, mu)
    if b > CH:
        return F(1)
    if b < CH:
        return RHO
    return RHO + (1 - RHO) * zeta_at_tie


def odds_to_mu(z):
    return z / (1 + z)


def mu_to_odds(m):
    return m / (1 - m)


def dec(x, n=10):
    return f"{float(x):.{n}f}"


def head(text):
    print()
    print("=" * 96)
    print(text)
    print("=" * 96)
