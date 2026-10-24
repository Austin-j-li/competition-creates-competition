"""Development probe: enumerate equilibria at a few points and print them."""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fractions import Fraction as F
from t6_core import bench, enumerate_equilibria, fl, FLOWS

def show(P, **kw):
    t = time.time()
    eqs, und, M = enumerate_equilibria(P, **kw)
    print(f"lam={P['lam']} beta={P['beta']} theta={P['theta']} r={P['r']} kw={kw}  ({time.time()-t:.2f}s)  undecided={len(und)}")
    for u in und:
        print('   UNDECIDED', u)
    for q in eqs:
        mu = M.posteriors(q['a'], q['s'])
        print(f"   {q['label']:24s} {q['where']:9s} A={fl(q['a']):.6f} S={fl(q['s']):.6f} E={fl(q['out']['E']):.6f} "
              f"e=({','.join(f'{fl(q['e'][x]):.3f}' for x in FLOWS)}) mu=({','.join(f'{fl(mu[x]):.4f}' for x in FLOWS)})")

for args in sys.argv[1:]:
    lam, beta, theta, r = [F(v) for v in args.split(',')]
    show(bench(lam=lam, beta=beta, theta=theta, r=r))
