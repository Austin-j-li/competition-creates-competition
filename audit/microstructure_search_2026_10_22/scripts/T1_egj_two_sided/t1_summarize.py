"""Summaries of the scans (prints maps; reads scan_bench_*.csv and scan_interval_*.csv).

Run from the repository root:
  .venv/bin/python audit/microstructure_search_2026_10_22/scripts/T1_egj_two_sided/t1_summarize.py
"""
import csv
import glob
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
RHO = 0.25


def parse(field):
    out = []
    if not field:
        return out
    for part in field.split(';'):
        lab, kind, cm, E, OH, a, b = part.split('|')
        out.append(dict(label=lab, kind=kind, cm=cm, E=float(E), OH=float(OH), a=float(a), b=float(b)))
    return out


def load(mode):
    data = {}
    und = 0
    for fn in sorted(glob.glob(str(HERE / f'scan_{mode}_*.csv'))):
        with open(fn) as fh:
            for row in csv.DictReader(fh):
                key = (F(row['theta']), F(row['lam']), F(row['r']), row['rules'])
                data[key] = parse(row['equilibria'])
                und += int(row['n_undecided'])
    return data, und


SHORT = {'T': 'T', 'BNS': 'B', 'SNB': 'S', 'NT': 'N', 'full buy, partial sell': 'F',
         'partial buy, full sell': 'f', 'partial buy, no sell': 'p', 'no buy, partial sell': 'q',
         'partial buy, partial sell': 'm'}


def code(eqs):
    if not eqs:
        return '.'
    if len(eqs) == 1:
        return SHORT.get(eqs[0]['label'], '?') + ('*' if eqs[0]['cm'] else '')
    return str(len(eqs)) if len(eqs) < 10 else '+'


def informative(q):
    return q['label'] != 'NT'


