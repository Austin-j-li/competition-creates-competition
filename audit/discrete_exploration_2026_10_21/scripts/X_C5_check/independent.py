from fractions import Fraction as F
from decimal import Decimal, localcontext
from typing import Callable


class Interval:
    def __init__(self, low: F | int, high: F | int | None = None) -> None:
        self.low = F(low)
        self.high = self.low if high is None else F(high)

    def __add__(self, other: 'Interval | F | int') -> 'Interval':
        other = interval(other)
        return Interval(self.low + other.low, self.high + other.high)

    __radd__ = __add__

    def __neg__(self) -> 'Interval':
        return Interval(-self.high, -self.low)

    def __sub__(self, other: 'Interval | F | int') -> 'Interval':
        return self + -interval(other)

    def __rsub__(self, other: 'Interval | F | int') -> 'Interval':
        return interval(other) + -self

    def __mul__(self, other: 'Interval | F | int') -> 'Interval':
        other = interval(other)
        values = [self.low * other.low, self.low * other.high,
                  self.high * other.low, self.high * other.high]
        return Interval(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, other: 'Interval | F | int') -> 'Interval':
        other = interval(other)
        if other.low <= 0 <= other.high:
            raise ValueError('A denominator contains zero.')
        return self * Interval(1 / other.high, 1 / other.low)

    def __rtruediv__(self, other: 'Interval | F | int') -> 'Interval':
        return interval(other) / self

    def __pow__(self, power: int) -> 'Interval':
        result = Interval(1)
        for _ in range(power):
            result = result * self
        return result


def interval(value: Interval | F | int) -> Interval:
    return value if isinstance(value, Interval) else Interval(value)


def decimal(value: F | int, digits: int = 14) -> str:
    value = F(value)
    with localcontext() as context:
        context.prec = 85
        return f'{Decimal(value.numerator) / Decimal(value.denominator):.{digits}f}'


