"""Print endpoint certificates and domain examples for the independent derivation."""

from fractions import Fraction as F
import mpmath as mp
from independent import auction, gross, threshold, slot_rows, signal_margins, show, dec, laplace_entry_for_cost, inverse_spread, laplace_cost_mixture

mp.mp.dps=70


def polynomial_add(a,b):
    return [(a[i] if i<len(a) else F(0))+(b[i] if i<len(b) else F(0)) for i in range(max(len(a),len(b)))]


def polynomial_product(a,b):
    result=[F(0)]*(len(a)+len(b)-1)
    for i,v in enumerate(a):
        for j,w in enumerate(b):
            result[i+j]+=v*w
    return result


def derivative(a):
    return [i*a[i] for i in range(1,len(a))]


def at(a,x):
    return sum(v*x**i for i,v in enumerate(a))


def laplace_cost_closed(r):
    """Integrate the cost tails with elementary antiderivatives."""
    z=auction(r)
    lower,upper=1/(1+mp.e),mp.e/(1+mp.e)
    floor,ceiling=gross(r,lower),gross(r,upper)
    scale=z['gh']-z['gl']
    factor=mp.exp(-mp.mpf(1)/2)/2
    def primitive(cost,j):
        t=(cost-z['gl'])/scale
        angle=mp.asin(mp.sqrt(t))
        root=mp.sqrt(t*(1-t))
        return scale*(t-factor*(angle-root)) if j==0 else scale*factor*(angle+root)
    means=[]
    for lo,hi in ((mp.mpf(0),mp.mpf('0.2')),(mp.mpf('5.9'),mp.mpf('6.1'))):
        full=max(mp.mpf(0),min(hi,floor)-lo)
        left,right=max(lo,floor),min(hi,ceiling)
        means.append([(full+(primitive(right,j)-primitive(left,j) if right>left else 0))/(hi-lo) for j in (0,1)])
    eh=means[0][0]/4+3*means[1][0]/4
    el=means[0][1]/4+3*means[1][1]/4
    return (eh+el)/2,eh/2


def main():
    ah,al=laplace_entry_for_cost(mp.mpf(3),mp.mpf(6))
    bB=(ah+al)/(1+mp.e)
    lamB=(mp.e-1)*bB
    J=lambda r:auction(r)['D']*(1-threshold(r))
    rA=mp.findroot(lambda r:J(r)-mp.mpf('0.02'),(mp.mpf('1.3'),mp.mpf('1.5')))
    tauA=threshold(rA)
    # In y=r-1, J=N/D. Form its derivative by polynomial arithmetic.
    N=[F(0),F(0),F(27),F(24),F(-4)]
    D=[F(144),F(288),F(136),F(-8)]
    deriv_num=polynomial_add(polynomial_product(derivative(N),D),[-v for v in polynomial_product(N,derivative(D))])
    print('J derivative numerator in y ascending:',list(map(str,deriv_num)))
    print('Derivative positive-term constant after division by 8y:',deriv_num[1]/8)
    print('Only negative term absolute bound on 0<y<3/4:',show(abs(deriv_num[5])*F(3,4)**4/8))
    print('J(r) numerator at y=0:',N[0],'J(5/3)-k:',show(J(F(5,3))-F(1,50)))
    print('rA:',show(rA),'tauA:',show(tauA))
    # At the upper prior limit, pi=tau(rN(pi)) and rho*D*pi=k.
    rstar=mp.findroot(lambda r:auction(r)['D']*threshold(r)-mp.mpf('0.08'),(mp.mpf('1.5'),mp.mpf('1.8')))
    print('Global upper prior limit:',show(threshold(rstar)),'strength:',show(rstar))
    for tag,b,lam in (('A',F(11,51),F(6,17)),('B',bB,lamB)):
        u=dec(lam/b)
        pi_low=tauA/((1+u)*(1-tauA)+tauA)
        print('LOWER_BOUNDARY',tag,'pi_low:',show(pi_low),'M:',show(pi_low*(1+u)/(1+pi_low*u)),
              'no_trade_margin:',show(mp.mpf('0.02')-auction(rA)['D']*max(pi_low,1-pi_low)/4),
              'full_buy_margin:',show(auction(rA)['D']*(1-tauA)-mp.mpf('0.02')))
        # This prior lies above tau(rA), yet admits coexistence at r=3/2.
        pi,r=F(321,500),F(3,2)
        s=((1-pi)*b*auction(r)['D']/F(1,50)-b)/pi
        rows,E,O,UH,UL=slot_rows(r,b,lam,pi=pi,s=s,t=F(0))
        print('ABOVE_COMMON_ENDPOINT_DOMAIN',tag,'pi',pi,'r',r,'s',show(s),'lambda',show(lam),
              'entry',show(E),'no_trade_margin',show(F(1,50)-F(1,4)*auction(r)['D']*max(pi,1-pi)),
              'H_buy_net',show(UH[1]),'L_sell_net',show(UL[-1]),'tau_minus_prior',show(threshold(r)-pi))
        # The raw interval alone does not imply the entry formula outside its prior domain.
        pi,r=F(321,500),F(7,5)
        s=((1-pi)*b*auction(r)['D']/F(1,50)-b)/pi
        rows,E,O,UH,UL=slot_rows(r,b,lam,pi=pi,s=s,t=F(0))
        formula=F(1,4)+F(3,4)*(1-pi)*b*auction(r)['D']/F(1,50)
        print('MISSING_PRIOR_RESTRICTION',tag,'pi',pi,'r',r,'rA<r<rF',rA<dec(r)<inverse_spread(F(1,50)/(1-pi*(b+lam)/(b+pi*lam))),
              'direct_entry',show(E),'formula',show(formula),'difference',show(E-formula),'L_sell_net',show(UL[-1]))
        # A stronger weak-order bound proves uniqueness over the complete accuracy grid.
        M=(b+lam)/(2*b+lam)
        worst_weak=F(0)
        smallest_strong=None
        for ai in range(68,73):
            for di in range(73,78):
                a,d=F(ai,100),F(di,100)
                z=auction(F(11,10))
                upper=M*(2*a-1)*(z['D']+F(3,20)*(2*d-1)*z['wh'])
                worst_weak=max(worst_weak,upper)
                strong=signal_margins(b,lam,a,d)[3]
                smallest_strong=strong if smallest_strong is None else min(smallest_strong,strong)
        print('ALL_25_UNIQUENESS',tag,'weak_order_margin',show(F(3,200)-worst_weak),'strong_order_margin',show(smallest_strong))
    target=(mp.mpf('0.522757')-mp.mpf('0.25'))/mp.mpf('0.75')
    b_round=2*target/(1+mp.e)
    lam_round=(mp.e-1)*b_round
    exact_O=mp.mpf(1)/8+3*(bB+lamB)/8
    round_O=mp.mpf(1)/8+3*(b_round+lam_round)/8
    print('B_SIX_DIGIT_ENTRY_MATCH ownership:',show(round_O),'B_EXACT_MATCH ownership:',show(exact_O))
    print('Different six-decimal ownership displays:',f'{float(round_O):.6f}',f'{float(exact_O):.6f}')
    for r in (mp.mpf(3),mp.mpf('3.6')):
        E,O=laplace_cost_closed(r)
        Q,HO=laplace_cost_mixture(r)
        print('LAPLACE_COST_ANTIDERIVATIVE',r,'E',show(E),'O',show(O),'cost_quadrature_differences',show(E-Q),show(O-HO))


if __name__=='__main__':
    main()
