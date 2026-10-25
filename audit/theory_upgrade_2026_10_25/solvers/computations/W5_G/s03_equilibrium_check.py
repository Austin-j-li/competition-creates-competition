"""Direct (E1)-(E6) check of stated tuples at off-prior points (rules IM and C1).

For a profile (sigma_H, sigma_L): Bayes posteriors (E1); prices from P = t0 + e w(mu) (E4) with entry from
the posterior under C1 (E3, with the challenger's belief = posterior when prices are distinct, E2);
investor optimality (E5) by evaluating U_j(q) at the tuple's prices and entry for every q.
Prints the margins; no assertions.
"""
import sys
sys.path.insert(0, "audit/theory_upgrade_2026_10_25/solvers/computations/W5_G")
from mpmath import mp, mpf, nstr
from model import *

s = slot()
u, lam, b, b0, beta = s["u"], s["lam"], s["b"], s["b0"], s["beta"]
eta = {-1: beta, 0: 1 - 2 * beta, 1: beta}
X = (-1, 0, 1)


def tuple_check(pi, r, sH, sL, label):
    a = auction(r)
    fH = {x: (1 - lam) * eta[x] + lam * sH[x] for x in X}
    fL = {x: (1 - lam) * eta[x] + lam * sL[x] for x in X}
    mu = {x: pi * fH[x] / (pi * fH[x] + (1 - pi) * fL[x]) for x in X}
    ent = {x: (mpf(1) if mu[x] >= a["tau"] else rho) for x in X}          # C1
    P = {x: a["t0"] + ent[x] * (a["wL"] + a["D"] * mu[x]) for x in X}
    distinct = len({nstr(P[x], 30) for x in X}) == 3
    # (E3) margin: B(mu)-cH = gam (mu - tau)
    e3 = {x: a["gam"] * (mu[x] - a["tau"]) for x in X}
    # (E5)
    U = {}
    for j, tj in (("H", a["tH"]), ("L", a["tL"])):
        U[j] = {q: q * (a["t0"] + ent[q] * (tj - a["t0"]) - P[q]) - k * abs(q) for q in X}
    ok = True
    for j, sj in (("H", sH), ("L", sL)):
        best = max(U[j].values())
        for q in X:
            if sj[q] > 0 and U[j][q] < best - mpf(10) ** -40:
                ok = False
    prob = {x: pi * fH[x] + (1 - pi) * fL[x] for x in X}
    Pbar = sum(prob[x] * P[x] for x in X)
    print(f"--- {label}: pi={nstr(pi,3)} r={nstr(r,4)} tau={nstr(a['tau'],6)} Delta={nstr(a['D'],6)}")
    print("    posteriors", {x: nstr(mu[x], 6) for x in X}, " entry", {x: nstr(ent[x], 3) for x in X},
          " prices distinct:", distinct)
    print("    E3 margins gam(mu-tau)", {x: nstr(e3[x], 5) for x in X})
    print("    U_H", {q: nstr(U["H"][q], 6) for q in X}, "  U_L", {q: nstr(U["L"][q], 6) for q in X})
    print("    E5 holds:", ok)
    Ip, Im = P[1] - P[0], P[0] - P[-1]
    print(f"    I+={nstr(Ip,6)} I-={nstr(Im,6)} I+-I-={nstr(Ip-Im,6)}  Pbar-P(0)={nstr(Pbar-P[0],6)}  "
          f"Pbar-P(-1)={nstr(Pbar-P[-1],6)}  p1={nstr(prob[1],6)} p-1={nstr(prob[-1],6)}")
    # announcement: pooled preparation-report mean
    PA = sum(prob[x] * ent[x] for x in X)
    mean = sum(prob[x] * ent[x] / PA * (1 - ent[x]) * (a["wL"] + a["D"] * mu[x]) for x in X)
    print(f"    prep-report mean = {nstr(mean,6)}")
    return dict(mu=mu, ent=ent, P=P, prob=prob, Pbar=Pbar, ok=ok)


full = ({-1: 0, 0: 0, 1: 1}, {-1: 1, 0: 0, 1: 0})
none = ({-1: 0, 0: 1, 1: 0}, {-1: 0, 0: 1, 1: 0})
buyonly = ({-1: 0, 0: 0, 1: 1}, {-1: 0, 0: 1, 1: 0})

# sale-deters regime at pi = 0.7
for r in (mpf("2.0"), mpf("2.5")):
    R = tuple_check(mpf("0.7"), r, *full, "full orders, sale-deters regime")
    a = auction(r)
    m = mbot(mpf("0.7"), u)
    print("    check T = -p_{-1}(1-rho)A(m):", nstr(-R["prob"][-1] * (1 - rho) * (a["wL"] + a["D"] * m), 8),
          " vs Pbar-P0", nstr(R["Pbar"] - R["P"][0], 8))

# full orders without recruitment at pi = 0.3 and 0.4 (false positive of the naive test)
tuple_check(mpf("0.3"), mpf("3.0"), *full, "full orders, no recruitment")
tuple_check(mpf("0.4"), mpf("3.0"), *full, "full orders, no recruitment")
# full orders with recruitment at pi = 0.6
tuple_check(mpf("0.6"), mpf("3.0"), *full, "full orders, buy recruits")

# purchases only, no recruitment, at pi = 0.3: zero order informative
for r in (mpf("2.0"), mpf("2.1"), mpf("2.2")):
    R = tuple_check(mpf("0.3"), r, *buyonly, "purchases only, no recruitment")

# A.14(iii): no-trade equilibrium at pi = 0.7, r = 1.2 (pi >= tau)
tuple_check(mpf("0.7"), mpf("1.2"), *none, "no informed trade, pi >= tau")
tuple_check(mpf("0.7"), mpf("2.0"), *none, "no informed trade, pi >= tau (check)")
