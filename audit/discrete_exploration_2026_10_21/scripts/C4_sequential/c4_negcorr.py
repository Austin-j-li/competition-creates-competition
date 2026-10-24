"""C4: negative correlation (kappa = -0.5).  Does challenger 2 prepare more often after a first entry? Print-only.

For each point it lists the equilibria found with pure round-1 strategies (round-2 mixtures allowed) and,
for every equilibrium, Pr(d2=1 | d1=1) and Pr(d2=1 | d1=0) (nan when the event d1=0 has probability 0).  When challenger 1 prepares at every round-1
signal, d1 = 0 is off path; the script then reports the counterfactual Pr(d2=1 | d1=0) from the specified
off-path continuation (beliefs after d1 = 0 equal the round-1 posterior, memo Section 2.4).
Usage: bash .../_slots/run_slot.sh .venv/bin/python -u .../c4_negcorr.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c4_core import Model, ST, SIG  # noqa: E402


def conditional_entry(m, eq):
    """Pr(d2=1 | d1=d) for d in {1, 0}, using each continuation even when it is off path."""
    out = {}
    for d in (1, 0):
        num = den = 0.0
        for s in ST:
            for S1 in SIG:
                p1 = m.prior[s] * m.psig(S1, eq['alpha'][s])
                c = eq['cont'][(S1, d)]
                w = p1  # counterfactual weight: every round-1 history, as if challenger 1 chose d there
                num += w * c['ebar'][s]
                den += w
        out[d] = num / den
    return out


def main():
    kappa = -0.5
    for r in (1.2, 3.0, 3.6):
        for cH in (3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.4, 4.5, 5.2, 5.6):
            m = Model(r=r, cH=cH, kappa=kappa)
            eqs = [e for e in m.round1(mixed=False) if 'empty_continuation' not in e]
            if not eqs:
                print(f'r={r} cH={cH}: no equilibrium with pure round-1 strategies (NC {m.nc_holds()})')
                continue
            for eq in eqs:
                cf = conditional_entry(m, eq)
                buyers = ''.join(s + ' ' for s in ST if eq['alpha'][s] > 0.5).strip()
                r2mix = [f'{kk}' for kk, c in eq['cont'].items() if c['mixing'] or c['tie_mix']]
                print(f'r={r} cH={cH} (NC {m.nc_holds()}): round-1 buyers [{buyers}] e1 g={eq["e1"]["g"]:.3f} b={eq["e1"]["b"]:.3f}; '
                      f'E1={eq["E1"]:.4f} E2={eq["E2"]:.4f} both={eq["E12"]:.4f}; on path P(d2|d1=1)={eq["p2_given_1"]:.4f} '
                      f'P(d2|d1=0)={eq["p2_given_0"]:.4f}; unweighted over round-1 signals: after d1=1 {cf[1]:.4f}, '
                      f'after d1=0 {cf[0]:.4f}; round-2 mixing at {r2mix or "-"}')


if __name__ == '__main__':
    main()
