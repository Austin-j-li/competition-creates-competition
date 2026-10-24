"""Scan priors for (i) no pure equilibrium (GAP) and (ii) interior-beta equilibria (G(beta)=0), at benchmark strengths."""
import sys
from common import *
import branch, pieces as pc

set_mode('hp')
par = P()
for r in [Fr(6, 5), Fr(3, 2), Fr(3), Fr(18, 5), Fr(21, 5)]:
    A = auction(par, r)
    gaps, mixed = [], []
    N = 400
    for i in range(0, N + 1):
        phi = K(i, N)
        eqs, G0, G1 = branch.equilibria(par, A, phi)
        if not eqs:
            gaps.append(float(phi))
        roots = branch.mixed_roots(par, A, phi, 0, 200)
        if roots:
            mixed.append((float(phi), [mp.nstr(x, 5) for x in roots]))
    print(f"r={float(r)}: priors without a pure equilibrium: {len(gaps)} of {N+1}", ('range [%.4f, %.4f]' % (gaps[0], gaps[-1])) if gaps else '')
    print(f"   priors with an interior-beta root of G: {len(mixed)}", mixed[:6])
