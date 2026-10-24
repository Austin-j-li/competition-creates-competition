"""N4.3: the incumbent trades through the slot (jamming), exact arithmetic with rational brackets.

The incumbent knows its own value R ~ U[0, r]. With probability chi it fills the slot and submits one order.
It does not know the class. Its payoff is the trade (q (V_T - P) - k|q|) plus a scale factor zeta times its
auction profit, which depends on the outside challenger's entry at the flow it creates.
The challenger is never in the slot; it sees the price (the three prices are checked to be distinct).
Strategies of the incumbent are cutoff rules: sell iff R < R_s, buy iff R >= R_b.
Liquidity masses are held at b = 11/51 (chi <= 11/51).
Print-only. Run from the repository root:
  .venv/bin/python audit/microstructure_search_2026_10_22/scripts/N4_strategic_traders/n43_incumbent.py
"""
from fractions import Fraction as F
from common import H, L, P, RHO, CH, K, PI, R0, R1, R2, BETA, LAM, dec, head, objects, Bf, expect
from slot3 import engine, informed_ok, chall_ok, prices_distinct, XS


def cell_values(o, a, b_, e):
    """E[V_T | R in [a, b), entry e] averaged by class, as a function V(j, e); exact integration."""
    r = o["r"]
    width = b_ - a

    def cond(pieces):
        return expect(pieces, r) * r / width       # E[f(R) 1{R in cell}] / Pr(cell)

    def V(j, e):
        th = H if j == "H" else L
        no = cond([(max(a, P), b_, P, F(0))])                              # p 1{R >= p} on the cell
        with_ = cond([(a, min(b_, P), P, F(0)), (max(a, P), min(b_, th), F(0), F(1)), (max(a, th), b_, th, F(0))])
        return (1 - e) * no + e * with_

    def A(e):
        i0 = cond([(max(a, P), b_, -P, F(1))])
        iH = cond([(max(a, H), b_, -H, F(1))])
        iL = cond([(max(a, L), b_, -L, F(1))])
        return (1 - e) * i0 + e * (PI * iH + (1 - PI) * iL)
    return V, A


def inc_types(o, Rs, Rb, zeta):
    """Three cells: sellers [0, Rs), waiters [Rs, Rb), buyers [Rb, r]. Empty cells are dropped."""
    r = o["r"]
    out = []
    for name, a, b_, q in (("sell", F(0), Rs, -1), ("wait", Rs, Rb, 0), ("buy", Rb, r, 1)):
        if b_ > a:
            V, A = cell_values(o, a, b_, F(1))
            out.append(dict(name=name, prob=(b_ - a) / r, q=q, V=V, own_entry=None, A=(lambda e, A=A: zeta * A(e))))
    return out


def point_gain(o, ev, R, q, zeta):
    """Gain of an incumbent with value R from order q against the schedule ev (trade plus scaled auction)."""
    e = ev["e_out"][q]
    e0 = ev["e_out"][0]

    def V(e_):
        no = P if R >= P else F(0)
        with_ = PI * max(P, min(R, H)) + (1 - PI) * max(P, min(R, L))
        return (1 - e_) * no + e_ * with_

    def A(e_):
        return (1 - e_) * max(R - P, F(0)) + e_ * (PI * max(R - H, F(0)) + (1 - PI) * max(R - L, F(0)))
    return q * (V(e) - ev["price"][q]) - K * abs(q) + zeta * (A(e) - A(e0))


def eta_fixed_b(lam, chi, beta):
    b = (1 - lam) * beta
    lq = 1 - lam - chi
    bp = b / lq
    return {-1: bp, 0: 1 - 2 * bp, 1: bp}


