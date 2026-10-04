"""Forcing level for pure order schedules with half-line pools (referee version).
For a consistent schedule (oH,oL,pool) define m = min over s in [0,1] and both types of d/ds [s F_theta(s)].
If k < m the full order is strictly preferred to every partial order, so the schedule can only be an
equilibrium with full orders. k_pure = inf of m over non-full schedules."""
import csv, math, sys
from scipy import optimize
from model import *
from random_tests import crossing

def marg(P, theta, s, pcs, oH, oL, h=1e-5):
    sg = 1.0 if theta == 'H' else -1.0
    up = payoff(P, theta, sg * (s + h), pcs, oH, oL) + P.k * (s + h)
    dn = payoff(P, theta, sg * max(s - h, 1e-9), pcs, oH, oL) + P.k * max(s - h, 1e-9)
    return (up - dn) / ((s + h) - max(s - h, 1e-9))

def schedule_min(P, qH, qL, pool, ss=(0.0, 0.1, 0.25, 0.4, 0.55, 0.7, 0.8, 0.9, 1.0)):
    oH, oL = ((qH, 1.0),), ((qL, 1.0),)
    pcs = entry_pieces(P, oH, oL, pool)
    best = 1e9; arg = None
    for th in ('H', 'L'):
        for s in ss:
            if s == 0.0:
                continue
            m = marg(P, th, s, pcs, oH, oL)
            if m < best:
                best, arg = m, (th, s)
    return best, arg

def consistent_cutoffs(P, a, qH, qL, n=3):
    """List of pools (-inf,x') that are consistent for pure orders; returns [] if no pool-consistent schedule."""
    oH, oL = ((qH, 1.0),), ((qL, 1.0),)
    zc = crossing(P, oH, oL, a.tauL)
    if zc == -math.inf:
        return [()]            # posterior never below tauL: pool-free continuation
    if zc == math.inf:
        return []
    pb = lambda c: pool_belief(P, oH, oL, ((-math.inf, c),)) - a.tauL
    if pb(zc + 1e-12) >= 0:
        return []
    top = 40.0 if pb(40.0) < 0 else optimize.brentq(pb, zc, 40.0, xtol=1e-12) - 1e-9
    return [((-math.inf, zc + t * (top - zc)),) for t in [0.0, 0.5, 1.0][:n]] if top > zc else []

def kpure(P, qHs, qLs):
    a = auction(P)
    best = (1e9, None)
    for qH in qHs:
        for qL in qLs:
            if qH == 1.0 and qL == -1.0:
                continue
            if qH == 0.0 and qL == 0.0:
                continue
            for pool in consistent_cutoffs(P, a, qH, qL):
                m, arg = schedule_min(P, qH, qL, pool)
                if m < best[0]:
                    best = (m, (qH, qL, pool, arg))
    return best

if __name__ == "__main__":
    P0 = Prm(r=3.0, k=0.02, rho=0.25)
    qHs = [1.0, 0.8, 0.6, 0.4]
    qLs = [-1.0 + 0.05 * i for i in range(0, 21)]
    rows = []
    for cL in (2.37, 2.45, 2.55, 2.65, 2.75, 2.95):
        m, info = kpure(with_(P0, cL=cL), qHs, qLs)
        print("cL=%.2f k_pure=%.5f at qH=%.2f qL=%.2f pool=%s arg=%s" % (cL, m, info[0], info[1], [(round(l,3) if l!=-math.inf else '-inf', round(h,3)) for l,h in info[2]], info[3]), flush=True)
        rows.append(dict(cL=cL, kpure=m, qH=info[0], qL=info[1]))
    with open('forcing_map.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
