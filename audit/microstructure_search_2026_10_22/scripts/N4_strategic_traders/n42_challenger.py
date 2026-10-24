"""N4.2: the challenger trades through the slot (toehold purchase or short sale), exact enumeration.

The challenger learns its cost (0 with probability rho, else c_H) before the slot. With probability chi it
fills the slot and submits one order in {-1, 0, 1}; it then knows that the price carries no class information
and decides on the prior. Otherwise it sees the price (equivalently the flow) and decides as in the base model.
Bids stay truthful. The liquidity buy and sell masses are held at calibration A's b = (1 - lam) beta
(the challenger's presence replaces liquidity abstentions), so chi <= (1 - lam)(1 - 2 beta) = 11/51.
Print-only. Run from the repository root:
  .venv/bin/python audit/microstructure_search_2026_10_22/scripts/N4_strategic_traders/n42_challenger.py
"""
import itertools
from fractions import Fraction as F
from common import RHO, CH, K, PI, R0, R1, R2, BETA, LAM, dec, head, objects, Bf
from slot3 import engine, informed_ok, third_ok, chall_ok, prices_distinct, XS


def chall_types(o, qlow, qhigh):
    gbar = PI * o["gH"] + (1 - PI) * o["gL"]
    low = dict(name="low", prob=RHO, q=qlow, V=lambda j, e: o["t0"] + o["w" + j], own_entry=1, A=lambda e: gbar)
    high = dict(name="high", prob=1 - RHO, q=qhigh, V=lambda j, e: o["t0"], own_entry=0, A=lambda e: F(0))
    return [low, high]


def eta_fixed_b(lam, chi, beta):
    b = (1 - lam) * beta
    lq = 1 - lam - chi
    bp = b / lq
    return {-1: bp, 0: 1 - 2 * bp, 1: bp}


def fmt(d, n=6):
    return "{" + ", ".join(f"{q}: {dec(v, n)}" for q, v in sorted(d.items())) + "}"


def root_in_unit(fun, n=60):
    """Bisection root of fun on (0, 1) if fun changes sign between the ends; returns a midpoint or None."""
    f0, f1 = fun(F(0)), fun(F(1))
    if f0 is None or f1 is None or (f0 > 0) == (f1 > 0):
        return None
    lo, hi = F(0), F(1)
    for _ in range(n):
        mid = (lo + hi) / 2
        fm = fun(mid)
        if (fm > 0) == (f0 > 0):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def show(ev, s, t, ql, qh):
    print(f"    EQUILIBRIUM: informed (s,t)=({dec(s,6)},{dec(t,6)}); challenger low-cost order {ql}, high-cost order {qh}; "
          f"prices distinct={prices_distinct(ev)}")
    print(f"      mu_out = {fmt(ev['mu_out'])}  mu_mm = {fmt(ev['mu_mm'])}  e_out = {fmt(ev['e_out'],4)}")
    print(f"      prices = {fmt(ev['price'])}  E = {dec(ev['E'],6)}  O_H = {dec(ev['OH'],6)}  proceeds T = {dec(ev['T'],6)}")
    print(f"      informed payoffs H = {fmt(ev['pay']['H'])}  L = {fmt(ev['pay']['L'])}")
    for nm in ("low", "high"):
        print(f"      challenger {nm}-cost payoffs by order = {fmt(ev['pay3'][nm])}")


def enumerate_all(r, lam, chi, beta, inv="IM", rule="C1", verbose=True):
    o = objects(r)
    eta = eta_fixed_b(lam, chi, beta)
    found = []
    for ql, qh in itertools.product(XS, XS):
        types = chall_types(o, ql, qh)
        s_list = [F(0), F(1)]
        t_list = [F(0), F(1)]
        # partial informed orders: indifference roots given the other class's pure order
        for tt in (F(0), F(1)):
            root = root_in_unit(lambda x: engine(o, lam, chi, eta, x, tt, types)["pay"]["H"][1])
            if root is not None:
                s_list.append(root)
        for ss in (F(0), F(1)):
            root = root_in_unit(lambda x: engine(o, lam, chi, eta, ss, x, types)["pay"]["L"][-1])
            if root is not None:
                t_list.append(root)
        for s in s_list:
            for t in t_list:
                ev = engine(o, lam, chi, eta, s, t, types)
                okH, okL = informed_ok(ev, s, t, inv)
                # a bisection root is an approximate indifference: accept when the payoff is within 1e-15 of zero
                if 0 < s < 1:
                    okH = abs(ev["pay"]["H"][1]) < F(1, 10 ** 15) and ev["pay"]["H"][-1] <= ev["pay"]["H"][0]
                if 0 < t < 1:
                    okL = abs(ev["pay"]["L"][-1]) < F(1, 10 ** 15) and ev["pay"]["L"][1] <= ev["pay"]["L"][0]
                ok3 = third_ok(ev, types)
                okC = chall_ok(o, ev, rule)
                if okH and okL and all(ok3.values()) and okC:
                    dup = any(ql == f[2] and qh == f[3] and abs(s - f[0]) < F(1, 10 ** 12) and abs(t - f[1]) < F(1, 10 ** 12)
                              for f in found)
                    if not dup:
                        found.append((s, t, ql, qh, ev))
    if verbose:
        print(f"\n  r = {r} (~{dec(r,4)}), chi = {chi} (~{dec(chi,5)}), liquidity law {{-1,0,1}} = "
              f"({dec(eta[-1],5)}, {dec(eta[0],5)}, {dec(eta[1],5)}), tau = {dec(o['tau'],6)}, {inv}/{rule}")
        for (s, t, ql, qh, ev) in found:
            show(ev, s, t, ql, qh)
    return o, found


