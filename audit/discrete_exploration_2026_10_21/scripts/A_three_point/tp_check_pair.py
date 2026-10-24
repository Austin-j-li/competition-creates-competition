"""Recompute the paired memo's comparison targets with this folder's modules.

Run from the repository root:
  .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/A_three_point/tp_check_pair.py

Each block prints the values found by the first-principles solver of this
folder (exact rationals) next to the target value quoted in the paired memo.
"""
import sys
from fractions import Fraction as F

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import tp_first_principles as fp  # noqa: E402
import tp_closed_form as cf  # noqa: E402

BENCH = {"h": F(10), "ell": F(1), "p": F(1, 2), "rho": F(1, 4), "cL": F(0),
         "cH": F(6), "k": F(1, 50), "r": F(3), "lam": F(1), "pi": F(1, 2)}


def fmt(x):
    if isinstance(x, F):
        if x.denominator == 1:
            return f"{x.numerator}"
        return f"{x.numerator}/{x.denominator} ({float(x):.6f})"
    return str(x)


def par_with(**kw):
    q = dict(BENCH)
    q.update(kw)
    return q


def main():
    print("1. Lower-flow challenger mixture: r=3, c_H=4, pi=2/3, lam=3/5, k=4/27")
    par = par_with(cH=F(4), pi=F(2, 3), lam=F(3, 5), k=F(4, 27))
    t = cf.tau(par)
    s_star = (par["pi"] - t) / (par["pi"] * (1 - t))
    print(f"   tau={fmt(t)} s*={fmt(s_star)} beta*={fmt(s_star / par['lam'])}"
          "  (target 93/200, 121/214, 605/642)")
    print(f"   K_1={fmt(cf.K_values(par)[1])}  (target 4/27)")
    eqs = fp.solve(par, s_star / par["lam"], F(0), inv_rule="M", ch_rule="X",
                   xi_grid=(F(0), F(1, 2), F(1)))
    for e in eqs:
        if e["entry"][-1] == F(5, 8):
            print("   entry", {x: fmt(v) for x, v in e["entry"].items()})
            print("   price", {x: fmt(v) for x, v in e["price"].items()})
            print(f"   E={fmt(e['E'])} O_H={fmt(e['OH'])} R_T={fmt(e['RT'])}"
                  "  (target 296/321, 1619/2568, 1213/963)")
    print(f"   number of schedules found at beta*: {len(eqs)}")

    print("2. Prior tie with distinct middle prices: c_H=103/24, r=3, k=1/10,"
          " beta=1/2, rates (1/4, 1/4, 13/20, 1)")
    par = par_with(cH=F(103, 24), k=F(1, 10))
    eqs = fp.solve(par, F(1, 2), F(0), inv_rule="M", ch_rule="X",
                   xi_grid=(F(0), F(8, 15), F(1)))
    for e in eqs:
        if e["entry"][0] == F(1, 4) and e["entry"][1] == F(13, 20):
            print("   entry", {x: fmt(v) for x, v in e["entry"].items()})
            print("   price", {x: fmt(v) for x, v in e["price"].items()},
                  " (target P0=59/96, P1=149/160)")
            print(f"   E={fmt(e['E'])} O_H={fmt(e['OH'])} R_T={fmt(e['RT'])}"
                  "  (target 107/240, 61/240, 4553/5760)")
            print(f"   U_H(buy)={fmt(e['UH'])} blocks={e['blocks']}")
    print("   passive belief, zero rule, k=1/10: equilibria at the prior tie")
    for bH in (F(0), F(1)):
        for e in fp.solve(par, bH, F(0), inv_rule="Z", ch_rule="X",
                          offpath="passive", xi_grid=(F(0), F(1))):
            print(f"     bH={fmt(bH)} entry={ {x: fmt(v) for x, v in e['entry'].items()} }"
                  f" E={fmt(e['E'])} O_H={fmt(e['OH'])} R_T={fmt(e['RT'])}")

    print("3. Top tie: c_H=203/24, r=3, sigma_2=1/2  (target 5/16, 3/16, 263/384)")
    par = par_with(cH=F(203, 24))
    for e in fp.solve(par, F(1), F(0), ch_rule="X", xi_grid=(F(1, 2),)):
        print(f"   E={fmt(e['E'])} O_H={fmt(e['OH'])} R_T={fmt(e['RT'])}")

    print("4. Passive gap at r=9/5, k=1/50  (target K=2/135, N=1/45)")
    for lam in (F(1), F(1, 5)):
        par = par_with(r=F(9, 5), lam=lam)
        K = cf.K_rule_E(par)
        grid = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]
        for rule in ("Z", "M"):
            eqs_ic = fp.equilibria(par, grid, inv_rule=rule)
            eqs_pa = fp.equilibria(par, grid, inv_rule=rule, offpath="passive")
            print(f"   lam={fmt(lam)} rule {rule}: K={fmt(K)} N={fmt(F(3, 2) * K)};"
                  f" IC equilibria bH={sorted(set(fmt(e['bH']) for e in eqs_ic))};"
                  f" passive equilibria={len(eqs_pa)}")

    print("5. Passive belief at k=K (r=3, k=1/18): rule Z and rule M")
    par = par_with(k=F(1, 18))
    grid = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]
    for rule in ("Z", "M"):
        eqs = fp.equilibria(par, grid, inv_rule=rule, offpath="passive")
        print(f"   rule {rule}: bH={sorted(set(fmt(e['bH']) for e in eqs))}")

    print("6. Trade set in r is not an interval: c_H=4, k=1/5, pi=1/2")
    for r in (F(3), F(5), F(7)):
        par = par_with(cH=F(4), k=F(1, 5), r=r)
        eqs = fp.equilibria(par, [F(0), F(1)])
        print(f"   r={fmt(r)} region={cf.region(par)} K={fmt(cf.K_rule_E(par))}"
              f" bH={sorted(set(fmt(e['bH']) for e in eqs))}")

    print("7. Presence values of the paired memo at r=3 (lam = 4/5, 3/5, 2/5, 1/5, 19/20)")
    for lam in (F(19, 20), F(4, 5), F(3, 5), F(2, 5), F(1, 5)):
        par = par_with(lam=lam)
        for e in fp.equilibria(par, [F(0), F(1)]):
            print(f"   lam={fmt(lam)}: E={fmt(e['E'])} O_H={fmt(e['OH'])}"
                  f" R_T={fmt(e['RT'])}")


