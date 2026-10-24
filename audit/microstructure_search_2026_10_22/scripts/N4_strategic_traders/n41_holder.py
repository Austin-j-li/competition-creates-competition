"""N4.1: a holder with a stake fills the non-informed slot (manipulation by an uninformed trader).

Slot: informed investor with probability lam (sees the class; orders in {-1,0,1} at cost k|q|).
Otherwise a holder with stake omega (order units, pays V_T, sunk) fills the slot:
  forced sale with probability beta, forced purchase with probability beta, free choice otherwise.
The free holder maximizes omega E[V_T | q] + q (E[V_T | q, uninformed] - P(q)) - k |q|.
Competitive price P(x) = t_0 + e(x) [w_L + Delta mu(x)]; the challenger sees the price and its cost.
Print-only; all comparisons use fractions.Fraction. Run from the repository root:
  .venv/bin/python audit/microstructure_search_2026_10_22/scripts/N4_strategic_traders/n41_holder.py
"""
import sys
from fractions import Fraction as F
from common import (H, L, P, RHO, CH, K, PI, R0, R1, R2, BETA, LAM, dec, head, objects, Bf, entry_C1,
                    post, r_of_delta)

XS = (-1, 0, 1)


def masses(lam, beta, s, t, m, mm):
    """Class-conditional flow masses. s, t: informed H buy / L sell probabilities; m, mm: free holder buy / sell."""
    c = (1 - lam) * (1 - 2 * beta)
    hb = (1 - lam) * beta + c * m        # holder purchase mass
    hs = (1 - lam) * beta + c * mm       # holder sale mass
    hz = c * (1 - m - mm)                # holder abstention mass
    aH = {1: lam * s + hb, -1: hs, 0: lam * (1 - s) + hz}
    aL = {1: hb, -1: lam * t + hs, 0: lam * (1 - t) + hz}
    return aH, aL


def evaluate(o, lam, beta, omega, s, t, m, mm, ent=None):
    aH, aL = masses(lam, beta, s, t, m, mm)
    mu = {x: post(aH[x], aL[x]) for x in XS}
    e = {x: entry_C1(o, mu[x]) for x in XS}
    if ent:
        e.update(ent)
    price = {x: o["t0"] + e[x] * (o["wL"] + o["D"] * mu[x]) for x in XS}
    val = {"H": {x: o["t0"] + e[x] * o["wH"] for x in XS}, "L": {x: o["t0"] + e[x] * o["wL"] for x in XS}}
    pay = {j: {q: q * (val[j][q] - price[q]) - K * abs(q) for q in XS} for j in "HL"}
    vU = {x: o["t0"] + e[x] * (o["wL"] + o["D"] * PI) for x in XS}       # uninformed value of one share
    payU = {q: omega * vU[q] + q * (vU[q] - price[q]) - K * abs(q) for q in XS}   # free holder, in the slot
    prob = {x: PI * aH[x] + (1 - PI) * aL[x] for x in XS}
    E = sum(prob[x] * e[x] for x in XS)
    OH = PI * sum(aH[x] * e[x] for x in XS)
    return dict(aH=aH, aL=aL, mu=mu, e=e, price=price, pay=pay, payU=payU, vU=vU, prob=prob, E=E, OH=OH)


def br_ok(pay, strat, rule):
    """strat: dict order -> probability. rule IM: support within argmax; I0: zero at indifference."""
    mx = max(pay.values())
    arg = {q for q, v in pay.items() if v == mx}
    supp = {q for q, w in strat.items() if w > 0}
    if not supp <= arg:
        return False
    if rule == "I0" and 0 in arg and supp != {0}:
        return False
    return True


def chall_ok(o, mu, e, rule):
    B = Bf(o, mu)
    if B > CH:
        return e == 1
    if B < CH:
        return e == RHO
    return (e == 1) if rule == "C1" else (RHO <= e <= 1)


def verify(o, lam, beta, omega, s, t, m, mm, ent, inv="IM", chall="C1"):
    ev = evaluate(o, lam, beta, omega, s, t, m, mm, ent)
    okH = br_ok(ev["pay"]["H"], {1: s, 0: 1 - s}, inv)
    okL = br_ok(ev["pay"]["L"], {-1: t, 0: 1 - t}, inv)
    okU = br_ok(ev["payU"], {1: m, -1: mm, 0: 1 - m - mm}, inv)
    okC = all(chall_ok(o, ev["mu"][x], ev["e"][x], chall) for x in XS)
    return ev, okH, okL, okU, okC


