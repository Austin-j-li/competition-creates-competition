"""Certificates for one (theta, lam) candidate (computer-assisted: exact or rational-interval steps).

Usage (repository root):
  .venv/bin/python .../t1_certificates.py THETA LAM        e.g.  1/10 4/5

For the candidate it prints:
  1. every equilibrium at r in {6/5, 31/20, 8/5, 33/20, 3, 18/5} under four rule sets;
  2. an independent re-verification of each equilibrium (posteriors by Bayes' rule from the
     strategy, entry from B(mu) against c_H, payoffs by direct summation over the noise),
     in rational interval arithmetic;
  3. the upward-entry certificate at 31/20 < 8/5 < 33/20 (disjoint rational enclosures);
  4. Prop. A.9 at r1 = 3: feedback against hidden prices, both re-solved;
  5. the closed-form no-trade boundary and the partial-buy branch on a strength grid.
"""
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from t1_core import bench, auction, noise, Iv, fmt, r_of_spread
from t1_solver import enumerate_equilibria

RULES = [('MX_IC', dict(investor='M', challenger='X', belief='IC')),
         ('ME_IC', dict(investor='M', challenger='E', belief='IC')),
         ('ZE_IC', dict(investor='Z', challenger='E', belief='IC')),
         ('MX_PA', dict(investor='M', challenger='X', belief='passive'))]
STRENGTHS = [F(6, 5), F(31, 20), F(8, 5), F(33, 20), F(3), F(18, 5)]


def show(v, digits=10):
    if isinstance(v, Iv):
        if v.lo == v.hi:
            return fmt(v.lo, digits)
        return f"[{float(v.lo):.{digits}f}, {float(v.hi):.{digits}f}]"
    return fmt(v, digits)


def verify(P, q, belief, hidden=False):
    """Independent check of one record. Returns a text line."""
    A = auction(P)
    n = noise(P['theta'])
    pi, rho, k, lam = P['pi'], P['rho'], P['k'], P['lam']
    a, b, e = q['a'], q['b'], q['e']
    vplus, vminus = (F(1), F(0)) if belief == 'IC' else (F(1, 2), F(1, 2))
    fH, fL, mu = {}, {}, {}
    for x in range(-2, 3):
        fH[x] = (1 - Iv.of(a)) * n.get(x, 0) + Iv.of(a) * n.get(x - 1, 0)
        fL[x] = (1 - Iv.of(b)) * n.get(x, 0) + Iv.of(b) * n.get(x + 1, 0)
    used = {}
    for x in range(-2, 3):
        den = fH[x] * pi + fL[x] * (1 - pi)
        used[x] = den.hi > 0
        if den.lo > 0:
            mu[x] = fH[x] * pi / den
        elif x == 2 and fH[x].hi == 0:
            mu[x] = Iv(vplus)
            used[x] = False
        elif x == -2 and fL[x].hi == 0:
            mu[x] = Iv(vminus)
            used[x] = False
        else:
            return 'cannot classify a flow'
    # entry consistency
    ee = {}
    msgs = []
    for x in range(-2, 3):
        Bx = A['gL'] + mu[x] * (A['gH'] - A['gL']) - P['cH']
        if hidden:
            want = F(1) if A['gL'] + pi * (A['gH'] - A['gL']) >= P['cH'] else rho
            ee[x] = Iv(want)
            continue
        if x in e:
            ee[x] = Iv.of(e[x])
            if Bx.lo > 0 and not (ee[x].lo == 1):
                msgs.append(f'x={x}: should prepare')
            if Bx.hi < 0 and not (ee[x].hi == rho):
                msgs.append(f'x={x}: should not prepare')
            if Bx.lo <= 0 <= Bx.hi:
                msgs.append(f'x={x}: tie, e={show(ee[x], 6)}')
        else:
            ee[x] = Iv(1) if Bx.lo >= 0 else Iv(rho)
    D = A['D']
    # payoffs by direct summation over the noise
    gains = {}
    for j in ('H', 'L'):
        for qq in (-1, 1):
            tot = Iv(0)
            for z, pz in n.items():
                x = qq + z
                res = ee[x] * D * (1 - mu[x]) if j == 'H' else -(ee[x] * D * mu[x])
                tot = tot + res * (pz * qq)
            gains[(j, qq)] = tot - k
    gH, gL = gains[('H', 1)], gains[('L', -1)]

    def cond(rate, g):
        if isinstance(rate, Iv) and rate.lo != rate.hi:
            return 'indifferent' if (g.lo <= 0 <= g.hi) else 'FAIL(indiff)'
        rate = rate.lo if isinstance(rate, Iv) else rate
        if rate == 0:
            return 'abstains' if g.hi <= 0 else 'FAIL(abstain)'
        if rate == lam:
            return 'trades fully' if g.lo >= 0 else 'FAIL(full)'
        return 'indifferent' if (g.lo <= 0 <= g.hi) else 'FAIL(indiff)'
    ww = max(gains[('H', -1)].hi, gains[('L', 1)].hi)
    return (f"H {cond(a, gH)} (net {show(gH, 8)}), L {cond(b, gL)} (net {show(gL, 8)}); "
            f"wrong-way net payoffs <= {float(ww):.6f} < 0: {ww < 0}" + (('; ' + '; '.join(msgs)) if msgs else ''))


