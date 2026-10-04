"""Starved family (1,-v) with half-line pool (-inf,x'), found by the L-type first-order condition,
then every member is checked by global best response of both types. Independent of the other tracks."""
import csv, math, sys
from scipy import optimize
from model import *

def UL_prime(P, v, xp, h=2e-5):
    oH, oL = ((1.0, 1.0),), ((-v, 1.0),)
    pool = ((-math.inf, xp),)
    pcs = entry_pieces(P, oH, oL, pool)
    u1 = payoff(P, 'L', -(v + h), pcs, oH, oL)
    u0 = payoff(P, 'L', -(v - h), pcs, oH, oL)
    return (u1 - u0) / (2 * h)   # d/ds with s=-q

def xprime_of_v(P, v):
    g = lambda xp: UL_prime(P, v, xp)
    try:
        return optimize.brentq(g, 0.0, 8.0, xtol=1e-12)
    except ValueError:
        return None

def member(P, v):
    xp = xprime_of_v(P, v)
    if xp is None:
        return None
    a = auction(P)
    pb = F(xp - 1, P.b) / (F(xp - 1, P.b) + F(xp + v, P.b))
    muX = f(xp - 1, P.b) / (f(xp - 1, P.b) + f(xp + v, P.b))
    return dict(v=v, xp=xp, pool_belief=pb, mu_at_xp=muX)

if __name__ == "__main__":
    P0 = Prm(r=3.0, k=0.02, rho=0.25)
    a = auction(P0)
    vH = P0.b * logit(a.tauH) - 1
    print("v_H", vH)
    # existence threshold: inf over v of B(pool belief) as v -> v_H
    for v in (0.5, 0.6, 0.7, 0.73, 0.74, vH - 1e-4, vH - 1e-6):
        m = member(P0, v)
        print(v, m, "B(pool belief)=%.5f" % B(P0, m['pool_belief']), "B(mu_xp)=%.5f" % B(P0, m['mu_at_xp']))
