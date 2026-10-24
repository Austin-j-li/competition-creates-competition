"""Public financial toehold s (truthful bids held fixed): entry gain B^s(mu) = B(mu) + s (wL + DT mu).

Prints: (i) window for Proposition 2 analog, (ii) information ceiling r_C(s), (iii) dB^s/dr sign,
(iv) outcomes at the prior for s in {0, .1, .2, .5}, (v) the target's optimal disclosure with a toehold.
"""
import sys
from common import *
import branch, pieces as pc

set_mode('hp')
par = P()
a = par.a
m1 = a / (1 + a)
M1 = 1 - m1
half = K(1, 2)
print("a =", mp.nstr(a, 10), " M1 =", mp.nstr(M1, 10))


def Bs(A, mu, s):
    return A['gL'] + s * A['wL'] + mu * ((A['gH'] - A['gL']) + s * A['DT'])


r0, r1, r2 = Fr(6, 5), Fr(3), Fr(18, 5)
A0, A1 = auction(par, r0), auction(par, r1)
print("\n(i) c_H window for the Prop. 2 analog: B^s_{r0}(1/2) < cH <= B^s_{r1}(M1)")
for s in [0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0]:
    ss = num(Fr(s).limit_denominator(1000))
    lo = Bs(A0, half, ss)
    hi = Bs(A1, M1, ss)
    print(f"  s={s:5.2f}: lower={mp.nstr(lo,8)}  upper={mp.nstr(hi,8)}  width={mp.nstr(hi-lo,6)}   c_H=5 admissible: {bool(lo < 5 <= hi)}")
# critical s at which the prior alone recruits at r0 (cH = 5)
s_crit = (par.cH - Bs(A0, half, 0)) / (A0['wL'] + A0['DT'] * half)
print("  s* with B^s_{r0}(1/2) = 5:", mp.nstr(s_crit, 8))

print("\n(ii) information ceiling r_C(s): largest r with B^s_r(M1) >= c_H (c_H = 5)")
for s in [0, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0]:
    ss = num(Fr(s).limit_denominator(1000))
    f = lambda r: Bs(auction(par, r), M1, ss) - par.cH
    lo, hi = K(3), K(99, 10)
    if f(hi) >= 0:
        print(f"  s={s:5.2f}: no ceiling below r=h (B^s_r(M1) >= cH for all r < 9.9)")
        continue
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) >= 0:
            lo = mid
        else:
            hi = mid
    print(f"  s={s:5.2f}: r_C = {mp.nstr(lo,8)}")

print("\n(iii) dB^s/dr at fixed mu, s in [0,1]: sign check on a grid (negative means deterrence survives)")
worst = None
for s in [0, 0.25, 0.5, 0.75, 1.0]:
    for mu in [0, 0.25, 0.5, 0.75, 1.0]:
        for r in [1.2, 2, 3, 5, 8]:
            h = mp.mpf('1e-20')
            fr = lambda x: Bs(auction(par, x), num(Fr(mu).limit_denominator(100)), num(Fr(s).limit_denominator(100)))
            rr = mp.mpf(r)
            d = (fr(rr + h) - fr(rr - h)) / (2 * h)
            worst = d if worst is None or d > worst else worst
print("  largest derivative found:", mp.nstr(worst, 6))

print("\n(iv) trading-stage outcomes at the prior 1/2 with toehold s (full buying selected if it exists)")
for r in [r0, r1, r2, Fr(21, 5), Fr(5)]:
    A = auction(par, r)
    for s in [0, 0.1, 0.2, 0.5]:
        ss = num(Fr(s).limit_denominator(1000))
        eqs, G0, G1 = branch.equilibria(par, A, half, ss)
        desc = '; '.join(f"{l}: E={mp.nstr(o['E'],5)} OH={mp.nstr(o['OH'],5)}" for l, o in eqs) or 'no pure eq'
        print(f"  r={float(r):.1f} s={s:3.1f} tau^s={mp.nstr(tau(par, A, ss),5)}: {desc}")

print("\n(v) optimal disclosure with a toehold (r = 3)")
for r in [Fr(3), Fr(21, 5)]:
    A = auction(par, r)
    for s in [0, 0.1, 0.2, 0.5, 1.0]:
        ss = num(Fr(s).limit_denominator(1000))
        pts, st, cs = pc.hull_points(par, A, 'inf', ss)
        if pts is None:
            print(f"  r={float(r)} s={s}: tau^s={mp.nstr(st['tau'],5)} not in (0,1)")
            continue
        hull = pc.upper_hull([(p[0], p[1], p[2], p[3], p[4]) for p in pts])
        val, v1, v2, w = pc.policy_at(hull, half)
        E = (1 - w) * v1[4]['E'] + w * v2[4]['E']
        print(f"  r={float(r)} s={s:3.1f}: tau^s={mp.nstr(st['tau'],5)} phi*={mp.nstr(v2[0],6)} w={mp.nstr(w,5)} E={mp.nstr(E,5)} Pi-t0={mp.nstr(val-A['t0'],6)}")
