"""More digits for the benchmark-primitive mixture path. Prints only."""
from mpmath import mp, mpf, sqrt, e as E
mp.dps = 40
exec(open('audit/theory_upgrade_2026_10_25/solvers/computations/W2_G/share.py').read().split('print("=== (1)')[0])
src = open('audit/theory_upgrade_2026_10_25/solvers/computations/W2_G/share.py').read()
start = src.index('# ---------- research branch')
end = src.index('print("\\n=== (3)')
exec(src[start:end])
r0, q, d = mpf("1.5"), mpf("0.004"), mpf("0.01")
rows = []
for c in (mpf("9.99"), mpf("10.01")):
    s = branch([(1 - q, mpf(0), r0), (q, c - d, c + d)], BM)
    rows.append(s)
    print(f"c={c}: Delta={mp.nstr(s['Delta'], 12)} tau={mp.nstr(s['tau'], 12)} lamR={mp.nstr(s['lR'], 10)} entry={mp.nstr(s['ent'], 10)} e_H={mp.nstr(s['eH'], 10)} W_H={mp.nstr(s['WH'], 6)} O_H={mp.nstr(s['OH'], 10)} S_H={mp.nstr(s['SH'], 10)} branch={s['ok']}")
a, b = rows
print('dDelta=', mp.nstr(b['Delta'] - a['Delta'], 6), ' dtau=', mp.nstr(b['tau'] - a['tau'], 6), ' dlamR=', mp.nstr(b['lR'] - a['lR'], 6),
      ' pct e_H=', mp.nstr(100 * (b['eH'] / a['eH'] - 1), 6), ' pct O_H=', mp.nstr(100 * (b['OH'] / a['OH'] - 1), 6))
