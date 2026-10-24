"""For each incumbent strength: total length of priors with no pure equilibrium (cells labelled GAP) and cell count."""
from common import *
import pieces as pc

set_mode('hp')
par = P()
print("   r    GAP cells  total GAP length   first GAP cell")
for i in range(0, 161, 4):
    r = Fr(6, 5) + Fr(i, 20)
    A = auction(par, r)
    cs, st = pc.cells(par, A, 'inf')
    if cs is None:
        continue
    g = [c for c in cs if c['lab'] == 'GAP']
    tot = sum((c['hi'] - c['lo']) for c in g) if g else K(0)
    first = f"[{mp.nstr(g[0]['lo'],5)}, {mp.nstr(g[0]['hi'],5)}]" if g else ''
    print(f"{float(r):5.2f}  {len(g):6d}  {mp.nstr(tot,6):>14}   {first}")
