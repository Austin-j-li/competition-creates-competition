"""Starved existence threshold: lowest cL at which a starved member exists, at several k.
The infimum of the pool belief over the family is attained as v -> vH with x'(v) from the L-FOC.
Threshold: cL such that B(pool belief at the limit) = cL."""
import csv
from scipy import optimize
from model import *
from starved import member

def inf_belief(P):
    a = auction(P); vH = P.b * logit(a.tauH) - 1
    m = member(P, vH - 1e-7)
    return m['pool_belief'], m['xp']

def thr(k, rho=0.25, r=3.0):
    def g(cL):
        P = Prm(cL=cL, r=r, k=k, rho=rho)
        pb, xp = inf_belief(P)
        return auction(P).tauL - pb     # member exists iff pool belief < tauL
    return optimize.brentq(g, 2.37, 4.28, xtol=1e-9)

if __name__ == "__main__":
    rows = []
    theory = {0.0224: 2.8326, 0.02: 2.9844, 0.015: 3.3954, 0.01: 3.7831, 0.0075: 3.9367}
    for k, t in theory.items():
        c = thr(k)
        P = Prm(cL=c, r=3.0, k=k)
        pb, xp = inf_belief(P)
        print("k=%.4f threshold=%.6f (theory %.4f, diff %.1e) limit x'=%.4f pool belief=%.6f" % (k, c, t, c - t, xp, pb))
        rows.append(dict(k=k, thr=c, theory=t, diff=c - t, xp=xp, pool_belief=pb))
    with open("starved_thr.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