if __name__ == "__main__":
    main()


def count_paired_grid():
    """Recount the paired memo's base-grid failures from the closed forms.

    Grid of the paired memo: lam in 7 values, pi in {1/2, 1/3, 2/3},
    c_H in {4,...,8}, r = n/20 (n = 21..190), and k = n/1000 (n = 1..500)
    or n/100 (n = 51..300).  By the theorem, the outcome does not depend on
    lam, so each cell count is multiplied by 7.
    """
    ks = [F(n, 1000) for n in range(1, 501)] + [F(n, 100) for n in range(51, 301)]
    ks = sorted(set(ks))
    pass_zero = pass_any = ic_any_multi = ties = 0
    for pi in (F(1, 2), F(1, 3), F(2, 3)):
        for cH in (4, 5, 6, 7, 8):
            for n in range(21, 191):
                par = par_with(pi=pi, cH=F(cH), r=F(n, 20))
                if cf.B(par, pi) == par["cH"]:
                    ties += 1
                K = cf.K_rule_E(par)
                for k in ks:
                    if K <= k < F(3, 2) * K:
                        pass_zero += 1
                    if K < k < F(3, 2) * K:
                        pass_any += 1
                    if k == K:
                        ic_any_multi += 1
    print("8. Recount of the paired memo's base grid (times 7 presence values)")
    print(f"   prior ties on the grid: {ties}")
    print(f"   passive, zero rule, no equilibrium: {7 * pass_zero}  (target 1,332,674)")
    print(f"   passive, any rule, no equilibrium: {7 * pass_any}  (target 1,332,478)")
    print(f"   IC, any rule, multiple equilibria (k = K): {7 * ic_any_multi}  (target 196)")


if __name__ == "__main__":
    count_paired_grid()