def outward(value: F | int, upper: bool = False, digits: int = 25) -> str:
    value = F(value)
    scale = 10**digits
    integer = -((-value.numerator*scale)//value.denominator) if upper else value.numerator*scale//value.denominator
    return decimal(F(integer,scale),digits)


def scientific(value: F | int) -> str:
    value = F(value)
    with localcontext() as context:
        context.prec = 15
        return f'{Decimal(value.numerator)/Decimal(value.denominator):.6E}'


def display(name: str, value: Interval | F | int) -> None:
    if isinstance(value, Interval):
        print(name, '[' + outward(value.low) + ', ' + outward(value.high,True) + ']',
              'sign=' + str(sign(value)), 'width=' + scientific(value.high-value.low))
    else:
        print(name, str(value), decimal(value))


def auction(r: F | int, cost: F = F(6)) -> dict[str,F]:
    r = F(r)
    p, ell, h = F(1, 2), F(1), F(10)
    t0 = p * (1 - p / r)
    th = r / 2 + p * p / (2 * r)
    tl = ell - (ell * ell - p * p) / (2 * r)
    gh = h - th
    gl = (ell * ell - p * p) / (2 * r)
    a0 = (r * r - p * p) / (2 * r)
    return dict(r=r, cost=cost, t0=t0, wh=th-t0, wl=tl-t0, d=th-tl,
                gh=gh, gl=gl, tau=(cost-gl)/(gh-gl), a0=a0,
                ah=h-a0, al=(ell*ell+p*p)/(2*r), i0=(r-p)**2/(2*r))


RHO, K = F(1, 4), F(1, 50)


def ledger(p: dict[str,F], bh: F | Interval, bl: F | Interval,
           eh: F | Interval, el: F | Interval, tradeh: F | Interval,
           tradel: F | Interval) -> dict[str,F | Interval]:
    entry = (eh + el) / 2
    target = p['t0'] + (eh*p['wh'] + el*p['wl'])/2
    preparation = p['cost'] * (entry-RHO)
    challenger = (eh*p['gh'] + el*p['gl'])/2-preparation
    incumbent = p['i0'] + (eh*(p['ah']-p['wh']-p['gh'])
                           + el*(p['al']-p['wl']-p['gl']))/2
    allocation = p['a0'] + (eh*p['ah']+el*p['al'])/2
    expense = K*(bh+bl)/2
    gross = (bh*tradeh+bl*tradel)/2
    return dict(E=entry, OH=eh/2, T=target, C=challenger, R=incumbent,
                noise=gross, investor_trade=gross-expense,
                surplus=allocation-preparation-expense,
                accounting_residual=target+challenger+incumbent-allocation+preparation)


def three(p: dict[str,F], bh: F | int, bl: F | int, omega: F | int,
          topbelief: F = F(1), topentry: F | None = None,
          hidden: bool = False) -> tuple[list[F],dict[str,F | Interval]]:
    bh, bl, omega = F(bh), F(bl), F(omega)
    flows = (-1, 0, 1, 2)
    ph = {x: sum((1-bh if x == z else F(0)) + (bh if x == z+1 else F(0))
                 for z in (-1, 0, 1))/3 for x in flows}
    pl = {x: sum((1-bl if x == z else F(0)) + (bl if x == z+1 else F(0))
                 for z in (-1, 0, 1))/3 for x in flows}
    mu, entry, price = {}, {}, {}
    for x in flows:
        mu[x] = ph[x]/(ph[x]+pl[x]) if ph[x]+pl[x] else (topbelief if x == 2 else F(0))
        entry[x] = RHO if hidden or mu[x] < p['tau'] else F(1)
        if x == 2 and topentry is not None:
            entry[x] = topentry
        price[x] = p['t0']+entry[x]*(p['wl']+p['d']*mu[x])
    gains, trade = [], []
    for w in (p['wh'], p['wl']):
        values = {x:p['t0']+entry[x]*w for x in flows}
        u0 = omega*sum(values[z] for z in (-1, 0, 1))/3
        u1 = sum((omega+1)*values[z+1]-price[z+1] for z in (-1, 0, 1))/3-K
        gains.append(u1-u0)
        trade.append(sum(values[z+1]-price[z+1] for z in (-1, 0, 1))/3)
    eh = sum(ph[x]*entry[x] for x in flows)
    el = sum(pl[x]*entry[x] for x in flows)
    outcomes = ledger(p, bh, bl, eh, el, *trade)
    return gains, outcomes


def three_bounds(p: dict[str,F]) -> tuple[F,F,F,F]:
    g0 = three(p, 1, 0, 0)[0]
    g1 = three(p, 1, 0, 1)[0]
    onset = -g0[0]/(g1[0]-g0[0])
    upper = -g0[1]/(g1[1]-g0[1])
    beta = 1/p['tau']-1
    lo = three(p, 1, beta, 0)[0][1]
    hi = three(p, 1, beta, 1)[0][1]
    lower = -lo/(hi-lo)
    return onset, lower, upper, beta


def three_rows(p: dict[str,F], omega: F) -> list[tuple]:
    onset, lower, upper, cap = three_bounds(p)
    rows = []
    for name, bh, bl, e in [('NT',F(0),F(0),None),('S',F(1),F(0),None)]:
        gains, values = three(p,bh,bl,omega)
        suitable = all(g <= 0 if b == 0 else g >= 0 for g,b in zip(gains,(bh,bl)))
        if suitable:
            rows.append((name,bh,bl,e,gains,values))
    if omega == onset:
        bh = F(1,2)
        gains, values = three(p,bh,0,omega)
        rows.append(('Hm example',bh,F(0),None,gains,values))
    if lower <= omega <= upper:
        posterior = (omega*p['wl']*(1-RHO)-RHO*p['d']-3*K)/p['d']
        bl = 1/posterior-1
        if 0 < bl <= cap:
            gains, values = three(p,1,bl,omega)
            rows.append(('M',F(1),bl,F(1),gains,values))
    if omega >= lower:
        gfloor = three(p,1,cap,omega,topentry=RHO)[0][1]
        gfull = three(p,1,cap,omega,topentry=F(1))[0][1]
        e = RHO-(1-RHO)*gfloor/(gfull-gfloor)
        gains, values = three(p,1,cap,omega,topentry=e)
        rows.append(('Mprime',F(1),cap,e,gains,values))
    return rows


def exp_bounds() -> Interval:
    term, partial = F(1), F(1)
    even, odd = None, None
    for n in range(1, 62):
        term *= -F(1, 2*n)
        partial += term
        if n % 2:
            odd = partial
        else:
            even = partial
    return Interval(odd, even)


A = exp_bounds()
Q0, Q1 = A/(1+A), 1/(1+A)
SHIFT = Q1-Q0


def dl(p: dict[str,F], bh: Interval | F | int, bl: Interval | F | int,
       omega: Interval | F | int, e_good: Interval | F | int,
       e_bad: F = RHO) -> tuple[list[Interval],dict[str,F | Interval],Interval,Interval]:
    bh, bl, omega = interval(bh), interval(bl), interval(omega)
    ph = Q0+SHIFT*bh
    pl = Q0+SHIFT*bl
    good = ph/(ph+pl)
    bad = (1-ph)/(2-ph-pl)
    e_good, e_bad = interval(e_good), interval(e_bad)
    gains, trade = [], []
    for w in (p['wh'],p['wl']):
        vg = p['t0']+e_good*w
        vb = p['t0']+e_bad*w
        pg = p['t0']+e_good*(p['wl']+p['d']*good)
        pb = p['t0']+e_bad*(p['wl']+p['d']*bad)
        u0 = omega*(Q0*vg+Q1*vb)
        u1 = (omega+1)*(Q1*vg+Q0*vb)-(Q1*pg+Q0*pb)-K
        gains.append(u1-u0)
        trade.append(Q1*(vg-pg)+Q0*(vb-pb))
    eh = e_bad+(e_good-e_bad)*ph
    el = e_bad+(e_good-e_bad)*pl
    return gains, ledger(p,bh,bl,eh,el,*trade), good, bad


def sign(value: Interval | F | int) -> int:
    value = interval(value)
    return 1 if value.low > 0 else -1 if value.high < 0 else 0


def root_bracket(function: Callable[[F],Interval], left: F, right: F,
                 count: int = 75) -> tuple[Interval,Interval,Interval]:
    left, right = F(left), F(right)
    sleft = sign(function(left))
    for _ in range(count):
        mid = (left+right)/2
        smid = sign(function(mid))
        if smid == 0:
            break
        if smid == sleft:
            left = mid
        else:
            right = mid
    return Interval(left,right), function(left), function(right)


def dl_bounds(p: dict[str,F]) -> tuple[Interval,Interval,Interval,Interval,Interval,Interval]:
    cap = (Q1/p['tau']-1)/SHIFT
    threshold = Q0*(2*p['tau']-1)/((1-p['tau'])*SHIFT)
    zero, one = dl(p,1,0,0,1)[0], dl(p,1,0,1,1)[0]
    onset = -zero[0]/(one[0]-zero[0])
    upper = -zero[1]/(one[1]-zero[1])
    lo = dl(p,1,cap,0,1)[0][1]
    hi = dl(p,1,cap,1,1)[0][1]
    lower = -lo/(hi-lo)
    lo = dl(p,threshold,0,0,1)[0][0]
    hi = dl(p,threshold,0,1,1)[0][0]
    first = -lo/(hi-lo)
    return first,onset,lower,upper,cap,threshold


def dl_mprime(p: dict[str,F], omega: F, cap: Interval) -> Interval:
    gf = dl(p,1,cap,omega,RHO)[0][1]
    gg = dl(p,1,cap,omega,1)[0][1]
    return RHO-(1-RHO)*gf/(gg-gf)


def dl_hthreshold(p: dict[str,F], omega: F, bh: Interval) -> Interval:
    gf = dl(p,bh,0,omega,RHO)[0][0]
    gg = dl(p,bh,0,omega,1)[0][0]
    return RHO-(1-RHO)*gf/(gg-gf)


def main() -> None:
    print('INDEPENDENT THREE-POINT CALCULATION')
    for r in (F(6,5),F(3)):
        p = auction(r)
        print('r=',r)
        for name in ('d','wh','wl','tau'):
            display(name,p[name])
        onset,lower,upper,cap = three_bounds(p)
        for name,value in zip(('onset','lower','upper','cap'),(onset,lower,upper,cap)):
            display(name,value)
        for omega in (F(1,10),onset,lower,F(23,10),upper,F(3),F(10),F(100)):
            if omega < 0:
                continue
            print('stake=',omega)
            for name,bh,bl,e,gains,values in three_rows(p,omega):
                print(name,'bh=',bh,'bl=',bl,'e_top=',e,'gains=',[str(x) for x in gains])
                for key in ('E','OH','T','C','surplus'):
                    display(key,values[key])
        print('No-trade belief comparison')
        for omega in (F(1,10),F(1,5),F(1,3)):
            for belief in (F(1,2),p['tau'],F(1)):
                gains = three(p,0,0,omega,topbelief=belief)[0]
                print('stake=',omega,'top_belief=',belief,'gains=',[str(x) for x in gains])

    p = auction(3)
    lower = three_bounds(p)[1]
    rows = three_rows(p,lower)
    selected = {name:values for name,bh,bl,e,g,values in rows}
    hidden = three(p,1,0,0,hidden=True)[1]
    print('THREE-POINT WELFARE')
    for name,values in [('hidden',hidden),('S',selected['S']),('M_at_lower',selected['M'])]:
        print(name)
        for key,value in values.items():
            display(key,value)
    print('Changes: M minus S')
    for key in ('E','T','C','R','noise','investor_trade','surplus'):
        display(key,selected['M'][key]-selected['S'][key])
    display('target_gain_divided_by_challenger_loss',
            (selected['M']['T']-selected['S']['T'])/(selected['S']['C']-selected['M']['C']))
    display('fraction_of_information_surplus_lost',
            (selected['S']['surplus']-selected['M']['surplus'])/
            (selected['S']['surplus']-hidden['surplus']))
    for omega in (F(21,10),F(23,10),F(5,2)):
        for name,bh,bl,e,g,values in three_rows(p,omega):
            if name == 'M':
                print('Interior M stake=',omega)
                display('C_minus_hidden',values['C']-hidden['C'])
    print('Return economy: r=9')
    p = auction(9)
    for omega in (F(0),F(1000)):
        print('stake=',omega,'gains_S=',[str(x) for x in three(p,1,0,omega)[0]])

    print('INDEPENDENT DISCRETE-LAPLACE ENCLOSURES')
    print('Exact lower bound for a:',A.low)
    print('Exact upper bound for a:',A.high)
    display('a',A)
    display('q0',Q0)
    display('q1',Q1)
    for r in (F(6,5),F(3)):
        p = auction(r,F(5))
        first,onset,lower,upper,cap,threshold = dl_bounds(p)
        print('r=',r)
        for name,value in zip(('first','onset','lower','upper','cap','h_threshold'),
                              (first,onset,lower,upper,cap,threshold)):
            display(name,value)
        if r == F(6,5):
            for omega in (F(19,100),F(9,25)):
                print('stake=',omega)
                schedules = [('NT',F(0),F(0),RHO),
                             ('Hth',threshold,F(0),dl_hthreshold(p,omega,threshold))]
                if omega == F(9,25):
                    schedules += [('S',F(1),F(0),F(1)),
                                  ('Mprime',F(1),cap,dl_mprime(p,omega,cap))]
                for name,bh,bl,e in schedules:
                    print(name)
                    gains,values,good,bad = dl(p,bh,bl,omega,e)
                    for key,value in [('bh',interval(bh)),('bl',interval(bl)),('e',interval(e)),
                                      ('GH',gains[0]),('GL',gains[1]),('M',good),('m',bad)]:
                        display(key,value)
                    for key in ('E','OH','T','C','surplus'):
                        display(key,values[key])
                if omega == F(19,100):
                    root,gl,gr = root_bracket(lambda b:dl(p,b,0,omega,1)[0][0],
                                              threshold.high,F(1))
                    display('Hm_root',root)
                    display('Hm_left_gain',gl)
                    display('Hm_right_gain',gr)
                    print('Hm exact root bracket:',root.low,root.high)
                if omega == F(9,25):
                    root,gl,gr = root_bracket(lambda b:dl(p,1,b,omega,1)[0][1],F(0),cap.low)
                    display('M_root',root)
                    display('M_left_gain',gl)
                    display('M_right_gain',gr)
                    print('M exact root bracket:',root.low,root.high)
                    gains,values,good,bad = dl(p,1,root,omega,1)
                    display('M_GH',gains[0])
                    for key in ('E','OH','T','C','surplus'):
                        display('M_'+key,values[key])
            kreg = dl(p,threshold,0,0,RHO)[0][0]+K
            bad = dl(p,threshold,0,0,RHO)[3]
            bound = p['wl']/p['wh']*(K-kreg)-p['d']*RHO*(Q1*p['tau']+Q0*bad)-K
            display('K_minus_KI',K-kreg)
            display('all_stakes_L_upper_bound',bound)
        else:
            for name,omega,bh,bl,e in [('S',F(0),F(1),F(0),F(1)),
                    ('Mprime_3.5',F(7,2),F(1),cap,dl_mprime(p,F(7,2),cap)),
                    ('Mprime_100',F(100),F(1),cap,dl_mprime(p,F(100),cap))]:
                print(name)
                gains,values,good,bad = dl(p,bh,bl,omega,e)
                for key in ('E','OH','T','C','surplus'):
                    display(key,values[key])
            root,gl,gr = root_bracket(lambda b:dl(p,1,b,F(7,2),1)[0][1],F(0),cap.low)
            display('M_3.5_root',root)
            values = dl(p,1,root,F(7,2),1)[1]
            for key in ('E','OH','T','C','surplus'):
                display('M_3.5_'+key,values[key])
    print('Return economy: r=4')
    p = auction(4,F(5))
    display('best_B',p['gl']+Q1*(p['gh']-p['gl']))
    for omega in (F(0),F(1000)):
        gains = dl(p,1,0,omega,RHO)[0]
        for name,value in zip(('GH','GL'),gains):
            display(name,value)

    print('STRICT SIGN ENCLOSURES AT FIVE STAKES')
    for r,omega in ((F(6,5),F(9,50)),(F(6,5),F(9,25)),
                    (F(3),F(3)),(F(3),F(7,2)),(F(3),F(18,5))):
        p = auction(r,F(5))
        first,onset,lower,upper,cap,threshold = dl_bounds(p)
        nt = dl(p,0,0,omega,RHO)[0]
        sep = dl(p,1,0,omega,1)[0]
        lfloor = dl(p,1,cap,omega,RHO)[0]
        lfull = dl(p,1,cap,omega,1)[0]
        hfloor = dl(p,threshold,0,omega,RHO)[0]
        hfull = dl(p,threshold,0,omega,1)[0]
        print('r=',r,'stake=',omega)
        for name,value in [('NT_H',nt[0]),('NT_L',nt[1]),('S_H',sep[0]),('S_L',sep[1]),
                           ('Lcap_floor_H',lfloor[0]),('Lcap_floor_L',lfloor[1]),
                           ('Lcap_full_H',lfull[0]),('Lcap_full_L',lfull[1]),
                           ('Hthreshold_floor_H',hfloor[0]),('Hthreshold_floor_L',hfloor[1]),
                           ('Hthreshold_full_H',hfull[0]),('Hthreshold_full_L',hfull[1])]:
            print(name,'sign=',sign(value),'lower=',scientific(value.low),'upper=',scientific(value.high))


if __name__ == '__main__':
    main()
