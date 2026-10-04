"""Count local maxima of each type's payoff on random consistent schedules (1-2 atoms per type, random pools).
A mixed best response needs >= 2 global maxima of equal height, so zero schedules with 2+ local maxima rules out mixing
on the sample. Own generator (random_tests.draw)."""
import csv, math, random, sys
from multiprocessing import Pool as MP
from model import *
from random_tests import draw

def local_max_count(P, theta, pcs, oH, oL, n=161):
    qs = [-1 + 2 * i / (n - 1) for i in range(n)]
    us = [payoff(P, theta, q, pcs, oH, oL) for q in qs]
    cnt = 0
    for i in range(n):
        l = us[i - 1] if i > 0 else -1e9
        r = us[i + 1] if i < n - 1 else -1e9
        if us[i] > l + 1e-13 and us[i] >= r + 0.0 and us[i] > 1e-13 or (i in (0,) and False):
            cnt += 1
    # the zero order counts as a candidate only if it is a strict local max with value 0 (kink); handled by us[i]>1e-13 filter
    gmax = max(us)
    top = sum(1 for i in range(n) if us[i] > gmax - 1e-9)
    return cnt, gmax, top

def job(args):
    cL, seed, ndraw = args
    rng = random.Random(seed)
    P = Prm(cL=cL, r=3.0, k=0.02, rho=0.25); a = auction(P)
    res = []
    for _ in range(ndraw):
        d = draw(rng, P, a)
        if d is None:
            continue
        oH, oL, pool = d
        pcs = entry_pieces(P, oH, oL, pool)
        cH, gH, tH = local_max_count(P, 'H', pcs, oH, oL)
        cLm, gL, tL = local_max_count(P, 'L', pcs, oH, oL)
        res.append((cH, cLm, tH, tL))
    return cL, res

if __name__ == "__main__":
    cLs = [2.6, 2.8, 2.95, 2.98]
    jobs = [(cL, 100 * i + int(cL * 100), 60) for cL in cLs for i in range(4)]
    with MP(4) as p:
        out = p.map(job, jobs)
    rows = []
    for cL in cLs:
        allr = [r for c, rs in out if c == cL for r in rs]
        multi = sum(1 for r in allr if r[0] > 1 or r[1] > 1)
        print("cL=%.2f schedules=%d  with >=2 local maxima (H or L): %d ; max over types of ties at the top: %d" % (cL, len(allr), multi, max(max(r[2], r[3]) for r in allr)))
        rows.append(dict(cL=cL, schedules=len(allr), multi=multi))
    with open("mixed_audit.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