def thresholds(o, lam, beta):
    b = (1 - lam) * beta
    c = (1 - lam) * (1 - 2 * beta)
    M = (lam + b) / (lam + 2 * b)
    W = o["wL"] + o["D"] * PI
    den = (1 - RHO) * W
    Om1 = (o["D"] * (M - PI) + K) / den
    Om2 = (o["D"] * (o["tau"] - PI) + K) / den
    mmax = (lam * (1 - o["tau"]) - b * (2 * o["tau"] - 1)) / (c * (2 * o["tau"] - 1))
    return dict(b=b, c=c, M=M, W=W, Om1=Om1, Om2=Om2, mmax=mmax)


def L_rate(o, lam, b):
    D = o["D"]
    if RHO * D / 2 <= K:
        return F(0)
    if RHO * D * b / (2 * b + lam) >= K:
        return lam
    return b * (RHO * D / K - 2)


def candidates(o, lam, beta, omega):
    """Candidate profiles (s, t, m, mm, entry override, label) from the closed forms."""
    th = thresholds(o, lam, beta)
    b, c, M, W = th["b"], th["c"], th["M"], th["W"]
    tl = L_rate(o, lam, b) / lam       # L sale probability conditional on informed
    out = []
    out.append((F(0), F(0), F(0), F(0), None, "no trade: s = t = m = 0"))
    out.append((F(1), tl, F(0), F(0), None, "V3: m = 0"))
    if th["mmax"] >= 1:
        out.append((F(1), tl, F(1), F(0), None, "pure manipulation: m = 1, e(1) = 1"))
    A = omega * (1 - RHO) * W - K
    if A > 0:
        mstar = (lam * o["D"] / (2 * A) - lam - 2 * b) / (2 * c)
        if 0 < mstar < th["mmax"]:
            out.append((F(1), tl, mstar, F(0), None, "M: interior m*, e(1) = 1"))
    denom = omega * W - o["D"] * (o["tau"] - PI)
    if denom > 0 and 0 < th["mmax"] <= 1:
        estar = (K + RHO * omega * W) / denom
        if RHO <= estar <= 1:
            out.append((F(1), tl, th["mmax"], F(0), {1: estar}, f"M': m = m_max, e(1) = e* = {estar}"))
    return th, out


def report(o, lam, beta, omega, verbose=True):
    th, cands = candidates(o, lam, beta, omega)
    rows = []
    for (s, t, m, mm, ent, label) in cands:
        for inv in ("IM", "I0"):
            for ch in ("C1", "CM"):
                ev, okH, okL, okU, okC = verify(o, lam, beta, omega, s, t, m, mm, ent, inv, ch)
                rows.append((label, inv, ch, okH and okL and okU and okC, ev, s, t, m))
    if verbose:
        print(f"\n  r = {o['r']} (~{dec(o['r'],4)}), omega = {omega} (~{dec(omega,6)}); "
              f"Omega_2 = {th['Om2']} (~{dec(th['Om2'])}), Omega_1 = {th['Om1']} (~{dec(th['Om1'])}), "
              f"m_max = {th['mmax']} (~{dec(th['mmax'])})")
        for (label, inv, ch, ok, ev, s, t, m) in rows:
            gU = ev["payU"][1] - ev["payU"][0]
            print(f"    {label:<48} {inv}/{ch}: equilibrium={ok}  mu(1)={ev['mu'][1]} (~{dec(ev['mu'][1],6)}) "
                  f"e(1)={ev['e'][1]} (~{dec(ev['e'][1],6)})  t_L={t} (~{dec(t,4)})  E={ev['E']} (~{dec(ev['E'],6)}) "
                  f"O_H={dec(ev['OH'],6)}  holder gain buy-wait={gU} (~{dec(gU,6)})")
    return th, rows


