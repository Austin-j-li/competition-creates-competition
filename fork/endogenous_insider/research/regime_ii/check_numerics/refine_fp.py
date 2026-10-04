"""Refine L-fixed points found by fixed_point_scan and test the high type (full joint fixed point)."""
import csv, math, sys
from scipy import optimize
from model import *
from fixed_point_scan import sstar, consistent

def refine(cL, xp, qH, vlo, vhi):
    P = Prm(cL=cL, r=3.0, k=0.02, rho=0.25)
    g = lambda v: sstar(P, qH, v, xp)[0] - v
    v = optimize.brentq(g, vlo, vhi, xtol=1e-10)
    oH, oL = ((qH, 1.0),), ((-v, 1.0),)
    pool = ((-math.inf, xp),)
    pcs = entry_pieces(P, oH, oL, pool)
    qHb, uH, _ = best_response(P, 'H', pcs, oH, oL, 201)
    r = check(P, oH, oL, pool, ngrid=201)
    return dict(cL=cL, xp=xp, qH=qH, v=v, brH=qHb, regret_H=r['regret_H'], regret_L=r['regret_L'],
                accepted=r['accepted'], pool_belief=r['pool_belief'], tauL=r['tauL'], E=r['E'], OH=r['OH'])

if __name__ == "__main__":
    rows = []
    cands = []
    for fn in sys.argv[1:]:
        for row in csv.DictReader(open(fn)):
            cands.append((float(row['cL']), float(row['xp']), float(row['qH']), float(row['v_lo']), float(row['v_hi'])))
    seen = set()
    for cL, xp, qH, vlo, vhi in cands:
        key = (round(cL, 4), round(xp, 4), qH)
        if key in seen:
            continue
        seen.add(key)
        try:
            r = refine(cL, xp, qH, vlo, vhi)
        except Exception as e:
            print("skip", key, e); continue
        rows.append(r)
        print("cL=%.3f x'=%.3f qH=%.2f -> v=%.5f  brH=%.4f  acc=%s  belief %.5f/%.5f  E=%.5f regH=%.1e regL=%.1e"
              % (r['cL'], r['xp'], r['qH'], r['v'], r['brH'], r['accepted'], r['pool_belief'], r['tauL'], r['E'], r['regret_H'], r['regret_L']), flush=True)
    with open('refine_fp.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
