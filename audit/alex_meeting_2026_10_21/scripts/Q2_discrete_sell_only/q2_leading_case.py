#!/usr/bin/env python3
"""Discrete microstructure with a one-directional trading menu (print-only).

Memo: audit/alex_meeting_2026_10_21/memos/Q2_discrete_sell_only.md

Model (memo Section 2): theta in {H, L} with prior 1/2; noise z in {-1, 0, +1}
with probabilities (pi_-, pi_0, pi_+); the investor is present with
probability lam; the menu is sell-only (q in {-1, 0}) or buy-only
(q in {0, 1}); flow X = q + z; the price is E[V_T | X]; the challenger sees
the price and its cost.  Auction objects are eq. (4) of the paper.

All arithmetic in this file is exact (fractions.Fraction), except the
irrational cutoffs, which use math.sqrt.  Every printed number is a numerical
diagnostic of a closed form in the memo.  The script makes no assertion.

Run:  .venv/bin/python audit/alex_meeting_2026_10_21/scripts/Q2_discrete_sell_only/q2_leading_case.py
"""
from fractions import Fraction as Fr
import math

THIRD = (Fr(1, 3), Fr(1, 3), Fr(1, 3))
BENCH = dict(h=Fr(10), l=Fr(1), p=Fr(1, 2), rho=Fr(1, 4),
             cL=Fr(1), cH=Fr(6), k=Fr(1, 50))
R0, R1, R2_PAPER = Fr(6, 5), Fr(3), Fr(18, 5)
FLOWS = {'sell': (-2, -1, 0, 1), 'buy': (-1, 0, 1, 2)}
TRADER = {'sell': 'L', 'buy': 'H'}


def auction(par, r):
    """Eq. (4) of the paper, uniform incumbent on [0, r]."""
    h, l, p = par['h'], par['l'], par['p']
    return dict(t0=p * (1 - p / r),
                tH=r / 2 + p * p / (2 * r),
                tL=l - (l * l - p * p) / (2 * r),
                gH=h - r / 2 - p * p / (2 * r),
                gL=(l * l - p * p) / (2 * r),
                DT=(r - l) ** 2 / (2 * r))


def B(a, mu):
    return a['gL'] + mu * (a['gH'] - a['gL'])


def entry(par, a, mu):
    """Cost-averaged preparation at belief mu; an indifferent challenger prepares."""
    e = Fr(0)
    if par['cL'] <= B(a, mu):
        e += par['rho']
    if par['cH'] <= B(a, mu):
        e += 1 - par['rho']
    return e


def flow_law(menu, noise, lam, s):
    """Pr(X = x | theta) when the present investor trades with probability s."""
    step = -1 if menu == 'sell' else 1
    law = {x: Fr(0) for x in FLOWS[menu]}
    for z, pz in zip((-1, 0, 1), noise):
        law[z] += (1 - lam * s) * pz
        law[z + step] += lam * s * pz
    return law


def offpath_belief(menu, x, rule):
    """Belief at a flow that has zero probability under the candidate.

    'IC'      : Intuitive Criterion / D1 (memo Claim 3).  A flow reached only
                by a trade in the menu's direction is assigned to the type
                for which that trade is not equilibrium-dominated.
    'passive' : the prior 1/2.
    'adverse' : the belief most favourable to a deviating trader.
    """
    if rule == 'passive':
        return Fr(1, 2)
    if menu == 'sell':
        ic = Fr(0) if x == -2 else Fr(1)
        return ic if rule == 'IC' else 1 - ic
    ic = Fr(1) if x == 2 else Fr(0)
    return ic if rule == 'IC' else 1 - ic