def main():
    data, und = load('bench')
    if not data:
        print('no bench data')
        return
    thetas = sorted({k[0] for k in data})
    lams = sorted({k[1] for k in data})
    print(f'bench scan: {len(data)} rows; undecided root cases: {und}')
    print('Codes: T full orders; F full buy + partial sell; f partial buy + full sell; B buy-not-sell;')
    print('S sell-not-buy; p partial buy, no sell; q no buy, partial sell; m both partial; N no trade;')
    print('* challenger mixing; a digit = number of equilibria; . = none')

    for rule in ('MX_IC', 'ZE_IC', 'MX_PA'):
        for r in (F(6, 5), F(3), F(18, 5)):
            print(f'\n=== equilibrium set at r = {float(r)}, rules {rule} (rows theta, columns lam = 0.05 ... 1.00)')
            print('theta  ' + ' '.join(f'{float(l):>4.2f}' for l in lams))
            for th in thetas:
                cells = [code(data.get((th, l, r, rule), [])) for l in lams]
                print(f'{float(th):5.2f}  ' + ' '.join(f'{c:>4}' for c in cells))

    # Prop 2 (ii): unique informative equilibrium with entry above rho at r1 = 3
    print('\n=== Prop. 2(ii) at r1 = 3 (MX_IC): unique equilibrium, its entry (rows theta, cols lam)')
    for th in thetas:
        cells = []
        for l in lams:
            eqs = data.get((th, l, F(3), 'MX_IC'), [])
            if len(eqs) == 1 and informative(eqs[0]) and eqs[0]['E'] > RHO + 1e-12:
                cells.append(f"{eqs[0]['E']:.3f}")
            else:
                cells.append('  -  ')
        print(f'{float(th):5.2f}  ' + ' '.join(cells))

    # every equilibrium at r1 = 3 informative with entry above rho?
    for rule in ('MX_IC', 'ZE_IC', 'MX_PA'):
        rows = [(k_, eqs) for k_, eqs in data.items() if k_[2] == F(3) and k_[3] == rule]
        n_none = sum(1 for k_, eqs in rows if not eqs)
        n_nt = sum(1 for k_, eqs in rows if any(q['label'] == 'NT' for q in eqs))
        allE = [q['E'] for k_, eqs in rows for q in eqs]
        allO = [q['OH'] for k_, eqs in rows for q in eqs]
        print(f'\n=== r1 = 3, rules {rule}: grid points {len(rows)}; without equilibrium {n_none}; with no trade {n_nt};'
              f' entry over all equilibria in [{min(allE):.6f}, {max(allE):.6f}]; O_H in [{min(allO):.6f}, {max(allO):.6f}]')
        multi = [(float(k_[0]), float(k_[1])) for k_, eqs in rows if len(eqs) > 1]
        if multi:
            Es = [q['E'] for k_, eqs in rows if len(eqs) > 1 for q in eqs]
            print(f'    {len(multi)} points with several equilibria; their entry levels lie in [{min(Es):.6f}, {max(Es):.6f}];'
                  f' theta range {min(t for t, l in multi):.2f}-{max(t for t, l in multi):.2f}, lam range {min(l for t, l in multi):.2f}-{max(l for t, l in multi):.2f}')

    # Prop 2 (iii): minimum entry at r2 = 3.6
    mins = [min(q['E'] for q in eqs) for (th, l, r, rule), eqs in data.items() if r == F(18, 5) and eqs]
    print(f'\n=== r2 = 3.6: minimum entry over all equilibria and grid points and rule sets: {min(mins):.6f} (rho = 0.25)')
    empty36 = [(float(k[0]), float(k[1]), k[3]) for k, eqs in data.items() if k[2] == F(18, 5) and not eqs]
    print(f'    grid points with no equilibrium at 3.6: {len(empty36)} {empty36[:8]}')

    # Prop 3 at 1.55, 1.60, 1.65
    R3 = (F(31, 20), F(8, 5), F(33, 20))
    for rule in ('MX_IC', 'ME_IC', 'ZE_IC', 'MX_PA'):
        print(f'\n=== Prop. 3 at r = 1.55, 1.60, 1.65, rules {rule}')
        print('cell: C = no trade coexists with an informative equilibrium at all three strengths;')
        print('      U = also an upward pure-entry branch (p or B at each strength, entry strictly rising);')
        print('      c = coexistence at some but not all three; . = none')
        print('theta  ' + ' '.join(f'{float(l):>4.2f}' for l in lams))
        for th in thetas:
            cells = []
            for l in lams:
                co = []
                branch = []
                for r in R3:
                    eqs = data.get((th, l, r, rule), [])
                    hasNT = any(q['label'] == 'NT' for q in eqs)
                    inf = [q for q in eqs if informative(q)]
                    co.append(hasNT and bool(inf))
                    cand = [q['E'] for q in inf if q['label'] in ('partial buy, no sell', 'BNS') and not q['cm']]
                    branch.append(cand)
                if all(co):
                    up = all(branch) and any(
                        e1 < e2 < e3 for e1 in branch[0] for e2 in branch[1] for e3 in branch[2])
                    cells.append('U' if up else 'C')
                elif any(co):
                    cells.append('c')
                else:
                    cells.append('.')
            print(f'{float(th):5.2f}  ' + ' '.join(f'{c:>4}' for c in cells))

    # joint region: Prop 2 (i)-(ii) with a unique informative equilibrium at r1, and U at 1.55-1.65
    print('\n=== joint: unique informative equilibrium at r1 = 3 AND U at 1.55-1.65 (MX_IC); entry at r1 shown')
    for th in thetas:
        cells = []
        for l in lams:
            eqs3 = data.get((th, l, F(3), 'MX_IC'), [])
            ok2 = len(eqs3) == 1 and informative(eqs3[0]) and eqs3[0]['E'] > RHO
            branch = []
            co = True
            for r in R3:
                eqs = data.get((th, l, r, 'MX_IC'), [])
                co &= any(q['label'] == 'NT' for q in eqs) and any(informative(q) for q in eqs)
                branch.append([q['E'] for q in eqs if q['label'] in ('partial buy, no sell', 'BNS') and not q['cm']])
            up = co and all(branch) and any(e1 < e2 < e3 for e1 in branch[0] for e2 in branch[1] for e3 in branch[2])
            cells.append(f"{eqs3[0]['E']:.3f}{SHORT.get(eqs3[0]['label'], '?')}" if (ok2 and up) else '   -  ')
        print(f'{float(th):5.2f}  ' + ' '.join(cells))

    # details for selected candidates
    for th, l in ((F(1, 10), F(3, 5)), (F(1, 10), F(4, 5)), (F(3, 20), F(4, 5)), (F(2, 25), F(4, 5)),
                  (F(3, 25), F(7, 10)), (F(1, 5), F(3, 5))):
        print(f'\n--- details theta={float(th)}, lam={float(l)}')
        for r in (F(6, 5),) + R3 + (F(3), F(18, 5)):
            for rule in ('MX_IC', 'ZE_IC', 'MX_PA'):
                eqs = data.get((th, l, r, rule))
                if eqs is None:
                    continue
                s = ', '.join(f"{q['label']}{'*' + q['cm'] if q['cm'] else ''}: E={q['E']:.6f} O_H={q['OH']:.6f} (a={q['a']:.4f}, b={q['b']:.4f})"
                              for q in sorted(eqs, key=lambda q: q['E']))
                print(f'   r={float(r):.2f} {rule}: {s}')

    # interval scan: coexistence intervals and branch monotonicity
    idata, iund = load('interval')
    if idata:
        print(f'\n=== interval scan: {len(idata)} rows; undecided root cases: {iund}')
        pairs = sorted({(k[0], k[1]) for k in idata})
        for th, l in pairs:
            rs = sorted(k[2] for k in idata if k[0] == th and k[1] == l)
            co = [r for r in rs if any(q['label'] == 'NT' for q in idata[(th, l, r, 'MX_IC')]) and
                  any(informative(q) for q in idata[(th, l, r, 'MX_IC')])]
            nt = [r for r in rs if any(q['label'] == 'NT' for q in idata[(th, l, r, 'MX_IC')])]
            pb = [(r, max(q['E'] for q in idata[(th, l, r, 'MX_IC')] if q['label'] == 'partial buy, no sell' and not q['cm']))
                  for r in rs if any(q['label'] == 'partial buy, no sell' and not q['cm'] for q in idata[(th, l, r, 'MX_IC')])]
            mono = all(pb[i][1] < pb[i + 1][1] for i in range(len(pb) - 1)) if len(pb) > 1 else None
            print(f'theta={float(th):.2f} lam={float(l):.1f}: NT on [{float(min(nt)):.2f},{float(max(nt)):.2f}];'
                  f' coexistence on {len(co)} grid strengths in [{float(min(co)) if co else float("nan"):.2f},{float(max(co)) if co else float("nan"):.2f}];'
                  f' pure partial-buy branch on [{float(pb[0][0]) if pb else float("nan"):.2f},{float(pb[-1][0]) if pb else float("nan"):.2f}]'
                  f' with entry {pb[0][1] if pb else float("nan"):.4f} -> {pb[-1][1] if pb else float("nan"):.4f}, strictly rising: {mono}')


if __name__ == '__main__':
    main()
