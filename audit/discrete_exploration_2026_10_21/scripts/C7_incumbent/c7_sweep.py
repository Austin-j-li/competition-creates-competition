"""C7 sweep over incumbent strength r and over c_H (numerical diagnostic, print only).

For each r: all trading equilibria on a beta grid (pure ends plus bracketed interior roots),
for the base model and for the jump-bid model, with entry, ownership, preemption,
proceeds, and surplus. Also checks that the price separates good and bad news, and that the
good-news spread equals rho * Delta_T when the threshold is at or below ell.
Writes c7_sweep.csv (one row per r and model and equilibrium) and prints a summary.
"""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpmath import mp, mpf, nstr
import c7_model as M

mp.dps = 30
here = os.path.dirname(os.path.abspath(__file__))


def equilibria(par, r, jump, nb=60):
    betas = [mpf(i) / nb for i in range(nb + 1)]
    vals = [M.purchase_payoff(par, r, b, jump) for b in betas]
    eqs = []
    if vals[0] <= 0:
        eqs.append((mpf(0), 'pure'))
    if vals[-1] >= 0:
        eqs.append((mpf(1), 'pure'))
    for i in range(nb):
        if vals[i] > 0 > vals[i + 1] or vals[i] < 0 < vals[i + 1]:
            lo, hi, flo = betas[i], betas[i + 1], vals[i]
            for _ in range(60):
                mid = (lo + hi) / 2
                fm = M.purchase_payoff(par, r, mid, jump)
                if (fm > 0) == (flo > 0):
                    lo, flo = mid, fm
                else:
                    hi = mid
            gap = abs(M.purchase_payoff(par, r, lo, jump) - M.purchase_payoff(par, r, hi, jump))
            eqs.append(((lo + hi) / 2, 'interior' if gap < mpf('1e-12') else 'jump-through-zero'))
    return eqs, min(vals)


def main():
    par = M.Par()
    a = par.a
    m1, M1 = a / (1 + a), 1 / (1 + a)
    rows = []
    rs = [mpf('1.05') + mpf(i) / 50 for i in range(0, 179)]   # 1.05 .. 4.61
    for r in rs:
        A = M.auction(par, r)
        for jump in (False, True):
            eqs, minPi = equilibria(par, r, jump)
            for beta, kind in eqs:
                o = M.outcome(par, r, beta, jump)
                sep = True
                if beta > 0:
                    sep = o['PG'] > o['PB']
                rows.append(dict(r=nstr(r, 6), model='jump' if jump else 'base', beta=nstr(beta, 10), kind=kind,
                                 caseG=o['caseG'], RhatG=nstr(o['RhatG'], 10), JG=nstr(o['JG'], 10) if o['JG'] is not None else '',
                                 entry=nstr(o['entry'], 10), O_H=nstr(o['O_H'], 10), preempt=nstr(o['preempt'], 10),
                                 entry_goodnews=nstr(o['entry_goodnews'], 10),
                                 proceeds=nstr(o['proc'], 10), incumbent=nstr(o['inc'], 10), challenger=nstr(o['chal'], 10),
                                 surplus=nstr(o['surplus'], 10), SG_over_rhoDT=nstr(o['SG'] / (par.rho * A['DT']), 10),
                                 price_separates=sep, minPi=nstr(minPi, 8)))
    with open(os.path.join(here, 'c7_sweep.csv'), 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print('r, model: equilibria (beta kind entry O_H preempt caseG Rhat S_G/(rho DT) price_separates)')
    for row in rows:
        r = float(row['r'])
        if round(r * 100) % 20 == 5 or row['kind'] != 'pure' or 1.40 <= r <= 1.90 or 3.9 <= r <= 4.1:
            print(f"{row['r']:>6s} {row['model']:4s} beta={row['beta'][:8]:8s} {row['kind']:17s} entry={row['entry'][:9]:9s} "
                  f"O_H={row['O_H'][:9]:9s} preempt={row['preempt'][:8]:8s} {row['caseG']:15s} Rhat={row['RhatG'][:8]:8s} "
                  f"SG/rhoDT={row['SG_over_rhoDT'][:8]:8s} sep={row['price_separates']}")

    # neutralization check on a posterior grid at r >= r_N
    print('\nSpread S(mu)/(rho DT) on mu in [m1, M1], jump model:')
    for r in [mpf('2.5'), mpf('2.9'), mpf('2.95'), mpf(3), mpf('3.5'), mpf('3.9')]:
        A = M.auction(par, r)
        ratios = []
        for i in range(41):
            mu = m1 + (M1 - m1) * i / 40
            ratios.append(M.evaluate(par, r, mu, True)['S'] / (par.rho * A['DT']))
        print(f'  r={nstr(r,4)}: min={nstr(min(ratios),12)} max={nstr(max(ratios),12)}')

    print('\nPrice monotone in mu on [m1, M1] (jump model)?')
    for r in [mpf(2), mpf('2.5'), mpf(3), mpf('3.5'), mpf('3.9')]:
        Ps = [M.evaluate(par, r, m1 + (M1 - m1) * i / 80, True)['P'] for i in range(81)]
        print(f'  r={nstr(r,4)}: increasing={all(Ps[i+1] > Ps[i] for i in range(80))}')

    print('\nc_H sensitivity at r_1 = 3, full buying (jump model vs base):')
    for cH in ['4.85', '4.9', '4.95', '4.98', '5', '5.05', '5.1', '5.2', '5.31']:
        p2 = M.Par(cH=cH)
        ob = M.outcome(p2, mpf(3), mpf(1), False)
        oj = M.outcome(p2, mpf(3), mpf(1), True)
        Pij = M.purchase_payoff(p2, mpf(3), mpf(1), True)
        print(f"  c_H={cH:5s} caseG={oj['caseG']:15s} Rhat={nstr(oj['RhatG'],8):10s} J={nstr(oj['JG'],8) if oj['JG'] is not None else '-':10s} "
              f"entry base={nstr(ob['entry'],8)} jump={nstr(oj['entry'],8)}  dSurplus={nstr(oj['surplus']-ob['surplus'],6)} "
              f"dProceeds={nstr(oj['proc']-ob['proc'],6)} Pi_jump(1)={nstr(Pij,6)}")


if __name__ == '__main__':
    main()
