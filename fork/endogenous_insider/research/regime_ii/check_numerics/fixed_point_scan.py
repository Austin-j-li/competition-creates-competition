"""Search for pure-order equilibria (qH,-v) with half-line pool (-inf,x') at k=.02, rho=.25, r1=3.
For each fixed cutoff x' on a grid and each v on a grid (when the schedule is consistent), compute the low type's
global best response s*(v,x') and the high type's best response. A fixed point needs s* = v and qH* = qH.
We scan sign changes of s*-v along v at fixed x', refine by bisection, then verify with check().
Control: cL=3.0 must show the starved member."""
import csv, math, sys, time
from multiprocessing import Pool as MP
from scipy import optimize
from model import *
from random_tests import crossing

def consistent(P, a, qH, v, xp):
    oH, oL = ((qH, 1.0),), ((-v, 1.0),)
    zc = crossing(P, oH, oL, a.tauL)
    if zc == -math.inf:
        return xp is None
    if zc == math.inf:
        return False
    if xp < zc:
        return False
    return pool_belief(P, oH, oL, ((-math.inf, xp),)) < a.tauL

def sstar(P, qH, v, xp, ngrid=81):
    oH, oL = ((qH, 1.0),), ((-v, 1.0),)
    pool = ((-math.inf, xp),)
    pcs = entry_pieces(P, oH, oL, pool)
    q, u, _ = best_response(P, 'L', pcs, oH, oL, ngrid)
    return -q, u

def fiber(args):
    cL, xp, qH = args
    P = Prm(cL=cL, r=3.0, k=0.02, rho=0.25); a = auction(P)
    vs = [0.01 * i for i in range(0, 101)]
    out = []
    prev = None
    for v in vs:
        if not consistent(P, a, qH, v, xp):
            prev = None
            continue
        s, u = sstar(P, qH, v, xp)
        g = s - v
        if prev is not None and v < 0.995 and (prev[1] > 0) != (g > 0) and abs(g) < 0.9 and abs(prev[1]) < 0.9:
            out.append((cL, xp, qH, prev[0], v, prev[1], g))
        prev = (v, g)
    return out

if __name__ == "__main__":
    cLs = [float(c) for c in sys.argv[1].split(",")]
    qH = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    xps = [-1.0 + 0.01 * i for i in range(0, 251)]
    jobs = [(cL, xp, qH) for cL in cLs for xp in xps]
    t = time.time()
    with MP(4) as pool:
        res = pool.map(fiber, jobs)
    hits = [h for r in res for h in r]
    print("done %.0fs; sign changes: %d" % (time.time() - t, len(hits)))
    for h in hits:
        print(h)
    with open("fixed_point_scan_%s_%s.csv" % (sys.argv[1].replace(",", "_"), qH), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["cL", "xp", "qH", "v_lo", "v_hi", "g_lo", "g_hi"]); w.writerows(hits)
