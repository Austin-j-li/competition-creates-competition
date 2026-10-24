"""Development probe 2: compact equilibrium lists on a few (lam, theta) points (print only)."""
import sys
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from t1_core import bench
from t1_solver import enumerate_equilibria

def f(v):
    return float(v.mid()) if hasattr(v, 'mid') else float(v)

def line(P):
    eqs, und, M = enumerate_equilibria(P)
    parts = []
    for q in sorted(eqs, key=lambda q: f(q['out']['E'])):
        tag = {'NT': 'NT', 'T': 'T', 'BNS': 'BNS', 'SNB': 'SNB'}.get(q['label'], q['label'].replace('partial ', 'p').replace('full ', 'f').replace('no ', 'n').replace(' buy', 'B').replace(' sell', 'S').replace(', ', '/'))
        cm = ('*' + ''.join(str(x) for x in q['chall_mix'])) if q['chall_mix'] else ''
        parts.append(f"{tag}{cm}:{f(q['out']['E']):.3f}")
    return ' '.join(parts) + (f" UND={len(und)}" if und else '')

for th in (F(1, 10), F(3, 20), F(1, 5), F(3, 10), F(2, 5), F(9, 20)):
    for lam in (F(3, 5), F(4, 5), F(1)):
        print(f"theta={float(th):.3f} lam={float(lam):.2f}")
        for r in (F(31, 20), F(8, 5), F(33, 20), F(3), F(18, 5)):
            print(f"   r={float(r):.2f}: " + line(bench(r=r, lam=lam, theta=th)))
