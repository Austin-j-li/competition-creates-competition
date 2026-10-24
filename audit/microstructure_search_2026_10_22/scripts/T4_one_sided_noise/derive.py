"""Print exact benchmark evaluations and 40-digit evaluations of closed forms."""
from fractions import Fraction as F
import mpmath as mp
from math import factorial

mp.mp.dps = 40
RHO, K = F(1, 4), F(1, 50)
ROOT_TOL = mp.mpf('1e-32')


def auction(r):
    t0 = F(1, 2) - F(1, 4) / r
    th = r / 2 + F(1, 8) / r
    tl = 1 - F(3, 8) / r
    gh, gl = 10 - th, 1 - tl
    delta = th - tl
    tau = (6 - gl) / (gh - gl)
    return t0, th, tl, gh, gl, delta, tau


def number(x):
    if isinstance(x, F):
        return mp.mpf(x.numerator) / x.denominator
    return x


def show(label, x):
    exact = str(x) if isinstance(x, F) else ''
    print(label, exact, mp.nstr(number(x), 23))


def rational_bracket(fn, lo, hi):
    for _ in range(110):
        mid = (lo + hi) / 2
        if fn(mid) > 0:
            hi = mid
        else:
            lo = mid
    print('bracket endpoints:', lo, hi)
    print('endpoint values:', fn(lo), fn(hi))
    print('decimal bracket:', mp.nstr(number(lo), 30), mp.nstr(number(hi), 30))


def inverse_delta(d):
    d = number(d)
    return 1 + d + mp.sqrt(d*d + 2*d)


def calculate(a, label):
    print('\nCALIBRATION', label)
    m = 1 / (1 + a)
    show('a', a)
    show('M', m)
    for r in [F(6, 5), F(31, 20), F(8, 5), F(33, 20), F(3), F(18, 5)]:
        t0, th, tl, gh, gl, d, tau = auction(r)
        print('\nr =', r)
        show('tau', tau)
        show('NT buy gross', RHO*d/2)
        show('full buy gross, entry floor', RHO*d*(1-m))
        show('full buy gross, recruited', d*(1-m))
        show('ceiling margin B(M)-6', gl+m*(gh-gl)-6)
        ss = a*(2*tau-1)/((1-a)*(1-tau))
        es = K/(d*(1-tau))
        ns = a+(1-a)*ss/2
        show('D1 threshold purchase probability', ss)
        show('D1 threshold total entry', RHO+(es-RHO)*ns)
        show('D1 threshold upper entry', es)
        sd = (2-1/tau)/(1-a)
        ed = K/(a*d*tau)
        show('D3 threshold sale probability', sd)
        show('D3 threshold total entry', RHO+(ed-RHO)/(2*tau))
        show('D3 threshold upper entry', ed)
    r = F(3)
    t0, th, tl, gh, gl, d, tau = auction(r)
    n = (1+a)/2
    entry = RHO+(1-RHO)*n
    dr = (1-RHO)/2*((th-t0)+a*(tl-t0))
    dw = (1-RHO)*n*(gl+m*(gh-gl)-6+F(1, 12))
    print('\nOUTCOMES at r=3')
    show('entry', entry)
    show('high ownership', F(1, 2))
    show('target proceeds gain', dr)
    show('net surplus gain', dw)
    show('target proceeds level', t0+((th-t0)+(RHO+(1-RHO)*a)*(tl-t0))/2)
    show('B2 full recruited gross coefficient', m*(1-m)*(1+RHO))
    show('B2 full hidden gross coefficient', 2*RHO*m*(1-m))
    show('B2 entry', F(5, 8))
    show('B2 ownership', (RHO+(1-RHO)*m)/2)
    show('D1 full coexistence start', inverse_delta(K/(1-m)))
    show('D1 NT end', inverse_delta(2*K/RHO))
    show('D3 NT end with posterior zero', inverse_delta(2*K/(RHO*a)))
    show('B2 full coexistence start', inverse_delta(K/(m*(1-m)*(1+RHO))))
    aa = number(a)
    mm = number(m)
    r_a = mp.findroot(lambda rr: auction(rr)[5]*(1-auction(rr)[6])-number(K), (mp.mpf('1.3'),mp.mpf('1.5')), tol=ROOT_TOL)
    r_b = mp.findroot(lambda rr: aa*auction(rr)[5]*auction(rr)[6]-number(K), (mp.mpf('1.3'),mp.mpf('1.6')), tol=ROOT_TOL)
    r_c = mp.findroot(lambda rr: auction(rr)[4]+mm*(auction(rr)[3]-auction(rr)[4])-6, (3,4), tol=ROOT_TOL)
    for lab, val in [('D1 first informative r_A',r_a),('D3 threshold switch r_B',r_b),('ceiling r_C',r_c)]:
        show(lab,val)
    show('r_A residual',auction(r_a)[5]*(1-auction(r_a)[6])-number(K))
    show('r_C residual',auction(r_c)[4]+mm*(auction(r_c)[3]-auction(r_c)[4])-6)


