"""C4: benchmark table for the memo (Section 5). Print-only.

Four economies at each (kappa, r, c_H):
  SEQ   two challengers in sequence, prices observed (all equilibria found by c4_core)
  SEQ-H two challengers, prices hidden from both challengers (entry at prior beliefs)
  ONE   one challenger, prices observed (the round-2 game after d1 = 0 at the uniform prior)
  ONE-H one challenger, price hidden (entry at the prior)
Columns: entry of each challenger, both, conditional entry of challenger 2, ownership by a high-class
challenger, target proceeds, allocation value, preparation costs, net surplus (allocation minus preparation
costs), trading costs.
Usage: bash .../_slots/run_slot.sh .venv/bin/python .../c4_summary.py [kappa ...] [--cH x]
"""
import os
import sys
from itertools import product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c4_core import Model, ST, SIG  # noqa: E402
from c4_scan import dominance_fixed  # noqa: E402


def hidden_seq(m):
    """Both challengers decide at prior beliefs.  Returns outcome dict (allocation side only)."""
    rho, cH, pr = m.rho, m.cH, m.prior
    # challenger 2 after d1 = 1 and d1 = 0, at the prior
    e2 = {1: rho + (1 - rho) * (m.D * pr['LH'] >= cH),
          0: rho + (1 - rho) * (m.gL + m.D * (pr['HH'] + pr['LH']) >= cH)}
    g1 = sum(pr[s] * (m.g[s[0]] * (1 - e2[1]) + (m.D if s == 'HL' else 0.0) * e2[1]) for s in ST)
    e1 = rho + (1 - rho) * (g1 >= cH)
    out = dict(E1=e1, E2=e1 * e2[1] + (1 - e1) * e2[0], E12=e1 * e2[1], OH=0.0, proceeds=0.0, alloc=0.0)
    for s in ST:
        for d1, p1 in ((1, e1), (0, 1 - e1)):
            for d2, p2 in ((1, e2[d1]), (0, 1 - e2[d1])):
                w = pr[s] * p1 * p2
                out['proceeds'] += w * m.value(s, d1, d2)
                out['alloc'] += w * m.allocation(s, d1, d2)
                out['OH'] += w * (1.0 if ((d1 and s[0] == 'H') or (d2 and s[1] == 'H')) else 0.0)
    out['prep'] = (e1 - rho) * cH + (out['E2'] - rho) * cH
    out['net'] = out['alloc'] - out['prep']
    out['p2_1'] = e2[1]
    out['p2_0'] = e2[0]
    out['gain1_prior'] = g1
    return out


def one(m, hidden=False):
    """Single challenger.  Returns a list of outcome dicts (one per equilibrium)."""
    rho = m.rho
    res = []
    if hidden:
        e = rho + (1 - rho) * (m.B(0.5) >= m.cH)
        eqs = [dict(ebar={'H': e, 'L': e}, trade=None)]
    else:
        eqs = []
        for eq in m.round2(dict(m.prior), 0):
            eqs.append(dict(ebar={'H': eq['ebar']['HH'], 'L': eq['ebar']['HL']}, trade=eq['prob_trade'],
                            mixing=eq['mixing'], tie=eq['tie_mix']))
    for eq in eqs:
        eb = eq['ebar']
        E = 0.5 * (eb['H'] + eb['L'])
        proceeds = sum(0.5 * (m.t0 + eb[j] * (m.t[j] - m.t0)) for j in 'HL')
        alloc = 0.5 * ((1 - eb['H']) * m.A0 + eb['H'] * m.Ah) + 0.5 * ((1 - eb['L']) * m.A0 + eb['L'] * m.Al)
        prep = (E - rho) * m.cH
        res.append(dict(E=E, OH=0.5 * eb['H'], proceeds=proceeds, alloc=alloc, prep=prep, net=alloc - prep,
                        tradecost=None if eq['trade'] is None else m.k * eq['trade'],
                        note=('mixed ' if eq.get('mixing') else '') + ('tie' if eq.get('tie') else '')))
    return res


def row(label, d):
    def f(x):
        return '   -   ' if x is None else f'{x:.4f}'
    return (f"  {label:6s} E1={f(d.get('E1'))} E2={f(d.get('E2'))} both={f(d.get('E12'))} "
            f"P(d2|d1=1)={f(d.get('p2_1'))} P(d2|d1=0)={f(d.get('p2_0'))} OH={f(d.get('OH'))} "
            f"proceeds={f(d.get('proceeds'))} alloc={f(d.get('alloc'))} prep={f(d.get('prep'))} "
            f"net={f(d.get('net'))} trade={f(d.get('tradecost'))} {d.get('note', '')}")


def main():
    args = sys.argv[1:]
    kappas = [float(x) for x in args if not x.startswith('--') and x.replace('.', '', 1).replace('-', '', 1).isdigit()]
    kappas = kappas or [0.0, 0.5]
    cHs = [5.0]
    for i, x in enumerate(args):
        if x == '--cH':
            cHs = [float(v) for v in args[i + 1].split(',')]
    for kappa in kappas:
        for cH in cHs:
            print(f'\n######## kappa = {kappa}, c_H = {cH}')
            for r in (1.2, 3.0, 3.6):
                m = Model(r=r, cH=cH, kappa=kappa)
                print(f'r = {r}: B_r(1/2) = {m.B(0.5):.6f}; NC: {m.nc_holds()}')
                eqs = [e for e in m.round1(mixed=True, fixed=dominance_fixed(m), nscan=60) if 'empty_continuation' not in e]
                for eq in eqs:
                    d = dict(E1=eq['E1'], E2=eq['E2'], E12=eq['E12'], p2_1=eq['p2_given_1'], p2_0=eq['p2_given_0'],
                             OH=eq['OH'], proceeds=eq['proceeds'], alloc=eq['alloc'], prep=eq['prepcost'],
                             net=eq['net_surplus'], tradecost=eq['tradecost'],
                             note=('pure' if eq['pure_all'] else 'mixed') + f" round-1 buyers {[s for s in ST if eq['alpha'][s] > 0]}")
                    print(row('SEQ', d))
                hs = hidden_seq(m)
                hs['note'] = f"(challenger 1 gain at prior {hs['gain1_prior']:.4f})"
                print(row('SEQ-H', hs))
                for o in one(m):
                    print(row('ONE', dict(E1=o['E'], OH=o['OH'], proceeds=o['proceeds'], alloc=o['alloc'],
                                          prep=o['prep'], net=o['net'], tradecost=o['tradecost'], note=o['note'])))
                for o in one(m, hidden=True):
                    print(row('ONE-H', dict(E1=o['E'], OH=o['OH'], proceeds=o['proceeds'], alloc=o['alloc'],
                                            prep=o['prep'], net=o['net'])))


if __name__ == '__main__':
    main()
