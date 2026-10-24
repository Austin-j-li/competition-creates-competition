"""Hidden toehold: dominance check of the challenger's buy decision over the investor's mixing beta, and the investor's cost cutoff."""
import sys
from common import *
from toehold_hidden import *

kC = par.k
print("Gain of buying one unit for each challenger cost type, over beta in {0,.25,.5,.75,1}, (sL,sH) in {0,1}^2")
for r in [Fr(6, 5), Fr(3), Fr(18, 5), Fr(21, 5)]:
    A = auction(par, r)
    lo_cL, hi_cH = None, None
    for bq in [0, 1, 2, 3, 4]:
        beta = K(bq, 4)
        for sL in (0, 1):
            for sH in (0, 1):
                o = solve_profile(A, beta, sL, sH, kC)
                lo_cL = o['cL'] if lo_cL is None or o['cL'] < lo_cL else lo_cL
                hi_cH = o['cH'] if hi_cH is None or o['cH'] > hi_cH else hi_cH
    print(f"r={float(r)}: min over profiles of gain(c_L) = {mp.nstr(lo_cL,6)}  ;  max over profiles of gain(c_H) = {mp.nstr(hi_cH,6)}")

print("\nInvestor's gross gain per unit (gain + k) in the equilibrium profile with and without the hidden toehold (beta=1)")
for r in [Fr(3), Fr(18, 5), Fr(21, 5)]:
    A = auction(par, r)
    base = solve_profile(A, K(1), 0, 0, kC)
    hid = solve_profile(A, K(1), 1, 0, kC)
    print(f"r={float(r)}: baseline k_max={mp.nstr(base['gH']+par.k,8)}  hidden toehold k_max={mp.nstr(hid['gH']+par.k,8)}   prices base={[mp.nstr(p_,6) for p_ in base['price']]} hidden={[mp.nstr(p_,6) for p_ in hid['price']]}")

print("\nNo-trade cutoff at the weak strength with and without hidden toehold (beta=0): gross investor gain")
for r in [Fr(6, 5), Fr(3, 2)]:
    A = auction(par, r)
    base = solve_profile(A, K(0), 0, 0, kC)
    hid = solve_profile(A, K(0), 1, 0, kC)
    print(f"r={float(r)}: DT={mp.nstr(A['DT'],5)} baseline gross={mp.nstr(base['gH']+par.k,6)} hidden gross={mp.nstr(hid['gH']+par.k,6)}   (k={mp.nstr(par.k,4)})")
