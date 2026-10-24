"""Consolidated tables for the memo (hp mode, b = 2, benchmark values, c_H = 5, pi = 1/2)."""
from common import *
import branch, pieces as pc

set_mode('hp')
par = P()
a, rho, k = par.a, par.rho, par.k
half = K(1, 2)
print("Table A. No disclosure, full disclosure (d = 1), symmetric d = 0.55, optimal two-point policy.")
print(" r    t0      DT      tau    phi_aT  phi_T/a | none: E, O_H, Pi-t0 | full: E, O_H, Pi-t0 | d=.55: E, O_H, Pi-t0 | opt: phi*, w, E, O_H, Pi-t0 | Pi (levels) none / opt")
for r in [Fr(6, 5), Fr(3), Fr(18, 5), Fr(21, 5)]:
    A = auction(par, r)
    st = pc.structure(par, A)
    def sym(d):
        res = []
        for ph in (d, 1 - d):
            eqs, G0, G1 = branch.equilibria(par, A, ph)
            o = dict(eqs)['FB'] if len(eqs) == 2 else eqs[0][1]
            res.append(o)
        return [(res[0][x] + res[1][x]) / 2 for x in ('E', 'OH', 'Pi')]
    eqs = branch.equilibria(par, A, half)[0]
    ob = dict(eqs)['FB'] if len(eqs) == 2 else eqs[0][1]
    fd = sym(K(1))
    d55 = sym(K(55, 100))
    pts, st, cs = pc.hull_points(par, A, 'inf')
    hull = pc.upper_hull([(p[0], p[1], p[2], p[3], p[4]) for p in pts])
    val, v1, v2, w = pc.policy_at(hull, half)
    E = (1 - w) * v1[4]['E'] + w * v2[4]['E']
    OH = (1 - w) * v1[4]['OH'] + w * v2[4]['OH']
    f = lambda x, n=5: mp.nstr(x, n)
    print(f"{float(r):4.1f} {f(A['t0'])} {f(A['DT'])} {f(st['tau'])} {f(st['thr']['aT'])} {f(st['thr']['Ta'])} | {f(ob['E'])} {f(ob['OH'])} {f(ob['Pi']-A['t0'])} | {f(fd[0])} {f(fd[1])} {f(fd[2]-A['t0'])} | {f(d55[0])} {f(d55[1])} {f(d55[2]-A['t0'])} | {f(v2[0],6)} {f(w)} {f(E)} {f(OH)} {f(val-A['t0'])} | {f(ob['Pi'])} / {f(val)}")

print("\nTable B. Does the investor still trade in the pooled branch? Gross gain per unit (G1 + k) at phi*, and at the prior 1/2 without disclosure.")
for r in [Fr(3), Fr(18, 5), Fr(21, 5), Fr(5), Fr(7)]:
    A = auction(par, r)
    st = pc.structure(par, A)
    phi_star = st['thr']['Ta']
    g_star = branch.gain_buy(par, A, phi_star, K(1))[0] + k
    g_half = branch.gain_buy(par, A, half, K(1))[0] + k
    print(f"r={float(r):.1f}: k_max at phi*={mp.nstr(g_star,6)}   k_max at prior 1/2 (no disclosure)={mp.nstr(g_half,6)}   k={mp.nstr(k,3)}")

print("\nTable C. Market-undoing premium: persuaded mass with the market (phi* = phi_T/a) vs without trading (phi* = tau).")
for r in [Fr(2), Fr(3), Fr(18, 5), Fr(21, 5)]:
    A = auction(par, r)
    st = pc.structure(par, A)
    w_m = half / st['thr']['Ta']
    w_0 = half / st['tau']
    print(f"r={float(r):.1f}: w with market={mp.nstr(w_m,5)}  w without market={mp.nstr(w_0,5)}  entry with={mp.nstr(rho+(1-rho)*w_m,5)} without={mp.nstr(rho+(1-rho)*w_0,5)}")

print("\nTable D. Fixed symmetric signal, entry by incumbent strength (market responds).")
print(" d     E(r=1.2)  E(r=3.0)  E(r=3.6)  E(r=4.2)")
for dd in [500, 550, 600, 650, 700, 750, 900, 1000]:
    row = []
    for r in [Fr(6, 5), Fr(3), Fr(18, 5), Fr(21, 5)]:
        A = auction(par, r)
        d = K(dd, 1000)
        res = []
        for ph in (d, 1 - d):
            eqs = branch.equilibria(par, A, ph)[0]
            o = dict(eqs)['FB'] if len(eqs) == 2 else eqs[0][1]
            res.append(o['E'])
        row.append((res[0] + res[1]) / 2)
    print(f"{dd/1000:.3f}  " + "  ".join(f"{mp.nstr(x,6):>8}" for x in row))

print("\nTable E. Information ceilings (c_H = 5): market-only B_r(M1) >= c_H; full disclosure g_H(r) >= c_H.")
f1 = lambda r: Bgain(auction(par, r), 1 / (1 + a)) - par.cH
lo, hi = K(3), K(5)
for _ in range(200):
    mid = (lo + hi) / 2
    if f1(mid) >= 0:
        lo = mid
    else:
        hi = mid
print("  market-only ceiling r_C =", mp.nstr(lo, 8), "  (M1 =", mp.nstr(1 / (1 + a), 8), ")")
print("  disclosure ceiling: g_H(r) = c_H at r =", mp.nstr(5 + mp.sqrt(24.75), 8), "(r^2 - 10 r + p^2 = 0 at c_H = 5)")
