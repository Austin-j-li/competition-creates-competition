"""Print the branch-game equilibria on a grid of priors, for several incumbent strengths (hp mode)."""
import sys
from common import *
import branch

set_mode('hp')
par = P()
a = par.a
print('a =', mp.nstr(a, 12))
for r in [Fr(6, 5), Fr(3), Fr(18, 5), Fr(21, 5)]:
    A = auction(par, r)
    tau_r = tau(par, A)
    T = tau_r / (1 - tau_r) if tau_r < 1 else mp.inf
    print(f"\nr={float(r)}  DT={mp.nstr(A['DT'],6)} wL={mp.nstr(A['wL'],6)} gH={mp.nstr(A['gH'],6)} gL={mp.nstr(A['gL'],6)}  tau={mp.nstr(tau_r,8)}  T={mp.nstr(T,8)}  aT={mp.nstr(a*T,6)} T/a={mp.nstr(T/a,6)}")
    for i in range(1, 20):
        phi = K(i, 20)
        eqs, G0, G1 = branch.equilibria(par, A, phi)
        desc = '; '.join(f"{lab}: E={mp.nstr(o['E'],6)} OH={mp.nstr(o['OH'],6)} Pi-t0={mp.nstr(o['Pi']-A['t0'],6)}" for lab, o in eqs)
        print(f"phi={float(phi):.2f} G0={mp.nstr(G0,5):>9} G1={mp.nstr(G1,5):>9} | {desc if desc else 'NO PURE EQ'}")
