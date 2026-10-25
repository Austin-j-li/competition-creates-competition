"""Size of the naive-test bias; false-negative condition at priors above 1/2."""
import sys
sys.path.insert(0, "audit/theory_upgrade_2026_10_25/solvers/computations/W5_G")
from mpmath import mp, mpf, nstr
from model import *

s = slot()
u = s["u"]

print("== auction-free no-false-negative threshold rho < M/(2pi-m), benchmark slot ==")
best = (mpf(2), None)
for i in range(1, 1000):
    pi = mpf(1) / 2 + mpf(i) / 2000
    M, m = Mtop(pi, u), mbot(pi, u)
    th = M / (2 * pi - m)
    if th < best[0]:
        best = (th, pi)
for pi in (mpf("0.55"), mpf("0.6"), mpf("0.7"), mpf("0.8"), mpf("0.9")):
    M, m = Mtop(pi, u), mbot(pi, u)
    print(f"  pi={nstr(pi,3)}: M/(2pi-m) = {nstr(M/(2*pi-m),6)}")
print(f"  minimum over pi in (1/2,1): {nstr(best[0],6)} at pi={nstr(best[1],4)}")
for uu in (mpf(5), mpf(20), mpf(100)):
    bb = (mpf(2), None)
    for i in range(1, 1000):
        pi = mpf(1) / 2 + mpf(i) / 2000
        th = Mtop(pi, uu) / (2 * pi - mbot(pi, uu))
        if th < bb[0]:
            bb = (th, pi)
    print(f"  u={nstr(uu,4)}: min_pi M/(2pi-m) = {nstr(bb[0],6)} at pi={nstr(bb[1],4)}")

print("\n== false positive at pi<1/2 relative to the entry component recruitment would add at the same point ==")
print("   ratio  rho D[(M-pi)-(pi-m)] / ((1-rho) A(M)) on the benchmark path where full orders are unique")
worst = (mpf(0), None, None)
for i in range(1, 50):
    pi = mpf(i) / 100
    M, m = Mtop(pi, u), mbot(pi, u)
    kap = min(m, 1 - M)
    for j in range(0, 49):
        r = mpf("1.2") + mpf(j) * mpf("2.4") / 48
        a = auction(r)
        if rho * a["D"] * kap <= k:
            continue
        gap = rho * a["D"] * ((M - pi) - (pi - m))
        ec = (1 - rho) * (a["wL"] + a["D"] * M)
        if gap / ec > worst[0]:
            worst = (gap / ec, pi, r)
print(f"   max ratio {nstr(worst[0],5)} at pi={nstr(worst[1],3)}, r={nstr(worst[2],4)}")
for pi, r in ((mpf("0.3"), mpf("3.6")), (mpf("0.4"), mpf("3")), (mpf("0.45"), mpf("3"))):
    M, m = Mtop(pi, u), mbot(pi, u)
    a = auction(r)
    gap = rho * a["D"] * ((M - pi) - (pi - m))
    ec = (1 - rho) * (a["wL"] + a["D"] * M)
    print(f"   pi={nstr(pi,3)} r={nstr(r,3)}: gap={nstr(gap,5)}  (1-rho)A(M)={nstr(ec,5)}  ratio={nstr(gap/ec,4)}"
          f"  gap/I-={nstr(gap/(rho*a['D']*(pi-m)),4)}")
print("   upper bound over all auctions: rho[(M-pi)-(pi-m)]/((1-rho)M) (uses w_L>=0)")
mx = (mpf(0), None)
for i in range(1, 500):
    pi = mpf(i) / 1000
    M, m = Mtop(pi, u), mbot(pi, u)
    v = rho * ((M - pi) - (pi - m)) / ((1 - rho) * M)
    if v > mx[0]:
        mx = (v, pi)
print(f"   sup over pi<1/2 at the benchmark slot and rho=1/4: {nstr(mx[0],5)} at pi={nstr(mx[1],3)}")

print("\n== a false negative exists when rho is large and the slot is very informative (not benchmark) ==")
from mpmath import mpf as F_
rho2, k2, u2, pi = F_("0.8"), F_("0.01"), F_(20), F_("0.9")
r = F_(9)
a = auction(r)
cH2 = a["gL"] + F_("0.95") * a["gam"]
tau2 = (cH2 - a["gL"]) / a["gam"]
M, m = Mtop(pi, u2), mbot(pi, u2)
Ip = rho2 * a["D"] * (M - pi) + (1 - rho2) * (a["wL"] + a["D"] * M)
Im = rho2 * a["D"] * (pi - m)
print(f"   rho=0.8, u=20, pi=0.9, U[0,9], h=10, ell=1, p=1/2, c_H={nstr(cH2,6)}, k=0.01: tau={nstr(tau2,4)} M={nstr(M,5)} m={nstr(m,4)}")
print(f"   K_H = D(1-M) - k = {nstr(a['D']*(1-M)-k2,4)}, K_L = rho D m - k = {nstr(rho2*a['D']*m-k2,4)}  (full orders an equilibrium if both >0)")
print(f"   I+ - I- = {nstr(Ip-Im,5)} although a purchase recruits; threshold M/(2pi-m) = {nstr(M/(2*pi-m),4)} < rho")
p1 = s["b"] * 0  # placeholder to keep namespace tidy
