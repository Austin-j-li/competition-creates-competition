"""Identification from counts and prices at general priors (full orders; purchases only; branch R)."""
import sys
sys.path.insert(0, "audit/theory_upgrade_2026_10_25/solvers/computations/W5_G")
from mpmath import mp, mpf, nstr, sqrt, findroot
from model import *

s = slot()
u, lam, b, b0, beta = s["u"], s["lam"], s["b"], s["b0"], s["beta"]

print("== (a) known prior pi != 1/2, full orders: counts -> slot, then sale impact -> rho*Delta ==")
for pi, r in ((mpf("0.4"), mpf(3)), (mpf("0.6"), mpf(3)), (mpf("0.55"), mpf("2.5"))):
    F = full_orders(pi, r)
    p1, pm1 = F["prob"][1], F["prob"][-1]
    v, EX = p1 + pm1, p1 - pm1
    lam_hat = EX / (2 * pi - 1)
    b_hat = (v - lam_hat) / 2
    u_hat = lam_hat / b_hat
    beta_hat = b_hat / (1 - lam_hat)
    m_hat = mbot(pi, u_hat)
    rhoD_hat = F["Im"] / (pi - m_hat)
    ecomp_hat = F["Ip"] - (pm1 / p1) * F["Im"]
    a = F["a"]
    print(f"pi={nstr(pi,3)} r={nstr(r,3)}: lam_hat={nstr(lam_hat,8)} (true {nstr(lam,8)}) beta_hat={nstr(beta_hat,8)} "
          f"rhoD_hat={nstr(rhoD_hat,8)} (true {nstr(rho*a['D'],8)}) entry comp hat={nstr(ecomp_hat,8)} "
          f"(true {nstr((F['ent'][1]-F['ent'][0])*A(r,F['M']),8)})")
    print(f"     class comp = I- v/p1 = {nstr(F['Im']*v/p1,8)} vs rho D (M-m) = {nstr(rho*a['D']*(F['M']-F['m']),8)};"
          f"  informed share lam/v = {nstr(lam/v,6)}, M-m = {nstr(F['M']-F['m'],6)}, 2M-1 = {nstr(2*F['M']-1,6)}")

print("\n== (b) unknown prior: counts (v, E[X]) + sale impact + rho*Delta -> (pi, lam, b) ==")
for pi, r in ((mpf("0.4"), mpf(3)), (mpf("0.6"), mpf(3)), (mpf("0.3"), mpf("3.2")), (mpf("0.7"), mpf("3.2"))):
    F = full_orders(pi, r)
    p1, pm1 = F["prob"][1], F["prob"][-1]
    v, EX = p1 + pm1, p1 - pm1
    rhoD = rho * F["a"]["D"]
    phi = pm1 * F["Im"] / (rhoD * EX)
    roots = [-2 * phi + sqrt(4 * phi**2 + 1), -2 * phi - sqrt(4 * phi**2 + 1)]
    t_in = [t for t in roots if -1 < t < 1]
    pi_hat = (1 + t_in[0]) / 2
    lam_hat = EX / t_in[0]
    b_hat = (v - lam_hat) / 2
    print(f"true pi={nstr(pi,3)}: phi={nstr(phi,8)} roots t={[nstr(t,8) for t in roots]} -> pi_hat={nstr(pi_hat,10)} "
          f"lam_hat={nstr(lam_hat,10)} b_hat={nstr(b_hat,10)}  (regime ent0={nstr(F['ent'][0],2)}, ent-1={nstr(F['ent'][-1],2)})")

print("\n   identified set from counts alone (pi unknown): pi' -> lam'=E[X]/(2pi'-1), b'=(v-lam')/2, beta'=b'/(1-lam')")
for pi_true in (mpf("0.6"), mpf("0.7")):
    F = full_orders(pi_true, mpf(3))
    p1, pm1 = F["prob"][1], F["prob"][-1]
    v, EX = p1 + pm1, p1 - pm1
    print(f"  true pi={nstr(pi_true,3)} (lam={nstr(lam,6)}, beta={nstr(beta,6)}): v={nstr(v,8)} E[X]={nstr(EX,8)}")
    feas = []
    for i in range(1, 1000):
        pp = mpf(1) / 2 + mpf(i) / 2000
        lp = EX / (2 * pp - 1)
        bp = (v - lp) / 2
        if not (0 < lp < 1 and bp > 0):
            continue
        bet = bp / (1 - lp)
        if bet <= mpf(1) / 3:
            feas.append((pp, lp, bp, bet))
    print(f"    feasible pi' in [{nstr(feas[0][0],5)}, {nstr(feas[-1][0],5)}] on the grid; "
          f"endpoints lam'={nstr(feas[0][1],5)}..{nstr(feas[-1][1],5)}, beta'={nstr(feas[0][3],5)}..{nstr(feas[-1][3],5)}")
    # exact lower end: lam' = v (b'=0) or beta' = 1/3, whichever binds
    # beta'(pi') = (v-lam')/(2(1-lam')) <= 1/3  <=>  3v - 3lam' <= 2 - 2lam'  <=>  lam' >= 3v-2
    print(f"    beta'<=1/3 <=> lam' >= 3v-2 = {nstr(3*v-2,6)};  b'>0 <=> lam' < v = {nstr(v,6)}; "
          f"pi' range: ((1+E[X]/v)/2, (1+E[X]/max(3v-2,E[X]))/2) = ({nstr((1+EX/v)/2,6)}, {nstr((1+EX/max(3*v-2,EX))/2,6)})")

