from fractions import Fraction
import mpmath as mp

mp.mp.dps = 80
q = lambda x: mp.mpf(str(Fraction(x).numerator)) / Fraction(x).denominator
beta, rho, k, a = map(q, ('0.294655', '1/4', '1/50', '1/40'))
p, h, ell, c = map(q, ('1/2', '10', '1', '6'))

# Integrals of the cash-auction payoffs, split at the reserve and value.
def auction(v, r):
    cut = min(v, r)
    gross = (p * (v-p) + v*(cut-p) - (cut**2-p**2)/2) / r
    proceeds = (p**2 + (cut**2-p**2)/2 + v*(r-cut)) / r
    return gross, proceeds

def objects(r):
    gh, th = auction(h, r)
    gl, tl = auction(ell, r)
    return th-tl, (c-gl)/(gh-gl)

def le(r):
    _, tau = objects(r)
    return beta*(2*tau-1)/(beta+(1-2*beta)*(1-tau))

def ml(lam):
    return (1-lam)*beta/(2*beta+lam*(1-2*beta))

def out(name, val):
    print(name + ': ' + mp.nstr(val, 55))

cap = q('33/100')
d155, tau155 = objects(q('31/20'))
d165, _ = objects(q('33/20'))
alo = (d165*ml(cap)-k)/(2*cap)
aup = (d155*(1-tau155)-k)/(2*le(q('31/20')))
out('cap - lambda_E(3)', cap-le(q('3')))
out('lambda_E(18/5) - cap', le(q('18/5'))-cap)
out('a - a_lo(cap)', a-alo)
out('a_up - a', aup-a)
out('entry at cap 0.33', rho+(1-rho)*(beta+(q('1/2')-beta)*cap))
for r in (q('3'), q('18/5')):
    d, tau = objects(r)
    out('strong-research margin at r='+str(r), rho*d*ml(cap)-k-a*cap)

u = mp.e-1
lam = u*beta/(1+u*beta)
b = (1-lam)*beta
M = mp.e/(1+mp.e)
out('benchmark cap', lam)
out('Cov(X,1_A) at r=3', (1-rho)*(b+lam/2))
out('benchmark entry at r=3', rho+(1-rho)*(b+lam/2))
# B_r(M)=Mh-M*r/2+(ell**2-p**2-M*ell**2)/(2*r).
rc = (M*h-c + mp.sqrt((M*h-c)**2+M*(ell**2-p**2-M*ell**2)))/M
out('entry ceiling r_C', rc)
pi = q('3/10')
Mpi = pi*mp.e/(1-pi+pi*mp.e)
gh, _ = auction(h, q('3'))
gl, _ = auction(ell, q('3'))
out('M(0.3)', Mpi)
out('B_3(M(0.3))-6', Mpi*gh+(1-Mpi)*gl-c)
out('Z purchase payoff at r=1.55', rho*d155/2-k)

# Moderate-gap row, point values 2 and 1.
r0,r1 = q('21/20'),q('3/2')
cost, kc = q('89/100'), q('1/500')
gh0,th0=auction(q('2'),r0)
gl0,tl0=auction(q('1'),r0)
gh1,th1=auction(q('2'),r1)
gl1,tl1=auction(q('1'),r1)
out('moderate H1 prior margin', cost-(gh0+gl0)/2)
out('moderate H1 top margin', M*gh1+(1-M)*gl1-cost)
out('moderate H2 weak margin', kc-(th0-tl0))
out('moderate H2 strong margin', rho*(1-M)*(th1-tl1)-kc)
out('moderate entry at r1', rho+(1-rho)*(b+lam/2))
out('moderate ownership at r1', (rho+(1-rho)*(b+lam))/2)