def solve_cutoffs(o, lam, chi, beta, zeta, e1_hyp, s=F(1), t=F(1), n=36, verbose=True):
    """Fixed point of the two cutoffs under the hypothesis e_out(1) = e1_hyp (1 or rho). Bisection on each."""
    r = o["r"]
    eta = eta_fixed_b(lam, chi, beta)

    def ev_of(Rs, Rb):
        types = inc_types(o, Rs, Rb, zeta)
        return engine(o, lam, chi, eta, s, t, types, ent_override={1: e1_hyp}, chall_in_third=False)

    # sell cutoff: gain of selling minus waiting at R = Rs equals zero (price at -1 depends on Rs only)
    def gs(Rs):
        ev = ev_of(Rs, r)
        return point_gain(o, ev, Rs, -1, zeta)
    lo, hi = F(0), r
    if gs(lo + F(1, 10 ** 6)) <= 0:
        Rs = F(0)
    else:
        for _ in range(n):
            mid = (lo + hi) / 2
            if gs(mid) > 0:
                lo = mid
            else:
                hi = mid
        Rs = (lo + hi) / 2

    # buy cutoff: gain of buying minus waiting at R = Rb equals zero (price at 1 depends on Rb only)
    def gb(Rb):
        ev = ev_of(Rs, Rb)
        return point_gain(o, ev, Rb, 1, zeta)
    if gb(r - F(1, 10 ** 6)) <= 0:
        Rb = r                       # nobody buys
    else:
        lo, hi = F(0), r
        if gb(F(1, 10 ** 6)) > 0:
            Rb = F(0)
        else:
            for _ in range(n):
                mid = (lo + hi) / 2
                if gb(mid) > 0:
                    hi = mid
                else:
                    lo = mid
            Rb = (lo + hi) / 2
    ev = ev_of(Rs, Rb)
    # consistency of the entry hypothesis at flow 1 and best responses
    B1 = Bf(o, ev["mu_out"][1])
    consistent = (B1 >= CH) if e1_hyp == 1 else (B1 < CH)
    okH, okL = informed_ok(ev, s, t)
    okC = chall_ok(o, ev) if consistent else False
    # sample check of the incumbent's best response at many R
    worst = None
    for i in range(0, 61):
        R = r * F(i, 60)
        gains = {q: point_gain(o, ev, R, q, zeta) for q in XS}
        chosen = -1 if R < Rs else (1 if (R >= Rb and Rb < r) else 0)
        slack = gains[chosen] - max(gains.values())
        if worst is None or slack < worst[0]:
            worst = (slack, R, chosen, {q: dec(v, 5) for q, v in gains.items()})
    if verbose:
        print(f"    hypothesis e_out(1) = {e1_hyp}: R_s ~ {dec(Rs,6)}, R_b ~ {dec(Rb,6)} (buy share {dec((r-Rb)/r,5)}); "
              f"mu_out(1) = {dec(ev['mu_out'][1],6)} vs tau = {dec(o['tau'],6)}: consistent = {consistent}; "
              f"informed ok = {okH and okL}; prices = " + "{" + ", ".join(f"{x}: {dec(ev['price'][x],5)}" for x in XS) + "}; "
              f"E = {dec(ev['E'],6)}; distinct prices = {prices_distinct(ev)}")
        print(f"      worst incumbent best-response slack over 61 values of R: {dec(worst[0],7)} at R = {dec(worst[1],4)} "
              f"(chosen {worst[2]}, gains {worst[3]})")
    return Rs, Rb, ev, consistent and okH and okL and okC


def main():
    lam, beta = LAM, BETA
    head("N4.3 The incumbent in the slot: calibration A, liquidity masses held at b = 11/51")
    for zeta in (F(1), F(10)):
        print(f"\n  ===== scale factor zeta = {zeta} on the incumbent's auction profit =====")
        for r in (R1, R2, R0):
            o = objects(r)
            s = F(0) if o["D"] < K else F(1)
            t = s
            print(f"\n  r = {r}: tau = {dec(o['tau'],6)}, informed (s,t) = ({s},{t})")
            for chi in (F(1, 51), F(1, 17), F(2, 17), F(3, 17), F(11, 51)):
                print(f"   chi = {chi} (~{dec(chi,5)})")
                for e1 in ((F(1), RHO) if s == 1 else (RHO,)):
                    solve_cutoffs(o, lam, chi, beta, zeta, e1, s, t)

    head("Threshold presence for the jammed equilibrium at r = 3 (zeta = 1): smallest chi on a fine grid")
    print("  (the outside challenger's posterior at flow 1 includes the incumbent's purchases: mu_mm(1))")
    o = objects(R1)
    first = None
    for i in range(1, 112):
        chi = F(i, 510)
        if chi > F(11, 51):
            break
        Rs, Rb, ev, ok = solve_cutoffs(o, lam, chi, beta, F(1), RHO, verbose=False)
        if ok and first is None:
            first = chi
            print(f"  jammed equilibrium first found at chi = {chi} (~{dec(chi,5)}): R_b ~ {dec(Rb,5)}, mu_out(1) = {dec(ev['mu_out'][1],6)}")
    if first is None:
        print("  no jammed equilibrium on the grid")
    print("  recruiting equilibrium existence on the same grid (hypothesis e_out(1) = 1, full informed orders):")
    last_ok, first_fail = None, None
    for i in range(1, 112):
        chi = F(i, 510)
        if chi > F(11, 51):
            break
        Rs, Rb, ev, ok = solve_cutoffs(o, lam, chi, beta, F(1), F(1), verbose=False)
        if ok:
            last_ok = chi
        elif first_fail is None:
            first_fail = (chi, ev["pay"]["L"][-1])
    print(f"  recruiting equilibrium with full informed orders verified up to chi = {last_ok} (~{dec(last_ok,5)});")
    if first_fail:
        print(f"  first failure at chi = {first_fail[0]} (~{dec(first_fail[0],5)}): the informed L sale return is {dec(first_fail[1],6)} < 0, "
              f"so L must mix (not classified here)")


if __name__ == "__main__":
    main()