def solve_profile(par, r, menu, noise, lam, sH, sL, rule='IC'):
    """Posteriors, flow-measurable prices and entry, and trading payoffs."""
    a = auction(par, r)
    lawH = flow_law(menu, noise, lam, sH)
    lawL = flow_law(menu, noise, lam, sL)
    mu, onpath = {}, {}
    for x in FLOWS[menu]:
        tot = lawH[x] + lawL[x]
        if tot > 0:
            mu[x], onpath[x] = lawH[x] / tot, True
        else:
            mu[x], onpath[x] = offpath_belief(menu, x, rule), False
    e = {x: entry(par, a, mu[x]) for x in FLOWS[menu]}
    wL = a['tL'] - a['t0']
    P = {x: a['t0'] + e[x] * (wL + a['DT'] * mu[x]) for x in FLOWS[menu]}
    # Two on-path flows with different posteriors can share a price only at
    # zero entry (price t0).  Check that the challenger then stays out.
    zero = [x for x in FLOWS[menu] if onpath[x] and e[x] == 0]
    pooled, pool_ok = None, True
    if len({mu[x] for x in zero}) > 1:
        mH = sum(lawH[x] for x in zero)
        mL = sum(lawL[x] for x in zero)
        pooled = mH / (mH + mL)
        pool_ok = entry(par, a, pooled) == 0
    step = -1 if menu == 'sell' else 1
    U, Eent = {}, {}
    for th in ('H', 'L'):
        gross = Fr(0)
        for z, pz in zip((-1, 0, 1), noise):
            x = z + step
            resid = e[x] * a['DT'] * ((1 if th == 'H' else 0) - mu[x])
            gross += pz * step * resid
        U[th] = gross - par['k']
    E = (sum(lawH[x] * e[x] for x in FLOWS[menu])
         + sum(lawL[x] * e[x] for x in FLOWS[menu])) / 2
    OH = sum(lawH[x] * e[x] for x in FLOWS[menu]) / 2
    return dict(a=a, mu=mu, onpath=onpath, e=e, P=P, U=U, E=E, OH=OH,
                pooled=pooled, pool_ok=pool_ok, lawH=lawH, lawL=lawL)


def is_best_response(s, U):
    """Weak best response of a type that trades with probability s."""
    if s == 0:
        return U <= 0
    if s == 1:
        return U >= 0
    return U == 0


def brute_force(par, r, menu, noise=THIRD, lam=Fr(1), rule='IC', n=20):
    grid = [Fr(i, n) for i in range(n + 1)]
    out = []
    for sH in grid:
        for sL in grid:
            sol = solve_profile(par, r, menu, noise, lam, sH, sL, rule)
            if (is_best_response(sH, sol['U']['H'])
                    and is_best_response(sL, sol['U']['L']) and sol['pool_ok']):
                out.append((sH, sL, sol))
    return out


def frak_r(par, d):
    """Root above ell of Delta_T(r) = d (paper eq. A.10)."""
    l = float(par['l'])
    return l + d + math.sqrt(d * d + 2 * l * d)


def r_of_B(par, mu, c):
    """Larger root of B_r(mu) = c (paper eq. A.11 with M replaced by mu)."""
    h, l, p = float(par['h']), float(par['l']), float(par['p'])
    mu, c = float(mu), float(c)
    A = mu * h - c
    return (A + math.sqrt(A * A + mu * ((1 - mu) * l * l - p * p))) / mu


def f(x, nd=6):
    return f"{float(x):.{nd}f}"


def show_eq(sH, sL, sol, menu):
    flows = FLOWS[menu]
    print(f"    (s_H, s_L) = ({sH}, {sL})   U_H = {f(sol['U']['H'])}   "
          f"U_L = {f(sol['U']['L'])}")
    print("      flow      : " + "  ".join(f"{x:>9d}" for x in flows))
    print("      Pr(x|H)   : " + "  ".join(f"{f(sol['lawH'][x], 4):>9}" for x in flows))
    print("      Pr(x|L)   : " + "  ".join(f"{f(sol['lawL'][x], 4):>9}" for x in flows))
    print("      posterior : " + "  ".join(
        f"{f(sol['mu'][x], 4) + ('' if sol['onpath'][x] else '*'):>9}" for x in flows))
    print("      entry     : " + "  ".join(f"{f(sol['e'][x], 4):>9}" for x in flows))
    print("      price     : " + "  ".join(f"{f(sol['P'][x], 4):>9}" for x in flows))
    print(f"      entry E = {f(sol['E'])}   high-value ownership O_H = {f(sol['OH'])}"
          + ("" if sol['pooled'] is None else f"   zero-entry pool posterior = {f(sol['pooled'])}"))


