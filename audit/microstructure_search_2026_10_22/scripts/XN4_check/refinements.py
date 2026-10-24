"""Further exact calculations for the review, from the independent equations."""
from fractions import Fraction as F
from independent import auction, bisect_fraction, integral_linear, show, L, B, C, RHO, K, P


def challenger_profile(chi, s, t):
    a=auction(F(3))
    wait=1-L-chi-2*B
    outside={1:(L*s/2+B/2,B/2), -1:(B/2,L*t/2+B/2),
             0:(L*(1-s)/2+wait/2,L*(1-t)/2+wait/2)}
    entry={};price={};mu={}
    for q,(ah,al) in outside.items():
        mu[q]=ah/(ah+al)
        entry[q]=F(1) if mu[q]>=a['tau'] else RHO
        extra=chi*RHO if q==1 else (chi*(1-RHO) if q==-1 else F(0))
        valextra=a['t0']+a['w'] if q==1 else a['t0']
        price[q]=(ah*(a['t0']+entry[q]*a['wh'])+al*(a['t0']+entry[q]*a['wl'])+extra*valextra)/(ah+al+extra)
    show('chi',chi);show('s',s);show('t',t)
    print('outside posterior',{q:str(v) for q,v in mu.items()})
    print('outside entry',{q:str(v) for q,v in entry.items()})
    print('prices',{q:str(v) for q,v in price.items()})
    for label,w in [('H',a['wh']),('L',a['wl'])]:
        print(label+' net payoffs',{q:str(q*(a['t0']+entry[q]*w-price[q])-K*abs(q)) for q in (-1,0,1)})
    for label,v in [('low-cost',a['t0']+a['w']),('high-cost',a['t0'])]:
        print(label+' net trade payoffs',{q:str(q*(v-price[q])-K*abs(q)) for q in (-1,0,1)})
    show('total entry',chi*RHO+sum((ah+al)*entry[q] for q,(ah,al) in outside.items()))


def challenger_refinement():
    print('CHALLENGER: AN INTERIOR INFORMED RATE BEFORE THE PURE THRESHOLD')
    a=auction(F(3));vh=a['t0']+RHO*a['wh'];vl=a['t0']+RHO*a['wl']
    vu=a['t0']+RHO*a['w'];vc=a['t0']+a['w']
    sstar=B*(2*a['tau']-1)/(L*(1-a['tau']))
    onset=(B*(vh-vu-K)-K*L*sstar/2)/(RHO*(vc-vh+K))
    show('earlier presence threshold',onset)
    show('recruitment threshold rate',sstar)
    chi=F(9,100)
    s=2*(B*(vh-vu-K)-chi*RHO*(vc-vh+K))/(K*L)
    t=min(F(1),2*(B*(vu-vl-K)-chi*(1-RHO)*(vl+K-a['t0']))/(L*K))
    challenger_profile(chi,s,t)
    print('DISCOVERY EQUILIBRIUM AT THE SAME PRESENCE')
    # On this branch the low-cost challenger waits, and the high-cost challenger sells.
    wait=1-L-chi-2*B
    muplus=(L+B)/(L+2*B)
    eplus=F(1)
    pplus=a['t0']+a['wl']+a['d']*muplus
    pminus=(L*t*(a['t0']+RHO*a['wl'])/2+B*vu+chi*(1-RHO)*a['t0'])/(L*t/2+B+chi*(1-RHO))
    pzero=(wait*vu+chi*RHO*vc)/(wait+chi*RHO)
    print('prices',{q:str(v) for q,v in {-1:pminus,0:pzero,1:pplus}.items()})
    show('H purchase net',a['t0']+a['wh']-pplus-K)
    show('L sale net',pminus-a['t0']-RHO*a['wl']-K)
    show('low-cost purchase net',vc-pplus-K)
    show('high-cost sale net',pminus-a['t0']-K)


def incumbent_refinement():
    print('\nINCUMBENT: A STRICT COUNTEREXAMPLE BELOW THE REPORTED PRESENCE')
    a=auction(F(3));chi=F(3,50);ih=L/2;mass=ih+B
    vh=a['t0']+RHO*a['wh'];vl=a['t0']+RHO*a['wl'];vu=a['t0']+RHO*a['w']
    def buyprice(d):
        return (ih*vh+B*vu+chi*(3-d)*(F(1,2)+(3+d)/16)/3)/(mass+chi*(3-d)/3)
    dl,dh=bisect_fraction(lambda d:F(1,2)+d/8-buyprice(d)-K,F(1),F(2),100)
    def sellint(s):
        return RHO*P*P+integral_linear(P,s,F(3,8),RHO)
    def sellprice(s):
        return (ih*vl+B*vu+chi*sellint(s)/3)/(mass+chi*s/3)
    sl,sh=bisect_fraction(lambda s:F(3,8)+s/4-sellprice(s)+K,P,F(1),100)
    def gross(d):
        return (ih*a['gh']+B*(a['gh']+a['gl'])/2+chi*(3-d)*(17-d)/12)/(mass+chi*(3-d)/3)
    for label,value in [('chi',chi),('buy cutoff lower',dl),('buy cutoff upper',dh),
                        ('sale cutoff lower',sl),('sale cutoff upper',sh),
                        ('gross preparation minus 6 at lower cutoff',gross(dl)-6),
                        ('gross preparation minus 6 at upper cutoff',gross(dh)-6)]: show(label,value)
    d=(dl+dh)/2;s=(sl+sh)/2
    pwait=((C-chi)*vu+chi*integral_linear(s,F(1),F(3,8),RHO)/3
           +chi*integral_linear(F(1),d,F(1,2),F(1,8))/3)/((C-chi)+chi*(d-s)/3)
    show('sell price',sellprice(s));show('wait price',pwait);show('buy price',buyprice(d))
    show('H purchase net',vh-buyprice(d)-K)
    show('L sale net',sellprice(s)-vl-K)
    # Give compact, decimal-rational brackets with exact endpoint signs.
    for label,fn,lo,hi in [
        ('liquidity lower endpoint',lambda r:liq_boundary(r,RHO),F('3.11059926916'),F('3.11059926918')),
        ('liquidity upper endpoint',lambda r:liq_boundary(r,F(1)),F('3.78385486063'),F('3.78385486064')),
    ]:
        show(label+' lower',lo);show(label+' upper',hi)
        show(label+' lower sign',F(1) if fn(lo)>0 else F(-1))
        show(label+' upper sign',F(1) if fn(hi)>0 else F(-1))


def liq_boundary(r,e):
    a=auction(r);bh=(1-L)*F(2,5);vm=F(51,50)
    b=L*(1-a['tau'])/(2*a['tau']-1)
    return 2*b*b+(L-2*bh*(1-K/vm))*b-bh*(1-K/vm)*L+bh*e*a['d']*L/(2*vm)


challenger_refinement()
incumbent_refinement()