print("\n== (c) price identification at a known prior (A.12(d) generalised): u = s/[(1-pi)(pi-s)], s = I-/(rho Delta) ==")
for pi in (mpf("0.3"), mpf("0.5"), mpf("0.7")):
    F = full_orders(pi, mpf("3.2"))
    sv = F["Im"] / (rho * F["a"]["D"]) if F["ent"][0] == rho else None
    if sv is None:
        print("  regime not purchase-only at", pi)
        continue
    print(f"  pi={nstr(pi,2)}: u_hat={nstr(sv/((1-pi)*(pi-sv)),12)} true u={nstr(u,12)}")

print("\n== (d) purchases only (form F), general prior: lam = E[X]/pi, b = Pr(X=-1) ==")
for pi in (mpf("0.45"), mpf("0.55")):
    p1 = b + pi * lam
    pm1 = b
    EX = p1 - pm1
    print(f"  pi={nstr(pi,3)}: E[X]/pi = {nstr(EX/pi,10)} (lam={nstr(lam,10)}), Pr(X=-1)={nstr(pm1,10)} (b={nstr(b,10)})")

print("\n== (e) branch R at general prior: K_H = Delta (1-mu+(s)) = k with 1-mu+(s) = (1-pi) b/(b+pi s) ==")


def muplus(pi, s_, bb):
    return pi * (bb + s_) / (bb + pi * s_)


for pi, r in ((mpf("0.5"), mpf("1.45")), (mpf("0.55"), mpf("1.45")), (mpf("0.45"), mpf("1.45"))):
    a = auction(r)
    sR = b * ((1 - pi) * a["D"] / k - 1) / pi
    KH = a["D"] * (1 - muplus(pi, sR, b))
    M = Mtop(pi, u)
    conds = dict(J_gt_k=a["D"] * (1 - a["tau"]) > k, s_lt_lam=sR < lam, lowclass_abstain=rho * a["D"] * pi <= k,
                 pi_lt_tau=pi < a["tau"], mu_plus_above_tau=muplus(pi, sR, b) > a["tau"])
    print(f"  pi={nstr(pi,3)} r={nstr(r,3)}: s_R={nstr(sR,8)} K_H-k={nstr(KH-k,5)} E[X]=pi s_R={nstr(pi*sR,8)} "
          f"= b[(1-pi)D/k-1]={nstr(b*((1-pi)*a['D']/k-1),8)}  R exists: {all(conds.values())} {conds}")
    if pi == mpf("0.5"):
        print(f"     A4 check at pi=1/2: s_R = b[D/k-2] = {nstr(b*(a['D']/k-2),8)}; entry rho+(1-rho)bD/(2k) = "
              f"{nstr(rho+(1-rho)*b*a['D']/(2*k),8)}")
    # perturb lambda down with b fixed: same counts, still R?
    for dl in (mpf("0.01"), mpf("0.05")):
        lam2 = lam - dl
        beta2 = b / (1 - lam2)
        u2 = lam2 / b
        M2 = Mtop(pi, u2)
        ok = (sR < lam2) and (a["D"] * (1 - M2) < k) and beta2 <= mpf(1) / 3
        print(f"     lambda-{nstr(dl,2)}: beta'={nstr(beta2,6)} s_R<lam'={sR<lam2} D(1-M')<k={a['D']*(1-M2)<k} -> R with same counts: {ok}")

print("\n== weak identification: variance factor 1/(2pi-1)^2 ==")
for pi in (mpf("0.51"), mpf("0.55"), mpf("0.6"), mpf("0.7")):
    print(" ", nstr(pi, 3), nstr(1 / (2 * pi - 1) ** 2, 6))
