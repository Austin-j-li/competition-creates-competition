"""Development probe: print the solver's equilibrium sets at a few points (print only)."""
import sys, time
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from t1_core import bench
from t1_solver import enumerate_equilibria

def show(P, **kw):
    t = time.time()
    eqs, und, M = enumerate_equilibria(P, **kw)
    print(f"r={float(P['r']):.4f} lam={P['lam']} theta={P['theta']} k={P['k']} {kw}: {len(eqs)} eq, {len(und)} undecided, {time.time()-t:.2f}s")
    for q in eqs:
        a, b = q['a'], q['b']
        fa = float(a.mid()) if hasattr(a, 'mid') else float(a)
        fb = float(b.mid()) if hasattr(b, 'mid') else float(b)
        E = q['out']['E']; fE = float(E.mid()) if hasattr(E, 'mid') else float(E)
        es = {x: (float(v.mid()) if hasattr(v, 'mid') else float(v)) for x, v in q['e'].items()}
        print(f"   {q['label']:>26} [{q['kind']},{q['cert']}] a={fa:.6f} b={fb:.6f} e(-1,0,1)=({es[-1]:.4f},{es[0]:.4f},{es[1]:.4f}) E={fE:.6f} cm={q['chall_mix']} {q['note']} {q.get('E_range','')}")
    for u in und:
        print('   UNDECIDED', u)

# near-equal weights against Part A (lam = 1, r = 2: band; expect BNS, SNB, (s,s), (s,bR), (s,b*))
show(bench(r=2, lam=1, theta=F(333, 1000)))
show(bench(r=2, lam=1, theta=F(334, 1000)))
# theta = 1/4, lam = 1 at r = 1.55, 1.6, 1.65 and 3
for r in (F(31, 20), F(8, 5), F(33, 20), F(3), F(18, 5), F(6, 5)):
    show(bench(r=r, lam=1, theta=F(1, 4)))
