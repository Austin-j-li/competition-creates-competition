"""Referee checks of the closed-form claims. Prints and writes CSV only."""
from __future__ import annotations
import mpmath as mp
from check import (BENCH, Par, mM, pay, B, tau, FZ, SZ, logit, pool_post, J_quad, J_closed,
                   minimal_pool, frak_r, r_ceiling, write_csv, HERE)

par = BENCH
m, M = mM(par)
P = pay(par, 3)
rows = []
def rec(name, val, claim):
    rows.append({"name": name, "referee_value": val, "note_value": claim})
    print(f"{name:40s} {mp.nstr(val, 10):>16s}   note: {claim}")

# Table 1
rec("s_M", par.c - B(P, M), "-0.2172")
rec("s_D", par.c - B(P, mp.mpf(1)/2), "41/24=1.7083")
rec("s_D - 41/24", par.c - B(P, mp.mpf(1)/2) - mp.mpf(41)/24, "0")
rec("s_m", par.c - B(P, m), "3.6338")
rec("wL+M*DT", P["wL"] + M*P["DT"], "0.9457")
rec("wL+m*DT", P["wL"] + m*P["DT"], "(S) lower edge")
rec("d(3)", par.c - B(P, mp.mpf(1)/2) - P["wL"] - M*P["DT"], "0.7626")
ts0 = tau(par, P, 0); xs0 = logit(ts0)
rec("tau_0", ts0, "0.705"); rec("x*", xs0, "0.8712")
rec("J closed (S.2)", J_closed(par, P, xs0), "0.09550")
rec("J quadrature", J_quad(par, P, xs0), "0.09550")
rec("J closed - quad", J_closed(par, P, xs0) - J_quad(par, P, xs0), "0")
for x0 in [-1, -0.5, 0, 0.5, 1]:
    rec(f"J closed-quad at x={x0}", J_closed(par, P, mp.mpf(x0)) - J_quad(par, P, mp.mpf(x0)), "0")
rec("DT*m/2", P["DT"]*m/2, "0.08965")
rec("(1-1/b)J - k", (1-1/mp.mpf(par.b))*J_closed(par, P, xs0) - par.k, ">0")
rec("m - 1/4", m - mp.mpf(1)/4, ">0")
mub = pool_post(par, xs0)
rec("mubar*", mub, "0.3684")
rec("backstop top c-B(mubar*)", par.c - B(P, mub), "2.8051")
rec("p^2/r", mp.mpf(par.p)**2/3, "0.0833")
rec("rho_N", 2*par.k/P["DT"], "0.060"); rec("rho_U", par.k/((1-1/mp.mpf(par.b))*m*P["DT"]), "0.223")
rec("frak_r(k)", frak_r(par, par.k), "1.2210"); rec("frak_r(2k)", frak_r(par, 2*par.k), "1.3257")
rec("r_C", r_ceiling(par), "3.5927")
rec("r_hand", frak_r(par, 2*par.k/((1-1/mp.mpf(par.b))*m)), "2.1241")
rec("r_pool_forced", frak_r(par, par.k/((1-1/mp.mpf(par.b))*m)), "1.714 (CSV)")
# roots of the J test, by bisection in mpmath
def test_s0(r):
    Q = pay(par, r); t = tau(par, Q, 0)
    return (1-1/mp.mpf(par.b))*J_closed(par, Q, logit(t)) - par.k
def test_sD(r):
    Q = pay(par, r); return (1-1/mp.mpf(par.b))*J_closed(par, Q, 0) - par.k
rec("r_test_s0", mp.findroot(test_s0, (1.5, 3.0), solver='bisect'), "2.0155")
rec("r_test_sD", mp.findroot(test_sD, (1.3, 3.0), solver='bisect'), "1.8434")
# F.3 benchmark inequalities
for r_, nm in [(1.2, "r0"), (3, "r1"), (3.6, "r2")]:
    Q = pay(par, r_)
    rec(f"B_{nm}(1/2)", B(Q, mp.mpf(1)/2), "")
    rec(f"B_{nm}(M)", B(Q, M), "")
    rec(f"DT({nm})", Q["DT"], "")
# d(r) on (1, 10): closed form, concavity, endpoints, and a fine grid
def d(r):
    Q = pay(par, r); return par.c - B(Q, mp.mpf(1)/2) - Q["wL"] - M*Q["DT"]
def d_closed(r):
    r = mp.mpf(r)
    return par.c - par.h/2 + par.p - m*par.ell - (M-m)*r/4 - ((M-m)*par.ell**2/4 + par.p**2)/r
rec("d(1)", d(1), "3/4"); rec("d(10)", d(10), "4.05m-1.05"); rec("4.05m-1.05", 4.05*m-1.05, "")
grid = [1 + 9*i/2000 for i in range(2001)]
rec("min d on [1,10] grid", min(d(r) for r in grid), ">0")
rec("max |d - d_closed| on grid", max(abs(d(r)-d_closed(r)) for r in grid[::50]), "0")
# Table 2
print("\nTable 2")
t2 = []
sM, sD, sm = par.c - B(P, M), par.c - B(P, mp.mpf(1)/2), par.c - B(P, m)
for s in [sM, 0, 0.1, 0.5, 1.0, sD, 2.0, 3.0, sm - mp.mpf(10)**-12, sm]:
    o = minimal_pool(par, 3, mp.mpf(s)); t2.append(o)
    print(" ".join(mp.nstr(o[k], 5) for k in ["s", "E", "e_H", "e_L", "R_T", "outlay", "N", "W"]))
write_csv(HERE / "ref_table2.csv", t2)
# N(s) = t0 crossing
fN = lambda s: minimal_pool(par, 3, s)["N"] - P["t0"]
rec("s where minimal-pool N = t0", mp.findroot(fN, (0.5, 1.5), solver='bisect'), "near 0.93")
# W(s) and its zero above s_D
fW = lambda s: minimal_pool(par, 3, s)["W"]
rec("s where W = 0 (above s_D)", mp.findroot(fW, (sD, 2.0), solver='bisect'), "just above s_D")
# S.4 at r = 3: maximizer of W on [s_M, s_m)
ss = [sM + (sm - sM)*i/4000 for i in range(4000)]
Ws = [fW(s) for s in ss]
i = max(range(len(ss)), key=lambda j: Ws[j])
rec("argmax W on [s_M,s_m) at r=3", ss[i], "p^2/r = 0.0833")
write_csv(HERE / "ref_closed.csv", rows)
