"""Print first-principles equilibria and closed forms side by side.

Run from the repository root:
  .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/A_three_point/tp_compare.py

Each block prints one parameter point: its region, the cutoffs, every
equilibrium that the first-principles solver finds on a rational grid of
order profiles, and the closed-form values at the same profiles.
"""
import sys
from fractions import Fraction as F

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import tp_first_principles as fp  # noqa: E402
import tp_closed_form as cf  # noqa: E402


def fmt(x):
    if isinstance(x, F):
        if x.denominator == 1:
            return f"{x.numerator}"
        return f"{x.numerator}/{x.denominator} ({float(x):.6f})"
    return str(x)


BENCH = {"h": F(10), "ell": F(1), "p": F(1, 2), "rho": F(1, 4), "cL": F(0),
         "cH": F(6), "k": F(1, 50), "r": F(3), "lam": F(1), "pi": F(1, 2)}


def point(name, changes, grid=None, extra=(), inv_rule="Z", ch_rule="E",
          offpath="IC", xi_grid=(F(0), F(1, 2), F(1)), show_cf=True):
    par = dict(BENCH)
    par.update(changes)
    if grid is None:
        grid = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]
    grid = sorted(set(list(grid) + list(extra)))
    print("=" * 78)
    print(f"POINT {name}")
    print("  changes from benchmark:", {kk: fmt(v) for kk, v in changes.items()})
    print(f"  rules: investor {inv_rule}, challenger {ch_rule}, off-path {offpath}")
    o = cf.objects(par)
    Kr, K1 = cf.K_values(par)
    print(f"  t0={fmt(o['t0'])} tH={fmt(o['tH'])} tL={fmt(o['tL'])}")
    print(f"  gH={fmt(o['gH'])} gL={fmt(o['gL'])} DeltaT={fmt(o['DeltaT'])}")
    print(f"  tau={fmt(cf.tau(par))} m_lam={fmt(cf.m_lam(par))} "
          f"region={cf.region(par)}")
    print(f"  K_rho={fmt(Kr)} K_1={fmt(K1)} K(rule E)={fmt(cf.K_rule_E(par))} "
          f"k={fmt(par['k'])}")
    eqs = fp.equilibria(par, grid, offpath=offpath, inv_rule=inv_rule,
                        ch_rule=ch_rule, xi_grid=xi_grid)
    seen = []
    for e in eqs:
        key = (e["bH"], e["bL"], tuple(sorted(e["price"].items())))
        if key in seen:
            continue
        seen.append(key)
    print(f"  first principles: {len(eqs)} schedules, {len(seen)} distinct; "
          f"grid of bH, bL = {[fmt(g) for g in grid]}")
    shown = []
    for e in eqs:
        key = (e["bH"], e["bL"], tuple(sorted(e["price"].items())))
        if key in shown:
            continue
        shown.append(key)
        print(f"  - bH={fmt(e['bH'])} bL={fmt(e['bL'])} blocks={e['blocks']}")
        print("      posterior:", {x: fmt(v) for x, v in e["post"].items()})
        print("      entry    :", {x: fmt(v) for x, v in e["entry"].items()})
        print("      price    :", {x: fmt(v) for x, v in e["price"].items()})
        print(f"      U_H(buy)={fmt(e['UH'])} U_L(buy)={fmt(e['UL'])}")
        print(f"      E={fmt(e['E'])} O_H={fmt(e['OH'])} R_T={fmt(e['RT'])}")
        print(f"      W={fmt(e['W'])} Var={fmt(e['Var'])} "
              f"profit={fmt(e['profit'])} highcost={fmt(e['highcost'])}")
        if show_cf and e["bL"] == 0 and ch_rule == "E":
            s = par["lam"] * e["bH"]
            c = cf.outcomes(par, s, e["bH"])
            diffs = {key2: c[key2] - e[key2] for key2 in
                     ("E", "OH", "RT", "W", "Var", "profit")}
            pdiff = {x: c["price"][x] - e["price"][x] for x in c["price"]
                     if x in e["price"]}
            print("      closed-form minus first-principles:",
                  {kk: fmt(v) for kk, v in diffs.items()},
                  "prices:", {x: fmt(v) for x, v in pdiff.items()})
    if show_cf and ch_rule == "E":
        print("  closed-form purchase probabilities:",
              cf.predicted_beta(par, inv_rule=inv_rule, offpath=offpath))
    return par, eqs


def main():
    # 1. Benchmark path, pi = 1/2, lam = 1, c_L = 0.
    for r in (F(6, 5), F(3), F(18, 5), F(17, 2)):
        point(f"bench r={r}", {"r": r})
    # 2. Presence.
    for lam in (F(1, 2), F(3, 4)):
        point(f"r=3 lam={lam}", {"lam": lam})
    # 3. General prior.
    for pi in (F(1, 3), F(2, 3)):
        point(f"r=3 pi={pi}", {"pi": pi})
    # 4. Investor knife-edge k = K_rho(3) = 1/18 with mixing allowed.
    point("r=3 k=1/18 rule M", {"k": F(1, 18)}, inv_rule="M")
    point("r=3 k=1/18 rule Z", {"k": F(1, 18)}, inv_rule="Z")
    # 5. Region II (prior already justifies expensive entry).
    point("r=3 cH=4", {"cH": F(4)})
    point("r=3 cH=4 lam=1/2", {"cH": F(4), "lam": F(1, 2)})
    point("r=3 cH=4 k=K1=2/9 rule M", {"cH": F(4), "k": F(2, 9)},
          inv_rule="M", extra=(F(14, 107),))
    point("r=3 cH=4 k=K1=2/9 rule M, challenger X", {"cH": F(4), "k": F(2, 9)},
          inv_rule="M", ch_rule="X", extra=(F(14, 107),), show_cf=False)
    # 6. Region III knife-edge: cH = B_3(1/2) = 103/24.
    for kk in (F(1, 18), F(1, 10), F(2, 9)):
        point(f"r=3 cH=103/24 k={kk} rule E", {"cH": F(103, 24), "k": kk})
        point(f"r=3 cH=103/24 k={kk} rule X", {"cH": F(103, 24), "k": kk},
              ch_rule="X", show_cf=False)
    # 7. Top knife-edge: cH = gH(3) = 203/24.
    point("r=3 cH=203/24 rule E", {"cH": F(203, 24)})
    point("r=3 cH=203/24 rule X", {"cH": F(203, 24)}, ch_rule="X",
          show_cf=False)
    # 8. Off-path beliefs: (3/2) K_rho(3) = 1/12.
    for kk in (F(1, 15), F(1, 12), F(1, 10)):
        point(f"r=3 k={kk} IC", {"k": kk})
        point(f"r=3 k={kk} passive", {"k": kk}, offpath="passive")
    # 9. Region I.
    point("r=3 lam=1/2 cH=2", {"lam": F(1, 2), "cH": F(2)})
    # 10. Prior-work cross-check at c_L = 1.
    point("c_L=1 r=3", {"cL": F(1)}, show_cf=False)
    point("c_L=1 r=3 lam=3/4", {"cL": F(1), "lam": F(3, 4)}, show_cf=False)
    point("c_L=1 r=3 lam=9/10", {"cL": F(1), "lam": F(9, 10)}, show_cf=False)
    point("c_L=1 r=17/2", {"cL": F(1), "r": F(17, 2)}, show_cf=False)


if __name__ == "__main__":
    main()
