"""C7: trading equilibria at weak incumbents, r in [1.40, 1.86] (numerical diagnostic, print only).

Lists every equilibrium found on a beta grid with bisection, for the base and the jump model.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpmath import mp, mpf, nstr
import c7_model as M
from c7_sweep import equilibria

mp.dps = 30
par = M.Par()
for i in range(0, 93):
    r = mpf('1.40') + mpf(i) / 200
    for jump in (False, True):
        eqs, _ = equilibria(par, r, jump, nb=120)
        parts = []
        for beta, kind in eqs:
            o = M.outcome(par, r, beta, jump)
            parts.append(f"b={nstr(beta,6)} {kind[:5]} E={nstr(o['entry'],6)} pre={nstr(o['preempt'],4)} {o['caseG']}")
        print(f"r={nstr(r,5):6s} {'jump' if jump else 'base'}: " + ' | '.join(parts))
r = mpf('1.6')
print('\nDetail at r = 1.6, jump model, interior equilibrium:')
eqs, _ = equilibria(par, r, True, nb=120)
for beta, kind in eqs:
    o = M.outcome(par, r, beta, True)
    n = M.news(par, beta)
    print(f" beta={nstr(beta,12)} kind={kind} muG={nstr(n['muG'],10)} muB={nstr(n['muB'],10)} caseG={o['caseG']}"
          f" Rhat={nstr(o['RhatG'],10)} J={nstr(o['JG'],10) if o['JG'] is not None else '-'} entry={nstr(o['entry'],10)}"
          f" O_H={nstr(o['O_H'],10)} PG={nstr(o['PG'],10)} PB={nstr(o['PB'],10)} Pi={nstr(M.purchase_payoff(par, r, beta, True),6)}"
          f" surplus={nstr(o['surplus'],10)} proceeds={nstr(o['proc'],10)}")
print(' deterrence feasible for mu < c_H/(h-r) =', nstr(par.cH / (par.h - r), 10), '; tau(r) where B_r(tau)=c_H:',
      nstr((par.cH - M.auction(par, r)['gL']) / (M.auction(par, r)['gH'] - M.auction(par, r)['gL']), 10))
