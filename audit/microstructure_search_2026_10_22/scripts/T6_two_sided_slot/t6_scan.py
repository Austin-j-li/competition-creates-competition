"""Scan of the T6 model over (u, beta, theta), with u = lam / c and c = (1 - lam) beta.

Usage: python t6_scan.py CHUNK NCHUNKS OUTFILE [grid]
The scan covers the Prop. 2 strip 82/59 <= u < 2686/1559 (full-purchase top posterior in
[tau(3), tau(18/5))). Each grid point is solved exactly at r in {6/5, 31/20, 8/5, 33/20, 3, 18/5}
(investor rule M, challenger rule X). The script prints nothing but progress; it writes one CSV row
per grid point with summaries, not raw equilibria.
"""
import sys
import csv
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from t6_core import bench, enumerate_equilibria, fl, FLOWS  # noqa: E402

STRENGTHS = (F(6, 5), F(31, 20), F(8, 5), F(33, 20), F(3), F(18, 5))
MID = (F(31, 20), F(8, 5), F(33, 20))


def grid(name):
    if name == 'main':
        us = [F(140 + 2 * i, 100) for i in range(17)]            # 1.40 ... 1.72
        betas = [F(i, 20) for i in range(1, 11)]                  # 0.05 ... 0.50
        thetas = [F(i, 50) for i in range(1, 25)]                 # 0.02 ... 0.48
    elif name == 'fine':
        us = [F(140 + i, 100) for i in range(33)]                 # 1.40 ... 1.72
        betas = [F(i, 100) for i in (40, 42, 44, 45, 46, 47, 48, 49, 50)]
        thetas = [F(i, 100) for i in range(26, 46)]               # 0.26 ... 0.45
    elif name == 'pocket':
        us = [F(160 + i, 100) for i in range(13)] + [F(17225, 10000)]   # 1.60 ... 1.72, 1.7225
        betas = [F(44, 100), F(46, 100), F(48, 100), F(49, 100), F(495, 1000), F(1, 2)]
        thetas = [F(340 + 5 * i, 1000) for i in range(13)]               # 0.340 ... 0.400
    else:
        raise ValueError(name)
    pts = []
    for u in us:
        for b in betas:
            lam = u * b / (1 + u * b)
            for th in thetas:
                pts.append((u, b, lam, th))
    return pts


def summarize(P):
    row = {}
    eqs_by_r = {}
    und_total = 0
    for r in STRENGTHS:
        P['r'] = r
        eqs, und, M = enumerate_equilibria(P, investor='M', challenger='X')
        eqs_by_r[r] = eqs
        und_total += len(und)
    row['undecided'] = und_total
    # r = 6/5
    e0 = eqs_by_r[F(6, 5)]
    row['nt_unique_r0'] = int(len(e0) == 1 and e0[0]['label'] == 'NT')
    # r = 3
    e3 = eqs_by_r[F(3)]
    row['n_r1'] = len(e3)
    row['label_r1'] = '|'.join(q['label'] for q in e3)
    row['E_r1'] = '|'.join(f"{fl(q['out']['E']):.6f}" for q in e3)
    row['recruit_r1'] = '|'.join(''.join(str(x) for x in q['recruit']) for q in e3)
    # r = 18/5
    e36 = eqs_by_r[F(18, 5)]
    row['n_r2'] = len(e36)
    row['label_r2'] = '|'.join(q['label'] for q in e36)
    row['E_r2'] = '|'.join(f"{fl(q['out']['E']):.6f}" for q in e36)
    # middle strengths
    chains_any = []
    for r in MID:
        eqs = eqs_by_r[r]
        row[f'nt_{float(r):.2f}'] = int(any(q['label'] == 'NT' for q in eqs))
        inf = [q for q in eqs if q['label'] != 'NT']
        row[f'inf_{float(r):.2f}'] = ';'.join(
            f"{q['label']}/{''.join(str(x) for x in q['recruit'])}/{'X' if q['chall_mix'] else 'P'}/"
            f"{fl(q['out']['E']):.6f}/{fl(q['a']):.5f}/{fl(q['s']):.5f}" for q in inf)
        chains_any.append(inf)
    # branch criterion: pure-entry (no challenger mixing), no sale, same recruiting set, entry strictly rising
    best = None
    for q1 in chains_any[0]:
        for q2 in chains_any[1]:
            for q3 in chains_any[2]:
                qs = (q1, q2, q3)
                if any(q['chall_mix'] for q in qs):
                    continue
                if any(fl(q['s']) != 0 for q in qs):
                    continue
                if len({q['recruit'] for q in qs}) != 1:
                    continue
                Es = [fl(q['out']['E']) for q in qs]
                if Es[0] < Es[1] < Es[2]:
                    gap = min(Es[1] - Es[0], Es[2] - Es[1])
                    if best is None or gap > best[0]:
                        best = (gap, Es, ''.join(str(x) for x in q1['recruit']),
                                [q['label'] for q in qs])
    row['branch_up'] = int(best is not None)
    row['branch_gap'] = f"{best[0]:.6f}" if best else ''
    row['branch_E'] = '|'.join(f"{v:.6f}" for v in best[1]) if best else ''
    row['branch_recruit'] = best[2] if best else ''
    row['branch_labels'] = '|'.join(best[3]) if best else ''
    # weak criterion: any informative selection with strictly rising entry
    weak = False
    for q1 in chains_any[0]:
        for q2 in chains_any[1]:
            for q3 in chains_any[2]:
                Es = [fl(q['out']['E']) for q in (q1, q2, q3)]
                if Es[0] < Es[1] < Es[2]:
                    weak = True
    row['any_up'] = int(weak)
    return row


def main():
    chunk, nchunks, outfile = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    gname = sys.argv[4] if len(sys.argv) > 4 else 'main'
    pts = grid(gname)
    mine = pts[chunk::nchunks]
    fields = None
    t0 = time.time()
    with open(outfile, 'w', newline='') as fh:
        w = None
        for i, (u, b, lam, th) in enumerate(mine):
            P = bench(lam=lam, beta=b, theta=th)
            row = dict(u=f"{float(u):.4f}", beta=f"{float(b):.4f}", lam=f"{float(lam):.6f}",
                       lam_exact=str(lam), theta=f"{float(th):.4f}")
            row.update(summarize(P))
            if w is None:
                fields = list(row)
                w = csv.DictWriter(fh, fieldnames=fields)
                w.writeheader()
            w.writerow(row)
            fh.flush()
            if i % 100 == 0:
                print(f"[{chunk}] {i}/{len(mine)} points, {time.time() - t0:.0f}s", file=sys.stderr)
    print(f"[{chunk}] done: {len(mine)} points in {time.time() - t0:.0f}s", file=sys.stderr)


if __name__ == '__main__':
    main()
