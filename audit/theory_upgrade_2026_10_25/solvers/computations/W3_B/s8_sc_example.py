"""Targeted search: benchmark classes, reserve, k, rho, beta; vary c_H, a, lbar. Look for
(i) recruitment exit before the cap while J still rises; (ii) two separate recruiting segments."""
import sys, math
sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W3_B')
from model import *

def profile(P, rlo, rhi, n=4000):
    rs = [rlo + i*(rhi-rlo)/n for i in range(n+1)]
    rows = []
    for r in rs:
        A = auction(P, r)
        ok = 0.5 < A['tau'] < 1 and A['Delta'] > 2*P.k
        if not ok:
            rows.append((r, False, False, A, None)); continue
        Ls = Lam_star(A['Delta'], P); lam = min(P.lbar, Ls)
        rows.append((r, M_of(lam, P) >= A['tau'], Ls >= P.lbar, A, lam))
    segs = []; cur = None
    for (r, rec, capd, A, lam) in rows:
        if rec and cur is None: cur = dict(start=r, end=r, cap=capd, Jrise_at_end=None)
        elif rec: cur['end'] = r; cur['cap'] = cur['cap'] or capd
        elif cur is not None: segs.append(cur); cur = None
    if cur: segs.append(cur)
    return rows, segs

hits = []
for cH in [3 + 0.25*i for i in range(25)]:
    for a in [0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.2, 2.0]:
        P = Par(h=10, ell=1, p=0.5, cH=cH, k=0.02, rho=0.25, beta=0.3, a=a, lbar=0.9)
        rows, segs = profile(P, 1.05, 9.95, 1800)
        for sg in segs:
            if not sg['cap'] and sg['end'] < 9.9:
                # J rising at the exit?
                i = next(j for j, row in enumerate(rows) if row[0] >= sg['end'])
                J0, J1 = rows[i-1][3]['J'], rows[i+1][3]['J']
                if J1 > J0:
                    hits.append((cH, a, sg['start'], sg['end'], len(segs)))
        if len(segs) > 1:
            print("TWO SEGMENTS: cH=%.2f a=%.2f" % (cH, a), [(round(s['start'],3), round(s['end'],3), s['cap']) for s in segs])
print("exit-before-cap with J rising (cH, a, start, end, #segments):")
for h_ in hits[:12]:
    print("   ", tuple(round(x,4) if isinstance(x,float) else x for x in h_))
print("count", len(hits))
