"""Off-prior behaviour of the impact test at the benchmark auction and slot."""
import sys
sys.path.insert(0, "audit/theory_upgrade_2026_10_25/solvers/computations/W5_G")
from mpmath import mp, mpf, nstr, findroot
from model import *

s = slot()
u, lam, b, b0 = s["u"], s["lam"], s["b"], s["b0"]

print("== Bayes plausibility: p1(M-pi), p-1(pi-m), pi(1-pi)lam ==")
for pi in (mpf("0.1"), mpf("0.3"), mpf("0.5"), mpf("0.7"), mpf("0.9")):
    M, m = Mtop(pi, u), mbot(pi, u)
    p1, pm1 = b + pi * lam, b + (1 - pi) * lam
    print(nstr(pi, 2), nstr(p1 * (M - pi), 12), nstr(pm1 * (pi - m), 12), nstr(pi * (1 - pi) * lam, 12))


def root_tau(target, lo=mpf("1.05"), hi=mpf("9.9")):
    """strength at which tau(r) = target (tau increasing on the benchmark path)"""
    f = lambda r: auction(r)["tau"] - target
    if f(lo) > 0 or f(hi) < 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


print("\ntau on the path: tau(6/5) =", nstr(auction(mpf(6) / 5)["tau"], 6), " tau(18/5) =", nstr(auction(mpf(18) / 5)["tau"], 6))
print("\n== thresholds by prior (benchmark slot); path r in [1.2, 3.6] ==")
print("pi    M(pi)    m(pi)    kappa    rS_exist(rho D m=k)  rS_unique(rho D kappa=k)  r_pi(tau=pi)  r_C(pi)(tau=M)")
for pi in (mpf("0.3"), mpf("0.4"), mpf("0.45"), mpf("0.5"), mpf("0.55"), mpf("0.6"), mpf("0.7")):
    M, m = Mtop(pi, u), mbot(pi, u)
    kap = min(m, 1 - M)
    rSe = fr(k / (rho * m))
    rSu = fr(k / (rho * kap))
    rpi = root_tau(pi)
    rCp = root_tau(M)
    print(nstr(pi, 3), nstr(M, 6), nstr(m, 6), nstr(kap, 6), nstr(rSe, 6), nstr(rSu, 6),
          nstr(rpi, 6) if rpi else "none", nstr(rCp, 6) if rCp else "none (tau>M on path? %s)" % (auction(mpf(6)/5)["tau"] > M))

print("\n== grid: full orders, rule C1 ==")
hdr = "pi    r     tau     regime        KH-k      KL-k     uniq   I+        I-        I+-I-     T=Pbar-P0   T/p1      (e1-e0)A(M)  bias/I-"
print(hdr)
for pi in (mpf("0.3"), mpf("0.4"), mpf("0.45"), mpf("0.5"), mpf("0.55"), mpf("0.6"), mpf("0.7")):
    for r in (mpf("2.0"), mpf("2.5"), mpf("3.0"), mpf("3.4"), mpf("3.6")):
        F = full_orders(pi, r)
        a = F["a"]
        M, m = F["M"], F["m"]
        kap = min(m, 1 - M)
        if F["ent"][0] == rho and F["ent"][1] == 1:
            reg = "buy-recruits"
        elif F["ent"][0] == rho:
            reg = "none"
        elif F["ent"][-1] == rho:
            reg = "sale-deters"
        else:
            reg = "all-enter"
        uniq = rho * a["D"] * kap - k > 0
        ecomp = (F["ent"][1] - F["ent"][0]) * A(r, M)
        bias = (F["Ip"] - F["Im"]) / F["Im"]
        print(f"{nstr(pi,3):5} {nstr(r,3):5} {nstr(a['tau'],5):7} {reg:13} {nstr(F['KH']-k,4):9} {nstr(F['KL']-k,4):8} "
              f"{str(uniq):6} {nstr(F['Ip'],5):9} {nstr(F['Im'],5):9} {nstr(F['Ip']-F['Im'],4):9} {nstr(F['T'],5):11} "
              f"{nstr(F['T']/F['prob'][1],5):9} {nstr(ecomp,5):12} {nstr(bias,4)}")
    print()

print("== relative bias of the naive test without recruitment: (I+-I-)/I- = u(1-2pi)/(1+u pi) ==")
for pi in (mpf("0.2"), mpf("0.3"), mpf("0.4"), mpf("0.45"), mpf("0.49"), mpf("0.55"), mpf("0.6"), mpf("0.7")):
    print(nstr(pi, 3), nstr(u * (1 - 2 * pi) / (1 + u * pi), 6))