def rec_line(q):
    cm = f" challenger mixes at x={q['chall_mix']}" if q['chall_mix'] else ''
    es = ', '.join(show(q['e'][x], 6) for x in (-1, 0, 1))
    o = q['out']
    return (f"{q['label']:<26} a={show(q['a'], 9)} b={show(q['b'], 9)} e(-1,0,1)=({es}){cm}\n"
            f"{'':<29}E={show(o['E'], 9)} O_H={show(o['OH'], 9)} R_T={show(o['RT'], 9)} W={show(o['W'], 9)}"
            + (f"  [E range over tie choices {fmt(q['E_range'][0], 6)} .. {fmt(q['E_range'][1], 6)}]" if 'E_range' in q else ''))


def main():
    th = F(sys.argv[1]) if len(sys.argv) > 1 else F(1, 10)
    lam = F(sys.argv[2]) if len(sys.argv) > 2 else F(4, 5)
    print(f"Candidate: theta = {th} (noise weights {th}, {1 - 2 * th}, {th}), lam = {lam}; benchmark otherwise.")
    P0 = bench(theta=th, lam=lam)
    branch = {}
    allrec = {}
    for r in STRENGTHS:
        P = bench(r=r, theta=th, lam=lam)
        A = auction(P)
        print('\n' + '=' * 100)
        print(f"r = {fmt(r, 4)}: Delta = {fmt(A['D'])}, tau = {fmt(A['tau'])}, k/Delta = {fmt(P['k'] / A['D'])},"
              f" NT needs k/Delta >= rho(1-theta)/2 = {fmt(P['rho'] * (1 - th) / 2)}")
        for rule, kw in RULES:
            eqs, und, M = enumerate_equilibria(P, **kw)
            allrec[(r, rule)] = eqs
            print(f"-- rules {rule}: {len(eqs)} equilibria, {len(und)} undecided" + (f": {und}" if und else ''))
            for q in sorted(eqs, key=lambda q: float(q['out']['E'].mid() if isinstance(q['out']['E'], Iv) else q['out']['E'])):
                print('   ' + rec_line(q))
                print('      check: ' + verify(P, q, kw['belief']))
                if rule == 'MX_IC' and q['label'] in ('partial buy, no sell', 'BNS') and not q['chall_mix']:
                    branch.setdefault(r, []).append(q)

    print('\n' + '=' * 100)
    print('Upward-entry certificate on the pure-entry partial-buy / BNS branch at 31/20, 8/5, 33/20')
    picks = []
    for r in STRENGTHS[1:4]:
        cands = branch.get(r, [])
        print(f"  r={fmt(r, 4)}: " + '; '.join(f"{q['label']} E={show(q['out']['E'], 12)}" for q in cands))
        picks.append(cands)
    if all(picks):
        e1 = [Iv.of(q['out']['E']) for q in picks[0]]
        e2 = [Iv.of(q['out']['E']) for q in picks[1]]
        e3 = [Iv.of(q['out']['E']) for q in picks[2]]
        ok = [(x, y, z) for x in e1 for y in e2 for z in e3 if x.hi < y.lo and y.hi < z.lo]
        print(f"  strictly ordered enclosures exist: {bool(ok)}")
        if ok:
            x, y, z = ok[0]
            print(f"  gaps: E(8/5) - E(31/20) >= {float(y.lo - x.hi):.9f}; E(33/20) - E(8/5) >= {float(z.lo - y.hi):.9f}")

    print('\n' + '=' * 100)
    print('Prop. A.9 at r1 = 3: feedback against hidden prices (both re-solved, rules MX_IC)')
    P = bench(r=F(3), theta=th, lam=lam)
    fb = allrec[(F(3), 'MX_IC')]
    hid, undh, Mh = enumerate_equilibria(P, investor='M', challenger='X', belief='IC', hidden=True)
    print(f"  hidden-price equilibria: {len(hid)}")
    for q in hid:
        print('   ' + rec_line(q))
        print('      check: ' + verify(P, q, 'IC', hidden=True))
    for q1 in fb:
        for q0 in hid:
            dR = Iv.of(q1['out']['RT']) - Iv.of(q0['out']['RT'])
            dW = Iv.of(q1['out']['W']) - Iv.of(q0['out']['W'])
            print(f"  {q1['label']} vs hidden {q0['label']}: dR_T = {show(dR, 9)} (positive: {dR.lo > 0}),"
                  f" dW = {show(dW, 9)} (positive: {dW.lo > 0})")

    print('\n' + '=' * 100)
    print('Closed-form no-trade boundary (IC and passive) and NT existence')
    A = auction(P0)
    rIC = r_of_spread(2 * P0['k'] / (P0['rho'] * (1 - th)))
    rPA = r_of_spread(2 * P0['k'] / P0['rho'])
    print(f"  NT exists (IC completion) iff k >= rho Delta (1-theta)/2, i.e. r <= {float(rIC.hi):.9f}")
    print(f"  NT exists (passive beliefs) iff k >= rho Delta/2, i.e. r <= {float(rPA.hi):.9f}")


if __name__ == '__main__':
    main()
