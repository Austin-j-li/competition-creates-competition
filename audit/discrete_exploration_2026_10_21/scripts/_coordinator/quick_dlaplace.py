"""Coordinator's quick arithmetic look at the discrete-Laplace candidate (print only)."""
from mpmath import mp, mpf, e
mp.dps = 30
h, l, p, rho, k, b = mpf(10), mpf(1), mpf('0.5'), mpf('0.25'), mpf('0.02'), mpf(2)
def objs(r):
    t0 = p*(1-p/r); gH = h - r/2 - p**2/(2*r); gL = (l**2-p**2)/(2*r); D = (r-l)**2/(2*r)
    return t0, gH, gL, D
a = e**(-1/b)
m1 = 1/(1+e**(1/b)); M1 = 1-m1
print('a', a, 'm1', m1, 'M1', M1)
for r in [mpf('1.2'), mpf(3), mpf('3.6'), mpf('4'), mpf('4.2')]:
    t0, gH, gL, D = objs(r)
    B = lambda mu: gL + mu*(gH-gL)
    print(f'r={r}: D_T={D}, gH={gH}, gL={gL}, B(1/2)={B(mpf(1)/2)}, B(m1)={B(m1)}, B(M1)={B(M1)}, rho*m1*D={rho*m1*D}')
# full buying: P(good|H)=P(Z>=0)=1/(1+a); P(good|L)=P(Z>=1)=a/(1+a)
pg = (1/(1+a) + a/(1+a))/2
print('P(good news)', pg)
cH = 5
for r in [mpf(3)]:
    t0, gH, gL, D = objs(r)
    print('entry if only good news recruits H:', rho + (1-rho)*pg)
    print('O_H = 0.5*(rho + (1-rho)/(1+a)) =', (rho + (1-rho)/(1+a))/2)
print('O_H at rho only:', rho/2)
# full-buy H payoff at r1, entry after good news only
r = mpf(3); t0, gH, gL, D = objs(r)
# V_H - P at flow with posterior mu and entry e: e*D*(1-mu)
# gain of buying: E over Z of [V_H - P(Z+1)] = sum P(z) e(mu(z+1)) D (1-mu(z+1))
eg = rho + (1-rho)  # entry after good news (B(M1) >= cH)
eb = rho
gross = (1/(1+a))*eg*D*(1-M1) + (a/(1+a))*eb*D*(1-m1)
print('H gross buy profit at r1 (entry after good news):', gross, 'net', gross - k)
gross_noentry = rho*D*((1/(1+a))*(1-M1) + (a/(1+a))*(1-m1))
print('H gross if entry stays rho:', gross_noentry, 'net', gross_noentry-k)
