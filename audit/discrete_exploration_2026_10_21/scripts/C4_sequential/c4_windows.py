"""C4: cost windows on a fine c_H grid. Print-only.

For each kappa, c_H runs from 3.60 to 6.20 in steps of 0.02.  At r in {1.2, 3, 3.6} the script lists every
equilibrium in which investor 1 uses a pure strategy (c4_core.round1 with mixed=False; round-2 strategies may
mix, and the flag P/M says whether every on-path choice is pure) and merges consecutive c_H values with the
same outcome pattern into windows.  Round-1 mixtures are not searched here; c4_scan.py covers them on a
coarser grid.
Usage: bash .../_slots/run_slot.sh .venv/bin/python -u .../c4_windows.py KAPPA
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c4_core import Model, ST  # noqa: E402


def pattern(m):
    eqs = [e for e in m.round1(mixed=False) if 'empty_continuation' not in e]
    out = []
    for e in eqs:
        buyers = ''.join(s for s in ST if e['alpha'][s] > 0.5) or '-'
        out.append((buyers, 'P' if e['pure_all'] else 'M', round(float(e['E1']), 4), round(float(e['E2']), 4),
                    round(float(e['E12']), 4), round(float(e['p2_given_1']), 4)))
    return tuple(sorted(out))


def main():
    kappa = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
    rs = (1.2, 3.0, 3.6)
    grid = [round(3.60 + 0.02 * i, 2) for i in range(131)]
    rows = []
    for cH in grid:
        pats = tuple(pattern(Model(r=r, cH=cH, kappa=kappa)) for r in rs)
        rows.append((cH, pats))
    print(f'kappa = {kappa}; each entry per strength: (round-1 buyers, P = all pure / M = round-2 mixing, E1, E2, both, '
          f'P(d2|d1=1)) for every equilibrium with pure round-1 strategies')
    start = rows[0][0]
    for i, (cH, pats) in enumerate(rows):
        last = i == len(rows) - 1
        if last or rows[i + 1][1] != pats:
            print(f'\nc_H in [{start:.2f}, {cH:.2f}]:')
            for r, pt in zip(rs, pats):
                print(f'   r = {r}: {list(pt) if pt else "no equilibrium with pure round-1 strategies"}')
            if not last:
                start = rows[i + 1][0]


if __name__ == '__main__':
    main()
