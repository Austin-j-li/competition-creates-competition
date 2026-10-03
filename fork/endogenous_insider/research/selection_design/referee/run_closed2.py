"""Referee checks: Table 3 closed parts, Table 4, S.1(v)(d) interval, S.4 hypothesis, (S) range,
plateau knife edge, lottery, reserve, disclosure. Prints and writes CSV only."""
from __future__ import annotations
import mpmath as mp
from check import (BENCH, Par, mM, pay, B, tau, FZ, SZ, logit, pool_post, J_closed,
                   minimal_pool, frak_r, write_csv, HERE)

par = BENCH
m, M = mM(par)
half = mp.mpf(1)/2
P3 = pay(par, 3)

print("Table 3: s_D, d, t0, N at s_D for full-order minimal pool (closed form), C net")
for r in [1.2, 1.3, 1.55, 1.7, 1.85, 2.5, 3.0, 3.5, 4.0, 6.0, 9.95]:
    P = pay(par, r); sD = par.c - B(P, half)
    d = sD - P["wL"] - M*P["DT"]
    o = minimal_pool(par, r, sD)
    print(r, mp.nstr(sD, 5), mp.nstr(d, 4), mp.nstr(P["t0"], 4), "N_full", mp.nstr(o["N"], 4),
          "C_net", mp.nstr((P["tH"]+P["tL"])/2 - sD, 4), "DT<=2k", P["DT"] <= 2*par.k)

def N_pure(r, qH, qL):
    """N at s_D for pure orders (qH, qL), minimal pool at tau = 1/2: e_H + e_L = 1 (S.2(b))."""
    P = pay(par, r); sD = par.c - B(P, half); dlt = (qH - qL)/2
    eH, eL = SZ(par, -dlt), SZ(par, dlt)
    RT = P["t0"] + (eH*(P["tH"]-P["t0"]) + eL*P["wL"])/2
    return eH + eL, RT - sD*(eH+eL)/2
for r, qH, qL in [(1.55, 1, -0.227), (1.70, 1, -0.718)]:
    S, N = N_pure(r, qH, qL); print("Table 3 partial row", r, qH, qL, "e_H+e_L", mp.nstr(S, 6), "N", mp.nstr(N, 4))

print("\nTable 4: cost sweep at r=3")
rows4 = []
for c in [4.302, 4.782, 5.202, 5.222, 5.502, 6.0, 6.217]:
    q = Par(c=c); P = pay(q, 3); sD = c - B(P, half)
    sub = minimal_pool(q, 3, sD); live = minimal_pool(q, 3, 0)
    inS = (P["wL"] + m*P["DT"] <= sD <= P["wL"] + M*P["DT"])
    rows4.append(dict(c=c, s_D=sD, N_sD=sub["N"], RT_live=live["R_T"], gain_D=sub["N"]-P["t0"],
                      gain_live=sub["N"]-live["R_T"], S_fails_at_sD=inS))
    print(c, mp.nstr(sD, 4), mp.nstr(sub["N"], 4), mp.nstr(live["R_T"], 4), mp.nstr(sub["N"]-P["t0"], 4),
          mp.nstr(sub["N"]-live["R_T"], 4), "(S) fails at s_D:", inS)
write_csv(HERE / "ref_table4.csv", rows4)
cb = B(P3, half) + P3["wL"] + (1 - mp.e**(-1/mp.mpf(par.b))/2)*P3["DT"]
print("breakeven vs D", mp.nstr(cb, 8))
# gain vs live on a fine grid of c in (B(1/2), B(M)]
lo, hi = B(P3, half), B(P3, M)
mx = -mp.inf; arg = None
for i in range(1, 2001):
    c = lo + (hi-lo)*i/2000
    q = Par(c=float(c)); P = pay(q, 3); sD = q.c - B(P, half)
    g = minimal_pool(q, 3, sD)["N"] - minimal_pool(q, 3, 0)["R_T"]
    if g > mx: mx, arg = g, c
print("max gain vs live over c grid", mp.nstr(mx, 6), "at c", mp.nstr(arg, 6))
# small-gap expansion: derivative of gain wrt s_D at s_D -> 0
for eps in [1e-2, 1e-3, 1e-4]:
    c = float(lo + eps); q = Par(c=c); P = pay(q, 3); sD = q.c - B(P, half)
    print(" c=B(1/2)+", eps, "gain vs live", mp.nstr(minimal_pool(q, 3, sD)["N"] - minimal_pool(q, 3, 0)["R_T"], 6))

