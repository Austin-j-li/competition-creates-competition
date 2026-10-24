"""Exact derivative signs from independent polynomial formulas; print a certificate."""
from fractions import Fraction as Q
from functools import reduce
from math import gcd, lcm
from pathlib import Path

HERE = Path(__file__).resolve().parent


def trim(p):
    p = list(map(Q,p))
    while len(p)>1 and p[-1]==0:
        p.pop()
    return p


def add(a,b):
    return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])


def neg(a):
    return [-x for x in a]


def mul(a,b):
    c=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            c[i+j]+=x*y
    return trim(c)


def derivative(a):
    return trim([i*a[i] for i in range(1,len(a))] or [0])


def remainder(a,b):
    a=trim(a)
    while len(a)>=len(b) and a!=[0]:
        n=len(a)-len(b)
        ratio=a[-1]/b[-1]
        a=add(a,[0]*n+[-ratio*x for x in b])
    return a


def eval_poly(a,x):
    total=Q(0)
    for coefficient in reversed(a):
        total=total*x+coefficient
    return total


def integers(a):
    den=lcm(*(x.denominator for x in a))
    numbers=[int(x*den) for x in a]
    common=reduce(gcd,map(abs,numbers))
    return [Q(x//common) for x in numbers]


def chain(a):
    seq=[trim(a),derivative(a)]
    while seq[-1]!=[0]:
        tail=remainder(seq[-2],seq[-1])
        if tail==[0]:
            break
        seq.append(integers(neg(tail)))
    return seq


def variations(a,x):
    signs=[(eval_poly(p,x)>0)-(eval_poly(p,x)<0) for p in chain(a)]
    signs=[s for s in signs if s]
    return sum(a!=b for a,b in zip(signs,signs[1:])),signs


def qprime(num,den):
    return integers(add(mul(derivative(num),den),neg(mul(num,derivative(den)))))


def main():
    lines=[]
    def say(x):
        print(x)
        lines.append(str(x))
    # D=(r-1)^2/(2r), tau=(48r-3)/(4(-r^2+20r-1)).
    dn,dd=[1,-2,1],[0,2]
    tn,td=[-3,48],[-4,80,-4]
    nn=add(td,neg(tn))
    jn,jd=mul(dn,nn),mul(dd,td)
    sn,sd=mul(dn,mul(nn,nn)),mul(dd,mul(td,td))
    cases=[("tau",qprime(tn,td),Q(6,5),Q(18,5)),
        ("J",qprime(jn,jd),Q(6,5),Q(18,5)),
        ("D*(1-tau)^2",qprime(sn,sd),Q(6,5),Q(2)),
        ("D*tau",qprime(mul(dn,tn),mul(dd,td)),Q(6,5),Q(18,5)),
        ("tau denominator",list(map(Q,td)),Q(6,5),Q(18,5)),
        ("1-tau numerator",list(map(Q,nn)),Q(6,5),Q(18,5))]
    for label,p,lo,hi in cases:
        vl,sl=variations(p,lo)
        vh,sh=variations(p,hi)
        say(f"{label}: primitive integer coefficients, ascending = {list(map(str,p))}")
        say(f"  endpoint values: {eval_poly(p,lo)}, {eval_poly(p,hi)}")
        say(f"  Sturm signs at {lo}: {sl}; at {hi}: {sh}")
        say(f"  variations {vl},{vh}; root count {vl-vh}; left sign {(eval_poly(p,lo)>0)-(eval_poly(p,lo)<0)}")
    (HERE/"xp1_signs.log").write_text("\n".join(lines)+"\n")


if __name__=="__main__":
    main()
