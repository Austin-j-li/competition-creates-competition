"""Scans of the exact solver over (theta, lam) and strength r (computer-assisted at each grid point).

Usage (from the repository root; each call is one process, run it through the slot wrapper):
  .venv/bin/python .../t1_scan.py bench CHUNK NCHUNKS      -> scan_bench_CHUNK.csv
  .venv/bin/python .../t1_scan.py interval CHUNK NCHUNKS   -> scan_interval_CHUNK.csv

bench:    theta in {1/50, ..., 24/50} (theta = 1/3 is Part A), lam in {1/20, ..., 1},
          r in {6/5, 31/20, 8/5, 33/20, 3, 18/5}, four rule sets.
interval: theta in {3/50, ..., 15/50}, lam in {1/2, 3/5, ..., 1}, r = 1.20, 1.21, ..., 2.60,
          rule set (M, X, IC).
Each CSV row: theta, lam, r, rules, number of equilibria, number undecided, and one field with
every equilibrium as label|kind|challenger-mixing flows|E|O_H|a|b (decimals, 9 digits).
"""
import csv
import sys
import time
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from t1_core import bench
from t1_solver import enumerate_equilibria

RULES = {'MX_IC': dict(investor='M', challenger='X', belief='IC'),
         'ME_IC': dict(investor='M', challenger='E', belief='IC'),
         'ZE_IC': dict(investor='Z', challenger='E', belief='IC'),
         'MX_PA': dict(investor='M', challenger='X', belief='passive')}


def fl(v):
    return float(v.mid()) if hasattr(v, 'mid') else float(v)


def encode(eqs):
    parts = []
    for q in eqs:
        cm = ''.join(str(x) for x in q['chall_mix'])
        parts.append(f"{q['label']}|{q['kind']}|{cm}|{fl(q['out']['E']):.9f}|{fl(q['out']['OH']):.9f}|"
                     f"{fl(q['a']):.9f}|{fl(q['b']):.9f}")
    return ';'.join(parts)


def main():
    mode, chunk, nchunks = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    if mode == 'bench':
        thetas = [F(i, 50) for i in range(1, 25)]
        lams = [F(i, 20) for i in range(1, 21)]
        rs = [F(6, 5), F(31, 20), F(8, 5), F(33, 20), F(3), F(18, 5)]
        rules = list(RULES)
    else:
        thetas = [F(i, 50) for i in range(3, 16)]
        lams = [F(i, 10) for i in range(5, 11)]
        rs = [F(120 + i, 100) for i in range(0, 141)]
        rules = ['MX_IC']
    jobs = [(th, lam) for th in thetas for lam in lams]
    jobs = jobs[chunk::nchunks]
    out = HERE / f"scan_{mode}_{chunk}.csv"
    t0 = time.time()
    with open(out, 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['theta', 'lam', 'r', 'rules', 'n_eq', 'n_undecided', 'equilibria', 'undecided'])
        for th, lam in jobs:
            for r in rs:
                for rule in rules:
                    P = bench(r=r, lam=lam, theta=th)
                    eqs, und, M = enumerate_equilibria(P, **RULES[rule])
                    w.writerow([str(th), str(lam), str(r), rule, len(eqs), len(und), encode(eqs),
                                ' / '.join(und)[:300]])
            fh.flush()
    print(f"{mode} chunk {chunk}/{nchunks}: {len(jobs)} (theta, lam) pairs, {time.time() - t0:.1f} s -> {out.name}")


if __name__ == '__main__':
    main()
