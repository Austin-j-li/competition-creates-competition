"""EGJ's own case: equal three-point noise (theta = 1/3), two-sided unit orders, presence lam.

Prints exact (fractions) values for the memo's analytical results R1-R9.
Run from the repository root:
  .venv/bin/python audit/microstructure_search_2026_10_22/scripts/T1_egj_two_sided/t1_equal_weights.py
"""
import sys
from fractions import Fraction as F
from math import exp
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from t1_core import (FLOWS, bench, auction, auction_by_integration, flow_laws, posteriors,
                     entry_rule_E, entry_options, order_payoffs, outcomes, fmt, Iv,
                     r_of_spread, r_ceiling)

R0, R1, R2 = F(6, 5), F(3), F(18, 5)
LAMS = [F(1, 10), F(1, 4), F(1, 2), F(4, 7), F(82, 141), F(3, 5), F(5, 8), F(2686, 4245),
        F(7, 10), F(4, 5), F(6, 7), F(9, 10), F(1)]
IC = {2: F(1), -2: F(0)}          # EGJ's directional ("informed") completion
PASSIVE = {2: F(1, 2), -2: F(1, 2)}

PROFILES = {'NT': (0, 0), 'T': (1, 1), 'BNS': (1, 0), 'SNB': (0, 1)}


def header(s):
    print()
    print('=' * 100)
    print(s)
    print('=' * 100)


def evaluate(P, a, b, v_off, rule_X_e=None):
    """Exact schedule under rule E (or a given entry override at tie flows)."""
    A = auction(P)
    fH, fL = flow_laws(P, a, b)
    mu, used = posteriors(P, fH, fL, v_off)
    e = {x: entry_rule_E(P, A, mu[x]) for x in FLOWS}
    if rule_X_e:
        e.update(rule_X_e)
    pay = order_payoffs(P, A, mu, e)
    out = outcomes(P, A, fH, fL, mu, e)
    return A, fH, fL, mu, used, e, pay, out


def is_eq(P, a, b, pay, investor_rule):
    """Investor conditions for effective rates (a, b); rule 'Z' or 'M'."""
    k, lam = P['k'], P['lam']
    GH, GL = pay[('H', 1)], pay[('L', -1)]
    ok = True
    for rate, G in ((a, GH), (b, GL)):
        if investor_rule == 'Z':
            if rate == lam:
                ok &= G > k
            elif rate == 0:
                ok &= G <= k
            else:
                ok = False
        else:
            if rate == lam:
                ok &= G >= k
            elif rate == 0:
                ok &= G <= k
            else:
                ok &= G == k
    # wrong-way orders must not beat zero
    ok &= pay[('H', -1)] - k < 0 and pay[('L', 1)] - k < 0
    return ok


