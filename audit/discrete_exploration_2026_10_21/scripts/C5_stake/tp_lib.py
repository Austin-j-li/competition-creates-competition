"""Exact (rational) library for the three-point stake model. Print-only users import this file.

Model: noise Z in {-1,0,1}, each with probability 1/3. Orders q in {0,1} (buy-only).
Flow X = q + Z. The investor holds a stake omega. Payoff: omega*V_T + q*(V_T - P(X)) - k*q.
The challenger sees the price only. Low cost c_L = 0 (entry floor rho at every belief).
All numbers are fractions.Fraction. No assertions.
"""
from fractions import Fraction as F

BENCH = dict(h=F(10), l=F(1), p=F(1, 2), rho=F(1, 4), cL=F(0), cH=F(6), k=F(1, 50))
R0, R1, R2 = F(6, 5), F(3), F(18, 5)


def auction(r, par=BENCH):
    h, l, p = par["h"], par["l"], par["p"]
    t0 = p * (1 - p / r)
    tH = r / 2 + p * p / (2 * r)
    tL = l - (l * l - p * p) / (2 * r)
    gH = h - tH
    gL = (l * l - p * p) / (2 * r)
    return dict(r=r, t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, D=tH - tL,
                wL=tL - t0, wH=tH - t0)


def B(a, mu):
    return a["gL"] + mu * (a["gH"] - a["gL"])


def tau_of(a, par=BENCH):
    return (par["cH"] - a["gL"]) / (a["gH"] - a["gL"])


def entry_from_phi(par, phi):
    """Average entry when the high-cost type prepares with probability phi (c_L = 0)."""
    return par["rho"] + (1 - par["rho"]) * phi


def phi_of_belief(a, par, mu):
    """Challenger rule: 1 if B(mu) > cH, 0 if <, None (free) if equal."""
    b = B(a, mu)
    if b > par["cH"]:
        return F(1)
    if b < par["cH"]:
        return F(0)
    return None


def flows(bH, bL):
    """Flow probabilities f_j(x) for x in -1,0,1,2 when type j buys with probability b_j."""
    third = F(1, 3)
    fH = {-1: (1 - bH) * third, 0: third, 1: third, 2: bH * third}
    fL = {-1: (1 - bL) * third, 0: third, 1: third, 2: bL * third}
    return fH, fL


def posterior(fH, fL, x):
    s = fH[x] + fL[x]
    if s == 0:
        return None
    return fH[x] / s


def payoffs(a, par, omega, bH, bL, e, mu):
    """First-principles payoffs of buying (q=1) and not buying (q=0) for each type.

    e: dict flow -> entry probability (average over cost). mu: dict flow -> belief used by the
    market maker. Returns dict j -> (U(0), U(1)).
    """
    k = par["k"]
    third = F(1, 3)
    price = {x: a["t0"] + e[x] * (a["wL"] + a["D"] * mu[x]) for x in (-1, 0, 1, 2)}
    out = {}
    for j, w in (("H", a["wH"]), ("L", a["wL"])):
        res = {}
        for q in (0, 1):
            u = F(0)
            for z in (-1, 0, 1):
                x = q + z
                vt = a["t0"] + e[x] * w  # E[V_T | type j, flow x]
                u += third * (omega * vt + q * (vt - price[x]))
            res[q] = u - k * q
        out[j] = (res[0], res[1])
    return out


def regrets(bH, bL, pay):
    """Regret of each type at mixing probabilities (bH, bL): value lost versus the best action."""
    reg = {}
    for j, bj in (("H", bH), ("L", bL)):
        u0, u1 = pay[j]
        best = max(u0, u1)
        cur = bj * u1 + (1 - bj) * u0
        reg[j] = best - cur
    return reg


def gains(pay):
    return {j: pay[j][1] - pay[j][0] for j in pay}
