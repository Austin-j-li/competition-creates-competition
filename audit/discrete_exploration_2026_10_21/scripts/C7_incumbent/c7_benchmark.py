"""C7 benchmark: print continuation, trading, and welfare results at the benchmark (print only)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpmath import mp, mpf, nstr, findroot
from c7_model import Par, auction, D, B_prior, continuation, evaluate, news, purchase_payoff, outcome

mp.dps = 50
par = Par()
a = par.a
m1, M1 = a / (1 + a), 1 / (1 + a)
f = lambda x, n=12: nstr(x, n)

print('=== Constants (c_H = 5, b = 2, k = 0.02, rho = 0.25, pi = 1/2) ===')
print('a =', f(a), ' m1 =', f(m1), ' M1 =', f(M1), ' 2 m1 M1 =', f(2 * m1 * M1))
rD = par.h - par.cH / M1
rN = 2 * (par.h - par.cH / M1) - par.ell
rC = findroot(lambda r: B_prior(par, r, M1) - par.cH, 3.9)
print('r_D (deterrence feasible above) = h - c_H/M1 =', f(rD))
print('r_N (threshold <= ell above)    = 2(h - c_H/M1) - ell =', f(rN))
print('r_C (B_r(M1) = c_H)             =', f(rC))

print('\n=== Check D(mu;[0,r]) = B_r(mu) ===')
for r in [mpf('1.2'), mpf(3)]:
    for mu in [m1, mpf('0.5'), M1]:
        print(f' r={f(r,4)} mu={f(mu,6)}  D0={f(D(par, r, mu, 0))}  B={f(B_prior(par, r, mu))}')

print('\n=== Continuation at r_1 = 3, good news mu = M1 ===')
r1 = mpf(3)
A1 = auction(par, r1)
print('Delta_T(r1) =', f(A1['DT']), ' rho*Delta_T =', f(par.rho * A1['DT']))
for jump in (False, True):
    ev = evaluate(par, r1, M1, jump)
    print(f" jump={jump}: case={ev['case']}{ev['sub']} Rhat={f(ev['Rhat'])} J={f(ev['J']) if ev['J'] is not None else None}"
          f" entry={f(ev['entry'])} S={f(ev['S'])} P={f(ev['P'])}")
ev = evaluate(par, r1, M1, True)
print(' D(M1;[Rhat,r]) at threshold =', f(D(par, r1, M1, ev['Rhat'])), '(should equal c_H = 5)')
print(' D(M1;[p,r]) =', f(D(par, r1, M1, par.p)), ' D(M1;[ell,r]) =', f(D(par, r1, M1, par.ell)),
      ' M1(h-r) =', f(M1 * (par.h - r1)), ' M1(h-(ell+r)/2) =', f(M1 * (par.h - (par.ell + r1) / 2)))
print(' B(M1;[0,Rhat)) after silence =', f(D(par, r1, M1, 0, ev['Rhat'])))
evb = evaluate(par, r1, m1, True)
print(f" bad news mu=m1: case={evb['case']} entry={f(evb['entry'])} S={f(evb['S'])} P={f(evb['P'])}")
print(' P_G - P_B (jump) =', f(ev['P'] - evb['P']))

print('\n=== Trading stage at r_1: purchase payoff Pi(beta) (net of k) ===')
for beta in [mpf(0), mpf('0.25'), mpf('0.5'), mpf('0.75'), mpf(1)]:
    print(f' beta={f(beta,3)}  base={f(purchase_payoff(par, r1, beta, False))}  jump={f(purchase_payoff(par, r1, beta, True))}')
print(' closed forms: rho*DT/2 - k =', f(par.rho * A1['DT'] / 2 - par.k),
      '; 2 rho m1 M1 DT - k =', f(2 * par.rho * m1 * M1 * A1['DT'] - par.k),
      '; (1+rho) m1 M1 DT - k =', f((1 + par.rho) * m1 * M1 * A1['DT'] - par.k))
print(' global floor m1*rho*DT(r1) =', f(m1 * par.rho * A1['DT']), ' > k =', f(par.k))

print('\n=== Ex ante outcomes ===')
rows = []
for label, r, beta, jump in [('r0=1.2 no trade, base', mpf('1.2'), mpf(0), False),
                             ('r0=1.2 no trade, jump', mpf('1.2'), mpf(0), True),
                             ('r1=3 full buying, base', r1, mpf(1), False),
                             ('r1=3 full buying, jump', r1, mpf(1), True),
                             ('r2=3.6 full buying, base', mpf('3.6'), mpf(1), False),
                             ('r2=3.6 full buying, jump', mpf('3.6'), mpf(1), True),
                             ('r=4.2 full buying, base', mpf('4.2'), mpf(1), False),
                             ('r=4.2 full buying, jump', mpf('4.2'), mpf(1), True)]:
    o = outcome(par, r, beta, jump)
    rows.append((label, o))
    print(f" {label:28s} caseG={o['caseG']:14s} RhatG={f(o['RhatG'],8)} JG={f(o['JG'],8) if o['JG'] is not None else '-':>10s}"
          f" entry={f(o['entry'],9)} O_H={f(o['O_H'],9)} preempt={f(o['preempt'],9)}")
    print(f" {'':28s} proceeds={f(o['proc'],9)} incumbent={f(o['inc'],9)} challenger={f(o['chal'],9)}"
          f" surplus={f(o['surplus'],9)} sum-check={f(o['proc'] + o['inc'] + o['chal'] - o['surplus'],3)}")

print('\n=== Differences at r_1 (jump minus base, same full-buying information) ===')
ob, oj = rows[2][1], rows[3][1]
for key in ('entry', 'O_H', 'proc', 'inc', 'chal', 'surplus'):
    print(f' {key:9s}: {f(oj[key] - ob[key])}')

print('\n=== Price-hidden economy at r_1 (bidders see no price; mu = 1/2 for bidders) ===')
eh = evaluate(par, r1, mpf('0.5'), True)
print(f" case={eh['case']} entry={f(eh['entry'])} proceeds={f(eh['proc'])} surplus={f(eh['surplus'])}"
      f" incumbent={f(eh['inc'])} challenger={f(eh['chal'])}")
print(' access minus hidden, base: proceeds', f(ob['proc'] - eh['proc']), ' surplus', f(ob['surplus'] - eh['surplus']))
print(' access minus hidden, jump: proceeds', f(oj['proc'] - eh['proc']), ' surplus', f(oj['surplus'] - eh['surplus']))

print('\n=== Incumbent gain at good news, closed form check (R_hat <= ell) ===')
Rh, J = ev['Rhat'], ev['J']
mu = M1
rho, l, r = par.rho, par.ell, r1
gain = ((1 - rho) * (l - J)**2 / 2 + (1 - rho) * (mu * (r**2 - l**2) / 2 + ((1 - mu) * l - J) * (r - l))) / r
print(' incumbent gain at good news (closed form) =', f(gain))
print(' incumbent gain at good news (model)       =', f(ev['inc'] - evaluate(par, r1, M1, False)['inc']))
print(' target loss at good news (model)          =', f(evaluate(par, r1, M1, False)['proc'] - ev['proc']))