def grid_scan(o, lam, beta, omega, n=200):
    """Brute force over the free holder's buy probability m on a rational grid (C1 entry, full H purchase)."""
    th = thresholds(o, lam, beta)
    tl = L_rate(o, lam, th["b"]) / lam
    found, brackets, prev = [], [], None
    for i in range(n):          # m = 1 leaves flow 0 unused; it is excluded (it never recruits anyway)
        m = F(i, n)
        ev, okH, okL, okU, okC = verify(o, lam, beta, omega, F(1), tl, m, F(0), None, "IM", "C1")
        if okH and okL and okU and okC:
            found.append(m)
        g = ev["payU"][1] - ev["payU"][0]
        if prev is not None and (g > 0) != (prev[1] > 0):
            brackets.append((prev[0], m, prev[1], g))
        prev = (m, g)
    return found, brackets


def ledger(o, lam, beta, omega, s, t, m, mm, ent, label):
    ev = evaluate(o, lam, beta, omega, s, t, m, mm, ent)
    e, mu, prob, aH, aL = ev["e"], ev["mu"], ev["prob"], ev["aH"], ev["aL"]
    zeta = {x: (e[x] - RHO) / (1 - RHO) for x in XS}
    T = sum(PI * aH[x] * (o["t0"] + e[x] * o["wH"]) + (1 - PI) * aL[x] * (o["t0"] + e[x] * o["wL"]) for x in XS)
    S = sum(PI * aH[x] * (o["s0"] + e[x] * (o["sH"] - o["s0"])) + (1 - PI) * aL[x] * (o["s0"] + e[x] * (o["sL"] - o["s0"]))
            for x in XS)
    prep = sum(prob[x] * (1 - RHO) * zeta[x] * CH for x in XS)
    c = (1 - lam) * (1 - 2 * beta)
    nonzero = lam * (PI * s + (1 - PI) * t) + 2 * (1 - lam) * beta + c * (m + mm)
    tcost = K * nonzero
    W = S - prep - tcost
    chall = sum(PI * aH[x] * (RHO * o["gH"] + (1 - RHO) * zeta[x] * (o["gH"] - CH))
                + (1 - PI) * aL[x] * (RHO * o["gL"] + (1 - RHO) * zeta[x] * (o["gL"] - CH)) for x in XS)
    inc = sum(PI * aH[x] * ((1 - e[x]) * o["i0"] + e[x] * o["iH"]) + (1 - PI) * aL[x] * ((1 - e[x]) * o["i0"] + e[x] * o["iL"])
              for x in XS)
    inf_profit = lam * (PI * s * ev["pay"]["H"][1] + (1 - PI) * t * ev["pay"]["L"][-1])
    tradeU = {q: q * (ev["vU"][q] - ev["price"][q]) - K * abs(q) for q in XS}
    holder_trade = (1 - lam) * (beta * tradeU[1] + beta * tradeU[-1] + c * (m * tradeU[1] + mm * tradeU[-1]))
    holder_total = omega * T + holder_trade
    print(f"  {label:<26} T={dec(T,6)} S={dec(S,6)} prep={dec(prep,6)} k-cost={dec(tcost,6)} W={dec(W,6)} "
          f"chall={dec(chall,6)} inc={dec(inc,6)} informed={dec(inf_profit,6)} holder trade={dec(holder_trade,6)} "
          f"holder total={dec(holder_total,6)} E={dec(ev['E'],6)} O_H={dec(ev['OH'],6)}")
    print(f"      exact: T={T} W={W} chall={chall} inc={inc} informed={inf_profit} holder trade={holder_trade}")
    print(f"      identity check T+inc+chall_gross-W = prep+tcost-prep ... S-(T+inc+chall+prep) = {S - (T + inc + chall + prep)}")
    return dict(T=T, S=S, prep=prep, tcost=tcost, W=W, chall=chall, inc=inc, informed=inf_profit,
                holder_trade=holder_trade, holder_total=holder_total, E=ev["E"], OH=ev["OH"])