print("\n(S) failure range at r=3, kappa=1:", mp.nstr(P3["wL"]+m*P3["DT"], 6), mp.nstr(P3["wL"]+M*P3["DT"], 6))
# knife edge kappa*s = w_L + M*DT: plateau price equals t0; merged belief at t0
s_k = P3["wL"] + M*P3["DT"]
ts = tau(par, P3, s_k); xs = logit(ts)
pool_pr = (FZ(par, xs-1) + FZ(par, xs+1))/2
plat_pr = (SZ(par, 0) + SZ(par, 2))/2
mub = pool_post(par, xs)
merged = (pool_pr*mub + plat_pr*M)/(pool_pr + plat_pr)
print("knife edge s", mp.nstr(s_k, 6), "tau_s", mp.nstr(ts, 6), "pool mubar", mp.nstr(mub, 6),
      "merged belief at t0", mp.nstr(merged, 6), "-> prepares at t0?", merged >= ts)

print("\nS.1(v)(d): length of [x*_s, xbar_s) as tau_s falls from 1/2 to m")
prev = None; mono = True
for i in range(1, 400):
    t = half - (half - m)*i/400
    xs = logit(t)
    xb = mp.findroot(lambda x: pool_post(par, x) - t, (-1 + 1e-20, 200), solver='bisect')
    L = xb - xs
    if prev is not None and L > prev: mono = False
    prev = L
    if i in (1, 50, 100, 200, 300, 399): print(" tau", mp.nstr(t, 5), "x*", mp.nstr(xs, 5), "xbar", mp.nstr(xb, 5), "len", mp.nstr(L, 5))
print(" length strictly decreasing on grid:", mono)

print("\nS.4 hypothesis p^2/r in [s_M, s_m): check across r")
for r in [3.0, 3.5, 3.59, 4.0, 5.0]:
    P = pay(par, r); sM = par.c - B(P, M); sm = par.c - B(P, m); pig = mp.mpf(par.p)**2/r
    ss = [sM + (sm - sM)*i/2000 for i in range(2000)]
    W = [minimal_pool(par, r, s)["W"] for s in ss]
    j = max(range(len(ss)), key=lambda i: W[i])
    print(r, "s_M", mp.nstr(sM, 4), "p^2/r", mp.nstr(pig, 4), "argmax W", mp.nstr(ss[j], 4), "W there", mp.nstr(W[j], 4),
          "W(p^2/r)" if sM <= pig else "p^2/r outside window")

print("\nLottery rows (Table 6)")
P = P3; sm = par.c - B(P, m); live = minimal_pool(par, 3, 0)
aH, aL = live["e_H"], live["e_L"]
for rho in [0.07, 0.25]:
    eH, eL = rho + (1-rho)*aH, rho + (1-rho)*aL
    RT = P["t0"] + (eH*(P["tH"]-P["t0"]) + eL*P["wL"])/2
    W = rho*(B(P, half) + mp.mpf(par.p)**2/3 - par.c) + (1-rho)*live["W"]
    print(rho, "N", mp.nstr(RT - rho*sm, 4), "outlay", mp.nstr(rho*sm, 4), "W", mp.nstr(W, 4))

print("\nReserve: p' where tau = M at r=3, and B_{0,r}(1/2) limit")
def tau_res(pp):
    pp = mp.mpf(pp); r = mp.mpf(3)
    if pp <= 1:
        Q = pay(Par(p=float(pp)), 3); return tau(par, Q, 0)
    tH = r/2 + pp**2/(2*r); gH = par.h - tH
    return par.c/gH
print(" crossing p'", mp.nstr(mp.findroot(lambda x: tau_res(x) - M, (1.01, 1.5), solver='bisect'), 6))
print(" B_{0,r}(1/2) at r=1+:", mp.nstr((par.h - 1/2 + 1/2)/2, 5))
print("\nFull disclosure seller revenue r=3:", mp.nstr(P3["t0"] + (P3["tH"]-P3["t0"])/2, 6))
print("Claimed-backstop cost vs gain at r=3:", mp.nstr(par.c - B(P3, half), 5), mp.nstr(P3["wL"] + P3["DT"]/2, 5))
print("(B) epsilon bound at s_bar = s_D:", mp.nstr(min(P3["wL"] + m*P3["DT"], par.c - B(P3, half) - P3["wL"] - M*P3["DT"]), 5))
P0 = pay(par, 1.2)
print("r0=1.2: s_D", mp.nstr(par.c - B(P0, half), 5), "w_L+M DT", mp.nstr(P0["wL"] + M*P0["DT"], 5), "w_L+m DT", mp.nstr(P0["wL"]+m*P0["DT"], 5))