def report_economy(par, r, menu, noise=THIRD, lam=Fr(1), rule='IC', label=''):
    eqs = brute_force(par, r, menu, noise, lam, rule)
    print(f"  [{label}] menu={menu} r={f(r, 3)} lam={lam} rule={rule}: "
          f"{len(eqs)} grid equilibria (grid step 1/20 for each type)")
    if len(eqs) <= 2:
        for sH, sL, sol in eqs:
            show_eq(sH, sL, sol, menu)
    else:
        print("    trading probabilities found: "
              + ", ".join(f"({sH},{sL})" for sH, sL, _ in eqs))
    return eqs


def section(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


def main():
    par = dict(BENCH)

    section("A. Auction objects at the benchmark (paper eq. 4; exact)")
    for r in (R0, R1, R2_PAPER, Fr(9)):
        a = auction(par, r)
        print(f"  r = {f(r, 3)}: t0={f(a['t0'])} tH={f(a['tH'])} tL={f(a['tL'])} "
              f"gH={f(a['gH'])} gL={f(a['gL'])} Delta_T={f(a['DT'])}")
        print(f"           B(0)={f(B(a, 0))} B(1/3)={f(B(a, Fr(1, 3)))} "
              f"B(1/2)={f(B(a, Fr(1, 2)))} B(1)={f(B(a, 1))}   "
              f"e(0)={f(entry(par, a, 0), 4)} e(1/2)={f(entry(par, a, Fr(1, 2)), 4)} "
              f"e(1)={f(entry(par, a, 1), 4)}   kappa=e(1/2)Delta_T/3={f(entry(par, a, Fr(1, 2)) * a['DT'] / 3)}"
              f" vs k={f(par['k'])}")

    section("B. Posteriors for every sell-only profile (equal noise; symbolic check)")
    for sH, sL in ((0, 0), (0, Fr(1, 2)), (0, 1), (1, 0), (1, 1), (Fr(1, 4), Fr(3, 4))):
        sol = solve_profile(par, R1, 'sell', THIRD, Fr(1), Fr(sH), Fr(sL))
        print(f"  (s_H, s_L)=({sH},{sL}): " + "  ".join(
            f"X={x}: {f(sol['mu'][x], 4)}{'' if sol['onpath'][x] else '*'}"
            for x in FLOWS['sell']))
    print("  (* = off-path flow; IC belief shown)")

    section("C. All equilibria on a 21 x 21 grid, sell-only, benchmark vector")
    for r, lab in ((R0, 'r0'), (R1, 'r1'), (R2_PAPER, 'r2 = 3.6'), (Fr(9), 'r = 9')):
        report_economy(par, r, 'sell', label=lab)

    section("D. Same, buy-only (independent check, task 7)")
    for r, lab in ((R0, 'r0'), (R1, 'r1'), (R2_PAPER, 'r2 = 3.6'), (Fr(9), 'r = 9')):
        report_economy(par, r, 'buy', label=lab)

    section("E. Knife edge: k = rho Delta_T(r1)/3 = 1/18 at r1 (continuum of mixed equilibria)")
    knife = dict(par, k=Fr(1, 18))
    eqs = report_economy(knife, R1, 'sell', label='knife edge')
    print("    entry along the continuum: " + ", ".join(
        f"s_L={sL}: E={f(sol['E'], 4)}" for sH, sL, sol in eqs[::5]))

    section("F. Cutoffs (closed forms; floats)")
    rho, k = float(par['rho']), float(par['k'])
    b = 2.0
    m = 1 / (1 + math.exp(2 / b))
    M = 1 - m
    print(f"  discrete trading cutoff r* = frak_r(3k/rho)        = {frak_r(par, 3 * k / rho):.9f}")
    print(f"  no-trade boundary, passive off-path belief      = frak_r(2k/rho) = {frak_r(par, 2 * k / rho):.9f}")
    print(f"  no-trade boundary, adverse belief (e(1)=1)      = frak_r(3k/(1+rho)) = {frak_r(par, 3 * k / (1 + rho)):.9f}")
    print(f"  discrete high-cost ceiling r_C^D: g_H(r) = c_H    = {r_of_B(par, 1, par['cH']):.9f}")
    print(f"  pooling floor c_L <= B_r(1/3) holds for r <=    {r_of_B(par, Fr(1, 3), par['cL']):.9f}")
    print(f"  strong floor c_L <= g_L(r) holds for r <=       {float((par['l']**2 - par['p']**2) / (2 * par['cL'])):.9f}")
    print(f"  prior high-cost entry B_r(1/2) >= c_H for r <=  {r_of_B(par, Fr(1, 2), par['cH']):.9f} (below ell: never in domain)")
    print("  Laplace comparison (paper Prop. A.4, b = 2):")
    print(f"    r_N = frak_r(2k/rho)                    = {frak_r(par, 2 * k / rho):.9f}")
    print(f"    frak_r(k)                               = {frak_r(par, k):.9f}")
    print(f"    r_U = frak_r(k/((1-1/b) rho m))         = {frak_r(par, k / ((1 - 1 / b) * rho * m)):.9f}")
    print(f"    r_C : B_r(M) = c_H                      = {r_of_B(par, M, par['cH']):.9f}")

    section("G. Off-path belief rules and the no-trade region (sell-only)")
    for r in (Fr(3, 2), Fr(9, 5), Fr(19, 10), Fr(2)):
        row = []
        for rule in ('IC', 'passive', 'adverse'):
            sol = solve_profile(par, r, 'sell', THIRD, Fr(1), Fr(0), Fr(0), rule)
            row.append(f"{rule}: U_L(deviate)={f(sol['U']['L'])} -> "
                       f"{'NT holds' if sol['U']['L'] <= 0 else 'NT fails'}")
        n_eq = {rule: len(brute_force(par, r, 'sell', rule=rule)) for rule in ('IC', 'passive', 'adverse')}
        print(f"  r = {f(r, 2)}: " + " | ".join(row))
        print(f"           grid equilibria by rule: {n_eq}")

    section("H. Floor variants at r1 and r2 (sell-only, full selling)")
    for cL, lab in ((Fr(1), 'benchmark c_L = 1'), (Fr(0), 'c_L = 0 (strong floor)'),
                    (Fr(1, 5), 'c_L = 0.2')):
        v = dict(par, cL=cL)
        for r in (R0, R1, Fr(9)):
            eqs = brute_force(v, r, 'sell')
            for sH, sL, sol in eqs:
                print(f"  {lab:24s} r={f(r, 2)}: (s_H,s_L)=({sH},{sL}) "
                      f"E={f(sol['E'])} O_H={f(sol['OH'])}")
    print("  closed forms: E = rho + (1-rho)/6 = "
          f"{f(Fr(1, 4) + Fr(3, 4) / 6)} (strong floor); "
          f"E = 1/6 + 2 rho/3 = {f(Fr(1, 6) + Fr(2, 3) * Fr(1, 4))} (floor fails at X=-2); "
          f"O_H = (1 + 2 rho)/6 = {f((1 + 2 * Fr(1, 4)) / 6)}")

    section("I. Fixed-experiment control (Prop. A.3 analog): freeze full selling (0, 1)")
    for cL, lab in ((Fr(1), 'c_L = 1'), (Fr(0), 'c_L = 0'), (Fr(1, 5), 'c_L = 0.2')):
        v = dict(par, cL=cL)
        frozen = [solve_profile(v, r, 'sell', THIRD, Fr(1), Fr(0), Fr(1))['E'] for r in (R0, R1)]
        nt = [solve_profile(v, r, 'sell', THIRD, Fr(1), Fr(0), Fr(0))['E'] for r in (R0, R1)]
        eq = [brute_force(v, r, 'sell')[0][2]['E'] for r in (R0, R1)]
        print(f"  {lab:8s}: frozen full selling E(r0)={f(frozen[0])} E(r1)={f(frozen[1])} | "
              f"frozen no trade E(r0)={f(nt[0])} E(r1)={f(nt[1])} | "
              f"equilibrium E(r0)={f(eq[0])} E(r1)={f(eq[1])} | price hidden E = e(1/2) = "
              f"{f(entry(v, auction(v, R0), Fr(1, 2)))}, {f(entry(v, auction(v, R1), Fr(1, 2)))}")

    section("J. Investor presence lam < 1 (equal noise), r1, both menus")
    for cL in (Fr(1), Fr(0)):
        v = dict(par, cL=cL)
        for lam in (Fr(1), Fr(3, 4), Fr(1, 2)):
            for menu in ('sell', 'buy'):
                eqs = brute_force(v, R1, menu, lam=lam)
                for sH, sL, sol in eqs:
                    flows = FLOWS[menu]
                    post = " ".join(f"{x}:{f(sol['mu'][x], 3)}" for x in flows)
                    print(f"  c_L={f(cL, 1)} lam={str(lam):4s} {menu:4s}: (s_H,s_L)=({sH},{sL}) "
                          f"E={f(sol['E'])} O_H={f(sol['OH'])}  posteriors {post}")
    lam = Fr(3, 4)
    rho_ = par['rho']
    print("  closed forms (strong floor, high-cost entry at the top flow):")
    print(f"    sell-only E = rho + (1-rho)(2-lam)/6 = {f(rho_ + (1 - rho_) * (2 - lam) / 6)} at lam=3/4; "
          f"O_H = (1+2rho)/6 = {f((1 + 2 * rho_) / 6)}")
    print(f"    buy-only  E = rho + lam(1-rho)/6     = {f(rho_ + lam * (1 - rho_) / 6)} at lam=3/4; "
          f"O_H = rho/2 + lam(1-rho)/6 = {f(rho_ / 2 + lam * (1 - rho_) / 6)}")
    a1 = auction(par, R1)
    for lam in (Fr(1), Fr(3, 4), Fr(1, 2)):
        print(f"    lam={str(lam):4s}: sell-only top posterior 1/(2-lam)={f(1 / (2 - lam), 4)}, "
              f"B={f(B(a1, 1 / (2 - lam)), 4)} vs c_H=6; buy-only bottom posterior "
              f"(1-lam)/(2-lam)={f((1 - lam) / (2 - lam), 4)}, B={f(B(a1, (1 - lam) / (2 - lam)), 4)} vs c_L=1")

    section("K. Stake check (point-3 interaction): investor holds omega shares")
    for cL in (Fr(1), Fr(0)):
        v = dict(par, cL=cL)
        a = auction(v, R1)
        sol = solve_profile(v, R1, 'sell', THIRD, Fr(1), Fr(0), Fr(1))
        e = sol['e']
        mean_trade = sum(pz * e[z - 1] for z, pz in zip((-1, 0, 1), THIRD))
        mean_none = sum(pz * e[z] for z, pz in zip((-1, 0, 1), THIRD))
        loss = (a['tL'] - a['t0']) * (mean_none - mean_trade)
        print(f"  sell-only, c_L={f(cL, 1)}: L's trading gain U_L={f(sol['U']['L'])}; "
              f"stake loss per share from selling = {f(loss)}; full selling survives iff "
              f"omega <= {f(sol['U']['L'] / loss)}")
        solb = solve_profile(v, R1, 'buy', THIRD, Fr(1), Fr(1), Fr(0))
        eb = solb['e']
        mean_buy = sum(pz * eb[z + 1] for z, pz in zip((-1, 0, 1), THIRD))
        mean_none = sum(pz * eb[z] for z, pz in zip((-1, 0, 1), THIRD))
        gain = (a['tL'] - a['t0']) * (mean_buy - mean_none)
        print(f"  buy-only,  c_L={f(cL, 1)}: L's trading payoff from buying={f(solb['U']['L'])}; "
              f"stake gain per share from buying = {f(gain)}; L starts to buy (manipulation) iff "
              f"omega > {f(-solb['U']['L'] / gain)}")

    section("L. Buy-only menu with investor presence lam = 3/4, benchmark costs (c_L = 1)")
    lam = Fr(3, 4)
    m_lam = (1 - lam) / (2 - lam)
    for r, lab in ((R0, 'r0'), (R1, 'r1'), (R2_PAPER, 'r = 3.6'), (Fr(9), 'r = 9')):
        a = auction(par, r)
        print(f"  {lab}: posterior floor m_lam={f(m_lam, 4)}, B_r(m_lam)={f(B(a, m_lam), 4)} vs c_L=1; "
              f"g_H={f(a['gH'], 4)} vs c_H=6")
        report_economy(par, r, 'buy', lam=lam, label=lab)
    print(f"  closed forms: E = rho + lam(1-rho)/6 = {f(par['rho'] + lam * (1 - par['rho']) / 6)}, "
          f"O_H = rho/2 + lam(1-rho)/6 = {f(par['rho'] / 2 + lam * (1 - par['rho']) / 6)}")


if __name__ == '__main__':
    main()
