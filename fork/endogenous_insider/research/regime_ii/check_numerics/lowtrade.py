"""Low-trade family: orders (q,-q), no expensive entry. k as function of q for the symmetric schedule, then global check."""
import math, csv
from scipy import optimize
from model import *
from random_tests import crossing

def sym_profile(P, q):
    a = auction(P)
    oH, oL = ((q, 1.0),), ((-q, 1.0),)
    zc = crossing(P, oH, oL, a.tauL)
    pool = () if zc == -math.inf else ((-math.inf, zc),)
    return oH, oL, pool, zc

def marg_L(P, q, h=1e-6):
    oH, oL, pool, zc = sym_profile(P, q)
    pcs = entry_pieces(P, oH, oL, pool)
    up = payoff(P, 'L', -(q + h), pcs, oH, oL) + P.k * (q + h)
    dn = payoff(P, 'L', -(q - h), pcs, oH, oL) + P.k * (q - h)
    return (up - dn) / (2 * h)

if __name__ == "__main__":
    P0 = Prm(r=3.0, k=0.02, rho=0.25)
    a0 = auction(P0)
    print("no-trade bound rho*DT/2 =", P0.rho * a0.DT / 2)
    rows = []
    for cL in (2.4, 2.6, 2.8):
        P = with_(P0, cL=cL)
        for q in (0.05, 0.3, 0.5, 0.7, 0.8, 0.862, 0.87):
            oH, oL, pool, zc = sym_profile(P, q)
            print("cL=%.2f q=%.3f  k=m(q)=%.5f  pool=%s" % (cL, q, marg_L(P, q), "none" if not pool else "(-inf,%.3f)" % zc))
    # global check at k=m(q)
    for cL, q in ((2.4, 0.5), (2.4, 0.8), (2.6, 0.6), (2.8, 0.7)):
        P = with_(P0, cL=cL); k = marg_L(P, q); Pk = with_(P, k=k)
        oH, oL, pool, zc = sym_profile(Pk, q)
        r = check(Pk, oH, oL, pool, ngrid=401)
        print("cL=%.2f q=%.2f k=%.5f accepted=%s E=%.6f OH=%.6f regH=%.1e regL=%.1e brH=%.4f brL=%.4f" % (cL, q, k, r['accepted'], r['E'], r['OH'], r['regret_H'], r['regret_L'], r['br_H'], r['br_L']))
        rows.append(dict(cL=cL, q=q, k=k, accepted=r['accepted'], E=r['E'], OH=r['OH'], regH=r['regret_H'], regL=r['regret_L']))
    with open('lowtrade.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