def main():
    lam, beta = LAM, BETA
    head("N4.2 The challenger in the slot: calibration A with the liquidity masses held at b = 11/51")
    chis = [F(1, 51), F(1, 17), F(2, 17)]
    for r in (R0, R1, R2):
        for chi in chis:
            enumerate_all(r, lam, chi, beta)

    head("Crowding-out threshold at r = 3: the toehold profile (s = 0, low-cost buys) is an equilibrium iff the informed H purchase loses")
    o = objects(R1)
    b = (1 - lam) * beta
    # P(1) in the toehold profile: liquidity buys (entry rho, prior) and the low-cost challenger (entry 1, prior)
    vl = o["t0"] + RHO * (o["wL"] + o["D"] * PI)
    vc = o["t0"] + o["wL"] + o["D"] * PI
    vH = o["t0"] + RHO * o["wH"]
    # H's purchase gain: vH - P(1) - k <= 0  with  P(1) = (b vl + chi rho vc) / (b + chi rho); linear in chi
    # (vH - k)(b + chi rho) <= b vl + chi rho vc  <=>  chi rho (vH - k - vc) <= b (vl - vH + k)
    chibar = b * (vl - vH + K) / (RHO * (vH - K - vc))
    print(f"  v_liq(1) = {vl} (~{dec(vl,6)}), v_chall(1) = {vc} (~{dec(vc,6)}), v_H(1, entry rho) = {vH} (~{dec(vH,6)})")
    print(f"  H's purchase gain in the toehold profile = v_H - P(1) - k <= 0  iff  chi >= {chibar} (~{dec(chibar,6)})")
    for chi in [F(1, 17), F(7, 100), F(8, 100), F(9, 100), F(2, 17)]:
        P1 = (b * vl + chi * RHO * vc) / (b + chi * RHO)
        print(f"    chi = {chi} (~{dec(chi,5)}): P(1) = {dec(P1,6)}, H gain = {dec(vH - P1 - K,6)}")
    print("  Enumeration at chi just below and above the threshold:")
    for chi in [chibar - F(1, 1000), chibar + F(1, 1000)]:
        enumerate_all(R1, lam, chi, beta)

    head("Closed-form gains of the in-slot challenger against the base schedule (chi -> 0 limit, V3 at r)")
    for r in (R0, R1, R2):
        o = objects(r)
        b = (1 - lam) * beta
        M = (lam + b) / (lam + 2 * b)
        mum = b / (lam + 2 * b)
        s = F(0) if o["D"] < K else F(1)
        mu1 = M if s == 1 else PI
        mu_1 = mum if s == 1 else PI
        e1 = RHO + (1 - RHO) * (1 if Bf(o, mu1) >= CH else 0)
        W = o["wL"] + o["D"] * PI
        gain_low_buy = (1 - e1) * o["wL"] + o["D"] * (PI - e1 * mu1) - K
        gain_high_sell = RHO * (o["wL"] + o["D"] * mu_1) - K
        print(f"  r = {r}: e(1) = {e1}, mu(1) = {mu1} (~{dec(mu1,5)}), mu(-1) = {mu_1} (~{dec(mu_1,5)}); "
              f"low-cost buy gain = {gain_low_buy} (~{dec(gain_low_buy,6)}); high-cost sale gain = {gain_high_sell} (~{dec(gain_high_sell,6)})")

    head("Part (iii) at r = 18/5: outside posterior M(chi) with the liquidity masses held fixed (no dilution)")
    o = objects(R2)
    b = (1 - lam) * beta
    print(f"  M = {(lam + b) / (lam + 2 * b)} (~{dec((lam + b) / (lam + 2 * b),6)}) < tau(3.6) = {dec(o['tau'],6)} for every chi: "
          f"the outside challenger's posterior does not depend on chi when b is held fixed.")
    print("  With the plain law (beta = 1/3 for the liquidity trader, so b falls with chi), M(chi) = (lam + b(chi))/(lam + 2 b(chi)):")
    for chi in [F(0), F(1, 51), F(1, 34), F(1, 17), F(2, 17)]:
        bc = (1 - lam - chi) * beta
        Mc = (lam + bc) / (lam + 2 * bc)
        print(f"    chi = {chi}: b = {dec(bc,6)}, M = {dec(Mc,6)}, below tau(3.6) = {Mc < o['tau']}, "
              f"with low-cost challenger buying: mu_mm(1) = {dec((lam + bc + chi * RHO) / (lam + 2 * bc + 2 * chi * RHO),6)}")
    # exact chi where M(chi) = tau(3.6) under the plain law
    tt = o["tau"]
    bstar = lam * (1 - tt) / (2 * tt - 1)
    chistar = 1 - lam - bstar / beta
    print(f"  plain law: M(chi) < tau(3.6) iff chi < {chistar} (~{dec(chistar,6)}): a mechanical crowding-out of camouflage.")


if __name__ == "__main__":
    main()
