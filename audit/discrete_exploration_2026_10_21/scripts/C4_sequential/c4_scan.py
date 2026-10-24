"""C4: equilibrium table over (r, c_H) for one class correlation kappa. Print-only.

Usage (from the repository root, through the slot wrapper):
    bash audit/discrete_exploration_2026_10_21/scripts/_slots/run_slot.sh \
        .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C4_sequential/c4_scan.py KAPPA [detail]
For each point it lists every equilibrium found (pure, investor mixtures in both rounds, challenger-2
mixtures at a tie), the single-challenger reference, entry outcomes, and the round-2 information
comparison after d1 = 1 against d1 = 0 at each round-1 signal.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c4_core import Model, ST, SIG, describe  # noqa: E402


def event_post(m, nu, beta, S, event):
    mu = m.post(nu, beta, S)
    return sum(mu[s] for s in event)


def info_compare(m, eq):
    """Round-2 experiment after d1=1 against after d1=0, same round-1 history, for events j2=H and LH."""
    rows = []
    for S1 in SIG:
        nu = eq['mu1'][S1]
        rec = {}
        for d1 in (0, 1):
            beta = eq['cont'][(S1, d1)]['beta']
            rec[d1] = {}
            for name, ev in (('j2=H', ('HH', 'LH')), ('LH', ('LH',))):
                pg = event_post(m, nu, beta, 'g', ev)
                pb = event_post(m, nu, beta, 'b', ev)
                rec[d1][name] = (pg, pb)
        for name in ('j2=H', 'LH'):
            g0, b0 = rec[0][name]
            g1, b1 = rec[1][name]
            lo1, hi1 = min(g1, b1), max(g1, b1)
            lo0, hi0 = min(g0, b0), max(g0, b0)
            dom10 = lo1 <= lo0 + 1e-12 and hi0 <= hi1 + 1e-12
            dom01 = lo0 <= lo1 + 1e-12 and hi1 <= hi0 + 1e-12
            spread0, spread1 = hi0 - lo0, hi1 - lo1
            if spread0 < 1e-12 and spread1 < 1e-12:
                verdict = 'both uninformative'
            elif dom10 and not dom01:
                verdict = 'entry: more informative'
            elif dom01 and not dom10:
                verdict = 'entry: less informative'
            elif dom10 and dom01:
                verdict = 'equal'
            else:
                verdict = 'not ranked'
            rows.append((S1, name, (g0, b0), (g1, b1), verdict))
    return rows


def dominance_fixed(m):
    """Round-1 actions pinned by the memo's dominance results; valid only under the no-cascade condition."""
    q = m.prior['HH']
    r1hh = m.rho ** 2 * (1 - q / (q + m.a * (1 - q))) * m.D
    if m.nc_holds() and r1hh > m.k:
        return {'HH': 1.0, 'LL': 0.0}
    return {}


def main():
    args = sys.argv[1:]
    kappa = float(args[0]) if args else 0.0
    detail = 'detail' in args
    rs = [1.2, 3.0, 3.6]
    cHs = [3.6, 3.8, 4.0, 4.2, 4.4, 4.6, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4, 5.6, 5.8, 6.0]
    nscan = 60
    for i, x in enumerate(args):
        if x == '--r':
            rs = [float(v) for v in args[i + 1].split(',')]
        if x == '--cH':
            cHs = [float(v) for v in args[i + 1].split(',')]
        if x == '--nscan':
            nscan = int(args[i + 1])
    print(f'kappa = {kappa}  (b=2, k=0.02, rho=0.25, h=10, l=1, p=0.5)')
    for r in rs:
        for cH in cHs:
            m = Model(r=r, cH=cH, kappa=kappa)
            sing = m.single()
            stxt = '; '.join(f"E={x['E']:.4f}{' mix' if x['mixing'] else ''}{' tie' if x['tie'] else ''}" for x in sing)
            eqs = m.round1(mixed=True, fixed=dominance_fixed(m), nscan=nscan)
            empty = [e for e in eqs if 'empty_continuation' in e]
            eqs = [e for e in eqs if 'empty_continuation' not in e]
            print(f'\nr={r} cH={cH}: {len(eqs)} equilibria; no-cascade condition {m.nc_holds()}; single-challenger reference: {stxt}'
                  f'{"; empty round-2 sets at " + str(len(empty)) + " candidates" if empty else ""}')
            for eq in eqs:
                a = eq['alpha']
                buyers = ''.join(s + ' ' for s in ST if a[s] > 0.5) or 'none'
                mixs = f" mix {eq['mixing'][0]}={a[eq['mixing'][0]]:.4f}" if eq['mixing'] else ''
                r2mix = [f"{kk}:{c['mixing']}/{c['tie_mix']}" for kk, c in eq['cont'].items()
                         if (c['mixing'] or c['tie_mix']) and ((kk[1] == 1 and eq['e1'][kk[0]] > 0) or (kk[1] == 0 and eq['e1'][kk[0]] < 1))]
                print(f"  round-1 buyers [{buyers.strip()}]{mixs}; e1 g={eq['e1']['g']:.3f} b={eq['e1']['b']:.3f}; "
                      f"E1={eq['E1']:.4f} E2={eq['E2']:.4f} both={eq['E12']:.4f} "
                      f"P(d2|d1=1)={eq['p2_given_1']:.4f} P(d2|d1=0)={eq['p2_given_0']:.4f}; "
                      f"OH={eq['OH']:.4f} proceeds={eq['proceeds']:.4f} net={eq['net_surplus']:.4f}; "
                      f"pure&strict={eq['pure_all']}{'; round-2 mixing ' + ','.join(r2mix) if r2mix else ''}")
                for S1, name, (g0, b0), (g1, b1), verdict in info_compare(m, eq):
                    print(f"     info S1={S1} {name:4s}: after d1=0 post(g,b)=({g0:.4f},{b0:.4f}); "
                          f"after d1=1 post(g,b)=({g1:.4f},{b1:.4f}) -> {verdict}")
                if detail:
                    print(describe(m, eq, indent='     '))


if __name__ == '__main__':
    main()
