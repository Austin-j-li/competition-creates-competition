"""Summaries of the T6 scans (print only).

Usage: python t6_summarize.py scan_a.csv [scan_b.csv ...]
"""
import sys
import csv
from collections import defaultdict

PAPER_E1 = 0.522757


def load(paths):
    rows = []
    for p in paths:
        with open(p) as fh:
            rows.extend(csv.DictReader(fh))
    return rows


def flags(row):
    e3 = [float(v) for v in row['E_r1'].split('|') if v]
    e36 = [float(v) for v in row['E_r2'].split('|') if v]
    ok0 = row['nt_unique_r0'] == '1'
    ok1 = int(row['n_r1']) == 1 and e3 and e3[0] > 0.25 + 1e-12
    ok2 = int(row['n_r2']) == 1 and e36 and abs(e36[0] - 0.25) < 1e-12 and row['label_r2'] != 'NT'
    nt_mid = all(row[f'nt_{r}'] == '1' for r in ('1.55', '1.60', '1.65'))
    inf_mid = all(row[f'inf_{r}'] for r in ('1.55', '1.60', '1.65'))
    return dict(ok0=ok0, ok1=ok1, ok2=ok2, coex=nt_mid and inf_mid, up=row['branch_up'] == '1',
                anyup=row['any_up'] == '1', E3=e3[0] if e3 else None, lab3=row['label_r1'])


def main():
    rows = load(sys.argv[1:])
    print(f"points: {len(rows)}; undecided cases in total: {sum(int(r['undecided']) for r in rows)}")
    F = [flags(r) for r in rows]
    n = len(rows)
    print(f"Prop. 2(i)  (NT unique at 6/5):                     {sum(f['ok0'] for f in F)}/{n}")
    print(f"Prop. 2(ii) (unique equilibrium, entry > rho at 3):  {sum(bool(f['ok1']) for f in F)}/{n}")
    print(f"Prop. 2(iii)(unique, informative, entry rho at 18/5): {sum(bool(f['ok2']) for f in F)}/{n}")
    print(f"NT and an informative equilibrium at all three middle strengths: {sum(f['coex'] for f in F)}/{n}")
    print(f"pure-entry no-sale branch with strictly rising entry:  {sum(f['up'] for f in F)}/{n}")
    print(f"any informative selection with strictly rising entry:  {sum(f['anyup'] for f in F)}/{n}")
    labs = defaultdict(int)
    for f in F:
        labs[f['lab3']] += 1
    print('profiles at r = 3:', dict(labs))

    print('\nBy theta: counts of (ii)&(iii) points; of those, coexistence; rising branch; any rising; '
          'entry at 3 range on (ii)&(iii) points; on joint points')
    byth = defaultdict(list)
    for r, f in zip(rows, F):
        byth[r['theta']].append((r, f))
    for th in sorted(byth, key=float):
        items = byth[th]
        a = [(r, f) for r, f in items if f['ok0'] and f['ok1'] and f['ok2']]
        co = [x for x in a if x[1]['coex']]
        up = [x for x in a if x[1]['up']]
        au = [x for x in a if x[1]['anyup']]
        e = [f['E3'] for _, f in a]
        eu = [f['E3'] for _, f in up]
        rng = f"[{min(e):.4f}, {max(e):.4f}]" if e else '-'
        rngu = f"[{min(eu):.4f}, {max(eu):.4f}]" if eu else '-'
        print(f"theta={float(th):.2f}: {len(a):4d} | coex {len(co):4d} | branch {len(up):4d} | any-up {len(au):4d} | "
              f"E(3) {rng} | E(3) on branch points {rngu}")

    joint = [(r, f) for r, f in zip(rows, F) if f['ok0'] and f['ok1'] and f['ok2'] and f['up']]
    print(f"\nJoint points ((i)-(iii) unique and a rising pure branch): {len(joint)}")
    print('Closest entry at 3 to the paper (top 15):')
    for r, f in sorted(joint, key=lambda x: abs(x[1]['E3'] - PAPER_E1))[:15]:
        print(f"  u={r['u']} beta={r['beta']} lam={r['lam']} theta={r['theta']}: E(3)={f['E3']:.6f} {f['lab3']}; "
              f"branch E={r['branch_E']} set={r['branch_recruit']} labels={r['branch_labels']} gap={r['branch_gap']}")
    print('Largest branch gap (top 15):')
    for r, f in sorted(joint, key=lambda x: -float(x[0]['branch_gap']))[:15]:
        print(f"  u={r['u']} beta={r['beta']} lam={r['lam']} theta={r['theta']}: E(3)={f['E3']:.6f}; "
              f"branch E={r['branch_E']} set={r['branch_recruit']} labels={r['branch_labels']} gap={r['branch_gap']}")
    # informative equilibria at the middle strengths for theta <= 1/3 on (ii)&(iii) points
    print('\ntheta <= 1/3, (ii)&(iii) points: informative equilibrium types at 1.55 (label/recruit set/entry type)')
    types = defaultdict(int)
    for r, f in zip(rows, F):
        if float(r['theta']) <= 1 / 3 and f['ok1'] and f['ok2']:
            for item in r['inf_1.55'].split(';'):
                if item:
                    lab, rec, cm = item.split('/')[:3]
                    types[(lab, rec, cm)] += 1
    for key, v in sorted(types.items(), key=lambda t: -t[1]):
        print('  ', key, v)
    print('\ntheta > 1/3, (ii)&(iii) points: informative equilibrium types at 1.55')
    types = defaultdict(int)
    for r, f in zip(rows, F):
        if float(r['theta']) > 1 / 3 and f['ok1'] and f['ok2']:
            for item in r['inf_1.55'].split(';'):
                if item:
                    lab, rec, cm = item.split('/')[:3]
                    types[(lab, rec, cm)] += 1
    for key, v in sorted(types.items(), key=lambda t: -t[1]):
        print('  ', key, v)


if __name__ == '__main__':
    main()