print('Precision: 40 decimal digits. Root tolerance: 1e-32. Display: 23 significant digits.')
lo = 1/auction(F(18,5))[6]-1
hi = 1/auction(F(3))[6]-1
exp_lower = sum((F(1, factorial(n)) for n in range(13)), F(0))
exp_upper = exp_lower + F(14, 13*factorial(13))
show('exact exp(-1) lower bound minus strip lower endpoint',1/exp_upper-lo)
show('strip upper endpoint minus exact exp(-1) upper bound',hi-1/exp_lower)
show('open lower a',lo)
show('upper a, included only with preparation at equality',hi)
show('D2 lower rate',-mp.log(number(hi)))
show('D2 upper rate',-mp.log(number(lo)))
show('mean G lower limit',lo/(1-lo))
show('mean G upper limit',hi/(1-hi))
calculate(F(11,29),'rational match to V3')
calculate(mp.exp(-1),'paper ceiling match')
print('\nEXACT V3 MATCH')
b, lam = F(11,51), F(6,17)
a = b/(b+lam)
show('a',a)
show('upper signal mass ratio D1/V3',1/(b+lam))
show('V3 entry',RHO+(1-RHO)*(b+lam/2))
show('V3 ownership',(RHO+(1-RHO)*(b+lam))/2)
print('\nEXACT ROOT BRACKETS')
print('r_A')
rational_bracket(lambda r: auction(r)[5]*(1-auction(r)[6])-K,F(13,10),F(3,2))
print('r_F, a=11/29')
rational_bracket(lambda r: auction(r)[5]*F(11,40)-K,F(7,5),F(3,2))
print('r_N')
rational_bracket(lambda r: RHO*auction(r)[5]/2-K,F(17,10),F(9,5))
print('r_C, a=11/29; sign reversed')
rational_bracket(lambda r: 6-auction(r)[4]-F(29,40)*(auction(r)[3]-auction(r)[4]),F(3),F(18,5))
print('\nPURE AND MIXED D1 BELIEFS, a=11/29')
for sh, sl in [(F(0),F(0)),(F(1),F(0)),(F(0),F(1)),(F(1),F(1)),(F(2,5),F(1,3))]:
    bh, bl = a+(1-a)*sh, a+(1-a)*sl
    low = (1-sh)/(2-sh-sl) if sh+sl != 2 else 'unused'
    print('purchase rates',sh,sl,'low posterior',low,'upper posterior',bh/(bh+bl))
print('\nEXACT BENCHMARK SIGN MARGINS, WHOLE STRIP')
show('weak universal exclusion k-Delta',K-auction(F(6,5))[5])
show('strong lower payoff margin',RHO*auction(F(3))[5]*(1-auction(F(18,5))[6])-K)
show('very strong lower payoff margin',RHO*auction(F(18,5))[5]*(1-auction(F(18,5))[6])-K)
show('full informative margin at 1.55',auction(F(31,20))[5]*(1-auction(F(18,5))[6])-K)
for r in [F(31,20),F(8,5),F(33,20)]:
    d,tau=auction(r)[5:]
    show('D1 CM entry coefficient at '+str(r),K/(2*d*(1-tau)**2)-RHO/(2*(1-tau)))
    show('D3 CM entry coefficient on 1/a at '+str(r),K/(2*d*tau*tau))
    show('D3 CM entry constant at '+str(r),RHO-RHO/(2*tau))
print('\nD3 WHOLE-STRIP MARGINS')
show('strong floor return margin',RHO*lo*auction(F(3))[5]/2-K)
show('very strong floor return margin',RHO*lo*auction(F(18,5))[5]/2-K)
show('D3 threshold jump margin at 1.55',lo*auction(F(31,20))[5]*auction(F(31,20))[6]-K)
show('D3 unrecruited full-return exclusion at 1.65',K-RHO*auction(F(33,20))[5]*hi/(1+hi))
d,tau=auction(F(31,20))[5:]
show('D3 full entry minus threshold entry, worst endpoint at 1.55',(1-RHO)*(1+lo)/2-(K/(lo*d*tau)-RHO)/(2*tau))
rs = [F(31,20),F(8,5),F(33,20)]
for r, rr in zip(rs,rs[1:]):
    d,tau=auction(r)[5:]
    dd,tt=auction(rr)[5:]
    show('D1 CM entry drop divided by a '+str(r),K/(2*d*(1-tau)**2)-RHO/(2*(1-tau))-K/(2*dd*(1-tt)**2)+RHO/(2*(1-tt)))
    show('D3 CM entry drop lower bound '+str(r),K/(2*hi*d*tau*tau)-RHO/(2*tau)-K/(2*hi*dd*tt*tt)+RHO/(2*tt))