def main():
    header('A. Auction objects: closed forms against piecewise integration (exact)')
    for r in (R0, F(31, 20), F(8, 5), F(33, 20), R1, R2):
        P = bench(r=r)
        A, I = auction(P), auction_by_integration(P)
        diffs = [A[key] - I[key] for key in ('t0', 'tH', 'tL', 'gH', 'gL', 'D')]
        print(f"r={fmt(r, 4):>14}: t0={fmt(A['t0'])}, tH={fmt(A['tH'])}, tL={fmt(A['tL'])}, gH={fmt(A['gH'])},"
              f" gL={fmt(A['gL'])}, Delta={fmt(A['D'])}, tau={fmt(A['tau'])}; max |closed - integral| = {max(abs(x) for x in diffs)}")
        print(f"    B_r(1/2) = {fmt(A['gL'] + (A['gH'] - A['gL']) / 2)} (< c_H = 6), b*(r) = 2 - 1/tau = {fmt(2 - 1 / A['tau'])},"
              f" kappa = 3k/(rho Delta) = {fmt(3 * P['k'] / (P['rho'] * A['D']))}")

    header('B. Posteriors of the four pure profiles (equal weights), against the closed forms')
    for lam in (F(1, 2), F(3, 5), F(1)):
        for name, (sa, sb) in PROFILES.items():
            P = bench(lam=lam)
            a, b = lam * sa, lam * sb
            fH, fL = flow_laws(P, a, b)
            mu, used = posteriors(P, fH, fL, {2: None, -2: None})
            row = []
            for x in FLOWS:
                row.append(fmt(mu[x], 4) if used[x] else 'unused')
            print(f"lam={fmt(lam, 3):>6} {name:>3}: mu(-2..2) = " + ' | '.join(row))
        nu = 1 / (2 - lam)
        print(f"    closed forms: 1/(2-lam) = {fmt(nu, 4)}, (1-lam)/(2-lam) = {fmt(1 - nu, 4)}")

    header('C. Pure profiles at the benchmark strengths for each lam (IC completion; rule E)')
    print('Columns: equilibrium under (rule Z, rule M); gross payoffs G_H(buy), G_L(sell); entry by flow; E, O_H, R_T, W')
    for r in (R0, R1, R2):
        for lam in LAMS:
            P = bench(r=r, lam=lam)
            for name, (sa, sb) in PROFILES.items():
                a, b = lam * sa, lam * sb
                A, fH, fL, mu, used, e, pay, out = evaluate(P, a, b, IC)
                eqZ, eqM = is_eq(P, a, b, pay, 'Z'), is_eq(P, a, b, pay, 'M')
                if not (eqZ or eqM):
                    continue
                ent = ','.join(fmt(e[x], 2).split(' = ')[0] for x in FLOWS)
                print(f"r={fmt(r, 2):>10} lam={fmt(lam, 4):>18} {name:>3}: eq(Z,M)=({eqZ},{eqM}) "
                      f"G_H={float(pay[('H', 1)]):.6f} G_L={float(pay[('L', -1)]):.6f} e=({ent}) "
                      f"E={fmt(out['E'])} O_H={fmt(out['OH'])} R_T={fmt(out['RT'])} W={fmt(out['W'])}")

    header('D. Closed forms at r1 = 3 under full orders T: entry and ownership against lam')
    for lam in LAMS:
        P = bench(r=R1, lam=lam)
        A, fH, fL, mu, used, e, pay, out = evaluate(P, lam, lam, IC)
        bstar = 2 - 1 / A['tau']
        if lam >= bstar:
            E_cf, O_cf, R_cf = F(1, 2), F(1, 4) + lam / 8, F(13, 16) + lam / 12
        else:
            E_cf, O_cf = F(1, 4) + lam / 8, F(1, 8) + lam / 8
            R_cf = None
        print(f"lam={fmt(lam, 4):>18}: E={fmt(out['E'])} (closed form {fmt(E_cf)}), O_H={fmt(out['OH'])} (closed form {fmt(O_cf)}),"
              f" R_T={fmt(out['RT'])}" + (f" (closed form {fmt(R_cf)})" if R_cf is not None else ''))

    header('E. Normalised payoffs gamma = 3G/(rho Delta) and the band [ell_lam, 1] (equal weights)')
    for lam in LAMS:
        ell_lam = F(1, 2) + (1 - lam) / (2 - lam)
        print(f"lam={fmt(lam, 4):>18}: ell_lam = (4-3lam)/(2(2-lam)) = {fmt(ell_lam)};"
              f" SNB with recruitment at X=1 needs kappa >= 1/2 + (1-lam)/(rho(2-lam)) = {fmt(F(1, 2) + (1 - lam) / ((2 - lam) * F(1, 4)))}")
    print('kappa at the benchmark strengths:', ', '.join(
        f"r={fmt(r, 2)}: {fmt(3 * F(1, 50) / (F(1, 4) * auction(bench(r=r))['D']))}" for r in (R0, R1, R2)))

    header('F. Exact check of the closed-form correspondence on the band (mixed points are rational)')
    # pick strengths inside the band for several lam and verify each predicted equilibrium exactly
    k = F(1, 50)
    for lam in (F(1), F(9, 10), F(4, 5), F(3, 5)):
        for r in (F(2), F(21, 10), F(11, 5), F(12, 5), F(5, 2)):
            P = bench(r=r, lam=lam)
            A = auction(P)
            kappa = 3 * k / (P['rho'] * A['D'])
            ell_lam = F(1, 2) + (1 - lam) / (2 - lam)
            if not (ell_lam < kappa < 1):
                continue
            y = kappa - F(1, 2)
            s = (1 - 2 * y) / (1 - y)                      # u(s) = kappa - 1/2
            bstar = 2 - 1 / A['tau']
            yR = P['rho'] * (kappa - F(1, 2))
            bR = (1 - 2 * yR) / (1 - yR)                   # u(bR) = rho (kappa - 1/2)
            cands = {'BNS': (lam, F(0)), 'SNB': (F(0), lam), '(s,s)': (s, s), '(s,bR)': (s, bR)}
            line = f"lam={fmt(lam, 3):>6} r={fmt(r, 3):>9} kappa={float(kappa):.6f} s={float(s):.6f} b*={float(bstar):.6f} bR={float(bR):.6f}:"
            for name, (a, b) in cands.items():
                if not (0 <= a <= lam and 0 <= b <= lam):
                    line += f" {name}=outside"
                    continue
                A_, fH, fL, mu, used, e, pay, out = evaluate(P, a, b, IC)
                ok = is_eq(P, a, b, pay, 'M')
                line += f" {name}={'EQ' if ok else 'no'}(E={float(out['E']):.4f})"
            # challenger mixing at b = b*: H indifferent needs e1 with 1/2 + (e1/rho) u(b*) = kappa
            ub = (1 - bstar) / (2 - bstar)
            e1 = P['rho'] * (kappa - F(1, 2)) / ub
            if P['rho'] <= e1 <= 1 and 0 < bstar < lam:
                A_, fH, fL, mu, used, e, pay, out = evaluate(P, s, bstar, IC, rule_X_e={1: e1})
                ok = is_eq(P, s, bstar, pay, 'M') and mu[1] == A_['tau']
                line += f" (s,b*;e1={float(e1):.4f})={'EQ' if ok else 'no'}(E={float(out['E']):.4f})"
            print(line)

    header('G. Strength thresholds (rational brackets, width < 1e-50)')
    P = bench()
    for name, d in (('no-trade boundary, IC: frak r(3k/rho)', 3 * P['k'] / P['rho']),
                    ('no-trade boundary, passive: frak r(2k/rho) (= paper r_N)', 2 * P['k'] / P['rho']),
                    ('full-order boundary at lam=1: frak r(6k/rho)', 6 * P['k'] / P['rho'])):
        iv = r_of_spread(d)
        print(f"{name}: [{float(iv.lo):.12f}, {float(iv.hi):.12f}]")
    for lam in LAMS + [F(632121, 1000000)]:
        nu = 1 / (2 - lam)
        rc = r_ceiling(P, nu)
        ell_lam = F(1, 2) + (1 - lam) / (2 - lam)
        rU = r_of_spread(3 * P['k'] / (P['rho'] * ell_lam))
        print(f"lam={fmt(lam, 6):>22}: X=1 posterior 1/(2-lam)={float(nu):.6f}; interior ceiling r_C(1/(2-lam)) in "
              f"[{float(rc.lo):.9f}, {float(rc.hi):.9f}]; full orders unique for r > {float(rU.hi):.9f}")
    rc1 = r_ceiling(P, F(1))
    print(f"top-flow ceiling r_C(1) in [{float(rc1.lo):.12f}, {float(rc1.hi):.12f}] (= 4 + 3 sqrt(7)/2 = {4 + 1.5 * 7 ** 0.5:.12f})")
    lam_paper = 1 - exp(-1)
    M = 1 / (1 + exp(-1))
    print(f"paper calibration: lam = 1 - e^(-2/b) at b = 2 is {lam_paper:.9f}; then 1/(2-lam) = {1 / (2 - lam_paper):.9f} = M = {M:.9f}")
    # bracket of the paper's r_C using a rational enclosure of M
    Mlo, Mhi = F(731058578630, 10 ** 12), F(731058578631, 10 ** 12)
    a_ = r_ceiling(P, Mlo)
    b_ = r_ceiling(P, Mhi)
    print(f"r_C(M) in [{float(min(a_.lo, b_.lo)):.9f}, {float(max(a_.hi, b_.hi)):.9f}] (paper: 3.592658519)")

    header('H. Prop. 2(iii): every equilibrium at r2 = 18/5 has entry above rho (bound check, exact)')
    P = bench(r=R2)
    A = auction(P)
    bound = P['rho'] * A['D'] * (1 - A['tau']) / 2
    print(f"g_H(18/5) = {fmt(A['gH'])} > c_H = 6, so X = 2 recruits whenever it is used.")
    print(f"If a = 0 and entry = rho, H's buy earns at least rho Delta (1-theta)(1-tau) >= rho Delta (1-tau)/2 = {fmt(bound)} > k = 1/50: {bound > P['k']}")
    for lam in LAMS:
        P = bench(r=R2, lam=lam)
        A_, fH, fL, mu, used, e, pay, out = evaluate(P, lam, lam, IC)
        print(f"lam={fmt(lam, 4):>18}: unique T at 18/5, entry = {fmt(out['E'])}, O_H = {fmt(out['OH'])}")
    # largest k for which the bound still excludes a return, for every theta in (0, 1/2)
    print(f"the exclusion holds for every k < rho Delta(18/5)(1 - tau(18/5))/2 = {float(bound):.6f};"
          f" with equal weights trade at r1 needs k <= rho Delta(3)/3 = {fmt(F(1, 4) * auction(bench(r=R1))['D'] / 3)}")
    P3 = bench(r=R2)
    A3 = auction(P3)
    g_min = (F(1, 2) + (1 - A3['tau'])) * P3['rho'] * A3['D'] / 3
    print(f"equal weights, any k: a = 0 with no recruiting flow at 18/5 gives G_H >= (rho Delta/3)(1/2 + 1 - tau) = {fmt(g_min)}"
          f" > rho Delta(3)/3 = {fmt(F(1, 4) * auction(bench(r=R1))['D'] / 3)}")

    header('I. Prop. A.9 at r1 = 3: price access against hidden prices (same full orders in both)')
    for lam in (F(1, 2), F(4, 7), F(3, 5), F(632121, 10 ** 6), F(4, 5), F(1)):
        P = bench(r=R1, lam=lam)
        A, fH, fL, mu, used, e, pay, out = evaluate(P, lam, lam, IC)
        # hidden price: entry rho at every flow; check full orders are still the unique outcome
        eh = {x: P['rho'] for x in FLOWS}
        payh = order_payoffs(P, A, mu, eh)
        outh = outcomes(P, A, fH, fL, mu, eh)
        kappa = 3 * P['k'] / (P['rho'] * A['D'])
        ell_lam = F(1, 2) + (1 - lam) / (2 - lam)
        print(f"lam={fmt(lam, 4):>20}: hidden-price payoffs G_H={fmt(payh[('H', 1)])}, G_L={fmt(payh[('L', -1)])} > k: "
              f"{payh[('H', 1)] > P['k'] and payh[('L', -1)] > P['k']} (kappa={fmt(kappa)} < ell_lam={fmt(ell_lam)}: {kappa < ell_lam})")
        print(f"      access: E={fmt(out['E'])}, R_T={fmt(out['RT'])}, W={fmt(out['W'])}; hidden: E={fmt(outh['E'])}, R_T={fmt(outh['RT'])}, W={fmt(outh['W'])};"
              f" dR_T={fmt(out['RT'] - outh['RT'])}, dW={fmt(out['W'] - outh['W'])}")

    header('J. Passive beliefs: the no-equilibrium interval and the band without investor mixing')
    for r in (F(7, 4), F(9, 5), F(19, 10), F(39, 20)):
        P = bench(r=r, lam=F(1))
        A = auction(P)
        kappa = 3 * P['k'] / (P['rho'] * A['D'])
        res = []
        for name, (sa, sb) in PROFILES.items():
            a, b = P['lam'] * sa, P['lam'] * sb
            A_, fH, fL, mu, used, e, pay, out = evaluate(P, a, b, PASSIVE)
            res.append(f"{name}:{'EQ' if is_eq(P, a, b, pay, 'M') else 'no'}")
        print(f"r={fmt(r, 4):>12} kappa={float(kappa):.6f}: passive pure profiles " + ' '.join(res))


if __name__ == '__main__':
    main()
