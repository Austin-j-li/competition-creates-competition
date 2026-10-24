"""C4: recompute solved equilibria from integer flows, without the binary reduction. Print-only.

The reduced solver (c4_core.py) uses only the class S = 1{X >= 1} of each flow.  This script takes the
investors' strategies from a reduced solution, then recomputes everything over integer flows
x in [-N, N+1] with the exact noise probabilities n(z) = (1-a)/(1+a) a^|z|:
  flow posteriors, challenger gains and entry decisions (from flow posteriors, not from the reduced
  entry pattern), terminal values, prices, investor margins, and the aggregate outcomes.
It prints the largest differences from the reduced solution.  Truncation error is of order a^N.
Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C4_sequential/c4_flowcheck.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c4_core import Model, ST, SIG  # noqa: E402

N = 80


def noise(m):
    a = m.a
    return {z: (1 - a) / (1 + a) * a ** abs(z) for z in range(-N - 2, N + 3)}


def flow_probs(n, beta):
    return {x: beta * n.get(x - 1, 0.0) + (1 - beta) * n.get(x, 0.0) for x in range(-N, N + 2)}


def check(m, eq):
    n = noise(m)
    rho, cH = m.rho, m.cH
    xs = list(range(-N, N + 2))
    cls = lambda x: 'g' if x >= 1 else 'b'
    alpha = eq['alpha']
    P1x = {s: flow_probs(n, alpha[s]) for s in ST}
    out = dict(E1=0.0, E2=0.0, E12=0.0, proceeds=0.0)
    Pi1 = {s: -m.k for s in ST}
    maxdiff_post1 = maxdiff_gain1 = maxdiff_gain2 = maxdiff_Pi2 = 0.0
    entry_mismatch = 0
    price_gap_min = float('inf')
    Y = {}
    P1 = {}
    mu1x = {}
    for x1 in xs:
        w = {s: m.prior[s] * P1x[s][x1] for s in ST}
        z = sum(w.values())
        mu1 = {s: w[s] / z for s in ST}
        mu1x[x1] = mu1
        S1 = cls(x1)
        maxdiff_post1 = max(maxdiff_post1, max(abs(mu1[s] - eq['mu1'][S1][s]) for s in ST))
        Wd = {}
        G1 = {}
        e2store = {}
        for d1 in (0, 1):
            c = eq['cont'][(S1, d1)]
            beta = c['beta']
            P2x = {s: flow_probs(n, beta[s]) for s in ST}
            W = {s: 0.0 for s in ST}
            g1 = {s: 0.0 for s in ST}
            Pi2 = {s: -m.k for s in ST}
            V2 = {}
            P2 = {}
            e2x = {}
            for x2 in xs:
                w2 = {s: mu1[s] * P2x[s][x2] for s in ST}
                z2 = sum(w2.values())
                mu2 = {s: w2[s] / z2 for s in ST}
                gam = m.gain2(d1, mu2)
                S2 = cls(x2)
                if c['tie_mix'] == S2:
                    e2 = c['e'][S2]
                else:
                    e2 = 1.0 if gam >= cH else rho
                    if abs(e2 - c['e'][S2]) > 1e-12:
                        entry_mismatch += 1
                maxdiff_gain2 = max(maxdiff_gain2, abs(gam - c['Gam'][S2]))
                V = {s: m.base[d1][s] + e2 * m.inc[d1][s] for s in ST}
                P = sum(mu2[s] * V[s] for s in ST)
                V2[x2], P2[x2], e2x[x2] = V, P, e2
                for s in ST:
                    W[s] += P2x[s][x2] * V[s]
                    g1[s] += P2x[s][x2] * (m.g[s[0]] * (1 - e2) + (m.D if s == 'HL' else 0.0) * e2)
                    Pi2[s] += n.get(x2 - 1, 0.0) * (V[s] - P)
            maxdiff_Pi2 = max(maxdiff_Pi2, max(abs(Pi2[s] - c['Pi'][s]) for s in ST))
            # price separation between the two classes of x2
            pg = [P2[x] for x in xs if x >= 1]
            pb = [P2[x] for x in xs if x <= 0]
            if max(abs(pg[0] - c['P']['g']), abs(pb[0] - c['P']['b'])) > 1e-9:
                entry_mismatch += 1000
            if abs(c['mu']['g']['HH'] - c['mu']['b']['HH']) > 1e-9 or abs(c['mu']['g']['LH'] - c['mu']['b']['LH']) > 1e-9:
                price_gap_min = min(price_gap_min, abs(c['P']['g'] - c['P']['b']))
            Wd[d1] = W
            G1[d1] = g1
            e2store[d1] = (P2x, e2x)
        gam1 = sum(mu1[s] * G1[1][s] for s in ST)
        maxdiff_gain1 = max(maxdiff_gain1, abs(gam1 - eq['Gam1'][S1]))
        if eq['tie_mix'] == S1:
            e1 = eq['e1'][S1]
        else:
            e1 = 1.0 if gam1 >= cH else rho
            if abs(e1 - eq['e1'][S1]) > 1e-12:
                entry_mismatch += 1
        Y[x1] = {s: e1 * Wd[1][s] + (1 - e1) * Wd[0][s] for s in ST}
        P1[x1] = sum(mu1[s] * Y[x1][s] for s in ST)
        for s in ST:
            p1 = m.prior[s] * P1x[s][x1]
            for d1, pd in ((1, e1), (0, 1 - e1)):
                P2x, e2x = e2store[d1]
                for x2 in xs:
                    pp = p1 * pd * P2x[s][x2]
                    e2 = e2x[x2]
                    out['E1'] += pp * d1
                    out['E2'] += pp * e2
                    out['E12'] += pp * d1 * e2
                    out['proceeds'] += pp * (e2 * m.value(s, d1, 1) + (1 - e2) * m.value(s, d1, 0))
    for s in ST:
        for x1 in xs:
            Pi1[s] += n.get(x1 - 1, 0.0) * (Y[x1][s] - P1[x1])
    d_Pi1 = max(abs(Pi1[s] - eq['Pi1'][s]) for s in ST)
    gap1 = abs(P1[1] - P1[0])
    return dict(out=out, d_post1=maxdiff_post1, d_gain1=maxdiff_gain1, d_gain2=maxdiff_gain2,
                d_Pi2=maxdiff_Pi2, d_Pi1=d_Pi1, entry_mismatch=entry_mismatch,
                price_gap_round1=gap1, price_gap_round2_min=price_gap_min)


def main():
    cases = [dict(r=1.2, cH=5.0, kappa=0.0), dict(r=3.0, cH=5.0, kappa=0.0), dict(r=3.6, cH=5.0, kappa=0.0),
             dict(r=3.0, cH=4.0, kappa=0.0), dict(r=3.0, cH=5.0, kappa=0.5), dict(r=3.0, cH=5.0, kappa=-0.5),
             dict(r=1.2, cH=4.4, kappa=0.0)]
    for cs in cases:
        m = Model(**cs)
        eqs = [e for e in m.round1(mixed=False) if 'empty_continuation' not in e]
        print(f"\ncase {cs}: {len(eqs)} pure round-1 equilibria from the reduced solver")
        for eq in eqs:
            res = check(m, eq)
            o = res['out']
            print(f"  alpha {[eq['alpha'][s] for s in ST]} e1 g={eq['e1']['g']:.2f} b={eq['e1']['b']:.2f}")
            print(f"    reduced: E1={eq['E1']:.12f} E2={eq['E2']:.12f} both={eq['E12']:.12f} proceeds={eq['proceeds']:.12f}")
            print(f"    flows  : E1={o['E1']:.12f} E2={o['E2']:.12f} both={o['E12']:.12f} proceeds={o['proceeds']:.12f}")
            print(f"    max |diff|: round-1 posterior {res['d_post1']:.1e}, challenger-1 gain {res['d_gain1']:.1e}, "
                  f"challenger-2 gain {res['d_gain2']:.1e}, investor-2 margins {res['d_Pi2']:.1e}, investor-1 margins {res['d_Pi1']:.1e}; "
                  f"entry mismatches {res['entry_mismatch']}")
            print(f"    price gap between classes: round 1 {res['price_gap_round1']:.6f}; "
                  f"round 2 (informative histories) min {res['price_gap_round2_min']:.6f}")


if __name__ == '__main__':
    main()