def main():
    lam, beta = LAM, BETA
    head("N4.1 Holder with a stake in the slot: calibration A (beta = 1/3, lambda = 6/17)")
    o3 = objects(R1)
    th = thresholds(o3, lam, beta)
    print("  objects at r = 3:", {k: str(v) for k, v in o3.items()})
    print("  b =", th["b"], " c =", th["c"], " M =", th["M"], " W = w_L + Delta/2 =", th["W"])
    print("  Omega_2 =", th["Om2"], "~", dec(th["Om2"]), "  Omega_1 =", th["Om1"], "~", dec(th["Om1"]),
          "  m_max =", th["mmax"], "~", dec(th["mmax"]))
    print("  check Omega_2 < Omega_1:", th["Om2"] < th["Om1"])

    head("Candidate equilibria at r = 3 for a list of stakes (verified by direct best responses)")
    stakes = [F(0), F(1, 10), F(1, 4), th["Om2"], (th["Om2"] + th["Om1"]) / 2, th["Om1"], F(3, 10), F(1, 2), F(1), F(10)]
    for om in stakes:
        report(o3, lam, beta, om)

    head("Brute force over m (grid of 200) at r = 3, C1/IM, full H purchase: equilibrium m values")
    for om in [F(0), F(1, 4), (th["Om2"] + th["Om1"]) / 2, F(3, 10), F(1)]:
        found, br = grid_scan(o3, lam, beta, om)
        print(f"  omega = {om} (~{dec(om,6)}): equilibrium grid points m in {[str(x) for x in found]}; "
              f"sign changes of the holder's buy gain (C1 entry) at {[(str(a), str(b)) for a, b, _, _ in br]}")

    head("Weak (r = 6/5) and very strong (r = 18/5) strengths: the holder never manipulates")
    for r in (R0, R2):
        o = objects(r)
        s = F(0) if o["D"] < K else F(1)
        tl = L_rate(o, lam, th["b"]) / lam
        print(f"\n  r = {r}: Delta = {o['D']} (~{dec(o['D'],5)}), tau = {o['tau']} (~{dec(o['tau'],6)}), "
              f"M = {th['M']} (~{dec(th['M'],6)}), informed s = {s}, t_L = {tl}")
        for om in [F(0), F(1), F(10), F(100)]:
            best = None
            for i in range(0, 101):
                m = F(i, 100)
                ev = evaluate(o, lam, beta, om, s, tl, m, F(0))
                g = ev["payU"][1] - ev["payU"][0]
                gs = ev["payU"][-1] - ev["payU"][0]
                if best is None or g > best[0]:
                    best = (g, m, gs, ev["mu"][1], ev["e"][1])
            ev0, okH, okL, okU, okC = verify(o, lam, beta, om, s, tl, F(0), F(0), None)
            print(f"    omega = {str(om):>4}: V3 profile equilibrium = {okH and okL and okU and okC}; "
                  f"largest holder buy gain over m-grid = {dec(best[0],6)} at m = {best[1]} (mu(1) = {dec(best[3],5)}, e(1) = {best[4]}); "
                  f"sale gain at that m = {dec(best[2],6)}; H buy return at m=0 = {dec(ev0['pay']['H'][1],6)}")

    head("Three intermediate strengths 31/20, 8/5, 33/20: equilibria and entry by stake (IM, C1 and CM)")
    for om in [F(9, 100), F(1, 10), F(11, 100), F(12, 100), F(13, 100), F(14, 100), F(15, 100), F(1, 5), F(1, 4), F(3, 10)]:
        print(f"\n  omega = {om} (~{dec(om,4)})")
        for r in [F(31, 20), F(8, 5), F(33, 20)]:
            o = objects(r)
            th_r, rows = report(o, lam, beta, om, verbose=False)
            ok_rows = [(lab, inv, ch, ev) for (lab, inv, ch, ok, ev, s_, t_, m_) in rows if ok]
            txt = "; ".join(f"{lab.split(':')[0]} [{inv}/{ch}] E={dec(ev['E'],6)}" for (lab, inv, ch, ev) in ok_rows)
            print(f"    r = {str(r):>5}: Omega_2={dec(th_r['Om2'],5)} Omega_1={dec(th_r['Om1'],5)} m_max={dec(th_r['mmax'],4)} | {txt}")

    print("\n  Upper stake bound for M' with a full informed purchase: e*(omega) Delta (1 - tau) >= k")
    print("  omega_bar_H(r) = k Delta / (2 W [k - rho Delta (1 - tau)]) when k > rho Delta (1 - tau):")
    for r in [F(31, 20), F(8, 5), F(33, 20)]:
        o = objects(r)
        t = thresholds(o, lam, beta)
        gap = K - RHO * o["D"] * (1 - o["tau"])
        ob = K * o["D"] / (2 * t["W"] * gap) if gap > 0 else None
        print(f"    r = {str(r):>5}: Omega_1 = {t['Om1']} (~{dec(t['Om1'],6)}), omega_bar_H = {ob} (~{dec(ob,6) if ob else 'none'})")

    head("Phase in strength r: thresholds, m_max, and conditions (full-purchase region)")
    rF = r_of_delta(F(4, 55))
    rN = r_of_delta(F(4, 25))
    print("  r_F bracket:", [dec(x, 9) for x in rF], " r_N bracket:", [dec(x, 9) for x in rN])
    print(f"  {'r':>6} {'Delta':>9} {'tau':>9} {'w_L':>9} {'W':>9} {'Omega_2':>10} {'Omega_1':>10} {'m_max':>9} "
          f"{'t_L':>8} {'rho*D*(1-tau)-k':>16} {'D*(1-M)-k':>12}")
    for r in [F(147, 100), F(3, 2), F(31, 20), F(8, 5), F(33, 20), F(7, 4), F(2), F(5, 2), F(3), F(13, 4), F(17, 5), F(345, 100)]:
        o = objects(r)
        t = thresholds(o, lam, beta)
        tl = L_rate(o, lam, t["b"]) / lam
        print(f"  {dec(r,3):>6} {dec(o['D'],6):>9} {dec(o['tau'],6):>9} {dec(o['wL'],6):>9} {dec(t['W'],6):>9} "
              f"{dec(t['Om2'],7):>10} {dec(t['Om1'],7):>10} {dec(t['mmax'],6):>9} {dec(tl,4):>8} "
              f"{dec(RHO*o['D']*(1-o['tau'])-K,7):>16} {dec(o['D']*(1-t['M'])-K,7):>12}")
    # ceiling r_C: M = tau(r)
    def f(r):
        return objects(r)["tau"] - th["M"]
    lo, hi = F(3), F(18, 5)
    for _ in range(40):
        mid = (lo + hi) / 2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    print("  r_C bracket (tau = M):", dec(lo, 9), dec(hi, 9))
    # stake that minimizes Omega_2 over the grid (coarse): where is manipulation cheapest?
    best = None
    for i in range(0, 201):
        r = rF[1] + (lo - rF[1]) * F(i, 200)
        o = objects(r)
        t = thresholds(o, lam, beta)
        if best is None or t["Om2"] < best[0]:
            best = (t["Om2"], r)
    print(f"  smallest Omega_2 on the grid [r_F, r_C]: {dec(best[0],7)} at r ~ {dec(best[1],4)}")

    head("Welfare ledger at r = 3 (per share; W = S - preparation - trading costs)")
    tl = L_rate(o3, lam, th["b"]) / lam
    rows = {}
    rows["hidden price"] = ledger(o3, lam, beta, F(0), F(1), tl, F(0), F(0), {-1: RHO, 0: RHO, 1: RHO}, "hidden price, omega=0")
    rows["V3"] = ledger(o3, lam, beta, F(0), F(1), tl, F(0), F(0), None, "V3 (m=0), omega=0")
    for om in [th["Om2"], F(27, 100), F(28, 100), th["Om1"]]:
        thh, cands = candidates(o3, lam, beta, om)
        for (s, t, m, mm, ent, label) in cands:
            if label.startswith("M:"):
                ledger(o3, lam, beta, om, s, t, m, mm, ent, f"M, omega={dec(om,5)}")
    for om in [th["Om2"], th["Om1"], F(3, 10), F(1, 2), F(1), F(10)]:
        thh, cands = candidates(o3, lam, beta, om)
        for (s, t, m, mm, ent, label) in cands:
            if label.startswith("M'"):
                ledger(o3, lam, beta, om, s, t, m, mm, ent, f"M', omega={dec(om,5)}")
    print("\n  Holder's payoff in V3 at the same stakes (stake value plus forced-trade losses):")
    for om in [th["Om2"], th["Om1"], F(3, 10), F(1, 2), F(1)]:
        ledger(o3, lam, beta, om, F(1), tl, F(0), F(0), None, f"V3, omega={dec(om,5)}")


if __name__ == "__main__":
    main()
