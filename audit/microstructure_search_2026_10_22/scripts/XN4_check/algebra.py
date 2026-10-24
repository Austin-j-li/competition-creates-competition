"""Polynomial certificates for the local equilibrium calculations."""
from fractions import Fraction as F
from math import gcd, lcm
from independent import auction, L, B, RHO, K, show


def trim(a):
    a=list(a)
    while len(a)>1 and a[-1]==0: a.pop()
    return a


def add(a,b):
    out=[F(0)]*max(len(a),len(b))
    for i,x in enumerate(a): out[i]+=x
    for i,x in enumerate(b): out[i]+=x
    return trim(out)


def scale(a,k): return trim([x*k for x in a])


def mul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j]+=x*y
    return trim(out)


def derivative(a): return trim([i*a[i] for i in range(1,len(a))])


def remainder(a,b):
    out=trim(a)
    while len(out)>=len(b) and any(out):
        k=out[-1]/b[-1];shift=len(out)-len(b)
        for i,x in enumerate(b): out[i+shift]-=k*x
        out=trim(out)
    return out


def value(a,x):
    answer=F(0)
    for c in reversed(a):answer=answer*x+c
    return answer


def sturm(a):
    out=[a,derivative(a)]
    while any(out[-1]):
        rem=scale(remainder(out[-2],out[-1]),F(-1))
        if not any(rem):break
        out.append(rem)
    return out


def variation(seq,x):
    signs=[1 if value(a,x)>0 else -1 for a in seq if value(a,x)!=0]
    return sum(left!=right for left,right in zip(signs,signs[1:]))


def integers(a):
    den=lcm(*(c.denominator for c in a))
    out=[int(c*den) for c in a]
    factor=0
    for c in out:factor=gcd(factor,abs(c))
    return [c//factor for c in out]


rpoly=[F(0),F(1)]
u=[F(-1),F(32),F(-4)]
v=[F(-2),F(16),F(4)]
d=[F(-4),F(80),F(-4)]
bhat=(1-L)*F(2,5);vmax=F(51,50);alpha=1-K/vmax
for e in [RHO,F(1)]:
    pol=add(scale(mul(mul(rpoly,d),add(scale(u,L),scale(v,-bhat*alpha))),4*vmax),
            scale(mul([F(1),F(-2),F(1)],mul(v,v)),bhat*e))
    sequence=sturm(pol)
    print('liquidity endpoint polynomial e=',e,'coefficients low degree first:',integers(pol))
    show('Sturm variations at r=3',variation(sequence,F(3)))
    show('Sturm variations at r=4',variation(sequence,F(4)))
    show('number of roots on (3,4)',variation(sequence,F(3))-variation(sequence,F(4)))

# A lower participation bound holds under every strategy on r in [3,4].
dmin=auction(F(3))['d'];dmax=auction(F(4))['d']
bmin=bhat*(1-(dmax/2+K)/vmax)
show('uniform liquidity mass lower bound on [3,4]',bmin)
show('uniform correct-order payoff lower bound on [3,4]',RHO*dmin*bmin/(L+2*bmin)-K)

# Eliminate the incumbent presence from its cutoff and preparation equations.
a=auction(F(3));ih=L/2;mass=ih+B
vh=a['t0']+RHO*a['wh'];vu=a['t0']+RHO*a['w']
base_value=ih*vh+B*vu
margin=ih*(a['gh']-6)+B*((a['gh']+a['gl'])/2-6)
pol=add(scale(mul([mass*(F(1,2)-K)-base_value,mass/8],[F(7),F(1)]),F(3)),
        scale([F(3,16)+K,F(-1,16)],-12*margin))
print('correct incumbent cutoff polynomial coefficients low degree first:',integers(pol))
show('incumbent polynomial at 1',value(pol,F(1)))
show('incumbent polynomial at 2',value(pol,F(2)))
